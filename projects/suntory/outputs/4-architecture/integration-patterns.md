# 統合パターン定義

**作成日**: 2025-12-05
**プロジェクト**: サントリーグループ
**Phase**: 4 - Architecture Design

---

## 1. 統合パターン概要

### 1.1 パターン選択基準

```
┌─────────────────────────────────────────────────────────────────────┐
│                    統合パターン選択フローチャート                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  即座にレスポンスが必要？                                            │
│       │                                                             │
│       ├─ Yes → 同期通信                                             │
│       │         │                                                   │
│       │         ├─ 外部/ブラウザから？ → REST API                   │
│       │         │                                                   │
│       │         └─ 内部/高速必要？ → gRPC                           │
│       │                                                             │
│       └─ No → 非同期通信                                            │
│                 │                                                   │
│                 ├─ 複数購読者？ → Event-Driven (Pub/Sub)            │
│                 │                                                   │
│                 └─ 1対1処理？ → Message Queue                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 パターン一覧

| パターン | 用途 | 採用技術 |
|----------|------|----------|
| REST API | 外部公開、CRUD操作 | OpenAPI 3.0 |
| gRPC | 内部高速通信 | Protocol Buffers |
| Event-Driven | ドメインイベント伝播 | Apache Kafka |
| Message Queue | 非同期ジョブ処理 | Amazon SQS |
| GraphQL | BFF（Backend for Frontend） | Apollo |

---

## 2. 同期通信パターン

### 2.1 REST API

```yaml
REST API標準:

