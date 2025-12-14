# レガシー統合ハブパターン：実践的なマイクロサービス統合アプローチ

## 概要

レガシーシステムや外部システムとの統合を、専用の「統合ハブマイクロサービス」で管理するパターン。このパターンは、Anti-Corruption Layer (ACL) の概念を拡張し、複数のレガシーシステムとの統合を一元管理します。

## アーキテクチャ構成

```
┌────────────────────────────────────────────────────────────┐
│                  Core Microservices                        │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐     │
│  │Order MS │  │User MS  │  │Product  │  │Payment  │     │
│  │         │  │         │  │   MS    │  │   MS    │     │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘     │
│       │            │            │            │            │
└───────┼────────────┼────────────┼────────────┼────────────┘
        │            │            │            │
        └────────────┴────────────┴────────────┘
                         │
                         ▼
        ┌────────────────────────────────────┐
        │    Integration Hub Service         │
        │  ┌─────────────────────────────┐   │
        │  │ • データ変換               │   │
        │  │ • プロトコル変換           │   │
        │  │ • キャッシュ管理           │   │
        │  │ • エラーハンドリング       │   │
        │  │ • 監視・ログ              │   │
        │  └─────────────────────────────┘   │
        │           ┌───────────┐            │
        │           │ Cache DB  │            │
        │           └───────────┘            │
        └────────────────┬───────────────────┘
                         │
        ┌────────────────┴────────────────┐
        │                                 │
        ▼                                 ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│Legacy ERP   │  │External API │  │Legacy DB    │
│(SOAP)       │  │(REST)       │  │(Direct)     │
└─────────────┘  └─────────────┘  └─────────────┘
```

## パターンの特徴

### 1. 統合ハブの責務

```yaml
Integration Hub Service:
  データ取得:
    - バッチ同期（夜間処理）
    - リアルタイムAPI呼び出し
    - Change Data Capture (CDC)
    
  データ変換:
    - レガシーモデル → ドメインモデル
    - プロトコル変換（SOAP → REST）
    - データフォーマット変換
    
  データ管理:
    - キャッシュ戦略
    - データ鮮度管理
    - 整合性保証
    
  運用機能:
    - エラーハンドリング
    - リトライ処理
    - 監視・アラート
    - 監査ログ
```

### 2. 実装例

#### 統合ハブサービスの基本構造

```python
# integration_hub_service.py
from typing import Dict, Optional
from datetime import datetime, timedelta
import asyncio

class IntegrationHubService:
    def __init__(self, cache_service, legacy_clients):
        self.cache = cache_service
        self.legacy_erp = legacy_clients['erp']
        self.external_api = legacy_clients['external']
        self.legacy_db = legacy_clients['database']
        
    async def get_customer_data(self, customer_id: str) -> Dict:
        """顧客データの統合取得"""
        # 1. キャッシュチェック
        cached_data = await self.cache.get(f"customer:{customer_id}")
        if cached_data and self._is_fresh(cached_data):
            return cached_data['data']
            
        # 2. レガシーシステムから取得
        try:
            # 並列取得で高速化
            erp_data, external_data = await asyncio.gather(
                self._get_from_erp(customer_id),
                self._get_from_external_api(customer_id),
                return_exceptions=True
            )
            
            # 3. データ変換と統合
            integrated_data = self._transform_and_merge(
                erp_data, 
                external_data
            )
            
            # 4. キャッシュに保存
            await self.cache.set(
                f"customer:{customer_id}",
                {
                    'data': integrated_data,
                    'timestamp': datetime.now(),
                    'ttl': 3600  # 1時間
                }
            )
            
            return integrated_data
            
        except Exception as e:
            # フォールバック：古いキャッシュデータを返す
            if cached_data:
                logger.warning(f"Using stale cache due to error: {e}")
                return cached_data['data']
            raise
    
    def _transform_and_merge(self, erp_data, external_data):
        """レガシーデータをドメインモデルに変換"""
        return {
            'customerId': erp_data.get('CUST_ID'),
            'name': erp_data.get('CUST_NAME'),
            'email': external_data.get('email'),
            'status': self._map_status(erp_data.get('STATUS')),
            'creditLimit': float(erp_data.get('CREDIT_LMT', 0)),
            'lastUpdated': datetime.now().isoformat()
        }
```

#### バッチ同期の実装

```python
# batch_sync_service.py
class BatchSyncService:
    def __init__(self, integration_hub, scheduler):
        self.hub = integration_hub
        self.scheduler = scheduler
        
    def setup_sync_jobs(self):
        """バッチ同期ジョブの設定"""
        # 毎日午前2時に顧客データ同期
        self.scheduler.add_job(
            self.sync_customers,
            'cron',
            hour=2,
            minute=0,
            id='customer_sync'
        )
        
        # 4時間ごとに在庫データ同期
        self.scheduler.add_job(
            self.sync_inventory,
            'interval',
            hours=4,
            id='inventory_sync'
        )
    
    async def sync_customers(self):
        """顧客マスタの同期"""
        logger.info("Starting customer sync batch")
        
        # 1. 差分データの取得
        last_sync = await self.get_last_sync_timestamp('customers')
        changes = await self.hub.legacy_erp.get_customer_changes(last_sync)
        
        # 2. バッチ処理
        for batch in self._chunk(changes, size=100):
            await self._process_customer_batch(batch)
            
        # 3. 同期タイムスタンプ更新
        await self.update_sync_timestamp('customers')
```

