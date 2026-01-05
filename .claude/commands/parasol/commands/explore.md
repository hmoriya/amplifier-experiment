---
description: Value decomposition exploration with 3 axes (value/business/hybrid) using git worktree (project:parasol)
---

# Parasol Explore - 価値分解探索

3つの価値分解アプローチ（価値軸/事業部軸/ハイブリッド）を並行探索し、CL1まで作成して比較・選択します。

## 使用方法

```bash
/parasol:explore init              # 探索開始: VL1作成 + 3 worktree準備
/parasol:explore run value         # 価値軸で探索
/parasol:explore run business      # 事業部軸で探索
/parasol:explore run hybrid        # ハイブリッドで探索
/parasol:explore compare           # 3軸比較表生成
/parasol:explore select [axis]     # 選択してmainにマージ
/parasol:explore cleanup           # worktree削除
/parasol:explore status            # 探索状況確認
```

## 3つの探索軸

```
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│    価値軸        │ │   事業部軸       │ │  ハイブリッド    │
│   (value)       │ │  (business)     │ │   (hybrid)      │
├─────────────────┤ ├─────────────────┤ ├─────────────────┤
│ VL2:            │ │ VL2:            │ │ VL2-共通:       │
│ ・イノベーション │ │ ・事業A         │ │ ・共通価値      │
│ ・品質          │ │ ・事業B         │ │ VL2-事業:       │
│ ・サステナ      │ │ ・事業C         │ │ ・事業別価値    │
│                 │ │                 │ │                 │
│ VStr: 1体系     │ │ VStr: 事業別    │ │ VStr: 共通+事業 │
│ CL1: 統合分類   │ │ CL1: 事業別分類 │ │ CL1: 2層分類    │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

## 探索フロー

```
VL1（共通・mainブランチ）
        │
        │ /parasol:explore init
        │
        ├──────────────┼──────────────┐
        ▼              ▼              ▼
   ┌─────────┐   ┌─────────┐   ┌─────────┐
   │ value   │   │business │   │ hybrid  │
   │worktree │   │worktree │   │worktree │
   └────┬────┘   └────┬────┘   └────┬────┘
        │              │              │
        │ run value    │ run business │ run hybrid
        ▼              ▼              ▼
   VL2→VL3        VL2→VL3        VL2→VL3
   MS→VStr        MS→VStr        MS→VStr
   CL1            CL1            CL1
        │              │              │
        └──────────────┼──────────────┘
                       ▼
                   compare
                       │
                       ▼
                select [axis]
                       │
                       ▼
                   cleanup
```

---

## サブコマンド詳細

### init - 探索初期化

**実行内容:**
1. プロジェクト検出（parasol.yaml）
2. VL1（最上位価値）の確認/作成
3. 3つのworktreeを作成
4. 各worktreeにVL1をコピー

**Bash実行:**
```bash
# プロジェクトディレクトリで実行
PROJECT_NAME=$(basename $(pwd))
WORKTREE_BASE="../.worktrees"

# worktree作成
git worktree add "${WORKTREE_BASE}/${PROJECT_NAME}-value" -b "explore/${PROJECT_NAME}/value"
git worktree add "${WORKTREE_BASE}/${PROJECT_NAME}-business" -b "explore/${PROJECT_NAME}/business"
git worktree add "${WORKTREE_BASE}/${PROJECT_NAME}-hybrid" -b "explore/${PROJECT_NAME}/hybrid"
```

**出力メッセージ:**
```
✅ 探索環境を初期化しました

プロジェクト: {project-name}
VL1: outputs/2-value/vl1-definition.md

Worktrees:
├── .worktrees/{project}-value/    (branch: explore/{project}/value)
├── .worktrees/{project}-business/ (branch: explore/{project}/business)
└── .worktrees/{project}-hybrid/   (branch: explore/{project}/hybrid)

次のステップ:
→ /parasol:explore run value
→ /parasol:explore run business
→ /parasol:explore run hybrid
```

---

### run [axis] - 探索実行

**引数:** `value` | `business` | `hybrid`

**実行内容:**
1. 対応するworktreeに移動
2. VL2分解（軸に応じた分解）
3. VL3詳細化
4. MSバックキャスティング
5. バリューストリーム（VStr）導出
6. CL1活動領域識別（傾向的分類：Core/Supporting/Generic）
7. コミット

#### run value - 価値軸探索

**VL2分解の観点:**
- 企業が提供する「価値の種類」で分解
- 例: イノベーション価値、品質価値、サステナビリティ価値、グローバル価値

**出力構造:**
```
outputs/2-value/exploration/value/
├── vl2-vl3-decomposition.md    # 価値軸でのVL2→VL3分解
├── milestones.md               # VMS5→VMS1バックキャスティング
├── value-streams.md            # バリューストリーム（1体系）
└── cl1-classification.md       # CL1分類（統合）
```

**VL2→VL3テンプレート（価値軸）:**
```markdown
# VL2-VL3 価値分解（価値軸）

