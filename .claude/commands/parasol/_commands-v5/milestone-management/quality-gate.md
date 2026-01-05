# parasol:quality-gate - 品質ゲート実行コマンド

## 概要

各マイルストーンで定義された品質基準を自動的にチェックし、価値実現の品質を保証します。構造的必然性、価値の継承、実装の完全性など、多角的な品質チェックを統合的に実行します。

## 品質ゲートの思想

### なぜ品質ゲートが必要か

1. **価値の確実な実現**
   - 各段階で価値が正しく継承されているか検証
   - 価値の劣化や逸脱を防止

2. **構造的必然性の維持**
   - 想像の設計の混入を防ぐ
   - すべての決定が価値に基づくことを保証

3. **段階的な品質保証**
   - 問題を早期に発見し修正コストを削減
   - 次のマイルストーンへの確実な移行

## コマンド構文

```bash
amplifier parasol:quality-gate <サブコマンド> [オプション]
```

## サブコマンド

### check - 品質チェックの実行

現在のマイルストーンに対する品質チェックを実行します。

```bash
amplifier parasol:quality-gate check [--milestone <ms>] [--strict] [--fix]
```

**オプション:**
- `--milestone <ms>`: 特定のマイルストーンをチェック（デフォルト: 現在）
- `--strict`: 厳格モード（警告もエラーとして扱う）
- `--fix`: 自動修正可能な問題を修正
- `--category <name>`: 特定のカテゴリのみチェック

**実行例:**
```bash
# 現在のマイルストーンをチェック
amplifier parasol:quality-gate check

# VMS3を厳格モードでチェック
amplifier parasol:quality-gate check --milestone VMS3 --strict

# 価値継承カテゴリのみチェック
amplifier parasol:quality-gate check --category value-inheritance
```

### run-all - 全品質ゲートの実行

すべてのマイルストーンの品質ゲートを順次実行します。

```bash
amplifier parasol:quality-gate run-all [--stop-on-error] [--parallel]
```

**オプション:**
- `--stop-on-error`: エラー時に停止
- `--parallel`: 並列実行（独立したチェックのみ）
- `--report <file>`: 統合レポートを出力

**出力例:**
```
全体品質ゲート実行結果:

VMS1: ✓ PASS (12/12 チェック)
VMS2: ✓ PASS (18/18 チェック)
VMS3: ⚠ WARN (15/16 チェック, 1 警告)
VMS4: ✗ FAIL (8/14 チェック, 6 エラー)
VMS5: - SKIP (VMS4未完了)

総合スコア: 75.5%
推奨アクション: VMS4の問題を修正してください
```

### add-rule - カスタムルールの追加

プロジェクト固有の品質ルールを追加します。

```bash
amplifier parasol:quality-gate add-rule --file <rule-file> [--validate]
```

**ルール定義例:**
```yaml
# custom-quality-rules.yaml
rules:
  - id: min-test-coverage
    name: "最小テストカバレッジ"
    milestone: VMS4
    category: implementation
    check:
      type: metric
      target: test_coverage
      operator: ">="
      value: 80
    severity: error
    message: "テストカバレッジは80%以上必要です"
    
  - id: api-consistency
    name: "API一貫性チェック"
    milestone: VMS3
    category: design
    check:
      type: pattern
      pattern: "REST|GraphQL"
      exclusive: true
    severity: warning
    message: "APIスタイルを統一してください"
```

### configure - 品質ゲートの設定

品質ゲートの動作を設定します。

```bash
amplifier parasol:quality-gate configure [--interactive] [--preset <name>]
```

**設定項目:**
```yaml
# .parasol/quality-gate-config.yaml
config:
  strictness: standard  # low, standard, high
  auto_fix: true
  parallel_execution: false
  
  thresholds:
    pass_percentage: 100
    warn_as_error: false
    
  categories:
    value: enabled
    structure: enabled
    implementation: enabled
    performance: disabled
    
  notifications:
    on_fail: true
    on_success: false
    channels:
      - slack
      - email
```

