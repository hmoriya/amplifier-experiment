# BC2: Product Recipe - 設計ストーリー

## 概要

このドキュメントはBC2 Product Recipeの設計判断理由を記録します。
チーム全員が設計の背景を理解し、将来の変更時に意図を維持するための資料です。

---

## 1. Aggregate境界の設計判断

### Recipe Aggregate

**なぜAggregateRootとしたか：**

```
判断理由:
1. 製品開発の中核エンティティ
   - 処方は製品のアイデンティティそのもの
   - 原料構成、製造仕様、品質目標が一体として管理される
   - 処方なしに製品は存在しない

2. バージョン管理の単位
   - 承認済み処方は不変（イミュータブル）
   - 変更時は新バージョンを作成
   - バージョン全体が一つのトランザクション単位

3. 承認ワークフローの対象
   - Draft → UnderReview → Approved → Production の遷移
   - 承認時に処方全体が対象（部分承認なし）
   - 監査証跡は処方単位で保持

4. ドメインエキスパートの言語
   - 開発者は「処方」を独立した管理単位として認識
   - 「RCP-BEER-202411-001を承認する」が自然な操作単位
```

**RecipeIngredientをEntityにした理由：**

```
判断:
- 原料は順序と識別が必要（第1原料、第2原料...）
- 配合比率の合計100%制約はAggregate全体で検証
- 原料単体での独立した存在意義はない
→ Aggregate内のEntityとして定義

なぜValue Objectでないか:
- 原料の追加・削除・更新操作が頻繁
- 同一原料でも配合順序が異なれば区別が必要
- ingredientIdで個別参照が必要なケースあり
```

**ProcessSpecificationをEntityにした理由：**

```
判断:
- 製造仕様は複雑なネストした構造を持つ
- 糖化→煮沸→発酵→熟成→濾過の各仕様を個別更新
- 製造現場との連携でProcessSpecification単位で参照

設計選択:
- 複合Value Objectにすると変更が煩雑
- 子Entityとして配置し、部分更新を容易に
- ただし、ProcessSpecificationだけの独立保存は不可
```

### QualityStandard Aggregate

**なぜAggregateRootとしたか：**

```
判断理由:
1. 独立したライフサイクル
   - 品質基準は処方とは異なるタイミングで更新される
   - 法規制変更、社内基準改定で独立して変更
   - 有効期間（effectiveFrom/To）による世代管理

2. 複数処方への適用可能性
   - 基本的にはrecipeId参照だが、汎用基準の可能性
   - 品質基準テンプレートとしての再利用
   - 将来の拡張性を考慮

3. 別の承認フロー
   - 品質基準の承認は処方承認とは別
   - QAチームが責任を持つ独立した管理単位
```

**代替案と却下理由：**

```
却下案: Recipe Aggregateに品質基準を含める
  → 問題: 処方変更なしに品質基準だけ更新するケースに対応できない
  → 問題: 品質基準の有効期間管理が処方と混在して複雑化
  → 決定: 別Aggregateとし、recipeIdで弱参照
```

### SensoryEvaluation Aggregate

**なぜAggregateRootとしたか：**

```
判断理由:
1. 評価セッションの独立性
   - 一つの処方に対して複数回の官能評価を実施
   - 各評価セッションは独立したイベント
   - 評価結果の比較・トレンド分析が必要

2. パネリスト管理
   - 評価者の追加・削除は評価セッション単位
   - 最低3名の制約はセッション単位で検証
   - パネリスト個別のスコアを記録

3. イベント発行
   - SensoryEvaluationCompletedイベントを発行
   - 評価完了が処方の承認判断のトリガー
   - 処方Aggregateとは非同期で連携
```

**PanelistをEntityにした理由：**

```
判断:
- パネリストはセッション内で識別される必要がある
- 個別のスコア、コメントを持つ
- パネリストの資格（PanelQualification）で権限分け

なぜ別Aggregateでないか:
- パネリスト単体での存在意義がない
- 評価セッションなしにスコアは意味をなさない
- セッション完了後にパネリスト変更はない
```

---

## 2. Value Object選択の設計判断

### なぜValue Objectにしたか

| Value Object | 選択理由 |
|--------------|----------|
| RecipeCode | フォーマット（RCP-{ProductType}-YYYYMM-NNN）を値自体が保証。等価性比較。変更時は新コード発行。 |
| RecipeVersion | セマンティックバージョニング（major.minor.patch）。不変。比較演算（v1.0.0 < v1.1.0）が必要。 |
| ProductConcept | 製品コンセプトは複数属性の集合体。全体として意味を持つ。部分更新より全置換が適切。 |
| RangeSpec | min/max/target/unitの組み合わせ。不変で、同じ範囲仕様は等価。検証ロジックを内包。 |
| Score | 1.0〜10.0の範囲制約を値が保証。精度（0.1）も型で表現。 |
| Percentage | 0〜100%の範囲制約。合計100%の検証は親Entity（RecipeIngredient）で実施。 |

### ProductTypeをEnumにした理由