## VL1: 最上位価値
[vl1-definition.mdから継承]

## VL2: 価値グループ（価値軸分解）

### VL2-1: イノベーション価値
**定義**: 新しい価値を創造し続ける力
**VL1への貢献**: [貢献内容]

#### VL3詳細:
- VL3-1-1: 研究開発による技術革新
- VL3-1-2: 市場創造による新カテゴリー開拓
- VL3-1-3: オープンイノベーション

### VL2-2: 品質価値
**定義**: 妥協なき品質へのこだわり
**VL1への貢献**: [貢献内容]

#### VL3詳細:
- VL3-2-1: 原材料の品質管理
- VL3-2-2: 製造プロセスの品質保証
- VL3-2-3: 顧客体験の品質

### VL2-3: サステナビリティ価値
...

### VL2-4: グローバル価値
...

## 設計ストーリー
**なぜ価値軸で分解したか:**
[理由を記述]

**VL2グループ分けの理由:**
[理由を記述]
```

#### run business - 事業部軸探索

**VL2分解の観点:**
- 事業部/事業セグメントで分解
- 例: 飲料事業価値、酒類事業価値、その他事業価値

**出力構造:**
```
outputs/2-value/exploration/business/
├── vl2-vl3-decomposition.md    # 事業部軸でのVL2→VL3分解
├── milestones.md               # VMS5→VMS1（事業部別）
├── value-streams/              # バリューストリーム（事業部別）
│   ├── business-a-vstr.md
│   ├── business-b-vstr.md
│   └── business-c-vstr.md
└── cl1-classification.md       # CL1分類（事業部別）
```

**VL2→VL3テンプレート（事業部軸）:**
```markdown
# VL2-VL3 価値分解（事業部軸）

## VL1: 最上位価値
[vl1-definition.mdから継承]

## VL2: 価値グループ（事業部軸分解）

### VL2-1: [事業部A]価値
**定義**: [事業部Aが提供する価値]
**売上構成比**: XX%
**VL1への貢献**: [貢献内容]

#### VL3詳細:
- VL3-1-1: [事業部A固有の価値1]
- VL3-1-2: [事業部A固有の価値2]
- VL3-1-3: [事業部A固有の価値3]

### VL2-2: [事業部B]価値
...

### VL2-3: [事業部C]価値
...

## 設計ストーリー
**なぜ事業部軸で分解したか:**
[理由を記述]
```

#### run hybrid - ハイブリッド探索

**VL2分解の観点:**
- 共通基盤価値 + 事業別差別化価値の2層
- 例: 共通（創業精神、水環境）+ 事業別（飲料、酒類）

**出力構造:**
```
outputs/2-value/exploration/hybrid/
├── vl2-vl3-decomposition.md    # ハイブリッドVL2→VL3分解
├── milestones.md               # VMS5→VMS1（共通+事業別）
├── value-streams/              # バリューストリーム（2層）
│   ├── common-vstr.md          # 共通基盤VStr
│   ├── business-a-vstr.md      # 事業A差別化VStr
│   └── business-b-vstr.md      # 事業B差別化VStr
└── cl1-classification.md       # CL1分類（2層）
```

**VL2→VL3テンプレート（ハイブリッド）:**
```markdown
# VL2-VL3 価値分解（ハイブリッド）

## VL1: 最上位価値
[vl1-definition.mdから継承]

## VL2-共通: 共通基盤価値

### VL2-C1: [共通価値1]（例: 創業精神価値）
**定義**: 全事業に共通する価値基盤
**VL1への貢献**: [貢献内容]

#### VL3詳細:
- VL3-C1-1: [共通価値の詳細1]
- VL3-C1-2: [共通価値の詳細2]

### VL2-C2: [共通価値2]（例: 水環境価値）
...

## VL2-事業: 事業別差別化価値

