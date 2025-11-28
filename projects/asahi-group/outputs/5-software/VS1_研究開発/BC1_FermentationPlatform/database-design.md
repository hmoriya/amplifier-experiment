# BC1: Fermentation Platform - データベース設計

## 概要

| 項目 | 内容 |
|------|------|
| VS | VS1 研究開発 |
| BC | Fermentation Platform |
| Primary DB | PostgreSQL 15+ |
| Event Store | PostgreSQL (Event Sourcing) |
| Time Series | TimescaleDB |
| 外部連携 | Lab LIMS (Adapter) |

---

## 1. データベース構成

```
┌─────────────────────────────────────────────────────────────┐
│                  BC1: Fermentation Platform                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  PostgreSQL  │  │ Event Store  │  │ TimescaleDB  │      │
│  │   (Master)   │  │  (History)   │  │ (時系列)      │      │
│  │              │  │              │  │              │      │
│  │ • yeast_     │  │ • domain_    │  │ • measure    │      │
│  │   strains    │  │   events     │  │   ments_ts   │      │
│  │ • processes  │  │ • snapshots  │  │              │      │
│  │ • experiments│  │              │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. PostgreSQL Tables

### 2.1 酵母株関連

#### yeast_strains（酵母株マスタ）

```sql
CREATE TABLE yeast_strains (
    strain_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    strain_code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'research',
    registered_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    registered_by UUID,
    version INTEGER NOT NULL DEFAULT 1,

    CONSTRAINT chk_strain_code CHECK (strain_code ~ '^ASH-\d{4}-\d{4}$'),
    CONSTRAINT chk_status CHECK (status IN ('research', 'validated', 'production', 'archived')),
    CONSTRAINT chk_name_length CHECK (LENGTH(name) >= 1 AND LENGTH(name) <= 100)
);

CREATE INDEX idx_strains_status ON yeast_strains(status);
CREATE INDEX idx_strains_code ON yeast_strains(strain_code);
CREATE INDEX idx_strains_name ON yeast_strains USING gin(to_tsvector('simple', name));
CREATE INDEX idx_strains_registered ON yeast_strains(registered_at DESC);

COMMENT ON TABLE yeast_strains IS '酵母株マスタテーブル';
COMMENT ON COLUMN yeast_strains.strain_code IS '管理コード（ASH-YYYY-NNNN形式）';
COMMENT ON COLUMN yeast_strains.status IS 'ステータス: research/validated/production/archived';
```

#### strain_origins（酵母株由来）

```sql
CREATE TABLE strain_origins (
    origin_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    strain_id UUID NOT NULL REFERENCES yeast_strains(strain_id) ON DELETE CASCADE,
    source VARCHAR(20) NOT NULL,
    location VARCHAR(200),
    collected_at DATE,
    notes TEXT,

    CONSTRAINT chk_source CHECK (source IN ('natural', 'bred', 'modified', 'acquired'))
);

CREATE INDEX idx_origins_strain ON strain_origins(strain_id);

COMMENT ON TABLE strain_origins IS '酵母株の由来情報';
```

#### strain_parent_relations（親株関係）

```sql
CREATE TABLE strain_parent_relations (
    strain_id UUID NOT NULL REFERENCES yeast_strains(strain_id) ON DELETE CASCADE,
    parent_strain_id UUID NOT NULL REFERENCES yeast_strains(strain_id),
    relation_type VARCHAR(20) NOT NULL DEFAULT 'parent',

    PRIMARY KEY (strain_id, parent_strain_id),
    CONSTRAINT chk_no_self_ref CHECK (strain_id != parent_strain_id)
);

CREATE INDEX idx_parent_relations_parent ON strain_parent_relations(parent_strain_id);

