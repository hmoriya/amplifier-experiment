# Amplifier-Parasol DDD 統合フレームワーク

## 概要

このフレームワークは、パラソルV4の体系的な価値駆動開発とAmplifierのDDD（Document-Driven Development）を完全に統合したものです。

### 🎯 統合の原理

```
価値（WHY） → 能力（WHAT） → 実装（HOW）
```

この流れを、AmplifierのDDDコマンドで直接実行可能にします。

## 📊 フェーズとDDDステップの対応

| パラソルV4フェーズ | Amplifier DDDステップ | 主な成果物 |
|-------------------|---------------------|-----------|
| **Phase 0: 準備** | `/ddd:prime` | コンテキスト設定、価値定義 |
| **Phase 1: 価値デザイン** | `/ddd:1-plan` (前半) | 価値宣言、価値分解 |
| **Phase 2: ビジネスデザイン** | `/ddd:1-plan` (後半) | ケーパビリティ、オペレーション |
| **Phase 3: アーキテクチャ** | `/ddd:2-docs` | 境界コンテキスト、API仕様 |
| **Phase 4: ソフトウェア設計** | `/ddd:3-code-plan` | ドメインモデル、詳細設計 |
| **Phase 5: 実装** | `/ddd:4-code` | ソースコード、テスト |
| **Phase 6: プラットフォーム** | `/ddd:5-finish` | デプロイ、運用設定 |

## 🚀 実行方法

### Step 1: プロジェクトコンテキストの設定

```bash
# コンテキストをロード
/ddd:prime 0-prime/execute.md
```

### Step 2: 価値とビジネスの計画

```bash
# 価値デザインとビジネスデザインを実行
/ddd:1-plan 1-plan/execute.md
```

### Step 3: アーキテクチャドキュメント生成

```bash
# 境界コンテキストとAPI仕様を生成
/ddd:2-docs 2-docs/execute.md
```

### Step 4: ソフトウェア設計の計画

```bash
# ドメインモデルと詳細設計を作成
/ddd:3-code-plan 3-code-plan/execute.md
```

### Step 5: コード実装

```bash
# 実際のコードを生成
/ddd:4-code 4-code/execute.md
```

### Step 6: デプロイと完了

```bash
# プラットフォーム設定とデプロイ
/ddd:5-finish 5-finish/execute.md
```

## 📁 ディレクトリ構造

```
amplifier-parasol-ddd/
├── 0-prime/          # コンテキスト設定
├── 1-plan/           # 価値・ビジネス計画
├── 2-docs/           # アーキテクチャ文書
├── 3-code-plan/      # ソフトウェア設計
├── 4-code/           # 実装コード
└── 5-finish/         # デプロイ・運用
```

## 🔄 WHAT-HOW ZIGZAG構造の実装

パラソルV4のZIGZAG構造を、AmplifierのDDDプロセスで実現：

```
CL1 WHAT（戦略ケーパビリティ）
    ↘️ HOW → /ddd:1-plan
CL2 WHAT（戦術ケーパビリティ）
    ↘️ HOW → /ddd:2-docs
CL3 WHAT（ビジネスオペレーション）
    ↘️ HOW → /ddd:3-code-plan
L4 WHAT（詳細ユースケース）
    ↘️ HOW → /ddd:4-code
```

## 🎯 パラソルドメイン言語の活用

3要素記法 `日本語名 [英語名] [SYSTEM_NAME]` を全フェーズで一貫使用：

- `顧客 [Customer] [CUSTOMER]`
- `注文 [Order] [ORDER]`
- `在庫 [Inventory] [INVENTORY]`

この記法により、ビジネス側と開発側の共通理解を実現します。

## 📝 各フェーズの実行可能MD

各ディレクトリの`execute.md`ファイルは、そのフェーズの全タスクを統合した実行可能なMarkdownです。

### execute.mdの構造

```markdown
# Phase X: [フェーズ名]

## 実行コンテキスト
- 前提条件
- 入力
- 出力

## タスク
1. タスク1
2. タスク2
...

## 検証
- チェックリスト

## 次のステップ
```

## 🔧 設定ファイル

### .ddd/config.yaml

```yaml
framework: parasol-v4
version: 1.0.0
integration: amplifier-ddd

phases:
  - prime: value-context
  - plan: value-business-design
  - docs: architecture-contracts
  - code-plan: software-design
  - code: implementation
  - finish: platform-deployment

execution:
  mode: sequential
  validation: enabled
  ai-assistance: enabled
```

## 📊 成果物の流れ

```
価値宣言
    ↓
価値グループ・マイルストーン
    ↓
ケーパビリティマトリクス（CL1→CL2→CL3）
    ↓
ビジネスオペレーション（5パターン）
    ↓
境界コンテキスト・ドメインモデル
    ↓
API仕様・UIコンポーネント
    ↓
実装コード（バックエンド・フロントエンド）
    ↓
デプロイメント・運用
```

## 🚀 今すぐ始める

```bash
# プロジェクト初期化
git clone <repository>
cd amplifier-parasol-ddd

# DDDコンテキストをロード
/ddd:prime 0-prime/execute.md

# 価値デザインから開始
/ddd:1-plan 1-plan/1-1-value-design/execute.md
```

---

**Amplifier-Parasol DDD** - 価値駆動開発を実行可能なプロセスとして実現