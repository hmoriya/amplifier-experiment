# 統合パターン

**プロジェクト:** asashi (Asahi Group Holdings)
**作成日:** 2025-11-27
**ステータス:** 初版
**対象スコープ:** VS2 製品開発・イノベーション

---

## エグゼクティブサマリー

VS2サービス間の通信方式と統合パターンを定義しました。

**主要方針:**
- **同期通信**: 即時性が必要なクエリ・コマンドに使用
- **非同期通信**: 疎結合・スケーラビリティが必要な処理に使用
- **イベント駆動**: サービス間のデータ同期・通知に使用

**採用パターン:**

| パターン | 用途 | 採用技術 |
|----------|------|----------|
| REST API | 外部公開・同期クエリ | FastAPI + OpenAPI |
| gRPC | サービス間高速通信 | gRPC + Protocol Buffers |
| Event-Driven | 疎結合統合・通知 | Apache Kafka |
| CQRS | 読み書き分離 | PostgreSQL + Elasticsearch |

---

## 同期通信パターン

### REST API

#### 使用ケース

- 外部クライアント（Web/Mobile）からのアクセス
- 管理画面からの操作
- シンプルなCRUD操作
- 同期的なデータ取得

#### 標準仕様

```yaml
プロトコル: HTTP/1.1, HTTP/2
データ形式: JSON (application/json)
API仕様: OpenAPI 3.1
認証: JWT Bearer Token (OAuth 2.0)
レート制限: あり (サービスごとに設定)

URL設計:
  ベースURL: /api/v{version}/{service-name}
  リソース: 複数形名詞
  アクション: HTTPメソッドで表現

  例:
    GET    /api/v1/fermentation-research/yeast-strains
    GET    /api/v1/fermentation-research/yeast-strains/{id}
    POST   /api/v1/fermentation-research/yeast-strains
    PUT    /api/v1/fermentation-research/yeast-strains/{id}
    DELETE /api/v1/fermentation-research/yeast-strains/{id}

ステータスコード:
  200: 成功（GET, PUT）
  201: 作成成功（POST）
  204: 削除成功（DELETE）
  400: バリデーションエラー
  401: 認証エラー
  403: 認可エラー
  404: リソース未発見
  409: 競合（楽観ロック失敗等）
  500: サーバーエラー

エラーレスポンス:
  format:
    error:
      code: "VALIDATION_ERROR"
      message: "入力値が不正です"
      details:
        - field: "name"
          message: "必須項目です"
```

#### 適用サービス

| サービス | エンドポイント数 | 主要用途 |
|----------|----------------|----------|
| Fermentation Research | 15 | 酵母・レシピ管理 |
| Ingredient Research | 18 | 素材・配合管理 |
| Beer Development | 20 | 製品・プロジェクト管理 |
| Spirits Development | 12 | スピリッツ製品管理 |
| Beverage Development | 15 | 飲料製品管理 |
| R&D Support | 12 | 評価・試作依頼 |
| Process Engineering | 10 | プロセス設計・移管 |

---

### gRPC

#### 使用ケース

- サービス間の高速通信
- 大量データの転送
- ストリーミング処理
- 低レイテンシが必要な処理

#### 標準仕様

```yaml
プロトコル: HTTP/2
データ形式: Protocol Buffers 3
認証: mTLS (サービス間) または JWT
タイムアウト: 30秒（デフォルト）

定義ファイル管理:
  リポジトリ: asashi-proto
  バージョン管理: Git tags

サービス定義例:
  // fermentation_research.proto
  syntax = "proto3";
  package asashi.fermentation;

  service FermentationResearchService {
    rpc GetYeastStrain(GetYeastStrainRequest) returns (YeastStrain);
    rpc ListYeastStrains(ListYeastStrainsRequest) returns (stream YeastStrain);
    rpc GetFermentationRecipe(GetRecipeRequest) returns (FermentationRecipe);
  }
```

#### 適用箇所

