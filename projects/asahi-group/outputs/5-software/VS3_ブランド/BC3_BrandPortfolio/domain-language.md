# BC3: Brand Portfolio - ドメイン言語定義

## 概要

| 項目 | 内容 |
|------|------|
| VS | VS3 ブランド・マーケティング |
| BC | Brand Portfolio |
| ドメインタイプ | Core |
| 技術スタック | TypeScript / NestJS |
| アーキテクチャ | Modular Monolith |

---

## 1. Module構成（Modular Monolith）

```
┌─────────────────────────────────────────────────────────────┐
│               BC3: Brand Portfolio                           │
│                [Modular Monolith]                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │   Global     │ │    Local     │ │   Campaign   │        │
│  │   Brand      │ │    Brand     │ │   Planning   │        │
│  │   Module     │ │   Module     │ │   Module     │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
│           │              │               │                  │
│           └──────────────┼───────────────┘                  │
│                          ▼                                  │
│  ┌─────────────────────────────────────────────────┐       │
│  │          PostgreSQL + Redis Cache               │       │
│  └─────────────────────────────────────────────────┘       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Aggregates

### Brand Aggregate（ブランド）

```yaml
Root Entity: Brand
Description: グローバル・ローカルブランドの管理

Properties:
  - brandId: BrandId (識別子)
  - brandCode: BrandCode (管理コード)
  - name: BrandName (ブランド名)
  - brandType: BrandType (ブランドタイプ)
  - scope: BrandScope (展開範囲)
  - identity: BrandIdentity (ブランドアイデンティティ)
  - guidelines: BrandGuidelines (ガイドライン)
  - assets: List<BrandAsset> (アセット)
  - parentBrandId: BrandId (親ブランド - optional)
  - markets: List<MarketId> (展開市場)
  - status: BrandStatus (ステータス)
  - createdAt: DateTime
  - updatedAt: DateTime

Invariants:
  - brandCodeは一意で必須
  - 名称は必須で1-100文字
  - グローバルブランドはparentBrandIdを持たない
  - ローカルブランドはparentBrandId必須
  - アクティブブランドはidentity必須

Behaviors:
  - create(): ブランド作成
  - updateIdentity(): アイデンティティ更新
  - updateGuidelines(): ガイドライン更新
  - addAsset(): アセット追加
  - removeAsset(): アセット削除
  - expandToMarket(): 市場展開
  - withdrawFromMarket(): 市場撤退
  - activate(): アクティブ化
  - archive(): アーカイブ

Entity: BrandIdentity
Properties:
  - mission: string (ミッション)
  - vision: string (ビジョン)
  - values: List<string> (価値観)
  - personality: BrandPersonality (パーソナリティ)
  - positioning: string (ポジショニング)
  - tagline: string (タグライン)
  - storyNarrative: string (ブランドストーリー)

Entity: BrandGuidelines
Properties:
  - visualIdentity: VisualIdentityGuideline
  - voiceTone: VoiceToneGuideline
  - messaging: MessagingGuideline
  - usageRules: List<UsageRule>
  - approvedTemplates: List<TemplateReference>

Entity: BrandAsset
Properties:
  - assetId: AssetId
  - assetType: AssetType (logo, image, video, document)
  - name: string
  - url: AssetUrl
  - format: string
  - resolution: string
  - usage: AssetUsage
  - expiresAt: Date (optional)
```

### Campaign Aggregate（キャンペーン）

```yaml
Root Entity: Campaign
Description: マーケティングキャンペーンの企画・管理

Properties:
  - campaignId: CampaignId (識別子)
  - campaignCode: CampaignCode (管理コード)
  - name: CampaignName (キャンペーン名)
  - brandId: BrandId (対象ブランド)
  - objective: CampaignObjective (目的)
  - targetAudience: TargetAudience (ターゲット)
  - brief: CampaignBrief (ブリーフ)
  - budget: Budget (予算)
  - timeline: CampaignTimeline (スケジュール)
  - channels: List<MarketingChannel> (チャネル)
  - creatives: List<Creative> (クリエイティブ)
  - kpis: List<CampaignKPI> (KPI)
  - status: CampaignStatus (ステータス)
  - createdAt: DateTime
  - updatedAt: DateTime

Invariants:
  - brandIdは有効なブランドを参照
  - 開始日は終了日より前
  - 承認済みキャンペーンは基本情報変更不可
  - 実行中キャンペーンは削除不可

Behaviors:
  - create(): キャンペーン作成
  - updateBrief(): ブリーフ更新
  - setBudget(): 予算設定
  - setTimeline(): スケジュール設定
  - addChannel(): チャネル追加
  - addCreative(): クリエイティブ追加
  - setKPIs(): KPI設定
  - submit(): 承認申請
  - approve(): 承認
  - launch(): 開始
  - pause(): 一時停止
  - complete(): 完了
  - evaluate(): 効果測定

