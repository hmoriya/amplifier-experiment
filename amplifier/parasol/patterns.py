"""
Pattern library and pattern matching for Parasol DDD Framework
"""

import json
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class Pattern:
    """A reusable pattern definition"""

    id: str
    name: str
    category: str  # value, capability, domain, operation, implementation
    type: str  # structural, behavioral, architectural
    problem: str
    solution: str
    context: dict[str, Any]
    consequences: dict[str, Any]
    examples: list[dict] = field(default_factory=list)
    usage_count: int = 0
    success_rate: float = 0.0
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.metadata:
            self.metadata = {"created_at": datetime.now().isoformat(), "last_used": None, "version": "1.0.0"}


class PatternLibrary:
    """
    Central repository of patterns for Parasol framework
    """

    def __init__(self, library_path: Path | None = None):
        self.library_path = library_path or Path("patterns")
        self.patterns: dict[str, Pattern] = {}
        self._load_default_patterns()
        if self.library_path.exists():
            self._load_custom_patterns()

    def _load_default_patterns(self):
        """Load default patterns included with the framework"""
        default_patterns = [
            # Value patterns
            Pattern(
                id="VAL-001",
                name="Stakeholder Value Matrix",
                category="value",
                type="structural",
                problem="Need to identify and prioritize stakeholder values",
                solution="Create a matrix mapping stakeholders to their key values and priorities",
                context={"phase": "value_analysis", "applicability": "all_projects"},
                consequences={"benefits": ["Clear value alignment"], "liabilities": ["Time to create"]},
                tags=["stakeholder", "value", "analysis"],
            ),
            # Capability patterns
            Pattern(
                id="CAP-001",
                name="Hierarchical Capability Decomposition",
                category="capability",
                type="structural",
                problem="Need to break down high-level capabilities into implementable components",
                solution="Use three-level hierarchy: Strategic (L1) -> Tactical (L2) -> Operational (L3)",
                context={"phase": "capability_design", "applicability": "complex_systems"},
                consequences={"benefits": ["Clear structure"], "liabilities": ["Can be rigid"]},
                tags=["capability", "hierarchy", "decomposition"],
            ),
            # Domain patterns
            Pattern(
                id="DOM-001",
                name="Aggregate Root",
                category="domain",
                type="structural",
                problem="Need to maintain consistency boundaries in domain model",
                solution="Define aggregate roots that control access to related entities",
                context={"phase": "domain_modeling", "applicability": "ddd_projects"},
                consequences={"benefits": ["Consistency"], "liabilities": ["Complexity"]},
                tags=["ddd", "aggregate", "consistency"],
            ),
            # Operation patterns
            Pattern(
                id="OPS-001",
                name="CRUD Operations",
                category="operation",
                type="behavioral",
                problem="Need basic data manipulation operations",
                solution="Implement Create, Read, Update, Delete operations",
                context={"phase": "operation_design", "applicability": "data_centric"},
                consequences={"benefits": ["Simplicity"], "liabilities": ["Limited expressiveness"]},
                tags=["crud", "operations", "basic"],
            ),
            Pattern(
                id="OPS-002",
                name="Workflow Pattern",
                category="operation",
                type="behavioral",
                problem="Need to orchestrate multi-step business processes",
                solution="Define workflow with states, transitions, and guards",
                context={"phase": "operation_design", "applicability": "process_centric"},
                consequences={"benefits": ["Process clarity"], "liabilities": ["State complexity"]},
                tags=["workflow", "process", "state-machine"],
            ),
            # Implementation patterns
            Pattern(
                id="IMP-001",
                name="Microservice Architecture",
                category="implementation",
                type="architectural",
                problem="Need scalable and maintainable system architecture",
                solution="Decompose system into independently deployable services",
                context={"phase": "implementation", "applicability": "distributed_systems"},
                consequences={"benefits": ["Scalability"], "liabilities": ["Network complexity"]},
                tags=["microservices", "architecture", "distributed"],
            ),
        ]

        for pattern in default_patterns:
            self.patterns[pattern.id] = pattern

    def _load_custom_patterns(self):
        """Load custom patterns from library path"""
        pattern_files = self.library_path.glob("*.json")
        for file in pattern_files:
            try:
                with open(file) as f:
                    pattern_data = json.load(f)
                    pattern = Pattern(**pattern_data)
                    self.patterns[pattern.id] = pattern
            except Exception as e:
                print(f"Error loading pattern from {file}: {e}")

    def add_pattern(self, pattern: Pattern) -> str:
        """Add a new pattern to the library"""
        self.patterns[pattern.id] = pattern
        self._save_pattern(pattern)
        return pattern.id

    def get_pattern(self, pattern_id: str) -> Pattern | None:
        """Get a pattern by ID"""
        return self.patterns.get(pattern_id)

    def get_patterns(self, category: str | None = None, tags: list[str] | None = None) -> list[Pattern]:
        """Get patterns filtered by category and/or tags"""
        patterns = list(self.patterns.values())

        if category:
            patterns = [p for p in patterns if p.category == category]

        if tags:
            patterns = [p for p in patterns if any(tag in p.tags for tag in tags)]

        return patterns

    def update_pattern_usage(self, pattern_id: str, success: bool):
        """Update pattern usage statistics"""
        if pattern_id in self.patterns:
            pattern = self.patterns[pattern_id]
            pattern.usage_count += 1
            # Simple success rate calculation
            pattern.success_rate = (
                pattern.success_rate * (pattern.usage_count - 1) + (1.0 if success else 0.0)
            ) / pattern.usage_count
            pattern.metadata["last_used"] = datetime.now().isoformat()
            self._save_pattern(pattern)

    def update_pattern_scores(self, effectiveness_scores: dict[str, float]):
        """Update pattern effectiveness scores"""
        for pattern_id, score in effectiveness_scores.items():
            if pattern_id in self.patterns:
                pattern = self.patterns[pattern_id]
                pattern.metadata["effectiveness_score"] = score
                self._save_pattern(pattern)

    def _save_pattern(self, pattern: Pattern):
        """Save pattern to disk"""
        if not self.library_path.exists():
            self.library_path.mkdir(parents=True)

        file_path = self.library_path / f"{pattern.id}.json"
        pattern_dict = {
            "id": pattern.id,
            "name": pattern.name,
            "category": pattern.category,
            "type": pattern.type,
            "problem": pattern.problem,
            "solution": pattern.solution,
            "context": pattern.context,
            "consequences": pattern.consequences,
            "examples": pattern.examples,
            "usage_count": pattern.usage_count,
            "success_rate": pattern.success_rate,
            "tags": pattern.tags,
            "metadata": pattern.metadata,
        }

        with open(file_path, "w") as f:
            json.dump(pattern_dict, f, indent=2)

    def search_patterns(self, query: str) -> list[Pattern]:
        """Search patterns by text query"""
        query_lower = query.lower()
        results = []

        for pattern in self.patterns.values():
            if (
                query_lower in pattern.name.lower()
                or query_lower in pattern.problem.lower()
                or query_lower in pattern.solution.lower()
                or any(query_lower in tag.lower() for tag in pattern.tags)
            ):
                results.append(pattern)

        return results


