# parasol:value-trace - 価値トレース管理コマンド

## 概要

価値トレーサビリティシステムを活用して、プロジェクト全体の価値の流れを追跡・可視化・管理します。すべての設計判断と実装が価値にどう貢献するかを明確にし、構造的必然性を保証します。

## コマンド構文

```bash
amplifier parasol:value-trace <サブコマンド> [オプション]
```

## サブコマンド

### init - 価値トレースの初期化

新しいプロジェクトの価値トレーサビリティを初期化します。

```bash
amplifier parasol:value-trace init --project <project-name> [--from-url <url>] [--from-code <path>]
```

**オプション:**
- `--from-url <url>`: URLから価値を抽出して初期化
- `--from-code <path>`: 既存コードから価値を分析して初期化
- `--template <name>`: 業界別テンプレートを使用（retail, finance, healthcare等）

**実行例:**
```bash
# URLから価値を抽出
amplifier parasol:value-trace init --project asahi --from-url https://www.asahigroup-holdings.com

# 既存コードから分析
amplifier parasol:value-trace init --project myapp --from-code ./src
```

### record - 価値トレースの記録

コンポーネントや決定に対する価値の貢献を記録します。

```bash
amplifier parasol:value-trace record --component <name> --value <description> [--parent <parent-id>]
```

**オプション:**
- `--component <name>`: 対象コンポーネント名
- `--value <description>`: 提供する価値の説明
- `--parent <id>`: 親となる価値トレースID
- `--tags <tags>`: カテゴリタグ（カンマ区切り）
- `--impact <level>`: 影響度（low, medium, high, critical）

**実行例:**
```bash
# 基本的な価値記録
amplifier parasol:value-trace record \
  --component "user-authentication" \
  --value "セキュアなユーザー認証により顧客の信頼を確保" \
  --impact high

# 親子関係を持つ価値記録
amplifier parasol:value-trace record \
  --component "jwt-implementation" \
  --value "業界標準の認証方式により相互運用性を確保" \
  --parent auth-001 \
  --tags security,compliance
```

### visualize - 価値フローの可視化

プロジェクト全体の価値の流れを視覚的に表現します。

```bash
amplifier parasol:value-trace visualize [--output <file>] [--format <format>] [--filter <criteria>]
```

**オプション:**
- `--output <file>`: 出力ファイル名
- `--format <format>`: 出力形式（svg, png, html, mermaid）
- `--filter <criteria>`: フィルタ条件（component, tag, impact等）
- `--depth <n>`: 表示する階層の深さ
- `--highlight <ids>`: 強調表示する価値トレースID

**実行例:**
```bash
# 全体の価値フローを可視化
amplifier parasol:value-trace visualize --output value-flow.svg

# 高影響度の価値のみを表示
amplifier parasol:value-trace visualize \
  --filter impact=high,critical \
  --format html \
  --output critical-values.html
```

### analyze - 価値分析

価値の実現状況と構造的健全性を分析します。

```bash
amplifier parasol:value-trace analyze [--component <name>] [--milestone <ms>]
```

**オプション:**
- `--component <name>`: 特定コンポーネントの分析
- `--milestone <ms>`: 特定マイルストーンでの分析
- `--metrics`: 詳細メトリクスを表示
- `--suggestions`: 改善提案を生成

**分析内容:**
1. **価値カバレッジ**: すべての価値が実装でカバーされているか
2. **価値密度**: コンポーネントあたりの価値貢献度
3. **価値の連鎖**: 価値がどのように連鎖して最終価値を生むか
4. **ギャップ分析**: 未実現の価値や弱い連鎖の特定

**実行例:**
```bash
# プロジェクト全体の価値分析
amplifier parasol:value-trace analyze --metrics

# MS3時点での価値実現状況
amplifier parasol:value-trace analyze --milestone MS3 --suggestions
```

### report - 価値実現レポート

ステークホルダー向けの価値実現レポートを生成します。

```bash
amplifier parasol:value-trace report [--format <format>] [--audience <type>]
```

