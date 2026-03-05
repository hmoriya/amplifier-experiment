# parasol5 Project-Specific Extensions

プロジェクト固有のカスタマイズ・拡張用ディレクトリです。

## 方針

- `_project/` 配下はプロジェクト固有。コア更新時にも上書きされません
- コアコマンドの動作を変えたい場合は `overrides/` に同名ファイルを配置
- プロジェクト固有のパターンや知見は `knowledge/` に蓄積

## Structure

```
_project/
├── README.md              # このファイル
├── knowledge/             # プロジェクト固有のナレッジ
│   ├── patterns/          # 発見した設計パターン
│   ├── decisions/         # アーキテクチャ判断記録
│   └── learnings/         # 得られた知見
├── overrides/             # コアコマンドの上書き・拡張
└── outputs/               # プロジェクト固有の成果物テンプレート
```

## コア更新手順

```bash
# _project/ を保持したままコアを更新
rsync -av --exclude='_project/' <source>/parasol5/ .claude/commands/parasol5/
```

## ナレッジ還元

プロジェクトで得た知見が汎用的であれば、コア側の `_knowledge/` への還元を検討してください。
