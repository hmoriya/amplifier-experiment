# BC6: Functional Research - API仕様書

## 概要

機能性研究管理のREST API仕様。乳酸菌研究、機能性成分、健康効果実証の管理を提供。

**ベースURL**: `/api/v1/functional-research`
**認証**: OAuth 2.0 Bearer Token
**技術スタック**: Python/FastAPI

---

## エンドポイント一覧

### 乳酸菌研究 (LAB Research)

#### POST /lab-strains
乳酸菌株の登録

```yaml
Request:
  Content-Type: application/json
  Body:
    species: string (required)
    subspecies: string
    strain_name: string (required)
    isolation_source: string (required)
    isolation_date: date
    isolation_conditions:
      temperature: number
      ph: number
      medium: string
    preliminary_characteristics:
      gram_stain: string
      morphology: string

Response: 201 Created
  Body:
    strain_id: string
    status: "ISOLATED"
    created_at: timestamp
```

#### GET /lab-strains
乳酸菌株一覧取得

```yaml
Query Parameters:
  species: string (optional)
  status: string (optional)
  has_functional_activity: boolean (optional)
  page: integer (default: 1)
  limit: integer (default: 20)

Response: 200 OK
  Body:
    items: array<LABStrain>
    total: integer
```

#### GET /lab-strains/{strain_id}
乳酸菌株詳細取得

#### POST /lab-strains/{strain_id}/characterization
特性解析結果の登録

```yaml
Request:
  Body:
    morphology:
      cell_shape: string
      cell_size: string
      arrangement: string
    growth_conditions:
      optimal_temperature: number
      optimal_ph: number
      oxygen_requirement: string
    biochemical_profile:
      sugar_fermentation: object
      enzyme_activities: object
    genomic_features:
      genome_size_mb: number
      gc_content: number
      genbank_accession: string

Response: 200 OK
```

#### POST /lab-strains/{strain_id}/functional-tests
機能性テスト結果の登録

```yaml
Request:
  Body:
    test_type: string  # IMMUNOMODULATION | GUT_HEALTH | METABOLIC | etc
    methodology: string
    test_conditions: object
    results:
      primary_outcome: object
      secondary_outcomes: array
    statistical_analysis:
      p_value: number
      confidence_interval: string
      significance: boolean
    conclusion: string

Response: 201 Created
  Body:
    test_id: string
```

#### POST /lab-strains/{strain_id}/safety-assessment
安全性評価結果の登録

```yaml
Request:
  Body:
    assessment_type: string  # GENOMIC | PHENOTYPIC | IN_VIVO
    antibiotic_resistance:
      tested_antibiotics: array<string>
      results: object
      transferable_genes: array<string>
    virulence_factors:
      genes_screened: array<string>
      genes_detected: array<string>
    toxicity_tests:
      acute_toxicity: object
      genotoxicity: object
    conclusion: string
    safety_rating: string  # SAFE | CONDITIONAL | REQUIRES_FURTHER

Response: 200 OK
```

---

### 機能性成分 (Functional Ingredients)

#### POST /ingredients
機能性成分の登録

```yaml
Request:
  Body:
    compound_name: string (required)
    iupac_name: string
    molecular_formula: string
    molecular_weight: number
    structure_smiles: string
    cas_number: string
    classification: string
    source:
      source_type: string  # PLANT | MICROBIAL | ANIMAL | SYNTHETIC
      source_organism: string
      extraction_method: string

Response: 201 Created
  Body:
    ingredient_id: string
```

#### GET /ingredients
機能性成分一覧取得

```yaml
Query Parameters:
  classification: string
  bioactivity_type: string
  evidence_level: string
  page: integer
  limit: integer

Response: 200 OK
```

#### GET /ingredients/{ingredient_id}
機能性成分詳細取得

#### POST /ingredients/{ingredient_id}/bioactivity
生理活性データの登録

```yaml
Request:
  Body:
    activity_type: string (required)
    target: string
    potency:
      value: number
      unit: string  # IC50, EC50, etc
    assay_method: string
    evidence_level: string  # IN_VITRO | IN_VIVO | HUMAN
    supporting_data:
      raw_data_reference: string
      statistical_significance: boolean

Response: 201 Created
```

#### POST /ingredients/{ingredient_id}/mechanism
作用機序の登録

```yaml
Request:
  Body:
    primary_mechanism: string (required)
    molecular_targets: array<string>
    signaling_pathways: array<string>
    supporting_evidence:
      - study_type: string
        reference: string
        key_findings: string
    confidence_level: string  # HIGH | MEDIUM | LOW | HYPOTHETICAL

Response: 200 OK
```

---

### 健康効果実証 (Health Claim Evidence)

#### POST /health-claims
健康強調表示エビデンスの作成

```yaml
Request:
  Body:
    ingredient_id: string (required)
    claim:
      claim_type: string  # STRUCTURE_FUNCTION | DISEASE_RISK | HEALTH_MAINTENANCE
      claim_text: string (required)
      target_population: string
      conditions: array<string>
    target_regulation: string  # FOSHU | FNFC | FDA_STRUCTURE_FUNCTION

Response: 201 Created
  Body:
    evidence_id: string
    status: "DRAFT"
```

