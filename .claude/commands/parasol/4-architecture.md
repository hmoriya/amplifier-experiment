---
description: Application architecture design (project:parasol)
---

# Phase 4: Architecture - アーキテクチャ設計

Phase 3で定義したBounded Contextsを統合し、システム全体のアーキテクチャを設計します。

## 目的

- サービス境界の最終決定
- Context Map（BC間の関係）の作成
- 統合パターンの定義
- アーキテクチャ決定の文書化（ADR）



## 🔧 プロジェクト検出

**重要**: このコマンドはParasolプロジェクト内で実行する必要があります。

### 自動検出

コマンド実行時、以下の順序で `parasol.yaml` を自動探索：

1. **カレントディレクトリ** (`.`)
2. **親ディレクトリ** (`..`)
3. **祖父ディレクトリ** (`../..`)

### 検出成功

```
✅ プロジェクト検出: {project-name}

プロジェクトディレクトリ: projects/{project-name}/
出力先: projects/{project-name}/outputs/
```

プロジェクト設定を読み込み、Phase進捗を自動記録します。

### 検出失敗

```
❌ Parasolプロジェクトが見つかりません

📋 次のアクションを選択してください:

1. 新しいプロジェクトを作成
   → /parasol:project init {project-name}

2. 既存プロジェクトに移動
   → cd projects/{project-name}

3. プロジェクト一覧を確認
   → /parasol:project list
```

**ベストプラクティス**: プロジェクトディレクトリ内で作業
```bash
# 推奨
cd projects/my-project
/parasol:1-context

# 非推奨（プロジェクトが検出されない）
cd ~/somewhere-else
/parasol:1-context  # ❌
```

詳細は `.claude/commands/parasol/_project-detection.md` を参照。

## 成果物

以下のドキュメントを `outputs/4-architecture/` に作成します：

