# BC7: Functional Products - データベース設計

## 概要

機能性製品管理のデータベース設計。ノンアルコール製品、機能性飲料、低アルコール製品の永続化。

**データベース**: PostgreSQL 15+
**技術スタック**: Java/Spring Data JPA

---

## テーブル定義

### ノンアルコール製品テーブル

```sql
-- ノンアルコール製品
CREATE TABLE non_alcoholic_products (
    product_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    product_type JSONB NOT NULL,
    flavor_profile JSONB,
    production_method JSONB,
    health_positioning JSONB,
    target_occasions JSONB DEFAULT '[]',
    nutritional_info JSONB,
    zero_alcohol_verified BOOLEAN DEFAULT FALSE,
    verification_certificate VARCHAR(100),
    status VARCHAR(50) DEFAULT 'DEVELOPMENT',
    recipe_reference VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    launched_at TIMESTAMPTZ,
    CONSTRAINT valid_na_status CHECK (status IN (
        'DEVELOPMENT', 'TESTING', 'APPROVED', 'LAUNCHED', 'DISCONTINUED'
    ))
);

CREATE INDEX idx_na_product_status ON non_alcoholic_products(status);
CREATE INDEX idx_na_product_type ON non_alcoholic_products USING GIN((product_type->'category'));
CREATE INDEX idx_na_verified ON non_alcoholic_products(zero_alcohol_verified);

-- 0.00%検証記録
CREATE TABLE zero_alcohol_verifications (
    verification_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL REFERENCES non_alcoholic_products(product_id),
    verification_method VARCHAR(100) NOT NULL,
    test_results JSONB NOT NULL,
    certifying_body VARCHAR(200),
    certificate_number VARCHAR(100),
    verified BOOLEAN NOT NULL,
    verified_at TIMESTAMPTZ DEFAULT NOW(),
    valid_until DATE
);

CREATE INDEX idx_za_verification_product ON zero_alcohol_verifications(product_id);
```

### 機能性飲料テーブル

```sql
-- 機能性飲料
CREATE TABLE functional_beverages (
    product_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    functional_claim JSONB NOT NULL,
    active_ingredients JSONB NOT NULL DEFAULT '[]',
    evidence_reference VARCHAR(100),  -- BC6のevidence_id
    dosage_guidance JSONB,
    target_consumers JSONB,
    labeling JSONB,
    status VARCHAR(50) DEFAULT 'DRAFT',
    recipe_reference VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    launched_at TIMESTAMPTZ,
    CONSTRAINT valid_fb_status CHECK (status IN (
        'DRAFT', 'PENDING_EVIDENCE', 'PENDING_NOTIFICATION', 'APPROVED', 'LAUNCHED', 'DISCONTINUED'
    ))
);

CREATE INDEX idx_fb_status ON functional_beverages(status);
CREATE INDEX idx_fb_claim_type ON functional_beverages USING GIN((functional_claim->'claim_type'));
CREATE INDEX idx_fb_evidence ON functional_beverages(evidence_reference);

-- 規制届出
CREATE TABLE regulatory_notifications (
    notification_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL REFERENCES functional_beverages(product_id),
    notification_type VARCHAR(50) NOT NULL,
    target_authority VARCHAR(50) NOT NULL,
    submission_date DATE NOT NULL,
    届出番号 VARCHAR(50),  -- 機能性表示食品届出番号
    documents JSONB DEFAULT '[]',
    scientific_basis_summary TEXT,
    status VARCHAR(50) DEFAULT 'SUBMITTED',
    response_date DATE,
    response_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT valid_notification_status CHECK (status IN (
        'DRAFT', 'SUBMITTED', 'UNDER_REVIEW', 'ACCEPTED', 'REJECTED', 'WITHDRAWN'
    ))
);

CREATE INDEX idx_notification_product ON regulatory_notifications(product_id);
CREATE INDEX idx_notification_status ON regulatory_notifications(status);
CREATE UNIQUE INDEX idx_notification_number ON regulatory_notifications(届出番号) WHERE 届出番号 IS NOT NULL;

-- 機能性成分マッピング
CREATE TABLE product_ingredients_mapping (
    mapping_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL REFERENCES functional_beverages(product_id),
    ingredient_id VARCHAR(100) NOT NULL,  -- BC6のingredient_id
    amount_per_serving DECIMAL(10,4) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    function_description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(product_id, ingredient_id)
);

CREATE INDEX idx_ingredient_mapping_product ON product_ingredients_mapping(product_id);
```

### 低アルコール製品テーブル