#### API Gateway的な使い方

```javascript
// フロントエンドからの利用例
class CustomerService {
  constructor(apiClient) {
    this.api = apiClient;
    this.integrationHub = `${API_BASE}/integration-hub`;
  }
  
  async getCustomerProfile(customerId) {
    // 統合ハブ経由でレガシーデータを取得
    const legacyData = await this.api.get(
      `${this.integrationHub}/customers/${customerId}`
    );
    
    // コアマイクロサービスから最新データを取得
    const currentOrders = await this.api.get(
      `/order-service/customers/${customerId}/orders`
    );
    
    // フロントエンドで統合
    return {
      ...legacyData,
      recentOrders: currentOrders
    };
  }
}
```

### 3. エラーハンドリングとレジリエンス

```python
from tenacity import retry, stop_after_attempt, wait_exponential

class ResilientIntegrationHub:
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def call_legacy_system(self, request):
        """レガシーシステムへの呼び出し（リトライ付き）"""
        try:
            response = await self.legacy_client.call(request)
            return response
        except TimeoutError:
            # タイムアウト時はキャッシュから返す
            return await self.get_from_cache_or_fail(request)
        except Exception as e:
            logger.error(f"Legacy system error: {e}")
            raise
    
    async def get_with_fallback(self, key, primary_source, fallback_source):
        """フォールバック付きデータ取得"""
        try:
            # プライマリソースから取得
            return await primary_source(key)
        except Exception as primary_error:
            logger.warning(f"Primary source failed: {primary_error}")
            try:
                # フォールバックソースから取得
                return await fallback_source(key)
            except Exception as fallback_error:
                logger.error(f"All sources failed: {fallback_error}")
                # 最後の手段：デフォルト値
                return self.get_default_value(key)
```

### 4. 監視とオペレーション

```yaml
# monitoring.yaml
metrics:
  integration_hub:
    - name: legacy_call_duration
      type: histogram
      labels: [system, endpoint]
      
    - name: cache_hit_rate
      type: gauge
      labels: [data_type]
      
    - name: sync_job_duration
      type: histogram
      labels: [job_name]
      
    - name: error_rate
      type: counter
      labels: [system, error_type]

alerts:
  - name: HighLegacyLatency
    condition: legacy_call_duration > 5s
    for: 5m
    
  - name: LowCacheHitRate
    condition: cache_hit_rate < 0.8
    for: 10m
    
  - name: SyncJobFailed
    condition: sync_job_status == "failed"
    for: 1m
```

## ベストプラクティス

### 1. キャッシュ戦略

```python
class CacheStrategy:
    """データタイプ別のキャッシュ戦略"""
    
    STRATEGIES = {
        'customer_master': {
            'ttl': 86400,      # 24時間
            'refresh': True,   # バックグラウンド更新
            'fallback': True   # エラー時は古いデータ使用
        },
        'inventory': {
            'ttl': 300,        # 5分
            'refresh': False,  # リアルタイム性重視
            'fallback': False  # 正確性重視
        },
        'product_catalog': {
            'ttl': 3600,       # 1時間
            'refresh': True,
            'fallback': True
        }
    }
```

### 2. データ変換パターン

```python
class DataTransformer:
    """レガシーデータの変換"""
    
    def __init__(self):
        self.mappers = {
            'customer': CustomerMapper(),
            'order': OrderMapper(),
            'product': ProductMapper()
        }
    
    def transform(self, data_type, legacy_data):
        mapper = self.mappers.get(data_type)
        if not mapper:
            raise ValueError(f"Unknown data type: {data_type}")
            
        # 1. 検証
        mapper.validate(legacy_data)
        
        # 2. 変換
        domain_model = mapper.to_domain(legacy_data)
        
        # 3. エンリッチメント
        enriched = mapper.enrich(domain_model)
        
        return enriched
```

### 3. 段階的移行

```nginx
# 段階的な統合ハブへの移行
location /api/customers {
    # 読み取りは統合ハブ経由
    if ($request_method = GET) {
        proxy_pass http://integration-hub;
    }
    
    # 書き込みは直接レガシーへ（移行前）
    if ($request_method != GET) {
        proxy_pass http://legacy-system;
    }
}
```

## まとめ

統合ハブパターンの利点：

1. **複雑性の隔離**: レガシー統合の複雑性を1箇所に集約
2. **段階的移行**: 新旧システムの共存が可能
3. **パフォーマンス**: キャッシュによる高速化
4. **信頼性**: フォールバックとエラーハンドリング
5. **運用性**: 監視ポイントの明確化

このパターンは、特に以下の状況で有効：
- 複数のレガシーシステムが存在
- 段階的なモダナイゼーションが必要
- リアルタイムとバッチの混在
- 高い可用性要求

シンプルなAPI統合と組み合わせることで、実践的で保守性の高いマイクロサービスアーキテクチャを実現できます。