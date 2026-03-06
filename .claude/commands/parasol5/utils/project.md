---
description: Project management (parasol5:utils)
---

# Parasol V5 - Project Management

Parasolプロジェクトの作成、一覧表示、情報確認を行います。

## 使用方法

```bash
/parasol5:utils:project init {project-name}     # 新規プロジェクト作成
/parasol5:utils:project list                    # プロジェクト一覧
/parasol5:utils:project info                    # 現在のプロジェクト情報
/parasol5:utils:project status                  # 進捗確認（/parasol5:utils:statusのエイリアス）
```

## プロジェクト構造

```
projects/
└── {project-name}/
├── parasol.yaml              # プロジェクト設定
├── outputs/                  # 成果物ディレクトリ
│   ├── 0-init/              # (オプション) URL初期化データ
│   ├── 1-context/           # Phase 1 成果物
│   ├── 2-value/             # Phase 2 成果物
│   ├── 3-capabilities/      # Phase 3 成果物
│   ├── 4-architecture/      # Phase 4 成果物
│   ├── 5-software/          # Phase 5 成果物
│   ├── 6-implementation/    # Phase 6 成果物
│   └── 7-platform/          # Phase 7 成果物
└── docs/                    # (オプション) プロジェクト固有のドキュメント
```

## コマンド詳細

### project init - 新規プロジェクト作成

```bash
/parasol5:utils:project init my-ecommerce-platform
```

**実行内容**:

1. プロジェクトディレクトリ作成
```
projects/my-ecommerce-platform/ を作成
```

2. parasol.yaml 生成
```yaml
# projects/my-ecommerce-platform/parasol.yaml
project:
name: my-ecommerce-platform
display_name: My E-Commerce Platform
created: 2025-01-21T10:30:00Z
updated: 2025-01-21T10:30:00Z

# オプション（0-initで自動設定）
company_url: null
industry: null

phases:
phase0:
name: "Initialize from URL"
status: pending
completed: null

phase1:
name: "Context"
status: pending
completed: null
artifacts:
- organization-analysis.md
- market-assessment.md
- constraints.md
- stakeholder-map.md

phase2:
name: "Value Definition"
status: pending
completed: null
artifacts:
- value-definition.md
- value-streams-mapping.md
- enterprise-activities.md

phase3:
name: "Capabilities"
status: pending
completed: null
sub_phases:
cl1:
name: "Domain Classification"
status: pending
cl2:
name: "Subdomain Design"
status: pending
cl3:
name: "Bounded Context Definition"
status: pending

phase4:
name: "Architecture"
status: pending
completed: null

phase5:
name: "Software Design"
status: pending
completed: null

phase6:
name: "Implementation"
status: pending
completed: null

phase7:
name: "Platform"
status: pending
completed: null

settings:
output_dir: ./outputs
auto_backup: true
validation_strict: false
```

3. outputs/ ディレクトリ作成
```
projects/my-ecommerce-platform/outputs/ を作成
```

4. README.md 生成
```markdown
# My E-Commerce Platform

Parasol V5 プロジェクト

作成日: 2025-01-21

## クイックスタート

```bash
cd projects/my-ecommerce-platform

# オプション1: URLから自動初期化
/value5:init https://company.example.com

# オプション2: 手動でPhase 1から開始
/value5:context
```

## 進捗確認

```bash
/parasol5:utils:project info
/parasol5:utils:status
```

## プロジェクト構造

- `parasol.yaml`: プロジェクト設定
- `outputs/`: 全フェーズの成果物
- `docs/`: プロジェクト固有のドキュメント（任意）
```

**完了メッセージ**:
```
✅ プロジェクト作成完了: my-ecommerce-platform

プロジェクトディレクトリ:
projects/my-ecommerce-platform/

次のステップ:
1. プロジェクトディレクトリに移動:
cd projects/my-ecommerce-platform

2. URLから自動初期化（推奨）:
/value5:init https://company.example.com

または手動で開始:
/value5:context

3. 進捗確認:
/parasol5:utils:project info
```

