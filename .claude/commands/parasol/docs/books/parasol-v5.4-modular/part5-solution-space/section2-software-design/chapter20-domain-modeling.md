# 第20章　ドメインモデリング ― 概念の彫刻

## はじめに：言葉で世界を作る

ミケランジェロは「私は大理石から彫刻を作るのではない。すでにそこにある姿を解放するだけだ」と語りました。同様に、優れたドメインモデリングは、ビジネスの本質的な構造を「発見」し、それをコードとして表現する芸術です。

本章では、Parasol V5.4の文脈で、ビジネスドメインの深い理解をどのように精緻なモデルとして表現するかを解説します。

## ドメインモデリングの本質

### ユビキタス言語の構築

```typescript
export interface UbiquitousLanguage {
  // 用語定義
  terms: Map<string, TermDefinition>;
  
  // 文脈による意味の違い
  contextualMeanings: Map<string, Map<BoundedContext, Meaning>>;
  
  // 用語間の関係
  relationships: TermRelationship[];
  
  // 進化の履歴
  evolution: LanguageEvolution[];
}

export class LanguageBuilder {
  buildUbiquitousLanguage(
    domainExperts: DomainExpert[],
    developers: Developer[]
  ): UbiquitousLanguage {
    // 1. 用語の収集
    const collectedTerms = this.collectTermsFromStakeholders(
      [...domainExperts, ...developers]
    );
    
    // 2. 意味の明確化
    const clarifiedTerms = this.clarifyMeanings(
      collectedTerms,
      domainExperts
    );
    
    // 3. 文脈の識別
    const contextualizedTerms = this.identifyContexts(
      clarifiedTerms
    );
    
    // 4. 関係の定義
    const relationships = this.defineRelationships(
      contextualizedTerms
    );
    
    // 5. 検証と洗練
    return this.refineLanguage(
      contextualizedTerms,
      relationships,
      domainExperts
    );
  }
  
  private clarifyMeanings(
    terms: RawTerm[],
    experts: DomainExpert[]
  ): ClarifiedTerm[] {
    return terms.map(term => {
      // エキスパートとの対話セッション
      const expertOpinions = experts.map(expert => 
        this.conductClarificationSession(term, expert)
      );
      
      // 合意形成
      const consensus = this.buildConsensus(expertOpinions);
      
      // 具体例による検証
      const examples = this.gatherConcreteExamples(term, experts);
      
      return {
        term: term.name,
        definition: consensus.definition,
        examples,
        constraints: consensus.constraints,
        invariants: consensus.invariants
      };
    });
  }
}
```

### ドメインモデルの発見プロセス

```typescript
export class DomainModelDiscovery {
  async discoverModel(
    domain: BusinessDomain
  ): Promise<DomainModel> {
    // 1. 知識の収集
    const knowledge = await this.gatherDomainKnowledge(domain);
    
    // 2. 概念の抽出
    const concepts = await this.extractConcepts(knowledge);
    
    // 3. 振る舞いの識別
    const behaviors = await this.identifyBehaviors(concepts);
    
    // 4. ルールの発見
    const rules = await this.discoverBusinessRules(concepts);
    
    // 5. モデルの構築
    return this.constructModel(concepts, behaviors, rules);
  }
  
  private async extractConcepts(
    knowledge: DomainKnowledge
  ): Promise<Concept[]> {
    // イベントストーミング
    const events = await this.conductEventStorming(knowledge);
    
    // コマンドの識別
    const commands = this.identifyCommands(events);
    
    // エンティティの発見
    const entities = this.discoverEntities(events, commands);
    
    // 値オブジェクトの識別
    const valueObjects = this.identifyValueObjects(entities);
    
    // ドメインサービスの抽出
    const domainServices = this.extractDomainServices(
      events,
      commands,
      entities
    );
    
    return [...entities, ...valueObjects, ...domainServices];
  }
}
```

## 戦術的DDDパターンの適用

### エンティティの設計

