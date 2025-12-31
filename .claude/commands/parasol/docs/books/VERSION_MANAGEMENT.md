# Parasol書籍バージョン管理ガイド

このドキュメントは、Parasol方法論の書籍を複数バージョン管理するための構造とプロセスを定義します。

## バージョン管理構造

### ディレクトリ構成

```
.claude/commands/parasol/docs/books/
├── VERSION_MANAGEMENT.md (このファイル)
├── BOOK_TEMPLATE/              # 新バージョン作成用テンプレート
│   ├── README.md
│   ├── BOOK_DESIGN.md
│   ├── STYLE_GUIDE.md
│   ├── design/                 # 設計書テンプレート
│   ├── part-structure/         # パート構成テンプレート
│   └── tools/                  # 共通ツール
├── parasol-v5.4-modular/       # 現在のバージョン
├── parasol-v5.5/               # 将来のバージョン例
└── parasol-v6.0/               # メジャーバージョン例
```

## バージョン番号体系

### セマンティックバージョニング適用

```
vX.Y.Z-variant

X = メジャーバージョン（大規模な方法論の変更）
Y = マイナーバージョン（新フェーズ追加、重要な改善）
Z = パッチバージョン（誤字修正、小規模な改善）
variant = バリアント（modular, compact, executive等）
```

### バージョン例

- `v5.4-modular`: モジュラー設計版（現在）
- `v5.4-compact`: 簡略版
- `v5.5-modular`: 新機能追加版
- `v6.0-modular`: 次世代版

## 新バージョン作成プロセス

### 1. バージョン企画

```markdown
# VERSION_PLAN_v5.5.md

## 変更概要
- 追加されるフェーズ/章
- 更新される内容
- 削除される内容
- 対象読者の変更

## 影響分析
- 既存ユーザーへの影響
- 移行パス
- 互換性考慮事項
```

### 2. テンプレートからの初期化

```bash
# 新バージョンディレクトリ作成
cp -r BOOK_TEMPLATE/ parasol-v5.5/

# バージョン固有の設定
cd parasol-v5.5/
# VERSION_CONFIG.ymlを編集
```

### 3. VERSION_CONFIG.yml

```yaml
version: "5.5"
variant: "modular"
base_version: "5.4"  # ベースとなるバージョン
status: "development"  # development, beta, stable, deprecated

metadata:
  release_date: "2025-06-01"
  authors: ["Original Author", "Contributor"]
  language: "ja"
  
changes_from_base:
  added:
    - "Phase 8: AI統合"
    - "Chapter 39: 機械学習との融合"
  modified:
    - "Chapter 13: ZIGZAGプロセス改良"
  removed:
    - "Appendix C: 廃止予定ツール"

compatibility:
  backward_compatible: true
  migration_required: false
  breaking_changes: []
```

## バージョン間の差分管理

### 1. 変更追跡

```markdown
# CHANGELOG_v5.4_to_v5.5.md

## 追加
- Chapter 39: 機械学習との融合
- 付録F: AI/MLツールカタログ

## 変更
- Chapter 13: ZIGZAGプロセスにAI支援を追加
- Chapter 20: ドメインモデリングでのLLM活用

## 削除
- 付録C: レガシーツールリファレンス
```

### 2. 移行ガイド

```markdown
# MIGRATION_GUIDE_v5.4_to_v5.5.md

## 読者向け移行ガイド

### 主要な変更点
1. AI/ML統合の章が追加
2. ZIGZAGプロセスが拡張

### 学習パス
- 既存読者: Chapter 39から開始
- 新規読者: 通常の順序で学習
```

## バージョン管理ツール

### 1. バージョン比較ツール

```python
# tools/version_compare.py

def compare_versions(v1_path: str, v2_path: str):
    """
    2つのバージョン間の差分を分析
    """
    # 章構成の比較
    # 内容の差分
    # 図表の変更
    # コード例の更新
```

### 2. バージョン生成スクリプト

```bash
#!/bin/bash
# tools/create_new_version.sh

VERSION=$1
BASE_VERSION=$2
VARIANT=$3

# テンプレートからコピー
cp -r BOOK_TEMPLATE/ parasol-v${VERSION}-${VARIANT}/

# 基本バージョンから継承
./inherit_from_base.py $BASE_VERSION $VERSION

# 設定ファイル生成
./generate_config.py $VERSION $VARIANT
```

## 並行バージョン管理

### アクティブバージョン

同時に以下のバージョンを維持：

1. **Stable版**: 本番利用（例: v5.4）
2. **Beta版**: 次期リリース候補（例: v5.5-beta）
3. **Development版**: 開発中（例: v6.0-dev）

### バージョン状態

```yaml
# VERSIONS_STATUS.yml

versions:
  - version: "5.4-modular"
    status: "stable"
    support_until: "2026-12-31"
    
  - version: "5.5-modular"
    status: "beta"
    expected_stable: "2025-06-01"
    
  - version: "6.0-modular"
    status: "development"
    expected_beta: "2025-12-01"
```

## 品質保証

### バージョン別品質チェック

```markdown
# 各バージョンで必須
- [ ] 全章の品質レビュー完了
- [ ] 一貫性チェック合格
- [ ] コード例の動作確認
- [ ] 図表の整合性確認
- [ ] 用語集の更新
- [ ] 索引の再生成
```

### 自動化テスト

```python
# tests/version_tests.py

class VersionQualityTests:
    def test_chapter_structure(self, version):
        """各章が必須セクションを含むか確認"""
        
    def test_code_examples(self, version):
        """コード例が実行可能か確認"""
        
    def test_cross_references(self, version):
        """相互参照の整合性確認"""
```

## エージェント設定

### parasol-version-manager（新規エージェント案）

```markdown
# .claude/agents/parasol-version-manager.md

目的: Parasol書籍の複数バージョン管理を支援

機能:
- 新バージョンの初期化
- バージョン間の差分分析
- 移行ガイドの生成
- 品質チェックの実行
```

## 次のステップ

1. **BOOK_TEMPLATE/の作成**
   - 共通構造の抽出
   - テンプレート化
   - ツールの整備

2. **現行版の整理**
   - v5.4-modularの最終化
   - アーカイブの整理
   - ベースラインの確立

3. **次期バージョンの企画**
   - v5.5の変更内容検討
   - ロードマップ作成
   - チーム体制の検討

---

最終更新: 2025-12-29
用途: Parasol書籍の持続的な進化と管理