#### GET /health-claims
健康強調表示一覧取得

#### GET /health-claims/{evidence_id}
健康強調表示詳細取得

#### POST /health-claims/{evidence_id}/clinical-trials
臨床試験の登録

```yaml
Request:
  Body:
    registry_number: string  # UMIN, ClinicalTrials.gov
    design:
      type: string  # RCT | CROSSOVER | PARALLEL | SINGLE_ARM
      blinding: string  # DOUBLE | SINGLE | OPEN
      control: string
    participants:
      target_n: integer
      enrolled_n: integer
      completed_n: integer
      inclusion_criteria: array<string>
      exclusion_criteria: array<string>
    intervention:
      test_product: string
      dosage: string
      duration_weeks: integer
      comparator: string
    outcomes:
      primary:
        measure: string
        timepoint: string
      secondary: array

Response: 201 Created
  Body:
    trial_id: string
```

#### PATCH /health-claims/{evidence_id}/clinical-trials/{trial_id}/results
臨床試験結果の登録

```yaml
Request:
  Body:
    primary_outcome:
      baseline_mean: number
      final_mean: number
      change: number
      p_value: number
    secondary_outcomes: array
    adverse_events:
      total: integer
      serious: integer
      related: integer
    conclusion: string
    publication:
      status: string  # SUBMITTED | PUBLISHED | IN_PREPARATION
      reference: string

Response: 200 OK
```

#### POST /health-claims/{evidence_id}/systematic-review
システマティックレビューの登録

```yaml
Request:
  Body:
    protocol_registration: string  # PROSPERO
    search_strategy:
      databases: array<string>
      search_terms: string
      date_range: object
    inclusion_criteria: array<string>
    studies_identified: integer
    studies_included: integer
    meta_analysis:
      performed: boolean
      pooled_effect: number
      confidence_interval: string
      heterogeneity_i2: number
    quality_assessment:
      tool_used: string  # GRADE, Cochrane RoB
      overall_quality: string
    conclusion: string

Response: 200 OK
```

#### POST /health-claims/{evidence_id}/evidence-package
エビデンスパッケージの作成

```yaml
Request:
  Body:
    assemble_from:
      clinical_trials: array<string>
      systematic_review_id: string
      observational_studies: array<string>

Response: 200 OK
  Body:
    evidence_level: string  # A | B | C | D
    total_studies: integer
    rct_count: integer
    consistency_rating: string
    overall_strength: string
    gaps_identified: array<string>
```

#### POST /health-claims/{evidence_id}/submit
規制当局への申請

```yaml
Request:
  Body:
    target_authority: string  # CAA | FDA | EFSA
    submission_type: string  # NEW | AMENDMENT | RENEWAL
    submission_date: date
    documents: array<string>  # Document IDs

Response: 200 OK
  Body:
    submission_id: string
    status: "SUBMITTED"
```

---

## 共通スキーマ

### LABStrain

```yaml
LABStrain:
  type: object
  properties:
    strain_id:
      type: string
    species:
      type: string
    strain_name:
      type: string
    status:
      type: string
      enum: [ISOLATED, CHARACTERIZING, SCREENING, VALIDATED, DEPOSITED, ARCHIVED]
    characterization:
      $ref: '#/components/schemas/StrainCharacterization'
    functional_activities:
      type: array
      items:
        $ref: '#/components/schemas/FunctionalTest'
    safety_status:
      type: string
      enum: [NOT_ASSESSED, IN_PROGRESS, SAFE, CONDITIONAL, FAILED]
```

### FunctionalIngredient

```yaml
FunctionalIngredient:
  type: object
  properties:
    ingredient_id:
      type: string
    compound_info:
      $ref: '#/components/schemas/CompoundInformation'
    bioactivities:
      type: array
      items:
        $ref: '#/components/schemas/Bioactivity'
    mechanism:
      $ref: '#/components/schemas/MechanismOfAction'
    status:
      type: string
      enum: [IDENTIFIED, SCREENING, VALIDATED, COMMERCIAL]
```

### HealthClaimEvidence

```yaml
HealthClaimEvidence:
  type: object
  properties:
    evidence_id:
      type: string
    claim:
      $ref: '#/components/schemas/HealthClaim'
    ingredient_id:
      type: string
    evidence_package:
      $ref: '#/components/schemas/EvidencePackage'
    clinical_trials:
      type: array
      items:
        $ref: '#/components/schemas/ClinicalTrial'
    status:
      type: string
      enum: [DRAFT, COMPILING, SUBMITTED, APPROVED, REJECTED]
    regulatory_submissions:
      type: array
```

---

## エラーレスポンス

```yaml
# エラーコード例
FR001: "Strain not found"
FR002: "Characterization required before functional testing"
FR003: "Safety assessment must pass before application"
FR004: "Ingredient not found"
FR005: "Insufficient evidence for claim level"
FR006: "Clinical trial registry number required"
FR007: "Systematic review protocol must be registered"
```

---

## レート制限

| エンドポイント | 制限 |
|---------------|------|
| 全エンドポイント | 500回/分 |
| 大規模データ取得 | 50回/分 |
