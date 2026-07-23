# MMM (Marketing Mix) Module

<!-- BEGIN AUTO-GENERATED: models-mmm -->
<!-- generated: 2026-07-23 -->
**Mmm**

| Model | Layer | Description |
|-------|-------|-------------|
| `int_execution_mmm_controls_weekly` | Intermediate | Long-form weekly MMM control variables (macro / seasonality /
operational signals the regression conditions on but do... |
| `int_execution_mmm_kpis_weekly` | Intermediate | Long-form weekly KPI registry for the Marketing Mix Modeling (MMM)
pipeline. One row per (`week`, `kpi_name`) on a co... |
| `int_execution_mmm_media_weekly` | Intermediate | Long-form weekly MMM media (incentive / reward / outlay) registry.
One row per (`week`, `media_name`) on the same con... |
| `fct_execution_mmm_baseline_latest` | Fact | Per-(KPI, media) baseline KPI: the median KPI value during weeks
where the media's adstocked spend sits in the bottom... |
| `fct_execution_mmm_collinearity_latest` | Fact | Pairwise Pearson correlation matrix between MMM media columns
computed over the last 730 days of `fct_execution_mmm_s... |
| `fct_execution_mmm_spine_weekly` | Fact | MMM weekly spine — wide pivot of `int_execution_mmm_kpis_weekly`,
`int_execution_mmm_media_weekly`, and `int_executio... |
| `api_execution_mmm_spine_weekly` | API | API view passthrough over `fct_execution_mmm_spine_weekly`. Tier1
endpoint (`api:mmm_spine_weekly`), requires `X-API-... |

<!-- END AUTO-GENERATED: models-mmm -->
