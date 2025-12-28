# 付録：CQRS・イベントソーシング実装ガイド

本付録では、第22章で解説したCQRSとイベントソーシングの具体的な実装方法を示します。

## CQRSの実装

### 基本的な構造

```typescript
// 従来のCRUDアプローチ
export class TraditionalProductService {
  async getProduct(id: string): Promise<Product> {
    return await this.db.products.findById(id);
  }
  
  async updateProduct(id: string, data: UpdateData): Promise<void> {
    const product = await this.db.products.findById(id);
    product.update(data);
    await this.db.products.save(product);
  }
  
  // 読み取りと書き込みが同じモデルを使用
  // 問題：複雑なクエリニーズとビジネスロジックの混在
}

// CQRSアプローチ
export interface CQRS {
  // コマンド側（書き込み）
  commands: {
    model: "リッチなドメインモデル";
    focus: "ビジネスロジックと整合性";
    optimization: "書き込み性能";
  };
  
  // クエリ側（読み取り）
  queries: {
    model: "特化した読み取りモデル";
    focus: "表示ニーズに最適化";
    optimization: "読み取り性能";
  };
}
```

### コマンドハンドラの実装

```typescript
// コマンド側の実装
export class ProductCommandHandler {
  constructor(
    private repository: ProductRepository,
    private eventBus: EventBus
  ) {}
  
  async handle(command: UpdateProductCommand): Promise<void> {
    // リッチなドメインモデルを使用
    const product = await this.repository.findById(
      ProductId.fromString(command.productId)
    );
    
    if (!product) {
      throw new ProductNotFoundError(command.productId);
    }
    
    // ビジネスロジックの実行
    const result = product.updatePrice(
      Money.create(command.newPrice)
    );
    
    if (result.isFailure) {
      throw new BusinessRuleViolationError(result.error);
    }
    
    // 集約の保存
    await this.repository.save(product);
    
    // イベントの発行
    const events = product.getUncommittedEvents();
    for (const event of events) {
      await this.eventBus.publish(event);
    }
  }
}
```

### クエリサービスの実装

```typescript
// クエリ側の実装
export class ProductQueryService {
  constructor(
    private readDb: ReadDatabase
  ) {}
  
  async findProductDetails(
    productId: string
  ): Promise<ProductDetailsView> {
    // 表示に特化したモデルから直接取得
    return await this.readDb.query(`
      SELECT 
        p.id,
        p.name,
        p.description,
        p.price,
        p.currency,
        c.name as category_name,
        COUNT(r.id) as review_count,
        AVG(r.rating) as average_rating,
        s.quantity as stock_level
      FROM product_views p
      LEFT JOIN categories c ON p.category_id = c.id
      LEFT JOIN reviews r ON p.id = r.product_id
      LEFT JOIN stock_levels s ON p.id = s.product_id
      WHERE p.id = ?
      GROUP BY p.id
    `, [productId]);
  }
  
  async searchProducts(
    criteria: SearchCriteria
  ): Promise<ProductSearchResult[]> {
    // Elasticsearchなど、検索に特化したストアを使用
    const results = await this.searchEngine.search({
      index: 'products',
      body: {
        query: {
          bool: {
            must: [
              { match: { name: criteria.keyword } },
              { range: { price: { gte: criteria.minPrice, lte: criteria.maxPrice } } }
            ]
          }
        }
      }
    });
    
    return results.hits.map(hit => hit._source);
  }
}
```

### CQRSアーキテクチャ全体