```
判断:
- Beer/LowMaltBeer/Happoshu/NonAlcohol/RTD/Spirits の固定リスト
- 日本の酒税法に基づく分類
- 各タイプで異なる法規制、品質基準が適用される
- 新しい製品タイプ追加はまれ（法改正時のみ）

なぜマスターテーブルでないか:
- 追加頻度が非常に低い
- 各タイプに紐づくロジックがある
- コードでの型安全性を優先
```

### RecipeStatusの状態遷移設計

```yaml
Draft → UnderReview (submit)
UnderReview → Approved (approve)
UnderReview → Draft (reject)
Approved → Production (release)
Production → Archived (archive)
```

**設計判断：**

```
1. Draftへの戻りは「却下」のみ
   - 承認後の変更は新バージョン作成
   - 監査証跡を維持

2. Approved → Production の分離
   - 承認後も製造開始前の準備期間がある
   - 製造リリースは別のアクション

3. Archivedは終了状態
   - 戻り遷移なし
   - 復活が必要な場合は新バージョン作成
```

---

## 3. API設計の設計判断

### エンドポイント構造

```yaml
設計原則:
  RESTful: リソース指向
  CQRS対応: 読み取り専用エンドポイントの分離
  一貫性: 全BC共通パターン
```

### /recipes エンドポイント設計

```
POST /recipes
  設計理由:
  - 処方作成時の必須項目は最小限（name, productType）
  - 原料・製造仕様は後から段階的に追加
  - 下書き状態（Draft）で作成

PUT /recipes/{recipeId}
  設計理由:
  - 全体更新はDraft状態のみ許可
  - UnderReview以降は部分更新エンドポイントを使用

PATCH /recipes/{recipeId}/ingredients
PATCH /recipes/{recipeId}/process-spec
PATCH /recipes/{recipeId}/target-profile
  設計理由:
  - セクション単位の更新を明示化
  - 監査ログで「何を変更したか」が明確
  - 並行編集の競合を最小化
```

### 承認ワークフローAPI設計

```
POST /recipes/{recipeId}/submit
POST /recipes/{recipeId}/approve
POST /recipes/{recipeId}/reject
  設計理由:
  - 状態遷移をアクションとして明示化
  - 単なるPUT（status変更）ではなく、ビジネスアクション
  - 各アクションで権限チェック、バリデーション実行

  reject のボディ:
  {
    "reason": "原料Aの供給が不安定のため再検討"
  }
  → 却下理由は監査証跡として必須
```

### 官能評価API設計

```
POST /sensory-evaluations
  設計理由:
  - 評価セッションの作成
  - recipeId、evaluationType、evaluationDate が必須
  - パネリストは後から追加

POST /sensory-evaluations/{evaluationId}/panelists
  設計理由:
  - パネリスト追加は評価開始前のみ
  - 最低3名の制約は complete 時に検証

POST /sensory-evaluations/{evaluationId}/scores
  設計理由:
  - スコア記録は評価中のみ
  - パネリストごとにスコアを記録
  - リクエストボディ: { panelistId, scores: { attributeId: score } }

POST /sensory-evaluations/{evaluationId}/complete
  設計理由:
  - 明示的な完了アクション
  - 統計計算（平均、標準偏差）を実行
  - SensoryEvaluationCompletedイベント発行
```

---

## 4. インデックス設計の設計判断

### Recipeインデックス

```sql
-- 主要検索パターンとインデックス
idx_recipes_status            -- ステータス別一覧（承認待ち、製造中など）
idx_recipes_code              -- コード検索（一意、ログ連携）
idx_recipes_product_type      -- 製品タイプ別フィルタ
idx_recipes_brand             -- ブランド別処方一覧
idx_recipes_status_updated    -- 複合（ステータス + 更新日時）
```

**インデックス判断理由：**

```
ステータス別一覧:
- 「承認待ち処方一覧」が頻繁なユースケース
- 製造部門は「Production」ステータスのみ参照
- ステータスのカーディナリティは低いがインデックス効果あり

ブランド別検索:
- VS3 Brand Portfolioからの参照
- ブランドに紐づく処方一覧取得
- 外部キー制約と合わせてインデックス
```

### QualityStandardインデックス

```sql
idx_quality_recipe            -- 処方別品質基準
idx_quality_effective         -- 有効期間での検索
idx_quality_recipe_active     -- 複合（recipeId + status=Active）
```

**有効期間インデックス判断：**

```
検索パターン:
- 「今日時点で有効な品質基準」
- 範囲検索（effectiveFrom <= today <= effectiveTo）
- Btreeインデックスが適切
```

### SensoryEvaluationインデックス

```sql
idx_evaluations_recipe        -- 処方別評価一覧
idx_evaluations_date          -- 日付範囲検索
idx_evaluations_type          -- 評価タイプ別
idx_panelist_scores           -- パネリスト別スコア（分析用）
```

**パネリストスコアインデックス判断：**

```
分析要件:
- パネリストの評価傾向分析
- 評価者間の一致度計算
- 外れ値検出

設計:
- scores（JSONB）にGINインデックス
- または正規化してpanelist_scoresテーブル分離
→ 初期はJSONB、分析頻度増加で正規化検討
```

