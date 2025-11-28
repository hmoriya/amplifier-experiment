# BC1: Fermentation Platform - ドメイン言語定義

## 概要

| 項目 | 内容 |
|------|------|
| VS | VS1 研究開発 |
| BC | Fermentation Platform |
| ドメインタイプ | Core |
| 技術スタック | Python / FastAPI |
| アーキテクチャ | Hexagonal + Event Sourcing |

---

## 1. Aggregates

### YeastStrain Aggregate（酵母株）

```yaml
Root Entity: YeastStrain
Description: 特定の特性を持つ酵母の系統

Properties:
  - strainId: StrainId (識別子)
  - strainCode: StrainCode (管理コード)
  - name: StrainName (名称)
  - origin: StrainOrigin (由来)
  - characteristics: YeastCharacteristics (特性)
  - flavorProfile: FlavorProfile (風味プロファイル)
  - fermentationProfile: FermentationProfile (発酵特性)
  - status: StrainStatus (ステータス)
  - registeredAt: DateTime (登録日時)
  - updatedAt: DateTime (更新日時)

Invariants:
  - strainCodeは一意で必須
  - 名称は必須で1-100文字
  - characteristicsは最低1項目必要
  - 実験用株は商用利用不可

Behaviors:
  - register(): 新規酵母株登録
  - updateCharacteristics(): 特性情報更新
  - updateFlavorProfile(): 風味プロファイル更新
  - optimize(): 最適化情報登録
  - archive(): アーカイブ化
  - activate(): 再活性化
```

### FermentationProcess Aggregate（発酵プロセス）

```yaml
Root Entity: FermentationProcess
Description: 発酵条件と経過を管理するプロセス

Properties:
  - processId: ProcessId (識別子)
  - processCode: ProcessCode (管理コード)
  - strainId: StrainId (使用酵母株)
  - conditions: FermentationConditions (発酵条件)
  - timeline: List<FermentationStage> (発酵ステージリスト)
  - measurements: List<ProcessMeasurement> (測定データ)
  - scaleType: ScaleType (スケールタイプ)
  - status: ProcessStatus (ステータス)
  - startedAt: DateTime (開始日時)
  - completedAt: DateTime (完了日時)

Invariants:
  - strainIdは有効な酵母株を参照
  - conditionsは必須
  - scaleTypeに応じた条件制約あり
  - 完了時は結果データ必須

Behaviors:
  - start(): プロセス開始
  - recordMeasurement(): 測定データ記録
  - adjustConditions(): 条件調整
  - advanceStage(): ステージ進行
  - complete(): プロセス完了
  - abort(): プロセス中断

Entity: FermentationStage
Properties:
  - stageId: StageId
  - name: StageName
  - targetConditions: FermentationConditions
  - duration: Duration
  - status: StageStatus

Entity: ProcessMeasurement
Properties:
  - measurementId: MeasurementId
  - measuredAt: DateTime
  - temperature: Temperature
  - ph: PhValue
  - gravity: SpecificGravity
  - cellCount: CellCount
  - notes: string
```

### ResearchExperiment Aggregate（研究実験）

```yaml
Root Entity: ResearchExperiment
Description: 微生物学研究の実験管理

Properties:
  - experimentId: ExperimentId (識別子)
  - experimentCode: ExperimentCode (管理コード)
  - title: string (タイトル)
  - hypothesis: string (仮説)
  - methodology: ExperimentMethodology (実験手法)
  - strainIds: List<StrainId> (使用酵母株)
  - variables: List<ExperimentVariable> (実験変数)
  - results: ExperimentResults (実験結果)
  - findings: List<ResearchFinding> (発見事項)
  - status: ExperimentStatus (ステータス)
  - conductedBy: ResearcherId (実施者)
  - startedAt: DateTime (開始日)
  - completedAt: DateTime (完了日)

Invariants:
  - タイトルと仮説は必須
  - 最低1つの実験変数が必要
  - 完了時は結果が必須

Behaviors:
  - plan(): 実験計画
  - start(): 実験開始
  - recordVariable(): 変数記録
  - recordResult(): 結果記録
  - addFinding(): 発見事項追加
  - complete(): 実験完了
  - publishFindings(): 発見事項公開
```

---

## 2. Value Objects