```typescript
export abstract class Entity<ID extends EntityId> {
  protected readonly id: ID;
  protected domainEvents: DomainEvent[] = [];
  
  protected constructor(id: ID) {
    this.id = id;
  }
  
  getId(): ID {
    return this.id;
  }
  
  equals(other: Entity<ID>): boolean {
    if (other === null || other === undefined) {
      return false;
    }
    
    if (this === other) {
      return true;
    }
    
    return this.id.equals(other.id);
  }
  
  protected addDomainEvent(event: DomainEvent): void {
    this.domainEvents.push(event);
  }
  
  clearEvents(): void {
    this.domainEvents = [];
  }
  
  getUncommittedEvents(): DomainEvent[] {
    return this.domainEvents;
  }
}

// 実例：顧客エンティティ
export class Customer extends Entity<CustomerId> {
  private name: CustomerName;
  private email: Email;
  private status: CustomerStatus;
  private creditLimit: Money;
  private registrationDate: Date;
  
  private constructor(
    id: CustomerId,
    props: CustomerProps
  ) {
    super(id);
    this.name = props.name;
    this.email = props.email;
    this.status = props.status;
    this.creditLimit = props.creditLimit;
    this.registrationDate = props.registrationDate;
  }
  
  static create(props: CreateCustomerProps): Customer {
    const customerId = CustomerId.generate();
    
    const customer = new Customer(customerId, {
      name: CustomerName.create(props.firstName, props.lastName),
      email: Email.create(props.email),
      status: CustomerStatus.ACTIVE,
      creditLimit: Money.create(props.initialCreditLimit),
      registrationDate: new Date()
    });
    
    customer.addDomainEvent(
      new CustomerCreatedEvent(customerId, props)
    );
    
    return customer;
  }
  
  // ビジネスロジック
  placeOrder(order: Order): Result<void> {
    // 信用限度額のチェック
    if (!this.hasEnoughCredit(order.totalAmount)) {
      return Result.fail("Insufficient credit limit");
    }
    
    // ステータスのチェック
    if (!this.canPlaceOrder()) {
      return Result.fail("Customer status does not allow ordering");
    }
    
    this.addDomainEvent(
      new OrderPlacedEvent(this.id, order.id)
    );
    
    return Result.ok();
  }
  
  private hasEnoughCredit(orderAmount: Money): boolean {
    // 現在の注文総額を取得（リポジトリ経由）
    const currentOrderTotal = this.getCurrentOrderTotal();
    const projectedTotal = currentOrderTotal.add(orderAmount);
    
    return projectedTotal.lessThanOrEqual(this.creditLimit);
  }
  
  private canPlaceOrder(): boolean {
    return this.status === CustomerStatus.ACTIVE;
  }
}
```

### 値オブジェクトの設計

```typescript
export abstract class ValueObject<T> {
  protected readonly props: T;
  
  protected constructor(props: T) {
    this.props = Object.freeze(props);
  }
  
  equals(vo?: ValueObject<T>): boolean {
    if (vo === null || vo === undefined) {
      return false;
    }
    
    if (vo.props === undefined) {
      return false;
    }
    
    return JSON.stringify(this.props) === JSON.stringify(vo.props);
  }
}

// 実例：金額
export class Money extends ValueObject<MoneyProps> {
  private constructor(props: MoneyProps) {
    super(props);
  }
  
  static create(amount: number, currency: string = 'JPY'): Money {
    if (amount < 0) {
      throw new Error('Amount cannot be negative');
    }
    
    if (!this.isValidCurrency(currency)) {
      throw new Error(`Invalid currency: ${currency}`);
    }
    
    return new Money({ amount, currency });
  }
  
  add(other: Money): Money {
    if (this.props.currency !== other.props.currency) {
      throw new Error('Cannot add money with different currencies');
    }
    
    return Money.create(
      this.props.amount + other.props.amount,
      this.props.currency
    );
  }
  
  multiply(factor: number): Money {
    return Money.create(
      Math.round(this.props.amount * factor),
      this.props.currency
    );
  }
  
  lessThanOrEqual(other: Money): boolean {
    if (this.props.currency !== other.props.currency) {
      throw new Error('Cannot compare money with different currencies');
    }
    
    return this.props.amount <= other.props.amount;
  }
  
  private static isValidCurrency(currency: string): boolean {
    const validCurrencies = ['JPY', 'USD', 'EUR', 'GBP'];
    return validCurrencies.includes(currency);
  }
  
  toString(): string {
    return `${this.props.currency} ${this.props.amount}`;
  }
}

// 実例：メールアドレス
export class Email extends ValueObject<{ value: string }> {
  private constructor(value: string) {
    super({ value });
  }
  
  static create(email: string): Email {
    if (!this.isValid(email)) {
      throw new Error(`Invalid email address: ${email}`);
    }
    
    return new Email(email.toLowerCase());
  }
  
  private static isValid(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }
  
  getValue(): string {
    return this.props.value;
  }
  
  getDomain(): string {
    return this.props.value.split('@')[1];
  }
}
```

### ドメインサービスの設計

