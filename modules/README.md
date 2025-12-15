# Amplifier Modules

This directory contains Amplifier-compatible modules that extend the platform with specialized functionality.

## Module Structure

Each module follows the standard Amplifier module structure:

```
module-name/
├── pyproject.toml              # Module metadata and dependencies
├── amplifier_module_<name>/    # Python package
│   ├── __init__.py
│   └── main.py                 # Module entry point
├── README.md                   # Module documentation
└── tests/                      # Module tests
```

## Available Modules

### parasol-cli
Command-line interface for the Parasol DDD framework, providing guided development through 7 phases.

### knowledge-synthesis
Advanced knowledge processing and synthesis capabilities with multi-perspective extraction and graph representation.

### ccsdk-toolkit
Claude Code SDK toolkit with defensive utilities for robust LLM integration.

## Creating New Modules

1. Create a new directory under `modules/`
2. Add `pyproject.toml` with module metadata
3. Implement the module following Amplifier conventions
4. Add tests and documentation
5. Register in the parent `bundle.md`

## Dependencies

Modules should only depend on:
- `amplifier-core` (the kernel)
- External packages (declared in pyproject.toml)
- NOT other modules (maintain independence)