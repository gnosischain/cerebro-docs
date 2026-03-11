# Dashboard Configuration

The metrics dashboard uses a YAML-driven configuration system. All layout, metric placement, and sector definitions are managed through YAML files and JavaScript metric definitions. No code changes are needed to add new metrics or rearrange the layout.

## Configuration Hierarchy

```
public/dashboard.yml                  -- Sector index (ordering, icons, palettes)
  |
  +-- public/dashboards/overview.yml  -- Sector layout (metrics, tabs, grid)
  +-- public/dashboards/consensus.yml
  +-- public/dashboards/bridges.yml
  +-- ...
  |
src/queries/*.js                      -- Metric definitions (SQL, chart type, formatting)
```

At startup, the frontend loads `dashboard.yml`, resolves each sector's `source` file, and merges the layout entries with metric definitions from `src/queries/` to produce fully configured widgets.

## Sector Index (`dashboard.yml`)

The top-level `public/dashboard.yml` defines the sector catalog:

```yaml
Overview:
  name: Overview
  order: 1
  icon: "chart-icon"
  iconClass: "chart-line"
  source: /dashboards/overview.yml

GnosisPay:
  name: Gnosis Pay
  order: 10
  icon: "card-icon"
  iconClass: credit-card
  palette: gnosis-pay
  source: /dashboards/gnosis-pay.yml

Consensus:
  name: Consensus
  order: 20
  icon: "validator-icon"
  iconClass: "shield-check"
  source: /dashboards/consensus.yml
```

### Sector Properties

| Property | Required | Description |
|----------|----------|-------------|
| `name` | Yes | Display name in the sidebar navigation |
| `order` | Yes | Numeric sort order (lower appears first) |
| `icon` | Yes | Icon identifier |
| `iconClass` | Yes | CSS icon class (Lucide icon name) |
| `source` | Yes | Path to the sector layout YAML file |
| `palette` | No | Named color palette preset (e.g., `gnosis-pay`, `standard`) |

## Sector Layout Files

Each sector file in `public/dashboards/` defines either a flat list of metrics or a tabbed layout.

### Simple Layout (Flat Metrics)

```yaml
metrics:
  - id: overview_total_transactions
    gridRow: 1
    gridColumn: 1 / span 2
    minHeight: 130px

  - id: overview_active_validators
    gridRow: 1
    gridColumn: 3
    minHeight: 130px

  - id: overview_daily_transactions_chart
    gridRow: 2
    gridColumn: 1 / span 3
    minHeight: 400px
```

### Tabbed Layout

```yaml
tabs:
  - name: Validators
    metrics:
      - id: consensus_active_validators
        gridRow: 1
        gridColumn: 1 / span 3
        minHeight: 400px

      - id: consensus_validator_deposits
        gridRow: 2
        gridColumn: 1 / span 2
        minHeight: 350px

  - name: Attestations
    metrics:
      - id: consensus_attestation_rate
        gridRow: 1
        gridColumn: 1 / span 3
        minHeight: 400px
```

### Grid Placement Properties

| Property | Required | Description |
|----------|----------|-------------|
| `id` | Yes | Metric ID matching a definition in `src/queries/` |
| `gridRow` | Yes | CSS Grid row position |
| `gridColumn` | Yes | CSS Grid column position (supports `span` syntax) |
| `minHeight` | No | Minimum card height (CSS value, e.g., `400px`) |

## Metric Definitions (`src/queries/`)

Each metric is defined as a JavaScript module exporting a configuration object:

```javascript
// src/queries/dailyTransactions.js
const dailyTransactions = {
  id: 'daily_transactions',
  name: 'Daily Transactions',
  description: 'Total transactions per day on Gnosis Chain',
  metricDescription: 'Counts all transactions included in blocks...',
  format: 'formatNumber',
  chartType: 'line',
  color: '#00BCD4',
  query: `
    SELECT
      toDate(dt) AS date,
      txs AS value
    FROM dbt.api_execution_transactions_daily
    WHERE dt BETWEEN '{from}' AND '{to}'
    ORDER BY date
  `
};

export default dailyTransactions;
```

