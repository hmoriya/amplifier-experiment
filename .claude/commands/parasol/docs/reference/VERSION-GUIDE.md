# Parasol バージョンガイド

Parasolには2つのバージョンがあります。プロジェクトの規模と目的に応じて選択してください。

---

## バージョン比較

| 項目 | V4（完全版） | V5（実用版） |
|------|-------------|-------------|
| **場所** | `/parasol/phases/` | `.claude/commands/parasol/` |
| **実行方法** | `/ddd:1-plan` + MDファイル | `/parasol:X-xxx` スラッシュコマンド |
| **所要時間** | 複数日〜週単位 | 数時間〜数日 |
| **フェーズ数** | 7フェーズ（Phase 0-6） | 8フェーズ（Phase 0-7） |
| **能力階層** | L1→L2→L3（戦略→戦術→運用） | CL1→CL2→CL3→BC（活動領域→ケイパビリティ→オペレーション→境界コンテキスト） |
| **成果物** | 詳細設計書、コード生成 | 実用設計書、実装ガイド |
| **適用規模** | 大規模エンタープライズ | 中小規模〜大規模対応 |

---

## Parasol V4（完全版）

### コンセプト

**「重厚長大な本格的DDDプロセス」**

エンタープライズ規模のシステム刷新に対応する、網羅的かつ体系的なアプローチ。
Amplifier DDDワークフローと統合し、各フェーズを厳密に実行します。

### フェーズ構成

```
Phase 0: プロジェクトコンテキスト
    ↓  組織分析、市場環境評価、制約条件の明確化
Phase 1: 価値定義
    ↓  Business Nine Dimensions + Five Pillarsフレームワーク
Phase 2: 能力設計
    ↓  L1戦略的能力 → L2戦術的能力 → L3運用的能力
Phase 3: ドメインモデリング
    ↓  Bounded Contexts、エンティティ、アグリゲート、ドメインイベント
Phase 4: オペレーション設計
    ↓  CRUD操作、ワークフロー、分析機能、コラボレーション
Phase 5: 実装生成
    ↓  コード自動生成、テストコード、API仕様、ドキュメント
Phase 6: 検証と最適化
       パフォーマンステスト、セキュリティ監査、ビジネス価値検証
```

### 能力階層（L1/L2/L3）

```
L1: 戦略的能力（Strategic Capabilities）
├── 組織全体の競争優位性を決定
├── 経営レベルの意思決定に直結
└── 例: デジタルイノベーション、顧客体験変革

L2: 戦術的能力（Tactical Capabilities）
├── L1を実現する具体的な能力
├── 部門レベルの実行計画
└── 例: オムニチャネル販売、データ駆動マーケティング

L3: 運用的能力（Operational Capabilities）
├── L2を支える日常的な業務能力
├── 実装レベルの詳細
└── 例: 在庫最適化、注文処理、顧客対応
```

### 使用方法

```bash
# DDDコンテキストをロード
/ddd:prime

# 各フェーズのMDファイルを実行
/ddd:1-plan parasol/phases/phase2-capability/2-1-strategic-capabilities.md
/ddd:2-docs
/ddd:3-code-plan
/ddd:4-code
/ddd:5-finish
```

### 適用シナリオ

- 大規模エンタープライズのDX推進
- 基幹システムのモダナイゼーション
- 複数年にわたる段階的移行プロジェクト
- 厳密なガバナンスが求められるプロジェクト

---

## Parasol V5（実用版）

### コンセプト

**「Claude Code統合型 Value Stream駆動アプローチ」**

Value Stream（価値の流れ）を起点に、ビジネス価値を素早く特定し、
Claude Codeとシームレスに統合された実用的プロセス。

### 🎯 V5特有機能

#### 設計ストーリー出力

V5では、価値分解やアーキテクチャ設計の各段階で**「なぜそう設計したか」**を自動出力します。

| フェーズ | 出力内容 |
|----------|----------|
| **Phase 2: 価値定義** | 価値分解の理由、MSバックキャスティングの論理、MS→VS変換の意図 |
| **Phase 3: ケーパビリティ** | ドメイン分類の理由、Phase 2からの継承関係、既存ケーパビリティ参照、重複回避の工夫 |
| **Phase 4: アーキテクチャ** | サービス境界決定の理由、統合パターン選択の根拠 |

**効果:**
- チーム全員の設計理解を促進
- 意思決定の根拠を記録
- プロジェクト固有の学習資産として蓄積

