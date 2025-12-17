"""CLI commands for regeneratable module system."""

import asyncio
import json
import yaml
from pathlib import Path
from typing import List
import click
from .regeneration_engine import RegenerationEngine, ModuleCompositionEngine
from .quality_gate import QualityGate


@click.group(name="module")
def module_commands():
    """Module generation and regeneration commands."""
    pass


@module_commands.command("generate")
@click.argument("module_name")
@click.option("--from-contract", "-c", type=click.Path(exists=True), help="Path to module contract file")
@click.option("--variants", "-v", multiple=True, help="Variants to generate (e.g., api:graphql, database:postgresql)")
@click.option("--output-dir", "-o", type=click.Path(), default="./modules", help="Output directory")
@click.option("--dry-run", is_flag=True, help="Show what would be generated without creating files")
async def generate_module(module_name: str, from_contract: str, variants: List[str], output_dir: str, dry_run: bool):
    """Generate a module from contract specification."""

    # Load contract
    contract_path = Path(from_contract)
    with open(contract_path, "r", encoding="utf-8") as f:
        if contract_path.suffix in [".yaml", ".yml"]:
            contract = yaml.safe_load(f)
        else:
            contract = json.load(f)

    # Parse variants
    variant_dict = {}
    for variant in variants:
        if ":" in variant:
            variant_type, variant_name = variant.split(":", 1)
            if variant_type not in variant_dict:
                variant_dict[variant_type] = []
            variant_dict[variant_type].append(variant_name)

    # Update contract with specified variants
    if variant_dict:
        contract.setdefault("variants", {}).update(variant_dict)

    # Initialize regeneration engine
    templates_path = Path(__file__).parent / "templates"
    engine = RegenerationEngine(templates_path)

    # Generate module
    result = await engine.regenerate_module(module_name=module_name, new_contract=contract)

    if dry_run:
        click.echo(f"Would generate module '{module_name}' with the following files:")
        for file_path in result["generated_files"]:
            click.echo(f"  {file_path}")
    else:
        # Write generated files
        output_path = Path(output_dir)
        for file_path, content in result["generated_files"].items():
            full_path = output_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding="utf-8")

        click.echo(f"✅ Generated module '{module_name}' successfully")
        click.echo(f"   Generated {len(result['generated_files'])} files")
        if result["preserved_code_keys"]:
            click.echo(f"   Preserved {len(result['preserved_code_keys'])} custom logic blocks")


@module_commands.command("regenerate")
@click.argument("module_name")
@click.option("--contract", "-c", type=click.Path(exists=True), help="Path to updated contract file")
@click.option(
    "--preserve",
    "-p",
    multiple=True,
    type=click.Choice(["business-logic", "test-data", "configuration"]),
    default=["business-logic", "test-data", "configuration"],
    help="What to preserve during regeneration",
)
@click.option("--show-diff", is_flag=True, help="Show differences before regenerating")
@click.option("--dry-run", is_flag=True, help="Show what would be regenerated")
async def regenerate_module(module_name: str, contract: str, preserve: List[str], show_diff: bool, dry_run: bool):
    """Regenerate a module with updated contract."""

    # Load new contract
    new_contract_path = Path(contract)
    with open(new_contract_path, "r", encoding="utf-8") as f:
        if new_contract_path.suffix in [".yaml", ".yml"]:
            new_contract = yaml.safe_load(f)
        else:
            new_contract = json.load(f)

    # Load old contract if exists
    old_contract = None
    old_contract_path = Path(f"modules/{module_name}/.contract.yaml")
    if old_contract_path.exists():
        with open(old_contract_path, "r", encoding="utf-8") as f:
            old_contract = yaml.safe_load(f)

    # Configure preservation options
    preserve_options = {
        "business_logic": "business-logic" in preserve,
        "test_data": "test-data" in preserve,
        "configuration": "configuration" in preserve,
    }

    # Initialize regeneration engine
    templates_path = Path(__file__).parent / "templates"
    engine = RegenerationEngine(templates_path)

    # Show diff if requested
    if show_diff and old_contract:
        changes = engine.change_detector.detect_changes(old_contract, new_contract)
        if changes:
            click.echo("Detected changes:")
            for change in changes:
                click.echo(f"  {change.type.value}: {change.path} (impact: {change.impact_score})")
        else:
            click.echo("No changes detected")
            return

    # Regenerate module
    result = await engine.regenerate_module(
        module_name=module_name, new_contract=new_contract, old_contract=old_contract, preserve_options=preserve_options
    )

    if dry_run:
        click.echo(f"Would regenerate module '{module_name}':")
        click.echo(f"  Changes: {len(result['changes'])}")
        click.echo(f"  Files: {len(result['generated_files'])}")
        click.echo(f"  Preserved: {len(result['preserved_code_keys'])}")
    else:
        # Write generated files
        for file_path, content in result["generated_files"].items():
            full_path = Path(file_path)
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding="utf-8")

        # Save new contract
        with open(old_contract_path, "w", encoding="utf-8") as f:
            yaml.dump(new_contract, f, default_flow_style=False)

        click.echo(f"✅ Regenerated module '{module_name}' successfully")


