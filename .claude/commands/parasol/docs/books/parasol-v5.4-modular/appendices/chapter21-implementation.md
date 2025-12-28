# Appendix: Chapter 21 - Aggregate Design Implementation Details

## Core Implementation Patterns

### Base Aggregate Root Class

```typescript
export abstract class AggregateRoot<T extends EntityId> extends Entity<T> {
  private domainEvents: DomainEvent[] = [];
  private isModified: boolean = false;
  
  protected constructor(id: T) {
    super(id);
  }
  
  // Domain event management
  protected addDomainEvent(event: DomainEvent): void {
    this.domainEvents.push(event);
  }
  
  getDomainEvents(): DomainEvent[] {
    return [...this.domainEvents];
  }
  
  clearDomainEvents(): void {
    this.domainEvents = [];
  }
  
  // Change tracking
  protected markAsModified(): void {
    this.isModified = true;
  }
  
  hasChanges(): boolean {
    return this.isModified;
  }
  
  // Invariant enforcement
  protected enforceInvariant(
    condition: boolean,
    message: string
  ): void {
    if (!condition) {
      throw new InvariantViolationError(message);
    }
  }
  
  // Child entity management
  protected getChild<C extends Entity<any>>(
    children: C[],
    id: EntityId
  ): C | undefined {
    return children.find(child => child.getId().equals(id));
  }
  
  protected addChild<C extends Entity<any>>(
    children: C[],
    child: C,
    maxCount?: number
  ): void {
    if (maxCount) {
      this.enforceInvariant(
        children.length < maxCount,
        `Cannot exceed maximum of ${maxCount} items`
      );
    }
    children.push(child);
  }
  
  protected removeChild<C extends Entity<any>>(
    children: C[],
    id: EntityId
  ): C | undefined {
    const index = children.findIndex(
      child => child.getId().equals(id)
    );
    
    if (index === -1) {
      return undefined;
    }
    
    const [removed] = children.splice(index, 1);
    return removed;
  }
  
  // Convenience method for tracking changes
  protected trackChange(event: DomainEvent): void {
    this.addDomainEvent(event);
    this.markAsModified();
  }
}
```

### Complete Shopping Cart Implementation