---

## 5. ドメインサービス設計判断

### RecipeDesignServiceの配置

```
判断:
- 処方設計支援は複数の情報源を参照
  - VS1 Fermentation Platformの酵母情報
  - 原料マスター
  - 過去の類似処方
- 単一Aggregateに属さない横断的機能
→ ドメインサービスとして配置

VS間連携:
- VS1のYeastStrainを参照（読み取りのみ）
- イベント（YeastStrainOptimized）で最新情報を取得
- 直接APIコールは避け、ローカルキャッシュを使用
```

### QualityAssessmentServiceの配置

```
判断:
- 品質評価は処方 + 品質基準 + 測定データを使用
- 複数Aggregateを横断
- 判定ロジックが複雑（許容範囲、逸脱レベル）
→ ドメインサービス

判定ロジック:
1. 各品質項目を基準と比較
2. 逸脱項目を特定・分類（軽微/重大）
3. 総合合否判定
4. ComplianceStatus（Pass/Fail/ConditionalPass）を返却
```

### SensoryAnalysisServiceの配置

```
判断:
- 統計分析（平均、標準偏差、外れ値検出）
- 複数評価セッションの比較
- 目標プロファイルとの差分分析
→ 純粋な計算ロジックをドメインサービス化

外れ値検出アルゴリズム:
- 2σルール（平均±2標準偏差外を外れ値）
- パネリスト資格による重み付けオプション
- 設定可能なパラメータとして外部化
```

---

## 6. VS間イベント連携の設計判断

### VS2 → VS3 イベント

| イベント | 目的 | 設計判断 |
|----------|------|----------|
| RecipeApproved | ブランド施策への利用可能通知 | 処方承認でマーケティング計画が開始可能 |
| ProductApproved | 製品情報の共有 | 品質基準クリアで正式に製品として登録 |

**イベント設計判断：**

```
RecipeApproved vs ProductApproved の分離:
- RecipeApproved: 処方自体の承認（技術的承認）
- ProductApproved: 全品質基準クリアの製品承認（商品化承認）

分離理由:
- マーケティングは処方承認時点で企画開始可能
- 製品承認は追加の品質検証後
- 2段階の通知で早期の準備開始を可能に
```

### VS1 → VS2 イベント受信

```
受信イベント:
- YeastStrainOptimized: 酵母改善情報を処方に反映可能
- YeastStrainValidated: 新規酵母が利用可能になった通知

処理方針:
- イベント受信でローカルキャッシュ更新
- 処方設計時に最新酵母情報を参照
- 既存処方への自動反映はしない（手動判断）
```

---

## 7. CQRSの設計判断

### なぜCQRSを採用したか

```
判断理由:
1. 読み取りと書き込みの頻度差
   - 処方参照（製造現場、QA）: 高頻度
   - 処方更新（開発チーム）: 低頻度
   - 読み取りモデルの最適化が有効

2. 複雑な検索要件
   - 原料構成での検索
   - 風味プロファイル類似検索
   - 検索用の非正規化ビューが有効

3. レポーティング要件
   - 品質トレンド分析
   - 処方比較レポート
   - 分析用の読み取りモデルが必要
```

### 読み取りモデル設計

```yaml
RecipeListView:
  目的: 処方一覧の高速表示
  内容: ID、コード、名前、タイプ、ステータス、更新日
  更新: RecipeCreated、RecipeSubmitted、RecipeApproved時

RecipeDetailView:
  目的: 処方詳細の完全表示
  内容: 処方全情報 + 関連品質基準 + 最新評価結果
  更新: 関連イベント発生時に非同期更新

RecipeSearchView:
  目的: 検索最適化
  内容: 検索対象フィールドを平坦化
  インデックス: 全文検索、原料検索、風味検索
```

---

## 8. 設計上の妥協と将来課題

### 現在の妥協

```
1. 原料マスター連携
   - 現在: 原料情報を処方内に埋め込み
   - 理想: 原料マスターBCとの連携
   - 理由: 初期はシンプルに、原料管理要件が明確化後に分離

2. 官能評価の統計分析
   - 現在: 基本統計（平均、標準偏差）
   - 理想: 高度な分析（PCA、クラスター分析）
   - 理由: データ蓄積後に分析要件を具体化

3. 処方バージョン管理
   - 現在: major.minor.patch のシンプルなバージョン
   - 理想: Git的な差分管理、ブランチ
   - 理由: 運用しながら要件を明確化
```

### 将来の拡張ポイント

```
1. AI支援処方設計
   - 目標風味から原料構成を自動提案
   - 過去の成功処方からの学習
   - → RecipeDesignServiceの拡張点として設計

2. 原料マスター分離
   - 原料BC（Ingredient）の新設
   - サプライチェーン連携
   - → ingredientIdの参照先を変更

3. 高度な官能分析
   - 消費者嗜好予測
   - マーケットフィット分析
   - → SensoryAnalysisServiceの拡張
```

---

**作成日**: 2025-11-28
**VS**: VS2 製品開発
**BC**: BC2 Product Recipe
**参照**: domain-language.md, api-specification.md, database-design.md
