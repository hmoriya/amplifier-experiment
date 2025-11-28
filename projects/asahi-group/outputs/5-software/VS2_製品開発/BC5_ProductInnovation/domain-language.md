# BC5: Product Innovation - ドメイン言語定義

## 概要

製品イノベーションのドメイン。実験的製品の企画、限定品の開発、コラボレーション企画の管理を担う。

**BCタイプ**: Supporting（VS2内でBC2を支援）
**技術スタック**: Java/Spring Boot（VS2統一）
**アーキテクチャ**: Hexagonal Architecture

---

## ユビキタス言語

### 集約（Aggregates）

#### 1. ExperimentalProduct（実験的製品）

市場テスト用の実験的な製品企画。

```
ExperimentalProduct {
  product_id: ProductId                     // 製品ID
  concept: ProductConcept                   // コンセプト
  target_segment: TargetSegment             // ターゲット層
  innovation_type: InnovationType           // イノベーション種別
  prototypes: list<Prototype>               // プロトタイプ
  market_tests: list<MarketTest>            // 市場テスト
  feedback: list<ConsumerFeedback>          // 消費者フィードバック
  decision: LaunchDecision                  // 発売判断
  status: ExperimentStatus
  created_at: timestamp
  updated_at: timestamp
}
```

**ビジネスルール**:
- プロトタイプは最低2案作成
- 市場テスト前に社内評価を通過必須
- Go/No-Go判断は3ヶ月以内に決定

#### 2. LimitedEdition（限定品）

期間限定・地域限定の製品企画。

```
LimitedEdition {
  edition_id: EditionId                     // 限定品ID
  base_product: BaseProductRef              // ベース製品参照
  edition_type: EditionType                 // 限定種別
  theme: EditionTheme                       // テーマ
  availability: AvailabilityWindow          // 販売期間・地域
  production_plan: ProductionPlan           // 生産計画
  marketing_plan: MarketingPlan             // マーケティング計画
  performance: EditionPerformance           // 実績
  status: EditionStatus
}
```

**ビジネスルール**:
- 販売期間は最大6ヶ月
- 生産数量は需要予測の80-120%範囲
- 季節限定は前シーズン実績を参考

#### 3. CollaborationProject（コラボ企画）

他社・他ブランドとのコラボレーション製品企画。

```
CollaborationProject {
  project_id: ProjectId                     // 企画ID
  partners: list<CollabPartner>             // コラボパートナー
  concept: CollabConcept                    // コラボコンセプト
  product_design: CollabProductDesign       // 製品設計
  terms: CollabTerms                        // 条件・契約
  timeline: ProjectTimeline                 // タイムライン
  responsibilities: ResponsibilityMatrix    // 役割分担
  revenue_share: RevenueShareModel          // 収益配分
  status: ProjectStatus
}
```

**ビジネスルール**:
- パートナーブランド価値の相互向上が条件
- 品質基準はAsahi側を適用
- 収益配分は事前合意必須

---

### 値オブジェクト（Value Objects）

```
ProductConcept {
  name: string
  tagline: string
  unique_value_proposition: string
  inspiration_source: string
  key_features: list<string>
  differentiation_points: list<string>
}

TargetSegment {
  demographic: DemographicProfile
  psychographic: PsychographicProfile
  occasions: list<ConsumptionOccasion>
  pain_points: list<string>
  desired_benefits: list<string>
}

InnovationType {
  category: string  // FLAVOR | PACKAGING | FUNCTION | EXPERIENCE | HYBRID
  novelty_level: string  // INCREMENTAL | SUBSTANTIAL | BREAKTHROUGH
  technology_dependency: list<string>
}

Prototype {
  prototype_id: string
  version: string
  recipe_ref: string
  packaging_spec: PackagingSpec
  sensory_profile: SensoryProfile
  production_feasibility: FeasibilityAssessment
  estimated_cost: Cost
  evaluation_results: list<EvaluationResult>
}

MarketTest {
  test_id: string
  test_type: string  // BLIND_TASTE | CONCEPT_TEST | IN_STORE | ONLINE_PANEL
  sample_size: int
  geography: list<string>
  duration: DateRange
  metrics: TestMetrics
  results: TestResults
}

EditionTheme {
  name: string
  story: string
  visual_identity: VisualIdentity
  seasonal_relevance: string
  cultural_connection: string
}

AvailabilityWindow {
  start_date: date
  end_date: date
  regions: list<Region>
  channels: list<SalesChannel>
  quantity_limit: int
}

CollabPartner {
  partner_id: string
  partner_name: string
  partner_type: string  // BRAND | ARTIST | CELEBRITY | CHARACTER | EVENT
  brand_value_alignment: float
  audience_overlap: float
}
```

