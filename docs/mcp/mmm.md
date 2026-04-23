# Marketing Mix Modeling (MMM)

Cerebro ships with a gated **Marketing Mix Modeling** workflow that adapts the Hakuhodo DY / Google framework to on-chain incentive attribution on Gnosis Chain. When a user asks *"which emissions actually drove TVL?"* or *"what is the ROI of our liquidity-mining program?"* — this is the workflow.

!!! info "Looking for the method itself?"
    This page is the **tooling reference**. For the long-form explainer of MMM as a method — response curves, adstock, Bayesian estimation, the 9 validation checkpoints, and the causal-DAG rules from Chapter 3 of the guidebook — see [Research / Marketing Mix Modeling (MMM)](../research/mmm/index.md).

!!! tip "Day-to-day usage"
    For the practical playbook — prompt phrasing, data sufficiency checks, a Sector Readiness Matrix, reading fitted coefficients, and copy-pasteable recipes — see the **[MMM User Guide](mmm-user-guide.md)**. It's the shortest path from user question to a defensible attribution answer.

MMM here is prompt-layer only. No new MCP tools, no schema changes. Three personas (`mmm_analyst`, `mmm_causal_reviewer`, `mmm_simulator`) coordinate via a hard-gated handoff pattern that blocks `generate_report` until a DAG review passes.

## Crypto ↔ MMM mapping

The translation from traditional advertising MMM to on-chain DeFi:

| MMM concept | Gnosis-sector analog | Typical data source |
|---|---|---|
| Media spend / impressions | Token emissions, LM rewards, validator APR, bridge incentives | `dbt.stg_consensus__withdrawals`, `fct_execution_yields_opportunities_latest`, contracts module |
| Business KPI | TVL, DEX volume, DAU, tx count, bridge deposits, yield flows | execution + contracts sectors |
| Control variables | Gas price, ETH / stablecoin macro moves, holidays, protocol launches | existing time-series |
| Confounders | Simultaneous launches (typical in DeFi) | DAG structure + intervention pattern |
| Response curve | Diminishing returns on incentives | Hill (S-shape) or concave log-log |
| Adstock | Delayed user retention after incentives end | Geometric decay λ |

## The three-agent pipeline

```
┌─────────────────┐    DAG handoff    ┌──────────────────────┐
│  mmm_analyst    │──────────────────▶│  mmm_causal_reviewer │
│                 │   (markdown table │                      │
│  spine→corr→    │    of nodes+edges)│  chronological /     │
│  baseline→      │                   │  non-inclusion /     │
│  adstock→fit    │                   │  identifiability     │
└─────────────────┘                   └──────────┬───────────┘
                                                 │ VERDICT
                      ┌──────────────────────────┴──────────┐
                      │                                     │
                      ▼ PASS                                ▼ BLOCK
              ┌───────────────────┐              ┌──────────────────────┐
              │  generate_charts  │              │  Apply prescribed    │
              │  (5 required)     │              │  fix; re-submit DAG  │
              │  generate_report  │              └──────────────────────┘
              └─────────┬─────────┘
                        │ optional
                        ▼
                ┌──────────────────┐
                │  mmm_simulator   │  (marginal ROI + ±30% reallocation)
                └──────────────────┘
```

## Personas

### `mmm_analyst`

Runs the full SOP on a chosen sector. Covers 13 Critical Rules, a 7-step ClickHouse toolkit, and a "When NOT to use" list.

**SOP:**

1. **Discover** — `search_models` for KPI + "media" (incentive) variables.
2. **Verify** — `describe_table` for column names and grain.
3. **Spine-fill** — continuous weekly time spine (no missing weeks).
4. **Multicollinearity** — pairwise correlation; merge/drop/segment any |corr| > 0.9.
5. **Baseline** — extract baseline KPI from bottom-decile-adstock weeks.
6. **Transform** — geometric adstock per media.
7. **Fit** — concave (log-log) AND Hill grid search per media; pick lower holdout MAE.
8. **Decompose** — per-week contribution per media → stacked-area chart.
9. **DAG handoff** — emit a markdown DAG table; session passes to `mmm_causal_reviewer`.
10. **Report** — `generate_charts` (5 required) → `generate_report`.

**Strictly refuses:**

- Sectors with <60 weekly rows (downgrades output to "directional only" with a banner)
- Single-campaign scenarios (use A/B attribution instead)
- Structural-break windows (hardforks, bridge exploits) without an explicit step-dummy
- KPI variance dominated by a single outlier week

### `mmm_causal_reviewer`

