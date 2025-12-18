# Book to PDF Module

Parasol V5 書籍をPDFに変換するモジュール。

## 概要

Markdownで書かれたParasol V5の書籍を、美しくフォーマットされたPDFに変換します。

### 主な機能

- **章立て構造の保持**: 部・章・節の階層を維持
- **日本語フォント対応**: 美しい日本語組版
- **コードハイライト**: シンタックスハイライト付きコードブロック
- **図表対応**: Mermaidダイアグラムの自動変換
- **目次自動生成**: クリック可能な目次
- **ページ番号**: 章ごとのページ番号
- **カスタムスタイル**: Parasol V5ブランディング

## インストール

```bash
cd modules/book-to-pdf
uv pip install -e .
```

### 追加要件

日本語フォントのインストール：
```bash
# macOS
brew install font-noto-sans-cjk-jp

# Ubuntu/Debian
sudo apt-get install fonts-noto-cjk

# Windows
# Noto Sans JPをダウンロードしてインストール
```

## 使用方法

### 全書籍のPDF生成

```bash
book2pdf convert
```

デフォルトで以下のファイルが生成されます：
- `output/parasol-v5-complete-guide.pdf` - 完全版
- `output/parasol-v5-part1-foundation.pdf` - 第I部
- `output/parasol-v5-part2-understanding.pdf` - 第II部
- `output/parasol-v5-part3-practice.pdf` - 第III部
- `output/parasol-v5-part4-advanced.pdf` - 第IV部

### 特定の部分のみ生成

```bash
# 特定の部のみ
book2pdf convert --part 1

# 特定の章のみ
book2pdf convert --chapter 5

# カスタム出力
book2pdf convert --output my-book.pdf
```

### スタイルオプション

```bash
# A4サイズ（デフォルト）
book2pdf convert --page-size A4

# レターサイズ
book2pdf convert --page-size letter

# フォントサイズ調整
book2pdf convert --font-size 11

# 行間調整
book2pdf convert --line-height 1.8
```

### プレビューモード

```bash
# HTMLプレビュー（高速確認用）
book2pdf preview

# 指定ポートで起動
book2pdf preview --port 8080
```

## 高度な使用法

### カスタムテンプレート

```bash
# カスタムCSSを使用
book2pdf convert --css custom-style.css

# カスタムヘッダー/フッター
book2pdf convert --header-template header.html
```

### 複数フォーマット出力

```bash
# PDF + HTML + EPUB
book2pdf export --formats pdf,html,epub
```

### バッチ処理

```yaml
# batch-config.yaml
outputs:
  - name: complete-guide
    parts: all
    output: parasol-v5-complete.pdf
    
  - name: quick-reference
    chapters: [2, 5, 8]
    output: parasol-v5-quick-ref.pdf
    
  - name: implementation-guide
    parts: [3, 4]
    output: parasol-v5-implementation.pdf
```

```bash
book2pdf batch --config batch-config.yaml
```

## 出力例

生成されるPDFの特徴：

1. **表紙**: タイトル、バージョン、生成日付
2. **目次**: クリック可能なナビゲーション
3. **本文**: 
   - 見出しの階層構造
   - コードブロックのシンタックスハイライト
   - 表の美しい組版
   - 図表の自動配置
4. **付録**: 用語集、参考文献
5. **索引**: キーワード索引（オプション）

## 技術仕様

### 使用ライブラリ

- **WeasyPrint**: HTML/CSSからPDF生成
- **Markdown**: Markdownパース
- **Pygments**: シンタックスハイライト
- **PyYAML**: 設定ファイル処理
- **Click**: CLI インターフェース

### ファイル構造

```
book-to-pdf/
├── templates/
│   ├── base.html
│   ├── cover.html
│   └── toc.html
├── styles/
│   ├── default.css
│   ├── print.css
│   └── syntax.css
└── converters/
    ├── markdown_converter.py
    ├── mermaid_converter.py
    └── pdf_generator.py
```

## カスタマイズ

### CSS変数

```css
/* カスタマイズ可能な変数 */
:root {
  --primary-color: #2C3E50;
  --accent-color: #3498DB;
  --font-family-main: 'Noto Sans JP', sans-serif;
  --font-family-code: 'Source Code Pro', monospace;
  --base-font-size: 10pt;
  --line-height: 1.6;
  --margin-top: 2cm;
  --margin-bottom: 2cm;
  --margin-inner: 3cm;
  --margin-outer: 2cm;
}
```

### メタデータ設定

```yaml
# metadata.yaml
title: "Parasol V5 完全ガイド"
subtitle: "価値駆動の実践的システム設計"
author: "Parasol Team"
version: "1.0.0"
language: ja
keywords:
  - Parasol
  - V5
  - システム設計
  - 価値駆動
```

## トラブルシューティング

### 日本語が表示されない

```bash
# フォント一覧を確認
book2pdf check-fonts

# フォントパスを指定
book2pdf convert --font-path /path/to/fonts
```

### メモリ不足エラー

```bash
# チャンクサイズを調整
book2pdf convert --chunk-size 50

# 画像品質を下げる
book2pdf convert --image-quality 85
```

### Mermaidダイアグラムが表示されない

```bash
# Mermaid CLIをインストール
npm install -g @mermaid-js/mermaid-cli

# パスを確認
book2pdf check-dependencies
```

## ライセンス

MIT License