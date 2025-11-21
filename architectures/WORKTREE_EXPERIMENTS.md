# Git Worktree アーキテクチャ実験環境

## 概要

Git worktreeを使用して、複数のアーキテクチャパターンを並行して実験・比較できる環境です。
各アーキテクチャは独立したworktreeで開発され、簡単に切り替えて比較できます。

## 実験可能なアーキテクチャ

### 1. 🏛️ Monolithic Architecture (`arch/monolithic`)
単一のコードベースで全機能を実装する伝統的アーキテクチャ

### 2. 🎯 Microservices Architecture (`arch/microservices`)
機能を独立したサービスに分割する分散アーキテクチャ

### 3. 🔌 Event-Driven Architecture (`arch/event-driven`)
イベントを中心とした非同期通信アーキテクチャ

### 4. 🧅 Onion/Clean Architecture (`arch/clean`)
ドメインを中心とした層構造アーキテクチャ

### 5. 🔷 Hexagonal Architecture (`arch/hexagonal`)
ポートとアダプターパターンによる柔軟なアーキテクチャ

### 6. ⚡ Serverless Architecture (`arch/serverless`)
サーバーレス関数を活用したクラウドネイティブアーキテクチャ

### 7. 🌂 Parasol V3-V4 Hybrid (`arch/parasol-hybrid`)
パラソルV3.0とV4の統合アーキテクチャ

### 8. 📊 CQRS + Event Sourcing (`arch/cqrs-es`)
コマンドとクエリを分離し、イベントソーシングを活用

## セットアップ手順

### 1. Worktree環境の初期化

```bash
# セットアップスクリプトを実行
./architectures/setup-worktrees.sh

# または手動で各worktreeを作成
git worktree add -b arch/monolithic ../amplifier-monolithic
git worktree add -b arch/microservices ../amplifier-microservices
git worktree add -b arch/event-driven ../amplifier-event-driven
git worktree add -b arch/clean ../amplifier-clean
git worktree add -b arch/hexagonal ../amplifier-hexagonal
git worktree add -b arch/serverless ../amplifier-serverless
git worktree add -b arch/parasol-hybrid ../amplifier-parasol-hybrid
git worktree add -b arch/cqrs-es ../amplifier-cqrs-es
```

### 2. 特定のアーキテクチャに切り替え

```bash
# Microservicesアーキテクチャに切り替え
cd ../amplifier-microservices

# または元のディレクトリから
cd $(git worktree list | grep microservices | awk '{print $1}')
```

### 3. アーキテクチャの実装

各worktreeで独立して開発：

```bash
# Microservicesの実装
cd ../amplifier-microservices
python architectures/implement.py --arch microservices

# Clean Architectureの実装
cd ../amplifier-clean
python architectures/implement.py --arch clean
```

## アーキテクチャ詳細

### Monolithic Architecture

```yaml
structure:
  /src:
    /controllers: # HTTPコントローラー
    /services: # ビジネスロジック
    /models: # データモデル
    /database: # データベース層
    /utils: # ユーティリティ

pros:
  - シンプルな構造
  - デバッグが容易
  - トランザクション管理が簡単

cons:
  - スケーラビリティの制限
  - 技術スタックの固定
  - 大規模チームでの開発が困難

use_cases:
  - 小規模プロジェクト
  - プロトタイプ
  - 単純なCRUDアプリケーション
```

### Microservices Architecture

```yaml
structure:
  /services:
    /auth-service: # 認証サービス
    /task-service: # タスク管理サービス
    /notification-service: # 通知サービス
  /api-gateway: # APIゲートウェイ
  /service-mesh: # サービスメッシュ設定

pros:
  - 独立したデプロイ
  - 技術の多様性
  - 高いスケーラビリティ

cons:
  - 運用の複雑さ
  - ネットワークオーバーヘッド
  - 分散トランザクションの難しさ

use_cases:
  - 大規模システム
  - 異なるチームによる開発
  - 高いスケーラビリティ要件
```

### Event-Driven Architecture

```yaml
structure:
  /events:
    /producers: # イベント生成者
    /consumers: # イベント消費者
    /schemas: # イベントスキーマ
  /event-bus: # イベントバス実装
  /saga: # サガパターン実装

pros:
  - 疎結合
  - 高い拡張性
  - リアルタイム処理

cons:
  - イベントフローの複雑さ
  - デバッグの困難さ
  - 最終一貫性

use_cases:
  - リアルタイムシステム
  - 非同期処理が多いシステム
  - マイクロサービス間の通信
```

### Clean/Onion Architecture

```yaml
structure:
  /domain: # ドメイン層（中心）
    /entities:
    /value-objects:
  /application: # アプリケーション層
    /use-cases:
    /interfaces:
  /infrastructure: # インフラ層（外側）
    /persistence:
    /external-services:
  /presentation: # プレゼンテーション層

pros:
  - ドメインロジックの独立性
  - テストが容易
  - 依存関係の明確化

cons:
  - 初期設定の複雑さ
  - 抽象化のオーバーヘッド
  - 学習曲線

use_cases:
  - ドメインが複雑なシステム
  - 長期的なメンテナンス
  - DDDの実践
```

### Hexagonal Architecture

```yaml
structure:
  /domain: # ドメイン
  /ports: # ポート（インターフェース）
    /inbound:
    /outbound:
  /adapters: # アダプター（実装）
    /inbound:
      /rest:
      /grpc:
    /outbound:
      /database:
      /external-api:

pros:
  - 高い柔軟性
  - 技術的詳細の分離
  - テストのしやすさ

cons:
  - 概念の理解が必要
  - ボイラープレートコード
  - 小規模プロジェクトには過剰

use_cases:
  - 複数の入出力チャネル
  - 技術スタックの変更可能性
  - ポートフォリオシステム
```

