---
description: Capability decomposition - L2 WHAT in ZIGZAG process (project:parasol)
---

# Phase 3: Capabilities - ケイパビリティ分解

## ZIGZAGプロセスにおける位置づけ

```
┌─────────────────────────────────────────────────────────────┐
│ Level 2: サービス層                                         │
│                                                             │
│   ★ WHAT: Capability  →    HOW: Service設計                │
│     Phase 3 ← 今ここ       Phase 4                         │
└─────────────────────────────────────────────────────────────┘
```

**Phase 3の役割**: Value Stage（Phase 2で定義）をスイムレーンとして、各Stageに必要なCapability（サービス候補）を特定します。

**重要原則**: Phase 4でサービス枠を確定するため、ここでは「何が必要か」（WHAT）に集中します。

## 使用方法

```bash
# CL1: 活動領域分類（戦略的、投資判断）
/parasol:3-capabilities cl1

# CL2: ケイパビリティ設計（戦術的、サービス境界）
/parasol:3-capabilities cl2              # インタラクティブ選択
/parasol:3-capabilities cl2 VS2          # VS2（製品開発）を直接指定

# CL3: 業務オペレーション定義（運用的、業務活動）
/parasol:3-capabilities cl3                           # インタラクティブ選択
/parasol:3-capabilities cl3 fermentation-research     # 直接指定

# BC: 実装設計（技術的、開発者向け）
/parasol:3-capabilities bc fermentation-research      # 直接指定

# CL3 + パラソルドメイン言語生成（V5新機能）
/parasol:3-capabilities cl3 --with-domain-language
```

## 🎯 設計哲学の適用

### DDD的ボトムアップを防ぐトップダウン設計

> **重要**: Phase 3は**価値ストリームから分解**する。エキスパートの意見から構築しない。

#### ❌ 避けるべきDDD的パターン

**ボトムアップの罠**:
- 「ドメインエキスパートに聞いてみましょう」
- 「イベントストーミングで境界を発見」
- 「ユーザーストーリーから開始」
- 「現在の組織構造をそのまま反映」

**断片化の問題**:
- 各チームの視点で個別最適化
- 統合が後付けになる
- 価値ストリームとの整合性が失われる

#### ✅ Parasolのトップダウンアプローチ

**価値起点の分解**:
```
Phase 2で定義された価値ストリーム
    ↓
VS別に必要なケイパビリティを特定
    ↓  
価値フロー全体での整合性確保
    ↓
ビジネスオペレーションに分解
```

**統合設計の原則**:
- 価値ストリームが境界を決定する
- 各ケイパビリティは価値への貢献が明確
- 価値フロー全体を最初から設計
- 局所最適ではなく全体最適を追求

#### 必須の価値トレーサビリティ

**各ケイパビリティについて回答必須**:
1. **どの価値ストリーム**に貢献するか？
2. **どの顧客価値**を実現するか？
3. **なぜ独立したケイパビリティ**である必要があるか？
4. **他のケイパビリティと**どう連携するか？

## 設計原則

### ケイパビリティ分解における哲学

Phase 3では、Parasolの「**保守性と変更容易性**」を重視してケイパビリティを分解します：

1. **価値駆動の境界設定**
   - 価値ストリームから導出される明確な境界
   - ケイパビリティは独立して理解・変更可能な単位
   - 過度に細かく分割しすぎない（複雑化を避ける）
   - 各ケイパビリティが明確な責任を持つ

2. **将来の変更を想定**
   - ビジネス変化が予想される箇所を境界に
   - 変更頻度が異なる機能は分離
   - 技術的要求ではなくビジネス要求で分割

3. **運用可能性の確保**
   - 各ケイパビリティが独立してテスト・デプロイ可能
   - チームが管理可能なサイズ
   - 障害時の影響範囲が明確

詳細は [PHILOSOPHY.md](./PHILOSOPHY.md) を参照してください。

## 🤖 サブエージェント活用について

**重要**: ケイパビリティ分解は複雑な分析・設計タスクです。このコマンドは適切なサブエージェントに作業を委譲します。

### 使用するサブエージェント

**CL1: ドメイン分類**
- `zen-architect` (ANALYZE mode)
- 戦略的分析により Core/Supporting/Generic を分類
- 投資配分と優先順位を推奨

**CL2: サブドメイン設計**
- `zen-architect` (ARCHITECT mode)
- ドメイン内のサブドメイン候補を抽出
- マイクロサービス境界を設計

**CL3: Bounded Context定義**
- `zen-architect` (ARCHITECT mode) - BC責務と境界
- `api-contract-designer` - API契約設計（必要に応じて）

### サブエージェント活用の利点

✅ **専門的な分析**: 戦略分析やアプリケーション設計の専門知識を活用
✅ **一貫性**: 確立されたパターンとベストプラクティスを適用
✅ **効率性**: 複雑なタスクを効率的に実行
✅ **品質保証**: 設計品質のレビューと検証

## 目的

ケイパビリティの階層的分解により、ビジネス価値からソフトウェア設計への橋渡しを行います：

- **CL1 活動領域**: 戦略的分類（Core/Supporting/Generic）- 経営層向け
- **CL2 ケイパビリティ**: サービス境界の定義（≈マイクロサービス候補）- 事業部長向け
- **CL3 業務オペレーション**: 具体的な業務活動の定義 - 業務担当者向け
- **BC 実装設計**: 技術設計（集約/イベント/API）- 開発者向け

## 🎯 V5特有機能: ケーパビリティ設計ストーリー出力

**重要**: Parasol V5では、ケーパビリティ分解の各段階で**設計ストーリー（なぜそう設計したか）**を出力します。

### 設計ストーリーの目的

- **設計判断の可視化**: なぜこのドメイン分類か、なぜこの粒度で分解したかを明確に
- **継承関係の明示**: Phase 2の価値定義からどう継承されたかを追跡可能に
- **重複回避の説明**: 既存ケーパビリティとの重複をどう避けたかを記録

### 出力タイミングと内容

| フェーズ | 出力内容 |
|----------|----------|
| **CL1ドメイン分類** | なぜこのVSをCore/Supporting/Genericに分類したか |
| **CL2サブドメイン設計** | なぜこの粒度で分解したか、Phase 2からの継承関係 |
| **CL3 BC定義** | なぜこの境界でBCを切ったか、既存BCとの関係 |

### 設計ストーリーテンプレート

各成果物に以下の「設計ストーリー」セクションを含めます：

```markdown
## 設計ストーリー：なぜこのケーパビリティ構造なのか

### 1. Phase 2からの継承

**継承元（Value Definition）:**
- VL2-1（製品イノベーション価値）→ VS2（製品開発）
- VL3-1-1（発酵技術）→ fermentation-research サブドメイン

**継承の理由:**
[なぜこの価値要素がこのケーパビリティに対応するのか]

### 2. ドメイン分類の理由（CL1）

**Coreに分類した理由:**
- [競争優位の源泉である根拠]
- [他社が真似できない要素]

**Supportingに分類した理由:**
- [重要だが差別化要因ではない根拠]

### 3. 参照した既存ケーパビリティ

**registry.yamlから参照:**
- `fermentation-research`: 類似プロジェクト（asashi）で定義済み → 命名パターンを踏襲
- `product-development`: グローバルパターンとして存在 → 接頭辞でプロジェクト固有化

**業界パターンから参照:**
- `decomposition-patterns.md`: 製造業パターン「研究開発分離型」を適用

### 4. 重複回避の工夫

**命名での重複回避:**
| 候補名 | 問題 | 採用名 | 回避方法 |
|--------|------|--------|----------|
| customer-management | VS3と重複 | vs2-customer-insights | VS接頭辞で区別 |
| quality-control | 汎用的すぎる | quality-assurance-research | 目的を明確化 |

**境界での重複回避:**
- `ingredient-research` と `functional-ingredients` を分離した理由:
  - 前者は「素材そのもの」の研究（原料チーム）
  - 後者は「機能性成分」の研究（健康チーム）
  - チーム境界とスキルセットが異なる

### 5. サブドメイン粒度の決定理由（CL2）

**分解基準:**
| 基準 | 適用結果 |
|------|----------|
| チーム独立性 | 発酵研究は専門チーム → 独立サブドメイン |
| データ境界 | 酵母データは機密性高 → 独立DB必要 |
| 変更頻度 | 製品開発は高頻度 → 分離してデプロイ独立 |

### 6. BC境界の決定理由（CL3）

**集約ルート選定の理由:**
- `YeastStrain` を集約ルートにした理由: 酵母株が全ての実験・培養の起点
- `FermentationExperiment` を別集約にした理由: ライフサイクルが独立

**イベント設計の理由:**
- `YeastStrainRegistered` を公開イベントにした理由: 下流の製品開発チームが新酵母を検知する必要
```