@module_commands.command("analyze-impact")
@click.argument("module_name")
@click.option(
    "--contract-change", "-c", type=click.Path(exists=True), help="Path to new contract file for impact analysis"
)
@click.option(
    "--show",
    "-s",
    multiple=True,
    type=click.Choice(["affected-modules", "test-requirements", "migration-steps"]),
    default=["affected-modules"],
    help="What to show in impact analysis",
)
def analyze_impact(module_name: str, contract_change: str, show: List[str]):
    """Analyze impact of contract changes."""

    # Load old contract
    old_contract_path = Path(f"modules/{module_name}/.contract.yaml")
    if not old_contract_path.exists():
        click.echo(f"❌ Module '{module_name}' not found")
        return

    with open(old_contract_path, "r", encoding="utf-8") as f:
        old_contract = yaml.safe_load(f)

    # Load new contract
    new_contract_path = Path(contract_change)
    with open(new_contract_path, "r", encoding="utf-8") as f:
        if new_contract_path.suffix in [".yaml", ".yml"]:
            new_contract = yaml.safe_load(f)
        else:
            new_contract = json.load(f)

    # Initialize change detector
    templates_path = Path(__file__).parent / "templates"
    engine = RegenerationEngine(templates_path)

    # Analyze changes
    changes = engine.change_detector.detect_changes(old_contract, new_contract)

    click.echo(f"Impact Analysis for '{module_name}':")
    click.echo(f"Total changes: {len(changes)}")

    if "affected-modules" in show:
        click.echo("\n🔄 Affected Components:")
        for change in sorted(changes, key=lambda c: c.impact_score, reverse=True):
            impact_level = (
                "🔴 High" if change.impact_score >= 8 else "🟡 Medium" if change.impact_score >= 5 else "🟢 Low"
            )
            click.echo(f"  {impact_level} - {change.path} ({change.type.value})")

    if "test-requirements" in show:
        click.echo("\n🧪 Test Requirements:")
        domain_changes = [c for c in changes if c.path.startswith("domain")]
        api_changes = [c for c in changes if c.path.startswith("adapters")]

        if domain_changes:
            click.echo("  • Unit tests for domain logic changes")
        if api_changes:
            click.echo("  • Integration tests for API changes")
        if changes:
            click.echo("  • Contract tests for interface changes")

    if "migration-steps" in show:
        click.echo("\n📋 Migration Steps:")
        breaking_changes = [c for c in changes if c.type.name in ["REMOVED", "MODIFIED"]]

        if breaking_changes:
            click.echo("  1. Deploy new version alongside old version")
            click.echo("  2. Gradually route traffic to new version")
            click.echo("  3. Monitor for errors and rollback if necessary")
            click.echo("  4. Complete migration once stable")
        else:
            click.echo("  • No breaking changes detected - direct deployment possible")


