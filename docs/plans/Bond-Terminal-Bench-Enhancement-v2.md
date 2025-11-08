# Bond Terminal Bench Enhancement (v2)

Prepared by **GitHub Copilot (Codex)** — November 8, 2025

## 1. Executive Summary
Bond will evolve into a multi-phase intelligence and execution agent inspired by Apex2, optimized specifically for Terminal Bench. This v2 plan integrates feedback on feasibility, compliance, orchestration, and evaluation. We scope the work into phased deliverables (P0–P2) with explicit guardrails, fallbacks, and instrumentation so we can deliver incremental wins while derisking the broader vision.

## 2. Goals & Success Criteria
- **Primary Goal**: Achieve >55% accuracy on Terminal Bench 2.0 with GLM-4.6 while preserving safety and compliance.
- **Secondary Goals**: Reduce task turnaround time, raise recovery success rates, and produce auditable execution traces.
- **Key Enablers**: High-signal web intelligence, environment-aware planning, risk-aware execution, rigorous validation.

## 3. Guiding Principles
1. **Ship in vertical slices**: Each phase should run end-to-end, even if simplified.
2. **Guardrails first**: Compliance, fallbacks, and token budgeting are first-class requirements, not afterthoughts.
3. **Observability everywhere**: Every tool emits metrics so we can measure impact and regressions.
4. **Model-agnostic orchestration**: Allow mixing GLM-4.6 and Claude when it materially improves quality while tracking cost/latency.

## 4. Delivery Roadmap
### Phase P0 (Foundation – target: 2 weeks)
- Implement compliant **web_search v0** (single round) using an approved SERP provider (SerpAPI or Google Programmable Search).
- Introduce **PlannerOrchestrator** to schedule search → synthesis → execution within token budgets.
- Add **risk-aware prompts** for top categories (system, security, ML).
- Instrument metrics: search success rate, tokens by phase, execution errors.
- Acceptance: run synthetic benchmarks (10 curated tasks) showing improved plan quality vs. baseline.

### Phase P1 (Intelligence Expansion – target: +3 weeks)
- Upgrade web search to **multi-round** with AI Overview parsing & fallback logic.
- Add **environment observation tool** with capability detection (HTTP, Docker, pip list availability).
- Implement **strategy synthesis** combining search + environment + prior execution (if any).
- Introduce **recovery prompts** and **validation tool**; log recovery activations.
- Acceptance: 20-task internal gauntlet with success metrics, ensure no ToS violations, token usage < defined thresholds.

### Phase P2 (Advanced & Optional – target: +4 weeks)
- Add **predictive intelligence** (task categorisation, key file extraction, multimodal hints).
- Implement **Docker exploration agent** where environments permit.
- Add **second-pass intelligence refresh** mid-execution when tasks stall.
- Integrate fully with Harbor’s `BaseInstalledAgent` (install script, log ingestion).
- Acceptance: successful Harbor dry-run, Terminal Bench pilot with monitoring.

## 5. System Architecture Overview
```
┌───────────────────┐     ┌───────────────────────┐
│ Bond CLI / Harbor │ --> │ PlannerOrchestrator   │
└───────────────────┘     │  - Token budgeter     │
                          │  - Phase scheduler    │
                          └─────────┬────────────┘
                                    │
         ┌──────────────────────────┼───────────────────────────┐
         │                          │                           │
┌────────────────────┐  ┌────────────────────┐      ┌────────────────────┐
│ Intelligence Tools │  │ Recovery & Guard   │      │ Execution Engine   │
│ - web_search       │  │ - Risk prompts     │      │ - Command runner   │
│ - observe_env      │  │ - Recovery prompts │      │ - Validation       │
│ - deep_strategy    │  │ - Validation       │      │ - Logging          │
│ - docker_probe(*)  │  └────────────────────┘      └────────────────────┘
│ - synthesize       │
└────────────────────┘
```
(*) optional P2 component depending on environment capability.

## 6. Detailed Design Elements

### 6.1 PlannerOrchestrator
- Responsibilities: manage phase ordering, track token budgets, enforce timeouts, collect tool outputs, resolve conflicts.
- Interfaces:
  ```python
  class PlannerOrchestrator:
      def run_episode(self, instruction: str, context: Optional[EpisodeState]) -> EpisodeResult:
          ...
  ```
- Features:
  - Token ledger per phase (search, strategy, synthesis, execution, recovery) with hard caps.
  - Parallel execution support with concurrency limits.
  - Fallback routing (e.g., if web search fails, use local knowledge base).

### 6.2 Web Search Tool (P0→P1)
- **Provider**: Start with SerpAPI (licensed) or Google Programmable Search (API key required). Document ToS and secure credentials.
- **AI Overview parsing**: Use HTML parsing for the `gws-output-pages-elements-homepage_additional-output` block. If absent, fallback to summarising top results.
- **Multi-round logic** (P1): max 3 rounds; each round uses previous findings to refine query; if budget exhausted or confidence high, stop early.
- **Fallbacks**:
  - If provider fails: retry with exponential backoff (max 3 attempts), then degrade to internal knowledge or user-provided docs.
  - If network blocked: log capability flag and skip search gracefully.
- **API signature**:
  ```python
  def web_search(query: str,
                 round_num: int,
                 previous_findings: Optional[str],
                 bias_domains: List[str],
                 budget: TokenBudget) -> WebSearchResult:
      ...
  ```
