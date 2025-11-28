#!/usr/bin/env python3
"""
Architecture Comparison Framework
Compares different architecture implementations across multiple worktrees
"""

import argparse
import json
import subprocess
from contextlib import suppress
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


@dataclass
class ArchitectureMetrics:
    """Metrics for architecture evaluation"""

    complexity: float = 0.0  # 1-5 scale
    scalability: float = 0.0  # 1-5 scale
    maintainability: float = 0.0  # 1-5 scale
    testability: float = 0.0  # 1-5 scale
    performance: float = 0.0  # 1-5 scale
    flexibility: float = 0.0  # 1-5 scale
    learning_curve: float = 0.0  # 1-5 scale (lower is better)
    operational_overhead: float = 0.0  # 1-5 scale (lower is better)

    # Performance metrics
    response_time_p50: float = 0.0  # milliseconds
    response_time_p95: float = 0.0  # milliseconds
    throughput: float = 0.0  # requests per second
    memory_usage: float = 0.0  # MB

    # Code metrics
    lines_of_code: int = 0
    number_of_files: int = 0
    test_coverage: float = 0.0  # percentage
    cyclomatic_complexity: float = 0.0

    # Build metrics
    build_time: float = 0.0  # seconds
    docker_image_size: float = 0.0  # MB


@dataclass
class Architecture:
    """Architecture definition and metrics"""

    name: str
    path: Path
    branch: str
    description: str
    metrics: ArchitectureMetrics = field(default_factory=ArchitectureMetrics)
    pros: list[str] = field(default_factory=list)
    cons: list[str] = field(default_factory=list)
    use_cases: list[str] = field(default_factory=list)


