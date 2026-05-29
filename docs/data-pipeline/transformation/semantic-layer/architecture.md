# Architecture

## File layout

The semantic layer lives in two places in the `dbt-cerebro` repo:

```
dbt-cerebro/
├── models/                     -- dbt models (sources, staging, int_, fct_, api_)
│   ├── shared/marts/dim_time_spine_{daily,weekly,monthly}.sql
│   ├── revenue/marts/fct_revenue_per_user_{weekly,monthly}.sql
│   ├── execution/gpay/marts/fct_execution_gpay_users_distinct.sql
│   ├── execution/gnosis_app/marts/fct_execution_gnosis_app_users_distinct.sql
│   └── execution/Circles/marts/fct_execution_circles_human_avatars_distinct.sql
│
└── semantic/                   -- authoring + relationships, NOT dbt models
    ├── authoring/
    │   ├── consensus/semantic_models.yml
    │   ├── execution/{cow,gpay,gnosis_app,lending,Circles,...}/semantic_models.yml
    │   ├── revenue/semantic_models.yml
    │   ├── bridges/semantic_models.yml
    │   ├── mixpanel_ga/semantic_models.yml
    │   └── shared/semantic_models.yml
    ├── relationships/
    │   ├── time_spines.yml          -- cross-grain bridges
    │   ├── user_pseudonym.yml       -- cross-sector user joins
    │   ├── execution_graph.yml      -- entity-graph joins (Circles, Safe, validator)
    │   └── execution_transactions.yml
    └── overrides/
        └── defaults.yml             -- metric aliases, docs enrichments
```

The compiled output lives in `target/semantic_registry.json` (one of the
artifacts produced by `dbt run` / `dbt compile` + the post-build script).
The MCP server reads this artifact remotely from GitHub Pages.

## What each piece does

### `models/` — dbt SQL

The actual SQL that materializes data in ClickHouse. **The semantic layer
adds zero SQL** — it only references models that already exist. The
exception is the small set of user-keyed marts and time spines that were
created specifically as cross-sector entry points:

- `dim_time_spine_{daily,weekly,monthly}` — reference time dimensions
- `fct_revenue_per_user_{weekly,monthly}` — pseudonym-keyed per-user
  projections of `int_revenue_fees_{weekly,monthly}_per_user`
- `fct_execution_gpay_users_distinct` — deduped `int_execution_gpay_safe_identities`
- `fct_execution_gnosis_app_users_distinct` — flag-enriched projection of
  `int_execution_gnosis_app_user_identities`
- `fct_execution_circles_human_avatars_distinct` — Human-filtered
  projection of `api_execution_circles_v2_avatar_metadata`

Everything else in `models/` predates the semantic-layer work.

### `semantic/authoring/<module>/semantic_models.yml`

One file per module. Two top-level blocks:

```yaml
semantic_models:
  - name: <model_or_alias>
    model: ref('<dbt_model>')
    entities:
      - name: user_pseudonym       # for cross-sector joins
        type: primary
        expr: toString(user_pseudonym)
    dimensions:
      - name: week
        type: time
        expr: week                 # may include derivations: addDays(week, 1) etc.
        type_params:
          time_granularity: week
      - name: protocol
        type: categorical
        expr: label                # the underlying SQL column
    measures:
      - name: lending_deposits_volume_value    # MUST be globally unique
        agg: sum                                # see `_AGG_TO_CLICKHOUSE` in cerebro-mcp
        expr: deposits_volume_weekly
    config:
      meta:
        cerebro:
          owner: analytics_team
          quality_tier: approved   # approved / candidate / blocked
          grain: week
          question_synonyms:
            - lending deposits weekly
            - aave deposits

metrics:
  - name: lending_deposits_volume_weekly       # the metric ID callers use
    label: Lending Deposits Volume (Weekly)
    description: >
      Sum of weekly deposit volume per (protocol, token).
    type: simple
    type_params:
      measure: lending_deposits_volume_value
    config:
      meta:
        cerebro:
          quality_tier: approved
          grain: week
          owner: analytics_team
          allowed_dimensions: [week, symbol, token_class, protocol]
          supported_time_grains: [week, month]
          question_synonyms:
            - lending deposits weekly
            - aave deposits weekly
```

A few invariants the build enforces (see [maintenance](maintenance.md)):

