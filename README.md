# Bond CLI Agent

Bond is an interactive CLI agent for z.ai's GLM-4.6 model inspired by the Fly.io "Everyone Write an Agent" pattern and the Apex2 Terminal Bench agent. The long-term goal is to match Apex2's "Predict -> Explore -> Synthesize -> Execute" performance while keeping the core implementation simple and extensible.

## Current Status
- Repository scaffolding is in place (`bond/` package plus CLI entry point stubs).
- `pyproject.toml` targets a Poetry-managed Python environment and will soon include the `zai-sdk` dependency.
- The implementation roadmap lives in `init-implementation-plan.md` and drives day-to-day work.

## Near-Term Plan
Bond will grow through incremental phases:
1. **Environment & Core**: Configure the z.ai client, manage conversation state, and ship a minimal `BondAgent` that can echo model responses.
2. **Tool Foundations**: Introduce a registry, wire up smoke-test tools (ping, echo), and ensure model function calling works end-to-end.
3. **Conversation & CLI Loop**: Build the interactive terminal experience with session commands and multi-turn tool handling.
4. **Reliability & Telemetry**: Layer in structured logging, retries, and tests so future capabilities can be benchmarked.
5. **Apex2-Inspired Growth**: Add predictive intelligence, observation runs, strategy synthesis, and a pluggable search pipeline.
6. **Execution & Benchmarking**: Harden heredoc tooling, recovery prompts, and instrumentation to prep for Terminal Bench style evaluation.

See `init-implementation-plan.md` for detailed deliverables, guiding principles, and open questions.

## References
- Fly.io article: https://fly.io/blog/everyone-write-an-agent/
- Apex2 Terminal Bench agent: https://github.com/heartyguy/Apex2-Terminal-Bench-Agent