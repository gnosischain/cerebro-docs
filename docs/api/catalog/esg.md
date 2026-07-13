# ESG API Endpoints

<!-- BEGIN AUTO-GENERATED: api-catalog-esg -->
_9 endpoints across 9 resources. Generated from the dbt manifest — edits inside this block will be overwritten. Regenerate with `python scripts/update_docs.py --only api`._

## carbon_emissions

The `api_esg_carbon_emissions_daily` model provides daily aggregated estimates of carbon emissions, including moving averages and uncertainty bounds, to support ESG reporting and analysis.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/esg/carbon_emissions/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/esg/carbon_emissions/daily`"
    The `api_esg_carbon_emissions_daily` model provides daily aggregated estimates of carbon emissions, including moving averages and uncertainty bounds, to support ESG reporting and analysis.

    Model: `api_esg_carbon_emissions_daily` — table `dbt.api_esg_carbon_emissions_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific calendar date for the recorded carbon emissions data. |
    | `ma7_value` | `Float64` | 7-day moving average of the daily mean CO2 emissions in kilograms, providing a smoothed trend over the past week. |
    | `ma7_lower_90` | `Float64` | 7-day moving average of the lower 90% confidence bound for daily CO2 emissions in kilograms, indicating the lower estimate of uncertainty. |
    | `ma7_upper_90` | `Float64` | 7-day moving average of the upper 90% confidence bound for daily CO2 emissions in kilograms, indicating the upper estimate of uncertainty. |
    | `ma7_lower_95` | `Float64` | 7-day moving average of the lower 95% confidence bound for daily CO2 emissions in kilograms, representing a more conservative lower estimate. |
    | `ma7_upper_95` | `Float64` | 7-day moving average of the upper 95% confidence bound for daily CO2 emissions in kilograms, representing a more conservative upper estimate. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/esg/carbon_emissions/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## carbon_emissions_annualised

This model provides the most recent annualized projection of CO2 emissions in tonnes, derived from ESG carbon footprint data, to support environmental impact assessments and reporting.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/esg/carbon_emissions_annualised/latest` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/esg/carbon_emissions_annualised/latest`"
    This model provides the most recent annualized projection of CO2 emissions in tonnes, derived from ESG carbon footprint data, to support environmental impact assessments and reporting.

    Model: `api_esg_carbon_emissions_annualised_latest` — table `dbt.api_esg_carbon_emissions_annualised_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `annual_co2_tonnes_projected` | `Float64` | Estimated total CO2 emissions in tonnes for the latest available year, representing projected annualized emissions based on recent data. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/esg/carbon_emissions_annualised/latest"
    ```

## carbon_emissions_distribution