---

### project list - プロジェクト一覧

```bash
/parasol5:utils:project list
```

**実行内容**:

1. projects/ ディレクトリをスキャン
2. 各プロジェクトの parasol.yaml を読み込み
3. プロジェクト情報とステータスを表示

**出力例**:
```
📁 Parasol プロジェクト一覧

projects/ ディレクトリ: /Users/username/amplifier-experiment/projects

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ asahi-beer-platform
作成: 2025-01-20  更新: 2025-01-22
Phase 3: Capabilities (CL2 進行中)
進捗: ██████████░░░░░░░░░░ 50% (4/7 フェーズ完了)

cd projects/asahi-beer-platform

🔄 toyota-supply-chain
作成: 2025-01-21  更新: 2025-01-21
Phase 1: Context (完了)
進捗: ███░░░░░░░░░░░░░░░░░ 14% (1/7 フェーズ完了)

cd projects/toyota-supply-chain

⏸️ sony-iot-platform
作成: 2025-01-22  更新: 2025-01-22
Phase 0: 未開始
進捗: ░░░░░░░░░░░░░░░░░░░░ 0%

cd projects/sony-iot-platform

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

合計: 3 プロジェクト
完了: 0
進行中: 2
未開始: 1

新しいプロジェクトを作成:
→ /parasol5:utils:project init {project-name}
```

---

### project info - 現在のプロジェクト情報

```bash
/parasol5:utils:project info
```

**実行内容**:

1. カレントディレクトリで parasol.yaml を探索
2. プロジェクト情報を読み込み
3. 詳細情報と進捗を表示

**出力例**:
```
📊 プロジェクト情報

プロジェクト名: asahi-beer-platform
作成日: 2025-01-20
最終更新: 2025-01-22 15:30

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏢 組織情報:
会社URL: https://asahi-group-holdings.com
業界: Beverage Manufacturing

📁 プロジェクトディレクトリ:
/Users/username/projects/asahi-beer-platform

📂 出力ディレクトリ:
./outputs

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 Phase 進捗:

✅ Phase 0: Initialize from URL
完了日: 2025-01-20 10:30

✅ Phase 1: Context
完了日: 2025-01-20 14:20
成果物: 4/4

✅ Phase 2: Value Definition
完了日: 2025-01-21 11:15
成果物: 3/3 + VS0-VS7 全定義

🔄 Phase 3: Capabilities
状況: 進行中（CL2 - Subdomain Design）
完了: CL1 ✅
進行中: CL2 🔄 (core domain 完了、supporting 進行中)
未着手: CL3 ⏸️

⏸️ Phase 4: Application Design
状況: 未着手（Phase 3完了待ち）

⏸️ Phase 5: Software Design
状況: 未着手

⏸️ Phase 6: Implementation
状況: 未着手

⏸️ Phase 7: Platform
状況: 未着手

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 全体進捗: 50% (3.5/7 フェーズ完了)

進捗バー: ██████████░░░░░░░░░░

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 次のアクション:

1. Phase 3 CL2 を完了:
/parasol5:capability:decompose cl2 supporting
/parasol5:capability:decompose cl2 generic

2. Phase 3 CL3 を開始:
/parasol5:capability:decompose cl3

3. 詳細なステータス確認:
/parasol5:utils:status phase3

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 便利なコマンド:

- 全プロジェクト一覧: /parasol5:utils:project list
- Phase別ステータス: /parasol5:utils:status phase3
- バリデーション: /parasol5:utils:validate
```

---

### project status - 進捗確認（エイリアス）

```bash
/parasol5:utils:project status
```

これは `/parasol5:utils:status` のエイリアスです。詳細は `/parasol5:utils:status` を参照してください。

---

## プロジェクト検出ロジック

全てのParasolコマンド（0-init, 1-context, 2-value, ...）は、実行時に以下のロジックでプロジェクトを検出します：

### 検出順序