```yaml
高速データ取得:
  Beer Development → Fermentation Research:
    - GetYeastStrain: 酵母詳細取得（単一）
    - ListYeastStrains: 酵母一覧取得（ストリーミング）

  Beer Development → Ingredient Research:
    - GetIngredient: 素材詳細取得
    - GetFormulation: 配合詳細取得

バッチ処理:
  R&D Support → Beer Development:
    - StreamEvaluationResults: 評価結果一括送信
```

---

## 非同期通信パターン

### Event-Driven (Pub/Sub)

#### 使用ケース

- ドメインイベントの伝播
- 疎結合なサービス間統合
- 最終的整合性の実現
- 監査ログ・履歴記録

#### 標準仕様

```yaml
メッセージブローカー: Apache Kafka
クラスタ構成: 3ブローカー (本番環境)
レプリケーション: 3
パーティション: イベントタイプごとに設定

イベント形式: CloudEvents 1.0
スキーマ管理: Confluent Schema Registry (Avro)

イベント構造:
  {
    "specversion": "1.0",
    "type": "asashi.fermentation.YeastStrainRegistered",
    "source": "/fermentation-research-service",
    "id": "uuid",
    "time": "2025-11-27T10:00:00Z",
    "datacontenttype": "application/json",
    "data": {
      "strainId": "YS-2025-001",
      "name": "Asahi Premium Yeast #42",
      "characteristics": {...}
    }
  }

トピック命名規則:
  形式: {domain}.{aggregate}.{event-type}
  例:
    - fermentation.yeast-strain.registered
    - fermentation.yeast-strain.improved
    - beer-development.product.concept-approved
    - rnd-support.sensory-evaluation.completed
```

#### 主要イベント一覧

```yaml
Fermentation Research Service:
  Published:
    - YeastStrainRegistered        # 酵母株登録
    - YeastStrainImproved          # 酵母株改良
    - FermentationRecipeCreated    # レシピ作成
    - ResearchKnowledgeDocumented  # 技術知見文書化
  Subscribed:
    - (外部イベントなし)

Ingredient Research Service:
  Published:
    - IngredientRegistered         # 素材登録
    - FormulationRecipeCreated     # 配合レシピ作成
    - FunctionalEvidenceValidated  # 機能性エビデンス検証完了
    - SupplierAssessmentCompleted  # サプライヤー評価完了
  Subscribed:
    - (外部イベントなし)

Beer Development Service:
  Published:
    - ProductConceptApproved           # コンセプト承認
    - PrototypeCreated                 # 試作品作成
    - ProductSpecificationFinalized    # 製品規格確定
    - ProductTransferredToManufacturing # 製造移管完了
  Subscribed:
    - YeastStrainRegistered
    - YeastStrainImproved
    - FermentationRecipeCreated
    - IngredientRegistered
    - SensoryEvaluationCompleted
    - PrototypeBatchCompleted
    - TechnologyTransferValidated

Spirits Development Service:
  Published:
    - SpiritsProductCreated
    - MaturationBatchStarted
    - MaturationComplete
    - ProductBlendFinalized
  Subscribed:
    - YeastStrainImproved
    - SensoryEvaluationCompleted

Beverage Development Service:
  Published:
    - BeverageProductCreated
    - FunctionalClaimSubmitted
    - RegulatoryApprovalReceived
  Subscribed:
    - IngredientRegistered
    - FunctionalEvidenceValidated
    - SensoryEvaluationCompleted

R&D Support Service:
  Published:
    - SensoryEvaluationCompleted
    - SensoryReportGenerated
    - PrototypeRequestReceived
    - PrototypeBatchCompleted
  Subscribed:
    - ProductConceptApproved (評価準備のため)

Process Engineering Service:
  Published:
    - ProcessDesignCompleted
    - TechnologyTransferInitiated
    - TechnologyTransferValidated
  Subscribed:
    - ProductSpecificationFinalized
    - PrototypeBatchCompleted
```

---

### Message Queue (Point-to-Point)

