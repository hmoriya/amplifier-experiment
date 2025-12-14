---
description: Initialize project from company URL (project:parasol)
---

# Parasol V5 - Phase 0: Initialize from URL

会社のウェブサイトURLから自動的にプロジェクトコンテキストと価値定義の初期案を生成します。

## 使用方法

```bash
/parasol:0-init https://company.example.com
/parasol:0-init https://company.example.com --deep  # より詳細な分析（複数ページ）
```

## 目的

手動でのコンテキスト確立に時間がかかる場合、会社の公開情報から自動的に：
- **Phase 1: Context** の成果物を生成
- **Phase 2: Value Definition** の初期案を生成
- 後続のコマンドで洗練・修正可能な形式で出力



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

## 🤖 使用するAmplifierサブエージェント

このコマンドは複数のサブエージェントを**並行実行**して効率的に分析します：

### 1. WebFetch（情報収集）
会社URLから以下の情報を収集：
- About Us / Company Profile
- Vision / Mission / Values
- Products / Services
- Company History / Timeline
- Leadership Team
- Press Releases / News

### 2. content-researcher（コンテンツ抽出）
収集した情報から構造化データを抽出：
- 組織概要
- ビジョン・ミッション・バリュー
- 事業内容とサービス
- 主要ステークホルダー
- 市場ポジショニング

### 3. analysis-engine（深い分析）
DEEP modeで詳細分析：
- 競合分析（推測）
- 市場環境評価
- SWOT分析の初期案
- ステークホルダーマッピング

### 4. zen-architect（戦略分析）
ANALYZE modeで戦略的分析：
- Value Streams候補の抽出（VS0-VS7）
- エンタープライズ活動の識別
- ドメイン分類の初期案

## 実行フロー

### ステップ1: URL検証と情報収集

```
ユーザー入力: https://company.example.com
↓
URL検証（有効性チェック）
↓
WebFetch tool 起動（並行実行）
├─ メインページ（About Us, Home）
├─ Vision/Mission ページ
├─ Products/Services ページ
└─ News/Blog ページ（オプション）
↓
outputs/0-init/raw-content.md に保存
```

### ステップ2: 並行サブエージェント実行

```
🔄 並行実行（Task toolで3つ同時起動）

Task 1: content-researcher
プロンプト:
"""
以下の会社ウェブサイトコンテンツから構造化情報を抽出してください：

{raw-content}

抽出項目:
1. 組織概要（会社名、設立年、本社、従業員数、売上）
2. ビジョン・ミッション・バリュー
3. 事業内容（製品・サービスの詳細）
4. 沿革・歴史
5. 経営陣・組織構造
6. 市場ポジショニング
7. 主要顧客セグメント
8. 技術スタック・プラットフォーム（記載があれば）

出力形式: 構造化Markdown
"""
↓
outputs/0-init/structured-info.md

Task 2: analysis-engine (DEEP mode)
プロンプト:
"""
以下の会社情報を深く分析してください：

{structured-info}

分析項目:
1. 市場環境分析
- 業界トレンド
- 市場規模と成長性
- 規制環境
2. 競合分析（推測）
- 主要競合
- 差別化要因
3. SWOT分析
- 強み（Strengths）
- 弱み（Weaknesses）
- 機会（Opportunities）
- 脅威（Threats）
4. ステークホルダー分析
- 主要ステークホルダー
- Power/Interest マトリックス

出力形式: 分析レポート（Markdown）
"""
↓
outputs/0-init/analysis-report.md

Task 3: zen-architect (ANALYZE mode)
プロンプト:
"""
以下の会社情報から戦略的な価値の流れ（Value Streams）を抽出してください：

{structured-info}
{analysis-report}

タスク:
1. Value Streams候補の識別（VS0-VS7）
- VS0: ビジョン策定
- VS1: 市場機会発見
- VS2: 製品開発
- VS3: マーケティング
- VS4: 販売・流通
- VS5: カスタマーサポート
- VS6: データ活用
- VS7: 業務改善

2. エンタープライズ活動の識別
- 各VSに紐づく主要活動

3. 初期ドメイン分類案
- Core Domain候補
- Supporting Domain候補
- Generic Domain候補

出力形式: 戦略分析レポート（Markdown）
"""
↓
outputs/0-init/strategic-analysis.md
```

### ステップ3: Phase 1 成果物生成

3つのサブエージェント結果を統合して Phase 1 成果物を生成：

