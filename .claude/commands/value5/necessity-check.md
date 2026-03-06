---
description: Structural necessity check (parasol5:value)
---

# parasol5:value:necessity-check - 構造的必然性検証コマンド

## 概要

すべての設計決定と実装が構造的必然性を持つことを検証します。価値から導かれない恣意的な設計や、論理的根拠のない実装を検出し、プロジェクトの構造的健全性を保証します。

## コマンド構文

```bash
amplifier parasol5:value:necessity-check [対象] [オプション]
```

## 基本使用法

### プロジェクト全体の検証

```bash
# 標準チェック
amplifier parasol5:value:necessity-check

# 詳細な深層チェック
amplifier parasol5:value:necessity-check --deep

# 自動修正モード
amplifier parasol5:value:necessity-check --fix
```

### 特定コンポーネントの検証

```bash
# 単一コンポーネント
amplifier parasol5:value:necessity-check --component user-service

# 複数コンポーネント
amplifier parasol5:value:necessity-check --components auth,payment,notification

# パターンマッチング
amplifier parasol5:value:necessity-check --pattern "*-service"
```

## 検証レベル

### Level 1: 基本検証（デフォルト）

```bash
amplifier parasol5:value:necessity-check --level basic
```

**検証項目:**
- 価値トレースとの関連付け
- 基本的な論理構造
- 明らかな矛盾の検出

### Level 2: 標準検証

```bash
amplifier parasol5:value:necessity-check --level standard
```

**検証項目:**
- Level 1のすべて
- 設計パターンの妥当性
- 依存関係の必然性
- 複雑性の正当化

### Level 3: 厳格検証

```bash
amplifier parasol5:value:necessity-check --level strict
```

**検証項目:**
- Level 2のすべて
- すべての設計決定の根拠
- 代替案の検討証跡
- 将来拡張性の必然性

## 検証カテゴリ

### 1. 価値駆動検証

```yaml
検証内容:
  - すべてのコンポーネントが価値に貢献しているか
  - 価値への貢献度が明確か
  - 価値の重複や矛盾がないか

検出例:
  - "このコンポーネントは価値トレースに関連付けられていません"
  - "複数の矛盾する価値に関連付けられています"
```

### 2. 論理的必然性検証

```yaml
検証内容:
  - 設計が論理的に導出されているか
  - 不必要な複雑性がないか
  - より単純な代替案が存在しないか

検出例:
  - "3層のインダイレクションは必然性がありません"
  - "このパターンはユースケースに対して過剰です"
```

### 3. 技術的必然性検証

```yaml
検証内容:
  - 技術選択が要件から必然的か
  - オーバーエンジニアリングがないか
  - 技術的負債の正当性

検出例:
  - "マイクロサービス化の必然性が証明されていません"
  - "このフレームワークの選択根拠が不明確です"
```

## 自動修正機能

### --fix オプション

```bash
# インタラクティブ修正
amplifier parasol5:value:necessity-check --fix --interactive

# 自動修正（安全な修正のみ）
amplifier parasol5:value:necessity-check --fix --safe

# 積極的な自動修正
amplifier parasol5:value:necessity-check --fix --aggressive
```

## カスタムルール

### ルール定義

```yaml
# .parasol/necessity-rules.yaml
rules:
  - id: no-util-packages
    description: "utilパッケージは必然性がない"
    severity: error
    pattern: "**/util/**"
    message: "明確な責務を持つパッケージに分割してください"

  - id: max-indirection
    description: "3層以上のインダイレクション禁止"
    severity: warning
    check: indirection-depth
    threshold: 3

  - id: justify-patterns
    description: "デザインパターンには正当化が必要"
    severity: error
    patterns: [factory, strategy, observer]
    require: justification-comment
```

## ベストプラクティス

### 1. 段階的導入

```bash
# Step 1: 警告のみ（ブロックしない）
amplifier parasol5:value:necessity-check --warn-only

# Step 2: 新規コードのみチェック
amplifier parasol5:value:necessity-check --new-code-only

# Step 3: 全体適用
amplifier parasol5:value:necessity-check --level strict
```

### 2. 継続的改善

```bash
# 月次分析
amplifier parasol5:value:necessity-check --monthly-analysis

# 改善トレンドの可視化
amplifier parasol5:value:necessity-check --trend-chart --output trend.png
```

## 次のステップ

構造的必然性を確保したら：

```bash
# 想像の設計を検出・除去
amplifier parasol5:value:imagination-detect

# マイルストーンへ進行
amplifier parasol5:milestone:status
```
