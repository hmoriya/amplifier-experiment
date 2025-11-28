# BC6: Functional Research - データベース設計

## 概要

機能性研究管理のデータベース設計。乳酸菌研究、機能性成分、健康効果実証の永続化。

**データベース**: PostgreSQL 15+
**技術スタック**: Python/SQLAlchemy

---

## テーブル定義

### 乳酸菌研究テーブル

```sql
-- 乳酸菌株
CREATE TABLE lab_strains (
    strain_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    species VARCHAR(100) NOT NULL,
    subspecies VARCHAR(100),
    strain_name VARCHAR(100) NOT NULL,
    isolation_source VARCHAR(200) NOT NULL,
    isolation_date DATE,
    isolation_conditions JSONB,
    genbank_accession VARCHAR(50),
    deposited_at VARCHAR(200),
    deposit_number VARCHAR(50),
    status VARCHAR(50) DEFAULT 'ISOLATED',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT valid_status CHECK (status IN (
        'ISOLATED', 'CHARACTERIZING', 'SCREENING', 'VALIDATED', 'DEPOSITED', 'ARCHIVED'
    ))
);

CREATE INDEX idx_strain_species ON lab_strains(species);
CREATE INDEX idx_strain_status ON lab_strains(status);
CREATE UNIQUE INDEX idx_strain_genbank ON lab_strains(genbank_accession) WHERE genbank_accession IS NOT NULL;

-- 特性解析
CREATE TABLE strain_characterizations (
    characterization_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    strain_id UUID NOT NULL REFERENCES lab_strains(strain_id),
    morphology JSONB,
    growth_conditions JSONB,
    biochemical_profile JSONB,
    genomic_features JSONB,
    metabolite_profile JSONB,
    characterized_at TIMESTAMPTZ DEFAULT NOW(),
    characterized_by VARCHAR(100),
    UNIQUE(strain_id)
);

-- 機能性テスト
CREATE TABLE functional_tests (
    test_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    strain_id UUID NOT NULL REFERENCES lab_strains(strain_id),
    test_type VARCHAR(50) NOT NULL,
    methodology VARCHAR(500),
    test_conditions JSONB,
    results JSONB NOT NULL,
    statistical_analysis JSONB,
    conclusion TEXT,
    significance_level VARCHAR(20),
    tested_at TIMESTAMPTZ DEFAULT NOW(),
    tested_by VARCHAR(100)
);

CREATE INDEX idx_func_test_strain ON functional_tests(strain_id);
CREATE INDEX idx_func_test_type ON functional_tests(test_type);

-- 安全性評価
CREATE TABLE safety_assessments (
    assessment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    strain_id UUID NOT NULL REFERENCES lab_strains(strain_id),
    assessment_type VARCHAR(50) NOT NULL,
    antibiotic_resistance JSONB,
    virulence_factors JSONB,
    toxicity_tests JSONB,
    biogenic_amines JSONB,
    conclusion TEXT,
    safety_rating VARCHAR(50),
    assessed_at TIMESTAMPTZ DEFAULT NOW(),
    assessed_by VARCHAR(100),
    UNIQUE(strain_id, assessment_type)
);

CREATE INDEX idx_safety_strain ON safety_assessments(strain_id);
CREATE INDEX idx_safety_rating ON safety_assessments(safety_rating);
```

### 機能性成分テーブル

