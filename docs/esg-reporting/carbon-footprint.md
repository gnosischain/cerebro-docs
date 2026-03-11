---
title: Carbon Footprint Calculation
description: Final emissions formula, uncertainty propagation, and confidence intervals
---

# Carbon Footprint Calculation

This page describes the final carbon footprint formula, how uncertainties from all upstream models are propagated through the calculation, and how confidence intervals are constructed for reporting.

## Core Formula

The daily CO2 emissions for the Gnosis Chain network are calculated as:

$$
CO_{2,\text{daily}} \text{ (kg)} = \frac{N \times P_W \times 24 \times PUE \times CI}{1{,}000{,}000}
$$

Where:

| Symbol | Description | Unit |
|:-------|:------------|:-----|
| $N$    | Estimated number of nodes | count |
| $P_W$  | Average power consumption per node | watts (W) |
| $24$   | Hours per day | hours |
| $PUE$  | Power Usage Effectiveness (data center overhead) | dimensionless |
| $CI$   | Carbon intensity of electricity | gCO2/kWh |
| $1{,}000{,}000$ | Conversion factor (W to kW, g to kg) | -- |

## Full Per-Category, Per-Country Expansion

In practice, the calculation is disaggregated by **node category** (Home, Professional, Cloud) and **country**, then summed:

$$
CO_{2,\text{daily}} = \sum_{c} \sum_{k} \frac{N_{c,k} \times P_{k} \times 24 \times PUE_{k} \times CI_{c}}{1{,}000{,}000}
$$

Where:

- $c$ indexes countries
- $k$ indexes node categories (Home, Professional, Cloud)
- $N_{c,k}$ = estimated node count for category $k$ in country $c$
- $P_k$ = power consumption for category $k$ (varies by client and hardware profile)
- $PUE_k$ = PUE for category $k$ (Home: ~1.0, Professional: ~1.2, Cloud: ~1.1--1.4)
- $CI_c$ = carbon intensity for country $c$

This disaggregation allows reporting at any level of granularity: per-country, per-category, or total network.

## Uncertainty Propagation

Each input variable carries its own uncertainty. The relative uncertainty in the final CO2 estimate is computed by combining all sources in quadrature:

$$
\frac{\sigma_{CO_2}}{CO_2} = \sqrt{\left(\frac{\sigma_N}{N}\right)^2 + \left(\frac{\sigma_P}{P}\right)^2 + \left(\frac{\sigma_{CI}}{CI}\right)^2}
$$

!!! info "Independence Assumption"
    This formula assumes the uncertainties in node count, power consumption, and carbon intensity are independent. In practice, mild correlations exist (e.g., regions with more hidden nodes may also have less reliable CI data), but these are second-order effects.

### Typical Uncertainty Magnitudes

| Source | Symbol | Typical Range | Primary Driver |
|:-------|:------:|:-------------:|:---------------|
| Node population estimate | $\sigma_N / N$ | 15--30% | Hidden nodes undetected by Nebula crawler |
| Power consumption | $\sigma_P / P$ | 10--20% | Variation across hardware, client software, and validator count |
| Carbon intensity | $\sigma_{CI} / CI$ | 12--25% | Grid-type uncertainty + seasonal adjustment + Ember data lag |
| PUE | -- | 10--20% | Absorbed into power term; varies by facility type |
| Combined | $\sigma_{CO_2} / CO_2$ | 22--40% | Dominated by node count uncertainty |

## Confidence Intervals

Given the combined relative uncertainty $\sigma_{CO_2} / CO_2$, confidence intervals are constructed assuming a log-normal distribution:

| Confidence Level | Multiplier | Formula |
|:----------------:|:----------:|:--------|
| 68% (1-sigma)    | 1.000      | $CO_2 \pm 1.00 \times \sigma_{CO_2}$ |
| 90%              | 1.645      | $CO_2 \pm 1.645 \times \sigma_{CO_2}$ |
| 95%              | 1.960      | $CO_2 \pm 1.96 \times \sigma_{CO_2}$ |
| 99%              | 2.576      | $CO_2 \pm 2.576 \times \sigma_{CO_2}$ |

