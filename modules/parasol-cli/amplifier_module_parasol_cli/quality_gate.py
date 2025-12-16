"""Quality Gate system for Parasol phases."""

import json
import yaml
from pathlib import Path
from typing import List, Tuple
from dataclasses import dataclass
from datetime import datetime
import jsonschema


@dataclass
class ValidationResult:
    """Result of a validation check."""

    phase: int
    passed: bool
    errors: List[str]
    warnings: List[str]
    timestamp: str

    def to_dict(self) -> dict:
        return {
            "phase": self.phase,
            "passed": self.passed,
            "errors": self.errors,
            "warnings": self.warnings,
            "timestamp": self.timestamp,
        }


class QualityGate:
    """Quality gate system for validating phase outputs."""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.contracts_path = Path(__file__).parent.parent.parent.parent / "parasol/contracts/phase-contracts.yaml"
        self.contracts = self._load_contracts()

    def _load_contracts(self) -> dict:
        """Load phase contracts from YAML."""
        if self.contracts_path.exists():
            with open(self.contracts_path) as f:
                return yaml.safe_load(f)
        return {"contracts": {}, "phase_transitions": {}}

    def validate_phase(self, phase: int) -> ValidationResult:
        """Validate outputs for a specific phase."""
        errors = []
        warnings = []

        # Check if phase outputs exist
        phase_dir = self.project_path / f"outputs/{phase}-{self._get_phase_name(phase)}"
        if not phase_dir.exists():
            errors.append(f"Phase {phase} output directory not found")
            return ValidationResult(
                phase=phase, passed=False, errors=errors, warnings=warnings, timestamp=datetime.now().isoformat()
            )

        # Get contract for this phase
        contract_key = f"phase{phase}_output"
        if contract_key not in self.contracts.get("contracts", {}):
            warnings.append(f"No contract defined for phase {phase}")
        else:
            # Validate against schema
            contract = self.contracts["contracts"][contract_key]
            schema = contract.get("schema", {})

            # Load phase outputs
            phase_data = self._load_phase_outputs(phase_dir)

            # Validate using jsonschema
            try:
                jsonschema.validate(phase_data, schema)
            except jsonschema.exceptions.ValidationError as e:
                errors.append(f"Schema validation failed: {str(e)}")
            except Exception as e:
                errors.append(f"Validation error: {str(e)}")

        # Check transition rules
        transition_key = f"phase{phase - 1}_to_phase{phase}" if phase > 1 else None
        if transition_key and transition_key in self.contracts.get("phase_transitions", {}):
            transition = self.contracts["phase_transitions"][transition_key]

            # Check prerequisites
            for prereq in transition.get("prerequisites", []):
                if not self._check_prerequisite(prereq, phase - 1):
                    errors.append(f"Prerequisite not met: {prereq}")

            # Run validations
            for validation in transition.get("validations", []):
                result, error = self._run_validation(validation, phase - 1)
                if not result:
                    errors.append(f"Validation failed: {error}")

        return ValidationResult(
            phase=phase, passed=len(errors) == 0, errors=errors, warnings=warnings, timestamp=datetime.now().isoformat()
        )

    def _load_phase_outputs(self, phase_dir: Path) -> dict:
        """Load all outputs from a phase directory into a dict."""
        outputs = {}

        for file_path in phase_dir.glob("*.md"):
            key = file_path.stem.replace("-", "_")
            outputs[key] = self._parse_markdown_file(file_path)

        for file_path in phase_dir.glob("*.json"):
            key = file_path.stem.replace("-", "_")
            with open(file_path) as f:
                outputs[key] = json.load(f)

        return outputs

    def _parse_markdown_file(self, file_path: Path) -> dict:
        """Parse a markdown file and extract structured data."""
        # Simple implementation - in real version would parse YAML frontmatter
        # and extract structured data from markdown
        return {"file": str(file_path), "exists": True, "size": file_path.stat().st_size}

    def _check_prerequisite(self, prereq: str, phase: int) -> bool:
        """Check if a prerequisite is met."""
        phase_dir = self.project_path / f"outputs/{phase}-{self._get_phase_name(phase)}"

        if prereq == "all_required_outputs_exist":
            # Check if all required files exist
            required_files = self._get_required_files(phase)
            for file_name in required_files:
                if not (phase_dir / file_name).exists():
                    return False
            return True

        # Add more prerequisite checks as needed
        return True

    def _run_validation(self, validation: str, phase: int) -> Tuple[bool, str]:
        """Run a validation rule."""
        # Simple implementation - in real version would evaluate validation expressions
        return True, ""

    def _get_phase_name(self, phase: int) -> str:
        """Get phase name for directory."""
        names = {
            1: "context",
            2: "value",
            3: "capabilities",
            4: "architecture",
            5: "software",
            6: "implementation",
            7: "platform",
        }
        return names.get(phase, f"phase{phase}")

    def _get_required_files(self, phase: int) -> List[str]:
        """Get required output files for a phase."""
        required = {
            1: ["organization-analysis.md", "market-assessment.md", "stakeholder-map.md", "constraints.md"],
            2: ["value-streams-mapping.md", "enterprise-activities.md", "value-definition.md"],
            3: ["domain-classification.md", "subdomain-design.md", "capability-map.md"],
            4: ["architecture-overview.md", "context-map.md", "integration-patterns.md"],
            5: ["api-specifications.md", "domain-models.md", "database-schemas.md"],
            6: ["implementation-plan.md", "module-specifications.md"],
            7: ["deployment-architecture.md", "monitoring-strategy.md"],
        }
        return required.get(phase, [])

    def generate_report(self, phase: int) -> str:
        """Generate a quality gate report for a phase."""
        result = self.validate_phase(phase)

        report = f"# Quality Gate Report - Phase {phase}\n\n"
        report += f"**Date**: {result.timestamp}\n"
        report += f"**Status**: {'✅ PASSED' if result.passed else '❌ FAILED'}\n\n"

        if result.errors:
            report += "## Errors\n\n"
            for error in result.errors:
                report += f"- ❌ {error}\n"
            report += "\n"

        if result.warnings:
            report += "## Warnings\n\n"
            for warning in result.warnings:
                report += f"- ⚠️ {warning}\n"
            report += "\n"

        if result.passed:
            report += "## Next Steps\n\n"
            report += f"Phase {phase} validation passed. You can proceed to Phase {phase + 1}.\n"
        else:
            report += "## Required Actions\n\n"
            report += f"Please address the errors above before proceeding to Phase {phase + 1}.\n"

        return report

    def save_validation_result(self, result: ValidationResult):
        """Save validation result to project."""
        validation_dir = self.project_path / "quality-gates"
        validation_dir.mkdir(exist_ok=True)

        file_path = validation_dir / f"phase{result.phase}-validation.json"
        with open(file_path, "w") as f:
            json.dump(result.to_dict(), f, indent=2)
