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

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bond is a **Python 3.12** CLI agent that connects to z.ai's GLM-4.6 model via an Anthropic-compatible API endpoint. It implements tool calling capabilities using the Anthropic Python library.

## Project Structure

```
/home/will/projects/bond/
├── main.py                  # Main entry point - interactive CLI
├── pyproject.toml           # Python project configuration with anthropic dependency
├── settings.json            # Environment variable configuration
├── bond/
│   ├── __init__.py
│   ├── agent.py             # Core BondAgent class with tool calling
│   ├── cli.py               # Interactive CLI loop
│   ├── config.py            # Configuration loader
│   └── tools.py             # Tool implementations (ping, echo, calculate, etc.)
├── docs/                    # Documentation and planning
├── openspec/                # OpenSpec change management
└── tests/                   # Test files
```

## Architecture

- **Agent Core**: `bond/agent.py` implements the main `BondAgent` class
- **API Integration**: Uses the **Anthropic Python library** to connect to z.ai
- **Endpoint**: `https://api.z.ai/api/anthropic` (Anthropic-compatible, not OpenAI)
- **Tool Calling**: Native Anthropic format with `{name, description, input_schema}`
- **Modern Python packaging**: Uses `pyproject.toml` (PEP 518/621)
- **Package manager**: Uses `uv` for environment management
- **Virtual environment**: Located at `.venv/`

## Critical API Integration Details

### Must Use Anthropic Library
z.ai provides an **Anthropic-compatible endpoint**, not an OpenAI-compatible one. This means:

1. **Use `anthropic` Python library** (already in dependencies)
2. **Tool format**: Must use Anthropic's native schema:
   ```python
   {
       'name': 'tool_name',
       'description': 'What the tool does',
       'input_schema': {
           'type': 'object',
           'properties': {...},
           'required': [...]
       }
   }
   ```
   **NOT** OpenAI format:
   ```python
   {
       'type': 'function',
       'function': {
           'name': '...',
           'description': '...',
           'parameters': {...}
       }
   }
   ```

3. **Environment Variables**: Must use Anthropic's standard names:
   - `ANTHROPIC_API_KEY` or `ANTHROPIC_AUTH_TOKEN` - Your z.ai API token
   - `ANTHROPIC_BASE_URL` - Set to `https://api.z.ai/api/anthropic`
   - `ANTHROPIC_MODEL` - Set to `glm-4.6`
   
   **Do NOT use** custom prefixes like `BOND_*` or `ZAI_*`

4. **Message Format**: Use Anthropic's message structure with proper role handling

## Development Commands

```bash
# Run the application (interactive CLI)
uv run python -m main

# Run with specific configuration
# Edit settings.json to configure environment variables

# Run tests
pytest

# Run tests with coverage
pytest --cov

# Lint code
ruff check .

# Format code
ruff format .
```

## Dependencies

- **Runtime dependencies**: 
  - `anthropic` - Official Anthropic Python library for API access
- **Development dependencies**: pytest, ruff
- **Python version**: Requires Python 3.12+

## Configuration

Configuration is loaded from `settings.json`:
```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "your-z.ai-token",
    "ANTHROPIC_BASE_URL": "https://api.z.ai/api/anthropic",
    "ANTHROPIC_MODEL": "glm-4.6"
  }
}
```

The `bond/config.py` module loads these environment variables and provides them to the agent.

## Key Implementation Files

- **bond/agent.py**: Core `BondAgent` class
  - Manages conversation context
  - Handles tool registration and calling
  - Converts between internal and Anthropic message formats
  - **Critical**: Tools must be stored in Anthropic format (see above)
  
- **bond/cli.py**: Interactive CLI interface
  - REPL loop for user interaction
  - Command processing (`/help`, `/exit`, `/tools`, etc.)
  - Tool execution and response handling
  
- **bond/tools.py**: Built-in tools
  - `ping(host)` - Network connectivity testing (adapted from Fly.io article)
  - `get_system_info()` - System information
  - `echo(message)` - Echo messages
  - `calculate(operation, a, b)` - Basic math
  
- **bond/config.py**: Configuration management
  - Loads from `settings.json`
  - Provides API credentials and settings

## Tool Development Guidelines

### Creating New Tools
When implementing tools for Bond, follow this pattern:

1. **Function Signature**: Tools are simple Python functions with type hints
2. **Error Handling**: Always include try/except blocks for robustness
3. **Return Types**: Return strings for simple output, JSON-serializable objects for complex data
4. **Documentation**: Include clear docstrings with Args and Returns sections

**Example Tool Template:**
```python
def tool_name(param1: str, param2: int) -> str:
    """
    Brief description of what the tool does.

    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2

    Returns:
        Description of return value
    """
    try:
        # Tool implementation here
        result = "success"
        return result
    except Exception as e:
        return f"error: {e}"
```

### Tool Registration
Register tools in `bond/cli.py` using the Anthropic schema format:

```python
agent.add_tool(
    name="tool_name",
    description="Brief description for the LLM",
    parameters={
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "Description for the LLM"
            },
            "param2": {
                "type": "integer",
                "description": "Description for the LLM"
            }
        },
        "required": ["param1", "param2"],
    },
    function=tool_name
)
```

### Key Implementation Insights
- **Subprocess Usage**: Use `subprocess.run()` with proper error handling for system commands
- **Text Output**: Always use `text=True` for subprocess to get string output
- **Error Capture**: Combine stdout and stderr with `stderr=subprocess.STDOUT`
- **Parameter Validation**: Let the LLM handle parameter validation based on schemas

## Project Status

Bond is now a **working CLI agent** with:
- ✅ Tool calling integration with z.ai's Anthropic endpoint
- ✅ Interactive CLI with multiple built-in tools
- ✅ Proper message and tool format handling
- ✅ Configuration management via settings.json
- ✅ Tool development patterns and best practices established

Next steps focus on reliability, testing, and advanced features from the Apex2 pattern.