---

### ドメインイベント（Domain Events）

```
# 実験的製品イベント
ExperimentalProductProposed      // 企画提案
PrototypeCreated                 // プロトタイプ作成
MarketTestScheduled              // 市場テスト予定
MarketTestCompleted              // 市場テスト完了
LaunchDecisionMade               // 発売判断
ProductLaunched                  // 製品発売
ExperimentConcluded              // 実験終了

# 限定品イベント
LimitedEditionPlanned            // 限定品計画
ProductionStarted                // 生産開始
EditionLaunched                  // 限定品発売
SalesTargetAchieved              // 販売目標達成
EditionConcluded                 // 限定品終了

# コラボ企画イベント
CollaborationProposed            // コラボ提案
PartnerAgreed                    // パートナー合意
DesignApproved                   // デザイン承認
CollabProductLaunched            // コラボ製品発売
CollaborationConcluded           // コラボ終了
```

---

### VS間連携イベント（Kafka）

#### 発行イベント

```json
{
  "event_type": "product_innovation.launch_decision_made",
  "payload": {
    "product_id": "string",
    "decision": "GO | NO_GO | PIVOT",
    "product_concept": {
      "name": "string",
      "category": "string",
      "target_segment": "string"
    },
    "decided_at": "timestamp"
  }
}
```

#### 購読イベント

```json
// BC2からのレシピ承認通知
{
  "event_type": "product_recipe.recipe_approved",
  "payload": {
    "recipe_id": "string",
    "product_category": "string"
  }
}
```

---

## ドメインサービス

### ExperimentalProductService

```java
public interface ExperimentalProductService {
    ExperimentalProduct proposeProduct(ProductConcept concept, TargetSegment segment);
    Prototype createPrototype(ProductId productId, PrototypeSpec spec);
    MarketTest scheduleMarketTest(ProductId productId, MarketTestPlan plan);
    LaunchDecision evaluateAndDecide(ProductId productId);
}
```

### LimitedEditionService

```java
public interface LimitedEditionService {
    LimitedEdition planEdition(BaseProductRef baseProduct, EditionTheme theme);
    ProductionPlan createProductionPlan(EditionId editionId, DemandForecast forecast);
    void launchEdition(EditionId editionId);
    EditionPerformance trackPerformance(EditionId editionId);
}
```

### CollaborationService

```java
public interface CollaborationService {
    CollaborationProject proposeCollaboration(CollabConcept concept, List<CollabPartner> partners);
    void negotiateTerms(ProjectId projectId, CollabTerms proposedTerms);
    void approveDesign(ProjectId projectId, CollabProductDesign design);
    RevenueReport calculateRevenueShare(ProjectId projectId, Period period);
}
```

---

## 用語集

| 日本語 | 英語 | 定義 |
|--------|------|------|
| 実験的製品 | Experimental Product | 市場テスト用の試験的製品 |
| 限定品 | Limited Edition | 期間・地域・数量限定の製品 |
| コラボ企画 | Collaboration Project | 他社・他ブランドとの共同企画 |
| 市場テスト | Market Test | 消費者反応を測定する試験販売 |
| 発売判断 | Launch Decision | Go/No-Go/Pivotの意思決定 |
