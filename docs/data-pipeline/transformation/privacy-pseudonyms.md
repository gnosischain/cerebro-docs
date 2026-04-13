# Privacy & Pseudonyms

dbt-cerebro models combine public on-chain data with Mixpanel product analytics. Both sides contain identifiers that can be used to link a real person across domains: wallet addresses on-chain, `distinct_id` (often a wallet address) in Mixpanel. This page explains how cross-domain joins are implemented so we never materialize a raw wallet address in a queryable table, while still allowing analytics like "how many Mixpanel users also own a Gnosis Pay Safe?".

## Threat model

The problem we are solving is **rainbow-table reversibility of on-chain identifiers**.

Every wallet address on Gnosis Chain is public. Anyone with a warehouse read role can iterate the address space, compute `H(addr)` for any function `H`, and recover the original address from its hash. A plain `sipHash64(distinct_id)` therefore provides no real privacy if `distinct_id` is a wallet, because an attacker can pre-compute `sipHash64` over every known address and reverse the mapping. The hash function must be **keyed** with a secret salt that the attacker does not have, otherwise the rainbow-table attack is trivial.

What we want:

- Cross-domain joins must still work: a Mixpanel row for `distinct_id = 0xabc…` must be joinable to an on-chain row for the same `0xabc…`.
- Raw addresses must never appear in any materialized column that warehouse readers can query.
- The join must be deterministic across runs: the same address must produce the same pseudonym every time, forever.
- Rotating the pseudonym space must be possible (breaks continuity but unlinks historical data) and forbidden (breaks continuity and everything that depended on it) — both at the same time. In practice: possible, but we never do it.

## The `pseudonymize_address` macro

`macros/pseudonymize_address.sql` is the single entry point. Every model that stores or joins on a pseudonymized address uses this macro — there are no bespoke hash calls anywhere else in the repo.

```jinja
{% macro pseudonymize_address(addr_expr) %}
    sipHash64(concat(unhex('{{ env_var("CEREBRO_PII_SALT") }}'), lower({{ addr_expr }})))
{% endmacro %}
```

Three things to notice:

1. **`env_var("CEREBRO_PII_SALT")` has no default.** If the env var is unset, `dbt parse` fails loudly. A silent fallback to an empty salt would re-introduce the rainbow-table problem this macro exists to prevent.
2. **The salt is hex-decoded via `unhex(...)` inside ClickHouse.** This is not decorative — it is the result of a debugging session where the original string salt contained a literal `'` byte that broke the SQL string literal. Hex encoding guarantees the rendered SQL only contains `[0-9a-fA-F]`, making any byte sequence safe.
3. **The input is lowercased before hashing.** On-chain addresses appear in mixed case (EIP-55 checksummed) in some sources and lowercase in others. Lowercasing makes the hash insensitive to the representation, so the same wallet always produces the same pseudonym regardless of which side of the join normalizes the address.

The output is `UInt64`. That matches the `user_id_hash` column type in `stg_mixpanel_ga__events`, so the join is a cheap 8-byte equality compare.

## The salt contract

The salt is not configuration — it is a permanent, warehouse-wide secret. Rotating it invalidates every pseudonym already stored and breaks every cross-domain join that assumes continuity.

Rules for operators:

- **Format:** hex-encoded string, even length, `[0-9a-fA-F]` only. Generate with `openssl rand -hex 32` for 32 bytes of entropy (64 hex chars).
- **Storage:** the orchestrator's environment (dbt CI, local shell, cron container). Never committed to the repo. Never printed in logs.
- **Lifetime:** permanent. Once a production `dbt run` has written rows using a given salt, that salt is frozen. Rotating it would orphan every pseudonym already in the warehouse.
- **Loss handling:** if the salt is lost, every pseudonymized column is effectively undecipherable and non-joinable. There is no recovery — you would have to choose a new salt and full-refresh every model that uses `pseudonymize_address`.

The contract is enforced structurally:

| Constraint | Enforcement |
|---|---|
| Must be set | `env_var(..., no default)` → `dbt parse` fails |
| Must be hex | `unhex(...)` inside ClickHouse → runtime error on non-hex input |
| Must not be empty | A zero-byte salt makes the hash trivially reversible — guard at set time, not at macro time |

## How a cross-domain join actually works

Take the Gnosis Pay → Mixpanel bridge as the canonical example.

On the Mixpanel side, every row in `stg_mixpanel_ga__events` already has `user_id_hash`, which is `pseudonymize_address(distinct_id)` applied at ingestion. The raw `distinct_id` is never projected to the downstream table.

