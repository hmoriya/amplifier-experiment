---
bundle:
  name: parasol-bc-architecture-patterns
  version: 1.0.0
  description: Architecture patterns for modular Bounded Context design
  
includes:
  - bundle: ./bc-modular-design.md
  
config:
  architecture_patterns:
    - hexagonal
    - clean-architecture
    - ports-and-adapters
    - event-driven
    - cqrs-es
    - modular-monolith
---

# BC Architecture Patterns for Modular Design

モジュラー化されたBounded Contextのアーキテクチャパターン集です。

## 基本原則

### 1. モジュール独立性
- 各モジュールは独立してデプロイ・テスト可能
- 契約ベースの通信
- 循環依存の禁止

### 2. 明確な境界
- パブリックAPIとプライベート実装の分離
- ドメインロジックの保護
- インフラストラクチャからの独立

## アーキテクチャパターン

### 1. Hexagonal Architecture (Ports and Adapters)

```yaml
# architecture/hexagonal-pattern.yaml
bounded_context:
  name: ProductManagement
  
  core:
    domain:
      location: modules/domain/
      contains:
        - entities
        - value_objects
        - domain_services
        - domain_events
        
    application:
      location: modules/application/
      contains:
        - use_cases
        - application_services
        - ports (interfaces)
        
  adapters:
    primary:  # 外部からBCを駆動
      - type: rest_api
        location: modules/adapters/api/rest/
        implements: ports.api
        
      - type: graphql_api
        location: modules/adapters/api/graphql/
        implements: ports.api
        
      - type: grpc_api
        location: modules/adapters/api/grpc/
        implements: ports.api
        
      - type: frontend_react
        location: modules/adapters/frontend/react/
        implements: ports.ui
        
      - type: frontend_vue
        location: modules/adapters/frontend/vue/
        implements: ports.ui
        
    secondary:  # BCが外部を駆動
      - type: postgresql
        location: modules/adapters/persistence/postgresql/
        implements: ports.repository
        
      - type: mongodb
        location: modules/adapters/persistence/mongodb/
        implements: ports.repository
        
      - type: event_publisher
        location: modules/adapters/events/publisher/
        implements: ports.event_bus
```

#### 実装例

```typescript
// modules/domain/entities/product.ts
export class Product {
  constructor(
    private readonly id: ProductId,
    private name: ProductName,
    private price: Money,
    private category: Category
  ) {}
  
  changePrice(newPrice: Money): DomainEvent[] {
    this.price = newPrice;
    return [new ProductPriceChanged(this.id, newPrice)];
  }
}

// modules/application/ports/product-repository.ts
export interface ProductRepository {
  findById(id: ProductId): Promise<Product | null>;
  save(product: Product): Promise<void>;
  findByCategory(category: Category): Promise<Product[]>;
}

// modules/application/use-cases/update-product-price.ts
export class UpdateProductPriceUseCase {
  constructor(
    private repository: ProductRepository,
    private eventBus: EventBus
  ) {}
  
  async execute(productId: string, newPrice: number): Promise<void> {
    const product = await this.repository.findById(new ProductId(productId));
    if (!product) throw new ProductNotFoundError();
    
    const events = product.changePrice(new Money(newPrice));
    await this.repository.save(product);
    await this.eventBus.publishAll(events);
  }
}

// modules/adapters/api/graphql/resolvers/product.resolver.ts
@Resolver('Product')
export class ProductResolver {
  constructor(
    private updatePriceUseCase: UpdateProductPriceUseCase
  ) {}
  
  @Mutation()
  async updateProductPrice(
    @Args('productId') productId: string,
    @Args('price') price: number
  ): Promise<boolean> {
    await this.updatePriceUseCase.execute(productId, price);
    return true;
  }
}
```

### 2. Clean Architecture Pattern

```yaml
# architecture/clean-architecture.yaml
layers:
  entities:
    location: modules/entities/
    dependencies: []  # 依存なし
    contains:
      - domain_models
      - business_rules
      
  use_cases:
    location: modules/use-cases/
    dependencies: [entities]
    contains:
      - application_business_rules
      - use_case_interactors
      
  interface_adapters:
    location: modules/interface-adapters/
    dependencies: [use_cases, entities]
    contains:
      - controllers
      - presenters
      - gateways
      
  frameworks_and_drivers:
    location: modules/frameworks/
    dependencies: [interface_adapters]
    contains:
      - web_framework
      - database
      - ui_framework
      
flow_of_control:
  - UI/API → Controller → UseCase → Entity
  - Entity → UseCase → Presenter → UI/API
```

### 3. Event-Driven Modular Architecture

```yaml
# architecture/event-driven-modular.yaml
modules:
  product_catalog:
    publishes:
      - ProductCreated
      - ProductUpdated
      - ProductDeleted
      - PriceChanged
      
    subscribes:
      - InventoryUpdated
      - CategoryChanged
      
  pricing_engine:
    publishes:
      - PriceCalculated
      - DiscountApplied
      
    subscribes:
      - ProductCreated
      - MarketConditionsChanged
      
  inventory_management:
    publishes:
      - InventoryUpdated
      - StockDepleted
      
    subscribes:
      - ProductSold
      - ProductRestocked
      
event_bus:
  type: async
  implementation: kafka
  serialization: protobuf
  
event_store:
  type: event-sourcing
  implementation: eventstore-db
```

#### Event-Driven実装例

