"""
Knowledge base system for Parasol DDD Framework
Manages learning, insights, and accumulated knowledge
"""

import json
import sqlite3
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class KnowledgeItem:
    """A piece of knowledge or learning"""

    id: str
    type: str  # pattern, learning, decision, metric
    category: str
    content: dict[str, Any]
    metadata: dict[str, Any] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    project: str | None = None
    phase: str | None = None
    impact: str = "medium"  # high, medium, low


@dataclass
class Learning:
    """A learning from project execution"""

    situation: str
    action: str
    result: str
    insight: str
    recommendation: str
    impact: str
    tags: list[str] = field(default_factory=list)


class KnowledgeBase:
    """
    Central knowledge repository for Parasol framework
    """

    def __init__(self, db_path: Path | None = None):
        self.db_path = db_path or Path("knowledge.db")
        self.connection = None
        self._initialize_database()
        self.knowledge_items: dict[str, KnowledgeItem] = {}
        self._load_knowledge()

    def _initialize_database(self):
        """Initialize SQLite database for knowledge storage"""
        self.connection = sqlite3.connect(str(self.db_path))
        cursor = self.connection.cursor()

        # Create knowledge items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_items (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                category TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata TEXT,
                tags TEXT,
                created_at TEXT NOT NULL,
                project TEXT,
                phase TEXT,
                impact TEXT
            )
        """)

        # Create learnings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                situation TEXT NOT NULL,
                action TEXT NOT NULL,
                result TEXT NOT NULL,
                insight TEXT NOT NULL,
                recommendation TEXT NOT NULL,
                impact TEXT,
                tags TEXT,
                created_at TEXT NOT NULL,
                project TEXT
            )
        """)

        # Create patterns usage table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pattern_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_id TEXT NOT NULL,
                project TEXT NOT NULL,
                phase TEXT,
                success BOOLEAN,
                timestamp TEXT NOT NULL
            )
        """)

        self.connection.commit()

    def _load_knowledge(self):
        """Load knowledge items from database"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM knowledge_items")

        for row in cursor.fetchall():
            item = KnowledgeItem(
                id=row[0],
                type=row[1],
                category=row[2],
                content=json.loads(row[3]),
                metadata=json.loads(row[4]) if row[4] else {},
                tags=json.loads(row[5]) if row[5] else [],
                created_at=row[6],
                project=row[7],
                phase=row[8],
                impact=row[9],
            )
            self.knowledge_items[item.id] = item

    def add_knowledge(self, item: KnowledgeItem):
        """Add a knowledge item to the base"""
        self.knowledge_items[item.id] = item

        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO knowledge_items
            (id, type, category, content, metadata, tags, created_at, project, phase, impact)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                item.id,
                item.type,
                item.category,
                json.dumps(item.content),
                json.dumps(item.metadata),
                json.dumps(item.tags),
                item.created_at,
                item.project,
                item.phase,
                item.impact,
            ),
        )
        self.connection.commit()

    def add_learning(self, learning: dict[str, Any]):
        """Add a learning to the knowledge base"""
        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO learnings
            (situation, action, result, insight, recommendation, impact, tags, created_at, project)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                learning.get("situation", ""),
                learning.get("action", ""),
                learning.get("result", ""),
                learning.get("insight", ""),
                learning.get("recommendation", ""),
                learning.get("impact", "medium"),
                json.dumps(learning.get("tags", [])),
                datetime.now().isoformat(),
                learning.get("project", ""),
            ),
        )
        self.connection.commit()

    def collect_from_phase(self, phase_name: str, phase_output: dict[str, Any]):
        """Collect knowledge from phase execution"""
        # Extract patterns used
        if "applied_patterns" in phase_output:
            for pattern in phase_output["applied_patterns"]:
                self.record_pattern_usage(pattern, phase_name, phase_output.get("project", "unknown"))

        # Extract decisions made
        if "decisions" in phase_output:
            for decision in phase_output["decisions"]:
                item = KnowledgeItem(
                    id=f"DEC-{datetime.now().timestamp()}",
                    type="decision",
                    category=phase_name,
                    content=decision,
                    phase=phase_name,
                    impact="medium",
                )
                self.add_knowledge(item)

        # Extract metrics
        if "metrics" in phase_output:
            item = KnowledgeItem(
                id=f"MET-{datetime.now().timestamp()}",
                type="metric",
                category=phase_name,
                content=phase_output["metrics"],
                phase=phase_name,
                impact="low",
            )
            self.add_knowledge(item)

    def record_pattern_usage(self, pattern_id: str, phase: str, project: str, success: bool = True):
        """Record pattern usage"""
        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO pattern_usage (pattern_id, project, phase, success, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """,
            (pattern_id, project, phase, success, datetime.now().isoformat()),
        )
        self.connection.commit()

    def get_recent_learnings(self, limit: int = 10) -> list[dict]:
        """Get recent learnings"""
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT * FROM learnings ORDER BY created_at DESC LIMIT ?
        """,
            (limit,),
        )

        learnings = []
        for row in cursor.fetchall():
            learnings.append(
                {
                    "id": row[0],
                    "situation": row[1],
                    "action": row[2],
                    "result": row[3],
                    "insight": row[4],
                    "recommendation": row[5],
                    "impact": row[6],
                    "tags": json.loads(row[7]) if row[7] else [],
                    "created_at": row[8],
                    "project": row[9],
                }
            )

        return learnings

    def search(self, query: str, filters: dict | None = None) -> list[KnowledgeItem]:
        """Search knowledge base"""
        results = []
        query_lower = query.lower()

        for item in self.knowledge_items.values():
            # Text search
            if (
                query_lower in json.dumps(item.content).lower()
                or query_lower in item.category.lower()
                or any(query_lower in tag.lower() for tag in item.tags)
            ):
                # Apply filters if provided
                if filters:
                    if "type" in filters and item.type != filters["type"]:
                        continue
                    if "category" in filters and item.category != filters["category"]:
                        continue
                    if "impact" in filters and item.impact != filters["impact"]:
                        continue
                    if "phase" in filters and item.phase != filters["phase"]:
                        continue

                results.append(item)

        return results

    def get_insights_for_context(self, context: dict[str, Any]) -> list[dict]:
        """Get relevant insights for current context"""
        insights = []

        # Get phase-specific insights
        current_phase = context.get("current_phase", "")
        if current_phase:
            phase_items = self.search("", filters={"phase": current_phase})
            for item in phase_items:
                if item.type in ["learning", "decision"]:
                    insights.append({"type": item.type, "content": item.content, "impact": item.impact})

        return insights

    def analyze_pattern_effectiveness(self) -> dict[str, float]:
        """Analyze pattern effectiveness across projects"""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT pattern_id,
                   COUNT(*) as usage_count,
                   SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as success_count
            FROM pattern_usage
            GROUP BY pattern_id
        """)

        effectiveness = {}
        for row in cursor.fetchall():
            pattern_id = row[0]
            usage_count = row[1]
            success_count = row[2]
            effectiveness[pattern_id] = success_count / usage_count if usage_count > 0 else 0

        return effectiveness

    def get_item_count(self) -> int:
        """Get total number of knowledge items"""
        return len(self.knowledge_items)

    def export_knowledge(self, export_path: Path):
        """Export knowledge base to JSON"""
        export_data = {
            "knowledge_items": [
                {
                    "id": item.id,
                    "type": item.type,
                    "category": item.category,
                    "content": item.content,
                    "metadata": item.metadata,
                    "tags": item.tags,
                    "created_at": item.created_at,
                    "project": item.project,
                    "phase": item.phase,
                    "impact": item.impact,
                }
                for item in self.knowledge_items.values()
            ],
            "learnings": self.get_recent_learnings(limit=1000),
            "pattern_effectiveness": self.analyze_pattern_effectiveness(),
        }

        with open(export_path, "w") as f:
            json.dump(export_data, f, indent=2)

    def import_knowledge(self, import_path: Path):
        """Import knowledge from JSON"""
        with open(import_path) as f:
            import_data = json.load(f)

        # Import knowledge items
        for item_data in import_data.get("knowledge_items", []):
            item = KnowledgeItem(**item_data)
            self.add_knowledge(item)

        # Import learnings
        for learning in import_data.get("learnings", []):
            self.add_learning(learning)


class KnowledgeCollector:
    """
    Collects knowledge from various sources during execution
    """

    def __init__(self, knowledge_base: KnowledgeBase):
        self.knowledge_base = knowledge_base
        self.current_collection = []

    def start_collection(self, project: str, phase: str):
        """Start collecting knowledge for a phase"""
        self.current_collection = []
        self.current_project = project
        self.current_phase = phase

    def collect_decision(self, decision: dict[str, Any]):
        """Collect a decision made during execution"""
        item = KnowledgeItem(
            id=f"DEC-{datetime.now().timestamp()}",
            type="decision",
            category=self.current_phase,
            content=decision,
            project=self.current_project,
            phase=self.current_phase,
            impact=decision.get("impact", "medium"),
        )
        self.current_collection.append(item)

    def collect_insight(self, insight: str, tags: list[str] = None):
        """Collect an insight"""
        item = KnowledgeItem(
            id=f"INS-{datetime.now().timestamp()}",
            type="insight",
            category=self.current_phase,
            content={"insight": insight},
            project=self.current_project,
            phase=self.current_phase,
            tags=tags or [],
            impact="medium",
        )
        self.current_collection.append(item)

    def collect_metric(self, metric_name: str, value: Any):
        """Collect a metric"""
        item = KnowledgeItem(
            id=f"MET-{datetime.now().timestamp()}",
            type="metric",
            category=self.current_phase,
            content={"metric": metric_name, "value": value},
            project=self.current_project,
            phase=self.current_phase,
            impact="low",
        )
        self.current_collection.append(item)

    def finalize_collection(self):
        """Finalize and store collected knowledge"""
        for item in self.current_collection:
            self.knowledge_base.add_knowledge(item)

        # Create learning from collection
        if self.current_collection:
            learning = {
                "situation": f"Executing {self.current_phase} for {self.current_project}",
                "action": f"Collected {len(self.current_collection)} knowledge items",
                "result": "Knowledge successfully collected",
                "insight": self._summarize_insights(),
                "recommendation": self._generate_recommendations(),
                "project": self.current_project,
                "impact": "medium",
            }
            self.knowledge_base.add_learning(learning)

        self.current_collection = []

    def _summarize_insights(self) -> str:
        """Summarize collected insights"""
        insights = [item for item in self.current_collection if item.type == "insight"]
        if insights:
            return f"Collected {len(insights)} insights during {self.current_phase}"
        return "No specific insights collected"

    def _generate_recommendations(self) -> str:
        """Generate recommendations from collection"""
        decisions = [item for item in self.current_collection if item.type == "decision"]
        if decisions:
            return f"Review {len(decisions)} decisions for future reference"
        return "Continue with standard process"
