#!/usr/bin/env python3
"""
Example execution of Parasol DDD Framework
Demonstrates a complete run through all phases
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from amplifier.parasol import CapabilityDesignPhase
from amplifier.parasol import DomainModelingPhase
from amplifier.parasol import ImplementationGenerationPhase
from amplifier.parasol import KnowledgeBase
from amplifier.parasol import OperationDesignPhase
from amplifier.parasol import ParasolEngine
from amplifier.parasol import ParasolMemory
from amplifier.parasol import PatternLibrary
from amplifier.parasol import ValidationOptimizationPhase
from amplifier.parasol import ValueAnalysisPhase


def create_parasol_engine():
    """Create and configure Parasol engine"""

    # Initialize components
    knowledge_base = KnowledgeBase(Path("parasol_knowledge.db"))
    pattern_library = PatternLibrary(Path("parasol_patterns"))
    memory = ParasolMemory(Path("parasol_memory"))

    # Create engine
    engine = ParasolEngine(knowledge_base=knowledge_base, pattern_library=pattern_library, memory=memory)

    # Register all phases
    phases = [
        ValueAnalysisPhase(),
        CapabilityDesignPhase(),
        DomainModelingPhase(),
        OperationDesignPhase(),
        ImplementationGenerationPhase(),
        ValidationOptimizationPhase(),
    ]

    for phase in phases:
        engine.register_phase(phase)

    return engine


def run_consulting_dashboard_example():
    """
    Example: Consulting Dashboard Development
    Demonstrates full lifecycle from value to implementation
    """

    print("=" * 60)
    print("🌂 Parasol DDD Framework - Consulting Dashboard Example")
    print("=" * 60)

    # Define value proposition
    value_definition = {
        "core_value": "Enable data-driven consulting project management",
        "supporting_values": [
            "Real-time project visibility",
            "Resource optimization",
            "Risk mitigation",
            "Knowledge management",
        ],
        "stakeholders": [
            {
                "name": "Project Managers",
                "interest": "high",
                "influence": "high",
                "values": ["visibility", "control", "efficiency"],
            },
            {
                "name": "Consultants",
                "interest": "high",
                "influence": "medium",
                "values": ["productivity", "collaboration", "knowledge"],
            },
            {
                "name": "Clients",
                "interest": "medium",
                "influence": "high",
                "values": ["transparency", "results", "value"],
            },
        ],
        "metrics": {
            "project_visibility": "100%",
            "resource_utilization": "> 85%",
            "project_success_rate": "> 95%",
            "time_to_insight": "< 1 minute",
            "user_satisfaction": "> 4.5/5",
        },
        "roi_target": "400%",
        "payback_period": "3 months",
    }

    # Create engine
    engine = create_parasol_engine()

    # Initialize project
    print("\n📁 Initializing project...")
    context = engine.initialize_project(
        project_name="consulting-dashboard",
        project_path="./generated/consulting-dashboard",
        value_definition=value_definition,
    )
    print(f"✅ Project initialized at: {context.project_path}")

    # Start memory tracking
    execution_id = engine.memory.start_execution("consulting-dashboard")
    print(f"📝 Execution ID: {execution_id}")

    # Execute all phases
    print("\n🚀 Executing Parasol Framework...")
    print("-" * 40)

    result = engine.execute()

    # Display results
    print("\n📊 Execution Results:")
    print("-" * 40)

    if "phases_executed" in result:
        print(f"✅ Phases executed: {', '.join(result['phases_executed'])}")

    if "patterns_applied" in result:
        print(f"🎯 Patterns applied: {len(result['patterns_applied'])}")
        for pattern in result["patterns_applied"][:5]:
            print(f"   - {pattern}")

    if "generated_artifacts" in result:
        print(f"📦 Artifacts generated: {len(result['generated_artifacts'])}")
        for artifact_type, path in result["generated_artifacts"].items():
            print(f"   - {artifact_type}: {path}")

    if "metrics" in result:
        print("📈 Metrics:")
        for metric, value in result["metrics"].items():
            print(f"   - {metric}: {value}")

    # Complete execution
    engine.memory.complete_execution(feedback={"success": True, "notes": "Example execution completed successfully"})

    # Learn from execution
    print("\n🧠 Learning from execution...")
    engine.learn_from_execution(
        {"issues": [], "suggestions": ["Consider adding more domain patterns"], "success": True}
    )

    # Analyze patterns
    pattern_analysis = engine.memory.analyze_execution_patterns()
    if pattern_analysis["most_effective_patterns"]:
        print("📊 Most effective patterns:")
        for pattern, effectiveness in pattern_analysis["most_effective_patterns"][:3]:
            print(f"   - {pattern}: {effectiveness:.0%} effective")

    print("\n✅ Example completed successfully!")
    print("=" * 60)

    return result


def run_task_management_example():
    """
    Example: Task Management System
    Demonstrates V3.0 L3 Capability ⊃ Operations pattern
    """

    print("=" * 60)
    print("🌂 Parasol DDD Framework - Task Management Example")
    print("=" * 60)

    # Define value for task management
    value_definition = {
        "core_value": "Maximize team productivity through efficient task management",
        "metrics": {
            "task_completion_rate": "> 90%",
            "average_cycle_time": "< 3 days",
            "team_utilization": "75-85%",
            "on_time_delivery": "> 95%",
        },
        "roi_target": "250%",
    }

    # Create engine
    engine = create_parasol_engine()

    # Initialize project
    print("\n📁 Initializing task management project...")
    context = engine.initialize_project(
        project_name="task-management", project_path="./generated/task-management", value_definition=value_definition
    )

    # Execute specific phases
    print("\n🚀 Executing selected phases...")
    phases_to_run = ["Value Analysis", "Capability Design", "Domain Modeling", "Operation Design"]

    result = engine.execute(phases=phases_to_run)

    # Display L3 Capability ⊃ Operations structure
    print("\n📋 L3 Capabilities and Operations:")
    print("-" * 40)

    if context.capabilities.get("L3"):
        for cap in context.capabilities["L3"][:3]:
            print(f"\n🔹 {cap['name']} (L3 Capability)")
            print(f"   What: {cap['what']}")
            if cap.get("operations"):
                print("   Operations (How):")
                for op in cap["operations"][:4]:
                    print(f"      - {op}")

    print("\n✅ Task management example completed!")
    print("=" * 60)

    return result


def demonstrate_pattern_learning():
    """
    Demonstrate pattern learning and knowledge accumulation
    """

    print("=" * 60)
    print("🧠 Pattern Learning Demonstration")
    print("=" * 60)

    # Create engine with existing knowledge
    engine = create_parasol_engine()

    # Simulate multiple executions
    projects = [
        ("project-alpha", {"core_value": "Efficiency"}),
        ("project-beta", {"core_value": "Quality"}),
        ("project-gamma", {"core_value": "Innovation"}),
    ]

    for project_name, value_def in projects:
        print(f"\n📁 Running {project_name}...")

        context = engine.initialize_project(
            project_name=project_name, project_path=f"./generated/{project_name}", value_definition=value_def
        )

        # Execute with pattern tracking
        result = engine.execute(phases=["Value Analysis", "Capability Design"])

        # Record success
        engine.pattern_library.update_pattern_usage("CAP-001", success=True)

    # Analyze accumulated knowledge
    print("\n📊 Knowledge Analysis:")
    print("-" * 40)

    # Pattern effectiveness
    effectiveness = engine.knowledge_base.analyze_pattern_effectiveness()
    print("Pattern Effectiveness:")
    for pattern_id, score in list(effectiveness.items())[:5]:
        print(f"   - {pattern_id}: {score:.0%}")

    # Recent learnings
    learnings = engine.knowledge_base.get_recent_learnings(limit=3)
    print("\nRecent Learnings:")
    for learning in learnings:
        print(f"   - {learning['insight']}")

    # Memory analysis
    memory_learnings = engine.memory.learn_from_history()
    print("\nExecution Statistics:")
    print(f"   - Total executions: {memory_learnings['total_executions']}")
    print(f"   - Successful: {memory_learnings['successful_executions']}")
    print(f"   - Avg phases/execution: {memory_learnings['average_phases_per_execution']:.1f}")

    print("\n✅ Pattern learning demonstration completed!")
    print("=" * 60)


def main():
    """Main execution function"""

    print("\n" + "=" * 60)
    print("🌂 PARASOL DDD FRAMEWORK - AMPLIFIER INTEGRATION")
    print("=" * 60)
    print("\nThis demonstration shows the Parasol DDD Framework in action,")
    print("executing through all phases from value analysis to implementation.")
    print("\n")

    # Run examples
    examples = [
        ("1. Consulting Dashboard", run_consulting_dashboard_example),
        ("2. Task Management System", run_task_management_example),
        ("3. Pattern Learning", demonstrate_pattern_learning),
    ]

    print("Available examples:")
    for name, _ in examples:
        print(f"  {name}")

    print("\nRunning all examples...")
    print("\n")

    for name, example_func in examples:
        try:
            print(f"\n{'=' * 60}")
            print(f"Running: {name}")
            print("=" * 60)
            example_func()
        except Exception as e:
            print(f"❌ Error in {name}: {e}")
            import traceback

            traceback.print_exc()

    print("\n" + "=" * 60)
    print("🎉 All examples completed!")
    print("=" * 60)
    print("\nThe Parasol DDD Framework demonstrates how development can")
    print("expand systematically from a central value definition,")
    print("accumulating knowledge and patterns for continuous improvement.")
    print("\n")


if __name__ == "__main__":
    main()
