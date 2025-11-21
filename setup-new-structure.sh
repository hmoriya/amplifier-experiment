#!/bin/bash
# Setup script for new Amplifier + Parasol project structure

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR"

echo "🌂 Setting up Amplifier + Parasol Integrated Project Structure"
echo "=============================================================="
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Function to create directory with message
create_dir() {
    local dir_path=$1
    local description=$2

    if [ ! -d "$dir_path" ]; then
        mkdir -p "$dir_path"
        echo -e "${GREEN}✅ Created${NC}: $description"
    else
        echo -e "${YELLOW}⚠️  Exists${NC}: $description"
    fi
}

# Function to create file with content
create_file() {
    local file_path=$1
    local description=$2
    local content=$3

    if [ ! -f "$file_path" ]; then
        echo "$content" > "$file_path"
        echo -e "${GREEN}✅ Created${NC}: $description"
    else
        echo -e "${YELLOW}⚠️  Exists${NC}: $description"
    fi
}

echo -e "${BLUE}📋 Setting up Parasol Framework Core...${NC}"
echo "----------------------------------------"

# Parasol core structure
create_dir "$PROJECT_ROOT/parasol/phases/01-value-analysis" "Value Analysis Phase"
create_dir "$PROJECT_ROOT/parasol/phases/02-capability-design" "Capability Design Phase"
create_dir "$PROJECT_ROOT/parasol/phases/03-domain-modeling" "Domain Modeling Phase"
create_dir "$PROJECT_ROOT/parasol/phases/04-operation-design" "Operation Design Phase"
create_dir "$PROJECT_ROOT/parasol/phases/05-implementation" "Implementation Phase"
create_dir "$PROJECT_ROOT/parasol/phases/06-validation" "Validation Phase"

create_dir "$PROJECT_ROOT/parasol/patterns/value" "Value Patterns"
create_dir "$PROJECT_ROOT/parasol/patterns/capability" "Capability Patterns"
create_dir "$PROJECT_ROOT/parasol/patterns/domain" "Domain Patterns"
create_dir "$PROJECT_ROOT/parasol/patterns/operation" "Operation Patterns"
create_dir "$PROJECT_ROOT/parasol/patterns/implementation" "Implementation Patterns"

create_dir "$PROJECT_ROOT/parasol/knowledge/database" "Knowledge Database"
create_dir "$PROJECT_ROOT/parasol/knowledge/learnings" "Learnings Storage"
create_dir "$PROJECT_ROOT/parasol/knowledge/metrics" "Metrics Storage"

echo ""
echo -e "${BLUE}📚 Setting up Templates...${NC}"
echo "----------------------------------------"

# Template structure
create_dir "$PROJECT_ROOT/templates/microservices" "Microservices Template"
create_dir "$PROJECT_ROOT/templates/monolithic" "Monolithic Template"
create_dir "$PROJECT_ROOT/templates/clean-architecture" "Clean Architecture Template"
create_dir "$PROJECT_ROOT/templates/parasol-standard" "Parasol Standard Template"

# Create standard template structure
TEMPLATE_DIR="$PROJECT_ROOT/templates/parasol-standard"
create_dir "$TEMPLATE_DIR/src/domain/entities" "Domain Entities"
create_dir "$TEMPLATE_DIR/src/domain/value-objects" "Value Objects"
create_dir "$TEMPLATE_DIR/src/domain/services" "Domain Services"
create_dir "$TEMPLATE_DIR/src/application/use-cases" "Use Cases"
create_dir "$TEMPLATE_DIR/src/application/ports" "Ports"
create_dir "$TEMPLATE_DIR/src/infrastructure/persistence" "Persistence"
create_dir "$TEMPLATE_DIR/src/infrastructure/external" "External Services"
create_dir "$TEMPLATE_DIR/src/presentation/api" "API Layer"
create_dir "$TEMPLATE_DIR/src/presentation/web" "Web Layer"

echo ""
echo -e "${BLUE}🛠️ Setting up Tools...${NC}"
echo "----------------------------------------"

# Tools structure
create_dir "$PROJECT_ROOT/tools/cli" "CLI Tools"
create_dir "$PROJECT_ROOT/tools/vscode-extension" "VS Code Extension"

# Create CLI tools
create_file "$PROJECT_ROOT/tools/cli/parasol" "Parasol CLI" '#!/bin/bash
# Parasol CLI Tool

case "$1" in
    init)
        echo "Initializing new Parasol project: $2"
        ;;
    generate)
        echo "Generating $2: $3"
        ;;
    analyze)
        echo "Analyzing project: $2"
        ;;
    *)
        echo "Usage: parasol {init|generate|analyze} [options]"
        ;;
esac'

chmod +x "$PROJECT_ROOT/tools/cli/parasol"

echo ""
echo -e "${BLUE}⚙️ Setting up Configuration...${NC}"
echo "----------------------------------------"

