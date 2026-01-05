# Parasol V4 リファレンス

**バージョン**: V4（完全版）
**場所**: `/parasol/` (プロジェクトルート)

---

## 概要

Parasol V4は「重厚長大な本格的DDDプロセス」として、エンタープライズ規模のシステム刷新に対応する網羅的かつ体系的なアプローチです。

---

## V4 vs V5 比較

| 項目 | V4（完全版） | V5（実用版） |
|------|-------------|-------------|
| **場所** | `/parasol/` | `/.claude/commands/parasol/` |
| **実行方法** | `/ddd:1-plan` + MDファイル | `/parasol:X-xxx` スラッシュコマンド |
| **所要時間** | 複数日〜週単位 | 数時間〜数日 |
| **フェーズ数** | 7フェーズ（Phase 0-6） | 8フェーズ（Phase 0-7） |
| **能力階層** | L1→L2→L3（戦略→戦術→運用） | CL1→CL2→CL3 + BC境界確定 |
| **成果物** | 詳細設計書、コード生成 | 実用設計書、実装ガイド |
| **適用規模** | 大規模エンタープライズ | 中小規模〜大規模対応 |

---

## V4 フェーズ構成

```
Phase 0: プロジェクトコンテキスト
    ↓
Phase 1: 価値定義（Business Nine Dimensions + Five Pillars）
    ↓
Phase 2: 能力設計（L1戦略→L2戦術→L3運用）
    ↓
Phase 3: ドメインモデリング（BC、Entity、Aggregate）
    ↓
Phase 4: オペレーション設計（CRUD、Workflow）
    ↓
Phase 5: 実装生成（コード、テスト、API）
    ↓
Phase 6: 検証と最適化
```

---

## 各フェーズ詳細

### Phase 0: プロジェクトコンテキスト

- 組織分析、市場環境評価
- 既存システムアセスメント
- 制約条件の明確化

### Phase 1: 価値定義

- **Business Nine Dimensions**フレームワーク使用
- Nine Dimensions + Five Pillarsによる価値構造化
- ビジネス価値の明確化と具体化

### Phase 2: 能力設計

| レベル | 名称 | 説明 |
|--------|------|------|
| L1 | 戦略的能力 | Strategic Capabilities |
| L2 | 戦術的能力 | Tactical Capabilities |
| L3 | 運用的能力 | Operational Capabilities |

### Phase 3: ドメインモデリング

- 境界コンテキスト（Bounded Contexts）
- エンティティとアグリゲート
- ドメインイベント

### Phase 4: オペレーション設計

- CRUD操作定義
- ワークフロー設計
- 分析機能
- コラボレーション

### Phase 5: 実装生成

- コード自動生成
- テストコード生成
- API仕様生成
- ドキュメント生成

### Phase 6: 検証と最適化

- パフォーマンステスト
- セキュリティ監査
- ビジネス価値検証
- 継続的改善

---

## V4 ディレクトリ構造

```
/parasol/                         # V4ルート
├── phases/                       # フェーズ定義
│   ├── 01-value-analysis/
│   ├── 02-capability-design/
│   ├── 03-domain-modeling/
│   ├── 04-operation-design/
│   ├── 05-implementation/
│   ├── 06-validation/
│   └── README.md
├── commands/                     # V4コマンド
├── patterns/                     # 設計パターン
├── knowledge/                    # 知識ベース
├── bundles/                      # バンドル
├── contracts/                    # コントラクト
├── examples/                     # 例
└── value-definition/             # 価値定義
```

---

## V4 実行方法

### Amplifier DDD統合

```bash
# DDDコンテキストをロード
/ddd:prime

# 各フェーズの実行
/ddd:1-plan [フェーズのMDファイル]
/ddd:2-docs
/ddd:3-code-plan
/ddd:4-code
/ddd:5-finish
```

### フェーズ別実行例

```bash
# Phase 1: 価値分析
/parasol value-analysis "組織の中核価値とビジョンの構造化"

# Phase 2: 能力設計
/ddd:1-plan phase2-capability/2-1-strategic-capabilities.md

# Phase 3: ドメインモデリング
/ddd:1-plan phase3-domain/3-1-bounded-contexts.md
```

---

## V4を使うべきケース

- 大規模エンタープライズシステムの刷新
- 複数チームによる長期プロジェクト
- 詳細な設計ドキュメントが必要な場合
- コード自動生成まで含めた完全なワークフロー

---

## V5への移行

V4からV5への移行を検討する場合：

1. **既存成果物の活用**: V4で作成した価値定義、能力設計はV5でも活用可能
2. **フェーズのマッピング**: V4のL1-L3はV5のCL1-CL3に概念的に対応
3. **実行スタイルの変更**: MDファイル実行からスラッシュコマンドへ

---

## 関連リンク

- [V5 概要](../overview-v5.md)
- [VERSION-GUIDE](./VERSION-GUIDE.md)
- [V4 phases README](/parasol/phases/README.md)
