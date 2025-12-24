# Parasol V5 書籍ディレクトリ構成

## 整理完了報告（2025-12-19）

docsディレクトリ下の書籍関連ファイルを、`books/`ディレクトリに整理しました。

## 新しいディレクトリ構造

```
docs/
├── books/                              # 全書籍の統合ディレクトリ
│   ├── README.md                       # 書籍コレクション概要
│   │
│   ├── parasol-v5-complete-guide/      # Parasol V5 完全ガイド
│   │   ├── README.md                   # 15章構成の包括的ガイド
│   │   ├── part1-foundation/           # 第I部：基礎編
│   │   ├── part2-understanding/        # 第II部：理解編
│   │   ├── part3-practice/             # 第III部：実践編
│   │   ├── part4-advanced/             # 第IV部：発展編
│   │   └── appendices/                 # 付録
│   │
│   ├── good-design-book/               # 「良い設計とは何か」
│   │   ├── README.md                   # 価値駆動設計の探求
│   │   ├── good-design-book-proposal.md
│   │   ├── part1-redefining/           # 執筆済み章
│   │   └── 各種企画・構成ファイル
│   │
│   ├── v5-agile-guide/                 # アジャイル実践ガイド（初版）
│   │   ├── README.md                   # V5×アジャイル統合
│   │   ├── part1-foundation/           # 第1部原稿
│   │   ├── v5_agile_guide_part1.html  # 生成済みHTML
│   │   └── v5_agile_guide_part1.pdf   # 生成済みPDF
│   │
│   └── v5-agile-guide-revised/         # アジャイルガイド（改訂版）
│       ├── README.md                   # 原点回帰アプローチ
│       ├── agile-value-research.md     # リサーチ結果
│       ├── part1-complete.md           # 第1部完全版
│       ├── part1-agile-value-guide.html
│       └── part1-agile-value-guide.pdf
```

## その他のディレクトリ（書籍以外）

- `commands/` - CLIコマンドリファレンス
- `guides/` - 実装ガイド・仕様書
- `philosophy/` - 哲学・設計思想
- `reference/` - リファレンス文書
- `value-system/` - 価値トレーサビリティシステム

## 主な変更点

1. **統合管理**: すべての書籍を`books/`ディレクトリに集約
2. **明確な分離**: 各書籍ごとに独立したディレクトリ
3. **README追加**: 各書籍ディレクトリにREADMEを配置
4. **一貫性**: ファイル命名規則の統一

## メリット

- 書籍の種類と内容が一目で分かる
- 各書籍の進捗管理が容易
- 新しい書籍の追加が簡単
- ビルド・生成プロセスの独立性

## 今後の展開

1. 各書籍の執筆継続
2. 統一的な生成スクリプトの作成
3. 書籍間の相互参照の整理
4. オンライン公開の準備