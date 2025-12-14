# ケーパビリティ命名ガイドライン

**Parasol V5 - DXにふさわしい命名規則**

**バージョン**: V2.0（機能特性別変換ルール追加）

---

## なぜ「管理」を排除するのか

### 「管理」がもたらす負の連鎖

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    「管理」→ CRUD思考 → システム停滞                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  【問題の連鎖】                                                              │
│                                                                             │
│    「○○管理」という命名                                                     │
│         │                                                                   │
│         ▼                                                                   │
│    CRUD思考を誘発（登録・更新・削除・参照）                                   │
│         │                                                                   │
│         ▼                                                                   │
│    データベーステーブル中心設計                                               │
│         │                                                                   │
│         ▼                                                                   │
│    ビジネスロジック埋没・分散                                                 │
│         │                                                                   │
│         ▼                                                                   │
│    変革・進化しづらいシステム（技術的負債の蓄積）                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### DXワードがもたらす正の連鎖

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DXワード → 価値創造思考 → システム進化                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  【価値創造の連鎖】                                                          │
│                                                                             │
│    オーケストレーション → 連携・調整・最適化 → プロセス中心設計              │
│                                                                             │
│    インテリジェンス    → 分析・予測・推奨   → データ活用設計                 │
│                                                                             │
│    ハブ              → 関係・接続・価値交換 → エコシステム設計               │
│                                                                             │
│    エンジン          → 自動化・駆動・加速  → 処理効率設計                    │
│                                                                             │
│  ────────────────────────────────────────────────────────────────────────   │
│                                                                             │
│  ★ 名称が思考を規定する → 組織の思考OSアップグレード                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 機能特性別変換ルール（推奨）

### 変換ルール表

| 機能特性 | 使用ワード | 英語 | 適用条件 |
|----------|-----------|------|----------|
| **調整・連携中心** | オーケストレーション | Orchestration | 複数要素の調整・連携が主機能 |
| **分析・予測中心** | インテリジェンス | Intelligence | データ分析・予測・意思決定支援が主機能 |
| **関係性中心** | ハブ | Hub | 関係者・システム間の接続・価値交換が主機能 |
| **処理・自動化中心** | エンジン | Engine | 自動処理・駆動・効率化が主機能 |

### 具体的変換例

| 旧名称（管理） | 新名称（DX） | 機能特性 | 理由 |
|--------------|-------------|----------|------|
| 受注管理 | 受注オーケストレーション | 調整・連携 | 複数部門・システムの調整 |
| 在庫管理 | 在庫インテリジェンス | 分析・予測 | 需要予測・最適配置の分析 |
| 配送管理 | 配送オーケストレーション | 調整・連携 | 配送業者・倉庫の調整 |
| 顧客管理 | カスタマーハブ | 関係性 | 顧客との接点・価値交換 |
| 決済管理 | 決済エンジン | 処理・自動化 | 決済処理の自動実行 |
| 出荷管理 | 出荷エンジン | 処理・自動化 | 出荷処理の自動実行 |
| 需要管理 | 需要インテリジェンス | 分析・予測 | 需要予測・分析 |
| パートナー管理 | パートナーハブ | 関係性 | パートナーとの接続 |
| プロジェクト管理 | プロジェクトオーケストレーション | 調整・連携 | タスク・リソースの調整 |

### 判断フローチャート

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    機能特性判断フロー                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  このケイパビリティの主機能は？                                              │
│         │                                                                   │
│         ├─► 複数の要素・部門・システムを調整する                             │
│         │   → オーケストレーション（Orchestration）                         │
│         │                                                                   │
│         ├─► データを分析・予測・意思決定を支援する                           │
│         │   → インテリジェンス（Intelligence）                              │
│         │                                                                   │
│         ├─► 関係者・システムを接続・価値交換する                             │
│         │   → ハブ（Hub）                                                   │
│         │                                                                   │
│         └─► 処理を自動化・効率化・加速する                                   │
│             → エンジン（Engine）                                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 基本原則