```typescript
export class CQRSArchitecture {
  // コマンド側のコンポーネント
  commandSide = {
    // コマンドバス
    commandBus: class CommandBus {
      private handlers = new Map<string, CommandHandler>();
      
      register<T extends Command>(
        commandType: string,
        handler: CommandHandler<T>
      ): void {
        this.handlers.set(commandType, handler);
      }
      
      async dispatch<T extends Command>(command: T): Promise<void> {
        const handler = this.handlers.get(command.type);
        if (!handler) {
          throw new Error(`No handler for command: ${command.type}`);
        }
        
        await handler.handle(command);
      }
    },
    
    // コマンドハンドラ
    handlers: {
      CreateProductHandler,
      UpdateProductHandler,
      DiscontinueProductHandler
    },
    
    // ドメインモデル
    domain: {
      Product,
      ProductRepository
    }
  };
  
  // クエリ側のコンポーネント
  querySide = {
    // クエリバス
    queryBus: class QueryBus {
      private handlers = new Map<string, QueryHandler>();
      
      register<T extends Query, R>(
        queryType: string,
        handler: QueryHandler<T, R>
      ): void {
        this.handlers.set(queryType, handler);
      }
      
      async dispatch<T extends Query, R>(query: T): Promise<R> {
        const handler = this.handlers.get(query.type);
        if (!handler) {
          throw new Error(`No handler for query: ${query.type}`);
        }
        
        return await handler.handle(query);
      }
    },
    
    // クエリハンドラ
    handlers: {
      FindProductDetailsHandler,
      SearchProductsHandler,
      GetProductCatalogHandler
    },
    
    // 読み取りモデル
    readModels: {
      ProductDetailsView,
      ProductSearchView,
      ProductCatalogView
    }
  };
  
  // 同期メカニズム
  synchronization = {
    // イベントプロジェクション
    projections: class ProjectionManager {
      private projections: Projection[] = [];
      
      register(projection: Projection): void {
        this.projections.push(projection);
      }
      
      async project(event: DomainEvent): Promise<void> {
        // 並列実行で高速化
        await Promise.all(
          this.projections.map(p => p.project(event))
        );
      }
    }
  };
}
```

## イベントソーシングの実装

### イベントストアのインターフェース

```typescript
export interface EventStore {
  append(
    streamId: string,
    events: DomainEvent[],
    expectedVersion: number
  ): Promise<void>;
  
  readStream(
    streamId: string,
    fromVersion?: number
  ): Promise<StoredEvent[]>;
  
  readAll(
    fromPosition?: number
  ): Promise<StoredEvent[]>;
}

export interface StoredEvent {
  id: string;
  streamId: string;
  version: number;
  type: string;
  data: any;
  metadata: EventMetadata;
  timestamp: Date;
  position: number;
}

export interface EventMetadata {
  userId?: string;
  correlationId?: string;
  causationId?: string;
  timestamp: Date;
}
```

### PostgreSQLベースのイベントストア

```typescript
// イベントストアの実装
export class PostgresEventStore implements EventStore {
  constructor(
    private db: Database,
    private serializer: EventSerializer
  ) {}
  
  async append(
    streamId: string,
    events: DomainEvent[],
    expectedVersion: number
  ): Promise<void> {
    await this.db.transaction(async tx => {
      // 楽観的同時実行制御
      const currentVersion = await this.getCurrentVersion(tx, streamId);
      
      if (currentVersion !== expectedVersion) {
        throw new ConcurrencyError(
          `Expected version ${expectedVersion}, but was ${currentVersion}`
        );
      }
      
      // イベントの保存
      let version = currentVersion;
      for (const event of events) {
        version++;
        
        await tx.events.create({
          data: {
            streamId,
            version,
            type: event.constructor.name,
            data: this.serializer.serialize(event),
            metadata: this.createMetadata(event),
            timestamp: new Date()
          }
        });
      }
      
      // ストリームのバージョン更新
      await tx.streams.upsert({
        where: { streamId },
        create: { streamId, version },
        update: { version }
      });
    });
  }
  
  async readStream(
    streamId: string,
    fromVersion: number = 0
  ): Promise<StoredEvent[]> {
    const events = await this.db.events.findMany({
      where: {
        streamId,
        version: { gt: fromVersion }
      },
      orderBy: { version: 'asc' }
    });
    
    return events.map(e => ({
      id: e.id,
      streamId: e.streamId,
      version: e.version,
      type: e.type,
      data: this.serializer.deserialize(e.type, e.data),
      metadata: e.metadata,
      timestamp: e.timestamp,
      position: e.position
    }));
  }
  
  private async getCurrentVersion(
    tx: Transaction,
    streamId: string
  ): Promise<number> {
    const stream = await tx.streams.findUnique({
      where: { streamId }
    });
    
    return stream?.version ?? 0;
  }
}
```

