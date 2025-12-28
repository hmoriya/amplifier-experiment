# Appendix: Chapter 20 Implementation Details

## Technical Implementation Reference

This appendix contains the detailed code implementations referenced in Chapter 20. These examples show how the domain modeling concepts translate into TypeScript code using Domain-Driven Design patterns.

## Building Ubiquitous Language

```typescript
export interface UbiquitousLanguage {
  // Term definitions
  terms: Map<string, TermDefinition>;
  
  // Contextual meanings
  contextualMeanings: Map<string, Map<BoundedContext, Meaning>>;
  
  // Term relationships
  relationships: TermRelationship[];
  
  // Evolution history
  evolution: LanguageEvolution[];
}

export class LanguageBuilder {
  buildUbiquitousLanguage(
    domainExperts: DomainExpert[],
    developers: Developer[]
  ): UbiquitousLanguage {
    // 1. Collect terms
    const collectedTerms = this.collectTermsFromStakeholders(
      [...domainExperts, ...developers]
    );
    
    // 2. Clarify meanings
    const clarifiedTerms = this.clarifyMeanings(
      collectedTerms,
      domainExperts
    );
    
    // 3. Identify contexts
    const contextualizedTerms = this.identifyContexts(
      clarifiedTerms
    );
    
    // 4. Define relationships
    const relationships = this.defineRelationships(
      contextualizedTerms
    );
    
    // 5. Validate and refine
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
      // Expert dialogue sessions
      const expertOpinions = experts.map(expert => 
        this.conductClarificationSession(term, expert)
      );
      
      // Build consensus
      const consensus = this.buildConsensus(expertOpinions);
      
      // Gather concrete examples
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

## Domain Model Discovery Process

```typescript
export class DomainModelDiscovery {
  async discoverModel(
    domain: BusinessDomain
  ): Promise<DomainModel> {
    // 1. Knowledge gathering
    const knowledge = await this.gatherDomainKnowledge(domain);
    
    // 2. Concept extraction
    const concepts = await this.extractConcepts(knowledge);
    
    // 3. Behavior identification
    const behaviors = await this.identifyBehaviors(concepts);
    
    // 4. Rule discovery
    const rules = await this.discoverBusinessRules(concepts);
    
    // 5. Model construction
    return this.constructModel(concepts, behaviors, rules);
  }
  
  private async extractConcepts(
    knowledge: DomainKnowledge
  ): Promise<Concept[]> {
    // Event storming
    const events = await this.conductEventStorming(knowledge);
    
    // Command identification
    const commands = this.identifyCommands(events);
    
    // Entity discovery
    const entities = this.discoverEntities(events, commands);
    
    // Value object identification
    const valueObjects = this.identifyValueObjects(entities);
    
    // Domain service extraction
    const domainServices = this.extractDomainServices(
      events,
      commands,
      entities
    );
    
    return [...entities, ...valueObjects, ...domainServices];
  }
}
```

## Tactical DDD Patterns

### Base Entity Implementation

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
```

### Customer Entity Example

```typescript
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
  
  // Business logic
  placeOrder(order: Order): Result<void> {
    // Credit limit check
    if (!this.hasEnoughCredit(order.totalAmount)) {
      return Result.fail("Insufficient credit limit");
    }
    
    // Status check
    if (!this.canPlaceOrder()) {
      return Result.fail("Customer status does not allow ordering");
    }
    
    this.addDomainEvent(
      new OrderPlacedEvent(this.id, order.id)
    );
    
    return Result.ok();
  }
  
  private hasEnoughCredit(orderAmount: Money): boolean {
    // Get current order total (via repository)
    const currentOrderTotal = this.getCurrentOrderTotal();
    const projectedTotal = currentOrderTotal.add(orderAmount);
    
    return projectedTotal.lessThanOrEqual(this.creditLimit);
  }
  
  private canPlaceOrder(): boolean {
    return this.status === CustomerStatus.ACTIVE;
  }
}
```

