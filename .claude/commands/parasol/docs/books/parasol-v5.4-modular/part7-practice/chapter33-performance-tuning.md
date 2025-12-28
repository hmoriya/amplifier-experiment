# 第33章　パフォーマンスチューニング ― 速度の追求

## はじめに：F1レースの精密調整

F1レースでは、勝利への鍵は単なる速いエンジンではありません。タイヤの空気圧、ウィングの角度、サスペンションの硬さ、そして無数の小さな調整が、コンマ数秒の差を生み出します。ソフトウェアのパフォーマンスチューニングも同様に、細部への注意と体系的なアプローチが極めて重要です。

本章では、Parasol V5.4を使用したシステムにおいて、実践的なパフォーマンスチューニングのテクニックと戦略を解説します。

## パフォーマンス分析の基礎

### パフォーマンスメトリクスの定義

```typescript
export interface PerformanceMetrics {
  latency: {
    p50: number;  // 50パーセンタイル
    p90: number;  // 90パーセンタイル
    p95: number;  // 95パーセンタイル
    p99: number;  // 99パーセンタイル
    max: number;  // 最大値
  };
  
  throughput: {
    requestsPerSecond: number;
    bytesPerSecond: number;
    concurrentConnections: number;
  };
  
  resources: {
    cpu: {
      usage: number;      // パーセンテージ
      throttling: number; // スロットリング時間
    };
    memory: {
      used: number;       // バイト
      heap: number;       // ヒープサイズ
      gcTime: number;     // GC時間
    };
    io: {
      diskReadOps: number;
      diskWriteOps: number;
      networkIn: number;
      networkOut: number;
    };
  };
  
  errors: {
    errorRate: number;
    timeouts: number;
    failures: number;
  };
}

export class PerformanceAnalyzer {
  // ボトルネックの特定
  async identifyBottlenecks(
    metrics: PerformanceMetrics[]
  ): Promise<BottleneckAnalysis> {
    const analysis: BottleneckAnalysis = {
      cpuBound: false,
      memoryBound: false,
      ioBound: false,
      networkBound: false,
      recommendations: []
    };
    
    // CPU分析
    const avgCpuUsage = this.calculateAverage(
      metrics.map(m => m.resources.cpu.usage)
    );
    
    if (avgCpuUsage > 80) {
      analysis.cpuBound = true;
      analysis.recommendations.push({
        type: "CPU_OPTIMIZATION",
        priority: "HIGH",
        suggestions: [
          "アルゴリズムの最適化",
          "並列処理の活用",
          "キャッシングの実装",
          "不要な計算の削減"
        ]
      });
    }
    
    // メモリ分析
    const memoryGrowthRate = this.calculateGrowthRate(
      metrics.map(m => m.resources.memory.used)
    );
    
    if (memoryGrowthRate > 0.1) { // 10%以上の増加率
      analysis.memoryBound = true;
      analysis.recommendations.push({
        type: "MEMORY_LEAK",
        priority: "CRITICAL",
        suggestions: [
          "メモリリークの調査",
          "オブジェクトプールの使用",
          "不要な参照の削除",
          "ガベージコレクションの最適化"
        ]
      });
    }
    
    // I/O分析
    const ioWaitTime = this.calculateIOWait(metrics);
    
    if (ioWaitTime > 30) { // 30%以上のI/O待機
      analysis.ioBound = true;
      analysis.recommendations.push({
        type: "IO_OPTIMIZATION",
        priority: "HIGH",
        suggestions: [
          "非同期I/Oの活用",
          "バッチ処理の実装",
          "データベースクエリの最適化",
          "インデックスの追加"
        ]
      });
    }
    
    return analysis;
  }
  
  // プロファイリングの実行
  async profileApplication(
    duration: number = 60000 // 1分間
  ): Promise<ProfilingResult> {
    const profiler = new CPUProfiler();
    const heapProfiler = new HeapProfiler();
    
    // CPUプロファイリング開始
    profiler.start();
    const heapSnapshot1 = await heapProfiler.takeSnapshot();
    
    // 実行
    await this.wait(duration);
    
    // プロファイリング終了
    const cpuProfile = profiler.stop();
    const heapSnapshot2 = await heapProfiler.takeSnapshot();
    
    // 分析
    return {
      cpu: this.analyzeCPUProfile(cpuProfile),
      memory: this.analyzeHeapDiff(heapSnapshot1, heapSnapshot2),
      flamegraph: this.generateFlamegraph(cpuProfile),
      recommendations: this.generateRecommendations(cpuProfile, heapSnapshot2)
    };
  }
}
```