class PatternMatcher:
    """
    Matches patterns to current context for application
    """

    def __init__(self, pattern_library: PatternLibrary):
        self.pattern_library = pattern_library

    def find_applicable_patterns(self, context: Any, phase: str) -> list[Pattern]:
        """Find patterns applicable to current context and phase"""
        applicable_patterns = []

        # Get patterns for current phase
        phase_patterns = self._get_phase_patterns(phase)

        for pattern in phase_patterns:
            if self._is_pattern_applicable(pattern, context):
                applicable_patterns.append(pattern)

        # Sort by success rate and usage
        applicable_patterns.sort(key=lambda p: (p.success_rate, p.usage_count), reverse=True)

        return applicable_patterns

    def _get_phase_patterns(self, phase: str) -> list[Pattern]:
        """Get patterns relevant to current phase"""
        phase_mapping = {
            "Value Analysis": "value",
            "Capability Design": "capability",
            "Domain Modeling": "domain",
            "Operation Design": "operation",
            "Implementation Generation": "implementation",
            "Validation and Optimization": "implementation",
        }

        category = phase_mapping.get(phase, "")
        return self.pattern_library.get_patterns(category=category)

    def _is_pattern_applicable(self, pattern: Pattern, context: Any) -> bool:
        """Check if a pattern is applicable to the current context"""
        # Check context applicability
        pattern_applicability = pattern.context.get("applicability", "all")

        if pattern_applicability == "all" or pattern_applicability == "all_projects":
            return True

        # More sophisticated checks based on project characteristics
        if hasattr(context, "metadata"):
            project_type = context.metadata.get("project_type", "")

            if pattern_applicability == "complex_systems" and "complex" in project_type:
                return True
            if pattern_applicability == "ddd_projects" and "ddd" in project_type:
                return True
            if pattern_applicability == "distributed_systems" and "distributed" in project_type:
                return True

        # Check if pattern has been successful in similar contexts
        if pattern.success_rate > 0.7:
            return True

        return False

    def recommend_pattern(self, context: Any, problem_description: str) -> Pattern | None:
        """Recommend a pattern based on problem description"""
        # Search for patterns matching the problem
        search_results = self.pattern_library.search_patterns(problem_description)

        if not search_results:
            return None

        # Filter by applicability
        applicable = [p for p in search_results if self._is_pattern_applicable(p, context)]

        if not applicable:
            return search_results[0]  # Return best match even if not perfectly applicable

        # Return the most successful applicable pattern
        return max(applicable, key=lambda p: p.success_rate)

    def instantiate_pattern(self, pattern: Pattern, parameters: dict[str, Any]) -> dict[str, Any]:
        """Instantiate a pattern with specific parameters"""
        instantiation = {
            "pattern_id": pattern.id,
            "pattern_name": pattern.name,
            "parameters": parameters,
            "solution_template": self._expand_solution(pattern.solution, parameters),
            "generated_at": datetime.now().isoformat(),
        }

        # Add examples if available
        if pattern.examples:
            instantiation["example"] = pattern.examples[0]

        return instantiation

    def _expand_solution(self, solution_template: str, parameters: dict[str, Any]) -> str:
        """Expand solution template with parameters"""
        expanded = solution_template

        for key, value in parameters.items():
            placeholder = f"{{{key}}}"
            if placeholder in expanded:
                expanded = expanded.replace(placeholder, str(value))

        return expanded
