Plan: Build Bond - CLI Agent for z.ai GLM-4.6

Vision
- Deliver an interactive CLI agent (Claude Code style) powered by z.ai's GLM-4.6 that starts simple yet can evolve into an Apex2-class terminal agent.
- Embrace the Apex2 philosophy of "Predict -> Explore -> Synthesize -> Execute" while keeping early iterations lightweight and fast to ship.

Guiding Principles (informed by Apex2)
- Build a clear separation between prediction, exploration, synthesis, and execution loops so we can add sophistication without rewrites.
- Keep context/thread management explicit to enable rich strategy synthesis later.
- Prefer tool-driven interactions for observability, recovery, and determinism; reserve direct model replies for narrative glue.
- Instrument everything (inputs, tool calls, timing) from day one to support later ablation and benchmarking.

Technical Stack
- Language: Python 3.12+
- SDK: zai-sdk (official Python SDK from z.ai)
- API surface: OpenAI-compatible chat.completions.create()
- Model: glm-4.6 (key from `.env`)
- Base URL: https://api.z.ai/api/paas/v4/
- Dependency management: Poetry (pyproject.toml) + optional extras for advanced tooling (tiktoken, httpx, etc.)

Roadmap Overview
- Phase 0: Environment & project scaffolding
- Phase 1: Minimal agent core
- Phase 2: Tool system foundations
- Phase 3: Conversation & CLI loop
- Phase 4: Reliability, logging, and tests
- Phase 5: Apex2-inspired capability growth
- Phase 6: Benchmarking, guardrails, and polish

Phase 0: Environment & Project Scaffolding
1. Add `zai-sdk` dependency, lock with Poetry.
2. Load environment variables via `dotenv` helper.
3. Provide sample `.env.example` documenting required keys.
4. Establish project layout (`bond/` package, `cli.py`, `agent.py`, `tools.py`, `config.py`).

Phase 1: Minimal Agent Core
1. Implement `ZaiClient` wrapper handling authentication, retries, and request logging.
2. Create `ConversationState` (timestamps, roles, tokens, tool call metadata).
3. Define message model (system, user, assistant, tool) mirroring OpenAI semantics.
4. Provide a `BondAgent` skeleton with `send_message()` that relays user input and returns assistant text.

Phase 2: Tool System Foundations
1. Implement tool schema registry (name, description, JSONSchema params, callable reference).
2. Ship `ping` and `echo` tools for smoke testing.
3. Add dispatcher that transforms tool calls into Python function invocations and emits structured tool responses.
4. Validate schema adherence and argument coercion; include error pathway for invalid tool requests.

Phase 3: Conversation & CLI Loop
1. Build interactive CLI using `prompt_toolkit` (or `readline` fallback) with persistent session context.
2. Provide session commands (`/exit`, `/reset`, `/history`, `/save <path>`).
3. Stream assistant responses with tokens per chunk for future latency tracking.
4. Support multi-turn tool usage: call LLM, execute queued tool calls, append results, continue until assistant returns final text.

Phase 4: Reliability, Logging, and Tests
1. Integrate structured logging (JSON lines) for each turn: request, response, tool call, latency, token counts.
2. Add request retry/backoff, graceful handling of API/network failures, and CLI recovery prompts.
3. Cover core flows with unit tests (tool dispatch, message serialization, CLI commands) and golden transcripts.
4. Provide developer diagnostics (`bond --debug`) that dumps internal state per turn.

Phase 5: Apex2-Inspired Capability Growth
5.1 Predictive Intelligence
    - Introduce a pre-execution "prediction" pass that classifies task category, extracts referenced files, and flags multimodal needs (text only initially).
    - Store predictions in conversation metadata for later strategy synthesis.
5.2 Exploratory Observation
    - Implement observation tools (filesystem snapshot, dependency check, process inspection) patterned after Apex2's heuristic environment observation.
    - Allow scheduled observation bursts (episode 0/turn 5) controlled by config.
5.3 Strategy Synthesis
    - Create `StrategyBuffer` that aggregates predictions, observations, and search results into a concise context block fed back to the model.
    - Support risk assessment prompts and alternative strategy generation before main execution.
5.4 Web Search Pipeline (stub first)
    - Abstract search interface so local stubs can later switch to live SERP scraping.
    - Implement multi-round search orchestration (generate queries, fetch results, summarize top findings, enforce no Terminal Bench leakage).

Phase 6: Execution Optimization & Recovery
1. Add heredoc helper commands and validation before writing files to reduce shell errors.
2. Implement recovery prompt templates for common execution failures (syntax error, import error, missing file).
3. Track long-running commands with heartbeat monitoring and cancellation hooks.
4. Provide optional parallel exploration agents (secondary threads) that gather context while main agent executes.

Phase 7: Benchmarking, Guardrails, and Product Polish
1. Instrument success metrics (task duration, tool usage counts, error rate) for comparison against Terminal Bench baselines.
2. Add configurable safety rails (command allow/deny lists, dry-run mode, high-risk confirmations).
3. Package CLI (`bond` entrypoint), provide onboarding guide, and prep for internal beta.
4. Plan ablation study harness mirroring Apex2 methodology to measure component impact.

Apex2 Capability Parity Path
- Predictive Intelligence: Phase 5.1 lays groundwork for task categorization and key file detection.
- Parallel Intelligence Gathering: Phase 5.2 and Phase 6.4 introduce orchestrated exploration agents.
- Strategy Synthesis: Phase 5.3 formalizes context merging before execution.
- Advanced Search: Phase 5.4 provides the architecture for multi-round SERP search with AI overview extraction.
- Execution Robustness: Phase 6 mirrors Apex2's heredoc repair, recovery prompts, and validation steps.
- Validation Discipline: Phase 7 adds final output checks to avoid premature completion.

Key Design Decisions
- OpenAI-compatible message schema keeps migration friction low if we swap models or add multi-LLM routing.
- Tool-first execution makes advanced features (search, observation, recovery agents) pluggable.
- Structured logs enable Apex-style ablations without retrofitting instrumentation.
- Configuration-driven behavior (YAML/pyproject section) allows quick tuning per benchmark run.

Immediate Next Steps (Weeks 0-2)
1. Complete Phases 0 and 1 to establish a working agent skeleton.
2. Deliver Phase 2 with the ping tool and dispatcher to prove tool wiring.
3. Stand up the Phase 3 CLI loop; run manual transcripts verifying tool calls.
4. Draft logging schema (Phase 4 item 1) so early runs collect usable telemetry.

Open Questions
- Which tasks or benchmarks beyond Terminal Bench should drive early validation (e.g., internal scripts, user stories)?
- What level of offline search capability is acceptable before integrating live SERP APIs?
- How much concurrency can we reasonably introduce in Phase 6 without overcomplicating early releases?

Appendix: Example User Flow (Early Phase)
$ bond
> ping the system
✓ Tool called: ping
> list files in project root
✓ Tool called: filesystem_list('.')
> thanks!
Goodbye!