COMMENT ON TABLE strain_parent_relations IS '酵母株の親子関係';
```

#### strain_characteristics（酵母特性）

```sql
CREATE TABLE strain_characteristics (
    characteristic_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    strain_id UUID NOT NULL REFERENCES yeast_strains(strain_id) ON DELETE CASCADE,
    alcohol_tolerance DECIMAL(5,2),
    temp_min DECIMAL(4,1),
    temp_max DECIMAL(4,1),
    flocculation_level VARCHAR(10),
    attenuation_min DECIMAL(5,2),
    attenuation_max DECIMAL(5,2),
    oxygen_requirement VARCHAR(10),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_flocculation CHECK (flocculation_level IN ('low', 'medium', 'high')),
    CONSTRAINT chk_oxygen CHECK (oxygen_requirement IN ('low', 'medium', 'high')),
    CONSTRAINT chk_temp_range CHECK (temp_min <= temp_max),
    CONSTRAINT chk_attenuation_range CHECK (attenuation_min <= attenuation_max)
);

CREATE UNIQUE INDEX idx_characteristics_strain ON strain_characteristics(strain_id);

COMMENT ON TABLE strain_characteristics IS '酵母株の発酵特性';
```

#### strain_flavor_profiles（風味プロファイル）

```sql
CREATE TABLE strain_flavor_profiles (
    profile_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    strain_id UUID NOT NULL REFERENCES yeast_strains(strain_id) ON DELETE CASCADE,
    ester_level VARCHAR(10),
    phenol_level VARCHAR(10),
    sulfur_level VARCHAR(10),
    fruitiness VARCHAR(10),
    spiciness VARCHAR(10),
    cleanness VARCHAR(10),
    notes TEXT[],
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_flavor_levels CHECK (
        ester_level IN ('none', 'very_low', 'low', 'medium', 'high', 'very_high') AND
        phenol_level IN ('none', 'very_low', 'low', 'medium', 'high', 'very_high') AND
        sulfur_level IN ('none', 'very_low', 'low', 'medium', 'high', 'very_high') AND
        fruitiness IN ('none', 'very_low', 'low', 'medium', 'high', 'very_high') AND
        spiciness IN ('none', 'very_low', 'low', 'medium', 'high', 'very_high') AND
        cleanness IN ('none', 'very_low', 'low', 'medium', 'high', 'very_high')
    )
);

CREATE UNIQUE INDEX idx_flavor_strain ON strain_flavor_profiles(strain_id);

COMMENT ON TABLE strain_flavor_profiles IS '酵母株の風味プロファイル';
```

#### strain_fermentation_profiles（発酵プロファイル）

```sql
CREATE TABLE strain_fermentation_profiles (
    profile_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    strain_id UUID NOT NULL REFERENCES yeast_strains(strain_id) ON DELETE CASCADE,
    optimal_temperature DECIMAL(4,1),
    fermentation_speed VARCHAR(10),
    duration_min_days INTEGER,
    duration_max_days INTEGER,
    co2_production VARCHAR(10),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_speed CHECK (fermentation_speed IN ('slow', 'medium', 'fast')),
    CONSTRAINT chk_co2 CHECK (co2_production IN ('low', 'medium', 'high')),
    CONSTRAINT chk_duration CHECK (duration_min_days <= duration_max_days)
);

CREATE UNIQUE INDEX idx_fermentation_strain ON strain_fermentation_profiles(strain_id);

COMMENT ON TABLE strain_fermentation_profiles IS '酵母株の発酵プロファイル';
```

### 2.2 発酵プロセス関連

#### fermentation_processes（発酵プロセス）

```sql
CREATE TABLE fermentation_processes (
    process_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    process_code VARCHAR(20) NOT NULL UNIQUE,
    strain_id UUID NOT NULL REFERENCES yeast_strains(strain_id),
    scale_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'planned',
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by UUID,
    version INTEGER NOT NULL DEFAULT 1,

    CONSTRAINT chk_process_code CHECK (process_code ~ '^FP-\d{8}-\d{3}$'),
    CONSTRAINT chk_scale CHECK (scale_type IN ('laboratory', 'pilot', 'production')),
    CONSTRAINT chk_process_status CHECK (status IN ('planned', 'in_progress', 'completed', 'aborted')),
    CONSTRAINT chk_dates CHECK (completed_at IS NULL OR completed_at >= started_at)
);

