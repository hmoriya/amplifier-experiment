---
bundle:
  name: parasol-module-communication
  version: 1.0.0
  description: Module communication patterns for loosely coupled BC design
  
includes:
  - bundle: ./bc-architecture-patterns.md
  
config:
  communication_styles:
    - synchronous
    - asynchronous
    - event-driven
    - choreography
    - orchestration
---

# Module Communication Patterns

モジュール間の疎結合な通信パターン集です。

## 通信方式の選択基準

### 同期通信を選ぶべき場合
- 即座に結果が必要
- トランザクション整合性が必要
- シンプルな要求/応答パターン
- レイテンシが許容範囲内

### 非同期通信を選ぶべき場合
- 結果を待つ必要がない
- 長時間実行される処理
- 複数のモジュールに通知が必要
- 結果整合性で十分

## 1. API Gateway Pattern

```yaml
api_gateway:
  purpose: 統一されたエントリーポイント提供
  
  structure:
    frontend_apps:
      - react_app
      - vue_app
      - mobile_app
      
    gateway:
      responsibilities:
        - authentication
        - rate_limiting
        - request_routing
        - response_aggregation
        
    backend_modules:
      - product_service
      - order_service
      - customer_service
```

### 実装例：GraphQL Federation

```typescript
// gateway/schema.ts
import { ApolloGateway } from '@apollo/gateway';

const gateway = new ApolloGateway({
  serviceList: [
    { name: 'products', url: 'http://products:4001/graphql' },
    { name: 'orders', url: 'http://orders:4002/graphql' },
    { name: 'customers', url: 'http://customers:4003/graphql' },
  ],
});

// modules/products/schema.graphql
extend type Query {
  product(id: ID!): Product
  products(filter: ProductFilter): [Product!]!
}

type Product @key(fields: "id") {
  id: ID!
  name: String!
  price: Money!
  category: Category!
}

// modules/orders/schema.graphql
extend type Order {
  # Productサービスから取得
  items: [OrderItem!]! @requires(fields: "productIds")
}
```

## 2. Service Mesh Pattern

```yaml
service_mesh:
  purpose: モジュール間通信の管理と可観測性
  
  features:
    traffic_management:
      - load_balancing
      - circuit_breaking
      - retry_policies
      
    security:
      - mutual_tls
      - authorization_policies
      
    observability:
      - distributed_tracing
      - metrics_collection
      
  implementation:
    data_plane: envoy_proxy
    control_plane: istio
```

### サイドカープロキシ設定

```yaml
# modules/product/deployment.yaml
apiVersion: v1
kind: Service
metadata:
  name: product-service
spec:
  ports:
  - port: 80
    targetPort: 8080
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: product-service
spec:
  template:
    metadata:
      annotations:
        sidecar.istio.io/inject: "true"
    spec:
      containers:
      - name: product-app
        image: product-service:latest
        ports:
        - containerPort: 8080
```

## 3. Transaction Coordination Patterns

**Note**: This section shows traditional SAGA patterns. For Parasol V5's frontend orchestration approach, see `v5-event-driven-patterns.md`.

```yaml
traditional_saga_pattern:
  purpose: 複数モジュールにまたがるトランザクション管理
  
  types:
    choreography:
      description: イベント駆動での協調
      use_case: シンプルなワークフロー
      
    orchestration:
      description: 中央制御での管理
      use_case: 複雑なビジネスプロセス
```

**Parasol V5 Alternative**:
```yaml
v5_transaction_pattern:
  purpose: フロントエンド主導のトランザクション管理
  
  approach:
    frontend_orchestration:
      description: エッジでのワークフロー管理
      benefits: [simple_debugging, immediate_feedback, user_control]
      
    optimistic_coordination:
      description: 楽観的ロックと補償ベース
      benefits: [fast_ui, graceful_degradation, no_backend_state]
```

### Choreography実装例

```typescript
// modules/order/saga/order-placement-saga.ts
export class OrderPlacementSaga {
  @StartSaga()
  async handle(command: PlaceOrderCommand): Promise<void> {
    // 1. 在庫確認
    await this.eventBus.publish(
      new CheckInventoryCommand(command.items)
    );
  }
  
  @SagaEventHandler(InventoryCheckedEvent)
  async onInventoryChecked(event: InventoryCheckedEvent): Promise<void> {
    if (!event.available) {
      await this.compensate();
      return;
    }
    
    // 2. 支払い処理
    await this.eventBus.publish(
      new ProcessPaymentCommand(event.orderId, event.amount)
    );
  }
  
  @SagaEventHandler(PaymentProcessedEvent)
  async onPaymentProcessed(event: PaymentProcessedEvent): Promise<void> {
    // 3. 配送手配
    await this.eventBus.publish(
      new ArrangeShippingCommand(event.orderId)
    );
  }
  
  @CompensationHandler()
  async compensate(): Promise<void> {
    // ロールバック処理
    await this.eventBus.publish(new CancelOrderCommand());
  }
}
```

### Orchestration実装例

```typescript
// modules/order/orchestrator/order-orchestrator.ts
export class OrderOrchestrator {
  async placeOrder(order: Order): Promise<OrderResult> {
    const saga = new SagaBuilder<OrderContext>()
      .step('check-inventory')
        .invoke(this.inventoryService.checkAvailability)
        .withCompensation(this.inventoryService.releaseReservation)
      .step('process-payment')
        .invoke(this.paymentService.charge)
        .withCompensation(this.paymentService.refund)
      .step('arrange-shipping')
        .invoke(this.shippingService.schedule)
        .withCompensation(this.shippingService.cancel)
      .build();
      
    return await saga.execute({ order });
  }
}
```

