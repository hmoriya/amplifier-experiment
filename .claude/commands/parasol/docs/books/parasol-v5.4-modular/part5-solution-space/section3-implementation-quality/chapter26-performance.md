# 第26章　パフォーマンス最適化 ― 速度の追求

## はじめに：F1レースカーのチューニング

F1レースでは、わずか0.001秒の差が勝敗を分けます。エンジニアたちは、空力特性、重量配分、タイヤ圧、燃料効率など、無数のパラメータを調整し、マシンの性能を極限まで引き出します。ソフトウェアのパフォーマンス最適化も同様に、システムの各層で緻密なチューニングを行い、最高の性能を追求する技術です。

本章では、Parasol V5.4の文脈で、システムパフォーマンスを体系的に分析し、最適化する手法を解説します。

## パフォーマンス最適化の原則

### パフォーマンスの多面性

```typescript
export interface PerformanceDimensions {
  // レスポンス性能
  latency: {
    definition: "リクエストからレスポンスまでの時間";
    metrics: {
      p50: "中央値レスポンスタイム";
      p95: "95パーセンタイル";
      p99: "99パーセンタイル";
      max: "最大レスポンスタイム";
    };
    targets: {
      api: "< 100ms (p95)";
      page: "< 1000ms (p95)";
      interaction: "< 50ms";
    };
  };
  
  // スループット
  throughput: {
    definition: "単位時間あたりの処理能力";
    metrics: {
      rps: "Requests per second";
      tps: "Transactions per second";
      concurrent: "同時接続数";
    };
    targets: {
      api: "> 10,000 rps";
      database: "> 5,000 tps";
      websocket: "> 100,000 connections";
    };
  };
  
  // リソース効率
  efficiency: {
    cpu: "CPU使用率 < 70%";
    memory: "メモリ使用率 < 80%";
    disk: "ディスクI/O < 80%";
    network: "帯域使用率 < 70%";
  };
  
  // スケーラビリティ
  scalability: {
    horizontal: "ノード追加による性能向上";
    vertical: "リソース追加による性能向上";
    elasticity: "負荷に応じた自動スケーリング";
  };
}

export class PerformanceOptimizationStrategy {
  // 測定 → 分析 → 最適化のサイクル
  async optimize(system: System): Promise<OptimizationResult> {
    // 1. ベースライン測定
    const baseline = await this.measureBaseline(system);
    
    // 2. ボトルネック分析
    const bottlenecks = await this.analyzeBottlenecks(baseline);
    
    // 3. 最適化計画
    const plan = this.createOptimizationPlan(bottlenecks);
    
    // 4. 実行と検証
    const results: OptimizationResult[] = [];
    for (const optimization of plan.optimizations) {
      const result = await this.applyOptimization(optimization);
      results.push(result);
      
      // 効果測定
      const improved = await this.measureImprovement(baseline, result);
      if (!improved) {
        await this.rollbackOptimization(optimization);
      }
    }
    
    return this.summarizeResults(results);
  }
}
```

### パフォーマンス測定

```typescript
export class PerformanceMeasurement {
  // APMツールの統合
  private apm: APMClient = new DatadogAPM({
    service: "parasol-api",
    env: "production",
    version: "5.4.0"
  });
  
  // カスタムメトリクス
  async measureCustomMetrics(): Promise<CustomMetrics> {
    return {
      // ビジネスメトリクス
      business: {
        ordersPerMinute: await this.measureOrderThroughput(),
        checkoutConversion: await this.measureConversionRate(),
        searchRelevancy: await this.measureSearchQuality()
      },
      
      // 技術メトリクス
      technical: {
        databaseConnections: await this.measureDBConnections(),
        cacheHitRate: await this.measureCacheEfficiency(),
        queueDepth: await this.measureQueueBacklog()
      },
      
      // ユーザー体験メトリクス
      userExperience: {
        firstContentfulPaint: await this.measureFCP(),
        timeToInteractive: await this.measureTTI(),
        cumulativeLayoutShift: await this.measureCLS()
      }
    };
  }
  
  // 分散トレーシング
  implementTracing(): TracingConfiguration {
    return {
      sampler: {
        type: "adaptive",
        targetRate: 1000, // 1000 traces/second
        rules: [
          { service: "api", sample: 0.1 },
          { error: true, sample: 1.0 },
          { slowRequest: true, sample: 1.0 }
        ]
      },
      
      propagation: {
        inject: ["http_headers", "grpc_metadata"],
        extract: ["http_headers", "grpc_metadata"],
        baggage: ["user_id", "session_id", "request_id"]
      },
      
      instrumentation: {
        automatic: [
          "http", "grpc", "database", "redis", "kafka"
        ],
        manual: [
          {
            operation: "business.checkout",
            tags: { component: "checkout", span_type: "business" }
          },
          {
            operation: "cache.computation",
            tags: { component: "cache", span_type: "cache" }
          }
        ]
      }
    };
  }
}
```