```typescript
// Value Objects
export class CartItemId extends EntityId {
  static generate(): CartItemId {
    return new CartItemId(uuid());
  }
}

export class CartId extends EntityId {
  static generate(): CartId {
    return new CartId(uuid());
  }
}

export enum CartStatus {
  ACTIVE = "ACTIVE",
  CHECKED_OUT = "CHECKED_OUT",
  EXPIRED = "EXPIRED",
  ABANDONED = "ABANDONED"
}

// Domain Events
export class ShoppingCartCreated extends DomainEvent {
  constructor(
    public readonly cartId: CartId,
    public readonly customerId: CustomerId
  ) {
    super();
  }
}

export class ItemAddedToCart extends DomainEvent {
  constructor(
    public readonly cartId: CartId,
    public readonly productId: ProductId,
    public readonly quantity: number,
    public readonly price: Money
  ) {
    super();
  }
}

export class ItemRemovedFromCart extends DomainEvent {
  constructor(
    public readonly cartId: CartId,
    public readonly productId: ProductId
  ) {
    super();
  }
}

export class CartCheckedOut extends DomainEvent {
  constructor(
    public readonly cartId: CartId,
    public readonly customerId: CustomerId,
    public readonly total: Money
  ) {
    super();
  }
}

// Cart Item Entity (within aggregate)
class CartItem extends Entity<CartItemId> {
  private productId: ProductId;
  private quantity: number;
  private unitPrice: Money;
  private addedAt: Date;
  
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
    this.addedAt = new Date();
  }
  
  static create(
    productId: ProductId,
    quantity: number,
    unitPrice: Money
  ): CartItem {
    if (quantity <= 0) {
      throw new Error("Quantity must be positive");
    }
    
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
  
  increaseQuantity(amount: number): Result<void> {
    return this.updateQuantity(this.quantity + amount);
  }
  
  decreaseQuantity(amount: number): Result<void> {
    return this.updateQuantity(this.quantity - amount);
  }
  
  getProductId(): ProductId {
    return this.productId;
  }
  
  getQuantity(): number {
    return this.quantity;
  }
  
  getUnitPrice(): Money {
    return this.unitPrice;
  }
  
  getSubtotal(): Money {
    return this.unitPrice.multiply(this.quantity);
  }
  
  getAddedAt(): Date {
    return this.addedAt;
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

// Shopping Cart Aggregate Root
export class ShoppingCart extends AggregateRoot<CartId> {
  private static readonly MAX_ITEMS = 50;
  private static readonly MAX_QUANTITY_PER_ITEM = 100;
  private static readonly EXPIRY_HOURS = 24;
  
  private customerId: CustomerId;
  private items: CartItem[];
  private status: CartStatus;
  private createdAt: Date;
  private lastModifiedAt: Date;
  
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
  
  // Factory method
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
  
  // Reconstitution for persistence
  static reconstitute(
    id: CartId,
    customerId: CustomerId,
    items: Array<{
      productId: ProductId;
      quantity: number;
      unitPrice: Money;
    }>,
    status: CartStatus,
    createdAt: Date,
    lastModifiedAt: Date
  ): ShoppingCart {
    const cart = new ShoppingCart(id, customerId);
    
    cart.items = items.map(item =>
      CartItem.create(
        item.productId,
        item.quantity,
        item.unitPrice
      )
    );
    
    cart.status = status;
    cart.createdAt = createdAt;
    cart.lastModifiedAt = lastModifiedAt;
    
    return cart;
  }
  
  // Business methods
  addItem(
    productId: ProductId,
    quantity: number,
    price: Money
  ): Result<void> {
    // Check cart status
    if (this.status !== CartStatus.ACTIVE) {
      return Result.fail("Cannot add items to inactive cart");
    }
    
    // Validate quantity
    if (quantity <= 0) {
      return Result.fail("Quantity must be positive");
    }
    
    // Check cart expiry
    if (this.isExpired()) {
      this.expire();
      return Result.fail("Cart has expired");
    }
    
    // Check maximum items invariant
    const existingItem = this.findItem(productId);
    
    if (!existingItem) {
      this.enforceInvariant(
        this.items.length < ShoppingCart.MAX_ITEMS,
        `Cart cannot contain more than ${ShoppingCart.MAX_ITEMS} different items`
      );
    }
    
    // Add or update item
    if (existingItem) {
      const newQuantity = existingItem.getQuantity() + quantity;
      
      if (newQuantity > ShoppingCart.MAX_QUANTITY_PER_ITEM) {
        return Result.fail(
          `Total quantity cannot exceed ${ShoppingCart.MAX_QUANTITY_PER_ITEM}`
        );
      }
      
      const result = existingItem.updateQuantity(newQuantity);
      if (result.isFailure) {
        return result;
      }
    } else {
      const newItem = CartItem.create(
        productId,
        quantity,
        price
      );
      
      this.items.push(newItem);
    }
    
    this.updateLastModified();
    
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
    this.updateLastModified();
    
    this.trackChange(
      new ItemRemovedFromCart(this.id, productId)
    );
    
    return Result.ok();
  }
  
  updateItemQuantity(
    productId: ProductId,
    quantity: number
  ): Result<void> {
    if (this.status !== CartStatus.ACTIVE) {
      return Result.fail("Cannot update items in inactive cart");
    }
    
    const item = this.findItem(productId);
    if (!item) {
      return Result.fail("Item not found in cart");
    }
    
    if (quantity === 0) {
      return this.removeItem(productId);
    }
    
    const result = item.updateQuantity(quantity);
    if (result.isFailure) {
      return result;
    }
    
    this.updateLastModified();
    
    this.trackChange(
      new ItemQuantityUpdated(
        this.id,
        productId,
        quantity
      )
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
    
    if (this.isExpired()) {
      this.expire();
      return Result.fail("Cart has expired");
    }
    
    const total = this.calculateTotal();
    this.status = CartStatus.CHECKED_OUT;
    this.updateLastModified();
    
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
  
  abandon(): void {
    if (this.status === CartStatus.ACTIVE) {
      this.status = CartStatus.ABANDONED;
      this.updateLastModified();
      
      this.trackChange(
        new CartAbandoned(this.id)
      );
    }
  }
  
  // Query methods
  getCustomerId(): CustomerId {
    return this.customerId;
  }
  
  getItems(): ReadonlyArray<{
    productId: ProductId;
    quantity: number;
    unitPrice: Money;
    subtotal: Money;
  }> {
    return this.items.map(item => ({
      productId: item.getProductId(),
      quantity: item.getQuantity(),
      unitPrice: item.getUnitPrice(),
      subtotal: item.getSubtotal()
    }));
  }
  
  getItemCount(): number {
    return this.items.reduce(
      (count, item) => count + item.getQuantity(),
      0
    );
  }
  
  getTotal(): Money {
    return this.calculateTotal();
  }
  
  getStatus(): CartStatus {
    return this.status;
  }
  
  isEmpty(): boolean {
    return this.items.length === 0;
  }
  
  isActive(): boolean {
    return this.status === CartStatus.ACTIVE;
  }
  
  getCreatedAt(): Date {
    return this.createdAt;
  }
  
  getLastModifiedAt(): Date {
    return this.lastModifiedAt;
  }
  
  // Private helper methods
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
  
  private updateLastModified(): void {
    this.lastModifiedAt = new Date();
  }
  
  private isExpired(): boolean {
    const expiryTime = new Date(this.lastModifiedAt);
    expiryTime.setHours(
      expiryTime.getHours() + ShoppingCart.EXPIRY_HOURS
    );
    
    return new Date() > expiryTime;
  }
  
  private expire(): void {
    this.status = CartStatus.EXPIRED;
    this.trackChange(new CartExpired(this.id));
  }
}
```

