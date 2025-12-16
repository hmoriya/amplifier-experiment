"""Main entry point for Parasol CLI module."""

import click
from pathlib import Path
import yaml
from datetime import datetime


class ParasolCLI:
    """Parasol DDD Framework CLI for managing enterprise projects through 7 phases."""

    def __init__(self):
        self.phases = {
            1: "Context (Organization, Market, Stakeholders)",
            2: "Value (Value Streams, Enterprise Activities)",
            3: "Capabilities (Domain Classification, Subdomains)",
            4: "Architecture (Application Design, Integration)",
            5: "Software Design (APIs, Domain Language)",
            6: "Implementation (Code Generation)",
            7: "Platform (Deployment, Monitoring)",
        }

    @click.group()
    def cli(self):
        """Parasol DDD Framework CLI."""
        pass

    @cli.command()
    @click.argument("project_name")
    @click.option("--path", "-p", default=".", help="Project path")
    def init(self, project_name: str, path: str):
        """Initialize a new Parasol project."""
        project_path = Path(path) / project_name
        project_path.mkdir(parents=True, exist_ok=True)

        # Create parasol.yaml
        config = {
            "project": {
                "name": project_name,
                "version": "0.1.0",
                "created": datetime.now().isoformat(),
                "phases_completed": [],
            },
            "context": {"industry": "", "organization": "", "market_segment": ""},
        }

        with open(project_path / "parasol.yaml", "w") as f:
            yaml.dump(config, f, default_flow_style=False)

        # Create phase directories
        for phase in range(1, 8):
            phase_dir = project_path / f"outputs/{phase}-{self._get_phase_name(phase)}"
            phase_dir.mkdir(parents=True, exist_ok=True)

        click.echo(f"✓ Initialized Parasol project: {project_name}")
        click.echo(f"  Location: {project_path}")
        click.echo("  Next: Run 'parasol phase 1' to begin context analysis")

    @cli.command()
    @click.argument("phase_number", type=int)
    @click.option("--project", "-p", default=".", help="Project path")
    def phase(self, phase_number: int, project: str):
        """Execute a specific Parasol phase."""
        if phase_number not in self.phases:
            click.echo(f"Error: Invalid phase {phase_number}. Valid phases: 1-7", err=True)
            return

        project_path = Path(project)
        if not (project_path / "parasol.yaml").exists():
            click.echo("Error: Not a Parasol project (parasol.yaml not found)", err=True)
            return

        click.echo(f"Executing Phase {phase_number}: {self.phases[phase_number]}")
        click.echo("Use Amplifier agents to complete this phase:")
        click.echo(f"  amplifier run 'Execute Parasol phase {phase_number}'")

    @cli.command()
    @click.option("--project", "-p", default=".", help="Project path")
    def status(self, project: str):
        """Show project status."""
        project_path = Path(project)
        config_file = project_path / "parasol.yaml"

        if not config_file.exists():
            click.echo("Error: Not a Parasol project", err=True)
            return

        with open(config_file) as f:
            config = yaml.safe_load(f)

        click.echo(f"Project: {config['project']['name']}")
        click.echo(f"Version: {config['project']['version']}")
        click.echo(f"Created: {config['project']['created']}")
        click.echo("\nPhases:")

        completed = set(config["project"].get("phases_completed", []))
        for phase_num, phase_desc in self.phases.items():
            status = "✓" if phase_num in completed else "○"
            click.echo(f"  {status} Phase {phase_num}: {phase_desc}")

    def _get_phase_name(self, phase: int) -> str:
        """Get simplified phase name for directory."""
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


# Amplifier module entry point
def get_tool_callable():
    """Return the tool callable for Amplifier."""
    cli = ParasolCLI()
    return cli.cli


if __name__ == "__main__":
    cli = ParasolCLI()
    cli.cli()
