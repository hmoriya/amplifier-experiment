# 第21章　集約設計 ― 一貫性の境界

## はじめに：城壁の内側

中世の城塞都市は、強固な城壁によって外界から守られていました。城門は唯一の出入り口として厳重に管理され、城壁内の秩序と一貫性が保たれていました。ソフトウェアにおける「集約」も同じです。データの一貫性を保つための境界を定め、その内側の整合性を保証します。

本章では、Parasol V5.4の文脈で、効果的な集約設計の原則と実践的なテクニックを解説します。

## 集約設計の基本原則

### 集約とは何か

```typescript
export interface AggregateDesignPrinciples {
  // 単一の一貫性境界
  consistencyBoundary: {
    scope: "トランザクション境界と一致";
    rule: "1つのトランザクションで1つの集約のみを更新";
  };
  
  // 不変条件の強制
  invariants: {
    definition: "常に真でなければならないビジネスルール";
    enforcement: "集約ルートが責任を持つ";
  };
  
  // 小さな集約
  size: {
    guideline: "可能な限り小さく保つ";
    reason: "並行性とパフォーマンスの向上";
  };
  
  // ID による参照
  references: {
    rule: "他の集約はIDでのみ参照";
    benefit: "疎結合と独立した永続化";
  };
}

export abstract class AggregateRoot<T extends EntityId> extends Entity<T> {
  // 集約の境界を守る責任
  
  protected enforceInvariant(
    condition: boolean,
    message: string
  ): void {
    if (!condition) {
      throw new InvariantViolationError(message);
    }
  }
  
  // 子エンティティへの制御されたアクセス
  protected getChild<C extends Entity<any>>(
    children: C[],
    id: EntityId
  ): C | undefined {
    return children.find(child => child.getId().equals(id));
  }
  
  // 変更の追跡
  protected trackChange(event: DomainEvent): void {
    this.addDomainEvent(event);
    this.markAsModified();
  }
}
```

### 集約境界の発見

```typescript
export class AggregateBoundaryDiscovery {
  discoverBoundaries(
    domain: DomainModel
  ): AggregateBoundary[] {
    // 1. 不変条件の識別
    const invariants = this.identifyInvariants(domain);
    
    // 2. ライフサイクルの分析
    const lifecycles = this.analyzeLifecycles(domain);
    
    // 3. トランザクション要件の確認
    const transactionRequirements = this.analyzeTransactions(domain);
    
    // 4. 並行性の考慮
    const concurrencyNeeds = this.analyzeConcurrency(domain);
    
    // 5. 境界の定義
    return this.defineBoundaries(
      invariants,
      lifecycles,
      transactionRequirements,
      concurrencyNeeds
    );
  }
  
  private identifyInvariants(
    domain: DomainModel
  ): Invariant[] {
    const invariants: Invariant[] = [];
    
    // ビジネスルールから不変条件を抽出
    for (const rule of domain.businessRules) {
      if (this.isInvariant(rule)) {
        invariants.push({
          name: rule.name,
          description: rule.description,
          scope: this.determineScope(rule),
          enforcementStrategy: this.determineStrategy(rule)
        });
      }
    }
    
    return invariants;
  }
  
  private defineBoundaries(
    invariants: Invariant[],
    lifecycles: Lifecycle[],
    transactions: TransactionRequirement[],
    concurrency: ConcurrencyNeed[]
  ): AggregateBoundary[] {
    // 不変条件でグループ化
    const invariantGroups = this.groupByInvariantScope(invariants);
    
    // ライフサイクルで検証
    const lifecycleValidated = this.validateWithLifecycles(
      invariantGroups,
      lifecycles
    );
    
    // トランザクション境界で調整
    const transactionAligned = this.alignWithTransactions(
      lifecycleValidated,
      transactions
    );
    
    // 並行性を考慮して最適化
    return this.optimizeForConcurrency(
      transactionAligned,
      concurrency
    );
  }
}
```

## 実践的な集約設計パターン

### ショッピングカート集約の例

