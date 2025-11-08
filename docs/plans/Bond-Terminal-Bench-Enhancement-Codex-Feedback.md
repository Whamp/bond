# Bond Terminal Bench Enhancement — Codex Feedback

## Overall Assessment
- Ambitious, well-structured proposal that closely mirrors Apex2’s successful multi-phase playbook.
- Clear separation of phases and tool responsibilities gives the agent a strong conceptual framework.
- However, the implementation scope is extremely broad. A staged rollout plan, risk mitigations, and concrete integration details will be essential to keep execution tractable.

## What’s Working Well
- **Holistic pipeline:** Plan covers prediction → intelligence gathering → synthesis → guarded execution, which should meaningfully raise Terminal Bench accuracy if delivered.
- **High-leverage innovations highlighted:** Focus on Google AI Overview extraction and multi-round querying aligns with Apex2 learnings about search depth.
- **Token budgeting:** Thoughtful allocation acknowledges that intelligence gathering needs large context windows.
- **Risk-aware execution:** Explicit recovery and validation layers will reduce false positives and catastrophic mistakes.

## Key Gaps & Questions
1. **Feasibility & sequencing:** The document lists many new systems (SERP tooling, Docker agent, recovery layer, Harbor integration) but lacks a phased delivery plan. Which increments can ship independently? How will progress be measured between milestones?
2. **Search infrastructure compliance:** Using SERP scraping/Google AI Overview extraction may violate ToS and could trigger IP bans. What service or proxy will we rely on? Do we have budget/API keys? Need legal/compliance sign-off before investing.
3. **Fallback behaviour:** What happens if Google AI Overview is absent, the SERP call fails, or rate limits hit? Plan needs graceful degradation and cached knowledge re-use.
4. **Intelligence orchestration:** Parallel agents require an orchestrator (scheduler, success criteria, timeouts). The spec should define how results are merged, how conflicting insights are resolved, and how we avoid blowing the token budget.
5. **Environment assumptions:** Docker access, outbound networking, and `pip list` may be restricted in benchmark sandboxes. Need a capability matrix for Terminal Bench environments to avoid building features we can’t run.
6. **Data hygiene:** Quality-control step mentions filtering “Terminal Bench” references. Need an explicit sanitisation module (regex list, evaluation). Also consider logging redaction so stored transcripts remain clean.
7. **Model alignment:** We call out GLM-4.6 but rely on Claude for search query generation. Are we standardising on one model? How do we orchestrate cross-model workflows and reconcile costs/latencies?
8. **Evaluation loop:** Success metrics are outcome-based. We also need intermediate KPIs (search coverage, plan completeness, recovery activation rate) plus harnesses or synthetic tasks to regression-test each phase.
9. **Harbor integration detail:** The `BaseInstalledAgent` example is skeletal. We need to specify what data moves between Harbor and Bond, where logs/state live, and how multi-phase orchestration maps onto Harbor executions.

## Risks & Mitigations
- **Scope creep:** Ship P0 as a minimal vertical slice: one multi-round search implementation + synthesis + risk prompts. Defer Docker agent and predictive intelligence until baseline is stable.
- **Operational complexity:** Introduce a central `PlannerOrchestrator` component responsible for token budgeting, parallelism, and retries. Without this, complexity may sprawl across tools.
- **Token overflow:** Multi-round search + long synthesis may exceed context windows. Add guardrails (budget accounting per phase, truncation strategies, streaming summarisation) early.
- **Benchmark leakage:** Double-check search + logging stack to avoid pulling restricted benchmark content. Consider offline knowledge base seeding to reduce live web reliance.
- **SERP fragility:** Prototype with a supported API (SerpAPI, Google Programmable Search) while researching AI Overview parsing. Document plan B if Overview markup changes.

## Suggested Next Steps
1. **Author a phased roadmap** (P0 / P1 / P2 deliverables with acceptance tests and owner assignments). Include instrumentation requirements for each phase.
2. **Prototype `web_search` vertical slice**: choose SERP provider, implement one search round, capture AI Overview (when present), design fallback summary. Validate ToS compliance.
3. **Design orchestration layer**: a module that coordinates phases, tracks token spend, and persists artifacts (search results, strategies, recovery logs).
4. **Define evaluation harness**: create synthetic tasks mirroring Terminal Bench patterns to measure incremental improvements before live runs.
5. **Document environment capabilities**: confirm Terminal Bench allows outbound HTTP, Docker, etc. Capture constraints to avoid wasted implementation.
6. **Security/compliance review**: run tooling plan past legal/infra teams, especially around scraping, Docker usage, and data retention.
7. **Detail Harbor integration**: expand `BondInstalledAgent` spec with real command sequences, context handoff, and log schema.

## Open Questions for Plan Owners
- Which model mix are we targeting (Claude vs GLM vs others) and how will we manage cross-model prompting?
- Do we have access to SERP APIs / proxies today, and who owns the credentials?
- How will we unit/integration test components that rely on live web search or Docker without flakiness?
- What is the rollback strategy if the new intelligence layers degrade performance during benchmarks?
- Who owns ongoing maintenance for the web search tool as Google’s UI/AI Overview evolves?

---
Prepared by **GitHub Copilot (Codex)** — November 8, 2025