**outputs/1-context/organization-analysis.md**
```markdown
# 組織分析

## 組織概要
{content-researcher から}

## 事業構造
{content-researcher から}

## 戦略方向性
{zen-architect から}

## グループガバナンス
{structured-info から}

---
⚠️ **自動生成**: このドキュメントは会社URLから自動生成されました。
レビューして必要に応じて修正してください。
```

**outputs/1-context/market-assessment.md**
```markdown
# 市場評価

## 市場環境
{analysis-engine から}

## 競合分析
{analysis-engine から（推測ベース）}

## 顧客セグメント
{structured-info から}

---
⚠️ **自動生成・要検証**: 競合分析は推測に基づきます。
実際の市場調査結果で補完してください。
```

**outputs/1-context/constraints.md**
```markdown
# 制約事項

## 技術制約
{structured-info から技術スタック情報}

## 組織制約
（テンプレート - 手動入力推奨）

## 規制制約
{analysis-engine から規制環境}

## 時間制約
（テンプレート - 手動入力推奨）

---
⚠️ **要補完**: 多くの制約は手動で追加する必要があります。
```

**outputs/1-context/stakeholder-map.md**
```markdown
# ステークホルダーマップ

## ステークホルダー識別
{analysis-engine から}

## 影響マップ（Power/Interest）
{analysis-engine から}

---
⚠️ **自動生成**: Power/Interest評価は推測に基づきます。
実際のステークホルダー分析で検証してください。
```

### ステップ4: Phase 2 初期案生成

**outputs/2-value/value-definition.md**
```markdown
# 価値定義

## ビジョン
{structured-info から}

## ミッション
{structured-info から}

## コアバリュー
{structured-info から}

## 戦略目標
{strategic-analysis から}

---
⚠️ **初期案**: 公開情報から生成した初期案です。
内部の戦略文書と照合して洗練してください。
```

**outputs/2-value/value-streams-mapping.md**
```markdown
# Value Streams マッピング

{zen-architect の VS0-VS7 候補}

---
⚠️ **候補案**: これは初期候補です。
`/parasol:2-value` コマンドで各VSを詳細化してください。
```

**outputs/2-value/enterprise-activities.md**
```markdown
# エンタープライズ活動

{zen-architect のエンタープライズ活動識別}

---
⚠️ **初期案**: 各VSの主要活動の初期案です。
実際の業務フローと照合して詳細化してください。
```

### ステップ5: 結果レポート

```
✅ Phase 0: Initialize from URL 完了

会社URL: https://company.example.com
収集ページ数: 5
分析時間: 約3-5分

生成成果物:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 outputs/0-init/ (分析データ)
✅ raw-content.md - 収集した生コンテンツ
✅ structured-info.md - 構造化情報
✅ analysis-report.md - 深い分析レポート
✅ strategic-analysis.md - 戦略分析レポート

📁 outputs/1-context/ (Phase 1 - 自動生成)
✅ organization-analysis.md
✅ market-assessment.md
⚠️ constraints.md (要補完)
✅ stakeholder-map.md

📁 outputs/2-value/ (Phase 2 - 初期案)
✅ value-definition.md
✅ value-streams-mapping.md (VS0-VS7 候補)
✅ enterprise-activities.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ 重要な注意事項:

1. **自動生成の限界**: 
公開情報からの推測が含まれます。必ずレビューしてください。

2. **要手動補完**: 
- 技術制約の詳細
- 組織内部の制約
- 時間制約
- 正確な競合分析

3. **次のステップ**:
a. 生成された成果物をレビュー・修正
b. Phase 1を完全にするため: `/parasol:1-context` で追加情報を補完
c. Phase 2のVS詳細化: `/parasol:2-value VS0` から順に

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 自動生成品質スコア:

組織分析:       ★★★★☆ (80%) - 公開情報から十分な情報取得
市場評価:       ★★★☆☆ (60%) - 競合分析は推測ベース、要検証
制約事項:       ★★☆☆☆ (40%) - 多くの制約は手動入力必要
ステークホルダー: ★★★☆☆ (60%) - 主要SHは識別、Power/Interestは推測
Value Streams:  ★★★★☆ (75%) - 良い初期候補、詳細化必要

総合スコア: ★★★☆☆ (65%)

推奨: 自動生成を出発点として、内部情報で補完してください。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 推奨ワークフロー:

1. outputs/0-init/ のレポートを読む（背景理解）
2. outputs/1-context/ の各ファイルをレビュー・修正
3. constraints.md を手動で補完
4. outputs/2-value/ をレビュー
5. `/parasol:2-value VS0` から各VSを詳細化
6. `/parasol:status` で進捗確認
7. `/parasol:3-capabilities cl1` でドメイン分類へ
```

## --deep オプション

より詳細な分析を実行：

