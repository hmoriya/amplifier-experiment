#!/bin/bash
# Git Worktree Setup Script for Architecture Experiments

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PARENT_DIR="$(dirname "$PROJECT_ROOT")"

echo "🌂 Setting up Parasol Architecture Experiment Worktrees"
echo "======================================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Architecture definitions
declare -a ARCHITECTURES=(
    "monolithic:Monolithic Architecture"
    "microservices:Microservices Architecture"
    "event-driven:Event-Driven Architecture"
    "clean:Clean/Onion Architecture"
    "hexagonal:Hexagonal Architecture"
    "serverless:Serverless Architecture"
    "parasol-hybrid:Parasol V3-V4 Hybrid"
    "cqrs-es:CQRS + Event Sourcing"
)

# Function to create worktree
create_worktree() {
    local arch_name=$1
    local arch_desc=$2
    local branch_name="arch/${arch_name}"
    local worktree_path="${PARENT_DIR}/amplifier-${arch_name}"

    echo -e "${BLUE}Setting up ${arch_desc}...${NC}"

    # Check if worktree already exists
    if git worktree list | grep -q "$worktree_path"; then
        echo -e "${YELLOW}  ⚠️  Worktree already exists at ${worktree_path}${NC}"
    else
        # Check if branch exists
        if git show-ref --verify --quiet "refs/heads/${branch_name}"; then
            echo -e "${YELLOW}  Branch ${branch_name} already exists, using it${NC}"
            git worktree add "$worktree_path" "$branch_name"
        else
            echo -e "${GREEN}  Creating new branch ${branch_name}${NC}"
            git worktree add -b "$branch_name" "$worktree_path"
        fi

        echo -e "${GREEN}  ✅ Created worktree at ${worktree_path}${NC}"

        # Create architecture-specific structure
        setup_architecture "$arch_name" "$worktree_path"
    fi

    echo ""
}

# Function to setup architecture-specific structure
setup_architecture() {
    local arch_name=$1
    local worktree_path=$2

    echo -e "${BLUE}  Setting up ${arch_name} structure...${NC}"

    # Create base architecture directory
    mkdir -p "${worktree_path}/architecture"

    # Create architecture-specific configuration
    cat > "${worktree_path}/architecture/config.yaml" << EOF
architecture:
  type: ${arch_name}
  version: "1.0.0"
  description: "Implementation of ${arch_name} architecture pattern"

structure:
  base_path: ./src
  test_path: ./tests
  docs_path: ./docs

metrics:
  track_performance: true
  track_complexity: true
  track_dependencies: true
EOF

    # Create architecture-specific directories
    case $arch_name in
        "monolithic")
            mkdir -p "${worktree_path}/src"/{controllers,services,models,database,utils}
            ;;
        "microservices")
            mkdir -p "${worktree_path}/services"/{auth-service,task-service,notification-service}
            mkdir -p "${worktree_path}"/{api-gateway,service-mesh}
            ;;
        "event-driven")
            mkdir -p "${worktree_path}/events"/{producers,consumers,schemas}
            mkdir -p "${worktree_path}"/{event-bus,saga}
            ;;
        "clean")
            mkdir -p "${worktree_path}/domain"/{entities,value-objects}
            mkdir -p "${worktree_path}/application"/{use-cases,interfaces}
            mkdir -p "${worktree_path}/infrastructure"/{persistence,external-services}
            mkdir -p "${worktree_path}/presentation"
            ;;
        "hexagonal")
            mkdir -p "${worktree_path}/domain"
            mkdir -p "${worktree_path}/ports"/{inbound,outbound}
            mkdir -p "${worktree_path}/adapters/inbound"/{rest,grpc}
            mkdir -p "${worktree_path}/adapters/outbound"/{database,external-api}
            ;;
        "serverless")
            mkdir -p "${worktree_path}/functions"/{api,workers,triggers}
            mkdir -p "${worktree_path}/infrastructure"/{terraform,cloudformation}
            ;;
        "parasol-hybrid")
            mkdir -p "${worktree_path}/capabilities"/{L1-strategic,L2-tactical,L3-operational/operations}
            mkdir -p "${worktree_path}"/{value-streams,bounded-contexts}
            ;;
        "cqrs-es")
            mkdir -p "${worktree_path}/command"/{handlers,aggregates}
            mkdir -p "${worktree_path}/query"/{handlers,projections}
            mkdir -p "${worktree_path}/events"/{store,snapshots}
            ;;
    esac

    echo -e "${GREEN}  ✅ Architecture structure created${NC}"
}

# Function to list all worktrees
list_worktrees() {
    echo -e "${BLUE}Current worktrees:${NC}"
    git worktree list | while read -r line; do
        if echo "$line" | grep -q "amplifier-"; then
            echo -e "${GREEN}  $line${NC}"
        else
            echo "  $line"
        fi
    done
}

# Main execution
main() {
    cd "$PROJECT_ROOT"

    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        echo -e "${RED}Error: Not in a git repository${NC}"
        exit 1
    fi

    echo "Setting up worktrees in: ${PARENT_DIR}"
    echo ""

    # Create worktrees for each architecture
    for arch_entry in "${ARCHITECTURES[@]}"; do
        IFS=':' read -r arch_name arch_desc <<< "$arch_entry"
        create_worktree "$arch_name" "$arch_desc"
    done

    echo "======================================================="
    echo -e "${GREEN}✅ All worktrees created successfully!${NC}"
    echo ""

    # List all worktrees
    list_worktrees

    echo ""
    echo "📝 Next steps:"
    echo "  1. Navigate to a worktree: cd ../amplifier-<architecture>"
    echo "  2. Implement the architecture: python architecture/implement.py"
    echo "  3. Run tests: python -m pytest tests/"
    echo "  4. Compare architectures: python architectures/compare.py"
    echo ""
    echo "To remove all worktrees: ./architectures/cleanup-worktrees.sh"
}

# Run main function
main "$@"