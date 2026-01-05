# Parasol Bundle System

Parasolフレームワークのバンドルシステムは、Amplifierの設計思想を取り入れた柔軟な構成管理を提供します。

## バンドル構造

```
parasol/bundles/
├── base/                    # 基本バンドル
│   └── parasol-base.md
├── phases/                  # フェーズ別バンドル
│   ├── phase1-context.md
│   ├── phase2-value.md
│   └── ...
├── industry/               # 業界別バンドル
│   ├── retail.md
│   ├── finance.md
│   └── manufacturing.md
├── region/                 # 地域別バンドル
│   ├── japan.md
│   ├── us.md
│   └── eu.md
└── approach/              # アプローチ別バンドル
    ├── value-driven.md
    ├── capability-driven.md
    └── platform-driven.md
```

## 使用方法

### 基本的な使用

```bash
# 単一バンドルの使用
parasol --bundle ./bundles/base/parasol-base.md init my-project

# 複数バンドルの組み合わせ
parasol \
  --bundle ./bundles/base/parasol-base.md \
  --bundle ./bundles/industry/retail.md \
  --bundle ./bundles/region/japan.md \
  init retail-japan-project
```

### フェーズ別実行

```bash
# Phase 1のみを実行
parasol --bundle ./bundles/phases/phase1-context.md execute

# 特定業界向けPhase 2
parasol \
  --bundle ./bundles/phases/phase2-value.md \
  --bundle ./bundles/industry/finance.md \
  execute
```

## バンドルの優先順位

後から読み込まれたバンドルが前のバンドルの設定を上書きします：

1. base（基本設定）
2. approach（アプローチ別）
3. industry（業界別）
4. region（地域別）
5. project-specific（プロジェクト固有）

## バンドル作成ガイド

新しいバンドルを作成する際は、以下のテンプレートを使用してください：

```yaml
---
bundle:
  name: parasol-[type]-[name]
  version: 1.0.0
  description: [Description]
  
# 他のバンドルを含める
includes:
  - bundle: ../base/parasol-base.md
  
# 設定の上書き
config:
  phases:
    phase2:
      value_stream_style: [style]
      templates:
        - [template definitions]
        
# エージェントの追加
agents:
  include:
    - parasol:[specific-agent]
---

# Bundle Documentation

[Bundle specific documentation and guidelines]
```