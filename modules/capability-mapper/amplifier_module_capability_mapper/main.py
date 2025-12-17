#!/usr/bin/env python3
"""
Capability Mapper - Main CLI entry point.

Provides systematic capability decomposition following the ZIGZAG pattern.
"""

import json
from datetime import datetime
from pathlib import Path

import click
import yaml
from pydantic import BaseModel
from pydantic import Field
from rich.console import Console
from rich.prompt import Confirm
from rich.prompt import IntPrompt
from rich.prompt import Prompt
from rich.table import Table
from rich.tree import Tree

console = Console()


class ActivityArea(BaseModel):
    """CL1: Activity Area (活動領域)"""

    id: str
    name: str
    description: str
    value_stream_id: str


class Capability(BaseModel):
    """CL2: Business Capability"""

    id: str
    name: str
    description: str = ""
    activity_area_id: str
    maturity_current: int = Field(ge=1, le=5, default=1)
    maturity_target: int = Field(ge=1, le=5)
    priority: str = Field(default="medium", regex="^(low|medium|high|critical)$")


class Operation(BaseModel):
    """CL3: Business Operation"""

    id: str
    name: str
    capability_id: str
    sla: str = ""
    automation_level: str = Field(default="manual", regex="^(manual|semi-auto|full-auto)$")


class Service(BaseModel):
    """Service derived from Capability"""

    name: str
    capability_id: str
    pattern: str
    operations: list[str]
    events: list[str] = []
    dependencies: list[str] = []


class CapabilityMap(BaseModel):
    """Complete capability map"""

    value_stream: dict[str, str]
    activity_areas: list[ActivityArea] = []
    capabilities: list[Capability] = []
    operations: list[Operation] = []
    services: list[Service] = []
    created_at: datetime = Field(default_factory=datetime.now)