### 参照すべきリソース

| リソース | 用途 | パス |
|----------|------|------|
| **registry.yaml** | 既存ケーパビリティの重複チェック | `_capability-knowledge/registry.yaml` |
| **decomposition-patterns.md** | 業界別分解パターン | `_capability-knowledge/patterns/` |
| **examples/{project}.md** | 類似プロジェクトの学び | `_capability-knowledge/examples/` |
| **Phase 2成果物** | 継承元の価値定義 | `outputs/2-value/` |

---

## 📛 命名ガイドライン

**重要**: DXにふさわしい命名を行うため、「XXX管理」表現を避けてください。

### 避けるべきパターン

| 避ける表現 | 推奨表現 | 理由 |
|-----------|---------|------|
| `xxx-management` | `xxx-optimization`, `xxx-orchestration` | 静的→動的 |
| `inventory-management` | `inventory-optimization` | 在庫は「最適化」する |
| `order-management` | `order-fulfillment` | 注文の「充足」 |
| `customer-management` | `customer-engagement` | 顧客との「関係構築」 |
| `data-management` | `data-engineering` | データの「技術的構築」 |

### 推奨パターン

| パターン | 意味 | 例 |
|---------|------|-----|
| `xxx-research` | 研究・探究 | `fermentation-research` |
| `xxx-development` | 開発・進化 | `beer-development` |
| `xxx-engineering` | 技術的構築 | `process-engineering` |
| `xxx-optimization` | 最適化 | `supply-optimization` |
| `xxx-innovation` | 革新・創造 | `product-innovation` |

**詳細**: `.claude/commands/parasol/_capability-naming-guide.md`

---

## 🔍 VS横断一意性チェック

**重要**: ケーパビリティ名はValue Stream（VS）を横断して**唯一無二**である必要があります。

### チェックタイミング

- **CL2（サブドメイン設計）完了時**: 新規サブドメイン名を登録
- **CL3（BC定義）完了時**: BC名を登録

### チェック方法

**ステップ1**: registry.yaml を読み込み
```bash
# 既存ケーパビリティを確認
cat .claude/commands/parasol/_capability-knowledge/registry.yaml
```

**ステップ2**: 重複チェック
```yaml
# all_capability_names セクションで重複確認
all_capability_names:
  - fermentation-research        # asashi VS2
  - ingredient-research          # asashi VS2
  - customer-engagement          # 別プロジェクト VS3（重複NG）
```

**ステップ3**: 重複時の対処
```
⚠️ 重複検出: "customer-engagement" は既に登録済み

対処オプション:
1. VS接頭辞を追加: vs3-customer-engagement
2. より具体的な名前に変更: b2b-customer-engagement
3. 既存と統合可能か検討
```

### 自動チェック（AI実行時）

CL2/CL3実行時、AIは以下を自動実行：

1. `registry.yaml` を読み込み
2. 新規ケーパビリティ名の重複チェック
3. 類似名グループ（similar_name_groups）との照合
4. 問題なければ `registry.yaml` に追加

---

## 📚 ナレッジベース活用

ケーパビリティ分解の知見を蓄積・再利用するためのナレッジベースを提供します。

### ディレクトリ構成

```
.claude/commands/parasol/_capability-knowledge/
├── README.md                    # 概要
├── registry.yaml                # ケーパビリティ登録簿（一意性保証）
├── patterns/                    # パターン集
│   ├── decomposition-patterns.md # 分解パターン
│   └── naming-patterns.md       # 命名パターン（→ _capability-naming-guide.md）
└── examples/                    # 事例集
    └── {project-name}.md        # プロジェクト別の学び
```

### 活用タイミング

**分解開始前**:
1. `patterns/decomposition-patterns.md` で業界パターンを確認
2. `examples/` で類似プロジェクトの学びを参照
3. `registry.yaml` で既存ケーパビリティを把握

**分解完了後**:
1. `registry.yaml` に新規ケーパビリティを登録
2. `examples/{project-name}.md` に学びを記録
3. 新パターン発見時は `patterns/` に追加

### AIへの指示

CL2/CL3実行時、以下を自動実行：

```yaml
分解開始時:
  - registry.yaml を読み込み、既存ケーパビリティを把握
  - 業界パターンを patterns/decomposition-patterns.md から参照
  - 命名ガイドライン _capability-naming-guide.md を適用

分解完了時:
  - 新規ケーパビリティを registry.yaml に追加
  - 命名理由（naming_rationale）を記録
  - 類似ケーパビリティとの関係を related_capabilities に記録

プロジェクト完了時:
  - examples/{project-name}.md に学びを記録
  - 新パターン発見時は patterns/ に追加提案
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

## 重要な概念

### ケイパビリティ階層の定義

**ビジネスフレンドリーな4階層モデル**

ZIGZAGパターン: **WHAT → HOW → WHAT → HOW**

```
Value Stream (価値創造の流れ)
     │
     ▼
┌─────────────────────────────────────────────────────────────────┐
│ CL1: 活動領域 (Activity Area)                                    │
│ ─────────────────────────────────────────────────────────────── │
│ 【WHAT領域】何の活動領域か？                                       │
│ • 対象: 経営層・事業企画                                          │
│ • 目的: 投資判断・リソース配分の単位                               │
│ • 分類: Core（差別化）/ Supporting（重要）/ Generic（標準）        │
│ • 例: A1基盤技術研究, A2原料調達, A3酒類製品開発                   │
│                                                                 │
│ DDD対応: Domain Classification (Core/Supporting/Generic)         │
└─────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────┐
│ CL2: ケイパビリティ (Capability) ★メイン概念                       │
│ ─────────────────────────────────────────────────────────────── │
│ 【HOW構造】どう組織するか？                                        │
│ • 対象: 事業部長・プロダクトオーナー                               │
│ • 目的: チーム境界・システム境界・データ所有権の定義                │
│ • 粒度: 5-9名のチームで担当可能な範囲（≈マイクロサービス候補）      │
│ • 例: fermentation-research, premium-beer-development           │
│                                                                 │
│ 【注意】小さな活動領域はCL2をスキップしてCL3へ進むことも可          │
│ DDD対応: Subdomain                                              │
└─────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────┐
│ CL3: 業務オペレーション (Business Operation)                       │
│ ─────────────────────────────────────────────────────────────── │
│ 【WHAT詳細】具体的に何をするか？                                   │
│ • 対象: 業務担当者・ドメインエキスパート                           │
│ • 目的: 日々の業務活動の定義                                      │
│ • 構造: トリガー → 活動内容 → 成果物                              │
│ • 粒度: 1日〜1週間で完結する業務単位                              │
│ • 例: 酵母株探索・収集、酵母株育種・改良、発酵条件最適化           │
│                                                                 │
│ DDD対応: Use Case / Business Process                            │
└─────────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────┐
│ BC: 実装設計 (Bounded Context)                                   │
│ ─────────────────────────────────────────────────────────────── │
│ 【HOW実装】どう実装するか？                                        │
│ • 対象: 開発者・アーキテクト                                      │
│ • 目的: CL3の業務オペレーションを実装するための技術設計            │
│ • 内容: 集約 / ドメインイベント / API契約 / ユビキタス言語         │
│ • 例: fermentation-research-bc                                  │
│                                                                 │
│ DDD対応: Bounded Context                                        │
└─────────────────────────────────────────────────────────────────┘
```

### ZIGZAGパターンの説明

```
WHAT       →      HOW        →      WHAT       →      HOW
何の領域?        どう組織?         何をする?         どう実装?
    │               │                │                │
   CL1            CL2              CL3              BC
 活動領域     ケイパビリティ     業務OP          実装設計
 ─────────   ────────────     ─────────       ─────────
  経営層        事業部長        業務担当         開発者