## アプリケーション層の最適化

### コードレベル最適化

```typescript
export class CodeOptimization {
  // アルゴリズム最適化
  optimizeAlgorithm(original: Function): OptimizedFunction {
    // Before: O(n²) - ネストループ
    function findDuplicatesSlow(items: number[]): number[] {
      const duplicates: number[] = [];
      for (let i = 0; i < items.length; i++) {
        for (let j = i + 1; j < items.length; j++) {
          if (items[i] === items[j] && !duplicates.includes(items[i])) {
            duplicates.push(items[i]);
          }
        }
      }
      return duplicates;
    }
    
    // After: O(n) - ハッシュマップ使用
    function findDuplicatesFast(items: number[]): number[] {
      const seen = new Set<number>();
      const duplicates = new Set<number>();
      
      for (const item of items) {
        if (seen.has(item)) {
          duplicates.add(item);
        }
        seen.add(item);
      }
      
      return Array.from(duplicates);
    }
    
    return {
      optimized: findDuplicatesFast,
      improvement: {
        timeComplexity: { from: "O(n²)", to: "O(n)" },
        spaceComplexity: { from: "O(1)", to: "O(n)" },
        benchmark: "100x faster for n=10000"
      }
    };
  }
  
  // メモリ最適化
  optimizeMemory(): MemoryOptimizations {
    return {
      // オブジェクトプーリング
      objectPooling: {
        implementation: `
          class ObjectPool<T> {
            private pool: T[] = [];
            private factory: () => T;
            private reset: (obj: T) => void;
            
            constructor(factory: () => T, reset: (obj: T) => void) {
              this.factory = factory;
              this.reset = reset;
            }
            
            acquire(): T {
              return this.pool.pop() || this.factory();
            }
            
            release(obj: T): void {
              this.reset(obj);
              this.pool.push(obj);
            }
          }
          
          // 使用例
          const bufferPool = new ObjectPool(
            () => Buffer.allocUnsafe(1024 * 1024), // 1MB
            (buf) => buf.fill(0)
          );
        `,
        benefits: "GC圧力の削減、メモリ割り当てコストの削減"
      },
      
      // 遅延評価
      lazyEvaluation: {
        implementation: `
          class LazyValue<T> {
            private value?: T;
            private computed = false;
            private compute: () => T;
            
            constructor(compute: () => T) {
              this.compute = compute;
            }
            
            get(): T {
              if (!this.computed) {
                this.value = this.compute();
                this.computed = true;
              }
              return this.value!;
            }
          }
          
          // 使用例
          const expensiveData = new LazyValue(() => {
            return performExpensiveCalculation();
          });
        `,
        benefits: "不要な計算の回避、初期化時間の短縮"
      },
      
      // 文字列ビルダー
      stringBuilder: {
        implementation: `
          class StringBuilder {
            private chunks: string[] = [];
            
            append(str: string): this {
              this.chunks.push(str);
              return this;
            }
            
            toString(): string {
              return this.chunks.join('');
            }
          }
        `,
        benefits: "文字列結合のメモリ効率化"
      }
    };
  }
  
  // 非同期処理最適化
  optimizeAsync(): AsyncOptimizations {
    return {
      // バッチ処理
      batching: {
        implementation: `
          class BatchProcessor<T, R> {
            private queue: Array<{
              item: T;
              resolve: (result: R) => void;
              reject: (error: Error) => void;
            }> = [];
            private timer?: NodeJS.Timeout;
            
            constructor(
              private processor: (items: T[]) => Promise<R[]>,
              private maxBatchSize: number = 100,
              private maxWaitTime: number = 10
            ) {}
            
            async process(item: T): Promise<R> {
              return new Promise((resolve, reject) => {
                this.queue.push({ item, resolve, reject });
                
                if (this.queue.length >= this.maxBatchSize) {
                  this.flush();
                } else if (!this.timer) {
                  this.timer = setTimeout(() => this.flush(), this.maxWaitTime);
                }
              });
            }
            
            private async flush(): Promise<void> {
              if (this.timer) {
                clearTimeout(this.timer);
                this.timer = undefined;
              }
              
              const batch = this.queue.splice(0);
              if (batch.length === 0) return;
              
              try {
                const results = await this.processor(batch.map(b => b.item));
                batch.forEach((b, i) => b.resolve(results[i]));
              } catch (error) {
                batch.forEach(b => b.reject(error as Error));
              }
            }
          }
        `,
        benefits: "APIコール削減、スループット向上"
      },
      
      // 並列処理制御
      parallelControl: {
        implementation: `
          class ParallelQueue {
            private running = 0;
            private queue: Array<() => Promise<any>> = [];
            
            constructor(private concurrency: number = 5) {}
            
            async add<T>(task: () => Promise<T>): Promise<T> {
              if (this.running >= this.concurrency) {
                await new Promise(resolve => this.queue.push(resolve));
              }
              
              this.running++;
              try {
                return await task();
              } finally {
                this.running--;
                const next = this.queue.shift();
                if (next) next();
              }
            }
          }
        `,
        benefits: "リソース管理、システム安定性"
      }
    };
  }
}
```