### Base Value Object Implementation

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
```

### Money Value Object Example

```typescript
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
```

### Email Value Object Example

```typescript
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

## Domain Service Implementation

```typescript
export interface DomainService {
  // Domain services are stateless
}

// Example: Pricing Service
export class PricingService implements DomainService {
  calculatePrice(
    product: Product,
    quantity: number,
    customer: Customer,
    promotions: Promotion[]
  ): PricingResult {
    // Base price calculation
    const basePrice = product.getPrice().multiply(quantity);
    
    // Customer-specific discount
    const customerDiscount = this.calculateCustomerDiscount(
      customer,
      basePrice
    );
    
    // Promotion discount
    const promotionDiscount = this.calculatePromotionDiscount(
      product,
      quantity,
      promotions
    );
    
    // Final price calculation
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
    
    // Select best promotion
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

## Aggregate Design

### Aggregate Root Base Class

```typescript
export abstract class AggregateRoot<ID extends EntityId> extends Entity<ID> {
  // Aggregate root is the only external entry point
  
  protected validateInvariants(): void {
    // Validate aggregate-wide invariants
  }
  
  protected apply(event: DomainEvent): void {
    // Apply event and change state
    this.addDomainEvent(event);
    this.validateInvariants();
  }
}
```

### Order Aggregate Example

```typescript
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
    
    // Add initial order lines
    props.items.forEach(item => {
      order.addOrderLine(item.productId, item.quantity);
    });
    
    order.apply(
      new OrderCreatedEvent(orderId, props)
    );
    
    return order;
  }
  
  // Business methods
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
    // Order amount limit check
    const totalAmount = this.calculateTotalAmount();
    if (totalAmount.greaterThan(Money.create(10000000))) {
      throw new Error("Order amount exceeds maximum limit");
    }
    
    // Duplicate order line check
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

// Order Line (Entity within Aggregate)
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
      unitPrice: Money.create(0) // Set by pricing service later
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

## Domain Events

### Base Domain Event

```typescript
export abstract class DomainEvent {
  readonly occurredOn: Date;
  readonly aggregateId: string;
  
  constructor(aggregateId: string) {
    this.occurredOn = new Date();
    this.aggregateId = aggregateId;
  }
}
```

### Order Events

```typescript
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
```

### Event Handlers

```typescript
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

## Repository Pattern

### Repository Interface

```typescript
export interface Repository<T extends AggregateRoot<any>, ID extends EntityId> {
  findById(id: ID): Promise<T | null>;
  save(aggregate: T): Promise<void>;
  delete(id: ID): Promise<void>;
}
```

### Customer Repository

```typescript
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
    
    // Publish domain events
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

## Specification Pattern

### Base Specification

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
```

### Customer Specifications

```typescript
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

// Combining specifications
const canPlaceHighValueOrder = new PremiumCustomerSpecification()
  .or(
    new ActiveCustomerSpecification()
      .and(new HasGoodCreditHistorySpecification())
  );

