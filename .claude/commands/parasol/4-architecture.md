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

## 🎯 V5特有機能: アーキテクチャ設計ストーリー出力

**重要**: Parasol V5では、アーキテクチャ設計の各段階で**設計ストーリー（なぜそう設計したか）**を出力します。

### 設計ストーリーの目的

- **設計判断の可視化**: なぜこのサービス境界にしたか、なぜこの統合パターンを選んだかを明確に
- **チーム間の認識統一**: アーキテクチャ決定の背景をチーム全員が理解
- **将来の変更容易性**: 後から見直す際に「なぜこうなっているか」がわかる

### 出力タイミングと内容

| フェーズ | 出力内容 |
|----------|----------|
| **サービス境界決定** | なぜこのBCをこのサービスにまとめた/分離したか |
| **Context Map作成** | なぜこの統合パターン（Customer-Supplier等）を選んだか |
| **統合パターン決定** | なぜ同期/非同期、REST/gRPC/イベント等を選んだか |

### 設計ストーリーテンプレート

各成果物に以下の「設計ストーリー」セクションを含めます：

```markdown
## 設計ストーリー：なぜこのアーキテクチャなのか

### 1. サービス境界の設計理由

**このサービスにまとめた理由:**
[凝集度、チーム構造、デプロイ独立性などの観点から説明]

**分離した理由（複数BC→複数サービスの場合）:**
[スケーラビリティ、チーム境界、変更頻度の違いなど]

### 2. Context Map設計の理由

**統合パターン選択の理由:**
- Customer-Supplier: [なぜ上下関係にしたか]
- Partnership: [なぜ対等関係にしたか]
- Shared Kernel: [なぜ共有にしたか]
- Anti-Corruption Layer: [なぜ変換層が必要か]

### 3. 統合方式の理由

**同期/非同期の選択理由:**
[レイテンシ要件、整合性要件、障害分離の観点から]

**プロトコル選択の理由:**
- REST: [外部公開、シンプルさ]
- gRPC: [内部通信、パフォーマンス]
- Event-Driven: [疎結合、スケーラビリティ]
```

### ADRとの関係

設計ストーリーは**簡潔な理由説明**、ADRは**詳細な意思決定記録**として使い分けます：

| 用途 | 設計ストーリー | ADR |
|------|----------------|-----|
| **目的** | 理解促進 | 意思決定の公式記録 |
| **詳細度** | 簡潔（数行） | 詳細（代替案含む） |
| **配置** | 各成果物に埋め込み | decisions/ディレクトリに独立 |
| **更新** | 設計変更時に更新 | 新規ADRで置換 |



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

以下のディレクトリ構造で `outputs/4-architecture/` に成果物を作成します：

```
outputs/4-architecture/
├── architecture-overview.md              # Phase 4全体概要
│
├── {vs-name}/                            # Value Stream毎のディレクトリ
│   ├── overview.md                       # VS概要・サービス一覧
│   ├── context-map.md                    # VS内Context Map
│   └── services/                         # サービス毎のディレクトリ
│       └── {service-name}/
│           ├── service-definition.md     # サービス定義（API, イベント, データ等）
│           └── bounded-contexts/         # このサービスに含まれるBC
│               └── {bc-name}-bc.md → ../../../../../3-capabilities/.../  # シンボリックリンク
│
└── cross-vs/                             # VS横断共通設計
    ├── integration-patterns.md           # 統合パターン定義
    └── decisions/                        # Architecture Decision Records
        └── adr-*.md
```

### シンボリックリンクによるBC参照

各サービスディレクトリ内の `bounded-contexts/` には、Phase 3で定義したBCファイルへの
**シンボリックリンク**を配置します。

**メリット:**
- BC定義はPhase 3に単一ソースとして維持
- サービスディレクトリから含まれるBCが一目でわかる
- BC定義を更新すれば自動的に反映

### 成果物一覧

1. **architecture-overview.md** - Phase 4全体の概要とナビゲーション
2. **{vs-name}/overview.md** - VS毎のアーキテクチャ概要
3. **{vs-name}/context-map.md** - VS内サービス間関係（Context Map）
4. **{vs-name}/services/{service}/service-definition.md** - サービス定義
5. **cross-vs/integration-patterns.md** - VS横断の統合パターン
6. **cross-vs/decisions/adr-*.md** - Architecture Decision Records