### キャッシング戦略

```typescript
export class CachingStrategy {
  // 多層キャッシュアーキテクチャ
  implementMultiLayerCache(): CacheArchitecture {
    return {
      layers: [
        {
          name: "L1 - Application Memory",
          type: "in-memory",
          size: "100MB",
          ttl: "5 minutes",
          implementation: `
            class L1Cache {
              private cache = new Map<string, CacheEntry>();
              private maxSize = 100 * 1024 * 1024; // 100MB
              private currentSize = 0;
              
              async get(key: string): Promise<any | null> {
                const entry = this.cache.get(key);
                if (!entry) return null;
                
                if (Date.now() > entry.expiry) {
                  this.cache.delete(key);
                  return null;
                }
                
                entry.hits++;
                entry.lastAccess = Date.now();
                return entry.value;
              }
              
              async set(key: string, value: any, ttl: number): Promise<void> {
                const size = this.estimateSize(value);
                
                // LRU eviction if needed
                while (this.currentSize + size > this.maxSize) {
                  this.evictLRU();
                }
                
                this.cache.set(key, {
                  value,
                  size,
                  expiry: Date.now() + ttl,
                  hits: 0,
                  lastAccess: Date.now()
                });
                
                this.currentSize += size;
              }
            }
          `
        },
        {
          name: "L2 - Redis",
          type: "distributed",
          size: "10GB",
          ttl: "1 hour",
          features: ["clustering", "persistence", "pub/sub"]
        },
        {
          name: "L3 - CDN",
          type: "edge",
          size: "unlimited",
          ttl: "24 hours",
          features: ["global distribution", "automatic invalidation"]
        }
      ],
      
      strategies: {
        cacheAside: {
          read: "Check cache → Miss? Load from source → Update cache → Return",
          write: "Write to source → Invalidate cache"
        },
        
        writeThrough: {
          read: "Read from cache",
          write: "Write to cache → Write to source"
        },
        
        writeBehind: {
          read: "Read from cache",
          write: "Write to cache → Queue write to source"
        }
      },
      
      patterns: {
        // ロシアンドール（入れ子）キャッシング
        russianDoll: `
          async function getProductWithReviews(productId: string) {
            const cacheKey = \`product:\${productId}:with-reviews\`;
            
            return await cache.getOrSet(cacheKey, async () => {
              const product = await cache.getOrSet(
                \`product:\${productId}\`,
                () => db.getProduct(productId),
                3600
              );
              
              const reviews = await cache.getOrSet(
                \`reviews:product:\${productId}\`,
                () => db.getReviews(productId),
                1800
              );
              
              return { ...product, reviews };
            }, 900);
          }
        `,
        
        // タグベースの無効化
        tagBased: `
          class TaggedCache {
            async set(key: string, value: any, tags: string[]): Promise<void> {
              await this.cache.set(key, value);
              
              for (const tag of tags) {
                await this.cache.sadd(\`tag:\${tag}\`, key);
              }
            }
            
            async invalidateByTag(tag: string): Promise<void> {
              const keys = await this.cache.smembers(\`tag:\${tag}\`);
              
              if (keys.length > 0) {
                await this.cache.del(...keys);
                await this.cache.del(\`tag:\${tag}\`);
              }
            }
          }
        `
      }
    };
  }
  
  // キャッシュ最適化
  optimizeCache(): CacheOptimizations {
    return {
      // プリフェッチング
      prefetching: {
        strategy: "予測的キャッシュ読み込み",
        implementation: `
          class PredictiveCache {
            async prefetch(userId: string, context: UserContext): Promise<void> {
              const predictions = await this.ml.predictNextActions(userId, context);
              
              // 確率の高い順にプリフェッチ
              for (const prediction of predictions) {
                if (prediction.probability > 0.7) {
                  // バックグラウンドでキャッシュに読み込み
                  this.warmCache(prediction.resource);
                }
              }
            }
          }
        `
      },
      
      // キャッシュウォーミング
      warming: {
        strategy: "事前キャッシュ読み込み",
        implementation: `
          class CacheWarmer {
            async warmPopularItems(): Promise<void> {
              const popularItems = await this.analytics.getPopularItems(100);
              
              await Promise.all(
                popularItems.map(item => 
                  this.cache.set(item.key, item.value, item.ttl)
                )
              );
            }
            
            scheduleWarming(): void {
              // 毎朝6時にキャッシュウォーミング
              cron.schedule('0 6 * * *', () => this.warmPopularItems());
            }
          }
        `
      }
    };
  }
}
```

## データベース最適化

### クエリ最適化

```typescript
export class DatabaseOptimization {
  // クエリ分析と最適化
  async optimizeQueries(database: Database): Promise<OptimizationReport> {
    const slowQueries = await this.identifySlowQueries(database);
    const optimizations: QueryOptimization[] = [];
    
    for (const query of slowQueries) {
      const analysis = await this.analyzeQuery(query);
      const optimization = this.suggestOptimization(analysis);
      optimizations.push(optimization);
    }
    
    return {
      totalQueries: slowQueries.length,
      optimizations,
      estimatedImprovement: this.calculateImpact(optimizations)
    };
  }
  
