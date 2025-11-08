# Bond CLI Agent

Bond is an interactive CLI agent for z.ai's GLM-4.6 model inspired by the Fly.io "Everyone Write an Agent" pattern and the Apex2 Terminal Bench agent. The long-term goal is to match Apex2's "Predict -> Explore -> Synthesize -> Execute" performance while keeping the core implementation simple and extensible.

## Current Status
- Repository scaffolding is in place (`bond/` package plus CLI entry point stubs).
- `pyproject.toml` targets a uv-managed Python environment with the `anthropic` library.
- The implementation roadmap lives in `init-implementation-plan.md` and drives day-to-day work.
- **Working tool calling integration** with z.ai's Anthropic-compatible endpoint.

## API Integration

Bond uses the **Anthropic Python library** to connect to z.ai's Anthropic-compatible endpoint at `https://api.z.ai/api/anthropic`. This is important because:

### Why Anthropic Library?
- z.ai provides an **Anthropic-compatible API endpoint** (not OpenAI-compatible)
- The endpoint expects Anthropic's native message format and tool schema
- Tool definitions must use Anthropic's format: `{name, description, input_schema}` (not OpenAI's `{type: 'function', function: {...}}`)

### Environment Variables
Because we use the Anthropic library, we must use **Anthropic's standard environment variable names**:
- `ANTHROPIC_API_KEY` or `ANTHROPIC_AUTH_TOKEN` - Your z.ai API token
- `ANTHROPIC_BASE_URL` - Set to `https://api.z.ai/api/anthropic`
- `ANTHROPIC_MODEL` - Set to `glm-4.6` (or other z.ai models)

**Do NOT use** custom prefixes like `BOND_*` or `ZAI_*` - the Anthropic library looks for its own standard variable names.

## Current Implementation

### Tool Implementation Pattern
Bond follows the Fly.io "Everyone Write an Agent" pattern for tool development:

**Tools are simple Python functions with clear interfaces:**
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

**Tool registration uses Anthropic's native schema format:**
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

### Available Tools
- **ping(host)** - Network connectivity testing with full ping output
- **get_system_info()** - System information (platform, Python version, etc.)
- **echo(message)** - Message echoing for testing
- **calculate(operation, a, b)** - Basic mathematical operations

## Near-Term Plan
Bond will grow through incremental phases:
1. **Environment & Core**: ✅ Configure the z.ai client, manage conversation state, and ship a minimal `BondAgent` that can echo model responses.
2. **Tool Foundations**: ✅ Introduce a registry, wire up smoke-test tools (ping, echo), and ensure model function calling works end-to-end.
3. **Conversation & CLI Loop**: ✅ Build the interactive terminal experience with session commands and multi-turn tool handling.
4. **Reliability & Telemetry**: Layer in structured logging, retries, and tests so future capabilities can be benchmarked.
5. **Apex2-Inspired Growth**: Add predictive intelligence, observation runs, strategy synthesis, and a pluggable search pipeline.
6. **Execution & Benchmarking**: Harden heredoc tooling, recovery prompts, and instrumentation to prep for Terminal Bench style evaluation.

See `init-implementation-plan.md` for detailed deliverables, guiding principles, and open questions.

## References
- Fly.io article: https://fly.io/blog/everyone-write-an-agent/
- Apex2 Terminal Bench agent: https://github.com/heartyguy/Apex2-Terminal-Bench-Agent