## 実行手順

### ステップ1: ディレクトリ構造の作成

Phase 2で定義したValue Streamごとにディレクトリを作成します。

```bash
# VS毎のディレクトリ作成例
outputs/4-architecture/
├── vs1-market-insight/
├── vs2-product-innovation/
├── vs3-branding/
├── vs4-supply-chain/
├── vs5-quality/
├── vs6-data-platform/
└── cross-vs/
```

### ステップ2: サービス境界の決定とサービス定義

Phase 3のCL3（Bounded Contexts）を基に、Value Stream毎にマイクロサービス境界を決定し、
サービス毎にディレクトリを作成してサービス定義ファイルを配置します。

**成果物**: `outputs/4-architecture/{vs-name}/services/{service-name}/service-definition.md`

#### サービス定義テンプレート

```markdown
# {Service Name}（{日本語名}）

**プロジェクト:** {project-name}
**Value Stream:** {VS名}
**作成日:** {date}
**ステータス:** 初版

---

## 基本情報

| 項目 | 値 |
|------|-----|
| **サービス名** | {Service Name} |
| **日本語名** | {日本語名} |
| **ドメインタイプ** | Core / Supporting / Generic |
| **所有チーム** | {チーム名} |
| **リポジトリ** | `{org}/{repo-name}` |

---

## 含まれるBounded Contexts

- **{bc-name} BC**
  - 参照: `outputs/3-capabilities/{vs}/cl3-bounded-contexts/{bc}.md`

**統合/分離理由:**
{なぜこれらのBCを1つのサービスにまとめた/分離したか}

---

## 責務

### ミッション
{このサービスの存在意義}

### 主要責務
1. {責務1}
2. {責務2}
3. {責務3}

---

## ドメインモデル

### Aggregates

\```yaml
{AggregateName}:
  説明: {説明}
  Root Entity: {ルートエンティティ}
  Entities:
    - {Entity1}
    - {Entity2}
  Value Objects:
    - {VO1}
    - {VO2}
\```

---

## API仕様

### REST API

\```yaml
Base URL: /api/v1/{service-name}

Endpoints:
  GET /{resources}: {説明}
  POST /{resources}: {説明}
  GET /{resources}/{id}: {説明}
  PUT /{resources}/{id}: {説明}
\```

---

## イベント

### Published Events

\```yaml
{EventName}: {説明}
{EventName2}: {説明}
\```

### Subscribed Events

\```yaml
{EventName}: (from {source-service})
  → {トリガーされるアクション}
\```

---

## データストア

\```yaml
Primary Database:
  Type: PostgreSQL
  Schema: {schema_name}
\```

---

## 依存関係

### 依存先（Upstream）

| サービス | 依存内容 |
|----------|----------|
| {Service} | {何を利用するか} |

### 提供先（Downstream）

| サービス | 提供内容 |
|----------|----------|
| {Service} | {何を提供するか} |

---

## 非機能要件

\```yaml
Scaling:
  Requirement: 高/中/低
  Replicas: {数}

SLA: {目標}%
\```

---

**作成者:** Claude (Parasol V5)
**最終更新:** {date}
```

#### サービスディレクトリ構造例

```
vs2-product-innovation/
└── services/
    ├── fermentation-research-service/
    │   ├── service-definition.md
    │   └── bounded-contexts/
    │       └── fermentation-research-bc.md → symlink to Phase 3
    ├── beer-development-service/
    │   ├── service-definition.md
    │   └── bounded-contexts/
    │       ├── premium-beer-development-bc.md → symlink
    │       └── craft-innovation-development-bc.md → symlink
    └── ...
```

### ステップ2.5: BCシンボリックリンクの作成

サービスに含まれるBCをディレクトリから可視化するため、Phase 3のBCファイルへの
シンボリックリンクを作成します。

