# BC2: Product Recipe - ドメイン言語定義

## 概要

| 項目 | 内容 |
|------|------|
| VS | VS2 製品開発 |
| BC | Product Recipe |
| ドメインタイプ | Core |
| 技術スタック | Java / Spring Boot |
| アーキテクチャ | Hexagonal + CQRS |

---

## 1. Aggregates

### Recipe Aggregate（製品処方）

```yaml
Root Entity: Recipe
Description: ビール・飲料製品の処方仕様

Properties:
  - recipeId: RecipeId (識別子)
  - recipeCode: RecipeCode (管理コード)
  - name: RecipeName (製品名)
  - productType: ProductType (製品タイプ)
  - version: RecipeVersion (バージョン)
  - concept: ProductConcept (製品コンセプト)
  - ingredients: List<RecipeIngredient> (原料構成)
  - processSpec: ProcessSpecification (製造仕様)
  - targetProfile: TargetFlavorProfile (目標風味)
  - qualitySpec: QualitySpecification (品質基準)
  - status: RecipeStatus (ステータス)
  - createdAt: DateTime
  - updatedAt: DateTime
  - approvedAt: DateTime
  - approvedBy: UserId

Invariants:
  - recipeCodeは一意で必須
  - 名称は必須で1-200文字
  - 承認済み処方は変更不可（新バージョン作成）
  - ingredientsは最低1つ必要
  - 製造用処方はqualitySpec必須

Behaviors:
  - create(): 新規処方作成
  - updateIngredients(): 原料構成更新
  - updateProcessSpec(): 製造仕様更新
  - setTargetProfile(): 目標風味設定
  - setQualitySpec(): 品質基準設定
  - submit(): 承認申請
  - approve(): 承認
  - reject(): 却下
  - createNewVersion(): 新バージョン作成
  - archive(): アーカイブ

Entity: RecipeIngredient
Properties:
  - ingredientId: IngredientId
  - ingredientType: IngredientType
  - name: string
  - ratio: Percentage (配合比率)
  - specification: IngredientSpec
  - supplier: SupplierId (optional)
Invariants:
  - 配合比率の合計は100%

Entity: ProcessSpecification
Properties:
  - mashingSpec: MashingSpec (糖化仕様)
  - boilingSpec: BoilingSpec (煮沸仕様)
  - fermentationSpec: FermentationSpec (発酵仕様)
  - maturationSpec: MaturationSpec (熟成仕様)
  - filteringSpec: FilteringSpec (濾過仕様)
```

### QualityStandard Aggregate（品質基準）

```yaml
Root Entity: QualityStandard
Description: 製品品質の評価基準

Properties:
  - standardId: StandardId (識別子)
  - recipeId: RecipeId (対象処方)
  - physicalSpec: PhysicalSpecification (理化学規格)
  - sensorySpec: SensorySpecification (官能規格)
  - microbiologicalSpec: MicrobiologicalSpec (微生物規格)
  - shelfLifeSpec: ShelfLifeSpec (賞味期限規格)
  - status: StandardStatus
  - effectiveFrom: Date
  - effectiveTo: Date

Invariants:
  - recipeIdは有効な処方を参照
  - effectiveFromはeffectiveToより前
  - 有効期間は重複不可

Behaviors:
  - define(): 品質基準定義
  - update(): 基準更新
  - activate(): 有効化
  - expire(): 期限切れ処理

Entity: PhysicalSpecification
Properties:
  - alcoholContent: RangeSpec (アルコール度数)
  - originalGravity: RangeSpec (原麦汁エキス)
  - color: RangeSpec (色度)
  - bitterness: RangeSpec (苦味価)
  - carbonation: RangeSpec (炭酸ガス)
  - ph: RangeSpec (pH)

Entity: SensorySpecification
Properties:
  - appearance: SensoryAttribute (外観)
  - aroma: SensoryAttribute (香り)
  - taste: SensoryAttribute (味)
  - mouthfeel: SensoryAttribute (口当たり)
  - aftertaste: SensoryAttribute (後味)
  - overallBalance: SensoryAttribute (全体バランス)
```

### SensoryEvaluation Aggregate（官能評価）