```

### CL2とCL3の違い（重要）

| 観点 | CL2（ケイパビリティ） | CL3（業務オペレーション） |
|------|----------------------|-------------------------|
| **質問** | どう組織するか？ | 何をするか？ |
| **対象** | 事業部長・PO | 業務担当者 |
| **粒度** | 5-9名チーム単位 | 1日〜1週間の業務 |
| **出力** | サービス境界、チーム境界 | オペレーション詳細（トリガー/成果物） |
| **スキップ** | 小さな活動領域なら省略可 | 必須（BCの入力となる） |

### CL3とBCの違い（重要）

| 観点 | CL3（業務オペレーション） | BC（実装設計） |
|------|-------------------------|----------------|
| **質問** | 何をするか？ | どう実装するか？ |
| **対象** | 業務担当者 | 開発者 |
| **言語** | 業務用語 | 技術用語 + ユビキタス言語 |
| **内容** | 業務フロー、業務ルール | 集約、イベント、API契約 |

### アジャイル開発との対応

| パラソル概念 | アジャイル対応 | 期間 |
|-------------|---------------|------|
| **CL3: ビジネスオペレーション** | Epic / Feature | 複数スプリント |
| **Actor UseCase** | User Story ★ | 1スプリント内 |
| **View** | Task | 数時間〜数日 |

**重要**: ビジネスオペレーション（CL3）は複数アクターが協調する業務活動であり、ユースケースではありません。Actor UseCaseが単一ユーザの完結操作として、アジャイルのUser Storyに対応します。

詳細: `_software-design-reference/business-operations.md` の「アジャイル開発との対応関係」セクション

### Bounded Context（BC）と CL3 の関係

**BCは「活動境界」、CL3は「活動」**

```
BC = 活動境界（関心事が一貫する範囲）
│
│  包含関係（1 BC : N CL3）
▼
CL3 = 活動（境界内で行われる業務操作）
```

| 概念 | 定義 | 比喩 | Phase |
|------|------|------|-------|
| **BC** | 活動の境界（同じ言葉が同じ意味を持つ範囲） | 部屋の壁 | Phase 4 |
| **CL3** | 境界内で行われる業務活動 | 部屋の中での作業 | Phase 3 |

**言語境界は結果であり原因ではない**: 活動が違うから関心事が違い、だから同じ言葉でも意味が異なる。

詳細: `_parasol-overview.md` の「6.2 Bounded Context と CL3 の関係」セクション

### 実例：fermentation-research

```
【CL1】活動領域
└── A1基盤技術研究 → Core Domain（競争優位の源泉）

【CL2】ケイパビリティ（A1基盤技術研究内）
├── fermentation-research（発酵研究）← チーム境界
├── ingredient-research（素材研究）
└── ...

【CL3】業務オペレーション（fermentation-research内）
├── OP-FER-001: 酵母株探索・収集
│   └── トリガー: 研究計画確定 → 成果物: 酵母サンプル
├── OP-FER-002: 酵母株育種・改良
│   └── トリガー: 製品要件受領 → 成果物: 改良酵母株
├── OP-FER-003: 発酵条件最適化
│   └── トリガー: 品質要件 → 成果物: 最適条件データ
└── ...

【BC】実装設計（fermentation-research-bc）
├── Aggregate: YeastStrain（酵母株）
│   └── Entity: StrainVariant
│   └── ValueObject: GeneticProfile, FermentationProfile
├── Domain Event: YeastStrainRegistered, BreedingCompleted
├── API: POST /yeast-strains, GET /fermentation-conditions
└── ...
```

## 成果物構造

```
outputs/3-capabilities/
├── {vs-number}-{vs-slug}/                    # VSディレクトリ（Phase 2から導出）
│   ├── cl1-domain-classification.md          # CL1: ドメイン分類（Core/Supporting/Generic）
│   ├── cl2-subdomain-design.md               # CL2: ケイパビリティ設計（サービス境界候補）
│   └── cl3-business-operations/              # CL3: ビジネスオペレーション（What）
│       └── {capability}-operations.md        #      各ケイパビリティの業務活動一覧
└── ...
```

**重要**: Phase 3 はビジネス観点（What）の定義のみ。BCの確定とソフトウェア設計は以下のPhaseで行います：

- **Phase 4**: capability-bc-mapping.md でCL2→BC対応を確定、context-map.md でBC間関係を定義
- **Phase 5**: BC単位で domain-language.md（パラソルドメイン言語）、API仕様、テスト定義を作成

### CL3とBCの分離について

**V5.1の設計思想**: ビジネス定義（What）と技術設計（How）を Phase で明確に分離

```
# Phase 3: ビジネス観点（担当者：事業部長・PO・業務担当者）
outputs/3-capabilities/{vs}/
├── cl1-domain-classification.md      # Core/Supporting/Generic 分類
├── cl2-subdomain-design.md           # ケイパビリティ（サービス境界候補）
└── cl3-business-operations/          # 具体的業務活動
    └── {capability}-operations.md

# Phase 4: アーキテクチャ観点（担当者：アーキテクト）
outputs/4-architecture/
├── capability-bc-mapping.md          # CL2 → BC 対応表
├── context-map.md                    # BC間関係（U/D, ACL等）
└── services/{service}/bounded-contexts.md

# Phase 5: ソフトウェア設計（担当者：設計者・開発者）
outputs/5-software/{service}/{bc-name}/
├── domain-language.md                # パラソルドメイン言語（SSOT）
├── api-specification.md
└── tests/                            # テスト定義
```

参照: [capability-bc-test-structure.md](./_software-design-reference/capability-bc-test-structure.md)

### VSディレクトリ命名規則

**重要**: ディレクトリ名はPhase 2の `value-streams-mapping.md` から動的に導出されます。

**形式**: `{vs-number}-{vs-slug}`
- `{vs-number}`: vs0, vs1, vs2, ... （VS番号）
- `{vs-slug}`: VS名をkebab-caseに変換（日本語→英語→kebab-case）

**導出プロセス**:
1. `outputs/2-value/value-streams-mapping.md` を読み込み
2. 各VSの名前を取得
3. 名前をkebab-case英語に変換してディレクトリ名を生成

**例（プロジェクトにより異なる）**:
```
Phase 2で定義されたVS:
- VS0: ビジョン策定・戦略立案 → vs0-vision-strategy/
- VS2: 製品開発・イノベーション → vs2-product-innovation/
- VS2: 研究開発・技術革新 → vs2-research-development/  # 別プロジェクト
```

**プロジェクト固有のマッピング**:
- コマンド実行時に `parasol.yaml` と `value-streams-mapping.md` を参照
- プロジェクトごとに適切なディレクトリ名を自動決定

## コングロマリット（事業部軸パターン）でのCL分解

> ⚠️ **重要**: Phase 1でコングロマリットと判定された場合、Phase 2で事業部軸パターンが選択されています。
> CL分解も事業部ごとに独立して実施してください。

### 事業部軸でのCL1設計原則

```
┌─────────────────────────────────────────────────────────────────────┐
│  コングロマリット CL1 設計                                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【各事業部のCL1は独立して定義】                                     │
│                                                                     │
│  事業部A VStr (VS0-VS7)                                             │
│  └─ CL1: Core（事業A固有）/ Supporting（事業A支援）                 │
│                                                                     │
│  事業部B VStr (VS0-VS7)                                             │
│  └─ CL1: Core（事業B固有）/ Supporting（事業B支援）                 │
│                                                                     │
│  【事業横断の共通機能は別レイヤー】                                  │
│                                                                     │
│  Supporting Layer（全事業支援）                                      │
│  └─ 共通R&D、品質保証基盤、物流基盤                                 │
│                                                                     │
│  Generic Layer（全社共通）                                           │
│  └─ 統合調達、顧客データ基盤、ブランド資産、認証/監査               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### シナジー関連ケイパビリティの配置

| 種類 | 例 | 配置先 | 理由 |
|------|-----|--------|------|
| クロスセル分析 | 顧客購買傾向分析 | Supporting Layer | 事業横断だが差別化要因ではない |
| 共通顧客基盤 | 統合CRM | Generic Layer | 全事業で標準化可能 |
| 共通研究基盤 | 基礎研究プラットフォーム | Supporting Layer | 事業横断の支援機能 |
| 事業固有の製造 | 酒類製造、飲料製造 | 各事業のCore | 差別化要因 |

**重要**: シナジー関連のケイパビリティを「シナジーBC」として定義してはいけません。
詳細: `_patterns/_axes/business-unit-axis.md`（コングロマリット設計原則）

---

## Phase 3a: CL1 - Domain Classification

### コマンド

```bash
/parasol:3-capabilities cl1
```

### 実行フロー

**ステップ1**: Phase 2の成果物を確認
- value-streams-mapping.md から VS0-VS7 を読み込み
- enterprise-activities.md からエンタープライズ活動を把握

**ステップ2**: 🤖 zen-architect サブエージェントに委譲

