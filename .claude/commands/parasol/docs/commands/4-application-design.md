---
description: Application design - microservice decomposition (project:parasol)
---

# Phase 4: Application Design - アプリケーションデザイン（マイクロサービス分割）

## 設計哲学

### アプリケーション設計における原則

Phase 4では、Parasolの「**保守性と変更容易性**」を最優先にしたアプリケーション設計を行います：

1. **APIファーストアーキテクチャ**
   - 同期通信を基本とし、追跡しやすいフロー
   - イベント駆動の複雑さを回避
   - 必要時のみバッチ処理を活用

2. **デフォルト統合パターン**
   - **Orchestration at the Edge**: フロントエンドオーケストレーション
   - **Integration Hub Pattern**: レガシー統合ハブ
   - キューシステムの回避

3. **テスト可能性の重視**
   - ローカル環境での完全テスト
   - サービスの停止・入れ替えが容易
   - デバッグの容易さ

詳細は [PHILOSOPHY.md](./PHILOSOPHY.md) および [default-integration-patterns.md](./_patterns/_integration/default-integration-patterns.md) を参照してください。

Phase 3で定義したビジネス能力（CL1/CL2/CL3）を基に、技術的観点からBounded Contextsを定義し、システム全体のアプリケーションアーキテクチャを設計します。

## 目的

- サービス境界の最終決定
- Context Map（BC間の関係）の作成
- 統合パターンの定義
- アーキテクチャ決定の文書化（ADR）

## 🎯 V5.1 デフォルト統合パターン

Parasol V5.1では、シンプルさと実用性を重視した標準統合パターンを提供しています：

### 1. Orchestration at the Edge
- フロントエンドがビジネスフローを制御
- 複雑なイベント駆動を回避
- デバッグとトレースが容易

### 2. Integration Hub Pattern
- レガシーシステムとの統合を一元管理
- バッチとリアルタイムのハイブリッド
- Anti-Corruption Layerによる保護

詳細は `_patterns/_integration/default-integration-patterns.md` を参照してください。

## 🎯 V5特有機能: アプリケーション設計ストーリー出力

**重要**: Parasol V5では、アプリケーション設計の各段階で**設計ストーリー（なぜそう設計したか）**を出力します。

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

## 🤖 Amplifierサブエージェント連携

Phase 4では以下のサブエージェントを活用して、アーキテクチャ設計を深化させます。

### 使用するサブエージェント

| サブエージェント | 用途 | 起動タイミング |
|-----------------|------|---------------|
| **zen-architect** (ARCHITECT) | システム設計、サービス境界決定 | 全体設計時 |
| **database-architect** | データベース設計、永続化戦略 | データモデル設計時 |
| **integration-specialist** | 外部システム連携、API設計 | 統合パターン決定時 |
| **security-guardian** | セキュリティアーキテクチャレビュー | セキュリティ設計時 |

### zen-architect (ARCHITECT mode) の活用

サービス境界とContext Mapの設計を委譲します：

```
Task tool を使用して zen-architect (ARCHITECT mode) を起動：

プロンプト:
「Phase 3のBC定義を基に、サービスアーキテクチャを設計してください。

入力:
- Bounded Contexts: {bc_list_from_phase3}
- Core/Supporting/Generic分類: {domain_classification}
- 統合要件: {integration_requirements}

設計タスク:
1. BC→サービスのマッピング（1:1, N:1, 1:N）
2. サービス間の依存関係とContext Map
3. 統合パターンの選択（Customer-Supplier, Partnership等）
4. 非機能要件（スケーラビリティ、可用性）への対応

設計ストーリーも含めて出力してください。」
```

### database-architect の活用

各サービスのデータ永続化戦略を設計します：

```
Task tool を使用して database-architect を起動：

プロンプト:
「以下のサービス群のデータベースアーキテクチャを設計してください。

入力:
- サービス一覧: {service_list}
- 各サービスの集約ルート: {aggregates_per_service}
- 整合性要件: {consistency_requirements}
- クエリパターン: {expected_query_patterns}

設計タスク:
1. データベース選定（RDB/NoSQL/混合）の理由
2. サービス毎のスキーマ概要
3. 結果整合性 vs 強整合性の判断
4. イベントソーシング適用の検討
5. CQRS適用の検討

出力:
- database-strategy.md（戦略文書）
- 各サービスのデータモデル概要
- ADR: データベース選定理由」
```

### integration-specialist の活用

外部システムやサービス間の統合を設計します：

```
Task tool を使用して integration-specialist を起動：

プロンプト:
「サービス間および外部システムとの統合アーキテクチャを設計してください。

入力:
- 内部サービス一覧: {internal_services}
- 外部システム: {external_systems}
- 統合パターン候補: {integration_patterns}

設計タスク:
1. 同期/非同期の選択と理由
2. API Gateway設計
3. イベントバス/メッセージブローカー設計
4. サーキットブレーカー等のレジリエンスパターン
5. 認証・認可アーキテクチャ

出力:
- integration-architecture.md
- API仕様の方針
- ADR: 統合パターン選択理由」
```