??? example "Worked Example: Daily Carbon Footprint"
    **Given:**

    - Network energy consumption: **3,666 kWh/day**
    - Effective carbon intensity: CI = **320 gCO2/kWh**
    - Node count uncertainty: $\sigma_N / N$ = 25%
    - Power uncertainty: $\sigma_P / P$ = 15%
    - CI uncertainty: $\sigma_{CI} / CI$ = 8%

    **Step 1 -- Compute daily emissions:**

    $$
    CO_{2,\text{daily}} = \frac{3{,}666 \text{ kWh} \times 320 \text{ gCO}_2\text{/kWh}}{1{,}000} = 1{,}173 \text{ kg CO}_2\text{/day}
    $$

    **Step 2 -- Compute combined relative uncertainty:**

    $$
    \frac{\sigma_{CO_2}}{CO_2} = \sqrt{0.25^2 + 0.15^2 + 0.08^2} = \sqrt{0.0625 + 0.0225 + 0.0064} = \sqrt{0.0914} = 0.302 = 30.2\%
    $$

    **Step 3 -- Compute absolute uncertainty:**

    $$
    \sigma_{CO_2} = 1{,}173 \times 0.302 = 354 \text{ kg CO}_2\text{/day}
    $$

    **Step 4 -- Construct 95% confidence interval:**

    $$
    CI_{95\%} = 1{,}173 \pm 1.96 \times 354 = 1{,}173 \pm 694
    $$

    $$
    CI_{95\%} = [479, 1{,}867] \text{ kg CO}_2\text{/day}
    $$

    **Result:** The daily carbon footprint is estimated at **1,173 kg CO2/day** with a 95% confidence interval of **[479, 1,867] kg CO2/day**.

## Strengths

The Gnosis Chain ESG methodology has several notable strengths:

- **Empirical hardware data**: Power consumption estimates are grounded in CCRI benchmarking data for actual validator hardware, not theoretical models
- **Chao-1 population estimation**: The hidden node population is estimated using the Chao-1 ecological estimator, a well-established method for estimating population sizes from incomplete samples
- **Comprehensive uncertainty quantification**: Every stage of the pipeline propagates uncertainty, producing confidence intervals rather than point estimates
- **Seasonal carbon intensity adjustments**: Continent-level seasonal factors capture the variation in electricity generation mix throughout the year
- **Client-specific power profiles**: Different execution and consensus client combinations are assigned distinct power consumption estimates based on measured benchmarks
- **Country-level granularity**: Carbon intensity is resolved at the country level using Ember data, not coarse regional averages

## Known Limitations

!!! warning "Not a Measurement"
    The carbon footprint figures produced by this pipeline are **estimates, not direct measurements**. No on-device power metering is performed. The results should be interpreted as best-effort approximations with explicitly quantified uncertainty.

| Limitation | Impact | Magnitude |
|:-----------|:-------|:---------:|
| Hidden nodes not detected by Nebula | Undercount of true network size | ~25% |
| Power consumption variation across hardware | Single average per category may not reflect actual distribution | +/-15% |
| VPN/proxy misattribution of node locations | Nodes mapped to incorrect countries, skewing CI weighting | ~5% |
| Monthly Ember data granularity | Cannot capture intra-month generation mix changes (e.g., weather events) | Moderate |
| Client efficiency estimates based on limited benchmarks | May not reflect real-world conditions under load | +/-10% |
| PUE averages per category | Actual PUE varies widely even within a category | +/-10--20% |
| Multi-validator nodes | A single machine running multiple validators is counted once for power but contributes multiple validator slots | Variable |

## References

??? quote "Citations"
    1. **Chao, A. (1984)**. Nonparametric estimation of the number of classes in a population. *Scandinavian Journal of Statistics*, 11(4), 265--270. Foundation for the Chao-1 hidden population estimator used in node count estimation.

    2. **Crypto Carbon Ratings Institute (CCRI, 2022)**. Energy Consumption and Carbon Emissions of Proof-of-Stake Networks. Provides empirical power consumption benchmarks for validator hardware across multiple PoS networks including Gnosis Chain.

    3. **Ember (2024)**. Global Electricity Review 2024. Annual and monthly electricity generation data by country and fuel type, used for country-level carbon intensity calculations.

    4. **Chao, A. & Chiu, C.-H. (2016)**. Species richness: estimation and comparison. *Wiley StatsRef: Statistics Reference Online*, 1--26. Extended coverage of Chao estimators including bias correction and confidence interval construction.

## Internal References

- [ESG Data Pipeline](data-pipeline.md) -- Full dbt model DAG and specifications
- [Carbon Intensity Model](carbon-intensity.md) -- Ember data integration and CI calculation details
- [Dashboard & API](dashboard-api.md) -- ESG dashboard and API endpoint documentation