```typescript
// 集約ルート
export class ShoppingCart extends AggregateRoot<CartId> {
  private customerId: CustomerId;
  private items: CartItem[];
  private status: CartStatus;
  private createdAt: Date;
  private lastModifiedAt: Date;
  
  // プライベートコンストラクタ（ファクトリメソッド経由でのみ生成）
  private constructor(
    id: CartId,
    customerId: CustomerId
  ) {
    super(id);
    this.customerId = customerId;
    this.items = [];
    this.status = CartStatus.ACTIVE;
    this.createdAt = new Date();
    this.lastModifiedAt = new Date();
  }
  
  // ファクトリメソッド
  static create(customerId: CustomerId): ShoppingCart {
    const cart = new ShoppingCart(
      CartId.generate(),
      customerId
    );
    
    cart.trackChange(
      new ShoppingCartCreated(cart.id, customerId)
    );
    
    return cart;
  }
  
  // ビジネスメソッド（集約の境界を守る）
  addItem(
    productId: ProductId,
    quantity: number,
    price: Money
  ): Result<void> {
    // ステータスチェック
    if (this.status !== CartStatus.ACTIVE) {
      return Result.fail("Cannot add items to inactive cart");
    }
    
    // 数量の妥当性チェック
    if (quantity <= 0) {
      return Result.fail("Quantity must be positive");
    }
    
    // 最大アイテム数チェック（不変条件）
    this.enforceInvariant(
      this.items.length < 50,
      "Cart cannot contain more than 50 different items"
    );
    
    // 既存アイテムの確認
    const existingItem = this.findItem(productId);
    
    if (existingItem) {
      // 数量を更新
      const result = existingItem.updateQuantity(
        existingItem.getQuantity() + quantity
      );
      
      if (result.isFailure) {
        return result;
      }
    } else {
      // 新しいアイテムを追加
      const newItem = CartItem.create(
        productId,
        quantity,
        price
      );
      
      this.items.push(newItem);
    }
    
    this.lastModifiedAt = new Date();
    
    this.trackChange(
      new ItemAddedToCart(
        this.id,
        productId,
        quantity,
        price
      )
    );
    
    return Result.ok();
  }
  
  removeItem(productId: ProductId): Result<void> {
    if (this.status !== CartStatus.ACTIVE) {
      return Result.fail("Cannot remove items from inactive cart");
    }
    
    const itemIndex = this.items.findIndex(
      item => item.getProductId().equals(productId)
    );
    
    if (itemIndex === -1) {
      return Result.fail("Item not found in cart");
    }
    
    this.items.splice(itemIndex, 1);
    this.lastModifiedAt = new Date();
    
    this.trackChange(
      new ItemRemovedFromCart(this.id, productId)
    );
    
    return Result.ok();
  }
  
  checkout(): Result<CheckoutInfo> {
    if (this.status !== CartStatus.ACTIVE) {
      return Result.fail("Cart is not active");
    }
    
    if (this.items.length === 0) {
      return Result.fail("Cannot checkout empty cart");
    }
    
    // 在庫チェックは外部で行う（別の集約）
    // ここでは集約内の一貫性のみを保証
    
    const total = this.calculateTotal();
    this.status = CartStatus.CHECKED_OUT;
    
    this.trackChange(
      new CartCheckedOut(
        this.id,
        this.customerId,
        total
      )
    );
    
    return Result.ok({
      cartId: this.id,
      customerId: this.customerId,
      items: this.items.map(item => item.toCheckoutItem()),
      total
    });
  }
  
  // プライベートメソッド
  private findItem(productId: ProductId): CartItem | undefined {
    return this.items.find(
      item => item.getProductId().equals(productId)
    );
  }
  
  private calculateTotal(): Money {
    return this.items.reduce(
      (total, item) => total.add(item.getSubtotal()),
      Money.zero()
    );
  }
}

// 集約内のエンティティ
class CartItem extends Entity<CartItemId> {
  private productId: ProductId;
  private quantity: number;
  private unitPrice: Money;
  
  private constructor(
    id: CartItemId,
    productId: ProductId,
    quantity: number,
    unitPrice: Money
  ) {
    super(id);
    this.productId = productId;
    this.quantity = quantity;
    this.unitPrice = unitPrice;
  }
  
  static create(
    productId: ProductId,
    quantity: number,
    unitPrice: Money
  ): CartItem {
    return new CartItem(
      CartItemId.generate(),
      productId,
      quantity,
      unitPrice
    );
  }
  
  updateQuantity(newQuantity: number): Result<void> {
    if (newQuantity <= 0) {
      return Result.fail("Quantity must be positive");
    }
    
    if (newQuantity > 100) {
      return Result.fail("Quantity cannot exceed 100");
    }
    
    this.quantity = newQuantity;
    return Result.ok();
  }
  
  getProductId(): ProductId {
    return this.productId;
  }
  
  getQuantity(): number {
    return this.quantity;
  }
  
  getSubtotal(): Money {
    return this.unitPrice.multiply(this.quantity);
  }
  
  toCheckoutItem(): CheckoutItem {
    return {
      productId: this.productId,
      quantity: this.quantity,
      unitPrice: this.unitPrice,
      subtotal: this.getSubtotal()
    };
  }
}
```