**オプション:**
- `--format <format>`: レポート形式（pdf, html, markdown, pptx）
- `--audience <type>`: 対象読者（executive, technical, stakeholder）
- `--period <range>`: レポート期間
- `--language <lang>`: 出力言語（ja, en）

**レポート内容:**
- エグゼクティブサマリー
- 価値実現の進捗状況
- 主要な価値指標（KVI: Key Value Indicators）
- リスクと機会の分析
- 次のステップの推奨事項

**実行例:**
```bash
# 経営層向けレポート（日本語）
amplifier parasol:value-trace report \
  --format pdf \
  --audience executive \
  --language ja

# 技術チーム向け詳細レポート
amplifier parasol:value-trace report \
  --format html \
  --audience technical \
  --period last-sprint
```

### validate - 価値の妥当性検証

記録された価値が構造的必然性を持つかを検証します。

```bash
amplifier parasol:value-trace validate [--fix] [--strict]
```

**オプション:**
- `--fix`: 検出された問題を自動修正
- `--strict`: 厳格なルールで検証
- `--rules <file>`: カスタム検証ルールを適用

**検証項目:**
- 価値の具体性（曖昧な表現の検出）
- 価値の測定可能性（KPIとの関連付け）
- 価値の実現可能性（技術的制約との整合性）
- 価値の一貫性（矛盾する価値の検出）

**実行例:**
```bash
# 標準検証
amplifier parasol:value-trace validate

# 自動修正モード
amplifier parasol:value-trace validate --fix --strict
```

## 統合機能

### 他コマンドとの連携

```bash
# マイルストーン進行時の自動価値チェック
amplifier parasol:milestone advance --to MS3 --validate-values

# 構造的必然性チェックとの統合
amplifier parasol:necessity-check --with-value-trace

# AIアシストによる価値抽出
amplifier parasol:value-trace init --ai-discover
```

### 価値トレースファイル形式

```yaml
# .parasol/value-traces.yaml
version: "5.0"
project: asahi
traces:
  - id: val-001
    component: customer-portal
    value: "顧客の利便性向上による満足度向上"
    impact: critical
    created: 2024-01-15T10:00:00Z
    tags: [ux, customer-satisfaction]
    children:
      - val-002
      - val-003
    metrics:
      - name: customer_satisfaction_score
        current: 4.2
        target: 4.5
      - name: portal_usage_rate
        current: 65%
        target: 80%
```

## ベストプラクティス

### 1. 価値の粒度

```yaml
# 良い例：具体的で測定可能
value: "注文処理時間を5秒から2秒に短縮し、顧客の待ち時間を60%削減"

# 悪い例：曖昧で測定不可能
value: "システムを改善する"
```

### 2. 価値の連鎖

```yaml
# ビジネス価値（最上位）
business_value: "市場シェアの拡大"
  # 顧客価値（中間）
  customer_value: "購買体験の向上"
    # 機能価値（実装）
    feature_value: "ワンクリック購入機能"
```

### 3. 継続的な追跡

```bash
# CI/CDパイプラインでの自動チェック
- name: Value Trace Validation
  run: amplifier parasol:value-trace validate --strict
  
# デプロイ前の価値実現確認
- name: Value Realization Check
  run: amplifier parasol:value-trace analyze --milestone current
```

## トラブルシューティング

### 価値の重複検出

```bash
# 重複する価値定義を検出
amplifier parasol:value-trace analyze --check-duplicates

# 類似の価値を統合
amplifier parasol:value-trace merge --interactive
```

### 価値の欠落検出

```bash
# コンポーネントに価値が定義されていない箇所を検出
amplifier parasol:value-trace coverage --show-gaps

# AIアシストで欠落価値を提案
amplifier parasol:value-trace suggest --component <name>
```

## 次のステップ

価値トレースを設定したら、以下のコマンドで構造的必然性を確保：

```bash
# 構造的必然性のチェック
amplifier parasol:necessity-check

# マイルストーンの進行
amplifier parasol:milestone advance
```