### Aggregate Repository Interface

```typescript
export interface AggregateRepository<T extends AggregateRoot<any>> {
  findById(id: EntityId): Promise<T | null>;
  save(aggregate: T): Promise<void>;
  delete(id: EntityId): Promise<void>;
}

// Shopping Cart Repository
export interface ShoppingCartRepository 
  extends AggregateRepository<ShoppingCart> {
  findById(id: CartId): Promise<ShoppingCart | null>;
  findByCustomerId(customerId: CustomerId): Promise<ShoppingCart[]>;
  findActiveByCustomerId(customerId: CustomerId): Promise<ShoppingCart | null>;
  save(cart: ShoppingCart): Promise<void>;
  delete(id: CartId): Promise<void>;
}

// Implementation with event publishing
export class ShoppingCartRepositoryImpl implements ShoppingCartRepository {
  constructor(
    private db: Database,
    private eventBus: EventBus
  ) {}
  
  async findById(id: CartId): Promise<ShoppingCart | null> {
    const data = await this.db.shoppingCarts.findUnique({
      where: { id: id.value },
      include: { items: true }
    });
    
    if (!data) {
      return null;
    }
    
    return this.reconstitute(data);
  }
  
  async save(cart: ShoppingCart): Promise<void> {
    const data = this.toPersistence(cart);
    
    await this.db.transaction(async (tx) => {
      // Save aggregate
      await tx.shoppingCarts.upsert({
        where: { id: data.id },
        create: data,
        update: data
      });
      
      // Delete and recreate items (simpler than complex diffing)
      await tx.cartItems.deleteMany({
        where: { cartId: data.id }
      });
      
      if (data.items.length > 0) {
        await tx.cartItems.createMany({
          data: data.items
        });
      }
    });
    
    // Publish domain events
    const events = cart.getDomainEvents();
    for (const event of events) {
      await this.eventBus.publish(event);
    }
    
    // Clear events after publishing
    cart.clearDomainEvents();
  }
  
  private reconstitute(data: any): ShoppingCart {
    const items = data.items.map((item: any) => ({
      productId: ProductId.fromString(item.productId),
      quantity: item.quantity,
      unitPrice: Money.fromCents(item.unitPriceCents)
    }));
    
    return ShoppingCart.reconstitute(
      CartId.fromString(data.id),
      CustomerId.fromString(data.customerId),
      items,
      data.status as CartStatus,
      new Date(data.createdAt),
      new Date(data.lastModifiedAt)
    );
  }
  
  private toPersistence(cart: ShoppingCart): any {
    const items = cart.getItems();
    
    return {
      id: cart.getId().value,
      customerId: cart.getCustomerId().value,
      status: cart.getStatus(),
      createdAt: cart.getCreatedAt(),
      lastModifiedAt: cart.getLastModifiedAt(),
      items: items.map((item, index) => ({
        id: `${cart.getId().value}_${index}`,
        cartId: cart.getId().value,
        productId: item.productId.value,
        quantity: item.quantity,
        unitPriceCents: item.unitPrice.toCents()
      }))
    };
  }
}
```

### Domain Service for Aggregate Coordination

