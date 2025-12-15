# Parasol CLI Module

Command-line interface for the Parasol DDD Framework, providing structured guidance through 7 phases of enterprise development.

## Installation

This module is included in the amplifier-experiment bundle. When using the bundle:

```bash
amplifier --bundle ../../bundle.md run "parasol init my-project"
```

## Usage

### Initialize a new project

```bash
parasol init my-project
```

Creates a new Parasol project with:
- `parasol.yaml` configuration file
- Phase-specific output directories
- Project structure for all 7 phases

### Check project status

```bash
parasol status
```

Shows:
- Project information
- Phase completion status
- Next recommended actions

### Execute a phase

```bash
parasol phase 1  # Start context analysis
parasol phase 2  # Define value streams
# ... etc
```

## Phases

1. **Context**: Organization analysis, market assessment, stakeholder mapping
2. **Value**: Value stream identification, enterprise activities
3. **Capabilities**: Domain classification, subdomain design
4. **Architecture**: Application design, integration patterns
5. **Software**: API design, domain language, database schemas
6. **Implementation**: Code generation, module development
7. **Platform**: Deployment, monitoring, operations

## Integration with Amplifier Agents

Each phase is supported by specialized Amplifier agents:

- Phase 1: `parasol-phase1-context`
- Phase 2: `parasol-phase2-value`
- Phase 3: `parasol-phase3-capabilities`
- Phase 4: `parasol-phase4-architecture`
- Phase 5: `parasol-phase5-software`
- Phase 6: `parasol-phase6-implementation`
- Phase 7: `parasol-phase7-platform`

## Project Structure

```
my-project/
├── parasol.yaml           # Project configuration
└── outputs/
    ├── 1-context/         # Organization, market, stakeholders
    ├── 2-value/           # Value streams, activities
    ├── 3-capabilities/    # Domains, subdomains
    ├── 4-architecture/    # Design, integration
    ├── 5-software/        # APIs, schemas
    ├── 6-implementation/  # Generated code
    └── 7-platform/        # Deployment configs
```