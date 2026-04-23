# Marketing Mix Modeling — Foundations

!!! note "Scope of this section"
    This is a **domain reference**: what MMM is, where it came from, the statistical machinery under the hood, and the structural considerations that make or break a real model. The companion page [MCP / Marketing Mix Modeling](../../mcp/mmm.md) is the **tooling reference** for running MMM against Gnosis Chain data through Cerebro.

    Source: *Marketing Mix Modeling Guidebook* (Hakuhodo DY media partners Inc., 2023). Chapter and page references in this document point at that guidebook. The crypto / Gnosis adaptations are Cerebro-specific.

## What is Marketing Mix Modeling

**Marketing Mix Modeling (MMM)** is a statistical method that estimates the contribution of media and marketing activities to a business KPI using aggregate time-series data. It answers three questions a CMO can act on:

1. **Diagnose** — What, how much, and how are the media and marketing activities contributing to the business?
2. **Optimise** — Are the budget allocations reasonable, and what would a better one look like?
3. **Simulate** — What business outcome should we expect under a new plan?

MMM does **not** require user-level tracking. It works on aggregate time series — weekly or daily media spend / impressions, KPI values, and control variables — which is why it has become the default privacy-safe attribution method as third-party cookies are deprecated and walled gardens expand.

### Why the industry is returning to MMM

Three forces push measurement back toward MMM:

- **Cookie-less era.** Apple ITP (2017+) and Google's deprecation of 3rd-party cookies (late 2024) break the browser-side identity fabric Multi-Touch Attribution (MTA) relied on. iPhone market share in Japan is 66% vs. 28% globally — cookie restrictions already bite hard there.
- **Walled gardens.** Closed platforms (large social networks, streaming services) don't return impression-level data to advertisers.
- **Low e-commerce rates in some categories.** Consumer goods in Japan still have <10% e-commerce penetration for food, beverages, automobiles — the user journey is mostly offline and uninstrumented.

MMM pre-dates all of this. The re-adoption isn't novelty; it's a fallback to a method that was always valid and whose assumptions (aggregate data, time-series, domain priors) are the assumptions you're forced back to.

### Crypto adaptation — the mapping this docs site uses

| MMM concept | Gnosis-sector analog |
|---|---|
| Media spend / impressions | Token emissions, LM rewards, validator APR, bridge incentives |
| Business KPI | TVL, DEX volume, DAU, tx count, bridge flows |
| Control variables | Gas price, ETH / stablecoin macro moves, holidays, protocol launches |
| Confounders | Simultaneously-launched incentive programs (common in DeFi) |