### 「XXX管理」表現を避ける

DXにふさわしい命名は、**静的な「管理」ではなく、動的な「進化・発展・改善」**を表現します。

### 避けるべきパターン

| 避けるべき表現 | 問題点 |
|--------------|--------|
| `xxx-management` | 静的、維持・保守の印象 |
| `xxx-administration` | 管理者目線、官僚的 |
| `xxx-control` | 制御・監視の印象 |
| `xxx-master` | マスターデータ管理の印象 |
| `xxx-handling` | 処理・取り扱いの印象 |

### 推奨パターン

#### 1. **価値創造型** (Value Creation)

顧客やビジネスへの価値を直接表現：

| パターン | 意味 | 例 |
|---------|------|-----|
| `xxx-innovation` | 革新・創造 | `product-innovation`, `process-innovation` |
| `xxx-development` | 開発・進化 | `beer-development`, `talent-development` |
| `xxx-design` | 設計・創造 | `experience-design`, `service-design` |
| `xxx-creation` | 創出・生成 | `value-creation`, `content-creation` |

#### 2. **変革型** (Transformation)

変化・進化・改善を表現：

| パターン | 意味 | 例 |
|---------|------|-----|
| `xxx-transformation` | 変革 | `digital-transformation`, `business-transformation` |
| `xxx-optimization` | 最適化 | `supply-optimization`, `cost-optimization` |
| `xxx-enhancement` | 強化・向上 | `quality-enhancement`, `performance-enhancement` |
| `xxx-evolution` | 進化 | `brand-evolution`, `capability-evolution` |
| `xxx-acceleration` | 加速 | `growth-acceleration`, `time-to-market-acceleration` |

#### 3. **アクション型** (Action-Oriented)

具体的なビジネスアクションを表現：

| パターン | 意味 | 例 |
|---------|------|-----|
| `xxx-research` | 研究・探究 | `fermentation-research`, `market-research` |
| `xxx-engineering` | 技術的構築 | `process-engineering`, `data-engineering` |
| `xxx-analysis` | 分析・洞察 | `customer-analysis`, `trend-analysis` |
| `xxx-discovery` | 発見 | `insight-discovery`, `opportunity-discovery` |
| `xxx-orchestration` | 統合調整 | `service-orchestration`, `workflow-orchestration` |

#### 4. **成果型** (Outcome-Focused)

達成すべき成果を表現：

| パターン | 意味 | 例 |
|---------|------|-----|
| `xxx-enablement` | 実現支援 | `sales-enablement`, `digital-enablement` |
| `xxx-fulfillment` | 充足・達成 | `order-fulfillment`, `customer-fulfillment` |
| `xxx-delivery` | 提供・配信 | `value-delivery`, `service-delivery` |
| `xxx-intelligence` | 知能化 | `business-intelligence`, `competitive-intelligence` |
| `xxx-experience` | 体験 | `customer-experience`, `employee-experience` |

#### 5. **関係構築型** (Relationship-Focused)

関係性やつながりを表現：

| パターン | 意味 | 例 |
|---------|------|-----|
| `xxx-engagement` | 関与・エンゲージメント | `customer-engagement`, `stakeholder-engagement` |
| `xxx-collaboration` | 協働 | `partner-collaboration`, `cross-functional-collaboration` |
| `xxx-integration` | 統合 | `system-integration`, `data-integration` |
| `xxx-orchestration` | 調整・連携 | `ecosystem-orchestration` |

---

## 変換例

### ❌ → ✅ 命名変換表