```
Task tool を使用して zen-architect (ANALYZE mode) を起動：

プロンプト:
"""
Parasol V5 - Phase 3a: Domain Classification (CL1)

## タスク
outputs/2-value/ の成果物を分析し、ドメインをCore/Supporting/Genericに分類してください。

## 入力
- value-streams-mapping.md: VS0-VS7の定義
- enterprise-activities.md: エンタープライズ活動
- organization-analysis.md: 組織の戦略方向性

## 分析観点

### Core Domain（競争優位の源泉）
- 戦略的重要性: 高
- 競争優位性: 高
- 複雑度: 高
- カスタマイズ必要性: 高
- 推奨投資配分: 70%

### Supporting Domain（ビジネス支援）
- 戦略的重要性: 中
- 競争優位性: 低
- 複雑度: 中
- カスタマイズ必要性: 中
- 推奨投資配分: 20%

### Generic Domain（汎用機能）
- 戦略的重要性: 低
- 競争優位性: なし
- 複雑度: 低
- カスタマイズ必要性: 低
- 推奨投資配分: 10%（外部サービス購入推奨）

## 出力形式
outputs/3-capabilities/{vs-dir}/cl1-domain-classification.md

※ {vs-dir} はPhase 2のVS定義から動的に決定（例: vs2-product-innovation/）

テンプレート構造：
1. ドメイン分類サマリー（Core/Supporting/Generic各リスト）
2. 各活動領域の詳細
- 活動領域名
- 説明
- 戦略的重要性 / 競争優位性 / 複雑度
- 分類理由
3. 投資配分推奨
4. 次のステップ（CL2: サブドメイン設計）
"""
```

**ステップ3**: zen-architectの出力を確認し、cl1-domain-classification.md を生成

**ステップ4**: 結果レポート
```
✅ CL1: Domain Classification ({vs-number}: {vs-name}) 完了

分類結果:
- Core Activities: X 個
- Supporting Activities: X 個
- Generic Activities: X 個

成果物: outputs/3-capabilities/{vs-dir}/cl1-domain-classification.md

次のステップ:
→ `/parasol:3-capabilities cl2 {vs-number}` でサブドメイン設計
```

### テンプレート: strategic-classification.md

```markdown
# Strategic Domain Classification (CL1)

プロジェクト: {プロジェクト名}
作成日: {日付}

## ドメイン分類サマリー

### Core Domains（競争優位の源泉）
1. **product-catalog**: 製品情報キュレーションの中核
2. **order-orchestration**: 注文処理の中核
3. **customer-insights**: 顧客理解と体験最適化

### Supporting Domains（ビジネス支援）
1. **inventory-optimization**: 在庫最適化
2. **payment-processing**: 決済処理
3. **customer-service**: カスタマーサービス
4. **analytics**: 分析とレポーティング

### Generic Domains（汎用機能）
1. **notification**: 通知配信
2. **authentication**: 認証・認可

## 詳細分析

### Core Domain: product-catalog

**説明**: 製品情報のキュレーション、カタログ構成、価格設定の中核機能

**関連Value Stream**:
- VS2: 製品開発

**評価**:
- 戦略的重要性: ★★★★★ (5/5)
- 競争優位性: ★★★★★ (5/5)
- 複雑度: ★★★★☆ (4/5)
- カスタマイズ必要性: ★★★★★ (5/5)

**分類理由**:
製品カタログの独自性と柔軟性が競争優位を生む。業界特有の製品分類、動的価格設定、在庫連携などの複雑なビジネスルールを含む。既製品では対応困難。

**推奨アプローチ**: フルカスタム開発、最高品質の投資

---

### Core Domain: order-orchestration

**説明**: 注文受付から出荷までのオーダーライフサイクルオーケストレーション

**関連Value Stream**:
- VS4: 販売・流通

**評価**:
- 戦略的重要性: ★★★★★ (5/5)
- 競争優位性: ★★★★☆ (4/5)
- 複雑度: ★★★★★ (5/5)
- カスタマイズ必要性: ★★★★☆ (4/5)

**分類理由**:
独自の注文処理フロー、複数チャネル統合、リアルタイム在庫引当などが競争優位を生む。複雑な状態遷移とイベント駆動アーキテクチャが必要。

**推奨アプローチ**: フルカスタム開発、イベントソーシング検討

---

### Supporting Domain: inventory-optimization

**説明**: 在庫レベル最適化、入出庫処理、需要予測連携

**関連Value Stream**:
- VS2: 製品開発（在庫計画）
- VS4: 販売・流通（在庫引当）

**評価**:
- 戦略的重要性: ★★★☆☆ (3/5)
- 競争優位性: ★★☆☆☆ (2/5)
- 複雑度: ★★★☆☆ (3/5)
- カスタマイズ必要性: ★★★☆☆ (3/5)

**分類理由**:
重要だが競争優位の直接的源泉ではない。一部カスタマイズは必要だが、既製品をベースに拡張可能。

**推奨アプローチ**: 既製品 + カスタマイズ、または社内開発（中程度の投資）

---

### Generic Domain: notification

**説明**: Email、SMS、Pushなどの通知配信

**関連Value Stream**:
- 全VSに横断的に利用

**評価**:
- 戦略的重要性: ★★☆☆☆ (2/5)
- 競争優位性: ★☆☆☆☆ (1/5)
- 複雑度: ★★☆☆☆ (2/5)
- カスタマイズ必要性: ★☆☆☆☆ (1/5)

**分類理由**:
汎用的な機能で競争優位を生まない。成熟した外部サービス（SendGrid、Twilio、FCM等）が多数存在。

**推奨アプローチ**: 外部SaaS利用（SendGrid、Twilio等）

## 投資配分推奨

```
Core Domains (3個):      70% の投資
Supporting Domains (4個): 20% の投資
Generic Domains (2個):    10% の投資（主に統合コスト）

推奨配分:
- product-catalog: 30%
- order-management: 25%
- customer-insights: 15%
- Supporting全体: 20%
- Generic全体: 10%
```

## 戦略的推奨事項

1. **Core Domain集中投資**: product-catalogとorder-managementに最高品質のエンジニアを配置
2. **Supporting Domain効率化**: 既製品活用とカスタマイズのバランス
3. **Generic Domain外注**: 通知・認証は外部SaaS利用で迅速に立ち上げ
4. **技術的負債回避**: Core Domainでの技術的負債は競争力を直接損なうため、品質を優先

## 次のステップ

CL2: サブドメイン設計

各Value Streamをサブドメイン（≈マイクロサービス候補）に分解：

```bash
# Core Domain のVSから開始（優先度高）
/parasol:3-capabilities cl2 VS2    # 製品開発・イノベーション
/parasol:3-capabilities cl2 VS3    # ブランディング・マーケティング
/parasol:3-capabilities cl2 VS4    # 販売・流通・サプライチェーン

# Supporting Domain のVS
/parasol:3-capabilities cl2 VS1    # 市場機会発見
/parasol:3-capabilities cl2 VS5    # カスタマーサポート
/parasol:3-capabilities cl2 VS6    # データ活用・DX
/parasol:3-capabilities cl2 VS7    # 業務改善

# Generic Domain のVS
/parasol:3-capabilities cl2 VS0    # ビジョン策定・戦略立案
```
```


## Phase 3b: CL2 - Subdomain Design

### コマンド

```bash
/parasol:3-capabilities cl2              # インタラクティブ選択（VS一覧から選択）
/parasol:3-capabilities cl2 VS2          # VS2（製品開発）を直接指定
/parasol:3-capabilities cl2 VS3          # VS3（ブランディング）を直接指定
/parasol:3-capabilities cl2 VS4          # VS4（販売・流通）を直接指定
```

### 実行フロー

**ステップ1**: Value Stream選択
- パラメータなし → インタラクティブ選択（詳細化済みVSの一覧から選択）
- パラメータあり（VS番号）→ 直接実行

**ステップ2**: Phase 2の成果物を確認
- vs{N}-detail.md から該当VSの詳細定義を取得
- strategic-classification.md からドメインタイプ（Core/Supporting/Generic）を確認

**ステップ3**: 🤖 zen-architect サブエージェントに委譲

