# BC4: Research Innovation - データベース設計

## 概要

研究イノベーション管理のデータベース設計。産学連携、セレンディピティエンジン、研究ポートフォリオの永続化。

**データベース**: PostgreSQL 15+
**グラフDB**: Neo4j（知識グラフ用）
**技術スタック**: Python/SQLAlchemy

---

## PostgreSQL スキーマ

### 産学連携テーブル

```sql
-- 連携パートナー
CREATE TABLE research_partners (
    partner_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    partner_type VARCHAR(50) NOT NULL,  -- UNIVERSITY, RESEARCH_INSTITUTE, CORPORATE, GOVERNMENT
    expertise_areas JSONB DEFAULT '[]',
    location JSONB,
    contact_info JSONB,
    reputation_score DECIMAL(3,2),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_partners_type ON research_partners(partner_type);
CREATE INDEX idx_partners_expertise ON research_partners USING GIN(expertise_areas);

-- 連携プロジェクト
CREATE TABLE collaborations (
    collaboration_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    partner_id UUID NOT NULL REFERENCES research_partners(partner_id),
    title VARCHAR(300) NOT NULL,
    description TEXT,
    objectives JSONB DEFAULT '[]',
    scope JSONB,
    start_date DATE,
    end_date DATE,
    budget DECIMAL(15,2),
    status VARCHAR(50) NOT NULL DEFAULT 'PROPOSED',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT valid_status CHECK (status IN (
        'PROPOSED', 'NEGOTIATING', 'ACTIVE', 'ON_HOLD', 'COMPLETED', 'TERMINATED'
    ))
);

CREATE INDEX idx_collab_partner ON collaborations(partner_id);
CREATE INDEX idx_collab_status ON collaborations(status);
CREATE INDEX idx_collab_dates ON collaborations(start_date, end_date);

-- 契約・合意
CREATE TABLE agreements (
    agreement_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    collaboration_id UUID NOT NULL REFERENCES collaborations(collaboration_id),
    agreement_type VARCHAR(50) NOT NULL,  -- NDA, MOU, CONTRACT, AMENDMENT
    terms JSONB NOT NULL,
    ip_ownership VARCHAR(50),  -- JOINT, PARTNER, ASAHI
    effective_date DATE NOT NULL,
    expiry_date DATE,
    signed_at TIMESTAMPTZ,
    document_url VARCHAR(500),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- マイルストーン
CREATE TABLE milestones (
    milestone_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    collaboration_id UUID NOT NULL REFERENCES collaborations(collaboration_id),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    target_date DATE NOT NULL,
    completed_date DATE,
    progress_percentage INT DEFAULT 0 CHECK (progress_percentage BETWEEN 0 AND 100),
    deliverables JSONB DEFAULT '[]',
    status VARCHAR(50) DEFAULT 'PENDING',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_milestone_collab ON milestones(collaboration_id);
CREATE INDEX idx_milestone_status ON milestones(status);

-- 研究成果
CREATE TABLE research_outcomes (
    outcome_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    collaboration_id UUID NOT NULL REFERENCES collaborations(collaboration_id),
    outcome_type VARCHAR(50) NOT NULL,  -- PATENT, PAPER, TECHNOLOGY, DATA, PROTOTYPE
    title VARCHAR(300) NOT NULL,
    description TEXT,
    ip_status VARCHAR(50),
    commercialization_potential VARCHAR(50),
    publication_date DATE,
    external_references JSONB DEFAULT '[]',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_outcome_collab ON research_outcomes(collaboration_id);
CREATE INDEX idx_outcome_type ON research_outcomes(outcome_type);
```

### 研究ポートフォリオテーブル

```sql
-- 研究テーマ
CREATE TABLE research_themes (
    theme_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,  -- BASIC, APPLIED, DEVELOPMENT
    risk_level VARCHAR(50) NOT NULL,  -- LOW, MEDIUM, HIGH, EXPERIMENTAL
    expected_roi DECIMAL(5,2),
    timeline_months INT,
    status VARCHAR(50) DEFAULT 'PLANNING',
    parent_theme_id UUID REFERENCES research_themes(theme_id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_theme_category ON research_themes(category);
CREATE INDEX idx_theme_risk ON research_themes(risk_level);
CREATE INDEX idx_theme_status ON research_themes(status);

-- リソース配分
CREATE TABLE resource_allocations (
    allocation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    theme_id UUID NOT NULL REFERENCES research_themes(theme_id),
    fiscal_year INT NOT NULL,
    budget_percentage DECIMAL(5,2) NOT NULL CHECK (budget_percentage BETWEEN 0 AND 100),
    budget_amount DECIMAL(15,2),
    headcount INT DEFAULT 0,
    equipment_hours DECIMAL(10,2) DEFAULT 0,
    priority INT DEFAULT 5 CHECK (priority BETWEEN 1 AND 10),
    effective_from DATE NOT NULL,
    effective_to DATE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(theme_id, fiscal_year)
);

CREATE INDEX idx_allocation_theme ON resource_allocations(theme_id);
CREATE INDEX idx_allocation_year ON resource_allocations(fiscal_year);

-- ポートフォリオスナップショット
CREATE TABLE portfolio_snapshots (
    snapshot_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    snapshot_date DATE NOT NULL,
    allocations JSONB NOT NULL,
    risk_profile JSONB NOT NULL,
    performance_metrics JSONB,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_snapshot_date ON portfolio_snapshots(snapshot_date);

-- リバランス履歴
CREATE TABLE rebalance_events (
    rebalance_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    strategy VARCHAR(50) NOT NULL,
    before_allocation JSONB NOT NULL,
    after_allocation JSONB NOT NULL,
    changes JSONB NOT NULL,
    rationale TEXT,
    approved_by VARCHAR(100),
    executed_at TIMESTAMPTZ DEFAULT NOW()
);
```

