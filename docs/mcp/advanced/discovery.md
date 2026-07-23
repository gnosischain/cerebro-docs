# Finding Tools: find, list, and Lean Core

With 190+ tools registered, "which tool do I use?" is itself a routing problem. Cerebro solves it with three mechanisms: a single semantic front door (`find`), a unified listing tool (`list`), and an opt-in lean-core surface that trims what is *advertised* without changing what is *callable*.

## `find` — the single front door

`find(query, mode="auto", limit=8)` (in `src/cerebro_mcp/tools/semantic/find.py`; registered when `SEMANTIC_ENABLED=true`) answers "what do I use for X?" in one call. It ranks, in one payload:

- **`top_tools`** — BM25 over the whole registered-tool corpus (names, docstring first lines, domains, tags), with `app_only` hydration tools excluded and actionable tools pinned first;
- **`top_metrics`** — approved semantic metrics from the same routing core `preflight_analytics_request` uses (near-miss queries surface their closest metrics flagged `low_confidence` instead of a dead end);
- **`top_models`** — dbt model hits via the shared catalog index;
- **`recommended_action`** — the contract that makes `find` useful: a concrete next tool with **pre-filled args** and a one-line `why`, e.g. `{"tool": "query_metrics", "call": "query_metrics(metrics=['gnosis_pay_active_users'])", …}`.

The recommended action is mode-aware:

| Mode | Behaviour |
|---|---|
| `answer` (default) | Points straight at `query_metrics` when an approved metric covers the question — **no preflight needed**. Falls back to `discover_models` → `describe_table` → `execute_query` on a coverage gap. |
| `chart` / `report` | Routes through `preflight_analytics_request` first, so the chart/report hard gate is respected. |
| `auto` | Conservative intent inference — defaults to `answer` unless the query clearly asks for a chart or report. |

An answer-mode `find` records `semantic_find_ran` (unblocking raw discovery) but deliberately does **not** set `semantic_preflight_ran` — it can never open the chart/report gates by accident. The tool corpus is built lazily on first call and rebuilt whenever the registered-tool set changes, so dynamically registered tools are searchable too.

## `list` — one listing front door

`list(kind=...)` (in `src/cerebro_mcp/tools/analytics/list_unifier.py`) dispatches to the same helpers the legacy per-kind tools call, so output is byte-identical:

| `kind` | Replaces | Extra args |
|---|---|---|
| `"tables"` | `list_tables` | `database` (default `dbt`), `name_pattern` / `like`, `page_size`, `page_token`, `include_detailed_columns` |
| `"databases"` | `list_databases` | — |
| `"charts"` | `list_charts` | — |
| `"reports"` | `list_reports` | `limit` (default 20) |
| `"saved_queries"` | `list_saved_queries` | — |

The five legacy `list_*` tools remain registered and callable during the deprecation window; both they and `list` are classified `tier="advanced"`, so they vanish from the advertised list under lean core while staying invocable.

## Lean core and `load_tools`

When `LEAN_CORE_ENABLED=true`, the model-facing tool list is trimmed to the **~18-tool core surface** — `CORE_TOOL_NAMES` in `src/cerebro_mcp/tools/tool_meta.py`: `find`, `query_metrics`, `execute_query`, `describe_table`, `get_model_details`, `get_metric_details`, `explain_metric_query`, `preflight_analytics_request`, `quick_chart`, `quick_metric_chart`, `generate_chart`, `generate_charts`, `generate_metric_charts`, `generate_report`, `get_help`, `system_status`, `verify_numbers`, plus the escape hatch `load_tools`.

Everything else stays **registered and callable by name** — only the advertised list shrinks. `load_tools(names)` un-hides named advanced tools and best-effort emits `notifications/tools/list_changed` so the client refetches. Two caveats from the implementation: the un-hide is process-global (not per-session), and the list-changed notification is best-effort — if a tool doesn't reappear in the list, it is still directly callable.

## The TOOL_META model

Every static tool carries a compact descriptor in `tools/tool_meta.py` — this is what `find`'s ranking and the lean-core filter run on:

- **`domain`** — a coarse grouping (`discovery`, `semantic`, `schema`, `query`, `visualization`, `reporting`, `web3`, `governance`, `research`, `storyteller`, `meta`), inferred from the name or risk registry when not explicit;
- **`tier`** — `core` (an everyday entry point, gently boosted in `find` and kept visible under lean core) or `advanced` (the long tail; the default);
- **`tags`** — free-text search terms BM25 wouldn't get from the name alone, falling back to the docstring's first line.

Dynamic custom tools are auto-classified and exempt from the coverage lint; a *static* tool missing both a `TOOL_META` entry and a risk-registry entry fails a hard lint, so the metadata cannot silently rot.

## See also

- [Available Tools](../tools.md) — the categorised reference this machinery navigates
- [Semantic Metrics](semantic-metrics.md) — the metric registry `find` routes into
- [Setup — Feature flags](../setup.md#feature-flags) — `SEMANTIC_ENABLED`, `LEAN_CORE_ENABLED`