- **Measure names are globally unique.** Metrics bind to measures **by
  name** — `build_metrics()` builds a `measure_name → [models]` map and a
  metric pointing at a name that exists on more than one semantic_model
  is an `ambiguous_measure_binding` error. This is why uniqueness is
  mandatory the moment you want a metric for a measure, and why
  `scripts/semantic/scaffold_metrics.py` uniquifies collided names to
  `<semantic_model_name>__<measure>` before emitting the ~965
  auto-generated candidate metrics.
- **Metrics resolve deterministically.** `build_metrics()` keys
  `measure_to_models` as a sorted-first dict so the registry is
  reproducible even when an ambiguity exists.
- **A metric's root model must be `semantic_status: approved`** for the
  metric to be executable. Common gotcha: you add a candidate
  semantic_model and an approved metric pointing at it — the metric
  appears in `discover_metrics` but `query_metrics` rejects it.

### `semantic/relationships/*.yml`

Declare cross-sector joins. The MCP planner reads these to find paths
between metric roots. Three kinds in production today:

| File | Axis | Purpose |
| --- | --- | --- |
| `time_spines.yml` | `day` / `week` / `month` | Cross-grain composition. Every weekly mart joins to `dim_time_spine_weekly`. |
| `user_pseudonym.yml` | `user_pseudonym` | Cross-sector user-overlap. 7-node graph (revenue ×2 grains, gpay, gnosis_app, circles, validator withdrawal addresses, + the Safe owner↔contract bridge). |
| `execution_graph.yml` | `circles_avatar`, `safe`, `validator`, ... | Entity-specific joins (Circles trust graph, GP wallet ↔ Safe owner, validator withdrawal address ↔ Safe). |

Relationship shape:

```yaml
relationships:
  - name: revenue_per_user_weekly_to_gpay_identity
    left_model: fct_revenue_per_user_weekly
    right_model: fct_execution_gpay_users_distinct
    left_keys: [user_pseudonym]
    right_keys: [user_pseudonym]
    cardinality: many_to_many
    join_semantics: inner
    via_entity: user_pseudonym
    preferred_bridge: true
    safe_for_dimension_enrichment: true
    aggregate_then_join_only: false
    allow_any_join: false
    quality_tier: approved
```

The fields the planner actually uses:

- `left_model` / `right_model` / `left_keys` / `right_keys` — join condition.
- `via_entity` — the entity axis. Edges sharing a `via_entity` form a
  reachability graph.
- `cardinality` + `join_semantics` — affects which join type the planner
  emits (`INNER` vs `LEFT`).
- `preferred_bridge` — used for cost weighting in
  `find_safest_path` (cerebro-mcp `semantic_graph.py`).
- `quality_tier` — only `approved` relationships are eligible for the
  planner's path search. Lets you stage new joins as `candidate`.

### `target/semantic_registry.json`

The build artifact. Schema:

```jsonc
{
  "metadata": { "manifest_hash": "...", "catalog_hash": "..." },
  "models": {
    "<model_name>": {
      "name": "...",
      "semantic_status": "approved" | "candidate" | "docs_only",
      "dimensions": [...],
      "measures": [...],
      "module": "execution",
      "tags": [...]
    }
  },
  "metrics": {
    "<metric_name>": {
      "measure": "...",
      "root_model": "...",
      "quality_tier": "approved" | "candidate" | "blocked",
      "semantic_status": "approved" | "candidate",
      "allowed_dimensions": [...],
      "supported_time_grains": [...],
      "question_synonyms": [...]
    }
  },
  "relationships": [...],
  "coverage_summary": {...}
}
```

The MCP server reads this whole file at startup and on each refresh
(default poll: 300s; force via `reload_semantic_registry`).

## Build flow