```typescript
// modules/domain/events/product-events.ts
export interface DomainEvent {
  aggregateId: string;
  eventType: string;
  eventVersion: number;
  occurredAt: Date;
}

export class ProductPriceChanged implements DomainEvent {
  eventType = 'ProductPriceChanged';
  eventVersion = 1;
  occurredAt = new Date();
  
  constructor(
    public aggregateId: string,
    public oldPrice: Money,
    public newPrice: Money,
    public reason: string
  ) {}
}

// modules/adapters/events/kafka-event-bus.ts
export class KafkaEventBus implements EventBus {
  async publish(event: DomainEvent): Promise<void> {
    const topic = this.getTopicForEvent(event);
    await this.producer.send({
      topic,
      messages: [{
        key: event.aggregateId,
        value: JSON.stringify(event),
        headers: {
          eventType: event.eventType,
          eventVersion: event.eventVersion.toString()
        }
      }]
    });
  }
  
  async subscribe(eventType: string, handler: EventHandler): Promise<void> {
    await this.consumer.subscribe({ topic: eventType });
    await this.consumer.run({
      eachMessage: async ({ message }) => {
        const event = JSON.parse(message.value.toString());
        await handler.handle(event);
      }
    });
  }
}
```

### 4. CQRS + Event Sourcing Pattern

```yaml
# architecture/cqrs-es-pattern.yaml
command_side:
  aggregates:
    location: modules/command/aggregates/
    responsibilities:
      - business_rules_enforcement
      - event_generation
      - state_transitions
      
  command_handlers:
    location: modules/command/handlers/
    responsibilities:
      - command_validation
      - aggregate_loading
      - event_persistence
      
  event_store:
    location: modules/command/event-store/
    implementation: postgres_jsonb
    
query_side:
  projections:
    location: modules/query/projections/
    types:
      - product_list_view
      - product_detail_view
      - category_summary_view
      
  query_handlers:
    location: modules/query/handlers/
    responsibilities:
      - query_optimization
      - caching
      - pagination
      
  read_models:
    location: modules/query/read-models/
    storage:
      - postgresql: normalized_views
      - elasticsearch: search_indices
      - redis: cache_layer
```

### 5. Modular Monolith Pattern

```yaml
# architecture/modular-monolith.yaml
structure:
  shared_kernel:
    location: shared/
    contains:
      - value_objects
      - common_interfaces
      - base_classes
      
  modules:
    product_management:
      location: modules/product-management/
      public_api: modules/product-management/api/
      internal: modules/product-management/internal/
      database_schema: product_mgmt
      
    order_management:
      location: modules/order-management/
      public_api: modules/order-management/api/
      internal: modules/order-management/internal/
      database_schema: order_mgmt
      
    customer_management:
      location: modules/customer-management/
      public_api: modules/customer-management/api/
      internal: modules/customer-management/internal/
      database_schema: customer_mgmt
      
  module_communication:
    sync:
      - method: direct_call
        rule: only_through_public_api
        
    async:
      - method: in_memory_events
        implementation: MediatR
        
  deployment:
    type: single_deployment_unit
    future_path: microservices_extraction
```

## モジュール間通信パターン

### 1. 同期通信

```typescript
// modules/order-management/api/order-service.interface.ts
export interface IOrderService {
  createOrder(customerId: string, items: OrderItem[]): Promise<OrderId>;
  getOrderStatus(orderId: string): Promise<OrderStatus>;
}

// modules/product-management/internal/order-integration.ts
export class OrderIntegration {
  constructor(private orderService: IOrderService) {}
  
  async checkProductAvailability(items: OrderItem[]): Promise<boolean> {
    // OrderServiceの公開APIのみを使用
    return this.orderService.validateItems(items);
  }
}
```

### 2. 非同期通信

```typescript
// modules/shared/events/integration-events.ts
export class OrderPlacedEvent {
  constructor(
    public orderId: string,
    public customerId: string,
    public items: Array<{productId: string; quantity: number}>,
    public totalAmount: Money
  ) {}
}

// modules/inventory-management/handlers/order-events.handler.ts
@EventHandler(OrderPlacedEvent)
export class OrderPlacedHandler {
  async handle(event: OrderPlacedEvent): Promise<void> {
    for (const item of event.items) {
      await this.inventoryService.reserveStock(
        item.productId,
        item.quantity
      );
    }
  }
}
```

## アンチパターンと対策

### 1. 循環依存

```yaml
# ❌ アンチパターン
module_a:
  depends_on: [module_b]
  
module_b:
  depends_on: [module_a]
  
# ✅ 解決策
shared_contracts:
  location: contracts/
  contains: [interfaces, events]
  
module_a:
  depends_on: [shared_contracts]
  
module_b:
  depends_on: [shared_contracts]
```

### 2. 過度な結合

```yaml
# ❌ アンチパターン
order_module:
  directly_accesses:
    - product_module.database
    - customer_module.internal_services
    
# ✅ 解決策
order_module:
  uses:
    - product_module.public_api
    - customer_module.public_api
```

## CLI統合

```bash
# アーキテクチャパターンでBC生成
parasol bc generate ProductManagement \
  --architecture hexagonal \
  --modules domain,api,persistence,frontend \
  --adapters rest,graphql,postgresql,react

# アーキテクチャ検証
parasol bc validate ProductManagement \
  --check circular-dependencies \
  --check module-boundaries \
  --check public-api-usage

# アーキテクチャ可視化
parasol bc visualize ProductManagement \
  --format mermaid \
  --show dependencies,events,apis
```

## 移行パス

```yaml
migration_paths:
  modular_monolith_to_microservices:
    steps:
      - identify_seams
      - extract_shared_kernel
      - define_service_boundaries
      - implement_api_gateway
      - gradual_extraction
      
  layered_to_hexagonal:
    steps:
      - identify_ports
      - extract_adapters
      - isolate_domain
      - implement_dependency_inversion
      
  synchronous_to_event_driven:
    steps:
      - identify_integration_points
      - define_events
      - implement_event_bus
      - gradual_decoupling
```