### 酵母株関連

```yaml
StrainId:
  Type: UUID
  Validation: 有効なUUID形式

StrainCode:
  Type: String
  Format: "ASH-YYYY-NNNN" (例: ASH-2024-0001)
  Validation: 正規表現パターンマッチ、一意性

StrainName:
  Type: String
  Validation: 1-100文字

StrainOrigin:
  Type: Record
  Properties:
    - source: enum [Natural, Bred, Modified, Acquired]
    - location: string (採取地/取得元)
    - collectedAt: Date
    - parentStrainIds: List<StrainId> (親株)

YeastCharacteristics:
  Type: Record
  Properties:
    - alcoholTolerance: Percentage (アルコール耐性)
    - temperatureRange: TemperatureRange (適温範囲)
    - flocculationLevel: enum [Low, Medium, High] (凝集性)
    - attenuationRange: PercentageRange (発酵度範囲)
    - oxygenRequirement: enum [Low, Medium, High] (酸素要求量)

FlavorProfile:
  Type: Record
  Properties:
    - esterLevel: FlavorLevel (エステル)
    - phenolLevel: FlavorLevel (フェノール)
    - sulfurLevel: FlavorLevel (硫黄化合物)
    - fruitiness: FlavorLevel (フルーティさ)
    - spiciness: FlavorLevel (スパイシーさ)
    - cleanness: FlavorLevel (クリーンさ)
    - notes: List<string> (特記事項)

FlavorLevel:
  Type: Enum
  Values: [None, VeryLow, Low, Medium, High, VeryHigh]

FermentationProfile:
  Type: Record
  Properties:
    - optimalTemperature: Temperature (最適温度)
    - fermentationSpeed: enum [Slow, Medium, Fast] (発酵速度)
    - typicalDuration: DurationRange (標準発酵期間)
    - co2Production: enum [Low, Medium, High] (CO2生成量)

StrainStatus:
  Type: Enum
  Values: [Research, Validated, Production, Archived]
  Default: Research
```

### 発酵プロセス関連

```yaml
ProcessId:
  Type: UUID
  Validation: 有効なUUID形式

ProcessCode:
  Type: String
  Format: "FP-YYYYMMDD-NNN" (例: FP-20241127-001)

FermentationConditions:
  Type: Record
  Properties:
    - temperature: Temperature
    - pressure: Pressure (気圧)
    - dissolvedOxygen: Concentration (溶存酸素)
    - pitchRate: CellConcentration (接種量)
    - wortGravity: SpecificGravity (麦汁比重)

Temperature:
  Type: Decimal
  Unit: Celsius
  Range: -10.0 to 100.0
  Precision: 0.1

SpecificGravity:
  Type: Decimal
  Range: 0.990 to 1.200
  Precision: 0.001

PhValue:
  Type: Decimal
  Range: 0.0 to 14.0
  Precision: 0.01

ScaleType:
  Type: Enum
  Values: [Laboratory, Pilot, Production]
  Constraints:
    Laboratory: 1-100L
    Pilot: 100-1000L
    Production: 1000L+

ProcessStatus:
  Type: Enum
  Values: [Planned, InProgress, Completed, Aborted]
```

### 研究関連

```yaml
ExperimentId:
  Type: UUID

ExperimentCode:
  Type: String
  Format: "EXP-YYYY-NNNN"

ExperimentMethodology:
  Type: Record
  Properties:
    - type: enum [Comparative, Factorial, Optimization, Exploratory]
    - description: string
    - equipment: List<string>
    - protocols: List<ProtocolReference>

ExperimentVariable:
  Type: Record
  Properties:
    - name: string
    - type: enum [Independent, Dependent, Controlled]
    - unit: string
    - range: Range (min, max)
    - measuredValues: List<Decimal>

ExperimentResults:
  Type: Record
  Properties:
    - summary: string
    - dataFiles: List<FileReference>
    - statisticalAnalysis: StatisticalAnalysis
    - conclusion: string

ResearchFinding:
  Type: Record
  Properties:
    - findingId: FindingId
    - type: enum [Expected, Unexpected, Serendipitous]
    - description: string
    - significance: enum [Low, Medium, High, Breakthrough]
    - applicationPotential: List<string>
```

---

