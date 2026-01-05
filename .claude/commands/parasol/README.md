# Parasol V5 Framework - ディレクトリ構成ガイド

**バージョン**: V5.4
**最終更新**: 2025-01-05

---

## 概要

Parasol V5は価値駆動のシステム設計フレームワークです。このディレクトリには、フレームワークのコマンド、概念、リファレンス、およびプロジェクト資産が体系的に整理されています。

---

## ディレクトリ構成

```
parasol/
│
├── 📋 ルートファイル
│   ├── VERSION                    # 現在のバージョン（V5.4）
│   ├── CHANGELOG-V5.4.md          # バージョン変更履歴
│   ├── PARASOL_SHARED_CONTEXT.md  # 共有コンテキスト定義
│   └── README.md                  # このファイル
│
├── 🎯 commands/                   # スラッシュコマンド定義
├── 💡 concepts/                   # 概念・哲学文書
├── 📚 reference/                  # リファレンス文書
├── 📖 docs/                       # 詳細ドキュメント
├── 🏗️ projects/                   # プロジェクトデータ
│
├── 🔧 _commands-v5/               # V5コマンド実装
├── 🧠 _capability-knowledge/      # ケイパビリティ知識ベース
├── 📐 _patterns/                  # 設計パターン
├── 💻 _software-design-reference/ # ソフトウェア設計リファレンス
└── 📕 book-generators/            # 書籍生成ツール
```

---

## ディレクトリ詳細

### 📋 ルートファイル

| ファイル | 目的 | 更新頻度 |
|---------|------|---------|
| `VERSION` | 現在のParasolバージョン | リリース時 |
| `CHANGELOG-V5.4.md` | 変更履歴・リリースノート | 機能追加時 |
| `PARASOL_SHARED_CONTEXT.md` | エージェント間共有コンテキスト | 必要時 |
| `README.md` | 構成ガイド（このファイル） | 構造変更時 |

---

### 🎯 commands/ - スラッシュコマンド

Claude Codeで実行可能なスラッシュコマンドの定義。

| ファイル | コマンド | 説明 |
|---------|---------|------|
| `explore.md` | `/parasol:explore` | 3軸価値分解探索（value/business/hybrid） |
| `domain-language.md` | `/parasol:domain-language` | ドメイン言語定義 |

**命名規則**: `{コマンド名}.md`

---

### 💡 concepts/ - 概念・哲学

Parasolの根本的な概念と設計哲学。

| ファイル | 内容 |
|---------|------|
| `PARASOL-CONCEPT.md` | Parasolとは何か（日傘のメタファー） |
| `PHILOSOPHY.md` | 設計哲学・判断の羅針盤 |
| `DDD-VS-PARASOL-ANALYSIS.md` | DDDとParasolの比較分析 |

**命名規則**: `{概念名}.md`（大文字推奨）

---

### 📚 reference/ - リファレンス

技術的なリファレンス文書・ガイド。

| ファイル | 内容 |
|---------|------|
| `overview-v5.md` | V5全体概要 |
| `architecture-overview.md` | アーキテクチャ概要 |
| `value-methodology.md` | 価値方法論（VL/VS/VMS） |
| `value-analysis-flow.md` | 価値分析フロー詳細 |
| `domain-language-guide.md` | ドメイン言語ガイド |
| `project-detection.md` | プロジェクト検出ロジック |
| `parasol-framework-reference.md` | フレームワーク総合リファレンス |

**命名規則**: `{トピック名}.md`（小文字ハイフン区切り）

---

### 📖 docs/ - 詳細ドキュメント

書籍、ガイド、詳細解説など。

```
docs/
├── books/                    # 書籍コンテンツ
│   ├── parasol-v5-complete-guide/   # V5完全ガイド
│   ├── parasol-v5.4-modular/        # V5.4モジュラー版
│   └── good-design-book/            # 良い設計の本
├── guides/                   # 実践ガイド
├── philosophy/               # 哲学詳細
└── examples/                 # 事例・サンプル
```

---

### 🏗️ projects/ - プロジェクトデータ

実際のプロジェクトで生成されるParasolアーティファクト。

```
projects/
└── {project-name}/
    ├── context.md           # Phase 0-1: 組織コンテキスト
    ├── value-streams.md     # Phase 2: 価値ストリーム
    ├── capabilities.md      # Phase 3: ケイパビリティ
    ├── architecture.md      # Phase 4: アーキテクチャ
    └── ...
```

---

### 🔧 _commands-v5/ - V5コマンド実装

内部コマンド実装。`_`プレフィックスは内部ファイルを示す。

---

### 🧠 _capability-knowledge/ - ケイパビリティ知識

業界別・機能別のケイパビリティパターン知識ベース。

---

### 📐 _patterns/ - 設計パターン

再利用可能な設計パターン集。

---

### 💻 _software-design-reference/ - ソフトウェア設計

DDDパターン、アーキテクチャパターンなどの技術リファレンス。

---

### 📕 book-generators/ - 書籍生成

書籍コンテンツの自動生成ツール。

---

## 命名規約

### ディレクトリ

| プレフィックス | 意味 | 例 |
|---------------|------|-----|
| (なし) | 公開・ユーザー向け | `commands/`, `concepts/` |
| `_` | 内部・システム用 | `_patterns/`, `_commands-v5/` |

### ファイル

| パターン | 用途 | 例 |
|---------|------|-----|
| `UPPER-CASE.md` | 概念・重要文書 | `PHILOSOPHY.md` |
| `lower-case.md` | 通常文書 | `overview-v5.md` |
| `kebab-case.md` | 複合名 | `value-analysis-flow.md` |

---

## ファイル追加ガイドライン

### 新しいコマンドを追加する場合

1. `commands/` に `{command-name}.md` を作成
2. フロントマターに `description` を記述
3. `_commands-v5/` に実装詳細を配置（必要な場合）

### 新しい概念文書を追加する場合

1. `concepts/` に `{CONCEPT-NAME}.md` を作成
2. Parasolの根本的な「なぜ」に答える内容

### 新しいリファレンスを追加する場合

1. `reference/` に `{topic-name}.md` を作成
2. 技術的な「どのように」に答える内容

---

## 関連リソース

- **エージェント**: `.claude/agents/axiomatic-design-advisor.md` - 公理的設計アドバイザー
- **書籍生成**: `amplifier/parasol_book_v54/` - 書籍生成モジュール
- **Parasolフェーズエージェント**: `.claude/agents/parasol-phase*.md`

---

## バージョン履歴

| バージョン | 日付 | 変更内容 |
|-----------|------|---------|
| V5.4 | 2025-01 | ディレクトリ構造整理、公理的設計統合 |
| V5.3 | 2024-12 | モジュラー書籍構造 |
| V5.0 | 2024-11 | 初期V5リリース |