1. **カレントディレクトリ**: `./parasol.yaml`
2. **親ディレクトリ**: `../parasol.yaml`
3. **祖父ディレクトリ**: `../../parasol.yaml`

最大3階層まで遡って探索します。

### 検出成功

```
✅ プロジェクト検出: asahi-beer-platform

プロジェクトディレクトリ: projects/asahi-beer-platform/
出力先: projects/asahi-beer-platform/outputs/

[コマンド実行]
```

### 検出失敗

```
❌ Parasolプロジェクトが見つかりません

このディレクトリはParasolプロジェクトではありません。

オプション1: 新しいプロジェクトを作成
→ /parasol5:utils:project init {project-name}

オプション2: 既存プロジェクトに移動
→ cd projects/{project-name}

オプション3: プロジェクト一覧を確認
→ /parasol5:utils:project list
```

---

## Phase進捗の自動更新

各Phaseコマンド実行時、parasol.yaml が自動更新されます：

**Phase完了時**:
```yaml
phase1:
status: completed
completed: 2025-01-20T14:20:00Z
artifacts:
- organization-analysis.md (created)
- market-assessment.md (created)
- constraints.md (created)
- stakeholder-map.md (created)
```

**Phase進行中**:
```yaml
phase3:
status: in_progress
sub_phases:
cl1:
status: completed
completed: 2025-01-21T10:00:00Z
cl2:
status: in_progress
updated: 2025-01-22T15:30:00Z
cl3:
status: pending
```

---

## エラーケース

### プロジェクト名が既に存在

```
❌ プロジェクトが既に存在します: my-ecommerce-platform

既存プロジェクト:
projects/my-ecommerce-platform/
作成日: 2025-01-20

オプション:
1. 既存プロジェクトを使用:
cd projects/my-ecommerce-platform

2. 別の名前で作成:
/parasol5:utils:project init my-ecommerce-platform-v2

3. 既存プロジェクトを削除してから再作成（注意）
```

### projects/ ディレクトリが存在しない

```
⚠️ projects/ ディレクトリが存在しません

作成しますか？ (y/n):
> y

✅ projects/ ディレクトリを作成しました

続行: /parasol5:utils:project init {project-name}
```

### 無効なプロジェクト名

```
❌ 無効なプロジェクト名: My Project!

プロジェクト名の制約:
- 小文字、数字、ハイフンのみ使用可能
- 最初は文字で開始
- 長さ: 3-50文字

有効な例:
my-ecommerce-platform
toyota-supply-chain-2024
sony-iot

無効な例:
My Project!  (スペース、記号)
2-project    (数字で開始)
ab           (短すぎる)
```

---

## ベストプラクティス

### プロジェクト命名

**推奨パターン**:
- `{company}-{domain}-{purpose}`
- 例: `asahi-beer-ecommerce`
- 例: `toyota-supply-chain-platform`
- 例: `sony-iot-gateway`

### プロジェクト構成

```
projects/
├── {project-name}/
│   ├── parasol.yaml           # 必須: プロジェクト設定
│   ├── README.md              # 推奨: プロジェクト概要
│   ├── outputs/               # 必須: Parasol成果物
│   ├── docs/                  # 任意: 追加ドキュメント
│   │   ├── architecture/
│   │   ├── decisions/         # ADRs
│   │   └── meetings/
│   └── .gitignore             # 推奨
```

### バージョン管理

**Git管理推奨**:
```bash
cd projects/my-project
git init
git add .
git commit -m "Initial Parasol project setup"
```

**.gitignore 例**:
```
# Parasol outputs (大きいファイルを除外する場合)
# outputs/

# 一時ファイル
*.tmp
.DS_Store
```

---

## 関連コマンド

- `/value5:init` - URLからプロジェクト初期化
- `/value5:context` - Phase 1 開始
- `/parasol5:utils:status` - 詳細な進捗確認
- `/parasol5:utils:validate` - プロジェクト検証
- `/parasol5:utils:help` - ヘルプシステム
