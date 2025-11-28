# BC4: Research Innovation - API仕様書

## 概要

研究イノベーション管理のREST API仕様。産学連携、セレンディピティエンジン、研究ポートフォリオ管理を提供。

**ベースURL**: `/api/v1/research-innovation`
**認証**: OAuth 2.0 Bearer Token
**技術スタック**: Python/FastAPI

---

## エンドポイント一覧

### 産学連携 (Collaborations)

#### POST /collaborations
新規連携プロジェクトの提案

```yaml
Request:
  Content-Type: application/json
  Body:
    partner_id: string (required)
    project:
      title: string (required)
      description: string
      objectives: array<string>
      duration_months: integer
      estimated_budget: number
    proposed_terms:
      ip_ownership: string  # JOINT | PARTNER | ASAHI
      confidentiality_level: string

Response: 201 Created
  Body:
    collaboration_id: string
    status: "PROPOSED"
    created_at: timestamp
```

#### GET /collaborations
連携プロジェクト一覧取得

```yaml
Query Parameters:
  status: string (optional)  # PROPOSED | NEGOTIATING | ACTIVE | COMPLETED
  partner_type: string (optional)
  page: integer (default: 1)
  limit: integer (default: 20)

Response: 200 OK
  Body:
    items: array<Collaboration>
    total: integer
    page: integer
```

#### GET /collaborations/{collaboration_id}
連携プロジェクト詳細取得

#### PATCH /collaborations/{collaboration_id}/milestones/{milestone_id}
マイルストーン進捗更新

```yaml
Request:
  Body:
    progress_percentage: integer (0-100)
    notes: string
    deliverables: array<string>

Response: 200 OK
```

#### POST /collaborations/{collaboration_id}/outcomes
成果物登録

```yaml
Request:
  Body:
    outcome_type: string  # PATENT | PAPER | TECHNOLOGY | DATA
    title: string
    description: string
    ip_status: string
    commercialization_potential: string

Response: 201 Created
```

---

### セレンディピティエンジン (Serendipity)

#### POST /serendipity/knowledge-nodes
知識ノード追加

```yaml
Request:
  Body:
    domain: string (required)
    concept: string (required)
    keywords: array<string>
    source: string
    metadata: object

Response: 201 Created
  Body:
    node_id: string
    relevance_score: number
```

#### GET /serendipity/connections
関連性探索

```yaml
Query Parameters:
  node_id: string (required)
  depth: integer (default: 2, max: 5)
  min_strength: number (default: 0.3)
  connection_types: array<string>

Response: 200 OK
  Body:
    connections: array<Connection>
    paths: array<Path>
```

#### POST /serendipity/discover
発見セッション実行

```yaml
Request:
  Body:
    focus_areas: array<string> (required)
    exploration_mode: string  # BROAD | FOCUSED | RANDOM
    max_insights: integer (default: 10)

Response: 200 OK
  Body:
    session_id: string
    insights: array<Insight>
    novel_connections: array<Connection>
```

#### POST /serendipity/insights/{insight_id}/validate
洞察の検証

```yaml
Request:
  Body:
    validation_result: string  # CONFIRMED | REJECTED | NEEDS_RESEARCH
    reviewer_notes: string
    potential_applications: array<string>

Response: 200 OK
```

---

### 研究ポートフォリオ (Portfolio)

#### GET /portfolio
現在のポートフォリオ取得

```yaml
Response: 200 OK
  Body:
    portfolio_id: string
    themes: array<ResearchTheme>
    allocations: array<Allocation>
    risk_profile:
      overall_risk: string
      risk_distribution: object
    performance:
      roi_ytd: number
      success_rate: number
```

#### POST /portfolio/themes
研究テーマ追加

```yaml
Request:
  Body:
    name: string (required)
    category: string  # BASIC | APPLIED | DEVELOPMENT
    risk_level: string
    expected_roi: number
    timeline_months: integer
    initial_budget: number

Response: 201 Created
```

#### PUT /portfolio/allocations
リソース配分更新

```yaml
Request:
  Body:
    allocations:
      - theme_id: string
        budget_percentage: number
        headcount: integer
        priority: integer

Response: 200 OK
  Body:
    updated_allocations: array
    warnings: array<string>  # 配分ルール違反の警告
```

#### POST /portfolio/simulate
シナリオシミュレーション

```yaml
Request:
  Body:
    scenario_name: string
    allocation_changes: array<AllocationChange>
    assumptions:
      market_growth: number
      success_probability_modifier: number

Response: 200 OK
  Body:
    scenario_id: string
    projected_outcomes:
      expected_roi: number
      risk_adjusted_return: number
      success_probability: number
    recommendations: array<string>
```

#### POST /portfolio/rebalance
リバランス実行

```yaml
Request:
  Body:
    strategy: string  # RISK_MINIMIZE | RETURN_MAXIMIZE | BALANCED
    constraints:
      max_single_theme: number (default: 0.3)
      min_basic_research: number (default: 0.15)

Response: 200 OK
  Body:
    rebalance_id: string
    changes: array<AllocationChange>
    effective_date: date
```

---

## 共通スキーマ

### Collaboration

```yaml
Collaboration:
  type: object
  properties:
    collaboration_id:
      type: string
    partner:
      $ref: '#/components/schemas/ResearchPartner'
    project:
      $ref: '#/components/schemas/CollaborationProject'
    status:
      type: string
      enum: [PROPOSED, NEGOTIATING, ACTIVE, ON_HOLD, COMPLETED, TERMINATED]
    milestones:
      type: array
      items:
        $ref: '#/components/schemas/Milestone'
    outcomes:
      type: array
      items:
        $ref: '#/components/schemas/ResearchOutcome'
```

### SerendipityInsight

```yaml
SerendipityInsight:
  type: object
  properties:
    insight_id:
      type: string
    source_connections:
      type: array
      items:
        type: string
    description:
      type: string
    novelty_score:
      type: number
      minimum: 0
      maximum: 1
    feasibility_score:
      type: number
    potential_impact:
      type: string
      enum: [LOW, MEDIUM, HIGH, TRANSFORMATIVE]
    validation_status:
      type: string
      enum: [PENDING, CONFIRMED, REJECTED, NEEDS_RESEARCH]
```

### ResearchTheme

```yaml
ResearchTheme:
  type: object
  properties:
    theme_id:
      type: string
    name:
      type: string
    category:
      type: string
      enum: [BASIC, APPLIED, DEVELOPMENT]
    risk_level:
      type: string
      enum: [LOW, MEDIUM, HIGH, EXPERIMENTAL]
    status:
      type: string
      enum: [PLANNING, ACTIVE, PAUSED, COMPLETED, ARCHIVED]
    metrics:
      type: object
      properties:
        budget_spent:
          type: number
        milestones_completed:
          type: integer
        papers_published:
          type: integer
        patents_filed:
          type: integer
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
RI001: "Partner not found"
RI002: "Collaboration already exists with this partner"
RI003: "Invalid allocation - exceeds 100%"
RI004: "Risk profile violation"
RI005: "Knowledge node not found"
RI006: "Insight validation required before application"
```

---

## レート制限

| エンドポイント | 制限 |
|---------------|------|
| 発見セッション | 10回/時間 |
| シミュレーション | 20回/時間 |
| その他 | 1000回/時間 |