### 大きな集約の分割パターン

```typescript
// Before: 大きすぎる集約
class LargeOrder extends AggregateRoot<OrderId> {
  private customer: Customer;          // ❌ エンティティ全体を保持
  private items: OrderItem[];
  private shipping: ShippingInfo;
  private payment: PaymentInfo;
  private invoices: Invoice[];         // ❌ 関連する全ての請求書
  private shipments: Shipment[];       // ❌ 関連する全ての出荷
  private returns: Return[];           // ❌ 関連する全ての返品
  
  // 多くの責任と複雑な不変条件...
}

// After: 適切に分割された集約
class Order extends AggregateRoot<OrderId> {
  private customerId: CustomerId;      // ✓ IDで参照
  private items: OrderItem[];
  private status: OrderStatus;
  private placedAt: Date;
  
  // 注文の作成と確認に関する責任のみ
  
  placeOrder(): Result<OrderPlaced> {
    // 注文の確定
    this.status = OrderStatus.PLACED;
    
    const event = new OrderPlaced(
      this.id,
      this.customerId,
      this.items,
      this.calculateTotal()
    );
    
    this.trackChange(event);
    
    return Result.ok(event);
  }
}

// 支払いは別の集約
class Payment extends AggregateRoot<PaymentId> {
  private orderId: OrderId;            // ✓ IDで参照
  private amount: Money;
  private method: PaymentMethod;
  private status: PaymentStatus;
  
  // 支払い処理に関する責任のみ
  
  processPayment(): Result<PaymentProcessed> {
    // 支払い処理ロジック
  }
}

// 出荷も別の集約
class Shipment extends AggregateRoot<ShipmentId> {
  private orderId: OrderId;            // ✓ IDで参照
  private items: ShipmentItem[];
  private address: Address;
  private carrier: Carrier;
  private status: ShipmentStatus;
  
  // 出荷に関する責任のみ
  
  ship(): Result<ShipmentDispatched> {
    // 出荷処理ロジック
  }
}
```

### 集約間の協調パターン

```typescript
// ドメインサービスを使った集約間の協調
export class OrderFulfillmentService {
  constructor(
    private orderRepo: OrderRepository,
    private paymentRepo: PaymentRepository,
    private inventoryRepo: InventoryRepository,
    private shipmentRepo: ShipmentRepository,
    private eventBus: EventBus
  ) {}
  
  async fulfillOrder(
    orderId: OrderId
  ): Promise<Result<void>> {
    // 1. 注文の取得
    const order = await this.orderRepo.findById(orderId);
    if (!order) {
      return Result.fail("Order not found");
    }
    
    // 2. 在庫の確保（別の集約）
    const reservationResult = await this.reserveInventory(order);
    if (reservationResult.isFailure) {
      return Result.fail(reservationResult.error);
    }
    
    // 3. 支払いの作成（別の集約）
    const payment = Payment.create(
      orderId,
      order.getTotal()
    );
    await this.paymentRepo.save(payment);
    
    // 4. 支払い処理
    const paymentResult = payment.processPayment();
    if (paymentResult.isFailure) {
      // 在庫の予約をキャンセル
      await this.releaseInventory(reservationResult.value);
      return Result.fail(paymentResult.error);
    }
    
    await this.paymentRepo.save(payment);
    
    // 5. 出荷の作成（別の集約）
    const shipment = Shipment.create(
      orderId,
      order.getShippingAddress()
    );
    await this.shipmentRepo.save(shipment);
    
    // 6. イベントの発行
    await this.eventBus.publish(
      new OrderFulfilled(orderId)
    );
    
    return Result.ok();
  }
  
  private async reserveInventory(
    order: Order
  ): Promise<Result<ReservationId>> {
    // 各商品の在庫を確保
    const reservations: InventoryReservation[] = [];
    
    for (const item of order.getItems()) {
      const inventory = await this.inventoryRepo.findByProductId(
        item.productId
      );
      
      if (!inventory) {
        // ロールバック
        await this.rollbackReservations(reservations);
        return Result.fail(`Product ${item.productId} not found`);
      }
      
      const reservationResult = inventory.reserve(
        item.quantity
      );
      
      if (reservationResult.isFailure) {
        // ロールバック
        await this.rollbackReservations(reservations);
        return Result.fail(reservationResult.error);
      }
      
      await this.inventoryRepo.save(inventory);
      reservations.push(reservationResult.value);
    }
    
    return Result.ok(ReservationId.generate());
  }
}
```

