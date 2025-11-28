# BC2: Product Recipe - データベース設計

## 概要

| 項目 | 内容 |
|------|------|
| VS | VS2 製品開発 |
| BC | Product Recipe |
| Primary DB | PostgreSQL 15+ (Write Model) |
| Search DB | Elasticsearch 8.x (Read Model) |
| アーキテクチャ | CQRS |

---

## 1. データベース構成（CQRS）

```
┌─────────────────────────────────────────────────────────────┐
│                    BC2: Product Recipe                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────────────────┐    ┌────────────────────┐          │
│  │   PostgreSQL       │    │   Elasticsearch    │          │
│  │   (Write Model)    │───►│   (Read Model)     │          │
│  │                    │CDC │                    │          │
│  │ • recipes          │    │ • recipes_index    │          │
│  │ • ingredients      │    │ • evaluations_     │          │
│  │ • quality_         │    │   index            │          │
│  │   standards        │    │                    │          │
│  │ • evaluations      │    │                    │          │
│  └────────────────────┘    └────────────────────┘          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. PostgreSQL Tables (Write Model)

### 2.1 処方関連

#### recipes（処方マスタ）

```sql
CREATE TABLE recipes (
    recipe_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipe_code VARCHAR(30) NOT NULL UNIQUE,
    name VARCHAR(200) NOT NULL,
    product_type VARCHAR(20) NOT NULL,
    version_major INTEGER NOT NULL DEFAULT 1,
    version_minor INTEGER NOT NULL DEFAULT 0,
    version_patch INTEGER NOT NULL DEFAULT 0,
    parent_recipe_id UUID REFERENCES recipes(recipe_id),
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by UUID,
    approved_at TIMESTAMP,
    approved_by UUID,
    version INTEGER NOT NULL DEFAULT 1,

    CONSTRAINT chk_product_type CHECK (product_type IN (
        'beer', 'low_malt_beer', 'happoshu', 'non_alcohol', 'rtd', 'spirits'
    )),
    CONSTRAINT chk_status CHECK (status IN (
        'draft', 'under_review', 'approved', 'production', 'archived'
    )),
    CONSTRAINT chk_name_length CHECK (LENGTH(name) >= 1 AND LENGTH(name) <= 200)
);

CREATE INDEX idx_recipes_code ON recipes(recipe_code);
CREATE INDEX idx_recipes_type ON recipes(product_type);
CREATE INDEX idx_recipes_status ON recipes(status);
CREATE INDEX idx_recipes_name ON recipes USING gin(to_tsvector('simple', name));
CREATE INDEX idx_recipes_parent ON recipes(parent_recipe_id);
CREATE INDEX idx_recipes_created ON recipes(created_at DESC);