```typescript
export interface DomainService {
  // ドメインサービスはステートレス
}

// 実例：価格計算サービス
export class PricingService implements DomainService {
  calculatePrice(
    product: Product,
    quantity: number,
    customer: Customer,
    promotions: Promotion[]
  ): PricingResult {
    // 基本価格の計算
    const basePrice = product.getPrice().multiply(quantity);
    
    // 顧客別割引の適用
    const customerDiscount = this.calculateCustomerDiscount(
      customer,
      basePrice
    );
    
    // プロモーション割引の適用
    const promotionDiscount = this.calculatePromotionDiscount(
      product,
      quantity,
      promotions
    );
    
    // 最終価格の計算
    const finalPrice = basePrice
      .subtract(customerDiscount)
      .subtract(promotionDiscount);
    
    return {
      basePrice,
      customerDiscount,
      promotionDiscount,
      finalPrice,
      appliedPromotions: this.getAppliedPromotions(product, promotions)
    };
  }
  
  private calculateCustomerDiscount(
    customer: Customer,
    basePrice: Money
  ): Money {
    const discountRate = customer.getDiscountRate();
    return basePrice.multiply(discountRate);
  }
  
  private calculatePromotionDiscount(
    product: Product,
    quantity: number,
    promotions: Promotion[]
  ): Money {
    const applicablePromotions = promotions.filter(
      promo => promo.isApplicableTo(product, quantity)
    );
    
    // 最も有利なプロモーションを選択
    const bestPromotion = this.selectBestPromotion(
      applicablePromotions,
      product,
      quantity
    );
    
    return bestPromotion
      ? bestPromotion.calculateDiscount(product, quantity)
      : Money.create(0);
  }
}
```

## 集約の設計原則

### 集約境界の定義

```typescript
export abstract class AggregateRoot<ID extends EntityId> extends Entity<ID> {
  // 集約ルートは外部からの唯一のエントリーポイント
  
  protected validateInvariants(): void {
    // 集約全体の不変条件を検証
  }
  
  protected apply(event: DomainEvent): void {
    // イベントを適用して状態を変更
    this.addDomainEvent(event);
    this.validateInvariants();
  }
}

// 実例：注文集約
export class Order extends AggregateRoot<OrderId> {
  private customerId: CustomerId;
  private orderLines: OrderLine[];
  private status: OrderStatus;
  private shippingAddress: Address;
  private placedAt: Date;
  
  private constructor(
    id: OrderId,
    props: OrderProps
  ) {
    super(id);
    this.customerId = props.customerId;
    this.orderLines = props.orderLines || [];
    this.status = props.status;
    this.shippingAddress = props.shippingAddress;
    this.placedAt = props.placedAt;
  }
  
  static create(props: CreateOrderProps): Order {
    const orderId = OrderId.generate();
    
    const order = new Order(orderId, {
      customerId: props.customerId,
      orderLines: [],
      status: OrderStatus.DRAFT,
      shippingAddress: props.shippingAddress,
      placedAt: new Date()
    });
    
    // 初期の注文明細を追加
    props.items.forEach(item => {
      order.addOrderLine(item.productId, item.quantity);
    });
    
    order.apply(
      new OrderCreatedEvent(orderId, props)
    );
    
    return order;
  }
  
  // ビジネスメソッド
  addOrderLine(productId: ProductId, quantity: number): void {
    if (this.status !== OrderStatus.DRAFT) {
      throw new Error("Cannot modify a confirmed order");
    }
    
    const existingLine = this.orderLines.find(
      line => line.productId.equals(productId)
    );
    
    if (existingLine) {
      existingLine.increaseQuantity(quantity);
    } else {
      this.orderLines.push(
        OrderLine.create(productId, quantity)
      );
    }
    
    this.apply(
      new OrderLineAddedEvent(this.id, productId, quantity)
    );
  }
  
  confirm(): void {
    if (this.status !== OrderStatus.DRAFT) {
      throw new Error("Order is already confirmed");
    }
    
    if (this.orderLines.length === 0) {
      throw new Error("Cannot confirm an empty order");
    }
    
    this.status = OrderStatus.CONFIRMED;
    
    this.apply(
      new OrderConfirmedEvent(this.id)
    );
  }
  
  ship(): void {
    if (this.status !== OrderStatus.CONFIRMED) {
      throw new Error("Only confirmed orders can be shipped");
    }
    
    this.status = OrderStatus.SHIPPED;
    
    this.apply(
      new OrderShippedEvent(this.id)
    );
  }
  
  protected validateInvariants(): void {
    // 注文金額の上限チェック
    const totalAmount = this.calculateTotalAmount();
    if (totalAmount.greaterThan(Money.create(10000000))) {
      throw new Error("Order amount exceeds maximum limit");
    }
    
    // 注文明細の重複チェック
    const productIds = this.orderLines.map(line => line.productId.value);
    if (new Set(productIds).size !== productIds.length) {
      throw new Error("Duplicate order lines detected");
    }
  }
  
  private calculateTotalAmount(): Money {
    return this.orderLines.reduce(
      (total, line) => total.add(line.getSubtotal()),
      Money.create(0)
    );
  }
}

// 注文明細（集約内エンティティ）
class OrderLine extends Entity<OrderLineId> {
  productId: ProductId;
  private quantity: number;
  private unitPrice: Money;
  
  private constructor(
    id: OrderLineId,
    props: OrderLineProps
  ) {
    super(id);
    this.productId = props.productId;
    this.quantity = props.quantity;
    this.unitPrice = props.unitPrice;
  }
  
  static create(productId: ProductId, quantity: number): OrderLine {
    if (quantity <= 0) {
      throw new Error("Quantity must be positive");
    }
    
    return new OrderLine(OrderLineId.generate(), {
      productId,
      quantity,
      unitPrice: Money.create(0) // 後で価格サービスから設定
    });
  }
  
  increaseQuantity(amount: number): void {
    if (amount <= 0) {
      throw new Error("Amount must be positive");
    }
    
    this.quantity += amount;
  }
  
  getSubtotal(): Money {
    return this.unitPrice.multiply(this.quantity);
  }
}
```

