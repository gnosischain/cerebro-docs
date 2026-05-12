# Measurement Stack (MTA + MMM)

This page is the **implementation reference** for the 24 dbt models that
back Multi-Touch Attribution and Marketing Mix Modeling on Gnosis sectors.
For the conceptual framing of MTA see [the MTA Foundations
page](../../research/mta/index.md); for MMM see [the MMM Foundations
page](../../research/mmm/index.md).

## Why this is a dbt stack and not a semantic-layer query

The Cerebro semantic layer covers most analytics with composable
metric / dimension definitions. The measurement stack lives in dbt
because each layer breaks an assumption the semantic layer makes:

- **The pseudonym salt is build-time only.** `pseudonymize_address`
  reads `CEREBRO_PII_SALT` from the dbt environment. The salt is **never**
  exposed at query time, so a hash from a raw address can only be
  produced inside a dbt run. Identity bridges therefore cannot be
  expressed as a semantic metric — they must be materialised tables.
- **Journey spines are relational, not aggregate.** The semantic layer
  composes aggregate measures over dimensional cuts. A journey is a
  per-conversion ordered list of prior touchpoints — a JOIN, not an
  aggregate. Materialising the JOIN once (with leakage guards baked in)
  saves every downstream query from re-doing it.
- **The MMM weekly spine needs continuous-time fill.** The regression
  pipeline must see every week even when no upstream source emitted a
  row. The dbt intermediates use the `weekly_spine` macro plus
  registry-driven `LEFT JOIN` to manufacture the missing weeks. A
  semantic-layer query over the raw sources would silently truncate.
- **Per-row credit math depends on per-conversion aggregates.** The
  attribution mart computes `td_raw / sum(td_raw) per conversion` for
  the time-decay rule and `1 / count(*) per conversion` for linear.
  These are window-style aggregates that the v3 implementation rewrote
  as pre-aggregate-then-JOIN to fit the 10 GiB memory cap (see the
  attribution mart description below).
- **OOM constraints.** The role fan-out × 30-day lookback for GP
  journeys OOM'd at the cluster's per-query memory cap on a single
  pass; the dbt model uses `meta.full_refresh.batch_months: 1` so
  `scripts/full_refresh/refresh.py` rebuilds it month-by-month.
  Semantic-layer queries can't express that.

## The `internal_only` boundary

Two models in the stack are tagged `internal_only` +
`privacy:tier_internal` and configured with `meta.expose_to_mcp = false`:

- `int_execution_gnosis_app_user_identity_bridge`
- `int_execution_gpay_user_identity_bridge`

These bridges are the **only** place in the warehouse where raw
addresses live alongside pseudonyms. cerebro-mcp's `discover_models`
filter hides them from agents, the `INTERNAL_ONLY_TABLES` runtime guard
denies them from `execute_query`, and cerebro-api never registers a
route for them (no `api:<resource>` tag). Every other model in the
stack reads from the bridge once at build time and keys on
`user_pseudonym` thereafter.

See [Privacy & Pseudonyms](privacy-pseudonyms.md) for the full
pseudonymization approach.

## The 24-model layout

### Gnosis App (10 models)

| Layer | Model | Purpose |
|---|---|---|
| Identity | `int_execution_gnosis_app_user_identity_bridge` | Raw `address` ↔ `user_pseudonym` pairing. **Internal only.** |
| Touchpoints | `int_execution_gnosis_app_events_chain_unified` | Long-form chain event log keyed by pseudonym. UNIONs onboard, six heuristic kinds, swap_signed, swap_filled, topup, marketplace_buy, token_offer_claim. |
| Touchpoints | `int_execution_gnosis_app_events_mixpanel_unified` | Long-form Mixpanel event log (existing model, referenced for completeness). |
| Touchpoints | `int_execution_gnosis_app_user_events_unified` | UNION ALL of chain + Mixpanel — the touchpoint table the MTA persona reads. |
| Conversions | `int_execution_gnosis_app_conversions` | One row per conversion with `conversion_kind` as a column (topup / swap_filled / token_offer_claim / marketplace_buy). |
| Diagnostics | `int_execution_gnosis_app_coverage_daily` | Per-(date, kind) tracked-coverage stats with the leakage guard pre-applied. |
| Marts | `fct_execution_gnosis_app_journeys_{7,30,60}d` | Pre-joined journey spine via `build_journey_lookback(N, 'gnosis_app')`. The 30d cut is the default; 7d and 60d are sensitivity-sweep variants emitted from the same macro. |
| Marts | `fct_execution_gnosis_app_funnel_daily` | `windowFunnel` diagnostics driven by seed `mta_funnels.csv`. |
| Marts | `fct_execution_gnosis_app_attribution_{7,30,60}d` | First / last / linear / time-decay credit per (kind, event_kind) over the 180-day window. Time-decay half-life is fixed at 7 days regardless of lookback (it is a customer-decay parameter, not a window parameter). |
| API | `api_execution_gnosis_app_attribution_{7,30,60}d` | View passthrough, Tier1, `granularity:rolling_180d`. |

