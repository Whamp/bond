<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->

# Agent Instructions for Bond Project

## Critical: z.ai Anthropic Endpoint Integration

When working with Bond's API integration, you **must** understand these requirements:

### 1. Use Anthropic Python Library
z.ai provides an **Anthropic-compatible API endpoint** at `https://api.z.ai/api/anthropic`, not an OpenAI-compatible one.

**Always use:**
- The `anthropic` Python library (already in dependencies)
- Anthropic's native message formats
- Anthropic's tool schema format

**Never use:**
- OpenAI Python library
- OpenAI message or tool formats
- Custom API wrappers (use official Anthropic library)

### 2. Tool Schema Format
Tools **must** be defined in Anthropic's native format:

```python
{
    'name': 'tool_name',
    'description': 'What the tool does',
    'input_schema': {
        'type': 'object',
        'properties': {
            'param': {'type': 'string', 'description': '...'}
        },
        'required': ['param']
    }
}
```

**This is WRONG** (OpenAI format):
```python
{
    'type': 'function',
    'function': {
        'name': 'tool_name',
        'description': '...',
        'parameters': {...}
    }
}
```

The z.ai endpoint will return a 422 error if you send tools in OpenAI format.

### 3. Environment Variables
Because we use the Anthropic library, we **must** use Anthropic's standard environment variable names:

**Correct:**
- `ANTHROPIC_API_KEY` or `ANTHROPIC_AUTH_TOKEN`
- `ANTHROPIC_BASE_URL`
- `ANTHROPIC_MODEL`

**Incorrect (do not use):**
- `BOND_*` prefix
- `ZAI_*` prefix
- `OPENAI_*` prefix
- Custom variable names

The Anthropic library automatically reads its standard environment variables. Using custom names requires extra configuration and is error-prone.

### 4. Configuration Pattern
Bond uses `settings.json` to set environment variables before importing the Anthropic library. See `bond/config.py` for the implementation.

## Tool Implementation Best Practices

### Tool Development Pattern
Based on the Fly.io article adaptation, tools should follow this pattern:

1. **Simple Functions**: Tools are Python functions with clear signatures
2. **Robust Error Handling**: Always wrap operations in try/except blocks
3. **String Returns**: Return strings for simplicity (complex data gets JSON-encoded automatically)
4. **Proper Subprocess Usage**: Use `subprocess.run()` with correct parameters

**Example (ping tool implementation):**
```python
def ping(host: str) -> str:
    """Ping some host on the internet."""
    try:
        result = subprocess.run(
            ["ping", "-c", "5", host],
            text=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE
        )
        return result.stdout
    except Exception as e:
        return f"error: {e}"
```

### Registration Pattern
Always use Anthropic's native schema format when registering tools:

```python
agent.add_tool(
    name="ping",
    description="ping some host on the internet",
    parameters={
        "type": "object",
        "properties": {
            "host": {
                "type": "string",
                "description": "hostname or IP"
            }
        },
        "required": ["host"],
    },
    function=ping
)
```

### Common Implementation Details
- **Subprocess parameters**: `text=True` for string output, `stderr=subprocess.STDOUT` to capture errors
- **Error format**: Return `"error: {message}"` for consistency
- **Parameter handling**: Let the LLM validate parameters based on the schema
- **Return types**: Strings preferred, JSON-serializable objects also supported

## Project Architecture

Bond follows the Fly.io "Everyone Write an Agent" pattern:
- **Context**: Array of message objects
- **Tools**: JSON schemas the LLM can call (Anthropic format)
- **Loop**: Call LLM → Handle tool calls → Repeat

Key files:
- `bond/agent.py` - Core agent with tool calling and message format conversion
- `bond/cli.py` - Interactive REPL and tool registration
- `bond/tools.py` - Tool implementations (ping, system_info, echo, calculate)
- `bond/config.py` - Configuration loader for environment variables