1. **service-boundaries.md** - サービス境界定義
2. **context-map.md** - Context Map（BC間の関係とパターン）
3. **integration-patterns.md** - 統合パターンと通信方式
4. **decisions/** - Architecture Decision Records (ADRs)

## 実行手順

### ステップ1: サービス境界の決定

Phase 3のCL2（サブドメイン）を基に、最終的なマイクロサービス境界を決定します。

**成果物**: `outputs/4-architecture/service-boundaries.md`

```yaml
サービス一覧:

ProductCatalogService:
含まれるBC:
- Product Catalog BC (Core)
責務:
- 製品情報管理
- カテゴリ管理
- 製品検索
公開API:
- REST API: /api/products/*
- gRPC: ProductCatalogService
データストア:
- PostgreSQL (製品マスタ)
- Elasticsearch (検索インデックス)
スケーリング要件: 高

OrderService:
含まれるBC:
- Order Management BC (Core)
- Payment Processing BC (Supporting)
責務:
- 注文処理
- 支払い処理
- 注文履歴管理
公開API:
- REST API: /api/orders/*
- Events: OrderCreated, OrderCompleted
データストア:
- PostgreSQL (注文データ)
スケーリング要件: 高

PricingService:
含まれるBC:
- Pricing BC (Core)
責務:
- 価格計算
- プロモーション管理
公開API:
- REST API: /api/pricing/*
- gRPC: PricingService (高速計算用)
データストア:
- PostgreSQL (価格ルール)
- Redis (キャッシュ)
スケーリング要件: 中

InventoryService:
含まれるBC:
- Inventory Management BC (Supporting)
責務:
- 在庫追跡
- 在庫引当
公開API:
- REST API: /api/inventory/*
- Events: InventoryUpdated
データストア:
- PostgreSQL (在庫データ)
スケーリング要件: 中

CustomerService:
含まれるBC:
- Customer Support BC (Supporting)
責務:
- サポートチケット管理
- 顧客対応履歴
公開API:
- REST API: /api/support/*
データストア:
- PostgreSQL
スケーリング要件: 低

PlatformServices:
含まれるBC:
- Authentication BC (Generic)
- Notification BC (Generic)
責務:
- 認証・認可
- 通知配信
推奨: Auth0, AWS SES等の既製品利用
公開API:
- REST API: /api/auth/*, /api/notifications/*
スケーリング要件: 中

サービス統合方針:
- 1つのBCが複雑すぎない場合は統合可能
- チーム境界を尊重
- デプロイ独立性を維持
- データ所有権は明確に分離
```

### ステップ2: Context Mapの作成

BC間の関係性とパターンを定義します。

**成果物**: `outputs/4-architecture/context-map.md`

```yaml
Context Map:

ProductCatalog BC → Pricing BC:
パターン: Customer-Supplier
関係性: ProductCatalogがUpstream、PricingがDownstream
契約: Product情報API + ProductUpdatedイベント
理由: 価格設定には製品情報が必要

ProductCatalog BC → Order BC:
パターン: Customer-Supplier
関係性: ProductCatalogがUpstream、OrderがDownstream
契約: Product情報API
理由: 注文処理には製品情報が必要

ProductCatalog BC → Inventory BC:
パターン: Customer-Supplier
関係性: ProductCatalogがUpstream、InventoryがDownstream
契約: SKU情報API
理由: 在庫管理にはSKU情報が必要

Pricing BC → Order BC:
パターン: Customer-Supplier
関係性: PricingがUpstream、OrderがDownstream
契約: 価格計算API
理由: 注文時の価格計算に必要

Order BC → Inventory BC:
パターン: Partnership
関係性: 双方向の協力関係
契約: 
- Order → Inventory: 在庫引当リクエスト
- Inventory → Order: 在庫状態通知
理由: 注文と在庫は密接に連携

Order BC → Payment BC:
パターンン: Customer-Supplier
関係性: OrderがUpstream、PaymentがDownstream
契約: 支払い処理API + PaymentCompletedイベント
理由: 注文完了には支払い処理が必要

Authentication BC → All Services:
パターン: Published Language
関係性: 認証BCが標準を提供、全サービスがConformist
契約: JWT Token標準
理由: 全サービスで統一された認証方式

Notification BC → All Services:
パターン: Open Host Service
関係性: 通知BCが汎用サービスを提供
契約: 通知送信API（Email, SMS, Push）
理由: 全サービスから通知を送信可能

Context Mapの視覚化:
[図を別途作成: Mermaid, PlantUML, または手書き]

統合の考慮事項:
- 循環依存の回避
- イベント駆動による疎結合
- 同期呼び出しは最小限に
- 各BCのデータ自律性を維持
```

### ステップ3: 統合パターンの定義

サービス間通信の具体的なパターンを定義します。

**成果物**: `outputs/4-architecture/integration-patterns.md`

```yaml
同期通信パターン:

REST API:
使用ケース: 
- 外部からのアクセス（Web, Mobile）
- 管理画面
- シンプルなCRUD操作
標準:
- HTTP/REST
- JSON
- OpenAPI 3.0仕様書
認証: JWT Bearer Token
レート制限: あり

gRPC:
使用ケース:
- サービス間の高速通信
- 大量データの転送
- ストリーミング
標準:
- Protocol Buffers
- HTTP/2
認証: mTLS or JWT
使用例: Pricing計算、Product情報取得

非同期通信パターン:

Event-Driven (Pub/Sub):
使用ケース:
- ドメインイベントの伝播
- 疎結合な統合
- 最終的整合性の実現
技術:
- Kafka or RabbitMQ or AWS SNS/SQS
イベント標準:
- CloudEvents形式
- Avro or JSON Schema
主要イベント:
- ProductCreated, ProductUpdated
- OrderCreated, OrderCompleted
- InventoryUpdated
- PaymentCompleted

Message Queue (Point-to-Point):
使用ケース:
- 非同期ジョブ処理
- リトライが必要な処理
技術: 
- RabbitMQ or AWS SQS

データ統合パターン:

CQRS (Command Query Responsibility Segregation):
使用ケース:
- 読み取りと書き込みの分離が必要な場合
- 複雑な検索要件
適用サービス:
- ProductCatalog: 書き込みはPostgreSQL、読み取りはElasticsearch

Event Sourcing:
使用ケース:
- 完全な監査ログが必要
- 時系列分析が必要
適用候補:
- Order Service（注文履歴の完全追跡）
※初期実装では見送り、必要に応じて追加

Saga Pattern:
使用ケース:
- 複数サービスにまたがるトランザクション
適用例:
- 注文処理: Order → Payment → Inventory → Notification
実装: Choreography（イベント駆動）推奨

レジリエンスパターン:

Circuit Breaker:
- 下流サービスの障害から保護
- ライブラリ: Resilience4j or Polly

Retry with Exponential Backoff:
- 一時的な障害への対応

Timeout:
- 全ての同期呼び出しにタイムアウト設定

Bulkhead:
- リソース分離によるカスケード障害防止
```

### ステップ4: ADR（Architecture Decision Records）の作成

重要なアーキテクチャ決定を文書化します。

**成果物**: `outputs/4-architecture/decisions/adr-*.md`

ADRテンプレート:

```markdown
# ADR-001: [決定のタイトル]

## ステータス
[提案中 | 承認済み | 却下 | 廃止 | 置換済み]

## コンテキスト
[決定が必要になった背景と問題]

## 決定
[採用する解決策]

## 結果
[この決定による影響]
- 良い影響
- 悪い影響/トレードオフ
- リスク

## 代替案
[検討した他の選択肢とその評価]

## 関連
[関連するADR、ドキュメント]
```

推奨ADRトピック例:
- ADR-001: マイクロサービスアーキテクチャの採用
- ADR-002: イベントバスとしてKafkaを選択
- ADR-003: API Gatewayパターンの採用
- ADR-004: データベース per Service パターン
- ADR-005: 認証方式（JWT）の選択
- ADR-006: CQRS適用範囲の決定
- ADR-007: サービスメッシュの見送り（初期フェーズ）

## 完了条件

以下の成果物が作成されたら完了：

- ✅ service-boundaries.md
- ✅ context-map.md
- ✅ integration-patterns.md
- ✅ decisions/adr-*.md（最低5つ）

## 完了メッセージ

```
✅ Phase 4: Architecture が完了しました

成果物:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ outputs/4-architecture/service-boundaries.md
✅ outputs/4-architecture/context-map.md
✅ outputs/4-architecture/integration-patterns.md
✅ outputs/4-architecture/decisions/
- ADR-001: マイクロサービスアーキテクチャ採用
- ADR-002: Kafka選択
- ADR-003: API Gateway採用
- ADR-004: Database per Service
- ADR-005: JWT認証
[5 ADRs作成済み]

アーキテクチャサマリー:
定義済みサービス: 6
- ProductCatalogService (Core)
- OrderService (Core)
- PricingService (Core)
- InventoryService (Supporting)
- CustomerService (Supporting)
- PlatformServices (Generic)

Context Map関係: 8
統合パターン: REST, gRPC, Event-Driven, CQRS

📊 ステータス確認:
→ `/parasol:status phase4`

🎯 次のステップ: Phase 5 Software Design
→ `/parasol:5-software`

Phase 5では各サービス/BCの詳細設計を行います：
- ドメインモデル（Parasol Domain Language）
- API仕様（OpenAPI）
- データベース設計
- ビジネスオペレーション（Use Cases + UI）
```

## エラーケース

**前提条件未満足:**
```
❌ Phase 3が完了していません

Phase 3でBounded Contextsを定義してください:
→ `/parasol:3-capabilities cl3`
```

**CL3未完了:**
```
❌ 全てのBounded Contextが定義されていません

未定義のBC:
- inventory-management
- customer-service

先にBC定義を完了してください:
→ `/parasol:3-capabilities cl3 inventory-management`
```

## バリデーション

作成後、以下を自動チェック：

1. **サービス完全性**: 全BCがいずれかのサービスに含まれているか
2. **Context Map整合性**: service-boundariesで定義したサービス間の関係がContext Mapに記載されているか
3. **循環依存**: Context Mapに循環依存がないか
4. **ADR完全性**: 主要な決定がADRとして文書化されているか

問題がある場合：

```
⚠️ バリデーション警告

サービス境界:
- Authentication BCがどのサービスにも含まれていません

Context Map:
- Order BC → Pricing BCの関係が未定義です
- 循環依存を検出: A → B → C → A

ADR:
- データベース選択に関するADRが不足しています

修正して再度確認しますか？
→ `/parasol:validate phase4`
```

## アーキテクチャレビューチェックリスト

Phase 4完了前に確認すべき項目：

### サービス設計
- [ ] 各サービスは単一責任を持つか
- [ ] サービスのサイズは適切か（小さすぎ/大きすぎないか）
- [ ] デプロイ独立性が保たれているか
- [ ] データ所有権が明確に分離されているか

### 統合設計
- [ ] 同期呼び出しは最小限か
- [ ] イベント駆動で疎結合になっているか
- [ ] 循環依存がないか
- [ ] 障害の伝播を防ぐ設計か

### 非機能要件
- [ ] スケーラビリティ要件を満たすか
- [ ] レジリエンスパターンが適用されているか
- [ ] セキュリティ要件が考慮されているか
- [ ] 監視・運用性が考慮されているか

### 文書化
- [ ] 全ての重要決定がADRに記録されているか
- [ ] Context Mapが最新か
- [ ] API契約が明確か

## 参考資料

- **フレームワーク設計**: `parasol-v4-lite/FRAMEWORK-DESIGN.md`
- **テンプレート**: `parasol-v4-lite/templates/phase4/`
- `service-boundary-template.md`
- `context-map-template.md`
- `adr-template.md`
- **Context Mapパターン**: `/parasol:0-help mapping`