- **Compliance**: maintain sanitisation module that filters banned keywords ("Terminal Bench", etc.) before queries/logging.

### 6.3 Environment Observation Tool (P1)
- Detect capabilities: HTTP egress, Docker availability (`docker ps`), pip visibility.
- Return structured data with command transcripts and redacted secrets.
- Respect environment constraints (if command unavailable, return descriptive error but do not fail pipeline).

### 6.4 Deep Strategy Generation (P1)
- Prompt executed with GLM-4.6 by default; optional Claude invocation if search results require reprocessing.
- Must include guard instructions limiting command execution to planning stage only.

### 6.5 Strategy Synthesis (P1)
- Combine artifacts: search summaries, environment data, prior execution logs, risk category hints.
- Provide final action plan + prioritized TODO list + risk checklist + fallback commands.
- Provide condensed version (<800 tokens) for GLM context.

### 6.6 Risk-Aware Execution & Recovery (P0→P1)
- Prompt templates keyed by category (system, security, ML, web, data) containing do/don’t lists, rollback reminders.
- Recovery modules triggered on common errors with idempotent suggestions; track activation counts.
- Validation tool checks logs for errors/tests before claiming success. Blocks completion on unresolved failures.

### 6.7 Docker Exploration Agent (P2)
- Launch ephemeral container only if environment capability flag true and policy allows.
- Sandbox command list (whitelisted operations). Hard timeout (e.g., 120s) and cleanup enforced by orchestrator.

### 6.8 Harbor Integration (P2)
- Extend `BondInstalledAgent` to:
  - Install dependencies (`install_bond.sh`).
  - Execute `bond run --instruction ...` with orchestrator controlling phases.
  - Export artifacts to Harbor context (search logs, strategy, execution transcripts) under `/logs/agent/`.
  - Populate Harbor context with structured summary for downstream evaluators.

## 7. Token Budget & Guardrails
| Phase                | Target Tokens | Hard Cap | Notes |
|----------------------|---------------|----------|-------|
| Predictive (P2)      | 400           | 600      | Skip if budget tight |
| Web Search per round | 800           | 1000     | Includes AI Overview + summarisation |
| Deep Strategy        | 1200          | 1500     | Stream summaries if nearing cap |
| Synthesis            | 700           | 900      | Produce condensed + verbose outputs |
| Execution Prompts    | 600           | 800      | Includes risk and recovery messages |
| Recovery / Validation| 300           | 500      | Reserve buffer |

PlannerOrchestrator enforces cap; on overflow, oldest data is summarised or truncated.

## 8. Compliance & Security Considerations
- **Web search**: Use licensed API; respect rate limits; maintain audit log of queries; implement keyword filter to avoid benchmark leakage.
- **Data retention**: Redact tokens, API keys, and personal data from logs. Provide retention policy (e.g., scrub after benchmark run).
- **Docker usage**: Only enable in environments explicitly flagged safe; ensure cleanup; document resources required.
- **Model usage**: Track cross-model prompts (GLM vs Claude) and ensure vendor-specific terms are met.

## 9. Evaluation & Instrumentation
- **Metrics**: search success rate, number of rounds executed, strategy length, recovery activations, validation failures, execution duration, tokens per phase.
- **Harness**: Build synthetic Terminal Bench-like tasks (e.g., repo tracing, log analysis) for regression testing; run nightly.
- **Rollback plan**: ability to disable new features via feature flags if metrics regress.

## 10. Dependencies & Ownership
| Component                   | Owner            | Dependency |
|-----------------------------|------------------|------------|
| SERP provider integration   | Infra team       | API key, ToS review |
| PlannerOrchestrator         | Bond core        | Token accounting |
| Risk prompts & recovery     | Safety team      | Category taxonomy |
| Harbor integration          | Bond core        | Harbor SDK |
| Docker probes               | Infra + Bond     | Environment matrix |

## 11. Risks & Mitigations
- **Scope creep** → Strict phased roadmap; complete P0 before starting P1.
- **SERP instability** → Abstract provider; add contract tests; maintain fallback summariser.
- **Token blow-up** → Enforce token ledger, stream summarisation.
- **Benchmark leakage** → Sanitise queries/logs; manual reviews; maintain denylist tests.
- **Flaky integrations** → Use mocks for tests; add retry & circuit breakers; feature-flag new tools.

## 12. Open Questions
1. Final decision on SERP provider and budget? (owner: product lead)
2. Who supplies and maintains API keys / proxies? (owner: infra)
3. How to simulate Docker-enabled vs sandboxed workloads for testing? (owner: QA)
4. Are we committing to Claude+GLM or standardising on GLM only? Need cost analysis.
5. What is the Harbor telemetry schema for agent artifacts?

## 13. Next Immediate Actions (Week 1)
1. Secure SERP provider access + legal approval.
2. Draft PlannerOrchestrator skeleton with token ledger.
3. Implement web_search v0 (single-round) with sanitisation + fallback.
4. Author risk prompt templates for top 3 categories.
5. Assemble synthetic benchmark suite for P0 acceptance.

---
This v2 plan balances ambition with pragmatism, ensuring Bond progresses toward Apex2-level intelligence while respecting operational constraints and delivering measurable value at each step.