# Global configuration
create_file "$PROJECT_ROOT/config/parasol.config.yaml" "Parasol Configuration" 'parasol:
  version: "4.0"
  defaults:
    architecture: clean-hexagonal
    patterns:
      auto_apply: true
    knowledge:
      collect: true

phases:
  - value-analysis
  - capability-design
  - domain-modeling
  - operation-design
  - implementation
  - validation'

create_file "$PROJECT_ROOT/config/amplifier.config.yaml" "Amplifier Configuration" 'amplifier:
  ddd:
    enabled: true
    workflow: standard
    artifacts_path: .ddd

  agents:
    available:
      - zen-architect
      - modular-builder
      - bug-hunter
      - test-coverage

  memory:
    enabled: true
    path: .amplifier/memory

  synthesis:
    enabled: true
    auto_collect: true'

create_file "$PROJECT_ROOT/config/workspace.json" "Workspace Configuration" '{
  "version": "1.0.0",
  "projects": {},
  "defaults": {
    "template": "parasol-standard",
    "architecture": "clean-hexagonal"
  },
  "tools": {
    "cli": "./tools/cli/parasol",
    "vscode": "./tools/vscode-extension"
  }
}'

echo ""
echo -e "${BLUE}🚀 Setting up Sample Project...${NC}"
echo "----------------------------------------"

# Sample project
SAMPLE_PROJECT="$PROJECT_ROOT/projects/consulting-dashboard"
create_dir "$SAMPLE_PROJECT/.ddd" "DDD Workflow Artifacts"
create_dir "$SAMPLE_PROJECT/parasol/capabilities" "Capability Definitions"
create_dir "$SAMPLE_PROJECT/parasol/operations" "Operation Definitions"
create_dir "$SAMPLE_PROJECT/src/domain/entities" "Domain Layer"
create_dir "$SAMPLE_PROJECT/src/application/use-cases" "Application Layer"
create_dir "$SAMPLE_PROJECT/src/infrastructure/persistence" "Infrastructure Layer"
create_dir "$SAMPLE_PROJECT/src/presentation/api" "Presentation Layer"
create_dir "$SAMPLE_PROJECT/tests/unit" "Unit Tests"
create_dir "$SAMPLE_PROJECT/tests/integration" "Integration Tests"
create_dir "$SAMPLE_PROJECT/tests/e2e" "E2E Tests"
create_dir "$SAMPLE_PROJECT/docs" "Documentation"

# Sample project configuration
create_file "$SAMPLE_PROJECT/parasol.yaml" "Project Configuration" 'project:
  name: consulting-dashboard
  type: enterprise
  architecture: clean-hexagonal
  description: "Consulting project management dashboard"

parasol:
  version: "4.0"
  phases: all

patterns:
  auto_apply: true
  library: ../../parasol/patterns

knowledge:
  collect: true
  database: ../../parasol/knowledge/database

capabilities:
  L1:
    - id: project-success
      name: "Project Success Capability"
  L2:
    - id: task-management
      name: "Task Management Capability"
  L3:
    - id: task-crud
      name: "Task CRUD Operations"'

create_file "$SAMPLE_PROJECT/README.md" "Project README" '# Consulting Dashboard

A comprehensive consulting project management dashboard built with Parasol Framework and Amplifier.

## Getting Started

```bash
# Initialize project
parasol init

# Run DDD workflow
/ddd:1-plan "Implement dashboard features"

# Generate code
parasol generate entity Task
parasol generate use-case CreateTask
```

## Architecture

Clean/Hexagonal Architecture with Parasol capability hierarchy.

## Documentation

See `docs/` directory for detailed documentation.'

echo ""
echo -e "${BLUE}📖 Creating Documentation...${NC}"
echo "----------------------------------------"

create_file "$PROJECT_ROOT/docs/getting-started.md" "Getting Started Guide" '# Getting Started with Amplifier + Parasol

## Prerequisites
- Node.js 18+
- Git
- Docker (optional)

## Quick Start

1. Create new project:
```bash
./tools/cli/parasol init my-project
```

2. Navigate to project:
```bash
cd projects/my-project
```

3. Start DDD workflow:
```bash
/ddd:1-plan "My feature description"
```

## Project Structure

- `parasol/` - Framework core
- `projects/` - Your projects
- `templates/` - Project templates
- `tools/` - Development tools'

echo ""
echo "=============================================================="
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo ""
echo "📂 New Structure Created:"
echo "  - parasol/     : Framework core"
echo "  - projects/    : Real projects"
echo "  - templates/   : Project templates"
echo "  - tools/       : CLI and development tools"
echo "  - config/      : Global configuration"
echo "  - docs/        : Documentation"
echo ""
echo "🚀 Next Steps:"
echo "  1. Create a new project: ./tools/cli/parasol init my-project"
echo "  2. Navigate to project: cd projects/my-project"
echo "  3. Start development: /ddd:1-plan \"Your feature\""
echo ""
echo "📚 Documentation: docs/getting-started.md"
echo "🔧 CLI Tool: ./tools/cli/parasol"
echo ""