class CapabilityMapper:
    """Main capability mapping engine"""

    def __init__(self, data_dir: Path = Path("./capability_data")):
        self.data_dir = data_dir
        self.data_dir.mkdir(exist_ok=True)
        self.current_map: CapabilityMap | None = None
        self._load_or_create_map()

    def _load_or_create_map(self):
        """Load existing map or create new"""
        map_file = self.data_dir / "capability_map.yaml"
        if map_file.exists():
            with open(map_file) as f:
                data = yaml.safe_load(f)
                self.current_map = CapabilityMap(**data)
        else:
            self.current_map = CapabilityMap(value_stream={})

    def save_map(self):
        """Save current map"""
        if not self.current_map:
            return

        map_file = self.data_dir / "capability_map.yaml"
        with open(map_file, "w", encoding="utf-8") as f:
            yaml.dump(self.current_map.model_dump(mode="json"), f, allow_unicode=True, sort_keys=False)

    def decompose_value_stream(self, value_stream_name: str):
        """ZIGZAG pattern decomposition"""
        console.print(f"\n[bold blue]価値ストリームの分解: {value_stream_name}[/bold blue]\n")

        # Value Stream
        vs_id = f"VS-{len(self.current_map.value_stream) + 1:03d}"
        self.current_map.value_stream = {
            "id": vs_id,
            "name": value_stream_name,
            "description": Prompt.ask("価値ストリームの説明"),
        }

        # CL1: Activity Areas
        console.print("\n[bold]CL1: 活動領域 (Activity Areas) の定義[/bold]")
        console.print("この価値を実現するための主要な活動領域を定義します。")

        num_areas = IntPrompt.ask("活動領域の数", default=3, min_value=1, max_value=10)

        for i in range(num_areas):
            console.print(f"\n[cyan]活動領域 {i + 1}:[/cyan]")
            area = ActivityArea(
                id=f"AA-{len(self.current_map.activity_areas) + 1:03d}",
                name=Prompt.ask("活動領域名"),
                description=Prompt.ask("説明"),
                value_stream_id=vs_id,
            )
            self.current_map.activity_areas.append(area)

            # CL2: Capabilities for this area
            self._define_capabilities(area)

        self.save_map()
        console.print("\n[green]✓ 価値ストリームの分解が完了しました[/green]")

    def _define_capabilities(self, area: ActivityArea):
        """Define capabilities for an activity area"""
        console.print(f"\n[bold]CL2: {area.name} のケイパビリティ定義[/bold]")

        num_caps = IntPrompt.ask("ケイパビリティ数", default=2, min_value=1, max_value=5)

        for i in range(num_caps):
            console.print(f"\n[cyan]ケイパビリティ {i + 1}:[/cyan]")

            cap = Capability(
                id=f"BC-{len(self.current_map.capabilities) + 1:03d}",
                name=Prompt.ask("ケイパビリティ名"),
                description=Prompt.ask("説明", default=""),
                activity_area_id=area.id,
                maturity_current=IntPrompt.ask("現在の成熟度 (1-5)", default=2, min_value=1, max_value=5),
                maturity_target=IntPrompt.ask("目標成熟度 (1-5)", default=4, min_value=1, max_value=5),
                priority=Prompt.ask("優先度", default="medium", choices=["low", "medium", "high", "critical"]),
            )
            self.current_map.capabilities.append(cap)

            # CL3: Operations for this capability
            if Confirm.ask("このケイパビリティのオペレーションを定義しますか？", default=True):
                self._define_operations(cap)

    def _define_operations(self, capability: Capability):
        """Define operations for a capability"""
        console.print(f"\n[bold]CL3: {capability.name} のオペレーション定義[/bold]")

        num_ops = IntPrompt.ask("オペレーション数", default=2, min_value=1, max_value=5)

        for i in range(num_ops):
            op = Operation(
                id=f"BO-{len(self.current_map.operations) + 1:03d}",
                name=Prompt.ask(f"オペレーション {i + 1} の名前"),
                capability_id=capability.id,
                sla=Prompt.ask("SLA", default=""),
                automation_level=Prompt.ask(
                    "自動化レベル", default="manual", choices=["manual", "semi-auto", "full-auto"]
                ),
            )
            self.current_map.operations.append(op)

    def visualize_map(self, format: str = "tree"):
        """Visualize capability map"""
        if not self.current_map or not self.current_map.value_stream:
            console.print("[red]ケイパビリティマップが存在しません[/red]")
            return

        if format == "tree":
            self._visualize_tree()
        elif format == "mermaid":
            self._visualize_mermaid()
        else:
            console.print(f"[red]未対応の形式: {format}[/red]")

    def _visualize_tree(self):
        """Tree visualization"""
        vs = self.current_map.value_stream
        tree = Tree(f"[bold blue]{vs['name']}[/bold blue] ({vs['id']})")

        # Group by activity areas
        for area in self.current_map.activity_areas:
            area_branch = tree.add(f"[yellow]{area.name}[/yellow] ({area.id})")

            # Add capabilities
            caps = [c for c in self.current_map.capabilities if c.activity_area_id == area.id]
            for cap in caps:
                cap_text = f"[green]{cap.name}[/green] ({cap.id})"
                cap_text += f" [dim]成熟度: {cap.maturity_current}→{cap.maturity_target}[/dim]"
                cap_branch = area_branch.add(cap_text)

                # Add operations
                ops = [o for o in self.current_map.operations if o.capability_id == cap.id]
                for op in ops:
                    op_text = f"[cyan]{op.name}[/cyan] ({op.id})"
                    if op.automation_level != "manual":
                        op_text += f" [dim]{op.automation_level}[/dim]"
                    cap_branch.add(op_text)

        console.print(tree)

    def _visualize_mermaid(self):
        """Mermaid diagram output"""
        lines = ["```mermaid", "graph TB"]

        vs = self.current_map.value_stream
        lines.append(f'    VS["{vs["name"]}"]')

        # Activity areas
        for area in self.current_map.activity_areas:
            lines.append(f'    VS --> {area.id}["{area.name}"]')

        # Capabilities
        for cap in self.current_map.capabilities:
            lines.append(f'    {cap.activity_area_id} --> {cap.id}["{cap.name}"]')

        # Operations
        for op in self.current_map.operations:
            lines.append(f'    {op.capability_id} --> {op.id}["{op.name}"]')

        lines.append("```")
        console.print("\n".join(lines))

    def assess_capability(self, capability_id: str | None = None):
        """Assess capability maturity"""
        if capability_id:
            caps = [c for c in self.current_map.capabilities if c.id == capability_id]
        else:
            caps = self.current_map.capabilities

        if not caps:
            console.print("[red]ケイパビリティが見つかりません[/red]")
            return

        table = Table(title="ケイパビリティ成熟度評価")
        table.add_column("ID", style="cyan")
        table.add_column("ケイパビリティ", style="green")
        table.add_column("現在", justify="center")
        table.add_column("目標", justify="center")
        table.add_column("ギャップ", justify="center")
        table.add_column("優先度", justify="center")

        for cap in caps:
            gap = cap.maturity_target - cap.maturity_current
            gap_style = "red" if gap >= 3 else "yellow" if gap >= 2 else "green"
            priority_style = "red" if cap.priority == "critical" else "yellow" if cap.priority == "high" else "white"

            table.add_row(
                cap.id,
                cap.name,
                str(cap.maturity_current),
                str(cap.maturity_target),
                f"[{gap_style}]{gap}[/{gap_style}]",
                f"[{priority_style}]{cap.priority}[/{priority_style}]",
            )

        console.print(table)

    def generate_service(self, capability_id: str, pattern: str = "entity-service"):
        """Generate service from capability"""
        cap = next((c for c in self.current_map.capabilities if c.id == capability_id), None)
        if not cap:
            console.print(f"[red]ケイパビリティ {capability_id} が見つかりません[/red]")
            return

        # Get operations
        ops = [o for o in self.current_map.operations if o.capability_id == capability_id]

        service = Service(
            name=f"{cap.name.replace(' ', '')}Service",
            capability_id=capability_id,
            pattern=pattern,
            operations=[f"{op.name.replace(' ', '_').lower()}" for op in ops],
        )

        # Add CRUD operations based on pattern
        if pattern == "entity-service":
            service.operations.extend(
                [
                    f"create_{cap.name.lower().replace(' ', '_')}",
                    f"get_{cap.name.lower().replace(' ', '_')}",
                    f"update_{cap.name.lower().replace(' ', '_')}",
                    f"delete_{cap.name.lower().replace(' ', '_')}",
                ]
            )
            service.events = [
                f"{cap.name.lower().replace(' ', '_')}.created",
                f"{cap.name.lower().replace(' ', '_')}.updated",
                f"{cap.name.lower().replace(' ', '_')}.deleted",
            ]

        self.current_map.services.append(service)
        self.save_map()

        # Display generated service
        console.print(f"\n[green]✓ サービス生成完了: {service.name}[/green]\n")
        console.print(yaml.dump(service.model_dump(), allow_unicode=True, sort_keys=False))

    def export_map(self, format: str = "yaml"):
        """Export capability map"""
        if not self.current_map:
            console.print("[red]エクスポートするマップがありません[/red]")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if format == "yaml":
            filename = f"capability_map_{timestamp}.yaml"
            with open(filename, "w", encoding="utf-8") as f:
                yaml.dump(self.current_map.model_dump(mode="json"), f, allow_unicode=True, sort_keys=False)
        elif format == "json":
            filename = f"capability_map_{timestamp}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.current_map.model_dump(mode="json"), f, ensure_ascii=False, indent=2)
        else:
            console.print(f"[red]未対応の形式: {format}[/red]")
            return

        console.print(f"[green]✓ エクスポート完了: {filename}[/green]")


