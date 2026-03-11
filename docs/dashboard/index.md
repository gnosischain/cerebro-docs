# Metrics Dashboard

The Gnosis Metrics Dashboard is a web application that visualizes on-chain analytics from the Gnosis Chain ClickHouse data warehouse. Built with React 19, ECharts 5.6, Tailwind CSS 4, and shadcn/ui components, it provides a YAML-driven, config-first architecture deployed on Vercel with serverless API functions and server-side caching.

**Live instance**: [metrics.gnosischain.com](https://metrics.gnosischain.com)

## Architecture

The dashboard follows a three-layer architecture:

```
+---------------------------+
|    Frontend (React 19)    |
|    Vite + ECharts + CSS   |
|    YAML-driven layouts    |
+-------------+-------------+
              |
              | /api/metrics/:id
              |
+-------------v-------------+
|  Vercel Serverless API    |
|  File-based cache (/tmp)  |
|  In-memory fallback       |
+-------------+-------------+
              |
              | ClickHouse HTTP
              |
+-------------v-------------+
|  ClickHouse Cloud         |
|  dbt models + raw tables  |
+---------------------------+
```

### Frontend

The React application resolves its layout from YAML configuration files:

1. `public/dashboard.yml` defines the top-level sector index (ordering, icons, palette)
2. `public/dashboards/<sector>.yml` defines the metric grid layout for each sector
3. `src/queries/*.js` files contain metric definitions (SQL queries, chart options, formatting)

At render time, YAML layout entries are merged with metric definitions to produce fully configured chart widgets.

### API Proxy

Vercel serverless functions handle ClickHouse communication:

- Credentials are kept server-side and never exposed to the frontend
- Queries are executed via the ClickHouse HTTP interface
- Results are cached to minimize database load

### Caching System

A two-tier caching system reduces ClickHouse query volume:

| Tier | Mechanism | Scope |
|------|-----------|-------|
| Primary | File-based cache in `/tmp` | Vercel function filesystem |
| Fallback | In-memory cache | Within a single function invocation |

Cache entries have a configurable TTL (default: 24 hours) and are automatically refreshed daily. If ClickHouse is unreachable, the system serves stale cached data rather than failing.

## Features

### Theme Support

The dashboard supports light and dark themes with a toggle in the header. Theme state persists across page reloads. Chart colors and UI elements adapt automatically.

### Metric Search

The header includes a search bar with fuzzy matching against all metrics placed in the YAML configuration. Search results link directly to the relevant dashboard and tab.

- Highest priority: metric name exact/prefix/token matches
- Then: metric ID token matches
- Then: tab, dashboard, and description context matches
- Light typo tolerance (edit distance 1 for longer tokens)
- Maximum 8 results for clarity

### Responsive Grid

Metric widgets are placed in a CSS Grid layout defined by YAML properties (`gridRow`, `gridColumn`, `minHeight`). The grid adapts to viewport width for mobile and tablet breakpoints.

### Chart Controls

Each chart card provides three controls:

| Control | Function |
|---------|----------|
| Info popover | Displays metric description and methodology notes |
| PNG download | Exports the chart as a PNG image |
| Expand modal | Opens the chart in a full-screen modal for detailed inspection |

### Palette System

Dashboards can specify a named color palette in YAML. The palette applies to all charts within that dashboard sector, with metric-level color overrides taking precedence. If a palette has fewer colors than required series, additional colors are sourced from the `standard` fallback palette.

## Technology Stack

| Component | Technology |
|-----------|------------|
| Framework | React 19 |
| Build tool | Vite |
| Charting | ECharts 5.6 |
| UI components | shadcn/ui (Radix primitives) |
| Styling | Tailwind CSS 4 |
| Deployment | Vercel (serverless functions + static hosting) |
| Database | ClickHouse Cloud |
| Configuration | YAML |

## Next Steps

- [Sectors](sectors.md) -- Overview of all 9 dashboard sectors and their metrics
- [Configuration](configuration.md) -- How to add metrics, sectors, and configure caching
