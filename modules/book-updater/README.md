# Book Updater Module

Parasol V5書籍を最新のコマンドやガイドから自動更新するモジュール。

## 概要

このモジュールは、Parasol V5の書籍コンテンツを最新の実装と同期させ、以下を自動的に更新します：

- V5コマンドの最新仕様を反映
- 実装例を最新のコードに更新
- 新しいパターンやベストプラクティスを追加
- 廃止された機能の削除・更新
- 用語やコンセプトの一貫性確保

## 主な機能

### 1. コンテンツ同期
- **コマンドリファレンス同期**: `/parasol/commands/` から最新仕様を抽出
- **実装例の更新**: `/modules/` から実際の実装例を抽出
- **パターン更新**: `/parasol/bundles/patterns/` から最新パターンを反映

### 2. 自動検証
- **用語一貫性チェック**: 定義された用語集との照合
- **コード例の検証**: 実際に動作するか確認
- **リンク検証**: 内部リンクの有効性確認
- **バージョン整合性**: V5仕様との整合性確認

### 3. 差分管理
- **変更箇所のハイライト**: 更新された箇所を明示
- **レビュー用差分**: 人間がレビューしやすい形式で出力
- **履歴管理**: 更新履歴の記録

## インストール

```bash
cd modules/book-updater
uv pip install -e .
```

## 使用方法

### 基本的な更新

```bash
# 全体の更新チェック
bookupdater check

# 自動更新の実行
bookupdater update

# 特定の章のみ更新
bookupdater update --chapter 5

# ドライラン（変更内容の確認のみ）
bookupdater update --dry-run
```

### 高度な使用方法

```bash
# カスタム設定での更新
bookupdater update --config custom-rules.yaml

# インタラクティブモード（変更を1つずつ確認）
bookupdater update --interactive

# 特定のパターンのみ更新
bookupdater update --pattern "価値ストリーム"

# バックアップを作成してから更新
bookupdater update --backup
```

## 設定ファイル

### update-rules.yaml

```yaml
# 更新ルールの定義
rules:
  # コマンドリファレンスの同期
  command_sync:
    source: /parasol/commands/
    target_pattern: "## コマンドリファレンス"
    update_mode: replace  # replace, merge, append
  
  # 実装例の更新
  code_examples:
    sources:
      - /modules/*/examples/
      - /parasol/examples/
    validation: true
    syntax_check: true
  
  # 用語の統一
  terminology:
    glossary: /parasol/docs/glossary.yaml
    strict_mode: true
  
  # 廃止された機能
  deprecated:
    - pattern: "Event Sourcing"
      replacement: "軽量イベント通知"
    - pattern: "Backend SAGA"
      replacement: "フロントエンドオーケストレーション"

# 除外設定
exclude:
  - appendices/history.md  # 歴史的文書は更新しない
  - examples/legacy/       # レガシー例は保持

# 検証設定
validation:
  check_links: true
  check_code: true
  check_terminology: true
  check_consistency: true
```

## 更新フロー

### 1. 分析フェーズ
```bash
# 現在の書籍と最新実装の差分を分析
bookupdater analyze

# 出力例:
# 📊 分析結果:
# - 新しいコマンド: 5個
# - 更新が必要な例: 12箇所
# - 廃止された機能: 3箇所
# - 用語の不一致: 8箇所
```

### 2. 計画フェーズ
```bash
# 更新計画の生成
bookupdater plan

# 出力: update-plan.md
# - 各章の更新内容
# - 優先度
# - 推定作業量
```

### 3. 実行フェーズ
```bash
# 段階的に更新
bookupdater update --step-by-step

# 各ステップで確認:
# [1/5] コマンドリファレンスを更新しますか？ (y/n)
```

## 出力例

### 更新レポート
```markdown
# Book Update Report - 2024-12-17

## 概要
- 更新された章: 5
- 追加されたセクション: 3
- 更新されたコード例: 15
- 修正されたリンク: 7

## 詳細

### 第5章: ケイパビリティ分解
- 追加: ZIGZAG パターンの詳細説明
- 更新: capability-mapper コマンドの使用例
- 削除: 古いCQRSベースの例

### 第8章: 実装パターン
- 更新: フロントエンドオーケストレーションの例
- 追加: 軽量イベント通知パターン
...
```

## 検証機能

### コード検証
```python
# 書籍内のコードブロックを抽出して検証
def validate_code_blocks(chapter_content: str) -> List[ValidationResult]:
    """コード例が実際に動作するか検証"""
    # TypeScript/JavaScript の構文チェック
    # Python コードの実行可能性チェック
    # インポート文の有効性確認
```

### リンク検証
```python
def validate_links(content: str) -> List[BrokenLink]:
    """内部リンクと外部リンクの有効性を確認"""
    # ファイルの存在確認
    # アンカーの存在確認
    # 外部URLの到達可能性
```

## カスタマイズ

### カスタムルールの作成
```python
# custom_rules.py
from bookupdater.rules import UpdateRule

class MyCustomRule(UpdateRule):
    """プロジェクト固有の更新ルール"""
    
    def should_update(self, content: str) -> bool:
        # 更新が必要か判定
        return "old_pattern" in content
    
    def update(self, content: str) -> str:
        # 実際の更新処理
        return content.replace("old_pattern", "new_pattern")
```

## トラブルシューティング

### 更新が検出されない
```bash
# キャッシュをクリア
bookupdater clear-cache

# 強制的に全スキャン
bookupdater check --force
```

### 誤った更新を戻す
```bash
# バックアップから復元
bookupdater restore --from backup-20241217

# 特定の変更のみ取り消し
bookupdater revert --change-id abc123
```

## ベストプラクティス

1. **定期的な実行**: 週次でチェックを実行
2. **段階的更新**: 大きな変更は章ごとに分割
3. **レビュープロセス**: 自動更新後は必ず人間がレビュー
4. **バックアップ**: 更新前に必ずバックアップ
5. **テスト**: 更新後はPDF生成でレイアウト確認

## ライセンス

MIT License