### security-guardian の活用（オプション）

セキュリティ観点でのアーキテクチャレビューを実施：

```
Task tool を使用して security-guardian を起動：

プロンプト:
「設計されたアーキテクチャのセキュリティレビューを実施してください。

入力:
- アーキテクチャ概要: {architecture_overview}
- 認証・認可設計: {auth_design}
- データフロー: {data_flows}

レビュー観点:
1. OWASP Top 10への対応
2. 認証・認可の適切性
3. データ保護（暗号化、マスキング）
4. 監査ログ設計
5. セキュリティ境界の妥当性

出力:
- security-review.md
- 推奨事項リスト
- ADR: セキュリティ設計決定」
```

### サブエージェント出力の統合

```
outputs/4-architecture/
├── architecture-overview.md     # 最終成果物
├── database-strategy.md         # database-architect出力 ← New
├── integration-architecture.md  # integration-specialist出力 ← New
├── security-review.md           # security-guardian出力 ← New
└── decisions/
    ├── adr-001-*.md
    └── adr-002-*.md
```

---

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
├── capability-bc-mapping.md              # ★ CL2-BC対応表（必須）
├── context-map.md                        # BC間関係（Context Map）
├── architecture-overview.md              # Phase 4全体概要
├── integration-patterns.md               # ★ 統合パターン設計（V5.1追加）
│
├── services/                             # サービス毎のディレクトリ
│   └── {service-name}/
│       └── bounded-contexts.md           # サービス内BC一覧
│
└── decisions/                            # Architecture Decision Records
    └── adr-*.md
```

### capability-bc-mapping.md（必須）

**V5.1の重要な追加要件**: Phase 4 では CL2（Capability）から BC（Bounded Context）への
対応関係を明示的に定義します。

```markdown
# Capability-BC Mapping

## 対応パターン

| CL2 Capability | BC名 | 対応パターン | 理由 |
|----------------|------|-------------|------|
| fermentation-research | fermentation-bc | 1:1 | 単一責務で完結 |
| quality-control, quality-assurance | quality-bc | N:1統合 | 関連性が高い |
| large-capability | cap-a-bc, cap-b-bc | 1:N分割 | 複雑性が高い |

## 対応パターンの選択基準

- **1:1対応**: 小規模・単純なケース
- **N:1統合**: 関連性の高いCapability群を1BCに統合
- **1:N分割**: 複雑・大規模なCapabilityを複数BCに分割
```

参照: [capability-bc-test-structure.md](./_software-design-reference/capability-bc-test-structure.md)

### 成果物一覧

1. **capability-bc-mapping.md** - ★ CL2-BC対応表（必須・Phase 5への橋渡し）
2. **context-map.md** - BC間関係（U/D, ACL, Partnership等）
3. **architecture-overview.md** - Phase 4全体の概要とナビゲーション
4. **integration-patterns.md** - ★ 統合パターン設計（V5.1追加）
5. **services/{service}/bounded-contexts.md** - サービス内BC一覧
6. **decisions/adr-*.md** - Architecture Decision Records

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

### コングロマリット（事業部軸パターン）でのContext Map

> ⚠️ **重要**: コングロマリットでは事業部間の関係をContext Mapで表現します。
> シナジーはVStrではなく、BC間の関係性として設計してください。

**事業部間の推奨Context Mapパターン**:

| パターン | 適用場面 | 結合度 | 例 |
|----------|----------|--------|-----|
| **Separate Ways** | 事業間の独立性が高い場合 | 最低 | 酒類BC ↔ 飲料BC（データ非共有） |
| **Published Language** | 共通マスタの参照 | 低 | 顧客マスター → 各事業BC（参照のみ） |
| **Shared Kernel** | 必須の共有データ | 中 | 顧客ID基盤（読み取り専用） |
| **Customer-Supplier** | 明確な上下関係 | 中〜高 | R&D基盤 → 各事業BC |
| **Partnership** | 慎重に使用 | 高 | 事業部間では避ける（結合度が高い） |

```
┌─────────────────────────────────────────────────────────────────────┐
│  コングロマリット Context Map 推奨構造                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────┐        │
│  │     Shared Kernel (読み取り専用)                         │        │
│  │   顧客マスター、商品カタログ（参照のみ、更新は各事業）    │        │
│  └─────────────────────────────────────────────────────────┘        │
│              ↓ Published Language                                   │
│                                                                     │
│  ┌──────────────┐  Separate Ways  ┌──────────────┐                 │
│  │  事業A BC群   │ ←─────────────→ │  事業B BC群   │                 │
│  │  (酒類)       │                 │  (飲料)       │                 │
│  └──────────────┘                 └──────────────┘                 │
│         ↑                                 ↑                         │
│         │ Customer-Supplier               │ Customer-Supplier       │
│         ↓                                 ↓                         │
│  ┌─────────────────────────────────────────────────────────┐        │
│  │     Supporting Layer BC群                                │        │
│  │   共通R&D、品質保証基盤、物流基盤                         │        │
│  └─────────────────────────────────────────────────────────┘        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

