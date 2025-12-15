# Amplifier Agents

This directory contains agent definitions for the Amplifier Experiment bundle. Agents use the new `meta:` frontmatter format required by Amplifier bundles.

## Agent Format

All agents must use this frontmatter format:

```yaml
---
meta:
  name: agent-name
  description: "Agent description with usage examples..."
---
# Agent Instructions

[Agent content here]
```

## Agent Categories

### parasol-agents/
Agents for the Parasol DDD framework, covering all 7 phases of development.

### synthesis-agents/
Knowledge synthesis and extraction agents for processing documents and generating insights.

### development-agents/
General development agents for architecture, implementation, testing, and debugging.

## Creating New Agents

1. Create a new `.md` file in the appropriate subdirectory
2. Use the `meta:` frontmatter format (not `agent:` or other formats)
3. Provide clear description with usage examples
4. Include the agent in the parent `bundle.md` agents list

## Agent Naming Convention

- Use kebab-case for agent names
- Prefix with category when appropriate (e.g., `parasol-phase1-context`)
- Keep names descriptive but concise