```
Task tool を使用して zen-architect (ARCHITECT mode) を起動：

プロンプト:
"""
Parasol V5 - Phase 3b: Subdomain Design (CL2)

## タスク
Value Stream {vs-number}（{vs-name}）をサブドメイン（ビジネスオペレーション群）に分解してください。
各サブドメインは関連するビジネスオペレーションの集合であり、将来のマイクロサービス候補となります。

## 入力
- vs{N}-detail.md: 該当VSの詳細定義（価値の流れ、活動、KPI等）
- strategic-classification.md: ドメイン分類結果（このVSのドメインタイプ確認用）
- value-streams-mapping.md: 全体のValue Streams概要
- enterprise-activities.md: ビジネス活動

## 対象Value Stream
{vs-detail.mdの内容を提示}

例（VS2: 製品開発・イノベーション の場合）:
- 基盤技術研究（酵母、発酵、乳酸菌）
- 製品コンセプト開発
- 酒類製品開発
- 飲料・食品開発

## 分解観点

### サブドメイン = ビジネスオペレーション群
サブドメインは、関連するビジネスオペレーション（業務活動）をグループ化したものです。
以下の観点から各ドメインをサブドメインに分解：

1. **業務の関連性**: 関連するビジネスオペレーションがまとまっているか
2. **責務の凝集性**: 単一の明確な責務を持つか
3. **変更の独立性**: 他と独立して変更できるか
4. **チーム配置**: 独立したチームで開発・運用可能か
5. **データ境界**: 独自のデータストアを持つべきか
6. **スケーリング要件**: 独立したスケーリングが必要か

### サブドメイン定義に含める情報
- サブドメイン名（kebab-case）
- 目的と責務
- **ビジネスオペレーション一覧**（このサブドメインで実行する業務活動）
- 関連するValue Streams
- データ所有範囲
- 他サブドメインとの依存関係
- マイクロサービス候補としての評価

## 出力形式
outputs/3-capabilities/{vs-dir}/cl2-subdomain-design.md

※ {vs-dir} はPhase 2のVS定義から動的に決定

テンプレート構造：
1. Value Stream概要（名前、ドメインタイプ、目的）
2. サブドメイン一覧
3. 各サブドメインの詳細定義
4. サブドメイン間の関係図
5. マイクロサービス境界の推奨
6. 次のステップ（CL3: BC定義）

## 制約
- サブドメイン名は kebab-case で統一
- 各サブドメインは1つの明確な責務を持つ
- サブドメイン数はVSの複雑度に応じて（Core VS: 4-6個、Supporting VS: 2-4個、Generic VS: 1-3個を目安）
"""
```

**ステップ4**: zen-architectの出力を確認し、cl2-subdomain-design.md を生成

**ステップ5**: 結果レポート
```
✅ CL2: Subdomain Design ({vs-number}: {vs-name}) 完了

ドメインタイプ: {Core/Supporting/Generic} Domain

サブドメイン:
- {subdomain-1}: {説明}
- {subdomain-2}: {説明}
... (合計 X 個)

成果物: outputs/3-capabilities/{vs-dir}/cl2-subdomain-design.md

次のステップ:
→ `/parasol:3-capabilities cl3 {subdomain-name}` で各サブドメインのBC定義
```

### テンプレート: vs{N}-subdomains.md

```markdown
# VS{N}: {VS名} - Subdomain Design (CL2)

プロジェクト: {プロジェクト名}
Value Stream: VS{N} - {VS名}
ドメインタイプ: {Core/Supporting/Generic} Domain
作成日: {日付}

## Value Stream 概要

**目的**: {VSの目的}

**価値の流れ（Phase 2より）**:
- A1: {活動1}
- A2: {活動2}
- ...

---

## サブドメイン一覧

### 1. vs{N}-{subdomain-name-1}
**目的**: {サブドメインの目的}

### 2. vs{N}-{subdomain-name-2}
**目的**: {サブドメインの目的}

### 3. vs{N}-{subdomain-name-3}
**目的**: {サブドメインの目的}

---

## サブドメイン詳細

### 1. vs{N}-{subdomain-name-1}

**目的**: {詳細な目的}

**ビジネスオペレーション一覧**:
このサブドメインで実行する業務活動：
- {オペレーション1}: {説明}
- {オペレーション2}: {説明}
- {オペレーション3}: {説明}

**対応する活動（Phase 2のValue Flowより）**:
- A{X}: {活動名}

**データ所有範囲**:
- {テーブル/データストア1}
- {テーブル/データストア2}

**他サブドメインとの依存関係**:
- {依存サブドメイン1}: {関係の説明}
- {依存サブドメイン2}: {関係の説明}

**マイクロサービス候補評価**:
- 独立性: {高/中/低}（{理由}）
- スケーラビリティ: {高/中/低}（{理由}）
- チーム境界: {明確/曖昧}
- データ境界: {明確/曖昧}

**推奨**: {独立マイクロサービス化 / モジュラーモノリス / 既存統合} ★★★★★

---

## サブドメイン関係図

```
{ASCIIアートでサブドメイン間の依存関係を図示}
```

## マイクロサービス境界の推奨

### このVS内での優先順位

1. **vs{N}-{subdomain-1}**: {理由}
2. **vs{N}-{subdomain-2}**: {理由}
3. **vs{N}-{subdomain-3}**: {理由}

### 他VSとの統合ポイント

- VS{X}の{subdomain}: {統合理由と方式}
- VS{Y}の{subdomain}: {統合理由と方式}

## 次のステップ

CL3: Bounded Context 定義

このVSのサブドメインのBounded Contextを定義：

```bash
# VS{N}のサブドメインから
/parasol:3-capabilities cl3 vs{N}-{subdomain-1}
/parasol:3-capabilities cl3 vs{N}-{subdomain-2}
/parasol:3-capabilities cl3 vs{N}-{subdomain-3}
```

**重要**: BC定義ではユビキタス言語、集約、エンティティ、値オブジェクトを明確化します。
```


## Phase 3c: CL3 - Business Operations Definition（業務オペレーション定義）

### コマンド

```bash
/parasol:3-capabilities cl3                      # インタラクティブ選択
/parasol:3-capabilities cl3 fermentation-research # 直接指定
```

### 実行フロー

**ステップ1**: ケイパビリティ選択
- パラメータなし → 全ケイパビリティリストからインタラクティブ選択
- パラメータあり → 直接実行

**ステップ2**: CL2の成果物を確認
- 該当するケイパビリティ定義を cl2-subdomain-design.md から読み込み

**ステップ3**: 🤖 zen-architect サブエージェントに委譲

```
Task tool を使用して zen-architect (ARCHITECT mode) を起動：

プロンプト:
"""
Parasol V5 - Phase 3c: Business Operations Definition (CL3)

## タスク
ケイパビリティ "{capability-name}" の業務オペレーションを定義してください。
業務オペレーションは**業務担当者・ドメインエキスパート向け**の具体的な業務活動定義です。

## 入力
- cl2-subdomain-design.md: 該当VSのケイパビリティ定義
- vs{N}-detail.md: Value Streamの詳細定義
- cl1-domain-classification.md: ドメイン分類

## 業務オペレーション定義要素

### 1. ケイパビリティ概要
- ケイパビリティ名
- 目的と責務
- 担当チーム・担当者

### 2. 業務オペレーション一覧
このケイパビリティで実行する業務活動：
- **オペレーションID**: OP-{3letter}-{number} 形式
- **オペレーション名**: 日本語での業務名
- **トリガー**: 何がこの業務を開始するか
- **活動内容**: 具体的な作業ステップ
- **成果物**: この業務で生成されるもの
- **業務ルール**: 守るべきルール・制約

### 3. 業務フロー
オペレーション間の関係と流れ：
- 前後関係（どの業務の後に実行されるか）
- 並行実行可能な業務
- 条件分岐

### 4. 業務用語（ユビキタス言語の種）
このケイパビリティで使用する主要な業務用語：
- ドメインオブジェクト（業務で扱うモノ・コト）
- 業務ルール用語
- 状態遷移用語

### 5. 取扱データ
このケイパビリティが扱うデータ：
- マスタデータ
- トランザクションデータ
- 参照データ

## 出力形式
outputs/3-capabilities/{vs-dir}/cl3-business-operations/{capability-name}-operations.md

※ {vs-dir} はPhase 2のVS定義から動的に決定

テンプレート構造：
1. ケイパビリティ概要
2. 業務オペレーション一覧（ID、名前、トリガー、成果物）
3. 各オペレーションの詳細
4. 業務フロー図
5. 業務用語集
6. 取扱データ一覧
7. 次のステップ（BC: 実装設計）

## 制約
- オペレーションIDは OP-{3letter}-{number} 形式
- 粒度は 1日〜1週間で完結する業務単位
- 技術用語は使わない（業務担当者向け）

"""
```

**ステップ4**: zen-architectの出力を確認し、{capability-name}-operations.md を生成

**ステップ5**: 結果レポート
```
✅ CL3: Business Operations Definition ({capability-name}) 完了

定義内容:
- 業務オペレーション: X個
- 業務用語: X個
- 取扱データ: X種類

成果物:
outputs/3-capabilities/{vs-dir}/cl3-business-operations/{capability-name}-operations.md

次のステップ:
1. 他のケイパビリティの業務オペレーション定義を完了
2. 全CL3完了後 → `/parasol:3-capabilities bc {capability-name}` で実装設計
```