```yaml
Root Entity: SensoryEvaluation
Description: 製品の官能評価セッション

Properties:
  - evaluationId: EvaluationId (識別子)
  - evaluationType: EvaluationType (評価タイプ)
  - recipeId: RecipeId (対象処方)
  - sampleId: SampleId (評価サンプル)
  - panelists: List<Panelist> (評価パネル)
  - evaluationDate: Date (評価日)
  - results: EvaluationResults (評価結果)
  - status: EvaluationStatus

Invariants:
  - panelistsは最低3名必要
  - 評価完了時はresults必須

Behaviors:
  - schedule(): 評価スケジュール
  - addPanelist(): パネリスト追加
  - removePanelist(): パネリスト削除
  - start(): 評価開始
  - recordScore(): スコア記録
  - complete(): 評価完了
  - generateReport(): レポート生成

Entity: Panelist
Properties:
  - panelistId: PanelistId
  - name: string
  - qualification: PanelQualification
  - scores: Map<AttributeId, Score>
  - comments: string

Entity: EvaluationResults
Properties:
  - averageScores: Map<AttributeId, AverageScore>
  - standardDeviations: Map<AttributeId, Decimal>
  - overallScore: Score
  - panelConsensus: ConsensusLevel
  - recommendation: EvaluationRecommendation
```

---

## 2. Value Objects

### 処方関連

```yaml
RecipeId:
  Type: UUID
  Validation: 有効なUUID形式

RecipeCode:
  Type: String
  Format: "RCP-{ProductType}-YYYYMM-NNN" (例: RCP-BEER-202411-001)
  Validation: 正規表現パターンマッチ、一意性

RecipeName:
  Type: String
  Validation: 1-200文字

ProductType:
  Type: Enum
  Values: [Beer, LowMaltBeer, Happoshu, NonAlcohol, RTD, Spirits]

RecipeVersion:
  Type: Record
  Properties:
    - major: Integer
    - minor: Integer
    - patch: Integer
  Format: "v{major}.{minor}.{patch}"

ProductConcept:
  Type: Record
  Properties:
    - description: String (製品説明)
    - targetConsumer: String (ターゲット消費者)
    - positioning: String (市場ポジショニング)
    - keyFeatures: List<String> (主要特徴)
    - brandId: BrandId (optional)

RecipeStatus:
  Type: Enum
  Values: [Draft, UnderReview, Approved, Production, Archived]
  Default: Draft
  Transitions:
    Draft -> UnderReview (submit)
    UnderReview -> Approved (approve)
    UnderReview -> Draft (reject)
    Approved -> Production (release)
    Production -> Archived (archive)
```

### 原料関連

```yaml
IngredientType:
  Type: Enum
  Values: [Malt, Hop, Yeast, Water, Adjunct, Additive]

IngredientSpec:
  Type: Record
  Properties:
    - grade: String (グレード)
    - origin: String (産地)
    - characteristics: Map<String, String>

Percentage:
  Type: Decimal
  Range: 0.00 to 100.00
  Precision: 0.01
  Validation: 合計が100%になること
```

### 製造仕様関連

```yaml
MashingSpec:
  Type: Record
  Properties:
    - mashInTemperature: Temperature
    - mashSteps: List<MashStep>
    - waterToGrainRatio: Ratio
    - totalMashTime: Duration

MashStep:
  Type: Record
  Properties:
    - temperature: Temperature
    - duration: Duration
    - purpose: String (例: 糖化休止、タンパク分解)

BoilingSpec:
  Type: Record
  Properties:
    - boilDuration: Duration
    - hopAdditions: List<HopAddition>
    - evaporationRate: Percentage

HopAddition:
  Type: Record
  Properties:
    - hopVariety: String
    - amount: Weight
    - additionTime: Duration (煮沸開始からの時間)
    - purpose: enum [Bittering, Flavor, Aroma, DryHop]

FermentationSpec:
  Type: Record
  Properties:
    - yeastStrainId: StrainId
    - pitchRate: CellConcentration
    - fermentationTemperature: Temperature
    - fermentationDuration: Duration
    - attenuationTarget: Percentage
```

### 品質関連