```sql
-- 低アルコール製品
CREATE TABLE low_alcohol_products (
    product_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    base_style VARCHAR(50) NOT NULL,
    alcohol_content JSONB NOT NULL,
    reduction_method JSONB,
    flavor_compensation JSONB,
    positioning JSONB,
    consumption_guidance JSONB,
    compliance_status VARCHAR(50),
    tax_classification VARCHAR(50),
    status VARCHAR(50) DEFAULT 'FORMULATION',
    recipe_reference VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    launched_at TIMESTAMPTZ,
    CONSTRAINT valid_la_status CHECK (status IN (
        'FORMULATION', 'PROCESS_VALIDATION', 'SENSORY_TESTING', 'APPROVED', 'LAUNCHED', 'DISCONTINUED'
    ))
);

CREATE INDEX idx_la_status ON low_alcohol_products(status);
CREATE INDEX idx_la_base_style ON low_alcohol_products(base_style);
CREATE INDEX idx_la_alcohol_category ON low_alcohol_products USING GIN((alcohol_content->'category'));

-- 低アルコール化プロセス検証
CREATE TABLE process_validations (
    validation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL REFERENCES low_alcohol_products(product_id),
    process_parameters JSONB NOT NULL,
    quality_metrics JSONB NOT NULL,
    batch_samples JSONB NOT NULL,
    process_approved BOOLEAN,
    recommendations JSONB DEFAULT '[]',
    validated_at TIMESTAMPTZ DEFAULT NOW(),
    validated_by VARCHAR(100)
);

CREATE INDEX idx_process_validation_product ON process_validations(product_id);

-- コンプライアンスチェック
CREATE TABLE compliance_checks (
    check_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL,
    product_type VARCHAR(50) NOT NULL,  -- NA, FUNCTIONAL, LOW_ALCOHOL
    target_markets JSONB NOT NULL,
    labeling_claims JSONB,
    compliance_status VARCHAR(50) NOT NULL,
    market_requirements JSONB,
    warnings_required JSONB DEFAULT '[]',
    tax_classification VARCHAR(50),
    checked_at TIMESTAMPTZ DEFAULT NOW(),
    valid_until DATE
);

CREATE INDEX idx_compliance_product ON compliance_checks(product_id);
CREATE INDEX idx_compliance_status ON compliance_checks(compliance_status);
```

### 共通テーブル

```sql
-- 製品共通情報（ビュー用）
CREATE TABLE product_common_info (
    info_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL,
    product_type VARCHAR(50) NOT NULL,  -- NON_ALCOHOLIC, FUNCTIONAL, LOW_ALCOHOL
    sku VARCHAR(50),
    barcode VARCHAR(50),
    package_sizes JSONB DEFAULT '[]',
    distribution_channels JSONB DEFAULT '[]',
    launch_markets JSONB DEFAULT '[]',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(product_id, product_type)
);

CREATE INDEX idx_common_product ON product_common_info(product_id);
CREATE INDEX idx_common_type ON product_common_info(product_type);
CREATE UNIQUE INDEX idx_common_sku ON product_common_info(sku) WHERE sku IS NOT NULL;

-- 官能評価記録
CREATE TABLE sensory_evaluations (
    evaluation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL,
    product_type VARCHAR(50) NOT NULL,
    evaluation_date DATE NOT NULL,
    panel_size INT,
    evaluation_type VARCHAR(50),  -- INTERNAL | CONSUMER | EXPERT
    scores JSONB NOT NULL,
    comparison_products JSONB DEFAULT '[]',
    comments TEXT,
    recommendation VARCHAR(50),
    evaluated_by VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_sensory_product ON sensory_evaluations(product_id);
CREATE INDEX idx_sensory_date ON sensory_evaluations(evaluation_date);
```

---

## ビュー定義

### 全機能性製品統合ビュー

```sql
CREATE VIEW v_all_functional_products AS
SELECT
    'NON_ALCOHOLIC' as product_type,
    product_id,
    name,
    status,
    zero_alcohol_verified as verified,
    created_at,
    launched_at
FROM non_alcoholic_products
UNION ALL
SELECT
    'FUNCTIONAL' as product_type,
    product_id,
    name,
    status,
    CASE WHEN evidence_reference IS NOT NULL THEN TRUE ELSE FALSE END as verified,
    created_at,
    launched_at
FROM functional_beverages
UNION ALL
SELECT
    'LOW_ALCOHOL' as product_type,
    product_id,
    name,
    status,
    CASE WHEN compliance_status = 'COMPLIANT' THEN TRUE ELSE FALSE END as verified,
    created_at,
    launched_at
FROM low_alcohol_products;
```

### 機能性飲料届出状況ビュー

```sql
CREATE VIEW v_functional_beverage_regulatory AS
SELECT
    fb.product_id,
    fb.name,
    fb.functional_claim->>'claim_type' as claim_type,
    fb.functional_claim->>'claim_text' as claim_text,
    fb.status as product_status,
    rn.届出番号,
    rn.status as notification_status,
    rn.submission_date,
    rn.response_date,
    fb.launched_at
FROM functional_beverages fb
LEFT JOIN regulatory_notifications rn ON fb.product_id = rn.product_id
    AND rn.status IN ('SUBMITTED', 'ACCEPTED');
```

---

## データ移行・連携

### BC6との連携

```sql
-- エビデンス参照の検証（アプリケーション層で実装）
-- evidence_referenceはBC6のevidence_idを参照

-- 成分マッピングの同期トリガー（オプション）
CREATE OR REPLACE FUNCTION notify_ingredient_linked()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM pg_notify('ingredient_linked',
        json_build_object(
            'product_id', NEW.product_id,
            'ingredient_id', NEW.ingredient_id
        )::text
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_ingredient_linked
AFTER INSERT ON product_ingredients_mapping
FOR EACH ROW EXECUTE FUNCTION notify_ingredient_linked();
```

---

## データ保持ポリシー

| テーブル | 保持期間 | 備考 |
|---------|---------|------|
| *_products | 永続 | マスタデータ |
| regulatory_notifications | 永続 | 法的記録 |
| compliance_checks | 5年 | 最新のみアクティブ |
| sensory_evaluations | 10年 | 品質記録 |

---

## パフォーマンス考慮

1. **JSONB使用理由**:
   - 製品属性は種類により構造が異なる
   - 柔軟な検索のためGINインデックス使用

2. **分離設計**:
   - 3種類の製品を別テーブルで管理（将来の拡張性）
   - 共通情報は別テーブルで統合管理

3. **接続プール設定**:
   - HikariCP: maximumPoolSize=15
   - 読み取り多めのワークロード想定