  // インデックス最適化
  optimizeIndexes(): IndexOptimizations {
    return {
      // 複合インデックス
      compositeIndexes: `
        -- Before: 個別インデックスでは効率が悪い
        CREATE INDEX idx_user_id ON orders(user_id);
        CREATE INDEX idx_status ON orders(status);
        
        -- After: 複合インデックスで高速化
        CREATE INDEX idx_user_status ON orders(user_id, status);
        CREATE INDEX idx_status_created ON orders(status, created_at);
      `,
      
      // 部分インデックス
      partialIndexes: `
        -- アクティブな注文のみインデックス化
        CREATE INDEX idx_active_orders ON orders(created_at)
        WHERE status IN ('pending', 'processing');
        
        -- 削除されていないレコードのみ
        CREATE INDEX idx_active_users ON users(email)
        WHERE deleted_at IS NULL;
      `,
      
      // カバリングインデックス
      coveringIndexes: `
        -- クエリで必要な全カラムを含む
        CREATE INDEX idx_order_summary ON orders(
          user_id, status, created_at
        ) INCLUDE (total_amount, item_count);
        
        -- インデックスオンリースキャンが可能
        SELECT total_amount, item_count
        FROM orders
        WHERE user_id = ? AND status = ?
        ORDER BY created_at DESC;
      `
    };
  }
  