仕様:
  format: OpenAPI 3.0
  認証: Bearer Token (JWT)
  バージョニング: URL Path (/api/v1/*)

設計原則:
  - リソース指向
  - HTTPメソッドの適切な使用
  - HAL形式のハイパーメディア
  - 一貫したエラーレスポンス

HTTPメソッド:
  GET: リソース取得（冪等）
  POST: リソース作成
  PUT: リソース全体更新
  PATCH: リソース部分更新
  DELETE: リソース削除

ステータスコード:
  200: OK
  201: Created
  204: No Content
  400: Bad Request
  401: Unauthorized
  403: Forbidden
  404: Not Found
  409: Conflict
  422: Unprocessable Entity
  500: Internal Server Error
  503: Service Unavailable

エラーレスポンス形式:
  {
    "error": {
      "code": "VALIDATION_ERROR",
      "message": "入力値が不正です",
      "details": [
        {
          "field": "email",
          "message": "有効なメールアドレスを入力してください"
        }
      ],
      "traceId": "abc123"
    }
  }

ページネーション:
  クエリパラメータ:
    - page: ページ番号（1始まり）
    - size: ページサイズ（デフォルト20、最大100）
  レスポンス:
    {
      "data": [...],
      "pagination": {
        "page": 1,
        "size": 20,
        "totalPages": 10,
        "totalItems": 195
      }
    }

レート制限:
  ヘッダー:
    - X-RateLimit-Limit: 1000
    - X-RateLimit-Remaining: 999
    - X-RateLimit-Reset: 1640000000
  制限超過: 429 Too Many Requests
```

### 2.2 gRPC

```yaml
gRPC標準:

仕様:
  format: Protocol Buffers 3
  認証: mTLS + JWT metadata
  ロードバランシング: クライアントサイド

使用ケース:
  - サービス間の高速通信
  - 大量データ転送
  - ストリーミング
  - 低レイテンシ要件

適用サービス間:
  - Customer Platform → Marketing (顧客セグメント取得)
  - R&D Platform → Manufacturing (レシピデータ取得)
  - Supply Chain → Manufacturing (在庫照会)

プロトコル定義例:
  syntax = "proto3";
  package suntory.crm.v1;

  service CustomerService {
    rpc GetCustomerProfile(GetCustomerProfileRequest)
        returns (CustomerProfile);
    rpc ListCustomersBySegment(ListCustomersBySegmentRequest)
        returns (stream CustomerProfile);
  }

  message GetCustomerProfileRequest {
    string customer_id = 1;
  }

  message CustomerProfile {
    string id = 1;
    string name = 2;
    repeated string segments = 3;
    google.protobuf.Timestamp created_at = 4;
  }

エラーハンドリング:
  - gRPC Status Codes使用
  - 詳細エラーはmetadataで伝達
  - リトライはExponential Backoff
```

### 2.3 GraphQL（BFF用）

```yaml
GraphQL標準:

仕様:
  バージョン: GraphQL 2021
  認証: Bearer Token (JWT)
  実装: Apollo Server

使用ケース:
  - モバイルアプリ向けBFF
  - ダッシュボード向けBFF
  - 複数サービスのアグリゲーション

適用:
  - 消費者向けアプリ（会員サービス）
  - 営業ダッシュボード
  - 経営ダッシュボード

スキーマ設計原則:
  - フェデレーション対応
  - N+1問題をDataLoaderで解決
  - 深さ制限（max 7階層）
  - 複雑度制限

スキーマ例:
  type Query {
    customer(id: ID!): Customer
    products(category: String, first: Int): ProductConnection
    campaigns(status: CampaignStatus): [Campaign]
  }

  type Customer {
    id: ID!
    name: String!
    segments: [Segment!]!
    purchaseHistory(first: Int): [Purchase!]!
  }

  type Mutation {
    enrollCampaign(customerId: ID!, campaignId: ID!): Enrollment
  }
```

---

## 3. 非同期通信パターン

### 3.1 Event-Driven（Pub/Sub）

```yaml
Event-Driven標準:

技術選定: Apache Kafka

理由:
  - 高スループット
  - 永続化・リプレイ可能
  - パーティショニングによるスケーラビリティ
  - 成熟したエコシステム

イベント形式: CloudEvents 1.0

イベントスキーマ:
  {
    "specversion": "1.0",
    "type": "suntory.manufacturing.v1.ProductionCompleted",
    "source": "/services/manufacturing/beverage",
    "id": "uuid-here",
    "time": "2025-12-05T10:00:00Z",
    "datacontenttype": "application/json",
    "data": {
      "productionOrderId": "PO-2025-001",
      "productId": "PRD-BEV-001",
      "quantity": 10000,
      "completedAt": "2025-12-05T10:00:00Z"
    }
  }

トピック命名規則:
  形式: {domain}.{aggregate}.{event-type}
  例:
    - manufacturing.production.completed
    - customer.profile.updated
    - supply-chain.shipment.dispatched

パーティショニング戦略:
  - 製造: productId
  - 顧客: customerId
  - 注文: orderId
  - デフォルト: ランダム

保持期間:
  - 通常イベント: 7日
  - 監査イベント: 1年
  - コンパクション対象: 永続

コンシューマーグループ:
  命名: {service-name}-{purpose}
  例: marketing-beverage-campaign-sync

デッドレターキュー:
  形式: {original-topic}.dlq
  監視: アラート設定必須
```

### 3.2 主要イベントフロー

```
┌─────────────────────────────────────────────────────────────────────┐
│                    製造完了イベントフロー                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Manufacturing Service                                              │
│       │                                                             │
│       │ ProductionCompleted                                         │
│       ▼                                                             │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Kafka                                     │   │
│  │           Topic: manufacturing.production.completed           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│       │                    │                    │                   │
│       ▼                    ▼                    ▼                   │
│  ┌──────────┐       ┌──────────┐       ┌──────────┐               │
│  │  Supply  │       │ Finance  │       │  Sust.   │               │
│  │  Chain   │       │ Service  │       │ Service  │               │
│  └──────────┘       └──────────┘       └──────────┘               │
│  在庫更新           原価計上           環境データ                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    顧客プロファイル更新フロー                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Customer Platform Service                                          │
│       │                                                             │
│       │ CustomerProfileUpdated                                      │
│       ▼                                                             │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Kafka                                     │   │
│  │           Topic: customer.profile.updated                     │   │
│  └─────────────────────────────────────────────────────────────┘   │
│       │                    │                    │                   │
│       ▼                    ▼                    ▼                   │
│  ┌──────────┐       ┌──────────┐       ┌──────────┐               │
│  │ Mkt-Bev  │       │ Mkt-Spi  │       │ Mkt-...  │               │
│  └──────────┘       └──────────┘       └──────────┘               │
│  セグメント         セグメント         セグメント                   │
│  再計算             再計算             再計算                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.3 Message Queue（Point-to-Point）

```yaml
Message Queue標準:

技術選定: Amazon SQS（または RabbitMQ）

使用ケース:
  - 非同期ジョブ処理
  - 長時間処理タスク
  - リトライが必要な処理

適用例:
  - レポート生成
  - バッチ処理
  - 外部システム連携
  - メール送信

キュー命名規則:
  形式: {service}-{purpose}-queue
  例:
    - sustainability-report-generation-queue
    - marketing-email-dispatch-queue
    - finance-batch-processing-queue

メッセージ形式:
  {
    "messageId": "uuid-here",
    "type": "ReportGenerationRequest",
    "timestamp": "2025-12-05T10:00:00Z",
    "payload": {
      "reportType": "ESG_QUARTERLY",
      "period": "2025-Q4",
      "requestedBy": "user-123"
    },
    "metadata": {
      "correlationId": "request-uuid",
      "priority": "normal"
    }
  }

リトライ戦略:
  maxRetries: 3
  backoff: exponential
  initialDelay: 1s
  maxDelay: 60s
  deadLetterQueue: true

可視性タイムアウト:
  デフォルト: 30秒
  長時間処理: 最大12時間
```

---

## 4. データ統合パターン

### 4.1 CQRS（Command Query Responsibility Segregation）

```yaml
CQRS適用サービス:

Customer Platform Service:
  目的: 読み取り性能最適化

  コマンド側:
    データストア: PostgreSQL
    操作: 顧客登録、プロファイル更新、同意管理
    整合性: 強い整合性

  クエリ側:
    データストア: Elasticsearch
    操作: 顧客検索、セグメント抽出
    整合性: 結果整合性（〜1秒遅延許容）

  同期:
    方式: イベント駆動
    イベント: CustomerProfileUpdated
    処理: Kafkaコンシューマーでインデックス更新

R&D Platform Service:
  目的: 研究ドキュメント検索最適化

  コマンド側:
    データストア: PostgreSQL + MongoDB
    操作: 研究データ登録、レシピ更新

  クエリ側:
    データストア: Elasticsearch
    操作: 研究論文検索、レシピ検索

  同期:
    方式: 変更データキャプチャ（CDC）
    ツール: Debezium
```

### 4.2 Saga Pattern

```yaml
Saga適用フロー:

新製品リリースSaga:

  ステップ:
    1. Brand Management: 製品マスタ登録
       補償: 製品マスタ削除

    2. R&D Platform: 製造仕様登録
       補償: 製造仕様削除

    3. Manufacturing: 製造準備確認
       補償: 製造準備キャンセル

    4. Supply Chain: 原材料調達開始
       補償: 調達キャンセル

    5. Marketing: キャンペーン準備
       補償: キャンペーンキャンセル

  実装: Choreography（イベント駆動）

  イベントフロー:
    ProductMasterCreated
    → ManufacturingSpecRegistered
    → ProductionReadinessConfirmed
    → ProcurementInitiated
    → CampaignPrepared
    → ProductLaunchCompleted

  失敗時:
    各ステップで失敗イベント発行
    → 前ステップの補償アクション実行

注文処理Saga（将来拡張用）:

  ステップ:
    1. 在庫引当
    2. 支払い処理
    3. 出荷指示
    4. 通知送信

  実装: Orchestration（専用Sagaサービス）
```

---

## 5. レジリエンスパターン

### 5.1 Circuit Breaker

```yaml
Circuit Breaker設定:

ライブラリ: Resilience4j（Java）、go-resiliency（Go）

デフォルト設定:
  failureRateThreshold: 50%
  slowCallRateThreshold: 100%
  slowCallDurationThreshold: 2s
  permittedNumberOfCallsInHalfOpenState: 3
  slidingWindowSize: 10
  waitDurationInOpenState: 30s

サービス別カスタマイズ:
  IT Platform（認証）:
    failureRateThreshold: 30%
    waitDurationInOpenState: 10s
    理由: 認証は最重要、早めにオープン

  外部API連携:
    failureRateThreshold: 70%
    waitDurationInOpenState: 60s
    理由: 外部は不安定なことが多い

フォールバック戦略:
  認証: キャッシュからのトークン検証
  顧客データ: キャッシュからの返却
  レポート: 非同期処理への切り替え
```

### 5.2 Retry with Exponential Backoff

```yaml
Retry設定:

デフォルト:
  maxRetries: 3
  initialInterval: 100ms
  multiplier: 2
  maxInterval: 10s
  retryableExceptions:
    - ConnectionException
    - TimeoutException
    - ServiceUnavailableException

リトライ対象外:
  - 400系エラー（クライアントエラー）
  - 認証エラー
  - ビジネスロジックエラー

Jitter追加:
  enabled: true
  factor: 0.1
  理由: 雷群問題の回避
```

### 5.3 Timeout設定

```yaml
Timeout設定:

同期呼び出し:
  REST API:
    connect: 3s
    read: 30s
    write: 30s

  gRPC:
    connect: 1s
    deadline: 10s

サービス別カスタマイズ:
  認証API: 5s（厳格）
  検索API: 10s
  レポート生成API: 300s（長時間許容）

非同期処理:
  メッセージ処理: 5分
  バッチジョブ: ジョブ別に設定
```

### 5.4 Bulkhead（隔壁）

```yaml
Bulkhead設定:

スレッドプール分離:
  認証処理:
    maxConcurrent: 50
    maxWait: 1s

  データベース処理:
    maxConcurrent: 100
    maxWait: 5s

  外部API連携:
    maxConcurrent: 20
    maxWait: 10s

目的:
  - 1つの障害が全体に波及しない
  - リソース枯渇の防止
  - 優先度に基づくリソース配分
```

---

## 6. 監視・可観測性

### 6.1 分散トレーシング

```yaml
分散トレーシング:

技術選定: OpenTelemetry + Jaeger

トレースID伝播:
  ヘッダー: traceparent (W3C Trace Context)
  形式: 00-{trace-id}-{span-id}-{flags}

サンプリング:
  本番: 1%（エラー時は100%）
  ステージング: 10%
  開発: 100%

スパン属性:
  必須:
    - service.name
    - service.version
    - http.method
    - http.url
    - http.status_code
  推奨:
    - user.id
    - tenant.id
    - business.operation
```

### 6.2 ログ集約

```yaml
ログ集約:

技術選定: ELK Stack（Elasticsearch, Logstash, Kibana）

ログ形式: JSON（構造化ログ）

必須フィールド:
  - timestamp
  - level
  - message
  - service
  - traceId
  - spanId

ログレベル:
  ERROR: 障害、要対応
  WARN: 警告、監視対象
  INFO: 重要なビジネスイベント
  DEBUG: 詳細デバッグ情報

保持期間:
  ERROR/WARN: 90日
  INFO: 30日
  DEBUG: 7日
```

### 6.3 メトリクス

```yaml
メトリクス:

技術選定: Prometheus + Grafana

RED Metrics:
  Rate: リクエストレート（req/s）
  Errors: エラーレート（%）
  Duration: レイテンシ分布（p50, p90, p99）

USE Metrics:
  Utilization: CPU、メモリ、ディスク使用率
  Saturation: キュー長、待機スレッド
  Errors: システムエラー

ビジネスメトリクス:
  - 注文数/時間
  - 顧客登録数/日
  - API呼び出し数/サービス

アラート閾値:
  エラーレート: > 1%
  レイテンシP99: > 3s
  CPU使用率: > 80%
```

---

## 7. セキュリティパターン

### 7.1 認証・認可

```yaml
認証:
  方式: OAuth 2.0 + OIDC
  IdP: IT Platform Service（内製）または Auth0
  トークン: JWT
  有効期限:
    アクセストークン: 1時間
    リフレッシュトークン: 7日

認可:
  方式: RBAC + ABAC
  権限チェック: 各サービスで実施
  ポリシー管理: 集中管理（IT Platform）

サービス間認証:
  方式: mTLS
  証明書管理: HashiCorp Vault
  ローテーション: 90日
```

### 7.2 API Gateway

```yaml
API Gateway:

技術選定: Kong または AWS API Gateway

機能:
  - 認証・認可
  - レート制限
  - リクエスト/レスポンス変換
  - ログ・メトリクス収集
  - CORS処理

配置:
  - 外部向け: パブリックAPI Gateway
  - 内部向け: サービスメッシュ（Istio）またはダイレクト
```

---

**統合パターン定義完了**: 2025-12-05
**次ステップ**: ADR作成