### Metric Properties

| Property | Required | Description |
|----------|----------|-------------|
| `id` | Yes | Unique identifier matching the YAML layout `id` |
| `name` | Yes | Display name shown on the chart card title |
| `description` | No | Subtitle shown below the card title |
| `metricDescription` | No | Extended description shown in the info popover (supports markdown) |
| `format` | Yes | Value formatter function name (from `src/utils/formatter.js`) |
| `chartType` | Yes | ECharts chart type (`line`, `bar`, `area`, `pie`, `number`, etc.) |
| `color` | No | Primary chart color (hex string) |
| `colors` | No | Array of colors for multi-series charts |
| `query` | Yes | SQL query with `{from}` and `{to}` date placeholders |

### Chart Types

The dashboard supports several chart types, each suited to different data visualizations:

| `chartType` Value | Component | Use Case |
|-------------------|-----------|----------|
| `line` | LineChart | Time series trends, continuous data over time |
| `bar` | BarChart | Categorical comparisons, rankings, discrete values |
| `area` | StackedArea | Time series with volume emphasis, cumulative totals |
| `pie` | PieChart | Proportional distribution of categories |
| `number` | NumberDisplay | Single KPI or headline metric with optional delta |
| `stackedBar` | BarChart (stacked) | Multi-series categorical data showing composition |
| `multiLine` | LineChart (multi-series) | Multiple time series on a single axis |

The `NumberDisplay` type renders a large headline number with an optional percentage change indicator. It is typically used in the first row of a sector layout for key performance indicators.

### Query Placeholders

SQL queries support these placeholder tokens, which are replaced at request time:

| Placeholder | Substitution |
|-------------|--------------|
| `{from}` | Start date (ISO format, e.g., `2026-01-01`) |
| `{to}` | End date (ISO format, e.g., `2026-03-10`) |

## Adding a New Metric

1. **Create the metric definition** in `src/queries/`:

    ```javascript
    // src/queries/newMetric.js
    const newMetric = {
      id: 'new_metric_id',
      name: 'My New Metric',
      description: 'Description of the metric',
      format: 'formatNumber',
      chartType: 'line',
      color: '#4CAF50',
      query: `
        SELECT
          toDate(dt) AS date,
          some_column AS value
        FROM dbt.api_execution_some_table
        WHERE dt BETWEEN '{from}' AND '{to}'
        ORDER BY date
      `
    };

    export default newMetric;
    ```

2. **Place the metric in a sector YAML file** (`public/dashboards/<sector>.yml`):

    ```yaml
    metrics:
      # ... existing metrics ...
      - id: new_metric_id
        gridRow: 3
        gridColumn: 1 / span 3
        minHeight: 400px
    ```

3. **Export the query to the API layer**:

    ```bash
    pnpm run export-queries
    ```

    This script copies metric queries from `src/queries/` to `api/queries/` in the JSON format consumed by the serverless API.

4. **Test locally**:

    ```bash
    pnpm dev
    ```

5. **Deploy**:

    ```bash
    vercel --prod
    ```

!!! note "Visibility Requirement"
    Metrics that exist in `src/queries/` but are **not** placed in any YAML sector file will not appear in the dashboard or in header search results. A metric must be referenced by `id` in at least one sector layout to be rendered.

## Adding a New Sector

1. **Create the sector layout file** at `public/dashboards/<new-sector>.yml`:

    ```yaml
    metrics:
      - id: first_metric
        gridRow: 1
        gridColumn: 1 / span 3
        minHeight: 400px
    ```

2. **Register the sector** in `public/dashboard.yml`:

    ```yaml
    NewSector:
      name: New Sector
      order: 50
      icon: "new-icon"
      iconClass: "layers"
      source: /dashboards/new-sector.yml
    ```

3. Restart the development server. The new sector will appear in the sidebar navigation.

## Palette System

Dashboards can opt into named color palettes defined in `src/utils/dashboardPalettes.js`. Palettes are applied at the dashboard level and affect all charts within that sector.

### Precedence Rules

