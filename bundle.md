---
bundle:
  name: amplifier-experiment
  version: 1.0.0
  description: Amplifier extension with Parasol Framework for enterprise DDD and Knowledge Synthesis systems

includes:
  # Include official Amplifier foundation bundle when available
  # - bundle: git+https://github.com/microsoft/amplifier-foundation@main

tools:
  # Parasol CLI for DDD-based development
  - module: parasol-cli
    source: ./modules/parasol-cli
    
  # Knowledge Synthesis tools
  - module: knowledge-synthesis
    source: ./modules/knowledge-synthesis
    
  # CCSDK Toolkit
  - module: ccsdk-toolkit
    source: ./modules/ccsdk-toolkit

agents:
  include:
    # Parasol Framework Agents
    - amplifier-experiment:parasol-phase1-context
    - amplifier-experiment:parasol-phase2-value
    - amplifier-experiment:parasol-phase3-capabilities
    - amplifier-experiment:parasol-phase4-architecture
    - amplifier-experiment:parasol-phase5-software
    - amplifier-experiment:parasol-phase6-implementation
    - amplifier-experiment:parasol-phase7-platform
    
    # Knowledge Synthesis Agents
    - amplifier-experiment:concept-extractor
    - amplifier-experiment:insight-synthesizer
    - amplifier-experiment:knowledge-archaeologist
    - amplifier-experiment:tension-keeper
    - amplifier-experiment:uncertainty-navigator
    
    # Development Agents
    - amplifier-experiment:zen-architect
    - amplifier-experiment:modular-builder
    - amplifier-experiment:bug-hunter
    - amplifier-experiment:test-coverage
    - amplifier-experiment:integration-specialist

config:
  # Default configuration for modules
  knowledge-synthesis:
    default_output_dir: .data/knowledge
    extraction_model: claude-3-sonnet-20240229
    synthesis_model: claude-3-opus-20240229
    
  parasol-cli:
    default_project_dir: projects
    phases_enabled: [1, 2, 3, 4, 5, 6, 7]
---

# Amplifier Experiment Bundle

This bundle extends [Microsoft Amplifier](https://github.com/microsoft/amplifier) with enterprise-focused development tools and AI-powered knowledge synthesis capabilities.

## Features

### Parasol Framework
A comprehensive Domain-Driven Design (DDD) implementation framework that guides development through 7 phases:
- Phase 1: Context (Organization, Market, Stakeholders)
- Phase 2: Value (Value Streams, Enterprise Activities)
- Phase 3: Capabilities (Domain Classification, Subdomains)
- Phase 4: Architecture (Application Design, Integration)
- Phase 5: Software Design (APIs, Domain Language)
- Phase 6: Implementation (Code Generation)
- Phase 7: Platform (Deployment, Monitoring)

### Knowledge Synthesis System
Advanced knowledge processing and synthesis capabilities:
- Multi-perspective concept extraction
- Tension and uncertainty preservation
- Knowledge archaeology (temporal evolution)
- Graph-based knowledge representation
- Insight synthesis across domains

### Development Tools
Professional development agents:
- Zen Architect: Analysis-first development
- Modular Builder: Component implementation
- Bug Hunter: Systematic debugging
- Test Coverage: Comprehensive testing
- Integration Specialist: External service integration

## Usage

```bash
# Load this bundle with Amplifier
amplifier --bundle https://github.com/hmoriya/amplifier-experiment/bundle.md run "Start Parasol phase 1 analysis"

# Or use locally
git clone https://github.com/hmoriya/amplifier-experiment
amplifier --bundle ./amplifier-experiment/bundle.md run "Extract concepts from documents"
```

## Requirements

- Amplifier CLI installed (`pip install amplifier`)
- Python 3.11+
- API keys for Claude (Anthropic) or other LLM providers

## Contributing

This is an experimental extension of Amplifier. Contributions should:
- Follow Amplifier's modular architecture principles
- Maintain clear boundaries between modules
- Include comprehensive documentation
- Add tests for new functionality

## License

MIT License - See LICENSE file for details