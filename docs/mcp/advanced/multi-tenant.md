# Multi-Tenant

How Cerebro stamps every workflow with a SHA-256 hash of the calling identity, and what that does and doesn't give you.

## What it is

Every workflow row in `~/.cerebro/cerebro_state.db` has an optional `owner TEXT` column populated with a SHA-256 hash of the caller's identifier. Plaintext identifiers never persist — the contextvar holds only the hex digest.

```text
CEREBRO_OWNER          = "alice@gnosis.io"
CEREBRO_OWNER_HASH_SALT = "rotate-quarterly-2026Q2"
→ owner_hash           = "9f4a3c…e21c"   (32-byte hex)
```

This adds **separation** (your `list_resumable_workflows` returns only your workflows). It is **not** authorization on its own.

## When it matters

- Multi-human SSE deployments where you want each user to see only their own work.
- Audit logs: forensic correlation by deployment without exposing real emails.
- Compliance: rotating the salt is a hard tenant reset — old workflows become unreachable.

For single-user stdio deployments, identity is irrelevant — the env var is unused or set as a constant.

## Sources of identity

| Transport | Source | When set |
|---|---|---|
| stdio | `CEREBRO_OWNER` env var | Once at server boot, in `server.py:main()` |
| SSE | `X-Cerebro-Owner` HTTP header | Per request, in `BearerAuthMiddleware.__call__` (try/finally with `Token.reset()`) |

If neither is set, the contextvar stays `None`, all workflows write `owner=NULL`, and the read filter treats NULL as legacy / visible to everyone (single-tenant fallback).

## Optional salt

Set `CEREBRO_OWNER_HASH_SALT` to make hashes deployment-specific — useful if you ever share or back up `cerebro_state.db` and don't want hashes cross-referenceable against a known list of emails.

Salt rotation is a **hard tenant reset**: existing hashes were salted with the old value, so they no longer match the new value. Old workflows become invisible to their original owners. Use it only after a credential leak or compliance event.

## How filters work

`EventStore.list_workflows(owner=, include_unowned=True)` builds:

```sql
WHERE (owner = ? OR (include_unowned AND owner IS NULL))
```

So a caller with hash `H` sees:

- Their own workflows (where `owner = H`)
- Plus any `NULL`-owned workflows (legacy)

Pass `include_unowned=False` to enforce strict isolation (no NULL fall-through).

`get_workflow(workflow_id, requesting_owner=H)` returns `None` for rows owned by anyone other than `H` (or NULL). "Not yours" is treated the same as "not found" so callers don't have to distinguish.

## Trust model

The identity is **self-attested unless an upstream auth proxy verifies it**. Cerebro doesn't validate the header — that's the proxy's job.

| Deployment shape | Multi-tenant safe? |
|---|---|
| Single-user stdio | n/a (one user) |
| Single-token shared SSE | **no** — anyone with the token can claim any owner |
| Per-user JWTs validated upstream | yes, if the proxy enforces claim-to-header binding |
| stdio with multiple users sharing the OS account | **no** — env var is a constant |

For real authorization, validate JWT claims in middleware before the request hits Cerebro.

## Setup recipes

### Local stdio (single user)

```json
{
  "mcpServers": {
    "cerebro": {
      "command": "cerebro-mcp",
      "env": {
        "CEREBRO_OWNER": "alice@gnosis.io",
        "CEREBRO_OWNER_HASH_SALT": "rotate-me-quarterly",
        "CLICKHOUSE_PASSWORD": "..."
      }
    }
  }
}
```

### SSE with per-user identity

Cerebro side:

```bash
cerebro-mcp --sse
# expects MCP_AUTH_TOKEN to be set
```

Client config (each user sends their own header):

```json
{
  "mcpServers": {
    "cerebro": {
      "url": "https://mcp.analytics.gnosis.io/sse",
      "headers": {
        "Authorization": "Bearer <shared-token>",
        "X-Cerebro-Owner": "alice@gnosis.io"
      }
    }
  }
}
```

For real isolation, deploy an auth proxy (e.g. Pomerium / oauth2-proxy) that validates the user's identity, then injects the verified email as `X-Cerebro-Owner` and strips any client-supplied value.

## Audit query: owner distribution

```bash
sqlite3 ~/.cerebro/cerebro_state.db \
  "SELECT substr(owner, 1, 12) AS owner_prefix, count(*)
   FROM workflows GROUP BY owner_prefix ORDER BY 2 DESC"
```

```text
owner_prefix  count
9f4a3ce21c    142
NULL           18
b7d8f0c11a     67
```

`NULL` rows are legacy or single-tenant fallback writes — they're visible to everyone.

## Best practices

- **Set both `CEREBRO_OWNER` and `CEREBRO_OWNER_HASH_SALT`** in any deployment that has more than one human. Forgetting the salt means hashes are reversible against any known email list.
- **Document salt rotation policy** if you adopt one. Rotating without a plan is a tenant reset, not a security maintenance.
- **Don't conflate this layer with authorization.** It's separation, not auth. Add JWT validation upstream for real authz.

## Pitfalls

- **Trying to share a workflow across owners.** No re-owning tool exists today; cross-tenant access is blocked by design.
- **Backing up `cerebro_state.db` without a salt.** Means anyone with the backup can recompute owner hashes from a list of suspected emails.
- **Rotating the salt mid-project.** All in-flight workflows become invisible — destructive. Always plan a hand-off period.

## See also

- [Memory & Resume](memory-and-resume.md) — schema + read filters
- [Security & Audit](../security.md) — overlap with the audit log
- [Setup](../setup.md) — env-var configuration
