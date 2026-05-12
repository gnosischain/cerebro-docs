# Measurement Flow (MTA + MMM + Unified)

This page is the **agent-facing reference** for measurement workflows on
Cerebro MCP. It covers how the [Cerebro Dispatcher](dispatcher.md) routes
measurement requests, which personas participate, and which dbt tables
and seeds the personas read.

For the conceptual framing of what each method does, see the research
pages: [MTA Foundations](../research/mta/index.md) and
[MMM Foundations](../research/mmm/index.md). For the dbt implementation,
see [Measurement Stack (MTA + MMM)](../data-pipeline/transformation/measurement-stack.md).

## Dispatcher routing

Every non-trivial analytics request enters Cerebro through the
[dispatcher](dispatcher.md). The dispatcher classifies the intent,
runs `preflight_analytics_request`, picks a specialist chain, and emits
a binding **dispatch manifest**. Three measurement chains are relevant
to this page:

| User intent | Chain |
|---|---|
| Per-touch credit assignment over observed user journeys ("which app actions precede topup / swap / claim", "how do first-touch and last-touch compare") | `mta_analyst` → `statistical_reviewer` → `generate_report` |
| Sector-level contribution / ROI analysis ("did the LM rewards program drive TVL", "which emissions actually moved volume") | `mmm_analyst` → `mmm_causal_reviewer` → `generate_report` |
| Combine MMM lift with MTA shares ("attribute MMM-measured lift across observed user journeys", "calibrate MTA against MMM lift") | `mmm_analyst` → `mmm_causal_reviewer` → `mta_analyst` → `unified_causal_reviewer` → `generate_report` |
| Optional follow-up — bounded prescription | `..._reviewer` PASS → `mmm_simulator` or `unified_allocator` |

The dispatcher manifest is **binding** — workflow rules encoded in
project `CLAUDE.md` (Report Workflow / MMM Workflow / Data Query SOP /
MTA Workflow) are subordinate to the manifest emitted on turn 1.

## MTA Workflow

Used when the user asks for touchpoint attribution, conversion paths, or
"which app actions precede topup / swap / claim".

1. `get_agent_persona("mta_analyst")` — adopt the SOP.
2. **Discovery is mandatory every run.** Run `search_models` /
   `discover_models`, then `describe_table` on every model used. The
   persona's "context examples" are illustrative and not a contract.
3. Build a runtime mapping (user, timestamp, touchpoint, conversion
   columns + identity grain) from `describe_table` output.
4. Volume gates: <30 conversions → descriptive only; 30–499 →
   rule-based + funnel; ≥500 → Markov + Shapley proxy allowed.
   Default lookback = 30 days; sweep 7 / 14 / 30 / 60 when volume
   permits.
5. Hand numerical claims to `statistical_reviewer`.

**MTA output is observational.** No causal claim is allowed unless paired
with MMM PASS, an experiment, or a named quasi-experimental design.

## MMM Workflow

Used when the user asks for contribution attribution, ROI across
incentive programs, budget optimisation, or "which emissions / rewards
actually drove TVL / volume / users".

1. `get_agent_persona("mmm_analyst")` — adopt the MMM SOP. The analyst
   runs spine-fill → multicollinearity check → baseline extraction →
   adstock + response-curve fit (concave and Hill; pick lower MAE) →
   contribution decomposition → SQL bootstrap for credibility intervals.
2. **Orchestration handoff (no inter-agent calls).** Synthesize the
   analyst's output into a markdown DAG table (nodes = variables,
   edges = hypothesised causation, flags = co-launched / confounded
   pairs). Then call `get_agent_persona("mmm_causal_reviewer")` and
   pass that table verbatim. The reviewer returns a pass/fail verdict.
3. **Do not call `generate_report` until the verdict is PASS.** On
   BLOCK, apply the reviewer's prescribed fixes (intervention,
   segmentation, or front-door variable) and resubmit.
4. If the user asks "what should we do next?":
   `get_agent_persona("mmm_simulator")`, passing the fitted
   `(β, r, λ, current_spend, baseline_kpi)` per media. The simulator
   bounds shifts at ±30% per period and returns marginal-ROI +
   reallocation charts.

Required charts in the final MMM report (on top of the standard
`generate_report` gates):

- Contribution stacked-area over time (`series_field = media`)
- Spend vs. effectiveness share (grouped bar)
- Response curve per media (scatter + fitted line)
- Adstock decay (bar, per media, showing λ)
- Causal-review table (from `mmm_causal_reviewer`)

## Unified MMM + MTA Workflow

Used when the user asks to combine MMM and MTA — e.g. "attribute
MMM-measured lift across observed user journeys" or "calibrate our MTA
shares against the MMM lift estimate".

1. `get_agent_persona("mmm_analyst")` and run the MMM workflow above.
2. Submit the DAG to `mmm_causal_reviewer`. **Only after PASS** proceed
   to step 3.
3. `get_agent_persona("mta_analyst")` and run the MTA workflow.
4. `get_agent_persona("unified_causal_reviewer")` and pass **both** the
   MMM artifact and the MTA artifact. The reviewer runs eight checks
   (MMM-gate, conversion consistency, incrementality bound, coverage,
   leakage, identity grain, selection bias, method stability) and
   returns PASS / BLOCK with calibration applied:

   $$
   \text{calibrated\_credit}_i = \text{raw\_mta\_credit}_i \times \frac{\text{MMM\_lift}}{\sum_j \text{raw\_credit}_j}
   $$

