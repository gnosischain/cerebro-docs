# CoW Explorer

Read-only analyst surface over the `cow_db` ClickHouse database: CoW Protocol fills, execution and reference prices, observed order lifecycles and known open intents, settled solver competitions, and entity drill-downs across ten production networks plus Sepolia.

- **Resource URI:** `ui://cerebro/cow_explorer`
- **Entry tool:** `open_cow_explorer(...)`
- **Backed by:** `src/cerebro_mcp/tools/visualization/cow_explorer.py`, reading `cow_db` (populated by the standalone [cow-indexer](../../data-pipeline/ingestion/cow-indexer.md) service)

## What it is

CoW Explorer is a sectioned dashboard over indexed CoW Protocol data. Nine sections cover the protocol at different altitudes:

| Section | Focus |
|---|---|
| `overview` | Coverage matrix, network activity, protocol KPIs, chain share |
| `markets` | Pair-scoped candles, reference prices, book depth, depth heatmap, trade tape |
| `trades` | Settled fill activity and per-fill tape |
| `orders` | Observed order lifecycle, known intents, execution quality, order classes (incl. ComposableCoW / TWAP) |
| `auctions` | Indexed settled competitions |
| `solvers` | Competition statistics, rankings, execution flow, solver directory |
| `traders` | Leaderboard, activity, 12-month growth accounting and cohort retention |
| `patterns` | Solver-pair matrix, trader-solver affinity, fee-policy and quote-delta quality |
| `live` | Indexing pulse plus 1-hour-bounded trade / settlement / intent feeds |

Every dataset discloses its indexed time window and coverage basis; the app never claims a complete live book.

### Three data planes, deliberately kept apart

The app intentionally distinguishes three kinds of data that are easy to conflate:

1. **Settled on-chain execution** — trades and settlements with block timestamps ("Settled fills", "Execution prices"). This is what actually happened on-chain, bounded by the indexer checkpoint.
2. **Auction and native reference prices** — competition reference prices and native-price API observations ("observed series"). These are pricing context, not executions.
3. **The indexer's observed open-order snapshot** — order lifecycles and "known open intents" ("observed snapshot"), keyed by creation date and observation time.

!!! warning "Open orders are observation-based, not authoritative"
    Order-lifecycle and open-intent datasets reflect what the indexer has *observed* of the off-chain order flow — labelled "Known open intents (observed snapshot)" in the app. They are not an authoritative view of the CoW order book: an order the indexer never saw simply is not there, and statuses lag the observation time. Settled execution data is the only plane that is on-chain ground truth.

### Outbound links and icons

- **Block-explorer links are outbound only.** Every chain carries an explorer config (Blockscout on most chains; BscScan, Avalanche Explorer, and Plasmascan where applicable) used purely to build `tx` / `address` / `token` links out of the app. No explorer API is queried.
- **Token icons via CoinGecko are optional and cached.** `load_cow_explorer_icon` overlays token imagery from the CoinGecko token lists (30-minute in-process cache, HTTPS-only image hosts). The overlay never blocks on the network — it returns whatever is cached and flags `icon_overlay_pending` when background fetches are still filling in. Missing icons degrade to client-side monograms.

## When to use it

- Historical CoW fills, prices, or volumes on any indexed network.
- "What is waiting to execute right now?" — with the observation caveat above.
- Solver analysis: competition win rates, ranking distributions, score gaps.
- Order-flow quality: surplus vs limit, creation-to-fill latency, fee policies.
- Drill-downs on a specific order UID, transaction hash, address, token, auction, or solver.

For general-purpose analytics over dbt models, use `find` / `query_metrics` instead — this app is scoped to `cow_db`.

## How to open it

```text
open_cow_explorer()                                   # all-networks overview
open_cow_explorer(section="markets", chain_id=100)    # Gnosis markets
open_cow_explorer(section="live")                     # live pulse + feeds
open_cow_explorer(query="0x…")                        # resolve an entity by id
open_cow_explorer(entity_type="solver", identifier="0x…", chain_id=1)
```

Key parameters of the entry tool:

