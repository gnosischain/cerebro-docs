# Hybrid Search

How `search_models`, `discover_models`, and `get_relevant_columns` rank dbt models and columns.

## What it is

Cerebro replaces naive token-overlap search with a hybrid ranker:

1. **BM25** over an enriched per-model blob (name + description + tags + owner + column names + column descriptions + path tokens + `meta.inference_notes`).
2. **Token-overlap** legacy ranker (substring counting, hand-tuned tie-breakers).
3. **Reciprocal Rank Fusion (RRF)** combines both rankings: items ranked highly by both rise to the top.

A separate **Column BM25 index** ranks columns within a single model — this is what powers column-scoped schema injection on wide tables.

A **networkx DAG** of model + source nodes provides deterministic lineage: `get_upstream_lineage`, `get_downstream_impact`.

All deterministic. No embeddings, no model loading. Builds in <100ms on the live ~862-model manifest.

## When it matters

- Every `search_models` call uses this transparently.
- `get_relevant_columns(model, query, top_k)` ranks columns by BM25 against the query and always includes join keys + time grains.
- Column-scoped schema injection (`schema_context.py`) keeps prompts compact on wide tables (100+ columns) without losing the columns the SQL actually needs.

## Measured outcomes

On the live manifest (862 models / 75 sources / 5,136 column docs):

| Metric | Hybrid | Legacy | Δ |
|---|---|---|---|
| `search_models` median latency | 2.3 ms | 1.4 ms | +0.9 ms |
| `hit@1` (12-query eval) | **4/12 (33%)** | 1/12 (8%) | **+25 pp** |
| `hit@3` | **9/12 (75%)** | 5/12 (42%) | **+33 pp** |
| `hit@5` | **11/12 (92%)** | 10/12 (83%) | +9 pp |
| Lineage query latency | 14 µs median | n/a | — |
| Memory total | ~7 MB | ~4 MB | +3 MB |

The +0.9 ms search overhead is well below typical MCP serialization overhead. `hit@1` improved 4× absolute.

## Why it improved

1. **Distinctive name tokens dominate.** BM25 weights rare tokens (high IDF) — a model whose **name** contains the query terms gets a strong signal that token-overlap counts the same as any other match.
2. **Column descriptions add direct query→data signal.** A model with a column `effective_balance` matches `"validator balance"` even if its description is generic.

## Column-scoped schema injection

`schema_context.py` produces a markdown schema block per model:

1. Tables narrower than `SQL_COMPILER_FULL_SCHEMA_THRESHOLD` (default 30) → inject every column.
2. Wider tables → BM25-rank columns against the query, keep top-K + an allowlist of join keys / partition columns / time grains (`_ALWAYS_KEEP_NAMES`).
3. **Anaemic floor**: if BM25 + always-keep < `top_k`, pad with the first K columns so an off-topic query against a wide staging table still gets a usable schema.
4. The block ends with a comment naming the omitted columns and how to request them via `get_relevant_columns`.

## Configuration

| Variable | Default | Description |
|---|---|---|
| `SQL_COMPILER_FULL_SCHEMA_THRESHOLD` | 30 | Below this column count, full schema is injected |
| `SQL_COMPILER_TOP_COLUMNS` | 20 | Cap for wide-table scoping |

## Tools that use this transparently

| Tool | What hybrid search does |
|---|---|
| `search_models` | Returns BM25+overlap fused ranking |
| `discover_models` | Same, with filters applied first |
| `get_relevant_columns` | Column BM25, plus join-key allowlist |
| `get_model_details` | No ranking; uses lineage walk |
| `get_upstream_lineage` / `get_downstream_impact` | networkx ancestors / descendants |
| `preflight_analytics_request` | Search + lineage to gate the request |

## Known residual failure modes

- `dex pool fees` — column descriptions mentioning "fees" or "pool" promote unrelated models. Classic length-norm vs recall trade-off; deferred fix is multi-field BM25.
- `*_latest` vs `*_dist_*` snapshot models competing with `_daily` time-series models. Deferred fix is a name-pattern boost layer.

## Best practices

- **Query for what you want to know, not what you think the table is called.** "validator withdrawals last 30d" beats "consensus_layer_withdrawals_table".
- **Don't stop at first match.** The dispatcher names model tiers but the catalog has more — see [Quality Gates](quality-gates.md#9-discovered_model_coverage).
- **Use `get_relevant_columns(model, query)` for wide tables** before writing SQL — keeps the prompt compact without losing the right columns.

## See also

- [Tools §1](../tools.md#1-discovery-schema)
- [Quality Gates](quality-gates.md) — `discovered_model_coverage` enforces that you actually used the search results
- [Phase 1 design doc (cerebro-mcp repo)](https://github.com/gnosischain/cerebro-mcp/blob/main/docs/phase1_hybrid_search.md) — full sprint write-up
