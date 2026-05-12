# Mini-Apps

Interactive React + ECharts mini-apps that render inline in any MCP-aware host (Claude Desktop, Claude Code, custom hosts). Each is a single-file HTML bundle served by the MCP server over a `ui://cerebro/<app>` resource URI.

## Apps at a glance

| App | Resource URI | Entry tool | Purpose |
|---|---|---|---|
| [Portfolio](portfolio.md) | `ui://cerebro/portfolio` | `open_portfolio` | Address-centric view across Circles / GPay / Safe / DeFi |
| [Graph Explorer](graph-explorer.md) | `ui://cerebro/graph_explorer` | `open_graph_explorer` | Cross-sector force graph |
| [Metric Lab](metric-lab.md) | `ui://cerebro/metric_lab` | `open_metric_lab*` | Build a metric from SQL or the semantic registry |
| [Contract Explorer](contract-explorer.md) | `ui://cerebro/contract_explorer` | `open_contract_explorer` | Inspect any EVM contract via RPC: ABI, read calls, decoded txs |

The Report Renderer (`ui://cerebro/report`, entry `generate_report`) shares the same plumbing — covered on the [Reports](../reports.md) page.

## Shared plumbing

All mini-apps follow the same protocol:

1. The entry tool returns a `MiniAppPayload` of type `INITIAL_LOAD` with `view_state` and one or more `datasets`.
2. The frontend reads it via `useMiniApp` and calls back to the MCP host with `callServerTool` (e.g. `expand_graph_explorer_node`).
3. Subsequent tool calls return `PATCH_VIEW_STATE` payloads that the UI merges in place.
4. Hidden hydration tools (`get_mini_app_rows`, `get_mini_app_state`) are callable only by the frontend (classified `app_only` — see [Security](../security.md)).

```mermaid
flowchart LR
  Agent -- "open_*" --> MCP
  MCP -- INITIAL_LOAD --> UI
  UI -- "callServerTool(expand_*)" --> MCP
  MCP -- PATCH_VIEW_STATE --> UI
```

## Launching a mini-app

In any MCP-aware host:

```text
> Open the portfolio for 0xabc…
agent calls open_portfolio(address="0xabc…")
→ panel renders inline
```

For terminal-only hosts, the mini-app opens in the default browser.

## See also

- [Tools](../tools.md#6-mini-apps-live-ui-surfaces) — full tool reference
- [Portfolio](portfolio.md), [Graph Explorer](graph-explorer.md), [Metric Lab](metric-lab.md), [Contract Explorer](contract-explorer.md)
- [Reports](../reports.md) — the Report Renderer mini-app