```typescript
export class OrderFulfillmentService {
  constructor(
    private orderRepo: OrderRepository,
    private paymentRepo: PaymentRepository,
    private inventoryRepo: InventoryRepository,
    private shipmentRepo: ShipmentRepository,
    private eventBus: EventBus
  ) {}
  
  async fulfillOrder(orderId: OrderId): Promise<Result<void>> {
    // Step 1: Load order aggregate
    const order = await this.orderRepo.findById(orderId);
    if (!order) {
      return Result.fail("Order not found");
    }
    
    // Step 2: Create saga to coordinate aggregates
    const saga = new OrderFulfillmentSaga(orderId);
    
    try {
      // Reserve inventory (separate aggregate)
      const reservationResult = await this.reserveInventory(order);
      if (reservationResult.isFailure) {
        return Result.fail(reservationResult.error);
      }
      saga.recordInventoryReserved(reservationResult.value);
      
      // Process payment (separate aggregate)
      const paymentResult = await this.processPayment(order);
      if (paymentResult.isFailure) {
        await this.compensate(saga);
        return Result.fail(paymentResult.error);
      }
      saga.recordPaymentProcessed(paymentResult.value);
      
      // Create shipment (separate aggregate)
      const shipmentResult = await this.createShipment(order);
      if (shipmentResult.isFailure) {
        await this.compensate(saga);
        return Result.fail(shipmentResult.error);
      }
      saga.recordShipmentCreated(shipmentResult.value);
      
      // Mark order as fulfilled
      order.markAsFulfilled();
      await this.orderRepo.save(order);
      
      // Publish success event
      await this.eventBus.publish(
        new OrderFulfilled(orderId, Date.now())
      );
      
      return Result.ok();
      
    } catch (error) {
      // Compensate on any failure
      await this.compensate(saga);
      return Result.fail(`Order fulfillment failed: ${error.message}`);
    }
  }
  
  private async reserveInventory(
    order: Order
  ): Promise<Result<ReservationId>> {
    const reservations: InventoryReservation[] = [];
    
    for (const item of order.getItems()) {
      const inventory = await this.inventoryRepo.findByProductId(
        item.productId
      );
      
      if (!inventory) {
        await this.rollbackReservations(reservations);
        return Result.fail(`Product ${item.productId} not found`);
      }
      
      const result = inventory.reserve(item.quantity);
      if (result.isFailure) {
        await this.rollbackReservations(reservations);
        return Result.fail(result.error);
      }
      
      await this.inventoryRepo.save(inventory);
      reservations.push(result.value);
    }
    
    return Result.ok(ReservationId.generate());
  }
  
  private async compensate(saga: OrderFulfillmentSaga): Promise<void> {
    // Reverse all completed steps
    const compensations = saga.getCompensations();
    
    for (const compensation of compensations) {
      try {
        await compensation.execute();
      } catch (error) {
        // Log but continue - best effort compensation
        console.error(`Compensation failed: ${error}`);
      }
    }
  }
}
```

### Event-Sourced Aggregate Implementation

```typescript
export abstract class EventSourcedAggregateRoot<T extends EntityId> 
  extends AggregateRoot<T> {
  
  private version: number = 0;
  private changes: DomainEvent[] = [];
  
  protected constructor(id: T) {
    super(id);
  }
  
  // Reconstitute from events
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

// Event-sourced cart example
export class EventSourcedCart extends EventSourcedAggregateRoot<CartId> {
  private customerId!: CustomerId;
  private items: Map<string, CartItem> = new Map();
  private status!: CartStatus;
  
  static create(customerId: CustomerId): EventSourcedCart {
    const cart = new EventSourcedCart(CartId.generate());
    
    cart.applyChange(
      new CartCreated(cart.id.value, customerId.value)
    );
    
    return cart;
  }
  
  static fromEvents(events: DomainEvent[]): EventSourcedCart {
    return EventSourcedAggregateRoot.reconstitute(
      events,
      id => new EventSourcedCart(id as CartId)
    );
  }
  
  addItem(productId: ProductId, quantity: number, price: Money): void {
    if (this.status !== CartStatus.ACTIVE) {
      throw new Error("Cannot add items to inactive cart");
    }
    
    this.applyChange(
      new ItemAddedToCart(
        this.id.value,
        productId.value,
        quantity,
        price.toJSON()
      )
    );
  }
  
  // Event handlers
  private onCartCreated(event: CartCreated): void {
    this.customerId = CustomerId.fromString(event.customerId);
    this.status = CartStatus.ACTIVE;
  }
  
  private onItemAddedToCart(event: ItemAddedToCart): void {
    const item = CartItem.create(
      ProductId.fromString(event.productId),
      event.quantity,
      Money.fromJSON(event.price)
    );
    
    this.items.set(event.productId, item);
  }
}
```

