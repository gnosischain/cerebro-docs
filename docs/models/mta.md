# MTA (Attribution) Module

<!-- BEGIN AUTO-GENERATED: models-mta -->
**Gnosis**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_gnosis_app_conversions` | Intermediate | GA conversion registry — one row per observed conversion event,
with `conversion_kind` carried as a column rather tha... |
| `int_execution_gnosis_app_coverage_daily` | Intermediate | Per-day, per-conversion-kind tracked-coverage stats. The MTA
persona reads this to print the coverage block ("X% of t... |
| `int_execution_gnosis_app_events_chain_unified` | Intermediate | Long-form on-chain GA event log at full timestamp grain, keyed by
`user_pseudonym` (no raw address ever leaves the br... |
| `int_execution_gnosis_app_user_events_unified` | Intermediate | Thin UNION ALL of `int_execution_gnosis_app_events_chain_unified` +
`int_execution_gnosis_app_events_mixpanel_unified... |
| `fct_execution_gnosis_app_attribution_30d` | Fact | Pre-computed first / last / linear / time-decay (half-life = 7d)
attribution per (`conversion_kind`, `event_kind`) ov... |
| `fct_execution_gnosis_app_attribution_60d` | Fact | Pre-computed first / last / linear / time-decay (half-life = 7d)
attribution per (`conversion_kind`, `event_kind`) ov... |
| `fct_execution_gnosis_app_attribution_7d` | Fact | Pre-computed first / last / linear / time-decay (half-life = 7d)
attribution per (`conversion_kind`, `event_kind`) ov... |
| `fct_execution_gnosis_app_funnel_daily` | Fact | Per-day funnel diagnostics over `int_execution_gnosis_app_user_events_unified`
using ClickHouse `windowFunnel`. Funne... |
| `fct_execution_gnosis_app_journeys_30d` | Fact | Pre-joined GA-side journey spine with a 30-day lookback. One row per
(user_pseudonym, conversion_kind, conversion_ts,... |
| `fct_execution_gnosis_app_journeys_60d` | Fact | Pre-joined GA-side journey spine with a 60-day lookback. One row per
(user_pseudonym, conversion_kind, conversion_ts,... |
| `fct_execution_gnosis_app_journeys_7d` | Fact | Pre-joined GA-side journey spine with a 7-day lookback. One row per
(user_pseudonym, conversion_kind, conversion_ts, ... |
| `api_execution_gnosis_app_attribution_30d` | API | API view passthrough over `fct_execution_gnosis_app_attribution_30d`.
Tier1 endpoint (`api:gnosis_app_attribution_30d... |
| `api_execution_gnosis_app_attribution_60d` | API | API view passthrough over `fct_execution_gnosis_app_attribution_60d`.
Tier1 endpoint (`api:gnosis_app_attribution_60d... |
| `api_execution_gnosis_app_attribution_7d` | API | API view passthrough over `fct_execution_gnosis_app_attribution_7d`.
Tier1 endpoint (`api:gnosis_app_attribution_7d`)... |

**Gpay**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_gpay_conversions` | Intermediate | GP conversion registry. One row per (conversion event, identity_role)
pair via the bridge fan-out — every chain conve... |
| `int_execution_gpay_coverage_daily` | Intermediate | Per-day, per-(`conversion_kind`, `identity_role`) tracked-coverage
stats. Same shape as `int_execution_gnosis_app_cov... |
| `int_execution_gpay_user_events_unified` | Intermediate | Long-form GP-side chain event log keyed by
(`user_pseudonym`, `identity_role`). Source:
`int_execution_gpay_activity`... |
| `fct_execution_gpay_attribution_30d` | Fact | Pre-computed first / last / linear / time-decay (HL=7d) attribution
per (`conversion_kind`, `identity_role`, `event_k... |
| `fct_execution_gpay_attribution_60d` | Fact | Pre-computed first / last / linear / time-decay (HL=7d) attribution
per (`conversion_kind`, `identity_role`, `event_k... |
| `fct_execution_gpay_attribution_7d` | Fact | Pre-computed first / last / linear / time-decay (HL=7d) attribution
per (`conversion_kind`, `identity_role`, `event_k... |
| `fct_execution_gpay_journeys_30d` | Fact | Pre-joined GP-side journey spine with a 30-day lookback. One row per
(user_pseudonym, identity_role, conversion_kind,... |
| `fct_execution_gpay_journeys_60d` | Fact | Pre-joined GP-side journey spine with a 60-day lookback. Sensitivity-
sweep variant of the canonical `_30d` mart. Bui... |
| `fct_execution_gpay_journeys_7d` | Fact | Pre-joined GP-side journey spine with a 7-day lookback. One row per
(user_pseudonym, identity_role, conversion_kind, ... |
| `api_execution_gpay_attribution_30d` | API | API view passthrough over `fct_execution_gpay_attribution_30d`.
Tier1 endpoint (`api:gpay_attribution_30d`), requires... |
| `api_execution_gpay_attribution_60d` | API | API view passthrough over `fct_execution_gpay_attribution_60d`.
Tier1 endpoint (`api:gpay_attribution_60d`), requires... |
| `api_execution_gpay_attribution_7d` | API | API view passthrough over `fct_execution_gpay_attribution_7d`.
Tier1 endpoint (`api:gpay_attribution_7d`), requires `... |

<!-- END AUTO-GENERATED: models-mta -->