DAG gate. Receives a markdown table from the session (nodes = variables, edges = hypothesized causation, flags = co-launched / confounded pairs). Runs the three Hakuhodo Guidebook Ch.3 checks and returns a structured verdict.

**Verdict table format:**

```markdown
| Check | Guidebook ref | Verdict | Evidence |
|---|---|---|---|
| Chronological (cause before effect) | p.91 | pass / fail | cite edges; flag any running backwards in time |
| Non-inclusion (no overlapping variables) | p.92 | pass / fail | list variable pairs checked |
| Identifiability (no unresolved confounding) | p.93, 120–129 | pass / fail + recommendation | list confounded edges + fix |

VERDICT: PASS  |  BLOCK
```

**Prescribed fixes on identifiability failure (priority order):**

1. **Intervention pattern** — cite an existing "dark period" or staggered flight that preserves identifiability.
2. **Segmentation** — split the DAG by audience or protocol so within-segment correlation drops.
3. **Front-door variable** — propose an intermediate node satisfying the front-door criterion. Crypto-specific candidates:
      - Unique-wallet count (between incentive and TVL)
      - Brand-query proxy (explorer page views, governance-forum mentions)
      - Bridge-inflow lag (between ecosystem campaign and on-chain KPI)
4. **Dark-period request** — recommend a future intentional pause of one incentive.

**Refuses to**: quote coefficients, run SQL, or touch the actual numbers. Review DAG text only.

### `mmm_simulator`

Prescription step. Given fitted `(β, r, λ, current_spend, baseline_kpi)` per media, computes marginal ROI and a reallocation bounded at ±30%/period.

```sql
-- Marginal ROI = d(KPI)/d(spend) = β · r · spend^(r-1)
SELECT
  media, beta, r, current_spend,
  beta * r * pow(current_spend, r - 1) AS marginal_roi,
  (beta * pow(current_spend, r)) / current_spend AS avg_roi
FROM fitted_curves
ORDER BY marginal_roi DESC;
```

**Hard rules:**

- Never suggest >30% week-over-week shift for a single media (Guidebook p.80 footnote).
- Never extrapolate beyond 1.5× max historical `current_spend` without an "out-of-sample — high uncertainty" annotation.
- Never zero out a media on a single window — recommend "observe under reduced spend" as a dark-period intervention (which also improves future identifiability).
- Refuses to run without a passing `mmm_causal_reviewer` verdict in the session.

## ClickHouse MMM Toolkit

The full SQL toolkit ships inside `mmm_analyst.md`. Key snippets below.

### 1. Multicollinearity check (VIF proxy)

```sql
-- Flag incentive variables that move together (>0.9 correlation)
SELECT
  corr(emissions_protocol_a, emissions_protocol_b) AS corr_ab,
  corr(emissions_protocol_a, validator_rewards)    AS corr_av,
  corr(emissions_protocol_b, validator_rewards)    AS corr_bv
FROM weekly_incentives
WHERE week >= today() - INTERVAL 2 YEAR;
-- Any |corr| > 0.9 → merge, drop, or segment (Guidebook p.38)
```

### 2. Continuous time spine + geometric adstock

```sql
-- FIRST fill missing weeks with 0 emissions (sparse event data is common)
WITH spine AS (
  SELECT
    toStartOfWeek(toDate(week)) AS week,
    coalesce(sum(emissions), 0) AS emissions
  FROM weekly_incentives
  WHERE week >= today() - INTERVAL 2 YEAR
  GROUP BY week
  ORDER BY week WITH FILL STEP toIntervalWeek(1)
),
-- THEN build variable-length window arrays per row
windowed AS (
  SELECT
    week, emissions,
    arrayReverse(groupArray(emissions) OVER (
      ORDER BY week ROWS BETWEEN 8 PRECEDING AND CURRENT ROW
    )) AS emissions_win
  FROM spine
)
-- FINALLY apply geometric decay. IMPORTANT: use range(length(arr)), not range(9) —
-- the window is shorter than 9 at the start of the series, and arrayMap raises
-- SIZES_OF_ARRAYS_DONT_MATCH if the index array is longer.
SELECT
  week, emissions,
  arraySum(arrayMap((x, i) -> x * pow(0.5, i),
    emissions_win,
    range(length(emissions_win))
  )) AS emissions_adstock
FROM windowed
ORDER BY week;
```

### 3. Baseline extraction (required before log-log)

```sql
-- KPI-when-spend-is-near-zero: median KPI during bottom-decile adstock weeks.
-- Prevents log(0) and prevents the multiplicative model from implying KPI→0
-- when emissions→0 (which is false for TVL — organic demand still exists).
WITH thresholds AS (
  SELECT quantile(0.1)(emissions_adstock) AS p10 FROM transformed_weekly
)
SELECT quantile(0.5)(tvl) AS baseline_tvl
FROM transformed_weekly, thresholds
WHERE emissions_adstock <= p10;
```

