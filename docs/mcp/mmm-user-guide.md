# MMM User Guide

Practical playbook for running Marketing Mix Modeling through Cerebro MCP today. The fastest path from a user question about incentives to a defensible attribution answer.

!!! info "Companion docs"
    - **[MCP / Marketing Mix Modeling](mmm.md)** — the tooling reference (persona contracts, SQL toolkit, smoke-test worked example, patched-bug catalog)
    - **[Research / Marketing Mix Modeling](../research/mmm/index.md)** — the method theory (Hakuhodo guidebook chapter-by-chapter)
    - This page is the **how-to**. If you know *what* MMM is and *how* it's implemented, start here for day-to-day usage.

## TL;DR — the 7-step recipe

```text
1. Ask with MMM-trigger phrasing ("which incentives drove X", "ROI of Y program")
   → dispatcher routes to the mmm intent automatically
2. Pre-flight: check weekly-row count for your KPI table. ≥60 rows is the floor.
3. Let mmm_analyst run the SOP end-to-end (spine → corr → baseline → adstock → fit → decompose)
4. Write the DAG as a markdown table yourself — do not let the LLM skip this
5. Submit DAG to mmm_causal_reviewer; iterate on BLOCK verdicts
6. Only after PASS verdict → generate_charts + generate_report
7. For "what should we do?" prescriptions → mmm_simulator with fitted (β, r, λ)
```

If any step confuses you, the rest of this page expands each one with real data and copy-pasteable prompts.

---

## 1. Phrase the question to hit the `mmm` intent

The [Cerebro Dispatcher](dispatcher.md) classifies intent from keywords. Get the phrasing right and the MMM chain (with its reviewer gate) runs automatically. Get it wrong and the dispatcher routes you to a generic report flow that skips the DAG review — and you'll silently ship whatever the model fitted.

### Phrasings that land on `mmm`

- *"Which emissions actually drove TVL last quarter?"*
- *"What is the ROI of our liquidity-mining program on DEX volume?"*
- *"Attribute swap volume to the incentive streams we ran"*
- *"Reallocate our validator-reward budget for next month"*
- *"Contribution of each incentive stream to active-user growth"*
- *"Compare marginal ROI across our three rewards programs"*

### Phrasings that misroute (avoid if you want MMM)

| What you said | Where it goes | What you miss |
|---|---|---|
| "Give me a report on DEX activity" | `full_report` | No DAG review, no response-curve fitting |
| "Show me TVL by protocol" | `specialist_topic` → `defi_analyst` | Descriptive only, no causal claim |
| "Which protocols are growing?" | `specialist_topic` → `growth_analyst` | No attribution, no ROI |
| "Effect of LM on TVL" | Might land on any of the above | "Effect" is too weak — prefer "contribution" or "drove" |

### Explicit override when you know the intent

If the dispatcher misroutes, name the specialist directly. Rule 10 of the dispatcher persona respects explicit invocations:

```text
Use mmm_analyst on sector=<name>, KPI=<column>, media=[<col1>, <col2>],
window=last 104 weeks.
```

---

## 2. Pre-flight — does your sector have enough data?

The `mmm_analyst` rule 4 downgrades output to "directional only" below 60 weekly rows. The rule is there because coefficient estimates below that threshold are dominated by noise — but the model will still *produce* numbers, and it's easy to mistake noise for signal.

Run this single SQL against the KPI candidate table **before** invoking MMM:

```sql
SELECT
  count() AS n_weeks,
  min(week) AS first,
  max(week) AS last,
  dateDiff('week', min(week), max(week)) AS span_weeks
FROM dbt.<your_kpi_table>
```

For non-weekly tables, bucket to `toMonday(toDate(<timestamp_col>))` first.

### Decision tree

```
n_weeks ≥ 104 (≥2 years)  →  real MMM. Bootstrap CIs are meaningful.
n_weeks 60–103             →  Full SOP runs; caveat the credible intervals.
n_weeks 30–59              →  Directional only. Use to rank media by elasticity
                              (which is concave, which isn't). Don't quote ROI
                              numbers with intervals — they are prior artifacts.
n_weeks < 30               →  Skip MMM. Use A/B comparison or simple correlation.
```