COMMENT ON TABLE recipes IS '製品処方マスタテーブル';
```

#### recipe_concepts（製品コンセプト）

```sql
CREATE TABLE recipe_concepts (
    concept_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipe_id UUID NOT NULL REFERENCES recipes(recipe_id) ON DELETE CASCADE,
    description TEXT,
    target_consumer TEXT,
    positioning TEXT,
    key_features TEXT[],
    brand_id UUID,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_concepts_recipe ON recipe_concepts(recipe_id);

COMMENT ON TABLE recipe_concepts IS '製品コンセプト情報';
```

#### recipe_ingredients（原料構成）

```sql
CREATE TABLE recipe_ingredients (
    ingredient_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipe_id UUID NOT NULL REFERENCES recipes(recipe_id) ON DELETE CASCADE,
    ingredient_type VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL,
    ratio DECIMAL(5,2) NOT NULL,
    spec_grade VARCHAR(50),
    spec_origin VARCHAR(100),
    spec_characteristics JSONB,
    supplier_id UUID,
    display_order INTEGER NOT NULL DEFAULT 0,

    CONSTRAINT chk_ingredient_type CHECK (ingredient_type IN (
        'malt', 'hop', 'yeast', 'water', 'adjunct', 'additive'
    )),
    CONSTRAINT chk_ratio CHECK (ratio >= 0 AND ratio <= 100)
);

CREATE INDEX idx_ingredients_recipe ON recipe_ingredients(recipe_id, display_order);
CREATE INDEX idx_ingredients_type ON recipe_ingredients(ingredient_type);

COMMENT ON TABLE recipe_ingredients IS '処方原料構成';
```

#### recipe_process_specs（製造仕様）

```sql
CREATE TABLE recipe_process_specs (
    spec_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipe_id UUID NOT NULL REFERENCES recipes(recipe_id) ON DELETE CASCADE,
    mashing_spec JSONB,
    boiling_spec JSONB,
    fermentation_spec JSONB,
    maturation_spec JSONB,
    filtering_spec JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_process_specs_recipe ON recipe_process_specs(recipe_id);

COMMENT ON TABLE recipe_process_specs IS '製造仕様';
COMMENT ON COLUMN recipe_process_specs.fermentation_spec IS '発酵仕様（yeast_strain_id含む）';
```

#### recipe_target_profiles（目標風味プロファイル）

```sql
CREATE TABLE recipe_target_profiles (
    profile_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipe_id UUID NOT NULL REFERENCES recipes(recipe_id) ON DELETE CASCADE,
    appearance TEXT,
    aroma TEXT,
    taste TEXT,
    mouthfeel TEXT,
    aftertaste TEXT,
    target_alcohol DECIMAL(4,1),
    target_bitterness DECIMAL(5,1),
    target_color DECIMAL(5,1),
    target_gravity DECIMAL(6,4),
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_target_profiles_recipe ON recipe_target_profiles(recipe_id);

COMMENT ON TABLE recipe_target_profiles IS '目標風味プロファイル';
```

### 2.2 品質基準関連

#### quality_standards（品質基準）

```sql
CREATE TABLE quality_standards (
    standard_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipe_id UUID NOT NULL REFERENCES recipes(recipe_id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    effective_from DATE,
    effective_to DATE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by UUID,

    CONSTRAINT chk_standard_status CHECK (status IN ('draft', 'active', 'expired')),
    CONSTRAINT chk_effective_dates CHECK (effective_to IS NULL OR effective_from <= effective_to)
);

CREATE INDEX idx_standards_recipe ON quality_standards(recipe_id);
CREATE INDEX idx_standards_status ON quality_standards(status);
CREATE INDEX idx_standards_effective ON quality_standards(effective_from, effective_to);

COMMENT ON TABLE quality_standards IS '品質基準マスタ';
```

#### physical_specifications（理化学規格）

```sql
CREATE TABLE physical_specifications (
    spec_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    standard_id UUID NOT NULL REFERENCES quality_standards(standard_id) ON DELETE CASCADE,
    alcohol_min DECIMAL(4,1),
    alcohol_max DECIMAL(4,1),
    alcohol_target DECIMAL(4,1),
    gravity_min DECIMAL(6,4),
    gravity_max DECIMAL(6,4),
    gravity_target DECIMAL(6,4),
    color_min DECIMAL(5,1),
    color_max DECIMAL(5,1),
    color_target DECIMAL(5,1),
    bitterness_min DECIMAL(5,1),
    bitterness_max DECIMAL(5,1),
    bitterness_target DECIMAL(5,1),
    carbonation_min DECIMAL(4,2),
    carbonation_max DECIMAL(4,2),
    ph_min DECIMAL(4,2),
    ph_max DECIMAL(4,2)
);

CREATE UNIQUE INDEX idx_physical_specs_standard ON physical_specifications(standard_id);

COMMENT ON TABLE physical_specifications IS '理化学規格';
```

#### sensory_specifications（官能規格）

```sql
CREATE TABLE sensory_specifications (
    spec_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    standard_id UUID NOT NULL REFERENCES quality_standards(standard_id) ON DELETE CASCADE,
    attribute_name VARCHAR(50) NOT NULL,
    target_score DECIMAL(3,1),
    min_score DECIMAL(3,1),
    max_score DECIMAL(3,1),
    description TEXT,

    CONSTRAINT chk_score_range CHECK (
        target_score BETWEEN 1.0 AND 10.0 AND
        min_score BETWEEN 1.0 AND 10.0 AND
        max_score BETWEEN 1.0 AND 10.0
    )
);

CREATE INDEX idx_sensory_specs_standard ON sensory_specifications(standard_id);

COMMENT ON TABLE sensory_specifications IS '官能規格';
```

### 2.3 官能評価関連

#### sensory_evaluations（官能評価）

```sql
CREATE TABLE sensory_evaluations (
    evaluation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evaluation_type VARCHAR(20) NOT NULL,
    recipe_id UUID NOT NULL REFERENCES recipes(recipe_id),
    sample_id UUID,
    evaluation_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'scheduled',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP,
    created_by UUID,

    CONSTRAINT chk_eval_type CHECK (evaluation_type IN (
        'development', 'quality_check', 'benchmark', 'consumer'
    )),
    CONSTRAINT chk_eval_status CHECK (status IN (
        'scheduled', 'in_progress', 'completed', 'cancelled'
    ))
);

CREATE INDEX idx_evaluations_recipe ON sensory_evaluations(recipe_id);
CREATE INDEX idx_evaluations_date ON sensory_evaluations(evaluation_date);
CREATE INDEX idx_evaluations_status ON sensory_evaluations(status);

COMMENT ON TABLE sensory_evaluations IS '官能評価セッション';
```

#### evaluation_panelists（評価パネリスト）

```sql
CREATE TABLE evaluation_panelists (
    evaluation_id UUID NOT NULL REFERENCES sensory_evaluations(evaluation_id) ON DELETE CASCADE,
    panelist_id UUID NOT NULL,
    panelist_name VARCHAR(100),
    qualification VARCHAR(50),
    joined_at TIMESTAMP NOT NULL DEFAULT NOW(),

    PRIMARY KEY (evaluation_id, panelist_id)
);

CREATE INDEX idx_panelists_panelist ON evaluation_panelists(panelist_id);

COMMENT ON TABLE evaluation_panelists IS '評価参加パネリスト';
```

#### panelist_scores（パネリストスコア）

```sql
CREATE TABLE panelist_scores (
    score_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evaluation_id UUID NOT NULL,
    panelist_id UUID NOT NULL,
    attribute_name VARCHAR(50) NOT NULL,
    score DECIMAL(3,1) NOT NULL,
    recorded_at TIMESTAMP NOT NULL DEFAULT NOW(),

    FOREIGN KEY (evaluation_id, panelist_id)
        REFERENCES evaluation_panelists(evaluation_id, panelist_id) ON DELETE CASCADE,

    CONSTRAINT chk_score CHECK (score BETWEEN 1.0 AND 10.0)
);

CREATE INDEX idx_scores_evaluation ON panelist_scores(evaluation_id);
CREATE UNIQUE INDEX idx_scores_unique ON panelist_scores(evaluation_id, panelist_id, attribute_name);

COMMENT ON TABLE panelist_scores IS 'パネリスト個別スコア';
```

#### panelist_comments（パネリストコメント）

```sql
CREATE TABLE panelist_comments (
    comment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evaluation_id UUID NOT NULL,
    panelist_id UUID NOT NULL,
    comments TEXT,
    recorded_at TIMESTAMP NOT NULL DEFAULT NOW(),

    FOREIGN KEY (evaluation_id, panelist_id)
        REFERENCES evaluation_panelists(evaluation_id, panelist_id) ON DELETE CASCADE
);

CREATE UNIQUE INDEX idx_comments_unique ON panelist_comments(evaluation_id, panelist_id);

COMMENT ON TABLE panelist_comments IS 'パネリストコメント';
```

#### evaluation_results（評価結果サマリー）

```sql
CREATE TABLE evaluation_results (
    result_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evaluation_id UUID NOT NULL REFERENCES sensory_evaluations(evaluation_id) ON DELETE CASCADE,
    overall_score DECIMAL(3,1),
    panel_consensus VARCHAR(10),
    recommendation VARCHAR(500),
    calculated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_consensus CHECK (panel_consensus IN ('high', 'medium', 'low'))
);

CREATE UNIQUE INDEX idx_results_evaluation ON evaluation_results(evaluation_id);

COMMENT ON TABLE evaluation_results IS '官能評価結果サマリー';
```

#### evaluation_average_scores（評価平均スコア）

```sql
CREATE TABLE evaluation_average_scores (
    evaluation_id UUID NOT NULL REFERENCES sensory_evaluations(evaluation_id) ON DELETE CASCADE,
    attribute_name VARCHAR(50) NOT NULL,
    average_score DECIMAL(4,2) NOT NULL,
    std_deviation DECIMAL(4,2),
    min_score DECIMAL(3,1),
    max_score DECIMAL(3,1),
    panelist_count INTEGER NOT NULL,

    PRIMARY KEY (evaluation_id, attribute_name)
);

COMMENT ON TABLE evaluation_average_scores IS '属性別平均スコア';
```

---

## 3. Elasticsearch Index (Read Model)

### recipes_index

```json
{
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 1,
    "analysis": {
      "analyzer": {
        "recipe_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "recipe_synonyms"]
        },
        "ja_analyzer": {
          "type": "custom",
          "tokenizer": "kuromoji_tokenizer",
          "filter": ["kuromoji_baseform", "lowercase"]
        }
      },
      "filter": {
        "recipe_synonyms": {
          "type": "synonym",
          "synonyms": [
            "ビール,beer",
            "発泡酒,happoshu",
            "ノンアル,non_alcohol,ノンアルコール"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "recipe_id": { "type": "keyword" },
      "recipe_code": { "type": "keyword" },
      "name": {
        "type": "text",
        "analyzer": "ja_analyzer",
        "fields": {
          "keyword": { "type": "keyword" },
          "suggest": {
            "type": "completion",
            "analyzer": "simple"
          }
        }
      },
      "product_type": { "type": "keyword" },
      "status": { "type": "keyword" },
      "version": {
        "type": "object",
        "properties": {
          "major": { "type": "integer" },
          "minor": { "type": "integer" },
          "patch": { "type": "integer" },
          "display": { "type": "keyword" }
        }
      },
      "concept": {
        "type": "object",
        "properties": {
          "description": { "type": "text", "analyzer": "ja_analyzer" },
          "target_consumer": { "type": "text" },
          "positioning": { "type": "text" },
          "key_features": { "type": "keyword" },
          "brand_id": { "type": "keyword" }
        }
      },
      "ingredients": {
        "type": "nested",
        "properties": {
          "ingredient_type": { "type": "keyword" },
          "name": { "type": "text" },
          "ratio": { "type": "float" }
        }
      },
      "target_profile": {
        "type": "object",
        "properties": {
          "target_alcohol": { "type": "float" },
          "target_bitterness": { "type": "float" },
          "target_color": { "type": "float" }
        }
      },
      "quality_spec": {
        "type": "object",
        "properties": {
          "alcohol_range": { "type": "float_range" },
          "bitterness_range": { "type": "float_range" }
        }
      },
      "fermentation": {
        "type": "object",
        "properties": {
          "yeast_strain_id": { "type": "keyword" },
          "yeast_strain_name": { "type": "text" }
        }
      },
      "created_at": { "type": "date" },
      "updated_at": { "type": "date" },
      "approved_at": { "type": "date" },
      "created_by": { "type": "keyword" },
      "approved_by": { "type": "keyword" }
    }
  }
}
```

### evaluations_index

```json
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1
  },
  "mappings": {
    "properties": {
      "evaluation_id": { "type": "keyword" },
      "evaluation_type": { "type": "keyword" },
      "recipe_id": { "type": "keyword" },
      "recipe_name": { "type": "text" },
      "evaluation_date": { "type": "date" },
      "status": { "type": "keyword" },
      "panelist_count": { "type": "integer" },
      "results": {
        "type": "object",
        "properties": {
          "overall_score": { "type": "float" },
          "panel_consensus": { "type": "keyword" },
          "recommendation": { "type": "text" }
        }
      },
      "scores": {
        "type": "nested",
        "properties": {
          "attribute": { "type": "keyword" },
          "average": { "type": "float" },
          "std_dev": { "type": "float" }
        }
      }
    }
  }
}
```

---

## 4. Views

### recipe_summary_view

```sql
CREATE VIEW recipe_summary_view AS
SELECT
    r.recipe_id,
    r.recipe_code,
    r.name,
    r.product_type,
    CONCAT('v', r.version_major, '.', r.version_minor, '.', r.version_patch) AS version_display,
    r.status,
    r.created_at,
    r.approved_at,
    rc.description AS concept_description,
    rc.brand_id,
    COUNT(DISTINCT ri.ingredient_id) AS ingredient_count,
    rtp.target_alcohol,
    rtp.target_bitterness,
    (SELECT COUNT(*) FROM sensory_evaluations se WHERE se.recipe_id = r.recipe_id) AS evaluation_count
FROM recipes r
LEFT JOIN recipe_concepts rc ON r.recipe_id = rc.recipe_id
LEFT JOIN recipe_ingredients ri ON r.recipe_id = ri.recipe_id
LEFT JOIN recipe_target_profiles rtp ON r.recipe_id = rtp.recipe_id
GROUP BY r.recipe_id, r.recipe_code, r.name, r.product_type,
         r.version_major, r.version_minor, r.version_patch,
         r.status, r.created_at, r.approved_at,
         rc.description, rc.brand_id,
         rtp.target_alcohol, rtp.target_bitterness;

COMMENT ON VIEW recipe_summary_view IS '処方サマリービュー';
```

### evaluation_summary_view

```sql
CREATE VIEW evaluation_summary_view AS
SELECT
    se.evaluation_id,
    se.evaluation_type,
    se.recipe_id,
    r.name AS recipe_name,
    r.recipe_code,
    se.evaluation_date,
    se.status,
    COUNT(DISTINCT ep.panelist_id) AS panelist_count,
    er.overall_score,
    er.panel_consensus,
    er.recommendation
FROM sensory_evaluations se
JOIN recipes r ON se.recipe_id = r.recipe_id
LEFT JOIN evaluation_panelists ep ON se.evaluation_id = ep.evaluation_id
LEFT JOIN evaluation_results er ON se.evaluation_id = er.evaluation_id
GROUP BY se.evaluation_id, se.evaluation_type, se.recipe_id,
         r.name, r.recipe_code, se.evaluation_date, se.status,
         er.overall_score, er.panel_consensus, er.recommendation;

COMMENT ON VIEW evaluation_summary_view IS '官能評価サマリービュー';
```

---

## 5. Functions & Triggers

### 処方コード自動生成

```sql
CREATE OR REPLACE FUNCTION generate_recipe_code()
RETURNS TRIGGER AS $$
DECLARE
    type_code VARCHAR(10);
    year_month VARCHAR(6);
    seq_num INTEGER;
BEGIN
    IF NEW.recipe_code IS NULL THEN
        type_code := UPPER(NEW.product_type);
        year_month := TO_CHAR(NOW(), 'YYYYMM');

        SELECT COALESCE(MAX(CAST(SUBSTRING(recipe_code FROM '.*-(\d{3})$') AS INTEGER)), 0) + 1
        INTO seq_num
        FROM recipes
        WHERE recipe_code LIKE 'RCP-' || type_code || '-' || year_month || '-%';

        NEW.recipe_code := 'RCP-' || type_code || '-' || year_month || '-' || LPAD(seq_num::TEXT, 3, '0');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_recipe_code_gen
    BEFORE INSERT ON recipes
    FOR EACH ROW EXECUTE FUNCTION generate_recipe_code();
```

### 原料比率合計チェック

```sql
CREATE OR REPLACE FUNCTION check_ingredient_ratio()
RETURNS TRIGGER AS $$
DECLARE
    total_ratio DECIMAL(6,2);
BEGIN
    SELECT COALESCE(SUM(ratio), 0) INTO total_ratio
    FROM recipe_ingredients
    WHERE recipe_id = NEW.recipe_id AND ingredient_id != NEW.ingredient_id;

    total_ratio := total_ratio + NEW.ratio;

    IF total_ratio > 100 THEN
        RAISE EXCEPTION 'Total ingredient ratio cannot exceed 100%% (current: %%)', total_ratio;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_ratio
    BEFORE INSERT OR UPDATE ON recipe_ingredients
    FOR EACH ROW EXECUTE FUNCTION check_ingredient_ratio();
```

### 評価結果自動計算

```sql
CREATE OR REPLACE FUNCTION calculate_evaluation_results()
RETURNS TRIGGER AS $$
DECLARE
    avg_scores RECORD;
    overall DECIMAL(3,1);
    consensus VARCHAR(10);
    max_std_dev DECIMAL(4,2);
BEGIN
    -- 全体平均スコア計算
    SELECT AVG(score) INTO overall
    FROM panelist_scores
    WHERE evaluation_id = NEW.evaluation_id;

    -- 最大標準偏差でコンセンサス判定
    SELECT MAX(std_deviation) INTO max_std_dev
    FROM evaluation_average_scores
    WHERE evaluation_id = NEW.evaluation_id;

    IF max_std_dev < 0.5 THEN
        consensus := 'high';
    ELSIF max_std_dev < 1.0 THEN
        consensus := 'medium';
    ELSE
        consensus := 'low';
    END IF;

    -- 結果を更新または挿入
    INSERT INTO evaluation_results (evaluation_id, overall_score, panel_consensus, calculated_at)
    VALUES (NEW.evaluation_id, overall, consensus, NOW())
    ON CONFLICT (evaluation_id) DO UPDATE
    SET overall_score = overall,
        panel_consensus = consensus,
        calculated_at = NOW();

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

---

## 6. CDC (Change Data Capture) 設定

### Debezium Connector設定

```json
{
  "name": "recipe-postgres-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres-recipe",
    "database.port": "5432",
    "database.user": "debezium",
    "database.password": "${secrets:postgres-password}",
    "database.dbname": "recipe_db",
    "database.server.name": "recipe",
    "table.include.list": "public.recipes,public.recipe_concepts,public.recipe_ingredients,public.sensory_evaluations,public.evaluation_results",
    "plugin.name": "pgoutput",
    "slot.name": "recipe_slot",
    "publication.name": "recipe_publication",
    "transforms": "route",
    "transforms.route.type": "org.apache.kafka.connect.transforms.RegexRouter",
    "transforms.route.regex": "([^.]+)\\.([^.]+)\\.([^.]+)",
    "transforms.route.replacement": "recipe-cdc.$3"
  }
}
```

### Elasticsearch Sink設定

```json
{
  "name": "recipe-elasticsearch-sink",
  "config": {
    "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
    "topics": "recipe-cdc.recipes",
    "connection.url": "http://elasticsearch:9200",
    "type.name": "_doc",
    "key.ignore": "false",
    "schema.ignore": "true",
    "behavior.on.null.values": "delete",
    "transforms": "flatten",
    "transforms.flatten.type": "org.apache.kafka.connect.transforms.Flatten$Value"
  }
}
```

---

## 7. Migration Strategy

### マイグレーションファイル

```
V001__create_recipes_tables.sql
V002__create_quality_standards_tables.sql
V003__create_sensory_evaluation_tables.sql
V004__create_views.sql
V005__create_functions_triggers.sql
V006__create_indexes.sql
V007__insert_master_data.sql
```

### 初期マスタデータ

```sql
-- V007__insert_master_data.sql

-- サンプル処方
INSERT INTO recipes (name, product_type, status) VALUES
('Asahi Super Dry', 'beer', 'production'),
('Asahi Super Dry Draft', 'beer', 'production'),
('Clear Asahi', 'happoshu', 'production'),
('Dry Zero', 'non_alcohol', 'production');
```

---

## 8. Data Retention & Backup

### データ保持ポリシー

| データ種別 | 保持期間 | 処理 |
|-----------|---------|------|
| 処方マスタ | 永続 | アーカイブステータスで論理削除 |
| 品質基準 | 10年 | expired後10年で物理削除 |
| 官能評価 | 5年 | 完了後5年で物理削除 |
| パネリストスコア | 3年 | 評価完了後3年で匿名化 |

### バックアップ戦略

```yaml
PostgreSQL:
  Full Backup: Daily at 03:00
  Retention: 30 days
  Point-in-time Recovery: 7 days

Elasticsearch:
  Snapshot: Daily at 04:00
  Retention: 14 days
  Repository: S3
```

---

**作成日**: 2025-11-28
**VS**: VS2 製品開発
**BC**: BC2 Product Recipe
**次BC**: BC3 Brand Portfolio
