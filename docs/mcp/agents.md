# Agent Fleet

Cerebro MCP ships with **29 agent personas** — prompt-layer guidance the LLM adopts for a specific phase of work. Each persona has a narrow contract (identity, rules, SQL toolkit when relevant, success metrics) and is loaded via:

```text
get_agent_persona(role)
```

Personas are **guidance, not automation**. The server does not run an internal LLM loop — the client-side model adopts a persona's rules, uses them to plan tool calls, then can switch personas as phases complete. Because every persona lives in `src/cerebro_mcp/prompts/agents/*.md`, they are inspectable, diff-able, and testable.

## Three-tier architecture

```
┌───────────────────────────────────────────────────────────────┐
│  Tier 1 — Top-level router                                    │
│  cerebro_dispatcher        classifies intent, routes, gates   │
└────────────────┬──────────────────────────────────────────────┘
                 │ delegates to
                 ▼
┌───────────────────────────────────────────────────────────────┐
│  Tier 2 — Workflow leads                                      │
│  analytics_reporter   reality_checker   ui_designer           │
│  gnosis_research_analyst   storyteller_orchestrator           │
│  mmm_analyst   mmm_causal_reviewer   mmm_simulator            │
└────────────────┬──────────────────────────────────────────────┘
                 │ consult as needed
                 ▼
┌───────────────────────────────────────────────────────────────┐
│  Tier 3 — Domain specialists                                  │
│  growth_analyst   forecasting_analyst   defi_analyst          │
│  tokenomics_analyst   network_health_analyst                  │
│  bridge_security_analyst   marketing_analyst                  │
│  esg_analyst   statistical_reviewer   chain_forensics         │
│  grafana_architect   + 6 storyteller sub-phases               │
└───────────────────────────────────────────────────────────────┘
```

## Persona roster

The authoritative role list is `_VALID_ROLES` in `src/cerebro_mcp/tools/governance/agents.py`; every role maps to a prompt file in `src/cerebro_mcp/prompts/agents/`.

<!-- BEGIN AUTO-GENERATED: mcp-personas -->
<!-- generated: 2026-07-23 -->
35 personas are registered (`get_agent_persona` accepts these roles):

