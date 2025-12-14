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

# MS3を厳格モードでチェック
amplifier parasol:quality-gate check --milestone MS3 --strict

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

MS1: ✓ PASS (12/12 チェック)
MS2: ✓ PASS (18/18 チェック)  
MS3: ⚠ WARN (15/16 チェック, 1 警告)
MS4: ✗ FAIL (8/14 チェック, 6 エラー)
MS5: - SKIP (MS4未完了)

総合スコア: 75.5%
推奨アクション: MS4の問題を修正してください
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
    milestone: MS4
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
    milestone: MS3
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

### MS1: 価値発見の品質ゲート

```yaml
MS1_gates:
  - value_clarity:
      description: "価値が明確に定義されているか"
      checks:
        - 価値の具体性（抽象的でない）
        - 測定可能性（KPIとの関連）
        - 実現可能性（技術的制約内）
        
  - stakeholder_coverage:
      description: "主要ステークホルダーが網羅されているか"
      checks:
        - 内部ステークホルダーの特定
        - 外部ステークホルダーの特定
        - 利害関係の明確化
        
  - value_uniqueness:
      description: "提供価値に独自性があるか"
      checks:
        - 競合差別化要因
        - 市場での位置付け
```

### MS2: 価値設計の品質ゲート

```yaml
MS2_gates:
  - value_decomposition:
      description: "価値が適切にケイパビリティに分解されているか"
      checks:
        - 完全性（すべての価値がカバー）
        - 粒度の適切性（大きすぎず小さすぎず）
        - 重複の排除
        
  - priority_consistency:
      description: "優先順位が一貫しているか"
      checks:
        - ビジネス価値との整合性
        - 依存関係の考慮
        - リソース制約の反映
        
  - capability_feasibility:
      description: "ケイパビリティが実現可能か"
      checks:
        - 技術的実現性
        - チームスキルとの適合
        - 予算内での実現性
```

### MS3: 構造設計の品質ゲート

```yaml
MS3_gates:
  - domain_consistency:
      description: "ドメインモデルが一貫しているか"
      checks:
        - ユビキタス言語の統一
        - 境界コンテキストの明確性
        - ドメインイベントの完全性
        
  - structural_necessity:
      description: "設計に構造的必然性があるか"
      checks:
        - 過剰な抽象化の排除
        - 適切な結合度
        - 単一責任の原則
        
  - technical_alignment:
      description: "技術選択が適切か"
      checks:
        - 要件との整合性
        - チームの技術力
        - 保守性の考慮
```

### MS4: 実装設計の品質ゲート

```yaml
MS4_gates:
  - api_quality:
      description: "APIが高品質か"
      checks:
        - RESTful原則の遵守
        - 一貫したエラーハンドリング
        - バージョニング戦略
        
  - data_integrity:
      description: "データ整合性が保証されているか"
      checks:
        - トランザクション境界
        - 一貫性レベルの定義
        - バックアップ戦略
        
  - security_compliance:
      description: "セキュリティ要件を満たすか"
      checks:
        - 認証・認可の実装
        - データ暗号化
        - 監査ログ
```

### MS5: 価値実現の品質ゲート

```yaml
MS5_gates:
  - implementation_completeness:
      description: "実装が完全か"
      checks:
        - 全機能の実装
        - エラーハンドリング
        - ロギングとモニタリング
        
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
amplifier parasol:quality-gate metrics --milestone MS3

# トレンド表示
amplifier parasol:quality-gate metrics --trend --days 30
```

**出力例:**
```
MS3 品質メトリクス:

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
    milestone: MS4
    calculation: "avg(response_times)"
    threshold: "<200ms"
    
  - id: value-delivery-rate
    name: "価値提供率"
    milestone: MS5
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