```sql
-- 機能性成分
CREATE TABLE functional_ingredients (
    ingredient_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    compound_name VARCHAR(200) NOT NULL,
    iupac_name VARCHAR(500),
    molecular_formula VARCHAR(100),
    molecular_weight DECIMAL(10,4),
    structure_smiles TEXT,
    structure_inchi TEXT,
    cas_number VARCHAR(50),
    classification VARCHAR(50),
    source_type VARCHAR(50),
    source_organism VARCHAR(200),
    extraction_method TEXT,
    status VARCHAR(50) DEFAULT 'IDENTIFIED',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT valid_ingredient_status CHECK (status IN (
        'IDENTIFIED', 'SCREENING', 'VALIDATED', 'COMMERCIAL', 'DISCONTINUED'
    ))
);

CREATE INDEX idx_ingredient_class ON functional_ingredients(classification);
CREATE INDEX idx_ingredient_status ON functional_ingredients(status);
CREATE UNIQUE INDEX idx_ingredient_cas ON functional_ingredients(cas_number) WHERE cas_number IS NOT NULL;

-- 生理活性データ
CREATE TABLE bioactivities (
    bioactivity_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ingredient_id UUID NOT NULL REFERENCES functional_ingredients(ingredient_id),
    activity_type VARCHAR(100) NOT NULL,
    target VARCHAR(200),
    potency_value DECIMAL(15,6),
    potency_unit VARCHAR(50),
    assay_method VARCHAR(500),
    evidence_level VARCHAR(50),  -- IN_VITRO, IN_VIVO, HUMAN
    raw_data_reference VARCHAR(500),
    statistical_significance BOOLEAN,
    recorded_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_bioactivity_ingredient ON bioactivities(ingredient_id);
CREATE INDEX idx_bioactivity_type ON bioactivities(activity_type);
CREATE INDEX idx_bioactivity_evidence ON bioactivities(evidence_level);

-- 作用機序
CREATE TABLE mechanisms_of_action (
    mechanism_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ingredient_id UUID NOT NULL REFERENCES functional_ingredients(ingredient_id),
    primary_mechanism TEXT NOT NULL,
    molecular_targets JSONB DEFAULT '[]',
    signaling_pathways JSONB DEFAULT '[]',
    supporting_evidence JSONB DEFAULT '[]',
    confidence_level VARCHAR(50),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(ingredient_id)
);

-- 用量反応データ
CREATE TABLE dose_responses (
    response_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ingredient_id UUID NOT NULL REFERENCES functional_ingredients(ingredient_id),
    endpoint VARCHAR(200) NOT NULL,
    doses JSONB NOT NULL,  -- array of {dose, unit, response}
    model_type VARCHAR(50),  -- LINEAR, SIGMOID, etc
    ed50 DECIMAL(15,6),
    ed50_unit VARCHAR(50),
    r_squared DECIMAL(5,4),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_dose_response_ingredient ON dose_responses(ingredient_id);
```

### 健康効果実証テーブル

```sql
-- 健康強調表示
CREATE TABLE health_claims (
    evidence_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ingredient_id UUID NOT NULL REFERENCES functional_ingredients(ingredient_id),
    claim_type VARCHAR(50) NOT NULL,
    claim_text TEXT NOT NULL,
    target_population VARCHAR(200),
    conditions JSONB DEFAULT '[]',
    disclaimers JSONB DEFAULT '[]',
    target_regulation VARCHAR(50),
    status VARCHAR(50) DEFAULT 'DRAFT',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT valid_claim_status CHECK (status IN (
        'DRAFT', 'COMPILING', 'REVIEW', 'SUBMITTED', 'APPROVED', 'REJECTED', 'WITHDRAWN'
    ))
);

CREATE INDEX idx_claim_ingredient ON health_claims(ingredient_id);
CREATE INDEX idx_claim_status ON health_claims(status);
CREATE INDEX idx_claim_regulation ON health_claims(target_regulation);

-- 臨床試験
CREATE TABLE clinical_trials (
    trial_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evidence_id UUID NOT NULL REFERENCES health_claims(evidence_id),
    registry_number VARCHAR(100),
    registry_type VARCHAR(50),  -- UMIN, NCT, ISRCTN
    design JSONB NOT NULL,
    participants JSONB NOT NULL,
    intervention JSONB NOT NULL,
    outcomes JSONB NOT NULL,
    results JSONB,
    adverse_events JSONB,
    conclusion TEXT,
    publication_status VARCHAR(50),
    publication_reference VARCHAR(500),
    trial_start_date DATE,
    trial_end_date DATE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_trial_evidence ON clinical_trials(evidence_id);
CREATE UNIQUE INDEX idx_trial_registry ON clinical_trials(registry_number) WHERE registry_number IS NOT NULL;

-- システマティックレビュー
CREATE TABLE systematic_reviews (
    review_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evidence_id UUID NOT NULL REFERENCES health_claims(evidence_id),
    protocol_registration VARCHAR(100),  -- PROSPERO
    search_strategy JSONB NOT NULL,
    inclusion_criteria JSONB,
    studies_identified INT,
    studies_screened INT,
    studies_included INT,
    meta_analysis JSONB,
    quality_assessment JSONB,
    conclusion TEXT,
    publication_reference VARCHAR(500),
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(evidence_id)
);

-- エビデンスパッケージ
CREATE TABLE evidence_packages (
    package_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evidence_id UUID NOT NULL REFERENCES health_claims(evidence_id),
    evidence_level VARCHAR(10) NOT NULL,  -- A, B, C, D
    total_studies INT NOT NULL,
    rct_count INT DEFAULT 0,
    observational_count INT DEFAULT 0,
    meta_analysis_available BOOLEAN DEFAULT FALSE,
    consistency_rating VARCHAR(50),
    overall_strength VARCHAR(50),
    gaps_identified JSONB DEFAULT '[]',
    assembled_at TIMESTAMPTZ DEFAULT NOW(),
    assembled_by VARCHAR(100),
    UNIQUE(evidence_id)
);

CREATE INDEX idx_package_level ON evidence_packages(evidence_level);

-- 規制申請
CREATE TABLE regulatory_submissions (
    submission_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evidence_id UUID NOT NULL REFERENCES health_claims(evidence_id),
    target_authority VARCHAR(50) NOT NULL,
    submission_type VARCHAR(50) NOT NULL,
    submission_date DATE NOT NULL,
    reference_number VARCHAR(100),
    documents JSONB DEFAULT '[]',
    status VARCHAR(50) DEFAULT 'SUBMITTED',
    decision_date DATE,
    decision_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_submission_evidence ON regulatory_submissions(evidence_id);
CREATE INDEX idx_submission_authority ON regulatory_submissions(target_authority);
CREATE INDEX idx_submission_status ON regulatory_submissions(status);
```

