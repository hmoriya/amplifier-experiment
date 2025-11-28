# BC7: Functional Products - API仕様書

## 概要

機能性製品管理のREST API仕様。ノンアルコール製品、機能性飲料、低アルコール製品の管理を提供。

**ベースURL**: `/api/v1/functional-products`
**認証**: OAuth 2.0 Bearer Token
**技術スタック**: Java/Spring Boot

---

## エンドポイント一覧

### ノンアルコール製品 (Non-Alcoholic Products)

#### POST /non-alcoholic
ノンアルコール製品の登録

```yaml
Request:
  Content-Type: application/json
  Body:
    product_type:
      category: string  # BEER_TASTE | WINE_TASTE | COCKTAIL_TASTE
      subcategory: string
    name: string (required)
    flavor_profile:
      primary_notes: array<string>
      bitterness_ibu: integer
      body: string  # LIGHT | MEDIUM | FULL
      carbonation: string
    production_method:
      method_type: string  # DEALCOHOLIZATION | ARRESTED_FERMENTATION | NON_FERMENTED
      process_details: string
    health_positioning:
      calorie_claim: string
      sugar_claim: string
    target_occasions: array<string>

Response: 201 Created
  Body:
    product_id: string
    status: "DEVELOPMENT"
    created_at: timestamp
```

#### GET /non-alcoholic
ノンアルコール製品一覧取得

```yaml
Query Parameters:
  category: string (optional)
  status: string (optional)
  calorie_claim: string (optional)
  page: integer (default: 1)
  limit: integer (default: 20)

Response: 200 OK
  Body:
    items: array<NonAlcoholicProduct>
    total: integer
```

#### GET /non-alcoholic/{product_id}
ノンアルコール製品詳細取得

#### POST /non-alcoholic/{product_id}/verify-zero-alcohol
0.00%アルコール検証

```yaml
Request:
  Body:
    verification_method: string
    test_results:
      - batch_id: string
        alcohol_reading: number  # must be 0.00
        test_date: date
        lab_reference: string
    certifying_body: string

Response: 200 OK
  Body:
    verification_id: string
    verified: boolean
    certificate_number: string
```

#### PUT /non-alcoholic/{product_id}/nutritional-info
栄養成分情報の更新

```yaml
Request:
  Body:
    serving_size_ml: integer (required)
    energy_kcal: number
    protein_g: number
    fat_g: number
    carbohydrate_g: number
    sugar_g: number
    sodium_mg: number
    additional_nutrients:
      - name: string
        amount: number
        unit: string

Response: 200 OK
```

---

### 機能性飲料 (Functional Beverages)

#### POST /functional
機能性飲料の登録

```yaml
Request:
  Body:
    name: string (required)
    functional_claim:
      claim_type: string  # FOSHU | FNFC | FOODS_WITH_NUTRIENT
      claim_text: string (required)
    active_ingredients:
      - ingredient_name: string
        amount_per_serving: number
        unit: string
        function: string
    target_consumers:
      age_group: string
      health_concerns: array<string>
    dosage_guidance:
      recommended_serving: string
      frequency: string
      timing: string

Response: 201 Created
  Body:
    product_id: string
    status: "DRAFT"
```

#### GET /functional
機能性飲料一覧取得

```yaml
Query Parameters:
  claim_type: string
  status: string
  ingredient: string
  page: integer
  limit: integer

Response: 200 OK
```

#### GET /functional/{product_id}
機能性飲料詳細取得

#### POST /functional/{product_id}/link-evidence
エビデンスパッケージとの紐付け

```yaml
Request:
  Body:
    evidence_id: string (required)  # BC6のevidence_id
    evidence_summary: string
    key_studies: array<string>

Response: 200 OK
  Body:
    linked_at: timestamp
    evidence_level: string
```

#### POST /functional/{product_id}/regulatory-notification
規制当局への届出

```yaml
Request:
  Body:
    notification_type: string  # FNFC_NEW | FNFC_CHANGE | FOSHU_APPLICATION
    target_authority: string  # CAA (消費者庁)
    documents:
      - document_type: string
        file_reference: string
    scientific_basis_summary: string
    planned_launch_date: date

Response: 201 Created
  Body:
    notification_id: string
    submission_date: date
    expected_response_date: date
    status: "SUBMITTED"
```

#### PATCH /functional/{product_id}/regulatory-status
規制ステータスの更新

```yaml
Request:
  Body:
    notification_number: string  # 届出番号
    status: string  # ACCEPTED | REJECTED | PENDING_REVISION
    official_response_date: date
    notes: string

Response: 200 OK
```

#### PUT /functional/{product_id}/labeling
表示内容の設定

```yaml
Request:
  Body:
    front_label:
      product_name: string
      functional_claim_display: string
      届出番号: string
    back_label:
      ingredients_list: string
      nutritional_facts: object
      allergen_info: array<string>
      warnings: array<string>
      dosage_instructions: string
      storage_instructions: string
    package_insert: string

Response: 200 OK
```

---

### 低アルコール製品 (Low Alcohol Products)

#### POST /low-alcohol
低アルコール製品の登録

