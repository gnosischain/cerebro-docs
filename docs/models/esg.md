# ESG Module

The ESG (Environmental, Social, and Governance) module contains approximately **18 models** focused on environmental sustainability metrics for the Gnosis Chain network. It estimates carbon emissions, electrical power consumption, and maps node geographic distribution to regional electricity carbon intensity factors using data from the Ember Global Electricity Review.

## Data Sources

The ESG module combines data from multiple sources:

| Source | Database | Description |
|--------|----------|-------------|
| P2P crawl data | `nebula` | Node geographic distribution from IP geolocation |
| Consensus data | `consensus` | Validator counts and staking participation |
| Ember electricity data | `crawlers_data` | Country-level electricity generation mix and carbon intensity factors |
| Hardware reference data | Built-in | Estimated power consumption profiles for typical validator node hardware |
| ProbeLab data | `crawlers_data` | Cloud provider and hosting classification supplements geographic attribution |

### Ember Global Electricity Review

The [Ember](https://ember-climate.org/) dataset is the backbone of the ESG module's carbon intensity calculations. It provides annually updated, country-level data on:

- Electricity generation by source (coal, gas, oil, nuclear, hydro, wind, solar, bioenergy, other renewables)
- Carbon intensity of electricity generation (gCO2/kWh)
- Total generation capacity and demand

The crawler pipeline fetches Ember data periodically and loads it into the `crawlers_data` database for use by the dbt models.

## Model Categories

<!-- BEGIN AUTO-GENERATED: models-esg -->
**Carbon**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_esg_carbon_intensity_ensemble` | Intermediate | The `int_esg_carbon_intensity_ensemble` model aggregates and enhances uncertainty estimates for country-level electri... |
| `fct_esg_carbon_footprint_uncertainty` | Fact | This model calculates the uncertainty in the carbon footprint of a network by aggregating power consumption, energy, ... |
| `api_esg_carbon_emissions_annualised_latest` | API | This model provides the most recent annualized projection of CO2 emissions in tonnes, derived from ESG carbon footpri... |
| `api_esg_carbon_emissions_daily` | API | The `api_esg_carbon_emissions_daily` model provides daily aggregated estimates of carbon emissions, including moving ... |
| `api_esg_carbon_timeseries_bands` | API | This view provides daily estimates and uncertainty bounds of carbon emissions (in kg CO2) with moving averages and mo... |

**Cif**

| Model | Layer | Description |
|-------|-------|-------------|
| `api_esg_cif_network_vs_countries_daily` | API | This view provides daily effective carbon intensity metrics for the network and selected countries, enabling comparis... |

**Dynamic**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_esg_dynamic_power_consumption` | Intermediate | The int_esg_dynamic_power_consumption model calculates estimated power consumption metrics for different node categor... |

**Energy**

| Model | Layer | Description |
|-------|-------|-------------|
| `api_esg_energy_consumption_annualised_latest` | API | This dbt view provides the latest annualized energy consumption projection in MWh, supporting ESG and carbon footprin... |
| `api_esg_energy_monthly` | API | The api_esg_energy_monthly model aggregates total energy consumption in kilowatt-hours (kWh) on a monthly basis, prov... |

**Estimated**

| Model | Layer | Description |
|-------|-------|-------------|
| `api_esg_estimated_nodes_daily` | API | The api_esg_estimated_nodes_daily model provides daily estimates of observed and projected node counts related to ESG... |

**Info**

| Model | Layer | Description |
|-------|-------|-------------|
| `api_esg_info_annual_daily` | API | The api_esg_info_annual_daily model provides daily projections of energy consumption and CO2 emissions with associate... |
| `api_esg_info_category_daily` | API | The api_esg_info_category_daily model aggregates daily ESG-related metrics, including carbon footprint, energy consum... |

**Node**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_esg_node_classification` | Intermediate | The `int_esg_node_classification` model aggregates and classifies peer nodes based on their observed attributes and o... |
| `int_esg_node_client_distribution` | Intermediate | This model estimates the distribution of client nodes across different node categories by integrating client counts f... |
| `int_esg_node_geographic_distribution` | Intermediate | This model provides a detailed geographic distribution of nodes within different categories, including estimated coun... |
| `int_esg_node_population_chao1` | Intermediate | The int_esg_node_population_chao1 model calculates the estimated diversity of peer nodes based on connection attempts... |

<!-- END AUTO-GENERATED: models-esg -->

## Methodology

The carbon emission estimation follows this pipeline:

```
Step 1: Node Count
    P2P crawl data -> total reachable nodes
                          |
Step 2: Geographic Distribution
    IP geolocation -> map each node to a country
                          |
Step 3: Power Estimate
    Hardware profiles -> per-node power consumption (kWh)
    (execution + consensus client, ~50-100W average)
                          |
Step 4: Carbon Intensity
    Ember data -> country-level gCO2/kWh factor
    Power per node * carbon intensity = emissions per node
                          |
Step 5: Aggregation
    Sum per-node, per-country weighted emissions
    = Total network daily CO2 estimate
```

### Hardware Power Profiles

The module uses conservative power estimates for typical validator hardware configurations:

| Configuration | Estimated Power | Notes |
|---------------|-----------------|-------|
| Lightweight (RPi-class) | ~15-25W | ARM-based single-board computers |
| Standard (NUC-class) | ~50-75W | Intel NUC or mini-PC |
| Server (rack-mounted) | ~100-200W | Dedicated server hardware |
| Cloud instance | ~75-150W | Estimated based on cloud provider PUE |

The default model assumes an average power draw of approximately 50-100W per node, accounting for both execution and consensus client processes running on the same machine.

!!! note "Estimation Caveats"
    These are estimates, not measurements. Actual power consumption varies by hardware, client implementation, and workload. Carbon intensity factors are annual averages and do not capture real-time grid mix variations. Nodes behind VPNs or proxies may be geolocated inaccurately.

## Gnosis Chain vs. Other Networks

Gnosis Chain uses a Proof-of-Stake consensus mechanism with 1 GNO per validator, resulting in a relatively low energy footprint compared to Proof-of-Work networks. The ESG module quantifies this advantage by providing concrete power and emissions estimates.

| Network | Consensus | Annual Energy (est.) |
|---------|-----------|----------------------|
| Gnosis Chain | Proof-of-Stake (1 GNO) | ~500-1000 MWh |
| Ethereum | Proof-of-Stake (32 ETH) | ~2,600 MWh |
| Bitcoin | Proof-of-Work | ~130,000,000 MWh |

!!! info "Orders of Magnitude"
    Gnosis Chain's energy consumption is approximately 5 orders of magnitude lower than Bitcoin and roughly 3x lower than Ethereum (due to lower hardware requirements per validator).

## Key Models Reference

| Model | Description | Key Columns |
|-------|-------------|-------------|
| `api_esg_carbon_emissions_daily` | Daily CO2 estimates | `dt`, `total_co2_grams`, `total_kwh`, `node_count` |
| `api_esg_power_consumption_daily` | Daily power draw | `dt`, `total_kwh`, `avg_watts_per_node`, `node_count` |
| `int_esg_nodes_energy_attribution_daily` | Per-country attribution | `dt`, `country`, `node_count`, `co2_grams`, `carbon_intensity_gco2_kwh` |
| `int_esg_ember_carbon_intensity` | Country carbon factors | `country`, `year`, `carbon_intensity_gco2_kwh` |

## Query Examples

Retrieve daily carbon emissions for the past 30 days:

```sql
SELECT dt, total_co2_grams, total_kwh, node_count
FROM dbt.api_esg_carbon_emissions_daily
WHERE dt >= today() - 30
ORDER BY dt
```

Check emissions by country:

```sql
SELECT country, node_count, co2_grams, carbon_intensity_gco2_kwh
FROM dbt.int_esg_nodes_energy_attribution_daily
WHERE dt = today() - 1
ORDER BY co2_grams DESC
LIMIT 20
```

Compare electricity generation mix for top hosting countries:

```sql
SELECT country, coal_pct, gas_pct, nuclear_pct, renewables_pct
FROM dbt.int_esg_ember_generation_mix
WHERE country IN ('DE', 'US', 'FI', 'FR', 'NL')
ORDER BY renewables_pct DESC
```

Track power consumption trends:

```sql
SELECT
    toStartOfWeek(dt) AS week,
    avg(total_kwh) AS avg_daily_kwh,
    avg(node_count) AS avg_nodes
FROM dbt.api_esg_power_consumption_daily
WHERE dt >= today() - 90
GROUP BY week
ORDER BY week
```

## Related Modules

- [P2P](p2p.md) -- Node geographic distribution feeds into ESG carbon calculations
- [Consensus](consensus.md) -- Validator counts determine the network's node footprint
- [ProbeLab](probelab.md) -- Cloud provider data supplements hosting infrastructure analysis
- [Crawlers](crawlers.md) -- Ember electricity data is ingested through the crawler pipeline