### VL2-B1: [事業A]差別化価値
**定義**: [事業A固有の差別化価値]
**VL1への貢献**: [貢献内容]
**共通価値との関係**: [どの共通価値を基盤とするか]

#### VL3詳細:
- VL3-B1-1: [事業A差別化価値1]
- VL3-B1-2: [事業A差別化価値2]

### VL2-B2: [事業B]差別化価値
...

## 設計ストーリー
**なぜハイブリッドで分解したか:**
[理由を記述]

**共通と事業別の切り分け理由:**
[理由を記述]
```

---

### CL1分類テンプレート

各探索軸の `cl1-classification.md` で使用:

```markdown
# CL1 活動領域識別（傾向的分類）

※この分類は参考情報です。CL2で各ケイパビリティを個別に正式分類します。

## 分類サマリー

| 分類 | 投資配分 | 領域数 |
|------|----------|--------|
| ★ Core | XX% | N個 |
| ◆ Supporting | XX% | N個 |
| ○ Generic | XX% | N個 |

## ★ Core（差別化源泉）

競争優位性の源泉となる活動領域。内製・投資集中。

| 領域 | VL3との対応 | 理由 |
|------|------------|------|
| [領域名] | VL3-X-X | [なぜCoreか] |

## ◆ Supporting（重要支援）

Coreを支える重要な活動。効率化・標準化。

| 領域 | VL3との対応 | 理由 |
|------|------------|------|
| [領域名] | VL3-X-X | [なぜSupportingか] |

## ○ Generic（標準化可能）

業界標準で代替可能。外部化・パッケージ活用。

| 領域 | VL3との対応 | 理由 |
|------|------------|------|
| [領域名] | VL3-X-X | [なぜGenericか] |

## 設計ストーリー
**分類判断の基準:**
[基準を記述]
```

---

### compare - 比較表生成

**実行内容:**
1. 3つのworktreeから成果物を読み込み
2. 比較表を生成
3. mainブランチに `exploration/comparison.md` として保存

**比較表テンプレート:**
```markdown
# 価値分解探索 比較表

## 探索サマリー

| 項目 | 価値軸 | 事業部軸 | ハイブリッド |
|------|--------|----------|--------------|
| VL2数 | N個 | N個 | 共通N個+事業N個 |
| VStr数 | 1体系 | 事業数体系 | 1+事業数体系 |
| CL1 Core傾向数 | N個 | N個 | N個 |
| CL1 Core傾向投資比率 | XX% | XX% | XX% |

## VL2構造の比較

### 価値軸
```
VL2: イノベーション / 品質 / サステナ / グローバル
```

### 事業部軸
```
VL2: 事業A / 事業B / 事業C
```

### ハイブリッド
```
VL2-共通: 共通価値1 / 共通価値2
VL2-事業: 事業A / 事業B
```

## バリューストリーム構造の比較

[各軸のVStr構造を図示]

## CL1分類の比較

### Core領域の違い

| 価値軸のCore | 事業部軸のCore | ハイブリッドのCore |
|--------------|----------------|-------------------|
| [領域] | [領域] | [領域] |

### 投資配分の違い

[投資配分の比較図]

## 評価

### メリット・デメリット

| 軸 | メリット | デメリット |
|----|----------|------------|
| 価値軸 | [メリット] | [デメリット] |
| 事業部軸 | [メリット] | [デメリット] |
| ハイブリッド | [メリット] | [デメリット] |

### 適合度評価

| 評価観点 | 価値軸 | 事業部軸 | ハイブリッド |
|----------|--------|----------|--------------|
| 経営視点との整合 | ○/△/× | ○/△/× | ○/△/× |
| 実務との整合 | ○/△/× | ○/△/× | ○/△/× |
| 投資判断のしやすさ | ○/△/× | ○/△/× | ○/△/× |
| 将来の拡張性 | ○/△/× | ○/△/× | ○/△/× |

## 推奨

**推奨軸**: [value | business | hybrid]

