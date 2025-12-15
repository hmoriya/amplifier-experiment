# CCSDK Toolkit Module

Claude Code SDK toolkit providing defensive utilities and patterns for building robust LLM-powered tools.

## Features

- **Tool Templates**: Quick-start templates for common patterns (basic, streaming, multi-stage)
- **Defensive Utilities**: Battle-tested patterns for handling LLM responses
- **JSON Extraction**: Robust parsing of JSON from any LLM output format
- **Retry Patterns**: Intelligent retry with error feedback for self-correction
- **Prompt Isolation**: Prevent context contamination in prompts

## Installation

This module is included in the amplifier-experiment bundle:

```bash
amplifier --bundle ../../bundle.md run "ccsdk-toolkit create my-tool"
```

## Usage

### Create a new tool

```bash
ccsdk-toolkit create my-analyzer --template basic
ccsdk-toolkit create my-processor --template streaming
ccsdk-toolkit create my-pipeline --template multi-stage
```

Creates a new tool with:
- Main tool implementation
- Defensive utilities module
- Usage examples

### Validate JSON from LLM

```bash
ccsdk-toolkit validate-json output.json
```

Attempts to extract and validate JSON from LLM output, handling common issues like:
- Markdown code blocks
- Explanatory text
- Malformed JSON
- Trailing commas

### View defensive patterns

```bash
ccsdk-toolkit patterns
```

Lists available defensive patterns with descriptions.

## Defensive Patterns

### parse_llm_json()
Extracts JSON from any LLM response format:

```python
from defensive import parse_llm_json

response = """
Here's the JSON you requested:
```json
{"result": "success", "confidence": 0.85}
```
"""

data = parse_llm_json(response)
# Returns: {"result": "success", "confidence": 0.85}
```

### retry_with_feedback()
Intelligent retry that provides error context to LLM:

```python
from defensive import retry_with_feedback

result = await retry_with_feedback(
    session=claude_session,
    prompt="Generate valid JSON with name and age",
    parse_fn=parse_llm_json,
    max_retries=3
)
```

### isolate_prompt()
Prevents context contamination:

```python
from defensive import isolate_prompt

safe_prompt = isolate_prompt(user_input)
# Wraps input in tags to prevent instruction leakage
```

## Tool Structure

Generated tools follow this structure:

```
my-tool/
├── my_tool.py      # Main tool implementation
├── defensive.py    # Defensive utilities
└── example.py      # Usage examples
```

## Best Practices

1. **Always use defensive parsing** - Never trust raw LLM output
2. **Implement retry logic** - Transient failures are common
3. **Isolate user content** - Prevent prompt injection
4. **Validate structure** - Ensure responses match expected format
5. **Handle timeouts** - Set reasonable limits on operations

## Integration with Claude Code SDK

Tools created with this toolkit integrate seamlessly with Claude Code SDK:

```python
from claude_code_sdk import ClaudeCodeSession
from defensive import parse_llm_json, retry_with_feedback

async with ClaudeCodeSession(api_key=api_key) as session:
    result = await retry_with_feedback(
        session=session,
        prompt=prompt,
        parse_fn=parse_llm_json
    )
```