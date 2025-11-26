---
description: Project context setup (project:parasol)
---

# Phase 1: Context - プロジェクト文脈確立

プロジェクトの基本的な文脈を確立します。このフェーズは1回のみ実行し、プロジェクト全体の基盤となります。

## 目的

- 組織の現状を理解する
- 市場環境を評価する
- 制約事項を明確にする
- ステークホルダーを特定する



## 🔧 プロジェクト検出

**重要**: このコマンドはParasolプロジェクト内で実行する必要があります。

### 自動検出

コマンド実行時、以下の順序で `parasol.yaml` を自動探索：

1. **カレントディレクトリ** (`.`)
2. **親ディレクトリ** (`..`)
3. **祖父ディレクトリ** (`../..`)

### 検出成功

```
✅ プロジェクト検出: {project-name}

プロジェクトディレクトリ: projects/{project-name}/
出力先: projects/{project-name}/outputs/
```

プロジェクト設定を読み込み、Phase進捗を自動記録します。

### 検出失敗

```
❌ Parasolプロジェクトが見つかりません

📋 次のアクションを選択してください:

1. 新しいプロジェクトを作成
   → /parasol:project init {project-name}

2. 既存プロジェクトに移動
   → cd projects/{project-name}

3. プロジェクト一覧を確認
   → /parasol:project list
```

**ベストプラクティス**: プロジェクトディレクトリ内で作業
```bash
# 推奨
cd projects/my-project
/parasol:1-context

# 非推奨（プロジェクトが検出されない）
cd ~/somewhere-else
/parasol:1-context  # ❌
```

詳細は `.claude/commands/parasol/_project-detection.md` を参照。

## 成果物

以下のドキュメントを `outputs/1-context/` に作成します：

1. **organization-analysis.md** - 組織分析
2. **market-assessment.md** - 市場評価
3. **constraints.md** - 制約事項
4. **stakeholder-map.md** - ステークホルダーマップ

## 実行手順

### ステップ1: 出力ディレクトリの確認と作成

`outputs/1-context/` ディレクトリの存在を確認し、存在しない場合は作成します。

### ステップ2: 既存成果物の確認

既に成果物が存在する場合、上書き確認を行います：

```
⚠️ Phase 1 の成果物が既に存在します：
✅ organization-analysis.md
✅ market-assessment.md
⏸️ constraints.md (未作成)
⏸️ stakeholder-map.md (未作成)

選択してください：
1. 不足している成果物のみ作成 (推奨)
2. 全て再作成（既存を上書き）
3. キャンセル
```

### ステップ3-6: 各成果物の作成

インタラクティブモードで情報を収集しながら、以下を順次作成：

1. **organization-analysis.md** - 組織の現状分析
2. **market-assessment.md** - 市場環境評価
3. **constraints.md** - プロジェクト制約
4. **stakeholder-map.md** - ステークホルダー分析

各成果物の作成時、ユーザーと対話しながら情報を収集し、必要に応じてWeb検索で補完します。

**テンプレート参照**: `parasol-v4-lite/templates/phase1/`

## 完了条件

以下の4つの成果物が全て作成されたら完了：

- ✅ organization-analysis.md
- ✅ market-assessment.md
- ✅ constraints.md
- ✅ stakeholder-map.md

## 完了メッセージ

```
✅ Phase 1: Context が完了しました

成果物:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ outputs/1-context/organization-analysis.md
✅ outputs/1-context/market-assessment.md
✅ outputs/1-context/constraints.md
✅ outputs/1-context/stakeholder-map.md

📊 ステータス確認:
→ `/parasol:status phase1`

🎯 次のステップ: Phase 2 Value Definition
→ `/parasol:2-value`

💡 ヒント:
Phase 1 は反復不要です。内容を更新する場合は、
成果物ファイルを直接編集してください。
```

## エラーハンドリング

### エラー1: 出力ディレクトリ作成失敗

```
❌ 出力ディレクトリの作成に失敗しました

パス: outputs/1-context/
エラー: [詳細なエラーメッセージ]

対処方法:
1. ディレクトリの権限を確認
2. 手動でディレクトリを作成
3. 再度コマンドを実行
```

### エラー2: Web検索失敗

```
⚠️ Web検索に失敗しました

手動で情報を入力しますか？ (y/n):
> y

[インタラクティブモードに切り替え]
```

## バリデーション

作成後、以下を自動チェック：

1. **ファイル存在確認**: 4つの成果物が全て存在するか
2. **内容確認**: 各ファイルが空でないか、最小限のセクションを含むか
3. **整合性確認**: 組織名などの基本情報が一貫しているか

問題がある場合：

```
⚠️ バリデーション警告

- constraints.md が空です
- organization-analysis.md に "組織概要" セクションがありません

修正して再度確認しますか？
→ `/parasol:validate phase1`
```

## 参考資料

- **フレームワーク設計**: `parasol-v4-lite/FRAMEWORK-DESIGN.md`
- **テンプレート**: `parasol-v4-lite/templates/phase1/`
