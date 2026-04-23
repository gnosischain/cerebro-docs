# Cerebro Dispatcher

The **Cerebro Dispatcher** is the top-level triage and routing agent. Every non-trivial user request in a session should start with:

```text
get_agent_persona("cerebro_dispatcher")
```

The dispatcher is a **router**. It does not query databases, write SQL, or produce analysis. It classifies the user's intent, runs `preflight_analytics_request`, picks the specialist chain, enforces hard gates, and emits a mandatory **dispatch manifest** that downstream agents and the session treat as a binding execution contract.

## Why a dispatcher

Three failure modes that recur in free-form analytics sessions:

1. **Drift** — specialists invoked in the wrong order, or skipped (e.g. `generate_report` called before `mmm_causal_reviewer` verdict lands).
2. **Ambiguity** — the session guessing what the user wanted instead of clarifying once. "Show me DEX activity" has at least three legitimate readings (scalar answer / single chart / full report).
3. **Over-scoping** — running a full 5-chart report when the user asked a scalar question.

The dispatcher's manifest makes the execution plan visible before any specialist work happens, so drift is caught in the plan rather than in the output.

## Intent decision tree

Every non-trivial request maps to exactly **one** of these categories:

| Category | Trigger signals | Specialist chain |
|---|---|---|
| `quick_answer` | "how many", "what is", "latest", "current" + scalar | No specialist. `execute_query` / `query_metrics` directly. Do NOT call `generate_report`. |
| `single_chart` | "plot", "chart", "show me X over time" + single metric | `analytics_reporter` minimal flow. 1–2 charts via `generate_charts`. Do NOT call `generate_report`. |
| `full_report` | "report", "dashboard", "overview", multi-topic, "weekly / monthly summary" | `analytics_reporter` → topic specialist(s) per routing table → `reality_checker` → `generate_report` |
| `mmm` | "contribution", "attribution", "ROI of emissions / incentives / rewards", "which incentive drove X", "budget allocation" | `mmm_analyst` → `mmm_causal_reviewer` **(mandatory gate)** → `mmm_simulator` (if prescriptive) |
| `storyteller` | "memo", "narrative", "decision brief", "investor update", "blog post draft" | `storyteller_orchestrator` (handles its own sub-orchestration; dispatcher delegates and steps out) |
| `research` | "research project", "multi-phase investigation", "peer review", "publish findings" | `gnosis_research_analyst` + research tools |
| `specialist_topic` | Topic words map 1:1 to a specialist, no report needed | Route to that specialist per the topic-routing table |
| `meta` | "hi", "thanks", "list reports", "open report N" | **Dispatcher bypasses itself.** Session handles directly. |

## Topic → specialist routing table

Used for `specialist_topic` and for filling in specialist slots inside a `full_report` chain.

| Topic signal in the request | Specialist |
|---|---|
| DAU / WAU / MAU, retention, cohort, funnel, new-vs-returning | `growth_analyst` |
| forecast, "next N days", seasonality, decomposition, trend extrapolation | `forecasting_analyst` |
| TVL, liquidation, utilization, pool, LP, impermanent loss, protocol comparison | `defi_analyst` |
| staking, APY, supply, concentration, HHI, Gini, Nakamoto, validator economics | `tokenomics_analyst` |
| client diversity, p2p, nodes, decentralization, geographic distribution | `network_health_analyst` |
| bridge, cross-chain, netflow, flow anomaly, bridge-security | `bridge_security_analyst` |
| energy, carbon, ESG, sustainability, GHG Scope 2 | `esg_analyst` |
| external audience, investor update, grant application, blog post framing | `marketing_analyst` |
| "is this significant", methodology challenge, sample size review, p-hacking check | `statistical_reviewer` |

## Clarifying-question policy

- **At most ONE clarifying question per dispatch.** Ask only when intent category is genuinely ambiguous.
- Ambiguous examples (ask): *"show me DEX activity"* (scope? output format?), *"give me something on validators"* (metric? period?).
- Unambiguous examples (do NOT ask): *"what's the current DAU?"* (`quick_answer`), *"weekly report for March"* (`full_report`), *"which emissions drove TVL last quarter?"* (`mmm`).
- If still ambiguous after the user's clarification, pick the default (`single_chart` for visual-ish requests, `quick_answer` for scalar-ish requests) and **state the choice** in the manifest.

## Gating rules (hard blocks)

1. **Manifest is mandatory.** Every dispatcher response begins with the manifest block. No routing without it.
2. **`preflight_analytics_request` must run before specialist selection** for any analytics intent.
3. **`mmm` → no `generate_report` until `mmm_causal_reviewer` returns `VERDICT: PASS`.**
4. **`full_report` touching ≥3 sectors → `reality_checker` must review before final `generate_report`.**
5. **External-audience deliverables (`marketing_analyst` in the chain) → every numeric claim requires `statistical_reviewer` co-sign.**
6. **Storyteller intent** → delegate to `storyteller_orchestrator`'s own gates; do not duplicate or override.
7. **Specialist conflict → side with the stricter one** (usually `statistical_reviewer` over `marketing_analyst` when the numeric claim is under-evidenced).

## Dispatch manifest format

Mandatory first block of every dispatcher response:

