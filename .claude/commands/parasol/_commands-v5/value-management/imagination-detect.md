# parasol:imagination-detect - 想像の設計検出・除去コマンド

## 概要

価値から導かれない「想像の設計」を自動検出し、除去します。エンジニアの思い込み、過剰な将来予測、根拠のない最適化など、構造的必然性を持たない設計を特定し、価値駆動の設計に置き換えます。

## 想像の設計とは

### 典型的なパターン

1. **過剰な抽象化**
   - "将来使うかもしれない"という理由での汎用化
   - 現在の要求を超えた拡張性

2. **早すぎる最適化**
   - 測定されていないパフォーマンス問題への対処
   - 仮想的なスケーラビリティ要求

3. **技術的好奇心駆動**
   - 新技術の採用自体が目的化
   - ビジネス価値と無関係な技術選択

4. **コピー&ペーストアーキテクチャ**
   - 文脈を無視した他システムの模倣
   - "業界標準"の盲目的適用

## コマンド構文

```bash
amplifier parasol:imagination-detect <サブコマンド> [オプション]
```

## サブコマンド

### scan - 想像の設計をスキャン

プロジェクト全体をスキャンして想像の設計を検出します。

```bash
amplifier parasol:imagination-detect scan [--severity <level>] [--output <file>]
```

**オプション:**
- `--severity <level>`: 検出レベル（low, medium, high, critical）
- `--output <file>`: 結果の出力先
- `--pattern <glob>`: スキャン対象のパターン
- `--exclude <glob>`: 除外パターン

**検出例:**
```yaml
検出結果:
  - location: src/utils/SuperGenericFactory.ts
    type: over-abstraction
    severity: high
    reason: "1つの実装に対して3層の抽象化"
    suggestion: "直接実装に置き換え"
    
  - location: src/services/FutureProofAPI.ts
    type: premature-optimization
    severity: medium
    reason: "使用されていないキャッシュレイヤー"
    suggestion: "実際のパフォーマンス問題が発生してから実装"
```

### analyze - 詳細分析

検出された想像の設計を詳細に分析します。

```bash
amplifier parasol:imagination-detect analyze [--id <detection-id>] [--deep]
```

**分析内容:**
1. **影響範囲分析**
   - 影響を受けるコンポーネント
   - 依存関係の把握
   - リファクタリングの複雑度

2. **コスト分析**
   - 維持コスト
   - 複雑性コスト
   - 機会コスト

3. **代替案の提示**
   - シンプルな実装案
   - 段階的移行プラン
   - リスク評価

**出力例:**
```markdown
## 想像の設計分析レポート

### 対象: SuperGenericFactory

**現状の問題:**
- 3層の不必要な抽象化
- 実際の使用は1パターンのみ
- コード理解に30分以上必要

**影響範囲:**
- 直接依存: 5コンポーネント
- 間接依存: 12コンポーネント
- テストコード: 150行

**推奨アクション:**
1. 直接実装への置き換え（推定: 2時間）
2. 既存インターフェースの段階的除去
3. テストの簡素化

**期待効果:**
- コード量: -70%
- 複雑性: -85%
- 保守性: +200%
```

### refactor - 自動リファクタリング

想像の設計を価値駆動の設計に自動的に置き換えます。

```bash
amplifier parasol:imagination-detect refactor [--dry-run] [--interactive] [--backup]
```

**オプション:**
- `--dry-run`: 変更内容のプレビューのみ
- `--interactive`: 対話的に確認しながら実行
- `--backup`: 変更前のバックアップを作成
- `--strategy <name>`: リファクタリング戦略

**リファクタリング戦略:**

1. **simplify** (デフォルト)
   ```bash
   amplifier parasol:imagination-detect refactor --strategy simplify
   ```
   - 不要な抽象化を除去
   - 直接的な実装に置換

2. **gradual**
   ```bash
   amplifier parasol:imagination-detect refactor --strategy gradual
   ```
   - 段階的な移行
   - 後方互換性を維持

3. **aggressive**
   ```bash
   amplifier parasol:imagination-detect refactor --strategy aggressive
   ```
   - 大胆な構造変更
   - 最もシンプルな形へ

### prevent - 予防的チェック

新しいコードが想像の設計を含まないかチェックします。

```bash
amplifier parasol:imagination-detect prevent [--hook] [--ci]
```

**使用例:**

```bash
# Git pre-commitフック
amplifier parasol:imagination-detect prevent --hook

# CI/CDパイプライン
amplifier parasol:imagination-detect prevent --ci --fail-on medium
```

## 検出パターン

### 1. 過剰な抽象化パターン

```yaml
patterns:
  unnecessary_interface:
    description: "単一実装のインターフェース"
    indicators:
      - 実装クラスが1つのみ
      - 将来の拡張計画なし
      - 価値への貢献が不明
      
  abstract_factory_overkill:
    description: "過剰なファクトリーパターン"
    indicators:
      - 生成オブジェクトが固定
      - 設定による分岐なし
      - new演算子で十分
```

