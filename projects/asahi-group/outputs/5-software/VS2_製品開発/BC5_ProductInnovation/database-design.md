# BC5: Product Innovation - データベース設計

## 概要

製品イノベーション管理のデータベース設計。実験的製品、限定品、コラボ企画の永続化。

**データベース**: PostgreSQL 15+
**技術スタック**: Java/Spring Data JPA

---

## ERダイアグラム概要

```
┌─────────────────────┐     ┌─────────────────────┐
│ experimental_       │     │ limited_editions    │
│ products            │     │                     │
├─────────────────────┤     ├─────────────────────┤
│ product_id (PK)     │     │ edition_id (PK)     │
│ concept             │     │ base_product_id     │
│ target_segment      │     │ theme               │
│ innovation_type     │     │ availability        │
│ status              │     │ status              │
└────────┬────────────┘     └─────────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────────┐     ┌─────────────────────┐
│ prototypes          │     │ collaboration_      │
├─────────────────────┤     │ projects            │
│ prototype_id (PK)   │     ├─────────────────────┤
│ product_id (FK)     │     │ project_id (PK)     │
│ version             │     │ concept             │
│ recipe_ref          │     │ terms               │
└─────────────────────┘     │ status              │
                            └─────────────────────┘
```

---

## テーブル定義

### 実験的製品テーブル

```sql
-- 実験的製品
CREATE TABLE experimental_products (
    product_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    concept JSONB NOT NULL,
    target_segment JSONB NOT NULL,
    innovation_type JSONB NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'PROPOSED',
    decision JSONB,
    created_by VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT valid_status CHECK (status IN (
        'PROPOSED', 'PROTOTYPING', 'TESTING', 'DECIDING',
        'APPROVED', 'REJECTED', 'PIVOTING', 'LAUNCHED'
    ))
);

CREATE INDEX idx_exp_product_status ON experimental_products(status);
CREATE INDEX idx_exp_product_innovation ON experimental_products USING GIN((innovation_type->'category'));
CREATE INDEX idx_exp_product_created ON experimental_products(created_at);

-- プロトタイプ
CREATE TABLE prototypes (
    prototype_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL REFERENCES experimental_products(product_id),
    version VARCHAR(20) NOT NULL,
    recipe_reference VARCHAR(100),
    packaging_spec JSONB,
    sensory_profile JSONB,
    production_feasibility JSONB,
    estimated_cost JSONB,
    evaluation_results JSONB DEFAULT '[]',
    status VARCHAR(50) DEFAULT 'DRAFT',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(product_id, version)
);

CREATE INDEX idx_prototype_product ON prototypes(product_id);

-- 市場テスト
CREATE TABLE market_tests (
    test_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL REFERENCES experimental_products(product_id),
    test_type VARCHAR(50) NOT NULL,
    sample_size INT NOT NULL,
    geography JSONB DEFAULT '[]',
    start_date DATE,
    end_date DATE,
    success_criteria JSONB,
    metrics JSONB,
    results JSONB,
    status VARCHAR(50) DEFAULT 'SCHEDULED',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE INDEX idx_market_test_product ON market_tests(product_id);
CREATE INDEX idx_market_test_status ON market_tests(status);
CREATE INDEX idx_market_test_dates ON market_tests(start_date, end_date);

-- 消費者フィードバック
CREATE TABLE consumer_feedback (
    feedback_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    test_id UUID NOT NULL REFERENCES market_tests(test_id),
    respondent_id VARCHAR(100),
    demographic JSONB,
    responses JSONB NOT NULL,
    sentiment_score DECIMAL(3,2),
    key_quotes JSONB DEFAULT '[]',
    submitted_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_feedback_test ON consumer_feedback(test_id);
```

### 限定品テーブル

```sql
-- 限定品
CREATE TABLE limited_editions (
    edition_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    base_product_id VARCHAR(100) NOT NULL,
    edition_type VARCHAR(50) NOT NULL,
    theme JSONB NOT NULL,
    availability JSONB NOT NULL,
    production_plan JSONB,
    marketing_plan JSONB,
    status VARCHAR(50) DEFAULT 'PLANNED',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    launched_at TIMESTAMPTZ,
    concluded_at TIMESTAMPTZ,
    CONSTRAINT valid_edition_type CHECK (edition_type IN (
        'SEASONAL', 'REGIONAL', 'QUANTITY', 'ANNIVERSARY', 'COLLABORATION'
    )),
    CONSTRAINT valid_edition_status CHECK (status IN (
        'PLANNED', 'IN_PRODUCTION', 'ACTIVE', 'SOLD_OUT', 'CONCLUDED'
    ))
);

CREATE INDEX idx_edition_type ON limited_editions(edition_type);
CREATE INDEX idx_edition_status ON limited_editions(status);
CREATE INDEX idx_edition_base_product ON limited_editions(base_product_id);

-- 限定品販売実績
CREATE TABLE edition_sales (
    sale_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    edition_id UUID NOT NULL REFERENCES limited_editions(edition_id),
    sale_date DATE NOT NULL,
    region VARCHAR(50),
    channel VARCHAR(50),
    quantity_sold INT NOT NULL,
    revenue DECIMAL(15,2),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(edition_id, sale_date, region, channel)
);

CREATE INDEX idx_edition_sales_edition ON edition_sales(edition_id);
CREATE INDEX idx_edition_sales_date ON edition_sales(sale_date);

-- 限定品在庫
CREATE TABLE edition_inventory (
    inventory_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    edition_id UUID NOT NULL REFERENCES limited_editions(edition_id),
    region VARCHAR(50) NOT NULL,
    warehouse VARCHAR(100),
    quantity_available INT NOT NULL DEFAULT 0,
    quantity_reserved INT NOT NULL DEFAULT 0,
    last_updated TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(edition_id, region, warehouse)
);

CREATE INDEX idx_edition_inventory ON edition_inventory(edition_id);
```

