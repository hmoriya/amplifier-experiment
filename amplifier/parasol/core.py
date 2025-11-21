"""
Parasol Core Engine - Central orchestrator for the DDD framework
"""

from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from .knowledge import KnowledgeBase
from .memory import ParasolMemory
from .patterns import PatternLibrary
from .patterns import PatternMatcher
from .phases import PhaseBase


@dataclass
class ParasolContext:
    """Context for Parasol execution"""

    project_name: str
    project_path: Path
    value_definition: dict[str, Any]
    capabilities: dict[str, list[Any]] = field(default_factory=dict)
    bounded_contexts: list[dict] = field(default_factory=list)
    operations: list[dict] = field(default_factory=list)
    generated_artifacts: dict[str, Path] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.metadata["created_at"] = datetime.now().isoformat()
        self.metadata["parasol_version"] = "1.0.0"


class ParasolEngine:
    """
    Main engine for Parasol DDD Framework

    Orchestrates the entire development flow from value analysis
    through implementation generation.
    """

    def __init__(
        self,
        knowledge_base: KnowledgeBase | None = None,
        pattern_library: PatternLibrary | None = None,
        memory: ParasolMemory | None = None,
    ):
        self.knowledge_base = knowledge_base or KnowledgeBase()
        self.pattern_library = pattern_library or PatternLibrary()
        self.memory = memory or ParasolMemory()
        self.phases: list[PhaseBase] = []
        self.context: ParasolContext | None = None
        self.pattern_matcher = PatternMatcher(self.pattern_library)

    def initialize_project(
        self, project_name: str, project_path: str, value_definition: dict[str, Any]
    ) -> ParasolContext:
        """Initialize a new Parasol project"""
        self.context = ParasolContext(
            project_name=project_name, project_path=Path(project_path), value_definition=value_definition
        )

        # Store in memory
        self.memory.store_project_context(self.context)

        # Initialize project structure
        self._create_project_structure()

        return self.context

    def register_phase(self, phase: PhaseBase):
        """Register a phase in the execution pipeline"""
        self.phases.append(phase)
        phase.set_engine(self)

    def execute(self, phases: list[str] | None = None) -> dict[str, Any]:
        """
        Execute the Parasol framework

        Args:
            phases: Optional list of phase names to execute.
                   If None, executes all registered phases.
        """
        if not self.context:
            raise ValueError("Project not initialized. Call initialize_project first.")

        results = {}
        phases_to_execute = self._get_phases_to_execute(phases)

        for phase in phases_to_execute:
            print(f"🚀 Executing Phase: {phase.name}")

            # Check gate conditions
            if not phase.check_gate_conditions(self.context):
                print(f"⚠️  Gate conditions not met for {phase.name}")
                continue

            # Execute phase
            result = phase.execute(self.context)
            results[phase.name] = result

            # Collect knowledge from phase output
            self.knowledge_base.collect_from_phase(phase.name, result)

            # Apply patterns
            patterns = self.pattern_matcher.find_applicable_patterns(self.context, phase.name)
            for pattern in patterns:
                self._apply_pattern(pattern, phase.name)

            # Store results in memory
            self.memory.store_phase_result(phase.name, result)

            # Update context with phase results
            phase.update_context(self.context, result)

        # Generate final report
        final_report = self._generate_report(results)

        return final_report

    def _get_phases_to_execute(self, phase_names: list[str] | None) -> list[PhaseBase]:
        """Get list of phases to execute"""
        if phase_names is None:
            return self.phases

        return [p for p in self.phases if p.name in phase_names]

    def _create_project_structure(self):
        """Create the project directory structure"""
        directories = [
            "value-analysis",
            "capabilities",
            "bounded-contexts",
            "operations",
            "implementation",
            "validation",
            "patterns",
            "knowledge",
        ]

        for dir_name in directories:
            dir_path = self.context.project_path / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)

    def _apply_pattern(self, pattern: dict, phase_name: str):
        """Apply a pattern to the current context"""
        print(f"  📋 Applying pattern: {pattern['name']}")

        # Pattern application logic
        if pattern["type"] == "structural":
            self._apply_structural_pattern(pattern)
        elif pattern["type"] == "behavioral":
            self._apply_behavioral_pattern(pattern)
        elif pattern["type"] == "architectural":
            self._apply_architectural_pattern(pattern)

        # Record pattern usage
        self.knowledge_base.record_pattern_usage(pattern["id"], phase_name, self.context.project_name)

    def _apply_structural_pattern(self, pattern: dict):
        """Apply a structural pattern"""
        # Implementation specific to structural patterns
        pass

    def _apply_behavioral_pattern(self, pattern: dict):
        """Apply a behavioral pattern"""
        # Implementation specific to behavioral patterns
        pass

    def _apply_architectural_pattern(self, pattern: dict):
        """Apply an architectural pattern"""
        # Implementation specific to architectural patterns
        pass

    def _generate_report(self, results: dict[str, Any]) -> dict[str, Any]:
        """Generate comprehensive report of the execution"""
        report = {
            "project": self.context.project_name,
            "execution_time": datetime.now().isoformat(),
            "phases_executed": list(results.keys()),
            "results": results,
            "patterns_applied": self.memory.get_applied_patterns(),
            "knowledge_gained": self.knowledge_base.get_recent_learnings(),
            "generated_artifacts": self.context.generated_artifacts,
            "metrics": self._calculate_metrics(results),
        }

        # Save report
        report_path = self.context.project_path / "parasol-report.yaml"
        with open(report_path, "w") as f:
            yaml.dump(report, f, default_flow_style=False)

        return report

    def _calculate_metrics(self, results: dict[str, Any]) -> dict[str, Any]:
        """Calculate execution metrics"""
        return {
            "capabilities_defined": len(self.context.capabilities.get("L3", [])),
            "bounded_contexts": len(self.context.bounded_contexts),
            "operations_designed": len(self.context.operations),
            "patterns_applied": self.memory.get_pattern_count(),
            "knowledge_items_created": self.knowledge_base.get_item_count(),
        }

    def learn_from_execution(self, feedback: dict[str, Any]):
        """Learn from execution results and feedback"""
        learning = {
            "project": self.context.project_name,
            "feedback": feedback,
            "patterns_effectiveness": self._analyze_pattern_effectiveness(),
            "improvements": self._identify_improvements(feedback),
        }

        self.knowledge_base.add_learning(learning)
        self.pattern_library.update_pattern_scores(learning["patterns_effectiveness"])

    def _analyze_pattern_effectiveness(self) -> dict[str, float]:
        """Analyze how effective patterns were"""
        effectiveness = {}
        for pattern_id in self.memory.get_applied_patterns():
            effectiveness[pattern_id] = self._calculate_pattern_effectiveness(pattern_id)
        return effectiveness

    def _calculate_pattern_effectiveness(self, pattern_id: str) -> float:
        """Calculate effectiveness score for a pattern"""
        # Simplified calculation - would be more complex in practice
        return 0.85

    def _identify_improvements(self, feedback: dict[str, Any]) -> list[str]:
        """Identify areas for improvement based on feedback"""
        improvements = []

        if feedback.get("issues"):
            for issue in feedback["issues"]:
                improvements.append(f"Address: {issue}")

        if feedback.get("suggestions"):
            for suggestion in feedback["suggestions"]:
                improvements.append(f"Consider: {suggestion}")

        return improvements