## ドメインイベントの設計

### イベントの定義と発行

```typescript
export abstract class DomainEvent {
  readonly occurredOn: Date;
  readonly aggregateId: string;
  
  constructor(aggregateId: string) {
    this.occurredOn = new Date();
    this.aggregateId = aggregateId;
  }
}

// 実例：注文関連イベント
export class OrderCreatedEvent extends DomainEvent {
  constructor(
    orderId: OrderId,
    public readonly customerId: CustomerId,
    public readonly items: OrderItemData[]
  ) {
    super(orderId.value);
  }
}

export class OrderConfirmedEvent extends DomainEvent {
  constructor(
    orderId: OrderId
  ) {
    super(orderId.value);
  }
}

export class OrderShippedEvent extends DomainEvent {
  constructor(
    orderId: OrderId,
    public readonly trackingNumber?: string
  ) {
    super(orderId.value);
  }
}

// イベントハンドラ
export interface DomainEventHandler<T extends DomainEvent> {
  handle(event: T): Promise<void>;
}

export class SendOrderConfirmationEmail 
  implements DomainEventHandler<OrderConfirmedEvent> {
  
  constructor(
    private emailService: EmailService,
    private customerRepository: CustomerRepository
  ) {}
  
  async handle(event: OrderConfirmedEvent): Promise<void> {
    const order = await this.orderRepository.findById(
      OrderId.create(event.aggregateId)
    );
    
    const customer = await this.customerRepository.findById(
      order.customerId
    );
    
    await this.emailService.send({
      to: customer.email.getValue(),
      subject: `Order Confirmation - ${event.aggregateId}`,
      template: 'order-confirmation',
      data: {
        customerName: customer.name.getFullName(),
        orderId: event.aggregateId,
        orderDate: event.occurredOn
      }
    });
  }
}
```

## ドメインモデルの実装パターン

### リポジトリパターン

```typescript
export interface Repository<T extends AggregateRoot<any>, ID extends EntityId> {
  findById(id: ID): Promise<T | null>;
  save(aggregate: T): Promise<void>;
  delete(id: ID): Promise<void>;
}

// 実例：顧客リポジトリ
export interface CustomerRepository extends Repository<Customer, CustomerId> {
  findByEmail(email: Email): Promise<Customer | null>;
  findActiveCustomers(): Promise<Customer[]>;
  findByStatus(status: CustomerStatus): Promise<Customer[]>;
}

export class CustomerRepositoryImpl implements CustomerRepository {
  constructor(
    private db: Database,
    private eventBus: EventBus
  ) {}
  
  async findById(id: CustomerId): Promise<Customer | null> {
    const data = await this.db.customers.findOne({
      where: { id: id.value }
    });
    
    if (!data) {
      return null;
    }
    
    return this.reconstitute(data);
  }
  
  async save(customer: Customer): Promise<void> {
    const data = this.toPersistence(customer);
    
    await this.db.customers.upsert({
      where: { id: data.id },
      create: data,
      update: data
    });
    
    // ドメインイベントの発行
    const events = customer.getUncommittedEvents();
    for (const event of events) {
      await this.eventBus.publish(event);
    }
    
    customer.clearEvents();
  }
  
  private reconstitute(data: CustomerData): Customer {
    return Customer.reconstitute({
      id: CustomerId.create(data.id),
      name: CustomerName.create(data.firstName, data.lastName),
      email: Email.create(data.email),
      status: data.status as CustomerStatus,
      creditLimit: Money.create(data.creditLimit),
      registrationDate: data.registrationDate
    });
  }
  
  private toPersistence(customer: Customer): CustomerData {
    return {
      id: customer.id.value,
      firstName: customer.name.firstName,
      lastName: customer.name.lastName,
      email: customer.email.getValue(),
      status: customer.status,
      creditLimit: customer.creditLimit.amount,
      creditCurrency: customer.creditLimit.currency,
      registrationDate: customer.registrationDate
    };
  }
}
```