The mathematical machinery (response curves, adstock, Bayesian estimation, causal DAGs) transfers cleanly. What differs is the domain priors and the specific failure modes — see §[Adapting MMM to On-Chain Incentives](#adapting-mmm-to-on-chain-incentives).

---

## The MMM process

```
┌────────────┐   ┌────────────┐   ┌──────────────┐   ┌───────────┐   ┌────────────┐   ┌────────────┐
│  Data      │ → │  Data      │ → │  Model       │ → │ Parameter │ → │ Validation │ → │ Utilization│
│  Selection │   │  Cleansing │   │  Structure   │   │ Estimation│   │            │   │            │
└────────────┘   └────────────┘   └──────────────┘   └───────────┘   └────────────┘   └────────────┘
                         ↑                ↑                 ↑                ↑
                         └────────────────┴─────────────────┴────────────────┘
                          Iterate: adjust data / structure / priors based on validation
```

Some steps look like ordinary regression modelling; three are MMM-specific and worth dwelling on — input-data selection, response-curve transformation, and adstock.

---

## 1. Data selection

### Input data categories

| Type | Examples | Source |
|---|---|---|
| **Dependent variable (KPI)** | Revenue, conversions, active users, installs | Internal |
| **Media variables** | Spend / GRP / impressions / clicks per channel (TV, radio, print, OOH, YouTube, Google Search, Meta, TikTok, …) | Media-agency DBs, platform APIs |
| **Product metrics** | Pricing, updates, user ratings, survey data | Internal, app stores |
| **Promotions** | Discount %, promo type, inventory, event flags | Internal, retail data |
| **Competitor signals** | Promotions, launches, ad activity, app rankings | Web scraping, public data |
| **Popularity** | Hashtag volume, Google Trends, app rankings | Public data |
| **Macro** | GDP, Covid flags, weather, holidays, seasonality | Public data |

Models are normally **weekly, two-plus years**. Daily is possible for high-volume digital advertisers but multiplies the parameter pressure.

### KPI selection trade-off

Pick the KPI too shallow (e.g. "reach") and you lose causal relevance to the business. Pick it too deep (e.g. LTV, lifetime revenue) and too many unobservable factors sit between media and outcome — sales-workforce skill, call-center performance, AI-chatbot quality, product quality — none of which are cleanly quantifiable. A common compromise is an intermediate KPI like *brand search volume* or *website registrations*.

### Media variable: spend, impressions, or clicks?

| Option | When | Notes |
|---|---|---|
| **Spend** | Rarely recommended for modern media mixes | Spend doesn't describe exposure — CPM varies widely across channels and flights |
| **Impressions** | **Default choice** | Describes exposure regardless of path (view-through or click-through) |
| **Reach × frequency** | Ideal but often infeasible | Cross-campaign reach requires individual-level deduplication data |
| **Clicks** | Limited cases (e.g. branded search) | Ignores view contribution |
| **Views** | Not recommended | "View" definitions differ across platforms |

### Granularity for actionable insight

Rolling up to "TV" and "Digital total" is too coarse — the model user can't find improvement points. Rolling all the way down to individual creatives is usually too sparse. **Placement level** (Bumper / Masthead / Instream-skippable) or **bidding-strategy level** (Manual CPC / Target CPA / App Campaign) is typically right.

### Rule-of-thumb for data volume

Degrees of freedom per parameter is the fundamental constraint. With 20 parameters and 100 weeks:

$$
\text{df per parameter} = \frac{100 - 20}{20} = 4
$$

Four samples per parameter is **not enough** for reliable estimation. Flight-time skewness (Christmas concentration, end-of-month sales), very-small-spend channels, and narrow-target digital segments all shrink the effective sample further. Fixes: reduce the number of parameters, collect more weeks, or increase granularity from national to geo / sub-brand level.

---

## 2. Data cleansing

### Missing values

Every missing value breaks the downstream statistical package. Options, in order of sophistication:

| Method | How | Trade-off |
|---|---|---|
| Average imputation | Insert mean or median | Easy, but shrinks variance of independent variables |
| Normal regression imputation | Regress the missing variable on the others | Better, but still underestimates variance |
| **Stochastic regression imputation** | Add a random-error term to the regression | Preserves variance; recommended for MMM |
| **Multiple imputation** | Create N imputed datasets, fit N models, combine | Most robust; expensive |

### Outliers

Outliers are **contextual**, not purely statistical. Before deleting a point, check:

- Data-entry or ETL error → fix
- Scheduled event (holiday, big campaign, product launch) → add an event / dummy variable
- Sudden event (pandemic, natural disaster, competitor launch) → add a variable

The default response is to *add a variable* that explains the outlier, not to drop the row.

### Data-form changes

- **Categorical → binary.** Promotion type `{none, 10% discount, 5% discount}` → two dummy columns. If the categorical is *ordinal* (popularity rank), keep it numeric.
- **Character → numeric/binary.** Promotion meta `"10% discount, grocery"` → `discount_pct=10` + `promo_grocery=1` + `promo_fashion=0`.

### Multicollinearity

The single most common failure mode in MMM. When two media variables move together (e.g. TV and Display ads ran in identical weekly flights), the regression cannot separate their effects — and will often assign a **negative** coefficient to one of them, which is nonsense for paid media.

Detection: **Variance Inflation Factor (VIF)**, computed by regressing each independent variable on the others:

$$
\text{VIF}_i = \frac{1}{1 - R_i^2}
$$

Rule of thumb: VIF > 10 (equivalent to multiple correlation coefficient |R| > ~0.95) means the variable cannot be cleanly separated from the others. Fixes:

| Fix | When | Cost |
|---|---|---|
| **Merge** | Two tightly-coupled channels can be summarised as one "total" variable | Loses granularity, but no data loss |
| **Remove** | One of the pair can be dropped | Misattributes effects to the remaining variable |
| **Divide** (segment) | Geo / audience / brand split can break the correlation within segment | Best option when data exists; often infeasible |

See §[Chapter 3 — Model Structure Considerations](#chapter-3-structural-considerations) for the deeper fix: intentional intervention in the media plan to create identifiability.

### Scaling

Variables in drastically different units (TV spend in ¥M, search clicks in K) aren't comparable post-estimation and can make optimisers misbehave. Options:

| Method | Formula | When |
|---|---|---|
| Min-max | $x' = (x - \min) / (\max - \min)$ | Clear natural interval |
| **Mean** | $x' = x / \text{mean}(x)$ | **MMM default** — keeps values positive; sales and impressions are nonnegative |
| Standardisation | $x' = (x - \text{mean}) / \text{std}$ | Other ML applications |

Mean scaling preserves nonnegativity, which matters for multiplicative models and response curves.

---

## 3. Model structure

The step where MMM departs most from ordinary regression. A full MMM looks like:

$$
\text{Revenue}_t = b + \sum_m \beta_m \cdot \text{Hill}\left(\text{Adstock}\bigl(x_{t,m}, \dots, x_{t-l,m}\bigr),\; K_m,\; S_m\right) + \text{trend}_t + \text{seas}_t + \sum_c \gamma_c\, d_{t,c} + \varepsilon_t
$$

Four pieces:

- **(A)** Response curve — `Hill(·)` — models saturation in the media-to-KPI relationship
- **(B)** Adstock — carries past media exposure forward with decay
- **(C)** Trend + seasonality — the baseline that exists without marketing
- Control variables — promotions, price, macro

### Additive vs. multiplicative

Two structural choices for how media effects combine:

**Additive** (effects are separable):

$$
\text{Revenue} = b + w_{TV}\,x_{TV} + w_{SEM}\,x_{SEM} + w_{\text{prom}}\,x_{\text{prom}} + \dots
$$

**Multiplicative** (effects are interacting — "synergy"):

$$
\text{Revenue} = b \cdot x_{TV}^{w_{TV}} \cdot x_{SEM}^{w_{SEM}} \cdot x_{\text{prom}}^{w_{\text{prom}}} \cdot \dots
$$

Taking logs converts multiplicative to additive-in-logs:

$$
\log \text{Revenue} = \log b + w_{TV} \log x_{TV} + \dots
$$

**Interpretation difference.** If TV doubles and SEM doubles:

- Additive: incremental contribution of TV is $2M \cdot w_{TV} - 1M \cdot w_{TV} = M \cdot w_{TV}$, cleanly attributable.
- Multiplicative: incremental contribution of TV is $(\text{other factors}) \cdot (2^{w_{TV}} - 1) \cdot 2^{w_{SEM}}$ — depends on SEM too.

Additive gives cleaner per-channel attribution. Multiplicative captures interactions. Neither is universally right.

### (A) Response curves — why linearity is wrong

Linear models falsely assume *infinite* revenue per additional dollar. Reality: media saturates — at some point another impression doesn't move the needle because reach and frequency have ceilings.

Two functional forms dominate MMM:

#### Concave (power) curve

$$
y = \beta \cdot x^r \quad (0 < r < 1)
$$

Models immediate impact that saturates gradually. Typical for performance-like signals (retargeting, search).

#### Hill (S-shape) curve

$$
\text{Hill}(x) = \frac{1}{1 + (x / K)^{-S}}
$$

Two parameters:

- **$K$** = half-saturation point (where the curve reaches 0.5)
- **$S$** = slope / steepness

The Hill curve models an initial *flat* region — the first few impressions don't move awareness — then an acceleration through a sweet spot, then saturation. Typical for awareness media (TV, video, OOH).

Both curves can be combined with a scaling coefficient $\beta_m$ that carries the media-specific incremental effect.

### Metrics on the curve

Two ROI metrics derive directly from the fitted curve:

- **ROI (ROAS)** — $\dfrac{\text{Incremental revenue}}{\text{Spend}}$ — the slope from the origin to a point on the curve
- **Marginal ROI** — the gradient of the tangent at the current spend point — "speed of revenue increase from the next dollar"

Marginal ROI is the right signal for incremental budget decisions; ROAS is what finance reports historically.

### (B) Adstock — time carry-over

Advertising effects linger. If YouTube runs today, the effect on tomorrow's search volume is nonzero and continues decaying for weeks.

**Geometric adstock** (simplest):

$$
\text{adstock}_{t,m} = x_{t,m} + \lambda_m \cdot \text{adstock}_{t-1, m}
$$

- High $\lambda$ (≈0.8) → long tail, rich media like TV / video
- Low $\lambda$ (≈0.2) → short tail, direct-response like search

**Weibull PDF adstock** — allows non-monotone decay shapes via a scale and shape parameter.

**Carry-over with delay (Google 2017)**:

$$
\text{adstock}_{t,m} = \frac{\sum_{l=0}^{L-1} w_m(l) \cdot x_{t-l, m}}{\sum_{l=0}^{L-1} w_m(l)}, \qquad w_m(l) = \alpha_m^{(l - \theta_m)^2}
$$

$\theta_m$ is a *lag* parameter — captures campaigns that target future sales (a campaign in early December aimed at the Christmas peak has $\theta > 0$).

### Transformation order

Two orders, same operators:

- **Response curve then adstock** — apply the nonlinear transform first, stock the transformed effects. Recommended when spend is concentrated on distinct pulses (on/off flighting).
- **Adstock then response curve** — stock raw spend, then apply the nonlinear transform. Recommended when single-period spend is small relative to cumulative spend.

### (C) Trend and seasonality

Trend and seasonality are baseline demand — the KPI level that would exist with zero marketing. Two approaches:

| Observed variable | Latent / functional form |
|---|---|
| Macro data (GDP, category distribution volume), holiday flags | Logistic trend $trend_t = C / (1 + e^{-k(t-m)})$, Fourier seasonality $seas_t = \sum_k \gamma_k \sin(2\pi k t / s) + \dots$ |

Bayesian Structural Time Series (BSTS) gives a more flexible latent model if observed baseline data is thin.

### Variant model structures

- **Geo-unit MMM.** When national history is short (e.g. 2 years = 104 weeks), but geo breakdowns exist (prefecture, DMA, zip). 208 DMAs × 104 weeks = 21,840 observations — enough to fit per-geo parameters for scale, trend, seasonality.
- **Brand / audience MMM.** Same idea along the business-segment axis. Combining geo × brand is possible if data supports it.

---

## 4. Parameter estimation

Three families:

| Method | Minimises | Output | When |
|---|---|---|---|
| **OLS** | $\|y - f(x, w)\|^2$ | Point estimate + confidence interval | Baseline; assumes normal residuals |
| **Regularisation** (Ridge / Lasso) | $\|y - f(x, w)\|^2 + \lambda \|w\|^2$ | Point estimate (via cross-validation) | When prediction accuracy is the goal, not inference |
| **Bayesian** (MCMC) | Posterior $p(w\mid x, y) \propto p(y \mid x, w) p(w)$ | Full posterior distribution + credible intervals | **Recommended for MMM** — integrates prior knowledge, gives uncertainty |

### Why Bayesian is the MMM default

Two practical advantages:

1. **Priors encode domain knowledge** — past experiment results, industry benchmarks, sensible bounds on adstock decay. This is critical when data is short.
2. **Credible intervals**, not just point estimates. MMM reports ROI *ranges*, which is the right unit for planning under uncertainty.

### Bayes' theorem for MMM

$$
p(w \mid x, y) = \frac{p(y \mid x, w) \cdot p(w)}{p(y \mid x)}
$$

- $p(w)$ — prior, encodes assumptions
- $p(y \mid x, w)$ — likelihood, encodes the model
- $p(y \mid x)$ — evidence (constant w.r.t. $w$; ignored during sampling)
- $p(w \mid x, y)$ — posterior, what we want

### MCMC — Markov Chain Monte Carlo

Direct posterior calculation is intractable. MCMC replaces integration with sampling:

1. Initialise from the prior
2. Compute likelihood at current sample
3. Propose a new sample (Metropolis–Hastings, Gibbs, or modern variants like NUTS)
4. Accept / reject based on likelihood change
5. Repeat for ~5000 steps per chain, 4+ chains

The resulting trajectory approximates the posterior. See §[Validation / MCMC convergence](#1-mcmc-convergence) for how to know if it worked.

---

## 5. Validation — the nine checkpoints

After parameter estimation, an MMM is evaluated on **nine** dimensions. Objective metrics catch mechanical problems; contextual checks catch domain nonsense.

### 1. MCMC convergence

The **Rhat** statistic (Gelman–Rubin) compares within-chain and between-chain variance:

$$
\hat{R} = \sqrt{\frac{\hat V}{W}}, \qquad \hat V = \frac{n-1}{n} W + \frac{1}{n} B
$$

- $W$ = average of within-chain variance
- $B$ = between-chain variance of the chain means

Rule of thumb: **Rhat < 1.1** means the chains have converged. Rhat > 1.1 means discard early burn-in samples, increase chain length, or investigate structural heterogeneity (e.g. region-dependent parameters).

### 2. Prediction fitting

In-sample and out-of-sample prediction on the KPI. Three metrics:

- **$R^2 > 0.85$** — good explanation of variance
- **MAPE < 10%** — average percentage error tolerable for operational use
- **Durbin–Watson ∈ [1.5, 2.5]** — residuals not autocorrelated (DW outside that band usually means a missing variable)

Hold-out should be chosen with business sense, not a fixed 7:3 or 8:2 split. Two years of weekly data validated on one quarter is fine if the business is stationary.

### 3. Prior vs. posterior distributions

If the posterior is extremely sensitive to the prior, the data isn't informing the model much — results depend on assumptions. If means are stable but shape differs, the point estimates are reliable but uncertainty differs. Both need documented rationale.

### 4. Response curves — shape plausibility

Visual inspection of fitted curves:

- Does TV look S-shaped? (Should)
- Does retargeting look concave with fast saturation? (Should)
- Are the gradients comparable in magnitude across media? (Paid search usually has the highest marginal ROI)

### 5. Adstock decay — plausibility

Fitted λ should match format priors:

- Video / TV — slow decay (λ ≈ 0.6–0.8)
- Search / text ads — fast decay (λ ≈ 0.2–0.4)

If TV decays *faster* than Search, the model is structurally wrong.

### 6. ROAS (ROI) estimation

For each media $m$:

$$
\text{ROAS}_m = \frac{\sum_{t_0 \le t \le t_1 + L - 1} \hat Y_t^m(x) - \hat Y_t^m(\tilde x)}{\sum_{t_0 \le t \le t_1} x_{t,m}}
$$

where $\tilde x$ sets the media's spend to zero in the evaluation window — the numerator is the counterfactual difference. Report **both the mean and the credible-interval width**:

- Wide intervals → lack of data or campaign-execution variance; soften conclusions.
- Outlier mean ROAS → investigate. Compare to alternative model specs.

### 7. Spend vs. effectiveness share

For each media, compare **% of total spend** to **% of modeled incremental KPI**. Large gaps (e.g. media $H$ is 25% of spend but 5% of effect) are candidates for budget reallocation — but only after ruling out model error.

### 8. Time-series breakdown

Stacked-area decomposition of KPI into baseline + each media's contribution over time. Visual sanity check: do spikes align with campaigns? Do holiday effects land in baseline (where they belong) or in the wrong channel?

### 9. Multiple-model comparison

Fit several candidate models (different priors, different response-curve shapes, different control variables), compare on all of the above, and pick the one whose contextual checks make most sense. Objective metrics alone are never enough.

---

## 6. Model utilisation

An MMM typically serves three organisational layers, each with different time horizons and decision rights.

### Strategic — Managing Director / business-division head

- Horizon: quarter / year
- Decision: does the current financial plan match expected outcomes, and where to move capital across the portfolio?
- MMM use: predict KPI gap, adjust macro-level budgets between countries / product lines

### Tactical — Marketing Director

- Horizon: month / quarter
- Decision: ROI by country, brand, or target audience — where to prioritise?
- MMM use: cross-segment ROI comparison, prioritisation of markets

### Operational — Marketing Operations / media planning

- Horizon: week / month
- Decision: how to reallocate the next budget across channels?
- MMM use: optimiser output — take fitted response curves, apply budget constraint, get optimal per-channel spend

### Why budget shifts are bounded

Typical optimisers constrain per-channel change to ±30% period-over-period. Two reasons:

- Operational feasibility — media plans have committed flights, supply-contract minimums, creative-production lead times
- Model confidence — extrapolating far outside the observed spend range is unreliable

---

## Chapter 3: Structural considerations

The hardest step in MMM is *creating the right model structure*. The guidebook dedicates its longest chapter to this because an incorrectly-structured model can produce confident, pretty, and wrong ROI numbers — and those numbers will drive real budget decisions.

### Three checkpoints for structural appropriateness

1. **Chronological** — causality is always forward in time. An event that is measured *later* cannot be the cause of something measured *earlier*.
2. **Logical non-inclusion** — two variables on the explanatory side must not contain one another.
3. **Identifiability** — the effect of interest must be recoverable from the data, given observed and unobserved variables.

### Check 1 — Chronological relation

Causality is always a forward-in-time relationship. The classic anti-pattern:

> "Affiliate marketing **spend** causes conversions."

It doesn't. Affiliate marketing pays per performance. Conversions cause spend to be recorded, not the other way around. The arrow runs from conversions → spend, and including spend as an explanatory variable is model leakage.

Correct examples:

- Click on digital ad → website visit
- Impression on digital ad → conversion
- Brand awareness → brand-query search volume

### Check 2 — Logical non-inclusion

Two variables on the explanatory side cannot be in an inclusion relationship. If you have:

- Total conversions
- Conversions driven by affiliate marketing

…you cannot have both as siblings — affiliate conversions are inside total conversions. The fix is to split: *conversions driven by affiliate* + *conversions driven by everything else*, disjoint and exhaustive.

### Check 3 — Identifiability

Even with correctly-directed arrows and non-overlapping variables, the effect of interest might not be estimable from the data. This is where *causal-graph criteria* matter. Three criteria from Pearl (2009):

#### Single-door criterion — for direct effects

If you want the direct effect $\alpha$ of $X \to Y$ and a variable $Z$:

- is not a descendant of $Y$, and
- d-separates $X$ and $Y$ in the subgraph with $X \to Y$ removed,

then $\alpha$ is identifiable as the partial regression coefficient of $X$ in $Y = \alpha X + \beta Z + \varepsilon$.

#### Back-door criterion — for total effects under confounding

If $X$ and $Y$ share an unobserved common cause, adjusting for a set $Z$ that blocks all *back-door* paths from $X$ to $Y$ (paths starting with an arrow *into* $X$) identifies the total effect.

#### Front-door criterion — when back-door adjustment is impossible

If no admissible $Z$ exists for the back door, but there is a variable $M$ such that:

- $M$ intercepts all directed paths from $X$ to $Y$,
- no unblocked back-door from $X$ to $M$,
- all back-doors from $M$ to $Y$ are blocked by $X$,

then the $X \to Y$ effect is identifiable as $\alpha_{X \to M} \cdot \alpha_{M \to Y}$.

In marketing terms: if media $T$ and purchase $Y$ are confounded, but $T \to \text{brand recall } M \to Y$, then brand-recall surveys can act as a front-door variable and recover the effect.

### Three sales-channel DAG types

Real-world MMMs sort into three DAG shapes depending on sales channel:

| Type | Sales channel | Typical routes |
|---|---|---|
| **Online** | E-commerce, apps, digital services | *Click route*: digital acquisition ads → online CV. Optionally *search route*: TV / video → brand search → CV |
| **Hybrid** | Online + in-house channels (durables, services, some CPG) | Adds an *offline route*: TV / video → in-store visits |
| **Offline** | Store sales via distribution (CPG) | Mainly *offline route*: TV / video → brand preference → distribution → store visits |

The simplest MMM — single-layer regression of KPI on media — only works cleanly for the *click route* in the online type. Adding search or offline routes requires hierarchical / layered structure.

### Why a single-layer model breaks on layered routes

The guidebook runs a simulation study to quantify this. Scenario 2 generates synthetic data where:

- TV and digital video drive brand search volume
- Brand-search and branded-search ads drive conversions
- Display and generic search drive conversions directly

When a **single-layer** model is applied to this two-layer truth, with total CVs as the dependent variable and all media spend as direct explanatory variables:

- TV contribution is under-attributed by approximately **9.8×**
- Branded search contribution is under-attributed by approximately **9.8×**
- Organic baseline is over-attributed by approximately **4.6×**

Not a subtle error — a full order of magnitude. Objective fit metrics (R² ≈ 0.88, MAPE ≈ 6%) don't catch it. Only contextual structural review does.

### How to rescue identifiability when media are correlated

The guidebook gives three practical levers beyond model rewrites:

1. **Staggered flighting** — run two correlated media in deliberately different flight patterns so the correlation drops in the data.
2. **Dark periods** — institute periods where one specific medium is entirely paused, to observe the isolated baseline.
3. **Intermediate measurement** — measure a plausible front-door variable (brand recall surveys, unique-wallet growth for crypto) and include it in the model structure.

These are *marketing operations* decisions, not statistics tricks — the MMM team has to negotiate with campaign planners to create identifiable data. The guidebook frames this as "intentional trial and error": experimentation integrated into marketing operations so the models have something to attribute.

---

## Adapting MMM to on-chain incentives

Three adaptations matter when porting this framework to Gnosis Chain.

### Media, KPI, and control mapping (recap)

| MMM | Crypto |
|---|---|
| Media spend / impressions | Emissions, LM rewards, validator APR, airdrops, bridge incentives |
| KPI | TVL, volume, DAU, tx count, bridge flows |
| Control vars | Gas price, ETH macro, holiday seasonality, protocol launches |

### Crypto-specific failure modes

- **Pay-for-performance loops.** Validator APR is *computed from* deposit volume — so regressing deposits on APR is a reverse-causation trap. Same pattern appears for any token-emission program whose rate is rebalanced to hit a target.
- **Co-launched incentive programs.** DeFi protocols routinely launch multiple incentive streams on the same week (LM + airdrop + referral bonus). Their weekly correlation is often >0.9 → multicollinearity. The fix is the same as the guidebook prescribes — intervention, segmentation, or a front-door variable.
- **Short data windows.** Most Gnosis-sector time series have <60 weekly rows. Below the guidebook threshold, output should be downgraded to "directional only" and Bayesian MCMC is overkill — point estimates with bootstrap intervals are the honest summary.

### Crypto-specific front-door candidates

When the direct incentive → KPI effect is confounded, these on-chain intermediates often satisfy the front-door criterion:

- **Unique-wallet count** between incentive and TVL
- **Brand-query proxy** — block-explorer page views, governance-forum mentions (if off-chain data available)
- **Bridge-inflow lag** between ecosystem campaign and on-chain KPI

### How Cerebro implements this

See [MCP / Marketing Mix Modeling](../../mcp/mmm.md) for the three-persona pipeline (`mmm_analyst` → `mmm_causal_reviewer` → `mmm_simulator`), the full ClickHouse SQL toolkit, and a worked smoke-test example on Gnosis App data.

The key implementation choices:

- **No in-process MCMC.** Response curves fit via ClickHouse `simpleLinearRegression` on log-transformed inputs; credible intervals via SQL bootstrap. Adequate for point estimates; upgrade to Stan / PyMC if tight intervals are the bottleneck.
- **Gated DAG review.** `mmm_causal_reviewer` runs the three Chapter 3 checks against the proposed DAG and **blocks `generate_report`** until it returns `VERDICT: PASS`. This encodes the guidebook's central finding — that structural review is what prevents 9.8× attribution errors.
- **Bounded simulation.** `mmm_simulator` caps per-period reallocation at ±30% and refuses to extrapolate beyond 1.5× observed spend, matching the guidebook's operational-feasibility constraint.

---

## Further reading

- **Hakuhodo DY media partners Inc. (2023).** *Marketing Mix Modeling Guidebook.* The primary source for this page. Chapters 1–3 cover context, mathematical basics, and model-structure considerations respectively.
- **Google (2017).** *Bayesian Methods for Media Mix Modeling with Carryover and Shape Effects.* The canonical reference for the Hill function + carry-over specification used in most modern MMMs.
- **Google (2017).** *Geo-level Bayesian Hierarchical Media Mix Modeling.* The geo-unit variant that unlocks MMM on short national histories.
- **Google (2018).** *Bias Correction For Paid Search in Media Mix Modeling.* Handling the search-route bias discussed in Chapter 3.
- **Google (2019).** *Measuring Effectiveness: Three Grand Challenges.* The long-term-effects modelling constraint and the cold-reader framing.
- **Edwin NG, Zhishi Wang, Athena Dai (2021).** *Bayesian Time Varying Coefficient Model with Applications to Marketing Mix Modeling.* Time-varying coefficients for dynamic businesses.
- **Judea Pearl (2009).** *Causality: Models, Reasoning, and Inference.* Single-door, back-door, and front-door criteria used in Chapter 3.
- **LightweightMMM** — Google's open-source Bayesian MMM library, used as the working model in the guidebook's simulation studies.

## See also — Cerebro implementation

- [MCP / Marketing Mix Modeling](../../mcp/mmm.md) — Cerebro's three-persona MMM pipeline with full SQL toolkit
- [MCP / MMM User Guide](../../mcp/mmm-user-guide.md) — practical playbook: prompt phrasing, data sufficiency, Sector Readiness Matrix, reading coefficients, recipes, FAQ
- [MCP / Cerebro Dispatcher](../../mcp/dispatcher.md) — the top-level router that classifies `mmm` intent and enforces the reviewer gate
- [MCP / Agent Fleet](../../mcp/agents.md) — where the three MMM personas sit in the broader fleet
