# プロジェクト検出（全コマンド共通）

このセクションは全てのParasolコマンドに含まれる共通ロジックです。

## プロジェクト検出

コマンド実行時、以下の順序で `parasol.yaml` を自動探索：

### 探索順序

1. **カレントディレクトリ** (`.`)
2. **親ディレクトリ** (`..`)  
3. **祖父ディレクトリ** (`../..`)

最大3階層まで遡って探索します。

### 検出成功

```
✅ プロジェクト検出: {project-name}

プロジェクトディレクトリ: projects/{project-name}/
出力先: projects/{project-name}/outputs/

[コマンド実行を続行]
```

**動作**:
- `parasol.yaml` からプロジェクト設定を読み込み
- 出力パスを `{project_dir}/outputs/` に設定
- Phase進捗を `parasol.yaml` に自動記録
- プロジェクト名をコマンド出力に表示

### 検出失敗

```
❌ Parasolプロジェクトが見つかりません

このディレクトリはParasolプロジェクトではありません。

📋 次のアクションを選択してください:

1. 新しいプロジェクトを作成
→ /parasol:project init {project-name}

2. 既存プロジェクトに移動
→ cd projects/{project-name}

3. プロジェクト一覧を確認
→ /parasol:project list

ヒント: Parasolコマンドは必ずプロジェクトディレクトリ内で実行してください。
```

**エラー時の動作**:
- コマンド実行を中止
- プロジェクト初期化を促す
- 既存プロジェクトへの移動方法を提示

## parasol.yaml の構造

```yaml
project:
name: my-project
display_name: My Project
company_url: https://company.example.com
created: 2025-01-21T10:30:00Z
updated: 2025-01-22T15:45:00Z

phases:
phase0:
status: completed | in_progress | pending
completed: 2025-01-21T11:00:00Z
phase1:
status: completed
completed: 2025-01-21T14:20:00Z
# ... 他のPhases

settings:
output_dir: ./outputs
auto_backup: true
```

## Phase進捗の自動更新

各コマンド実行時、対応するPhaseのステータスを自動更新：

### Phase開始時

```yaml
phase1:
status: in_progress
started: 2025-01-21T13:00:00Z
```

### Phase完了時

```yaml
phase1:
status: completed
completed: 2025-01-21T14:20:00Z
artifacts:
- organization-analysis.md (created)
- market-assessment.md (created)
- constraints.md (created)
- stakeholder-map.md (created)
```

### Sub-Phase更新

Phase 3 などのサブフェーズを持つPhase：

```yaml
phase3:
status: in_progress
sub_phases:
cl1:
status: completed
completed: 2025-01-21T10:00:00Z
cl2:
status: in_progress
started: 2025-01-22T09:00:00Z
updated: 2025-01-22T15:30:00Z
cl3:
status: pending
```

## 出力パスの解決

プロジェクト設定に基づいて出力パスを解決：

```
parasol.yaml の場所: projects/my-project/parasol.yaml
output_dir 設定: ./outputs

解決されたパス: projects/my-project/outputs/
```

### パス解決例

```python
# 疑似コード
project_dir = find_parasol_yaml()  # projects/my-project/
config = load_yaml(project_dir / "parasol.yaml")
output_dir = project_dir / config["settings"]["output_dir"]  
# → projects/my-project/outputs/

phase1_dir = output_dir / "1-context"
# → projects/my-project/outputs/1-context/
```

## エラーハンドリング

### parasol.yaml が破損

```
❌ parasol.yaml の読み込みに失敗しました

ファイル: projects/my-project/parasol.yaml
エラー: YAML解析エラー（行15: インデントエラー）

対処方法:
1. parasol.yaml を手動で修正
2. バックアップから復元（auto_backupが有効な場合）
3. プロジェクトを再作成（最終手段）
```

### 出力ディレクトリの権限エラー

```
❌ 出力ディレクトリへの書き込みに失敗しました

ディレクトリ: projects/my-project/outputs/1-context
エラー: Permission denied

対処方法:
1. ディレクトリの権限を確認: ls -la projects/my-project/outputs
2. 権限を修正: chmod 755 projects/my-project/outputs
```

## ベストプラクティス

### プロジェクトディレクトリで作業

```bash
# 推奨
cd projects/my-project
/parasol:1-context

# 非推奨（プロジェクトが検出されない可能性）
cd ~/somewhere-else
/parasol:1-context  # ❌ プロジェクト未検出
```

### プロジェクトの確認

作業前にプロジェクトを確認：

```bash
# 現在のプロジェクト情報
/parasol:project info

# プロジェクト一覧
/parasol:project list
```

### 複数プロジェクトの並行作業

```bash
# プロジェクトA
cd projects/project-a
/parasol:3-capabilities cl1

# 別ターミナルでプロジェクトB
cd projects/project-b
/parasol:2-value VS0
```

それぞれ独立して進捗が管理されます。