### イベントソースド集約の基底クラス

```typescript
export abstract class EventSourcedAggregate<T extends EntityId> {
  protected id: T;
  protected version: number = 0;
  private uncommittedEvents: DomainEvent[] = [];
  
  constructor(id: T) {
    this.id = id;
  }
  
  // イベントの適用（状態変更）
  protected abstract applyEvent(event: DomainEvent): void;
  
  // 新しいイベントを発生させる
  protected raiseEvent(event: DomainEvent): void {
    // イベントを状態に適用
    this.applyEvent(event);
    this.version++;
    
    // 未コミットリストに追加
    this.uncommittedEvents.push(event);
  }
  
  // ストアからの再構築
  static fromEvents<A extends EventSourcedAggregate<any>>(
    ctor: new (id: EntityId) => A,
    events: DomainEvent[]
  ): A {
    if (events.length === 0) {
      throw new Error("Cannot reconstitute from empty event stream");
    }
    
    // 最初のイベントからIDを取得
    const firstEvent = events[0];
    const id = EntityId.fromString(firstEvent.aggregateId);
    
    // 集約インスタンスを作成
    const aggregate = new ctor(id);
    
    // イベントを順番に適用
    for (const event of events) {
      aggregate.applyEvent(event);
      aggregate.version++;
    }
    
    return aggregate;
  }
  
  // 未コミットイベントの取得
  getUncommittedEvents(): DomainEvent[] {
    return this.uncommittedEvents;
  }
  
  // イベントのコミット完了
  markEventsAsCommitted(): void {
    this.uncommittedEvents = [];
  }
  
  getId(): T {
    return this.id;
  }
  
  getVersion(): number {
    return this.version;
  }
}
```

### 具体的なイベントソースド集約の例

```typescript
// 実例：イベントソースド製品集約
export class EventSourcedProduct extends EventSourcedAggregate<ProductId> {
  // 状態
  private name!: string;
  private description!: string;
  private price!: Money;
  private status!: ProductStatus;
  private categoryId!: CategoryId;
  
  // ファクトリメソッド
  static create(
    name: string,
    description: string,
    price: Money,
    categoryId: CategoryId
  ): EventSourcedProduct {
    const productId = ProductId.generate();
    const product = new EventSourcedProduct(productId);
    
    // イベントを発生
    product.raiseEvent(new ProductCreated({
      productId: productId.value,
      name,
      description,
      price: price.toJSON(),
      categoryId: categoryId.value,
      timestamp: new Date()
    }));
    
    return product;
  }
  
  // ビジネスメソッド
  updatePrice(newPrice: Money): Result<void> {
    // ビジネスルールのチェック
    if (this.status === ProductStatus.DISCONTINUED) {
      return Result.fail("Cannot update price of discontinued product");
    }
    
    const priceChangePercentage = this.calculatePriceChange(newPrice);
    if (Math.abs(priceChangePercentage) > 50) {
      return Result.fail("Price change cannot exceed 50%");
    }
    
    // イベントを発生
    this.raiseEvent(new ProductPriceUpdated({
      productId: this.id.value,
      oldPrice: this.price.toJSON(),
      newPrice: newPrice.toJSON(),
      timestamp: new Date()
    }));
    
    return Result.ok();
  }
  
  discontinue(): Result<void> {
    if (this.status === ProductStatus.DISCONTINUED) {
      return Result.fail("Product is already discontinued");
    }
    
    this.raiseEvent(new ProductDiscontinued({
      productId: this.id.value,
      timestamp: new Date()
    }));
    
    return Result.ok();
  }
  
  // イベントハンドラ（状態の更新）
  protected applyEvent(event: DomainEvent): void {
    if (event instanceof ProductCreated) {
      this.name = event.data.name;
      this.description = event.data.description;
      this.price = Money.fromJSON(event.data.price);
      this.categoryId = CategoryId.fromString(event.data.categoryId);
      this.status = ProductStatus.ACTIVE;
    }
    
    if (event instanceof ProductPriceUpdated) {
      this.price = Money.fromJSON(event.data.newPrice);
    }
    
    if (event instanceof ProductDiscontinued) {
      this.status = ProductStatus.DISCONTINUED;
    }
  }
  
  private calculatePriceChange(newPrice: Money): number {
    const oldAmount = this.price.getAmount();
    const newAmount = newPrice.getAmount();
    return ((newAmount - oldAmount) / oldAmount) * 100;
  }
}
```