### セレンディピティ関連（補助テーブル）

```sql
-- 発見セッション
CREATE TABLE discovery_sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    focus_areas JSONB NOT NULL,
    exploration_mode VARCHAR(50) NOT NULL,
    participants JSONB DEFAULT '[]',
    insights_generated INT DEFAULT 0,
    connections_discovered INT DEFAULT 0,
    session_start TIMESTAMPTZ NOT NULL,
    session_end TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 洞察記録
CREATE TABLE serendipity_insights (
    insight_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES discovery_sessions(session_id),
    source_connections JSONB NOT NULL,
    description TEXT NOT NULL,
    novelty_score DECIMAL(3,2),
    feasibility_score DECIMAL(3,2),
    potential_impact VARCHAR(50),
    validation_status VARCHAR(50) DEFAULT 'PENDING',
    validated_by VARCHAR(100),
    validated_at TIMESTAMPTZ,
    potential_applications JSONB DEFAULT '[]',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_insight_session ON serendipity_insights(session_id);
CREATE INDEX idx_insight_status ON serendipity_insights(validation_status);
CREATE INDEX idx_insight_impact ON serendipity_insights(potential_impact);
```

---

## Neo4j 知識グラフスキーマ

### ノードタイプ

```cypher
// 知識ノード
(:KnowledgeNode {
  node_id: string,
  domain: string,
  concept: string,
  keywords: [string],
  source: string,
  relevance_score: float,
  created_at: datetime
})

// 分野ノード
(:Domain {
  name: string,
  description: string,
  parent_domain: string
})

// 研究者ノード
(:Researcher {
  researcher_id: string,
  name: string,
  expertise: [string]
})
```

### リレーションシップタイプ

```cypher
// 知識ノード間の関連
(:KnowledgeNode)-[:CONNECTS_TO {
  connection_type: string,  // ANALOGY, CONTRAST, COMPLEMENT, HYBRID
  strength: float,
  discovered_at: datetime,
  discovered_by: string,
  validated: boolean
}]->(:KnowledgeNode)

// 分野への所属
(:KnowledgeNode)-[:BELONGS_TO]->(:Domain)

// 発見者
(:Researcher)-[:DISCOVERED]->(:KnowledgeNode)

// 分野階層
(:Domain)-[:PARENT_OF]->(:Domain)
```

### インデックス

```cypher
CREATE INDEX knowledge_node_domain FOR (n:KnowledgeNode) ON (n.domain);
CREATE INDEX knowledge_node_concept FOR (n:KnowledgeNode) ON (n.concept);
CREATE FULLTEXT INDEX knowledge_keywords FOR (n:KnowledgeNode) ON EACH [n.concept, n.keywords];
```

### サンプルクエリ

```cypher
// 2ホップ以内の関連ノード探索
MATCH path = (start:KnowledgeNode {node_id: $node_id})-[r:CONNECTS_TO*1..2]-(related)
WHERE ALL(rel IN relationships(path) WHERE rel.strength >= $min_strength)
RETURN path, [rel IN relationships(path) | rel.strength] as strengths

// クロスドメイン発見
MATCH (n1:KnowledgeNode)-[:BELONGS_TO]->(d1:Domain),
      (n2:KnowledgeNode)-[:BELONGS_TO]->(d2:Domain)
WHERE d1 <> d2
  AND NOT (n1)-[:CONNECTS_TO]-(n2)
  AND n1.relevance_score > 0.5
  AND n2.relevance_score > 0.5
RETURN n1, n2, d1.name as domain1, d2.name as domain2
LIMIT 20

// セレンディピティパス発見
MATCH path = shortestPath((n1:KnowledgeNode)-[:CONNECTS_TO*..5]-(n2:KnowledgeNode))
WHERE n1.domain <> n2.domain
  AND n1.node_id = $source_id
RETURN path, length(path) as path_length
ORDER BY path_length
LIMIT 10
```

---

## データ移行・同期

### PostgreSQL → Neo4j 同期

```python
# 知識ノードの同期（定期バッチ）
async def sync_knowledge_nodes():
    """PostgreSQLの補助データをNeo4jに同期"""
    # 新規ノードの同期
    new_nodes = await pg_conn.fetch("""
        SELECT * FROM knowledge_node_staging
        WHERE synced_at IS NULL
    """)

    for node in new_nodes:
        await neo4j_session.run("""
            MERGE (n:KnowledgeNode {node_id: $node_id})
            SET n.domain = $domain,
                n.concept = $concept,
                n.keywords = $keywords,
                n.relevance_score = $relevance_score
        """, node)
```

---

## バックアップ戦略

| データベース | バックアップ頻度 | 保持期間 |
|-------------|----------------|---------|
| PostgreSQL | 日次フル + 継続WAL | 90日 |
| Neo4j | 日次フル | 30日 |

---

## パフォーマンス考慮

1. **PostgreSQL**:
   - 連携プロジェクトは数百〜数千件規模
   - GINインデックスでJSONB検索を高速化

2. **Neo4j**:
   - 知識ノードは数万件規模を想定
   - 関連性探索は深度制限（最大5ホップ）
   - メモリ設定: heap 4GB推奨
