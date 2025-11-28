# BC5: Product Innovation - API仕様書

## 概要

製品イノベーション管理のREST API仕様。実験的製品、限定品、コラボ企画の管理を提供。

**ベースURL**: `/api/v1/product-innovation`
**認証**: OAuth 2.0 Bearer Token
**技術スタック**: Java/Spring Boot

---

## エンドポイント一覧

### 実験的製品 (Experimental Products)

#### POST /experimental-products
実験的製品の企画提案

```yaml
Request:
  Content-Type: application/json
  Body:
    concept:
      name: string (required)
      tagline: string
      unique_value_proposition: string (required)
      key_features: array<string>
    target_segment:
      demographic:
        age_range: string
        gender: string
        income_level: string
      occasions: array<string>
      desired_benefits: array<string>
    innovation_type:
      category: string  # FLAVOR | PACKAGING | FUNCTION | EXPERIENCE
      novelty_level: string  # INCREMENTAL | SUBSTANTIAL | BREAKTHROUGH

Response: 201 Created
  Body:
    product_id: string
    status: "PROPOSED"
    created_at: timestamp
```

#### GET /experimental-products
実験的製品一覧取得

```yaml
Query Parameters:
  status: string (optional)
  innovation_type: string (optional)
  created_after: date (optional)
  page: integer (default: 1)
  limit: integer (default: 20)

Response: 200 OK
  Body:
    items: array<ExperimentalProduct>
    total: integer
```

#### GET /experimental-products/{product_id}
実験的製品詳細取得

#### POST /experimental-products/{product_id}/prototypes
プロトタイプ作成

```yaml
Request:
  Body:
    version: string
    recipe_reference: string
    packaging_spec:
      format: string
      size_ml: integer
      material: string
    sensory_targets:
      sweetness: integer (1-10)
      bitterness: integer (1-10)
      body: integer (1-10)
    estimated_cost:
      amount: number
      currency: string

Response: 201 Created
  Body:
    prototype_id: string
    created_at: timestamp
```

#### POST /experimental-products/{product_id}/market-tests
市場テストのスケジュール

```yaml
Request:
  Body:
    test_type: string  # BLIND_TASTE | CONCEPT_TEST | IN_STORE | ONLINE_PANEL
    sample_size: integer (required)
    geography: array<string>
    start_date: date
    end_date: date
    success_criteria:
      min_purchase_intent: number
      min_uniqueness_score: number

Response: 201 Created
  Body:
    test_id: string
    status: "SCHEDULED"
```

#### POST /experimental-products/{product_id}/market-tests/{test_id}/results
市場テスト結果登録

```yaml
Request:
  Body:
    metrics:
      purchase_intent: number
      uniqueness_score: number
      price_sensitivity: number
      repeat_intent: number
    qualitative_feedback: array<string>
    recommendations: array<string>

Response: 200 OK
```

#### POST /experimental-products/{product_id}/decision
発売判断登録

```yaml
Request:
  Body:
    decision: string  # GO | NO_GO | PIVOT
    rationale: string
    conditions: array<string>  # GO条件
    next_steps: array<string>

Response: 200 OK
  Body:
    decision_id: string
    decided_at: timestamp
```

---

### 限定品 (Limited Editions)

#### POST /limited-editions
限定品企画

```yaml
Request:
  Body:
    base_product_id: string (required)
    edition_type: string  # SEASONAL | REGIONAL | QUANTITY | ANNIVERSARY
    theme:
      name: string (required)
      story: string
      seasonal_relevance: string
    availability:
      start_date: date (required)
      end_date: date (required)
      regions: array<string>
      quantity_limit: integer

Response: 201 Created
  Body:
    edition_id: string
    status: "PLANNED"
```

#### GET /limited-editions
限定品一覧取得

```yaml
Query Parameters:
  status: string
  edition_type: string
  active_on: date  # 指定日時点で販売中のもの
  page: integer
  limit: integer

Response: 200 OK
```

#### GET /limited-editions/{edition_id}
限定品詳細取得

#### PUT /limited-editions/{edition_id}/production-plan
生産計画設定

```yaml
Request:
  Body:
    total_quantity: integer (required)
    production_batches:
      - batch_number: integer
        quantity: integer
        production_date: date
        factory: string
    distribution_plan:
      - region: string
        allocation_percentage: number

Response: 200 OK
```

#### POST /limited-editions/{edition_id}/launch
限定品発売開始

```yaml
Response: 200 OK
  Body:
    edition_id: string
    launched_at: timestamp
    status: "ACTIVE"
```

#### GET /limited-editions/{edition_id}/performance
販売実績取得

