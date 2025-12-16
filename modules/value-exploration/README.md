# Value Exploration Module

Parasol V5 価値駆動設計のための価値探索・発見モジュール。

## 概要

ビジネス価値を対話的に発見し、構造化するためのCLIツールです。

### 主な機能

- **対話型価値探索**: ガイド付き質問で価値を発見
- **九次元分析**: Impact, Velocity, Messaging, Reach, Sentiment, Metrics, Balance, Depth, Foundation
- **価値階層化**: VL1-VL3 の3層構造で価値を整理
- **価値ストリーム**: 複数の価値を連結してフローを定義

## インストール

```bash
cd modules/value-exploration
uv pip install -e .
```

## 使用方法

### 価値探索セッション

```bash
value-explore discover
```

対話形式でビジネス・ステークホルダー・運用の観点から価値を発見します。

### 九次元分析

```bash
value-explore analyze VAL-001
```

特定の価値を9つの次元で評価します：

| 次元 | 説明 |
|------|------|
| Impact | 影響力 - どれだけの変化を生むか |
| Velocity | 速度 - どれだけ速く価値を届けるか |
| Messaging | 伝達力 - 価値をどう伝えるか |
| Reach | 到達力 - どこまで価値を広げるか |
| Sentiment | 感情価値 - どんな感情を生むか |
| Metrics | 測定可能性 - 価値をどう測るか |
| Balance | 均衡 - 各価値のバランス |
| Depth | 深度 - 価値の深さと持続性 |
| Foundation | 基盤 - 価値の土台の強さ |

### 価値ストリーム作成

```bash
value-explore stream
```

複数の価値を連結して価値ストリームを定義します。

### 価値表示

```bash
value-explore show
```

発見した価値を階層形式で表示します。

### エクスポート

```bash
value-explore export --format yaml
value-explore export --format json
```

## 出力形式

```yaml
values:
  - id: VAL-001
    name: 24時間以内配送
    description: 注文から24時間以内に商品を届ける
    level: 1  # VL1
    current_state: 72時間
    target_state: 24時間
    metrics:
      - 平均配送時間
      - 配送成功率
    nine_dimensions:
      Impact: 5
      Velocity: 4
      # ...

streams:
  - id: VS-001
    name: 顧客満足向上ストリーム
    values: [VAL-001, VAL-002, VAL-003]
```

## Parasol V5 との連携

このモジュールで発見した価値は、Parasol V5 の以下のフェーズで活用できます：

- **Phase 2 (Value)**: 価値定義の入力として使用
- **Phase 3 (Capabilities)**: 価値からケイパビリティを導出
- **価値トレーサビリティ**: 価値の追跡基盤として機能

## ライセンス

MIT License