#### 使用ケース

- 非同期ジョブ処理
- リトライが必要な処理
- 順序保証が必要な処理
- バックプレッシャー制御

#### 標準仕様

```yaml
メッセージブローカー: RabbitMQ
キュー命名規則: {service}.{operation}.queue
エクスチェンジ: Direct Exchange

リトライ設定:
  最大リトライ: 3回
  バックオフ: Exponential (1s, 2s, 4s)
  デッドレター: {queue}.dlq

適用例:
  rnd-support.sensory-evaluation.queue:
    - 官能評価依頼の処理
    - 順序保証: なし
    - リトライ: あり

  process-engineering.technology-transfer.queue:
    - 技術移管タスクの処理
    - 順序保証: あり（同一製品内）
    - リトライ: あり
```

---

## データ統合パターン

### CQRS (Command Query Responsibility Segregation)

#### 使用ケース

- 読み取りと書き込みの分離が必要な場合
- 複雑な検索要件
- 読み取りスケールが書き込みより高い場合

#### 適用サービス

```yaml
Beer Development Service:
  Command Side:
    Database: PostgreSQL
    用途: 製品登録・更新・削除
    整合性: 強整合性

  Query Side:
    Database: Elasticsearch
    用途: 製品検索・フィルタリング
    整合性: 最終的整合性

  同期方法:
    - ProductCreated → Elasticsearch Index更新
    - ProductUpdated → Elasticsearch Index更新
    - ProductDeleted → Elasticsearch Index削除

Ingredient Research Service:
  Command Side:
    Database: PostgreSQL
    用途: 素材・配合管理

  Query Side:
    Database: Elasticsearch
    用途: 素材検索・フィルタリング
```

### Saga Pattern

#### 使用ケース

- 複数サービスにまたがるトランザクション
- 補償トランザクションによるロールバック

#### 適用例: 製品開発完了フロー

```yaml
Saga名: ProductDevelopmentCompletionSaga
実装方式: Choreography (イベント駆動)

フロー:
  1. Beer Development: ProductSpecificationFinalized発行
     ↓
  2. R&D Support: 最終評価完了確認
     ↓ SensoryEvaluationCompleted
  3. Process Engineering: 技術移管開始
     ↓ TechnologyTransferInitiated
  4. Process Engineering: 技術移管検証
     ↓ TechnologyTransferValidated
  5. Beer Development: 製造移管完了
     → ProductTransferredToManufacturing発行

補償アクション:
  - 技術移管失敗時: TransferRollbackRequested発行
  - 評価不合格時: SpecificationRevisionRequired発行
```

---

## レジリエンスパターン

### Circuit Breaker

```yaml
適用:
  全サービス間同期呼び出し

設定:
  ライブラリ: Resilience4j (Python: pybreaker)

  パラメータ:
    failureRateThreshold: 50%      # 失敗率閾値
    waitDurationInOpenState: 30s   # オープン状態維持時間
    permittedNumberOfCallsInHalfOpenState: 5
    slidingWindowSize: 10

状態遷移:
  CLOSED → OPEN: 失敗率50%超過
  OPEN → HALF_OPEN: 30秒後
  HALF_OPEN → CLOSED: 5回連続成功
  HALF_OPEN → OPEN: 1回でも失敗
```

### Retry with Exponential Backoff

```yaml
適用:
  一時的な障害が予想される呼び出し

設定:
  maxAttempts: 3
  initialDelay: 100ms
  maxDelay: 2s
  multiplier: 2.0
  retryableExceptions:
    - ConnectionTimeout
    - ServiceUnavailable
```

### Timeout

```yaml
適用:
  全ての同期呼び出し

設定:
  REST API: 30秒
  gRPC: 30秒
  Database: 10秒
  Cache: 1秒
```

### Bulkhead