CREATE INDEX idx_processes_strain ON fermentation_processes(strain_id);
CREATE INDEX idx_processes_status ON fermentation_processes(status);
CREATE INDEX idx_processes_started ON fermentation_processes(started_at DESC);
CREATE INDEX idx_processes_code ON fermentation_processes(process_code);

COMMENT ON TABLE fermentation_processes IS '発酵プロセス管理';
```

#### fermentation_conditions（発酵条件）

```sql
CREATE TABLE fermentation_conditions (
    condition_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    process_id UUID NOT NULL REFERENCES fermentation_processes(process_id) ON DELETE CASCADE,
    temperature DECIMAL(5,2),
    pressure DECIMAL(6,2),
    dissolved_oxygen DECIMAL(6,3),
    pitch_rate DECIMAL(10,2),
    wort_gravity DECIMAL(6,4),
    effective_from TIMESTAMP NOT NULL DEFAULT NOW(),
    reason VARCHAR(500),

    CONSTRAINT chk_gravity CHECK (wort_gravity BETWEEN 0.990 AND 1.200)
);

CREATE INDEX idx_conditions_process ON fermentation_conditions(process_id, effective_from DESC);

COMMENT ON TABLE fermentation_conditions IS '発酵条件履歴';
```

#### fermentation_stages（発酵ステージ）

```sql
CREATE TABLE fermentation_stages (
    stage_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    process_id UUID NOT NULL REFERENCES fermentation_processes(process_id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    sequence_order INTEGER NOT NULL,
    target_temperature DECIMAL(5,2),
    target_duration_hours INTEGER,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    started_at TIMESTAMP,
    completed_at TIMESTAMP,

    CONSTRAINT chk_stage_status CHECK (status IN ('pending', 'active', 'completed')),
    UNIQUE (process_id, sequence_order)
);

CREATE INDEX idx_stages_process ON fermentation_stages(process_id, sequence_order);

COMMENT ON TABLE fermentation_stages IS '発酵ステージ定義';
```

### 2.3 研究実験関連

#### research_experiments（研究実験）

```sql
CREATE TABLE research_experiments (
    experiment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    experiment_code VARCHAR(20) NOT NULL UNIQUE,
    title VARCHAR(200) NOT NULL,
    hypothesis TEXT NOT NULL,
    methodology_type VARCHAR(20) NOT NULL,
    methodology_description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'planned',
    conducted_by UUID,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_exp_code CHECK (experiment_code ~ '^EXP-\d{4}-\d{4}$'),
    CONSTRAINT chk_methodology CHECK (methodology_type IN ('comparative', 'factorial', 'optimization', 'exploratory')),
    CONSTRAINT chk_exp_status CHECK (status IN ('planned', 'in_progress', 'completed'))
);

CREATE INDEX idx_experiments_status ON research_experiments(status);
CREATE INDEX idx_experiments_researcher ON research_experiments(conducted_by);
CREATE INDEX idx_experiments_title ON research_experiments USING gin(to_tsvector('simple', title));

COMMENT ON TABLE research_experiments IS '研究実験管理';
```

#### experiment_strains（実験使用酵母株）

```sql
CREATE TABLE experiment_strains (
    experiment_id UUID NOT NULL REFERENCES research_experiments(experiment_id) ON DELETE CASCADE,
    strain_id UUID NOT NULL REFERENCES yeast_strains(strain_id),
    role VARCHAR(50),

    PRIMARY KEY (experiment_id, strain_id)
);

CREATE INDEX idx_exp_strains_strain ON experiment_strains(strain_id);

COMMENT ON TABLE experiment_strains IS '実験に使用する酵母株';
```

#### experiment_variables（実験変数）

```sql
CREATE TABLE experiment_variables (
    variable_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    experiment_id UUID NOT NULL REFERENCES research_experiments(experiment_id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    variable_type VARCHAR(20) NOT NULL,
    unit VARCHAR(50),
    range_min DECIMAL(15,5),
    range_max DECIMAL(15,5),

    CONSTRAINT chk_var_type CHECK (variable_type IN ('independent', 'dependent', 'controlled'))
);

CREATE INDEX idx_variables_experiment ON experiment_variables(experiment_id);

COMMENT ON TABLE experiment_variables IS '実験変数定義';
```

#### experiment_results（実験結果）

```sql
CREATE TABLE experiment_results (
    result_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    experiment_id UUID NOT NULL REFERENCES research_experiments(experiment_id) ON DELETE CASCADE,
    summary TEXT,
    conclusion TEXT,
    recorded_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_results_experiment ON experiment_results(experiment_id);

COMMENT ON TABLE experiment_results IS '実験結果サマリー';
```

#### research_findings（研究発見事項）

```sql
CREATE TABLE research_findings (
    finding_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    experiment_id UUID NOT NULL REFERENCES research_experiments(experiment_id) ON DELETE CASCADE,
    finding_type VARCHAR(20) NOT NULL,
    description TEXT NOT NULL,
    significance VARCHAR(20) NOT NULL,
    application_potential TEXT[],
    discovered_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_finding_type CHECK (finding_type IN ('expected', 'unexpected', 'serendipitous')),
    CONSTRAINT chk_significance CHECK (significance IN ('low', 'medium', 'high', 'breakthrough'))
);

CREATE INDEX idx_findings_experiment ON research_findings(experiment_id);
CREATE INDEX idx_findings_significance ON research_findings(significance);
CREATE INDEX idx_findings_description ON research_findings USING gin(to_tsvector('simple', description));

COMMENT ON TABLE research_findings IS '研究発見事項';
```

---

## 3. Event Store Tables

### domain_events（ドメインイベント）

```sql
CREATE TABLE domain_events (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_type VARCHAR(50) NOT NULL,
    aggregate_id UUID NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB NOT NULL,
    metadata JSONB,
    version INTEGER NOT NULL,
    occurred_at TIMESTAMP NOT NULL DEFAULT NOW(),

    UNIQUE (aggregate_id, version)
);

CREATE INDEX idx_events_aggregate ON domain_events(aggregate_type, aggregate_id, version);
CREATE INDEX idx_events_type ON domain_events(event_type);
CREATE INDEX idx_events_occurred ON domain_events(occurred_at DESC);
CREATE INDEX idx_events_data ON domain_events USING gin(event_data);

COMMENT ON TABLE domain_events IS 'Event Sourcing用ドメインイベントストア';
```

### aggregate_snapshots（集約スナップショット）

```sql
CREATE TABLE aggregate_snapshots (
    snapshot_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_type VARCHAR(50) NOT NULL,
    aggregate_id UUID NOT NULL,
    snapshot_data JSONB NOT NULL,
    version INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    UNIQUE (aggregate_type, aggregate_id, version)
);

CREATE INDEX idx_snapshots_aggregate ON aggregate_snapshots(aggregate_type, aggregate_id, version DESC);

COMMENT ON TABLE aggregate_snapshots IS '集約の状態スナップショット';
```

### outbox_events（アウトボックス）

```sql
CREATE TABLE outbox_events (
    outbox_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type VARCHAR(100) NOT NULL,
    topic VARCHAR(200) NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    published_at TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    retry_count INTEGER NOT NULL DEFAULT 0,

    CONSTRAINT chk_outbox_status CHECK (status IN ('pending', 'published', 'failed'))
);

CREATE INDEX idx_outbox_status ON outbox_events(status, created_at) WHERE status = 'pending';
CREATE INDEX idx_outbox_published ON outbox_events(published_at DESC) WHERE status = 'published';

COMMENT ON TABLE outbox_events IS 'イベント発行用アウトボックスパターン';
```

---

## 4. TimescaleDB Tables（時系列データ）

### process_measurements（発酵測定データ）

```sql
-- TimescaleDB拡張が必要
CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE process_measurements (
    measurement_id UUID DEFAULT gen_random_uuid(),
    process_id UUID NOT NULL,
    measured_at TIMESTAMPTZ NOT NULL,
    temperature DECIMAL(5,2),
    ph DECIMAL(4,2),
    gravity DECIMAL(6,4),
    cell_count DECIMAL(12,2),
    dissolved_oxygen DECIMAL(6,3),
    notes TEXT,

    PRIMARY KEY (process_id, measured_at)
);

-- ハイパーテーブル化（時系列最適化）
SELECT create_hypertable('process_measurements', 'measured_at');

-- 圧縮ポリシー（30日以上古いデータを圧縮）
ALTER TABLE process_measurements SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'process_id'
);

SELECT add_compression_policy('process_measurements', INTERVAL '30 days');

-- データ保持ポリシー（2年以上古いデータを削除）
SELECT add_retention_policy('process_measurements', INTERVAL '2 years');

CREATE INDEX idx_measurements_process_time ON process_measurements(process_id, measured_at DESC);

COMMENT ON TABLE process_measurements IS '発酵プロセス測定データ（TimescaleDB）';
```

---

## 5. Views

### active_strains_view

```sql
CREATE VIEW active_strains_view AS
SELECT
    s.strain_id,
    s.strain_code,
    s.name,
    s.status,
    sc.alcohol_tolerance,
    sc.flocculation_level,
    fp.ester_level,
    fp.fruitiness,
    fp.cleanness,
    COUNT(DISTINCT p.process_id) AS process_count,
    MAX(p.started_at) AS last_used_at
FROM yeast_strains s
LEFT JOIN strain_characteristics sc ON s.strain_id = sc.strain_id
LEFT JOIN strain_flavor_profiles fp ON s.strain_id = fp.strain_id
LEFT JOIN fermentation_processes p ON s.strain_id = p.strain_id
WHERE s.status IN ('validated', 'production')
GROUP BY s.strain_id, s.strain_code, s.name, s.status,
         sc.alcohol_tolerance, sc.flocculation_level,
         fp.ester_level, fp.fruitiness, fp.cleanness;

COMMENT ON VIEW active_strains_view IS '利用可能な酵母株一覧';
```

### process_summary_view

```sql
CREATE VIEW process_summary_view AS
SELECT
    p.process_id,
    p.process_code,
    p.scale_type,
    p.status,
    p.started_at,
    p.completed_at,
    s.strain_code,
    s.name AS strain_name,
    fc.temperature AS current_temperature,
    (SELECT COUNT(*) FROM process_measurements pm WHERE pm.process_id = p.process_id) AS measurement_count,
    EXTRACT(EPOCH FROM (COALESCE(p.completed_at, NOW()) - p.started_at))/3600 AS duration_hours
FROM fermentation_processes p
JOIN yeast_strains s ON p.strain_id = s.strain_id
LEFT JOIN LATERAL (
    SELECT * FROM fermentation_conditions fc2
    WHERE fc2.process_id = p.process_id
    ORDER BY fc2.effective_from DESC
    LIMIT 1
) fc ON true;

COMMENT ON VIEW process_summary_view IS '発酵プロセスサマリー';
```

### findings_search_view

```sql
CREATE VIEW findings_search_view AS
SELECT
    f.finding_id,
    f.finding_type,
    f.description,
    f.significance,
    f.application_potential,
    f.discovered_at,
    e.experiment_code,
    e.title AS experiment_title,
    array_agg(DISTINCT s.name) AS strain_names
FROM research_findings f
JOIN research_experiments e ON f.experiment_id = e.experiment_id
LEFT JOIN experiment_strains es ON e.experiment_id = es.experiment_id
LEFT JOIN yeast_strains s ON es.strain_id = s.strain_id
GROUP BY f.finding_id, f.finding_type, f.description, f.significance,
         f.application_potential, f.discovered_at, e.experiment_code, e.title;

COMMENT ON VIEW findings_search_view IS '研究発見事項検索用ビュー';
```

---

## 6. Functions & Triggers

### 自動更新タイムスタンプ

```sql
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_strains_updated
    BEFORE UPDATE ON yeast_strains
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_characteristics_updated
    BEFORE UPDATE ON strain_characteristics
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

### 酵母株コード自動生成

```sql
CREATE OR REPLACE FUNCTION generate_strain_code()
RETURNS TRIGGER AS $$
DECLARE
    year_part VARCHAR(4);
    seq_num INTEGER;
BEGIN
    IF NEW.strain_code IS NULL THEN
        year_part := TO_CHAR(NOW(), 'YYYY');
        SELECT COALESCE(MAX(CAST(SUBSTRING(strain_code FROM 10 FOR 4) AS INTEGER)), 0) + 1
        INTO seq_num
        FROM yeast_strains
        WHERE strain_code LIKE 'ASH-' || year_part || '-%';

        NEW.strain_code := 'ASH-' || year_part || '-' || LPAD(seq_num::TEXT, 4, '0');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_strain_code_gen
    BEFORE INSERT ON yeast_strains
    FOR EACH ROW EXECUTE FUNCTION generate_strain_code();
```

### プロセスコード自動生成

```sql
CREATE OR REPLACE FUNCTION generate_process_code()
RETURNS TRIGGER AS $$
DECLARE
    date_part VARCHAR(8);
    seq_num INTEGER;
BEGIN
    IF NEW.process_code IS NULL THEN
        date_part := TO_CHAR(NOW(), 'YYYYMMDD');
        SELECT COALESCE(MAX(CAST(SUBSTRING(process_code FROM 13 FOR 3) AS INTEGER)), 0) + 1
        INTO seq_num
        FROM fermentation_processes
        WHERE process_code LIKE 'FP-' || date_part || '-%';

        NEW.process_code := 'FP-' || date_part || '-' || LPAD(seq_num::TEXT, 3, '0');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_process_code_gen
    BEFORE INSERT ON fermentation_processes
    FOR EACH ROW EXECUTE FUNCTION generate_process_code();
```

---

## 7. Migration Strategy

### 初期マイグレーション

```
V001__create_extensions.sql
V002__create_yeast_strains.sql
V003__create_strain_details.sql
V004__create_fermentation_processes.sql
V005__create_experiments.sql
V006__create_event_store.sql
V007__create_timescaledb_tables.sql
V008__create_views.sql
V009__create_functions_triggers.sql
V010__insert_initial_data.sql
```

### サンプルデータ

```sql
-- V010__insert_initial_data.sql

-- サンプル酵母株
INSERT INTO yeast_strains (strain_code, name, status) VALUES
('ASH-2024-0001', 'Asahi Premium Lager Yeast', 'production'),
('ASH-2024-0002', 'Super Dry Original Yeast', 'production'),
('ASH-2024-0003', 'Experimental Ale Yeast #1', 'research');

-- 特性データ
INSERT INTO strain_characteristics (strain_id, alcohol_tolerance, temp_min, temp_max, flocculation_level, attenuation_min, attenuation_max, oxygen_requirement)
SELECT strain_id, 12.0, 8.0, 14.0, 'high', 75.0, 82.0, 'medium'
FROM yeast_strains WHERE strain_code = 'ASH-2024-0001';
```

---

## 8. Data Retention & Backup

### データ保持ポリシー

| データ種別 | 保持期間 | 処理 |
|-----------|---------|------|
| 酵母株マスタ | 永続 | アーカイブステータスで論理削除 |
| 発酵プロセス | 10年 | 完了後10年で物理削除 |
| 測定データ | 2年 | TimescaleDB自動削除 |
| イベントストア | 5年 | 古いイベントは圧縮保存 |
| 研究発見事項 | 永続 | 重要な知的財産として保持 |

### バックアップ戦略

```yaml
Full Backup:
  Schedule: Daily at 02:00
  Retention: 30 days

Incremental Backup:
  Schedule: Every 4 hours
  Retention: 7 days

WAL Archive:
  Mode: Continuous
  Retention: 7 days

TimescaleDB:
  Compression: 30 days+
  Continuous Aggregate: 1 hour intervals
```

---

**作成日**: 2025-11-28
**VS**: VS1 研究開発
**BC**: BC1 Fermentation Platform
**次BC**: BC2 Product Recipe