### 仕様パターン

```typescript
export abstract class Specification<T> {
  abstract isSatisfiedBy(candidate: T): boolean;
  
  and(other: Specification<T>): Specification<T> {
    return new AndSpecification(this, other);
  }
  
  or(other: Specification<T>): Specification<T> {
    return new OrSpecification(this, other);
  }
  
  not(): Specification<T> {
    return new NotSpecification(this);
  }
}

// 実例：顧客仕様
class PremiumCustomerSpecification extends Specification<Customer> {
  isSatisfiedBy(customer: Customer): boolean {
    return customer.status === CustomerStatus.PREMIUM &&
           customer.creditLimit.amount >= 1000000;
  }
}

class ActiveCustomerSpecification extends Specification<Customer> {
  isSatisfiedBy(customer: Customer): boolean {
    return customer.status === CustomerStatus.ACTIVE;
  }
}

// 仕様の組み合わせ
const canPlaceHighValueOrder = new PremiumCustomerSpecification()
  .or(
    new ActiveCustomerSpecification()
      .and(new HasGoodCreditHistorySpecification())
  );

// 使用例
if (canPlaceHighValueOrder.isSatisfiedBy(customer)) {
  // 高額注文を許可
}
```

## ドメインモデルの進化

### モデルの深化プロセス

```typescript
export class ModelEvolution {
  evolveDomainModel(
    currentModel: DomainModel,
    insights: DomainInsight[]
  ): EvolvedModel {
    // 1. 新しい概念の発見
    const newConcepts = this.discoverNewConcepts(insights);
    
    // 2. 既存概念の洗練
    const refinedConcepts = this.refineConcepts(
      currentModel.concepts,
      insights
    );
    
    // 3. 関係の再構築
    const updatedRelationships = this.restructureRelationships(
      refinedConcepts,
      newConcepts
    );
    
    // 4. 境界の再定義
    const newBoundaries = this.redefineBoundaries(
      refinedConcepts,
      updatedRelationships
    );
    
    // 5. 移行計画
    const migrationPlan = this.createMigrationPlan(
      currentModel,
      { concepts: refinedConcepts, boundaries: newBoundaries }
    );
    
    return {
      model: { concepts: refinedConcepts, boundaries: newBoundaries },
      migrationPlan,
      benefits: this.assessBenefits(currentModel, refinedConcepts)
    };
  }
}
```

## まとめ

ドメインモデリングは、ビジネスの本質を捉え、それをコードとして表現する芸術です。Parasol V5.4における成功の鍵：

1. **ユビキタス言語の徹底** - ビジネスとITの共通言語を構築
2. **概念の正確な表現** - エンティティ、値オブジェクト、集約を適切に使い分け
3. **不変条件の明確化** - ビジネスルールをモデルに組み込む
4. **境界の慎重な設計** - 集約の境界を小さく保つ
5. **継続的な深化** - モデルは常に進化し続ける

優れたドメインモデルは、ビジネスの複雑性を管理し、変化に対応できる柔軟性を提供します。

### 次章への架橋

ドメインモデルの基礎を理解したところで、第21章では集約の設計について、より詳細に掘り下げていきます。

---

## 演習問題

1. ECサイトの「商品レビュー」機能をドメインモデルとして設計してください。エンティティ、値オブジェクト、集約境界を明確にしてください。

2. 「在庫管理」ドメインにおいて、「在庫切れ」「入荷待ち」「予約可能」などの状態遷移をモデル化してください。

3. あなたの組織の主要なビジネスドメインを選び、ユビキタス言語の辞書を作成してください。