---

## 3. Sector Readiness Matrix (Gnosis Chain, as of 2026-04-27)

Concrete week-counts from live ClickHouse, so you know what's buildable today without guessing.

| Source table | Weeks | First week | Last week | Readiness |
|---|---:|---|---|---|
| `execution.transactions` (→wk) | **394** | 2018-10 | 2026-04 | **Real MMM (≥2y)** — full history |
| `dbt.stg_consensus__validators` (→wk) | **229** | 2021-12 | 2026-04 | **Real MMM (≥2y)** |
| `dbt.stg_consensus__withdrawals` (→wk) | **143** | 2023-07 | 2026-04 | **Real MMM (≥2y)** |
| `dbt.int_bridges_flows_daily` (→wk) | **121** | 2023-12 | 2026-04 | **Real MMM (≥2y)** |
| `dbt.api_bridges_cum_netflow_weekly_by_bridge` | **120** | 2023-12 | 2026-04 | **Real MMM (≥2y)** |
| `dbt.fct_execution_gnosis_app_swaps_weekly` | 24 | 2025-11 | 2026-04 | Skip MMM; use A/B |
| `dbt.fct_execution_gnosis_app_gpay_topups_weekly` | 23 | 2025-11 | 2026-04 | Skip MMM; use A/B |
| `dbt.fct_execution_gnosis_app_token_offer_claims_weekly` | 21 | 2025-11 | 2026-04 | Skip MMM; use A/B |

### What this means in practice