5. **Do not call `generate_report` until the unified verdict is PASS.**
   On BLOCK, apply the prescribed fix and resubmit.
6. Optional prescription: `get_agent_persona("unified_allocator")` for
   bounded micro / tactical recommendations. Inherits the ±30% / period
   cap from `mmm_simulator`. **Refuses to run without
   `unified_causal_reviewer` PASS.**

The unified report **must** disclose the `unexplained / untracked`
residual — the portion of MMM-estimated lift no observed touchpoint
can claim. Omitting it overstates the explanatory power of the
touchpoint set.

## Personas referenced

| Persona | Loaded via | Role |
|---|---|---|
| `mta_analyst` | `get_agent_persona("mta_analyst")` | Per-user journey + credit assignment |
| `mmm_analyst` | `get_agent_persona("mmm_analyst")` | Aggregate weekly MMM regression |
| `mmm_causal_reviewer` | `get_agent_persona("mmm_causal_reviewer")` | DAG review, PASS / BLOCK |
| `unified_causal_reviewer` | `get_agent_persona("unified_causal_reviewer")` | Eight-check unified review + calibration |
| `mmm_simulator` | `get_agent_persona("mmm_simulator")` | Bounded MMM-side reallocation |
| `unified_allocator` | `get_agent_persona("unified_allocator")` | Bounded unified prescription |

Persona source files live in `cerebro-mcp/src/cerebro_mcp/prompts/agents/`.

## Tables agents query

Personas read the materialised marts directly. The relevant tables are:

| Sector | Touchpoint table | Conversion table | Journey table | Attribution table | API view |
|---|---|---|---|---|---|
| Gnosis App | `int_execution_gnosis_app_user_events_unified` | `int_execution_gnosis_app_conversions` | `fct_execution_gnosis_app_journeys_{7,30,60}d` | `fct_execution_gnosis_app_attribution_{7,30,60}d` | `api_execution_gnosis_app_attribution_{7,30,60}d` |
| Gnosis Pay | `int_execution_gpay_user_events_unified` | `int_execution_gpay_conversions` | `fct_execution_gpay_journeys_{7,30,60}d` | `fct_execution_gpay_attribution_{7,30,60}d` | `api_execution_gpay_attribution_{7,30,60}d` |

The 30-day variant is the default. The 7-day cut is for short-attribution sensitivity sweeps; the 60-day for long-tail. The GP 60-day journey is the heaviest of the marts (3-role identity fan-out × 60-day lookback × 2-year history) — `meta.full_refresh.batch_months: 1` keeps it building, and `refresh.py` auto-retries any individual batch that pushes the 10 GiB cluster cap.

Per-day coverage diagnostics:

| Sector | Coverage table |
|---|---|
| Gnosis App | `int_execution_gnosis_app_coverage_daily` |
| Gnosis Pay | `int_execution_gpay_coverage_daily` (per `(date, kind, identity_role)`) |

Funnel diagnostics:

| Sector | Funnel table |
|---|---|
| Gnosis App | `fct_execution_gnosis_app_funnel_daily` |

MMM:

| Layer | Table |
|---|---|
| Long-form intermediates | `int_execution_mmm_kpis_weekly` / `int_execution_mmm_media_weekly` / `int_execution_mmm_controls_weekly` |
| Wide spine | `fct_execution_mmm_spine_weekly` |
| API view | `api_execution_mmm_spine_weekly` |
| Pre-computed baselines | `fct_execution_mmm_baseline_latest` |
| Collinearity matrix | `fct_execution_mmm_collinearity_latest` |

The two identity bridges
(`int_execution_gnosis_app_user_identity_bridge` and
`int_execution_gpay_user_identity_bridge`) are **not** queryable from
MCP — they are tagged `internal_only` and the `INTERNAL_ONLY_TABLES`
runtime guard rejects them at `execute_query`. See
[the implementation reference](../data-pipeline/transformation/measurement-stack.md#the-internal_only-boundary).

## Seeds that drive the pipeline

The personas reference these seeds when they need to enumerate kinds /
roles / funnels / registries without re-deriving them:

- `mta_event_kinds`, `mta_conversion_kinds`, `mta_conversion_to_event_kind`
- `mta_gp_event_kinds`, `mta_gp_conversion_kinds`,
  `mta_gp_identity_roles`, `mta_gp_conversion_to_event_kind`
- `mta_funnels` — drives `fct_execution_gnosis_app_funnel_daily`. One
  row per funnel: `funnel_name`, `step_1_event_kind`,
  `step_2_event_kind`, `step_3_event_kind`, `window_seconds`.
- `mmm_kpi_registry`, `mmm_media_registry`, `mmm_control_registry`
- `mmm_holiday_weeks`, `mmm_hardfork_steps`

## Cross-references

- [Cerebro Dispatcher](dispatcher.md) — routing details and the manifest
  format.
- [Agent Fleet](agents.md) — the full persona list.
- [Report Generation](reports.md) — `generate_report` enforcement gates.
- [MTA Foundations](../research/mta/index.md) — conceptual reference.
- [MMM Foundations](../research/mmm/index.md) — conceptual reference.
- [Measurement Stack (dbt)](../data-pipeline/transformation/measurement-stack.md) — model-by-model implementation reference.