```yaml
RangeSpec:
  Type: Record
  Properties:
    - min: Decimal
    - max: Decimal
    - target: Decimal
    - unit: String
  Validation: min <= target <= max

SensoryAttribute:
  Type: Record
  Properties:
    - attributeName: String
    - targetScore: Score
    - acceptableRange: RangeSpec
    - description: String

Score:
  Type: Decimal
  Range: 1.0 to 10.0
  Precision: 0.1

EvaluationType:
  Type: Enum
  Values: [Development, QualityCheck, Benchmark, Consumer]

ConsensusLevel:
  Type: Enum
  Values: [High, Medium, Low]
  Definition:
    High: 標準偏差 < 0.5
    Medium: 標準偏差 0.5-1.0
    Low: 標準偏差 > 1.0
```

---

## 3. Domain Events

### 処方イベント

```yaml
RecipeCreated:
  Description: 新規処方が作成された
  Properties:
    - recipeId: RecipeId
    - recipeCode: RecipeCode
    - name: RecipeName
    - productType: ProductType
    - createdBy: UserId
    - createdAt: DateTime
  Trigger: Recipe.create()

RecipeSubmitted:
  Description: 処方が承認申請された
  Properties:
    - recipeId: RecipeId
    - submittedBy: UserId
    - submittedAt: DateTime
  Trigger: Recipe.submit()

RecipeApproved:
  Description: 処方が承認された
  Properties:
    - recipeId: RecipeId
    - recipeCode: RecipeCode
    - name: RecipeName
    - approvedBy: UserId
    - approvedAt: DateTime
  Trigger: Recipe.approve()
  Subscribers: [BrandPortfolio, ProductInnovation]
  VS間: Yes (→ VS3)

RecipeRejected:
  Description: 処方が却下された
  Properties:
    - recipeId: RecipeId
    - rejectedBy: UserId
    - reason: String
    - rejectedAt: DateTime
  Trigger: Recipe.reject()

RecipeReleasedToProduction:
  Description: 処方が製造リリースされた
  Properties:
    - recipeId: RecipeId
    - recipeCode: RecipeCode
    - version: RecipeVersion
    - releasedAt: DateTime
  Trigger: RecipeStatus → Production
  Subscribers: [SupplyChain, QualityAssurance]

ProductApproved:
  Description: 製品が最終承認された（VS3へ通知）
  Properties:
    - recipeId: RecipeId
    - productInfo: ProductInfo
    - marketingPoints: List<String>
    - approvedAt: DateTime
  Trigger: 全ての品質基準クリア
  Subscribers: [BrandPortfolio]
  VS間: Yes (→ VS3)
```

### 品質イベント

```yaml
QualityStandardDefined:
  Description: 品質基準が定義された
  Properties:
    - standardId: StandardId
    - recipeId: RecipeId
    - definedAt: DateTime
  Trigger: QualityStandard.define()

SensoryEvaluationCompleted:
  Description: 官能評価が完了した
  Properties:
    - evaluationId: EvaluationId
    - recipeId: RecipeId
    - overallScore: Score
    - recommendation: EvaluationRecommendation
    - completedAt: DateTime
  Trigger: SensoryEvaluation.complete()

QualityCheckPassed:
  Description: 品質チェックに合格した
  Properties:
    - recipeId: RecipeId
    - checkType: String
    - passedAt: DateTime
  Trigger: 全品質基準クリア

QualityCheckFailed:
  Description: 品質チェックに不合格
  Properties:
    - recipeId: RecipeId
    - checkType: String
    - failureReasons: List<String>
    - failedAt: DateTime
  Trigger: 品質基準未達
```

---

## 4. Domain Services

### RecipeDesignService

```yaml
Responsibility: 処方設計支援
Methods:
  - designRecipe(concept, targetProfile, constraints):
      Input:
        - concept: ProductConcept
        - targetProfile: TargetFlavorProfile
        - constraints: RecipeConstraints
      Output:
        - suggestedRecipe: RecipeSuggestion
        - ingredientRecommendations: List<IngredientRecommendation>
      Logic:
        - コンセプトから原料構成を提案
        - 目標風味達成のための配合計算
        - 制約条件（コスト、供給）の考慮

  - calculateNutrition(recipe):
      Input:
        - recipe: Recipe
      Output:
        - nutritionFacts: NutritionFacts
      Logic:
        - 原料からカロリー、炭水化物等を計算
        - 法規制に基づく表示値算出
```