### イベントソースドリポジトリ

```typescript
export class EventSourcedProductRepository {
  constructor(
    private eventStore: EventStore
  ) {}
  
  async findById(id: ProductId): Promise<EventSourcedProduct | null> {
    const events = await this.eventStore.readStream(id.value);
    
    if (events.length === 0) {
      return null;
    }
    
    // イベントから集約を再構築
    const domainEvents = events.map(e => e.data as DomainEvent);
    return EventSourcedProduct.fromEvents(
      EventSourcedProduct,
      domainEvents
    );
  }
  
  async save(product: EventSourcedProduct): Promise<void> {
    const uncommittedEvents = product.getUncommittedEvents();
    
    if (uncommittedEvents.length === 0) {
      return; // 変更なし
    }
    
    // イベントストアに保存
    await this.eventStore.append(
      product.getId().value,
      uncommittedEvents,
      product.getVersion() - uncommittedEvents.length
    );
    
    // コミット済みとしてマーク
    product.markEventsAsCommitted();
  }
}
```

## プロジェクションの実装

### 基本的なプロジェクションインターフェース

```typescript
export interface Projection {
  project(event: StoredEvent): Promise<void>;
}
```

### 製品カタログプロジェクション

```typescript
// 製品カタログプロジェクション
export class ProductCatalogProjection implements Projection {
  constructor(
    private readDb: ReadDatabase
  ) {}
  
  async project(event: StoredEvent): Promise<void> {
    const eventData = event.data;
    
    switch (event.type) {
      case 'ProductCreated':
        await this.handleProductCreated(eventData);
        break;
      
      case 'ProductPriceUpdated':
        await this.handleProductPriceUpdated(eventData);
        break;
      
      case 'ProductDiscontinued':
        await this.handleProductDiscontinued(eventData);
        break;
    }
  }
  
  private async handleProductCreated(
    event: ProductCreated
  ): Promise<void> {
    await this.readDb.productCatalog.create({
      data: {
        productId: event.data.productId,
        name: event.data.name,
        description: event.data.description,
        price: event.data.price.amount,
        currency: event.data.price.currency,
        categoryId: event.data.categoryId,
        status: 'ACTIVE',
        createdAt: event.timestamp,
        updatedAt: event.timestamp
      }
    });
  }
  
  private async handleProductPriceUpdated(
    event: ProductPriceUpdated
  ): Promise<void> {
    await this.readDb.productCatalog.update({
      where: { productId: event.data.productId },
      data: {
        price: event.data.newPrice.amount,
        updatedAt: event.timestamp
      }
    });
  }
  
  private async handleProductDiscontinued(
    event: ProductDiscontinued
  ): Promise<void> {
    await this.readDb.productCatalog.update({
      where: { productId: event.data.productId },
      data: {
        status: 'DISCONTINUED',
        discontinuedAt: event.timestamp,
        updatedAt: event.timestamp
      }
    });
  }
}
```