  // クエリ書き換え
  rewriteQueries(): QueryRewrites {
    return {
      // N+1問題の解決
      fixNPlusOne: {
        before: `
          // N+1クエリ
          const users = await db.query('SELECT * FROM users');
          for (const user of users) {
            const orders = await db.query(
              'SELECT * FROM orders WHERE user_id = ?',
              [user.id]
            );
            user.orders = orders;
          }
        `,
        after: `
          // JOINまたはバッチ取得
          const users = await db.query(\`
            SELECT u.*, o.*
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id
            ORDER BY u.id, o.created_at DESC
          \`);
          
          // または
          const users = await db.query('SELECT * FROM users');
          const userIds = users.map(u => u.id);
          const orders = await db.query(
            'SELECT * FROM orders WHERE user_id = ANY(?)',
            [userIds]
          );
        `
      },
      
      // サブクエリの最適化
      optimizeSubquery: {
        before: `
          SELECT *
          FROM products
          WHERE price > (
            SELECT AVG(price) FROM products
          )
        `,
        after: `
          WITH avg_price AS (
            SELECT AVG(price) as avg FROM products
          )
          SELECT p.*
          FROM products p, avg_price a
          WHERE p.price > a.avg
        `
      }
    };
  }
}
```

### データベースパフォーマンスチューニング

```typescript
export class DatabaseTuning {
  // 接続プール最適化
  optimizeConnectionPool(): ConnectionPoolConfig {
    return {
      sizing: {
        formula: "connections = (cores * 2) + effective_spindle_count",
        calculation: {
          cores: 8,
          effectiveSpindleCount: 1, // SSDの場合
          recommended: 17
        }
      },
      
      configuration: {
        min: 5,
        max: 20,
        idleTimeout: 30000,
        connectionTimeout: 5000,
        validationQuery: "SELECT 1",
        testOnBorrow: true,
        testWhileIdle: true,
        timeBetweenEvictionRuns: 60000
      },
      
      monitoring: `
        class PoolMonitor {
          monitor(pool: ConnectionPool): PoolMetrics {
            return {
              active: pool.activeConnections(),
              idle: pool.idleConnections(),
              waiting: pool.waitingRequests(),
              totalCreated: pool.totalCreated(),
              totalDestroyed: pool.totalDestroyed(),
              utilizationRate: pool.active / pool.max,
              waitTime: pool.avgWaitTime()
            };
          }
          
          autoTune(metrics: PoolMetrics): PoolAdjustment {
            if (metrics.utilizationRate > 0.8 && metrics.waitTime > 100) {
              return { action: 'increase', by: 5 };
            }
            if (metrics.utilizationRate < 0.3 && metrics.idle > 10) {
              return { action: 'decrease', by: 3 };
            }
            return { action: 'none' };
          }
        }
      `
    };
  }
  
  // パーティショニング戦略
  implementPartitioning(): PartitioningStrategy {
    return {
      // 時系列パーティショニング
      timeBasedPartitioning: `
        -- 月別パーティション
        CREATE TABLE orders (
          id BIGINT,
          user_id BIGINT,
          created_at TIMESTAMP,
          ...
        ) PARTITION BY RANGE (created_at);
        
        CREATE TABLE orders_2024_01 PARTITION OF orders
          FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
          
        CREATE TABLE orders_2024_02 PARTITION OF orders
          FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
        
        -- 自動パーティション管理
        CREATE OR REPLACE FUNCTION create_monthly_partition()
        RETURNS void AS $$
        DECLARE
          start_date date;
          end_date date;
          partition_name text;
        BEGIN
          start_date := date_trunc('month', CURRENT_DATE + interval '1 month');
          end_date := start_date + interval '1 month';
          partition_name := 'orders_' || to_char(start_date, 'YYYY_MM');
          
          EXECUTE format('CREATE TABLE IF NOT EXISTS %I PARTITION OF orders 
            FOR VALUES FROM (%L) TO (%L)',
            partition_name, start_date, end_date);
        END;
        $$ LANGUAGE plpgsql;
      `,
      
      // ハッシュパーティショニング
      hashPartitioning: `
        -- ユーザーIDでハッシュ分割
        CREATE TABLE users (
          id BIGINT,
          email VARCHAR(255),
          ...
        ) PARTITION BY HASH (id);
        
        CREATE TABLE users_p0 PARTITION OF users
          FOR VALUES WITH (modulus 4, remainder 0);
        CREATE TABLE users_p1 PARTITION OF users
          FOR VALUES WITH (modulus 4, remainder 1);
        CREATE TABLE users_p2 PARTITION OF users
          FOR VALUES WITH (modulus 4, remainder 2);
        CREATE TABLE users_p3 PARTITION OF users
          FOR VALUES WITH (modulus 4, remainder 3);
      `
    };
  }
}
```

## システムレベル最適化

### 負荷分散と自動スケーリング

```typescript
export class SystemOptimization {
  // ロードバランシング戦略
  implementLoadBalancing(): LoadBalancingConfig {
    return {
      algorithms: {
        roundRobin: {
          description: "順番に振り分け",
          useCase: "均等な負荷分散"
        },
        
        leastConnections: {
          description: "最小接続数のサーバーへ",
          useCase: "長時間接続の分散"
        },
        
        weightedRoundRobin: {
          description: "重み付きラウンドロビン",
          useCase: "サーバー性能差がある場合",
          implementation: `
            class WeightedRoundRobin {
              private servers: Array<{server: Server, weight: number}>;
              private currentWeights: number[] = [];
              
              selectServer(): Server {
                let totalWeight = 0;
                let selectedIndex = -1;
                
                for (let i = 0; i < this.servers.length; i++) {
                  this.currentWeights[i] += this.servers[i].weight;
                  totalWeight += this.servers[i].weight;
                  
                  if (selectedIndex === -1 || 
                      this.currentWeights[i] > this.currentWeights[selectedIndex]) {
                    selectedIndex = i;
                  }
                }
                
                this.currentWeights[selectedIndex] -= totalWeight;
                return this.servers[selectedIndex].server;
              }
            }
          `
        },
        
        consistentHashing: {
          description: "一貫性ハッシュ法",
          useCase: "キャッシュサーバーなど",
          implementation: `
            class ConsistentHash {
              private ring: Map<number, Server> = new Map();
              private replicas: number = 150;
              
              addServer(server: Server): void {
                for (let i = 0; i < this.replicas; i++) {
                  const hash = this.hash(\`\${server.id}:\${i}\`);
                  this.ring.set(hash, server);
                }
              }
              
              getServer(key: string): Server {
                const hash = this.hash(key);
                const sortedHashes = Array.from(this.ring.keys()).sort((a, b) => a - b);
                
                for (const h of sortedHashes) {
                  if (h >= hash) {
                    return this.ring.get(h)!;
                  }
                }
                
                return this.ring.get(sortedHashes[0])!;
              }
            }
          `
        }
      },
      
      healthChecks: {
        http: {
          endpoint: "/health",
          interval: 5,
          timeout: 3,
          unhealthyThreshold: 2,
          healthyThreshold: 3
        },
        
        tcp: {
          port: 3000,
          interval: 5,
          timeout: 2
        }
      }
    };
  }
  