## 標準品質ゲート

**重要**: VMSは「プロセス完了」ではなく「**顧客が得ている価値状態**」を定義します。
品質ゲートは、顧客がその価値状態に到達できるかを検証します。

### VMS1: 顧客が最初の価値を体験できる状態（3ヶ月後）

```yaml
VMS1_gates:
  - first_value_delivery:
      description: "顧客が最初の具体的価値を体験できるか"
      checks:
        - VL3レベルの価値が1つ以上実現
        - 顧客が価値を認識できる接点が存在
        - 価値指標での改善確認

  - customer_touchpoint:
      description: "顧客接点が機能しているか"
      checks:
        - 価値を体験できるUIが稼働
        - 基本的なユーザージャーニーが完了可能
        - フィードバック収集メカニズムが稼働

  - measurable_improvement:
      description: "測定可能な改善が確認できるか"
      checks:
        - ベースライン指標からの改善
        - 顧客満足度指標の設定
        - 価値実現の証拠
```

### VMS2: 顧客が価値を認識し選択できる状態（6ヶ月後）

```yaml
VMS2_gates:
  - value_recognition:
      description: "顧客が価値を認識しているか"
      checks:
        - 複数のVL3価値が実現
        - 顧客からの価値認識フィードバック
        - 利用パターンの形成

  - choice_enablement:
      description: "顧客が価値を選択できるか"
      checks:
        - 複数の価値オプションが利用可能
        - 顧客が自分のニーズに合わせて選択可能
        - パーソナライゼーションの基盤

  - adoption_metrics:
      description: "採用指標が目標に達しているか"
      checks:
        - アクティブユーザー数の増加
        - リピート利用率
        - 機能利用率
```

### VMS3: 顧客が主要価値を日常的に体験できる状態（9ヶ月後）

```yaml
VMS3_gates:
  - daily_value_experience:
      description: "顧客が日常的に価値を体験しているか"
      checks:
        - VL2レベルの主要価値が実現
        - 日常利用パターンの確立
        - 習慣化指標の達成

  - core_journey_completion:
      description: "コアユーザージャーニーが完全か"
      checks:
        - 主要ユースケースが全て稼働
        - エンドツーエンドのフローが完成
        - 主要機能の安定稼働

  - quality_consistency:
      description: "品質が一貫しているか"
      checks:
        - パフォーマンス目標の達成
        - 可用性目標の達成
        - ユーザー体験の一貫性
```

### VMS4: 顧客が全面的に価値を実感している状態（12ヶ月後）

```yaml
VMS4_gates:
  - comprehensive_value:
      description: "顧客が全面的に価値を実感しているか"
      checks:
        - VL1レベルの戦略的価値が実現
        - 全バリューストリームが稼働
        - 顧客ロイヤルティの向上

  - business_impact:
      description: "ビジネス成果が達成されているか"
      checks:
        - ROI目標の達成
        - コスト削減/収益増加の証拠
        - 競争優位性の確立

  - operational_excellence:
      description: "運用品質が高いか"
      checks:
        - SLA達成率
        - インシデント対応時間
        - システム安定性
```

### VMS5: 顧客が期待を超える価値を日常的に享受している状態（18ヶ月後）

```yaml
VMS5_gates:
  - exceeded_expectations:
      description: "顧客の期待を超えているか"
      checks:
        - 顧客満足度が目標を超過
        - NPS/CSATの継続的向上
        - 顧客からの自発的推薦

  - continuous_value_growth:
      description: "価値が継続的に成長しているか"
      checks:
        - 新機能による価値追加
        - 既存価値の深化
        - イノベーションパイプライン
        
  - test_coverage:
      description: "十分なテストがあるか"
      checks:
        - 単体テストカバレッジ（>80%）
        - 統合テストの実施
        - E2Eテストの実施
        
  - value_validation:
      description: "価値が実現されているか"
      checks:
        - KPI目標の達成
        - ユーザー受け入れテスト
        - パフォーマンス基準
```