```
                 ┌──────────────────────────────────────┐
                 │   Author writes / edits files in:    │
                 │   models/**/*.sql                    │
                 │   models/**/schema.yml               │
                 │   semantic/authoring/**/*.yml        │
                 │   semantic/relationships/**/*.yml    │
                 └──────────────────────────────────────┘
                                  │
                                  ▼
                 ┌──────────────────────────────────────┐
                 │  dbt run / dbt compile               │
                 │  → target/manifest.json              │
                 │  → target/catalog.json               │
                 │  → target/semantic_manifest.json     │
                 └──────────────────────────────────────┘
                                  │
                                  ▼
                 ┌──────────────────────────────────────┐
                 │  python3 scripts/semantic/           │
                 │    build_registry.py                 │
                 │  → target/semantic_registry.json     │
                 │  → target/semantic_validation_       │
                 │     report.json                      │
                 └──────────────────────────────────────┘
                                  │
                                  ▼
                 ┌──────────────────────────────────────┐
                 │  Publish to GitHub Pages             │
                 │  (https://gnosischain.github.io/     │
                 │   dbt-cerebro/semantic_registry.json)│
                 └──────────────────────────────────────┘
                                  │
                                  ▼
                 ┌──────────────────────────────────────┐
                 │  cerebro-mcp polls every 300s        │
                 │  (or force-refresh via               │
                 │   reload_semantic_registry tool)     │
                 └──────────────────────────────────────┘
                                  │
                                  ▼
                 ┌──────────────────────────────────────┐
                 │  AI agent / dashboard / analyst:     │
                 │  discover_metrics → query_metrics    │
                 └──────────────────────────────────────┘
```

## Validation pass

`build_registry.py --validate` runs all of these checks. Each maps to a
specific error code in `target/semantic_validation_report.json`:

| Error code | Cause | Fix |
| --- | --- | --- |
| `ambiguous_measure_binding` | Two `semantic_models` declare a measure with the same name; the metric pointing at it is non-deterministic. | Rename the measure on the intended source to be unique (convention: `<metric_name>_value`). |
| `missing_measure` | A metric references a measure name that no `semantic_model` declares. | Typo or stale reference. Either remove the metric or add the measure. |
| `metric_missing_root_model` | The measure binding produced no `root_model`. Almost always a downstream effect of `missing_measure` or `ambiguous_measure_binding`. | Fix the underlying measure binding. |
| `unknown_left_model` / `unknown_right_model` | A relationship references a dbt model name not in `target/manifest.json`. | Either build the missing model or fix the typo in the relationship file. |
| `approved_model_missing_measures` | A `semantic_model` tagged `quality_tier: approved` has no `measures:` block. | Either add measures or demote to `candidate`. |
| `allow_any_join_not_approved` (warning) | An `allow_any_join: true` relationship is not `approved`. Joins that collapse duplicates need explicit approval. | Either set `quality_tier: approved` and review the join, or set `allow_any_join: false`. |

The validation is non-fatal by default; CI should run it with `--validate`
and fail the build on errors.

Two validator behaviours are worth knowing because they prevent
false-positive errors against legitimate authoring:

- **Graph-meta column names are matched with ClickHouse quoting
  stripped.** A `graph.source_column: '`from`'` (back-ticked because
  `from` / `to` are reserved words and are interpolated verbatim into
  generated SQL) is validated against the catalog's bare `from` column —
  the validator strips back-ticks before the membership check, so quoted
  identifiers don't trip `graph_meta_unknown_column`.
- **Snapshot / no-time-dimension models are exempt from the `grain`
  requirement.** `REQUIRED_APPROVED_META` normally requires `grain`, but
  a semantic_model with no `type: time` dimension (e.g. a
  point-in-time `*_latest` snapshot) cannot have a meaningful grain, so
  `grain` is dropped from the required set for those models rather than
  emitting `missing_required_approved_meta`.

## Where the planner code lives

Bug fixes and feature work for the planner happen in the **`cerebro-mcp`**
repo (separate from `dbt-cerebro`). Key files:

- `src/cerebro_mcp/semantic_sql_compiler.py` — emits ClickHouse SQL from
  the metric plan. The `_AGG_TO_CLICKHOUSE` map lives here (translates
  `count_distinct` → `uniqExact`, etc.).
- `src/cerebro_mcp/semantic_planner.py` — resolves dimension bindings,
  including the time-spine upcast (`_try_time_spine_upcast`).
- `src/cerebro_mcp/semantic_graph.py` — builds the reachability graph
  from relationships and runs `find_safest_path`.
- `src/cerebro_mcp/semantic_loader.py` — registry refresh, ETag-based
  poll, and the force-reload path used by `reload_semantic_registry`.
- `src/cerebro_mcp/tools/semantic.py` — the MCP-tool surface
  (`discover_metrics`, `query_metrics`, `explain_metric_query`,
  `reload_semantic_registry`).

Changes to the planner or the SQL compiler should land as small PRs with
unit-test coverage (see `tests/test_semantic_*.py` in cerebro-mcp).
