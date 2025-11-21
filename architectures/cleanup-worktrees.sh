#!/bin/bash
# Cleanup script for Git Worktrees

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PARENT_DIR="$(dirname "$PROJECT_ROOT")"

echo "🧹 Cleaning up Architecture Experiment Worktrees"
echo "================================================"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Architecture names
declare -a ARCHITECTURES=(
    "monolithic"
    "microservices"
    "event-driven"
    "clean"
    "hexagonal"
    "serverless"
    "parasol-hybrid"
    "cqrs-es"
)

# Function to remove worktree
remove_worktree() {
    local arch_name=$1
    local worktree_path="${PARENT_DIR}/amplifier-${arch_name}"
    local branch_name="arch/${arch_name}"

    echo -e "${BLUE}Removing ${arch_name} worktree...${NC}"

    # Check if worktree exists
    if git worktree list | grep -q "$worktree_path"; then
        echo -e "${YELLOW}  Removing worktree at ${worktree_path}${NC}"
        git worktree remove "$worktree_path" --force 2>/dev/null || true
        echo -e "${GREEN}  ✅ Worktree removed${NC}"
    else
        echo -e "${YELLOW}  ⚠️  Worktree not found at ${worktree_path}${NC}"
    fi

    # Remove branch if it exists
    if git show-ref --verify --quiet "refs/heads/${branch_name}"; then
        echo -e "${YELLOW}  Removing branch ${branch_name}${NC}"
        git branch -D "$branch_name" 2>/dev/null || true
        echo -e "${GREEN}  ✅ Branch removed${NC}"
    fi

    echo ""
}

# Main execution
main() {
    cd "$PROJECT_ROOT"

    # Confirmation prompt
    echo -e "${YELLOW}⚠️  Warning: This will remove all architecture worktrees and branches!${NC}"
    read -p "Are you sure you want to continue? (y/N): " -n 1 -r
    echo ""

    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cleanup cancelled."
        exit 0
    fi

    echo ""

    # Remove each worktree
    for arch_name in "${ARCHITECTURES[@]}"; do
        remove_worktree "$arch_name"
    done

    # Clean up any prunable worktrees
    echo -e "${BLUE}Pruning worktree references...${NC}"
    git worktree prune
    echo -e "${GREEN}✅ Worktree references pruned${NC}"

    echo ""
    echo "================================================"
    echo -e "${GREEN}✅ Cleanup completed successfully!${NC}"
    echo ""

    # Show remaining worktrees
    echo -e "${BLUE}Remaining worktrees:${NC}"
    git worktree list
}

# Run main function
main "$@"