### テンプレート: {capability-name}-operations.md

```markdown
# 業務オペレーション: fermentation-research

プロジェクト: {プロジェクト名}
ケイパビリティ: fermentation-research（発酵研究）
作成日: {日付}

## 1. ケイパビリティ概要

### 目的
酵母株の探索・育種・発酵条件最適化を通じて、製品開発を支援する基盤技術研究

### 担当チーム
**発酵研究チーム**: 5名
- 主任研究員: 1名
- 研究員: 3名
- 技術補助: 1名

## 2. 業務オペレーション一覧

| ID | オペレーション名 | トリガー | 成果物 |
|----|-----------------|---------|--------|
| OP-FER-001 | 酵母株探索・収集 | 研究計画確定 | 酵母サンプル |
| OP-FER-002 | 酵母株育種・改良 | 製品要件受領 | 改良酵母株 |
| OP-FER-003 | 発酵条件最適化 | 品質要件確定 | 最適条件データ |
| OP-FER-004 | 発酵試験実施 | 酵母株選定完了 | 試験結果レポート |

## 3. 各オペレーションの詳細

### OP-FER-001: 酵母株探索・収集

**トリガー**: 研究計画の確定

**活動内容**:
1. 候補酵母株のスクリーニング
2. 特性評価（発酵力、香味成分）
3. 有望株の選定・保存

**成果物**: 酵母サンプル、特性評価データ

**業務ルール**:
- 最低3株以上を候補として選定
- 食品安全基準への適合確認必須

---

### OP-FER-002: 酵母株育種・改良

**トリガー**: 製品要件の受領

**活動内容**:
1. 育種目標の設定
2. 交配・選抜
3. 特性確認試験

**成果物**: 改良酵母株、育種記録

**業務ルール**:
- 育種記録は全工程を詳細に記録
- 親株情報の完全なトレーサビリティ

---

## 4. 業務フロー図

```
研究計画確定
     │
     ▼
┌─────────────────┐
│ OP-FER-001     │
│ 酵母株探索・収集 │
└────────┬────────┘
         │
         ▼
製品要件受領 ─────────────┐
         │               │
         ▼               │
┌─────────────────┐      │
│ OP-FER-002     │      │
│ 酵母株育種・改良 │      │
└────────┬────────┘      │
         │               │
         ▼               ▼
┌─────────────────┐  ┌─────────────────┐
│ OP-FER-003     │  │ OP-FER-004     │
│ 発酵条件最適化  │  │ 発酵試験実施   │
└─────────────────┘  └─────────────────┘
```

## 5. 業務用語集

| 用語 | 定義 |
|------|------|
| 酵母株 | 発酵に使用する酵母の系統 |
| 育種 | 交配や選抜により優良な形質を持つ株を作出すること |
| 発酵力 | 酵母が糖を分解してアルコールを生成する能力 |
| 香味成分 | 発酵過程で生成される風味に影響する化合物 |

## 6. 取扱データ

### マスタデータ
- 酵母株マスタ（株ID、親株情報、特性）
- 評価基準マスタ（評価項目、基準値）

### トランザクションデータ
- 特性評価結果
- 育種記録
- 発酵試験データ

## 7. 次のステップ

実装設計（BC）への移行：
```bash
/parasol:3-capabilities bc fermentation-research
```
```


## Phase 3d: BC - Implementation Design（実装設計）

### コマンド

```bash
/parasol:3-capabilities bc                       # インタラクティブ選択
/parasol:3-capabilities bc fermentation-research # 直接指定
```

### 実行フロー

**ステップ1**: ケイパビリティ選択
- パラメータなし → CL3定義済みケイパビリティからインタラクティブ選択
- パラメータあり → 直接実行

**ステップ2**: CL3の成果物を確認
- 該当する業務オペレーション定義を {capability-name}-operations.md から読み込み

**ステップ3**: 🤖 zen-architect + api-contract-designer サブエージェントに委譲

```
Task tool を使用して zen-architect (ARCHITECT mode) を起動：

プロンプト:
"""
Parasol V5 - Phase 3d: Implementation Design (BC)

## タスク
ケイパビリティ "{capability-name}" の実装設計（Bounded Context）を定義してください。
実装設計は**開発者・アーキテクト向け**の技術設計文書です。

## 入力
- {capability-name}-operations.md: 業務オペレーション定義（CL3）
- cl2-subdomain-design.md: ケイパビリティ定義
- cl1-domain-classification.md: ドメイン分類

## 実装設計要素

### 1. Bounded Context 概要
- BC名（{capability-name}-bc）
- 目的と責務（技術観点）
- 担当チーム

### 2. ユビキタス言語（Ubiquitous Language）
CL3の業務用語を技術用語にマッピング：
- ドメインオブジェクト → エンティティ/値オブジェクト
- 業務ルール → 不変条件/ドメインサービス
- 業務イベント → ドメインイベント

### 3. 集約設計（Aggregates）
- 集約ルート（Aggregate Root）
- エンティティ（Entities）
- 値オブジェクト（Value Objects）
- 不変条件（Invariants）

### 4. ドメインイベント（Domain Events）
- イベント名
- ペイロード
- 発生タイミング

### 5. Context Map（他BCとの関係）
- Upstream/Downstream関係
- 統合パターン（Customer-Supplier, Partnership等）

### 6. API契約（概要）
- 提供API
- 依存API

### 7. 技術スタック推奨
- 言語・フレームワーク
- データベース
- メッセージング

## 出力形式
outputs/3-capabilities/{vs-dir}/bounded-contexts/{capability-name}-bc.md

テンプレート構造：
1. BC概要
2. ユビキタス言語
3. 集約設計
4. ドメインイベント
5. Context Map
6. API契約
7. 技術スタック
8. 次のステップ（Phase 4）

## 制約
- BC名は "{capability-name}-bc" 形式
- CL3の業務オペレーションとの対応を明記
- 技術用語と業務用語の対訳を含める
"""
```

**ステップ4**: 必要に応じて api-contract-designer を追加起動

```
Task tool を使用して api-contract-designer を起動：

プロンプト:
"""
{capability-name}-bc のAPI契約を詳細設計してください。

入力: {capability-name}-bc.md, {capability-name}-operations.md

出力:
- RESTful API仕様（主要エンドポイント）
- リクエスト/レスポンス形式
- エラーハンドリング
"""
```

**ステップ5**: zen-architect + api-contract-designer の出力を確認し、{capability-name}-bc.md を生成

**ステップ6**: 結果レポート
```
✅ BC: Implementation Design ({capability-name}-bc) 完了

定義内容:
- 集約: X個
- ドメインイベント: X個
- API: X個
- 関連BC: X個

成果物:
outputs/3-capabilities/{vs-dir}/bounded-contexts/{capability-name}-bc.md

次のステップ:
1. 他のケイパビリティのBC定義を完了
2. パラソルドメイン言語からコード生成 → `/parasol:domain-language generate`
3. 全BC完了後 → `/parasol:4-application-design` でContext Map統合
```

### テンプレート: {capability-name}-bc.md