  // 自動スケーリング
  implementAutoScaling(): AutoScalingConfig {
    return {
      horizontal: {
        metrics: [
          {
            type: "CPU",
            target: 70,
            scaleUpThreshold: 80,
            scaleDownThreshold: 30
          },
          {
            type: "Memory",
            target: 75,
            scaleUpThreshold: 85,
            scaleDownThreshold: 40
          },
          {
            type: "RequestRate",
            target: 1000,
            scaleUpThreshold: 1200,
            scaleDownThreshold: 500
          }
        ],
        
        scaling: {
          minInstances: 2,
          maxInstances: 20,
          scaleUpRate: 3, // 一度に追加する最大インスタンス数
          scaleDownRate: 1, // 一度に削除する最大インスタンス数
          cooldownPeriod: 300, // 秒
          
          policy: `
            class AutoScaler {
              async evaluateScaling(metrics: Metrics): Promise<ScalingAction> {
                const violations = this.checkThresholds(metrics);
                
                if (violations.scaleUp.length > 0) {
                  const instances = this.calculateScaleUpCount(violations);
                  return { action: 'scale-up', count: instances };
                }
                
                if (violations.scaleDown.length === this.metrics.length) {
                  const instances = this.calculateScaleDownCount(violations);
                  return { action: 'scale-down', count: instances };
                }
                
                return { action: 'none' };
              }
            }
          `
        }
      },
      
      predictive: {
        description: "機械学習による予測的スケーリング",
        implementation: `
          class PredictiveScaler {
            async predictLoad(timeWindow: number): Promise<LoadPrediction> {
              const historicalData = await this.getHistoricalMetrics(timeWindow);
              const patterns = this.analyzePatterns(historicalData);
              
              // 時系列予測モデル
              const forecast = await this.prophet.forecast({
                data: historicalData,
                periods: 24, // 24時間先まで予測
                interval: '1h'
              });
              
              return {
                expectedPeak: forecast.yhat_upper.max(),
                peakTime: forecast.ds[forecast.yhat_upper.argmax()],
                recommendedCapacity: this.calculateCapacity(forecast)
              };
            }
          }
        `
      }
    };
  }
}
```

### ネットワーク最適化

```typescript
export class NetworkOptimization {
  // HTTP/2 と HTTP/3 最適化
  optimizeHTTP(): HTTPOptimizations {
    return {
      http2: {
        serverPush: `
          app.get('/index.html', (req, res) => {
            // Critical resources をプッシュ
            res.push('/styles/main.css', {
              request: { accept: 'text/css' },
              response: { 'content-type': 'text/css' }
            });
            
            res.push('/scripts/app.js', {
              request: { accept: 'application/javascript' },
              response: { 'content-type': 'application/javascript' }
            });
            
            res.sendFile('index.html');
          });
        `,
        
        prioritization: {
          critical: ["CSS", "fonts", "critical JS"],
          high: ["images above fold", "main JS"],
          medium: ["images below fold", "async JS"],
          low: ["analytics", "tracking"]
        }
      },
      
      http3: {
        benefits: ["0-RTT接続", "パケットロスに強い", "接続移行"],
        implementation: `
          const server = createQuicServer({
            key: fs.readFileSync('key.pem'),
            cert: fs.readFileSync('cert.pem'),
            
            // 0-RTTの有効化
            earlyData: true,
            
            // 輻輳制御
            congestionControl: 'bbr',
            
            // ストリーム優先度
            streamPriorities: true
          });
        `
      }
    };
  }
  
