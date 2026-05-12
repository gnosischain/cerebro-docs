# Contract Explorer

Single-contract inspection surface powered by direct JSON-RPC reads. Resolves a contract's ABI (Sourcify-first, with 4byte fallback for unverified contracts), follows proxies to the implementation, and lets you call any read function from the UI or via tool calls.

- **Resource URI:** `ui://cerebro/contract_explorer`
- **Entry tool:** `open_contract_explorer(address)`
- **Backed by:** `src/cerebro_mcp/tools/contract_explorer.py` + `tools/rpc.py` (`call_view_function`, `abi_resolver`, `web3_client`)

## When to use it

Use Contract Explorer when you have **one contract** and want **current on-chain state**:

- "What's `totalSupply()` / `owner()` / `paused()` on this address right now?"
- "Decode this transaction — what function was called with what arguments?"
- "Is this a proxy? Where's the implementation?"
- "What read functions does this contract even expose?"

For **multi-address sweeps, historical balances, USD-valued holdings, or aggregations**, use the dbt models via `execute_query` instead. Contract Explorer is one RPC round-trip per call; dbt is the right tool for batch and time-series.

## Entry points

| Tool | What it does |
|---|---|
| `open_contract_explorer(address)` | Opens the mini-app panel, resolves ABI, renders function list. |
| `load_contract_explorer_address(address)` | Swap the focused contract in an already-open panel. |
| `contract_explorer_call_function(function_name, args?, block_identifier="latest")` | Execute a read call from the panel context. |

## Standalone RPC tools

These work without the mini-app — same engine, agent-callable directly. See [Tools §7 — On-chain RPC & contract tools](../tools.md#7-on-chain-rpc-contract-tools).

- `contract_explore(address, include_abi=False)`
- `contract_call_function(address, function_name, args?, block_identifier="latest", function_signature?, ...)`
- `contract_decode_transaction_input(address?, tx_hash?, input_data?)`
- `contract_decode_receipt_logs(tx_hash, ...)`

## Typical flow

```text
> Inspect the GNO token contract
agent calls open_contract_explorer(address="0x6810e776880C02933D47DB1b9fc05908e5386b96")
→ panel opens; ABI resolved (Sourcify); function list populated

> What's the current totalSupply?
agent calls contract_explorer_call_function(function_name="totalSupply")
→ Function: totalSupply() (view) | Block: latest | Result: 10000000000000000000000000
```

## ABI resolution

`abi_resolver.resolve_abi` tries, in order:

1. Local ABI catalog (curated contracts).
2. Sourcify by chain ID + address.
3. 4byte selector lookup (synthesizes a minimal ABI from observed function selectors — enough to call known functions, not enough to enumerate full surface).

Proxy detection (EIP-1967 + transparent + minimal-proxy patterns) follows automatically; the resolved record reports the implementation address.

## Limits

- **State-changing functions are rejected at the tool layer.** Only `view` / `pure` calls go through.
- **Non-`latest` blocks need an archive node.** Set `GNOSIS_ARCHIVE_RPC_URL` in `.env`.
- **Overloaded functions:** pass `function_signature="transfer(address,uint256)"` instead of `function_name="transfer"`.

## See also

- [Tools §7 — On-chain RPC & contract tools](../tools.md#7-on-chain-rpc-contract-tools)
- [Portfolio](portfolio.md) — multi-protocol view for a single address (uses dbt, not RPC)
- [Graph Explorer](graph-explorer.md) — cross-sector relationship graph