## 4. Event Streaming Pattern

```yaml
event_streaming:
  purpose: リアルタイムデータ同期とイベントソーシング
  
  architecture:
    event_producers:
      - user_activity_tracker
      - order_processor
      - inventory_updater
      
    event_broker:
      implementation: kafka
      topics:
        - user_events
        - order_events
        - inventory_events
        
    event_consumers:
      - recommendation_engine
      - analytics_processor
      - notification_service
```

### Kafka Streams実装

```typescript
// modules/analytics/streams/order-analytics-stream.ts
export class OrderAnalyticsStream {
  buildTopology(): StreamsBuilder {
    const builder = new StreamsBuilder();
    
    // 注文イベントストリーム
    const orderStream = builder
      .stream<string, OrderEvent>('order-events')
      .filter((key, event) => event.type === 'OrderPlaced');
    
    // 時間窓での集計
    const hourlyStats = orderStream
      .groupByKey()
      .windowedBy(TimeWindows.of(Duration.ofHours(1)))
      .aggregate(
        () => new OrderStats(),
        (key, event, stats) => stats.add(event),
        Materialized.as('hourly-order-stats')
      );
    
    // 結果を別トピックへ
    hourlyStats
      .toStream()
      .to('order-analytics', Produced.with(Serdes.String(), orderStatsSerde));
    
    return builder;
  }
}
```

## 5. Backend for Frontend (BFF) Pattern

```yaml
bff_pattern:
  purpose: フロントエンド固有のAPIを提供
  
  structure:
    frontends:
      web_bff:
        for: react_spa
        optimizations:
          - graphql_aggregation
          - response_shaping
          
      mobile_bff:
        for: react_native_app
        optimizations:
          - data_minimization
          - offline_support
          
      admin_bff:
        for: admin_dashboard
        features:
          - bulk_operations
          - detailed_reporting
```

### BFF実装例

```typescript
// modules/bff/web-bff/resolvers/product-page.resolver.ts
export class ProductPageResolver {
  constructor(
    private productService: ProductService,
    private reviewService: ReviewService,
    private recommendationService: RecommendationService
  ) {}
  
  // 1回のリクエストで必要な全データを取得
  @Query()
  async productPage(@Args('productId') productId: string): Promise<ProductPageData> {
    const [product, reviews, recommendations] = await Promise.all([
      this.productService.getProduct(productId),
      this.reviewService.getReviews(productId),
      this.recommendationService.getSimilarProducts(productId)
    ]);
    
    return {
      product,
      reviews: reviews.slice(0, 5), // Web用に5件に制限
      recommendations: recommendations.slice(0, 8), // 8商品表示
      meta: {
        averageRating: this.calculateAverage(reviews),
        reviewCount: reviews.length
      }
    };
  }
}
```

## 6. CQRS通信パターン

```yaml
cqrs_communication:
  command_flow:
    client → command_gateway → command_handler → aggregate → event_store
    
  query_flow:
    client → query_gateway → query_handler → read_model → response
    
  sync_flow:
    event_store → event_processor → projection_builder → read_model
```

### 実装例

```typescript
// modules/cqrs/command-gateway.ts
export class CommandGateway {
  async send<T>(command: Command): Promise<T> {
    const handler = this.handlerRegistry.getHandler(command);
    
    // 検証
    await this.validator.validate(command);
    
    // 実行
    const result = await handler.handle(command);
    
    // イベント発行
    await this.eventBus.publishAll(result.events);
    
    return result.data;
  }
}

// modules/cqrs/query-gateway.ts
export class QueryGateway {
  async query<T>(query: Query): Promise<T> {
    // キャッシュチェック
    const cached = await this.cache.get(query);
    if (cached) return cached;
    
    // クエリ実行
    const handler = this.handlerRegistry.getHandler(query);
    const result = await handler.handle(query);
    
    // キャッシュ更新
    await this.cache.set(query, result);
    
    return result;
  }
}
```

## 通信パターンの組み合わせ

```yaml
hybrid_architecture:
  user_facing:
    pattern: api_gateway + bff
    reason: 最適化されたクライアント体験
    
  inter_module:
    pattern: service_mesh + event_streaming
    reason: 信頼性とリアルタイム性の両立
    
  data_consistency:
    pattern: saga + cqrs
    reason: 分散トランザクションと読み書き分離
```

## パフォーマンス考慮事項

```yaml
performance_guidelines:
  synchronous:
    connection_pooling:
      min: 10
      max: 100
      
    timeout_settings:
      connect: 1s
      read: 5s
      
    circuit_breaker:
      failure_threshold: 50%
      timeout: 30s
      
  asynchronous:
    message_batching:
      size: 100
      time: 100ms
      
    consumer_concurrency:
      min: 1
      max: 10
      
    retention_policy:
      events: 7_days
      dead_letter: 30_days
```

## CLI統合

```bash
# 通信パターンの実装
parasol bc implement-communication ProductManagement \
  --pattern saga-orchestration \
  --modules order,inventory,payment

# 通信のモニタリング設定
parasol bc setup-monitoring ProductManagement \
  --metrics latency,throughput,error-rate \
  --tracing distributed \
  --logging structured

# 通信パターンのテスト
parasol bc test-communication ProductManagement \
  --scenarios happy-path,timeout,circuit-break \
  --load-test 1000-rps
```