// Usage
if (canPlaceHighValueOrder.isSatisfiedBy(customer)) {
  // Allow high-value order
}
```

## Model Evolution

```typescript
export class ModelEvolution {
  evolveDomainModel(
    currentModel: DomainModel,
    insights: DomainInsight[]
  ): EvolvedModel {
    // 1. Discover new concepts
    const newConcepts = this.discoverNewConcepts(insights);
    
    // 2. Refine existing concepts
    const refinedConcepts = this.refineConcepts(
      currentModel.concepts,
      insights
    );
    
    // 3. Restructure relationships
    const updatedRelationships = this.restructureRelationships(
      refinedConcepts,
      newConcepts
    );
    
    // 4. Redefine boundaries
    const newBoundaries = this.redefineBoundaries(
      refinedConcepts,
      updatedRelationships
    );
    
    // 5. Create migration plan
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

## Supporting Types and Interfaces

```typescript
interface MoneyProps {
  amount: number;
  currency: string;
}

interface CustomerProps {
  name: CustomerName;
  email: Email;
  status: CustomerStatus;
  creditLimit: Money;
  registrationDate: Date;
}

interface CreateCustomerProps {
  firstName: string;
  lastName: string;
  email: string;
  initialCreditLimit: number;
}

interface OrderProps {
  customerId: CustomerId;
  orderLines: OrderLine[];
  status: OrderStatus;
  shippingAddress: Address;
  placedAt: Date;
}

interface CreateOrderProps {
  customerId: CustomerId;
  items: Array<{
    productId: ProductId;
    quantity: number;
  }>;
  shippingAddress: Address;
}

interface OrderLineProps {
  productId: ProductId;
  quantity: number;
  unitPrice: Money;
}

interface PricingResult {
  basePrice: Money;
  customerDiscount: Money;
  promotionDiscount: Money;
  finalPrice: Money;
  appliedPromotions: Promotion[];
}

enum CustomerStatus {
  ACTIVE = 'ACTIVE',
  INACTIVE = 'INACTIVE',
  SUSPENDED = 'SUSPENDED',
  PREMIUM = 'PREMIUM'
}

enum OrderStatus {
  DRAFT = 'DRAFT',
  CONFIRMED = 'CONFIRMED',
  SHIPPED = 'SHIPPED',
  DELIVERED = 'DELIVERED',
  CANCELLED = 'CANCELLED'
}
```

## Testing Domain Models

```typescript
describe('Customer', () => {
  it('should create a new customer with active status', () => {
    const customer = Customer.create({
      firstName: 'John',
      lastName: 'Doe',
      email: 'john.doe@example.com',
      initialCreditLimit: 10000
    });
    
    expect(customer.status).toBe(CustomerStatus.ACTIVE);
    expect(customer.creditLimit.amount).toBe(10000);
  });
  
  it('should prevent orders exceeding credit limit', () => {
    const customer = Customer.create({
      firstName: 'John',
      lastName: 'Doe',
      email: 'john.doe@example.com',
      initialCreditLimit: 5000
    });
    
    const order = Order.create({
      customerId: customer.id,
      items: [{ productId: ProductId.generate(), quantity: 10 }],
      shippingAddress: testAddress
    });
    
    // Assume order total is 6000
    order.totalAmount = Money.create(6000);
    
    const result = customer.placeOrder(order);
    
    expect(result.isFailure).toBe(true);
    expect(result.error).toBe("Insufficient credit limit");
  });
});

describe('Order', () => {
  it('should progress through valid state transitions', () => {
    const order = Order.create({
      customerId: CustomerId.generate(),
      items: [{ productId: ProductId.generate(), quantity: 2 }],
      shippingAddress: testAddress
    });
    
    expect(order.status).toBe(OrderStatus.DRAFT);
    
    order.confirm();
    expect(order.status).toBe(OrderStatus.CONFIRMED);
    
    order.ship();
    expect(order.status).toBe(OrderStatus.SHIPPED);
  });
  
  it('should enforce aggregate invariants', () => {
    const order = Order.create({
      customerId: CustomerId.generate(),
      items: [],
      shippingAddress: testAddress
    });
    
    // Add order line with excessive amount
    order.addOrderLine(ProductId.generate(), 1000000);
    
    expect(() => order.validateInvariants()).toThrow(
      "Order amount exceeds maximum limit"
    );
  });
});
```

## Best Practices Summary

1. **Keep aggregates small** - Only include what needs to maintain consistency
2. **Make implicit concepts explicit** - If the domain experts talk about it, model it
3. **Use value objects liberally** - They make the model more expressive
4. **Push behavior into domain objects** - Avoid anemic models
5. **Protect invariants at aggregate boundaries** - Don't let invalid states be representable
6. **Use domain events for side effects** - Keep aggregates focused on their core responsibility
7. **Evolve the model continuously** - It's never "done"