⚠️ 事業部間での Partnership は避ける（結合度が高くなりすぎる）
⚠️ 「シナジーBC」を定義してはいけない（シナジーはBC間関係で表現）
```

詳細: `_patterns/_axes/business-unit-axis.md`（コングロマリット設計原則）

---

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

VS横断のサービス間通信パターンを定義します。V5.1では、シンプルさと実用性を重視した2つのデフォルトパターンを推奨しています。

**成果物**: `outputs/4-architecture/integration-patterns.md`

#### 統合パターンテンプレート

```markdown
# 統合パターン設計

**プロジェクト**: {project-name}
**作成日**: {date}
**バージョン**: V5.1

---

## 採用パターン

### 1. Orchestration at the Edge

**適用箇所**:
- フロントエンドからのAPI呼び出し
- {具体的な適用例}

**理由**:
- {なぜこのパターンを選択したか}
- シンプルなフロー制御
- デバッグの容易さ

**実装方針**:
- フロントエンド: {技術スタック}
- API設計: RESTful, 冪等性確保
- エラーハンドリング: {方針}

### 2. Integration Hub Pattern

**適用箇所**:
- {レガシーシステム名}との統合
- {外部システム名}との連携

**理由**:
- レガシーシステムの複雑性隔離
- バッチとリアルタイムの混在
- データ変換の必要性

**統合ハブ設計**:
```yaml
integration-hub-service:
  レガシー連携:
    - システム: {レガシーシステム名}
    - プロトコル: {SOAP/REST/DB直接}
    - 同期方式: {バッチ/リアルタイム}
    - 更新頻度: {頻度}
  
  データ変換:
    - {レガシーモデル} → {ドメインモデル}
    - 検証ルール: {ルール}
  
  キャッシュ戦略:
    - マスタデータ: TTL 24時間
    - トランザクション: TTL 5-15分
```

### 3. 従来パターン（必要に応じて）

**非同期通信**（限定的使用）:
- 使用箇所: {具体例}
- 理由: {なぜ非同期が必要か}
- 実装: {メッセージキュー/イベントバス}

---

## 通信プロトコル標準

```yaml
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

## VMS4マイルストーン設定（運用設計完了）

### VMS4_Operational_Design_Milestone

```yaml
VMS4_Operational_Design_Milestone:
  target_completion: "Phase 3完了から6週間"
  success_criteria:
    architecture_completeness: "アプリケーションアーキテクチャ確定"
    service_boundaries: "マイクロサービス境界の最終決定"
    integration_patterns: "統合パターンとAPIの詳細設計完了"
    deployment_readiness: "実装・デプロイ準備完了"
  
  deliverables:
    - architecture-overview.md (全体設計)
    - context-map.md (BC統合設計)
    - services/{service}/service-definition.md (サービス詳細)
    - vms4-completion-report.md
    - operational-readiness-assessment.md

  measurement_framework:
    service_design_quality: "実装可能なサービス定義割合"
    integration_completeness: "API契約定義率"
    architectural_consistency: "設計原則準拠率"
  
  progression_requirements_to_vms5:
    implementation_planning: "実装計画とスケジュール"
    team_allocation: "開発チーム配置完了"
    technology_setup: "開発・運用環境準備"
    value_measurement: "価値測定システム準備"
```

### VMS4成果物（Phase 4-6統合）

| ファイル | Phase | 目的 | VMS5への影響 |
|---------|-------|------|-------------|
| **vms4-completion-report.md** | 4-6 | VMS4達成状況 | 価値実現開始条件 |
| **operational-readiness-assessment.md** | 4-6 | 運用準備度評価 | 価値測定体制準備 |
| **implementation-validation.md** | 6 | 実装品質検証 | 価値実現システム基盤 |

🎯 次のステップ: Phase 5 Software Design
→ `/parasol:5-software-design`

Phase 5では各サービス/BCの詳細設計を行います：
- ドメインモデル（Parasol Domain Language）
- API仕様（OpenAPI）
- VMS4マイルストーン進捗管理
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

- **テンプレート**: `parasol-v5/templates/phase4/`
- `service-boundary-template.md`
- `context-map-template.md`
- `adr-template.md`
- **Context Mapパターン**: `/parasol:0-help mapping`
