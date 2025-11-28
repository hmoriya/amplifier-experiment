# Use Case: 酵母株推薦 (Recommend Yeast Strain)

## 概要

| 項目 | 内容 |
|------|------|
| UC ID | BC1-UC-003 |
| 名称 | 酵母株推薦 |
| アクター | 醸造技術者、製品開発者、研究員 |
| トリガー | 新製品開発時、既存製品改良時 |
| 関連集約 | YeastStrain |
| 関連サービス | YeastRecommendationService |

---

## ユースケース記述

### 事前条件 (Preconditions)

1. アクターは認証済みで、酵母推薦機能へのアクセス権を持つ
2. システムに十分な酵母株データが登録されている
3. 目標とする風味プロファイルまたは発酵条件が明確

### 事後条件 (Postconditions)

1. 条件に適合する酵母株のランキングリストが生成される
2. 各推薦にマッチスコアと根拠が付与される
3. 推薦結果をセッションに保存（発酵プロセス開始への引継ぎ用）

### 基本フロー (Main Flow)

1. **開始**: アクターが「酵母株推薦」機能を選択
2. **推薦モード選択**:
   - 風味プロファイルベース
   - 発酵条件ベース
   - ハイブリッド（両方指定）
3. **目標入力**:
   - **風味プロファイル**: エステル/フェノール/フルーティ等のレベル
   - **発酵条件**: 温度範囲、発酵速度、発酵度
4. **制約条件入力**（任意）:
   - スケールタイプ制限
   - 除外株の指定
   - ステータス制限（Validated以上等）
5. **推薦実行**: システムがマッチング分析を実行
6. **結果表示**:
   - 推薦株のランキング（最大10件）
   - 各株のマッチスコア（0-100%）
   - マッチ/ミスマッチ項目の詳細
7. **詳細確認**: 任意の株を選択して詳細表示
8. **アクション選択**:
   - 発酵プロセス開始へ進む
   - 比較分析を実行
   - 結果をエクスポート

### 代替フロー (Alternative Flows)

**A1: テンプレートからの推薦**
- ステップ2で「テンプレートから選択」を選択
- 定義済みプロファイル（ラガー、エール、小麦等）を選択
- テンプレート値をベースに微調整

**A2: 既存製品からの推薦**
- ステップ2で「既存製品から」を選択
- BC2から製品レシピを参照
- 製品の目標プロファイルを取得して推薦実行

**A3: 複数条件での比較推薦**
- ステップ3で「複数条件を設定」を選択
- 最大3セットの条件を入力
- 各条件セットに対する推薦を並列表示

### 例外フロー (Exception Flows)

**E1: 適合株なし**
- マッチスコア閾値（50%）を超える株がない場合
- 「条件を満たす酵母株が見つかりません」を表示
- 条件の緩和を提案

**E2: データ不足**
- 酵母株データが10件未満の場合
- 警告を表示し、限定的な推薦結果を返す

---

## ビジネスルール

| BR ID | ルール | 検証タイミング |
|-------|--------|----------------|
| BR-020 | マッチスコア50%未満は非表示 | 結果生成時 |
| BR-021 | Production用途はValidated以上の株のみ | 制約適用時 |
| BR-022 | 推薦結果は最大10件 | 結果生成時 |
| BR-023 | 風味マッチは各項目±1レベルまで許容 | スコア計算時 |
| BR-024 | 過去成功実績のある株は+10%ボーナス | スコア計算時 |

---

## 推薦アルゴリズム

### スコア計算ロジック

```yaml
MatchScore:
  flavorMatch: 40%
    - 各FlavorLevel項目のマッチ度
    - 完全一致: 100%, ±1レベル: 70%, ±2レベル: 30%

  conditionMatch: 30%
    - 温度範囲の適合度
    - 発酵速度の一致度
    - 発酵度範囲のオーバーラップ

  historicalSuccess: 20%
    - 過去プロセスの成功率
    - 類似条件での実績

  availability: 10%
    - 現在のステータス（Production > Validated > Research）
    - 在庫/培養状況
```

---

## データ要件

### 入力データ

```yaml
YeastRecommendationInput:
  mode: enum [FlavorBased, ConditionBased, Hybrid]
  targetFlavorProfile: (if FlavorBased or Hybrid)
    esterLevel: FlavorLevel (optional)
    phenolLevel: FlavorLevel (optional)
    sulfurLevel: FlavorLevel (optional)
    fruitiness: FlavorLevel (optional)
    spiciness: FlavorLevel (optional)
    cleanness: FlavorLevel (optional)
  targetConditions: (if ConditionBased or Hybrid)
    temperatureRange: {min, max}
    fermentationSpeed: enum [Slow, Medium, Fast]
    targetAttenuation: percentage
  constraints:
    scaleType: enum [Laboratory, Pilot, Production] (optional)
    excludeStrainIds: array<uuid> (optional)
    minStatus: enum [Research, Validated, Production] (optional)
  maxResults: integer (default: 10, max: 20)
```

### 出力データ

```yaml
YeastRecommendationOutput:
  recommendations:
    - strain: YeastStrain
      matchScore: decimal (0-1)
      matchDetails:
        flavorMatch: decimal
        conditionMatch: decimal
        historicalSuccess: decimal
        availability: decimal
      matchedItems: array<string>
      mismatchedItems: array<string>
      notes: array<string>
  queryId: uuid (for session tracking)
  generatedAt: datetime
```

---

## 非機能要件

| 項目 | 要件 |
|------|------|
| 応答時間 | 推薦生成: 5秒以内 |
| キャッシュ | 同一条件は1時間キャッシュ |
| 精度 | マッチスコア±5%の精度 |

---

## 関連API

- POST `/recommendations/yeast` - 酵母株推薦
- GET `/yeast-strains/{strainId}` - 株詳細取得
- POST `/yeast-strains/compare` - 株比較
- POST `/fermentation-processes` - 推薦結果から発酵開始

---

## VS間連携

### BC2 ProductRecipe との連携

- 既存製品のターゲットプロファイル取得
- 推薦結果をレシピ設計に反映

### BC5 ProductInnovation との連携

- 新製品開発時の酵母探索
- 実験的な風味プロファイル推薦

---

**作成日**: 2025-11-28
**VS/BC**: VS1/BC1 Fermentation Platform