### コラボ企画テーブル

```sql
-- コラボ企画
CREATE TABLE collaboration_projects (
    project_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    concept JSONB NOT NULL,
    status VARCHAR(50) DEFAULT 'PROPOSED',
    terms JSONB,
    timeline JSONB,
    responsibilities JSONB,
    revenue_share JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    launched_at TIMESTAMPTZ,
    concluded_at TIMESTAMPTZ,
    CONSTRAINT valid_collab_status CHECK (status IN (
        'PROPOSED', 'NEGOTIATING', 'AGREED', 'IN_DEVELOPMENT', 'ACTIVE', 'CONCLUDED'
    ))
);

CREATE INDEX idx_collab_status ON collaboration_projects(status);

-- コラボパートナー
CREATE TABLE collab_partners (
    partner_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES collaboration_projects(project_id),
    partner_name VARCHAR(200) NOT NULL,
    partner_type VARCHAR(50) NOT NULL,
    brand_value_alignment DECIMAL(3,2),
    audience_overlap DECIMAL(3,2),
    contact_info JSONB,
    agreement_status VARCHAR(50) DEFAULT 'PENDING',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_collab_partner_project ON collab_partners(project_id);

-- コラボ製品デザイン
CREATE TABLE collab_designs (
    design_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES collaboration_projects(project_id),
    design_name VARCHAR(200) NOT NULL,
    description TEXT,
    design_files JSONB DEFAULT '[]',  -- S3 URLs
    packaging_mockup VARCHAR(500),     -- S3 URL
    version INT DEFAULT 1,
    approval_status VARCHAR(50) DEFAULT 'PENDING_APPROVAL',
    feedback JSONB,
    submitted_by VARCHAR(100),
    submitted_at TIMESTAMPTZ DEFAULT NOW(),
    approved_at TIMESTAMPTZ
);

CREATE INDEX idx_collab_design_project ON collab_designs(project_id);

-- コラボ収益レポート
CREATE TABLE collab_revenue (
    revenue_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES collaboration_projects(project_id),
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    total_revenue DECIMAL(15,2) NOT NULL,
    asahi_share DECIMAL(15,2),
    partner_share DECIMAL(15,2),
    calculation_details JSONB,
    status VARCHAR(50) DEFAULT 'DRAFT',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(project_id, period_start, period_end)
);

CREATE INDEX idx_collab_revenue_project ON collab_revenue(project_id);
```

---

## ビュー定義

### 実験的製品サマリービュー

```sql
CREATE VIEW v_experimental_product_summary AS
SELECT
    ep.product_id,
    ep.concept->>'name' as product_name,
    ep.innovation_type->>'category' as innovation_category,
    ep.status,
    COUNT(DISTINCT p.prototype_id) as prototype_count,
    COUNT(DISTINCT mt.test_id) as test_count,
    MAX(mt.completed_at) as last_test_date,
    ep.decision->>'decision' as launch_decision,
    ep.created_at
FROM experimental_products ep
LEFT JOIN prototypes p ON ep.product_id = p.product_id
LEFT JOIN market_tests mt ON ep.product_id = mt.product_id
GROUP BY ep.product_id;
```

### 限定品パフォーマンスビュー

```sql
CREATE VIEW v_edition_performance AS
SELECT
    le.edition_id,
    le.theme->>'name' as edition_name,
    le.edition_type,
    le.status,
    (le.availability->>'quantity_limit')::int as planned_quantity,
    COALESCE(SUM(es.quantity_sold), 0) as total_sold,
    COALESCE(SUM(es.revenue), 0) as total_revenue,
    CASE
        WHEN (le.availability->>'quantity_limit')::int > 0
        THEN ROUND(COALESCE(SUM(es.quantity_sold), 0)::decimal /
             (le.availability->>'quantity_limit')::int * 100, 2)
        ELSE 0
    END as sell_through_rate,
    le.launched_at,
    le.concluded_at
FROM limited_editions le
LEFT JOIN edition_sales es ON le.edition_id = es.edition_id
GROUP BY le.edition_id;
```

---

## インデックス戦略

### 主要クエリパターン

```sql
-- ステータス別一覧取得（頻出）
CREATE INDEX idx_exp_product_status_created
ON experimental_products(status, created_at DESC);

-- 期間内の限定品検索
CREATE INDEX idx_edition_availability
ON limited_editions USING GIN(availability);

-- コラボパートナー種別検索
CREATE INDEX idx_collab_partner_type
ON collab_partners(partner_type);
```

---

## データ保持ポリシー

| テーブル | 保持期間 | アーカイブ先 |
|---------|---------|-------------|
| experimental_products | 5年 | S3 Glacier |
| market_tests | 5年 | S3 Glacier |
| consumer_feedback | 3年 | S3 Glacier |
| limited_editions | 永続 | - |
| edition_sales | 7年 | S3 Glacier |
| collaboration_projects | 永続 | - |

---

## パフォーマンス考慮

1. **JSONB使用理由**:
   - concept, target_segmentなど構造が柔軟なデータ
   - GINインデックスで特定フィールドの検索可能

2. **パーティショニング検討**:
   - edition_sales: 年度別パーティション推奨（データ量増加時）

3. **接続プール設定**:
   - HikariCP: maximumPoolSize=20
   - connectionTimeout=30000ms