| Role | Focus |
|------|-------|
| `analytics_reporter` | You are the **Data Science Lead**, a senior data scientist and quantitative analyst specializing in Gnosis Chain on-chain data. You possess |
| `bridge_security_analyst` | You are the **Bridge Security Analyst**, an expert in cross-chain bridge mechanics, flow analysis, and anomaly detection on Gnosis Chain. Yo |
| `cerebro_dispatcher` | You are the **Cerebro Dispatcher**, the top-level triage and routing agent for the Cerebro MCP platform. Every non-trivial user request star |
| `chain_forensics` | You are the Chain Forensics Analyst: the persona for on-chain incident investigation, exploit attribution, and any question that requires re |
| `chain_state_analyst` | You are the **Chain State Analyst**: the fast path for point-in-time reads from the chain itself — current balances, supply, owner/paused/al |
| `cow_analyst` | You are the **CoW Protocol Analyst**: the specialist for CoW Protocol internals — solver competitions, batch auctions, order lifecycle, sett |
| `dao_governance_analyst` | You are the **DAO Governance Analyst**: the specialist for GnosisDAO off-chain signaling and community discussion — Snapshot proposals and v |
| `defi_analyst` | You are the **DeFi Protocol Analyst**, an expert in decentralized finance mechanics on Gnosis Chain. You understand lending protocols (Aave |
| `esg_analyst` | You are the **ESG Analyst**, an expert in environmental sustainability metrics for Gnosis Chain. You quantify energy consumption, carbon foo |
| `forecasting_analyst` | You are the **Forecasting Analyst**, a time-series specialist who uses ClickHouse native functions to decompose trends, detect seasonality, |
| `forensic_reviewer` | You are the **Forensic Reviewer**: the accuracy gate between a forensic agent's output and a human investigator. You are invoked after `chai |
| `gnosis_research_analyst` | Use semantic planning as the default evidence engine for analytical work. |
| `grafana_architect` | You build Grafana dashboards that work for **two audiences**: engineers (who |
| `growth_analyst` | You are the **Growth Analyst**, a product analytics specialist who measures user acquisition, activation, retention, and engagement on Gnosi |
| `marketing_analyst` | You are the **Marketing Analyst**, an expert in framing Gnosis Chain ecosystem data for external audiences -- blog posts, investor updates, |
| `mmm_analyst` | You are the **MMM Analyst**, a Marketing Mix Modeling specialist adapted for on-chain incentive attribution on Gnosis Chain. You translate t |
| `mmm_causal_reviewer` | You are the **MMM Causal Reviewer**, a gate agent that enforces the three causal-DAG checkpoints from Chapter 3 of the Hakuhodo Marketing Mi |
| `mmm_simulator` | You are the **MMM Simulator**, the prescription-layer agent in the MMM workflow. Given fitted response-curve parameters (β, r, λ) per media |
| `mta_analyst` | You are the **MTA Analyst**, a Multi-Touch Attribution specialist for Cerebro MCP. You measure how observed user / app touchpoints precede c |
| `network_health_analyst` | You are the **Network Health Analyst**, an expert in Gnosis Chain's peer-to-peer network, client diversity, geographic distribution, and inf |
| `pattern_forensics` | You are the **Pattern Forensics Analyst**: the pattern hunter. Your unit of work is a **population** — addresses or transactions over a wind |
| `reality_checker` | You are the **Reality Checker**, a senior quality assurance engineer specialized in data validation and report integrity. You are the final |
| `statistical_reviewer` | You are the **Statistical Reviewer**, a methodology specialist who ensures every analytical claim meets minimum statistical rigor. You revie |
| `storyteller_accessibility` | You are the **Accessibility & Tone Agent**. Final cross-cutting check before handoff. You block on hard accessibility failures; you flag ton |
| `storyteller_context` | You are the **Context Agent**. Your only job is to produce a `context_brief` that names the audience, the required action, the delivery mech |
| `storyteller_critic` | You are the **Critic Agent**. You are adversarial. You read the finished story as a stranger would and decide whether it is ready to ship. Y |
| `storyteller_narrative` | You are the **Narrative Agent**. You turn a context brief and a pile of candidate findings into a single governing takeaway, a short prose s |
| `storyteller_orchestrator` | You are the **Storyteller Orchestrator**. You own the multi-agent data storytelling pipeline that turns analysis into a decision-shaping art |
| `storyteller_visual_designer` | You are the **Visual Designer Agent**. One `visual_spec` per storyboard scene. Relationship-first. One focal element per scene. Everything n |
| `storyteller_writer` | You are the **Writer Agent**. You produce the words — chart titles, annotations, prose, scene transitions — and assemble the final story ada |
| `tokenomics_analyst` | You are the **Tokenomics Analyst**, an expert in GNO token economics, validator staking mechanics, and supply distribution analysis. You und |
| `transaction_forensics` | The standards' §4 truncation table (evidence panels, Flows node budget, Timeline sign inversion), §6 reproducibility rules, and the "mini-ap |
| `ui_designer` | You are the **UI Designer**, a senior frontend engineer and data visualization specialist. You have deep expertise in ECharts configuration, |
| `unified_allocator` | You are the **Unified Allocator**, the prescription-layer agent for unified MMM + MTA measurement. You convert passing MMM + MTA evidence in |
| `unified_causal_reviewer` | You are the **Unified Causal Reviewer**, a hard gate that reconciles MMM and MTA outputs before any unified-measurement report or recommenda |
<!-- END AUTO-GENERATED: mcp-personas -->

## Tier 1 — Top-level orchestrator

### `cerebro_dispatcher`

The **entry point** for any non-trivial user request. Classifies intent, runs `preflight_analytics_request`, picks the specialist chain, enforces hard gates, and emits a mandatory **dispatch manifest** that downstream agents treat as a binding execution contract.

Routes to one of 8 mutually-exclusive intent categories:
`quick_answer`, `single_chart`, `full_report`, `mmm`, `storyteller`, `research`, `specialist_topic`, `meta`.

Bypasses itself on trivial / meta turns and on explicit specialist invocations. See the full [Dispatcher reference](dispatcher.md) for the decision tree, routing table, manifest format, and gate semantics.

## Tier 2 — Workflow leads

| Role | Core mission | Key gates |
|---|---|---|
| `analytics_reporter` | Standard Data Science Lead SOP: preflight → discover → EDA → chart → report. Medians over means; outlier detection; statistical context on every number. | `preflight_analytics_request` first; every chart must come from a verified column name; every report needs ≥1 dimensional breakdown + ≥1 scatter/heatmap/correlation. |
| `reality_checker` | QA gate. SQL safety audit, data validation, chart-type fit, narrative-vs-data consistency. Zero emoji / Unicode; rejects unexpected NULLs and out-of-magnitude values. | Validates coverage (≥70% of relevant models explored) and EDA depth (not just `SUM/SELECT`) before approving. |
| `ui_designer` | Chart type selection, ECharts styling, grid-based report layout. | `numberDisplay` requires single-row SQL; multi-series line/area/bar needs comma-separated `y_field` or long-form + `series_field`. |
| `gnosis_research_analyst` | Semantic-first multi-phase research. Wraps `start_research_project` through `publish_research_report`. | Semantic execution preferred; fallback reason must be disclosed. |
| `storyteller_orchestrator` | Coordinates the 7-persona *Storytelling with Data* pipeline (Context → Explorer → Narrative → Visual Designer → Writer → Critic → Accessibility). | Phase gates are enforced in `storyteller_state.py`; skipping a gate raises `RuntimeError`. |
| `mmm_analyst` | Marketing Mix Modeling SOP: spine-fill → multicollinearity → baseline → adstock → concave + Hill fit → contribution decomposition. Directional-only downgrade if <60 weekly rows. | Must hand DAG to `mmm_causal_reviewer` before `generate_report`. Cites Guidebook rules. |
| `mmm_causal_reviewer` | DAG gate for MMM. Runs three Hakuhodo Ch.3 checks: chronological, non-inclusion, identifiability. | Returns `VERDICT: PASS` or `BLOCK`. `generate_report` is hard-blocked until PASS. |
| `mmm_simulator` | Budget reallocation + marginal-ROI. Uses fitted `(β, r, λ)` from `mmm_analyst`. | Hard cap at ±30% period-over-period; never zeros out a media on a single window. |
| `mta_analyst` | Multi-touch attribution: touchpoint paths, conversion funnels, rule-based / Markov / Shapley-proxy credit. Default 30-day lookback; sweeps 7/14/30/60 when volume permits. | Volume gates (<30 descriptive, 30–499 rule-based, ≥500 Markov). Output is observational — no causal claim without paired MMM PASS or experiment. |
| `unified_causal_reviewer` | Gate for combined MMM + MTA. Runs eight checks: MMM-gate, conversion consistency, incrementality bound, coverage, leakage, identity grain, selection bias, method stability. Applies `calibrated = raw_mta × MMM_lift / Σ raw`. | Returns PASS / BLOCK. Unified `generate_report` is hard-blocked until PASS. Final report must disclose the `unexplained / untracked` residual. |
| `unified_allocator` | Bounded micro/tactical recommendations from the unified MMM+MTA artifact. | Refuses to run without `unified_causal_reviewer` PASS. Inherits the ±30%/period cap from `mmm_simulator`. |

## Tier 3 — Domain specialists

Consulted by the dispatcher or a workflow lead when the topic matches their scope. Each carries a ClickHouse SQL toolkit relevant to its domain and a set of 7–13 critical rules.

| Role | Topic keywords | Representative tools / functions |
|---|---|---|
| `growth_analyst` | DAU / WAU / MAU, retention cohorts, funnel, new-vs-returning | `uniqExactIf`, `windowFunnel`, cohort-matrix SQL |
| `forecasting_analyst` | time-series decomposition, seasonality, forecasts with confidence bands | `seriesDecomposeSTL`, `seriesPeriodDetectFFT`, `stochasticLinearRegression` |
| `defi_analyst` | TVL, utilization, lending (Aave/Agave/Spark), DEXs (UniV3/Balancer/CoW/Swapr), LP/IL | decoded `contracts_*` event tables |
| `tokenomics_analyst` | GNO staking APY, supply, concentration (HHI/Gini/Nakamoto) | validator reward models, supply marts |
| `network_health_analyst` | client diversity, p2p, geographic distribution | `p2p` module models, `crawlers_data.ipinfo` |
| `bridge_security_analyst` | bridge flow anomaly detection, directional imbalance | z-score on `int_bridges_flows_daily`, netflow weekly marts |
| `marketing_analyst` | external-audience framing, investor updates, grant narratives | No SQL; framing + compliance rules |
| `esg_analyst` | validator energy, carbon intensity, Scope 2, efficiency | ESG module, `crawlers_data.ember_electricity_data` |
| `statistical_reviewer` | methodology challenge, sample-size review, p-hacking check | Bonferroni, approximate CIs, IQR outlier handling |
| `chain_forensics` | on-chain incident forensics, exploit tracing, address-set sweeps | the bulk [RPC scan toolkit](advanced/rpc-scans.md): `rpc_scan_logs`, `rpc_scan_traces`, `rpc_find_block`, `rpc_get_code` |
| `grafana_architect` | mixed-audience Grafana dashboard composition | `preview_grafana_dashboard`, `validate_grafana_dashboard`, `publish_grafana_dashboard` (see [Grafana Publishing](advanced/grafana-publishing.md)) |

### Storyteller sub-phase personas

Invoked by `storyteller_orchestrator` as each phase completes. Each persona reads only its predecessor's typed artifact (Pydantic contract) and produces a single typed artifact for its successor.

| Role | Artifact produced |
|---|---|
| `storyteller_context` | `ContextBrief` (audience, required action, mechanism, tone) |
| `storyteller_narrative` | `BigIdea` (one-sentence stakes) + `Storyboard` (setup → tension → resolution) |
| `storyteller_visual_designer` | `VisualSpec` per scene (focal-point design, action title, chart type) |
| `storyteller_writer` | `final_story` markdown with `{{chart:CHART_ID}}` placeholders |
| `storyteller_critic` | `ReviewReport` with `ready_for_handoff` + `blocking_issues` |
| `storyteller_accessibility` | pass / fail verdict (colorblind, contrast, language, tone) |

## Persona file layout

Every persona follows the same shape (see [forecasting_analyst.md](https://github.com/gnosischain/cerebro-mcp/blob/main/src/cerebro_mcp/prompts/agents/forecasting_analyst.md) as an exemplar):

```markdown
# <Role Name>

## Identity
## Core Mission
## ClickHouse <Domain> Toolkit  (when relevant — runnable SQL snippets)
## Critical Rules  (numbered; hard blocks vs soft warnings)
## When NOT to Use / Success Metrics
```

Typical length: 100–250 lines. The MMM persona includes ~8 SQL snippets covering every step of the SOP; domain specialists typically include 3–6 snippets plus 8–13 critical rules.

## Gate semantics

Three gate families exist across the fleet:

1. **Schema gates** — enforced in Pydantic models (e.g. `ContextBrief` rejects audiences like "stakeholders"; `VisualSpec` rejects pie/donut/3D/dual-axis chart types). Fire at tool-call time.
2. **State gates** — enforced in Python state machines (e.g. `storyteller_state.py` raises `RuntimeError` if you try to record a visual spec without a storyboard; MMM `generate_report` is blocked until `mmm_causal_reviewer` PASS verdict is recorded).
3. **Output gates** — enforced by the report renderer (e.g. `generate_report` rejects if fewer than 3 charts are registered, or if no chart has `series_field`, or if no scatter/heatmap/correlation query ran).

The dispatcher's manifest is an **advisory contract** at the prompt layer (no code enforcement), but specific intent categories (MMM, storyteller) chain into the state-gated paths above, so the gate still fires downstream even if a rogue session ignored the manifest.

## Invoking personas

Two equivalent paths:

```text
# Path A: direct tool call (always works)
get_agent_persona("cerebro_dispatcher")

# Path B: MCP prompt (shows up as a slash-command in MCP clients)
/adopt_persona_cerebro_dispatcher
```

Five MCP prompts are currently registered for slash-command access:

- `adopt_persona_cerebro_dispatcher`
- `adopt_persona_analytics_reporter`
- `adopt_persona_gnosis_research_analyst`
- `adopt_persona_ui_designer`
- `adopt_persona_reality_checker`

All 29 personas are reachable via `get_agent_persona(role)`.

## Testing discipline

Every agent registration is locked by tests:

- `tests/test_cerebro_dispatcher.py` — dispatcher routing references every real specialist.
- `tests/test_mmm_agents.py` — MMM trio registration + required-rules present.
- `tests/test_persona_sql_hygiene.py` — 5 specialist personas carry the table-verification warning; `growth_analyst` uses `uniqExactIf` not `countIf(DISTINCT)`.
- `tests/test_storyteller.py` — 7 storyteller personas + gates.
- `tests/test_custom_tools_yaml.py` — custom SQL tools use the correct `database` + divisor.

These tests catch the kind of rot that accumulates in prompt-layer agents — tables that no longer exist, coefficient orderings that drifted, or divisors that were wei / Gwei confused.

## Audit history

The fleet has been live-tested against ClickHouse to flush out prompt-vs-reality drift:

- **MMM smoke test (2026-04)** — 4 bugs in `mmm_analyst` SQL surfaced only by live execution (array-size mismatch, tuple-destructure syntax, `(k, b)` vs `(log_beta, r)` ordering, Hill grid needed mean-scaling). All patched; see [MMM reference](mmm.md#what-the-live-test-changed).
- **Persona audit (2026-04)** — 5 of 8 specialist personas had phantom `dbt.*` table references that looked authoritative. All patched with guard rules; lint tests added.
- **Custom-tools audit (2026-04)** — `get_validator_balance_history` and `get_validator_withdrawals` had wrong `database` field (`consensus` → `dbt`) and `get_validator_withdrawals` used the wrong decimal divisor (`1e18` wei-style for what is actually Gwei). Both patched.

See [MMM reference](mmm.md) for the worked smoke-test example and the SQL patches.

## Architecture selection (Phase 3)

The dispatcher persona now encodes a binding routing rule for **how** specialists should be composed (independently of *which* specialists). It picks one of three architectures based on whether the task is decomposable and how deep the sequential chain is:

| Decomposable | Sequential depth | Architecture | `parallelism` | Example |
|---|---|---|---|---|
| no  | high | Single specialist       | `single`     | "stddev of TVL over 30d" |
| no  | low  | Single specialist       | `single`     | "current bridge TVL" |
| yes | low  | Centralized parallel    | `parallel`   | "Q3 review: network + tokenomics + bridge" |
| yes | high | Centralized sequential  | `sequential` | "MMM contribution → causal review → simulation" |

**Independent (no-reviewer) parallel is forbidden.** The validating-orchestrator role (`statistical_reviewer`, `mmm_causal_reviewer`, `reality_checker`) is mandatory in any `parallel` plan. Reasoning: Google's "Science of Scaling Agent Systems" (2026) measured 17.2× error amplification on uncoordinated parallel agents vs 4.4× with a validating orchestrator.

The dispatch manifest gained a `Parallelism: <single | parallel | sequential>` line so downstream callers can see the routing decision explicitly. See [Dispatcher](dispatcher.md).

## See also

- [Dispatcher](dispatcher.md) — intent triage + routing table + manifest format
- [Workflows](workflows/index.md) — research / storyteller / sandbox flows the personas drive
- [Resumable Workflows](workflows/resumable-workflows.md) — what happens to a persona's work when it crashes
- [MMM](mmm.md) — Marketing Mix Modeling workflow end-to-end
- [Tools](tools.md) — full tool catalog
- [Reports](reports.md) — how `generate_report` assembles artifacts
- [Setup](setup.md) — connecting your MCP client