### Serverless Architecture

```yaml
structure:
  /functions: # Lambda関数
    /api: # API関数
    /workers: # バックグラウンド処理
    /triggers: # イベントトリガー
  /infrastructure: # IaC
    /terraform:
    /cloudformation:

pros:
  - 自動スケーリング
  - コスト効率
  - 運用負荷の軽減

cons:
  - ベンダーロックイン
  - コールドスタート
  - ローカル開発の困難さ

use_cases:
  - イベント駆動処理
  - 不定期なワークロード
  - APIバックエンド
```

### Parasol V3-V4 Hybrid

```yaml
structure:
  /capabilities: # V3.0の能力階層
    /L1-strategic:
    /L2-tactical:
    /L3-operational:
      /operations: # 子要素として操作
  /value-streams: # V4の価値ストリーム
  /bounded-contexts: # 統合されたBC

pros:
  - V3.0の正しい理解を反映
  - V4のWHAT-HOW構造
  - トップダウンとボトムアップの統合

cons:
  - 概念の複雑さ
  - 移行の手間
  - 学習コスト

use_cases:
  - 既存V3プロジェクトの移行
  - 価値駆動開発
  - エンタープライズシステム
```

### CQRS + Event Sourcing

```yaml
structure:
  /command: # コマンド側
    /handlers:
    /aggregates:
  /query: # クエリ側
    /handlers:
    /projections:
  /events: # イベントストア
    /store:
    /snapshots:

pros:
  - 読み書きの最適化
  - 完全な監査ログ
  - 時系列データの再現

cons:
  - 実装の複雑さ
  - 最終一貫性
  - ストレージ要件

use_cases:
  - 監査が重要なシステム
  - 読み書きの負荷が異なる
  - イベントドリブンシステム
```

## 比較フレームワーク

### 評価基準

```yaml
criteria:
  complexity: # 実装の複雑さ (1-5)
  scalability: # スケーラビリティ (1-5)
  maintainability: # 保守性 (1-5)
  testability: # テスト容易性 (1-5)
  performance: # パフォーマンス (1-5)
  flexibility: # 柔軟性 (1-5)
  learning_curve: # 学習曲線 (1-5, 低いほど良い)
  operational_overhead: # 運用負荷 (1-5, 低いほど良い)
```

### 比較マトリックス

| Architecture | Complexity | Scalability | Maintainability | Testability | Performance | Flexibility | Learning | Ops Overhead |
|--------------|------------|-------------|-----------------|-------------|-------------|-------------|----------|--------------|
| Monolithic | 2 | 2 | 3 | 3 | 4 | 2 | 2 | 2 |
| Microservices | 5 | 5 | 3 | 4 | 4 | 5 | 4 | 5 |
| Event-Driven | 4 | 5 | 3 | 3 | 4 | 5 | 4 | 4 |
| Clean/Onion | 4 | 3 | 5 | 5 | 3 | 4 | 4 | 3 |
| Hexagonal | 4 | 3 | 5 | 5 | 3 | 5 | 4 | 3 |
| Serverless | 3 | 5 | 4 | 3 | 4 | 4 | 3 | 2 |
| Parasol Hybrid | 5 | 4 | 4 | 4 | 3 | 4 | 5 | 4 |
| CQRS+ES | 5 | 4 | 3 | 4 | 4 | 4 | 5 | 4 |

## 実装サンプル

各アーキテクチャで同じ「タスク管理システム」を実装し、比較可能にします。

### 共通要件

```yaml
features:
  - タスクのCRUD操作
  - ユーザー認証
  - タスクの割り当て
  - 進捗追跡
  - 通知機能

api_endpoints:
  - POST /tasks
  - GET /tasks
  - PUT /tasks/:id
  - DELETE /tasks/:id
  - POST /tasks/:id/assign
  - GET /tasks/:id/progress
```

## 切り替えとテスト

### アーキテクチャ間の切り替え

```bash
# 現在のworktreeをリスト
git worktree list

# 特定のアーキテクチャに切り替え
cd ../amplifier-microservices

# テスト実行
python -m pytest tests/

# パフォーマンステスト
python architectures/benchmark.py
```

### 比較レポート生成

```bash
# 全アーキテクチャの比較レポート生成
python architectures/compare.py --all

# 特定の基準で比較
python architectures/compare.py --criteria scalability,performance

# 結果の可視化
python architectures/visualize.py --output comparison.html
```

## ベストプラクティス

1. **独立性の維持**: 各worktreeは独立して動作可能に
2. **共通インターフェース**: 同じAPIを実装して比較可能に
3. **メトリクス収集**: 各アーキテクチャのメトリクスを自動収集
4. **ドキュメント化**: 各アーキテクチャの決定理由を記録
5. **定期的な同期**: mainブランチの変更を各worktreeに反映

## クリーンアップ

```bash
# 特定のworktreeを削除
git worktree remove ../amplifier-monolithic

# 全worktreeを削除
./architectures/cleanup-worktrees.sh

# 不要なブランチを削除
git branch -d arch/monolithic
```

## まとめ

Git worktreeを活用することで、複数のアーキテクチャを並行して実験・比較できます。
各アーキテクチャの長所短所を実際に体験しながら、プロジェクトに最適な選択ができます。