### 2. 早すぎる最適化パターン

```yaml
patterns:
  premature_caching:
    description: "根拠のないキャッシュ実装"
    indicators:
      - パフォーマンス測定なし
      - キャッシュヒット率未測定
      - 複雑性の増加が顕著
      
  micro_optimization:
    description: "意味のない微小最適化"
    indicators:
      - 可読性の大幅な低下
      - 測定可能な改善なし
      - 保守コストの増加
```

### 3. 技術駆動パターン

```yaml
patterns:
  tech_for_tech:
    description: "技術自体が目的化"
    indicators:
      - ビジネス価値との関連なし
      - 既存技術で解決可能
      - 学習コストが価値を上回る
      
  resume_driven_development:
    description: "履歴書駆動開発"
    indicators:
      - 不必要に新しい技術
      - チームの習熟度無視
      - 移行コストが不明確
```

## カスタム検出ルール

### ルール定義

```yaml
# .parasol/imagination-rules.yaml
custom_rules:
  - id: no-future-proofing
    name: "将来の保証禁止"
    pattern: "Future|Proof|Eventually|Someday"
    message: "現在の価値に集中してください"
    severity: high
    
  - id: max-abstraction-layers
    name: "抽象化層の制限"
    type: structure
    max_layers: 2
    message: "2層を超える抽象化は想像の産物です"
    
  - id: justify-patterns
    name: "デザインパターンの正当化"
    patterns: [Singleton, Factory, Strategy]
    require: value_trace_reference
    message: "パターン使用には価値への貢献が必要です"
```

### ルールの適用

```bash
# カスタムルールでスキャン
amplifier parasol:imagination-detect scan --rules .parasol/imagination-rules.yaml

# 特定ルールのみ適用
amplifier parasol:imagination-detect scan --only no-future-proofing

# ルールの検証
amplifier parasol:imagination-detect validate-rules
```

## AIアシスト機能

### 自動提案

```bash
# AIによる改善提案
amplifier parasol:imagination-detect suggest --component auth-service

# コード生成
amplifier parasol:imagination-detect generate-alternative --detection-id DET-001
```

### 学習モード

```bash
# なぜそれが想像の設計なのかを説明
amplifier parasol:imagination-detect explain --educational

# チーム向けワークショップモード
amplifier parasol:imagination-detect workshop --interactive
```

## レポートとメトリクス

### 想像度スコア

```bash
# プロジェクトの想像度スコア
amplifier parasol:imagination-detect score

出力例：
プロジェクト想像度スコア: 35/100 (低いほど良い)

内訳:
- 過剰な抽象化: 15pts
- 早すぎる最適化: 10pts
- 技術駆動設計: 10pts

推奨: 20以下を目指しましょう
```

### トレンド分析

```bash
# 時系列での想像度推移
amplifier parasol:imagination-detect trend --days 90

# スプリントごとの分析
amplifier parasol:imagination-detect sprint-analysis
```

## 統合ワークフロー

### 継続的検出

```yaml
# .github/workflows/imagination-check.yml
name: Imagination Detection
on: [push, pull_request]

jobs:
  detect:
    runs-on: ubuntu-latest
    steps:
      - name: Detect Imagination
        run: |
          amplifier parasol:imagination-detect scan --ci
          amplifier parasol:imagination-detect score --fail-above 30
```

### IDE統合

```json
// settings.json
{
  "parasol.imagination-detect": {
    "realtime": true,
    "severity": "medium",
    "autoSuggest": true,
    "explanations": true
  }
}
```

## ベストプラクティス

### 1. 段階的導入

```bash
# Phase 1: 検出のみ
amplifier parasol:imagination-detect scan --report-only

# Phase 2: 新規コードのチェック
amplifier parasol:imagination-detect prevent --new-code

# Phase 3: 既存コードの改善
amplifier parasol:imagination-detect refactor --gradual
```

### 2. チーム教育

```bash
# ワークショップの実施
amplifier parasol:imagination-detect workshop

# 具体例での学習
amplifier parasol:imagination-detect examples --real-world

# ガイドラインの生成
amplifier parasol:imagination-detect generate-guidelines
```

### 3. 例外管理

```yaml
# .parasol/imagination-exceptions.yaml
exceptions:
  - path: src/legacy/**
    reason: "レガシーコードは段階的に改善"
    until: 2024-12-31
    
  - pattern: "**/migrations/**"
    reason: "マイグレーションは歴史的理由で保持"
    permanent: true
```

## 次のステップ

想像の設計を除去したら：

```bash
# マイルストーンへ進行
amplifier parasol:milestone advance

# 価値の再検証
amplifier parasol:value-trace validate
```