"""Value Exploration CLI for Parasol V5 value-driven design."""

import json
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from pathlib import Path

import click
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.prompt import Prompt
from rich.table import Table

console = Console()


@dataclass
class ValueDefinition:
    """A discovered business value."""

    id: str
    name: str
    description: str
    level: int  # VL1, VL2, VL3
    current_state: str
    target_state: str
    metrics: list[str] = field(default_factory=list)
    stakeholders: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    nine_dimensions: dict[str, int] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ValueStream:
    """A value stream connecting multiple values."""

    id: str
    name: str
    description: str
    values: list[str]  # Value IDs
    flow: list[dict]  # Value flow steps
    kpis: list[str] = field(default_factory=list)


class ValueExplorer:
    """Core value exploration engine."""

    NINE_DIMENSIONS = [
        ("Impact", "影響力 - どれだけの変化を生むか"),
        ("Velocity", "速度 - どれだけ速く価値を届けるか"),
        ("Messaging", "伝達力 - 価値をどう伝えるか"),
        ("Reach", "到達力 - どこまで価値を広げるか"),
        ("Sentiment", "感情価値 - どんな感情を生むか"),
        ("Metrics", "測定可能性 - 価値をどう測るか"),
        ("Balance", "均衡 - 各価値のバランス"),
        ("Depth", "深度 - 価値の深さと持続性"),
        ("Foundation", "基盤 - 価値の土台の強さ"),
    ]

    VALUE_QUESTIONS = {
        "business": [
            "この事業の存在意義は何ですか？",
            "競合との最大の差別化要因は何ですか？",
            "顧客が得る最も重要な価値は何ですか？",
            "3年後にどうなっていたいですか？",
        ],
        "stakeholder": [
            "最も重要なステークホルダーは誰ですか？",
            "各ステークホルダーが求める価値は何ですか？",
            "ステークホルダー間で相反する要求はありますか？",
        ],
        "operational": [
            "現在の最大のペインポイントは何ですか？",
            "改善したら最もインパクトがある領域は？",
            "測定している重要な指標は何ですか？",
        ],
    }

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.values: list[ValueDefinition] = []
        self.streams: list[ValueStream] = []

    def discover_values_interactive(self) -> list[ValueDefinition]:
        """Interactive value discovery through guided questions."""
        console.print(Panel("[bold blue]価値探索セッション[/bold blue]", subtitle="Parasol V5"))

        discovered = []

        for category, questions in self.VALUE_QUESTIONS.items():
            console.print(f"\n[bold cyan]【{category.upper()}】[/bold cyan]")

            for q in questions:
                answer = Prompt.ask(f"  {q}")
                if answer.strip():
                    # Extract potential values from answer
                    if Confirm.ask("  この回答から価値を抽出しますか？"):
                        value = self._create_value_from_answer(category, q, answer)
                        if value:
                            discovered.append(value)
                            console.print(f"  [green]✓ 価値を追加: {value.name}[/green]")

        self.values.extend(discovered)
        return discovered

    def _create_value_from_answer(self, category: str, question: str, answer: str) -> ValueDefinition | None:
        """Create a value definition from user's answer."""
        name = Prompt.ask("  価値の名前", default=answer[:30] if len(answer) > 30 else answer)
        description = Prompt.ask("  説明", default=answer)

        level_str = Prompt.ask("  価値レベル", choices=["1", "2", "3"], default="2")
        level = int(level_str)

        current = Prompt.ask("  現状")
        target = Prompt.ask("  目標")

        value_id = f"VAL-{len(self.values) + 1:03d}"

        return ValueDefinition(
            id=value_id,
            name=name,
            description=description,
            level=level,
            current_state=current,
            target_state=target,
            stakeholders=[category],
        )

    def analyze_nine_dimensions(self, value: ValueDefinition) -> dict[str, int]:
        """Analyze a value across 9 dimensions."""
        console.print(f"\n[bold]九次元分析: {value.name}[/bold]")
        console.print("[dim]各次元を1-5で評価してください[/dim]\n")

        scores = {}
        for dim_en, dim_ja in self.NINE_DIMENSIONS:
            score_str = Prompt.ask(f"  {dim_ja}", choices=["1", "2", "3", "4", "5"], default="3")
            scores[dim_en] = int(score_str)

        value.nine_dimensions = scores
        return scores

    def create_value_stream(self, values: list[ValueDefinition]) -> ValueStream | None:
        """Create a value stream from selected values."""
        if len(values) < 2:
            console.print("[yellow]価値ストリームには2つ以上の価値が必要です[/yellow]")
            return None

        console.print("\n[bold]価値ストリーム作成[/bold]")

        name = Prompt.ask("ストリーム名")
        description = Prompt.ask("説明")

        # Show available values
        table = Table(title="利用可能な価値")
        table.add_column("ID")
        table.add_column("名前")
        table.add_column("レベル")

        for v in values:
            table.add_row(v.id, v.name, f"VL{v.level}")

        console.print(table)

        value_ids = Prompt.ask("含める価値ID（カンマ区切り）").split(",")
        value_ids = [vid.strip() for vid in value_ids]

        stream_id = f"VS-{len(self.streams) + 1:03d}"

        stream = ValueStream(
            id=stream_id,
            name=name,
            description=description,
            values=value_ids,
            flow=[],
        )

        self.streams.append(stream)
        return stream

    def display_value_hierarchy(self) -> None:
        """Display discovered values as a hierarchy."""
        console.print("\n[bold blue]価値階層[/bold blue]\n")

        for level in [1, 2, 3]:
            level_values = [v for v in self.values if v.level == level]
            if level_values:
                console.print(f"[bold]VL{level}[/bold]")
                for v in level_values:
                    indent = "  " * level
                    console.print(f"{indent}├── {v.id}: {v.name}")
                    console.print(f"{indent}│   現状: {v.current_state}")
                    console.print(f"{indent}│   目標: {v.target_state}")

    def save(self, filename: str = "values.yaml") -> Path:
        """Save discovered values to file."""
        output_path = self.output_dir / filename

        data = {
            "values": [asdict(v) for v in self.values],
            "streams": [asdict(s) for s in self.streams],
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "total_values": len(self.values),
                "total_streams": len(self.streams),
            },
        }

        with open(output_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

        console.print(f"[green]✓ 保存完了: {output_path}[/green]")
        return output_path

    def load(self, filename: str = "values.yaml") -> bool:
        """Load values from file."""
        input_path = self.output_dir / filename

        if not input_path.exists():
            return False

        with open(input_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        self.values = [ValueDefinition(**v) for v in data.get("values", [])]
        self.streams = [ValueStream(**s) for s in data.get("streams", [])]

        return True


@click.group()
@click.option("--output", "-o", default=".data/values", help="出力ディレクトリ")
@click.pass_context
def cli(ctx: click.Context, output: str) -> None:
    """価値探索CLI - Parasol V5 価値駆動設計支援ツール"""
    ctx.ensure_object(dict)
    ctx.obj["explorer"] = ValueExplorer(Path(output))


@cli.command()
@click.pass_context
def discover(ctx: click.Context) -> None:
    """対話型価値探索セッションを開始"""
    explorer: ValueExplorer = ctx.obj["explorer"]
    explorer.load()

    values = explorer.discover_values_interactive()

    if values:
        console.print(f"\n[bold green]{len(values)}個の価値を発見しました[/bold green]")
        explorer.display_value_hierarchy()
        explorer.save()


@cli.command()
@click.argument("value_id")
@click.pass_context
def analyze(ctx: click.Context, value_id: str) -> None:
    """指定した価値の九次元分析を実行"""
    explorer: ValueExplorer = ctx.obj["explorer"]

    if not explorer.load():
        console.print("[red]価値データが見つかりません。先に discover を実行してください[/red]")
        return

    value = next((v for v in explorer.values if v.id == value_id), None)
    if not value:
        console.print(f"[red]価値 {value_id} が見つかりません[/red]")
        return

    scores = explorer.analyze_nine_dimensions(value)
    explorer.save()

    # Display radar-like summary
    console.print("\n[bold]分析結果[/bold]")
    for dim, score in scores.items():
        bar = "█" * score + "░" * (5 - score)
        console.print(f"  {dim:12} [{bar}] {score}/5")


@cli.command()
@click.pass_context
def stream(ctx: click.Context) -> None:
    """価値ストリームを作成"""
    explorer: ValueExplorer = ctx.obj["explorer"]

    if not explorer.load():
        console.print("[red]価値データが見つかりません。先に discover を実行してください[/red]")
        return

    if len(explorer.values) < 2:
        console.print("[yellow]価値ストリーム作成には2つ以上の価値が必要です[/yellow]")
        return

    stream = explorer.create_value_stream(explorer.values)
    if stream:
        console.print(f"[green]✓ 価値ストリーム作成: {stream.name}[/green]")
        explorer.save()


@cli.command()
@click.pass_context
def show(ctx: click.Context) -> None:
    """発見した価値を表示"""
    explorer: ValueExplorer = ctx.obj["explorer"]

    if not explorer.load():
        console.print("[yellow]価値データがありません[/yellow]")
        return

    explorer.display_value_hierarchy()

    if explorer.streams:
        console.print("\n[bold blue]価値ストリーム[/bold blue]")
        for s in explorer.streams:
            console.print(f"  {s.id}: {s.name}")
            console.print(f"       含む価値: {', '.join(s.values)}")


@cli.command()
@click.option("--format", "-f", type=click.Choice(["yaml", "json"]), default="yaml")
@click.pass_context
def export(ctx: click.Context, format: str) -> None:
    """価値データをエクスポート"""
    explorer: ValueExplorer = ctx.obj["explorer"]

    if not explorer.load():
        console.print("[yellow]価値データがありません[/yellow]")
        return

    if format == "json":
        output_path = explorer.output_dir / "values.json"
        data = {
            "values": [asdict(v) for v in explorer.values],
            "streams": [asdict(s) for s in explorer.streams],
        }
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    else:
        output_path = explorer.save("values-export.yaml")

    console.print(f"[green]✓ エクスポート完了: {output_path}[/green]")


def get_tool_callable():
    """Return the tool callable for Amplifier."""
    return cli


if __name__ == "__main__":
    cli()
