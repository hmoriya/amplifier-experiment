# Parasol V5 書籍生成ツール集

このディレクトリには、Parasol V5関連書籍を生成するためのスクリプトが整理されています。

## 🔧 メイン生成スクリプト

### 各書籍専用の生成ツール

| スクリプト | 対象書籍 | 説明 |
|-----------|---------|------|
| `generate_parasol_book.py` | V5完全ガイド | 15章構成の包括的ガイドを生成 |
| `generate_good_design_book_part1.py` | 良い設計とは何か | 価値駆動設計書籍の第1部を生成 |
| `generate_v5_agile_guide.py` | アジャイルガイド改訂版 | 原点回帰アプローチの改訂版を生成 |
| `generate_v5_agile_guide_part1.py` | アジャイルガイド初版 | V5×アジャイル統合ガイドを生成 |

### 汎用生成ツール

- `generate_book_with_diagrams.py` - 図表対応の汎用書籍生成
- `generate_book_simple.py` - シンプルな書籍生成

### PDF変換ツール

- `convert_v5_agile_guide_to_pdf.py` - HTML→PDF変換（Chrome使用）

## 📁 ディレクトリ構成

```
book-generators/
├── README.md                         # このファイル
├── tests/                           # テストスクリプト
│   ├── test_book_with_diagrams.py
│   ├── test_converter.py
│   └── ...
├── 各種生成スクリプト
└── 各種変換ユーティリティ
```

## 🚀 使用方法

### 1. V5完全ガイドの生成

```bash
cd /path/to/amplifier-experiment
python3 .claude/commands/parasol/book-generators/generate_parasol_book.py
```

生成物：`generated_books/parasol-v5-book.html`

### 2. 良い設計書籍（第1部）の生成

```bash
python3 .claude/commands/parasol/book-generators/generate_good_design_book_part1.py
```

生成物：`generated_books/good-design-book-part1.html`

### 3. アジャイルガイド改訂版の生成

```bash
python3 .claude/commands/parasol/book-generators/generate_v5_agile_guide.py
```

生成物：`.claude/commands/parasol/docs/books/v5-agile-guide-revised/part1-agile-value-guide.html`

### 4. PDF変換

```bash
python3 .claude/commands/parasol/book-generators/convert_v5_agile_guide_to_pdf.py
```

## 📝 各スクリプトの特徴

### generate_book_with_diagrams.py
- Mermaid図表のHTML/CSS変換対応
- ASCII図表の整形対応
- 章ごとの自動分割
- 目次自動生成

### generate_parasol_book.py
- 15章構成の完全ガイド専用
- 付録を含む全体構成対応
- プログレス管理統合

### generate_good_design_book_part1.py
- 価値駆動設計に特化
- 実例カタログ連携
- 段階的執筆対応

### generate_v5_agile_guide.py
- 改訂版専用の構成
- アジャイル原点回帰テーマ
- 共感的アプローチの文体

## 🛠️ 開発者向け情報

### 新しい書籍生成スクリプトの作成

1. 基本テンプレートとして`generate_book_simple.py`を参照
2. 書籍固有の設定を追加
3. `parasol_book_generator/`の共通エンジンを活用

### 共通エンジンの場所

```
/amplifier-experiment/parasol_book_generator/
├── generator.py         # メイン生成エンジン
├── diagram_generator.py # 図表処理
└── converters.py       # 変換ユーティリティ
```

## 📊 生成物の出力先

- HTML: `generated_books/` または各書籍ディレクトリ
- PDF: 各書籍ディレクトリ内

## 🔄 メンテナンス

- 定期的に未使用のスクリプトをアーカイブ
- 新機能は共通エンジンに追加
- 書籍固有の処理は各生成スクリプトに実装