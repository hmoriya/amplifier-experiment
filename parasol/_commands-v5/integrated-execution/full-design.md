# parasol:full-design - 完全設計コマンド

## 概要

MS1（価値発見）からMS3（構造設計）まで一括で実行し、実装可能な完全な設計を生成します。価値から構造まで一貫性を保ちながら、包括的な設計ドキュメントとアーキテクチャを自動生成する統合コマンドです。

## なぜFull Designが必要か

### 設計の分断を防ぐ
- **従来**: 価値定義→機能設計→技術設計が分断され、価値が劣化
- **Full Design**: 価値を中心に一貫した設計フローを保証

### 設計の手戻りを削減
- **従来**: 後工程で問題発覚→大幅な手戻り
- **Full Design**: 早期に全体整合性を検証→手戻りゼロ

### AIによる設計最適化
- **従来**: 人間の経験と勘に依存
- **Full Design**: AIが膨大なパターンから最適設計を提案

## コマンド構文

```bash
amplifier parasol:full-design [--project <name>] [--interactive] [--parallel]
```

## 実行モード

### 標準モード（推奨）

```bash
# プロジェクト指定で実行
amplifier parasol:full-design --project my-app

# 現在のディレクトリのプロジェクトを自動検出
amplifier parasol:full-design
```

### インタラクティブモード

```bash
# 各段階で確認しながら進行
amplifier parasol:full-design --interactive

対話フロー:
MS1 完了 → レビュー → 承認/修正 → MS2 実行
MS2 完了 → レビュー → 承認/修正 → MS3 実行
MS3 完了 → 最終レビュー → 設計完了
```

### 高速並列モード

```bash
# 独立した分析を並列実行（最大4倍高速）
amplifier parasol:full-design --parallel --workers 8

並列化される処理:
- 価値ストリームの独立分析
- ドメインモデルの並列生成
- 技術オプションの同時評価
```

## 実行フロー詳細

### MS1: 価値発見フェーズ（10-15分）

```yaml
実行内容:
  価値抽出:
    - ビジネスゴールの明確化
    - ステークホルダー価値マッピング
    - 価値指標（KVI）の定義
    
  価値検証:
    - 市場性の検証
    - 実現可能性の確認
    - ROI予測
    
  成果物:
    - value-map.yaml
    - stakeholder-matrix.md
    - kvi-dashboard.json
```

### MS2: 価値設計フェーズ（15-20分）

```yaml
実行内容:
  価値分解:
    - 価値ストリーム設計
    - ケイパビリティマッピング
    - 優先順位マトリックス
    
  依存関係分析:
    - ケイパビリティ間依存
    - 技術的前提条件
    - リソース制約
    
  成果物:
    - value-streams.yaml
    - capability-map.json
    - priority-matrix.md
    - dependency-graph.svg
```

### MS3: 構造設計フェーズ（20-30分）

```yaml
実行内容:
  ドメインモデリング:
    - バウンデッドコンテキスト定義
    - エンティティ/集約設計
    - ドメインイベント設計
    
  技術アーキテクチャ:
    - システム構成設計
    - 技術スタック選定
    - 非機能要件対応
    
  成果物:
    - domain-model.yaml
    - architecture-decisions.md
    - system-design.json
    - deployment-diagram.svg
```

## 実行例

### 成功例: SaaSプラットフォーム設計

