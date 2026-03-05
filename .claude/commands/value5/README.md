# Value5 - Value Space Command Package

**Parasol V5.8 価値空間コマンド - ポータブルパッケージ**

## Overview

価値の発見・定義・管理に関わるコマンド群（Phase 0-2 + 価値管理）。
`parasol5`（DDD/設計コマンド）と組み合わせて使用します。

## Setup

```bash
# value5単体で使用
cp -r value5/ <target-project>/.claude/commands/value5/

# parasol5と組み合わせて使用
cp -r value5/ parasol5/ <target-project>/.claude/commands/
```

## Commands

| Command | Description | Phase |
|---------|-------------|-------|
| `/value5:init` | Enterprise URL initial analysis | 0 |
| `/value5:context` | Project context establishment | 1 |
| `/value5:definition` | Value definition and VS design | 2 |
| `/value5:trace` | Value trace recording | - |
| `/value5:necessity-check` | Structural necessity verification | - |
| `/value5:imagination-detect` | Imaginary design detection | - |
| `/value5:inheritance` | Value inheritance check | - |

## Related Package

- **parasol5**: DDD/Architecture commands (Phase 3-5, 設計まで。実装はGitHub spec-kit等を使用)
  - `/parasol5:capability:decompose`
  - `/parasol5:architecture:application`, `/parasol5:architecture:software`
  - `/parasol5:milestone:status`, `/parasol5:milestone:quality-gate`
  - `/parasol5:execution:quick-start`, `/parasol5:execution:full-design`
  - `/parasol5:utils:help`, `/parasol5:utils:status`, `/parasol5:utils:project`, `/parasol5:utils:validate`

## Migration from old commands

| Old | New |
|-----|-----|
| `/parasol:0-init` | `/value5:init` |
| `/parasol:1-context` | `/value5:context` |
| `/parasol:2-value` | `/value5:definition` |

## Directory Structure

```
value5/
├── README.md
├── CONTEXT.md
├── VERSION
├── init.md
├── context.md
├── definition.md
├── trace.md
├── necessity-check.md
├── imagination-detect.md
├── inheritance.md
└── _knowledge/
    └── patterns/
        ├── _axes/
        └── industries/
```