```yaml
Request:
  Body:
    name: string (required)
    base_style: string  # LAGER | ALE | WHEAT | etc
    alcohol_content:
      percentage: number (required)  # 0.5 - 3.5
      category: string  # MICRO | LOW | REDUCED
    reduction_method:
      technique: string  # VACUUM_DISTILLATION | MEMBRANE | DILUTION
      flavor_impact: string
    positioning:
      target_occasion: string
      competitor_reference: string
      price_positioning: string

Response: 201 Created
  Body:
    product_id: string
    status: "FORMULATION"
```

#### GET /low-alcohol
低アルコール製品一覧取得

```yaml
Query Parameters:
  alcohol_category: string
  base_style: string
  status: string
  page: integer
  limit: integer

Response: 200 OK
```

#### GET /low-alcohol/{product_id}
低アルコール製品詳細取得

#### POST /low-alcohol/{product_id}/validate-process
低アルコール化プロセスの検証

```yaml
Request:
  Body:
    process_parameters:
      temperature: number
      pressure: number
      duration_minutes: integer
    quality_metrics:
      alcohol_removal_efficiency: number
      flavor_retention_score: number
      color_stability: boolean
    batch_samples:
      - batch_id: string
        measured_abv: number

Response: 200 OK
  Body:
    validation_id: string
    process_approved: boolean
    recommendations: array<string>
```

#### PUT /low-alcohol/{product_id}/flavor-compensation
風味補完の設定

```yaml
Request:
  Body:
    compensation_type: string  # HOP_ADDITION | MALT_ADJUSTMENT | ADJUNCT
    adjustments:
      - component: string
        action: string  # INCREASE | DECREASE | ADD
        amount: string
    target_profile:
      bitterness_ibu: integer
      body: string
      aroma_notes: array<string>
    sensory_evaluation:
      panel_score: number
      comparison_to_full_strength: number

Response: 200 OK
```

#### POST /low-alcohol/{product_id}/compliance-check
法規制コンプライアンスチェック

```yaml
Request:
  Body:
    target_markets: array<string>  # JP, US, EU, etc
    labeling_claims: array<string>

Response: 200 OK
  Body:
    compliance_status: string  # COMPLIANT | NON_COMPLIANT | REQUIRES_REVIEW
    market_specific_requirements:
      - market: string
        requirements: array<string>
        status: string
    warnings_required: array<string>
    tax_classification: string
```

---

## 共通スキーマ

### NonAlcoholicProduct

```yaml
NonAlcoholicProduct:
  type: object
  properties:
    product_id:
      type: string
    name:
      type: string
    product_type:
      $ref: '#/components/schemas/NAProductType'
    flavor_profile:
      $ref: '#/components/schemas/FlavorProfile'
    production_method:
      $ref: '#/components/schemas/ProductionMethod'
    health_positioning:
      $ref: '#/components/schemas/HealthPositioning'
    nutritional_info:
      $ref: '#/components/schemas/NutritionalInfo'
    zero_alcohol_verified:
      type: boolean
    status:
      type: string
      enum: [DEVELOPMENT, TESTING, APPROVED, LAUNCHED, DISCONTINUED]
```

### FunctionalBeverage

```yaml
FunctionalBeverage:
  type: object
  properties:
    product_id:
      type: string
    name:
      type: string
    functional_claim:
      $ref: '#/components/schemas/FunctionalClaim'
    active_ingredients:
      type: array
      items:
        $ref: '#/components/schemas/ActiveIngredient'
    evidence_reference:
      type: string
    dosage_guidance:
      $ref: '#/components/schemas/DosageGuidance'
    regulatory_status:
      type: object
      properties:
        notification_number:
          type: string
        status:
          type: string
          enum: [DRAFT, SUBMITTED, ACCEPTED, REJECTED, WITHDRAWN]
        accepted_date:
          type: string
          format: date
    status:
      type: string
      enum: [DRAFT, PENDING_EVIDENCE, PENDING_NOTIFICATION, APPROVED, LAUNCHED]
```

### LowAlcoholProduct

```yaml
LowAlcoholProduct:
  type: object
  properties:
    product_id:
      type: string
    name:
      type: string
    base_style:
      type: string
    alcohol_content:
      $ref: '#/components/schemas/AlcoholContent'
    reduction_method:
      $ref: '#/components/schemas/ReductionMethod'
    flavor_compensation:
      $ref: '#/components/schemas/FlavorCompensation'
    compliance_status:
      type: string
    status:
      type: string
      enum: [FORMULATION, PROCESS_VALIDATION, SENSORY_TESTING, APPROVED, LAUNCHED]
```

---

## エラーレスポンス

```yaml
# エラーコード例
FP001: "Product not found"
FP002: "Zero alcohol verification failed"
FP003: "Evidence package not linked"
FP004: "Regulatory notification required before launch"
FP005: "Alcohol content out of range for category"
FP006: "Compliance check failed for target market"
FP007: "Invalid functional claim format"
```

---

## レート制限

| エンドポイント | 制限 |
|---------------|------|
| 全エンドポイント | 500回/分 |
| 規制申請関連 | 20回/時間 |