### Testing Aggregates

```typescript
describe("ShoppingCart Aggregate", () => {
  describe("Adding items", () => {
    it("should add new item to empty cart", () => {
      // Arrange
      const customerId = CustomerId.generate();
      const cart = ShoppingCart.create(customerId);
      const productId = ProductId.generate();
      const price = Money.fromCents(1000);
      
      // Act
      const result = cart.addItem(productId, 2, price);
      
      // Assert
      expect(result.isSuccess).toBe(true);
      expect(cart.getItemCount()).toBe(2);
      expect(cart.getTotal().toCents()).toBe(2000);
      
      // Verify events
      const events = cart.getDomainEvents();
      expect(events).toHaveLength(2);
      expect(events[1]).toBeInstanceOf(ItemAddedToCart);
    });
    
    it("should enforce maximum items invariant", () => {
      // Arrange
      const cart = ShoppingCart.create(CustomerId.generate());
      
      // Add 50 items (maximum)
      for (let i = 0; i < 50; i++) {
        cart.addItem(
          ProductId.generate(),
          1,
          Money.fromCents(100)
        );
      }
      
      // Act & Assert
      expect(() => {
        cart.addItem(
          ProductId.generate(),
          1,
          Money.fromCents(100)
        );
      }).toThrow("Cart cannot contain more than 50 different items");
    });
  });
  
  describe("Checkout", () => {
    it("should prevent checkout of empty cart", () => {
      // Arrange
      const cart = ShoppingCart.create(CustomerId.generate());
      
      // Act
      const result = cart.checkout();
      
      // Assert
      expect(result.isFailure).toBe(true);
      expect(result.error).toBe("Cannot checkout empty cart");
    });
    
    it("should transition to checked out status", () => {
      // Arrange
      const cart = ShoppingCart.create(CustomerId.generate());
      cart.addItem(
        ProductId.generate(),
        1,
        Money.fromCents(1000)
      );
      
      // Act
      const result = cart.checkout();
      
      // Assert
      expect(result.isSuccess).toBe(true);
      expect(cart.getStatus()).toBe(CartStatus.CHECKED_OUT);
      
      // Verify no further modifications allowed
      const addResult = cart.addItem(
        ProductId.generate(),
        1,
        Money.fromCents(100)
      );
      expect(addResult.isFailure).toBe(true);
    });
  });
});
```

## Performance Optimization Patterns

### Read Model Projection

```typescript
export class CartSummaryProjection {
  constructor(private db: Database) {}
  
  async handle(event: DomainEvent): Promise<void> {
    if (event instanceof ShoppingCartCreated) {
      await this.db.cartSummaries.create({
        data: {
          cartId: event.cartId.value,
          customerId: event.customerId.value,
          itemCount: 0,
          totalCents: 0,
          status: CartStatus.ACTIVE,
          createdAt: event.occurredAt
        }
      });
    }
    
    if (event instanceof ItemAddedToCart) {
      const summary = await this.db.cartSummaries.findUnique({
        where: { cartId: event.cartId.value }
      });
      
      if (summary) {
        await this.db.cartSummaries.update({
          where: { cartId: event.cartId.value },
          data: {
            itemCount: summary.itemCount + event.quantity,
            totalCents: summary.totalCents + 
              (event.price.toCents() * event.quantity),
            lastModifiedAt: event.occurredAt
          }
        });
      }
    }
    
    if (event instanceof CartCheckedOut) {
      await this.db.cartSummaries.update({
        where: { cartId: event.cartId.value },
        data: {
          status: CartStatus.CHECKED_OUT,
          checkedOutAt: event.occurredAt
        }
      });
    }
  }
}

// Query service using read model
export class CartQueryService {
  constructor(private db: Database) {}
  
  async findActiveCartsByCustomer(
    customerId: CustomerId
  ): Promise<CartSummary[]> {
    const summaries = await this.db.cartSummaries.findMany({
      where: {
        customerId: customerId.value,
        status: CartStatus.ACTIVE
      },
      orderBy: { lastModifiedAt: 'desc' }
    });
    
    return summaries.map(s => new CartSummary(
      s.cartId,
      s.customerId,
      s.itemCount,
      Money.fromCents(s.totalCents),
      s.status,
      s.createdAt,
      s.lastModifiedAt
    ));
  }
}
```

This appendix provides the complete technical implementation details for aggregate design, including base classes, full examples, repository patterns, coordination between aggregates, event sourcing, testing strategies, and performance optimizations.