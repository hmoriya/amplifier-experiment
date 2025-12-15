# Knowledge Synthesis Module

Advanced knowledge processing and synthesis capabilities for extracting concepts, generating insights, and building knowledge graphs.

## Features

- **Multi-perspective concept extraction**: Extract concepts from various document formats
- **Insight synthesis**: Generate insights through convergence, divergence, and emergence patterns
- **Knowledge graph construction**: Build and visualize relationships between concepts
- **Tension preservation**: Maintain contradictions and uncertainties as valuable information
- **Temporal analysis**: Track evolution of concepts over time

## Installation

This module is included in the amplifier-experiment bundle:

```bash
amplifier --bundle ../../bundle.md run "knowledge synthesis extract ./docs"
```

## Usage

### Extract concepts from documents

```bash
knowledge-synthesis extract ./documents -o .data/knowledge
```

Extracts concepts from all markdown, text, and PDF files in the specified directory.

### Synthesize insights

```bash
knowledge-synthesis synthesize -t convergence
knowledge-synthesis synthesize -t divergence  
knowledge-synthesis synthesize -t emergence
```

Generates different types of insights:
- **Convergence**: Where multiple concepts align or support each other
- **Divergence**: Where concepts conflict or present alternatives
- **Emergence**: Where new patterns arise from concept interactions

### Build knowledge graph

```bash
knowledge-synthesis build-graph -f json
knowledge-synthesis build-graph -f graphml  # For visualization tools
knowledge-synthesis build-graph -f gexf     # For Gephi
```

Creates a graph representation of concepts and their relationships.

### Check status

```bash
knowledge-synthesis status
```

Shows current state of the knowledge base:
- Number of extracted concepts
- Generated insights count
- Graph statistics

## Output Structure

```
.data/knowledge/
├── concepts.json         # Extracted concepts
├── insights.json         # Synthesized insights
├── knowledge_graph.json  # Graph representation
└── events.jsonl          # Processing events log
```

## Integration with Agents

This module works with specialized knowledge agents:

- `concept-extractor`: Extracts atomic concepts from documents
- `insight-synthesizer`: Generates breakthrough insights
- `knowledge-archaeologist`: Analyzes temporal evolution
- `tension-keeper`: Preserves productive contradictions
- `uncertainty-navigator`: Maps boundaries of knowledge

## Concept Format

```json
{
  "id": "concept_123",
  "name": "Microservices Architecture",
  "description": "Architectural pattern for distributed systems",
  "source": "docs/architecture.md",
  "confidence": 0.85,
  "extracted_at": "2024-01-15T10:30:00Z",
  "relationships": ["concept_124", "concept_125"]
}
```

## Insight Format

```json
{
  "id": "insight_1",
  "title": "Convergence in Distributed Patterns",
  "description": "Multiple architectural patterns converge on similar principles",
  "concepts": ["concept_123", "concept_124", "concept_125"],
  "synthesis_type": "convergence",
  "confidence": 0.75,
  "generated_at": "2024-01-15T11:00:00Z"
}
```