```yaml
適用:
  リソース分離が必要なサービス

設定:
  方式: Thread Pool Bulkhead

  Beer Development Service:
    fermentation-research-calls:
      maxConcurrentCalls: 20
      maxWaitDuration: 5s
    ingredient-research-calls:
      maxConcurrentCalls: 20
      maxWaitDuration: 5s
```

---

## API Gateway

### 構成

```yaml
技術選定: Kong Gateway (OSS)

機能:
  - ルーティング
  - 認証・認可
  - レート制限
  - ロギング
  - メトリクス収集

ルーティング設定:
  /api/v1/fermentation-research/*:
    upstream: fermentation-research-service:8000
    plugins: [jwt-auth, rate-limiting, logging]

  /api/v1/ingredient-research/*:
    upstream: ingredient-research-service:8000
    plugins: [jwt-auth, rate-limiting, logging]

  /api/v1/beer-development/*:
    upstream: beer-development-service:8000
    plugins: [jwt-auth, rate-limiting, logging]

  # ... 他サービス

レート制限:
  デフォルト: 100 req/min per user
  管理API: 1000 req/min per service
```

---

## セキュリティ

### 認証・認可

```yaml
外部アクセス:
  方式: OAuth 2.0 + JWT
  IdP: Keycloak or Azure AD
  トークン有効期限: 1時間
  リフレッシュトークン: 7日

サービス間通信:
  方式: mTLS + Service Account JWT
  証明書管理: cert-manager (Kubernetes)
  ローテーション: 90日

認可:
  方式: RBAC (Role-Based Access Control)
  ロール例:
    - researcher: 研究データの読み書き
    - developer: 開発データの読み書き
    - viewer: 読み取りのみ
    - admin: 全権限
```

### データ保護

```yaml
転送中:
  - TLS 1.3 必須
  - 内部通信もmTLS

保存時:
  - データベース暗号化 (AES-256)
  - 機密データはフィールドレベル暗号化
```

---

## 監視・運用

### ログ

```yaml
フォーマット: JSON構造化ログ
集約: ELK Stack (Elasticsearch + Logstash + Kibana)

必須フィールド:
  - timestamp
  - service
  - level
  - message
  - trace_id
  - span_id
  - user_id (該当する場合)

ログレベル:
  DEBUG: 開発時のみ
  INFO: 通常オペレーション
  WARN: 注意が必要な状況
  ERROR: エラー発生
```

### メトリクス

```yaml
収集: Prometheus
可視化: Grafana

主要メトリクス:
  - request_total (リクエスト数)
  - request_duration_seconds (レイテンシ)
  - error_rate (エラー率)
  - active_connections (接続数)
  - circuit_breaker_state (サーキットブレーカー状態)
```

### 分散トレーシング

```yaml
技術: OpenTelemetry + Jaeger
サンプリング: 10% (本番), 100% (開発)

トレースヘッダー:
  - traceparent (W3C Trace Context)
  - tracestate
```

---

## 実装ガイドライン

### サービス間呼び出しの選択基準

```
┌─────────────────────────────────────────────┐
│              呼び出しの性質は？              │
└─────────────────────────┬───────────────────┘
                          │
          ┌───────────────┴───────────────┐
          │                               │
    即時応答が必要？                 通知・伝播？
          │                               │
    ┌─────┴─────┐                   ┌─────┴─────┐
    │           │                   │           │
  Yes          No                 Yes          No
    │           │                   │           │
┌───┴───┐ ┌────┴────┐         ┌────┴────┐ ┌────┴────┐
│       │ │         │         │         │ │         │
│高速？ │ │順序保証？│         │Event    │ │Queue    │
│       │ │         │         │(Kafka)  │ │(RabbitMQ)│
└───┬───┘ └────┬────┘         └─────────┘ └─────────┘
    │          │
┌───┴───┐ ┌────┴────┐
│       │ │         │
│gRPC   │ │Queue    │
│       │ │         │
└───────┘ └─────────┘
    │
┌───┴───┐
│REST   │
│       │
└───────┘
```

---

**作成者:** Claude (Parasol V5)
**最終更新:** 2025-11-27