```bash
/parasol:0-init https://company.example.com --deep
```

**追加動作**:
- より多くのページをクロール（最大10ページ）
- 各VSについてより詳細な分析
- 競合企業のURL分析（指定された場合）
- より詳細なSWOT分析

**実行時間**: 約10-15分（通常の3倍）

## エラーケース

### URLが無効

```
❌ 無効なURL: xyz

有効なURL形式:
- https://company.example.com
- http://company.example.com

使用例:
→ `/parasol:0-init https://company.example.com`
```

### URLにアクセスできない

```
❌ URLにアクセスできませんでした: https://company.example.com

考えられる原因:
- URLが存在しない（404エラー）
- アクセス制限（認証が必要）
- ネットワークエラー

対処法:
1. URLを確認してください
2. 公開されているページか確認
3. 手動で `/parasol:1-context` を実行
```

### 情報が不十分

```
⚠️ 収集できた情報が不十分です

収集できた情報:
- 組織概要: あり
- ビジョン/ミッション: なし ❌
- 事業内容: あり
- その他: 不足

推奨アクション:
1. 別のURL（About Usページなど）を試す
2. 手動で `/parasol:1-context` を実行して情報を補完
```

### outputs/ ディレクトリが既に存在

```
⚠️ outputs/ディレクトリが既に存在します

既存のParasolプロジェクトがあります。
上書きしますか？

オプション:
1. 上書き（既存データは失われます）
2. キャンセル（既存プロジェクトを保持）
3. マージ（既存データと統合）

推奨: 既存プロジェクトがある場合はキャンセルし、
手動で必要な部分のみ更新してください。
```

## サブエージェント実行時の注意

### content-researcher のフィードバック

```
⚠️ content-researcher からのフィードバック:

"収集したコンテンツからビジョン・ミッションが明確に抽出できません。
About Usページに記載がない可能性があります。"

推奨アクション:
- Vision/Missionページの直接URLを指定
- または手動で `/parasol:2-value` で入力
```

### analysis-engine のフィードバック

```
⚠️ analysis-engine からのフィードバック:

"競合分析を行うための市場情報が不足しています。
業界レポートやプレスリリースの追加が推奨されます。"

推奨アクション:
- --deep オプションでより多くのページを分析
- 手動で市場評価を補完
```

## 利点と制限

### ✅ 利点

1. **大幅な時間短縮**: 手動入力の50-70%を自動化
2. **客観的な視点**: 公開情報からの客観的分析
3. **見落とし防止**: 重要な情報の自動抽出
4. **一貫性**: 構造化されたフォーマット
5. **即座に開始**: URLだけでプロジェクト開始可能

### ⚠️ 制限

1. **公開情報のみ**: 内部情報は含まれない
2. **推測を含む**: 競合分析などは推測ベース
3. **手動検証必須**: 自動生成結果の検証が必要
4. **言語制約**: 英語サイトの方が精度高い
5. **技術詳細不足**: 技術スタックの詳細は限定的

## ベストプラクティス

### 🎯 推奨される使い方

1. **出発点として利用**
- 自動生成を叩き台として利用
- 内部情報で補完・修正

2. **段階的な洗練**
- Phase 1: 自動生成 → レビュー → 補完
- Phase 2: VS候補 → 各VS詳細化
- Phase 3以降: 通常のワークフロー

3. **検証ポイント**
- ビジョン/ミッションの正確性
- 事業内容の網羅性
- ステークホルダーの完全性
- Value Streamsの妥当性

### 🚫 避けるべき使い方

1. **自動生成を鵜呑みにする**
- 必ずレビューと検証を実施

2. **内部情報を無視**
- 公開情報だけでは不十分
- 内部の戦略文書と照合必須

3. **スキップしすぎ**
- 制約事項などの手動補完を省略しない

## 次のステップ

### 自動生成後の推奨ワークフロー

```bash
# 1. 生成結果のレビュー
/parasol:status

# 2. Phase 1 の補完（必要に応じて）
/parasol:1-context

# 3. Phase 2 の各VS詳細化
/parasol:2-value VS0
/parasol:2-value VS1
# ... VS7まで

# 4. 検証
/parasol:validate phase1
/parasol:validate phase2

# 5. Phase 3 へ進む
/parasol:3-capabilities cl1
```

## 関連コマンド

- `/parasol:1-context` - Phase 1: Context（手動または補完）
- `/parasol:2-value` - Phase 2: Value Definition（詳細化）
- `/parasol:status` - 進捗確認
- `/parasol:validate` - 生成結果の検証
- `/parasol:0-help` - ヘルプシステム
