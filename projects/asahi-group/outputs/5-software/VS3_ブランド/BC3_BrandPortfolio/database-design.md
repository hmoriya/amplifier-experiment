# BC3: Brand Portfolio - データベース設計

## 概要

| 項目 | 内容 |
|------|------|
| VS | VS3 ブランド・マーケティング |
| BC | Brand Portfolio |
| Primary DB | PostgreSQL 15+ |
| Cache | Redis |
| アーキテクチャ | Modular Monolith |

---

## 1. データベース構成

```
┌─────────────────────────────────────────────────────────────┐
│               BC3: Brand Portfolio                           │
│                [Modular Monolith]                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────┐       │
│  │              PostgreSQL                          │       │
│  │                                                  │       │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐        │       │
│  │  │  Global  │ │  Local   │ │ Campaign │        │       │
│  │  │  Brand   │ │  Brand   │ │ Planning │        │       │
│  │  │  Tables  │ │  Tables  │ │  Tables  │        │       │
│  │  └──────────┘ └──────────┘ └──────────┘        │       │
│  │                                                  │       │
│  └─────────────────────────────────────────────────┘       │
│                          │                                  │
│                          ▼                                  │
│  ┌─────────────────────────────────────────────────┐       │
│  │                 Redis Cache                      │       │
│  │  • Brand Guidelines Cache                        │       │
│  │  • Asset URLs Cache                              │       │
│  │  • Active Campaigns Cache                        │       │
│  └─────────────────────────────────────────────────┘       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. PostgreSQL Tables

### 2.1 ブランド関連（Global Brand Module）

#### brands（ブランドマスタ）

```sql
CREATE TABLE brands (
    brand_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    brand_code VARCHAR(30) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    brand_type VARCHAR(20) NOT NULL,
    scope VARCHAR(20) NOT NULL,
    parent_brand_id UUID REFERENCES brands(brand_id),
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by UUID,

    CONSTRAINT chk_brand_type CHECK (brand_type IN (
        'corporate', 'master', 'sub', 'product', 'endorsed'
    )),
    CONSTRAINT chk_scope CHECK (scope IN ('global', 'regional', 'local')),
    CONSTRAINT chk_status CHECK (status IN ('draft', 'active', 'sunset', 'archived')),
    CONSTRAINT chk_name_length CHECK (LENGTH(name) >= 1 AND LENGTH(name) <= 100),
    CONSTRAINT chk_no_self_parent CHECK (brand_id != parent_brand_id)
);

CREATE INDEX idx_brands_code ON brands(brand_code);
CREATE INDEX idx_brands_type ON brands(brand_type);
CREATE INDEX idx_brands_scope ON brands(scope);
CREATE INDEX idx_brands_status ON brands(status);
CREATE INDEX idx_brands_parent ON brands(parent_brand_id);
CREATE INDEX idx_brands_name ON brands USING gin(to_tsvector('simple', name));

