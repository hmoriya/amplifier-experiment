# parasol:quick-start - 高速スタートコマンド

## 概要

URLや既存コードベースから価値を自動抽出し、VMS1（価値発見）まで高速で到達します。最小限の入力で最大限の価値発見を実現し、プロジェクトを迅速に立ち上げる統合コマンドです。

## なぜQuick Startが必要か

### 従来の課題
1. **分析麻痺** - 完璧な計画を求めて開始が遅れる
2. **価値の見落とし** - 手動分析では重要な価値を見逃す
3. **初期設定の煩雑さ** - 多数のコマンドを順次実行する必要

### Quick Startの解決策
1. **即座に開始** - URLを入力するだけで分析開始
2. **AIによる網羅的発見** - 人間が見逃す価値も抽出
3. **ワンコマンド** - 複雑な初期設定を自動化

## コマンド構文

```bash
amplifier parasol:quick-start [--url <url>] [--codebase <path>] [--ai-assist]
```

## 基本使用法

### URLからの高速起動

```bash
# 企業サイトから価値抽出
amplifier parasol:quick-start --url https://www.asahigroup-holdings.com

# 複数URLから包括的分析
amplifier parasol:quick-start --urls urls.txt

# AIによる深層分析
amplifier parasol:quick-start --url https://example.com --ai-deep
```

### 既存コードベースからの起動

```bash
# ローカルコードベースを分析
amplifier parasol:quick-start --codebase ./src

# GitHubリポジトリから直接
amplifier parasol:quick-start --github owner/repo

# 特定の技術スタックを考慮
amplifier parasol:quick-start --codebase ./src --stack nodejs,react
```

### インタラクティブモード

```bash
# 対話的に情報を入力
amplifier parasol:quick-start --interactive

質問フロー:
1. プロジェクトの種類は？ (新規/既存改善/移行)
2. 主要なステークホルダーは？
3. 解決したい課題は？
4. 期待する成果は？
```

## 実行フロー

### Phase 1: 情報収集（～3分）

```yaml
自動実行内容:
  - URL解析:
      - メタデータ抽出
      - コンテンツ分析
      - リンク構造解析
      
  - コードベース分析:
      - アーキテクチャ推論
      - 依存関係マッピング
      - 技術スタック特定
      
  - 外部情報収集:
      - 業界トレンド
      - 競合分析
      - 規制要件
```

### Phase 2: 価値抽出（～5分）

```yaml
AI分析プロセス:
  - ビジネス価値の特定:
      - 収益向上機会
      - コスト削減領域
      - 競争優位性
      
  - 技術価値の発見:
      - 効率化ポテンシャル
      - スケーラビリティ
      - 保守性改善
      
  - ユーザー価値の抽出:
      - UX改善機会
      - 新機能可能性
      - 課題解決領域
```

### Phase 3: 初期構造化（～2分）

```yaml
自動生成物:
  - 価値マップ:
      - 価値階層構造
      - 価値間の関係
      - 優先順位候補
      
  - ステークホルダーマップ:
      - 主要関係者
      - 利害関係
      - コミュニケーションパス
      
  - 初期ロードマップ:
      - クイックウィン
      - 中期目標
      - 長期ビジョン
```

## 実行例

### 成功例: ECサイトリニューアル

```bash
$ amplifier parasol:quick-start --url https://old-ec-site.com

🚀 Parasol Quick Start - 高速プロジェクト立ち上げ

[Phase 1: 情報収集]
✓ URL解析完了: 523ページ分析
✓ 技術スタック特定: PHP 5.6, MySQL 5.5 (レガシー)
✓ 外部情報: EC市場成長率 15%/年

[Phase 2: 価値抽出]
発見された主要価値:
1. 🎯 ページ読み込み時間改善 (現在: 8秒 → 目標: 2秒)
2. 💰 モバイル売上向上 (現在: 20% → 目標: 60%)
3. 🔧 運用コスト削減 (現在: 月50万 → 目標: 月20万)
4. 🛡️ セキュリティ強化 (脆弱性: 15件検出)

[Phase 3: 初期構造化]
生成された成果物:
- 📊 価値マップ: ./outputs/value-map.yaml
- 👥 ステークホルダー: ./outputs/stakeholders.yaml
- 🗺️ ロードマップ: ./outputs/roadmap.md

プロジェクト "ec-renewal" が作成されました！

推奨される次のアクション:
1. amplifier parasol:milestone advance  # VMS2へ進行
2. amplifier parasol:value-trace visualize  # 価値を可視化
3. amplifier parasol:quick-start --review  # 結果をレビュー

完了時間: 7分32秒 ⚡
```

## オプション詳細

### 分析オプション

```bash
# 浅い分析（高速、基本情報のみ）
amplifier parasol:quick-start --depth shallow

# 標準分析（デフォルト）
amplifier parasol:quick-start --depth standard

# 深層分析（詳細、時間をかけて徹底分析）
amplifier parasol:quick-start --depth deep --timeout 30m
```

### AI支援オプション

```bash
# AIアシスト有効化
amplifier parasol:quick-start --ai-assist

# 特定のAIモデル使用
amplifier parasol:quick-start --ai-model gpt-4 --ai-temperature 0.7

# AIによる仮説生成
amplifier parasol:quick-start --ai-hypotheses 10
```