### 製品検索プロジェクション（Elasticsearch連携）

```typescript
// 製品検索プロジェクション（Elasticsearch）
export class ProductSearchProjection implements Projection {
  constructor(
    private searchClient: ElasticsearchClient
  ) {}
  
  async project(event: StoredEvent): Promise<void> {
    const eventData = event.data;
    
    switch (event.type) {
      case 'ProductCreated':
        await this.indexProduct(eventData);
        break;
      
      case 'ProductPriceUpdated':
        await this.updateProductPrice(eventData);
        break;
      
      case 'ProductDiscontinued':
        await this.removeProductFromSearch(eventData);
        break;
    }
  }
  
  private async indexProduct(event: ProductCreated): Promise<void> {
    await this.searchClient.index({
      index: 'products',
      id: event.data.productId,
      body: {
        name: event.data.name,
        description: event.data.description,
        price: event.data.price.amount,
        categoryId: event.data.categoryId,
        suggest: {
          input: [event.data.name],
          weight: 1
        }
      }
    });
  }
  
  private async updateProductPrice(event: ProductPriceUpdated): Promise<void> {
    await this.searchClient.update({
      index: 'products',
      id: event.data.productId,
      body: {
        doc: {
          price: event.data.newPrice.amount
        }
      }
    });
  }
  
  private async removeProductFromSearch(event: ProductDiscontinued): Promise<void> {
    await this.searchClient.delete({
      index: 'products',
      id: event.data.productId
    });
  }
}
```

### プロジェクションマネージャー

```typescript
export class ProjectionManager {
  private projections: Map<string, Projection[]> = new Map();
  private checkpoints: Map<string, number> = new Map();
  
  constructor(
    private eventStore: EventStore,
    private checkpointStore: CheckpointStore
  ) {}
  
  register(projectionName: string, projection: Projection): void {
    const projections = this.projections.get(projectionName) || [];
    projections.push(projection);
    this.projections.set(projectionName, projections);
  }
  
  async start(): Promise<void> {
    // 各プロジェクションのチェックポイントを読み込み
    for (const [name] of this.projections) {
      const checkpoint = await this.checkpointStore.get(name);
      this.checkpoints.set(name, checkpoint || 0);
    }
    
    // イベントの処理を開始
    await this.processEvents();
  }
  
  private async processEvents(): Promise<void> {
    while (true) {
      try {
        // 最小のチェックポイントから読み取り
        const minCheckpoint = Math.min(...this.checkpoints.values());
        const events = await this.eventStore.readAll(minCheckpoint);
        
        if (events.length === 0) {
          // 新しいイベントを待つ
          await this.sleep(1000);
          continue;
        }
        
        // イベントを各プロジェクションに配信
        for (const event of events) {
          await this.projectEvent(event);
        }
        
      } catch (error) {
        console.error('Projection error:', error);
        await this.sleep(5000); // エラー時は長めに待機
      }
    }
  }
  
  private async projectEvent(event: StoredEvent): Promise<void> {
    // 並列処理で高速化
    const projectionPromises: Promise<void>[] = [];
    
    for (const [name, projections] of this.projections) {
      const checkpoint = this.checkpoints.get(name) || 0;
      
      if (event.position > checkpoint) {
        // このプロジェクションはまだ処理していない
        for (const projection of projections) {
          projectionPromises.push(
            this.projectWithRetry(name, projection, event)
          );
        }
      }
    }
    
    // 全てのプロジェクションが完了するのを待つ
    await Promise.all(projectionPromises);
  }
  
  private async projectWithRetry(
    name: string,
    projection: Projection,
    event: StoredEvent
  ): Promise<void> {
    const maxRetries = 3;
    let lastError: Error | null = null;
    
    for (let i = 0; i < maxRetries; i++) {
      try {
        await projection.project(event);
        
        // チェックポイントを更新
        await this.checkpointStore.save(name, event.position);
        this.checkpoints.set(name, event.position);
        
        return;
      } catch (error) {
        lastError = error as Error;
        await this.sleep(Math.pow(2, i) * 1000); // 指数バックオフ
      }
    }
    
    throw new Error(
      `Failed to project event ${event.id} after ${maxRetries} retries: ${lastError}`
    );
  }
  
  private async sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

## 高度なパターン

### サーガパターンの実装

```typescript
export abstract class Saga {
  protected commandBus: CommandBus;
  