  // 圧縮と最小化
  implementCompression(): CompressionStrategy {
    return {
      dynamic: {
        algorithms: {
          brotli: {
            quality: 4, // リアルタイム圧縮用
            types: ["text/html", "application/json", "text/css"],
            minSize: 1024
          },
          
          gzip: {
            level: 6,
            types: ["text/*", "application/javascript"],
            minSize: 860
          }
        }
      },
      
      static: {
        prebuild: `
          // ビルド時に事前圧縮
          class PrecompressPlugin {
            apply(compiler: Compiler) {
              compiler.hooks.emit.tapPromise('PrecompressPlugin', async (compilation) => {
                const assets = compilation.assets;
                
                for (const filename in assets) {
                  if (this.shouldCompress(filename)) {
                    const content = assets[filename].source();
                    
                    // Brotli圧縮
                    const brotli = await promisify(zlib.brotliCompress)(content, {
                      params: { [zlib.constants.BROTLI_PARAM_QUALITY]: 11 }
                    });
                    
                    compilation.assets[\`\${filename}.br\`] = {
                      source: () => brotli,
                      size: () => brotli.length
                    };
                  }
                }
              });
            }
          }
        `
      }
    };
  }
}
```

## フロントエンド最適化

### レンダリングパフォーマンス

```typescript
export class FrontendOptimization {
  // React最適化
  optimizeReact(): ReactOptimizations {
    return {
      memoization: {
        // React.memoの適切な使用
        component: `
          const ExpensiveComponent = React.memo(({ data, onUpdate }) => {
            const processedData = useMemo(() => 
              expensiveProcessing(data), [data]
            );
            
            const handleClick = useCallback(() => {
              onUpdate(processedData);
            }, [processedData, onUpdate]);
            
            return (
              <div onClick={handleClick}>
                {processedData.map(item => 
                  <Item key={item.id} {...item} />
                )}
              </div>
            );
          }, (prevProps, nextProps) => {
            // カスタム比較関数
            return prevProps.data.id === nextProps.data.id &&
                   prevProps.data.version === nextProps.data.version;
          });
        `,
        
        // 仮想スクロール
        virtualScrolling: `
          const VirtualList = ({ items, itemHeight, containerHeight }) => {
            const [scrollTop, setScrollTop] = useState(0);
            
            const startIndex = Math.floor(scrollTop / itemHeight);
            const endIndex = Math.ceil(
              (scrollTop + containerHeight) / itemHeight
            );
            
            const visibleItems = items.slice(startIndex, endIndex);
            const totalHeight = items.length * itemHeight;
            
            return (
              <div 
                style={{ height: containerHeight, overflow: 'auto' }}
                onScroll={(e) => setScrollTop(e.target.scrollTop)}
              >
                <div style={{ height: totalHeight, position: 'relative' }}>
                  {visibleItems.map((item, index) => (
                    <div
                      key={item.id}
                      style={{
                        position: 'absolute',
                        top: (startIndex + index) * itemHeight,
                        height: itemHeight
                      }}
                    >
                      <Item {...item} />
                    </div>
                  ))}
                </div>
              </div>
            );
          };
        `
      },
      
      // コード分割
      codeSplitting: {
        routes: `
          const routes = [
            {
              path: '/',
              component: React.lazy(() => import('./pages/Home'))
            },
            {
              path: '/products',
              component: React.lazy(() => 
                import(/* webpackChunkName: "products" */ './pages/Products')
              )
            },
            {
              path: '/admin',
              component: React.lazy(() => 
                import(/* webpackChunkName: "admin" */ './pages/Admin')
              )
            }
          ];
        `,
        
        components: `
          // 条件付きインポート
          const HeavyComponent = React.lazy(() => {
            return new Promise(resolve => {
              // 必要になるまで遅延
              setTimeout(() => {
                resolve(import('./HeavyComponent'));
              }, 0);
            });
          });
        `
      }
    };
  }
  