1. **Metric-level colors win**: If a metric defines `color`, `colors`, `bandColors`, `lineColors`, or map-specific overrides, those are used regardless of the dashboard palette.
2. **Dashboard palette applies as fallback**: When metric-level colors are not explicitly defined, the dashboard's palette colors are used.
3. **Standard fallback**: If no dashboard palette is set or the palette name is invalid, the `standard` palette is used.
4. **Fill from standard**: If a custom palette has fewer colors than the number of chart series, additional colors are drawn from the `standard` palette before repeating.

### Defining a New Palette

Add a new preset to `src/utils/dashboardPalettes.js`:

```javascript
export const PALETTES = {
  standard: ['#3366CC', '#DC3912', '#FF9900', ...],
  'gnosis-pay': ['#04795B', '#06A87D', '#08D49E', ...],
  'my-palette': ['#1A1A2E', '#16213E', '#0F3460', '#E94560'],
};
```

Then reference it in `dashboard.yml`:

```yaml
MyDashboard:
  palette: my-palette
  source: /dashboards/my-dashboard.yml
```

## Caching Configuration

The serverless API implements server-side caching to minimize ClickHouse query load.

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CACHE_TTL_HOURS` | `24` | How long cache entries remain valid |
| `CACHE_REFRESH_HOURS` | `24` | How often the automatic cache refresh runs |

### Cache Behavior by Environment

| Environment | Default `useCached` | Cache-Control Header |
|-------------|--------------------|-----------------------|
| Development (`NODE_ENV=development`) | `false` | `no-store, max-age=0` |
| Production | `true` | Standard caching headers |

### Manual Cache Operations

Force a cache refresh for a specific request:

```
GET /api/metrics?refreshCache=true
```

Check cache status:

```
GET /api/test
```

(Requires `X-API-Key` header)

### Override Per-Request

You can explicitly control caching on any request:

```
GET /api/metrics/daily_transactions?useCached=false    # Force fresh query
GET /api/metrics/daily_transactions?useCached=true     # Use cache even in dev
```

## Environment Variables

### Backend (Serverless API)

| Variable | Required | Description |
|----------|----------|-------------|
| `CLICKHOUSE_HOST` | Yes | ClickHouse server hostname |
| `CLICKHOUSE_USER` | Yes | ClickHouse username |
| `CLICKHOUSE_PASSWORD` | Yes | ClickHouse password |
| `CLICKHOUSE_DATABASE` | No | Default database name |
| `CLICKHOUSE_DBT_SCHEMA` | No | dbt schema prefix for query rewriting (default: `dbt`) |
| `API_KEY` | Yes | API key for authenticating frontend requests |
| `CACHE_TTL_HOURS` | No | Cache validity period in hours (default: 24) |
| `CACHE_REFRESH_HOURS` | No | Cache auto-refresh interval in hours (default: 24) |

### Frontend (Vite)

| Variable | Required | Description |
|----------|----------|-------------|
| `VITE_API_URL` | Yes | API base URL (typically `/api` for relative path) |
| `VITE_API_KEY` | Yes | Same value as `API_KEY` |
| `VITE_USE_MOCK_DATA` | No | Set to `true` to use generated mock data instead of ClickHouse |
| `VITE_DASHBOARD_TITLE` | No | Custom dashboard title displayed in the header |
| `VITE_PUBLIC_BASE_URL` | No | Base URL for public assets |
| `VITE_DEV_API_PROXY_TARGET` | No | Local API proxy target for `pnpm dev` |

## Development

### Local Setup

```bash
git clone https://github.com/gnosischain/metrics-dashboard.git
cd metrics-dashboard
pnpm install
cp .env.example .env
# Edit .env with ClickHouse credentials
pnpm dev
```

### Mock Data Mode

Run without ClickHouse by enabling mock data generation:

```bash
VITE_USE_MOCK_DATA=true pnpm dev
```

The API will generate synthetic data for all metrics.

### Deployment

```bash
# Install Vercel CLI
npm install -g vercel
vercel login

# Deploy to production
vercel --prod
```

Set environment variables in the Vercel dashboard under Settings > Environment Variables.