  abstract handle(event: DomainEvent): Promise<void>;
}

// 注文処理サーガ
export class OrderFulfillmentSaga extends Saga {
  async handle(event: DomainEvent): Promise<void> {
    if (event instanceof OrderPlaced) {
      await this.handleOrderPlaced(event);
    }
    
    if (event instanceof PaymentProcessed) {
      await this.handlePaymentProcessed(event);
    }
    
    if (event instanceof PaymentFailed) {
      await this.handlePaymentFailed(event);
    }
    
    if (event instanceof ItemsReserved) {
      await this.handleItemsReserved(event);
    }
  }
  
  private async handleOrderPlaced(event: OrderPlaced): Promise<void> {
    // 在庫の予約
    await this.commandBus.dispatch(new ReserveItems({
      orderId: event.orderId,
      items: event.items,
      correlationId: event.orderId
    }));
  }
  
  private async handleItemsReserved(event: ItemsReserved): Promise<void> {
    // 支払い処理
    await this.commandBus.dispatch(new ProcessPayment({
      orderId: event.orderId,
      amount: event.totalAmount,
      correlationId: event.orderId
    }));
  }
  
  private async handlePaymentProcessed(event: PaymentProcessed): Promise<void> {
    // 出荷指示
    await this.commandBus.dispatch(new ShipOrder({
      orderId: event.orderId,
      correlationId: event.orderId
    }));
  }
  
  private async handlePaymentFailed(event: PaymentFailed): Promise<void> {
    // 補償：在庫の解放
    await this.commandBus.dispatch(new ReleaseItems({
      orderId: event.orderId,
      correlationId: event.orderId
    }));
    
    // 注文のキャンセル
    await this.commandBus.dispatch(new CancelOrder({
      orderId: event.orderId,
      reason: 'Payment failed',
      correlationId: event.orderId
    }));
  }
}
```

### スナップショットの実装

```typescript
export interface Snapshot {
  aggregateId: string;
  version: number;
  data: any;
  createdAt: Date;
}

export class SnapshotStore {
  constructor(private db: Database) {}
  
  async save(
    aggregateId: string,
    version: number,
    aggregate: EventSourcedAggregate<any>
  ): Promise<void> {
    const snapshot = {
      aggregateId,
      version,
      data: this.serializeAggregate(aggregate),
      createdAt: new Date()
    };
    
    await this.db.snapshots.create({ data: snapshot });
  }
  
  async get(aggregateId: string): Promise<Snapshot | null> {
    return await this.db.snapshots.findFirst({
      where: { aggregateId },
      orderBy: { version: 'desc' }
    });
  }
  
  private serializeAggregate(aggregate: any): any {
    // 集約の状態をシリアライズ
    return {
      type: aggregate.constructor.name,
      state: aggregate.getState()
    };
  }
}

// スナップショット対応リポジトリ
export class SnapshotAwareRepository {
  constructor(
    private eventStore: EventStore,
    private snapshotStore: SnapshotStore,
    private snapshotFrequency: number = 10
  ) {}
  