```bash
$ amplifier parasol:full-design --project saas-platform

🎯 Parasol Full Design - 完全設計自動生成

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[MS1: 価値発見] 10:23:15 - 10:35:42 (12分27秒)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

発見された中核価値:
1. 📊 データ分析の民主化
   - 非技術者でも高度な分析が可能
   - 価値: 分析工数を80%削減
   
2. 🔄 リアルタイムコラボレーション  
   - チーム全体でのインサイト共有
   - 価値: 意思決定速度を3倍に
   
3. 🤖 AI駆動の自動化
   - 定型分析の完全自動化
   - 価値: 人的エラーを95%削減

✓ 価値検証: すべての価値が市場ニーズと合致
✓ ステークホルダー: 12グループを特定・分析完了

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[MS2: 価値設計] 10:35:45 - 10:53:21 (17分36秒)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

設計された価値ストリーム:
• VS1: データ取り込みと変換
  └─ 15個のケイパビリティに分解
  
• VS2: 分析実行と可視化
  └─ 22個のケイパビリティに分解
  
• VS3: コラボレーションと共有
  └─ 18個のケイパビリティに分解

優先実装ケイパビリティ（Top 5）:
1. ドラッグ&ドロップデータインポート [P1]
2. ビジュアルクエリビルダー [P1]
3. リアルタイム共同編集 [P1]
4. AIレコメンデーション [P2]
5. 自動レポート生成 [P2]

✓ 依存関係: 循環依存なし、実装順序を最適化
✓ リソース見積: 6人×6ヶ月で中核機能実装可能

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[MS3: 構造設計] 10:53:25 - 11:21:08 (27分43秒)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

定義されたバウンデッドコンテキスト:
📦 DataIngestion Context
  - エンティティ: DataSource, Pipeline, Transform
  - 集約: IngestionJob
  - イベント: DataReceived, TransformCompleted

📦 Analytics Context  
  - エンティティ: Query, Dataset, Visualization
  - 集約: AnalysisSession
  - イベント: QueryExecuted, InsightGenerated

📦 Collaboration Context
  - エンティティ: Workspace, Member, Comment
  - 集約: SharedAnalysis
  - イベント: MemberJoined, CommentAdded

技術アーキテクチャ決定:
• マイクロサービス + イベント駆動
• 技術スタック:
  - Backend: Node.js + TypeScript
  - Event Bus: Apache Kafka
  - Database: PostgreSQL + ClickHouse
  - Cache: Redis
  - Frontend: React + WebSocket

非機能要件対応:
• スケーラビリティ: 水平スケール対応
• 可用性: 99.9% SLA
• セキュリティ: ゼロトラスト設計

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
設計完了！ 総実行時間: 57分46秒
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

生成された設計ドキュメント:
📁 projects/saas-platform/design/
  ├── 📄 executive-summary.pdf
  ├── 📊 value-architecture.html
  ├── 🏗️ technical-design.md
  ├── 📐 domain-models/
  ├── 🔧 api-specifications/
  └── 📈 implementation-roadmap.gantt

次の推奨アクション:
1. amplifier parasol:full-design --review  # 設計レビュー
2. amplifier parasol:milestone advance    # MS4へ進行
3. amplifier parasol:full-implementation  # 実装開始
```

## 高度なオプション

### 設計制約の指定

```bash
# 技術制約を指定
amplifier parasol:full-design \
  --constraints "cloud=aws,language=java,database=postgresql"

# 非機能要件を指定
amplifier parasol:full-design \
  --nfr "latency<100ms,availability>99.99%,cost<$10k/month"

# 既存システムとの統合
amplifier parasol:full-design \
  --integrate-with "./legacy-system-spec.yaml"
```

### AI設計アシスタント

```bash
# AIによる設計レビュー
amplifier parasol:full-design --ai-review

# 代替設計の生成
amplifier parasol:full-design --alternatives 3

# 設計パターン推奨
amplifier parasol:full-design --suggest-patterns
```

### チーム連携機能

```bash
# リアルタイム設計セッション
amplifier parasol:full-design --collaborative --session-id team123

# 設計承認ワークフロー
amplifier parasol:full-design --approval-required --approvers @architects

# 設計変更の追跡
amplifier parasol:full-design --track-changes --baseline v1.0
```

## 設計品質保証

### 自動品質チェック

