# Multi-Touch Attribution — Foundations

!!! note "Scope of this section"
    This is a **domain reference** for MTA on Gnosis sectors: what MTA is,
    how it differs from [Marketing Mix Modeling](../mmm/index.md), the
    journey schema the dbt pipeline materialises, the four credit
    functions, the volume gates that decide which methods are licensed,
    and the GP role grain. The companion implementation reference is
    [Measurement Stack (MTA + MMM)](../../data-pipeline/transformation/measurement-stack.md);
    the agent-facing reference is
    [Measurement Flow (MTA + MMM + Unified)](../../mcp/measurement-flow.md).

## What is Multi-Touch Attribution

**Multi-Touch Attribution (MTA)** is the user-journey, observational half
of the Cerebro measurement stack. For each conversion (a topup, a swap, a
GP payment), it builds the ordered list of prior touchpoints the same
identified user produced, then divides fractional credit across those
touchpoints by a chosen rule. The output looks like "out of 100 GA→GP
topups in the last 180 days, `chain.swap_filled` events received 32 units
of last-touch credit and 14 units of first-touch credit".

MTA is **observational**. It describes correlations along observed paths.
It does **not** estimate causal lift. The single fact that a user signed a
swap before topping up does not mean the swap caused the topup — both can
be effects of an unobserved third cause (a marketing email, a Telegram
post, a partner integration going live). For causal claims, MTA must be
paired with [MMM](../mmm/index.md) or a quasi-experimental design — see
the [Unified workflow](../../mcp/measurement-flow.md#unified-mmm-mta-workflow).

## When to use it

- "Which app actions tend to precede a Gnosis Pay topup?"
- "What's the typical path from `chain.token_offer_claim` to `chain.swap_filled`?"
- "How do first-touch and last-touch attribution compare for marketplace conversions?"
- "Where in the funnel are users dropping off?"

## When NOT to use it

- "Did the LM rewards program **cause** TVL to grow?" — that's MMM.
- Conversion volume <30 in the window — descriptive funnel only, no
  attribution credit (see volume gates below).
- No usable user identifier on either side — downgrade to aggregate
  funnel diagnostics.
- A clean A/B holdout exists — use the experiment readout directly.
  Experiment evidence beats observational MTA.

## How MTA differs from MMM

| | MTA | MMM |
|---|---|---|
| Unit of analysis | Per user, per conversion | Aggregate weekly time series |
| Inputs | Touchpoint stream + conversion stream + identity bridge | KPI / media / control wide spine |
| Output | Per-touchpoint credit (conversion-equivalent units) | Per-media β, response curve, contribution decomposition |
| Causal? | No — observational only | Yes, conditional on the DAG passing causal review |
| Bias profile | Conditional-on-conversion bias; touchpoint coverage haircuts | Aggregation bias; collinearity; baseline drift |
| Privacy posture | Pseudonyms over identified users | No user identity required at all |

The two are complementary. MMM tells you the lift; MTA describes how that
lift is distributed across observed user paths. The
[Unified workflow](../../mcp/measurement-flow.md#unified-mmm-mta-workflow)
calibrates MTA shares against an MMM PASS so the per-touchpoint credits
sum back to the MMM-estimated lift.

## The touch / conversion / journey schema

The dbt pipeline materialises three layers per sector
(`gnosis_app` and `gpay`):

| Layer | Table | Grain |
|---|---|---|
| Touchpoint | `int_execution_<sector>_user_events_unified` | One row per identified user × event |
| Conversion | `int_execution_<sector>_conversions` | One row per identified user × conversion |
| Journey | `fct_execution_<sector>_journeys_{7,30,60}d` | One row per (conversion, prior-Nd touchpoint). 30d is the default; 7d / 60d are sensitivity-sweep variants. Both sectors ship all three windows. The GP 60d mart is the heaviest (3-role identity fan-out × 60-day lookback × 2-year history) and microbatches at `batch_months: 1` to stay under the 10 GiB cluster cap. |

The journey spine applies two leakage guards at materialisation time:

1. **Temporal** — `event_ts < conversion_ts AND event_ts >= conversion_ts - 30 days`.
   A touch that happens after its own conversion is excluded.
2. **Self-exclusion** — the conversion's own canonical event kind is
   filtered out via the `conversion_kind_to_event_kind` macro. A `topup`
   conversion can never be tracked by its own `chain.topup` event.

All identified users are referenced by `user_pseudonym` (a keyed
`sipHash64` of the lowercased address), never by raw address — see
[Privacy & Pseudonyms](../../data-pipeline/transformation/privacy-pseudonyms.md).

## The four credit functions

For a conversion with `n` prior touchpoints
$t_1, t_2, \dots, t_n$ at lag-days $d_1, d_2, \dots, d_n$:

| Rule | Per-touch credit | Notes |
|---|---|---|
| First-touch | $1$ on $t_1$, else $0$ | Ties on $t_1$ split equally |
| Last-touch | $1$ on $t_n$, else $0$ | Ties on $t_n$ split equally |
| Linear | $1/n$ each | Distributes uniformly |
| Time-decay (HL=7d) | $\dfrac{e^{-d_i/7}}{\sum_j e^{-d_j/7}}$ | Half-life 7 days; recent touches weighted more |

By construction, each rule sums to **1.0** per conversion, so a row in
`fct_execution_<sector>_attribution_30d` reading `linear = 32.4` for
`event_kind = chain.swap_filled` means "swap_filled events accumulated
32.4 conversions' worth of linear credit in the 180-day window".

Markov removal-effect and sampled Shapley-proxy methods are licensed at
the ≥500-conversion volume tier and run in the persona, not the dbt
mart.

## Volume gates (hard)

| Conversions in window | Allowed |
|---:|---|
| <30 | Descriptive path / funnel only. **No credit assignment.** |
| 30–499 | Rule-based (first / last / linear / time-decay) + funnel. No Markov, no Shapley. |
| ≥500 | All methods including Markov removal effect and sampled Shapley proxy. |

Default lookback is 30 days. Sweep 7 / 14 / 30 / 60 when volume permits.

## The GP role grain

Gnosis Pay introduces a wrinkle MTA on a pure-EOA flow doesn't have:
the same human shows up under three different addresses depending on the
GP frontend code path. The GP measurement stack fans out every
conversion and every touchpoint by `identity_role`:

| Role | Address it carries | Research question it answers |
|---|---|---|
| `safe_self` | The Safe smart-account address | Treasury grain — "how does this Safe behave?" |
| `initial_owner` | The EOA that signed the Safe setup | Owner grain — "how does this human behave?" |
| `delegate` | A spender delegate EOA | Operator grain — usually a backend card-flow key |

Picking the right role at query time is **load-bearing** — different
roles answer different research questions and are not interchangeable.
The GP attribution mart carries `identity_role` as a column so a single
`WHERE` clause selects the grain:

```sql
-- Owner-grain attribution for GP payments
SELECT *
FROM api_execution_gpay_attribution_30d
WHERE conversion_kind = 'gpay_payment'
  AND identity_role   = 'initial_owner'
ORDER BY linear DESC;
```

A 2-owner Safe with one delegate produces 4 rows in the bridge
(2 `initial_owner` + 1 `delegate` + 1 `safe_self`). A payment from that
Safe yields 4 rows in `int_execution_gpay_user_events_unified`. This is
intentional: the same payment is one event from the Safe's perspective,
two events from the owners' perspectives, and one event from the
delegate's perspective.

See [Identity Grain in the MCP repo](https://github.com/gnosischain/cerebro-mcp/blob/main/docs/measurement/identity_grain.md)
for the canonical framing of why the wrong grain is the most common
silent failure in on-chain attribution.

## Unified MMM + MTA

When an analytics request asks "attribute MMM-measured lift across
observed user journeys" or "calibrate our MTA shares against the MMM
lift estimate", the dispatcher routes through the
[Unified MMM + MTA workflow](../../mcp/measurement-flow.md#unified-mmm-mta-workflow).
The unified causal reviewer runs eight checks (MMM-gate, conversion
consistency, incrementality bound, coverage, leakage, identity grain,
selection bias, method stability) and applies the calibration:

$$
\text{calibrated\_credit}_i = \text{raw\_mta\_credit}_i \times \frac{\text{MMM\_lift}}{\sum_j \text{raw\_credit}_j}
$$

The unified report **must** disclose the `unexplained / untracked`
residual — the portion of MMM-estimated lift no observed touchpoint can
claim. Omitting it overstates the explanatory power of the touchpoint set.

## Common failure modes

- **Hardcoded model names.** The persona's "context examples" are
  illustrative; live runs must rediscover via `search_models` /
  `discover_models` and confirm columns with `describe_table`.
- **Post-conversion leakage.** Forgetting `touch_ts < conversion_ts`
  makes downstream events look causal. The dbt journey spine enforces
  this guard at materialisation time, so leakage in MTA reports comes
  from custom queries that skip the mart.
- **Identity-grain mismatch.** Wallet-grain attribution on a Safe-heavy
  flow over-credits the relayer EOA. Owner-grain on an EOA-only flow
  over-credits gas activity. State and justify the grain.
- **Selection bias.** A `viewed-topup-screen` touchpoint dominates any
  attribution model — anyone who eventually topped up almost certainly
  viewed the screen first. Report a counterfactual or caveat.
- **Method instability.** When first-touch and Markov disagree wildly,
  the result is directional at best. Downgrade confidence.

## Cross-references

- [Measurement Stack (MTA + MMM)](../../data-pipeline/transformation/measurement-stack.md) — dbt-level implementation reference.
- [Measurement Flow (MTA + MMM + Unified)](../../mcp/measurement-flow.md) — agent-facing dispatcher routing and persona reference.
- [Privacy & Pseudonyms](../../data-pipeline/transformation/privacy-pseudonyms.md) — why every MTA model keys on `user_pseudonym`.
- [Marketing Mix Modeling](../mmm/index.md) — the aggregate / causal half of the stack.