```markdown
# Bounded Context: product-catalog-core-bc

プロジェクト: {プロジェクト名}
サブドメイン: product-catalog-core
作成日: {日付}

## 1. Bounded Context 概要

### 目的
製品マスタデータのキュレーションとカタログ構造の維持

### 責務
- 製品情報の登録・更新・削除
- カテゴリ階層の設計・維持
- 製品属性の定義・更新
- 製品メディア（画像・動画）のキュレーション
- 多言語対応

### チーム境界
**担当チーム**: Product Management Team
- プロダクトマネージャー: 1名
- バックエンドエンジニア: 2名
- フロントエンドエンジニア: 1名
- QAエンジニア: 1名

### ドメインタイプ
Core Domain（競争優位の源泉）

---

## 2. ユビキタス言語（Ubiquitous Language）

### 主要概念

**Product（製品）**
販売可能な商品アイテム。SKU単位で識別され、カテゴリに属する。

**Category（カテゴリ）**
製品を分類する階層構造。最大5階層まで。例: Electronics > Computers > Laptops > Gaming Laptops

**Attribute（属性）**
製品の特性を表す名前-値ペア。カテゴリごとに定義可能（例: Laptop カテゴリなら "CPU", "RAM", "Storage"）

**SKU (Stock Keeping Unit)**
在庫識別の最小単位。製品バリエーション（色・サイズ等）ごとに一意。

**ProductMedia（製品メディア）**
製品に紐づく画像・動画・3Dモデル等のメディアファイル。

**Catalog（カタログ）**
特定の目的でキュレートされた製品集合（例: "Summer Sale Catalog", "New Arrivals"）

### ビジネスルール

1. **製品は必ず1つ以上のカテゴリに属する**
2. **SKUはシステム全体で一意**
3. **カテゴリ階層は循環参照を許容しない**
4. **製品の削除は論理削除（soft delete）のみ**
5. **属性の型はカテゴリレベルで定義される**

### プロセス

**製品登録プロセス**
1. 製品基本情報入力
2. カテゴリ選択
3. 属性値設定（カテゴリに応じた属性）
4. SKU生成
5. メディア登録
6. 承認プロセス（必要に応じて）
7. 公開

**カテゴリ構造変更プロセス**
1. 変更計画作成
2. 影響範囲分析（配下の製品数）
3. 承認
4. 製品の再配置
5. 変更適用

---

## 3. 集約設計（Aggregates）

### Aggregate 1: Product（製品集約）

**集約ルート**: Product
**エンティティ**: ProductVariant（製品バリエーション）
**値オブジェクト**: 
- SKU
- Price（参照のみ、所有は pricing-bc）
- Dimensions（寸法: 幅・高さ・奥行・重量）
- ProductStatus（Draft/Active/Discontinued）

**不変条件（Invariants）**:
- 製品は必ず1つ以上のカテゴリに属する
- SKUはシステム全体で一意
- 少なくとも1つのProductVariantを持つ
- 公開状態（Active）の製品は必須属性が全て設定されている

**主要操作**:
```typescript
class Product {
// コマンド
create(name, categoryIds, attributes): Product
update(name?, categoryIds?, attributes?): void
addVariant(sku, options): ProductVariant
removeVariant(sku): void
publish(): void
discontinue(): void

// クエリ
getVariants(): ProductVariant[]
isPublishable(): boolean
}
```

---

### Aggregate 2: Category（カテゴリ集約）

**集約ルート**: Category
**エンティティ**: なし（単一エンティティ）
**値オブジェクト**:
- CategoryPath（階層パス: "/electronics/computers/laptops"）
- AttributeDefinition（属性定義: 名前・型・必須フラグ）

**不変条件（Invariants）**:
- カテゴリ階層に循環参照なし
- 最大階層深度は5
- 属性定義の型は一度設定したら変更不可（新規属性として追加）

**主要操作**:
```typescript
class Category {
// コマンド
create(name, parentId?): Category
rename(name): void
move(newParentId): void
addAttributeDefinition(name, type, required): void

// クエリ
getPath(): CategoryPath
getAttributeDefinitions(): AttributeDefinition[]
getChildren(): Category[]
getAncestors(): Category[]
}
```

---

### Aggregate 3: ProductMedia（製品メディア集約）

**集約ルート**: ProductMedia
**エンティティ**: なし
**値オブジェクト**:
- MediaUrl（メディアファイルのURL）
- MediaType（Image/Video/3DModel）
- MediaMetadata（解像度、ファイルサイズ等）

**不変条件（Invariants）**:
- メディアは必ず1つの製品に属する
- 表示順序は0以上のユニーク整数

**主要操作**:
```typescript
class ProductMedia {
// コマンド
upload(productId, file, type): ProductMedia
reorder(newPosition): void
delete(): void

// クエリ
getUrl(): string
getThumbnailUrl(): string
}
```

---

## 4. ドメインイベント（Domain Events）

### ProductCreated
```typescript
{
eventId: string
occurredAt: timestamp
productId: string
name: string
categoryIds: string[]
createdBy: string
}
```
**発生タイミング**: 製品が新規作成された時
**購読者**: search-bc（検索インデックス更新）, recommendation-bc（推奨モデル更新）

---

### ProductPublished
```typescript
{
eventId: string
occurredAt: timestamp
productId: string
publishedAt: timestamp
publishedBy: string
}
```
**発生タイミング**: 製品がDraftからActiveになった時
**購読者**: inventory-bc（在庫準備通知）, search-bc（公開インデックス追加）

---

### ProductUpdated
```typescript
{
eventId: string
occurredAt: timestamp
productId: string
changes: {field: string, oldValue: any, newValue: any}[]
updatedBy: string
}
```
**発生タイミング**: 製品情報が更新された時
**購読者**: pricing-bc（価格再計算）, search-bc（インデックス更新）

---

### CategoryRestructured
```typescript
{
eventId: string
occurredAt: timestamp
categoryId: string
oldParentId: string | null
newParentId: string | null
affectedProductIds: string[]
}
```
**発生タイミング**: カテゴリ階層が変更された時
**購読者**: search-bc（ファセット再構築）, analytics-bc（カテゴリ分析更新）

---

### ProductDiscontinued
```typescript
{
eventId: string
occurredAt: timestamp
productId: string
reason: string
discontinuedBy: string
}
```
**発生タイミング**: 製品が廃番になった時
**購読者**: inventory-bc（在庫処分計画）, order-bc（発注停止）

---

## 5. Context Map（他BCとの関係）

### Downstream BC（このBCがデータを提供）

**pricing-bc** (Customer-Supplier)
- 関係: Product Catalog が Upstream、Pricing が Downstream
- 提供データ: 製品ID、基本情報（名前・カテゴリ）
- パターン: Published Language（ProductDTO）
- イベント: ProductCreated, ProductUpdated

**inventory-bc** (Customer-Supplier)
- 関係: Product Catalog が Upstream、Inventory が Downstream
- 提供データ: 製品ID、SKU
- パターン: Published Language（ProductDTO）
- イベント: ProductPublished, ProductDiscontinued

**order-bc** (Customer-Supplier)
- 関係: Product Catalog が Upstream、Order が Downstream
- 提供データ: 製品情報（読み取り専用）
- パターン: Open Host Service（REST API）
- 同期API: GET /products/{id}

**search-bc** (Partnership)
- 関係: 相互依存（Product Catalog → イベント、Search → 検索API）
- 提供データ: 全製品情報（インデックス用）
- パターン: Partnership（緊密な連携）
- イベント: ProductCreated, ProductUpdated, ProductDiscontinued

### Upstream BC（このBCがデータを参照）

**authentication-bc** (Conformist)
- 関係: Authentication が Upstream、Product Catalog が Downstream
- 依存データ: ユーザーID、権限情報
- パターン: Conformist（認証標準に従う）
- 同期API: GET /users/{id}/permissions

### その他の関係

**recommendation-bc** (Published Language)
- 双方向だが疎結合
- Product Catalog → イベント（製品変更）
- Recommendation → 推奨結果（別途API）

---

## 6. API契約概要

### 提供API（Open Host Service）

**製品取得**
```
GET /api/v1/products/{productId}
Response: ProductDTO
```

**製品検索**
```
GET /api/v1/products?categoryId={id}&query={text}&page={n}
Response: PagedList<ProductSummaryDTO>
```

**カテゴリ階層取得**
```
GET /api/v1/categories
Response: CategoryTreeDTO
```

**製品作成**
```
POST /api/v1/products
Request: CreateProductCommand
Response: ProductDTO
```

### 依存API（他BCへの依存）

**認証・認可確認**
```
GET /api/v1/auth/permissions
→ authentication-bc
```

**在庫確認（オプショナル）**
```
GET /api/v1/inventory/stock/{sku}
→ inventory-bc（表示用のみ、所有はしない）
```

---

## 7. 技術スタック推奨

### バックエンド
- **言語**: TypeScript / Node.js
- **フレームワーク**: NestJS（DDD対応）
- **データベース**: PostgreSQL（製品マスタ）
- **キャッシュ**: Redis（読み取り負荷軽減）
- **イベントバス**: RabbitMQ / Kafka

### API
- **スタイル**: RESTful API
- **仕様**: OpenAPI 3.0
- **認証**: JWT（authentication-bc発行）
- **レート制限**: あり

### 監視・可観測性
- **ログ**: JSON構造化ログ
- **メトリクス**: Prometheus
- **トレーシング**: Jaeger

---

## 8. 次のステップ

### 即座の次のアクション

1. **他のサブドメインのBC定義**
```bash
/parasol:3-capabilities cl3 product-pricing
/parasol:3-capabilities cl3 order-management
# ... 全サブドメイン
```

### 全BC定義完了後

2. **Phase 4: Application Design - Context Map統合**
```bash
/parasol:4-application-design
```

Phase 4では：
- 全BCの関係を統合したContext Mapを作成
- サービス境界を確定
- 統合パターン（同期/非同期）を決定
- ADR（Architecture Decision Records）を作成
```


## エラーケース

### Phase 2 が完了していない