```yaml
品質チェック項目:
  価値整合性:
    - すべての設計要素が価値に紐づく
    - 価値の劣化がない
    - ROI基準を満たす
    
  設計原則:
    - SOLID原則の遵守
    - DDD戦略パターンの適用
    - マイクロサービス原則
    
  実装可能性:
    - 技術的実現性
    - チームスキルとの適合
    - 予算内での実現
```

### 設計メトリクス

```bash
# 設計品質スコア表示
amplifier parasol:full-design --show-metrics

出力例:
設計品質メトリクス:
- 価値カバレッジ: 98%
- 設計一貫性: 94%
- 複雑度スコア: 3.2/10 (シンプル)
- 技術リスク: Low
- 推定実装工数: 720人時
```

## カスタマイズ

### 設計テンプレート

```yaml
# .parasol/design-template.yaml
template:
  name: "Event-Driven Microservices"
  
  patterns:
    - event-sourcing
    - cqrs
    - saga-pattern
    
  constraints:
    - max-service-size: 2000loc
    - min-test-coverage: 90%
    - event-schema-versioning: required
    
  technology-preferences:
    language: typescript
    framework: nestjs
    event-bus: kafka
    database: event-store
```

### 設計ルール

```yaml
# .parasol/design-rules.yaml
rules:
  - id: no-circular-dependency
    severity: error
    message: "サービス間の循環依存は禁止"
    
  - id: bounded-context-size
    max-entities: 10
    max-aggregates: 5
    message: "コンテキストが大きすぎます"
    
  - id: api-versioning
    pattern: "/v[0-9]+/"
    required: true
    message: "APIバージョニングが必要です"
```

## トラブルシューティング

### 設計の不整合

```bash
# 不整合の検出と修正
amplifier parasol:full-design --validate --fix

# 特定フェーズの再実行
amplifier parasol:full-design --retry MS2

# デバッグモード
amplifier parasol:full-design --debug --verbose
```

### パフォーマンス問題

```bash
# 軽量モード（基本設計のみ）
amplifier parasol:full-design --lightweight

# タイムアウト延長
amplifier parasol:full-design --timeout 2h

# 段階的実行
amplifier parasol:full-design --staged
```

## ベストプラクティス

### 1. 事前準備

```bash
# 入力情報の整理
- ビジネス目標を明文化
- 制約条件をリスト化
- 既存資産を棚卸し

# チームアラインメント
- キックオフセッションの実施
- 共通理解の確立
```

### 2. 実行中の確認

```bash
# 各マイルストーンでの確認
amplifier parasol:full-design --pause-between-milestones

# 重要な決定での承認
amplifier parasol:full-design --require-approval-for critical-decisions
```

### 3. 設計後の活用

```bash
# 設計ドキュメントの活用
- Wiki/Confluenceへの自動公開
- アーキテクチャ決定記録（ADR）の生成
- 実装チェックリストの作成

# 継続的な設計更新
amplifier parasol:full-design --update --incremental
```

## 統合ワークフロー

### CI/CDパイプライン

```yaml
# 設計の継続的検証
- name: Design Validation
  run: |
    amplifier parasol:full-design --validate
    amplifier parasol:full-design --compare-with production
```

### 設計レビュープロセス

```bash
# レビュー用資料生成
amplifier parasol:full-design --generate-review-deck

# フィードバック収集
amplifier parasol:full-design --collect-feedback

# 設計の承認と凍結
amplifier parasol:full-design --freeze --version 1.0
```

## 次のステップ

Full Designが完了したら：

```bash
# 実装設計へ進む（MS4）
amplifier parasol:milestone advance

# 完全実装を開始
amplifier parasol:full-implementation

# 設計の詳細化
amplifier parasol:full-design --refine
```

## まとめ

Full Designは「**価値を形にする**」プロセスを自動化します。従来なら数週間かかった包括的な設計作業を1時間以内で完了し、価値から実装まで一貫性のある設計ドキュメントを生成します。人間は価値と制約を定義し、AIが最適な設計を導き出す - これがParasol V5の設計哲学です。