| 避けるべき命名 | 推奨命名 | 理由 |
|--------------|---------|------|
| `inventory-management` | `inventory-optimization` | 在庫は「管理」ではなく「最適化」する |
| `order-management` | `order-orchestration` または `order-fulfillment` | 注文の「オーケストレーション」や「充足」 |
| `customer-management` | `customer-engagement` | 顧客は「管理」ではなく「関係構築」 |
| `content-management` | `content-creation` または `content-delivery` | コンテンツは「創造」し「配信」する |
| `product-catalog-management` | `product-catalog-curation` | カタログは「キュレーション」（整理・選定） |
| `asset-management` | `asset-optimization` | 資産は「最適化」する |
| `resource-management` | `resource-orchestration` | リソースは「オーケストレーション」 |
| `knowledge-management` | `knowledge-synthesis` | 知識は「統合」する |
| `project-management` | `project-orchestration` | プロジェクトは「統合調整」 |
| `data-management` | `data-engineering` または `data-governance` | データは「エンジニアリング」または「ガバナンス」 |

---

## 業界別推奨パターン

### 飲料・食品業界（asashi参考）

| ドメイン | 推奨命名 | 理由 |
|---------|---------|------|
| 研究開発 | `xxx-research`, `xxx-development` | 研究・開発は継続的進化を表現 |
| 製造 | `xxx-engineering`, `xxx-optimization` | 製造プロセスの技術的改善を表現 |
| 品質 | `quality-assurance`, `quality-enhancement` | 品質の保証・向上を表現 |
| 原材料 | `ingredient-research`, `sourcing-optimization` | 素材研究・調達最適化を表現 |

### 金融業界

| ドメイン | 推奨命名 |
|---------|---------|
| 顧客 | `customer-engagement`, `advisory-experience` |
| リスク | `risk-intelligence`, `risk-mitigation` |
| 取引 | `transaction-processing`, `settlement-automation` |
| コンプライアンス | `compliance-assurance`, `regulatory-adaptation` |

### 製造業

| ドメイン | 推奨命名 |
|---------|---------|
| 生産 | `production-orchestration`, `manufacturing-intelligence` |
| 品質 | `quality-engineering`, `defect-prevention` |
| 在庫 | `inventory-optimization`, `supply-intelligence` |
| 設備 | `equipment-reliability`, `maintenance-optimization` |

### 小売・EC

| ドメイン | 推奨命名 |
|---------|---------|
| 商品 | `product-curation`, `assortment-optimization` |
| 注文 | `order-fulfillment`, `delivery-excellence` |
| 顧客 | `customer-experience`, `personalization-engine` |
| 販促 | `promotion-intelligence`, `campaign-optimization` |

---

## 検証チェックリスト

新しいケーパビリティ名を決める際のチェックリスト：

### ✅ 必須チェック

- [ ] 「XXX管理」「XXX-management」を含まない
- [ ] 動的な行動・変化を表現している
- [ ] ビジネス価値を想起させる
- [ ] kebab-case形式である
- [ ] VS横断で一意である（重複なし）

### ✅ 推奨チェック

- [ ] 顧客/ユーザー視点で意味が通じる
- [ ] 競争優位性や差別化を意識した表現
- [ ] 将来の進化・拡張を妨げない抽象度
- [ ] チーム/組織がオーナーシップを持ちやすい名前

---

## AI（Claude）への指示

ケーパビリティ名を生成する際、以下のルールを適用してください：

1. **「XXX管理」「XXX-management」を生成しない**
2. **推奨パターンから適切なものを選択**
3. **業界・ドメインに適した表現を使用**
4. **VS横断での一意性を確認**
5. **命名理由を記載**

```yaml
# 出力例
capability:
  name: fermentation-research
  name_ja: 発酵研究
  naming_rationale: |
    「発酵管理」ではなく「発酵研究」を採用。
    理由: 継続的な研究・進化を表現し、アサヒグループの競争優位性の源泉である
    酵母・発酵技術の探究姿勢を反映。
```

---

## 参考リンク

- Parasol V5 概念説明: `/parasol:0-help concepts`
- ケーパビリティ分解コマンド: `/parasol:3-capabilities`
- ナレッジベース: `.claude/commands/parasol/_capability-knowledge/`

---

**更新履歴:**
- 2025-12-11: V2.0 - 「管理→CRUD誘発→システム停滞」問題の解説追加、機能特性別変換ルール追加
- 2025-11-27: V1.0 - 初版作成
