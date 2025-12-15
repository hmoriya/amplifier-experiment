"""Main entry point for Knowledge Synthesis module."""

import click
from pathlib import Path
from typing import List, Optional, Dict, Any
import json
from datetime import datetime
import networkx as nx
from dataclasses import dataclass, asdict


@dataclass
class Concept:
    """Represents an extracted concept."""
    id: str
    name: str
    description: str
    source: str
    confidence: float
    extracted_at: str
    relationships: List[str]


@dataclass
class Insight:
    """Represents a synthesized insight."""
    id: str
    title: str
    description: str
    concepts: List[str]
    synthesis_type: str
    confidence: float
    generated_at: str


class KnowledgeSynthesisCLI:
    """Knowledge Synthesis CLI for extracting and synthesizing concepts from documents."""
    
    def __init__(self):
        self.output_dir = Path(".data/knowledge")
        self.graph_file = self.output_dir / "knowledge_graph.json"
    
    @click.group()
    def cli(self):
        """Knowledge Synthesis CLI for concept extraction and insight generation."""
        pass
    
    @cli.command()
    @click.argument('directory', type=click.Path(exists=True))
    @click.option('--output', '-o', default='.data/knowledge', help='Output directory')
    @click.option('--format', '-f', type=click.Choice(['json', 'markdown']), default='json')
    def extract(self, directory: str, output: str, format: str):
        """Extract concepts from documents in a directory."""
        input_path = Path(directory)
        output_path = Path(output)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Find documents
        doc_patterns = ['*.md', '*.txt', '*.pdf']
        documents = []
        for pattern in doc_patterns:
            documents.extend(input_path.rglob(pattern))
        
        click.echo(f"Found {len(documents)} documents to process")
        
        # Simulate extraction (in real implementation, would use AI agents)
        concepts = []
        for i, doc in enumerate(documents):
            concept = Concept(
                id=f"concept_{i}",
                name=f"Concept from {doc.name}",
                description=f"Key concept extracted from {doc}",
                source=str(doc),
                confidence=0.85,
                extracted_at=datetime.now().isoformat(),
                relationships=[]
            )
            concepts.append(concept)
        
        # Save results
        if format == 'json':
            with open(output_path / 'concepts.json', 'w') as f:
                json.dump([asdict(c) for c in concepts], f, indent=2)
        else:
            with open(output_path / 'concepts.md', 'w') as f:
                f.write("# Extracted Concepts\n\n")
                for c in concepts:
                    f.write(f"## {c.name}\n")
                    f.write(f"- **Source**: {c.source}\n")
                    f.write(f"- **Confidence**: {c.confidence}\n")
                    f.write(f"- **Description**: {c.description}\n\n")
        
        click.echo(f"✓ Extracted {len(concepts)} concepts")
        click.echo(f"  Output: {output_path}")
    
    @cli.command()
    @click.option('--input', '-i', default='.data/knowledge', help='Input directory')
    @click.option('--output', '-o', default='.data/knowledge', help='Output directory')
    @click.option('--type', '-t', type=click.Choice(['convergence', 'divergence', 'emergence']), 
                  default='convergence')
    def synthesize(self, input: str, output: str, type: str):
        """Synthesize insights from extracted concepts."""
        input_path = Path(input)
        output_path = Path(output)
        
        # Load concepts
        concepts_file = input_path / 'concepts.json'
        if not concepts_file.exists():
            click.echo("Error: No concepts found. Run 'extract' first.", err=True)
            return
        
        with open(concepts_file) as f:
            concepts_data = json.load(f)
        
        click.echo(f"Synthesizing {type} insights from {len(concepts_data)} concepts")
        
        # Simulate synthesis
        insights = []
        insight = Insight(
            id="insight_1",
            title=f"{type.capitalize()} Pattern Detected",
            description=f"Multiple concepts show {type} patterns suggesting new understanding",
            concepts=[c['id'] for c in concepts_data[:3]],
            synthesis_type=type,
            confidence=0.75,
            generated_at=datetime.now().isoformat()
        )
        insights.append(insight)
        
        # Save insights
        with open(output_path / 'insights.json', 'w') as f:
            json.dump([asdict(i) for i in insights], f, indent=2)
        
        click.echo(f"✓ Generated {len(insights)} insights")
        click.echo(f"  Output: {output_path / 'insights.json'}")
    
    @cli.command()
    @click.option('--input', '-i', default='.data/knowledge', help='Knowledge directory')
    @click.option('--format', '-f', type=click.Choice(['json', 'graphml', 'gexf']), default='json')
    def build_graph(self, input: str, format: str):
        """Build knowledge graph from concepts and insights."""
        input_path = Path(input)
        
        # Create graph
        G = nx.DiGraph()
        
        # Load concepts
        concepts_file = input_path / 'concepts.json'
        if concepts_file.exists():
            with open(concepts_file) as f:
                concepts = json.load(f)
                for c in concepts:
                    G.add_node(c['id'], **c)
        
        # Load insights
        insights_file = input_path / 'insights.json'
        if insights_file.exists():
            with open(insights_file) as f:
                insights = json.load(f)
                for i in insights:
                    G.add_node(i['id'], **i)
                    # Connect insights to concepts
                    for concept_id in i['concepts']:
                        G.add_edge(i['id'], concept_id, type='synthesized_from')
        
        # Save graph
        if format == 'json':
            data = nx.node_link_data(G)
            with open(input_path / 'knowledge_graph.json', 'w') as f:
                json.dump(data, f, indent=2)
        elif format == 'graphml':
            nx.write_graphml(G, input_path / 'knowledge_graph.graphml')
        else:  # gexf
            nx.write_gexf(G, input_path / 'knowledge_graph.gexf')
        
        click.echo(f"✓ Built knowledge graph")
        click.echo(f"  Nodes: {G.number_of_nodes()}")
        click.echo(f"  Edges: {G.number_of_edges()}")
        click.echo(f"  Output: {input_path / f'knowledge_graph.{format}'}")
    
    @cli.command()
    @click.option('--input', '-i', default='.data/knowledge', help='Knowledge directory')
    def status(self, input: str):
        """Show knowledge base status."""
        input_path = Path(input)
        
        if not input_path.exists():
            click.echo("No knowledge base found", err=True)
            return
        
        click.echo("Knowledge Base Status")
        click.echo("=" * 40)
        
        # Check concepts
        concepts_file = input_path / 'concepts.json'
        if concepts_file.exists():
            with open(concepts_file) as f:
                concepts = json.load(f)
                click.echo(f"Concepts: {len(concepts)}")
        else:
            click.echo("Concepts: 0")
        
        # Check insights
        insights_file = input_path / 'insights.json'
        if insights_file.exists():
            with open(insights_file) as f:
                insights = json.load(f)
                click.echo(f"Insights: {len(insights)}")
        else:
            click.echo("Insights: 0")
        
        # Check graph
        graph_file = input_path / 'knowledge_graph.json'
        if graph_file.exists():
            with open(graph_file) as f:
                graph_data = json.load(f)
                click.echo(f"Graph nodes: {len(graph_data.get('nodes', []))}")
                click.echo(f"Graph edges: {len(graph_data.get('links', []))}")
        else:
            click.echo("Graph: Not built")


# Amplifier module entry point
def get_tool_callable():
    """Return the tool callable for Amplifier."""
    cli = KnowledgeSynthesisCLI()
    return cli.cli


if __name__ == "__main__":
    cli = KnowledgeSynthesisCLI()
    cli.cli()