@click.group()
@click.pass_context
def cli(ctx):
    """Capability Mapper - Parasol V5 Phase 3 capability decomposition tool"""
    ctx.obj = CapabilityMapper()


@cli.command()
@click.option("--value-stream", "-v", required=True, help="Value stream name")
@click.pass_obj
def decompose(mapper: CapabilityMapper, value_stream: str):
    """Decompose value stream into capabilities"""
    mapper.decompose_value_stream(value_stream)


@cli.command()
@click.option("--format", "-f", type=click.Choice(["tree", "mermaid"]), default="tree")
@click.pass_obj
def visualize(mapper: CapabilityMapper, format: str):
    """Visualize capability map"""
    mapper.visualize_map(format)


@cli.command()
@click.option("--capability", "-c", help="Specific capability ID")
@click.pass_obj
def assess(mapper: CapabilityMapper, capability: str | None):
    """Assess capability maturity"""
    mapper.assess_capability(capability)


@cli.command("to-service")
@click.argument("capability_id")
@click.option(
    "--pattern",
    "-p",
    type=click.Choice(["entity-service", "task-service", "utility-service"]),
    default="entity-service",
)
@click.pass_obj
def to_service(mapper: CapabilityMapper, capability_id: str, pattern: str):
    """Generate service from capability"""
    mapper.generate_service(capability_id, pattern)


@cli.command()
@click.option("--format", "-f", type=click.Choice(["yaml", "json"]), default="yaml")
@click.pass_obj
def export(mapper: CapabilityMapper, format: str):
    """Export capability map"""
    mapper.export_map(format)


if __name__ == "__main__":
    cli()
