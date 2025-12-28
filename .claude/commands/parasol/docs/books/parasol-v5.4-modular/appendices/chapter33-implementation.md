# 付録：第33章　パフォーマンスチューニングの実装詳細

## パフォーマンスメトリクスの定義と収集

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
```

## ボトルネック分析の実装

```typescript
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

## アルゴリズム最適化の実装例

<div id="patterns"></div>

### 計算複雑度の改善

```typescript
// 最適化前：O(n²)の重複検出
function findDuplicatesSlow(array: number[]): number[] {
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

// 最適化後：O(n)の重複検出
function findDuplicatesFast(array: number[]): number[] {
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
```

### データ構造の最適化

```typescript
// 高速な挿入・削除・検索を実現するデータ構造
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
  
  private removeNode(node: Node<T>): void {
    if (node.prev) {
      node.prev.next = node.next;
    } else {
      this.head = node.next;
    }
    
    if (node.next) {
      node.next.prev = node.prev;
    } else {
      this.tail = node.prev;
    }
  }
}
```

## 並列処理の実装パターン

### バッチ並列処理

```typescript
async function processItemsInBatches<T, R>(
  items: T[],
  processor: (item: T) => Promise<R>,
  batchSize: number = 10
): Promise<R[]> {
  const results: R[] = [];
  
  for (let i = 0; i < items.length; i += batchSize) {
    const batch = items.slice(i, i + batchSize);
    const batchResults = await Promise.all(
      batch.map(item => processor(item))
    );
    results.push(...batchResults);
  }
  
  return results;
}
```

### 並行制御付き処理

```typescript
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
```

### ワーカースレッドプール

```typescript
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
```

## 多層キャッシュの実装

### L1キャッシュ（プロセス内）

```typescript
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
```

### L2キャッシュ（Redis）

```typescript
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
```

### キャッシュスタンピード対策

```typescript
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
```

## データベース最適化

### インデックス戦略

```sql
-- 単一カラムインデックス
CREATE INDEX idx_users_email ON users(email);

-- 複合インデックス（WHERE句とORDER BY句の最適化）
CREATE INDEX idx_orders_user_date 
ON orders(user_id, created_at DESC);

-- カバリングインデックス
CREATE INDEX idx_products_covering 
ON products(category_id, status, price)
INCLUDE (name, stock_quantity);

-- 部分インデックス（PostgreSQL）
CREATE INDEX idx_orders_pending 
ON orders(created_at) 
WHERE status = 'pending';
```

### N+1問題の解決

```typescript
// 問題：N+1クエリ
const users = await db.query("SELECT * FROM users");

for (const user of users) {
  const orders = await db.query(
    "SELECT * FROM orders WHERE user_id = ?",
    [user.id]
  );
  user.orders = orders;
}

// 解決策1：JOINを使用
const usersWithOrders = await db.query(`
  SELECT 
    u.*,
    o.id as order_id,
    o.total as order_total,
    o.created_at as order_created_at
  FROM users u
  LEFT JOIN orders o ON u.id = o.user_id
  ORDER BY u.id, o.created_at DESC
`);

// 解決策2：バッチ読み込み
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
```

### キーセットページネーション

```typescript
class KeysetPagination {
  async getPage(
    cursor?: { created_at: Date; id: number },
    limit: number = 20
  ): Promise<PageResult> {
    let query = `
      SELECT * FROM products 
      WHERE status = 'active'
    `;
    
    const params: any[] = [];
    
    if (cursor) {
      query += ` AND (created_at, id) < (?, ?)`;
      params.push(cursor.created_at, cursor.id);
    }
    
    query += ` ORDER BY created_at DESC, id DESC LIMIT ?`;
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
```

## パフォーマンステストの自動化

<div id="automation"></div>

```typescript
import { performance } from 'perf_hooks';

class PerformanceTester {
  async runLoadTest(
    scenario: LoadTestScenario
  ): Promise<LoadTestResult> {
    const results: RequestMetric[] = [];
    const startTime = performance.now();
    
    // ウォームアップ
    await this.warmup(scenario.warmupRequests);
    
    // 並行リクエストの実行
    const promises: Promise<void>[] = [];
    for (let i = 0; i < scenario.totalRequests; i++) {
      promises.push(this.executeRequest(scenario, results));
      
      // レート制限
      if ((i + 1) % scenario.concurrency === 0) {
        await Promise.all(promises);
        promises.length = 0;
      }
    }
    
    // 残りのリクエストを実行
    await Promise.all(promises);
    
    const endTime = performance.now();
    
    return this.analyzeResults(results, startTime, endTime);
  }
  
  private async executeRequest(
    scenario: LoadTestScenario,
    results: RequestMetric[]
  ): Promise<void> {
    const startTime = performance.now();
    
    try {
      const response = await fetch(scenario.url, {
        method: scenario.method,
        headers: scenario.headers,
        body: scenario.body
      });
      
      const endTime = performance.now();
      
      results.push({
        duration: endTime - startTime,
        statusCode: response.status,
        success: response.ok,
        timestamp: new Date()
      });
    } catch (error) {
      const endTime = performance.now();
      
      results.push({
        duration: endTime - startTime,
        statusCode: 0,
        success: false,
        error: error.message,
        timestamp: new Date()
      });
    }
  }
  
  private analyzeResults(
    results: RequestMetric[],
    startTime: number,
    endTime: number
  ): LoadTestResult {
    const durations = results
      .filter(r => r.success)
      .map(r => r.duration)
      .sort((a, b) => a - b);
    
    return {
      totalRequests: results.length,
      successfulRequests: results.filter(r => r.success).length,
      failedRequests: results.filter(r => !r.success).length,
      totalDuration: endTime - startTime,
      requestsPerSecond: results.length / ((endTime - startTime) / 1000),
      latency: {
        min: Math.min(...durations),
        max: Math.max(...durations),
        mean: durations.reduce((a, b) => a + b, 0) / durations.length,
        p50: this.percentile(durations, 0.5),
        p90: this.percentile(durations, 0.9),
        p95: this.percentile(durations, 0.95),
        p99: this.percentile(durations, 0.99)
      }
    };
  }
  
  private percentile(sorted: number[], p: number): number {
    const index = Math.ceil(sorted.length * p) - 1;
    return sorted[Math.max(0, index)];
  }
}
```