## 品質メトリクス

### メトリクス表示

```bash
# 現在のメトリクスを表示
amplifier parasol:quality-gate metrics

# 特定マイルストーンのメトリクス
amplifier parasol:quality-gate metrics --milestone VMS3

# トレンド表示
amplifier parasol:quality-gate metrics --trend --days 30
```

**出力例:**
```
VMS3 品質メトリクス:

構造的品質:
  複雑度スコア: 3.2/10 (良好)
  結合度: 0.15 (低結合 ✓)
  凝集度: 0.89 (高凝集 ✓)
  
価値アライメント:
  価値カバレッジ: 96%
  トレーサビリティ: 100%
  
技術的品質:
  技術負債: 2.5時間
  保守性指数: 85/100
```

### カスタムメトリクス

```yaml
# .parasol/custom-metrics.yaml
metrics:
  - id: api-response-time
    name: "API応答時間"
    milestone: VMS4
    calculation: "avg(response_times)"
    threshold: "<200ms"
    
  - id: value-delivery-rate
    name: "価値提供率"
    milestone: VMS5
    calculation: "delivered_features / planned_features * 100"
    threshold: ">90%"
```

## レポート生成

### 品質レポート

```bash
# 標準レポート生成
amplifier parasol:quality-gate report

# エグゼクティブサマリー
amplifier parasol:quality-gate report --executive --format pdf

# 詳細技術レポート
amplifier parasol:quality-gate report --technical --include-metrics
```

### 自動レポート

```bash
# マイルストーン完了時の自動レポート
amplifier parasol:quality-gate auto-report --on milestone-complete

# 定期レポート
amplifier parasol:quality-gate auto-report --schedule weekly
```

## CI/CD統合

### パイプライン統合

```yaml
# .github/workflows/quality-gate.yml
name: Quality Gate Check
on:
  push:
    branches: [main, develop]
  pull_request:

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Quality Gates
        run: |
          amplifier parasol:quality-gate check --strict
          amplifier parasol:quality-gate metrics >> $GITHUB_STEP_SUMMARY
          
      - name: Upload Report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: quality-report
          path: quality-report.html
```

### 自動修正フロー

```bash
# プルリクエストでの自動修正
amplifier parasol:quality-gate check --fix --commit --push
```

## トラブルシューティング

### 品質ゲート失敗時の対処

```bash
# 詳細な失敗理由の確認
amplifier parasol:quality-gate diagnose --verbose

# 特定のチェックをスキップ（一時的）
amplifier parasol:quality-gate check --skip-rules RULE-001,RULE-002

# 修正ガイドの生成
amplifier parasol:quality-gate fix-guide --interactive
```

### パフォーマンス最適化

```bash
# キャッシュの有効化
amplifier parasol:quality-gate check --use-cache

# 増分チェック
amplifier parasol:quality-gate check --incremental

# 並列実行
amplifier parasol:quality-gate check --parallel --workers 4
```

## ベストプラクティス

### 1. 継続的な品質チェック

```bash
# コミットフックでの自動チェック
echo 'amplifier parasol:quality-gate check --quick' >> .git/hooks/pre-commit

# プッシュ前の完全チェック
echo 'amplifier parasol:quality-gate check --strict' >> .git/hooks/pre-push
```

### 2. 段階的な品質向上

```bash
# Phase 1: 警告のみ
amplifier parasol:quality-gate configure --strictness low

# Phase 2: 主要項目をエラー化
amplifier parasol:quality-gate configure --strictness standard

# Phase 3: 完全な品質保証
amplifier parasol:quality-gate configure --strictness high
```

### 3. チーム学習

```bash
# 品質ガイドラインの生成
amplifier parasol:quality-gate generate-guidelines

# チーム向けワークショップ
amplifier parasol:quality-gate workshop --interactive
```

## 次のステップ

品質ゲートを通過したら：

```bash
# 価値継承のチェック
amplifier parasol:value-inheritance check

# 次のマイルストーンへ
amplifier parasol:milestone advance
```