## 集約設計の落とし穴と対策

### よくある設計ミス

```typescript
// アンチパターン1: 集約間の直接参照
class BadOrder {
  private customer: Customer;  // ❌ 別の集約への直接参照
  
  // これにより2つの問題が発生：
  // 1. 大きなオブジェクトグラフの読み込み
  // 2. トランザクション境界の曖昧さ
}

// 解決策: IDによる参照
class GoodOrder {
  private customerId: CustomerId;  // ✓ IDのみを保持
  
  // 必要に応じて別途取得
  async getCustomerName(repo: CustomerRepository): Promise<string> {
    const customer = await repo.findById(this.customerId);
    return customer?.getName() ?? "Unknown";
  }
}

// アンチパターン2: 集約をまたぐトランザクション
class BadOrderService {
  async placeOrder(cart: Cart, customer: Customer) {
    // ❌ 複数の集約を同一トランザクションで更新
    cart.checkout();
    customer.incrementOrderCount();
    
    await this.db.transaction(async tx => {
      await tx.save(cart);
      await tx.save(customer);
    });
  }
}

// 解決策: 結果整合性の活用
class GoodOrderService {
  async placeOrder(cartId: CartId, customerId: CustomerId) {
    // ✓ 1つの集約のみを更新
    const cart = await this.cartRepo.findById(cartId);
    const checkoutResult = cart.checkout();
    await this.cartRepo.save(cart);
    
    // ✓ イベントで他の集約に通知
    await this.eventBus.publish(
      new CartCheckedOut(cartId, customerId)
    );
  }
}

// イベントハンドラで顧客情報を更新
class CustomerOrderCountUpdater {
  async handle(event: CartCheckedOut) {
    const customer = await this.customerRepo.findById(event.customerId);
    customer.incrementOrderCount();
    await this.customerRepo.save(customer);
  }
}
```

### パフォーマンスを考慮した設計

```typescript
// 読み取りモデルの分離
export class OrderSummaryReadModel {
  // 集約とは別に、読み取り専用のモデルを用意
  constructor(
    public readonly orderId: string,
    public readonly customerName: string,
    public readonly totalAmount: number,
    public readonly status: string,
    public readonly itemCount: number
  ) {}
}

export class OrderSummaryProjection {
  async project(event: DomainEvent): Promise<void> {
    if (event instanceof OrderPlaced) {
      // 読み取りモデルを作成
      const customer = await this.getCustomerName(event.customerId);
      
      await this.db.orderSummaries.create({
        orderId: event.orderId,
        customerName: customer,
        totalAmount: event.total,
        status: 'PLACED',
        itemCount: event.items.length
      });
    }
    
    if (event instanceof OrderShipped) {
      // 読み取りモデルを更新
      await this.db.orderSummaries.update({
        where: { orderId: event.orderId },
        data: { status: 'SHIPPED' }
      });
    }
  }
}

// 効率的なクエリ
export class OrderQueryService {
  async findOrdersByCustomer(
    customerId: CustomerId
  ): Promise<OrderSummaryReadModel[]> {
    // 集約を経由せず、読み取りモデルから直接取得
    const summaries = await this.db.orderSummaries.findMany({
      where: { customerId: customerId.value }
    });
    
    return summaries.map(s => new OrderSummaryReadModel(
      s.orderId,
      s.customerName,
      s.totalAmount,
      s.status,
      s.itemCount
    ));
  }
}
```

## 集約の実装テクニック

