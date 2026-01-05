# parasol:necessity-check - 構造的必然性検証コマンド

## 概要

すべての設計決定と実装が構造的必然性を持つことを検証します。価値から導かれない恣意的な設計や、論理的根拠のない実装を検出し、プロジェクトの構造的健全性を保証します。

## コマンド構文

```bash
amplifier parasol:necessity-check [対象] [オプション]
```

## 基本使用法

### プロジェクト全体の検証

```bash
# 標準チェック
amplifier parasol:necessity-check

# 詳細な深層チェック
amplifier parasol:necessity-check --deep

# 自動修正モード
amplifier parasol:necessity-check --fix
```

### 特定コンポーネントの検証

```bash
# 単一コンポーネント
amplifier parasol:necessity-check --component user-service

# 複数コンポーネント
amplifier parasol:necessity-check --components auth,payment,notification

# パターンマッチング
amplifier parasol:necessity-check --pattern "*-service"
```

## 検証レベル

### Level 1: 基本検証（デフォルト）

```bash
amplifier parasol:necessity-check --level basic
```

**検証項目:**
- 価値トレースとの関連付け
- 基本的な論理構造
- 明らかな矛盾の検出

### Level 2: 標準検証

```bash
amplifier parasol:necessity-check --level standard
```

**検証項目:**
- Level 1のすべて
- 設計パターンの妥当性
- 依存関係の必然性
- 複雑性の正当化

### Level 3: 厳格検証

```bash
amplifier parasol:necessity-check --level strict
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
amplifier parasol:necessity-check --fix --interactive

# 自動修正（安全な修正のみ）
amplifier parasol:necessity-check --fix --safe

# 積極的な自動修正
amplifier parasol:necessity-check --fix --aggressive
```

### 修正可能な問題

1. **価値の関連付け欠落**
   - AIが価値を推論して提案
   - 既存の価値トレースと自動マッチング

2. **過剰な複雑性**
   - 不要な層の除去提案
   - シンプルなパターンへの置換

3. **論理的矛盾**
   - 矛盾する要件の調整
   - 依存関係の整理

## レポート機能

### 標準レポート

```bash
# コンソール出力
amplifier parasol:necessity-check --report

# HTML形式で出力
amplifier parasol:necessity-check --report --format html --output necessity-report.html
```

### 詳細分析レポート

```bash
# 問題の根本原因分析を含む
amplifier parasol:necessity-check --analyze --report-detail high

# 修正提案付きレポート
amplifier parasol:necessity-check --suggest-fixes --output fixes.md
```

### メトリクスダッシュボード

```bash
# 必然性スコアの表示
amplifier parasol:necessity-check --metrics

# 継続的モニタリング
amplifier parasol:necessity-check --monitor --interval 1h
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

### カスタムルールの適用

```bash
# カスタムルールを使用
amplifier parasol:necessity-check --rules .parasol/necessity-rules.yaml

# 特定のルールのみ適用
amplifier parasol:necessity-check --only-rules no-util-packages,max-indirection

# ルールを除外
amplifier parasol:necessity-check --exclude-rules justify-patterns
```

## 統合機能

### CI/CDパイプライン統合

```yaml
# .github/workflows/necessity-check.yml
- name: Structural Necessity Check
  run: |
    amplifier parasol:necessity-check --level strict --fail-on warning
    amplifier parasol:necessity-check --metrics >> $GITHUB_STEP_SUMMARY
```

### pre-commitフック

```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: necessity-check
      name: Check Structural Necessity
      entry: amplifier parasol:necessity-check --staged-only
      language: system
      pass_filenames: false
```

### IDEプラグイン連携

```json
// .vscode/settings.json
{
  "parasol.necessity-check": {
    "enabled": true,
    "level": "standard",
    "autoFix": true,
    "showInlineHints": true
  }
}
```

## 高度な使用法

### 比較分析

```bash
# ブランチ間の必然性比較
amplifier parasol:necessity-check --compare main..feature/new-auth

# 時系列での必然性推移
amplifier parasol:necessity-check --timeline --days 30
```

### What-if分析

```bash
# 変更による必然性への影響を予測
amplifier parasol:necessity-check --what-if remove-component:legacy-api

# リファクタリングのシミュレーション
amplifier parasol:necessity-check --simulate refactor:monolith-to-micro
```

## トラブルシューティング

### よくある問題と解決法

#### 1. 過剰な警告

```bash
# ベースラインの設定
amplifier parasol:necessity-check --create-baseline

# ベースライン以降の問題のみ表示
amplifier parasol:necessity-check --since-baseline
```

#### 2. 誤検知

```bash
# 特定の警告を抑制
amplifier parasol:necessity-check --suppress NESS-001,NESS-002

# 抑制ルールの管理
amplifier parasol:necessity-check --manage-suppressions
```

#### 3. パフォーマンス問題

```bash
# 増分チェック
amplifier parasol:necessity-check --incremental

# キャッシュの使用
amplifier parasol:necessity-check --use-cache

# 並列実行
amplifier parasol:necessity-check --parallel --workers 4
```

## ベストプラクティス

### 1. 段階的導入

```bash
# Step 1: 警告のみ（ブロックしない）
amplifier parasol:necessity-check --warn-only

# Step 2: 新規コードのみチェック
amplifier parasol:necessity-check --new-code-only

# Step 3: 全体適用
amplifier parasol:necessity-check --level strict
```

### 2. チーム教育

```bash
# 学習モード（詳細な説明付き）
amplifier parasol:necessity-check --educational

# チームレポートの生成
amplifier parasol:necessity-check --team-report --format pdf
```

### 3. 継続的改善

```bash
# 月次分析
amplifier parasol:necessity-check --monthly-analysis

# 改善トレンドの可視化
amplifier parasol:necessity-check --trend-chart --output trend.png
```

## 次のステップ

構造的必然性を確保したら：

```bash
# 想像の設計を検出・除去
amplifier parasol:imagination-detect

# マイルストーンへ進行
amplifier parasol:milestone advance
```