This view provides daily estimates and uncertainty bounds of carbon emissions (in kg CO2) with moving averages and month-to-date aggregations to support ESG reporting and analysis.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/esg/carbon_emissions_distribution/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/esg/carbon_emissions_distribution/daily`"
    This view provides daily estimates and uncertainty bounds of carbon emissions (in kg CO2) with moving averages and month-to-date aggregations to support ESG reporting and analysis.

    Model: `api_esg_carbon_timeseries_bands` — table `dbt.api_esg_carbon_timeseries_bands`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific calendar date for the recorded carbon emission data. |
    | `value` | `Float64` | The daily mean estimate of CO2 emissions in kilograms. |
    | `lower_95` | `Float64` | The lower bound of the 95% confidence interval for daily CO2 emissions. |
    | `upper_95` | `Float64` | The upper bound of the 95% confidence interval for daily CO2 emissions. |
    | `lower_90` | `Float64` | The lower bound of the 90% confidence interval for daily CO2 emissions. |
    | `upper_90` | `Float64` | The upper bound of the 90% confidence interval for daily CO2 emissions. |
    | `ma7_value` | `Float64` | 7-day moving average of the daily mean CO2 emissions, smoothing short-term fluctuations. |
    | `ma7_lower_95` | `Float64` | 7-day moving average of the lower 95% confidence bound. |
    | `ma7_upper_95` | `Float64` | 7-day moving average of the upper 95% confidence bound. |
    | `mtd_avg` | `DateTime64` | Month-to-date average of daily mean CO2 emissions up to the current date. |
    | `mtd_total` | `DateTime64` | Cumulative total of daily mean CO2 emissions for the current month. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/esg/carbon_emissions_distribution/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## carbon_intensity_factors

This view provides daily effective carbon intensity metrics for the network and selected countries, enabling comparison of carbon footprint performance over time.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/esg/carbon_intensity_factors/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/esg/carbon_intensity_factors/daily`"
    This view provides daily effective carbon intensity metrics for the network and selected countries, enabling comparison of carbon footprint performance over time.

    Model: `api_esg_cif_network_vs_countries_daily` — table `dbt.api_esg_cif_network_vs_countries_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific date for the recorded carbon intensity data, formatted as YYYY-MM-DD. |
    | `carbon_intensity` | `Float64` | The measured carbon intensity value in grams of CO2 equivalent per kWh, rounded to one decimal place. |
    | `entity_code` | `String` | Identifier for the data source or country, such as 'GNOSIS' for the network or country codes like 'USA' and 'DEU'. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/esg/carbon_intensity_factors/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## energy_and_emissions_annual

The api_esg_info_annual_daily model provides daily projections of energy consumption and CO2 emissions with associated uncertainty intervals, supporting ESG performance analysis at a daily granularity.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/esg/energy_and_emissions_annual/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/esg/energy_and_emissions_annual/daily`"
    The api_esg_info_annual_daily model provides daily projections of energy consumption and CO2 emissions with associated uncertainty intervals, supporting ESG performance analysis at a daily granularity.

    Model: `api_esg_info_annual_daily` — table `dbt.api_esg_info_annual_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific date for which the energy or emissions data is reported. |
    | `label` | `String` | The type of metric, either 'Energy (MWh)' or 'CO2e (tonnes)', indicating the measurement category. |
    | `mean_val` | `Float64` | The projected average value of energy consumption in MWh or CO2 emissions in tonnes for the given date. |
    | `lower_95` | `Float64` | The lower bound of the 95% confidence interval for the projected value. |
    | `upper_95` | `Float64` | The upper bound of the 95% confidence interval for the projected value. |
    | `lower_90` | `Float64` | The lower bound of the 90% confidence interval for the projected value. |
    | `upper_90` | `Float64` | The upper bound of the 90% confidence interval for the projected value. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/esg/energy_and_emissions_annual/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## energy_and_emissions_per_category

The api_esg_info_category_daily model aggregates daily ESG-related metrics, including carbon footprint, energy consumption, and node counts, categorized by stakeholder type for analytical insights.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/esg/energy_and_emissions_per_category/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/esg/energy_and_emissions_per_category/daily`"
    The api_esg_info_category_daily model aggregates daily ESG-related metrics, including carbon footprint, energy consumption, and node counts, categorized by stakeholder type for analytical insights.

    Model: `api_esg_info_category_daily` — table `dbt.api_esg_info_category_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The date for which the ESG metrics are recorded, in date format. |
    | `label` | `String` | The stakeholder group associated with the metrics, such as Home Staker, Professional Validator, Cloud Provider, or Unknown. |
    | `category` | `String` | The type of metric, either 'CO2e (kg)', 'Energy (kWh)', or 'Nodes'. |
    | `value` | `Float64` | The measured value of the metric, representing daily totals or counts. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/esg/energy_and_emissions_per_category/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## energy_consumption

The api_esg_energy_monthly model aggregates total energy consumption in kilowatt-hours (kWh) on a monthly basis, providing insights into energy usage trends for ESG reporting and analysis.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/esg/energy_consumption/monthly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/esg/energy_consumption/monthly`"
    The api_esg_energy_monthly model aggregates total energy consumption in kilowatt-hours (kWh) on a monthly basis, providing insights into energy usage trends for ESG reporting and analysis.

    Model: `api_esg_energy_monthly` — table `dbt.api_esg_energy_monthly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `DateTime64` | The first day of the month representing the aggregation period. |
    | `value` | `UInt64` | The total energy consumption in kilowatt-hours (kWh) for the given month. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/esg/energy_consumption/monthly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## energy_consumption_annualised

This dbt view provides the latest annualized energy consumption projection in MWh, supporting ESG and carbon footprint analysis for energy management.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/esg/energy_consumption_annualised/latest` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/esg/energy_consumption_annualised/latest`"
    This dbt view provides the latest annualized energy consumption projection in MWh, supporting ESG and carbon footprint analysis for energy management.

    Model: `api_esg_energy_consumption_annualised_latest` — table `dbt.api_esg_energy_consumption_annualised_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `annual_energy_Mwh_projected` | `Float64` | The projected total energy consumption for the year, expressed in megawatt-hours (MWh). |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/esg/energy_consumption_annualised/latest"
    ```

## estimated_nodes

The api_esg_estimated_nodes_daily model provides daily estimates of observed and projected node counts related to ESG carbon footprint analysis, facilitating trend analysis and uncertainty quantification.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/esg/estimated_nodes/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/esg/estimated_nodes/daily`"
    The api_esg_estimated_nodes_daily model provides daily estimates of observed and projected node counts related to ESG carbon footprint analysis, facilitating trend analysis and uncertainty quantification.

    Model: `api_esg_estimated_nodes_daily` — table `dbt.api_esg_estimated_nodes_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific calendar date for the recorded data point. |
    | `baseline_observed_nodes` | `Float64` | The observed number of nodes based on baseline measurements on the given date. |
    | `estimated_nodes` | `UInt64` | The model's estimated total number of nodes for the given date. |
    | `nodes_lower_95` | `UInt64` | The lower bound of the 95% confidence interval for the estimated node count. |
    | `nodes_upper_95` | `UInt64` | The upper bound of the 95% confidence interval for the estimated node count. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/esg/estimated_nodes/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```
<!-- END AUTO-GENERATED: api-catalog-esg -->