On the on-chain side, we pseudonymize the GP Safe's initial owners, spender delegates, and the Safe address itself, storing only the pseudonyms:

```sql
-- models/execution/gpay/intermediate/int_execution_gpay_safe_identities.sql
SELECT
    oe.safe_address                        AS gp_safe,
    'initial_owner'                        AS identity_role,
    {{ pseudonymize_address('oe.owner') }} AS user_pseudonym
FROM {{ ref('int_execution_safes_owner_events') }} oe
INNER JOIN gp_safes gs ON lower(oe.safe_address) = gs.gp_safe
WHERE oe.event_kind = 'safe_setup' AND oe.owner IS NOT NULL
```

The bridge fact table then joins on the pseudonyms:

```sql
-- models/mixpanel_ga/marts/fct_mixpanel_ga_gpay_users.sql
SELECT mp.user_id_hash, id.gp_safe, id.identity_role
FROM stg_mixpanel_ga__events mp
INNER JOIN int_execution_gpay_safe_identities id
    ON mp.user_id_hash = id.user_pseudonym
```

Neither side ever references a raw address column. The only way this join can produce a result is if the **same** `pseudonymize_address` macro was applied on both sides with the **same** salt — which is guaranteed because there is only one macro and one `CEREBRO_PII_SALT`.

## Rules for new cross-domain work

When you introduce a new model that wants to join Mixpanel data with on-chain data (or any two domains containing identifiers), follow these rules:

1. **Apply `pseudonymize_address` on both sides of the join.** Never leave a raw address column in the intermediate on-chain side and then hash it "later" in the mart. The raw column will leak.
2. **Pseudonymize once, at the boundary.** If you're building an intermediate that will be consumed by multiple marts, hash there so every downstream mart inherits the pseudonym without repeating the hash call.
3. **Treat `pseudonymize_address` as the only legal way to hash an identifier.** Do not write `sipHash64(...)` or `cityHash64(...)` directly anywhere a wallet address is involved. Enforce with a repo-level grep in review:

    ```bash
    rg "sipHash64\(" models/ | rg -v "pseudonymize_address\|user_id_hash\|device_id_hash"
    ```

4. **Union-match when the source ambiguity is real.** Mixpanel's `distinct_id` might be an EOA in one flow, a Safe address in another, and a delegate key in a third. Pseudonymize each plausible candidate and join on `user_id_hash IN (cand1, cand2, cand3)` rather than picking one and hoping. This is how the [Gnosis Pay Mixpanel bridge](../../protocols/gnosis-pay/mixpanel-bridge.md) works.
5. **Never log raw identifiers in diagnostics.** If a query needs to be run against raw data for debugging (e.g. sampling five `distinct_id` values to validate a join), do it in a scratch session with a human-readable warning, not in a committed model.

## Gotchas

- **Don't forget the lowercase.** If you join a pseudonymized mixed-case address against a pseudonymized lowercase address, the hashes will not match. The macro lowercases automatically, but if you pre-process the input (e.g. `replaceAll(addr, '0x', '')`) make sure the same transform is applied on both sides.
- **The salt lives in compiled SQL.** `env_var` is evaluated at dbt compile time, so the rendered SQL in `target/` contains the salt literal. Treat `target/` like a secret — don't commit it, don't publish compiled manifests to world-readable paths.
- **`NULL` and empty strings hash to the same bucket.** `lower(NULL) = NULL` in ClickHouse, and `sipHash64(concat(salt, NULL)) = NULL`. If you expect real addresses you should filter nulls upstream; they won't join to anything meaningful anyway.
- **Never bypass the macro with a bare hash call.** A `sipHash64(address)` written directly anywhere in a model is unsalted and reversible — treat it as if it stored the raw address. Always go through `pseudonymize_address` so the salt is applied automatically.

## Related pages

- [Safe & Module Registry Pattern](safe-module-registry-pattern.md) — the other half of the cross-domain bridge story: how on-chain addresses are discovered and catalogued before they get pseudonymized.
- [Gnosis Pay Mixpanel Bridge](../../protocols/gnosis-pay/mixpanel-bridge.md) — the first and most complete consumer of this pattern.
- [Gnosis App Heuristic Sector](../../protocols/gnosis-app/index.md) — same pseudonym pattern applied to a heuristic-derived user list with Mixpanel as the cross-check rather than the source of truth.