```
⚠️ Phase 2: Value Definition が完了していません

Value Streamsを先に定義してください:
→ `/parasol:2-value`

必要な成果物:
- value-streams-mapping.md (VS0-VS7)
- enterprise-activities.md
```

### CL1が完了していないのにCL2を実行

```
⚠️ CL1: Domain Classification が完了していません

先にドメイン分類を実行してください:
→ `/parasol:3-capabilities cl1`

必要な成果物:
- strategic-classification.md
```

### CL2が完了していないのにCL3を実行

```
⚠️ CL2: Subdomain Design が完了していません

先にサブドメイン設計を実行してください:
→ `/parasol:3-capabilities cl2`

必要な成果物:
- core-domain-subdomains.md
- supporting-domain-subdomains.md
- generic-domain-subdomains.md
```

### 無効なサブコマンド

```
❌ 無効なサブコマンド: xyz

有効なサブコマンド:
- cl1: Domain Classification (戦略的分類)
- cl2: Subdomain Design (サブドメイン設計)
- cl3: Bounded Context Definition (BC定義)

使用例:
→ `/parasol:3-capabilities cl1`
```

### 存在しないValue Stream指定（CL2）

```
❌ 無効なValue Stream指定: xyz

有効なValue Stream:
- VS0: ビジョン策定・戦略立案 (Generic)
- VS1: 市場機会発見 (Supporting)
- VS2: 製品開発・イノベーション (Core) ← 詳細化済み
- VS3: ブランディング (Core)
- ...

使用例:
→ `/parasol:3-capabilities cl2 VS2`

注意: 詳細化されていないVSは先にPhase 2で詳細化してください:
→ `/parasol:2-value VS3`
```

### 存在しないサブドメイン指定（CL3）

```
❌ サブドメイン "xyz" が見つかりません

定義済みサブドメイン一覧:
→ `/parasol:status phase3` で確認

または:
→ `/parasol:3-capabilities cl3` でインタラクティブ選択
```

## サブエージェント実行時の注意

### zen-architect が返すエラー

もしzen-architectが十分な情報がないと判断した場合：

```
⚠️ zen-architect からのフィードバック:

"Phase 2のValue Streams定義が不完全です。
特にVS2（製品開発）とVS4（販売・流通）の詳細が不足しています。

推奨アクション:
1. `/parasol:2-value VS2` でVS2を詳細化
2. `/parasol:2-value VS4` でVS4を詳細化
3. その後、再度 `/parasol:3-capabilities cl1` を実行"
```

→ この場合、zen-architectの推奨に従って前のPhaseを充実させてから再実行

### api-contract-designer が返すエラー

もしapi-contract-designerがBC定義が不十分と判断した場合：

```
⚠️ api-contract-designer からのフィードバック:

"Bounded Context定義の集約設計が不明確です。
特に Product 集約のライフサイクル遷移が未定義です。

推奨アクション:
1. zen-architectに Product のライフサイクル（Draft→Review→Published→Discontinued）を明確化するよう指示
2. その後、再度API契約設計を実行"
```

→ この場合、BC定義を補完してから再実行

## 進捗確認

Phase 3の進捗を確認：

```bash
/parasol:status phase3
```

出力例:
```
📊 Phase 3: Capabilities - 詳細ステータス

3a. Domain Classification (CL1)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ strategic-classification.md
Core Domains: VS2, VS3, VS4
Supporting Domains: VS1, VS5, VS6, VS7
Generic Domains: VS0

3b. Subdomain Design (CL2) - Value Stream別
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ vs2-subdomains.md (Core: 製品開発 - 4サブドメイン)
⏸️ vs3-subdomains.md (Core: ブランディング - 待機中)
⏸️ vs4-subdomains.md (Core: 販売・流通 - 待機中)
⏸️ vs0-subdomains.md (Generic: ビジョン策定 - 待機中)
... 他4個

完了: 1/8 VS (12.5%)

3c. Bounded Context Design (CL3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ vs2-fermentation-tech-bc.md (Core)
✅ vs2-product-development-bc.md (Core)
⏸️ vs2-quality-assurance-bc.md (待機中)
⏸️ vs2-packaging-innovation-bc.md (待機中)
... 他N個

完了: 2/4 BC (VS2のみ、50%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ステータス: 🔄 進行中
品質: 🟡 要継続（CL2とBC定義を完了させる必要あり）

次のアクション:
1. CL2の継続: `/parasol:3-capabilities cl2 VS3` (Core優先)
2. BC定義: `/parasol:3-capabilities cl3 vs2-quality-assurance`
3. 全BC完了後: `/parasol:4-application-design`

推奨順序:
優先: VS2, VS3, VS4 (Core Domain)
次: VS1, VS5, VS6, VS7 (Supporting Domain)
最後: VS0 (Generic Domain)
```

## バリデーション

Phase 3 完了後、検証を実行：

```bash
/parasol:validate phase3
```

検証項目:
- ✅ CL1: 全VS（VS0-VS7）のドメイン分類済み
- ✅ CL2: 詳細化済みVSのサブドメイン定義完了
- ✅ CL3: 全サブドメインのBC定義完了
- ✅ 命名規則: vs{N}-{name} 形式、kebab-case遵守
- ✅ トレーサビリティ: VS詳細 → Subdomain → BC の紐付き確認

## MS3マイルストーン設定（戦術設計完了）

### MS3_Tactical_Design_Milestone

```yaml
MS3_Tactical_Design_Milestone:
  target_completion: "Phase 3完了から4週間"
  success_criteria:
    domain_decomposition: "全VSのサブドメイン分解完了"
    bc_definition_quality: "95%以上のBC定義が実装可能レベル"
    context_mapping: "BC間の統合パターン明確化"
    technical_readiness: "Phase 4実装設計への準備完了"
  
  deliverables:
    - strategic-classification.md (CL1)
    - vs{N}-subdomains.md × 8 (CL2)
    - {subdomain}-bc.md × 全サブドメイン (CL3)
    - ms3-completion-report.md
    - tactical-design-validation.md
  
  measurement_framework:
    bc_completeness: "定義済みBC数 / 必要BC数"
    implementation_readiness: "実装可能なBC割合"
    integration_clarity: "Context Map関係定義率"
  
  progression_requirements_to_ms4:
    architectural_decisions: "主要アーキテクチャ判断の文書化"
    service_boundaries: "マイクロサービス境界の確定"
    integration_patterns: "同期/非同期統合パターン選択"
    technology_stack: "技術スタック選定完了"
```

### MS3成果物

Phase 3.2で以下を作成：

| ファイル | 目的 | MS4への影響 |
|---------|------|-------------|
| **ms3-completion-report.md** | MS3達成状況 | Phase 4開始条件 |
| **tactical-design-validation.md** | 戦術設計の品質評価 | 実装設計品質保証 |
| **context-mapping-summary.md** | BC間統合パターン総括 | アーキテクチャ設計指針 |

### 価値トレーサビリティ（MS3レベル）

```yaml
Value_Traceability_MS3:
  source_validation: "全BCがVL2/VL3価値要素に対応"
  capability_alignment: "戦略ケイパビリティとBC設計の整合"
  implementation_readiness: "価値実現に向けた実装準備度"
  
  anti_imagination_controls:
    - "技術設計の価値根拠明示"
    - "BCライフサイクルの価値寄与測定"
    - "戦術設計の価値影響評価"
```

## 次のステップ

Phase 3 (全CL完了) 後:

```bash
# Phase 4: Application Design へ進む
/parasol:4-application-design
```

Phase 4では:
- 全BCを統合したContext Mapを作成
- サービス境界を確定（マイクロサービス構成）
- 統合パターンを決定（同期/非同期、API/イベント）
- Architecture Decision Records (ADR) を作成
- MS4マイルストーン設定（運用設計完了）

## 関連コマンド

- `/parasol:2-value` - Phase 2: Value Definition（前提条件）
- `/parasol:4-application-design` - Phase 4: Application Design（次のステップ）
- `/parasol:status phase3` - Phase 3 の詳細進捗確認
- `/parasol:validate phase3` - Phase 3 の検証
- `/parasol:0-help concepts` - 主要概念の詳細説明

## 参考資料

### DDD戦略的設計
- Eric Evans "Domain-Driven Design"
- Vaughn Vernon "Implementing Domain-Driven Design"

### Context Mapping パターン
- Customer-Supplier: 上流・下流の明確な関係
- Partnership: 相互依存の緊密な関係
- Published Language: 標準化されたデータ形式
- Open Host Service: 公開API提供
- Conformist: 上流に従う
- Anticorruption Layer: 翻訳層で分離

### マイクロサービス設計
- Sam Newman "Building Microservices"
- Chris Richardson "Microservices Patterns"
