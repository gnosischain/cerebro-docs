# Web Analytics (Mixpanel/GA) Module

<!-- BEGIN AUTO-GENERATED: models-mixpanel_ga -->
<!-- generated: 2026-07-23 -->
**Events**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_mixpanel_ga__events` | Staging | Incremental staging table over raw Mixpanel events tracking Gnosis App
(app.gnosis.io) user interactions. Extracts al... |

**Ga**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_mixpanel_ga_client_first_events` | Intermediate | -- |
| `int_mixpanel_ga_events_daily` | Intermediate | Daily event counts by event_name and event_category for Gnosis App (app.gnosis.io) production traffic only.  Tracks t... |
| `int_mixpanel_ga_geo_daily` | Intermediate | Daily event counts by country and region. |
| `int_mixpanel_ga_gnosis_app_first_events` | Intermediate | INTERNAL ONLY. One row per Gnosis App account (user_pseudonym) per
first-conversion type, with the account's Mixpanel... |
| `int_mixpanel_ga_gpay_campaign_cohorts` | Intermediate | -- |
| `int_mixpanel_ga_gpay_first_events` | Intermediate | INTERNAL ONLY. One row per Gnosis Pay account (identity_role=initial_owner)
per first-event type. event_type is 'fund... |
| `int_mixpanel_ga_gpay_pay_bridge` | Intermediate | INTERNAL ONLY. Authoritative Safe -> Gnosis App account bridge, sourced from
the Mixpanel profile `pay` property (the... |
| `int_mixpanel_ga_modals_daily` | Intermediate | Daily open counts for each modal/bottom-sheet component in Gnosis App. Sourced from events where event_category = 'mo... |
| `int_mixpanel_ga_pages_daily` | Intermediate | Daily event counts by page path and domain. |
| `int_mixpanel_ga_tech_daily` | Intermediate | Daily event counts by browser, OS, and device type. |
| `int_mixpanel_ga_traffic_daily` | Intermediate | Daily event counts by referring domain. |
| `int_mixpanel_ga_usage_patterns_daily` | Intermediate | Daily event counts by hour of day and day of week (UTC). Enables temporal usage-pattern analysis. |
| `int_mixpanel_ga_user_acquisition` | Intermediate | INTERNAL ONLY. Per-user (user_id_hash) marketing attribution. Collapses
each identified production user's sparse UTM ... |
| `int_mixpanel_ga_user_lifecycle` | Intermediate | All-time per-user lifecycle metrics for Gnosis App (app.gnosis.io)
production traffic. One row per user_id_hash. Full... |
| `int_mixpanel_ga_user_profile` | Intermediate | INTERNAL ONLY. Canonical per-Gnosis-App-account attribute dimension from the
Mixpanel profile snapshot (latest per di... |
| `int_mixpanel_ga_users_daily` | Intermediate | Per-user daily activity summary for Gnosis App (app.gnosis.io) production traffic.  One row per (date, user_id_hash).... |
| `fct_mixpanel_ga_campaign_composition` | Fact | Campaign COMPOSITION (state-based, not weekly) — the current make-up of each first-touch campaign's users from the Mi... |
| `fct_mixpanel_ga_campaign_funnel_weekly` | Fact | Weekly growth funnel by UTM, first-touch attribution. Every funnel step in one tidy long model so "which campaign att... |
| `fct_mixpanel_ga_campaign_referrals` | Fact | Campaign REFERRAL composition (state-based snapshot) — of each first-touch campaign's identified users, how many beca... |
| `fct_mixpanel_ga_card_funnel_weekly` | Fact | Weekly card-order funnel over the signup cohort (first 'Create my profile' event that ISO week — the Growth dashboard... |
| `fct_mixpanel_ga_client_conversions_weekly` | Fact | Weekly progression of client-side (Mixpanel) conversions by UTM — card_order_started / card_ordered / crc_minted / ci... |
| `fct_mixpanel_ga_funnel_daily` | Fact | Day-scoped funnel conversion metrics for Gnosis App (app.gnosis.io).
Three funnels are computed per day using uniqExa... |
| `fct_mixpanel_ga_gnosis_app_acquisition_weekly` | Fact | Weekly progression of first Gnosis App conversions, broken down by
Mixpanel UTM campaign. Tidy/long shape: one row pe... |
| `fct_mixpanel_ga_gnosis_app_daily` | Fact | Daily-cumulative view of the Gnosis App sector.

cumulative_users counts distinct addresses first-seen on or before
e... |
| `fct_mixpanel_ga_gnosis_app_users` | Fact | Per-user fact for the Gnosis App sector with Mixpanel as a CHECK,
not as a source of truth.

Every row from int_execu... |
| `fct_mixpanel_ga_gpay_acquisition_weekly` | Fact | Weekly progression of Gnosis Pay first-funded accounts and first card
transactions, broken down by Mixpanel UTM campa... |
| `fct_mixpanel_ga_gpay_campaign_metrics_weekly` | Fact | Per-campaign weekly engagement/value for Gnosis Pay accounts: of the accounts attributed to each first-touch UTM camp... |
| `fct_mixpanel_ga_gpay_campaign_retention_weekly` | Fact | Per-campaign retention for Gnosis Pay: of the accounts first funded in cohort_week (per first-touch UTM campaign), ho... |
| `fct_mixpanel_ga_gpay_crossdomain_daily` | Fact | Daily rollup of Gnosis Pay ↔ Mixpanel matching with role-bucket and
activity dimensions.

Privacy boundary: every cro... |
| `fct_mixpanel_ga_gpay_users` | Fact | Per-user fact joining Mixpanel identified users to Gnosis Pay Safes
through the keyed-pseudonym identity bridge.

One... |
| `fct_mixpanel_ga_overview_daily` | Fact | Daily KPI summary for Gnosis App (app.gnosis.io) web analytics from Mixpanel: total events, DAU, unique devices, new/... |
| `fct_mixpanel_ga_users_weekly` | Fact | Week-scoped unique-user rollup for Gnosis App Mixpanel traffic. Weekly uniques cannot be derived from the daily marts... |
| `api_mixpanel_ga_campaign_composition` | API | Not exposed via cerebro-api; accessible to the internal MCP / semantic layer. Aggregate-only pass-through view over f... |
| `api_mixpanel_ga_campaign_funnel_weekly` | API | Not exposed via cerebro-api; accessible to the internal MCP / semantic layer. Aggregate-only pass-through view over f... |
| `api_mixpanel_ga_campaign_referrals` | API | Not exposed via cerebro-api; accessible to the internal MCP / semantic layer. Aggregate-only pass-through view over f... |
| `api_mixpanel_ga_card_funnel_weekly` | API | Not exposed via cerebro-api; accessible to the internal MCP / semantic layer. Aggregate-only pass-through view over f... |
| `api_mixpanel_ga_client_conversions_weekly` | API | Not exposed via cerebro-api; accessible to the internal MCP / semantic layer. Aggregate-only pass-through view over f... |
| `api_mixpanel_ga_events_daily` | API | Not exposed via cerebro-api; accessible to the internal MCP / semantic layer. Daily event counts by
Mixpanel event_na... |
| `api_mixpanel_ga_funnel_daily` | API | Not exposed via cerebro-api; accessible to the internal MCP / semantic layer. Pass-through over
fct_mixpanel_ga_funne... |
| `api_mixpanel_ga_geo_daily` | API | Not exposed via cerebro-api; accessible to the internal MCP / semantic layer. Daily Gnosis App
geographic breakdown, ... |
| `api_mixpanel_ga_gnosis_app_acquisition_weekly` | API | Not exposed via cerebro-api; accessible to the internal MCP / semantic
layer. Aggregate-only pass-through view over
f... |
| `api_mixpanel_ga_gpay_acquisition_weekly` | API | Not exposed via cerebro-api; accessible to the internal MCP / semantic
layer. Aggregate-only pass-through view over
f... |
| `api_mixpanel_ga_gpay_campaign_metrics_weekly` | API | Not exposed via cerebro-api; accessible to the internal MCP / semantic layer. Aggregate-only pass-through view over f... |
| `api_mixpanel_ga_gpay_campaign_retention_weekly` | API | Not exposed via cerebro-api; accessible to the internal MCP / semantic layer. Aggregate-only pass-through view over f... |
| `api_mixpanel_ga_gpay_card_spend_totals_weekly` | API | GROWTH — Gnosis Pay card-spend as weekly TOTALS (no campaign dimension). Summed over
campaign from api_mixpanel_ga_gp... |
| `api_mixpanel_ga_gpay_crossdomain_daily` | API | Not exposed via cerebro-api; accessible to the internal MCP / semantic
layer. Pass-through view over fct_mixpanel_ga_... |
| `api_mixpanel_ga_gpay_funded_totals_weekly` | API | GROWTH — Gnosis Pay funded / first_payment as weekly TOTALS (no campaign dimension).
GP-side conversions are keyed to... |
| `api_mixpanel_ga_growth_campaign_weekly` | API | GROWTH — campaign-attributable Gnosis App conversion funnel by UTM campaign x week.
Aggregate-only projection of api_... |
| `api_mixpanel_ga_modals_daily` | API | Not exposed via cerebro-api; accessible to the internal MCP / semantic layer. Daily open counts for
each modal/bottom... |
| `api_mixpanel_ga_overview_daily` | API | Not exposed via cerebro-api; accessible to the internal MCP / semantic layer. Pass-through view over
fct_mixpanel_ga_... |
| `api_mixpanel_ga_pages_daily` | API | Not exposed via cerebro-api; accessible to the internal MCP / semantic layer. Daily Gnosis App page-path
analytics. O... |
| `api_mixpanel_ga_tech_daily` | API | Not exposed via cerebro-api; accessible to the internal MCP / semantic layer. Daily Gnosis App
browser / OS / device-... |
| `api_mixpanel_ga_traffic_daily` | API | Not exposed via cerebro-api; accessible to the internal MCP / semantic layer. Daily Gnosis App traffic
breakdown by H... |
| `api_mixpanel_ga_usage_patterns_daily` | API | Not exposed via cerebro-api; accessible to the internal MCP / semantic layer. Daily Gnosis App event
counts by hour-o... |
| `api_mixpanel_ga_users_daily` | API | INTERNAL ONLY — blocked from BOTH cerebro-api AND MCP. Per-user daily
activity summary for Gnosis App production traf... |
| `api_mixpanel_ga_users_weekly` | API | Not exposed via cerebro-api; accessible to the internal MCP / semantic layer. Aggregate-only pass-through view over f... |

**Gnosis**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_gnosis_app_events_mixpanel_unified` | Intermediate | Long-form Mixpanel event log filtered to identified, production
traffic and inner-joined to int_execution_gnosis_app_... |

**Profiles**

| Model | Layer | Description |
|-------|-------|-------------|
| `stg_mixpanel_ga__profiles` | Staging | One row per Mixpanel People/profile (latest snapshot), privacy-safe.
Collapses the daily full-snapshot source (mixpan... |

<!-- END AUTO-GENERATED: models-mixpanel_ga -->