---

## ビュー定義

### 乳酸菌株サマリービュー

```sql
CREATE VIEW v_lab_strain_summary AS
SELECT
    ls.strain_id,
    ls.species,
    ls.strain_name,
    ls.status,
    sc.characterized_at IS NOT NULL as is_characterized,
    COUNT(DISTINCT ft.test_id) as functional_test_count,
    COUNT(DISTINCT ft.test_id) FILTER (WHERE ft.statistical_analysis->>'significance' = 'true') as significant_tests,
    sa.safety_rating,
    ls.created_at
FROM lab_strains ls
LEFT JOIN strain_characterizations sc ON ls.strain_id = sc.strain_id
LEFT JOIN functional_tests ft ON ls.strain_id = ft.strain_id
LEFT JOIN safety_assessments sa ON ls.strain_id = sa.strain_id AND sa.assessment_type = 'COMPREHENSIVE'
GROUP BY ls.strain_id, sc.characterized_at, sa.safety_rating;
```

### 機能性成分エビデンスビュー

```sql
CREATE VIEW v_ingredient_evidence_summary AS
SELECT
    fi.ingredient_id,
    fi.compound_name,
    fi.classification,
    fi.status,
    COUNT(DISTINCT b.bioactivity_id) as bioactivity_count,
    COUNT(DISTINCT b.bioactivity_id) FILTER (WHERE b.evidence_level = 'HUMAN') as human_evidence_count,
    moa.confidence_level as mechanism_confidence,
    hc.claim_text as approved_claim,
    ep.evidence_level
FROM functional_ingredients fi
LEFT JOIN bioactivities b ON fi.ingredient_id = b.ingredient_id
LEFT JOIN mechanisms_of_action moa ON fi.ingredient_id = moa.ingredient_id
LEFT JOIN health_claims hc ON fi.ingredient_id = hc.ingredient_id AND hc.status = 'APPROVED'
LEFT JOIN evidence_packages ep ON hc.evidence_id = ep.evidence_id
GROUP BY fi.ingredient_id, moa.confidence_level, hc.claim_text, ep.evidence_level;
```

---

## データ保持ポリシー

| テーブル | 保持期間 | 備考 |
|---------|---------|------|
| lab_strains | 永続 | 研究資産 |
| clinical_trials | 15年 | 規制要件 |
| regulatory_submissions | 永続 | 法的記録 |
| functional_tests | 10年 | - |

---

## パフォーマンス考慮

1. **JSONBインデックス**:
   - 頻繁にクエリされるJSONBフィールドにGINインデックス

2. **パーティショニング**:
   - clinical_trialsは年度別パーティション検討（規模拡大時）

3. **接続プール**:
   - SQLAlchemy pool_size=10, max_overflow=20
