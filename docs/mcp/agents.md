# Agent Fleet

Cerebro MCP ships with **23 agent personas** — prompt-layer guidance the LLM adopts for a specific phase of work. Each persona has a narrow contract (identity, rules, SQL toolkit when relevant, success metrics) and is loaded via:

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
│  esg_analyst   statistical_reviewer                           │
│  + 6 storyteller sub-phases                                   │
└───────────────────────────────────────────────────────────────┘
```

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

All 23 personas are reachable via `get_agent_persona(role)`.

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

## See also

- [Dispatcher](dispatcher.md) — intent triage + routing table + manifest format
- [MMM](mmm.md) — Marketing Mix Modeling workflow end-to-end
- [Tools](tools.md) — full tool catalog
- [Reports](reports.md) — how `generate_report` assembles artifacts
- [Setup](setup.md) — connecting your MCP client
