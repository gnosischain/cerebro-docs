---
title: Dashboard & API
description: ESG dashboard tabs, API endpoints, and query examples
---

# Dashboard & API

The ESG reporting data is surfaced through the Gnosis Analytics dashboard and a set of REST API endpoints. This page documents the dashboard structure, all available API endpoints, authentication, and example queries.

## Dashboard

The ESG dashboard is available at [analytics.gnosischain.com](https://analytics.gnosischain.com) under the **ESG** sector. It provides three tabs for exploring the network's environmental impact.

### Overview Tab

The Overview tab presents headline metrics and trends for the Gnosis Chain network's carbon footprint.

| Widget | Description |
|:-------|:------------|
| Annual CO2 Projection | Annualized carbon emissions estimate (tonnes CO2/year) with 95% confidence interval |
| Annual Energy Projection | Annualized energy consumption (MWh/year) with uncertainty bounds |
| Carbon Intensity Map | Choropleth map showing per-country carbon intensity weighted by node distribution |
| Daily Emissions Timeseries | Line chart of daily CO2 emissions (kg/day) with confidence bands (68%, 90%, 95%) |

### Breakdown Tab

The Breakdown tab disaggregates the network footprint by node category and shows node population trends.

| Widget | Description |
|:-------|:------------|
| Category Breakdown | Stacked bar chart showing Home / Professional / Cloud shares of emissions and energy |
| Annual Projections with Uncertainty | Per-category annualized projections with individual uncertainty bands |
| Estimated Nodes Timeseries | Line chart of total estimated nodes over time, with observed vs. hidden breakdown |

### Methodology Tab

The Methodology tab provides an embedded summary of the ESG estimation methodology, linking to this documentation for full details.

---

## API Endpoints

All ESG endpoints are served under the `/v1/esg/` path prefix. The table below lists every available endpoint.

### Endpoint Reference

| Endpoint | Method | Description |
|:---------|:------:|:------------|
| `/v1/esg/carbon_emissions/daily` | GET, POST | Daily carbon emissions with uncertainty bands |
| `/v1/esg/carbon_emissions_annualised/latest` | GET | Latest annualized CO2 projection (single row) |
| `/v1/esg/carbon_timeseries_bands/daily` | GET, POST | Daily emissions with 68/90/95% confidence bands |
| `/v1/esg/energy/monthly` | GET, POST | Monthly energy consumption by category |
| `/v1/esg/energy_consumption_annualised/latest` | GET | Latest annualized energy projection (single row) |
| `/v1/esg/cif_network_vs_countries/daily` | GET, POST | Network CI compared to individual countries |
| `/v1/esg/estimated_nodes/daily` | GET, POST | Daily node count estimates with category breakdown |
| `/v1/esg/info_category/daily` | GET, POST | Per-category daily breakdown (nodes, energy, CO2) |
| `/v1/esg/info_annual/daily` | GET, POST | Rolling annual projections updated daily |

### Common Parameters

All `daily` and `monthly` endpoints that support GET and POST accept the following query parameters:

| Parameter | Type | Default | Description |
|:----------|:-----|:--------|:------------|
| `dt` | `string` | -- | Filter by date (ISO 8601 format: `YYYY-MM-DD`). For ranges, use `dt_gte` and `dt_lte`. |
| `limit` | `integer` | 100 | Maximum number of rows to return (max: 10,000) |
| `offset` | `integer` | 0 | Number of rows to skip (for pagination) |
| `sort` | `string` | `date:desc` | Sort order. Format: `column:asc` or `column:desc` |

!!! tip "POST Requests"
    POST endpoints accept the same parameters as JSON in the request body. Use POST when constructing queries with multiple filters or when parameter values are complex.

### Response Format

All endpoints return JSON with the following structure:

```json
{
  "data": [
    {
      "date": "2025-12-01",
      "co2_kg_day": 1173.42,
      "co2_kg_day_lower_95": 479.21,
      "co2_kg_day_upper_95": 1867.63,
      "energy_kwh_day": 3666.31,
      "nodes_estimated": 1245.0
    }
  ],
  "meta": {
    "total_rows": 365,
    "limit": 100,
    "offset": 0,
    "execution_time_ms": 42
  }
}
```

---

## Authentication & Rate Limits

### API Tiers

| Tier | Authentication | Rate Limit | Access |
|:----:|:---------------|:----------:|:-------|
| Tier 0 | None (public) | 20 req/min | All ESG endpoints |
| Tier 1 | API key required | 100 req/min | All endpoints + extended history |
| Tier 2 | API key required | 500 req/min | All endpoints + raw data access |
| Tier 3 | API key required | 1,000 req/min | Enterprise / dedicated |

!!! info "Tier 0 -- No Authentication Required"
    All ESG endpoints listed above are available at **Tier 0** (public access) with no API key required. Rate limiting is applied per IP address at 20 requests per minute.

For Tier 1+ access, include your API key in the request header:

```bash
curl -H "X-API-Key: your-api-key" \
  "https://analytics.gnosischain.com/api/v1/esg/carbon_emissions/daily?limit=30"
```

---

## Query Examples

### 1. Daily Carbon Emissions -- Past 30 Days

Retrieve the most recent 30 days of daily carbon emissions with uncertainty bounds.

=== "SQL"

    ```sql
    SELECT
        date,
        co2_kg_day,
        co2_kg_day_lower_95,
        co2_kg_day_upper_95,
        energy_kwh_day,
        nodes_estimated
    FROM api_esg_carbon_emissions_daily
    WHERE date >= today() - INTERVAL 30 DAY
    ORDER BY date DESC
    ```

=== "API"

    ```bash
    curl "https://analytics.gnosischain.com/api/v1/esg/carbon_emissions/daily?limit=30&sort=date:desc"
    ```

=== "Python"

    ```python
    import requests

    response = requests.get(
        "https://analytics.gnosischain.com/api/v1/esg/carbon_emissions/daily",
        params={"limit": 30, "sort": "date:desc"}
    )
    data = response.json()["data"]
    ```

---

### 2. Emissions by Country

Show carbon emissions disaggregated by country, sorted by contribution.

=== "SQL"

    ```sql
    SELECT
        date,
        country_code,
        network_ci,
        country_ci,
        network_vs_country_ratio
    FROM api_esg_cif_network_vs_countries_daily
    WHERE date = today() - 1
    ORDER BY country_ci DESC
    LIMIT 20
    ```

=== "API"

    ```bash
    curl "https://analytics.gnosischain.com/api/v1/esg/cif_network_vs_countries/daily?dt=2025-12-01&limit=20&sort=country_ci:desc"
    ```

---

### 3. Compare Electricity Generation Mix

Query the staging model to compare generation mix across countries.

```sql
SELECT
    country_code,
    generation_type,
    share_pct
FROM stg_crawlers_data__ember_electricity_data
WHERE country_code IN ('DE', 'US', 'FR', 'NO', 'CN')
  AND date = (
      SELECT max(date)
      FROM stg_crawlers_data__ember_electricity_data
  )
ORDER BY country_code, share_pct DESC
```

---

### 4. Track Power Consumption Trends

Monitor how average power consumption per node evolves over time, broken down by category.

=== "SQL"

    ```sql
    SELECT
        date,
        category,
        nodes AS node_count,
        energy_kwh,
        co2_kg,
        power_w_avg
    FROM api_esg_info_category_daily
    WHERE date >= today() - INTERVAL 90 DAY
    ORDER BY date DESC, category
    ```

=== "API"

    ```bash
    curl "https://analytics.gnosischain.com/api/v1/esg/info_category/daily?limit=270&sort=date:desc"
    ```

---

### 5. Latest Annualized Projection with Uncertainty Bounds

Get the most recent annualized carbon footprint and energy projection, including confidence intervals.

=== "SQL"

    ```sql
    SELECT
        co2_tonnes_year,
        co2_tonnes_year_lower_95,
        co2_tonnes_year_upper_95,
        energy_mwh_year,
        as_of_date
    FROM api_esg_carbon_emissions_annualised_latest
    ```

=== "API"

    ```bash
    curl "https://analytics.gnosischain.com/api/v1/esg/carbon_emissions_annualised/latest"
    ```

=== "Response"

    ```json
    {
      "data": [
        {
          "co2_tonnes_year": 428.1,
          "co2_tonnes_year_lower_95": 174.9,
          "co2_tonnes_year_upper_95": 681.3,
          "energy_mwh_year": 1338.2,
          "as_of_date": "2025-12-01"
        }
      ],
      "meta": {
        "total_rows": 1,
        "limit": 1,
        "offset": 0,
        "execution_time_ms": 5
      }
    }
    ```

---

## Related Pages

- [Carbon Intensity Model](carbon-intensity.md) -- How country-level carbon intensity is calculated from Ember data
- [Carbon Footprint Calculation](carbon-footprint.md) -- The emissions formula and uncertainty propagation
- [ESG Data Pipeline](data-pipeline.md) -- Full dbt model DAG and specifications