## 3. Domain Events

### 酵母株イベント

```yaml
YeastStrainRegistered:
  Description: 新規酵母株が登録された
  Properties:
    - strainId: StrainId
    - strainCode: StrainCode
    - name: StrainName
    - origin: StrainOrigin
    - registeredAt: DateTime
  Trigger: YeastStrain.register()
  Subscribers: [ResearchInnovation, ProductRecipe]

YeastStrainOptimized:
  Description: 酵母株が最適化された
  Properties:
    - strainId: StrainId
    - optimizationType: string
    - improvements: Map<string, Improvement>
    - optimizedAt: DateTime
  Trigger: YeastStrain.optimize()
  Subscribers: [ProductRecipe, ProductInnovation]
  VS間: Yes (→ VS2)

YeastStrainValidated:
  Description: 酵母株が製造用として検証された
  Properties:
    - strainId: StrainId
    - validationResults: ValidationResults
    - validatedAt: DateTime
  Trigger: StrainStatus → Validated
  Subscribers: [ProductRecipe]
  VS間: Yes (→ VS2)

YeastStrainArchived:
  Description: 酵母株がアーカイブされた
  Properties:
    - strainId: StrainId
    - reason: string
    - archivedAt: DateTime
  Trigger: YeastStrain.archive()
```

### 発酵プロセスイベント

```yaml
FermentationProcessStarted:
  Description: 発酵プロセスが開始された
  Properties:
    - processId: ProcessId
    - strainId: StrainId
    - conditions: FermentationConditions
    - scaleType: ScaleType
    - startedAt: DateTime
  Trigger: FermentationProcess.start()

FermentationConditionsAdjusted:
  Description: 発酵条件が調整された
  Properties:
    - processId: ProcessId
    - previousConditions: FermentationConditions
    - newConditions: FermentationConditions
    - reason: string
    - adjustedAt: DateTime
  Trigger: FermentationProcess.adjustConditions()

FermentationProcessCompleted:
  Description: 発酵プロセスが完了した
  Properties:
    - processId: ProcessId
    - strainId: StrainId
    - finalMeasurements: ProcessMeasurement
    - duration: Duration
    - completedAt: DateTime
  Trigger: FermentationProcess.complete()

FermentationDataRecorded:
  Description: 発酵測定データが記録された
  Properties:
    - processId: ProcessId
    - measurement: ProcessMeasurement
    - recordedAt: DateTime
  Trigger: FermentationProcess.recordMeasurement()
```

### 研究実験イベント

```yaml
ExperimentCompleted:
  Description: 研究実験が完了した
  Properties:
    - experimentId: ExperimentId
    - title: string
    - results: ExperimentResults
    - findings: List<ResearchFinding>
    - completedAt: DateTime
  Trigger: ResearchExperiment.complete()
  Subscribers: [ResearchInnovation]

BreakthroughDiscovered:
  Description: 画期的な発見があった
  Properties:
    - experimentId: ExperimentId
    - findingId: FindingId
    - description: string
    - applicationPotential: List<string>
    - discoveredAt: DateTime
  Trigger: Finding.significance == Breakthrough
  Subscribers: [ResearchInnovation, ProductInnovation]
  VS間: Yes (→ VS2)
```

---

## 4. Domain Services

### YeastRecommendationService

```yaml
Responsibility: 目標に適した酵母株を推薦
Methods:
  - recommendForProfile(targetFlavorProfile, constraints):
      Input:
        - targetFlavorProfile: FlavorProfile
        - constraints: RecommendationConstraints
      Output:
        - recommendations: List<YeastRecommendation>
        - confidenceScores: Map<StrainId, Score>
      Logic:
        - 風味プロファイルのマッチング
        - 発酵条件の適合性評価
        - 過去実績の考慮
        - スコアリングと順位付け

  - recommendForConditions(fermentationConditions):
      Input:
        - fermentationConditions: FermentationConditions
      Output:
        - recommendations: List<YeastRecommendation>
      Logic:
        - 温度耐性の評価
        - 発酵速度の適合性
        - スケールタイプ考慮
```

### FermentationOptimizationService