### Gnosis Pay (7 models)

The GP stack mirrors the GA stack with **one extra column on every model:
`identity_role`** (LowCardinality, values `safe_self` / `initial_owner` /
`delegate`).

| Layer | Model | Purpose |
|---|---|---|
| Identity | `int_execution_gpay_user_identity_bridge` | Raw `address` × `identity_role` ↔ `user_pseudonym` pairing. **Internal only.** A 2-owner Safe with 1 delegate yields 4 rows. |
| Touchpoints | `int_execution_gpay_user_events_unified` | Chain card / safe activity, role-fanned-out. `event_kind` ∈ `gp.payment` / `gp.cashback_claim` / `gp.deposit` / `gp.withdrawal` / `gp.action_other`. |
| Conversions | `int_execution_gpay_conversions` | `gpay_payment` / `gpay_cashback_claim` / `gpay_funded` (first-ever inflow, computed across full history). |
| Diagnostics | `int_execution_gpay_coverage_daily` | Per-(date, kind, role) tracked coverage. |
| Marts | `fct_execution_gpay_journeys_{7,30,60}d` | `build_journey_lookback(N, 'gpay')` — adds `identity_role` to the JOIN. Microbatched in 1-month chunks (3-role × Nd lookback OOM'd single-pass on the 10 GiB cluster cap). The 60d variant is the heaviest of the three: monthly batches occasionally push the 10 GiB cap and `refresh.py` auto-retries the rare batch that does. |
| Marts | `fct_execution_gpay_attribution_{7,30,60}d` | First / last / linear / time-decay per (kind, role, event_kind). |
| API | `api_execution_gpay_attribution_{7,30,60}d` | View passthrough, Tier1. |

### MMM (7 models)

| Layer | Model | Purpose |
|---|---|---|
| Intermediate | `int_execution_mmm_kpis_weekly` | Long-form weekly KPI registry. Continuous spine via `weekly_spine` macro. |
| Intermediate | `int_execution_mmm_media_weekly` | Long-form weekly media (incentive / reward / outlay) registry. |
| Intermediate | `int_execution_mmm_controls_weekly` | Long-form weekly controls (gas, prices, week-of-year, holiday, hardfork step). |
| Marts | `fct_execution_mmm_spine_weekly` | Wide-pivot spine — one row per week, one column per (kpi \| media \| control). The MMM analyst's regression input. |
| Marts | `fct_execution_mmm_baseline_latest` | Per-(KPI, media) baseline median over weeks where the media's adstocked spend (λ=0.5) is in the bottom decile. |
| Marts | `fct_execution_mmm_collinearity_latest` | Pairwise Pearson correlation matrix between media columns over the trailing 730 days. |
| API | `api_execution_mmm_spine_weekly` | View passthrough, Tier1, `granularity:weekly`. |

## Macros that bind the stack

- `pseudonymize_address(expr)` — keyed `sipHash64` over the salted,
  lowercased address. Deterministic; the salt comes from
  `CEREBRO_PII_SALT`. Same macro is used at Mixpanel ingestion so the
  hashes line up.
- `build_journey_lookback(lookback_days, sector)` — generates the body
  of the per-sector journey spine mart. GP variant adds an
  `identity_role` equality to the conversion ↔ events join. Used by the
  live 30d marts and any future 7d / 14d / 60d sensitivity-sweep
  variants.
- `conversion_kind_to_event_kind(expr)` — `multiIf` mapping each
  `conversion_kind` to its corresponding event_kind. Used by the
  journey spine and the coverage_daily models to apply the
  self-exclusion leakage guard. Mirrors seeds
  `mta_conversion_to_event_kind.csv` and
  `mta_gp_conversion_to_event_kind.csv` — when a new conversion kind
  is added, the macro **and** the seed must both be updated.
- `weekly_spine(start, end)` — emits a continuous Monday-start week
  spine. Backs every MMM intermediate so missing-source-week rows are
  manufactured rather than truncated.
- `apply_monthly_incremental_filter(...)` — standard incremental
  watermark pattern; not new but used pervasively here.

## Seeds that drive the stack

| Seed | Drives |
|---|---|
| `mta_event_kinds.csv` | Validates GA `event_kind` values (relationship test). |
| `mta_conversion_kinds.csv` | Validates GA `conversion_kind` values. |
| `mta_conversion_to_event_kind.csv` | Documents the GA self-exclusion mapping. |
| `mta_gp_event_kinds.csv` | Validates GP `event_kind` values. |
| `mta_gp_conversion_kinds.csv` | Validates GP `conversion_kind` values. |
| `mta_gp_identity_roles.csv` | Validates `identity_role` values (`safe_self` / `initial_owner` / `delegate`). |
| `mta_gp_conversion_to_event_kind.csv` | Documents the GP self-exclusion mapping. |
| `mta_funnels.csv` | One row per funnel; drives `fct_execution_gnosis_app_funnel_daily`. |
| `mmm_kpi_registry.csv` | One row per KPI — name, units, value method, source model, `is_dedup_safe`. Drives the weekly spine fill. |
| `mmm_media_registry.csv` | One row per media — name, units, `is_outlay`, value method, source model. |
| `mmm_control_registry.csv` | One row per control — name, value method, source model. |
| `mmm_holiday_weeks.csv` | Hand-curated holiday weeks (drives `ctrl_is_holiday_week`). |
| `mmm_hardfork_steps.csv` | Hardfork dates (drives `ctrl_hardfork_step`). |

## OOM mitigations worth knowing about

- **GP journeys 30d.** The 3-role fan-out × all GP activity × 30-day
  lookback OOM'd at the 10 GiB cluster cap on a single 2-year
  full-refresh. The model is configured with
  `meta.full_refresh.batch_months: 1`; `scripts/full_refresh/refresh.py`
  drives the per-month batches and auto-retries the rare batch that
  pushes the limit.
- **Attribution mart v3 rewrite.** The first attempt used
  `groupArray + arraySort + ARRAY JOIN`; the second used window
  functions partitioned by (user, conversion). Both OOM'd because the
  partition key forced a 12 M-row sort. The current implementation
  pre-aggregates per conversion (~22 k rows), then JOINs back to score
  per touch. Sort space drops from 12 M to ~22 k. Pure GROUP BY +
  LEFT JOIN, no window functions, no array materialisation.
- **DEX volume dedup.** A per-tx dedup CTE on
  `int_execution_pools_dex_trades` OOM'd at the 10 GiB cap. The
  `dex_volume_usd_dedup` KPI accepts the known multi-hop overcount
  (first-hop-only) and surfaces `is_dedup_safe = false` on every row.
  Downstream consumers (and the analyst persona) see the flag and
  caveat any conclusions.
- **Grace-hash join algorithm.** Models that JOIN the bridge to wide
  upstreams set `pre_hook=["SET join_algorithm = 'grace_hash'"]` and
  reset in `post_hook` to keep peak memory bounded across the UNIONs.

## Cross-references

- [Privacy & Pseudonyms](privacy-pseudonyms.md) — the keyed-hash design.
- [Incremental Strategies](incremental-strategies.md) — `delete+insert`
  vs `append`, how `start_month` / `end_month` vars drive batched runs.
- [MTA Foundations](../../research/mta/index.md) — the conceptual layer.
- [MMM Foundations](../../research/mmm/index.md) — the conceptual layer.
- [Measurement Flow (MCP)](../../mcp/measurement-flow.md) — how agents
  consume these models.