```bash
# サービスディレクトリ内でシンボリックリンクを作成
cd outputs/4-architecture/{vs-name}/services/{service-name}
mkdir -p bounded-contexts

# Phase 3のBCファイルへのシンボリックリンク作成
ln -sf ../../../../../3-capabilities/{vs-name}/cl3-bounded-contexts/{bc-name}-bc.md bounded-contexts/
```

**例: Beer Development Service**
```bash
cd outputs/4-architecture/vs2-product-innovation/services/beer-development-service
mkdir -p bounded-contexts

ln -sf ../../../../../3-capabilities/vs2-product-innovation/cl3-bounded-contexts/premium-beer-development-bc.md bounded-contexts/
ln -sf ../../../../../3-capabilities/vs2-product-innovation/cl3-bounded-contexts/craft-innovation-development-bc.md bounded-contexts/
```

**確認方法:**
```bash
ls -la bounded-contexts/
# premium-beer-development-bc.md -> ../../../../../3-capabilities/.../premium-beer-development-bc.md
# craft-innovation-development-bc.md -> ../../../../../3-capabilities/.../craft-innovation-development-bc.md
```

### ステップ3: Context Mapの作成

VS内のサービス間関係性とパターンを定義します。

**成果物**: `outputs/4-architecture/{vs-name}/context-map.md`

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

### ステップ4: 統合パターンの定義

VS横断のサービス間通信パターンを定義します。

**成果物**: `outputs/4-architecture/cross-vs/integration-patterns.md`

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

### ステップ5: ADR（Architecture Decision Records）の作成

重要なアーキテクチャ決定を文書化します。

**成果物**: `outputs/4-architecture/cross-vs/decisions/adr-*.md`

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

- ✅ architecture-overview.md（全体概要）
- ✅ {vs-name}/overview.md（VS毎の概要）
- ✅ {vs-name}/context-map.md（VS毎のContext Map）
- ✅ {vs-name}/services/{service}/service-definition.md（サービス毎）
- ✅ cross-vs/integration-patterns.md
- ✅ cross-vs/decisions/adr-*.md（最低5つ）

## 完了メッセージ

```
✅ Phase 4: Architecture が完了しました

成果物:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ outputs/4-architecture/architecture-overview.md

VS別成果物:
✅ outputs/4-architecture/{vs-name}/
   ├── overview.md
   ├── context-map.md
   └── services/
       ├── {service-1}/service-definition.md
       ├── {service-2}/service-definition.md
       └── ...
[{N}サービス定義済み]

共通成果物:
✅ outputs/4-architecture/cross-vs/
   ├── integration-patterns.md
   └── decisions/
       ├── adr-001-*.md
       ├── adr-002-*.md
       └── ...
[{M} ADRs作成済み]

アーキテクチャサマリー:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Value Streams: {VS数}
定義済みサービス: {サービス数}
  - Core: {数}
  - Supporting: {数}
  - Generic: {数}

統合パターン: REST, gRPC, Event-Driven, CQRS

📊 ステータス確認:
→ `/parasol:0-status`

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

1. **ディレクトリ構造**: VS毎・サービス毎のディレクトリが正しく作成されているか
2. **サービス完全性**: 全BCがいずれかのサービスに含まれているか
3. **Context Map整合性**: サービス定義で定義した依存関係がContext Mapに記載されているか
4. **循環依存**: Context Mapに循環依存がないか
5. **ADR完全性**: 主要な決定がADRとして文書化されているか

問題がある場合：

```
⚠️ バリデーション警告

ディレクトリ構造:
- vs2-product-innovation/services/pricing-service/ が未作成です

サービス定義:
- Authentication BCがどのサービスにも含まれていません

Context Map:
- Order Service → Pricing Serviceの関係が未定義です
- 循環依存を検出: A → B → C → A

ADR:
- データベース選択に関するADRが不足しています

修正して再度確認しますか？
→ `/parasol:0-validate`
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

- **フレームワーク設計**: `parasol-v5/FRAMEWORK-DESIGN.md`
- **テンプレート**: `parasol-v5/templates/phase4/`
- `service-boundary-template.md`
- `context-map-template.md`
- `adr-template.md`
- **Context Mapパターン**: `/parasol:0-help mapping`