COMMENT ON TABLE brands IS 'ブランドマスタテーブル';
COMMENT ON COLUMN brands.brand_code IS 'ブランドコード（BRD-{Region}-{Type}-NNN形式）';
```

#### brand_identities（ブランドアイデンティティ）

```sql
CREATE TABLE brand_identities (
    identity_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    brand_id UUID NOT NULL REFERENCES brands(brand_id) ON DELETE CASCADE,
    mission TEXT,
    vision TEXT,
    values TEXT[],
    positioning TEXT,
    tagline VARCHAR(200),
    story_narrative TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_identities_brand ON brand_identities(brand_id);

COMMENT ON TABLE brand_identities IS 'ブランドアイデンティティ';
```

#### brand_personalities（ブランドパーソナリティ）

```sql
CREATE TABLE brand_personalities (
    personality_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    brand_id UUID NOT NULL REFERENCES brands(brand_id) ON DELETE CASCADE,
    traits TEXT[],
    archetypes TEXT[],
    tone_of_voice TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_personalities_brand ON brand_personalities(brand_id);

COMMENT ON TABLE brand_personalities IS 'ブランドパーソナリティ';
```

### 2.2 ガイドライン関連

#### brand_guidelines（ブランドガイドライン）

```sql
CREATE TABLE brand_guidelines (
    guideline_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    brand_id UUID NOT NULL REFERENCES brands(brand_id) ON DELETE CASCADE,
    version VARCHAR(20) NOT NULL DEFAULT '1.0.0',
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    published_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_guideline_status CHECK (status IN ('draft', 'published', 'archived'))
);

CREATE INDEX idx_guidelines_brand ON brand_guidelines(brand_id);
CREATE INDEX idx_guidelines_status ON brand_guidelines(status);

COMMENT ON TABLE brand_guidelines IS 'ブランドガイドラインバージョン管理';
```

#### visual_identity_guidelines（ビジュアルアイデンティティ）

```sql
CREATE TABLE visual_identity_guidelines (
    visual_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guideline_id UUID NOT NULL REFERENCES brand_guidelines(guideline_id) ON DELETE CASCADE,
    primary_colors JSONB,
    secondary_colors JSONB,
    typography JSONB,
    logo_usage JSONB,
    imagery JSONB,
    spacing JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_visual_guideline ON visual_identity_guidelines(guideline_id);

COMMENT ON TABLE visual_identity_guidelines IS 'ビジュアルアイデンティティガイドライン';
COMMENT ON COLUMN visual_identity_guidelines.primary_colors IS 'プライマリカラー定義（JSON配列）';
```

#### voice_tone_guidelines（ボイス&トーン）

```sql
CREATE TABLE voice_tone_guidelines (
    voice_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guideline_id UUID NOT NULL REFERENCES brand_guidelines(guideline_id) ON DELETE CASCADE,
    voice_attributes TEXT[],
    do_list TEXT[],
    dont_list TEXT[],
    examples JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_voice_guideline ON voice_tone_guidelines(guideline_id);

COMMENT ON TABLE voice_tone_guidelines IS 'ボイス&トーンガイドライン';
```

#### messaging_guidelines（メッセージング）

```sql
CREATE TABLE messaging_guidelines (
    messaging_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guideline_id UUID NOT NULL REFERENCES brand_guidelines(guideline_id) ON DELETE CASCADE,
    key_messages TEXT[],
    proof_points TEXT[],
    call_to_actions TEXT[],
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_messaging_guideline ON messaging_guidelines(guideline_id);

COMMENT ON TABLE messaging_guidelines IS 'メッセージングガイドライン';
```

#### usage_rules（使用ルール）

```sql
CREATE TABLE usage_rules (
    rule_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guideline_id UUID NOT NULL REFERENCES brand_guidelines(guideline_id) ON DELETE CASCADE,
    category VARCHAR(50) NOT NULL,
    rule_text TEXT NOT NULL,
    examples TEXT[],
    display_order INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX idx_usage_rules_guideline ON usage_rules(guideline_id, display_order);

COMMENT ON TABLE usage_rules IS 'ブランド使用ルール';
```

### 2.3 アセット関連

#### brand_assets（ブランドアセット）

```sql
CREATE TABLE brand_assets (
    asset_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    brand_id UUID NOT NULL REFERENCES brands(brand_id) ON DELETE CASCADE,
    asset_type VARCHAR(20) NOT NULL,
    name VARCHAR(200) NOT NULL,
    storage_url VARCHAR(1000) NOT NULL,
    cdn_url VARCHAR(1000),
    format VARCHAR(20),
    resolution VARCHAR(50),
    file_size INTEGER,
    usage VARCHAR(20),
    metadata JSONB,
    expires_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by UUID,

    CONSTRAINT chk_asset_type CHECK (asset_type IN (
        'logo', 'image', 'video', 'document', 'template'
    )),
    CONSTRAINT chk_usage CHECK (usage IN (
        'primary', 'secondary', 'digital', 'print', 'social'
    ))
);

CREATE INDEX idx_assets_brand ON brand_assets(brand_id);
CREATE INDEX idx_assets_type ON brand_assets(asset_type);
CREATE INDEX idx_assets_usage ON brand_assets(usage);
CREATE INDEX idx_assets_expires ON brand_assets(expires_at) WHERE expires_at IS NOT NULL;

COMMENT ON TABLE brand_assets IS 'ブランドアセット';
```

#### asset_variants（アセットバリアント）

```sql
CREATE TABLE asset_variants (
    variant_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id UUID NOT NULL REFERENCES brand_assets(asset_id) ON DELETE CASCADE,
    variant_type VARCHAR(20) NOT NULL,
    storage_url VARCHAR(1000) NOT NULL,
    width INTEGER,
    height INTEGER,
    file_size INTEGER,

    CONSTRAINT chk_variant_type CHECK (variant_type IN (
        'original', 'high', 'medium', 'low', 'thumbnail'
    ))
);

CREATE INDEX idx_variants_asset ON asset_variants(asset_id);

COMMENT ON TABLE asset_variants IS 'アセットサイズバリアント';
```

### 2.4 キャンペーン関連（Campaign Planning Module）

#### campaigns（キャンペーン）

```sql
CREATE TABLE campaigns (
    campaign_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_code VARCHAR(30) NOT NULL UNIQUE,
    name VARCHAR(200) NOT NULL,
    brand_id UUID NOT NULL REFERENCES brands(brand_id),
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    launch_date DATE,
    end_date DATE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by UUID,
    approved_at TIMESTAMP,
    approved_by UUID,

    CONSTRAINT chk_campaign_status CHECK (status IN (
        'draft', 'planning', 'approved', 'in_execution', 'completed', 'cancelled'
    )),
    CONSTRAINT chk_dates CHECK (end_date IS NULL OR launch_date <= end_date)
);

CREATE INDEX idx_campaigns_brand ON campaigns(brand_id);
CREATE INDEX idx_campaigns_status ON campaigns(status);
CREATE INDEX idx_campaigns_dates ON campaigns(launch_date, end_date);
CREATE INDEX idx_campaigns_code ON campaigns(campaign_code);

COMMENT ON TABLE campaigns IS 'マーケティングキャンペーン';
```

#### campaign_objectives（キャンペーン目的）

```sql
CREATE TABLE campaign_objectives (
    objective_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id UUID NOT NULL REFERENCES campaigns(campaign_id) ON DELETE CASCADE,
    objective_type VARCHAR(20) NOT NULL,
    description TEXT,
    targets JSONB,

    CONSTRAINT chk_objective_type CHECK (objective_type IN (
        'awareness', 'consideration', 'conversion', 'loyalty', 'advocacy'
    ))
);

CREATE UNIQUE INDEX idx_objectives_campaign ON campaign_objectives(campaign_id);

COMMENT ON TABLE campaign_objectives IS 'キャンペーン目的';
```

#### campaign_audiences（ターゲットオーディエンス）

```sql
CREATE TABLE campaign_audiences (
    audience_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id UUID NOT NULL REFERENCES campaigns(campaign_id) ON DELETE CASCADE,
    demographics JSONB,
    psychographics JSONB,
    behaviors JSONB,
    segments TEXT[]
);

CREATE UNIQUE INDEX idx_audiences_campaign ON campaign_audiences(campaign_id);

COMMENT ON TABLE campaign_audiences IS 'キャンペーンターゲットオーディエンス';
```

#### campaign_briefs（キャンペーンブリーフ）

```sql
CREATE TABLE campaign_briefs (
    brief_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id UUID NOT NULL REFERENCES campaigns(campaign_id) ON DELETE CASCADE,
    background TEXT,
    challenge TEXT,
    opportunity TEXT,
    key_message TEXT,
    creative_direction TEXT,
    mandatories TEXT[],
    restrictions TEXT[],
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_briefs_campaign ON campaign_briefs(campaign_id);

COMMENT ON TABLE campaign_briefs IS 'キャンペーンブリーフ';
```

#### campaign_budgets（キャンペーン予算）

```sql
CREATE TABLE campaign_budgets (
    budget_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id UUID NOT NULL REFERENCES campaigns(campaign_id) ON DELETE CASCADE,
    total_amount DECIMAL(15,2) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'JPY',
    allocation JSONB,
    contingency DECIMAL(15,2),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_budgets_campaign ON campaign_budgets(campaign_id);

COMMENT ON TABLE campaign_budgets IS 'キャンペーン予算';
```

#### campaign_timelines（キャンペーンタイムライン）

```sql
CREATE TABLE campaign_timelines (
    timeline_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id UUID NOT NULL REFERENCES campaigns(campaign_id) ON DELETE CASCADE,
    planning_start DATE,
    creative_deadline DATE,
    launch_date DATE,
    end_date DATE
);

CREATE UNIQUE INDEX idx_timelines_campaign ON campaign_timelines(campaign_id);

COMMENT ON TABLE campaign_timelines IS 'キャンペーンタイムライン';
```

#### campaign_milestones（マイルストーン）

```sql
CREATE TABLE campaign_milestones (
    milestone_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id UUID NOT NULL REFERENCES campaigns(campaign_id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    milestone_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    display_order INTEGER NOT NULL DEFAULT 0,

    CONSTRAINT chk_milestone_status CHECK (status IN ('pending', 'completed', 'missed'))
);

CREATE INDEX idx_milestones_campaign ON campaign_milestones(campaign_id, display_order);

COMMENT ON TABLE campaign_milestones IS 'キャンペーンマイルストーン';
```

#### campaign_channels（マーケティングチャネル）

```sql
CREATE TABLE campaign_channels (
    campaign_id UUID NOT NULL REFERENCES campaigns(campaign_id) ON DELETE CASCADE,
    channel VARCHAR(20) NOT NULL,
    budget_allocation DECIMAL(15,2),
    primary_flag BOOLEAN NOT NULL DEFAULT FALSE,

    PRIMARY KEY (campaign_id, channel),

    CONSTRAINT chk_channel CHECK (channel IN (
        'tv', 'radio', 'print', 'ooh', 'digital', 'social',
        'influencer', 'event', 'sponsorship', 'retail'
    ))
);

COMMENT ON TABLE campaign_channels IS 'キャンペーンチャネル';
```

#### campaign_kpis（KPI）

```sql
CREATE TABLE campaign_kpis (
    kpi_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id UUID NOT NULL REFERENCES campaigns(campaign_id) ON DELETE CASCADE,
    metric VARCHAR(50) NOT NULL,
    target_value DECIMAL(15,2) NOT NULL,
    unit VARCHAR(20),
    measurement_method TEXT,
    actual_value DECIMAL(15,2),
    measured_at TIMESTAMP
);

CREATE INDEX idx_kpis_campaign ON campaign_kpis(campaign_id);

COMMENT ON TABLE campaign_kpis IS 'キャンペーンKPI';
```

#### campaign_creatives（クリエイティブ）

```sql
CREATE TABLE campaign_creatives (
    creative_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id UUID NOT NULL REFERENCES campaigns(campaign_id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    format VARCHAR(50),
    channel VARCHAR(20),
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    approved_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_creative_status CHECK (status IN (
        'draft', 'in_review', 'approved', 'rejected'
    ))
);

CREATE INDEX idx_creatives_campaign ON campaign_creatives(campaign_id);
CREATE INDEX idx_creatives_status ON campaign_creatives(status);

COMMENT ON TABLE campaign_creatives IS 'キャンペーンクリエイティブ';
```

#### creative_assets（クリエイティブアセット紐付け）

```sql
CREATE TABLE creative_assets (
    creative_id UUID NOT NULL REFERENCES campaign_creatives(creative_id) ON DELETE CASCADE,
    asset_id UUID NOT NULL REFERENCES brand_assets(asset_id),

    PRIMARY KEY (creative_id, asset_id)
);

COMMENT ON TABLE creative_assets IS 'クリエイティブとアセットの紐付け';
```

#### campaign_results（キャンペーン結果）

```sql
CREATE TABLE campaign_results (
    result_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id UUID NOT NULL REFERENCES campaigns(campaign_id) ON DELETE CASCADE,
    roi DECIMAL(8,2),
    learnings TEXT[],
    recorded_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_results_campaign ON campaign_results(campaign_id);

COMMENT ON TABLE campaign_results IS 'キャンペーン結果';
```

### 2.5 市場関連（Local Brand Module）

#### market_presences（市場プレゼンス）

```sql
CREATE TABLE market_presences (
    presence_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    brand_id UUID NOT NULL REFERENCES brands(brand_id) ON DELETE CASCADE,
    market_id VARCHAR(2) NOT NULL,
    local_brand_name VARCHAR(100),
    local_tagline VARCHAR(200),
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    launched_at DATE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_market_id CHECK (market_id ~ '^[A-Z]{2}$'),
    CONSTRAINT chk_presence_status CHECK (status IN ('active', 'suspended', 'terminated')),
    UNIQUE (brand_id, market_id)
);

CREATE INDEX idx_presences_brand ON market_presences(brand_id);
CREATE INDEX idx_presences_market ON market_presences(market_id);
CREATE INDEX idx_presences_status ON market_presences(status);

COMMENT ON TABLE market_presences IS '市場プレゼンス';
COMMENT ON COLUMN market_presences.market_id IS 'ISO 3166-1 alpha-2 国コード';
```

#### market_localizations（市場ローカライズ）

```sql
CREATE TABLE market_localizations (
    localization_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    presence_id UUID NOT NULL REFERENCES market_presences(presence_id) ON DELETE CASCADE,
    language VARCHAR(5) NOT NULL,
    cultural_adaptations TEXT[],
    regulatory_compliance TEXT[],
    local_partners JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_localizations_presence ON market_localizations(presence_id);

COMMENT ON TABLE market_localizations IS '市場ローカライズ情報';
```

#### market_performances（市場パフォーマンス）

```sql
CREATE TABLE market_performances (
    performance_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    presence_id UUID NOT NULL REFERENCES market_presences(presence_id) ON DELETE CASCADE,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    market_share DECIMAL(5,2),
    sales_volume DECIMAL(15,2),
    brand_awareness DECIMAL(5,2),
    brand_preference DECIMAL(5,2),
    nps INTEGER,
    recorded_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_period CHECK (period_start <= period_end),
    CONSTRAINT chk_share CHECK (market_share BETWEEN 0 AND 100),
    CONSTRAINT chk_awareness CHECK (brand_awareness BETWEEN 0 AND 100),
    CONSTRAINT chk_preference CHECK (brand_preference BETWEEN 0 AND 100)
);

CREATE INDEX idx_performances_presence ON market_performances(presence_id);
CREATE INDEX idx_performances_period ON market_performances(period_start, period_end);

COMMENT ON TABLE market_performances IS '市場パフォーマンス実績';
```

#### market_competitors（競合情報）

```sql
CREATE TABLE market_competitors (
    competitor_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    presence_id UUID NOT NULL REFERENCES market_presences(presence_id) ON DELETE CASCADE,
    competitor_name VARCHAR(100) NOT NULL,
    market_share DECIMAL(5,2),
    positioning TEXT,
    strengths TEXT[],
    weaknesses TEXT[],
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_competitors_presence ON market_competitors(presence_id);

COMMENT ON TABLE market_competitors IS '競合情報';
```

---

## 3. Views

### brand_portfolio_view

```sql
CREATE VIEW brand_portfolio_view AS
SELECT
    b.brand_id,
    b.brand_code,
    b.name,
    b.brand_type,
    b.scope,
    b.status,
    pb.name AS parent_brand_name,
    bi.tagline,
    COUNT(DISTINCT mp.market_id) AS market_count,
    COUNT(DISTINCT ba.asset_id) AS asset_count,
    COUNT(DISTINCT c.campaign_id) FILTER (WHERE c.status = 'in_execution') AS active_campaigns
FROM brands b
LEFT JOIN brands pb ON b.parent_brand_id = pb.brand_id
LEFT JOIN brand_identities bi ON b.brand_id = bi.brand_id
LEFT JOIN market_presences mp ON b.brand_id = mp.brand_id AND mp.status = 'active'
LEFT JOIN brand_assets ba ON b.brand_id = ba.brand_id
LEFT JOIN campaigns c ON b.brand_id = c.brand_id
GROUP BY b.brand_id, b.brand_code, b.name, b.brand_type, b.scope, b.status,
         pb.name, bi.tagline;

COMMENT ON VIEW brand_portfolio_view IS 'ブランドポートフォリオビュー';
```

### active_campaigns_view

```sql
CREATE VIEW active_campaigns_view AS
SELECT
    c.campaign_id,
    c.campaign_code,
    c.name,
    c.status,
    c.launch_date,
    c.end_date,
    b.brand_id,
    b.name AS brand_name,
    co.objective_type,
    cb.total_amount AS budget,
    ARRAY_AGG(DISTINCT cc.channel) AS channels,
    COUNT(DISTINCT cr.creative_id) AS creative_count
FROM campaigns c
JOIN brands b ON c.brand_id = b.brand_id
LEFT JOIN campaign_objectives co ON c.campaign_id = co.campaign_id
LEFT JOIN campaign_budgets cb ON c.campaign_id = cb.campaign_id
LEFT JOIN campaign_channels cc ON c.campaign_id = cc.campaign_id
LEFT JOIN campaign_creatives cr ON c.campaign_id = cr.campaign_id
WHERE c.status IN ('planning', 'approved', 'in_execution')
GROUP BY c.campaign_id, c.campaign_code, c.name, c.status, c.launch_date, c.end_date,
         b.brand_id, b.name, co.objective_type, cb.total_amount;

COMMENT ON VIEW active_campaigns_view IS 'アクティブキャンペーンビュー';
```

### brand_market_performance_view

```sql
CREATE VIEW brand_market_performance_view AS
SELECT
    b.brand_id,
    b.name AS brand_name,
    mp.market_id,
    mp.local_brand_name,
    mp.status AS presence_status,
    mperf.period_start,
    mperf.period_end,
    mperf.market_share,
    mperf.sales_volume,
    mperf.brand_awareness,
    mperf.brand_preference,
    mperf.nps
FROM brands b
JOIN market_presences mp ON b.brand_id = mp.brand_id
LEFT JOIN market_performances mperf ON mp.presence_id = mperf.presence_id
WHERE mp.status = 'active';

COMMENT ON VIEW brand_market_performance_view IS 'ブランド市場パフォーマンスビュー';
```

---

## 4. Functions & Triggers

### ブランドコード自動生成

```sql
CREATE OR REPLACE FUNCTION generate_brand_code()
RETURNS TRIGGER AS $$
DECLARE
    region_code VARCHAR(3);
    type_code VARCHAR(4);
    seq_num INTEGER;
BEGIN
    IF NEW.brand_code IS NULL THEN
        -- Scope → Region code
        region_code := CASE NEW.scope
            WHEN 'global' THEN 'GLB'
            WHEN 'regional' THEN 'REG'
            WHEN 'local' THEN 'LCL'
        END;

        -- Type code
        type_code := UPPER(SUBSTRING(NEW.brand_type, 1, 4));

        SELECT COALESCE(MAX(CAST(SUBSTRING(brand_code FROM '.*-(\d{3})$') AS INTEGER)), 0) + 1
        INTO seq_num
        FROM brands
        WHERE brand_code LIKE 'BRD-' || region_code || '-' || type_code || '-%';

        NEW.brand_code := 'BRD-' || region_code || '-' || type_code || '-' || LPAD(seq_num::TEXT, 3, '0');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_brand_code_gen
    BEFORE INSERT ON brands
    FOR EACH ROW EXECUTE FUNCTION generate_brand_code();
```

### キャンペーンコード自動生成

```sql
CREATE OR REPLACE FUNCTION generate_campaign_code()
RETURNS TRIGGER AS $$
DECLARE
    brand_abbr VARCHAR(3);
    year_month VARCHAR(6);
    seq_num INTEGER;
BEGIN
    IF NEW.campaign_code IS NULL THEN
        SELECT UPPER(SUBSTRING(name, 1, 3)) INTO brand_abbr
        FROM brands WHERE brand_id = NEW.brand_id;

        year_month := TO_CHAR(NOW(), 'YYYYMM');

        SELECT COALESCE(MAX(CAST(SUBSTRING(campaign_code FROM '.*-(\d{3})$') AS INTEGER)), 0) + 1
        INTO seq_num
        FROM campaigns
        WHERE campaign_code LIKE 'CMP-' || brand_abbr || '-' || year_month || '-%';

        NEW.campaign_code := 'CMP-' || brand_abbr || '-' || year_month || '-' || LPAD(seq_num::TEXT, 3, '0');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_campaign_code_gen
    BEFORE INSERT ON campaigns
    FOR EACH ROW EXECUTE FUNCTION generate_campaign_code();
```

### 更新日時自動更新

```sql
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to relevant tables
CREATE TRIGGER trg_brands_updated BEFORE UPDATE ON brands FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER trg_identities_updated BEFORE UPDATE ON brand_identities FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER trg_campaigns_updated BEFORE UPDATE ON campaigns FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER trg_presences_updated BEFORE UPDATE ON market_presences FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

---

## 5. Redis Cache Schema

### ブランドガイドラインキャッシュ

```
Key: brand:guidelines:{brandId}
TTL: 1 hour
Value: JSON
{
  "brandId": "uuid",
  "visualIdentity": {...},
  "voiceTone": {...},
  "messaging": {...},
  "updatedAt": "timestamp"
}
```

### アセットURLキャッシュ

```
Key: brand:assets:{brandId}:{assetType}
TTL: 30 minutes
Value: JSON Array
[
  {
    "assetId": "uuid",
    "name": "...",
    "cdnUrl": "...",
    "variants": {...}
  }
]
```

### アクティブキャンペーンキャッシュ

```
Key: campaigns:active:{brandId}
TTL: 15 minutes
Value: JSON Array
[
  {
    "campaignId": "uuid",
    "name": "...",
    "status": "...",
    "launchDate": "..."
  }
]
```

### ブランド階層キャッシュ

```
Key: brand:hierarchy:{brandId}
TTL: 1 hour
Value: JSON
{
  "brand": {...},
  "parent": {...},
  "children": [...]
}
```

---

## 6. Migration Strategy

### マイグレーションファイル

```
V001__create_brands_tables.sql
V002__create_guidelines_tables.sql
V003__create_assets_tables.sql
V004__create_campaigns_tables.sql
V005__create_markets_tables.sql
V006__create_views.sql
V007__create_functions_triggers.sql
V008__insert_master_data.sql
```

### 初期マスタデータ

```sql
-- V008__insert_master_data.sql

-- グローバルブランド
INSERT INTO brands (name, brand_type, scope, status) VALUES
('Asahi', 'corporate', 'global', 'active'),
('Asahi Super Dry', 'master', 'global', 'active'),
('Peroni Nastro Azzurro', 'master', 'global', 'active'),
('Pilsner Urquell', 'master', 'regional', 'active');

-- ブランドアイデンティティ
INSERT INTO brand_identities (brand_id, mission, vision, tagline)
SELECT brand_id,
       'Deliver the best quality and excitement',
       'Be the world''s most innovative brewer',
       'Karakuchi'
FROM brands WHERE name = 'Asahi Super Dry';
```

---

## 7. Data Retention & Backup

### データ保持ポリシー

| データ種別 | 保持期間 | 処理 |
|-----------|---------|------|
| ブランドマスタ | 永続 | アーカイブステータスで論理削除 |
| ガイドライン | 永続 | バージョン管理で履歴保持 |
| アセット | 永続 | 期限切れのみ物理削除可 |
| キャンペーン | 5年 | 完了後5年でアーカイブ |
| 市場パフォーマンス | 10年 | 10年以上古いデータは集計のみ保持 |

### バックアップ戦略

```yaml
PostgreSQL:
  Full Backup: Daily at 02:00
  Retention: 30 days

Redis:
  RDB Snapshot: Every 15 minutes
  AOF: Always

Asset Storage (S3):
  Versioning: Enabled
  Cross-region Replication: Enabled
```

---

**作成日**: 2025-11-28
**VS**: VS3 ブランド・マーケティング
**BC**: BC3 Brand Portfolio
**次**: Supporting BCs (BC4-BC7)
