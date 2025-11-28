# BC4: Research Innovation - ドメイン言語定義

## 概要

研究イノベーションのドメイン。セレンディピティの創出、産学連携の推進、研究ポートフォリオの最適化を担う。

**BCタイプ**: Supporting（VS1内でBC1を支援）
**技術スタック**: Python/FastAPI（VS1統一）
**アーキテクチャ**: Hexagonal Architecture

---

## ユビキタス言語

### 集約（Aggregates）

#### 1. ResearchCollaboration（産学連携）

研究機関や大学との共同研究プロジェクト。

```
ResearchCollaboration {
  collaboration_id: CollaborationId        // 連携ID
  partner: ResearchPartner                  // 連携先情報
  project: CollaborationProject             // プロジェクト概要
  agreements: list<Agreement>               // 契約・合意事項
  milestones: list<Milestone>               // マイルストーン
  resources: SharedResources                // 共有リソース
  status: CollaborationStatus               // ステータス
  outcomes: list<ResearchOutcome>           // 成果物
  created_at: timestamp
  updated_at: timestamp
}
```

**ビジネスルール**:
- 連携開始前にNDA締結必須
- 知財の帰属を明確化
- 定期的な進捗レビュー（月次）

#### 2. SerendipityEngine（セレンディピティエンジン）

偶然の発見を促進する仕組み。異分野知識の組み合わせ提案。

```
SerendipityEngine {
  engine_id: EngineId
  knowledge_nodes: list<KnowledgeNode>      // 知識ノード
  connections: list<SerendipityConnection>  // 関連性
  discovery_sessions: list<DiscoverySession>// 発見セッション
  insights: list<SerendipityInsight>        // 洞察
  configuration: EngineConfiguration        // 設定
}
```

**ビジネスルール**:
- 最低3分野以上のクロスオーバーを推奨
- 発見の有用性評価を必須化
- 月次で新規知識ノードを追加

#### 3. ResearchPortfolio（研究ポートフォリオ）

研究テーマのポートフォリオ管理。リスク分散と戦略的投資配分。

```
ResearchPortfolio {
  portfolio_id: PortfolioId
  themes: list<ResearchTheme>               // 研究テーマ
  allocations: list<ResourceAllocation>     // リソース配分
  risk_profile: RiskProfile                 // リスクプロファイル
  performance: PortfolioPerformance         // パフォーマンス
  strategy: PortfolioStrategy               // 戦略
  rebalance_history: list<RebalanceEvent>   // リバランス履歴
}
```

**ビジネスルール**:
- 基礎研究：応用研究：開発研究 = 2:5:3 を基本配分
- 高リスク研究は全体の20%以下
- 四半期ごとにポートフォリオレビュー

---

### 値オブジェクト（Value Objects）

```
ResearchPartner {
  partner_id: string
  name: string
  type: PartnerType                         // UNIVERSITY | RESEARCH_INSTITUTE | CORPORATE | GOVERNMENT
  expertise_areas: list<string>
  location: Location
  contact: ContactInfo
}

CollaborationProject {
  title: string
  description: string
  objectives: list<string>
  scope: ProjectScope
  duration: DateRange
  budget: Budget
}

KnowledgeNode {
  node_id: string
  domain: string                            // 分野
  concept: string                           // 概念
  keywords: list<string>
  source: string                            // 情報源
  relevance_score: float                    // 関連性スコア
}

SerendipityConnection {
  source_node: string
  target_node: string
  connection_type: ConnectionType           // ANALOGY | CONTRAST | COMPLEMENT | HYBRID
  strength: float
  discovered_at: timestamp
  validated: boolean
}

ResearchTheme {
  theme_id: string
  name: string
  category: ThemeCategory                   // BASIC | APPLIED | DEVELOPMENT
  risk_level: RiskLevel                     // LOW | MEDIUM | HIGH | EXPERIMENTAL
  expected_roi: ROIEstimate
  timeline: TimelineEstimate
  dependencies: list<string>
}

ResourceAllocation {
  theme_id: string
  budget_percentage: float
  headcount: int
  equipment_hours: float
  priority: int
}
```

---

### ドメインイベント（Domain Events）

```
# 産学連携イベント
CollaborationProposed        // 連携提案
CollaborationAgreed          // 連携合意
MilestoneCompleted           // マイルストーン完了
OutcomePublished             // 成果発表
CollaborationConcluded       // 連携終了

# セレンディピティイベント
KnowledgeNodeAdded           // 知識ノード追加
ConnectionDiscovered         // 関連性発見
InsightGenerated             // 洞察生成
InsightValidated             // 洞察検証完了

# ポートフォリオイベント
ThemeAdded                   // テーマ追加
AllocationChanged            // 配分変更
PortfolioRebalanced          // リバランス実行
PerformanceReviewed          // パフォーマンスレビュー
```

---

### VS間連携イベント（Kafka）

#### 発行イベント

```json
{
  "event_type": "research_innovation.insight_validated",
  "payload": {
    "insight_id": "string",
    "insight_type": "TECHNOLOGY | PROCESS | MATERIAL",
    "description": "string",
    "potential_applications": ["string"],
    "validated_at": "timestamp"
  }
}
```

#### 購読イベント

```json
// BC1からの研究完了通知
{
  "event_type": "fermentation.experiment_completed",
  "payload": {
    "experiment_id": "string",
    "findings": ["string"]
  }
}
```

---

## ドメインサービス

### CollaborationManagementService

```python
class CollaborationManagementService:
    def propose_collaboration(partner_id, project_proposal) -> Collaboration
    def negotiate_terms(collaboration_id, terms) -> Agreement
    def track_milestone(collaboration_id, milestone_id, progress) -> MilestoneStatus
    def evaluate_outcome(collaboration_id, outcome) -> OutcomeEvaluation
```

### SerendipityService

```python
class SerendipityService:
    def add_knowledge_node(domain, concept, keywords) -> KnowledgeNode
    def discover_connections(node_id, depth=2) -> list[SerendipityConnection]
    def generate_insights(connection_ids) -> list[SerendipityInsight]
    def run_discovery_session(participants, focus_areas) -> DiscoverySession
```

### PortfolioOptimizationService

```python
class PortfolioOptimizationService:
    def analyze_current_allocation() -> AllocationAnalysis
    def recommend_rebalance(strategy) -> RebalanceRecommendation
    def simulate_scenario(allocation_changes) -> ScenarioResult
    def calculate_risk_metrics() -> RiskMetrics
```

---

## 用語集

| 日本語 | 英語 | 定義 |
|--------|------|------|
| 産学連携 | Research Collaboration | 大学・研究機関との共同研究 |
| セレンディピティ | Serendipity | 偶然の幸運な発見 |
| 知識ノード | Knowledge Node | 知識グラフの構成要素 |
| 研究ポートフォリオ | Research Portfolio | 研究テーマの戦略的組み合わせ |
| リバランス | Rebalance | リソース配分の再調整 |