**参照:**
- 業種別設計ストーリー例: `parasol/patterns/value/industry-value-stream-patterns.md`
- 価値方法論の背景: `.claude/commands/parasol/_value-methodology.md`

### フェーズ構成

```
Phase 0: プロジェクト管理
    ↓  init, list, status, validate
Phase 1: コンテキスト
    ↓  企業分析、現状把握
Phase 2: 価値定義
    ↓  Value Stream（VS）の特定と優先順位付け
Phase 3: ケーパビリティ分解
    ↓  CL1活動領域（傾向的分類）→ CL2ケイパビリティ（正式分類）→ CL3（≈BizOp）
Phase 4: アーキテクチャ
    ↓  サービス境界、コンテキストマップ
Phase 5: ソフトウェア設計
    ↓  BC詳細設計、API設計
Phase 6: 実装
    ↓  コード骨格、実装ガイド
Phase 7: プラットフォーム
       インフラ設計、CI/CD、監視
```

### 能力階層（CL1/CL2/CL3/BC）

```
CL1: 活動領域識別（傾向的分類）
├── Value Streamを活動領域として識別
├── Core/Supporting/Genericの傾向を把握（参考情報）
├── ※この分類はCL2に継承されない
└── 例: 研究開発領域、マーケティング領域

CL2: ケイパビリティ設計（正式分類）
├── 各活動領域内のケイパビリティを特定
├── Core/Supporting/Genericの正式分類（投資判断の根拠）
├── ※CL1がGenericでもCL2で個別にCore判定可能
└── 例: 発酵技術研究(Core)、消費者分析(Supporting)

CL3: 詳細分解（≈Business Operation）
├── 各ケイパビリティの業務を詳細化
├── 分類なし（網羅性が目的）
└── 例: 酵母株スクリーニング、感性評価テスト

BC: Bounded Context
├── 実装単位の境界を定義
├── 親CL2の分類を継承
└── 例: fermentation-research-bc, ingredient-research-bc
```

### 使用方法

```bash
# プロジェクト作成
/parasol:0-project init my-project

# 各フェーズを順次実行
/parasol:1-context
/parasol:2-value
/parasol:3-capabilities
/parasol:4-architecture
/parasol:5-software
/parasol:6-implementation
/parasol:7-platform

# 進捗確認
/parasol:0-status
```

### 適用シナリオ

- Claude Code統合環境での開発
- Value Stream駆動設計プロジェクト
- アジャイル開発チームでの活用
- 設計根拠の記録が重要なプロジェクト
- 中小規模から大規模まで対応

---

## 選択ガイド

### V4を選ぶべき場合

- [ ] プロジェクト期間が6ヶ月以上
- [ ] 複数部門・複数チームが関与
- [ ] 厳密な設計ドキュメントが必要
- [ ] 既存システムとの統合が複雑
- [ ] ガバナンス・監査要件が厳しい

### V5を選ぶべき場合

- [ ] Claude Code環境での開発
- [ ] Value Stream起点での設計
- [ ] アジャイル・イテレーティブな開発
- [ ] 豊富な支援システムの活用
- [ ] 設計ストーリーの自動生成が必要

---

## 併用パターン

V4とV5は排他ではなく、併用も可能です：

### パターン1: V5で探索 → V4で本格化

```
1. V5で素早くPOC実施
2. 価値が確認できたらV4で本格設計
3. V4の成果物をV5で参照しながら実装
```

### パターン2: V4の特定フェーズをV5で補完

```
1. V4でPhase 0-2を実施（価値定義まで）
2. V5のCL1-CL3でケーパビリティを高速分解
3. V4のPhase 4-6で実装・検証
```

### パターン3: 並行開発

```
- チームA: V4で基幹システム刷新
- チームB: V5で新規サービス開発
- 共通: ケーパビリティ命名規則、ナレッジベースを共有
```

---

## ナビゲーション

### V4（完全版）

- [フェーズ概要](./phases/README.md)
- [Phase 2: 能力設計](./phases/phase2-capability/)
- [Phase 3: ドメインモデリング](./phases/phase3-domain/)

### V5（実用版）

- [ヘルプ](../.claude/commands/parasol/0-help.md)
- [ケーパビリティ命名ガイド](../.claude/commands/parasol/_capability-naming-guide.md)
- [ナレッジベース](../.claude/commands/parasol/_capability-knowledge/)

---

**更新履歴:**
- 2025-11-27: 初版作成（V4/V5の明確な区別）
