"""
Memory system for Parasol DDD Framework
Manages execution history and context
"""

import json
import pickle
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class ExecutionMemory:
    """Memory of a single execution"""

    project_name: str
    execution_id: str
    started_at: str
    completed_at: str | None = None
    phases_executed: list[str] = field(default_factory=list)
    phase_results: dict[str, Any] = field(default_factory=dict)
    patterns_applied: list[str] = field(default_factory=list)
    decisions_made: list[dict] = field(default_factory=list)
    artifacts_generated: dict[str, str] = field(default_factory=dict)
    metrics: dict[str, Any] = field(default_factory=dict)
    feedback: dict | None = None


class ParasolMemory:
    """
    Memory system for Parasol framework
    Stores execution history and enables learning from past executions
    """

    def __init__(self, memory_path: Path | None = None):
        self.memory_path = memory_path or Path("parasol_memory")
        self.memory_path.mkdir(parents=True, exist_ok=True)

        self.current_execution: ExecutionMemory | None = None
        self.execution_history: dict[str, ExecutionMemory] = {}
        self.project_contexts: dict[str, Any] = {}

        self._load_memory()

    def _load_memory(self):
        """Load memory from disk"""
        history_file = self.memory_path / "execution_history.pkl"
        if history_file.exists():
            try:
                with open(history_file, "rb") as f:
                    self.execution_history = pickle.load(f)
            except Exception as e:
                print(f"Error loading execution history: {e}")

        contexts_file = self.memory_path / "project_contexts.pkl"
        if contexts_file.exists():
            try:
                with open(contexts_file, "rb") as f:
                    self.project_contexts = pickle.load(f)
            except Exception as e:
                print(f"Error loading project contexts: {e}")

    def _save_memory(self):
        """Save memory to disk"""
        history_file = self.memory_path / "execution_history.pkl"
        with open(history_file, "wb") as f:
            pickle.dump(self.execution_history, f)

        contexts_file = self.memory_path / "project_contexts.pkl"
        with open(contexts_file, "wb") as f:
            pickle.dump(self.project_contexts, f)

    def start_execution(self, project_name: str) -> str:
        """Start a new execution"""
        execution_id = f"exec-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        self.current_execution = ExecutionMemory(
            project_name=project_name, execution_id=execution_id, started_at=datetime.now().isoformat()
        )

        return execution_id

    def record_phase_execution(self, phase_name: str):
        """Record that a phase has been executed"""
        if self.current_execution:
            self.current_execution.phases_executed.append(phase_name)

    def store_phase_result(self, phase_name: str, result: dict[str, Any]):
        """Store the result of a phase execution"""
        if self.current_execution:
            self.current_execution.phase_results[phase_name] = result

            # Extract patterns if present
            if "applied_patterns" in result:
                self.current_execution.patterns_applied.extend(result["applied_patterns"])

    def record_decision(self, decision: dict[str, Any]):
        """Record a decision made during execution"""
        if self.current_execution:
            decision["timestamp"] = datetime.now().isoformat()
            self.current_execution.decisions_made.append(decision)

    def record_artifact(self, artifact_type: str, artifact_path: str):
        """Record a generated artifact"""
        if self.current_execution:
            self.current_execution.artifacts_generated[artifact_type] = artifact_path

    def record_metric(self, metric_name: str, value: Any):
        """Record a metric"""
        if self.current_execution:
            self.current_execution.metrics[metric_name] = value

    def complete_execution(self, feedback: dict | None = None):
        """Complete the current execution"""
        if self.current_execution:
            self.current_execution.completed_at = datetime.now().isoformat()
            self.current_execution.feedback = feedback

            # Store in history
            self.execution_history[self.current_execution.execution_id] = self.current_execution

            # Save to disk
            self._save_memory()
            self._save_execution_report(self.current_execution)

            self.current_execution = None

    def _save_execution_report(self, execution: ExecutionMemory):
        """Save execution report as JSON"""
        report_path = self.memory_path / f"{execution.execution_id}_report.json"

        report = {
            "project_name": execution.project_name,
            "execution_id": execution.execution_id,
            "started_at": execution.started_at,
            "completed_at": execution.completed_at,
            "phases_executed": execution.phases_executed,
            "phase_results": execution.phase_results,
            "patterns_applied": execution.patterns_applied,
            "decisions_made": execution.decisions_made,
            "artifacts_generated": execution.artifacts_generated,
            "metrics": execution.metrics,
            "feedback": execution.feedback,
        }

        with open(report_path, "w") as f:
            json.dump(report, f, indent=2, default=str)

    def store_project_context(self, context: Any):
        """Store project context"""
        if hasattr(context, "project_name"):
            self.project_contexts[context.project_name] = context
            self._save_memory()

    def get_project_context(self, project_name: str) -> Any | None:
        """Get stored project context"""
        return self.project_contexts.get(project_name)

    def get_execution_history(self, project_name: str | None = None) -> list[ExecutionMemory]:
        """Get execution history, optionally filtered by project"""
        history = list(self.execution_history.values())

        if project_name:
            history = [e for e in history if e.project_name == project_name]

        # Sort by start time
        history.sort(key=lambda e: e.started_at, reverse=True)

        return history

    def get_applied_patterns(self) -> list[str]:
        """Get list of applied patterns from current execution"""
        if self.current_execution:
            return self.current_execution.patterns_applied
        return []

    def get_pattern_count(self) -> int:
        """Get count of patterns applied in current execution"""
        if self.current_execution:
            return len(self.current_execution.patterns_applied)
        return 0

    def analyze_execution_patterns(self) -> dict[str, Any]:
        """Analyze patterns across all executions"""
        pattern_usage = {}
        pattern_success = {}

        for execution in self.execution_history.values():
            for pattern in execution.patterns_applied:
                pattern_usage[pattern] = pattern_usage.get(pattern, 0) + 1

                # Consider execution successful if it completed
                if execution.completed_at:
                    pattern_success[pattern] = pattern_success.get(pattern, 0) + 1

        # Calculate success rates
        pattern_effectiveness = {}
        for pattern, usage_count in pattern_usage.items():
            success_count = pattern_success.get(pattern, 0)
            pattern_effectiveness[pattern] = success_count / usage_count if usage_count > 0 else 0

        return {
            "pattern_usage": pattern_usage,
            "pattern_effectiveness": pattern_effectiveness,
            "most_used_patterns": sorted(pattern_usage.items(), key=lambda x: x[1], reverse=True)[:5],
            "most_effective_patterns": sorted(pattern_effectiveness.items(), key=lambda x: x[1], reverse=True)[:5],
        }

    def get_similar_executions(self, context: dict[str, Any]) -> list[ExecutionMemory]:
        """Find similar past executions"""
        similar = []

        # Simple similarity based on project characteristics
        for execution in self.execution_history.values():
            similarity_score = self._calculate_similarity(execution, context)
            if similarity_score > 0.5:
                similar.append(execution)

        return similar

    def _calculate_similarity(self, execution: ExecutionMemory, context: dict[str, Any]) -> float:
        """Calculate similarity between execution and context"""
        score = 0.0

        # Check phases executed
        if "phases" in context:
            common_phases = set(execution.phases_executed) & set(context["phases"])
            score += len(common_phases) / max(len(execution.phases_executed), len(context["phases"]))

        # Check patterns used
        if "patterns" in context:
            common_patterns = set(execution.patterns_applied) & set(context["patterns"])
            if execution.patterns_applied:
                score += len(common_patterns) / len(execution.patterns_applied)

        return score / 2  # Average of the scores

    def learn_from_history(self) -> dict[str, Any]:
        """Extract learnings from execution history"""
        learnings = {
            "total_executions": len(self.execution_history),
            "successful_executions": sum(1 for e in self.execution_history.values() if e.completed_at),
            "common_patterns": self._find_common_patterns(),
            "average_phases_per_execution": self._calculate_average_phases(),
            "common_decisions": self._analyze_common_decisions(),
        }

        return learnings

    def _find_common_patterns(self) -> list[str]:
        """Find most commonly used patterns"""
        pattern_count = {}

        for execution in self.execution_history.values():
            for pattern in execution.patterns_applied:
                pattern_count[pattern] = pattern_count.get(pattern, 0) + 1

        # Return top 5 most common
        sorted_patterns = sorted(pattern_count.items(), key=lambda x: x[1], reverse=True)
        return [p[0] for p in sorted_patterns[:5]]

    def _calculate_average_phases(self) -> float:
        """Calculate average number of phases per execution"""
        if not self.execution_history:
            return 0

        total_phases = sum(len(e.phases_executed) for e in self.execution_history.values())
        return total_phases / len(self.execution_history)

    def _analyze_common_decisions(self) -> list[dict]:
        """Analyze common decisions across executions"""
        decision_patterns = {}

        for execution in self.execution_history.values():
            for decision in execution.decisions_made:
                decision_type = decision.get("type", "unknown")
                decision_patterns[decision_type] = decision_patterns.get(decision_type, 0) + 1

        # Return top decision types
        sorted_decisions = sorted(decision_patterns.items(), key=lambda x: x[1], reverse=True)
        return [{"type": d[0], "count": d[1]} for d in sorted_decisions[:5]]

    def export_memory(self, export_path: Path):
        """Export memory to JSON"""
        memory_data = {
            "execution_history": [
                {
                    "project_name": e.project_name,
                    "execution_id": e.execution_id,
                    "started_at": e.started_at,
                    "completed_at": e.completed_at,
                    "phases_executed": e.phases_executed,
                    "patterns_applied": e.patterns_applied,
                    "metrics": e.metrics,
                }
                for e in self.execution_history.values()
            ],
            "learnings": self.learn_from_history(),
        }

        with open(export_path, "w") as f:
            json.dump(memory_data, f, indent=2, default=str)
