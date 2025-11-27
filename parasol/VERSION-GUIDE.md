# Parasol バージョンガイド

Parasolには2つのバージョンがあります。プロジェクトの規模と目的に応じて選択してください。

---

## バージョン比較

| 項目 | V4（完全版） | V5（軽量版） |
|------|-------------|-------------|
| **場所** | `/parasol/phases/` | `.claude/commands/parasol/` |
| **実行方法** | `/ddd:1-plan` + MDファイル | `/parasol:X-xxx` スラッシュコマンド |
| **所要時間** | 複数日〜週単位 | 数時間〜1日 |
| **フェーズ数** | 7フェーズ（Phase 0-6） | 8フェーズ（Phase 0-7） |
| **能力階層** | L1→L2→L3（戦略→戦術→運用） | CL1→CL2→CL3（ドメイン→サブドメイン→BC） |
| **成果物** | 詳細設計書、コード生成 | 軽量設計書、実装ガイド |
| **適用規模** | 大規模エンタープライズ | 中小規模〜POC |

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
    ↓  Nine Dimensions + Five Pillarsフレームワーク
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

## Parasol V5（軽量版）

### コンセプト

**「高速・実用的なValue Stream駆動アプローチ」**

Value Stream（価値の流れ）を起点に、ビジネス価値を素早く特定し、
アジャイルに設計・実装へ進むための軽量プロセス。

### 🎯 V5特有機能

#### 設計ストーリー出力

V5では、価値分解やアーキテクチャ設計の各段階で**「なぜそう設計したか」**を自動出力します。

| フェーズ | 出力内容 |
|----------|----------|
| **Phase 2: 価値定義** | 価値分解の理由、MSバックキャスティングの論理、MS→VS変換の意図 |
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
    ↓  CL1ドメイン分類 → CL2サブドメイン → CL3 Bounded Context
Phase 4: アーキテクチャ
    ↓  サービス境界、コンテキストマップ
Phase 5: ソフトウェア設計
    ↓  BC詳細設計、API設計
Phase 6: 実装
    ↓  コード骨格、実装ガイド
Phase 7: プラットフォーム
       インフラ設計、CI/CD、監視
```

### 能力階層（CL1/CL2/CL3）

```
CL1: ドメイン分類
├── Value Streamを「Core / Supporting / Generic」に分類
├── 投資優先度の決定
└── 例: VS2製品開発 → Core（差別化領域）

CL2: サブドメイン設計
├── 各ドメインを機能領域に分解
├── チーム境界の明確化
└── 例: 発酵研究、素材研究、製品開発...

CL3: Bounded Context定義
├── 実装単位の境界を定義
├── 集約ルート、エンティティ、イベント設計
└── 例: fermentation-research-bc, ingredient-research-bc...
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

- 新規サービス・プロダクトの立ち上げ
- POC（概念実証）プロジェクト
- アジャイル開発チームでの活用
- 短期間で成果を出す必要があるプロジェクト

---

## 選択ガイド

### V4を選ぶべき場合

- [ ] プロジェクト期間が6ヶ月以上
- [ ] 複数部門・複数チームが関与
- [ ] 厳密な設計ドキュメントが必要
- [ ] 既存システムとの統合が複雑
- [ ] ガバナンス・監査要件が厳しい

### V5を選ぶべき場合

- [ ] 素早く価値を検証したい
- [ ] スタートアップ的なスピード感が必要
- [ ] チーム規模が小〜中規模
- [ ] イテレーティブに改善していきたい
- [ ] Claude Codeで直接実行したい

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

### V5（軽量版）

- [ヘルプ](../.claude/commands/parasol/0-help.md)
- [ケーパビリティ命名ガイド](../.claude/commands/parasol/_capability-naming-guide.md)
- [ナレッジベース](../.claude/commands/parasol/_capability-knowledge/)

---

**更新履歴:**
- 2025-11-27: 初版作成（V4/V5の明確な区別）
