# Parasol書籍テンプレート

このディレクトリは、新しいバージョンのParasol書籍を作成するためのテンプレートです。

## テンプレート構造

```
BOOK_TEMPLATE/
├── README.md               # このファイル
├── VERSION_CONFIG.yml      # バージョン設定
├── BOOK_DESIGN.md         # 書籍設計書
├── STYLE_GUIDE.md         # スタイルガイド
├── CHAPTER_TEMPLATE.md    # 章テンプレート
├── config/                # 設定ファイル
│   ├── agents.yml         # エージェント設定
│   ├── quality.yml        # 品質基準
│   └── structure.yml      # 構造定義
├── design/                # 設計書
│   ├── DESIGN_TEMPLATE.md
│   └── examples/
├── part-structure/        # パート構成
│   ├── part1-template/
│   ├── part2-template/
│   └── ...
└── tools/                 # 共通ツール
    ├── chapter_generator.py
    ├── quality_checker.py
    └── version_migrator.py
```

## 使用方法

### 1. 新バージョンの作成

```bash
# テンプレートをコピー
cp -r BOOK_TEMPLATE/ parasol-vX.Y-variant/

# 設定ファイルを編集
cd parasol-vX.Y-variant/
vim VERSION_CONFIG.yml
```

### 2. バージョン設定

VERSION_CONFIG.ymlを編集：

```yaml
version: "X.Y"
variant: "modular|compact|executive"
base_version: "5.4"  # 継承元
status: "development"
```

### 3. 初期化スクリプトの実行

```bash
# Python環境で実行
python tools/initialize_version.py
```

## カスタマイズポイント

### 必須カスタマイズ

1. **VERSION_CONFIG.yml** - バージョン情報
2. **BOOK_DESIGN.md** - 対象読者、目的、構成
3. **part-structure/** - 章構成

### オプショナル

1. **STYLE_GUIDE.md** - 特別なスタイル要件
2. **config/agents.yml** - カスタムエージェント設定
3. **tools/** - バージョン固有のツール

## 品質チェックリスト

新バージョン作成時の確認事項：

- [ ] バージョン番号の一貫性
- [ ] ベースバージョンとの互換性確認
- [ ] 全必須ファイルの存在
- [ ] 設定ファイルの妥当性
- [ ] ツールの動作確認

## サポート

問題や質問がある場合は、VERSION_MANAGEMENT.mdを参照してください。