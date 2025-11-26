---
description: Value definition and enterprise activities (project:parasol)
---

# Phase 2: Value Definition - 価値定義

企業の価値創造を定義し、Value Streams (VS0-VS7) を確立します。

## 使用方法

```bash
/parasol:2-value              # インタラクティブ選択
/parasol:2-value VS0          # VS0を直接指定
/parasol:2-value VS1          # VS1を直接指定
...
```

## 目的

- 組織が提供する価値を明確化する
- バリューストリーム (VS0-VS7) を定義する
- エンタープライズ活動をマッピングする



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

以下のドキュメントを `outputs/2-value/` に作成します：

1. **value-definition.md** - 価値の定義（全体、1回のみ）
2. **value-streams-mapping.md** - VS0-VS7のマッピング（全体、1回のみ）
3. **enterprise-activities.md** - エンタープライズ活動（全体、1回のみ）

## 実行手順

### 初回実行時

Phase 2を初めて実行する場合、全体成果物を作成します：

#### ステップ1: 価値定義 (value-definition.md)

```yaml
価値概要:
ビジョン: [組織が目指す理想の姿]
ミッション: [組織の存在意義]
コアバリュー: [組織の中核的価値観]

提供価値:
顧客価値: [顧客に提供する価値]
事業価値: [事業として創出する価値]
社会価値: [社会に貢献する価値]
```

#### ステップ2: バリューストリームマッピング (value-streams-mapping.md)

VS0からVS7までの8つのValue Stagesを定義：

```yaml
VS0: ビジョン策定
目的: グローバル企業として進むべき方向性を明確化
主要活動: 戦略策定、ステークホルダー対話、組織整合
インプット: 市場動向、組織状況、競合分析
アウトプット: 中長期ビジョン、戦略方針、ロードマップ
ステークホルダー: 経営層、事業部門、投資家
成功指標: ビジョン共有度、戦略整合性

VS1: 市場機会発見
目的: 成長機会を特定し、顧客ニーズと市場トレンドを理解
主要活動: 市場調査、競合分析、機会特定
...

[VS2-VS7も同様に定義]
```

#### ステップ3: エンタープライズ活動 (enterprise-activities.md)

各VSに紐づくエンタープライズ活動を定義：

```yaml
VS0関連活動:
- 経営戦略策定
- グループガバナンス
- 中長期計画立案
- ステークホルダー対話

VS1関連活動:
- 市場調査・分析
- 顧客インサイト収集
- 競合ベンチマーク
- 機会評価

[VS2-VS7の活動も定義]

活動間の関係:
VS0 → VS1: ビジョンから市場機会を特定
VS1 → VS2: 機会から製品/サービスを開発
...
```

### VS個別指定時

特定のVSに関する詳細を確認・更新する場合：

```bash
/parasol:2-value VS2
```

指定されたVSの詳細を表示し、必要に応じて更新します。

## インタラクティブモード

パラメータなしで実行すると、VSリストを表示して選択を促します：

```
📋 Value Streams 一覧

既存のValue Streams:
✅ VS0: ビジョン策定
✅ VS1: 市場機会発見
✅ VS2: 製品開発
✅ VS3: マーケティング
✅ VS4: 販売・流通
✅ VS5: カスタマーサポート
✅ VS6: データ活用
✅ VS7: 継続的改善

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

選択してください:
1. 全体を確認・更新
2. 特定のVSを確認・更新
3. 新規作成（初回のみ）
4. キャンセル

> 
```

## 完了条件

以下の3つの成果物が作成されたら完了：

- ✅ value-definition.md
- ✅ value-streams-mapping.md (VS0-VS7定義)
- ✅ enterprise-activities.md

## 完了メッセージ

```
✅ Phase 2: Value Definition が完了しました

成果物:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ outputs/2-value/value-definition.md
✅ outputs/2-value/value-streams-mapping.md
✅ outputs/2-value/enterprise-activities.md

📊 Value Streams定義: 8/8 完了
✅ VS0: ビジョン策定
✅ VS1: 市場機会発見
✅ VS2: 製品開発
✅ VS3: マーケティング
✅ VS4: 販売・流通
✅ VS5: カスタマーサポート
✅ VS6: データ活用
✅ VS7: 継続的改善

📊 ステータス確認:
→ `/parasol:status phase2`

🎯 次のステップ: Phase 3 Capabilities - CL1 Domain Classification
→ `/parasol:3-capabilities cl1`

💡 ヒント:
- 特定のVSを更新: `/parasol:2-value VS0`
- 全体ステータス確認: `/parasol:status`
```

## エラーケース

**前提条件未満足:**
```
❌ Phase 1が完了していません

Phase 1を先に実行してください:
→ `/parasol:1-context`
```

**無効なVS指定:**
```
❌ 無効なValue Stream: VS9

有効なオプション: VS0, VS1, VS2, VS3, VS4, VS5, VS6, VS7
```

## バリデーション

作成後、以下を自動チェック：

1. **VS完全性**: VS0-VS7が全て定義されているか
2. **活動マッピング**: 各VSにエンタープライズ活動が紐付いているか
3. **一貫性**: 価値定義とVSが整合しているか
4. **トレーサビリティ**: VS間の関係が明確か

問題がある場合：

```
⚠️ バリデーション警告

- VS3の主要活動が未定義です
- VS5とVS6の活動に重複があります
- エンタープライズ活動で未マッピングのVSがあります

修正して再度確認しますか？
→ `/parasol:validate phase2`
```

## Value Streams (VS0-VS7) について

**VS0: ビジョン策定** - 戦略的方向性の確立
**VS1: 市場機会発見** - 成長機会の特定
**VS2: 製品開発** - 製品/サービスの創造
**VS3: マーケティング** - 市場での認知獲得
**VS4: 販売・流通** - 顧客への価値提供
**VS5: カスタマーサポート** - 顧客満足の維持
**VS6: データ活用** - データからの洞察
**VS7: 継続的改善** - 価値創造の最適化

これらは企業の価値創造サイクル全体をカバーします。

## 参考資料

- **フレームワーク設計**: `parasol-v4-lite/FRAMEWORK-DESIGN.md`
- **テンプレート**: `parasol-v4-lite/templates/phase2/`
- `vs0-template.md` (VS0専用)
- `vs1-7-template.md` (VS1-7共通)