- `environment_scope` — `"production"` (default) or `"testnet"`.
- `chain_id` — `0` selects the all-networks rollup where the section supports it (`overview`, `trades`, `solvers`, `traders`, `auctions`, `orders`, `live`); other sections coerce to a concrete chain with an explicit warning.
- `section` — one of the nine sections above (default `overview`).
- `query` — free-form entity search (order UID, tx hash, address, token, auction id, solver). A single match deep-links straight into the entity page; multiple matches render a candidate list.
- `base_token` / `quote_token` — pair seed for the markets section (must be provided together).
- `interval` — candle bucket: `5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `12h`, `1d`, `1w`.
- `window_days`, `start_at`, `end_at` — time range seed (per-section defaults range from 1 day for `live` to 30 days for most sections).
- `entity_type` + `identifier` — direct entity load, bypassing search (`order`, `transaction`, `address`, `token`, `auction`, `solver`).

The open path runs **zero ClickHouse queries**: the frontend applies the section's `core` dataset group and then streams every other group through `load_cow_explorer_datasets`, which is what keeps opening and section switches fast.

## Tool reference

`open_cow_explorer` is the only agent-visible tool. The other five are registered with `APP_ONLY_META` and marked `app_only` — the React frontend calls them; the agent never should (and hosted deployments hide them from the model-facing tool list).

### Entry point (agent-visible)

| Tool | Purpose | Key parameters |
|---|---|---|
| `open_cow_explorer` | Open the explorer on a section, search result, or entity | `environment_scope`, `chain_id`, `section`, `query`, `base_token`, `quote_token`, `interval`, `window_days`, `start_at`, `end_at`, `entity_type`, `identifier` |

### App-internal loaders

| Tool | Purpose | Key parameters |
|---|---|---|
| `load_cow_explorer_section` | Atomically load one section with its filter scope | `view_id`, `request_id`, `section`, plus scope filters (`chain_id`, pair, interval, range, `status`, `owner`, `solver`, `token`, `force_refresh`) |
| `search_cow_explorer` | Resolve an order, transaction, address, auction, or token | `view_id`, `request_id`, `query`, `chain_id` |
| `load_cow_entity` | Load a resolved entity bundle | `view_id`, `request_id`, `entity_type`, `identifier`, `chain_id` |
| `load_cow_explorer_datasets` | Load one deferred dataset group (additive) | `view_id`, `request_id`, `section`, `group`, `scope_id`, `force_refresh`, `depth_at` (`""` / `"live"` / ISO timestamp for book reconstruction), `heatmap_window` (`"24h"` / `"7d"` / `"all"`) |
| `load_cow_icon_overlay` | Overlay cached CoinGecko token icons for visible tokens | `view_id`, `request_id` |

## Best practices

- **Start at `chain_id=0`** for cross-network questions — overview, trades, solvers, traders, auctions, orders, and live all support the all-networks rollup.
- **Trust the coverage labels.** Each dataset carries its basis (`block_timestamp`, `observed_at`, `creation_date`, auction block time) and coverage mode; when comparing planes (e.g. execution price vs auction reference price), say which plane a number comes from.
- **Use entity deep-links** (`entity_type` + `identifier`) when you already hold an id — it skips the search round trip.

## Pitfalls

- **Treating known intents as the order book.** They are the observed snapshot (see the warning above), not a complete live book.
- **BNB Chain time series.** Indexed BNB Chain trades carry no block timestamps, so time-bounded views silently exclude them; the app surfaces this as a chain data note. Use entity lookups (ordered by block number) or all-history aggregates there.
- **Expecting live feeds to reach back.** The `live` section is hard-bounded to the last hour by design; use `trades` / `orders` for anything older.
- **Row caps.** Tape-style datasets cap at 10,000 rows; narrow the window or pair instead of paging expectations.

## See also

- [Mini-Apps overview](index.md)
- [CoW Indexer](../../data-pipeline/ingestion/cow-indexer.md) — the standalone service that populates `cow_db`
- [Governance Explorer](governance.md) — sibling read-only explorer over `governance_db`