Entity: CampaignBrief
Properties:
  - background: string (背景)
  - challenge: string (課題)
  - opportunity: string (機会)
  - keyMessage: string (キーメッセージ)
  - creativeDirection: string (クリエイティブ方向性)
  - mandatories: List<string> (必須要素)
  - restrictions: List<string> (制約事項)

Entity: Creative
Properties:
  - creativeId: CreativeId
  - name: string
  - format: CreativeFormat
  - channel: MarketingChannel
  - assets: List<AssetReference>
  - copy: CreativeCopy
  - status: CreativeStatus
  - approvedAt: DateTime
```

### MarketPresence Aggregate（市場プレゼンス）

```yaml
Root Entity: MarketPresence
Description: 各市場でのブランド展開状況

Properties:
  - presenceId: PresenceId (識別子)
  - brandId: BrandId (ブランド)
  - marketId: MarketId (市場)
  - localBrandName: string (現地名称)
  - localTagline: string (現地タグライン)
  - localization: MarketLocalization (ローカライズ情報)
  - performance: MarketPerformance (実績)
  - competitors: List<CompetitorInfo> (競合情報)
  - status: PresenceStatus
  - launchedAt: Date
  - updatedAt: DateTime

Invariants:
  - 同一ブランド・市場の組み合わせは一意
  - launchedAt以降のみ実績データ登録可

Behaviors:
  - establish(): プレゼンス確立
  - updateLocalization(): ローカライズ更新
  - recordPerformance(): 実績記録
  - updateCompetitors(): 競合情報更新
  - suspend(): 一時停止
  - terminate(): 終了
```

---

## 3. Value Objects

### ブランド関連

```yaml
BrandId:
  Type: UUID
  Validation: 有効なUUID形式

BrandCode:
  Type: String
  Format: "BRD-{Region}-{Type}-NNN" (例: BRD-GLB-BEER-001)
  Validation: 正規表現パターン、一意性

BrandName:
  Type: String
  Validation: 1-100文字

BrandType:
  Type: Enum
  Values: [Corporate, Master, Sub, Product, Endorsed]

BrandScope:
  Type: Enum
  Values: [Global, Regional, Local]

BrandStatus:
  Type: Enum
  Values: [Draft, Active, Sunset, Archived]
  Default: Draft

BrandPersonality:
  Type: Record
  Properties:
    - traits: List<PersonalityTrait>
    - archetypes: List<BrandArchetype>
    - toneOfVoice: ToneOfVoice
  PersonalityTrait: [Innovative, Trustworthy, Friendly, Bold, Sophisticated, Authentic]
  BrandArchetype: [Hero, Explorer, Creator, Caregiver, Ruler, Magician, etc.]

VisualIdentityGuideline:
  Type: Record
  Properties:
    - primaryColors: List<ColorSpec>
    - secondaryColors: List<ColorSpec>
    - typography: TypographySpec
    - logoUsage: LogoUsageSpec
    - imagery: ImageryGuideline
    - spacing: SpacingGuideline

