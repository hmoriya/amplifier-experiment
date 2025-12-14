# APIオーケストレーションパターン：シンプルさを追求するマイクロサービス統合

## 推奨パターン：Orchestration at the Edge

### 基本原則

イベント駆動アーキテクチャの複雑さを回避し、シンプルで理解しやすいシステムを構築するため、以下の原則を採用します：

```
1. APIファースト（同期通信）
2. クライアントサイドオーケストレーション
3. 各サービスの独立性維持
4. バッチ処理による非同期処理の分離
```

### アーキテクチャ構成

```
┌─────────────────────────────────────────────────────────┐
│              Frontend / Mobile App                       │
│                                                         │
│  async function createOrder() {                         │
│    // 1. 在庫確認                                       │
│    const stock = await inventoryAPI.check(productId)   │
│    if (!stock.available) return showError()            │
│                                                         │
│    // 2. 注文作成                                       │
│    const order = await orderAPI.create(orderData)      │
│                                                         │
│    // 3. 決済処理                                       │
│    const payment = await paymentAPI.charge(order.id)   │
│                                                         │
│    // 4. 在庫減算                                       │
│    await inventoryAPI.decrement(productId, quantity)   │
│                                                         │
│    return { order, payment }                           │
│  }                                                      │
│                                                         │
└─────────────────────┬───────────────────────────────────┘
                      │
    ┌─────────────────┼─────────────────┬─────────────────┐
    ▼                 ▼                 ▼                 ▼
┌─────────┐    ┌─────────┐      ┌─────────┐      ┌─────────┐
│Inventory│    │  Order  │      │ Payment │      │Shipping │
│   API   │    │   API   │      │   API   │      │   API   │
└─────────┘    └─────────┘      └─────────┘      └─────────┘
```

### メリット

1. **理解しやすさ**
   - 処理フローが明確で追跡しやすい
   - デバッグが容易
   - 新規開発者の学習曲線が緩やか

2. **変更の容易さ**
   - 各サービスが独立しているため個別に更新可能
   - APIバージョニングで後方互換性を保持
   - フロントエンドの変更で新しいフローに対応

3. **運用の簡素化**
   - トランザクションログが不要
   - メッセージキューの管理が不要
   - 監視ポイントが明確

### 実装パターン

#### 1. エラーハンドリング

```javascript
// フロントエンドでの実装例
class OrderService {
  async createOrder(orderData) {
    const errors = [];
    
    try {
      // 各APIコールを独立して実行
      const stock = await this.checkInventory(orderData.items);
      if (!stock.sufficient) {
        return { 
          success: false, 
          error: 'INSUFFICIENT_STOCK',
          details: stock.unavailableItems 
        };
      }
      
      const order = await this.createOrderRecord(orderData);
      const payment = await this.processPayment(order);
      
      if (payment.failed) {
        // 補償トランザクション
        await this.cancelOrder(order.id);
        return { 
          success: false, 
          error: 'PAYMENT_FAILED',
          details: payment.error 
        };
      }
      
      return { success: true, order, payment };
      
    } catch (error) {
      // ネットワークエラー等の処理
      return { 
        success: false, 
        error: 'SYSTEM_ERROR',
        details: error.message 
      };
    }
  }
}
```

#### 2. 冪等性の確保

```javascript
// APIサーバー側の実装例
class OrderAPI {
  async createOrder(request) {
    const idempotencyKey = request.headers['idempotency-key'];
    
    // 既存の結果を返す
    const existing = await this.cache.get(idempotencyKey);
    if (existing) {
      return existing;
    }
    
    // 新規作成
    const order = await this.orderService.create(request.body);
    
    // 結果をキャッシュ
    await this.cache.set(idempotencyKey, order, ttl = 3600);
    
    return order;
  }
}
```

#### 3. バッチ処理との連携

```yaml
# 日次バッチ処理の例
daily-reconciliation:
  schedule: "0 2 * * *"  # 毎日午前2時
  steps:
    - name: "注文集計"
      query: "SELECT * FROM orders WHERE created_at >= :yesterday"
    
    - name: "在庫同期"
      action: "reconcile_inventory_with_orders"
    
    - name: "レポート生成"
      output: "daily_sales_report.csv"
```

### ベストプラクティス

#### 1. API設計原則

- **RESTful設計**: 標準的なHTTP動詞を使用
- **バージョニング**: URLパス（/api/v1/orders）で管理
- **ページネーション**: 大量データの効率的な取得
- **フィルタリング**: クエリパラメータで柔軟に対応

#### 2. パフォーマンス最適化

```javascript
// 並列実行可能な処理
async function getOrderDetails(orderId) {
  const [order, customer, items] = await Promise.all([
    orderAPI.get(orderId),
    customerAPI.get(customerId),
    orderItemsAPI.list(orderId)
  ]);
  
  return { order, customer, items };
}
```

#### 3. 監視とロギング

```javascript
// 統一されたロギング
class APIClient {
  async request(method, url, data) {
    const requestId = generateRequestId();
    const start = Date.now();
    
    logger.info({
      requestId,
      method,
      url,
      timestamp: start
    });
    
    try {
      const response = await fetch(url, { method, body: data });
      
      logger.info({
        requestId,
        status: response.status,
        duration: Date.now() - start
      });
      
      return response;
    } catch (error) {
      logger.error({
        requestId,
        error: error.message,
        duration: Date.now() - start
      });
      throw error;
    }
  }
}
```

### セキュリティ考慮事項

1. **認証・認可**
   - OAuth 2.0 / OpenID Connect
   - API Gateway でのトークン検証
   - スコープベースのアクセス制御

2. **レート制限**
   - クライアント単位での制限
   - APIエンドポイント別の制限
   - 優先度に基づくスロットリング

3. **データ保護**
   - HTTPS必須
   - センシティブデータのマスキング
   - 監査ログの保持

### 移行戦略

既存のイベント駆動システムからの移行：

1. **段階的移行**
   - 新機能はAPIファーストで実装
   - 既存機能は徐々に置き換え
   - 並行稼働期間を設ける

2. **互換性維持**
   - イベントをAPIコールに変換するアダプター
   - 既存バッチ処理の維持
   - データ整合性の監視

### まとめ

このパターンは以下の場合に特に有効です：

- **中規模システム**: 過度な複雑性を避けたい
- **開発チームの規模**: 小〜中規模チーム
- **運用体制**: シンプルな運用を好む
- **ビジネス要件**: リアルタイム性より確実性を重視

イベント駆動アーキテクチャは強力ですが、その複雑さは多くの場合オーバーエンジニアリングになります。シンプルなAPIベースのアプローチで、保守性と拡張性を両立できます。

---

**参考資料**:
- Martin Fowler: "Microservices" (Smart endpoints and dumb pipes)
- Sam Newman: "Building Microservices" (Chapter 4: Integration)
- Netflix Technology Blog: "Optimizing the Netflix API"