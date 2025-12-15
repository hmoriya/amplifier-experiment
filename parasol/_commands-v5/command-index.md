# Parasol V5 コマンド一覧

## 価値管理コマンド群

### /parasol:value-trace
価値トレースの管理と可視化

```bash
# 価値トレースの初期化
amplifier parasol:value-trace init --project my-project

# 価値トレースの記録
amplifier parasol:value-trace record --component "user-auth" --value "セキュリティ向上"

# 価値フローの可視化
amplifier parasol:value-trace visualize --output value-flow.svg

# 価値実現レポート
amplifier parasol:value-trace report --format html
```

### /parasol:necessity-check
構造的必然性の検証

```bash
# 単体コンポーネントの検証
amplifier parasol:necessity-check --component "feature-x"

# プロジェクト全体の検証
amplifier parasol:necessity-check --project my-project --deep

# 自動修正モード
amplifier parasol:necessity-check --fix --interactive
```

### /parasol:imagination-detect
想像の設計の検出と除去

```bash
# 想像の設計をスキャン
amplifier parasol:imagination-detect scan

# 検出結果の詳細表示
amplifier parasol:imagination-detect show --verbose

# 自動リファクタリング
amplifier parasol:imagination-detect refactor --confirm
```

## マイルストーン管理コマンド群

### /parasol:milestone
VMS1-VMS5の統合管理

```bash
# 現在のマイルストーン状況
amplifier parasol:milestone status

# 特定マイルストーンへ移行
amplifier parasol:milestone advance --to VMS3

# マイルストーン間の依存関係確認
amplifier parasol:milestone dependencies --from VMS2 --to VMS4
```

### /parasol:quality-gate
品質ゲートの実行

```bash
# 現在のマイルストーンの品質チェック
amplifier parasol:quality-gate check

# すべての品質ゲートを実行
amplifier parasol:quality-gate run-all

# カスタム品質ルールの追加
amplifier parasol:quality-gate add-rule --file custom-rules.yaml
```

### /parasol:value-inheritance
価値継承のチェック

```bash
# 価値継承の検証
amplifier parasol:value-inheritance check

# 継承パスの可視化
amplifier parasol:value-inheritance visualize

# 欠落している継承の自動補完
amplifier parasol:value-inheritance repair
```

## 統合実行コマンド群

### /parasol:quick-start
高速スタート（VMS1まで自動実行）

```bash
# URLからプロジェクトを高速起動
amplifier parasol:quick-start --url https://example.com

# 既存コードベースから高速起動
amplifier parasol:quick-start --codebase ./src

# AIアシスト付き高速起動
amplifier parasol:quick-start --ai-assist
```

### /parasol:full-design
完全設計（VMS1-VMS3まで一括実行）

```bash
# 標準的な完全設計
amplifier parasol:full-design --project my-project

# インタラクティブモード
amplifier parasol:full-design --interactive

# 並列実行モード（高速）
amplifier parasol:full-design --parallel --workers 4
```

### /parasol:full-implementation
完全実装（VMS1-VMS5まで一括実行）

```bash
# 完全自動実装
amplifier parasol:full-implementation --auto

# ステップバイステップ実装
amplifier parasol:full-implementation --step-by-step

# ドライラン（実行計画の確認）
amplifier parasol:full-implementation --dry-run
```

## 分析・レポートコマンド群

### /parasol:value-report
価値実現レポートの生成

```bash
# 標準レポート生成
amplifier parasol:value-report generate

# エグゼクティブサマリー
amplifier parasol:value-report executive --format pdf

# 詳細分析レポート
amplifier parasol:value-report detailed --include-metrics
```

### /parasol:structural-analysis
構造的必然性の分析

```bash
# 構造分析の実行
amplifier parasol:structural-analysis run

# 弱点の特定
amplifier parasol:structural-analysis weaknesses

# 改善提案の生成
amplifier parasol:structural-analysis suggest-improvements
```

### /parasol:project-health
プロジェクト健全性診断

```bash
# 総合健全性チェック
amplifier parasol:project-health check

# リアルタイムモニタリング
amplifier parasol:project-health monitor --interval 60s

# 健全性ダッシュボード起動
amplifier parasol:project-health dashboard --port 8080
```

## グローバルオプション

すべてのコマンドで使用可能なオプション：

```bash
--project <name>     # プロジェクト名を指定
--config <file>      # カスタム設定ファイルを使用
--output <dir>       # 出力ディレクトリを指定
--format <format>    # 出力形式（json, yaml, html, pdf）
--verbose           # 詳細出力モード
--quiet             # 静音モード
--no-color          # カラー出力を無効化
--dry-run           # ドライランモード
--help              # ヘルプを表示
```

## エイリアスとショートカット

よく使うコマンドの短縮形：

```bash
# クイックコマンド
amplifier pv:trace    # parasol:value-trace
amplifier pv:check    # parasol:necessity-check
amplifier pv:ms       # parasol:milestone
amplifier pv:health   # parasol:project-health

# ワンライナー実行
amplifier pv:go       # quick-start + health check
amplifier pv:design   # full-design + value-report
amplifier pv:ship     # full-implementation + final report
```