### 出力オプション

```bash
# カスタム出力ディレクトリ
amplifier parasol:quick-start --output ./my-analysis

# 特定フォーマットで出力
amplifier parasol:quick-start --format json --pretty

# レポート生成
amplifier parasol:quick-start --generate-report --lang ja
```

## テンプレート機能

### 業界別テンプレート

```bash
# 小売業テンプレート
amplifier parasol:quick-start --template retail

# 金融サービステンプレート
amplifier parasol:quick-start --template fintech --compliance strict

# ヘルスケアテンプレート
amplifier parasol:quick-start --template healthcare --privacy hipaa
```

### カスタムテンプレート

```yaml
# .parasol/quick-start-template.yaml
template:
  name: "SaaS B2B"
  
  default_values:
    - scalability
    - multi-tenancy
    - api-first
    
  required_analysis:
    - pricing-model
    - integration-points
    - compliance-requirements
    
  stakeholder_roles:
    - product-owner
    - tech-lead
    - customer-success
```

## 高度な機能

### 継続的Quick Start

```bash
# 前回の続きから開始
amplifier parasol:quick-start --continue

# 差分分析（変更点のみ）
amplifier parasol:quick-start --incremental --since last-week

# 定期実行
amplifier parasol:quick-start --schedule weekly --notify slack
```

### 比較分析

```bash
# 競合サイトとの比較
amplifier parasol:quick-start --compare https://competitor.com

# 複数バージョンの比較
amplifier parasol:quick-start --baseline v1.0 --compare v2.0
```

### チーム連携

```bash
# チーム用ワークスペース作成
amplifier parasol:quick-start --team --invite team@example.com

# レビューセッション開始
amplifier parasol:quick-start --review-session --live

# 結果の共有
amplifier parasol:quick-start --share --format slides
```

## エラーハンドリング

### よくあるエラーと対処

```bash
# URL アクセスエラー
Error: Unable to access URL
対処: amplifier parasol:quick-start --url <url> --use-cache

# タイムアウト
Error: Analysis timeout
対処: amplifier parasol:quick-start --timeout 60m --depth shallow

# メモリ不足
Error: Out of memory
対処: amplifier parasol:quick-start --stream --low-memory
```

### リカバリー機能

```bash
# 中断からの再開
amplifier parasol:quick-start --resume

# 部分的な結果を保存
amplifier parasol:quick-start --save-partial

# エラーログの詳細
amplifier parasol:quick-start --debug --log-level trace
```

## ベストプラクティス

### 1. 適切な開始点の選択

```bash
# 新規プロジェクト: URLから開始
amplifier parasol:quick-start --url https://target.com

# 既存改善: コードベースから開始
amplifier parasol:quick-start --codebase ./current

# 移行プロジェクト: 両方を分析
amplifier parasol:quick-start --url https://old.com --codebase ./legacy
```

### 2. 段階的な深化

```bash
# Step 1: クイック分析
amplifier parasol:quick-start --depth shallow

# Step 2: 興味深い領域を深堀り
amplifier parasol:quick-start --focus "mobile-experience" --depth deep

# Step 3: 具体的な価値を詳細化
amplifier parasol:value-trace record --refine
```

### 3. チームアライメント

```bash
# 初回はチーム全員で実行
amplifier parasol:quick-start --interactive --team

# 結果を即座に共有
amplifier parasol:quick-start --share --notify @channel

# フィードバックを収集
amplifier parasol:quick-start --collect-feedback
```

## パフォーマンス最適化

### 高速化テクニック

```bash
# 並列処理を活用
amplifier parasol:quick-start --parallel --workers 8

# キャッシュを活用
amplifier parasol:quick-start --use-cache --cache-ttl 7d

# 不要な分析をスキップ
amplifier parasol:quick-start --skip images,videos
```

### リソース管理

```bash
# メモリ制限設定
amplifier parasol:quick-start --max-memory 4G

# CPU使用率制限
amplifier parasol:quick-start --cpu-limit 80%

# ネットワーク帯域制限
amplifier parasol:quick-start --bandwidth-limit 10M
```

## 統合ワークフロー

### CI/CDパイプライン

```yaml
# .github/workflows/quick-start.yml
name: Weekly Value Discovery
on:
  schedule:
    - cron: '0 9 * * 1'  # 毎週月曜9時
    
jobs:
  discover:
    runs-on: ubuntu-latest
    steps:
      - name: Run Quick Start Analysis
        run: |
          amplifier parasol:quick-start \
            --url ${{ vars.PRODUCTION_URL }} \
            --incremental \
            --notify-slack
```

### 自動化フロー

```bash
# 変更検知→自動分析
amplifier parasol:quick-start --watch --auto-analyze

# 結果に基づく自動アクション
amplifier parasol:quick-start --trigger-on "new-value-found"
```

## 次のステップ

Quick Startが完了したら：

```bash
# 詳細設計へ進む
amplifier parasol:full-design

# 価値の詳細化
amplifier parasol:value-trace refine

# 早期実装
amplifier parasol:milestone advance --to VMS2
```

## まとめ

Quick Startは「**すぐ始められる、でも手を抜かない**」を実現します。URLを入力して10分待つだけで、従来なら数日かかった価値発見プロセスが完了し、VMS1到達とともに明確な次のステップが見えてきます。