  // バンドル最適化
  optimizeBundling(): BundleOptimizations {
    return {
      webpack: {
        optimization: {
          splitChunks: {
            chunks: 'all',
            cacheGroups: {
              vendor: {
                test: /[\\/]node_modules[\\/]/,
                name: 'vendors',
                priority: 10
              },
              common: {
                minChunks: 2,
                priority: 5,
                reuseExistingChunk: true
              }
            }
          },
          
          // Tree shaking
          usedExports: true,
          sideEffects: false,
          
          // Terser設定
          minimizer: [
            new TerserPlugin({
              terserOptions: {
                parse: { ecma: 8 },
                compress: {
                  ecma: 5,
                  warnings: false,
                  comparisons: false,
                  inline: 2
                },
                mangle: { safari10: true },
                output: {
                  ecma: 5,
                  comments: false,
                  ascii_only: true
                }
              }
            })
          ]
        }
      }
    };
  }
}
```

## 監視と継続的最適化

### パフォーマンス監視ダッシュボード

```typescript
export class PerformanceMonitoring {
  // 統合監視システム
  createDashboard(): MonitoringDashboard {
    return {
      realTimeMetrics: {
        latency: {
          p50: this.gauge("latency.p50"),
          p95: this.gauge("latency.p95"),
          p99: this.gauge("latency.p99")
        },
        
        throughput: {
          requests: this.counter("requests.total"),
          errors: this.counter("requests.errors"),
          successRate: this.derive("requests.success_rate")
        },
        
        resources: {
          cpu: this.gauge("system.cpu"),
          memory: this.gauge("system.memory"),
          diskIO: this.gauge("system.disk.io"),
          networkIO: this.gauge("system.network.io")
        }
      },
      
      alerts: [
        {
          name: "High Latency",
          condition: "p95 > 1000ms for 5 minutes",
          severity: "warning"
        },
        {
          name: "Error Rate",
          condition: "error_rate > 5% for 2 minutes",
          severity: "critical"
        }
      ],
      
      slo: {
        availability: "99.9%",
        latency: "p99 < 500ms",
        errorRate: "< 1%"
      }
    };
  }
}
```

## まとめ

パフォーマンス最適化は、継続的な測定、分析、改善のサイクルです。Parasol V5.4における成功の鍵：

1. **測定駆動** - 推測ではなくデータに基づく最適化
2. **体系的アプローチ** - 全レイヤーでの包括的な最適化
3. **トレードオフの理解** - 速度、メモリ、保守性のバランス
4. **継続的改善** - 一度きりではなく継続的なプロセス
5. **ユーザー体験重視** - 技術指標だけでなく体感速度も重要

適切な最適化により、システムは高速で、スケーラブルで、効率的なものになります。

### 次章への架橋

システムのパフォーマンスを最適化する方法を学びました。第27章では、システムを保護するためのセキュリティ実装について詳しく見ていきます。

---

## 演習問題

1. 以下のコードのパフォーマンスボトルネックを特定し、最適化案を提示してください：
   ```typescript
   async function getOrdersWithCustomers(status: string) {
     const orders = await db.query('SELECT * FROM orders WHERE status = ?', [status]);
     
     for (const order of orders) {
       const customer = await db.query('SELECT * FROM customers WHERE id = ?', [order.customer_id]);
       order.customer = customer[0];
       
       const items = await db.query('SELECT * FROM order_items WHERE order_id = ?', [order.id]);
       order.items = items;
     }
     
     return orders.filter(o => o.customer.active).sort((a, b) => b.total - a.total);
   }
   ```

2. Webアプリケーションの初期表示を高速化するための戦略を5つ挙げ、それぞれの実装方法と期待効果を説明してください。

3. 100万件のレコードを持つテーブルに対する検索機能を最適化する計画を立ててください。インデックス設計、キャッシング戦略、クエリ最適化を含めてください。