### 4. Concave fit on INCREMENTAL KPI

```sql
-- Estimate β, r in (KPI − baseline) = β · adstock^r via log-log regression.
-- ClickHouse simpleLinearRegression returns Tuple(k, b) where:
--   k = SLOPE  → r (diminishing-returns exponent)
--   b = INTERCEPT  → log(β), so β = exp(b)
-- There is NO "AS (a, b)" tuple-destructure syntax — alias the whole tuple
-- and access via .1 (slope) and .2 (intercept).
SELECT
  fit.1 AS r,
  exp(fit.2) AS beta
FROM (
  SELECT
    simpleLinearRegression(
      log(emissions_adstock),
      log(greatest(tvl - {baseline_tvl:Float64}, 1))
    ) AS fit
  FROM transformed_weekly
  WHERE emissions_adstock > 0
    AND tvl > {baseline_tvl:Float64}
);
-- r < 1 → diminishing returns (concave curve). r > 1 is a red flag.
```

### 5. Hill (S-shape) fit via SQL grid search

```sql
-- simpleLinearRegression cannot fit Hill directly.
-- IMPORTANT: mean-scale both axes before gridding — K ∈ [0.05..1] is meaningless
-- against raw-unit adstock in the millions.
WITH
  scales AS (
    SELECT avg(emissions_adstock) AS s_ad, avg(tvl) AS s_kpi
    FROM transformed_weekly WHERE emissions_adstock > 0
  ),
  scaled AS (
    SELECT
      emissions_adstock / (SELECT s_ad FROM scales)  AS x,
      tvl / (SELECT s_kpi FROM scales)               AS y
    FROM transformed_weekly WHERE emissions_adstock > 0
  ),
  grid AS (
    SELECT arrayJoin(range(1, 21)) * 0.05 AS K,   -- K in [0.05..1.0]
           arrayJoin(range(1, 11)) * 0.5  AS S    -- S in [0.5..5.0]
  )
SELECT K, S,
       avg(abs(y - 1.0 / (1.0 + pow(x / K, -S)))) AS mae
FROM scaled CROSS JOIN grid
GROUP BY K, S
ORDER BY mae ASC LIMIT 1;
-- K and S returned are in scaled-unit space; multiply back by scales to interpret.
```

### 6. Contribution decomposition

```sql
-- Per-media predicted incremental KPI per week → backs the stacked-area chart
SELECT
  week,
  beta_a * pow(emissions_a_adstock, r_a) AS contrib_a,
  beta_b * pow(emissions_b_adstock, r_b) AS contrib_b,
  tvl - (beta_a * pow(emissions_a_adstock, r_a)
       + beta_b * pow(emissions_b_adstock, r_b)) AS residual
FROM transformed_weekly;
```

## Required charts in the MMM report

On top of the standard `generate_report` gates, an MMM report must include all five of these:

1. **Contribution stacked-area** over time (`series_field = media`)
2. **Spend vs. effectiveness share** (grouped bar) — reveals the familiar MMM misalignment between what you *spent* and what it *delivered*
3. **Response curve per media** (scatter + fitted line)
4. **Adstock decay** (bar per media, showing λ)
5. **Causal-review table** (markdown, from `mmm_causal_reviewer`)

## Workflow — end to end

```text
1. get_agent_persona("mmm_analyst")
2. Run the SOP: spine → corr check → baseline → adstock → concave + Hill fit → decompose
3. Synthesize the DAG as a markdown table:
   | Node | Variable | Source |
   | T    | claims_adstock | … |
   | P    | topups_adstock | … |
   | Y    | kpi_swap_volume | … |
   Edges: T→Y, P→Y, (optional: T→intermediate→Y)
   Flags: any co-launched / confounded pairs
4. get_agent_persona("mmm_causal_reviewer") — pass the DAG table verbatim
5. On BLOCK: apply prescribed fix, re-submit
   On PASS: proceed
6. generate_charts (batch, 5 required specs)
7. generate_report
8. Optional: get_agent_persona("mmm_simulator")
   - Pass fitted (β, r, λ, current_spend, baseline_kpi) per media
   - Returns marginal-ROI bar + ±30%-bounded allocation pie
```

## Worked example — Gnosis App (live smoke test)

A live run on three Gnosis App weekly tables produced these findings on ~24 weeks of data (directional only — below the 60-row floor).

**Tables used**:

- KPI: `dbt.fct_execution_gnosis_app_swaps_weekly.volume_usd_filled`
- Media A (incentive proxy): `dbt.fct_execution_gnosis_app_token_offer_claims_weekly.volume_received_usd`
- Media B (engagement proxy): `dbt.fct_execution_gnosis_app_gpay_topups_weekly.volume_usd`

**Multicollinearity:** all |corr| < 0.3 — no merging needed.

**Fitted curves (24 weeks, λ=0.5, 8-week adstock window):**

| Media | r | β | Interpretation |
|---|---|---|---|
| Claims | 0.118 | ≈4,953 | Very concave → already at saturation; extra claim-$ buys almost no incremental swap-$ |
| Topups | 0.458 | ≈2,623 | More elastic → marginal ROI headroom remains inside observed range |

**Hill comparison:** MAE ≈ 0.49 on scaled data vs. concave's clean fit → **concave wins** at this sample size. Rule 13 ("data-driven curve selection") correctly defaulted to concave.

**Causal review verdict (initial DAG):** **BLOCK**

- Chronological: pass
- Non-inclusion: pass
- Identifiability: **fail** — unobserved `n_ga_users` (Gnosis App user growth) likely drives both claims and topups and swaps (classic back-door per Guidebook p.123)

**Prescribed fix applied:** add `n_ga_users` as a front-door intermediate per Guidebook p.124 + add sin/cos(2π · weekOfYear/52) as a seasonality control. Revised DAG verdict: **PASS**.

**Simulator recommendation:**

| Media | Current spend share | Fitted r | Marginal ROI | Recommendation |
|---|---|---|---|---|
| Claims | ~42% | 0.118 | ~0 (saturated) | **Reduce 30% or hold** — past the knee |
| Topups | ~58% | 0.458 | Non-trivial | **Increase up to 30%** — headroom remains |

## What the live test changed

Four real SQL bugs surfaced only by running the persona against ClickHouse. All are fixed in the current `mmm_analyst` persona; the fixes are documented here so future edits don't regress.

| # | Bug | Fix |
|---|---|---|
| 1 | `arrayMap((x, i) → x · λⁱ, window, range(9))` raised `SIZES_OF_ARRAYS_DONT_MATCH` at the series start — the window is shorter than 9 until the 9th row. | Replaced with `range(length(win))`. |
| 2 | `simpleLinearRegression(...) AS (log_beta, r)` raised `SYNTAX_ERROR` — ClickHouse does not support tuple-destructure aliases. | Alias the whole tuple, access with `.1` / `.2`. |
| 3 | Persona documented the tuple as `(log_beta, r) = (intercept, slope)`, but ClickHouse actually returns `(k, b) = (slope, intercept)` — reversed. | Persona now maps `r = .1` (slope), `β = exp(.2)` (intercept). |
| 4 | Hill grid over `K ∈ [0.05..1]` was meaningless when adstock values are in the thousands. | Added mean-scaling step; K lives in scaled space with an annotation on how to rescale. |

These are the kinds of bugs that evade unit tests — they show up only in the real SQL dialect. The accompanying regression file `tests/test_persona_sql_hygiene.py` locks the four fixes in.

## Testing discipline

Six test files keep the MMM surface honest:

| Test file | Coverage |
|---|---|
| `tests/test_mmm_agents.py` | 11 tests: persona files exist, `_VALID_ROLES` registration, required rules present ("Continuous time spine", "Baseline extraction", 30% cap) |
| `tests/test_persona_sql_hygiene.py` | Locks in the 4 live-test fixes + the 5 specialist-persona warnings |
| `tests/test_custom_tools_yaml.py` | YAML custom tools still use correct `database` field + Gwei divisor |
| `tests/test_storyteller.py` | Separate storyteller gates still green |
| `tests/test_cerebro_dispatcher.py` | Dispatcher names every real specialist including the MMM trio |

Run:

```bash
uv run pytest tests/test_mmm_agents.py tests/test_persona_sql_hygiene.py
```

## Explicit non-goals

- **No Bayesian MCMC in-process.** Response curves fit via ClickHouse `simpleLinearRegression` on log-transformed inputs; credible intervals via SQL bootstrap. True Stan / PyMC is a follow-up if point estimates become insufficient for decision-making.
- **No new ingest for off-chain marketing spend / airdrops.** If needed, that's a separate data-pipeline task.
- **No new UI mini-app.** Reports render through the existing `generate_report` HTML pipeline.

## See also

- [Dispatcher](dispatcher.md) — the top-level router that classifies a user request as `mmm` intent
- [Agents](agents.md) — the three MMM personas in the context of the full 23-persona fleet
- [Reports](reports.md) — how `generate_report` renders the final MMM artifact