class ArchitectureComparator:
    """Compare multiple architecture implementations"""

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.architectures: dict[str, Architecture] = {}
        self._load_architectures()

    def _load_architectures(self):
        """Load architecture definitions"""
        architectures = [
            ("monolithic", "Monolithic Architecture"),
            ("microservices", "Microservices Architecture"),
            ("event-driven", "Event-Driven Architecture"),
            ("clean", "Clean/Onion Architecture"),
            ("hexagonal", "Hexagonal Architecture"),
            ("serverless", "Serverless Architecture"),
            ("parasol-hybrid", "Parasol V3-V4 Hybrid"),
            ("cqrs-es", "CQRS + Event Sourcing"),
        ]

        for arch_name, description in architectures:
            worktree_path = self.base_path.parent / f"amplifier-{arch_name}"
            if worktree_path.exists():
                self.architectures[arch_name] = Architecture(
                    name=arch_name, path=worktree_path, branch=f"arch/{arch_name}", description=description
                )

    def analyze_architecture(self, arch: Architecture) -> ArchitectureMetrics:
        """Analyze a single architecture"""
        metrics = ArchitectureMetrics()

        # Load predefined metrics if available
        config_file = arch.path / "architecture" / "config.yaml"
        if config_file.exists():
            with open(config_file) as f:
                config = yaml.safe_load(f)
                if "metrics" in config:
                    # Load any predefined metrics
                    pass

        # Calculate code metrics
        metrics.lines_of_code = self._count_lines_of_code(arch.path)
        metrics.number_of_files = self._count_files(arch.path)

        # Run tests and get coverage
        metrics.test_coverage = self._run_tests(arch.path)

        # Measure build time
        metrics.build_time = self._measure_build_time(arch.path)

        # Calculate complexity scores (simplified heuristics)
        metrics.complexity = self._calculate_complexity(arch)
        metrics.scalability = self._calculate_scalability(arch)
        metrics.maintainability = self._calculate_maintainability(arch)
        metrics.testability = self._calculate_testability(arch)

        return metrics

    def _count_lines_of_code(self, path: Path) -> int:
        """Count lines of code in Python files"""
        total_lines = 0
        for py_file in path.rglob("*.py"):
            if "test" not in str(py_file) and "__pycache__" not in str(py_file):
                try:
                    with open(py_file) as f:
                        total_lines += len(f.readlines())
                except Exception:
                    pass
        return total_lines

    def _count_files(self, path: Path) -> int:
        """Count number of Python files"""
        return len(list(path.rglob("*.py")))

    def _run_tests(self, path: Path) -> float:
        """Run tests and get coverage"""
        try:
            subprocess.run(
                ["python", "-m", "pytest", "--cov", "--cov-report=json"],
                cwd=path,
                capture_output=True,
                text=True,
                timeout=60,
            )
            # Parse coverage from JSON if available
            coverage_file = path / "coverage.json"
            if coverage_file.exists():
                with open(coverage_file) as f:
                    coverage_data = json.load(f)
                    return coverage_data.get("totals", {}).get("percent_covered", 0)
        except Exception:
            return 0.0
        return 0.0

    def _measure_build_time(self, path: Path) -> float:
        """Measure build time"""
        import time

        start_time = time.time()

        # Simulate build process
        with suppress(Exception):
            subprocess.run(["python", "-m", "compileall", "."], cwd=path, capture_output=True, timeout=30)

        return time.time() - start_time

    def _calculate_complexity(self, arch: Architecture) -> float:
        """Calculate complexity score"""
        scores = {
            "monolithic": 2.0,
            "microservices": 5.0,
            "event-driven": 4.0,
            "clean": 4.0,
            "hexagonal": 4.0,
            "serverless": 3.0,
            "parasol-hybrid": 5.0,
            "cqrs-es": 5.0,
        }
        return scores.get(arch.name, 3.0)

    def _calculate_scalability(self, arch: Architecture) -> float:
        """Calculate scalability score"""
        scores = {
            "monolithic": 2.0,
            "microservices": 5.0,
            "event-driven": 5.0,
            "clean": 3.0,
            "hexagonal": 3.0,
            "serverless": 5.0,
            "parasol-hybrid": 4.0,
            "cqrs-es": 4.0,
        }
        return scores.get(arch.name, 3.0)

    def _calculate_maintainability(self, arch: Architecture) -> float:
        """Calculate maintainability score"""
        scores = {
            "monolithic": 3.0,
            "microservices": 3.0,
            "event-driven": 3.0,
            "clean": 5.0,
            "hexagonal": 5.0,
            "serverless": 4.0,
            "parasol-hybrid": 4.0,
            "cqrs-es": 3.0,
        }
        return scores.get(arch.name, 3.0)

    def _calculate_testability(self, arch: Architecture) -> float:
        """Calculate testability score"""
        scores = {
            "monolithic": 3.0,
            "microservices": 4.0,
            "event-driven": 3.0,
            "clean": 5.0,
            "hexagonal": 5.0,
            "serverless": 3.0,
            "parasol-hybrid": 4.0,
            "cqrs-es": 4.0,
        }
        return scores.get(arch.name, 3.0)

    def compare_all(self) -> dict[str, Any]:
        """Compare all architectures"""
        results = {}

        for name, arch in self.architectures.items():
            print(f"Analyzing {arch.description}...")
            arch.metrics = self.analyze_architecture(arch)
            results[name] = {
                "description": arch.description,
                "metrics": arch.metrics.__dict__,
                "path": str(arch.path),
                "branch": arch.branch,
            }

        return results

    def generate_report(self, results: dict[str, Any], output_format: str = "markdown") -> str:
        """Generate comparison report"""

        if output_format == "markdown":
            return self._generate_markdown_report(results)
        if output_format == "json":
            return json.dumps(results, indent=2, default=str)
        if output_format == "html":
            return self._generate_html_report(results)
        raise ValueError(f"Unknown output format: {output_format}")

    def _generate_markdown_report(self, results: dict[str, Any]) -> str:
        """Generate markdown report"""
        report = []
        report.append("# Architecture Comparison Report")
        report.append(f"\n📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Summary table
        report.append("## Summary Comparison\n")
        report.append("| Architecture | Complexity | Scalability | Maintainability | Testability | Performance |")
        report.append("|--------------|------------|-------------|-----------------|-------------|-------------|")

        for _name, data in results.items():
            metrics = data["metrics"]
            report.append(
                f"| {data['description']} | "
                f"{metrics['complexity']:.1f} | "
                f"{metrics['scalability']:.1f} | "
                f"{metrics['maintainability']:.1f} | "
                f"{metrics['testability']:.1f} | "
                f"{metrics.get('performance', 0):.1f} |"
            )

        # Detailed metrics
        report.append("\n## Detailed Metrics\n")
        for _name, data in results.items():
            report.append(f"### {data['description']}\n")
            metrics = data["metrics"]

            report.append("#### Code Metrics")
            report.append(f"- Lines of Code: {metrics['lines_of_code']:,}")
            report.append(f"- Number of Files: {metrics['number_of_files']}")
            report.append(f"- Test Coverage: {metrics['test_coverage']:.1f}%")
            report.append(f"- Build Time: {metrics['build_time']:.2f}s")
            report.append("")

        # Recommendations
        report.append("## Recommendations\n")
        report.append(self._generate_recommendations(results))

        return "\n".join(report)

    def _generate_html_report(self, results: dict[str, Any]) -> str:
        """Generate HTML report with charts"""
        html = """
<!DOCTYPE html>
<html>
<head>
    <title>Architecture Comparison</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        .chart { width: 100%; height: 400px; margin: 20px 0; }
    </style>
</head>
<body>
    <h1>Architecture Comparison Report</h1>
    <div id="radar-chart" class="chart"></div>
    <div id="bar-chart" class="chart"></div>
    <script>
        // Radar chart for multi-dimensional comparison
        var radarData = [{
            type: 'scatterpolar',
            r: [/* Add data */],
            theta: ['Complexity', 'Scalability', 'Maintainability', 'Testability', 'Performance'],
            fill: 'toself',
            name: 'Architecture Name'
        }];

        var radarLayout = {
            polar: {
                radialaxis: {
                    visible: true,
                    range: [0, 5]
                }
            }
        };

        Plotly.newPlot('radar-chart', radarData, radarLayout);

        // Bar chart for code metrics
        var barData = [{
            x: [/* Architecture names */],
            y: [/* Lines of code */],
            type: 'bar',
            name: 'Lines of Code'
        }];

        Plotly.newPlot('bar-chart', barData);
    </script>
</body>
</html>
        """
        return html

    def _generate_recommendations(self, results: dict[str, Any]) -> str:
        """Generate recommendations based on analysis"""
        recommendations = []

        # Find best architecture for different criteria
        best_scalability = max(results.items(), key=lambda x: x[1]["metrics"]["scalability"])
        best_maintainability = max(results.items(), key=lambda x: x[1]["metrics"]["maintainability"])
        best_testability = max(results.items(), key=lambda x: x[1]["metrics"]["testability"])

        recommendations.append(f"- **Best for Scalability**: {best_scalability[1]['description']}")
        recommendations.append(f"- **Best for Maintainability**: {best_maintainability[1]['description']}")
        recommendations.append(f"- **Best for Testability**: {best_testability[1]['description']}")

        # Context-specific recommendations
        recommendations.append("\n### Context-Specific Recommendations\n")
        recommendations.append("- **Small Projects**: Consider Monolithic or Clean Architecture")
        recommendations.append("- **Large Scale Systems**: Microservices or Event-Driven Architecture")
        recommendations.append("- **Cloud Native**: Serverless or Microservices")
        recommendations.append("- **Complex Domain**: Clean/Hexagonal Architecture or Parasol Hybrid")

        return "\n".join(recommendations)

    def benchmark_performance(self, arch: Architecture) -> dict[str, float]:
        """Run performance benchmarks"""
        # This would run actual performance tests
        # For now, returning simulated values
        return {"response_time_p50": 50.0, "response_time_p95": 200.0, "throughput": 1000.0, "memory_usage": 256.0}


def main():
    parser = argparse.ArgumentParser(description="Compare architecture implementations")
    parser.add_argument("--all", action="store_true", help="Compare all architectures")
    parser.add_argument("--arch", nargs="+", help="Specific architectures to compare")
    parser.add_argument("--criteria", help="Comparison criteria (comma-separated)")
    parser.add_argument("--output", default="markdown", choices=["markdown", "json", "html"])
    parser.add_argument("--file", help="Output file path")

    args = parser.parse_args()

    # Get base path
    base_path = Path(__file__).parent.parent

    # Create comparator
    comparator = ArchitectureComparator(base_path)

    # Run comparison
    if args.all:
        results = comparator.compare_all()
    elif args.arch:
        # Compare specific architectures
        results = {}
        for arch_name in args.arch:
            if arch_name in comparator.architectures:
                arch = comparator.architectures[arch_name]
                arch.metrics = comparator.analyze_architecture(arch)
                results[arch_name] = {
                    "description": arch.description,
                    "metrics": arch.metrics.__dict__,
                    "path": str(arch.path),
                    "branch": arch.branch,
                }
    else:
        print("Please specify --all or --arch")
        return

    # Generate report
    report = comparator.generate_report(results, args.output)

    # Output report
    if args.file:
        with open(args.file, "w") as f:
            f.write(report)
        print(f"Report saved to {args.file}")
    else:
        print(report)


if __name__ == "__main__":
    main()
