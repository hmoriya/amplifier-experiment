# Parasol5 - DDD/Architecture Command Package

**Parasol V5.8 DDD・設計コマンド - ポータブルパッケージ**

## Overview

ケイパビリティ分解からアーキテクチャ設計までのDDD設計コマンド群（Phase 3-5）。
`value5`（価値空間コマンド）と組み合わせて使用します。
実装（Phase 6-7）は GitHub spec-kit 等の別ツールを使用します。

## Setup

```bash
# value5と組み合わせて使用（推奨）
cp -r value5/ parasol5/ <target-project>/.claude/commands/

# parasol5単体（value5の成果物が既にある場合）
cp -r parasol5/ <target-project>/.claude/commands/parasol5/
```

## Commands

### Capability（ケイパビリティ分解）- Phase 3

| Command | Description |
|---------|-------------|
| `/parasol5:capability:decompose` | CL1-CL3 capability decomposition |

### Architecture（アーキテクチャ設計）- Phase 4-5

| Command | Description |
|---------|-------------|
| `/parasol5:architecture:application` | Application architecture design |
| `/parasol5:architecture:software` | Software design (domain language, API, DB) |

### Milestone（マイルストーン管理）

| Command | Description |
|---------|-------------|
| `/parasol5:milestone:status` | VMS1-VMS5 progress management |
| `/parasol5:milestone:quality-gate` | Quality gate execution |

### Execution（統合実行）

| Command | Description | Scope |
|---------|-------------|-------|
| `/parasol5:execution:quick-start` | Quick project start | Up to VMS1 |
| `/parasol5:execution:full-design` | Full design execution | VMS1-VMS3 |

### Utilities

| Command | Description |
|---------|-------------|
| `/parasol5:utils:help` | Help |
| `/parasol5:utils:status` | Project status |
| `/parasol5:utils:project` | Project management |
| `/parasol5:utils:validate` | Artifact validation |

## Related Package: value5

Value space commands (Phase 0-2):

| Command | Description |
|---------|-------------|
| `/value5:init` | Enterprise URL initial analysis |
| `/value5:context` | Project context establishment |
| `/value5:definition` | Value definition and VS design |
| `/value5:trace` | Value trace recording |
| `/value5:necessity-check` | Structural necessity verification |
| `/value5:imagination-detect` | Imaginary design detection |
| `/value5:inheritance` | Value inheritance check |

## Directory Structure

```
parasol5/
├── README.md
├── VERSION
├── CONTEXT.md
├── capability/
├── architecture/
├── milestone/
├── execution/
├── utils/
└── _knowledge/
    ├── README.md                    # ナレッジベース目次
    ├── capability/                  # ケイパビリティ分解パターン
    ├── software-design/             # ソフトウェア設計（命名, オペレーション）
    ├── philosophy/                  # 設計哲学（ZIGZAG, CL階層, 公理的設計）
    ├── architecture/                # アーキテクチャ参照（API, DB, 統合）
    ├── concepts/                    # 設計コンセプト（DDD, TVDC, BIZBOK）
    ├── diagrams/                    # 構造図（三空間, CL3→BC）
    ├── validators/                  # 品質ゲートバリデータ（YAML）
    ├── reference/                   # フレームワーク参照（公理的設計, VS→CL）
    ├── guides/                      # 設計ガイド（実装, V5総合）
    └── versions/                    # バージョン仕様（V5.6, V5.7）
```

## Migration

| Old | New |
|-----|-----|
| `/parasol:0-init` | `/value5:init` |
| `/parasol:1-context` | `/value5:context` |
| `/parasol:2-value` | `/value5:definition` |
| `/parasol:3-capabilities` | `/parasol5:capability:decompose` |
| `/parasol:4-application` | `/parasol5:architecture:application` |
| `/parasol:5-software` | `/parasol5:architecture:software` |
| `/parasol:6-implementation` | (GitHub spec-kit等を使用) |
| `/parasol:7-platform` | (GitHub spec-kit等を使用) |