### QualityAssessmentService

```yaml
Responsibility: 品質評価
Methods:
  - assessQuality(recipeId, sampleData):
      Input:
        - recipeId: RecipeId
        - sampleData: SampleData
      Output:
        - assessmentResult: QualityAssessmentResult
        - compliance: ComplianceStatus
      Logic:
        - 品質基準との比較
        - 逸脱項目の特定
        - 合否判定

  - predictShelfLife(recipe, storageConditions):
      Input:
        - recipe: Recipe
        - storageConditions: StorageConditions
      Output:
        - predictedShelfLife: Duration
        - stabilityFactors: List<StabilityFactor>
```

### SensoryAnalysisService

```yaml
Responsibility: 官能評価分析
Methods:
  - analyzeResults(evaluationId):
      Input:
        - evaluationId: EvaluationId
      Output:
        - analysis: SensoryAnalysis
        - outliers: List<OutlierScore>
        - consensus: ConsensusReport
      Logic:
        - 統計分析（平均、標準偏差）
        - 外れ値検出
        - パネル一致度評価

  - compareToTarget(evaluationId, targetProfile):
      Input:
        - evaluationId: EvaluationId
        - targetProfile: TargetFlavorProfile
      Output:
        - comparison: ProfileComparison
        - deviations: List<AttributeDeviation>
```

---

## 5. Repositories

### RecipeRepository

```yaml
Methods:
  - save(recipe: Recipe): void
  - findById(id: RecipeId): Recipe
  - findByCode(code: RecipeCode): Recipe
  - findByStatus(status: RecipeStatus): List<Recipe>
  - findByProductType(type: ProductType): List<Recipe>
  - findByBrand(brandId: BrandId): List<Recipe>
  - searchByKeyword(keyword: String): List<Recipe>
  - getVersionHistory(recipeId: RecipeId): List<RecipeVersion>
  - delete(id: RecipeId): void
```

### QualityStandardRepository

```yaml
Methods:
  - save(standard: QualityStandard): void
  - findById(id: StandardId): QualityStandard
  - findByRecipe(recipeId: RecipeId): QualityStandard
  - findActiveByRecipe(recipeId: RecipeId): QualityStandard
  - findByEffectiveDate(date: Date): List<QualityStandard>
```

### SensoryEvaluationRepository

```yaml
Methods:
  - save(evaluation: SensoryEvaluation): void
  - findById(id: EvaluationId): SensoryEvaluation
  - findByRecipe(recipeId: RecipeId): List<SensoryEvaluation>
  - findByDateRange(start: Date, end: Date): List<SensoryEvaluation>
  - findByPanelist(panelistId: PanelistId): List<SensoryEvaluation>
```

---

## 6. ユビキタス言語 辞書

| 日本語 | 英語 | 定義 |
|--------|------|------|
| 処方 | Recipe | 原料配合・製造条件の仕様書 |
| 辛口 | Karakuchi | Super Dryの特徴的な味わい（キレ・爽快感） |
| 官能評価 | Sensory Evaluation | 訓練された評価者による味覚・嗅覚評価 |
| 官能パネル | Sensory Panel | 訓練された評価者グループ |
| 原麦汁エキス | Original Gravity | 発酵前の麦汁中の糖分濃度 |
| 苦味価 | Bitterness Unit (IBU) | ホップ由来の苦味の強さを示す単位 |
| 糖化 | Mashing | 麦芽のデンプンを糖に変換する工程 |
| 煮沸 | Boiling | 麦汁を煮沸しホップを添加する工程 |
| 熟成 | Maturation | 発酵後の貯蔵・熟成期間 |
| 濾過 | Filtering | 酵母や不純物を除去する工程 |
| ドライホッピング | Dry Hopping | 発酵後にホップを添加する手法 |
| アテニュエーション | Attenuation | 糖がアルコールに変換される割合（発酵度） |

---

**作成日**: 2025-11-28
**VS**: VS2 製品開発
**BC**: BC2 Product Recipe
**次成果物**: api-specification.md
