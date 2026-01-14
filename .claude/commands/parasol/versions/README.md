# Parasol バージョン別ドキュメント

このディレクトリには、Parasolの各バージョンの設計ドキュメントが整理されています。

## ディレクトリ構成

```
versions/
├── v5.4/
│   └── CHANGELOG.md          # V5.4 リリースノート
├── v5.5/
│   └── CHANGELOG.md          # V5.5 リリースノート
├── v5.6/
│   ├── CHANGELOG.md          # V5.6 リリースノート
│   └── SPECIFICATION.md      # V5.6 仕様書
└── v5.7/
    ├── CHANGELOG.md          # V5.7 リリースノート
    └── DESIGN-PRINCIPLES.md  # V5.7 設計原則
```

## 現在のバージョン

**V5.7** - Context-Driven Value Architecture

詳細は `../VERSION` ファイルを参照してください。

## 各バージョンの概要

| バージョン | コードネーム | 主な特徴 |
|-----------|-------------|---------|
| V5.4 | - | Axiomatic Design統合、モジュラー書籍構造 |
| V5.5 | - | TVDC 4分類、VCI導入、Phase 2-3価値継承 |
| V5.6 | 5W1H Value Architecture | BizBOKベース5W1H、Value Component強化 |
| V5.7 | Context-Driven Value Architecture | 価値継承構造=VStream構成、価値統合アーキテクチャ |

## バージョン間の関係

```
V5.4 (基盤)
  ↓ 拡張
V5.5 (TVDC/VCI)
  ↓ 拡張
V5.6 (5W1H)
  ↓ 拡張
V5.7 (価値継承構造) ← 現在
```

各バージョンは後方互換性を維持しています。