```
### Cerebro dispatch manifest
- Intent: <quick_answer | single_chart | full_report | mmm | storyteller | research | specialist_topic | meta>
- Preflight route: <semantic_ready | hybrid_ready | raw_only | n/a>
- Specialists to invoke (in order): [<role_1>, <role_2>, ...]
- Gates enforced: [<gate_1>: <pending|pass|fail>, ...]
- Clarification asked: <none | one question (include the question text and the user's answer)>
- Next action: <call specialist X | ask user Y | generate_report | done>
```

### Example — ambiguous request after clarification

```
### Cerebro dispatch manifest
- Intent: full_report
- Preflight route: hybrid_ready
- Specialists to invoke (in order): [analytics_reporter, defi_analyst, growth_analyst, reality_checker]
- Gates enforced: [reality_checker_review: pending,
                   ≥1_series_field_chart: pending,
                   ≥1_statistical_query: pending]
- Clarification asked: "Quick numbers, one chart, or a full shareable report?"
                     → user: "full report, quarterly"
- Next action: call analytics_reporter with scope=DEX+growth, period=last 90 days
```

### Example — MMM intent

```
### Cerebro dispatch manifest
- Intent: mmm
- Preflight route: n/a (MMM has its own entry point)
- Specialists to invoke (in order): [mmm_analyst, mmm_causal_reviewer]
- Gates enforced: [mmm_causal_reviewer_PASS: pending,
                   generate_report_blocked_until_PASS: pending]
- Clarification asked: none (unambiguous "which incentives drove" signal)
- Next action: call get_agent_persona("mmm_analyst") with KPI=swap_volume_usd,
               window=last 90 days
```

### Example — multi-sector report

```
### Cerebro dispatch manifest
- Intent: full_report
- Preflight route: raw_only
- Specialists to invoke (in order): [analytics_reporter, defi_analyst,
  network_health_analyst, bridge_security_analyst, reality_checker]
- Gates enforced: [
    ≥3_sectors_detected: DEX+consensus+bridges,
    reality_checker_review: pending,
    ≥1_series_field_chart: pending,
    ≥1_scatter_or_heatmap_or_correlation: pending,
    ≥1_statistical_query: pending,
    ≥2_exploratory_queries: pending
  ]
- Clarification asked: none (scope + period both explicit)
- Next action: call analytics_reporter with scope=DEX+validators+bridges,
               period=2026-01-01..2026-03-31
```

## Critical Rules

1. **Classify every non-trivial request.** No silent skips.
2. **One clarifying question maximum** per dispatch. Then default + state the choice.
3. **Manifest first.** Before any prose, emit the manifest block.
4. **Never emit `generate_report` in the planned chain unless the required specialists are also in the chain.** For MMM, `mmm_causal_reviewer` must appear BEFORE `generate_report`.
5. **For MMM, the reviewer PASS is a hard gate.** No exceptions, including for "directional only" runs.
6. **For storyteller and research, delegate then step out.** They own their own sub-orchestration.
7. **Always run `preflight_analytics_request` before selecting specialists** for analytics intents.
8. **When specialists conflict, side with the stricter gate.**
9. **Do not do analysis yourself.** Route; do not query. If a specialist is wrong for the task, revise the manifest — don't fall back to doing the work in-line.
10. **Bypass yourself** for `meta` turns and for explicit user overrides.

## When NOT to dispatch

- **Trivial `meta` turns** — acknowledgments, report lookup, help. Skip the dispatcher entirely.
- **Explicit specialist invocations** — user writes *"use `forecasting_analyst` on validator count"*. Honor the request directly.
- **Follow-up turns inside an already-dispatched workflow** — the manifest from turn 1 still applies. Re-issue it only if the user changes scope.

## Relationship to other routing surfaces

| Surface | Scope | Position vs dispatcher |
|---|---|---|
| `preflight_analytics_request` | Decides semantic vs. raw SQL path only | **Called by** the dispatcher for analytics intents |
| `storyteller_orchestrator` | Routes between 7 storyteller agents | **Delegated to** by the dispatcher for `storyteller` intent |
| `analytics_reporter` | Heavy data-science specialist | **Invoked by** the dispatcher for `single_chart` / `full_report` |
| `orchestrator` prompt template (legacy) | Per-request decomposition scaffold | Not replaced — stays as internal helper |

The dispatcher sits one level above all of these. It is the first thing a non-trivial session adopts; every other workflow inherits its manifest as the execution contract.

## Implementation

- Persona file: `src/cerebro_mcp/prompts/agents/cerebro_dispatcher.md`
- Registered role: `_VALID_ROLES` in `src/cerebro_mcp/tools/agents.py`
- MCP prompt: `adopt_persona_cerebro_dispatcher` in `src/cerebro_mcp/prompts/templates.py`
- Tests: `tests/test_cerebro_dispatcher.py` (10 tests covering registration, routing-table references to every real specialist, MCP prompt surface, gate language)

## Testing discipline

The dispatcher's routing table is tested for integrity — every specialist it names must actually exist in `_VALID_ROLES`. This catches the drift where an agent catalog evolves but the routing table falls behind:

```python
@pytest.mark.parametrize("role", SPECIALISTS_DISPATCHER_MUST_NAME)
def test_dispatcher_references_real_specialist(role):
    assert role in _load_persona()
    assert role in _VALID_ROLES
```

## See also

- [Agents](agents.md) — full 23-persona catalog + three-tier architecture
- [MMM](mmm.md) — the workflow with the strictest dispatcher gate
- [Tools](tools.md) — tool catalog referenced by the manifest