```yaml
Response: 200 OK
  Body:
    edition_id: string
    sales_summary:
      total_sold: integer
      revenue: number
      sell_through_rate: number
    regional_breakdown: array
    daily_sales: array
    comparison_to_forecast:
      variance_percentage: number
      status: string  # ABOVE | ON_TRACK | BELOW
```

---

### コラボ企画 (Collaboration Projects)

#### POST /collaborations
コラボ企画提案

```yaml
Request:
  Body:
    concept:
      name: string (required)
      description: string
      target_audience: string
      expected_impact: string
    partners:
      - partner_name: string
        partner_type: string  # BRAND | ARTIST | CELEBRITY | CHARACTER
        brand_value_alignment: number (0-1)
    preliminary_terms:
      duration_months: integer
      revenue_share_model: string

Response: 201 Created
  Body:
    project_id: string
    status: "PROPOSED"
```

#### GET /collaborations
コラボ企画一覧取得

#### GET /collaborations/{project_id}
コラボ企画詳細取得

#### PATCH /collaborations/{project_id}/terms
条件交渉・更新

```yaml
Request:
  Body:
    revenue_share:
      asahi_percentage: number
      partner_percentage: number
    responsibilities:
      product_development: string  # ASAHI | PARTNER | JOINT
      marketing: string
      distribution: string
    approval_required: boolean

Response: 200 OK
```

#### POST /collaborations/{project_id}/design
製品デザイン提出

```yaml
Request:
  Content-Type: multipart/form-data
  Body:
    design_name: string
    design_files: array<file>
    packaging_mockup: file
    description: string

Response: 201 Created
  Body:
    design_id: string
    status: "PENDING_APPROVAL"
```

#### POST /collaborations/{project_id}/design/{design_id}/approve
デザイン承認

```yaml
Request:
  Body:
    approved: boolean
    feedback: string
    modifications_required: array<string>

Response: 200 OK
```

#### POST /collaborations/{project_id}/launch
コラボ製品発売

```yaml
Response: 200 OK
  Body:
    launched_at: timestamp
    status: "ACTIVE"
```

---

## 共通スキーマ

### ExperimentalProduct

```yaml
ExperimentalProduct:
  type: object
  properties:
    product_id:
      type: string
    concept:
      $ref: '#/components/schemas/ProductConcept'
    target_segment:
      $ref: '#/components/schemas/TargetSegment'
    innovation_type:
      $ref: '#/components/schemas/InnovationType'
    prototypes:
      type: array
      items:
        $ref: '#/components/schemas/Prototype'
    market_tests:
      type: array
      items:
        $ref: '#/components/schemas/MarketTest'
    status:
      type: string
      enum: [PROPOSED, PROTOTYPING, TESTING, DECIDING, APPROVED, REJECTED, PIVOTING]
    decision:
      $ref: '#/components/schemas/LaunchDecision'
```

### LimitedEdition

```yaml
LimitedEdition:
  type: object
  properties:
    edition_id:
      type: string
    base_product_id:
      type: string
    edition_type:
      type: string
      enum: [SEASONAL, REGIONAL, QUANTITY, ANNIVERSARY, COLLABORATION]
    theme:
      $ref: '#/components/schemas/EditionTheme'
    availability:
      $ref: '#/components/schemas/AvailabilityWindow'
    status:
      type: string
      enum: [PLANNED, IN_PRODUCTION, ACTIVE, SOLD_OUT, CONCLUDED]
    performance:
      $ref: '#/components/schemas/EditionPerformance'
```

### CollaborationProject

```yaml
CollaborationProject:
  type: object
  properties:
    project_id:
      type: string
    partners:
      type: array
      items:
        $ref: '#/components/schemas/CollabPartner'
    concept:
      $ref: '#/components/schemas/CollabConcept'
    terms:
      $ref: '#/components/schemas/CollabTerms'
    status:
      type: string
      enum: [PROPOSED, NEGOTIATING, AGREED, IN_DEVELOPMENT, ACTIVE, CONCLUDED]
    revenue_to_date:
      type: number
```

---

## エラーレスポンス

```yaml
Error:
  type: object
  properties:
    error_code:
      type: string
    message:
      type: string
    details:
      type: object

# エラーコード例
PI001: "Experimental product not found"
PI002: "Cannot create prototype - product not in PROPOSED status"
PI003: "Market test already scheduled"
PI004: "Base product not found for limited edition"
PI005: "Partner agreement required before design submission"
PI006: "Revenue share percentages must equal 100%"
```

---

## レート制限

| エンドポイント | 制限 |
|---------------|------|
| 全エンドポイント | 500回/分 |
| ファイルアップロード | 50回/時間 |