ColorSpec:
  Type: Record
  Properties:
    - name: string
    - hex: string (#RRGGBB)
    - rgb: { r: number, g: number, b: number }
    - cmyk: { c: number, m: number, y: number, k: number }
    - pantone: string

VoiceToneGuideline:
  Type: Record
  Properties:
    - voiceAttributes: List<string>
    - toneByContext: Map<Context, ToneDescription>
    - doList: List<string>
    - dontList: List<string>
    - examples: List<VoiceExample>
```

### キャンペーン関連

```yaml
CampaignId:
  Type: UUID

CampaignCode:
  Type: String
  Format: "CMP-{Brand}-YYYYMM-NNN" (例: CMP-ASD-202411-001)

CampaignObjective:
  Type: Record
  Properties:
    - type: ObjectiveType
    - description: string
    - targets: List<ObjectiveTarget>
  ObjectiveType: [Awareness, Consideration, Conversion, Loyalty, Advocacy]

TargetAudience:
  Type: Record
  Properties:
    - demographics: Demographics
    - psychographics: Psychographics
    - behaviors: List<ConsumerBehavior>
    - segments: List<SegmentId>

Demographics:
  Type: Record
  Properties:
    - ageRange: { min: number, max: number }
    - gender: List<Gender>
    - income: IncomeLevel
    - location: List<GeoTarget>
    - occupation: List<string>

Psychographics:
  Type: Record
  Properties:
    - lifestyles: List<string>
    - values: List<string>
    - interests: List<string>
    - attitudes: List<string>

Budget:
  Type: Record
  Properties:
    - totalAmount: Money
    - allocation: Map<Channel, Money>
    - contingency: Money
    - currency: CurrencyCode

Money:
  Type: Record
  Properties:
    - amount: Decimal
    - currency: CurrencyCode

CampaignTimeline:
  Type: Record
  Properties:
    - planningStart: Date
    - creativeDeadline: Date
    - launchDate: Date
    - endDate: Date
    - milestones: List<Milestone>

MarketingChannel:
  Type: Enum
  Values: [TV, Radio, Print, OOH, Digital, Social, Influencer, Event, Sponsorship, Retail]

CampaignKPI:
  Type: Record
  Properties:
    - metric: KPIMetric
    - target: number
    - unit: string
    - measurementMethod: string
  KPIMetric: [Reach, Impressions, Engagement, CTR, Conversion, ROI, BrandLift, NPS]

CampaignStatus:
  Type: Enum
  Values: [Draft, Planning, Approved, InExecution, Completed, Cancelled]
```

### 市場関連

```yaml
MarketId:
  Type: String
  Format: ISO 3166-1 alpha-2 (例: JP, US, GB)

MarketLocalization:
  Type: Record
  Properties:
    - language: LanguageCode
    - culturalAdaptations: List<CulturalAdaptation>
    - regulatoryCompliance: List<RegulatoryItem>
    - localPartners: List<PartnerInfo>

MarketPerformance:
  Type: Record
  Properties:
    - marketShare: Percentage
    - salesVolume: number
    - brandAwareness: Percentage
    - brandPreference: Percentage
    - nps: number
    - period: DateRange

CompetitorInfo:
  Type: Record
  Properties:
    - competitorName: string
    - marketShare: Percentage
    - positioning: string
    - strengths: List<string>
    - weaknesses: List<string>
```

---

## 4. Domain Events

### ブランドイベント

```yaml
BrandCreated:
  Description: 新規ブランドが作成された
  Properties:
    - brandId: BrandId
    - brandCode: BrandCode
    - name: BrandName
    - brandType: BrandType
    - scope: BrandScope
    - createdAt: DateTime
  Trigger: Brand.create()

BrandIdentityUpdated:
  Description: ブランドアイデンティティが更新された
  Properties:
    - brandId: BrandId
    - updatedFields: List<string>
    - updatedAt: DateTime
  Trigger: Brand.updateIdentity()

BrandExpandedToMarket:
  Description: ブランドが新市場に展開された
  Properties:
    - brandId: BrandId
    - marketId: MarketId
    - localBrandName: string
    - expandedAt: DateTime
  Trigger: Brand.expandToMarket()

BrandGuidelinesPublished:
  Description: ブランドガイドラインが公開された
  Properties:
    - brandId: BrandId
    - version: string
    - publishedAt: DateTime
  Trigger: BrandGuidelines approved
```

### キャンペーンイベント

```yaml
CampaignCreated:
  Description: キャンペーンが作成された
  Properties:
    - campaignId: CampaignId
    - campaignCode: CampaignCode
    - brandId: BrandId
    - name: CampaignName
    - createdAt: DateTime
  Trigger: Campaign.create()

CampaignApproved:
  Description: キャンペーンが承認された
  Properties:
    - campaignId: CampaignId
    - brandId: BrandId
    - approvedBy: UserId
    - approvedAt: DateTime
  Trigger: Campaign.approve()

CampaignLaunched:
  Description: キャンペーンが開始された
  Properties:
    - campaignId: CampaignId
    - brandId: BrandId
    - channels: List<MarketingChannel>
    - launchedAt: DateTime
  Trigger: Campaign.launch()

CampaignCompleted:
  Description: キャンペーンが完了した
  Properties:
    - campaignId: CampaignId
    - brandId: BrandId
    - results: CampaignResults
    - completedAt: DateTime
  Trigger: Campaign.complete()
```

### 受信イベント（← VS2 製品開発）

```yaml
ProductApproved:
  Description: 製品が承認された（処方情報受信）
  Source: vs2.recipe.events
  Properties:
    - recipeId: RecipeId
    - productInfo: ProductInfo
    - marketingPoints: List<string>
  Handler:
    - ブランドと製品の紐付け
    - マーケティングポイントの取り込み
    - キャンペーン企画への反映
```

---

## 5. Domain Services

### BrandManagementService

```yaml
Responsibility: ブランドポートフォリオ管理
Methods:
  - getPortfolioOverview():
      Output:
        - globalBrands: List<BrandSummary>
        - regionalBrands: List<BrandSummary>
        - localBrands: List<BrandSummary>
        - metrics: PortfolioMetrics

  - analyzeBrandHierarchy(brandId):
      Input:
        - brandId: BrandId
      Output:
        - parentBrand: Brand
        - siblingBrands: List<Brand>
        - childBrands: List<Brand>
        - relationships: List<BrandRelationship>

  - evaluateBrandHealth(brandId):
      Input:
        - brandId: BrandId
      Output:
        - healthScore: Score
        - awareness: Percentage
        - preference: Percentage
        - loyalty: Percentage
        - recommendations: List<string>
```

### CampaignPlanningService

```yaml
Responsibility: キャンペーン企画支援
Methods:
  - generateCampaignBrief(brandId, objective, audience):
      Input:
        - brandId: BrandId
        - objective: CampaignObjective
        - audience: TargetAudience
      Output:
        - suggestedBrief: CampaignBrief
        - channelRecommendations: List<ChannelRecommendation>
        - budgetEstimate: BudgetEstimate

  - optimizeChannelMix(campaignId, budget):
      Input:
        - campaignId: CampaignId
        - budget: Budget
      Output:
        - optimizedAllocation: Map<Channel, Money>
        - expectedReach: number
        - expectedROI: Percentage

  - forecastCampaignPerformance(campaignId):
      Input:
        - campaignId: CampaignId
      Output:
        - projectedKPIs: Map<KPIMetric, Projection>
        - riskFactors: List<RiskFactor>
        - successProbability: Percentage
```

### BrandGuidelineService

```yaml
Responsibility: ブランドガイドライン管理
Methods:
  - getBrandGuidelines(brandId, market):
      Input:
        - brandId: BrandId
        - market: MarketId (optional)
      Output:
        - guidelines: BrandGuidelines
        - localizations: List<LocalizedGuideline>
        - assets: List<BrandAsset>

  - validateAssetCompliance(brandId, asset):
      Input:
        - brandId: BrandId
        - asset: AssetToValidate
      Output:
        - isCompliant: boolean
        - violations: List<GuidelineViolation>
        - suggestions: List<string>

  - generateStyleGuide(brandId, format):
      Input:
        - brandId: BrandId
        - format: StyleGuideFormat
      Output:
        - styleGuide: Document
        - downloadUrl: URL
```

---

## 6. Repositories

### BrandRepository

```yaml
Methods:
  - save(brand: Brand): void
  - findById(id: BrandId): Brand
  - findByCode(code: BrandCode): Brand
  - findByType(type: BrandType): List<Brand>
  - findByScope(scope: BrandScope): List<Brand>
  - findByParent(parentId: BrandId): List<Brand>
  - findByMarket(marketId: MarketId): List<Brand>
  - searchByKeyword(keyword: string): List<Brand>
  - delete(id: BrandId): void
```

### CampaignRepository

```yaml
Methods:
  - save(campaign: Campaign): void
  - findById(id: CampaignId): Campaign
  - findByCode(code: CampaignCode): Campaign
  - findByBrand(brandId: BrandId): List<Campaign>
  - findByStatus(status: CampaignStatus): List<Campaign>
  - findByDateRange(start: Date, end: Date): List<Campaign>
  - findActive(): List<Campaign>
  - searchByKeyword(keyword: string): List<Campaign>
```

### MarketPresenceRepository

```yaml
Methods:
  - save(presence: MarketPresence): void
  - findById(id: PresenceId): MarketPresence
  - findByBrand(brandId: BrandId): List<MarketPresence>
  - findByMarket(marketId: MarketId): List<MarketPresence>
  - findByBrandAndMarket(brandId: BrandId, marketId: MarketId): MarketPresence
```

---

## 7. ユビキタス言語 辞書

| 日本語 | 英語 | 定義 |
|--------|------|------|
| ブランドエクイティ | Brand Equity | ブランドが持つ資産価値・認知度・ロイヤルティの総体 |
| グローカル | Glocal | グローバル×ローカルの融合戦略 |
| ブランドアイデンティティ | Brand Identity | ブランドの本質的特性と表現要素 |
| ブランドガイドライン | Brand Guidelines | ブランド表現の統一基準 |
| タグライン | Tagline | ブランドを象徴する短いフレーズ |
| ブランドアーキテクチャ | Brand Architecture | ブランド間の関係性と階層構造 |
| マスターブランド | Master Brand | 企業や製品群を統括する親ブランド |
| サブブランド | Sub Brand | マスターブランド配下の製品ブランド |
| エンドースドブランド | Endorsed Brand | 親ブランドの支持を受けた独立ブランド |
| ブランドリフト | Brand Lift | 広告施策によるブランド認知・好感度の向上 |
| NPS | Net Promoter Score | 顧客推奨度を測る指標 |
| SOV | Share of Voice | 広告出稿量のシェア |
| IMC | Integrated Marketing Communication | 統合マーケティングコミュニケーション |

---

**作成日**: 2025-11-28
**VS**: VS3 ブランド・マーケティング
**BC**: BC3 Brand Portfolio
**次成果物**: api-specification.md