- **Bridge / validator / execution-layer MMM is ready *today*.** These are the single most valuable MMM targets on Gnosis — 2+ years of weekly history, lots of natural flight variation (bridge incentive campaigns, validator-reward adjustments, hard-fork boundaries).
- **Gnosis App MMM is directional only until Q4 2026.** The tables are too young. Use them for *pattern detection* (is claims impact saturating?) but not for point ROI claims. The live smoke test in [MCP / MMM](mmm.md#worked-example-gnosis-app-live-smoke-test) demonstrates exactly this regime.
- **Run the pre-flight query for any new candidate.** The matrix above is a snapshot; new marts land regularly and the readiness flips quickly once a table crosses 60 weeks.

---

## 4. Pick a defensible KPI × media pair

The persona won't catch bad pair selection — that's your job. Use this table before investing in a full run.

| Category | Good pair | Bad pair | Why |
|---|---|---|---|
| DEX volume MMM | `execution.transactions` → weekly swap count; media = bridge-inflow spikes, LM launch flags | KPI = "Uniswap volume" + media = "total DEX volume" | Non-inclusion fail (Guidebook p.92) |
| Validator deposits | `stg_consensus__withdrawals` (→ deposit proxy); media = APR adjustments, bridge inflows | KPI = deposits, media = **APR** | APR is *computed from* deposits — inverse causation (Guidebook p.91) |
| Bridge flows | `int_bridges_flows_daily` inbound USD; media = per-bridge incentive programs, destination-chain incentives | KPI = netflow, media = gas price | Gas is a **control**, not media |
| Active users | Weekly EOA counts; media = airdrop claim events, referral bonus events | KPI = "activity", media = gas spend | Gas spend is endogenous to activity |

### Traps the reviewer will catch anyway

- **Pay-for-performance loops.** Validator APR, affiliate-style rewards — these are computed *from* the KPI. Reviewer rule on chronological check (Guidebook p.91) will BLOCK.
- **Total-vs-component.** Having `total_dex_volume` and `uniswap_volume` on the same side. Reviewer non-inclusion check (Guidebook p.92) will BLOCK.
- **Media inside KPI.** "Does swapping drive TVL?" Swaps *are* TVL flows. The data wouldn't even make sense to fit.

---

## 5. Write the DAG yourself

This is the step where the LLM most often drifts. `mmm_analyst` finishes its SOP and tells you to synthesize a DAG — **do not let it skip to `generate_report`**. The MMM flow is multi-turn by design.

### Minimum acceptable DAG template

Paste this into your session once the fit is done, filling in the specifics:

```markdown
| Node | Variable | Source | Role |
|---|---|---|---|
| T₁  | <media_a>_adstock | dbt.<table>.<col> | media |
| T₂  | <media_b>_adstock | dbt.<table>.<col> | media |
| C   | <control_var>     | dbt.<table>.<col> | control (macro / seasonality) |
| Y   | <kpi>             | dbt.<table>.<col> | KPI |
| B   | baseline          | median KPI during bottom-decile combined-adstock weeks | baseline |

Edges: T₁→Y, T₂→Y, C→Y, B→Y
Flags:
 - <suspected confounder 1, e.g. unobserved n_ga_users driving both T and Y>
 - <suspected confounder 2, e.g. co-launched campaign in weeks W1–W4>
 - <any missing control, e.g. no seasonality term yet>
```

### A first-pass BLOCK is a good sign

The reviewer **should** be strict on your initial DAG. The guidebook simulation showed a 9.8× under-attribution error when structural review is skipped (see [Research / MMM § Why a single-layer model breaks](../research/mmm/index.md#why-a-single-layer-model-breaks-on-layered-routes)). A clean PASS on the first try usually means the flags block was lazy.

Flag confounders honestly. If `n_users` plausibly drives both your media and your KPI, list it as a suspected back-door — the reviewer will then prescribe the front-door fix (e.g. add `n_users` as an intermediate node).

### How to write the "Flags" block well

- **Cite the mechanism, not just the correlation.** "`claims_adstock` and `topups_adstock` both move with `n_ga_users` (user growth → more of both events)" is useful. "These are correlated" is not.
- **Note what's missing.** "No macro control for ETH price" is a fail condition under reviewer rule 7. Call it out yourself rather than hoping the reviewer misses it.
- **Don't over-flag.** If the correlation is 0.2 and there's no plausible confounder, don't invent one.

---

## 6. Read the fitted numbers correctly

After the fit you'll see something like:

| Media | r | β | MAE (scaled) | Interpretation |
|---|---:|---:|---:|---|
| Claims | 0.118 | 4,953 | 0.31 | Strongly diminishing returns — near saturation |
| Topups | 0.458 | 2,623 | 0.42 | Moderate elasticity — headroom remains |
| Bridge incentives | 0.72 | 1,840 | 0.18 | Near-linear in observed range — may saturate at higher spend |

### Reading `r` (the diminishing-returns exponent)

| Range | Interpretation | Implication |
|---|---|---|
| `r ≈ 0` | Saturated; extra spend buys ~nothing | Redirect budget elsewhere |
| `r ∈ (0.2, 0.4)` | Strongly concave, clear diminishing returns | Current spend is past the knee; modest reductions are safe |
| `r ∈ (0.4, 0.7)` | Healthy concave | Budget can still pay; headroom in observed range |
| `r ∈ (0.7, 1.0)` | Near-linear in observed range | Either un-saturated or the sample doesn't reach saturation yet |
| `r ≥ 1.0` | **Model is wrong** | Super-linear response to media isn't real — usually missing confounder or reverse causation. Kick back to the reviewer |

### Reading `β` (the scale coefficient)

- **β is scale-dependent.** A larger β for topups than claims doesn't mean topups are "stronger" — it depends on the units of the adstock axis.
- **Compare contributions, not coefficients.** Evaluate `β · adstock^r` at observed spend levels and sum per media — that's the comparable quantity.
- **Compare across *sectors* is invalid.** A β fitted on USD-scale volume is not the same β fitted on tx-count-scale volume. Coefficients do not port.

### Hill vs concave — which to trust

The persona fits both and picks the one with lower holdout MAE. In practice on short (<100 week) histories:

- Concave wins almost always. Hill's extra flexibility just memorizes noise.
- Hill wins when there's a genuine "awareness threshold" visible in the data — the KPI stays flat at low spend, then accelerates. You'll see this in the scatter chart, not in the MAE alone.
- If MAE is within 5% between the two, **prefer concave**. Occam.

---

## 7. Responding to a BLOCK verdict

The reviewer returns a verdict table with prescribed fixes. Apply them in this priority order:

1. **Front-door variable (priority 1).** If an on-chain intermediate exists in your data, add it as a node and re-run the analysis. Candidates on Gnosis:
      - **Unique-wallet count** between an incentive and a KPI
      - **Brand-query proxy** — block-explorer page views, governance-forum mentions (if off-chain data available)
      - **Bridge-inflow lag** between an ecosystem campaign and an on-chain KPI
2. **Segmentation (priority 2).** Split by protocol / audience / chain if within-segment correlation drops.
3. **Macro / seasonality control (priority 3).** Add `sin(2π · weekOfYear/52)` and `cos(...)` Fourier terms, plus an ETH-price control. Fixes reviewer rule 7 cheaply.
4. **Intervention request (priority 4).** Ask ops to schedule a future dark period. Real but slow; rarely viable for retrospective analysis.

### Iterating with the reviewer

The reviewer expects the DAG passed **verbatim** as a markdown table — don't rephrase. If it BLOCKs:

1. Read the `Evidence` column for each failed check
2. Apply the suggested fix in the `recommendation` column
3. Update the DAG markdown (new node, new edges, updated flags)
4. Call `get_agent_persona("mmm_causal_reviewer")` **again** — don't re-use the old verdict
5. Expect PASS or a refined BLOCK. Two iterations is normal; five means your data is genuinely confounded and MMM may not be recoverable.

**Do not try to "talk around" a BLOCK verdict.** The gate exists because structural review catches the 9.8× attribution errors. Fix the structure, re-submit.

---

## 8. Use `mmm_simulator` for forward-looking questions

After a PASS verdict, the simulator answers "what should we do next?". Invoke it as a separate turn with the full parameter handoff:

```text
get_agent_persona("mmm_simulator")

Fitted curves (from the MMM run I just completed):
- Claims:      β=4952.6, r=0.118, λ=0.5, current_spend=$1.8M/quarter
- Topups:      β=2623.3, r=0.458, λ=0.5, current_spend=$2.5M/quarter
- Bridge inc.: β=1840.0, r=0.720, λ=0.5, current_spend=$4.0M/quarter

Baseline KPI: $5,327/week
Total budget next quarter: $8.3M (unchanged)

Recommend optimal reallocation under the ±30% per-media cap.
```

### What the simulator returns

- **Marginal ROI bar chart** (sorted descending). Highest marginal ROI at current spend → where the next dollar should go.
- **Current vs proposed allocation** grouped bar.
- **Allocation pie** of the proposed share.
- **Predicted KPI delta** with credible-interval band (from the reviewer-passed bootstrap).

### Reading the ±30% cap output

The simulator *always* caps per-media shift at ±30% per period. So you'll see:

- `optimal_spend_raw` — what the math wants, unconstrained
- `optimal_spend_capped` — what the simulator actually recommends

If `raw ≫ capped`, the math wants a bigger shift than ops can execute safely. Stage the change over multiple periods: "shift 30% this quarter, re-fit, shift another 30% next quarter if the response curve holds".

The ±30% cap and the "never zero out a media on a single window" rule (simulator rule 8) are operational-feasibility constraints, not statistical limits. They mirror the Guidebook p.80 footnote.

---

## 9. When to skip MMM entirely

Four conditions where MMM is the wrong tool and you should tell the dispatcher so up front:

| Condition | Why | Use instead |
|---|---|---|
| **Single campaign** (one incentive program, one flight) | No variation to fit a response curve against | Simple A/B or difference-in-differences |
| **Structural break** in the data window (hard-fork, bridge exploit, tokenomics rework) | MMM will attribute the break to whatever media happened to be running that week | Either truncate the window or add an explicit step-dummy variable |
| **Single-outlier-dominated KPI** (one-off airdrop spike) | Fit will treat the outlier as the rule | Investigate the outlier first; winsorize or flag before fitting |
| **<30 weekly rows** | Coefficient estimates are noise | A/B comparison or descriptive trend analysis |

If any applies, tell the dispatcher directly: *"use A/B attribution instead of MMM for this, window contains the Shapella fork"*. The dispatcher routes to `analytics_reporter` in a standard flow.

---

## 10. Three end-to-end copy-pasteable prompts

### Example A — Full diagnostic run on a ready sector

```text
Run MMM on weekly bridge inflows to Gnosis Chain.
KPI: dbt.int_bridges_flows_daily — sum volume_usd where direction='inbound', bucket to week
Media A: weekly incentive-program spend per bridge (list any you're aware of as
         rows in the time series; else use bridge-side subsidies as a proxy)
Media B: destination-chain incentive flags (weekly 0/1)
Control: weekly ETH price, sin/cos(2π·weekOfYear/52) for seasonality
Window: last 104 weeks
Pass final DAG to mmm_causal_reviewer before generating any report.
```

Expected flow: dispatcher manifest → `mmm_analyst` runs the full SOP → you synthesize a DAG → likely BLOCK on missing front-door → add `unique_bridge_senders` intermediate → PASS → 5 required charts + report.

### Example B — Prescription-only (assumes a fit exists)

```text
Using the fitted parameters from my last bridge-inflow MMM run, what's the
optimal reallocation of the $8.3M quarterly incentive budget?

Fitted curves:
- Omnibridge XDAI subsidy: β=X, r=Y, λ=Z, current_spend=$W
- Hashi bridge incentive:  β=X, r=Y, λ=Z, current_spend=$W
- Destination-chain LM:    β=X, r=Y, λ=Z, current_spend=$W

Baseline weekly KPI: $N
Hold total constant. Respect the ±30% cap.
```

Expected flow: dispatcher routes straight to `mmm_simulator` (skips re-fitting), returns reallocation + marginal-ROI charts.

### Example C — Explicit specialist invocation

For when you already know exactly what you want and don't need the dispatcher:

```text
Use mmm_analyst directly on:
- KPI: dbt.stg_consensus__withdrawals, aggregated weekly as total amount
- Media: validator reward rate (weekly median APR), weekly bridge inflows
- Control: weekly ETH price, hard-fork flag (Shapella = 2023-08-01)
- Window: from 2023-09-01 to current

Skip the dispatcher. When fit is done, I'll write the DAG.
```

---

## 11. Common failure modes and fixes

| Symptom | Cause | Fix |
|---|---|---|
| Report appears without reviewer verdict | LLM skipped the DAG handoff | Interrupt: *"pass the DAG to `mmm_causal_reviewer` before generating the report"* |
| Single manifest with fabricated PASS | LLM self-reviewed its own DAG | Explicitly invoke `get_agent_persona("mmm_causal_reviewer")` as a **separate turn** |
| `r > 1` on fitted curves | Model is structurally wrong (missing confounder, reverse causation) | Re-examine DAG; usually a missing front-door or a pay-for-performance leak |
| Very wide credible intervals | Data window too short, or too much unexplained variance | Accept "directional only" label; don't quote single ROI numbers; investigate outliers |
| Simulator suggests zeroing a media | Shouldn't happen given simulator rule 8 | File as a prompt-drift bug; in the meantime manually floor at 70% of current spend |
| Reviewer PASSes a DAG missing macro/seasonality | Reviewer rule 7 drifted | Re-submit asking for review citing rule 7 explicitly |
| Contribution sums exceed KPI | Decomposition bug, usually double-counting | Verify no two media are in inclusion relationship |
| Hill beats concave by <5% MAE | Hill overfit to noise | Prefer concave; Hill's extra params aren't earning their keep |
| Adstock λ fitted at exactly 0.5 | Default was never fit | Verify the fit step actually searched over λ; re-run if not |

---

## 12. Diagnose a past run

Every MMM report carries its run manifest and the exact SQL embedded in each chart card. To audit a prior analysis:

1. `list_reports()` — find the MMM report by title or date
2. `open_report(report_id)` — opens the HTML locally or returns a file:// link
3. In the rendered report, click the `</>` icon on each chart to see the full CTE chain that produced it
4. Copy the SQL into a new `execute_query` call to reproduce the number
5. Compare fitted `r`, `β`, `λ` to your prior from the same sector

**Drifting coefficients week-over-week** usually mean the upstream dbt pipeline changed (column rename, grain change, new filter), **not** that the underlying effect changed. The first thing to diff is the chart SQL between the old and new run.

This is the main reason the MMM SQL is all in-persona and fully reproducible from the chart alone: every number in a published MMM report should be re-derivable without the original session context.

---

## 13. What NOT to do

- **Don't ask for "an MMM report" as a one-shot.** The flow is multi-turn by design (fit → DAG → review → report). If you try to compress it, the reviewer gate skips.
- **Don't copy-paste MMM coefficients across sectors.** Each sector has its own baseline, adstock λ, and curve shape. `β` and `r` do not transfer; even `λ` is sector-dependent.
- **Don't combine MMM with the storyteller workflow in the same session.** Both run gated pipelines and will compete for control of `generate_report`. Run MMM first, save the report, then start a fresh storyteller session that cites the saved report's numbers.
- **Don't expect MMM to tell you *why* an incentive worked.** It tells you *how much* it worked. Attribution ≠ mechanism. For mechanism, run a follow-up qualitative investigation (user behavior cohorts, on-chain path analysis) using `growth_analyst` or `defi_analyst`.
- **Don't treat the 24-week Gnosis App smoke-test numbers as a reference baseline.** They're a demonstration of the pipeline, not a defensible ROI claim — the window is below the 60-row floor.

---

## FAQ

**Q: Why can't I just use Google Meridian?**
A: You can, eventually. It would give real posteriors instead of SQL bootstrap CIs — but it's a 1-month integration (async job infra, TF + TFP dependencies, GPU costs, model-versioning). Not worth it until you have ≥2 sectors with ≥2 years of data that justify the overhead. See the ["how hard to use Meridian"](../research/mmm/index.md#further-reading) discussion for the full scoping.

**Q: Why do I need the reviewer if I already trust the data?**
A: The reviewer isn't about data trust; it's about *structural* trust. The simulation in Guidebook Ch.3 showed that a single undetected back-door can under-attribute a driver by ~9.8× **even on perfectly clean data**. The reviewer catches structure bugs that no amount of data validation can find.

**Q: Can I re-run an old DAG against new data?**
A: Yes — and it's a good practice. Pull the DAG markdown from the old report's chart SQL, re-verify the variables still exist in the catalog, re-submit to `mmm_causal_reviewer`, then re-run the fit. If the new fit's coefficients are very different, either the effect changed or the data pipeline changed. Diff the chart SQL first.

**Q: How do I compare two sectors?**
A: Not by coefficients. Run MMM twice, produce two reports, and compare **contributions at comparable spend levels** and **shapes of response curves**. Normalize by picking a common KPI unit (e.g. USD) if possible.

**Q: The reviewer keeps BLOCKing. Is my DAG just bad?**
A: Usually your **data** is confounded, not your DAG. If you've tried the front-door + segmentation + macro-control fixes and still BLOCK, MMM may not be recoverable on this data. The reviewer's honest answer is to wait for an intervention (dark period or staggered flights) that creates identifiability.

**Q: Can I fit MMM on daily data instead of weekly?**
A: Yes if you have ≥365 daily rows and your media variables are measured daily. Daily multiplies the parameter pressure — 13 params on 100 weekly rows ≈ 8 df per param; same 13 params on 100 daily rows ≈ 0.7 df per param. The floor for daily is ~730 rows (two years of daily). On Gnosis, `execution.transactions` qualifies; most other tables don't.

**Q: What if my media variable is binary (campaign on / off)?**
A: The SOP still works — adstock on a 0/1 series produces a smooth decay, and the concave fit just becomes a step with a carry-over tail. But the Hill fit degenerates; force concave in that case. State explicitly in the DAG flags block: *"media X is binary; forcing concave, Hill skipped."*

---

## See also

- [MCP / Marketing Mix Modeling](mmm.md) — the tooling reference with full SQL toolkit
- [MCP / Cerebro Dispatcher](dispatcher.md) — the top-level router that classifies MMM intent
- [MCP / Agent Fleet](agents.md) — where the three MMM personas sit in the broader fleet
- [Research / Marketing Mix Modeling](../research/mmm/index.md) — the method theory and Hakuhodo guidebook chapters