**理由**:
[推奨理由を記述]
```

---

### select [axis] - 選択・確定

**引数:** `value` | `business` | `hybrid`

**実行内容:**
1. 選択した軸の成果物を `outputs/2-value/selected/` にコピー
2. parasol.yaml の phase2 ステータスを更新
3. オプション: 選択したブランチをmainにマージ

**Bash実行:**
```bash
# 選択した軸の成果物をコピー
AXIS=$1  # value | business | hybrid
cp -r outputs/2-value/exploration/${AXIS}/* outputs/2-value/selected/

# コミット
git add outputs/2-value/selected/
git commit -m "feat(parasol): select ${AXIS} axis for value decomposition"
```

**出力メッセージ:**
```
✅ 価値分解軸を選択しました

選択: {axis}
成果物: outputs/2-value/selected/

次のステップ:
→ /parasol:3-capabilities cl1    # CL1を確定してCL2へ
→ /parasol:explore cleanup       # worktree削除
```

---

### cleanup - Worktree削除

**実行内容:**
1. 3つのworktreeを削除
2. 探索ブランチを削除（オプション）

**Bash実行:**
```bash
PROJECT_NAME=$(basename $(pwd))
WORKTREE_BASE="../.worktrees"

# worktree削除
git worktree remove "${WORKTREE_BASE}/${PROJECT_NAME}-value" --force
git worktree remove "${WORKTREE_BASE}/${PROJECT_NAME}-business" --force
git worktree remove "${WORKTREE_BASE}/${PROJECT_NAME}-hybrid" --force

# ブランチ削除（オプション）
git branch -D "explore/${PROJECT_NAME}/value"
git branch -D "explore/${PROJECT_NAME}/business"
git branch -D "explore/${PROJECT_NAME}/hybrid"
```

**出力メッセージ:**
```
✅ 探索環境をクリーンアップしました

削除されたworktrees:
├── .worktrees/{project}-value/
├── .worktrees/{project}-business/
└── .worktrees/{project}-hybrid/

削除されたブランチ:
├── explore/{project}/value
├── explore/{project}/business
└── explore/{project}/hybrid
```

---

### status - 探索状況確認

**出力例:**
```
📋 Parasol Explore Status

プロジェクト: suntory
VL1: ✅ 定義済み

┌─────────────────────────────────────────────────────────────┐
│ 探索状況                                                    │
├──────────┬──────────┬──────────┬──────────┬────────────────┤
│ 軸       │ VL2-VL3  │ VStr     │ CL1      │ 状態           │
├──────────┼──────────┼──────────┼──────────┼────────────────┤
│ value    │ ✅       │ ✅       │ ✅       │ 完了           │
│ business │ ✅       │ ✅       │ ⏳       │ CL1作成中      │
│ hybrid   │ ⏳       │ -        │ -        │ VL2-VL3作成中  │
└──────────┴──────────┴──────────┴──────────┴────────────────┘

Worktrees:
├── .worktrees/suntory-value/    (branch: explore/suntory/value)
├── .worktrees/suntory-business/ (branch: explore/suntory/business)
└── .worktrees/suntory-hybrid/   (branch: explore/suntory/hybrid)

次のステップ:
→ /parasol:explore run hybrid    # hybrid探索を継続
→ /parasol:explore compare       # 比較表生成（全軸完了後）
```

---

## プロジェクト検出

**重要**: このコマンドはParasolプロジェクト内で実行する必要があります。

### 自動検出

コマンド実行時、以下の順序で `parasol.yaml` を自動探索：

1. **カレントディレクトリ** (`.`)
2. **親ディレクトリ** (`..`)
3. **祖父ディレクトリ** (`../..`)

### 検出失敗時

```
❌ Parasolプロジェクトが見つかりません

📋 次のアクションを選択してください:

1. 新しいプロジェクトを作成
   → /parasol:0-project init {project-name}

2. 既存プロジェクトに移動
   → cd projects/{project-name}

3. プロジェクト一覧を確認
   → /parasol:0-project list
```

---

## 注意事項

### Worktree使用時の注意

1. **同じファイルを複数worktreeで同時編集しない**
   - 各worktreeは独立したブランチ
   - 同じファイルを編集するとマージ時にコンフリクト

2. **worktree間の移動**
   - `cd ../.worktrees/{project}-{axis}/` で移動
   - 各worktreeで独立して作業可能

3. **コミットの重要性**
   - 各探索軸の作業後は必ずコミット
   - compare時に最新状態を参照するため

### CL1まで作成する理由

- CL1（傾向的分類：Core/Supporting/Generic）まで見ると投資方向性が把握しやすい
- 価値分解の妥当性をCL1で検証できる
- 3軸の違いがCL1で明確になる
- ※CL1は参考情報、CL2で正式分類を行う

---

## 関連コマンド

- `/parasol:2-value` - 価値定義（探索なしの通常フロー）
- `/parasol:3-capabilities` - ケーパビリティ分解
- `/parasol:0-status` - プロジェクト状況確認