  async findById(id: string): Promise<EventSourcedAggregate<any> | null> {
    // スナップショットを確認
    const snapshot = await this.snapshotStore.get(id);
    
    let aggregate: EventSourcedAggregate<any>;
    let fromVersion = 0;
    
    if (snapshot) {
      // スナップショットから復元
      aggregate = this.deserializeSnapshot(snapshot);
      fromVersion = snapshot.version;
    }
    
    // スナップショット以降のイベントを取得
    const events = await this.eventStore.readStream(id, fromVersion);
    
    if (!snapshot && events.length === 0) {
      return null;
    }
    
    if (!snapshot) {
      // イベントから完全に再構築
      aggregate = this.createAggregateFromEvents(events);
    } else {
      // スナップショット以降のイベントを適用
      this.applyEventsToAggregate(aggregate, events);
    }
    
    return aggregate;
  }
  
  async save(aggregate: EventSourcedAggregate<any>): Promise<void> {
    const uncommittedEvents = aggregate.getUncommittedEvents();
    
    if (uncommittedEvents.length === 0) {
      return;
    }
    
    // イベントを保存
    await this.eventStore.append(
      aggregate.getId().value,
      uncommittedEvents,
      aggregate.getVersion() - uncommittedEvents.length
    );
    
    // スナップショットの作成を検討
    if (aggregate.getVersion() % this.snapshotFrequency === 0) {
      await this.snapshotStore.save(
        aggregate.getId().value,
        aggregate.getVersion(),
        aggregate
      );
    }
    
    aggregate.markEventsAsCommitted();
  }
  
  private deserializeSnapshot(snapshot: Snapshot): EventSourcedAggregate<any> {
    // スナップショットから集約を復元
    const AggregateClass = this.getAggregateClass(snapshot.data.type);
    const aggregate = new AggregateClass(snapshot.data.state.id);
    aggregate.restoreFromState(snapshot.data.state);
    return aggregate;
  }
  
  private createAggregateFromEvents(events: StoredEvent[]): EventSourcedAggregate<any> {
    // イベントから集約を構築するロジック
    // （実装は集約のタイプに依存）
    throw new Error("Implementation required");
  }
  
  private applyEventsToAggregate(
    aggregate: EventSourcedAggregate<any>,
    events: StoredEvent[]
  ): void {
    for (const event of events) {
      aggregate.applyEvent(event.data);
    }
  }
  
  private getAggregateClass(typeName: string): any {
    // 集約クラスのレジストリから取得
    // （実装は省略）
    throw new Error("Implementation required");
  }
}
```

## ベストプラクティス

### イベントの設計

1. **イベント名は過去形で**
   - ✅ `OrderPlaced`、`PaymentProcessed`
   - ❌ `PlaceOrder`、`ProcessPayment`

2. **イベントは不変**
   - 一度記録されたイベントは変更しない
   - 新しい情報は新しいイベントとして記録

3. **イベントのバージョニング**
   ```typescript
   interface EventV1 {
     version: 1;
     orderId: string;
     amount: number;
   }
   
   interface EventV2 {
     version: 2;
     orderId: string;
     amount: Money; // 型が変更された
   }
   ```

### パフォーマンス最適化

1. **スナップショット戦略**
   - イベント数が多い集約に対して定期的にスナップショットを作成
   - 一般的には10〜100イベントごと

2. **プロジェクションの並列化**
   - 独立したプロジェクションは並列実行
   - 順序が重要な場合のみ直列化

3. **イベントストアの分割**
   - 集約タイプごとにストリームを分割
   - 年月でのパーティショニング

## トラブルシューティング

### よくある問題と解決策

1. **イベントの順序問題**
   - 原因：並列処理による順序の乱れ
   - 解決：イベントのタイムスタンプと位置番号で管理

2. **プロジェクションの遅延**
   - 原因：処理が追いつかない
   - 解決：プロジェクションの並列度を上げる、キャッシュの活用

3. **メモリ不足**
   - 原因：大量のイベントの一括読み込み
   - 解決：ストリーミング処理、バッチサイズの調整