### イベントソーシングベースの集約

```typescript
export abstract class EventSourcedAggregateRoot<T extends EntityId> 
  extends AggregateRoot<T> {
  
  private version: number = 0;
  private changes: DomainEvent[] = [];
  
  protected constructor(id: T) {
    super(id);
  }
  
  // イベントから状態を復元
  static reconstitute<A extends EventSourcedAggregateRoot<any>>(
    events: DomainEvent[],
    createEmpty: (id: EntityId) => A
  ): A {
    if (events.length === 0) {
      throw new Error("No events to reconstitute from");
    }
    
    const aggregate = createEmpty(
      EntityId.fromString(events[0].aggregateId)
    );
    
    aggregate.rehydrate(events);
    return aggregate;
  }
  
  private rehydrate(events: DomainEvent[]): void {
    events.forEach(event => {
      this.applyEvent(event);
      this.version++;
    });
  }
  
  protected applyChange(event: DomainEvent): void {
    this.applyEvent(event);
    this.changes.push(event);
  }
  
  private applyEvent(event: DomainEvent): void {
    const handler = this.getEventHandler(event);
    if (handler) {
      handler.call(this, event);
    }
  }
  
  private getEventHandler(event: DomainEvent): Function | undefined {
    const handlerName = `on${event.constructor.name}`;
    return (this as any)[handlerName];
  }
  
  getUncommittedChanges(): DomainEvent[] {
    return this.changes;
  }
  
  markChangesAsCommitted(): void {
    this.changes = [];
  }
  
  getVersion(): number {
    return this.version;
  }
}

// 実装例
export class EventSourcedOrder 
  extends EventSourcedAggregateRoot<OrderId> {
  
  private customerId!: CustomerId;
  private items: Map<string, OrderItem> = new Map();
  private status!: OrderStatus;
  
  static create(customerId: CustomerId): EventSourcedOrder {
    const order = new EventSourcedOrder(OrderId.generate());
    
    order.applyChange(
      new OrderCreated(order.id.value, customerId.value)
    );
    
    return order;
  }
  
  static fromEvents(events: DomainEvent[]): EventSourcedOrder {
    return EventSourcedAggregateRoot.reconstitute(
      events,
      id => new EventSourcedOrder(id as OrderId)
    );
  }
  
  addItem(
    productId: ProductId,
    quantity: number,
    price: Money
  ): void {
    if (this.status !== OrderStatus.DRAFT) {
      throw new Error("Can only add items to draft orders");
    }
    
    this.applyChange(
      new OrderItemAdded(
        this.id.value,
        productId.value,
        quantity,
        price.toJSON()
      )
    );
  }
  
  // イベントハンドラ
  private onOrderCreated(event: OrderCreated): void {
    this.customerId = CustomerId.fromString(event.customerId);
    this.status = OrderStatus.DRAFT;
  }
  
  private onOrderItemAdded(event: OrderItemAdded): void {
    const item = OrderItem.create(
      ProductId.fromString(event.productId),
      event.quantity,
      Money.fromJSON(event.price)
    );
    
    this.items.set(event.productId, item);
  }
}
```

## まとめ

集約設計は、ドメイン駆動設計の中でも特に重要な要素です。Parasol V5.4における成功の鍵：

1. **小さな集約を維持** - 並行性とパフォーマンスの向上
2. **明確な境界** - トランザクション境界と一致させる
3. **ID による参照** - 集約間の疎結合を保つ
4. **不変条件の強制** - ビジネスルールを集約内で保証
5. **結果整合性の活用** - 集約間の協調はイベントで

適切に設計された集約は、システムの保守性、拡張性、パフォーマンスを大幅に向上させます。

### 次章への架橋

集約設計の基本を理解したところで、第22章ではCQRSとイベントソーシングについて、より高度なアーキテクチャパターンを解説します。

---

## 演習問題

1. 「ホテル予約システム」における部屋、予約、顧客の関係を分析し、適切な集約境界を設計してください。

2. 「在庫管理システム」で、商品の入出庫、棚卸し、在庫移動を扱う集約を設計してください。同時実行制御も考慮してください。

3. 大きすぎる「プロジェクト管理」集約（プロジェクト、タスク、メンバー、進捗、ドキュメントを含む）を、適切な粒度の複数の集約に分割してください。