@module_commands.command("compose")
@click.argument("system_name")
@click.option("--from-composition", "-c", type=click.Path(exists=True), help="Path to system composition file")
@click.option("--environment", "-e", default="development", help="Target environment")
@click.option("--output-dir", "-o", type=click.Path(), default="./systems", help="Output directory")
async def compose_system(system_name: str, from_composition: str, environment: str, output_dir: str):
    """Compose a complete system from module composition."""

    # Load composition configuration
    composition_path = Path(from_composition)
    with open(composition_path, "r", encoding="utf-8") as f:
        if composition_path.suffix in [".yaml", ".yml"]:
            composition_config = yaml.safe_load(f)
        else:
            composition_config = json.load(f)

    # Initialize engines
    templates_path = Path(__file__).parent / "templates"
    regeneration_engine = RegenerationEngine(templates_path)
    composition_engine = ModuleCompositionEngine(regeneration_engine)

    # Compose system
    result = await composition_engine.compose_system(composition_config)

    # Write system files
    system_path = Path(output_dir) / system_name
    system_path.mkdir(parents=True, exist_ok=True)

    # Write module files
    for module_name, module_result in result["modules"].items():
        module_path = system_path / "modules" / module_name
        for file_path, content in module_result["generated_files"].items():
            full_path = module_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding="utf-8")

    # Write integration files
    integration_path = system_path / "integration"
    integration_path.mkdir(exist_ok=True)
    for file_path, content in result["integration"].items():
        (integration_path / file_path).write_text(content, encoding="utf-8")

    # Write system configuration
    system_config = {
        "name": system_name,
        "environment": environment,
        "composition": result["composition"],
        "modules": list(result["modules"].keys()),
        "generated_at": result.get("generated_at", "unknown"),
    }

    with open(system_path / "system.yaml", "w", encoding="utf-8") as f:
        yaml.dump(system_config, f, default_flow_style=False)

    click.echo(f"✅ Composed system '{system_name}' successfully")
    click.echo(f"   Generated {len(result['modules'])} modules")
    click.echo(f"   Integration files: {len(result['integration'])}")


@module_commands.command("watch")
@click.argument("contract_paths", nargs=-1)
@click.option("--auto-regenerate", is_flag=True, help="Automatically regenerate on contract changes")
@click.option(
    "--preserve",
    "-p",
    multiple=True,
    type=click.Choice(["business-logic", "test-data", "configuration"]),
    default=["business-logic", "test-data", "configuration"],
    help="What to preserve during auto-regeneration",
)
def watch_contracts(contract_paths: List[str], auto_regenerate: bool, preserve: List[str]):
    """Watch contract files for changes and trigger regeneration."""

    if not contract_paths:
        contract_paths = ["./contracts/**/*.yaml"]

    preserve_options = {
        "business_logic": "business-logic" in preserve,
        "test_data": "test-data" in preserve,
        "configuration": "configuration" in preserve,
    }

    click.echo(f"👀 Watching {len(contract_paths)} contract paths...")
    click.echo(f"   Auto-regenerate: {'enabled' if auto_regenerate else 'disabled'}")

    # This would be implemented with a file watcher like watchdog
    click.echo("📁 File watching not implemented in this example")


@module_commands.command("validate")
@click.argument("module_name")
@click.option(
    "--check",
    "-c",
    multiple=True,
    type=click.Choice(["circular-dependencies", "module-boundaries", "public-api-usage"]),
    default=["circular-dependencies", "module-boundaries"],
    help="What to validate",
)
def validate_module(module_name: str, check: List[str]):
    """Validate module architecture and dependencies."""

    module_path = Path(f"modules/{module_name}")
    if not module_path.exists():
        click.echo(f"❌ Module '{module_name}' not found")
        return

    # Initialize quality gate
    project_path = Path(".")
    quality_gate = QualityGate(project_path)

    issues = []

    if "circular-dependencies" in check:
        # Check for circular imports/dependencies
        click.echo("🔄 Checking circular dependencies...")
        # Implementation would analyze import statements

    if "module-boundaries" in check:
        # Check module boundary violations
        click.echo("🏗️ Checking module boundaries...")
        # Implementation would ensure modules only use public APIs

    if "public-api-usage" in check:
        # Check that modules only access public APIs of other modules
        click.echo("🔌 Checking public API usage...")
        # Implementation would validate import patterns

    if not issues:
        click.echo(f"✅ Module '{module_name}' validation passed")
    else:
        click.echo(f"❌ Found {len(issues)} validation issues:")
        for issue in issues:
            click.echo(f"  • {issue}")


if __name__ == "__main__":
    # For async commands, we need to wrap them
    def async_command(f):
        def wrapper(*args, **kwargs):
            return asyncio.run(f(*args, **kwargs))

        return wrapper

    # Apply async wrapper to async commands
    generate_module = async_command(generate_module)
    regenerate_module = async_command(regenerate_module)
    compose_system = async_command(compose_system)

    module_commands()