```yaml
Responsibility: 発酵条件の最適化提案
Methods:
  - optimizeConditions(strainId, targetAttributes, scaleType):
      Input:
        - strainId: StrainId
        - targetAttributes: TargetAttributes
        - scaleType: ScaleType
      Output:
        - optimalConditions: FermentationConditions
        - expectedProfile: FlavorProfile
        - confidence: Score
      Logic:
        - 過去の発酵データ分析
        - 酵母特性との最適マッチング
        - スケールアップ係数の適用
        - 予測モデルによる推定

  - predictOutcome(processId, conditions):
      Input:
        - processId: ProcessId
        - conditions: FermentationConditions
      Output:
        - predictedProfile: FlavorProfile
        - predictedDuration: Duration
        - riskFactors: List<RiskFactor>
```

### StrainComparisonService

```yaml
Responsibility: 酵母株間の比較分析
Methods:
  - compareStrains(strainIds):
      Input:
        - strainIds: List<StrainId>
      Output:
        - comparisonMatrix: ComparisonMatrix
        - recommendations: List<string>
      Logic:
        - 特性比較表の生成
        - 強み・弱みの分析
        - 用途別推薦

  - findSimilarStrains(strainId, threshold):
      Input:
        - strainId: StrainId
        - threshold: Similarity
      Output:
        - similarStrains: List<SimilarStrain>
```

---

## 5. Repositories

### YeastStrainRepository

```yaml
Methods:
  - save(strain: YeastStrain): void
  - findById(id: StrainId): YeastStrain
  - findByCode(code: StrainCode): YeastStrain
  - findByStatus(status: StrainStatus): List<YeastStrain>
  - findByCharacteristics(criteria: CharacteristicsCriteria): List<YeastStrain>
  - findByFlavorProfile(profile: FlavorProfile, threshold: Similarity): List<YeastStrain>
  - searchByKeyword(keyword: string): List<YeastStrain>
  - delete(id: StrainId): void
  - getEventHistory(id: StrainId): List<DomainEvent>
```

### FermentationProcessRepository

```yaml
Methods:
  - save(process: FermentationProcess): void
  - findById(id: ProcessId): FermentationProcess
  - findByCode(code: ProcessCode): FermentationProcess
  - findByStrain(strainId: StrainId): List<FermentationProcess>
  - findByStatus(status: ProcessStatus): List<FermentationProcess>
  - findByDateRange(start: DateTime, end: DateTime): List<FermentationProcess>
  - getTimeSeries(processId: ProcessId): List<ProcessMeasurement>
```

### ResearchExperimentRepository

```yaml
Methods:
  - save(experiment: ResearchExperiment): void
  - findById(id: ExperimentId): ResearchExperiment
  - findByCode(code: ExperimentCode): ResearchExperiment
  - findByStrain(strainId: StrainId): List<ResearchExperiment>
  - findByResearcher(researcherId: ResearcherId): List<ResearchExperiment>
  - findByStatus(status: ExperimentStatus): List<ResearchExperiment>
  - searchFindings(keyword: string): List<ResearchFinding>
```

---

## 6. ユビキタス言語 辞書

| 日本語 | 英語 | 定義 |
|--------|------|------|
| 酵母株 | Yeast Strain | 特定の特性を持つ酵母の系統 |
| 発酵プロファイル | Fermentation Profile | 発酵過程で生成される香味成分の特性パターン |
| 風味プロファイル | Flavor Profile | 製品に付与される香味特性の総合評価 |
| スケールアップ | Scale-up | 実験室規模から工場規模への移行 |
| 接種量 | Pitch Rate | 発酵開始時に添加する酵母細胞の濃度 |
| 凝集性 | Flocculation | 酵母細胞が凝集して沈降する性質 |
| 発酵度 | Attenuation | 糖がアルコールに変換される割合 |
| エステル | Ester | フルーティな香りの原因となる化合物 |
| フェノール | Phenol | スパイシーやクローブ様の香りの原因化合物 |
| 比重 | Specific Gravity | 液体の密度を水と比較した値 |
| 溶存酸素 | Dissolved Oxygen | 液体中に溶け込んでいる酸素量 |
| セレンディピティ | Serendipity | 予期せぬ幸運な発見 |

---

**作成日**: 2025-11-28
**VS**: VS1 研究開発
**BC**: BC1 Fermentation Platform
**次成果物**: api-specification.md