## 最適化テクニック

### アルゴリズムの最適化

```typescript
export class AlgorithmOptimization {
  // 計算複雑度の改善
  improveTimeComplexity(): OptimizationExample {
    return {
      before: {
        name: "二重ループによる重複チェック",
        complexity: "O(n²)",
        implementation: `
          function findDuplicates(array: number[]): number[] {
            const duplicates: number[] = [];
            
            for (let i = 0; i < array.length; i++) {
              for (let j = i + 1; j < array.length; j++) {
                if (array[i] === array[j] && !duplicates.includes(array[i])) {
                  duplicates.push(array[i]);
                }
              }
            }
            
            return duplicates;
          }
        `
      },
      
      after: {
        name: "ハッシュマップを使用した最適化",
        complexity: "O(n)",
        implementation: `
          function findDuplicates(array: number[]): number[] {
            const seen = new Set<number>();
            const duplicates = new Set<number>();
            
            for (const num of array) {
              if (seen.has(num)) {
                duplicates.add(num);
              } else {
                seen.add(num);
              }
            }
            
            return Array.from(duplicates);
          }
        `,
        
        improvement: {
          timeComplexity: "O(n²) → O(n)",
          spaceComplexity: "O(1) → O(n)",
          performance: "100倍高速化（n=10000の場合）"
        }
      }
    };
  }
  
  // データ構造の選択
  selectOptimalDataStructure(): DataStructureComparison {
    return {
      scenario: "頻繁な挿入・削除・検索が必要なケース",
      
      options: [
        {
          structure: "Array",
          insertion: "O(n)",
          deletion: "O(n)",
          search: "O(n)",
          memory: "連続メモリ、キャッシュ効率良好",
          useCase: "小規模データ、順次アクセスが主"
        },
        {
          structure: "LinkedList",
          insertion: "O(1) at head/tail",
          deletion: "O(1) with reference",
          search: "O(n)",
          memory: "分散メモリ、オーバーヘッドあり",
          useCase: "頻繁な挿入・削除、サイズ可変"
        },
        {
          structure: "HashMap",
          insertion: "O(1) average",
          deletion: "O(1) average",
          search: "O(1) average",
          memory: "ハッシュテーブル、メモリ使用量大",
          useCase: "高速な検索が必要、キー・バリュー"
        },
        {
          structure: "B-Tree",
          insertion: "O(log n)",
          deletion: "O(log n)",
          search: "O(log n)",
          memory: "バランス木、ディスク効率良好",
          useCase: "データベース、範囲検索"
        }
      ],
      
      recommendation: `
        // 実装例：高速な挿入・削除・検索を実現
        class OptimizedDataStore<T> {
          private map = new Map<string, Node<T>>();
          private head: Node<T> | null = null;
          private tail: Node<T> | null = null;
          
          // O(1)での挿入
          insert(key: string, value: T): void {
            const node = new Node(key, value);
            this.map.set(key, node);
            
            if (!this.head) {
              this.head = this.tail = node;
            } else {
              node.prev = this.tail;
              this.tail!.next = node;
              this.tail = node;
            }
          }
          
          // O(1)での削除
          delete(key: string): boolean {
            const node = this.map.get(key);
            if (!node) return false;
            
            this.map.delete(key);
            this.removeNode(node);
            return true;
          }
          
          // O(1)での検索
          get(key: string): T | undefined {
            const node = this.map.get(key);
            return node?.value;
          }
        }
      `
    };
  }
}
```

### 非同期処理の最適化

```typescript
export class AsyncOptimization {
  // 並列処理の活用
  optimizeParallelProcessing(): ParallelizationStrategy {
    return {
      // 逐次処理（最適化前）
      sequential: {
        code: `
          async function processItems(items: Item[]): Promise<Result[]> {
            const results: Result[] = [];
            
            for (const item of items) {
              const result = await processItem(item); // 各アイテムを順番に処理
              results.push(result);
            }
            
            return results;
          }
        `,
        performance: {
          itemProcessTime: "100ms",
          totalItems: 100,
          totalTime: "10秒"
        }
      },
      
      // 並列処理（最適化後）
      parallel: {
        code: `
          async function processItems(items: Item[]): Promise<Result[]> {
            // 全アイテムを並列に処理
            return Promise.all(items.map(item => processItem(item)));
          }
        `,
        performance: {
          itemProcessTime: "100ms",
          totalItems: 100,
          totalTime: "100ms（同時実行数に依存）"
        }
      },
      
      // バッチ並列処理（リソース制限あり）
      batchParallel: {
        code: `
          async function processItemsInBatches(
            items: Item[],
            batchSize: number = 10
          ): Promise<Result[]> {
            const results: Result[] = [];
            
            for (let i = 0; i < items.length; i += batchSize) {
              const batch = items.slice(i, i + batchSize);
              const batchResults = await Promise.all(
                batch.map(item => processItem(item))
              );
              results.push(...batchResults);
            }
            
            return results;
          }
        `,
        performance: {
          itemProcessTime: "100ms",
          totalItems: 100,
          batchSize: 10,
          totalTime: "1秒（10バッチ × 100ms）"
        }
      },
      
      // 高度な並行制御
      advancedConcurrency: `
        import pLimit from 'p-limit';
        
        class ConcurrencyManager {
          private limit = pLimit(5); // 同時実行数を5に制限
          
          async processWithLimit<T, R>(
            items: T[],
            processor: (item: T) => Promise<R>
          ): Promise<R[]> {
            return Promise.all(
              items.map(item => 
                this.limit(() => processor(item))
              )
            );
          }
          
          // ストリーミング処理
          async *processStream<T, R>(
            items: AsyncIterable<T>,
            processor: (item: T) => Promise<R>
          ): AsyncGenerator<R> {
            const promises: Promise<R>[] = [];
            
            for await (const item of items) {
              promises.push(
                this.limit(() => processor(item))
              );
              
              // バッファサイズに達したら結果を順次yield
              if (promises.length >= 10) {
                yield await promises.shift()!;
              }
            }
            
            // 残りの結果をyield
            for (const promise of promises) {
              yield await promise;
            }
          }
        }
      `
    };
  }
  
  // イベントループの最適化
  optimizeEventLoop(): EventLoopOptimization {
    return {
      problem: "CPU集約的なタスクがイベントループをブロック",
      
      solutions: {
        // タスクの分割
        taskSplitting: `
          async function processLargeArray<T>(
            array: T[],
            processor: (item: T) => void,
            chunkSize: number = 1000
          ): Promise<void> {
            for (let i = 0; i < array.length; i += chunkSize) {
              const chunk = array.slice(i, i + chunkSize);
              
              // チャンクごとに処理
              chunk.forEach(processor);
              
              // イベントループに制御を戻す
              await new Promise(resolve => setImmediate(resolve));
            }
          }
        `,
        
        // ワーカースレッドの活用
        workerThreads: `
          import { Worker } from 'worker_threads';
          
          class WorkerPool {
            private workers: Worker[] = [];
            private queue: Array<{
              data: any;
              resolve: (value: any) => void;
              reject: (error: any) => void;
            }> = [];
            
            constructor(
              private workerScript: string,
              private poolSize: number = 4
            ) {
              this.initializeWorkers();
            }
            
            private initializeWorkers(): void {
              for (let i = 0; i < this.poolSize; i++) {
                const worker = new Worker(this.workerScript);
                
                worker.on('message', (result) => {
                  // 次のタスクを処理
                  const next = this.queue.shift();
                  if (next) {
                    worker.postMessage(next.data);
                    next.resolve(result);
                  } else {
                    this.workers.push(worker);
                  }
                });
                
                this.workers.push(worker);
              }
            }
            
            async execute<T, R>(data: T): Promise<R> {
              return new Promise((resolve, reject) => {
                const worker = this.workers.pop();
                
                if (worker) {
                  worker.postMessage(data);
                  worker.once('message', resolve);
                } else {
                  this.queue.push({ data, resolve, reject });
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

## キャッシング戦略

### 多層キャッシュアーキテクチャ

```typescript
export class CachingStrategy {
  // キャッシュレイヤーの設計
  implementMultiLayerCache(): CacheArchitecture {
    return {
      layers: [
        {
          name: "L1: プロセス内キャッシュ",
          type: "In-Memory",
          implementation: `
            class L1Cache {
              private cache = new Map<string, CacheEntry>();
              private maxSize: number = 1000;
              private ttl: number = 60000; // 1分
              
              get(key: string): any {
                const entry = this.cache.get(key);
                
                if (!entry) return null;
                
                // TTLチェック
                if (Date.now() > entry.expiry) {
                  this.cache.delete(key);
                  return null;
                }
                
                // LRU更新
                entry.lastAccessed = Date.now();
                return entry.value;
              }
              
              set(key: string, value: any, ttl?: number): void {
                // サイズ制限チェック
                if (this.cache.size >= this.maxSize) {
                  this.evictLRU();
                }
                
                this.cache.set(key, {
                  value,
                  expiry: Date.now() + (ttl || this.ttl),
                  lastAccessed: Date.now()
                });
              }
              
              private evictLRU(): void {
                let oldest = Date.now();
                let oldestKey = "";
                
                for (const [key, entry] of this.cache.entries()) {
                  if (entry.lastAccessed < oldest) {
                    oldest = entry.lastAccessed;
                    oldestKey = key;
                  }
                }
                
                if (oldestKey) {
                  this.cache.delete(oldestKey);
                }
              }
            }
          `,
          characteristics: {
            latency: "< 1ms",
            capacity: "1000 items",
            scope: "Process",
            persistence: "None"
          }
        },
        
        {
          name: "L2: Redis分散キャッシュ",
          type: "Distributed",
          implementation: `
            class L2Cache {
              private redis: Redis;
              private defaultTTL = 3600; // 1時間
              
              async get(key: string): Promise<any> {
                try {
                  const value = await this.redis.get(key);
                  return value ? JSON.parse(value) : null;
                } catch (error) {
                  // キャッシュミスとして扱う
                  return null;
                }
              }
              
              async set(
                key: string,
                value: any,
                ttl?: number
              ): Promise<void> {
                await this.redis.setex(
                  key,
                  ttl || this.defaultTTL,
                  JSON.stringify(value)
                );
              }
              
              // パイプライニングによるバッチ操作
              async mget(keys: string[]): Promise<any[]> {
                const pipeline = this.redis.pipeline();
                
                keys.forEach(key => pipeline.get(key));
                
                const results = await pipeline.exec();
                return results.map(([err, value]) => 
                  value ? JSON.parse(value) : null
                );
              }
              
              // キャッシュウォーミング
              async warmup(
                keys: string[],
                loader: (key: string) => Promise<any>
              ): Promise<void> {
                const missing = await this.findMissingKeys(keys);
                
                await Promise.all(
                  missing.map(async key => {
                    const value = await loader(key);
                    await this.set(key, value);
                  })
                );
              }
            }
          `,
          characteristics: {
            latency: "1-5ms",
            capacity: "10GB+",
            scope: "Cluster",
            persistence: "Optional"
          }
        },
        
        {
          name: "L3: CDNエッジキャッシュ",
          type: "Edge",
          configuration: {
            provider: "CloudFlare",
            rules: [
              {
                pattern: "/api/static/*",
                ttl: 86400, // 24時間
                cacheKey: "URL + Accept header"
              },
              {
                pattern: "/api/user/*",
                ttl: 300, // 5分
                cacheKey: "URL + Authorization header",
                purgeOnUpdate: true
              }
            ]
          }
        }
      ],
      
      // キャッシュ戦略
      strategies: {
        cacheAside: `
          async function getWithCache(
            key: string,
            loader: () => Promise<any>
          ): Promise<any> {
            // L1キャッシュチェック
            let value = l1Cache.get(key);
            if (value) return value;
            
            // L2キャッシュチェック
            value = await l2Cache.get(key);
            if (value) {
              l1Cache.set(key, value);
              return value;
            }
            
            // データソースから読み込み
            value = await loader();
            
            // キャッシュに書き込み
            await Promise.all([
              l1Cache.set(key, value),
              l2Cache.set(key, value)
            ]);
            
            return value;
          }
        `,
        
        writeThrough: `
          async function updateWithCache(
            key: string,
            value: any
          ): Promise<void> {
            // データソースに書き込み
            await dataSource.update(key, value);
            
            // キャッシュを更新
            await Promise.all([
              l1Cache.set(key, value),
              l2Cache.set(key, value),
              cdnCache.purge(key)
            ]);
          }
        `
      }
    };
  }
  
  // キャッシュ最適化テクニック
  implementCacheOptimizations(): CacheOptimizations {
    return {
      // キャッシュスタンピード対策
      stampedePrevention: `
        class StampedeProtection {
          private locks = new Map<string, Promise<any>>();
          
          async get(
            key: string,
            loader: () => Promise<any>
          ): Promise<any> {
            // 既に取得中の場合は待機
            const existingLock = this.locks.get(key);
            if (existingLock) {
              return existingLock;
            }
            
            // キャッシュチェック
            const cached = await cache.get(key);
            if (cached) return cached;
            
            // 新しい取得を開始
            const promise = this.loadWithLock(key, loader);
            this.locks.set(key, promise);
            
            try {
              return await promise;
            } finally {
              this.locks.delete(key);
            }
          }
          
          private async loadWithLock(
            key: string,
            loader: () => Promise<any>
          ): Promise<any> {
            const value = await loader();
            await cache.set(key, value);
            return value;
          }
        }
      `,
      
      // プリフェッチング
      prefetching: `
        class PrefetchStrategy {
          async handleRequest(
            requestedKey: string
          ): Promise<any> {
            // リクエストされたデータを取得
            const result = await cache.get(requestedKey);
            
            // 関連データをバックグラウンドでプリフェッチ
            this.prefetchRelated(requestedKey);
            
            return result;
          }
          
          private async prefetchRelated(
            key: string
          ): Promise<void> {
            const relatedKeys = this.predictRelatedKeys(key);
            
            // 非同期でプリフェッチ
            Promise.all(
              relatedKeys.map(async relatedKey => {
                const cached = await cache.get(relatedKey);
                if (!cached) {
                  const value = await loader(relatedKey);
                  await cache.set(relatedKey, value);
                }
              })
            );
          }
          
          private predictRelatedKeys(key: string): string[] {
            // 機械学習や統計的分析に基づく予測
            // ここでは簡単な例
            if (key.includes("product")) {
              const productId = this.extractProductId(key);
              return [
                \`reviews:\${productId}\`,
                \`recommendations:\${productId}\`,
                \`inventory:\${productId}\`
              ];
            }
            
            return [];
          }
        }
      `
    };
  }
}
```

## データベース最適化

### クエリ最適化

```typescript
export class DatabaseOptimization {
  // インデックス戦略
  implementIndexingStrategy(): IndexingGuide {
    return {
      principles: {
        selectivity: "高い選択性を持つカラムにインデックスを作成",
        cardinality: "カーディナリティの高いカラムを優先",
        covering: "カバリングインデックスでI/Oを削減",
        composite: "複合インデックスは左端から使用される"
      },
      
      examples: {
        // 単一カラムインデックス
        singleColumn: `
          -- ユーザー検索の最適化
          CREATE INDEX idx_users_email ON users(email);
          
          -- 日付範囲検索の最適化
          CREATE INDEX idx_orders_created_at ON orders(created_at);
        `,
        
        // 複合インデックス
        compositeIndex: `
          -- WHERE句とORDER BY句の最適化
          CREATE INDEX idx_orders_user_date 
          ON orders(user_id, created_at DESC);
          
          -- クエリ例
          SELECT * FROM orders 
          WHERE user_id = 123 
          ORDER BY created_at DESC 
          LIMIT 10;
        `,
        
        // カバリングインデックス
        coveringIndex: `
          -- 必要な全カラムをインデックスに含める
          CREATE INDEX idx_products_covering 
          ON products(category_id, status, price)
          INCLUDE (name, stock_quantity);
          
          -- テーブルアクセスなしで結果を返す
          SELECT name, price, stock_quantity 
          FROM products 
          WHERE category_id = 5 
          AND status = 'active' 
          AND price < 100;
        `,
        
        // 部分インデックス
        partialIndex: `
          -- 条件付きインデックス（PostgreSQL）
          CREATE INDEX idx_orders_pending 
          ON orders(created_at) 
          WHERE status = 'pending';
          
          -- アクティブユーザーのみのインデックス
          CREATE INDEX idx_users_active 
          ON users(last_login) 
          WHERE deleted_at IS NULL;
        `
      },
      
      monitoring: {
        // インデックス使用状況の監視
        usageQuery: `
          -- PostgreSQL: インデックス使用統計
          SELECT 
            schemaname,
            tablename,
            indexname,
            idx_scan,
            idx_tup_read,
            idx_tup_fetch
          FROM pg_stat_user_indexes
          ORDER BY idx_scan;
          
          -- MySQL: インデックス使用状況
          SELECT 
            table_schema,
            table_name,
            index_name,
            cardinality,
            seq_in_index
          FROM information_schema.statistics
          WHERE table_schema = 'your_database';
        `,
        
        // 不足インデックスの検出
        missingIndexes: `
          -- スロークエリログから頻繁なテーブルスキャンを検出
          SELECT 
            query,
            calls,
            total_time,
            mean_time,
            rows
          FROM pg_stat_statements
          WHERE query LIKE '%Seq Scan%'
          ORDER BY total_time DESC;
        `
      }
    };
  }
  
  // クエリパフォーマンスチューニング
  optimizeQueries(): QueryOptimizationTechniques {
    return {
      // N+1問題の解決
      nPlusOne: {
        problem: `
          // N+1クエリの例
          const users = await db.query("SELECT * FROM users");
          
          for (const user of users) {
            // 各ユーザーごとに追加クエリ
            const orders = await db.query(
              "SELECT * FROM orders WHERE user_id = ?",
              [user.id]
            );
            user.orders = orders;
          }
        `,
        
        solution: `
          // JOINによる解決
          const usersWithOrders = await db.query(\`
            SELECT 
              u.*,
              o.id as order_id,
              o.total as order_total,
              o.created_at as order_created_at
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id
            ORDER BY u.id, o.created_at DESC
          \`);
          
          // またはバッチ読み込み
          const users = await db.query("SELECT * FROM users");
          const userIds = users.map(u => u.id);
          
          const orders = await db.query(
            "SELECT * FROM orders WHERE user_id IN (?)",
            [userIds]
          );
          
          // メモリ内で結合
          const ordersByUser = groupBy(orders, 'user_id');
          users.forEach(user => {
            user.orders = ordersByUser[user.id] || [];
          });
        `
      },
      
      // ページネーション最適化
      pagination: {
        // オフセットベース（非効率）
        offsetBased: `
          -- 大きなオフセットは遅い
          SELECT * FROM products 
          ORDER BY created_at DESC 
          LIMIT 20 OFFSET 10000; -- 10000行をスキップ
        `,
        
        // カーソルベース（効率的）
        cursorBased: `
          -- 前回の最後のIDを使用
          SELECT * FROM products 
          WHERE id < :last_id 
          ORDER BY id DESC 
          LIMIT 20;
          
          -- 複合カーソル
          SELECT * FROM products 
          WHERE (created_at, id) < (:last_created_at, :last_id)
          ORDER BY created_at DESC, id DESC 
          LIMIT 20;
        `,
        
        // キーセットページネーション実装
        implementation: `
          class KeysetPagination {
            async getPage(
              cursor?: { created_at: Date; id: number },
              limit: number = 20
            ): Promise<PageResult> {
              let query = \`
                SELECT * FROM products 
                WHERE status = 'active'
              \`;
              
              const params: any[] = [];
              
              if (cursor) {
                query += \` AND (created_at, id) < (?, ?)\`;
                params.push(cursor.created_at, cursor.id);
              }
              
              query += \` ORDER BY created_at DESC, id DESC LIMIT ?\`;
              params.push(limit + 1);
              
              const results = await db.query(query, params);
              
              const hasNext = results.length > limit;
              const items = hasNext ? results.slice(0, -1) : results;
              
              const nextCursor = hasNext ? {
                created_at: items[items.length - 1].created_at,
                id: items[items.length - 1].id
              } : null;
              
              return { items, nextCursor, hasNext };
            }
          }
        `
      }
    };
  }
}