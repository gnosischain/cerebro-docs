# Execution API Endpoints

<!-- BEGIN AUTO-GENERATED: api-catalog-execution -->
<!-- generated: 2026-07-23 -->
_339 endpoints across 290 resources. Generated from the dbt manifest — edits inside this block will be overwritten. Regenerate with `python scripts/update_docs.py --only api`._

## account_balance_history

Simple API view for Account Portfolio balance history.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/account_balance_history/daily` | GET, POST | tier1 | `address`, `start_date`, `end_date` | limit/offset (envelope) | date ASC |

??? info "`GET/POST /v1/execution/account_balance_history/daily`"
    Simple API view for Account Portfolio balance history.

    Model: `api_execution_account_balance_history_daily` — table `dbt.api_execution_account_balance_history_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `address` | `IN` | `address` | string_list | case: lower; max_items: 20 |
    | `start_date` | `>=` | `date` | date | -- |
    | `end_date` | `<=` | `date` | date | -- |

    **Filter policy:** At least one filter required. Must provide one of: `address`.

    **Pagination:** `limit`/`offset` — default 1000, max 5000; response: envelope `{items, pagination}`

    **Sort:** `date ASC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `address` | `Nullable(String)` | -- |
    | `date` | `Date` | -- |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/account_balance_history/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## account_counterparty_graph

Simple API view for Account Portfolio counterparty graph rows.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/account_counterparty_graph/latest` | GET, POST | tier1 | `source`, `edge_type` | limit/offset (envelope) | weight DESC |

??? info "`GET/POST /v1/execution/account_counterparty_graph/latest`"
    Simple API view for Account Portfolio counterparty graph rows.

    Model: `api_execution_account_counterparty_graph` — table `dbt.api_execution_account_counterparty_graph`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `source` | `=` | `source` | string | case: lower |
    | `edge_type` | `=` | `edge_type` | string | -- |

    **Filter policy:** At least one filter required. Must provide one of: `source`.

    **Pagination:** `limit`/`offset` — default 60, max 250; response: envelope `{items, pagination}`

    **Sort:** `weight DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `edge_type` | `String` | Kind of relationship the edge represents. |
    | `weight` | `UInt64` | Edge weight — aggregated interaction count (or 1 for structural relations). |
    | `source` | `Nullable(String)` | -- |
    | `target` | `Nullable(String)` | -- |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/account_counterparty_graph/latest?source=VALUE" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## account_linked_entities

Simple API view for direct linked entities.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/account_linked_entities/latest` | GET, POST | tier1 | `root_address`, `relation`, `entity_type` | limit/offset (envelope) | last_seen_at DESC |

??? info "`GET/POST /v1/execution/account_linked_entities/latest`"
    Simple API view for direct linked entities.

    Model: `api_execution_account_linked_entities_latest` — table `dbt.api_execution_account_linked_entities_latest`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `root_address` | `IN` | `root_address` | string_list | case: lower; max_items: 20 |
    | `relation` | `=` | `relation` | string | -- |
    | `entity_type` | `=` | `entity_type` | string | -- |

    **Filter policy:** At least one filter required. Must provide one of: `root_address`.

    **Pagination:** `limit`/`offset` — default 100, max 5000; response: envelope `{items, pagination}`

    **Sort:** `last_seen_at DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `entity_type` | `String` | Type of linked entity ('safe', 'safe_owner', 'gpay_wallet', 'validator_credential'). |
    | `last_seen_at` | `DateTime` | Most recent timestamp evidencing the link (became-owner / last module event / slot timestamp). |
    | `relation` | `String` | Relationship of the entity to root_address. |
    | `root_address` | `Nullable(String)` | -- |
    | `entity_id` | `Nullable(String)` | -- |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/account_linked_entities/latest?root_address=VALUE1,VALUE2" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## account_profile

Simple API view over the latest Account Portfolio profile fact.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/account_profile/latest` | GET, POST | tier1 | `address` | limit/offset (envelope) | -- |

??? info "`GET/POST /v1/execution/account_profile/latest`"
    Simple API view over the latest Account Portfolio profile fact.

    Model: `api_execution_account_profile_latest` — table `dbt.api_execution_account_profile_latest`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `address` | `IN` | `address` | string_list | case: lower; max_items: 20 |

    **Filter policy:** At least one filter required. Must provide one of: `address`.

    **Pagination:** `limit`/`offset` — default 20, max 200; response: envelope `{items, pagination}`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `address` | `Nullable(String)` | -- |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/account_profile/latest?address=VALUE1,VALUE2" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## account_recent_transactions

Recent production-backed token movement rows for Account Portfolio transaction tables.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/account_recent_transactions/daily` | GET, POST | tier1 | `address`, `counterparty` | limit/offset (envelope) | date DESC |

??? info "`GET/POST /v1/execution/account_recent_transactions/daily`"
    Recent production-backed token movement rows for Account Portfolio transaction tables.

    Model: `api_execution_account_recent_transactions` — table `dbt.api_execution_account_recent_transactions`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `address` | `IN` | `address` | string_list | case: lower; max_items: 20 |
    | `counterparty` | `=` | `counterparty` | string | case: lower |

    **Filter policy:** At least one filter required. Must provide one of: `address`.

    **Pagination:** `limit`/`offset` — default 100, max 1000; response: envelope `{items, pagination}`

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `counterparty` | `Nullable(String)` | Counterparty address of the movement (other side of the transfer). |
    | `address` | `Nullable(String)` | -- |
    | `date` | `Date` | -- |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/account_recent_transactions/daily?address=VALUE1,VALUE2" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## account_safes

Reverse lookup — given an address, list every Safe it currently owns, enriched with that Safe's threshold, current owner count, and deployment date so the Account Portfolio Safe section can render a full table in a single round-trip. `require_any_of: [owner_address]`.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/account_safes/latest` | GET, POST | tier2 | `owner_address` | limit/offset (envelope) | became_owner_at DESC |

??? info "`GET/POST /v1/execution/account_safes/latest`"
    Reverse lookup — given an address, list every Safe it currently owns, enriched with that Safe's threshold, current owner count, and deployment date so the Account Portfolio Safe section can render a full table in a single round-trip. `require_any_of: [owner_address]`.

    Model: `api_execution_account_safes_latest` — table `dbt.api_execution_account_safes_latest`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `owner_address` | `=` | `owner_address` | string | Address whose owned Safes we want to list; case: lower |

    **Filter policy:** At least one filter required. Must provide one of: `owner_address`.

    **Pagination:** `limit`/`offset` — default 500, max 5000; response: envelope `{items, pagination}`

    **Sort:** `became_owner_at DESC` — user-sortable via `sort_by`: `owner_address`, `safe_address`, `became_owner_at`, `current_threshold`, `current_owner_count`, `deployment_date`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `owner_address` | `Nullable(String)` | The queried owner address (lowercase, 0x-prefixed); the required API filter. |
    | `safe_address` | `Nullable(String)` | A Safe currently owned by owner_address (lowercase, 0x-prefixed). |
    | `became_owner_at` | `DateTime64(0, 'UTC')` | Timestamp of the event that added (or set up) this owner. For an owner who was removed and re-added, this is the re-add time, not the original setup time. |
    | `current_threshold` | `Nullable(UInt32)` | Confirmations currently required by this Safe. |
    | `current_owner_count` | `UInt64` | Number of current owners of the Safe. |
    | `creation_version` | `String` | Safe contract version this proxy was set up against (e.g. 1.3.0, 1.4.1, 1.3.0L2). |
    | `deployment_date` | `Date` | Calendar date of the Safe's creation transaction. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/account_safes/latest?owner_address=VALUE" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## account_search

Simple API view over Account Portfolio search index.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/account_search/latest` | GET, POST | tier1 | `search_key`, `address`, `result_type` | limit/offset (envelope) | -- |

??? info "`GET/POST /v1/execution/account_search/latest`"
    Simple API view over Account Portfolio search index.

    Model: `api_execution_account_search_index` — table `dbt.api_execution_account_search_index`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `search_key` | `=` | `search_key` | string | case: lower |
    | `address` | `=` | `address` | string | case: lower |
    | `result_type` | `=` | `result_type` | string | -- |

    **Filter policy:** At least one filter required. Must provide one of: `search_key`.

    **Pagination:** `limit`/`offset` — default 20, max 100; response: envelope `{items, pagination}`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `address` | `String` | Resolved account address for the search result (lowercase). |
    | `search_key` | `Nullable(String)` | -- |
    | `result_type` | `String` | -- |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/account_search/latest?search_key=VALUE" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## account_token_balances

Simple API view for latest Account Portfolio token balances.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/account_token_balances/latest` | GET, POST | tier1 | `address`, `symbol` | limit/offset (envelope) | balance_usd DESC |

??? info "`GET/POST /v1/execution/account_token_balances/latest`"
    Simple API view for latest Account Portfolio token balances.

    Model: `api_execution_account_token_balances_latest` — table `dbt.api_execution_account_token_balances_latest`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `address` | `IN` | `address` | string_list | case: lower; max_items: 20 |
    | `symbol` | `=` | `symbol` | string | -- |

    **Filter policy:** At least one filter required. Must provide one of: `address`.

    **Pagination:** `limit`/`offset` — default 100, max 5000; response: envelope `{items, pagination}`

    **Sort:** `balance_usd DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `balance_usd` | `Float64` | Balance multiplied by the daily token price in USD. Null when no price is available for that (date, symbol). |
    | `symbol` | `String` | The token's symbol, serving as a human-readable identifier. |
    | `address` | `Nullable(String)` | -- |
    | `token_address` | `String` | -- |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/account_token_balances/latest?address=VALUE1,VALUE2" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## account_token_movements

Simple API view for Account Portfolio token movements.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/account_token_movements/daily` | GET, POST | tier1 | `address`, `counterparty`, `symbol`, `direction`, `start_date`, `end_date` | limit/offset (envelope) | date DESC |

??? info "`GET/POST /v1/execution/account_token_movements/daily`"
    Simple API view for Account Portfolio token movements.

    Model: `api_execution_account_token_movements_daily` — table `dbt.api_execution_account_token_movements_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `address` | `IN` | `address` | string_list | case: lower; max_items: 20 |
    | `counterparty` | `=` | `counterparty` | string | case: lower |
    | `symbol` | `=` | `symbol` | string | -- |
    | `direction` | `=` | `direction` | string | -- |
    | `start_date` | `>=` | `date` | date | -- |
    | `end_date` | `<=` | `date` | date | -- |

    **Filter policy:** At least one filter required. Must provide one of: `address`.

    **Pagination:** `limit`/`offset` — default 250, max 5000; response: envelope `{items, pagination}`

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `counterparty` | `Nullable(String)` | Counterparty address of the movement (other side of the transfer). |
    | `date` | `Date` | Movement date (daily grain). |
    | `symbol` | `String` | Token symbol of the moved asset. |
    | `address` | `Nullable(String)` | -- |
    | `direction` | `String` | -- |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/account_token_movements/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## account_transaction_summary

Simple API view for Account Portfolio transaction/activity summary.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/account_transaction_summary/latest` | GET, POST | tier1 | `address` | limit/offset (envelope) | -- |

??? info "`GET/POST /v1/execution/account_transaction_summary/latest`"
    Simple API view for Account Portfolio transaction/activity summary.

    Model: `api_execution_account_transaction_summary_latest` — table `dbt.api_execution_account_transaction_summary_latest`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `address` | `IN` | `address` | string_list | case: lower; max_items: 20 |

    **Filter policy:** At least one filter required. Must provide one of: `address`.

    **Pagination:** `limit`/`offset` — default 50, max 500; response: envelope `{items, pagination}`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `address` | `Nullable(String)` | -- |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/account_transaction_summary/latest?address=VALUE1,VALUE2" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## account_validators

Account-facing validator member view filterable by withdrawal address or credential.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/account_validators/latest` | GET, POST | tier1 | `withdrawal_address`, `withdrawal_credentials` | limit/offset (envelope) | validator_index ASC |

??? info "`GET/POST /v1/execution/account_validators/latest`"
    Account-facing validator member view filterable by withdrawal address or credential.

    Model: `api_execution_account_validators_latest` — table `dbt.api_execution_account_validators_latest`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `withdrawal_address` | `IN` | `withdrawal_address` | string_list | case: lower; max_items: 20 |
    | `withdrawal_credentials` | `=` | `withdrawal_credentials` | string | case: lower |

    **Filter policy:** At least one filter required. Must provide one of: `withdrawal_address`, `withdrawal_credentials`.

    **Pagination:** `limit`/`offset` — default 100, max 5000; response: envelope `{items, pagination}`

    **Sort:** `validator_index ASC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `withdrawal_credentials` | `String` | Lowercased withdrawal credentials the validator sits under — the Validator Explorer's operator grouping key. |
    | `validator_index` | `UInt32` | -- |
    | `withdrawal_address` | `Nullable(String)` | -- |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/account_validators/latest?withdrawal_address=VALUE1,VALUE2" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## active_senders_per_token

This view provides daily counts of active senders per API token, enabling analysis of token engagement over time.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/active_senders_per_token/daily` | GET | tier0 | `token`, `token_class`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/execution/active_senders_per_token/daily`"
    This view provides daily counts of active senders per API token, enabling analysis of token engagement over time.

    Model: `api_execution_tokens_active_senders_daily` — table `dbt.api_execution_tokens_active_senders_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `token` | string | Token symbol |
    | `token_class` | `=` | `token_class` | string | Token class (native, stablecoin, bridged, etc.) |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The calendar date for which the active sender count is recorded. |
    | `token` | `String` | The identifier of the API token being analyzed. |
    | `token_class` | `String` | The classification or category of the token, indicating its type or purpose. |
    | `value` | `UInt64` | The number of unique active senders associated with the token on the given date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/active_senders_per_token/daily?start_date=2026-01-01"
    ```

## address_resolver

Per-address merge view over `fct_execution_address_resolver`. Collapses the per-source rows into a single row per address using max() on every flag/count column. Hit by the Account Portfolio custom view on every address change. `require_any_of: [address]`.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/address_resolver/latest` | GET, POST | tier1 | `address` | limit/offset (envelope) | -- |

??? info "`GET/POST /v1/execution/address_resolver/latest`"
    Per-address merge view over `fct_execution_address_resolver`. Collapses the per-source rows into a single row per address using max() on every flag/count column. Hit by the Account Portfolio custom view on every address change. `require_any_of: [address]`.

    Model: `api_execution_address_resolver` — table `dbt.api_execution_address_resolver`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `address` | `=` | `address` | string | Gnosis Chain address (0x…). Returns one row with boolean flags + counts for each account-portfolio domain.; case: lower |

    **Filter policy:** At least one filter required. Must provide one of: `address`.

    **Pagination:** `limit`/`offset` — default 10, max 100; response: envelope `{items, pagination}`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `address` | `Nullable(String)` | -- |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/address_resolver/latest?address=VALUE" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## address_search

Lightweight dropdown source for the Account Portfolio tab's global filter. Two columns (address + display_name), `allow_unfiltered: true` so LabelSelector loads the full list in one request and substring-matches client-side.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/address_search/latest` | GET, POST | tier1 | -- | limit/offset (envelope) | connected_validator_count DESC, connected_safe_count DESC |

??? info "`GET/POST /v1/execution/address_search/latest`"
    Lightweight dropdown source for the Account Portfolio tab's global filter. Two columns (address + display_name), `allow_unfiltered: true` so LabelSelector loads the full list in one request and substring-matches client-side.

    Model: `api_execution_address_search` — table `dbt.api_execution_address_search`

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** `limit`/`offset` — default 10000, max 50000; response: envelope `{items, pagination}`

    **Sort:** `connected_validator_count DESC`, `connected_safe_count DESC` — user-sortable via `sort_by`: `address`, `display_name`, `connected_validator_count`, `connected_safe_count`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `connected_safe_count` | `UInt64` | Number of Safes this address currently owns (0 if not an owner). |
    | `connected_validator_count` | `UInt64` | Number of validators whose withdrawal_address is this address (0 if none). |
    | `address` | `Nullable(String)` | -- |
    | `display_name` | `String` | -- |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/address_search/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## balance_cohorts_amount_per_token

This view aggregates daily token balance cohort values, segmented by balance buckets, to support analysis of token holdings over time.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/balance_cohorts_amount_per_token/daily` | GET | tier1 | `token`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/execution/balance_cohorts_amount_per_token/daily`"
    This view aggregates daily token balance cohort values, segmented by balance buckets, to support analysis of token holdings over time.

    Model: `api_execution_tokens_balance_cohorts_value_daily` — table `dbt.api_execution_tokens_balance_cohorts_value_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `token` | string | Token symbol |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific calendar date for the recorded token balance data. |
    | `token` | `String` | The symbol representing the specific cryptocurrency or token. |
    | `cohort_unit` | `String` | The unit used for cohort bucketing ('usd' for balance_usd, 'native' for balance). |
    | `label` | `String` | The bucket label categorizing token balances, such as ranges or tiers. |
    | `value_native` | `Float64` | The total native token balance within the specified bucket on the given date. |
    | `value_usd` | `Float64` | The total USD value of token balances within the specified bucket on the given date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/balance_cohorts_amount_per_token/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## balance_cohorts_holders_per_token

This view provides daily snapshots of token balance cohort distributions among holders, enabling analysis of holder segmentation over time.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/balance_cohorts_holders_per_token/daily` | GET | tier1 | `token`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/execution/balance_cohorts_holders_per_token/daily`"
    This view provides daily snapshots of token balance cohort distributions among holders, enabling analysis of holder segmentation over time.

    Model: `api_execution_tokens_balance_cohorts_holders_daily` — table `dbt.api_execution_tokens_balance_cohorts_holders_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `token` | string | Token symbol |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The date of the snapshot, representing the day of data aggregation. |
    | `token` | `String` | The symbol identifier of the token being analyzed. |
    | `cohort_unit` | `String` | The unit used for cohort bucketing ('usd' for balance_usd, 'native' for balance). |
    | `label` | `String` | The balance bucket label categorizing holder balances, such as ranges or segments. |
    | `value` | `UInt64` | The number of holders within each balance bucket on the given date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/balance_cohorts_holders_per_token/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## blocks_gas_usage_pct

The api_execution_blocks_gas_usage_pct_daily model provides daily insights into the percentage of gas used by API execution blocks, assisting in monitoring resource consumption trends over time.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/blocks_gas_usage_pct/daily` | GET | tier1 | -- | -- | -- |
| `/v1/execution/blocks_gas_usage_pct/monthly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/blocks_gas_usage_pct/daily`"
    The api_execution_blocks_gas_usage_pct_daily model provides daily insights into the percentage of gas used by API execution blocks, assisting in monitoring resource consumption trends over time.

    Model: `api_execution_blocks_gas_usage_pct_daily` — table `dbt.api_execution_blocks_gas_usage_pct_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific day for which the gas usage percentage is recorded. |
    | `value` | `Float64` | The percentage of gas used by execution blocks on the given date, rounded to two decimal places. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/blocks_gas_usage_pct/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/blocks_gas_usage_pct/monthly`"
    This model provides a monthly percentage of gas usage for execution blocks, enabling analysis of gas consumption trends over time.

    Model: `api_execution_blocks_gas_usage_pct_monthly` — table `dbt.api_execution_blocks_gas_usage_pct_monthly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The month for which the gas usage percentage is reported, formatted as a date. |
    | `value` | `Float64` | The gas usage percentage for the month, rounded to two decimal places. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/blocks_gas_usage_pct/monthly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## blocks_per_clients_count

The api_execution_blocks_clients_cnt_daily model provides daily aggregated counts of API execution blocks per client, supporting operational monitoring and capacity planning.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/blocks_per_clients_count/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/blocks_per_clients_count/daily`"
    The api_execution_blocks_clients_cnt_daily model provides daily aggregated counts of API execution blocks per client, supporting operational monitoring and capacity planning.

    Model: `api_execution_blocks_clients_cnt_daily` — table `dbt.api_execution_blocks_clients_cnt_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific calendar date for the recorded data, formatted as YYYY-MM-DD. |
    | `client` | `String` | The identifier for the client associated with the API execution blocks. |
    | `value` | `UInt64` | The count of API execution blocks for the given client on the specified date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/blocks_per_clients_count/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## blocks_per_clients_pct

The api_execution_blocks_clients_pct_daily model provides daily percentage metrics of API execution blocks per client, facilitating monitoring of client-specific API usage patterns over time.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/blocks_per_clients_pct/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/blocks_per_clients_pct/daily`"
    The api_execution_blocks_clients_pct_daily model provides daily percentage metrics of API execution blocks per client, facilitating monitoring of client-specific API usage patterns over time.

    Model: `api_execution_blocks_clients_pct_daily` — table `dbt.api_execution_blocks_clients_pct_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific calendar date for the recorded metrics. |
    | `client` | `String` | Identifier for the client associated with the API execution data. |
    | `value` | `Float64` | The percentage of execution blocks for the client on the given date, rounded to two decimal places. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/blocks_per_clients_pct/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_backers_current

Time-series of currently-trusted (revocation-aware) backers; latest day excluded. Distinct from api:circles_v2_backers_cumulative (ever-backed).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_backers_current/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_backers_current/daily`"
    Time-series of currently-trusted (revocation-aware) backers; latest day excluded. Distinct from api:circles_v2_backers_cumulative (ever-backed).

    Model: `api_execution_circles_v2_backers_current_daily` — table `dbt.api_execution_circles_v2_backers_current_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day (UTC). |
    | `currently_trusted_backers` | `UInt64` | Distinct backers whose backers-group trust interval is open as of the end of this day (revocation-aware). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_backers_current/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_active_minters

Time-series view over fct_execution_circles_v2_active_minters_daily; latest day excluded.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_active_minters/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_active_minters/daily`"
    Time-series view over fct_execution_circles_v2_active_minters_daily; latest day excluded.

    Model: `api_execution_circles_v2_active_minters_daily` — table `dbt.api_execution_circles_v2_active_minters_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day (UTC). |
    | `active_minters` | `UInt64` | Distinct avatars meeting the active-minter criteria on this day. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_active_minters/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_active_trusts

API view of daily active trust count time series.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_active_trusts/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_active_trusts/daily`"
    API view of daily active trust count time series.

    Model: `api_execution_circles_v2_active_trusts_daily` — table `dbt.api_execution_circles_v2_active_trusts_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar date. |
    | `new_trusts` | `Int64` | Trust relationships created on this date. |
    | `revoked_trusts` | `Int64` | Trust relationships revoked/expired on this date. |
    | `active_trusts` | `Int64` | Cumulative active trust count. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_active_trusts/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_active_trusts_cnt

Latest active trust count with 7-day change percentage.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_active_trusts_cnt/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_active_trusts_cnt/latest`"
    Latest active trust count with 7-day change percentage.

    Model: `api_execution_circles_v2_active_trusts_cnt_latest` — table `dbt.api_execution_circles_v2_active_trusts_cnt_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `total` | `UInt64` | Current active trust count. |
    | `change_pct` | `Float64` | 7-day percentage change. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_active_trusts_cnt/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_avatar_balances

Daily CRC balance per avatar broken down by token (one row per avatar/date/token).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_avatar_balances/daily` | GET | tier1 | -- | -- | -- |
| `/v1/execution/circles_v2_avatar_balances/snapshot` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_avatar_balances/daily`"
    Daily CRC balance per avatar broken down by token (one row per avatar/date/token).

    Model: `api_execution_circles_v2_avatar_balances_daily` — table `dbt.api_execution_circles_v2_avatar_balances_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `avatar` | `String` | Address of the avatar. |
    | `date` | `Date` | Calendar date of the balance snapshot. |
    | `token_address` | `String` | Address of the Circles token contract held on that date. |
    | `balance` | `Float64` | Static balance held in the token on that date. |
    | `balance_demurraged` | `Float64` | Demurrage-adjusted balance held in the token on that date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_avatar_balances/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/circles_v2_avatar_balances/snapshot`"
    Latest per-(avatar, token) CRC balance snapshot with an is_wrapped flag indicating whether the token_address is an ERC-20 wrapper. Thin passthrough over fct_execution_circles_v2_avatar_balances_latest, which is materialised daily from the per-day balance fact joined to the distinct wrapper registry.

    Model: `api_execution_circles_v2_avatar_balances_latest` — table `dbt.api_execution_circles_v2_avatar_balances_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `avatar` | `String` | Address of the avatar holding the balance. |
    | `token_address` | `String` | Address of the Circles token contract. |
    | `is_wrapped` | `Bool` | True when the token is an ERC-20 wrapper around a personal CRC token (registered in `int_execution_circles_v2_wrappers`); false when it is the underlying ERC... |
    | `balance` | `Float64` | Static balance in token units (raw / 1e18). |
    | `balance_demurraged` | `Float64` | Demurrage-adjusted balance in token units. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_avatar_balances/snapshot" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_avatar_metadata

Per-avatar identity for Circles v2: on-chain registration metadata (avatar type, on-chain name, inviter, token_id, registration timestamp) joined to the most recently fetched IPFS profile from int_execution_circles_v2_avatar_metadata (display name, preview/image URLs, description, current digest ...

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_avatar_metadata/snapshot` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_avatar_metadata/snapshot`"
    Per-avatar identity for Circles v2: on-chain registration metadata (avatar type, on-chain name, inviter, token_id, registration timestamp) joined to the most recently fetched IPFS profile from int_execution_circles_v2_avatar_metadata (display name, preview/image URLs, description, current digest ...

    Model: `api_execution_circles_v2_avatar_metadata` — table `dbt.api_execution_circles_v2_avatar_metadata`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `avatar` | `String` | Address of the registered avatar. |
    | `avatar_type` | `String` | Avatar category (Human, Group, Org). |
    | `invited_by` | `String` | Address of the avatar that invited this avatar (NULL for Groups/Orgs). |
    | `name` | `String` | On-chain name set at registration (NULL for Humans). |
    | `token_id` | `String` | Personal token contract address (NULL for Orgs). |
    | `registered_at` | `DateTime64` | UTC timestamp of the registration event. |
    | `current_metadata_digest` | `Nullable(String)` | 0x-prefixed hex digest of the most recent metadata payload announced for this avatar by NameRegistry. NULL when the avatar has never published an IPFS profile. |
    | `current_ipfs_cid_v0` | `Nullable(String)` | CIDv0 derived from `current_metadata_digest`. |
    | `current_gateway_url` | `Nullable(String)` | Full IPFS gateway URL for the current digest using the configured `circles_ipfs_gateway` var. |
    | `metadata_name` | `String` | Display `name` field extracted from the current IPFS profile JSON. Populated for ~99.9% of resolved avatars. |
    | `metadata_symbol` | `String` | `symbol` field extracted from the current profile JSON. Rarely populated (group/org tokens only). |
    | `metadata_description` | `String` | `description` field extracted from the current profile JSON. Populated for ~20% of avatars. |
    | `metadata_image_url` | `String` | `imageUrl` field from the current profile JSON. Rarely populated (~1.5%); prefer `metadata_preview_image_url` for thumbnails. |
    | `metadata_preview_image_url` | `String` | `previewImageUrl` field from the current profile JSON. Populated for ~53% of avatars. |
    | `metadata_fetched_at` | `Nullable(DateTime)` | Timestamp the current IPFS payload was fetched from the gateway. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_avatar_metadata/snapshot" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_avatar_metadata_history

Historical timeline of every Circles v2 avatar metadata change. Thin passthrough over int_execution_circles_v2_avatar_metadata_history with one row per (avatar, metadata_digest) ever announced, in event order, carrying valid_from / valid_to / is_current and the parsed IPFS profile fields (name, s...

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_avatar_metadata_history/history` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_avatar_metadata_history/history`"
    Historical timeline of every Circles v2 avatar metadata change. Thin passthrough over int_execution_circles_v2_avatar_metadata_history with one row per (avatar, metadata_digest) ever announced, in event order, carrying valid_from / valid_to / is_current and the parsed IPFS profile fields (name, s...

    Model: `api_execution_circles_v2_avatar_metadata_history` — table `dbt.api_execution_circles_v2_avatar_metadata_history`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `avatar` | `String` | Address of the registered avatar. |
    | `avatar_type` | `String` | Avatar category (Human, Group, Org). |
    | `onchain_name` | `Nullable(String)` | On-chain name set at registration (Group/Org only). |
    | `metadata_digest` | `String` | 0x-prefixed hex digest emitted by this UpdateMetadataDigest event. |
    | `ipfs_cid_v0` | `String` | CIDv0 derived from `metadata_digest`. |
    | `gateway_url` | `String` | Full IPFS gateway URL for this digest version. |
    | `valid_from` | `DateTime64` | Timestamp of the on-chain UpdateMetadataDigest event that introduced this digest. |
    | `valid_to` | `Nullable(DateTime64)` | Timestamp of the next UpdateMetadataDigest event for this avatar. NULL on the most recent row. |
    | `is_current` | `Bool` | True when this row is the most recent metadata digest for the avatar. |
    | `transaction_hash` | `String` | Transaction hash of the on-chain event. |
    | `log_index` | `UInt32` | Log index of the on-chain event. |
    | `metadata_name` | `String` | Display `name` field extracted from this historical version's profile JSON. |
    | `metadata_symbol` | `String` | `symbol` field extracted from this historical version's profile JSON. |
    | `metadata_description` | `String` | `description` field extracted from this historical version's profile JSON. |
    | `metadata_image_url` | `String` | `imageUrl` field from this historical version's profile JSON. |
    | `metadata_preview_image_url` | `String` | `previewImageUrl` field from this historical version's profile JSON. |
    | `metadata_fetched_at` | `Nullable(DateTime)` | Timestamp the IPFS payload for this digest was fetched from the gateway. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_avatar_metadata_history/history" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_avatar_mint_activity

Daily personal-mint activity per Circles v2 avatar. A Circles v2 personal mint is a Hub TransferSingle event where from_address is the zero address (0x0000…0000) and the recipient is the avatar itself. Each row in int_execution_circles_v2_hub_transfers matching that shape represents one personalM...

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_avatar_mint_activity/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_avatar_mint_activity/daily`"
    Daily personal-mint activity per Circles v2 avatar. A Circles v2 personal mint is a Hub TransferSingle event where from_address is the zero address (0x0000…0000) and the recipient is the avatar itself. Each row in int_execution_circles_v2_hub_transfers matching that shape represents one personalM...

    Model: `api_execution_circles_v2_avatar_mint_activity_daily` — table `dbt.api_execution_circles_v2_avatar_mint_activity_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `avatar` | `String` | Address of the avatar receiving the mint. |
    | `date` | `Date` | Calendar date of the mint events (UTC). |
    | `mint_events` | `UInt64` | Number of personalMint() calls that landed on this day for the avatar. |
    | `amount_minted` | `Float64` | Total CRC minted to the avatar on this day (raw / 1e18). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_avatar_mint_activity/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_avatar_personal_token_supply

One-row-per-avatar summary of a Circles v2 avatar's own personal CRC token: total circulating supply, how much is wrapped as ERC-20, and the wrapped share. Thin passthrough over fct_execution_circles_v2_avatar_personal_token_supply_latest, which rolls up fct_execution_circles_v2_avatar_token_dist...

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_avatar_personal_token_supply/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_avatar_personal_token_supply/latest`"
    One-row-per-avatar summary of a Circles v2 avatar's own personal CRC token: total circulating supply, how much is wrapped as ERC-20, and the wrapped share. Thin passthrough over fct_execution_circles_v2_avatar_personal_token_supply_latest, which rolls up fct_execution_circles_v2_avatar_token_dist...

    Model: `api_execution_circles_v2_avatar_personal_token_supply_latest` — table `dbt.api_execution_circles_v2_avatar_personal_token_supply_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `avatar` | `String` | The avatar whose personal CRC token is being summarised. |
    | `supply` | `Float64` | Circulating supply of this avatar's personal CRC (sum of balances across all holder categories). |
    | `wrapped` | `Float64` | Portion of the supply currently held by the avatar's ERC-20 wrapper contracts. |
    | `unwrapped` | `Float64` | Portion of the supply held as native ERC-1155 (supply − wrapped). |
    | `wrapped_pct` | `Nullable(Float64)` | wrapped / supply × 100, rounded to 1 decimal. NULL when supply = 0. |
    | `supply_demurraged` | `Float64` | Demurrage-adjusted equivalent of supply. |
    | `wrapped_demurraged` | `Float64` | Demurrage-adjusted equivalent of wrapped. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_avatar_personal_token_supply/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_avatar_search

Lightweight (avatar, display_name) lookup used by the dashboard global filter to support searching avatars by display name OR address. Two columns, one row per registered Circles v2 avatar (sourced from api_execution_circles_v2_avatar_metadata). display_name prefers the IPFS profile name and fall...

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_avatar_search/snapshot` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_avatar_search/snapshot`"
    Lightweight (avatar, display_name) lookup used by the dashboard global filter to support searching avatars by display name OR address. Two columns, one row per registered Circles v2 avatar (sourced from api_execution_circles_v2_avatar_metadata). display_name prefers the IPFS profile name and fall...

    Model: `api_execution_circles_v2_avatar_search` — table `dbt.api_execution_circles_v2_avatar_search`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `avatar` | `String` | Address of the registered avatar. |
    | `display_name` | `String` | IPFS profile name with on-chain name fallback (empty when neither is set). |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_avatar_search/snapshot" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_avatar_token_distribution

Per-avatar distribution of holders of a Circles v2 personal CRC token (the ERC-1155 token whose token_address equals the avatar address). Thin passthrough over fct_execution_circles_v2_avatar_token_distribution, which classifies every current holder (above the 0.001 CRC dust threshold) as one of:...

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_avatar_token_distribution/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_avatar_token_distribution/latest`"
    Per-avatar distribution of holders of a Circles v2 personal CRC token (the ERC-1155 token whose token_address equals the avatar address). Thin passthrough over fct_execution_circles_v2_avatar_token_distribution, which classifies every current holder (above the 0.001 CRC dust threshold) as one of:...

    Model: `api_execution_circles_v2_avatar_token_distribution` — table `dbt.api_execution_circles_v2_avatar_token_distribution`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `avatar` | `String` | The avatar whose personal CRC token is being inspected. |
    | `holder_category` | `String` | One of Self, Wrapped (ERC-20), Other Circles avatars, Other contracts. |
    | `holder_count` | `UInt64` | Number of distinct accounts in this category that hold the avatar's CRC token (above the 0.001 CRC dust threshold). |
    | `balance` | `Float64` | Sum of static CRC balances held by accounts in this category. |
    | `balance_demurraged` | `Float64` | Sum of demurrage-adjusted CRC balances held by accounts in this category. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_avatar_token_distribution/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_avatar_tokens_held_count

Per-avatar count of distinct CRC tokens currently held with a balance above the 0.001 CRC dust threshold (1e15 raw wei). Thin passthrough over fct_execution_circles_v2_avatar_tokens_held_count, which is materialised daily from int_execution_circles_v2_balances_daily on the last completed day. Bac...

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_avatar_tokens_held_count/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_avatar_tokens_held_count/latest`"
    Per-avatar count of distinct CRC tokens currently held with a balance above the 0.001 CRC dust threshold (1e15 raw wei). Thin passthrough over fct_execution_circles_v2_avatar_tokens_held_count, which is materialised daily from int_execution_circles_v2_balances_daily on the last completed day. Bac...

    Model: `api_execution_circles_v2_avatar_tokens_held_count` — table `dbt.api_execution_circles_v2_avatar_tokens_held_count`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `avatar` | `String` | Address of the avatar holding the tokens. |
    | `tokens_held_count` | `UInt64` | Number of distinct token contracts the avatar holds with > 0.001 CRC. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_avatar_tokens_held_count/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_avatar_trust_network

Trust-network edge list for the Circles v2 Avatar Trust Network panel. One row per directed trust edge from the perspective of the focal avatar. For mutual relationships TWO rows are emitted (avatar → counterparty AND counterparty → avatar) so the chart renders both arrows. The dashboard's avatar...

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_avatar_trust_network/snapshot` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_avatar_trust_network/snapshot`"
    Trust-network edge list for the Circles v2 Avatar Trust Network panel. One row per directed trust edge from the perspective of the focal avatar. For mutual relationships TWO rows are emitted (avatar → counterparty AND counterparty → avatar) so the chart renders both arrows. The dashboard's avatar...

    Model: `api_execution_circles_v2_avatar_trust_network` — table `dbt.api_execution_circles_v2_avatar_trust_network`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `avatar` | `String` | The focal avatar this row belongs to (used by the dashboard's avatar global filter). |
    | `source_id` | `String` | Address of the truster on this edge. |
    | `target_id` | `String` | Address of the trustee on this edge. |
    | `source_name` | `String` | Display name of the source endpoint (IPFS profile name → on-chain name → truncated address). |
    | `target_name` | `String` | Display name of the target endpoint (IPFS profile name → on-chain name → truncated address). |
    | `source_image` | `String` | IPFS preview image URL of the source endpoint, or empty when no profile image is published. |
    | `target_image` | `String` | IPFS preview image URL of the target endpoint, or empty when no profile image is published. |
    | `direction` | `String` | One of "Mutual" / "Trust given" / "Trust received" — drives the edgeStyleField on the dashboard graph panel so each direction renders in its own colour. Mutu... |
    | `source_layer` | `String` | Concentric ring assignment for the source endpoint. "Focal avatar" when the source IS the focal avatar (centre), otherwise the direction label (Mutual / Trus... |
    | `target_layer` | `String` | Concentric ring assignment for the target endpoint. "Focal avatar" when the target IS the focal avatar (centre), otherwise the direction label. |
    | `value` | `UInt8` | Constant 1 (trust edges are unweighted; the column exists so the chart engine can size nodes by degree). |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_avatar_trust_network/snapshot" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_avatar_trust_relations

Current active trust relations pivoted to one row per (avatar, counterparty) pair with direction (outgoing, incoming, or mutual) and the timestamps of each direction.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_avatar_trust_relations/snapshot` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_avatar_trust_relations/snapshot`"
    Current active trust relations pivoted to one row per (avatar, counterparty) pair with direction (outgoing, incoming, or mutual) and the timestamps of each direction.

    Model: `api_execution_circles_v2_avatar_trust_relations` — table `dbt.api_execution_circles_v2_avatar_trust_relations`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `avatar` | `String` | The avatar address. |
    | `counterparty` | `String` | The other side of the trust relation. |
    | `direction` | `String` | outgoing if avatar trusts counterparty only; incoming if counterparty trusts avatar only; mutual if both directions exist. |
    | `outgoing_from` | `DateTime64` | Start timestamp of the outgoing trust (avatar -> counterparty); NULL if no outgoing trust exists. |
    | `incoming_from` | `DateTime64` | Start timestamp of the incoming trust (counterparty -> avatar); NULL if no incoming trust exists. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_avatar_trust_relations/snapshot" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_avatar_trusts

Daily cumulative trusts given and received per avatar.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_avatar_trusts/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_avatar_trusts/daily`"
    Daily cumulative trusts given and received per avatar.

    Model: `api_execution_circles_v2_avatar_trusts_daily` — table `dbt.api_execution_circles_v2_avatar_trusts_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `avatar` | `String` | Address of the avatar. |
    | `date` | `Date` | Calendar date. |
    | `trusts_given_count` | `Int64` | Cumulative count of outgoing trust relationships. |
    | `trusts_received_count` | `Int64` | Cumulative count of incoming trust relationships. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_avatar_trusts/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_avatar_trusts_summary

Latest snapshot of cumulative trusts given and received per avatar.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_avatar_trusts_summary/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_avatar_trusts_summary/latest`"
    Latest snapshot of cumulative trusts given and received per avatar.

    Model: `api_execution_circles_v2_avatar_trusts_summary` — table `dbt.api_execution_circles_v2_avatar_trusts_summary`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `avatar` | `String` | Address of the avatar. |
    | `trusts_given_count` | `Int64` | Cumulative count of outgoing trust relationships at latest day. |
    | `trusts_received_count` | `Int64` | Cumulative count of incoming trust relationships at latest day. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_avatar_trusts_summary/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_avatars

API view of daily avatar type counts and cumulative totals.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_avatars/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_avatars/daily`"
    API view of daily avatar type counts and cumulative totals.

    Model: `api_execution_circles_v2_avatars` — table `dbt.api_execution_circles_v2_avatars`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific date of the recorded avatar usage data. |
    | `avatar_type` | `String` | The category or type of avatar (Human, Group, Organization). |
    | `cnt` | `UInt64` | The number of new avatars registered on the given date. |
    | `total` | `UInt64` | The cumulative total of avatars of this type up to the given date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_avatars/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_avatars_current

API view of current Circles v2 avatar registrations.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_avatars_current/snapshot` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_avatars_current/snapshot`"
    API view of current Circles v2 avatar registrations.

    Model: `api_execution_circles_v2_avatars_current` — table `dbt.api_execution_circles_v2_avatars_current`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `block_number` | `UInt64` | Block number of the latest registration event. |
    | `block_timestamp` | `DateTime` | Block timestamp of the latest registration event. |
    | `transaction_hash` | `String` | Transaction hash of the latest registration event. |
    | `transaction_index` | `UInt64` | Transaction index within the block. |
    | `log_index` | `UInt64` | Log index within the transaction. |
    | `avatar_type` | `String` | Type of avatar (Human, Org, Group). |
    | `invited_by` | `String` | Address of the avatar that invited this avatar. |
    | `avatar` | `String` | Address of the registered avatar. |
    | `token_id` | `String` | Token ID associated with the avatar. |
    | `name` | `String` | Display name of the avatar. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_avatars_current/snapshot" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_backers_cumulative

Time-series view of trust-defined EVER-BACKED cumulative backers (ignores revocation); latest day excluded. For the revocation-aware series see api:circles_backers_current.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_backers_cumulative/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_backers_cumulative/daily`"
    Time-series view of trust-defined EVER-BACKED cumulative backers (ignores revocation); latest day excluded. For the revocation-aware series see api:circles_backers_current.

    Model: `api_execution_circles_v2_backers_cumulative_daily` — table `dbt.api_execution_circles_v2_backers_cumulative_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day (UTC). |
    | `new_backers` | `UInt64` | Trust-defined backers first trusted by the backers group on this day. |
    | `cumulative_backers` | `UInt64` | Running total of distinct trust-defined backers ever trusted up to and including this day (ignores revocation). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_backers_cumulative/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_backing_depositors_current

Snapshot of distinct depositor addresses.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_backing_depositors_current/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_backing_depositors_current/latest`"
    Snapshot of distinct depositor addresses.

    Model: `api_execution_circles_v2_backing_depositors_current` — table `dbt.api_execution_circles_v2_backing_depositors_current`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `backer` | `String` | Depositor address (emitted at least one backing event). |
    | `first_initiated_at` | `DateTime` | Timestamp of the depositor's earliest backing event. |
    | `last_event_at` | `DateTime` | Timestamp of the depositor's most recent backing event. |
    | `n_initiated` | `UInt64` | Number of 'initiated' backing events by this depositor. |
    | `n_completed` | `UInt64` | Number of 'completed' backing events by this depositor. |
    | `n_released` | `UInt64` | Number of 'released' backing events by this depositor. |
    | `n_distinct_assets` | `UInt64` | Distinct backing assets this depositor has pledged. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_backing_depositors_current/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_backing_events

Time-series of Circles v2 backing-lifecycle events, by stage.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_backing_events/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_backing_events/daily`"
    Time-series of Circles v2 backing-lifecycle events, by stage.

    Model: `api_execution_circles_v2_backing_events_daily` — table `dbt.api_execution_circles_v2_backing_events_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day (UTC). |
    | `lifecycle_stage` | `String` | Backing lifecycle stage (initiated / deployed / lbp_deployed / completed / released / asset_status_updated / global_release_updated). |
    | `n_events` | `UInt64` | Number of backing events in this stage on this day. |
    | `n_distinct_backers` | `UInt64` | Distinct backer addresses emitting an event in this stage on this day. |
    | `n_distinct_assets` | `UInt64` | Distinct backing assets pledged in this stage on this day. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_backing_events/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_balance_cohorts

Daily wealth distribution: distinct CRC holders bucketed by balance tier (0-1 / 1-10 / 10-100 / 100-1k / 1k-10k / 10k-100k / 100k+). Passthrough over int_execution_circles_v2_balance_cohorts_daily, excluding the current incomplete day.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_balance_cohorts/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_balance_cohorts/daily`"
    Daily wealth distribution: distinct CRC holders bucketed by balance tier (0-1 / 1-10 / 10-100 / 100-1k / 1k-10k / 10k-100k / 100k+). Passthrough over int_execution_circles_v2_balance_cohorts_daily, excluding the current incomplete day.

    Model: `api_execution_circles_v2_balance_cohorts_daily` — table `dbt.api_execution_circles_v2_balance_cohorts_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar date (current incomplete day excluded). |
    | `balance_bucket` | `String` | Balance range bucket label (e.g. '0-1', '1-10', '100k+'). |
    | `holder_count` | `UInt64` | Number of distinct holders in this bucket. |
    | `total_balance` | `Float64` | Sum of nominal balances in this bucket in CRC. |
    | `total_demurraged_balance` | `Nullable(Float64)` | Sum of demurrage-adjusted balances in this bucket in CRC. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_balance_cohorts/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_economically_active_avatars

Weekly economically active Circles avatars (ecosystem-wide, circles-first definition) by earning_kind, with the in-app-tx subset. The Gnosis App WEAU (in-app filtered) lives at api:gnosis_app_weekly_economically_active_users.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_economically_active_avatars/weekly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_economically_active_avatars/weekly`"
    Weekly economically active Circles avatars (ecosystem-wide, circles-first definition) by earning_kind, with the in-app-tx subset. The Gnosis App WEAU (in-app filtered) lives at api:gnosis_app_weekly_economically_active_users.

    Model: `api_execution_circles_v2_economically_active_avatars_weekly` — table `dbt.api_execution_circles_v2_economically_active_avatars_weekly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | Monday-aligned start of the week (UTC). |
    | `earning_kind` | `String` | 'gcrc_cashback', 'inviter_fee' or 'any'. |
    | `avatars` | `UInt64` | Distinct economically active avatars (ecosystem-wide). |
    | `avatars_in_app_tx` | `UInt64` | Subset whose earning events came via a Gnosis App relayer tx. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_economically_active_avatars/weekly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_gcrc_cashback

Weekly Circles v2 gCRC cashback distribution: distinct recipient count and total gCRC amount sent from the cashback wallet to app users (weeks meeting the >= 1 gCRC threshold). The latest incomplete week is excluded.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_gcrc_cashback/weekly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_gcrc_cashback/weekly`"
    Weekly Circles v2 gCRC cashback distribution: distinct recipient count and total gCRC amount sent from the cashback wallet to app users (weeks meeting the >= 1 gCRC threshold). The latest incomplete week is excluded.

    Model: `api_execution_circles_v2_gcrc_cashback_weekly` — table `dbt.api_execution_circles_v2_gcrc_cashback_weekly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | Start-of-week date (UTC, Monday start) for the cashback aggregation. |
    | `n_recipients` | `UInt64` | Distinct recipients that received gCRC cashback that week. |
    | `amount` | `Float64` | Total gCRC amount distributed as cashback that week. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_gcrc_cashback/weekly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_gcrc_cashback_cumulative

Cumulative Circles v2 gCRC cashback over time, one row per week: the running total gCRC distributed and the running count of distinct lifetime recipients (each recipient counted in the week they first received cashback).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_gcrc_cashback_cumulative/weekly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_gcrc_cashback_cumulative/weekly`"
    Cumulative Circles v2 gCRC cashback over time, one row per week: the running total gCRC distributed and the running count of distinct lifetime recipients (each recipient counted in the week they first received cashback).

    Model: `api_execution_circles_v2_gcrc_cashback_cumulative` — table `dbt.api_execution_circles_v2_gcrc_cashback_cumulative`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | Week start (Monday, UTC). |
    | `cumulative_amount` | `Float64` | Running total gCRC cashback distributed through the end of this week. |
    | `cumulative_recipients` | `UInt64` | Running count of distinct lifetime cashback recipients, each counted in the week they first received cashback. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_gcrc_cashback_cumulative/weekly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_gcrc_cashback_recipients_ranking

Top 100 lifetime recipients of Circles v2 gCRC cashback, ranked by total amount received, enriched with each recipient's avatar profile (display name and preview image).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_gcrc_cashback_recipients_ranking/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_gcrc_cashback_recipients_ranking/latest`"
    Top 100 lifetime recipients of Circles v2 gCRC cashback, ranked by total amount received, enriched with each recipient's avatar profile (display name and preview image).

    Model: `api_execution_circles_v2_gcrc_cashback_recipients_ranking` — table `dbt.api_execution_circles_v2_gcrc_cashback_recipients_ranking`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Date the snapshot was generated (today, UTC). |
    | `rank` | `UInt64` | Rank by total cashback received (1 = highest). |
    | `address` | `String` | Recipient avatar address. |
    | `display_name` | `String` | Human-readable display name, falling back to the address when no profile name exists. |
    | `preview_image_url` | `Nullable(String)` | Avatar preview image URL, if available. |
    | `total_amount` | `Float64` | Total gCRC cashback received across all weeks. |
    | `n_weeks` | `UInt64` | Number of distinct weeks the recipient received cashback. |
    | `last_week` | `Date` | Most recent week (UTC week start) the recipient received cashback. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_gcrc_cashback_recipients_ranking/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_gcrc_cashback_total

Lifetime (single-row) Circles v2 gCRC cashback totals for KPI tiles: the cumulative cashback amount distributed and the number of distinct recipients across all completed weeks.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_gcrc_cashback_total/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_gcrc_cashback_total/latest`"
    Lifetime (single-row) Circles v2 gCRC cashback totals for KPI tiles: the cumulative cashback amount distributed and the number of distinct recipients across all completed weeks.

    Model: `api_execution_circles_v2_gcrc_cashback_total` — table `dbt.api_execution_circles_v2_gcrc_cashback_total`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Snapshot date the totals were computed (today, UTC). |
    | `total_amount` | `Float64` | Cumulative gCRC cashback amount distributed across all completed weeks. |
    | `total_recipients` | `UInt64` | Distinct addresses that received gCRC cashback across all completed weeks. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_gcrc_cashback_total/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_group_collateral

Per-group daily member-CRC collateral (native units).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_group_collateral/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_group_collateral/daily`"
    Per-group daily member-CRC collateral (native units).

    Model: `api_execution_circles_v2_group_collateral_daily` — table `dbt.api_execution_circles_v2_group_collateral_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day (UTC). |
    | `group_address` | `String` | Lowercased group avatar address. |
    | `collateral` | `Float64` | Member-CRC collateral held by the group at end-of-day (native units, summed across all backing token ids). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_group_collateral/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_group_explorer_profile

One row per Circles v2 group: identity, on-chain handlers, and snapshot KPIs (members, supply, wrapped %, collateral, 7d mints, holders). Backs the Group Explorer identity header and KPI tiles.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_group_explorer_profile/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_group_explorer_profile/latest`"
    One row per Circles v2 group: identity, on-chain handlers, and snapshot KPIs (members, supply, wrapped %, collateral, 7d mints, holders). Backs the Group Explorer identity header and KPI tiles.

    Model: `api_execution_circles_v2_group_explorer_profile` — table `dbt.api_execution_circles_v2_group_explorer_profile`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `group_address` | `String` | Lowercased group avatar address. |
    | `as_of_date` | `Date` | Snapshot date the row was materialized (UTC). |
    | `display_name` | `String` | Group display name from metadata or on-chain fallback. |
    | `preview_image_url` | `Nullable(String)` | Group avatar preview image URL from metadata. |
    | `registered_at` | `DateTime` | Most recent on-chain registration timestamp for the group. |
    | `invited_by` | `Nullable(String)` | Address that invited the group per metadata. |
    | `owner` | `Nullable(String)` | Current group owner address. |
    | `treasury_address` | `Nullable(String)` | Current treasury handler address. |
    | `service` | `Nullable(String)` | Current service handler address. |
    | `mint_handler` | `Nullable(String)` | Current mint handler address. |
    | `redemption_handler` | `Nullable(String)` | Current redemption handler address. |
    | `n_members` | `UInt64` | Current group member count. |
    | `supply` | `Float64` | Current group token supply in native units. |
    | `wrapped_pct` | `Float64` | Share of supply held as ERC-20 wrapper. |
    | `collateral_total` | `Float64` | Latest total member-CRC collateral in native units. |
    | `mints_7d` | `Float64` | Group-token minted in the last 7 days in native units. |
    | `holders_count` | `UInt64` | Distinct holders of the group token. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_group_explorer_profile/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_group_holders

Holders of a group's token, resolving both native ERC-1155 and ERC-20 wrapper legs (wrapper mapped back to group via the wrapper registry).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_group_holders/snapshot` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_group_holders/snapshot`"
    Holders of a group's token, resolving both native ERC-1155 and ERC-20 wrapper legs (wrapper mapped back to group via the wrapper registry).

    Model: `api_execution_circles_v2_group_holders` — table `dbt.api_execution_circles_v2_group_holders`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Snapshot date the holder list was computed (today() UTC). |
    | `group_address` | `String` | Lowercased group avatar address. |
    | `holder` | `String` | Lowercased holder avatar address. |
    | `display_name` | `String` | Holder display name from IPFS metadata or on-chain name or address fallback. |
    | `balance` | `Float64` | Holder total group-token balance in native units summing the native and wrapper legs. |
    | `is_wrapped` | `UInt8` | 1 if any of the holder balance is held via an ERC-20 wrapper. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_group_holders/snapshot" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_group_member_scores

Latest on-chain score per (score-based group, member), from the OffchainScoreBasedMintPolicy PersonalMinted event. One row per member per group; score is the value at the member's most recent mint.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_group_member_scores/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_group_member_scores/latest`"
    Latest on-chain score per (score-based group, member), from the OffchainScoreBasedMintPolicy PersonalMinted event. One row per member per group; score is the value at the member's most recent mint.

    Model: `api_execution_circles_v2_group_member_scores` — table `dbt.api_execution_circles_v2_group_member_scores`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Date the snapshot was computed (query date |
    | `group_address` | `String` | Lowercased group avatar address. |
    | `member` | `String` | Member (minter) avatar address |
    | `score` | `UInt64` | Member's off-chain trust score at their latest mint. |
    | `last_mint_at` | `DateTime` | Timestamp of the member's latest score-based mint. |
    | `last_mint_amount` | `Float64` | Group tokens minted at the latest mint (CRC). |
    | `n_mints` | `UInt64` | Number of score-based mints by this member in this group. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_group_member_scores/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_group_members

Members of a group (trustees on its outgoing trust list) with profile and join date; is_mutual flags reciprocal trust.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_group_members/snapshot` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_group_members/snapshot`"
    Members of a group (trustees on its outgoing trust list) with profile and join date; is_mutual flags reciprocal trust.

    Model: `api_execution_circles_v2_group_members` — table `dbt.api_execution_circles_v2_group_members`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Snapshot date the row was materialized (constant today()). |
    | `group_address` | `String` | Lowercased group avatar address. |
    | `member` | `String` | Lowercased member avatar address. |
    | `display_name` | `String` | Member IPFS metadata name, else on-chain name, else the address. |
    | `preview_image_url` | `Nullable(String)` | Member profile preview image URL from IPFS metadata, if any. |
    | `member_since` | `DateTime` | Timestamp the member's trust edge became valid (join date). |
    | `is_mutual` | `UInt8` | 1 when the member also trusts the group back (reciprocal trust). |
    | `score` | `Nullable(UInt64)` | Member's latest on-chain mint score for score-based groups, else null. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_group_members/snapshot" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_group_mints

Per-group daily group-token mints vs collateral redemptions (distinct tokens/units, labelled in the kind column).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_group_mints/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_group_mints/daily`"
    Per-group daily group-token mints vs collateral redemptions (distinct tokens/units, labelled in the kind column).

    Model: `api_execution_circles_v2_group_mints_daily` — table `dbt.api_execution_circles_v2_group_mints_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day (UTC). |
    | `group_address` | `String` | Lowercased group avatar address. |
    | `kind` | `String` | Series label distinguishing group-token mints from collateral redemptions. |
    | `amount` | `Float64` | Summed amount for that day/group/kind (native CRC units, 1e18-scaled). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_group_mints/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_group_score_distribution

Count of members per score bucket, per score-based group. Buckets carry a bucket_rank for stable ordering in charts.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_group_score_distribution/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_group_score_distribution/latest`"
    Count of members per score bucket, per score-based group. Buckets carry a bucket_rank for stable ordering in charts.

    Model: `api_execution_circles_v2_group_score_distribution` — table `dbt.api_execution_circles_v2_group_score_distribution`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Date the snapshot was computed (UTC). |
    | `group_address` | `String` | Lowercased group avatar address. |
    | `score_bucket` | `String` | Score range bucket label (0-24 / 25-49 / 50-74 / 75-99 / 100-149 / 150+). |
    | `bucket_rank` | `UInt8` | Ordinal rank of the bucket for chart ordering. |
    | `n_members` | `UInt64` | Number of members in this score bucket. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_group_score_distribution/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_group_search

(group_address, display_name) lookup backing the Group Explorer global filter. One row per Circles v2 Group avatar.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_group_search/snapshot` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_group_search/snapshot`"
    (group_address, display_name) lookup backing the Group Explorer global filter. One row per Circles v2 Group avatar.

    Model: `api_execution_circles_v2_group_search` — table `dbt.api_execution_circles_v2_group_search`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Snapshot date the lookup was materialised (today() at build time). |
    | `group_address` | `String` | Lowercased group avatar address. |
    | `display_name` | `String` | IPFS metadata name, else on-chain name, else the address. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_group_search/snapshot" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_group_size

Per-group daily member count, from historical trust intervals.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_group_size/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_group_size/daily`"
    Per-group daily member count, from historical trust intervals.

    Model: `api_execution_circles_v2_group_size_daily` — table `dbt.api_execution_circles_v2_group_size_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `group_address` | `String` | Lowercased group avatar address. |
    | `date` | `Date` | Calendar day (UTC). |
    | `n_members` | `UInt64` | Number of members (trustees) in the group that day. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_group_size/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_group_size_distribution

Histogram of Circles v2 group sizes (members per group).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_group_size_distribution/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_group_size_distribution/latest`"
    Histogram of Circles v2 group sizes (members per group).

    Model: `api_execution_circles_v2_group_size_distribution` — table `dbt.api_execution_circles_v2_group_size_distribution`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `bucket` | `String` | Group-size bucket label, prefixed with its order (e.g. '1. 0', '2. 1–5', … '6. 500+'). |
    | `bucket_order` | `UInt8` | 1..6 ordering for stable stacking. |
    | `n_groups` | `UInt64` | Number of groups falling into this size bucket. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_group_size_distribution/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_group_supply

Per-group daily token supply, split native ERC-1155 vs ERC-20 wrapper (wrapper level = prefix-sum of wrapper supply deltas).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_group_supply/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_group_supply/daily`"
    Per-group daily token supply, split native ERC-1155 vs ERC-20 wrapper (wrapper level = prefix-sum of wrapper supply deltas).

    Model: `api_execution_circles_v2_group_supply_daily` — table `dbt.api_execution_circles_v2_group_supply_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `group_address` | `String` | Lowercased group avatar address. |
    | `date` | `Date` | Calendar day (UTC). |
    | `supply` | `Float64` | Nominal (non-demurraged) group token supply that day (native CRC units, 1e18-scaled). |
    | `supply_demurraged` | `Float64` | Demurraged group token supply that day (native CRC units, 1e18-scaled). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_group_supply/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_group_token_supply

Long-format time-series view (one row per (date, label)) over fct_execution_circles_v2_group_token_supply_daily, ready for a stacked-area chart with seriesField='label'. Latest day excluded.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_group_token_supply/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_group_token_supply/daily`"
    Long-format time-series view (one row per (date, label)) over fct_execution_circles_v2_group_token_supply_daily, ready for a stacked-area chart with seriesField='label'. Latest day excluded.

    Model: `api_execution_circles_v2_group_token_supply_daily` — table `dbt.api_execution_circles_v2_group_token_supply_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day (UTC). |
    | `label` | `String` | 'ERC-1155 (native)' or 'ERC-20 (wrapped)'. |
    | `value` | `Float64` | Group-token supply for this label's form on this day, in CRC. |
    | `value_demurraged` | `Float64` | Demurrage-adjusted equivalent of value. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_group_token_supply/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_group_token_supply_top

Top 100 Circles v2 groups by personal-token supply (leaderboard view).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_group_token_supply_top/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_group_token_supply_top/latest`"
    Top 100 Circles v2 groups by personal-token supply (leaderboard view).

    Model: `api_execution_circles_v2_group_token_supply_top_latest` — table `dbt.api_execution_circles_v2_group_token_supply_top_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `rank` | `UInt64` | Leaderboard rank (1 = largest supply), ordered by supply descending. |
    | `group_avatar` | `String` | Lowercase group avatar address. |
    | `display_name` | `Nullable(String)` | Group display name — IPFS metadata name, falling back to the on-chain name. NULL if none. |
    | `preview_image_url` | `Nullable(String)` | Preview image URL from the group's IPFS profile metadata. NULL if none. |
    | `supply` | `Float64` | Circulating supply of the group's own personal CRC token (sum across all holder categories). |
    | `wrapped` | `Float64` | Portion of the supply currently held by the avatar's ERC-20 wrapper contracts. |
    | `unwrapped` | `Float64` | Portion of the supply held as native ERC-1155 (supply − wrapped). |
    | `wrapped_pct` | `Nullable(Float64)` | wrapped / supply × 100. NULL when supply = 0. |
    | `supply_demurraged` | `Float64` | Demurrage-adjusted equivalent of supply. |
    | `n_members` | `UInt64` | Distinct trustees on the group's outgoing trust list (0 if none). |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_group_token_supply_top/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_groups_cnt

Latest count of group avatars and 7-day percentage change.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_groups_cnt/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_groups_cnt/latest`"
    Latest count of group avatars and 7-day percentage change.

    Model: `api_execution_circles_v2_groups_cnt_latest` — table `dbt.api_execution_circles_v2_groups_cnt_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `total` | `UInt64` | The total number of group avatars at the latest date. |
    | `change_pct` | `Float64` | Percentage change in group count compared to 7 days ago, rounded to 1 decimal. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_groups_cnt/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_groups_overview

Daily group registrations + collateral activity, with cumulative group total.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_groups_overview/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_groups_overview/daily`"
    Daily group registrations + collateral activity, with cumulative group total.

    Model: `api_execution_circles_v2_groups_overview_daily` — table `dbt.api_execution_circles_v2_groups_overview_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day (UTC). |
    | `n_new_groups` | `UInt64` | Group avatars registered on this day. |
    | `n_collateral_events` | `UInt64` | StandardTreasury lock/burn/return collateral events on this day. |
    | `n_distinct_groups_acting` | `UInt64` | Distinct groups touching collateral on this day. |
    | `n_groups_total` | `UInt64` | Cumulative running total of registered groups up to and including this day. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_groups_overview/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_hub_events

Time-series view over int_execution_circles_v2_hub_events_daily; latest day excluded.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_hub_events/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_hub_events/daily`"
    Time-series view over int_execution_circles_v2_hub_events_daily; latest day excluded.

    Model: `api_execution_circles_v2_hub_events_daily` — table `dbt.api_execution_circles_v2_hub_events_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day (UTC). |
    | `event_name` | `String` | Hub event name (RegisterHuman, Trust, TransferSingle, …). |
    | `n_events` | `UInt64` | Number of events of this kind on this day. |
    | `n_tx` | `UInt64` | Number of distinct transactions emitting this event on this day. |
    | `n_distinct_addresses` | `UInt64` | Distinct participant addresses across all event-specific fields. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_hub_events/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_humans_cnt

Latest count of human avatars and 7-day percentage change.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_humans_cnt/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_humans_cnt/latest`"
    Latest count of human avatars and 7-day percentage change.

    Model: `api_execution_circles_v2_humans_cnt_latest` — table `dbt.api_execution_circles_v2_humans_cnt_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `total` | `UInt64` | The total number of human avatars at the latest date. |
    | `change_pct` | `Float64` | Percentage change in human count compared to 7 days ago. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_humans_cnt/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_invite_funnel_cohort

Invitee cohort by month, with the five-stage mint-cadence funnel (Invited → ≥2 days → ≥7 days → ≥14 days → Active Minter) and the percentile latency to "came back" (second mint on a different day). Skips the trivial acceptance mint, which always fires.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_invite_funnel_cohort/monthly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_invite_funnel_cohort/monthly`"
    Invitee cohort by month, with the five-stage mint-cadence funnel (Invited → ≥2 days → ≥7 days → ≥14 days → Active Minter) and the percentile latency to "came back" (second mint on a different day). Skips the trivial acceptance mint, which always fires.

    Model: `api_execution_circles_v2_invite_funnel_cohort_monthly` — table `dbt.api_execution_circles_v2_invite_funnel_cohort_monthly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `cohort_month` | `Date` | Month the cohort was invited (toStartOfMonth of invited_at); the row grain. |
    | `n_invited` | `UInt64` | Total invitees in this cohort. |
    | `n_minted_2_days` | `UInt64` | Invitees with >= 2 distinct mint days in the first 30 days. |
    | `n_minted_7_days` | `UInt64` | Invitees with >= 7 distinct mint days in the first 30 days. |
    | `n_minted_14_days` | `UInt64` | Invitees with >= 14 distinct mint days in the first 30 days. |
    | `n_active_minter` | `UInt64` | Invitees that ever reached canonical Active Minter status (mint_days_14dw = 14 AND mint_14dw >= 80% of 336). |
    | `pct_minted_2_days` | `Float64` | n_minted_2_days / n_invited × 100, rounded to 1 decimal. |
    | `pct_minted_7_days` | `Float64` | n_minted_7_days / n_invited × 100, rounded to 1 decimal. |
    | `pct_minted_14_days` | `Float64` | n_minted_14_days / n_invited × 100, rounded to 1 decimal. |
    | `pct_active_minter` | `Float64` | n_active_minter / n_invited × 100, rounded to 1 decimal. |
    | `median_days_to_second_mint` | `Nullable(Int64)` | Median days from invite to the first mint on a different day. |
    | `p25_days_to_second_mint` | `Nullable(Int64)` | 25th-percentile days from invite to the first mint on a different day. |
    | `p75_days_to_second_mint` | `Nullable(Int64)` | 75th-percentile days from invite to the first mint on a different day. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_invite_funnel_cohort/monthly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_inviter_farm_quota

Inviter InvitationFarm leaderboard (invites claimed + current quota), ordered by invites_claimed. Passthrough over fct_execution_circles_v2_inviter_farm_quota with an as_of_date snapshot stamp.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_inviter_farm_quota/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_inviter_farm_quota/latest`"
    Inviter InvitationFarm leaderboard (invites claimed + current quota), ordered by invites_claimed. Passthrough over fct_execution_circles_v2_inviter_farm_quota with an as_of_date snapshot stamp.

    Model: `api_execution_circles_v2_inviter_farm_quota` — table `dbt.api_execution_circles_v2_inviter_farm_quota`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `inviter` | `String` | Lowercase inviter address. |
    | `invites_claimed` | `Int64` | Total invites claimed from the farm. |
    | `n_claim_events` | `UInt64` | Number of claim events. |
    | `current_quota` | `Nullable(Int64)` | Latest granted invite quota; NULL if never set. |
    | `first_claim_at` | `Nullable(DateTime)` | First claim timestamp; NULL if none. |
    | `last_claim_at` | `Nullable(DateTime)` | Most recent claim timestamp; NULL if none. |
    | `quota_updated_at` | `Nullable(DateTime)` | Latest quota-update timestamp; NULL if none. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max InvitationFarm event date). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_inviter_farm_quota/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_inviters_ranking

Top-N inviters leaderboard ordered by number of human avatars invited. Pre-joins the inviter's display name, preview image URL (IPFS profile), and current blacklist flag so the dashboard renders the table directly.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_inviters_ranking/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_inviters_ranking/latest`"
    Top-N inviters leaderboard ordered by number of human avatars invited. Pre-joins the inviter's display name, preview image URL (IPFS profile), and current blacklist flag so the dashboard renders the table directly.

    Model: `api_execution_circles_v2_inviters_ranking` — table `dbt.api_execution_circles_v2_inviters_ranking`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `rank` | `UInt64` | Leaderboard rank by invite count (1 = most invites). |
    | `inviter` | `String` | Lowercase inviter avatar address. |
    | `display_name` | `String` | IPFS profile display name (empty string when unset). |
    | `preview_image_url` | `String` | IPFS profile previewImageUrl (empty string when unset). |
    | `is_blacklisted` | `Bool` | True iff the address appears in stg_crawlers_data__circles_blacklisted at build time. |
    | `invite_count` | `UInt64` | Total humans invited. |
    | `first_invite_ts` | `DateTime` | Timestamp of the first invite. |
    | `last_invite_ts` | `DateTime` | Timestamp of the most recent invite. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_inviters_ranking/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_kpi_active_minters

KPI: yesterday's Active Minters count with WoW pct change.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_kpi_active_minters/latest` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_kpi_active_minters/latest`"
    KPI: yesterday's Active Minters count with WoW pct change.

    Model: `api_execution_circles_v2_kpi_active_minters_latest` — table `dbt.api_execution_circles_v2_kpi_active_minters_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `UInt64` | Active Minters count on the latest complete day. |
    | `change_pct` | `Nullable(Float64)` | Percent change vs the count 7 days earlier. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_kpi_active_minters/latest"
    ```

## circles_v2_kpi_avg_members_per_group

KPI: average and median members per group.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_kpi_avg_members_per_group/latest` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_kpi_avg_members_per_group/latest`"
    KPI: average and median members per group.

    Model: `api_execution_circles_v2_kpi_avg_members_per_group_latest` — table `dbt.api_execution_circles_v2_kpi_avg_members_per_group_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Nullable(Float64)` | Average member count across all groups |
    | `median_members` | `Float64` | Median member count across all groups. |
    | `change_pct` | `Nullable(Float64)` | Always NULL — no time series for group size upstream |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_kpi_avg_members_per_group/latest"
    ```

## circles_v2_kpi_avg_trusts_per_avatar

KPI: average trusts per human avatar = active_trusts / humans. Network-density indicator.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_kpi_avg_trusts_per_avatar/latest` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_kpi_avg_trusts_per_avatar/latest`"
    KPI: average trusts per human avatar = active_trusts / humans. Network-density indicator.

    Model: `api_execution_circles_v2_kpi_avg_trusts_per_avatar_latest` — table `dbt.api_execution_circles_v2_kpi_avg_trusts_per_avatar_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | active_trusts / humans (rounded to 2 decimals). |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_kpi_avg_trusts_per_avatar/latest"
    ```

## circles_v2_kpi_depositors_in_backers_pct

KPI: % of depositors that ended up trusted by the backers group.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_kpi_depositors_in_backers_pct/latest` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_kpi_depositors_in_backers_pct/latest`"
    KPI: % of depositors that ended up trusted by the backers group.

    Model: `api_execution_circles_v2_kpi_depositors_in_backers_pct_latest` — table `dbt.api_execution_circles_v2_kpi_depositors_in_backers_pct_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Nullable(Float64)` | Percent of distinct depositors that are also trust-defined backers (depositors_in_backers / total_depositors × 100). |
    | `total_depositors` | `UInt64` | Total distinct depositor addresses. |
    | `depositors_in_backers` | `UInt64` | Depositors that are also trusted by the backers group. |
    | `change_pct` | `Nullable(Float64)` | Always NULL — no time series |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_kpi_depositors_in_backers_pct/latest"
    ```

## circles_v2_kpi_group_token_supply

KPI: aggregate group-token supply with 7d change.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_kpi_group_token_supply/latest` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_kpi_group_token_supply/latest`"
    KPI: aggregate group-token supply with 7d change.

    Model: `api_execution_circles_v2_kpi_group_token_supply_latest` — table `dbt.api_execution_circles_v2_kpi_group_token_supply_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | Latest aggregate group-token supply across all groups |
    | `change_pct` | `Nullable(Float64)` | Percent change vs the aggregate group-token supply 7 days earlier. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_kpi_group_token_supply/latest"
    ```

## circles_v2_kpi_group_wrapped_pct

KPI: share of group-token supply held as ERC-20 wrappers, with 7d delta.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_kpi_group_wrapped_pct/latest` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_kpi_group_wrapped_pct/latest`"
    KPI: share of group-token supply held as ERC-20 wrappers, with 7d delta.

    Model: `api_execution_circles_v2_kpi_group_wrapped_pct_latest` — table `dbt.api_execution_circles_v2_kpi_group_wrapped_pct_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Nullable(Float64)` | Latest share of aggregate group-token supply held as ERC-20 wrappers (percent |
    | `change_pct` | `Nullable(Float64)` | Percentage-point change vs the wrapped share 7 days earlier. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_kpi_group_wrapped_pct/latest"
    ```

## circles_v2_kpi_mints

KPI: total mints in the last 7 full days with WoW pct change.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_kpi_mints/last_7d/7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_kpi_mints/last_7d/7d`"
    KPI: total mints in the last 7 full days with WoW pct change.

    Model: `api_execution_circles_v2_kpi_mints_7d` — table `dbt.api_execution_circles_v2_kpi_mints_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `UInt64` | Total mint events in last 7 days. |
    | `amount` | `Float64` | Total CRC minted in last 7 days. |
    | `change_pct` | `Nullable(Float64)` | Percent change vs prior 7d window. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_kpi_mints/last_7d/7d"
    ```

## circles_v2_kpi_new_backers

KPI: backers newly trusted in the last 7 days with WoW change.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_kpi_new_backers/latest/7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_kpi_new_backers/latest/7d`"
    KPI: backers newly trusted in the last 7 days with WoW change.

    Model: `api_execution_circles_v2_kpi_new_backers_7d` — table `dbt.api_execution_circles_v2_kpi_new_backers_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `UInt64` | Backers newly trusted by the backers group in the last 7 days. |
    | `change_pct` | `Nullable(Float64)` | Percent change vs the prior 7-day window. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_kpi_new_backers/latest/7d"
    ```

## circles_v2_kpi_new_groups

KPI: groups registered in the last 7 days with WoW change.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_kpi_new_groups/latest/7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_kpi_new_groups/latest/7d`"
    KPI: groups registered in the last 7 days with WoW change.

    Model: `api_execution_circles_v2_kpi_new_groups_7d` — table `dbt.api_execution_circles_v2_kpi_new_groups_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `UInt64` | Groups registered in the last 7 days. |
    | `change_pct` | `Nullable(Float64)` | Percent change vs the prior 7-day window. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_kpi_new_groups/latest/7d"
    ```

## circles_v2_kpi_new_trusts

KPI: new trusts granted in the last 7 full days with WoW pct change.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_kpi_new_trusts/last_7d/7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_kpi_new_trusts/last_7d/7d`"
    KPI: new trusts granted in the last 7 full days with WoW pct change.

    Model: `api_execution_circles_v2_kpi_new_trusts_7d` — table `dbt.api_execution_circles_v2_kpi_new_trusts_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `UInt64` | Total new trusts in last 7 days. |
    | `revoked` | `UInt64` | Total revoked trusts in last 7 days. |
    | `change_pct` | `Nullable(Float64)` | Percent change in new trusts vs the prior 7-day window. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_kpi_new_trusts/last_7d/7d"
    ```

## circles_v2_kpi_total_backers

KPI: backers currently trusted by the backers group (revocation-aware), with 7d change.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_kpi_total_backers/latest` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_kpi_total_backers/latest`"
    KPI: backers currently trusted by the backers group (revocation-aware), with 7d change.

    Model: `api_execution_circles_v2_kpi_total_backers_latest` — table `dbt.api_execution_circles_v2_kpi_total_backers_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `UInt64` | Backers currently trusted by the backers group (countIf(is_currently_trusted), latest complete day) — revocation-aware, not the ever-backed cumulative total. |
    | `change_pct` | `Nullable(Float64)` | Percent change vs 7 days earlier. NOTE: computed off the ever-backed cumulative series as a growth proxy, so it slightly overstates growth when revocations o... |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_kpi_total_backers/latest"
    ```

## circles_v2_kpi_total_depositors

KPI: total distinct depositors with 7d-new and WoW change.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_kpi_total_depositors/latest` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_kpi_total_depositors/latest`"
    KPI: total distinct depositors with 7d-new and WoW change.

    Model: `api_execution_circles_v2_kpi_total_depositors_latest` — table `dbt.api_execution_circles_v2_kpi_total_depositors_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `UInt64` | Total distinct depositors (addresses that have emitted a CirclesBackingInitiated event). |
    | `new_last_7d` | `UInt64` | Depositors whose first initiation was in the last 7 days. |
    | `change_pct` | `Nullable(Float64)` | Percent change in newly-initiated depositors vs the prior 7-day window. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_kpi_total_depositors/latest"
    ```

## circles_v2_kpi_total_supply

KPI: latest network-wide CRC supply with 7-day pct change.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_kpi_total_supply/latest` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_kpi_total_supply/latest`"
    KPI: latest network-wide CRC supply with 7-day pct change.

    Model: `api_execution_circles_v2_kpi_total_supply_latest` — table `dbt.api_execution_circles_v2_kpi_total_supply_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | Latest total CRC supply (raw / 1e18). |
    | `change_pct` | `Nullable(Float64)` | Percent change vs the total supply 7 days earlier. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_kpi_total_supply/latest"
    ```

## circles_v2_minter_cohort

Time-series view over fct_execution_circles_v2_minter_cohort_daily; latest day excluded.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_minter_cohort/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_minter_cohort/daily`"
    Time-series view over fct_execution_circles_v2_minter_cohort_daily; latest day excluded.

    Model: `api_execution_circles_v2_minter_cohort_daily` — table `dbt.api_execution_circles_v2_minter_cohort_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day (UTC). |
    | `cohort` | `String` | Human-readable 14-day mint-coverage bucket label. |
    | `cohort_order` | `UInt8` | 1..6 ordering for stable stacking (low → high coverage). |
    | `cnt` | `UInt64` | Distinct avatars in this bucket on this day. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_minter_cohort/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_mints

Time-series view over int_execution_circles_v2_mints_daily; latest day excluded. One row per (date, mint_kind) — mint_kind separates personal mints from group mints and V1→V2 migrations; aggregate across kinds for the network-total grain.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_mints/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_mints/daily`"
    Time-series view over int_execution_circles_v2_mints_daily; latest day excluded. One row per (date, mint_kind) — mint_kind separates personal mints from group mints and V1→V2 migrations; aggregate across kinds for the network-total grain.

    Model: `api_execution_circles_v2_mints_daily` — table `dbt.api_execution_circles_v2_mints_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day (UTC). |
    | `mint_kind` | `String` | personal \| group \| migration \| other. |
    | `n_mint_events` | `UInt64` | Number of mint events for this (date, mint_kind). |
    | `n_minters` | `UInt64` | Distinct recipient addresses (to_address) for this (date, mint_kind). |
    | `amount_minted` | `Float64` | Total CRC minted for this (date, mint_kind) (raw / 1e18). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_mints/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_orgs_cnt

Latest count of organization avatars and 7-day percentage change.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_orgs_cnt/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_orgs_cnt/latest`"
    Latest count of organization avatars and 7-day percentage change.

    Model: `api_execution_circles_v2_orgs_cnt_latest` — table `dbt.api_execution_circles_v2_orgs_cnt_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `total` | `UInt64` | The total number of organization avatars at the latest date. |
    | `change_pct` | `Float64` | Percentage change in organization count compared to 7 days ago. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_orgs_cnt/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_p2p_velocity

Peer-to-peer transfer velocity (mint/burn/wrap/unwrap excluded).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_p2p_velocity/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_p2p_velocity/daily`"
    Peer-to-peer transfer velocity (mint/burn/wrap/unwrap excluded).

    Model: `api_execution_circles_v2_p2p_velocity_daily` — table `dbt.api_execution_circles_v2_p2p_velocity_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day (UTC). |
    | `n_transfers` | `UInt64` | Number of peer-to-peer transfers on this day. |
    | `n_senders` | `UInt64` | Distinct p2p sender addresses on this day. |
    | `n_receivers` | `UInt64` | Distinct p2p recipient addresses on this day. |
    | `amount` | `Float64` | Total p2p transfer volume in CRC (raw / 1e18). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_p2p_velocity/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_pool_explorer_liquidity

Daily count of liquidity events (Mint = 'Add', Burn = 'Remove') per Uniswap V3 Circles pool, deduped on (transaction_hash, log_index) so each add/remove event counts once. One row per day, pool, and event kind.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_pool_explorer_liquidity/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_pool_explorer_liquidity/daily`"
    Daily count of liquidity events (Mint = 'Add', Burn = 'Remove') per Uniswap V3 Circles pool, deduped on (transaction_hash, log_index) so each add/remove event counts once. One row per day, pool, and event kind.

    Model: `api_execution_circles_v2_pool_explorer_liquidity_daily` — table `dbt.api_execution_circles_v2_pool_explorer_liquidity_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day (UTC) of the liquidity events, derived from block_timestamp. |
    | `pool_address` | `String` | Lowercase 0x-prefixed address of the Uniswap V3 Circles liquidity pool. |
    | `event_kind` | `String` | Liquidity event kind: 'Add' for Mint events, 'Remove' otherwise (Burn). |
    | `n_events` | `UInt64` | Distinct count of liquidity events that day for the pool and event kind, deduped on (transaction_hash, log_index). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_pool_explorer_liquidity/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_pool_explorer_liquidity_events

Individual liquidity events (Mint mapped to Add, Burn to Remove) for the main Uniswap V3 Circles pools, one row per event, with each token amount added/removed, the USD value of the event, and the LP (position owner). Prices are resolved via daily ASOF carry-forward (CRC legs from the crc20 price...

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_pool_explorer_liquidity_events/snapshot` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_pool_explorer_liquidity_events/snapshot`"
    Individual liquidity events (Mint mapped to Add, Burn to Remove) for the main Uniswap V3 Circles pools, one row per event, with each token amount added/removed, the USD value of the event, and the LP (position owner). Prices are resolved via daily ASOF carry-forward (CRC legs from the crc20 price...

    Model: `api_execution_circles_v2_pool_explorer_liquidity_events` — table `dbt.api_execution_circles_v2_pool_explorer_liquidity_events`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `pool_address` | `String` | Lowercase 0x pool contract address of the Uniswap V3 Circles pool the event belongs to. |
    | `ts` | `DateTime` | Block timestamp of the liquidity event (UTC); serves as the freshness column. |
    | `tx_hash` | `String` | Transaction hash of the liquidity event. |
    | `event_kind` | `String` | Liquidity action: 'Add' for Mint events, 'Remove' for Burn events. |
    | `token0_symbol` | `String` | Human-readable symbol of pool token0 (sDAI, EURe, s-gCRC, s-CBG, or an address prefix fallback). |
    | `amount0` | `Float64` | Amount of token0 added or removed in the event, scaled to whole units (divided by 1e18). |
    | `token1_symbol` | `String` | Human-readable symbol of pool token1 (sDAI, EURe, s-gCRC, s-CBG, or an address prefix fallback). |
    | `amount1` | `Float64` | Amount of token1 added or removed in the event, scaled to whole units (divided by 1e18). |
    | `amount_usd` | `Float64` | Total USD value of the event across both token legs, using ASOF carry-forward prices (0 when unpriced). |
    | `lp` | `String` | Lowercase 0x address of the liquidity provider (position owner) for the event. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_pool_explorer_liquidity_events/snapshot" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_pool_explorer_swaps

Daily swap activity per main Circles DEX pool tracked in the Pool Explorer: number of swaps, total USD volume, and distinct trader count, scoped to the curated set of liquidity pools.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_pool_explorer_swaps/daily` | GET | tier1 | -- | -- | -- |
| `/v1/execution/circles_v2_pool_explorer_swaps/snapshot` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_pool_explorer_swaps/daily`"
    Daily swap activity per main Circles DEX pool tracked in the Pool Explorer: number of swaps, total USD volume, and distinct trader count, scoped to the curated set of liquidity pools.

    Model: `api_execution_circles_v2_pool_explorer_swaps_daily` — table `dbt.api_execution_circles_v2_pool_explorer_swaps_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day of the swap activity (UTC), derived from block_timestamp. |
    | `pool_address` | `String` | Lower-cased liquidity pool contract address. |
    | `n_swaps` | `UInt64` | Number of swaps executed in the pool that day. |
    | `volume_usd` | `Float64` | Total swap volume in USD for the pool that day. |
    | `n_traders` | `UInt64` | Distinct traders (taker, falling back to tx sender) that day. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_pool_explorer_swaps/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/circles_v2_pool_explorer_swaps/snapshot`"
    Individual recent swaps executed on the main Circles v2 DEX pools, scoped to the curated liquidity pools for the Pool Explorer swaps table. One row per trade with the pool, timestamp, transaction hash, tokens and amounts on each side, USD value, and the trader address.

    Model: `api_execution_circles_v2_pool_explorer_swaps` — table `dbt.api_execution_circles_v2_pool_explorer_swaps`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `pool_address` | `String` | Lower-cased address of the Circles DEX pool the swap occurred in. |
    | `ts` | `DateTime` | Block timestamp of the swap (UTC); serves as the freshness column. |
    | `tx_hash` | `String` | Transaction hash of the swap. |
    | `token_sold` | `String` | Symbol of the token sold (input side) in the swap. |
    | `amount_sold` | `Float64` | Amount of the token sold (input side). |
    | `token_bought` | `String` | Symbol of the token bought (output side) in the swap. |
    | `amount_bought` | `Float64` | Amount of the token bought (output side). |
    | `amount_usd` | `Nullable(Float64)` | USD value of the swap; null when no price is available. |
    | `trader` | `String` | Trader address, taken as the taker if present else the transaction sender. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_pool_explorer_swaps/snapshot" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_pool_search

Point-in-time (pool_address, display_name) lookup of Circles v2 liquidity pools that backs the Pool Explorer filter dropdown. Returns one row per known pool with its lowercased contract address and human-readable label.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_pool_search/snapshot` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_pool_search/snapshot`"
    Point-in-time (pool_address, display_name) lookup of Circles v2 liquidity pools that backs the Pool Explorer filter dropdown. Returns one row per known pool with its lowercased contract address and human-readable label.

    Model: `api_execution_circles_v2_pool_search` — table `dbt.api_execution_circles_v2_pool_search`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Snapshot date the lookup was generated (today(), UTC). |
    | `pool_address` | `String` | Lowercased Circles liquidity pool contract address. |
    | `display_name` | `String` | Human-readable pool label shown in the Pool Explorer dropdown. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_pool_search/snapshot" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_pools

One row per main Circles DEX pool: latest TVL plus trailing-7d volume, trades, distinct traders and fees. Backs the Liquidity KPI tiles and pools leaderboard.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_pools/latest` | GET | tier1 | -- | -- | -- |
| `/v1/execution/circles_v2_pools/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_pools/latest`"
    One row per main Circles DEX pool: latest TVL plus trailing-7d volume, trades, distinct traders and fees. Backs the Liquidity KPI tiles and pools leaderboard.

    Model: `api_execution_circles_v2_pools_latest` — table `dbt.api_execution_circles_v2_pools_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Date the snapshot is computed as of (query date |
    | `pool_address` | `String` | Pool contract address (lowercase). |
    | `pool` | `String` | Human-readable pool label (token pair). |
    | `protocol` | `Nullable(String)` | DEX protocol (Uniswap V3). |
    | `tvl_usd` | `Nullable(Float64)` | Most recent daily TVL in USD. |
    | `volume_7d` | `Float64` | Trailing-7d trading volume in USD. |
    | `trades_7d` | `UInt64` | Trailing-7d swap count. |
    | `traders_7d` | `UInt64` | Trailing-7d distinct traders (deduplicated across days). |
    | `fees_7d` | `Float64` | Trailing-7d fees in USD. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_pools/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/circles_v2_pools/daily`"
    Daily liquidity/market metrics for the main Circles DEX pools (seed circles_liquidity_pools), one row per (date, pool). Sourced from int_execution_pools_metrics_daily; current incomplete day excluded.

    Model: `api_execution_circles_v2_pools_daily` — table `dbt.api_execution_circles_v2_pools_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day (UTC). |
    | `pool` | `String` | Human-readable pool label (token pair). |
    | `pool_address` | `String` | Pool contract address (lowercase). |
    | `protocol` | `String` | DEX protocol (Uniswap V3). |
    | `tvl_usd` | `Nullable(Float64)` | Total value locked in USD. |
    | `volume_usd` | `Float64` | Daily trading volume in USD. |
    | `fees_usd` | `Float64` | Daily accrued fees in USD. |
    | `swap_count` | `UInt64` | Number of Swap events on this pool on this day. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_pools/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_pools_reserves

Latest per-(pool, token) reserve, token USD price and TVL for the main Circles DEX pools. Emits two rows per pool (one per leg), backing the pool-reserves card.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_pools_reserves/latest` | GET | tier1 | -- | -- | -- |
| `/v1/execution/circles_v2_pools_reserves/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_pools_reserves/latest`"
    Latest per-(pool, token) reserve, token USD price and TVL for the main Circles DEX pools. Emits two rows per pool (one per leg), backing the pool-reserves card.

    Model: `api_execution_circles_v2_pools_reserves_latest` — table `dbt.api_execution_circles_v2_pools_reserves_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Freshness date the row was materialized (today, UTC). |
    | `pool` | `String` | Human-readable pool label. |
    | `pool_address` | `String` | On-chain address of the DEX pool contract. |
    | `token_address` | `String` | On-chain address of the reserve token (one of the pool's two legs). |
    | `token_symbol` | `String` | Symbol of the reserve token. |
    | `reserve` | `Float64` | Latest reserve amount held for this token in the pool. |
    | `price_usd` | `Float64` | Latest USD price of the reserve token. |
    | `tvl_usd` | `Float64` | Latest USD value of this token's reserve (reserve x price). |
    | `as_of` | `Date` | Most recent source date the latest reserve/price/TVL values were observed. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_pools_reserves/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/circles_v2_pools_reserves/daily`"
    Daily USD total value locked (TVL) per main Circles DEX pool, computed as the sum of both token legs' USD value. Backs the reserves-over-time chart and the latest-TVL used by the KPI and leaderboard.

    Model: `api_execution_circles_v2_pools_reserves_daily` — table `dbt.api_execution_circles_v2_pools_reserves_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day (UTC). |
    | `pool` | `String` | Human-readable pool label. |
    | `pool_address` | `String` | Pool contract address. |
    | `tvl_usd` | `Float64` | Total value locked in the pool that day in USD (sum of both token legs, rounded to 2 decimals). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_pools_reserves/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_pools_reserves_token

Daily per-(pool, token) reserve balance and USD valuation for the main Circles DEX pools (Uniswap V3 and Balancer V3). Base model behind the TVL rollup, the reserves-over-time chart and the reserves card; prices come from a daily ASOF carry-forward and the current incomplete day is excluded.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_pools_reserves_token/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_pools_reserves_token/daily`"
    Daily per-(pool, token) reserve balance and USD valuation for the main Circles DEX pools (Uniswap V3 and Balancer V3). Base model behind the TVL rollup, the reserves-over-time chart and the reserves card; prices come from a daily ASOF carry-forward and the current incomplete day is excluded.

    Model: `api_execution_circles_v2_pools_reserves_token_daily` — table `dbt.api_execution_circles_v2_pools_reserves_token_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day (UTC). |
    | `pool` | `String` | Human-readable pool label. |
    | `pool_address` | `String` | Pool contract address (lowercased, 0x-prefixed). |
    | `token_address` | `String` | Reserve token contract address (lowercased). |
    | `token_symbol` | `String` | Human-readable token symbol (sDAI/EURe/s-gCRC/s-CBG, or the address prefix as fallback). |
    | `reserve` | `Float64` | Token reserve balance held by the pool that day (native token units). |
    | `price_usd` | `Nullable(Float64)` | ASOF carry-forward USD price for the token, falling back to the earliest observed price; may be null when the token is unpriced. |
    | `tvl_usd` | `Nullable(Float64)` | USD value of the reserve (reserve * price_usd); null when the token leg is unpriced. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_pools_reserves_token/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_pools_traders

Daily distinct traders and trade count per main Circles DEX pool. A trader is the swap taker (Swap recipient), falling back to the tx signer.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_pools_traders/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_pools_traders/daily`"
    Daily distinct traders and trade count per main Circles DEX pool. A trader is the swap taker (Swap recipient), falling back to the tx signer.

    Model: `api_execution_circles_v2_pools_traders_daily` — table `dbt.api_execution_circles_v2_pools_traders_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day (UTC). |
    | `pool` | `String` | Human-readable pool label (token pair). |
    | `pool_address` | `String` | Pool contract address (lowercase). |
    | `distinct_traders` | `UInt64` | Distinct traders active in the pool that day. |
    | `trades` | `UInt64` | Number of swaps in the pool that day. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_pools_traders/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_score_mints

Daily score-based mint activity per group: mint count, distinct minters, average member score at mint, and total group tokens minted. Current incomplete day excluded.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_score_mints/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_score_mints/daily`"
    Daily score-based mint activity per group: mint count, distinct minters, average member score at mint, and total group tokens minted. Current incomplete day excluded.

    Model: `api_execution_circles_v2_score_mints_daily` — table `dbt.api_execution_circles_v2_score_mints_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `group_address` | `String` | Lowercased group avatar address. |
    | `date` | `Date` | Calendar day (UTC). |
    | `n_mints` | `UInt64` | Number of score-based mints that day. |
    | `n_minters` | `UInt64` | Distinct minters that day. |
    | `avg_score` | `Float64` | Average member score at mint that day. |
    | `amount` | `Float64` | Total group tokens minted that day (CRC). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_score_mints/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_stats_current

Snapshot of network-level Circles v2 counts (avatars total + by type, active trusts, tokens, wrappers). One row per measure.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_stats_current/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_stats_current/latest`"
    Snapshot of network-level Circles v2 counts (avatars total + by type, active trusts, tokens, wrappers). One row per measure.

    Model: `api_execution_circles_v2_stats_current` — table `dbt.api_execution_circles_v2_stats_current`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `measure` | `String` | Measure name (avatar_count_v2 / human_count_v2 / group_count_v2 / org_count_v2 / active_trust_count_v2 / token_count_v2 / wrapper_count_v2). |
    | `value` | `UInt64` | Measure value. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_stats_current/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_supply_by_holder_type

API view of daily CRC supply breakdown by holder type (avatar type or Dune label sector).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_supply_by_holder_type/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_supply_by_holder_type/daily`"
    API view of daily CRC supply breakdown by holder type (avatar type or Dune label sector).

    Model: `api_execution_circles_v2_supply_by_holder_type_daily` — table `dbt.api_execution_circles_v2_supply_by_holder_type_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar date. |
    | `label` | `String` | Holder classification (Human, Group, Organization, DEX, Wallets and AA, etc.). |
    | `value` | `Float64` | Nominal supply held by this holder type in CRC. |
    | `value_demurraged` | `Float64` | Demurrage-adjusted supply held by this holder type in CRC. |
    | `holder_count` | `UInt64` | Number of distinct addresses in this holder type. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_supply_by_holder_type/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_total_supply

API view of daily network-wide CRC supply.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_total_supply/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_total_supply/daily`"
    API view of daily network-wide CRC supply.

    Model: `api_execution_circles_v2_total_supply_daily` — table `dbt.api_execution_circles_v2_total_supply_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar date. |
    | `value` | `Float64` | Total CRC supply (nominal). |
    | `value_demurraged` | `Float64` | Total CRC supply (demurrage-adjusted). |
    | `token_count` | `UInt64` | Number of distinct tokens with non-zero supply. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_total_supply/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_transfers

Time-series of Circles v2 transfers by category.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_transfers/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_transfers/daily`"
    Time-series of Circles v2 transfers by category.

    Model: `api_execution_circles_v2_transfers_daily` — table `dbt.api_execution_circles_v2_transfers_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day (UTC). |
    | `transfer_category` | `String` | Transfer category (mint / burn / wrap / unwrap / p2p). |
    | `n_transfers` | `UInt64` | Number of transfers in this category on this day. |
    | `n_senders` | `UInt64` | Distinct sender addresses in this category on this day (zero address excluded). |
    | `n_receivers` | `UInt64` | Distinct recipient addresses in this category on this day (zero address excluded). |
    | `amount` | `Float64` | Sum of native transfer amount in CRC (raw / 1e18). |
    | `amount_demurraged` | `Float64` | Sum of demurrage-adjusted transfer amount in CRC. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_transfers/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_trust_relations_current

API view of current active Circles v2 trust relations.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_trust_relations_current/snapshot` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_trust_relations_current/snapshot`"
    API view of current active Circles v2 trust relations.

    Model: `api_execution_circles_v2_trust_relations_current` — table `dbt.api_execution_circles_v2_trust_relations_current`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `truster` | `String` | Address of the avatar granting trust. |
    | `trustee` | `String` | Address of the avatar receiving trust. |
    | `valid_from` | `DateTime64` | Start timestamp of the trust relation validity period. |
    | `valid_to` | `DateTime64` | End timestamp of the trust relation validity period. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_trust_relations_current/snapshot" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_trusts

Time-series view over int_execution_circles_v2_trusts_daily; latest day excluded.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_trusts/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_trusts/daily`"
    Time-series view over int_execution_circles_v2_trusts_daily; latest day excluded.

    Model: `api_execution_circles_v2_trusts_daily` — table `dbt.api_execution_circles_v2_trusts_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day (UTC). |
    | `n_trust_events` | `UInt64` | Total Trust events on this day. |
    | `n_new_trusts` | `UInt64` | Events granting or extending trust (expiry > now). |
    | `n_revoked_trusts` | `UInt64` | Events setting expiry <= now (revoke). |
    | `n_distinct_trusters` | `UInt64` | Distinct truster addresses active that day. |
    | `n_distinct_trustees` | `UInt64` | Distinct trustee addresses active that day. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_trusts/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_trusts_distribution

Distribution histogram of trust degree (given / received) across avatars. Each row is a (direction, bucket) cell with the count of avatars whose trust degree falls in that bucket as of the latest complete day.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_trusts_distribution/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_trusts_distribution/latest`"
    Distribution histogram of trust degree (given / received) across avatars. Each row is a (direction, bucket) cell with the count of avatars whose trust degree falls in that bucket as of the latest complete day.

    Model: `api_execution_circles_v2_trusts_distribution` — table `dbt.api_execution_circles_v2_trusts_distribution`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `direction` | `String` | 'given' or 'received'. |
    | `trust_bucket` | `String` | Bucket label (0 / 1-5 / 6-10 / 11-25 / 26-50 / 51-100 / 100+). |
    | `avatar_count` | `UInt64` | Number of avatars in this bucket. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_trusts_distribution/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## circles_v2_wrapper_share

Network wrapped vs unwrapped supply share over time.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/circles_v2_wrapper_share/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/circles_v2_wrapper_share/daily`"
    Network wrapped vs unwrapped supply share over time.

    Model: `api_execution_circles_v2_wrapper_share_daily` — table `dbt.api_execution_circles_v2_wrapper_share_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day (UTC). |
    | `wrapped_supply` | `Float64` | Cumulative ERC-20 wrapped CRC across all wrappers on this day. |
    | `unwrapped_supply` | `Float64` | Native (unwrapped) CRC supply on this day (total_supply - wrapped_supply). |
    | `total_supply` | `Float64` | Network-wide total CRC supply on this day. |
    | `wrapped_pct` | `Nullable(Float64)` | wrapped_supply / total_supply × 100, rounded to 2 decimals. NULL when total_supply = 0. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/circles_v2_wrapper_share/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## cow_batch_metrics_ts

Daily average number of trades settled per CoW Protocol batch. Values above 1.0 indicate days where the solver matched multiple orders in a single settlement. On Gnosis Chain this peaked at ~2.8 in mid-2021 and has been near 1.0 since 2022, reflecting that most batches now contain a single trade ...

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/cow_batch_metrics_ts/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/cow_batch_metrics_ts/daily`"
    Daily average number of trades settled per CoW Protocol batch. Values above 1.0 indicate days where the solver matched multiple orders in a single settlement. On Gnosis Chain this peaked at ~2.8 in mid-2021 and has been near 1.0 since 2022, reflecting that most batches now contain a single trade ...

    Model: `api_execution_cow_batch_metrics_ts` — table `dbt.api_execution_cow_batch_metrics_ts`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day of the batch-metrics time series. |
    | `value` | `Float64` | Average trades per batch on this day. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/cow_batch_metrics_ts/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## cow_batch_routing_ts

Daily share of CoW Protocol settlement batches by routing type, as percentages of total daily batches. Three labels: "Pure CoW" (multi-trade batch with zero AMM interactions — true Coincidence of Wants), "Partial CoW" (multi-trade batch with some AMM interactions, meaning at least some peer match...

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/cow_batch_routing_ts/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/cow_batch_routing_ts/daily`"
    Daily share of CoW Protocol settlement batches by routing type, as percentages of total daily batches. Three labels: "Pure CoW" (multi-trade batch with zero AMM interactions — true Coincidence of Wants), "Partial CoW" (multi-trade batch with some AMM interactions, meaning at least some peer match...

    Model: `api_execution_cow_batch_routing_ts` — table `dbt.api_execution_cow_batch_routing_ts`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day of the batch-routing time series. |
    | `label` | `String` | 'Pure CoW' \| 'Partial CoW' \| 'Pure DEX'. |
    | `value` | `Float64` | Percentage of daily batches in this routing category (0–100). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/cow_batch_routing_ts/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## cow_fees_ts

Daily CoW Protocol revenue (USD) on Gnosis Chain. Filtered to fee_source = 'api' — surplus-based fees introduced Sep 2024. Pre-Sep 2024 on-chain feeAmount values are excluded: under CoW v1's fee-subsidy model that field represented the user's signed-maximum fee ceiling, not actual protocol revenu...

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/cow_fees_ts/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/cow_fees_ts/daily`"
    Daily CoW Protocol revenue (USD) on Gnosis Chain. Filtered to fee_source = 'api' — surplus-based fees introduced Sep 2024. Pre-Sep 2024 on-chain feeAmount values are excluded: under CoW v1's fee-subsidy model that field represented the user's signed-maximum fee ceiling, not actual protocol revenu...

    Model: `api_execution_cow_fees_ts` — table `dbt.api_execution_cow_fees_ts`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day of the fees time series. |
    | `value` | `Nullable(Float64)` | Daily USD fees collected via the surplus-based fee model. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/cow_fees_ts/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## cow_kpi_active_solvers

Number of distinct solvers that settled at least one batch in the last 7 complete days, with week-over-week change. Reflects who is actually competing for batches, not just who is allow-listed.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/cow_kpi_active_solvers/last_7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/cow_kpi_active_solvers/last_7d`"
    Number of distinct solvers that settled at least one batch in the last 7 complete days, with week-over-week change. Reflects who is actually competing for batches, not just who is allow-listed.

    Model: `api_execution_cow_kpi_active_solvers` — table `dbt.api_execution_cow_kpi_active_solvers`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `UInt64` | Distinct solvers with >=1 batch in the last 7 complete days. |
    | `change_pct` | `Nullable(Float64)` | Percentage change vs the prior 7-day window. |
    | `as_of_date` | `Date` | Last complete day reflected in the trailing 7-day window (today - 1). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/cow_kpi_active_solvers/last_7d"
    ```

## cow_kpi_fees

7-day CoW Protocol revenue (USD) with week-over-week change. Reflects surplus-based fees (fee_source = 'api', Sep 2024+). Pre-Sep 2024 on-chain feeAmount is excluded because those values represent signed-maximum under CoW v1's fee-subsidy model, not actual revenue.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/cow_kpi_fees/last_7d/7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/cow_kpi_fees/last_7d/7d`"
    7-day CoW Protocol revenue (USD) with week-over-week change. Reflects surplus-based fees (fee_source = 'api', Sep 2024+). Pre-Sep 2024 on-chain feeAmount is excluded because those values represent signed-maximum under CoW v1's fee-subsidy model, not actual revenue.

    Model: `api_execution_cow_kpi_fees_7d` — table `dbt.api_execution_cow_kpi_fees_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Nullable(Float64)` | Total api-sourced fees USD over the last 7 complete days. |
    | `change_pct` | `Nullable(Float64)` | Percentage change vs the prior 7-day window. |
    | `as_of_date` | `Date` | Last complete day reflected in the trailing 7-day window (today - 1). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/cow_kpi_fees/last_7d/7d"
    ```

## cow_kpi_solver_value

7-day gross solver value (USD) with week-over-week change. Covers priceImprovement and surplus fee policies (Sep 2024+).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/cow_kpi_solver_value/last_7d/7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/cow_kpi_solver_value/last_7d/7d`"
    7-day gross solver value (USD) with week-over-week change. Covers priceImprovement and surplus fee policies (Sep 2024+).

    Model: `api_execution_cow_kpi_solver_value_7d` — table `dbt.api_execution_cow_kpi_solver_value_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Nullable(Float64)` | Total solver-generated value (USD) over the last 7 complete days. |
    | `change_pct` | `Nullable(Float64)` | Percentage change vs the prior 7-day window. |
    | `as_of_date` | `Date` | Last complete day reflected in the trailing 7-day window (today - 1). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/cow_kpi_solver_value/last_7d/7d"
    ```

## cow_kpi_traders

7-day unique trader count (exact) with week-over-week change. Uses fct_execution_cow_trades directly for exact uniqExact across the window (daily uniques are not additive).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/cow_kpi_traders/last_7d/7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/cow_kpi_traders/last_7d/7d`"
    7-day unique trader count (exact) with week-over-week change. Uses fct_execution_cow_trades directly for exact uniqExact across the window (daily uniques are not additive).

    Model: `api_execution_cow_kpi_traders_7d` — table `dbt.api_execution_cow_kpi_traders_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `UInt64` | Distinct taker addresses over the last 7 complete days. |
    | `change_pct` | `Nullable(Float64)` | Percentage change vs the prior 7-day window. |
    | `as_of_date` | `Date` | Last complete day reflected in the trailing 7-day window (today - 1). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/cow_kpi_traders/last_7d/7d"
    ```

## cow_kpi_trades

7-day CoW Protocol trade count with week-over-week change.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/cow_kpi_trades/last_7d/7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/cow_kpi_trades/last_7d/7d`"
    7-day CoW Protocol trade count with week-over-week change.

    Model: `api_execution_cow_kpi_trades_7d` — table `dbt.api_execution_cow_kpi_trades_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `UInt64` | Total trades over the last 7 complete days. |
    | `change_pct` | `Nullable(Float64)` | Percentage change vs the prior 7-day window. |
    | `as_of_date` | `Date` | Last complete day reflected in the trailing 7-day window (today - 1). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/cow_kpi_trades/last_7d/7d"
    ```

## cow_kpi_volume

7-day CoW Protocol trading volume with week-over-week change.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/cow_kpi_volume/last_7d/7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/cow_kpi_volume/last_7d/7d`"
    7-day CoW Protocol trading volume with week-over-week change.

    Model: `api_execution_cow_kpi_volume_7d` — table `dbt.api_execution_cow_kpi_volume_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | Total USD volume over the last 7 complete days. |
    | `change_pct` | `Nullable(Float64)` | Percentage change vs the prior 7-day window. |
    | `as_of_date` | `Date` | Last complete day reflected in the trailing 7-day window (today - 1). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/cow_kpi_volume/last_7d/7d"
    ```

## cow_solver_value_ts

Daily gross value generated by CoW solvers on Gnosis Chain (USD). For each trade with a priceImprovement or surplus fee policy, this is the full value found beyond the reference price before the protocol takes its cut (solver_value_usd = fee_usd / surplus_factor). Sep 2024+ only.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/cow_solver_value_ts/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/cow_solver_value_ts/daily`"
    Daily gross value generated by CoW solvers on Gnosis Chain (USD). For each trade with a priceImprovement or surplus fee policy, this is the full value found beyond the reference price before the protocol takes its cut (solver_value_usd = fee_usd / surplus_factor). Sep 2024+ only.

    Model: `api_execution_cow_solver_value_ts` — table `dbt.api_execution_cow_solver_value_ts`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day of the solver-value time series. |
    | `value` | `Nullable(Float64)` | Daily USD solver-generated value. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/cow_solver_value_ts/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## cow_solvers_volume_ts

Daily volume by solver, top 6 by recent (180d) volume plus an "Other" bucket. Solver labels come from the cow_solvers seed when available; otherwise fall back to a truncated address. Uses a 180-day ranking window to surface currently active solvers rather than historically dominant but now-inacti...

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/cow_solvers_volume_ts/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/cow_solvers_volume_ts/daily`"
    Daily volume by solver, top 6 by recent (180d) volume plus an "Other" bucket. Solver labels come from the cow_solvers seed when available; otherwise fall back to a truncated address. Uses a 180-day ranking window to surface currently active solvers rather than historically dominant but now-inacti...

    Model: `api_execution_cow_solvers_volume_ts` — table `dbt.api_execution_cow_solvers_volume_ts`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day of the per-solver volume time series. |
    | `label` | `String` | Solver name (from seed) or truncated address, or "Other". |
    | `value` | `Nullable(Float64)` | Daily USD volume for this solver group. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/cow_solvers_volume_ts/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## cow_top_pairs

Weekly volume by top 8 directional token pairs (sold → bought), with remaining pairs grouped as "Other". Pair ranking uses lifetime volume.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/cow_top_pairs/weekly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/cow_top_pairs/weekly`"
    Weekly volume by top 8 directional token pairs (sold → bought), with remaining pairs grouped as "Other". Pair ranking uses lifetime volume.

    Model: `api_execution_cow_top_pairs_weekly` — table `dbt.api_execution_cow_top_pairs_weekly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Week start (Monday). |
    | `label` | `String` | Directional pair label, e.g. 'USDC.e → EURe', or 'Other'. |
    | `value` | `Nullable(Float64)` | Weekly USD volume for this pair group. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/cow_top_pairs/weekly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## cow_trades_ts

Daily CoW Protocol trade count.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/cow_trades_ts/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/cow_trades_ts/daily`"
    Daily CoW Protocol trade count.

    Model: `api_execution_cow_trades_ts` — table `dbt.api_execution_cow_trades_ts`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day of the trade-count time series. |
    | `value` | `UInt64` | Number of trades on this day. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/cow_trades_ts/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## cow_volume_ts

Daily CoW Protocol trading volume. Client-side time-range filtering applies via the dashboard's global selector.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/cow_volume_ts/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/cow_volume_ts/daily`"
    Daily CoW Protocol trading volume. Client-side time-range filtering applies via the dashboard's global selector.

    Model: `api_execution_cow_volume_ts` — table `dbt.api_execution_cow_volume_ts`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day of the volume time series. |
    | `value` | `Nullable(Float64)` | Daily USD volume. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/cow_volume_ts/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## execution_lending

Long-format daily APY series per (token, protocol) across Aave V3 and SparkLend. Each row pivots into one of two apy_type values ('Lending APY' or 'Borrow APY'). Drives the lending APY time-series chart on the lending dashboard.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/execution_lending/daily` | GET | tier1 | -- | -- | -- |
| `/v1/execution/execution_lending/snapshot` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/execution_lending/daily`"
    Long-format daily APY series per (token, protocol) across Aave V3 and SparkLend. Each row pivots into one of two apy_type values ('Lending APY' or 'Borrow APY'). Drives the lending APY time-series chart on the lending dashboard.

    Model: `api_execution_lending_daily` — table `dbt.api_execution_lending_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | -- |
    | `token` | `String` | Reserve token symbol. |
    | `token_class` | `String` | -- |
    | `label` | `String` | Lending protocol identifier ('Aave V3' or 'SparkLend'). |
    | `apy_type` | `String` | 'Lending APY' or 'Borrow APY'. |
    | `value` | `Float64` | APY for the row's apy_type. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/execution_lending/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/execution_lending/snapshot`"
    Latest lending TVL per reserve token on Gnosis (aggregated across Aave V3 and SparkLend) for pie chart display. Each row is a token with its total USD value locked across all protocols.

    Model: `api_execution_lending_tvl_by_token_latest` — table `dbt.api_execution_lending_tvl_by_token_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `token` | `String` | -- |
    | `value` | `Float64` | -- |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/execution_lending/snapshot" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## execution_lending_activity_counts

Weekly lender/borrower distinct user counts pivoted into long format for stacked-bar activity charts. One row per (week, token, protocol, activity_type), filtered to non-zero counts. Sourced from fct_execution_lending_weekly.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/execution_lending_activity_counts/weekly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/execution_lending_activity_counts/weekly`"
    Weekly lender/borrower distinct user counts pivoted into long format for stacked-bar activity charts. One row per (week, token, protocol, activity_type), filtered to non-zero counts. Sourced from fct_execution_lending_weekly.

    Model: `api_execution_lending_activity_counts_weekly` — table `dbt.api_execution_lending_activity_counts_weekly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Week start date. |
    | `token` | `String` | Reserve token symbol. |
    | `token_class` | `String` | -- |
    | `label` | `String` | Lending protocol identifier. |
    | `activity_type` | `String` | 'Lenders' or 'Borrowers'. |
    | `value` | `UInt64` | Distinct user count for the activity_type in the week. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/execution_lending_activity_counts/weekly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## execution_lending_activity_volumes

Weekly deposit/borrow volumes pivoted into long format for stacked-bar volume charts. One row per (week, token, protocol, volume_type), filtered to non-zero volumes. Sourced from fct_execution_lending_weekly.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/execution_lending_activity_volumes/weekly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/execution_lending_activity_volumes/weekly`"
    Weekly deposit/borrow volumes pivoted into long format for stacked-bar volume charts. One row per (week, token, protocol, volume_type), filtered to non-zero volumes. Sourced from fct_execution_lending_weekly.

    Model: `api_execution_lending_activity_volumes_weekly` — table `dbt.api_execution_lending_activity_volumes_weekly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Week start date. |
    | `token` | `String` | Reserve token symbol. |
    | `token_class` | `String` | -- |
    | `label` | `String` | Lending protocol identifier. |
    | `volume_type` | `String` | 'Deposits' or 'Borrows'. |
    | `value` | `Float64` | Total volume in native units for the volume_type in the week. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/execution_lending_activity_volumes/weekly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## execution_lending_balance_cohorts_holders

Daily lender count by balance cohort per (protocol, token) across Aave V3 and SparkLend. Stacked bar chart data showing holder count per balance bucket, filterable by token and protocol.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/execution_lending_balance_cohorts_holders/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/execution_lending_balance_cohorts_holders/daily`"
    Daily lender count by balance cohort per (protocol, token) across Aave V3 and SparkLend. Stacked bar chart data showing holder count per balance bucket, filterable by token and protocol.

    Model: `api_execution_lending_balance_cohorts_holders_daily` — table `dbt.api_execution_lending_balance_cohorts_holders_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | -- |
    | `protocol` | `String` | Lending protocol identifier. |
    | `token` | `String` | -- |
    | `cohort_unit` | `String` | -- |
    | `label` | `String` | Balance bucket label. |
    | `value` | `UInt64` | -- |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/execution_lending_balance_cohorts_holders/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## execution_lending_balance_cohorts_value

Daily lender balance cohort values per (protocol, token) across Aave V3 and SparkLend. Stacked bar chart data showing total USD and native value held by lenders in each balance bucket, filterable by token and protocol.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/execution_lending_balance_cohorts_value/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/execution_lending_balance_cohorts_value/daily`"
    Daily lender balance cohort values per (protocol, token) across Aave V3 and SparkLend. Stacked bar chart data showing total USD and native value held by lenders in each balance bucket, filterable by token and protocol.

    Model: `api_execution_lending_balance_cohorts_value_daily` — table `dbt.api_execution_lending_balance_cohorts_value_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | -- |
    | `protocol` | `String` | Lending protocol identifier. One of 'Aave V3' or 'SparkLend'. |
    | `token` | `String` | -- |
    | `cohort_unit` | `String` | -- |
    | `label` | `String` | Balance bucket label (e.g. '10-100', '1k-10k'). |
    | `value_native` | `Float64` | -- |
    | `value_usd` | `Float64` | -- |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/execution_lending_balance_cohorts_value/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## execution_lending_borrowers_count

KPI view of recently-active borrowers on Gnosis (Aave V3, SparkLend). IMPORTANT — this is a 7-day FLOW, not a stock: unique wallets that emitted a Borrow within the trailing 7 days (bitmap-merged from fct_execution_lending_latest, granularity:last_7d). It is NOT symmetric with api_execution_lendi...

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/execution_lending_borrowers_count/last_7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/execution_lending_borrowers_count/last_7d`"
    KPI view of recently-active borrowers on Gnosis (Aave V3, SparkLend). IMPORTANT — this is a 7-day FLOW, not a stock: unique wallets that emitted a Borrow within the trailing 7 days (bitmap-merged from fct_execution_lending_latest, granularity:last_7d). It is NOT symmetric with api_execution_lendi...

    Model: `api_execution_lending_borrowers_count_7d` — table `dbt.api_execution_lending_borrowers_count_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `token` | `String` | Always 'ALL' (no per-token slice exposed). |
    | `protocol` | `String` | Lending protocol identifier or 'ALL' for the cross-protocol aggregate. |
    | `value` | `Float64` | Distinct wallets that borrowed within the trailing 7 days (FLOW, not a debt-balance stock). |
    | `change_pct` | `Nullable(Float64)` | Percent change vs the count 7 days earlier (NULL when prior is zero or missing). |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/execution_lending_borrowers_count/last_7d"
    ```

## execution_lending_lenders_count

KPI view of currently-active lenders on Gnosis (Aave V3, SparkLend). "Active lenders" is a STOCK measure — unique wallets currently holding a positive supply balance in a lending market on Gnosis (point-in-time count), not a flow measure (users who supplied within a window). One row per protocol ...

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/execution_lending_lenders_count/latest` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/execution_lending_lenders_count/latest`"
    KPI view of currently-active lenders on Gnosis (Aave V3, SparkLend). "Active lenders" is a STOCK measure — unique wallets currently holding a positive supply balance in a lending market on Gnosis (point-in-time count), not a flow measure (users who supplied within a window). One row per protocol ...

    Model: `api_execution_lending_lenders_count_7d` — table `dbt.api_execution_lending_lenders_count_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `token` | `String` | Always 'ALL' (no per-token slice exposed in this view). |
    | `protocol` | `String` | Lending protocol identifier or 'ALL' for the cross-protocol aggregate. |
    | `value` | `Float64` | Distinct lender count with positive supply balance on the latest available date. |
    | `change_pct` | `Nullable(Float64)` | Percent change vs the count 7 days earlier (NULL when the prior value is zero or missing). |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/execution_lending_lenders_count/latest"
    ```

## execution_pools_fee_apr

API view for fee APR (7D trailing) time series by token and pool label (Uniswap V3/Swapr V3 only). Uses accrued fees from Swap + Flash (gross; independent of Collect/claims).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/execution_pools_fee_apr/daily/7d` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/execution_pools_fee_apr/daily/7d`"
    API view for fee APR (7D trailing) time series by token and pool label (Uniswap V3/Swapr V3 only). Uses accrued fees from Swap + Flash (gross; independent of Collect/claims).

    Model: `api_execution_pools_fee_apr_7d_daily` — table `dbt.api_execution_pools_fee_apr_7d_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day (UTC) of the fee APR time series. |
    | `token` | `String` | Token symbol the pool is grouped under. |
    | `label` | `String` | Pool display name. |
    | `apy_type` | `String` | Constant metric label ("Fee APR (7D trailing)") used as the chart series name. |
    | `value` | `Float64` | 7-day trailing fee APR (annualized, %) for the pool on this date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/execution_pools_fee_apr/daily/7d" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## execution_pools_fees_usd

API view for daily fee revenue (USD) by token and pool, sourced from fct_execution_pools_daily.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/execution_pools_fees_usd/daily` | GET | tier1 | -- | -- | -- |
| `/v1/execution/execution_pools_fees_usd/snapshot/7d` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/execution_pools_fees_usd/daily`"
    API view for daily fee revenue (USD) by token and pool, sourced from fct_execution_pools_daily.

    Model: `api_execution_pools_fees_usd_daily` — table `dbt.api_execution_pools_fees_usd_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day (UTC) of the fee revenue time series. |
    | `token` | `String` | Token symbol the pool is grouped under. |
    | `label` | `String` | Pool display name. |
    | `value` | `Float64` | Daily gross fee revenue in USD. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/execution_pools_fees_usd/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/execution_pools_fees_usd/snapshot/7d`"
    Per-token total LP fees over the last 7 days (snapshot) with 7-day-prior change. Sourced from fct_execution_pools_snapshots filtered to metric='Fees_7D'.

    Model: `api_execution_pools_fees_7d` — table `dbt.api_execution_pools_fees_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `token` | `String` | Token symbol the snapshot is aggregated for. |
    | `value` | `Float64` | 7-day total fees in USD for the token. |
    | `change_pct` | `Nullable(Float64)` | Percent change vs the previous 7-day window. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/execution_pools_fees_usd/snapshot/7d" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## execution_pools_lp_activity

API view for daily LP activity (Mint/Burn event counts) per pool per token, unpivoted into one row per event type for the BarChart seriesField. Reuses pool labels and top-pool filtering from fct_execution_pools_daily.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/execution_pools_lp_activity/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/execution_pools_lp_activity/daily`"
    API view for daily LP activity (Mint/Burn event counts) per pool per token, unpivoted into one row per event type for the BarChart seriesField. Reuses pool labels and top-pool filtering from fct_execution_pools_daily.

    Model: `api_execution_pools_lp_activity_daily` — table `dbt.api_execution_pools_lp_activity_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day (UTC) of the LP activity. |
    | `token` | `String` | Token symbol the pools are grouped under. |
    | `label` | `String` | Pool label (token pair, protocol, address suffix) from fct_execution_pools_daily. |
    | `type` | `String` | LP event type — 'Add' (Mint events) or 'Remove' (Burn events). |
    | `value` | `UInt64` | Count of LP events of this type across all pools containing this token on this day. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/execution_pools_lp_activity/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## execution_pools_lps_count

API view for unique LP provider count over the last 7 days per token.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/execution_pools_lps_count/last_7d` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/execution_pools_lps_count/last_7d`"
    API view for unique LP provider count over the last 7 days per token.

    Model: `api_execution_pools_lps_count_7d` — table `dbt.api_execution_pools_lps_count_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `token` | `String` | Token symbol the LP count is aggregated for. |
    | `value` | `Float64` | Unique LP addresses over the last 7 days across all pools containing this token. |
    | `change_pct` | `Float64` | Percentage change vs the prior 7-day window. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/execution_pools_lps_count/last_7d" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## execution_pools_net_apr

API view for net APR (fee APR plus LVR) time series by token and pool label, with fee APR and LVR components.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/execution_pools_net_apr/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/execution_pools_net_apr/daily`"
    API view for net APR (fee APR plus LVR) time series by token and pool label, with fee APR and LVR components.

    Model: `api_execution_pools_net_apr_daily` — table `dbt.api_execution_pools_net_apr_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day (UTC) of the APR time series. |
    | `token` | `String` | Token symbol the pool is grouped under. |
    | `label` | `String` | Pool display name. |
    | `fee_apr_7d` | `Float64` | 7-day trailing fee APR (annualized, %). |
    | `lvr_apr_7d` | `Float64` | Annualised 7-day Loss Versus Rebalancing (%). Always <= 0 (negative = loss). |
    | `net_apr_7d` | `Float64` | Net APR (fee_apr_7d + lvr_apr_7d), the estimated real return after LVR cost. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/execution_pools_net_apr/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## execution_pools_swap_count

API view for daily swap event count by token and pool, sourced from fct_execution_pools_daily.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/execution_pools_swap_count/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/execution_pools_swap_count/daily`"
    API view for daily swap event count by token and pool, sourced from fct_execution_pools_daily.

    Model: `api_execution_pools_swap_count_daily` — table `dbt.api_execution_pools_swap_count_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day (UTC) of the swap-count time series. |
    | `token` | `String` | Token symbol the pool is grouped under. |
    | `label` | `String` | Pool display name. |
    | `value` | `UInt64` | Number of Swap events on this pool on this day. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/execution_pools_swap_count/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## execution_pools_tvl_by_pool

Latest-day TVL breakdown per (token, pool) for the pools dashboard's drill-down chart. One row per pool with positive TVL on the latest available date (excluding today, which may be partial). Sourced from fct_execution_pools_daily.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/execution_pools_tvl_by_pool/snapshot` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/execution_pools_tvl_by_pool/snapshot`"
    Latest-day TVL breakdown per (token, pool) for the pools dashboard's drill-down chart. One row per pool with positive TVL on the latest available date (excluding today, which may be partial). Sourced from fct_execution_pools_daily.

    Model: `api_execution_pools_tvl_by_pool_latest` — table `dbt.api_execution_pools_tvl_by_pool_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `token` | `String` | Reference token symbol used to group pools. |
    | `label` | `String` | Pool display name (combines symbols, protocol, address suffix). |
    | `value` | `Float64` | Pool TVL in USD on the latest available date. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/execution_pools_tvl_by_pool/snapshot" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## execution_pools_tvl_token

Daily TVL time series per (token, pool) decomposed into the contribution of each pool side. Sourced from fct_execution_pools_tvl_token_daily. Drives the per-token TVL stacked-area chart.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/execution_pools_tvl_token/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/execution_pools_tvl_token/daily`"
    Daily TVL time series per (token, pool) decomposed into the contribution of each pool side. Sourced from fct_execution_pools_tvl_token_daily. Drives the per-token TVL stacked-area chart.

    Model: `api_execution_pools_tvl_token_daily` — table `dbt.api_execution_pools_tvl_token_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day (UTC) of the TVL time series. |
    | `token` | `String` | Reference token symbol (renamed from ref_token). |
    | `label` | `String` | Pool display name. |
    | `series` | `String` | Series identifier for stacking (typically the side of the pool the TVL is denominated in). |
    | `tvl_usd` | `Float64` | Component TVL in USD for this row. |
    | `tvl_in_token0` | `Nullable(Float64)` | Pool TVL portion attributable to token0 (native units). |
    | `tvl_in_token1` | `Nullable(Float64)` | Pool TVL portion attributable to token1 (native units). |
    | `token0_symbol` | `String` | Symbol of the pool's token0. |
    | `token1_symbol` | `String` | Symbol of the pool's token1. |
    | `token_amount` | `Nullable(Float64)` | Token-side balance for the reference token on this date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/execution_pools_tvl_token/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## execution_pools_tvl_usd

API view for pool TVL (USD) time series by token and pool label.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/execution_pools_tvl_usd/daily` | GET | tier1 | -- | -- | -- |
| `/v1/execution/execution_pools_tvl_usd/snapshot` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/execution_pools_tvl_usd/daily`"
    API view for pool TVL (USD) time series by token and pool label.

    Model: `api_execution_pools_tvl_daily` — table `dbt.api_execution_pools_tvl_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day (UTC) of the TVL time series. |
    | `token` | `String` | Token symbol the pool is grouped under. |
    | `label` | `String` | Pool display name. |
    | `tvl_type` | `String` | Constant metric label ("TVL (USD)") used as the chart series name. |
    | `value` | `Float64` | Pool TVL in USD on this date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/execution_pools_tvl_usd/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/execution_pools_tvl_usd/snapshot`"
    Latest TVL snapshot per token across all tracked DEX pools with 7-day change. Sourced from fct_execution_pools_snapshots filtered to metric='TVL_Latest'.

    Model: `api_execution_pools_tvl_latest` — table `dbt.api_execution_pools_tvl_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `token` | `String` | Token symbol the snapshot is aggregated for. |
    | `value` | `Float64` | Latest TVL in USD. |
    | `change_pct` | `Nullable(Float64)` | Percent change in TVL vs 7 days ago. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/execution_pools_tvl_usd/snapshot" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## execution_pools_volume_usd

API view for daily trading volume (USD) by token and pool, sourced from fct_execution_pools_daily.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/execution_pools_volume_usd/daily` | GET | tier1 | -- | -- | -- |
| `/v1/execution/execution_pools_volume_usd/snapshot/7d` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/execution_pools_volume_usd/daily`"
    API view for daily trading volume (USD) by token and pool, sourced from fct_execution_pools_daily.

    Model: `api_execution_pools_volume_daily` — table `dbt.api_execution_pools_volume_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day (UTC) of the volume time series. |
    | `token` | `String` | Token symbol the pool is grouped under. |
    | `label` | `String` | Pool display name. |
    | `volume_type` | `String` | Constant metric label ("Volume (USD)") used as the chart series name. |
    | `value` | `Float64` | Daily gross trading volume in USD. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/execution_pools_volume_usd/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/execution_pools_volume_usd/snapshot/7d`"
    API view for 7-day total trading volume per token (snapshot from fct_execution_pools_snapshots).

    Model: `api_execution_pools_volume_7d` — table `dbt.api_execution_pools_volume_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `token` | `String` | Token symbol the snapshot is aggregated for. |
    | `value` | `Float64` | Total trading volume (USD) over the last 7 days. |
    | `change_pct` | `Float64` | Percentage change vs prior 7-day window. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/execution_pools_volume_usd/snapshot/7d" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_active_users_incl_gpay

Gnosis App Daily Active Users (DAU), Gnosis-Pay-inclusive variant over fct_execution_gnosis_app_users_daily_incl_gpay. Daily-grain member of the active-users-incl-gpay resolution triplet. Latest incomplete day (today) excluded.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_active_users_incl_gpay/daily` | GET | tier1 | `start_date`, `end_date` | -- | date DESC |
| `/v1/execution/gnosis_app_active_users_incl_gpay/weekly` | GET | tier1 | `start_date`, `end_date` | -- | week DESC |
| `/v1/execution/gnosis_app_active_users_incl_gpay/monthly` | GET | tier1 | `start_date`, `end_date` | -- | month DESC |

??? info "`GET /v1/execution/gnosis_app_active_users_incl_gpay/daily`"
    Gnosis App Daily Active Users (DAU), Gnosis-Pay-inclusive variant over fct_execution_gnosis_app_users_daily_incl_gpay. Daily-grain member of the active-users-incl-gpay resolution triplet. Latest incomplete day (today) excluded.

    Model: `api_execution_gnosis_app_active_users_incl_gpay_daily` — table `dbt.api_execution_gnosis_app_active_users_incl_gpay_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar date (UTC). Time-series grain. |
    | `active_users` | `UInt64` | Distinct active Gnosis App users on this date, additionally including GA owners whose only activity was a Gnosis Pay card-wallet transaction. |
    | `new_users` | `UInt64` | Users whose first-ever activity (onboarding) was on this date. |
    | `returning_users` | `UInt64` | Active this date AND active in the prior 7 days. |
    | `reactivated_users` | `UInt64` | Active this date, not active in the prior 30 days, but active earlier. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_active_users_incl_gpay/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/gnosis_app_active_users_incl_gpay/weekly`"
    Gnosis App Weekly Active Users (WAU), Gnosis-Pay-inclusive variant over fct_execution_gnosis_app_users_weekly_incl_gpay. Resolution-suffixed twin of api_execution_gnosis_app_weekly_active_users_incl_gpay; weekly-grain member of the active-users-incl-gpay resolution triplet. Latest incomplete week...

    Model: `api_execution_gnosis_app_active_users_incl_gpay_weekly` — table `dbt.api_execution_gnosis_app_active_users_incl_gpay_weekly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `start_date` | `>=` | `week` | date | Inclusive start week |
    | `end_date` | `<=` | `week` | date | Inclusive end week |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `week DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | Monday-aligned start of the week (UTC). Time-series grain. |
    | `active_users` | `UInt64` | Distinct active Gnosis App users in the week, additionally including GA owners whose only activity was a Gnosis Pay card-wallet transaction. |
    | `new_users` | `UInt64` | Users whose first-ever activity (onboarding) was this week. |
    | `returning_users` | `UInt64` | Active this week AND active the previous week. |
    | `reactivated_users` | `UInt64` | Active this week, not active in the prior 4 weeks, but active earlier. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_active_users_incl_gpay/weekly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/gnosis_app_active_users_incl_gpay/monthly`"
    Gnosis App Monthly Active Users (MAU), Gnosis-Pay-inclusive variant over fct_execution_gnosis_app_users_monthly_incl_gpay. Monthly-grain member of the active-users-incl-gpay resolution triplet. Latest incomplete month excluded.

    Model: `api_execution_gnosis_app_active_users_incl_gpay_monthly` — table `dbt.api_execution_gnosis_app_active_users_incl_gpay_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `start_date` | `>=` | `month` | date | Inclusive start month |
    | `end_date` | `<=` | `month` | date | Inclusive end month |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `month` | `Date` | First day of the month (UTC). Time-series grain. |
    | `active_users` | `UInt64` | Distinct active Gnosis App users in the month, additionally including GA owners whose only activity was a Gnosis Pay card-wallet transaction. |
    | `new_users` | `UInt64` | Users whose first-ever activity (onboarding) was this month. |
    | `returning_users` | `UInt64` | Active this month AND active the previous month. |
    | `reactivated_users` | `UInt64` | Active this month, not active in the prior 2 months, but active earlier. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_active_users_incl_gpay/monthly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_activity_by_action

FastAPI view over fct_execution_gnosis_app_activity_by_action_daily. Params: activity_kind, start_date, end_date.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_activity_by_action/daily` | GET | tier1 | `activity_kind`, `start_date`, `end_date` | -- | date DESC |
| `/v1/execution/gnosis_app_activity_by_action/weekly` | GET | tier1 | `activity_kind`, `start_date`, `end_date` | -- | week DESC |
| `/v1/execution/gnosis_app_activity_by_action/monthly` | GET | tier1 | `activity_kind`, `start_month`, `end_month` | -- | month DESC |

??? info "`GET /v1/execution/gnosis_app_activity_by_action/daily`"
    FastAPI view over fct_execution_gnosis_app_activity_by_action_daily. Params: activity_kind, start_date, end_date.

    Model: `api_execution_gnosis_app_activity_by_action_daily` — table `dbt.api_execution_gnosis_app_activity_by_action_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `activity_kind` | `=` | `activity_kind` | string | Activity kind (onboard, swap_filled, topup, marketplace_buy, etc.) |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar date (UTC). |
    | `activity_kind` | `String` | Type of activity (swap_filled / topup / marketplace_buy / circles_* / ...). |
    | `n_events` | `UInt64` | Number of events. |
    | `n_users` | `UInt64` | Distinct users. |
    | `amount_usd` | `Nullable(Float64)` | USD amount. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_activity_by_action/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/gnosis_app_activity_by_action/weekly`"
    FastAPI view over fct_execution_gnosis_app_activity_by_action_weekly.

    Model: `api_execution_gnosis_app_activity_by_action_weekly` — table `dbt.api_execution_gnosis_app_activity_by_action_weekly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `activity_kind` | `=` | `activity_kind` | string | Activity kind |
    | `start_date` | `>=` | `week` | date | Inclusive start week |
    | `end_date` | `<=` | `week` | date | Inclusive end week |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `week DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | Monday-aligned start of the week (UTC). |
    | `activity_kind` | `String` | Type of activity (swap_filled / topup / marketplace_buy / circles_* / ...). |
    | `n_events` | `UInt64` | Number of events. |
    | `n_users` | `UInt64` | Distinct users. |
    | `amount_usd` | `Nullable(Float64)` | USD amount. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_activity_by_action/weekly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/gnosis_app_activity_by_action/monthly`"
    FastAPI view over fct_execution_gnosis_app_activity_by_action_monthly.

    Model: `api_execution_gnosis_app_activity_by_action_monthly` — table `dbt.api_execution_gnosis_app_activity_by_action_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `activity_kind` | `=` | `activity_kind` | string | Activity kind |
    | `start_month` | `>=` | `month` | date | Inclusive start month |
    | `end_month` | `<=` | `month` | date | Inclusive end month |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `month` | `Date` | First day of the month (UTC). |
    | `activity_kind` | `String` | Type of activity (swap_filled / topup / marketplace_buy / circles_* / ...). |
    | `n_events` | `UInt64` | Number of events. |
    | `n_users` | `UInt64` | Distinct users. |
    | `amount_usd` | `Nullable(Float64)` | USD amount. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_activity_by_action/monthly?start_month=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_churn

FastAPI view over fct_execution_gnosis_app_churn_monthly. Params: scope, start_month, end_month.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_churn/monthly` | GET | tier1 | `scope`, `start_month`, `end_month` | -- | month DESC |

??? info "`GET /v1/execution/gnosis_app_churn/monthly`"
    FastAPI view over fct_execution_gnosis_app_churn_monthly. Params: scope, start_month, end_month.

    Model: `api_execution_gnosis_app_churn_monthly` — table `dbt.api_execution_gnosis_app_churn_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `scope` | `=` | `scope` | string | 'Any' or 'Swap' |
    | `start_month` | `>=` | `month` | date | Inclusive start month |
    | `end_month` | `<=` | `month` | date | Inclusive end month |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `scope` | `String` | Metric scope label ('Any' or 'Swap'). |
    | `month` | `Date` | First day of the month (UTC). |
    | `new_users` | `UInt64` | Distinct addresses whose first-ever activity was in this month. |
    | `retained_users` | `UInt64` | Active in this month and the previous month. |
    | `returning_users` | `UInt64` | Active this month and also active in the immediately prior period. |
    | `churned_users` | `UInt64` | Active this month but not the next. |
    | `total_active` | `UInt64` | Total distinct active users in the month. |
    | `churn_rate` | `Float64` | Share of users churned into the next month (percent). |
    | `retention_rate` | `Float64` | Share of users retained into the next month (percent). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_churn/monthly?start_month=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_circles_ecosystem_weekly_active_users

Whole-Circles-network weekly active reach (NOT Gnosis App growth; that is api:gnosis_app_users weekly / api:gnosis_app_kpi_weekly_active_users). Time-series over fct_execution_gnosis_app_weekly_active_users_circles_ecosystem (latest week excluded).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_circles_ecosystem_weekly_active_users/weekly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_circles_ecosystem_weekly_active_users/weekly`"
    Whole-Circles-network weekly active reach (NOT Gnosis App growth; that is api:gnosis_app_users weekly / api:gnosis_app_kpi_weekly_active_users). Time-series over fct_execution_gnosis_app_weekly_active_users_circles_ecosystem (latest week excluded).

    Model: `api_execution_gnosis_app_circles_ecosystem_weekly_active_users` — table `dbt.api_execution_gnosis_app_circles_ecosystem_weekly_active_users`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | Monday-aligned start of the week (UTC). Time-series grain. |
    | `is_blacklisted` | `Bool` | True if the address appears in the circles blacklist snapshot. |
    | `cnt` | `UInt64` | Distinct ecosystem-active addresses in this week × blacklist bucket. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_circles_ecosystem_weekly_active_users/weekly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_gpay_topups

FastAPI view over fct_execution_gnosis_app_gpay_topups_weekly.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_gpay_topups/weekly` | GET | tier1 | `start_date`, `end_date` | -- | week DESC |
| `/v1/execution/gnosis_app_gpay_topups/monthly` | GET | tier1 | `start_month`, `end_month` | -- | month DESC |

??? info "`GET /v1/execution/gnosis_app_gpay_topups/weekly`"
    FastAPI view over fct_execution_gnosis_app_gpay_topups_weekly.

    Model: `api_execution_gnosis_app_gpay_topups_weekly` — table `dbt.api_execution_gnosis_app_gpay_topups_weekly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `start_date` | `>=` | `week` | date | Inclusive start week |
    | `end_date` | `<=` | `week` | date | Inclusive end week |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `week DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | Monday-aligned start of the week (UTC). |
    | `n_topups` | `UInt64` | Number of in-app top-up events. |
    | `n_ga_users` | `UInt64` | Distinct Gnosis App users. |
    | `n_gp_wallets` | `UInt64` | Distinct Gnosis Pay wallets. |
    | `volume_usd` | `Nullable(Float64)` | USD volume. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_gpay_topups/weekly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/gnosis_app_gpay_topups/monthly`"
    FastAPI view over fct_execution_gnosis_app_gpay_topups_monthly.

    Model: `api_execution_gnosis_app_gpay_topups_monthly` — table `dbt.api_execution_gnosis_app_gpay_topups_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `start_month` | `>=` | `month` | date | Inclusive start month |
    | `end_month` | `<=` | `month` | date | Inclusive end month |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `month` | `Date` | First day of the month (UTC). |
    | `n_topups` | `UInt64` | Number of in-app top-up events. |
    | `n_ga_users` | `UInt64` | Distinct Gnosis App users. |
    | `n_gp_wallets` | `UInt64` | Distinct Gnosis Pay wallets. |
    | `volume_usd` | `Nullable(Float64)` | USD volume. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_gpay_topups/monthly?start_month=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_gpay_topups_by_token

FastAPI endpoint view of fct_execution_gnosis_app_gpay_topups_by_token_daily. Supports query params: token_bought_symbol, start_date, end_date.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_gpay_topups_by_token/daily` | GET | tier1 | `token_bought_symbol`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/execution/gnosis_app_gpay_topups_by_token/daily`"
    FastAPI endpoint view of fct_execution_gnosis_app_gpay_topups_by_token_daily. Supports query params: token_bought_symbol, start_date, end_date.

    Model: `api_execution_gnosis_app_gpay_topups_by_token_daily` — table `dbt.api_execution_gnosis_app_gpay_topups_by_token_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token_bought_symbol` | `=` | `token_bought_symbol` | string | Bought token symbol (e.g. 'EURe', 'USDC') |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar date (UTC). |
    | `token_bought_symbol` | `Nullable(String)` | Symbol of the token bought. |
    | `n_topups` | `UInt64` | Number of in-app top-up events. |
    | `n_ga_users` | `UInt64` | Distinct Gnosis App users. |
    | `n_gp_wallets` | `UInt64` | Distinct Gnosis Pay wallets. |
    | `volume_token_bought` | `Nullable(Float64)` | Volume of the bought token in native units. |
    | `volume_usd` | `Nullable(Float64)` | USD volume. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_gpay_topups_by_token/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_gpay_topups_cohort

FastAPI view over fct_execution_gnosis_app_gpay_topups_cohort_monthly. Params: start_month, end_month.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_gpay_topups_cohort/monthly` | GET | tier1 | `start_month`, `end_month` | -- | cohort_month DESC |

??? info "`GET /v1/execution/gnosis_app_gpay_topups_cohort/monthly`"
    FastAPI view over fct_execution_gnosis_app_gpay_topups_cohort_monthly. Params: start_month, end_month.

    Model: `api_execution_gnosis_app_gpay_topups_cohort_monthly` — table `dbt.api_execution_gnosis_app_gpay_topups_cohort_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `start_month` | `>=` | `cohort_month` | date | Inclusive start cohort month |
    | `end_month` | `<=` | `cohort_month` | date | Inclusive end cohort month |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `cohort_month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `cohort_month` | `Date` | Month of the user's first top-up (cohort anchor). |
    | `x` | `String` | Activity month as a string (toString(activity_month)); x-axis of the retention grid. |
    | `y` | `String` | First-top-up cohort month as a string (toString(cohort_month)); y-axis of the retention grid. |
    | `retention_pct` | `Float64` | Share of the first-top-up cohort still topping up in activity_month (users / initial_users x 100). |
    | `value_abs` | `UInt64` | Distinct cohort users who topped up in this cell (renamed from users). |
    | `amount_retention_pct` | `Nullable(Float64)` | Retained USD amount as a share of the cohort's initial amount (x100). |
    | `value_usd` | `Nullable(Float64)` | USD amount (renamed from amount_usd). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_gpay_topups_cohort/monthly?start_month=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_gpay_volume

FastAPI endpoint view of fct_execution_gnosis_app_gpay_volume_daily. GA-controlled Gnosis Pay funding (funded_volume_usd) and card spend (spend_usd) per day, split by onboarding_class, with cumulative series. Supports query params: onboarding_class, start_date, end_date.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_gpay_volume/daily` | GET | tier1 | `onboarding_class`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/execution/gnosis_app_gpay_volume/daily`"
    FastAPI endpoint view of fct_execution_gnosis_app_gpay_volume_daily. GA-controlled Gnosis Pay funding (funded_volume_usd) and card spend (spend_usd) per day, split by onboarding_class, with cumulative series. Supports query params: onboarding_class, start_date, end_date.

    Model: `api_execution_gnosis_app_gpay_volume_daily` — table `dbt.api_execution_gnosis_app_gpay_volume_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `onboarding_class` | `=` | `onboarding_class` | string | Onboarding class ('onboarded_via_ga' or 'imported') |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar date (UTC). |
    | `onboarding_class` | `String` | 'onboarded_via_ga' or 'imported'. |
    | `funded_volume_usd` | `Float64` | USD inflows (Fiat Top Up + Crypto Deposit) on GA-controlled Safes. |
    | `spend_usd` | `Float64` | USD card payments (action=Payment) on GA-controlled Safes. |
    | `spend_count` | `UInt64` | Number of card Payment transactions. |
    | `spending_wallets` | `UInt64` | Distinct GA-controlled Safes that made a card payment. |
    | `funded_volume_cumulative_usd` | `Float64` | Running total of funded_volume_usd within onboarding_class. |
    | `spend_cumulative_usd` | `Float64` | Running total of spend_usd within onboarding_class. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_gpay_volume/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_gpay_wallets

FastAPI endpoint view of fct_execution_gnosis_app_gpay_wallets_daily. Supports query params: onboarding_class, start_date, end_date.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_gpay_wallets/daily` | GET | tier1 | `onboarding_class`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/execution/gnosis_app_gpay_wallets/daily`"
    FastAPI endpoint view of fct_execution_gnosis_app_gpay_wallets_daily. Supports query params: onboarding_class, start_date, end_date.

    Model: `api_execution_gnosis_app_gpay_wallets_daily` — table `dbt.api_execution_gnosis_app_gpay_wallets_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `onboarding_class` | `=` | `onboarding_class` | string | Onboarding class ('onboarded_via_ga' or 'imported') |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar date (UTC). |
    | `onboarding_class` | `String` | 'onboarded_via_ga' or 'imported'. |
    | `n_ga_wallets_new` | `UInt64` | GP wallets that became GA-owned for the first time on this date. |
    | `n_ga_wallets_cumulative` | `UInt64` | Running total of ever-GA-owned GP wallets. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_gpay_wallets/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_gt_active_wallets

Public DAU series (active app-engaged wallets per day). WAU/MAU in the underlying fct.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_gt_active_wallets/daily` | GET | tier2 | -- | -- | date DESC |

??? info "`GET /v1/execution/gnosis_app_gt_active_wallets/daily`"
    Public DAU series (active app-engaged wallets per day). WAU/MAU in the underlying fct.

    Model: `api_execution_gnosis_app_gt_active_wallets` — table `dbt.api_execution_gnosis_app_gt_active_wallets`

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day. |
    | `active_wallets` | `UInt64` | Distinct active wallets that day. |
    | `new_wallets` | `UInt64` | First-ever-active wallets that day. |
    | `active_wallets_app_tagged` | `UInt64` | App-feature-active wallets that day (heuristic-comparable). |
    | `new_wallets_app_tagged` | `UInt64` | First-app-tagged-active wallets that day. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_gt_active_wallets/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_gt_reconciliation

Public reconciliation snapshot — registered (GT registry) vs active (heuristic) containment.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_gt_reconciliation/total` | GET | tier2 | -- | -- | registry_containment DESC |

??? info "`GET /v1/execution/gnosis_app_gt_reconciliation/total`"
    Public reconciliation snapshot — registered (GT registry) vs active (heuristic) containment.

    Model: `api_execution_gnosis_app_gt_user_reconciliation` — table `dbt.api_execution_gnosis_app_gt_user_reconciliation`

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `registry_containment DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `heuristic_users` | `UInt64` | Distinct heuristic active-user addresses. |
    | `gt_registry_users` | `UInt64` | GT registry (gnosis_app_user) count. |
    | `gt_avatar_users` | `UInt64` | GT avatar (active spine) count. |
    | `heuristic_in_registry` | `UInt64` | Heuristic users present in the GT registry. |
    | `heuristic_in_avatar` | `UInt64` | Heuristic users present in the GT avatar spine. |
    | `heuristic_only_vs_registry` | `UInt64` | Heuristic users absent from the GT registry. |
    | `registry_containment` | `Float64` | heuristic_in_registry / heuristic_users (cutover gate >= 0.90). |
    | `avatar_containment` | `Float64` | heuristic_in_avatar / heuristic_users (expected ~1.0). |
    | `as_of_date` | `Date` | Snapshot date (query/build date). |
    | `gt_registered_active` | `UInt64` | Canonical GT active users (registry + any app-tagged action). |
    | `gt_registered_active_incl_circles` | `UInt64` | Broad variant incl. generic Circles actions + referrals (sizing only). |
    | `gt_active_in_heuristic` | `UInt64` | Registered-active identities also in the heuristic active set. |
    | `gt_active_missed_by_heuristic` | `UInt64` | Registered-active identities the current-app heuristic misses (legacy/Metri/non-current). |
    | `gt_active_legacy_only` | `UInt64` | Registered-active identities with only legacy (Metri) signals, no current-app signal. |
    | `active_vs_heuristic_ratio` | `Float64` | gt_registered_active / heuristic_users. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_gt_reconciliation/total" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_gt_referrals

Public referral metrics — earned ledger vs full invite graph.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_gt_referrals/total` | GET | tier2 | -- | -- | n_edges DESC |

??? info "`GET /v1/execution/gnosis_app_gt_referrals/total`"
    Public referral metrics — earned ledger vs full invite graph.

    Model: `api_execution_gnosis_app_gt_referrals` — table `dbt.api_execution_gnosis_app_gt_referrals`

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `n_edges DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `metric_scope` | `String` | earned \| full_invite_graph. |
    | `n_inviters` | `UInt64` | Distinct inviters. |
    | `n_invitees` | `UInt64` | Distinct invitees. |
    | `n_edges` | `UInt64` | Invite edges. |
    | `total_reward_crc` | `Nullable(Float64)` | Native CRC rewards (earned scope only). |
    | `total_reward_usd` | `Nullable(Float64)` | Permanently NULL (no CRC price feed). |
    | `as_of_date` | `Date` | Snapshot date (query/build date). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_gt_referrals/total" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_gt_swaps

Public swap counts by scope x CoW status enum.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_gt_swaps/total` | GET | tier2 | `app_scope` | -- | n_swaps DESC |

??? info "`GET /v1/execution/gnosis_app_gt_swaps/total`"
    Public swap counts by scope x CoW status enum.

    Model: `api_execution_gnosis_app_gt_swaps` — table `dbt.api_execution_gnosis_app_gt_swaps`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `app_scope` | `=` | `app_scope` | string | gnosis_app \| metri \| third_party \| unknown \| test |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `n_swaps DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `app_scope` | `String` | native \| all_cow. |
    | `status` | `String` | CoW order status enum. |
    | `n_swaps` | `UInt64` | Order count. |
    | `n_swappers` | `UInt64` | Distinct owners. |
    | `as_of_date` | `Date` | Snapshot date (query/build date). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_gt_swaps/total?app_scope=VALUE" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_gt_wallet_cohort_retention

Public acquisition-cohort retention matrix (point-in-time; as_of_date).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_gt_wallet_cohort_retention/total` | GET | tier2 | -- | -- | cohort_month DESC, month_index ASC |

??? info "`GET /v1/execution/gnosis_app_gt_wallet_cohort_retention/total`"
    Public acquisition-cohort retention matrix (point-in-time; as_of_date).

    Model: `api_execution_gnosis_app_gt_wallet_cohort_retention` — table `dbt.api_execution_gnosis_app_gt_wallet_cohort_retention`

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `cohort_month DESC`, `month_index ASC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `basis` | `String` | any_action \| app_tagged. |
    | `cohort_month` | `Date` | Acquisition cohort month. |
    | `month_index` | `Int32` | Months since acquisition. |
    | `retained_wallets` | `UInt64` | Retained wallets at this index. |
    | `cohort_size` | `UInt64` | Cohort denominator. |
    | `retention_pct` | `Float64` | retained / cohort_size. |
    | `as_of_date` | `Date` | Snapshot (build) date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_gt_wallet_cohort_retention/total" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_gt_wallet_metrics

Public per-wallet metric endpoint (pseudonym-only; curated lifecycle/engagement/trust/segment surface). Point-in-time (as_of_date).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_gt_wallet_metrics/latest` | GET | tier1 | `user_pseudonym`, `engagement_tier`, `app_generation` | -- | n_actions DESC |

??? info "`GET /v1/execution/gnosis_app_gt_wallet_metrics/latest`"
    Public per-wallet metric endpoint (pseudonym-only; curated lifecycle/engagement/trust/segment surface). Point-in-time (as_of_date).

    Model: `api_execution_gnosis_app_gt_wallet_metrics` — table `dbt.api_execution_gnosis_app_gt_wallet_metrics`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `user_pseudonym` | `=` | `user_pseudonym` | string | sipHash64 pseudonym (joinable to mixpanel/gpay/circles) |
    | `engagement_tier` | `=` | `engagement_tier` | string | inactive \| casual \| core \| power |
    | `app_generation` | `=` | `app_generation` | string | current \| legacy \| both \| none |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `n_actions DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `user_pseudonym` | `UInt64` | sipHash64 pseudonym (joinable to mixpanel/gpay/circles). |
    | `app_generation` | `String` | current \| legacy \| both \| none. |
    | `engagement_tier` | `String` | inactive \| casual \| core \| power. |
    | `is_registered_active` | `Bool` | Canonical active flag. |
    | `is_active_30d` | `Bool` | Active within 30 days. |
    | `is_active_90d` | `Bool` | Active within 90 days. |
    | `tenure_days` | `Nullable(Int64)` | Days between first and last action. |
    | `days_since_last_action` | `Nullable(Int64)` | Days since last action. |
    | `n_actions` | `UInt64` | Total on-chain actions. |
    | `app_action_breadth` | `UInt16` | Distinct app-tagged action types (0-8). |
    | `n_swaps_gnosis_app` | `UInt64` | Swaps under app.gnosis.io. |
    | `n_swaps_metri` | `UInt64` | Swaps under app.metri.xyz. |
    | `n_metri_transfer` | `UInt64` | MetriTransfer events. |
    | `n_personal_mint` | `UInt64` | PersonalMint (CRC claim) events. |
    | `n_cashback` | `UInt64` | Cashback NFT mints. |
    | `n_investment` | `UInt64` | Metri auto-invest accounts. |
    | `n_invitees` | `UInt64` | Distinct invitees referred. |
    | `trusts_given` | `Int64` | Trust out-degree. |
    | `trusts_received` | `Int64` | Trust in-degree. |
    | `trusts_mutual` | `Int64` | Mutual trust count. |
    | `referral_crc_earned` | `Float64` | CRC earned as inviter. |
    | `earned_from_invites_crc` | `Float64` | Lifetime CRC from invites. |
    | `is_gp_card_user` | `Bool` | Linked to a GP card. |
    | `is_investor` | `Bool` | Owns an auto-invest account. |
    | `is_power_user` | `Bool` | High-breadth + recently active. |
    | `circles_version` | `Nullable(Int32)` | Avatar Circles version (1/2). |
    | `as_of_date` | `Date` | Snapshot (build) date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_gt_wallet_metrics/latest?user_pseudonym=VALUE" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_kpi_churn_rate

KPI: latest-month 'Any'-scope churn rate.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_kpi_churn_rate/last_month` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_kpi_churn_rate/last_month`"
    KPI: latest-month 'Any'-scope churn rate.

    Model: `api_execution_gnosis_app_kpi_churn_rate_latest` — table `dbt.api_execution_gnosis_app_kpi_churn_rate_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_kpi_churn_rate/last_month"
    ```

## gnosis_app_kpi_dau

KPI: DAU yesterday with pct change vs the day before.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_kpi_dau/last_day` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_kpi_dau/last_day`"
    KPI: DAU yesterday with pct change vs the day before.

    Model: `api_execution_gnosis_app_kpi_dau_latest` — table `dbt.api_execution_gnosis_app_kpi_dau_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_kpi_dau/last_day"
    ```

## gnosis_app_kpi_gp_wallets

KPI: count of GP wallets currently GA-owned.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_kpi_gp_wallets/snapshot` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_kpi_gp_wallets/snapshot`"
    KPI: count of GP wallets currently GA-owned.

    Model: `api_execution_gnosis_app_kpi_gp_wallets_latest` — table `dbt.api_execution_gnosis_app_kpi_gp_wallets_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_kpi_gp_wallets/snapshot"
    ```

## gnosis_app_kpi_gp_wallets_imported

KPI: cumulative GP wallets imported (pre-existing GP users who added GA).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_kpi_gp_wallets_imported/snapshot` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_kpi_gp_wallets_imported/snapshot`"
    KPI: cumulative GP wallets imported (pre-existing GP users who added GA).

    Model: `api_execution_gnosis_app_kpi_gp_wallets_imported` — table `dbt.api_execution_gnosis_app_kpi_gp_wallets_imported`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_kpi_gp_wallets_imported/snapshot"
    ```

## gnosis_app_kpi_gp_wallets_onboarded

KPI: cumulative GP wallets onboarded via Gnosis App.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_kpi_gp_wallets_onboarded/snapshot` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_kpi_gp_wallets_onboarded/snapshot`"
    KPI: cumulative GP wallets onboarded via Gnosis App.

    Model: `api_execution_gnosis_app_kpi_gp_wallets_onboarded` — table `dbt.api_execution_gnosis_app_kpi_gp_wallets_onboarded`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_kpi_gp_wallets_onboarded/snapshot"
    ```

## gnosis_app_kpi_marketplace_buys

KPI: marketplace buys in the last 7 full days.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_kpi_marketplace_buys/last_7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_kpi_marketplace_buys/last_7d`"
    KPI: marketplace buys in the last 7 full days.

    Model: `api_execution_gnosis_app_kpi_marketplace_buys_7d` — table `dbt.api_execution_gnosis_app_kpi_marketplace_buys_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_kpi_marketplace_buys/last_7d"
    ```

## gnosis_app_kpi_marketplace_buys_total

KPI: lifetime marketplace buys across all curated offers.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_kpi_marketplace_buys_total/snapshot` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_kpi_marketplace_buys_total/snapshot`"
    KPI: lifetime marketplace buys across all curated offers.

    Model: `api_execution_gnosis_app_kpi_marketplace_buys_total` — table `dbt.api_execution_gnosis_app_kpi_marketplace_buys_total`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_kpi_marketplace_buys_total/snapshot"
    ```

## gnosis_app_kpi_marketplace_payers

KPI: distinct marketplace payers in the last 7 full days.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_kpi_marketplace_payers/last_7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_kpi_marketplace_payers/last_7d`"
    KPI: distinct marketplace payers in the last 7 full days.

    Model: `api_execution_gnosis_app_kpi_marketplace_payers_7d` — table `dbt.api_execution_gnosis_app_kpi_marketplace_payers_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_kpi_marketplace_payers/last_7d"
    ```

## gnosis_app_kpi_mau

KPI: MAU for the latest complete month with pct change vs prior.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_kpi_mau/last_month` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_kpi_mau/last_month`"
    KPI: MAU for the latest complete month with pct change vs prior.

    Model: `api_execution_gnosis_app_kpi_mau_latest` — table `dbt.api_execution_gnosis_app_kpi_mau_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_kpi_mau/last_month"
    ```

## gnosis_app_kpi_new_users

KPI: new users in the last 7 full days with pct change vs prior 7d.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_kpi_new_users/last_7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_kpi_new_users/last_7d`"
    KPI: new users in the last 7 full days with pct change vs prior 7d.

    Model: `api_execution_gnosis_app_kpi_new_users_7d` — table `dbt.api_execution_gnosis_app_kpi_new_users_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_kpi_new_users/last_7d"
    ```

## gnosis_app_kpi_repeat_purchase_rate

KPI: share of last-30d active users with ≥2 swap_filled or marketplace_buy events.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_kpi_repeat_purchase_rate/last_30d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_kpi_repeat_purchase_rate/last_30d`"
    KPI: share of last-30d active users with ≥2 swap_filled or marketplace_buy events.

    Model: `api_execution_gnosis_app_kpi_repeat_purchase_rate_latest` — table `dbt.api_execution_gnosis_app_kpi_repeat_purchase_rate_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_kpi_repeat_purchase_rate/last_30d"
    ```

## gnosis_app_kpi_retention_pct

KPI: latest-cohort M1 retention %.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_kpi_retention_pct/last_month` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_kpi_retention_pct/last_month`"
    KPI: latest-cohort M1 retention %.

    Model: `api_execution_gnosis_app_kpi_retention_pct_latest` — table `dbt.api_execution_gnosis_app_kpi_retention_pct_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_kpi_retention_pct/last_month"
    ```

## gnosis_app_kpi_swap_fees

KPI: protocol fee revenue (USD) from filled swaps in last 7 full days with WoW pct change.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_kpi_swap_fees/last_7d/7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_kpi_swap_fees/last_7d/7d`"
    KPI: protocol fee revenue (USD) from filled swaps in last 7 full days with WoW pct change.

    Model: `api_execution_gnosis_app_kpi_swap_fees_7d` — table `dbt.api_execution_gnosis_app_kpi_swap_fees_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_kpi_swap_fees/last_7d/7d"
    ```

## gnosis_app_kpi_swap_volume

KPI: filled-swap USD volume in the last 7 full days.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_kpi_swap_volume/last_7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_kpi_swap_volume/last_7d`"
    KPI: filled-swap USD volume in the last 7 full days.

    Model: `api_execution_gnosis_app_kpi_swap_volume_7d` — table `dbt.api_execution_gnosis_app_kpi_swap_volume_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_kpi_swap_volume/last_7d"
    ```

## gnosis_app_kpi_swaps

KPI: signed swap count in the last 7 full days.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_kpi_swaps/last_7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_kpi_swaps/last_7d`"
    KPI: signed swap count in the last 7 full days.

    Model: `api_execution_gnosis_app_kpi_swaps_7d` — table `dbt.api_execution_gnosis_app_kpi_swaps_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_kpi_swaps/last_7d"
    ```

## gnosis_app_kpi_token_offer_claimers

KPI: distinct token-offer claimers in the last 7 full days.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_kpi_token_offer_claimers/last_7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_kpi_token_offer_claimers/last_7d`"
    KPI: distinct token-offer claimers in the last 7 full days.

    Model: `api_execution_gnosis_app_kpi_token_offer_claimers_7d` — table `dbt.api_execution_gnosis_app_kpi_token_offer_claimers_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_kpi_token_offer_claimers/last_7d"
    ```

## gnosis_app_kpi_token_offer_claims

KPI: token-offer claim count in the last 7 full days with pct change vs prior 7d.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_kpi_token_offer_claims/last_7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_kpi_token_offer_claims/last_7d`"
    KPI: token-offer claim count in the last 7 full days with pct change vs prior 7d.

    Model: `api_execution_gnosis_app_kpi_token_offer_claims_7d` — table `dbt.api_execution_gnosis_app_kpi_token_offer_claims_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_kpi_token_offer_claims/last_7d"
    ```

## gnosis_app_kpi_token_offer_volume

KPI: token-offer received-side USD volume in the last 7 full days.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_kpi_token_offer_volume/last_7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_kpi_token_offer_volume/last_7d`"
    KPI: token-offer received-side USD volume in the last 7 full days.

    Model: `api_execution_gnosis_app_kpi_token_offer_volume_7d` — table `dbt.api_execution_gnosis_app_kpi_token_offer_volume_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_kpi_token_offer_volume/last_7d"
    ```

## gnosis_app_kpi_topup_volume

KPI: topup USD volume in the last 7 full days.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_kpi_topup_volume/last_7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_kpi_topup_volume/last_7d`"
    KPI: topup USD volume in the last 7 full days.

    Model: `api_execution_gnosis_app_kpi_topup_volume_7d` — table `dbt.api_execution_gnosis_app_kpi_topup_volume_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_kpi_topup_volume/last_7d"
    ```

## gnosis_app_kpi_topups

KPI: topup count in the last 7 full days.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_kpi_topups/last_7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_kpi_topups/last_7d`"
    KPI: topup count in the last 7 full days.

    Model: `api_execution_gnosis_app_kpi_topups_7d` — table `dbt.api_execution_gnosis_app_kpi_topups_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_kpi_topups/last_7d"
    ```

## gnosis_app_kpi_total_users

KPI: total distinct GA users to date. Returns (value, change_pct).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_kpi_total_users/snapshot` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_kpi_total_users/snapshot`"
    KPI: total distinct GA users to date. Returns (value, change_pct).

    Model: `api_execution_gnosis_app_kpi_total_users` — table `dbt.api_execution_gnosis_app_kpi_total_users`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_kpi_total_users/snapshot"
    ```

## gnosis_app_kpi_wau

KPI: WAU for the latest complete week with pct change vs prior.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_kpi_wau/last_week` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_kpi_wau/last_week`"
    KPI: WAU for the latest complete week with pct change vs prior.

    Model: `api_execution_gnosis_app_kpi_wau_latest` — table `dbt.api_execution_gnosis_app_kpi_wau_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_kpi_wau/last_week"
    ```

## gnosis_app_kpi_weekly_active_users

KPI: latest complete week's Gnosis App WAU (Lineage A, fct_execution_gnosis_app_users_weekly.active_users — same population/columns as DAU & MAU) with WoW pct change.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_kpi_weekly_active_users/last_week` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_kpi_weekly_active_users/last_week`"
    KPI: latest complete week's Gnosis App WAU (Lineage A, fct_execution_gnosis_app_users_weekly.active_users — same population/columns as DAU & MAU) with WoW pct change.

    Model: `api_execution_gnosis_app_kpi_weekly_active_users_latest` — table `dbt.api_execution_gnosis_app_kpi_weekly_active_users_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_kpi_weekly_active_users/last_week"
    ```

## gnosis_app_kpi_weekly_economically_active_users

KPI: latest complete week's WEAU (non-blacklisted only) with WoW pct change.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_kpi_weekly_economically_active_users/last_week` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_kpi_weekly_economically_active_users/last_week`"
    KPI: latest complete week's WEAU (non-blacklisted only) with WoW pct change.

    Model: `api_execution_gnosis_app_kpi_weekly_economically_active_users_latest` — table `dbt.api_execution_gnosis_app_kpi_weekly_economically_active_users_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_kpi_weekly_economically_active_users/last_week"
    ```

## gnosis_app_marketplace_buys

FastAPI endpoint view of fct_execution_gnosis_app_marketplace_buys_daily. Supports query params: offer_name, start_date, end_date.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_marketplace_buys/daily` | GET | tier1 | `offer_name`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/execution/gnosis_app_marketplace_buys/daily`"
    FastAPI endpoint view of fct_execution_gnosis_app_marketplace_buys_daily. Supports query params: offer_name, start_date, end_date.

    Model: `api_execution_gnosis_app_marketplace_buys_daily` — table `dbt.api_execution_gnosis_app_marketplace_buys_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `offer_name` | `=` | `offer_name` | string | Offer name (as declared in createGateway) |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar date (UTC). |
    | `offer_name` | `String` | Human-readable offer name. |
    | `n_buys` | `UInt64` | Number of buy events. |
    | `n_payers` | `UInt64` | Distinct paying addresses. |
    | `volume_token` | `Nullable(Float64)` | Volume in native token units. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_marketplace_buys/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_marketplace_buys_cumulative

FastAPI endpoint view of fct_execution_gnosis_app_marketplace_buys_cumulative_daily. Supports query params: offer_name, start_date, end_date.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_marketplace_buys_cumulative/daily` | GET | tier1 | `offer_name`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/execution/gnosis_app_marketplace_buys_cumulative/daily`"
    FastAPI endpoint view of fct_execution_gnosis_app_marketplace_buys_cumulative_daily. Supports query params: offer_name, start_date, end_date.

    Model: `api_execution_gnosis_app_marketplace_buys_cumulative_daily` — table `dbt.api_execution_gnosis_app_marketplace_buys_cumulative_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `offer_name` | `=` | `offer_name` | string | Offer name |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar date (UTC). |
    | `offer_name` | `String` | Human-readable offer name. |
    | `n_buys` | `UInt64` | Number of buy events. |
    | `n_new_payers` | `UInt64` | Distinct addresses paying for the first time. |
    | `cumulative_buys` | `UInt64` | Running total of buys. |
    | `cumulative_payers` | `UInt64` | Running total of distinct payers. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_marketplace_buys_cumulative/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_marketplace_offers

FastAPI endpoint view of fct_execution_gnosis_app_marketplace_offers_latest. Supports query param: offer_name.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_marketplace_offers/snapshot` | GET | tier1 | `offer_name` | -- | total_buys DESC |

??? info "`GET /v1/execution/gnosis_app_marketplace_offers/snapshot`"
    FastAPI endpoint view of fct_execution_gnosis_app_marketplace_offers_latest. Supports query param: offer_name.

    Model: `api_execution_gnosis_app_marketplace_offers_latest` — table `dbt.api_execution_gnosis_app_marketplace_offers_latest`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `offer_name` | `=` | `offer_name` | string | Offer name |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `total_buys DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `offer_name` | `String` | Human-readable offer name. |
    | `gateway_address` | `String` | Payment gateway contract address. |
    | `created_at` | `DateTime` | Creation timestamp. |
    | `total_buys` | `UInt64` | Total buys. |
    | `total_payers` | `UInt64` | Total distinct payers. |
    | `first_buy_at` | `Nullable(DateTime)` | Timestamp of the address's first buy. |
    | `last_buy_at` | `Nullable(DateTime)` | Timestamp of the address's most recent buy. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_marketplace_offers/snapshot?offer_name=VALUE" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_purchase_freq_distribution

Distribution histogram of last-30d purchase counts per user (buckets 1/2/3/4-5/6-10/11+).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_purchase_freq_distribution/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_purchase_freq_distribution/latest`"
    Distribution histogram of last-30d purchase counts per user (buckets 1/2/3/4-5/6-10/11+).

    Model: `api_execution_gnosis_app_purchase_freq_distribution_latest` — table `dbt.api_execution_gnosis_app_purchase_freq_distribution_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_purchase_freq_distribution/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_retention

FastAPI view over fct_execution_gnosis_app_retention_monthly. Params: start_month, end_month.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_retention/monthly` | GET | tier1 | `start_month`, `end_month` | -- | cohort_month DESC |

??? info "`GET /v1/execution/gnosis_app_retention/monthly`"
    FastAPI view over fct_execution_gnosis_app_retention_monthly. Params: start_month, end_month.

    Model: `api_execution_gnosis_app_retention_monthly` — table `dbt.api_execution_gnosis_app_retention_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `start_month` | `>=` | `cohort_month` | date | Inclusive start cohort month |
    | `end_month` | `<=` | `cohort_month` | date | Inclusive end cohort month |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `cohort_month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `cohort_month` | `Date` | Onboard month (toStartOfMonth of the first 'onboard' row); the cohort anchor. |
    | `x` | `String` | Activity month as a string (toString(activity_month)); x-axis of the retention grid. |
    | `y` | `String` | Onboard cohort month as a string (toString(cohort_month)); y-axis of the retention grid. |
    | `retention_pct` | `Float64` | Share of the onboard cohort active in activity_month (users / initial_users x 100). |
    | `value_abs` | `UInt64` | Distinct cohort users active in this cell (renamed from users). |
    | `amount_retention_pct` | `Nullable(Float64)` | Activity USD as a share of the cohort's earliest activity-month USD (x100). |
    | `value_usd` | `Nullable(Float64)` | USD amount transacted by the cohort in activity_month (renamed from amount_usd). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_retention/monthly?start_month=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_retention_by_action

FastAPI view over fct_execution_gnosis_app_retention_by_action_monthly. Params: activity_kind, start_month, end_month.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_retention_by_action/monthly` | GET | tier1 | `activity_kind`, `start_month`, `end_month` | -- | cohort_month DESC |

??? info "`GET /v1/execution/gnosis_app_retention_by_action/monthly`"
    FastAPI view over fct_execution_gnosis_app_retention_by_action_monthly. Params: activity_kind, start_month, end_month.

    Model: `api_execution_gnosis_app_retention_by_action_monthly` — table `dbt.api_execution_gnosis_app_retention_by_action_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `activity_kind` | `=` | `activity_kind` | string | Activity kind to slice retention on |
    | `start_month` | `>=` | `cohort_month` | date | Inclusive start cohort month |
    | `end_month` | `<=` | `cohort_month` | date | Inclusive end cohort month |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `cohort_month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `cohort_month` | `Date` | Onboard month (first 'onboard' row); shared across all activity_kinds. |
    | `x` | `String` | Activity month as a string (toString(activity_month)); x-axis of the retention grid. |
    | `y` | `String` | Onboard cohort month as a string (toString(cohort_month)); y-axis of the retention grid. |
    | `activity_kind` | `String` | Type of activity the retention is sliced on (swap_filled / swap_signed / topup / marketplace_buy / token_offer_claim / circles_* / ...). |
    | `retention_pct` | `Float64` | Share of the onboard cohort doing this action in activity_month (users / initial_users x 100). |
    | `value_abs` | `UInt64` | Distinct cohort users doing this activity_kind in activity_month (renamed from users). |
    | `initial_users` | `UInt64` | Onboard-cohort size = distinct users onboarded in cohort_month (retention denominator). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_retention_by_action/monthly?start_month=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_swap_fees

Daily CoW protocol fee revenue from GA swaps (filled trades, pro-rated to USD).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_swap_fees/daily` | GET | tier1 | -- | -- | -- |
| `/v1/execution/gnosis_app_swap_fees/weekly` | GET | tier1 | -- | -- | -- |
| `/v1/execution/gnosis_app_swap_fees/monthly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_swap_fees/daily`"
    Daily CoW protocol fee revenue from GA swaps (filled trades, pro-rated to USD).

    Model: `api_execution_gnosis_app_swap_fees_daily` — table `dbt.api_execution_gnosis_app_swap_fees_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar date (UTC). |
    | `n_filled_swaps` | `UInt64` | Number of filled swaps on this date. |
    | `n_distinct_takers` | `UInt64` | Distinct taker (GA user) addresses with a filled swap on this date. |
    | `volume_usd` | `Nullable(Float64)` | Filled-swap USD volume on this date. |
    | `fee_native_total` | `Nullable(Float64)` | Sum of fee_amount in sold-token native units. |
    | `fee_usd_total` | `Nullable(Float64)` | Pro-rated fee in USD. |
    | `fee_pct_of_volume` | `Nullable(Float64)` | fee_usd_total / volume_usd × 100. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_swap_fees/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/gnosis_app_swap_fees/weekly`"
    Weekly rollup of swap_fees_daily.

    Model: `api_execution_gnosis_app_swap_fees_weekly` — table `dbt.api_execution_gnosis_app_swap_fees_weekly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | Monday-aligned start of the week (UTC). |
    | `n_filled_swaps` | `UInt64` | Number of filled swaps in this week. |
    | `volume_usd` | `Nullable(Float64)` | Filled-swap USD volume in this week. |
    | `fee_native_total` | `Nullable(Float64)` | Sum of fee_amount in sold-token native units. |
    | `fee_usd_total` | `Nullable(Float64)` | Pro-rated fee in USD. |
    | `fee_pct_of_volume` | `Nullable(Float64)` | fee_usd_total / volume_usd × 100. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_swap_fees/weekly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/gnosis_app_swap_fees/monthly`"
    Monthly rollup of swap_fees_daily.

    Model: `api_execution_gnosis_app_swap_fees_monthly` — table `dbt.api_execution_gnosis_app_swap_fees_monthly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `month` | `Date` | First day of the month (UTC). |
    | `n_filled_swaps` | `UInt64` | Number of filled swaps in this month. |
    | `volume_usd` | `Nullable(Float64)` | Filled-swap USD volume in this month. |
    | `fee_native_total` | `Nullable(Float64)` | Sum of fee_amount in sold-token native units. |
    | `fee_usd_total` | `Nullable(Float64)` | Pro-rated fee in USD. |
    | `fee_pct_of_volume` | `Nullable(Float64)` | fee_usd_total / volume_usd × 100. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_swap_fees/monthly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_swaps

FastAPI endpoint view of fct_execution_gnosis_app_swaps_daily. Supports query params: start_date, end_date.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_swaps/daily` | GET | tier1 | `start_date`, `end_date` | -- | date DESC |
| `/v1/execution/gnosis_app_swaps/weekly` | GET | tier1 | `start_date`, `end_date` | -- | week DESC |
| `/v1/execution/gnosis_app_swaps/monthly` | GET | tier1 | `start_month`, `end_month` | -- | month DESC |

??? info "`GET /v1/execution/gnosis_app_swaps/daily`"
    FastAPI endpoint view of fct_execution_gnosis_app_swaps_daily. Supports query params: start_date, end_date.

    Model: `api_execution_gnosis_app_swaps_daily` — table `dbt.api_execution_gnosis_app_swaps_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar date (UTC). |
    | `n_swaps` | `UInt64` | Number of swap orders. |
    | `n_swaps_filled` | `UInt64` | Number of swap orders that filled. |
    | `n_swaps_unfilled` | `UInt64` | Number of swap orders that did not fill. |
    | `n_swappers` | `UInt64` | Distinct addresses that swapped. |
    | `n_orders` | `UInt64` | Number of distinct orders. |
    | `volume_usd_filled` | `Nullable(Float64)` | USD volume of filled swaps. |
    | `volume_usd_priced` | `Nullable(Float64)` | USD volume for trades with a USD price available. |
    | `n_filled_unpriced` | `UInt64` | Filled swaps with no USD price available. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_swaps/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/gnosis_app_swaps/weekly`"
    FastAPI view over fct_execution_gnosis_app_swaps_weekly.

    Model: `api_execution_gnosis_app_swaps_weekly` — table `dbt.api_execution_gnosis_app_swaps_weekly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `start_date` | `>=` | `week` | date | Inclusive start week |
    | `end_date` | `<=` | `week` | date | Inclusive end week |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `week DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | Monday-aligned start of the week (UTC). |
    | `n_swaps` | `UInt64` | Number of swap orders. |
    | `n_swaps_filled` | `UInt64` | Number of swap orders that filled. |
    | `n_swaps_unfilled` | `UInt64` | Number of swap orders that did not fill. |
    | `n_swappers` | `UInt64` | Distinct addresses that swapped. |
    | `n_orders` | `UInt64` | Number of distinct orders. |
    | `volume_usd_filled` | `Nullable(Float64)` | USD volume of filled swaps. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_swaps/weekly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/gnosis_app_swaps/monthly`"
    FastAPI view over fct_execution_gnosis_app_swaps_monthly.

    Model: `api_execution_gnosis_app_swaps_monthly` — table `dbt.api_execution_gnosis_app_swaps_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `start_month` | `>=` | `month` | date | Inclusive start month |
    | `end_month` | `<=` | `month` | date | Inclusive end month |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `month` | `Date` | First day of the month (UTC). |
    | `n_swaps` | `UInt64` | Number of swap orders. |
    | `n_swaps_filled` | `UInt64` | Number of swap orders that filled. |
    | `n_swaps_unfilled` | `UInt64` | Number of swap orders that did not fill. |
    | `n_swappers` | `UInt64` | Distinct addresses that swapped. |
    | `n_orders` | `UInt64` | Number of distinct orders. |
    | `volume_usd_filled` | `Nullable(Float64)` | USD volume of filled swaps. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_swaps/monthly?start_month=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_swaps_by_pair

FastAPI view over fct_execution_gnosis_app_swaps_by_pair_daily. Params: pair, start_date, end_date.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_swaps_by_pair/daily` | GET | tier1 | `pair`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/execution/gnosis_app_swaps_by_pair/daily`"
    FastAPI view over fct_execution_gnosis_app_swaps_by_pair_daily. Params: pair, start_date, end_date.

    Model: `api_execution_gnosis_app_swaps_by_pair_daily` — table `dbt.api_execution_gnosis_app_swaps_by_pair_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `pair` | `=` | `pair` | string | Token pair label (e.g. 'CRC → EURe') |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar date (UTC). |
    | `pair` | `String` | Token pair label (sold -> bought). |
    | `token_sold_symbol` | `Nullable(String)` | Symbol of the token sold. |
    | `token_bought_symbol` | `Nullable(String)` | Symbol of the token bought. |
    | `n_swaps` | `UInt64` | Number of swap orders. |
    | `n_swaps_filled` | `UInt64` | Number of swap orders that filled. |
    | `n_swappers` | `UInt64` | Distinct addresses that swapped. |
    | `volume_usd_filled` | `Nullable(Float64)` | USD volume of filled swaps. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_swaps_by_pair/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_swaps_by_solver

FastAPI view over fct_execution_gnosis_app_swaps_by_solver_daily. Params: solver, start_date, end_date.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_swaps_by_solver/daily` | GET | tier1 | `solver`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/execution/gnosis_app_swaps_by_solver/daily`"
    FastAPI view over fct_execution_gnosis_app_swaps_by_solver_daily. Params: solver, start_date, end_date.

    Model: `api_execution_gnosis_app_swaps_by_solver_daily` — table `dbt.api_execution_gnosis_app_swaps_by_solver_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `solver` | `=` | `solver` | string | Solver address |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar date (UTC). |
    | `solver` | `String` | CoW solver that settled the trade. |
    | `n_swaps_filled` | `UInt64` | Number of swap orders that filled. |
    | `n_swappers` | `UInt64` | Distinct addresses that swapped. |
    | `volume_usd_filled` | `Nullable(Float64)` | USD volume of filled swaps. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_swaps_by_solver/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_time_to_first_conversion_cohort

Time from onboard to a user's FIRST event of each conversion kind, bucketed by onboard-month cohort. Long format: one row per (cohort_month, conversion_kind) over topup / swap_filled / marketplace_buy / token_offer_claim. Built on int_execution_gnosis_app_first_conversion. Modeling assumptions: *...

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_time_to_first_conversion_cohort/monthly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_time_to_first_conversion_cohort/monthly`"
    Time from onboard to a user's FIRST event of each conversion kind, bucketed by onboard-month cohort. Long format: one row per (cohort_month, conversion_kind) over topup / swap_filled / marketplace_buy / token_offer_claim. Built on int_execution_gnosis_app_first_conversion. Modeling assumptions: *...

    Model: `api_execution_gnosis_app_time_to_first_conversion_cohort_monthly` — table `dbt.api_execution_gnosis_app_time_to_first_conversion_cohort_monthly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `cohort_month` | `Date` | Onboard month (toStartOfMonth of first_seen_at). |
    | `conversion_kind` | `String` | topup / swap_filled / marketplace_buy / token_offer_claim. |
    | `n_in_cohort` | `UInt64` | Users onboarded in cohort_month (denominator). |
    | `n_converted` | `UInt64` | Users with a non-NULL first event of this kind. |
    | `pct_converted` | `Float64` | n_converted / n_in_cohort x 100. |
    | `median_days` | `Float64` | Median days onboard->first conversion, converters only, floored at 0. |
    | `p25_days` | `Float64` | 25th-pct days onboard->first conversion, converters only, floored at 0. |
    | `p75_days` | `Float64` | 75th-pct days onboard->first conversion, converters only, floored at 0. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_time_to_first_conversion_cohort/monthly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_token_offer_claim_funnel

Daily per-offer token-offer claim conversion (claims, claimers, USD received, claim_rate_pct).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_token_offer_claim_funnel/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_token_offer_claim_funnel/daily`"
    Daily per-offer token-offer claim conversion (claims, claimers, USD received, claim_rate_pct).

    Model: `api_execution_gnosis_app_token_offer_claim_funnel_daily` — table `dbt.api_execution_gnosis_app_token_offer_claim_funnel_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar date (UTC). |
    | `offer_address` | `String` | Address of the token offer (nextOffer). |
    | `n_claims` | `UInt64` | Number of token-offer claims on this date/offer. |
    | `n_claimers` | `UInt64` | Distinct addresses that claimed. |
    | `amount_received_usd` | `Float64` | USD value of offer tokens received by claimers. |
    | `n_active_pool_30d` | `UInt64` | Rolling 30-day active GA users (proxy eligible pool / funnel denominator). |
    | `claim_rate_pct` | `Nullable(Float64)` | n_claimers / n_active_pool_30d × 100 (NULL when the pool is empty). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_token_offer_claim_funnel/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_token_offer_claims

FastAPI view over fct_execution_gnosis_app_token_offer_claims_daily. Params: start_date, end_date.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_token_offer_claims/daily` | GET | tier1 | `start_date`, `end_date` | -- | date DESC |
| `/v1/execution/gnosis_app_token_offer_claims/weekly` | GET | tier1 | `start_date`, `end_date` | -- | week DESC |
| `/v1/execution/gnosis_app_token_offer_claims/monthly` | GET | tier1 | `start_date`, `end_date` | -- | month DESC |

??? info "`GET /v1/execution/gnosis_app_token_offer_claims/daily`"
    FastAPI view over fct_execution_gnosis_app_token_offer_claims_daily. Params: start_date, end_date.

    Model: `api_execution_gnosis_app_token_offer_claims_daily` — table `dbt.api_execution_gnosis_app_token_offer_claims_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar date (UTC). |
    | `n_claims` | `UInt64` | Number of token-offer claims. |
    | `n_claimers` | `UInt64` | Distinct addresses that claimed. |
    | `n_offers` | `UInt64` | Distinct token offers. |
    | `volume_received_token` | `Float64` | Token amount received by claimers (native units), rounded to 6 decimals. |
    | `volume_received_usd` | `Float64` | USD value received by claimers, rounded to 2 decimals. |
    | `volume_spent_crc` | `Float64` | CRC spent by claimers, rounded to 2 decimals. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_token_offer_claims/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/gnosis_app_token_offer_claims/weekly`"
    FastAPI view over fct_execution_gnosis_app_token_offer_claims_weekly. Params: start_date, end_date.

    Model: `api_execution_gnosis_app_token_offer_claims_weekly` — table `dbt.api_execution_gnosis_app_token_offer_claims_weekly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `start_date` | `>=` | `week` | date | Inclusive start week |
    | `end_date` | `<=` | `week` | date | Inclusive end week |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `week DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | Monday-aligned start of the week (UTC). |
    | `n_claims` | `UInt64` | Number of token-offer claims. |
    | `n_claimers` | `UInt64` | Distinct addresses that claimed. |
    | `n_offers` | `UInt64` | Distinct token offers. |
    | `volume_received_token` | `Float64` | Token amount received by claimers (native units), rounded to 6 decimals. |
    | `volume_received_usd` | `Float64` | USD value received by claimers, rounded to 2 decimals. |
    | `volume_spent_crc` | `Float64` | CRC spent by claimers, rounded to 2 decimals. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_token_offer_claims/weekly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/gnosis_app_token_offer_claims/monthly`"
    FastAPI view over fct_execution_gnosis_app_token_offer_claims_monthly. Params: start_date, end_date.

    Model: `api_execution_gnosis_app_token_offer_claims_monthly` — table `dbt.api_execution_gnosis_app_token_offer_claims_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `start_date` | `>=` | `month` | date | Inclusive start month |
    | `end_date` | `<=` | `month` | date | Inclusive end month |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `month` | `Date` | First day of the month (UTC). |
    | `n_claims` | `UInt64` | Number of token-offer claims. |
    | `n_claimers` | `UInt64` | Distinct addresses that claimed. |
    | `n_offers` | `UInt64` | Distinct token offers. |
    | `volume_received_token` | `Float64` | Token amount received by claimers (native units), rounded to 6 decimals. |
    | `volume_received_usd` | `Float64` | USD value received by claimers, rounded to 2 decimals. |
    | `volume_spent_crc` | `Float64` | CRC spent by claimers, rounded to 2 decimals. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_token_offer_claims/monthly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_token_offer_claims_by_offer

FastAPI view over fct_execution_gnosis_app_token_offer_claims_by_offer_daily. Params: offer_address, cycle_address, offer_token_symbol, start_date, end_date.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_token_offer_claims_by_offer/daily` | GET | tier1 | `offer_address`, `cycle_address`, `offer_token_symbol`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/execution/gnosis_app_token_offer_claims_by_offer/daily`"
    FastAPI view over fct_execution_gnosis_app_token_offer_claims_by_offer_daily. Params: offer_address, cycle_address, offer_token_symbol, start_date, end_date.

    Model: `api_execution_gnosis_app_token_offer_claims_by_offer_daily` — table `dbt.api_execution_gnosis_app_token_offer_claims_by_offer_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `offer_address` | `=` | `offer_address` | string | Specific offer (nextOffer) address, 0x-prefixed |
    | `cycle_address` | `=` | `cycle_address` | string | Specific offer-cycle contract address, 0x-prefixed |
    | `offer_token_symbol` | `=` | `offer_token_symbol` | string | Symbol of the offered token (e.g. 'GNO') |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar date (UTC). |
    | `offer_address` | `String` | Address of the token offer (nextOffer). |
    | `cycle_address` | `Nullable(String)` | Address of the offer cycle, if any. |
    | `offer_token_symbol` | `Nullable(String)` | Symbol of the token sold by the offer. |
    | `n_claims` | `UInt64` | Number of token-offer claims. |
    | `n_claimers` | `UInt64` | Distinct addresses that claimed. |
    | `volume_received_token` | `Float64` | Token amount received by claimers (native units), rounded to 6 decimals. |
    | `volume_received_usd` | `Float64` | USD value received by claimers, rounded to 2 decimals. |
    | `volume_spent_crc` | `Float64` | CRC spent by claimers, rounded to 2 decimals. |
    | `offer_price_in_crc` | `Nullable(Float64)` | Offer sticker price in CRC at creation time, rounded to 6 decimals. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_token_offer_claims_by_offer/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_token_offer_claims_cohort

FastAPI view over fct_execution_gnosis_app_token_offer_claims_cohort_monthly. Params: start_month, end_month.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_token_offer_claims_cohort/monthly` | GET | tier1 | `start_month`, `end_month` | -- | cohort_month DESC |

??? info "`GET /v1/execution/gnosis_app_token_offer_claims_cohort/monthly`"
    FastAPI view over fct_execution_gnosis_app_token_offer_claims_cohort_monthly. Params: start_month, end_month.

    Model: `api_execution_gnosis_app_token_offer_claims_cohort_monthly` — table `dbt.api_execution_gnosis_app_token_offer_claims_cohort_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `start_month` | `>=` | `cohort_month` | date | Inclusive start cohort month |
    | `end_month` | `<=` | `cohort_month` | date | Inclusive end cohort month |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `cohort_month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `cohort_month` | `Date` | Month of the user's first activity (cohort anchor). |
    | `x` | `String` | Activity month as a string (toString(activity_month)); x-axis of the retention grid. |
    | `y` | `String` | First-claim cohort month as a string (toString(cohort_month)); y-axis of the retention grid. |
    | `retention_pct` | `Float64` | Share of the first-claim cohort still claiming in activity_month (users / initial_users x 100). |
    | `value_abs` | `UInt64` | Distinct cohort users in this cell (renamed from users). |
    | `amount_retention_pct` | `Nullable(Float64)` | Retained USD amount as a share of the cohort's initial amount (x100). |
    | `value_usd` | `Nullable(Float64)` | USD amount (renamed from amount_usd). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_token_offer_claims_cohort/monthly?start_month=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_user_activity

Account-facing Gnosis App activity view.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_user_activity/daily` | GET, POST | tier1 | `address`, `activity_kind`, `start_date`, `end_date` | limit/offset (envelope) | date DESC |

??? info "`GET/POST /v1/execution/gnosis_app_user_activity/daily`"
    Account-facing Gnosis App activity view.

    Model: `api_execution_gnosis_app_user_activity_daily` — table `dbt.api_execution_gnosis_app_user_activity_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `address` | `IN` | `address` | string_list | case: lower; max_items: 20 |
    | `activity_kind` | `=` | `activity_kind` | string | -- |
    | `start_date` | `>=` | `date` | date | -- |
    | `end_date` | `<=` | `date` | date | -- |

    **Filter policy:** At least one filter required. Must provide one of: `address`.

    **Pagination:** `limit`/`offset` — default 200, max 5000; response: envelope `{items, pagination}`

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `activity_kind` | `String` | See enum above. |
    | `address` | `Nullable(String)` | -- |
    | `date` | `Date` | -- |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_user_activity/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_user_profile

Account-facing Gnosis App profile view from production current-user models.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_user_profile/latest` | GET, POST | tier1 | `address` | limit/offset (envelope) | -- |

??? info "`GET/POST /v1/execution/gnosis_app_user_profile/latest`"
    Account-facing Gnosis App profile view from production current-user models.

    Model: `api_execution_gnosis_app_user_profile_latest` — table `dbt.api_execution_gnosis_app_user_profile_latest`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `address` | `IN` | `address` | string_list | case: lower; max_items: 20 |

    **Filter policy:** At least one filter required. Must provide one of: `address`.

    **Pagination:** `limit`/`offset` — default 20, max 200; response: envelope `{items, pagination}`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `address` | `Nullable(String)` | -- |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_user_profile/latest?address=VALUE1,VALUE2" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_users

FastAPI view over fct_execution_gnosis_app_users_daily. Params: start_date, end_date.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_users/daily` | GET | tier1 | `start_date`, `end_date` | -- | date DESC |
| `/v1/execution/gnosis_app_users/weekly` | GET | tier1 | `start_date`, `end_date` | -- | week DESC |
| `/v1/execution/gnosis_app_users/monthly` | GET | tier1 | `start_date`, `end_date` | -- | month DESC |

??? info "`GET /v1/execution/gnosis_app_users/daily`"
    FastAPI view over fct_execution_gnosis_app_users_daily. Params: start_date, end_date.

    Model: `api_execution_gnosis_app_users_daily` — table `dbt.api_execution_gnosis_app_users_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar date (UTC). |
    | `new_users` | `UInt64` | Distinct addresses whose first-ever activity was on this date. |
    | `cumulative_users` | `UInt64` | Running total of distinct users up to and including this date. |
    | `active_users` | `UInt64` | Distinct addresses with any non-onboard activity on this date. |
    | `returning_users` | `UInt64` | Active this date and also active in the immediately prior period. |
    | `reactivated_users` | `UInt64` | Active this date after a dormancy gap, having been active earlier. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_users/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/gnosis_app_users/weekly`"
    FastAPI view over fct_execution_gnosis_app_users_weekly. Params: start_date, end_date.

    Model: `api_execution_gnosis_app_users_weekly` — table `dbt.api_execution_gnosis_app_users_weekly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `start_date` | `>=` | `week` | date | Inclusive start week |
    | `end_date` | `<=` | `week` | date | Inclusive end week |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `week DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | Monday-aligned start of the week (UTC). |
    | `new_users` | `UInt64` | Distinct addresses whose first-ever activity was in this week. |
    | `cumulative_users` | `UInt64` | Running total of distinct users up to and including this week. |
    | `active_users` | `UInt64` | Distinct addresses with any non-onboard activity in this week. |
    | `returning_users` | `UInt64` | Active this week and also active in the immediately prior week. |
    | `reactivated_users` | `UInt64` | Active this week after a dormancy gap, having been active earlier. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_users/weekly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/gnosis_app_users/monthly`"
    FastAPI view over fct_execution_gnosis_app_users_monthly. Params: start_month, end_month.

    Model: `api_execution_gnosis_app_users_monthly` — table `dbt.api_execution_gnosis_app_users_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `start_date` | `>=` | `month` | date | Inclusive start month |
    | `end_date` | `<=` | `month` | date | Inclusive end month |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `month` | `Date` | First day of the month (UTC). |
    | `new_users` | `UInt64` | Distinct addresses whose first-ever activity was in this month. |
    | `cumulative_users` | `UInt64` | Running total of distinct users up to and including this month. |
    | `active_users` | `UInt64` | Distinct addresses with any non-onboard activity in this month. |
    | `returning_users` | `UInt64` | Active this month and also active in the immediately prior month. |
    | `reactivated_users` | `UInt64` | Active this month after a dormancy gap, having been active earlier. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_users/monthly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_weekly_active_users

Gnosis App Weekly Active Users (WAU) time-series over fct_execution_gnosis_app_users_weekly.active_users (in-app active population; same as DAU/MAU lineage; latest incomplete week excluded). WEAU is a strict subset.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_weekly_active_users/weekly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_weekly_active_users/weekly`"
    Gnosis App Weekly Active Users (WAU) time-series over fct_execution_gnosis_app_users_weekly.active_users (in-app active population; same as DAU/MAU lineage; latest incomplete week excluded). WEAU is a strict subset.

    Model: `api_execution_gnosis_app_weekly_active_users` — table `dbt.api_execution_gnosis_app_weekly_active_users`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | Monday-aligned start of the week (UTC). Time-series grain. |
    | `active_users` | `UInt64` | Distinct in-app active Gnosis App users in the week (headline WAU; any non-onboard activity). |
    | `new_users` | `UInt64` | Users whose first-ever activity (onboarding) was this week. |
    | `returning_users` | `UInt64` | Active this week AND active the previous week. |
    | `reactivated_users` | `UInt64` | Active this week, not active in the prior 4 weeks, but active earlier. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_weekly_active_users/weekly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_weekly_active_users_incl_gpay

Gnosis App Weekly Active Users (WAU), Gnosis-Pay-inclusive variant of api_execution_gnosis_app_weekly_active_users: 'active' additionally counts any user-initiated Gnosis Pay card-wallet transaction (spend/withdrawal/off-ramp/fiat top-up) attributed to the safe's Gnosis App owner. Latest incomple...

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_weekly_active_users_incl_gpay/weekly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_weekly_active_users_incl_gpay/weekly`"
    Gnosis App Weekly Active Users (WAU), Gnosis-Pay-inclusive variant of api_execution_gnosis_app_weekly_active_users: 'active' additionally counts any user-initiated Gnosis Pay card-wallet transaction (spend/withdrawal/off-ramp/fiat top-up) attributed to the safe's Gnosis App owner. Latest incomple...

    Model: `api_execution_gnosis_app_weekly_active_users_incl_gpay` — table `dbt.api_execution_gnosis_app_weekly_active_users_incl_gpay`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | Monday-aligned start of the week (UTC). Time-series grain. |
    | `active_users` | `UInt64` | Distinct active Gnosis App users in the week, additionally including GA owners whose only activity was a Gnosis Pay card-wallet transaction. |
    | `new_users` | `UInt64` | Users whose first-ever activity (onboarding) was this week. |
    | `returning_users` | `UInt64` | Active this week AND active the previous week. |
    | `reactivated_users` | `UInt64` | Active this week, not active in the prior 4 weeks, but active earlier. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_weekly_active_users_incl_gpay/weekly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gnosis_app_weekly_economically_active_users

Time-series view over fct_execution_gnosis_app_weekly_economically_active_users (latest week excluded).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gnosis_app_weekly_economically_active_users/weekly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/gnosis_app_weekly_economically_active_users/weekly`"
    Time-series view over fct_execution_gnosis_app_weekly_economically_active_users (latest week excluded).

    Model: `api_execution_gnosis_app_weekly_economically_active_users` — table `dbt.api_execution_gnosis_app_weekly_economically_active_users`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | Monday-aligned start of the week (UTC). Time-series grain. |
    | `is_blacklisted` | `Bool` | True if the address appears in the circles blacklist snapshot. |
    | `cnt` | `UInt64` | Distinct economically active addresses in this week × blacklist bucket. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gnosis_app_weekly_economically_active_users/weekly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_accounts

Daily time series of the cumulative number of deployed Gnosis Pay accounts.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_accounts/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/gpay_accounts/daily`"
    Daily time series of the cumulative number of deployed Gnosis Pay accounts.

    Model: `api_execution_gpay_accounts_daily` — table `dbt.api_execution_gpay_accounts_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The calendar date (account deploy date). |
    | `value` | `Float64` | The cumulative number of deployed Gnosis Pay accounts up to and including the date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_accounts/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_active_users

Weekly time series of Gnosis Pay active user counts.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_active_users/weekly` | GET | tier1 | -- | -- | -- |
| `/v1/execution/gpay_active_users/last_7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gpay_active_users/weekly`"
    Weekly time series of Gnosis Pay active user counts.

    Model: `api_execution_gpay_active_users_weekly` — table `dbt.api_execution_gpay_active_users_weekly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The first day of the ISO week. |
    | `value` | `UInt64` | The number of active users in this week. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_active_users/weekly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/gpay_active_users/last_7d`"
    7-day active user count with period-over-period change percentage for Gnosis Pay.

    Model: `api_execution_gpay_active_users_7d` — table `dbt.api_execution_gpay_active_users_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | The number of active users in the last 7 days. |
    | `change_pct` | `Float64` | The percentage change compared to the previous 7-day period. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_active_users/last_7d"
    ```

## gpay_activity_by_action

Daily Gnosis Pay activity metrics broken down by action type, with counts and volumes.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_activity_by_action/daily` | GET | tier1 | `action`, `start_date`, `end_date` | -- | date DESC |
| `/v1/execution/gpay_activity_by_action/weekly` | GET | tier1 | `action`, `start_date`, `end_date` | -- | week DESC |
| `/v1/execution/gpay_activity_by_action/monthly` | GET | tier1 | `action`, `start_date`, `end_date` | -- | month DESC |

??? info "`GET /v1/execution/gpay_activity_by_action/daily`"
    Daily Gnosis Pay activity metrics broken down by action type, with counts and volumes.

    Model: `api_execution_gpay_activity_by_action_daily` — table `dbt.api_execution_gpay_activity_by_action_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `action` | `=` | `action` | string | Action type (Payment, Cashback, etc.) |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The calendar date. |
    | `action` | `String` | The activity type (e.g., Payment, Deposit, Withdrawal, Cashback). |
    | `activity_count` | `UInt64` | The number of transactions for this action on this date. |
    | `volume_usd` | `Float64` | The total USD volume for this action on this date. |
    | `volume_native` | `Float64` | The total native token volume for this action on this date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_activity_by_action/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/gpay_activity_by_action/weekly`"
    Weekly Gnosis Pay activity metrics broken down by action type, with counts and volumes.

    Model: `api_execution_gpay_activity_by_action_weekly` — table `dbt.api_execution_gpay_activity_by_action_weekly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `action` | `=` | `action` | string | Action type |
    | `start_date` | `>=` | `week` | date | Inclusive start date |
    | `end_date` | `<=` | `week` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `week DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `week` | `Date` | The first day of the ISO week. |
    | `action` | `String` | The activity type (e.g., Payment, Deposit, Withdrawal, Cashback). |
    | `activity_count` | `UInt64` | The number of transactions for this action in this week. |
    | `volume_usd` | `Float64` | The total USD volume for this action in this week. |
    | `volume_native` | `Float64` | The total native token volume for this action in this week. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_activity_by_action/weekly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/gpay_activity_by_action/monthly`"
    Monthly Gnosis Pay activity metrics broken down by action type, with counts and volumes.

    Model: `api_execution_gpay_activity_by_action_monthly` — table `dbt.api_execution_gpay_activity_by_action_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `action` | `=` | `action` | string | Action type |
    | `start_date` | `>=` | `month` | date | Inclusive start date |
    | `end_date` | `<=` | `month` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `month` | `Date` | The first day of the month. |
    | `action` | `String` | The activity type (e.g., Payment, Deposit, Withdrawal, Cashback). |
    | `activity_count` | `UInt64` | The number of transactions for this action in this month. |
    | `volume_usd` | `Float64` | The total USD volume for this action in this month. |
    | `volume_native` | `Float64` | The total native token volume for this action in this month. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_activity_by_action/monthly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_balance_cohorts_holders

Daily count of Gnosis Pay wallet holders in each balance cohort bucket by token.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_balance_cohorts_holders/daily` | GET | tier1 | `token`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/execution/gpay_balance_cohorts_holders/daily`"
    Daily count of Gnosis Pay wallet holders in each balance cohort bucket by token.

    Model: `api_execution_gpay_balance_cohorts_holders_daily` — table `dbt.api_execution_gpay_balance_cohorts_holders_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `token` | string | Token symbol |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The calendar date of the balance snapshot. |
    | `token` | `String` | The token symbol. |
    | `cohort_unit` | `String` | The unit used for cohort bucketing (e.g., USD, native). |
    | `label` | `String` | The balance range bucket label. |
    | `value` | `UInt64` | The number of holders in this cohort bucket. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_balance_cohorts_holders/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_balance_cohorts_value

Daily total value held in each balance cohort bucket by token, in native and USD.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_balance_cohorts_value/daily` | GET | tier1 | `token`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/execution/gpay_balance_cohorts_value/daily`"
    Daily total value held in each balance cohort bucket by token, in native and USD.

    Model: `api_execution_gpay_balance_cohorts_value_daily` — table `dbt.api_execution_gpay_balance_cohorts_value_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `token` | string | Token symbol |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The calendar date of the balance snapshot. |
    | `token` | `String` | The token symbol. |
    | `cohort_unit` | `String` | The unit used for cohort bucketing. |
    | `label` | `String` | The balance range bucket label. |
    | `value_native` | `Float64` | The total native token value in this bucket. |
    | `value_usd` | `Float64` | The total USD value in this bucket. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_balance_cohorts_value/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_balances_by_token

Daily total Gnosis Pay wallet balances by token in USD.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_balances_by_token/daily` | GET | tier1 | `token`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/execution/gpay_balances_by_token/daily`"
    Daily total Gnosis Pay wallet balances by token in USD.

    Model: `api_execution_gpay_balances_by_token_daily` — table `dbt.api_execution_gpay_balances_by_token_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `label` | string | Token symbol |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The calendar date of the balance snapshot. |
    | `label` | `String` | The token symbol. |
    | `value` | `Float64` | The total balance in USD for this token. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_balances_by_token/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_balances_native

Daily total Gnosis Pay wallet balances by token in native units.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_balances_native/daily` | GET | tier1 | `token`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/execution/gpay_balances_native/daily`"
    Daily total Gnosis Pay wallet balances by token in native units.

    Model: `api_execution_gpay_balances_native_daily` — table `dbt.api_execution_gpay_balances_native_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `label` | string | Token symbol |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The calendar date of the balance snapshot. |
    | `label` | `String` | The token symbol. |
    | `value` | `Float64` | The total balance in native token units. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_balances_native/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_balances_usd

Daily total Gnosis Pay wallet balances by token in USD.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_balances_usd/daily` | GET | tier1 | `token`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/execution/gpay_balances_usd/daily`"
    Daily total Gnosis Pay wallet balances by token in USD.

    Model: `api_execution_gpay_balances_usd_daily` — table `dbt.api_execution_gpay_balances_usd_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `label` | string | Token symbol |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The calendar date of the balance snapshot. |
    | `label` | `String` | The token symbol. |
    | `value` | `Float64` | The total balance in USD for this token. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_balances_usd/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_cashback

Weekly cashback amounts distributed by unit.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_cashback/weekly` | GET | tier1 | -- | -- | -- |
| `/v1/execution/gpay_cashback/7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gpay_cashback/weekly`"
    Weekly cashback amounts distributed by unit.

    Model: `api_execution_gpay_cashback_weekly` — table `dbt.api_execution_gpay_cashback_weekly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `unit` | `String` | The cashback unit (e.g., USD, GNO). |
    | `date` | `Date` | The first day of the ISO week. |
    | `value` | `Float64` | The cashback amount for this week. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_cashback/weekly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/gpay_cashback/7d`"
    7-day cashback summary with unit breakdown and period-over-period change percentage.

    Model: `api_execution_gpay_cashback_7d` — table `dbt.api_execution_gpay_cashback_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `unit` | `String` | The cashback unit (e.g., USD, GNO). |
    | `value` | `Float64` | The total cashback amount in the last 7 days. |
    | `change_pct` | `Float64` | The percentage change compared to the previous 7-day period. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_cashback/7d"
    ```

## gpay_cashback_cohort_retention

Monthly cashback cohort retention heatmap data showing retention and amount percentages across cohorts.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_cashback_cohort_retention/monthly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/gpay_cashback_cohort_retention/monthly`"
    Monthly cashback cohort retention heatmap data showing retention and amount percentages across cohorts.

    Model: `api_execution_gpay_cashback_cohort_retention_monthly` — table `dbt.api_execution_gpay_cashback_cohort_retention_monthly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `x` | `String` | The activity month (x-axis of the heatmap). |
    | `y` | `String` | The cohort month (y-axis of the heatmap). |
    | `retention_pct` | `Float64` | The user retention percentage for this cohort in this month. |
    | `value_abs` | `UInt64` | The absolute number of retained users. |
    | `amount_retention_pct` | `Float64` | The cashback amount retention percentage. |
    | `value_usd` | `Float64` | The total cashback amount in USD. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_cashback_cohort_retention/monthly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_cashback_cohort_retention_users

Monthly cashback cohort sizes over time, formatted for time series visualization.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_cashback_cohort_retention_users/monthly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/gpay_cashback_cohort_retention_users/monthly`"
    Monthly cashback cohort sizes over time, formatted for time series visualization.

    Model: `api_execution_gpay_cashback_cohort_retention_users_monthly` — table `dbt.api_execution_gpay_cashback_cohort_retention_users_monthly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The activity month. |
    | `label` | `String` | The cohort month label. |
    | `value` | `UInt64` | The number of active users from this cohort. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_cashback_cohort_retention_users/monthly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_cashback_cumulative

Cumulative cashback distributed over time by unit.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_cashback_cumulative/weekly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/gpay_cashback_cumulative/weekly`"
    Cumulative cashback distributed over time by unit.

    Model: `api_execution_gpay_cashback_cumulative` — table `dbt.api_execution_gpay_cashback_cumulative`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `unit` | `String` | The cashback unit (e.g., USD, GNO). |
    | `date` | `Date` | The calendar date. |
    | `value` | `Float64` | The cumulative cashback amount up to this date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_cashback_cumulative/weekly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_cashback_dist

Weekly cashback distribution percentiles for Gnosis Pay users.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_cashback_dist/weekly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/gpay_cashback_dist/weekly`"
    Weekly cashback distribution percentiles for Gnosis Pay users.

    Model: `api_execution_gpay_cashback_dist_weekly` — table `dbt.api_execution_gpay_cashback_dist_weekly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The first day of the ISO week. |
    | `q05` | `Float64` | The 5th percentile of cashback amounts. |
    | `q10` | `Float64` | The 10th percentile of cashback amounts. |
    | `q25` | `Float64` | The 25th percentile of cashback amounts. |
    | `q50` | `Float64` | The median cashback amount. |
    | `q75` | `Float64` | The 75th percentile of cashback amounts. |
    | `q90` | `Float64` | The 90th percentile of cashback amounts. |
    | `q95` | `Float64` | The 95th percentile of cashback amounts. |
    | `average` | `Float64` | The average cashback amount. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_cashback_dist/weekly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_cashback_impact

Monthly cashback impact analysis comparing payment behavior between user segments. Passes through all columns from the fact model.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_cashback_impact/monthly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/gpay_cashback_impact/monthly`"
    Monthly cashback impact analysis comparing payment behavior between user segments. Passes through all columns from the fact model.

    Model: `api_execution_gpay_cashback_impact_monthly` — table `dbt.api_execution_gpay_cashback_impact_monthly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `month` | `Date` | The first day of the month. |
    | `segment` | `String` | The user segment (e.g., cashback recipient, non-cashback). |
    | `users` | `UInt64` | The number of users in this segment. |
    | `payment_volume_usd` | `Float64` | The total payment volume in USD for this segment. |
    | `payment_count` | `UInt64` | The total number of payments for this segment. |
    | `avg_volume_per_user` | `Float64` | The average payment volume per user in USD. |
    | `avg_tx_per_user` | `Float64` | The average number of transactions per user. |
    | `deposit_volume_usd` | `Float64` | The total deposit volume in USD for this segment. |
    | `withdrawal_volume_usd` | `Float64` | The total withdrawal volume in USD for this segment. |
    | `net_flow_usd` | `Float64` | The net flow (deposits minus withdrawals) in USD. |
    | `pct_of_total_volume` | `Float64` | The percentage of total payment volume this segment represents. |
    | `pct_of_total_users` | `Float64` | The percentage of total users this segment represents. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_cashback_impact/monthly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_cashback_recipients

Weekly time series of unique Gnosis Pay cashback recipient counts.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_cashback_recipients/weekly` | GET | tier1 | -- | -- | -- |
| `/v1/execution/gpay_cashback_recipients/7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gpay_cashback_recipients/weekly`"
    Weekly time series of unique Gnosis Pay cashback recipient counts.

    Model: `api_execution_gpay_cashback_recipients_weekly` — table `dbt.api_execution_gpay_cashback_recipients_weekly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The first day of the ISO week. |
    | `value` | `UInt64` | The number of unique cashback recipients in this week. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_cashback_recipients/weekly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/gpay_cashback_recipients/7d`"
    7-day unique cashback recipient count with period-over-period change percentage.

    Model: `api_execution_gpay_cashback_recipients_7d` — table `dbt.api_execution_gpay_cashback_recipients_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | The number of unique cashback recipients in the last 7 days. |
    | `change_pct` | `Float64` | The percentage change compared to the previous 7-day period. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_cashback_recipients/7d"
    ```

## gpay_cashback_recipients_total

All-time total count of unique Gnosis Pay cashback recipients.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_cashback_recipients_total/all_time` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gpay_cashback_recipients_total/all_time`"
    All-time total count of unique Gnosis Pay cashback recipients.

    Model: `api_execution_gpay_cashback_recipients_total` — table `dbt.api_execution_gpay_cashback_recipients_total`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | The total number of unique cashback recipients. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_cashback_recipients_total/all_time"
    ```

## gpay_cashback_total

All-time total cashback distributed by unit.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_cashback_total/all_time` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gpay_cashback_total/all_time`"
    All-time total cashback distributed by unit.

    Model: `api_execution_gpay_cashback_total` — table `dbt.api_execution_gpay_cashback_total`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `unit` | `String` | The cashback unit (e.g., USD, GNO). |
    | `value` | `Float64` | The total cashback amount. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_cashback_total/all_time"
    ```

## gpay_churn

Monthly user churn breakdown for Gnosis Pay showing user segments and rates by activity scope.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_churn/monthly` | GET | tier1 | `scope`, `start_date`, `end_date` | -- | month DESC |

??? info "`GET /v1/execution/gpay_churn/monthly`"
    Monthly user churn breakdown for Gnosis Pay showing user segments and rates by activity scope.

    Model: `api_execution_gpay_churn_monthly` — table `dbt.api_execution_gpay_churn_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `scope` | `=` | `scope` | string | Churn scope |
    | `start_date` | `>=` | `month` | date | Inclusive start month |
    | `end_date` | `<=` | `month` | date | Inclusive end month |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `scope` | `String` | The activity scope for churn calculation (e.g., all, payment). |
    | `month` | `Date` | The first day of the month. |
    | `new_users` | `UInt64` | Users active for the first time this month. |
    | `retained_users` | `UInt64` | Users active in both this and the previous month. |
    | `returning_users` | `UInt64` | Users returning after a period of inactivity. |
    | `churned_users` | `UInt64` | Users active last month but not this month. |
    | `total_active` | `UInt64` | Total active users this month. |
    | `churn_rate` | `Float64` | The percentage of last month's users who churned. |
    | `retention_rate` | `Float64` | The percentage of last month's users who were retained. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_churn/monthly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_churn_rates

Monthly churn and retention rates for Gnosis Pay by activity scope.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_churn_rates/monthly` | GET | tier1 | `scope`, `start_date`, `end_date` | -- | month DESC |

??? info "`GET /v1/execution/gpay_churn_rates/monthly`"
    Monthly churn and retention rates for Gnosis Pay by activity scope.

    Model: `api_execution_gpay_churn_rates_monthly` — table `dbt.api_execution_gpay_churn_rates_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `scope` | `=` | `scope` | string | Churn scope |
    | `start_date` | `>=` | `month` | date | Inclusive start month |
    | `end_date` | `<=` | `month` | date | Inclusive end month |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `month DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `scope` | `String` | The activity scope (e.g., all, payment). |
    | `month` | `Date` | The first day of the month. |
    | `churn_rate` | `Float64` | The churn rate for the month. |
    | `retention_rate` | `Float64` | The retention rate for the month. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_churn_rates/monthly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_flows_snapshots

Token flow patterns between Gnosis Pay wallet labels for API consumption.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_flows_snapshots/in_ranges` | GET | tier1 | `symbol`, `window` | -- | -- |

??? info "`GET /v1/execution/gpay_flows_snapshots/in_ranges`"
    Token flow patterns between Gnosis Pay wallet labels for API consumption.

    Model: `api_execution_gpay_flows_snapshot` — table `dbt.api_execution_gpay_flows_snapshot`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `symbol` | `=` | `symbol` | string | Token symbol |
    | `window` | `=` | `window` | string | Time window (1D, 7D, 30D, 90D) |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `window` | `String` | The time window for the flow snapshot (e.g., 7D, 30D, All). |
    | `symbol` | `String` | The token symbol involved in the flow. |
    | `from_label` | `String` | The source label of the flow. |
    | `to_label` | `String` | The destination label of the flow. |
    | `amount_usd` | `Float64` | The total USD value of the flow. |
    | `tf_cnt` | `UInt64` | The number of individual transfers in the flow. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_flows_snapshots/in_ranges?symbol=VALUE" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_funded_addresses

Daily time series of cumulative funded Gnosis Pay wallet addresses.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_funded_addresses/daily` | GET | tier1 | -- | -- | -- |
| `/v1/execution/gpay_funded_addresses/weekly` | GET | tier1 | -- | -- | -- |
| `/v1/execution/gpay_funded_addresses/monthly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/gpay_funded_addresses/daily`"
    Daily time series of cumulative funded Gnosis Pay wallet addresses.

    Model: `api_execution_gpay_funded_addresses_daily` — table `dbt.api_execution_gpay_funded_addresses_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The calendar date. |
    | `value` | `UInt64` | The cumulative number of funded wallet addresses. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_funded_addresses/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/gpay_funded_addresses/weekly`"
    Weekly time series of cumulative funded Gnosis Pay wallet addresses.

    Model: `api_execution_gpay_funded_addresses_weekly` — table `dbt.api_execution_gpay_funded_addresses_weekly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The first day of the ISO week. |
    | `value` | `UInt64` | The cumulative number of funded wallet addresses. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_funded_addresses/weekly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/gpay_funded_addresses/monthly`"
    Monthly time series of cumulative funded Gnosis Pay wallet addresses.

    Model: `api_execution_gpay_funded_addresses_monthly` — table `dbt.api_execution_gpay_funded_addresses_monthly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The first day of the month. |
    | `value` | `UInt64` | The cumulative number of funded wallet addresses. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_funded_addresses/monthly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_gno_balance

Daily total GNO token balance across all Gnosis Pay wallets.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_gno_balance/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/gpay_gno_balance/daily`"
    Daily total GNO token balance across all Gnosis Pay wallets.

    Model: `api_execution_gpay_gno_balance_daily` — table `dbt.api_execution_gpay_gno_balance_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The calendar date. |
    | `value` | `Float64` | The total GNO balance across all wallets. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_gno_balance/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_gno_total_balance

Current total GNO token balance across all Gnosis Pay wallets.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_gno_total_balance/all_time` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gpay_gno_total_balance/all_time`"
    Current total GNO token balance across all Gnosis Pay wallets.

    Model: `api_execution_gpay_gno_total_balance` — table `dbt.api_execution_gpay_gno_total_balance`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | The total GNO balance. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_gno_total_balance/all_time"
    ```

## gpay_kpi

Monthly KPIs for Gnosis Pay, passing through all columns from the fact model.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_kpi/monthly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/gpay_kpi/monthly`"
    Monthly KPIs for Gnosis Pay, passing through all columns from the fact model.

    Model: `api_execution_gpay_kpi_monthly` — table `dbt.api_execution_gpay_kpi_monthly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `month` | `Date` | The first day of the month. |
    | `mau` | `UInt64` | Monthly active users across all activity types. |
    | `payment_mau` | `UInt64` | Monthly active users who made payments. |
    | `deposit_mau` | `UInt64` | Monthly active users who made deposits. |
    | `withdrawal_mau` | `UInt64` | Monthly active users who made withdrawals. |
    | `cashback_mau` | `UInt64` | Monthly active users who received cashback. |
    | `total_payment_volume_usd` | `Float64` | Total payment volume in USD for the month. |
    | `total_payment_count` | `UInt64` | Total number of payments in the month. |
    | `total_deposit_volume_usd` | `Float64` | Total deposit volume in USD for the month. |
    | `total_withdrawal_volume_usd` | `Float64` | Total withdrawal volume in USD for the month. |
    | `net_flow_usd` | `Float64` | Net flow (deposits minus withdrawals) in USD for the month. |
    | `cashback_total_usd` | `Float64` | Total cashback distributed in USD for the month. |
    | `cashback_total_gno` | `Float64` | Total cashback distributed in GNO tokens for the month. |
    | `refund_total_usd` | `Float64` | Total refund value in USD for the month. |
    | `reversal_total_usd` | `Float64` | Total reversal value in USD for the month. |
    | `arpu` | `Float64` | Average revenue per user in USD. |
    | `avg_tx_per_user` | `Float64` | Average number of transactions per active user. |
    | `repeat_purchase_rate` | `Float64` | Percentage of users who made more than one payment. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_kpi/monthly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_owner_balances_by_token

Daily total Gnosis Pay owner balances by token in USD.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_owner_balances_by_token/daily` | GET | tier1 | `token`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/execution/gpay_owner_balances_by_token/daily`"
    Daily total Gnosis Pay owner balances by token in USD.

    Model: `api_execution_gpay_owner_balances_by_token_daily` — table `dbt.api_execution_gpay_owner_balances_by_token_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `label` | string | Token symbol |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The calendar date of the balance snapshot. |
    | `label` | `String` | The token symbol. |
    | `value` | `Float64` | The total owner balance in USD for this token. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_owner_balances_by_token/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_owner_total_balance

Current total balance across all Gnosis Pay wallet owners in USD.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_owner_total_balance/all_time` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gpay_owner_total_balance/all_time`"
    Current total balance across all Gnosis Pay wallet owners in USD.

    Model: `api_execution_gpay_owner_total_balance` — table `dbt.api_execution_gpay_owner_total_balance`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | The total owner balance in USD. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_owner_total_balance/all_time"
    ```

## gpay_payments

7-day payment count with period-over-period change percentage.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_payments/last_7d` | GET | tier0 | -- | -- | -- |
| `/v1/execution/gpay_payments/hourly` | GET | tier1 | `token`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/execution/gpay_payments/last_7d`"
    7-day payment count with period-over-period change percentage.

    Model: `api_execution_gpay_payments_7d` — table `dbt.api_execution_gpay_payments_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | The total number of payments in the last 7 days. |
    | `change_pct` | `Float64` | The percentage change compared to the previous 7-day period. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_payments/last_7d"
    ```

??? info "`GET /v1/execution/gpay_payments/hourly`"
    Hourly payment counts by token for Gnosis Pay.

    Model: `api_execution_gpay_payments_hourly` — table `dbt.api_execution_gpay_payments_hourly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `label` | string | Token symbol |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `DateTime` | The hour timestamp of the payment activity. |
    | `label` | `String` | The token symbol. |
    | `value` | `UInt64` | The number of payments in this hour for this token. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_payments/hourly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_payments_by_token

Daily payment counts by token for Gnosis Pay.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_payments_by_token/daily` | GET | tier1 | `token`, `start_date`, `end_date` | -- | date DESC |
| `/v1/execution/gpay_payments_by_token/weekly` | GET | tier1 | `token`, `start_date`, `end_date` | -- | date DESC |
| `/v1/execution/gpay_payments_by_token/monthly` | GET | tier1 | `token`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/execution/gpay_payments_by_token/daily`"
    Daily payment counts by token for Gnosis Pay.

    Model: `api_execution_gpay_payments_by_token_daily` — table `dbt.api_execution_gpay_payments_by_token_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `label` | string | Token symbol |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The calendar date. |
    | `label` | `String` | The token symbol. |
    | `value` | `UInt64` | The number of payments for this token on this date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_payments_by_token/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/gpay_payments_by_token/weekly`"
    Weekly payment counts by token for Gnosis Pay.

    Model: `api_execution_gpay_payments_by_token_weekly` — table `dbt.api_execution_gpay_payments_by_token_weekly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `label` | string | Token symbol |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The first day of the ISO week. |
    | `label` | `String` | The token symbol. |
    | `value` | `UInt64` | The number of payments for this token in this week. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_payments_by_token/weekly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/gpay_payments_by_token/monthly`"
    Monthly payment counts by token for Gnosis Pay.

    Model: `api_execution_gpay_payments_by_token_monthly` — table `dbt.api_execution_gpay_payments_by_token_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `label` | string | Token symbol |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The first day of the month. |
    | `label` | `String` | The token symbol. |
    | `value` | `UInt64` | The number of payments for this token in this month. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_payments_by_token/monthly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_retention

Monthly cohort user counts over time, formatted for time series visualization.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_retention/monthly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/gpay_retention/monthly`"
    Monthly cohort user counts over time, formatted for time series visualization.

    Model: `api_execution_gpay_retention_monthly` — table `dbt.api_execution_gpay_retention_monthly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `String` | The activity month. |
    | `label` | `String` | The cohort month label. |
    | `value` | `UInt64` | The number of active users from this cohort. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_retention/monthly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_retention_by_action

Monthly cohort retention heatmap data for Gnosis Pay broken down by action type.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_retention_by_action/monthly` | GET | tier1 | `action` | -- | -- |

??? info "`GET /v1/execution/gpay_retention_by_action/monthly`"
    Monthly cohort retention heatmap data for Gnosis Pay broken down by action type.

    Model: `api_execution_gpay_retention_by_action_monthly` — table `dbt.api_execution_gpay_retention_by_action_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `action` | `=` | `action` | string | Action type |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `x` | `String` | The activity month (x-axis of the heatmap). |
    | `y` | `String` | The cohort month (y-axis of the heatmap). |
    | `action` | `String` | The activity type (e.g., Payment, Deposit, Withdrawal). |
    | `retention_pct` | `Float64` | The user retention percentage. |
    | `value_abs` | `UInt64` | The absolute number of retained users. |
    | `amount_retention_pct` | `Float64` | The amount retention percentage. |
    | `value_usd` | `Float64` | The total USD amount for the cohort in this month. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_retention_by_action/monthly?action=VALUE" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_retention_by_action_users

Monthly cohort user counts over time by action type, formatted for time series visualization.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_retention_by_action_users/monthly` | GET | tier1 | `action` | -- | -- |

??? info "`GET /v1/execution/gpay_retention_by_action_users/monthly`"
    Monthly cohort user counts over time by action type, formatted for time series visualization.

    Model: `api_execution_gpay_retention_by_action_users_monthly` — table `dbt.api_execution_gpay_retention_by_action_users_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `action` | `=` | `action` | string | Action type |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `action` | `String` | The activity type (e.g., Payment, Deposit, Withdrawal). |
    | `date` | `Date` | The activity month. |
    | `label` | `String` | The cohort month label. |
    | `value` | `UInt64` | The number of active users from this cohort. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_retention_by_action_users/monthly?action=VALUE" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_retention_pct

Monthly cohort retention heatmap data for all Gnosis Pay activity.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_retention_pct/monthly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/gpay_retention_pct/monthly`"
    Monthly cohort retention heatmap data for all Gnosis Pay activity.

    Model: `api_execution_gpay_retention_pct_monthly` — table `dbt.api_execution_gpay_retention_pct_monthly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `x` | `String` | The activity month (x-axis of the heatmap). |
    | `y` | `String` | The cohort month (y-axis of the heatmap). |
    | `retention_pct` | `Float64` | The user retention percentage. |
    | `value_abs` | `UInt64` | The absolute number of retained users. |
    | `amount_retention_pct` | `Float64` | The amount retention percentage. |
    | `value_usd` | `Float64` | The total USD amount for the cohort in this month. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_retention_pct/monthly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_retention_volume

Monthly cohort volume retention over time, formatted for time series visualization.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_retention_volume/monthly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/gpay_retention_volume/monthly`"
    Monthly cohort volume retention over time, formatted for time series visualization.

    Model: `api_execution_gpay_retention_volume_monthly` — table `dbt.api_execution_gpay_retention_volume_monthly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The activity month. |
    | `label` | `String` | The cohort month label. |
    | `value` | `Float64` | The total USD volume for this cohort in this month. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_retention_volume/monthly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_total_accounts

All-time total count of deployed Gnosis Pay accounts (Safes that enabled a Gnosis Pay Zodiac module - Delay / Roles / Spender), including accounts that never made a payment. Migrated Safes from the June 2026 migration are collapsed to a single account. This is the true "accounts deployed" figure,...

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_total_accounts/all_time` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gpay_total_accounts/all_time`"
    All-time total count of deployed Gnosis Pay accounts (Safes that enabled a Gnosis Pay Zodiac module - Delay / Roles / Spender), including accounts that never made a payment. Migrated Safes from the June 2026 migration are collapsed to a single account. This is the true "accounts deployed" figure,...

    Model: `api_execution_gpay_total_accounts` — table `dbt.api_execution_gpay_total_accounts`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | The total number of deployed Gnosis Pay accounts. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_total_accounts/all_time"
    ```

## gpay_total_balance

Current total balance across all Gnosis Pay wallets in USD.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_total_balance/all_time` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gpay_total_balance/all_time`"
    Current total balance across all Gnosis Pay wallets in USD.

    Model: `api_execution_gpay_total_balance` — table `dbt.api_execution_gpay_total_balance`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | The total balance in USD. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_total_balance/all_time"
    ```

## gpay_total_funded

All-time total count of funded Gnosis Pay wallets (users who made at least one payment).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_total_funded/all_time` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gpay_total_funded/all_time`"
    All-time total count of funded Gnosis Pay wallets (users who made at least one payment).

    Model: `api_execution_gpay_total_funded` — table `dbt.api_execution_gpay_total_funded`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | The total number of funded wallets. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_total_funded/all_time"
    ```

## gpay_total_payments

All-time total count of Gnosis Pay payments.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_total_payments/all_time` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gpay_total_payments/all_time`"
    All-time total count of Gnosis Pay payments.

    Model: `api_execution_gpay_total_payments` — table `dbt.api_execution_gpay_total_payments`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | The total number of payments. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_total_payments/all_time"
    ```

## gpay_total_volume

All-time total payment volume for Gnosis Pay in USD.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_total_volume/all_time` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gpay_total_volume/all_time`"
    All-time total payment volume for Gnosis Pay in USD.

    Model: `api_execution_gpay_total_volume` — table `dbt.api_execution_gpay_total_volume`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | The total payment volume in USD. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_total_volume/all_time"
    ```

## gpay_user_activity

Individual transaction-level activity for a specific Gnosis Pay user, filtered by wallet address.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_user_activity/latest` | GET, POST | tier0 | `wallet_address`, `action`, `symbol`, `start_date`, `end_date` | limit/offset (list) | date DESC |

??? info "`GET/POST /v1/execution/gpay_user_activity/latest`"
    Individual transaction-level activity for a specific Gnosis Pay user, filtered by wallet address.

    Model: `api_execution_gpay_user_activity` — table `dbt.api_execution_gpay_user_activity`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `wallet_address` | `IN` | `wallet_address` | string_list | Wallet address(es); case: lower; max_items: 20 |
    | `action` | `=` | `action` | string | Action type (Payment, Cashback, Fiat Top Up, etc.) |
    | `symbol` | `=` | `symbol` | string | Token symbol |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** At least one filter required. Must provide one of: `wallet_address`.

    **Pagination:** `limit`/`offset` — default 100, max 5000; response: bare JSON array

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `transaction_hash` | `String` | The unique hash identifier for the transaction. |
    | `wallet_address` | `String` | The Gnosis Pay wallet address. |
    | `timestamp` | `DateTime64(0, 'UTC')` | The UTC timestamp of the transaction. |
    | `date` | `Date` | The calendar date of the transaction. |
    | `action` | `String` | The activity type (e.g., Payment, Deposit, Withdrawal, Cashback). |
    | `symbol` | `String` | The token symbol involved in the transaction. |
    | `direction` | `String` | The direction of the transaction (e.g., inbound, outbound). |
    | `amount` | `Float64` | The decimal-adjusted token amount. |
    | `amount_usd` | `Float64` | The USD-equivalent value of the transaction. |
    | `counterparty` | `String` | The counterparty address in the transaction. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_user_activity/latest?start_date=2026-01-01"
    ```

## gpay_user_balances

Simple API view over latest Gnosis Pay wallet balances.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_user_balances/latest` | GET, POST | tier0 | `wallet_address`, `token` | limit/offset (envelope) | value_usd DESC |
| `/v1/execution/gpay_user_balances/daily` | GET, POST | tier0 | `wallet_address`, `token`, `start_date`, `end_date` | limit/offset (list) | date DESC |

??? info "`GET/POST /v1/execution/gpay_user_balances/latest`"
    Simple API view over latest Gnosis Pay wallet balances.

    Model: `api_execution_gpay_user_balances_latest` — table `dbt.api_execution_gpay_user_balances_latest`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `wallet_address` | `IN` | `wallet_address` | string_list | case: lower; max_items: 20 |
    | `token` | `=` | `token` | string | -- |

    **Filter policy:** At least one filter required. Must provide one of: `wallet_address`.

    **Pagination:** `limit`/`offset` — default 100, max 5000; response: envelope `{items, pagination}`

    **Sort:** `value_usd DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value_usd` | `Float64` | Total USD value of the wallet's holdings of the token at the latest snapshot date. |
    | `wallet_address` | `Nullable(String)` | The Gnosis Pay Safe wallet address holding the balance. |
    | `token` | `String` | The token symbol for the balance. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_user_balances/latest?wallet_address=VALUE1,VALUE2"
    ```

??? info "`GET/POST /v1/execution/gpay_user_balances/daily`"
    Daily token balances for a specific Gnosis Pay user in native and USD values.

    Model: `api_execution_gpay_user_balances_daily` — table `dbt.api_execution_gpay_user_balances_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `wallet_address` | `IN` | `wallet_address` | string_list | Wallet address(es); case: lower; max_items: 20 |
    | `token` | `=` | `token` | string | Token symbol |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** At least one filter required. Must provide one of: `wallet_address`.

    **Pagination:** `limit`/`offset` — default 100, max 5000; response: bare JSON array

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `wallet_address` | `String` | The Gnosis Pay wallet address. |
    | `date` | `Date` | The calendar date of the balance snapshot. |
    | `label` | `String` | The token symbol. |
    | `token` | `String` | The token contract address. |
    | `value_native` | `Float64` | The token balance in native units. |
    | `value_usd` | `Float64` | The token balance in USD. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_user_balances/daily?start_date=2026-01-01"
    ```

## gpay_user_cashback

Daily cashback amounts for a specific Gnosis Pay user.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_user_cashback/daily` | GET, POST | tier0 | `wallet_address`, `start_date`, `end_date` | limit/offset (list) | date DESC |

??? info "`GET/POST /v1/execution/gpay_user_cashback/daily`"
    Daily cashback amounts for a specific Gnosis Pay user.

    Model: `api_execution_gpay_user_cashback_daily` — table `dbt.api_execution_gpay_user_cashback_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `wallet_address` | `IN` | `wallet_address` | string_list | Wallet address(es); case: lower; max_items: 20 |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** At least one filter required. Must provide one of: `wallet_address`.

    **Pagination:** `limit`/`offset` — default 100, max 5000; response: bare JSON array

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `wallet_address` | `String` | The Gnosis Pay wallet address. |
    | `date` | `Date` | The calendar date. |
    | `value` | `Float64` | The cashback amount received on this date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_user_cashback/daily?start_date=2026-01-01"
    ```

## gpay_user_lifetime_metrics

Lifetime metrics for a specific Gnosis Pay user, passing through all columns from the fact model.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_user_lifetime_metrics/all_time` | GET, POST | tier0 | `wallet_address` | -- | -- |

??? info "`GET/POST /v1/execution/gpay_user_lifetime_metrics/all_time`"
    Lifetime metrics for a specific Gnosis Pay user, passing through all columns from the fact model.

    Model: `api_execution_gpay_user_lifetime_metrics` — table `dbt.api_execution_gpay_user_lifetime_metrics`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `wallet_address` | `IN` | `wallet_address` | string_list | Wallet address(es); case: lower; max_items: 50 |

    **Filter policy:** At least one filter required. Must provide one of: `wallet_address`.

    **Pagination:** none (full result set, bare JSON array)

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `wallet_address` | `String` | The Gnosis Pay wallet address. |
    | `first_activity_date` | `Date` | The date of the wallet's first recorded activity. |
    | `last_activity_date` | `Date` | The date of the wallet's most recent activity. |
    | `tenure_days` | `UInt64` | The number of days between first and last activity. |
    | `active_months` | `UInt64` | The number of distinct months the wallet was active. |
    | `total_payment_volume_usd` | `Float64` | Lifetime total payment volume in USD. |
    | `total_payment_count` | `UInt64` | Lifetime total number of payments. |
    | `total_deposit_volume_usd` | `Float64` | Lifetime total deposit volume in USD. |
    | `total_withdrawal_volume_usd` | `Float64` | Lifetime total withdrawal volume in USD. |
    | `net_flow_usd` | `Float64` | Lifetime net flow (deposits minus withdrawals) in USD. |
    | `total_cashback_usd` | `Float64` | Lifetime total cashback received in USD. |
    | `total_cashback_gno` | `Float64` | Lifetime total cashback received in GNO tokens. |
    | `total_refund_usd` | `Float64` | Lifetime total refund value in USD. |
    | `total_refund_count` | `UInt64` | Lifetime total number of refunds. |
    | `avg_monthly_payment_volume_usd` | `Float64` | Average monthly payment volume in USD across active months. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_user_lifetime_metrics/all_time?wallet_address=VALUE1,VALUE2"
    ```

## gpay_user_payments

Daily payment amounts by token for a specific Gnosis Pay user.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_user_payments/daily` | GET, POST | tier0 | `wallet_address`, `token`, `start_date`, `end_date` | limit/offset (list) | date DESC |

??? info "`GET/POST /v1/execution/gpay_user_payments/daily`"
    Daily payment amounts by token for a specific Gnosis Pay user.

    Model: `api_execution_gpay_user_payments_daily` — table `dbt.api_execution_gpay_user_payments_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `wallet_address` | `IN` | `wallet_address` | string_list | Wallet address(es); case: lower; max_items: 20 |
    | `token` | `=` | `label` | string | Token symbol |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** At least one filter required. Must provide one of: `wallet_address`.

    **Pagination:** `limit`/`offset` — default 100, max 5000; response: bare JSON array

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `wallet_address` | `String` | The Gnosis Pay wallet address. |
    | `date` | `Date` | The calendar date. |
    | `label` | `String` | The token symbol. |
    | `value` | `Float64` | The payment amount in USD on this date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_user_payments/daily?start_date=2026-01-01"
    ```

## gpay_user_top_wallets

API view of the top 50 Gnosis Pay wallets by lifetime payment volume. One row per wallet_address, selected from fct_execution_gpay_user_lifetime_metrics where total_payment_count > 0 and ordered by total_payment_volume_usd then tenure_days descending. Adds as_of_date (max date in int_execution_gp...

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_user_top_wallets/snapshot` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/gpay_user_top_wallets/snapshot`"
    API view of the top 50 Gnosis Pay wallets by lifetime payment volume. One row per wallet_address, selected from fct_execution_gpay_user_lifetime_metrics where total_payment_count > 0 and ordered by total_payment_volume_usd then tenure_days descending. Adds as_of_date (max date in int_execution_gp...

    Model: `api_execution_gpay_user_top_wallets` — table `dbt.api_execution_gpay_user_top_wallets`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `wallet_address` | `String` | The Gnosis Pay wallet address, one of the top 50 by lifetime payment volume. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in int_execution_gpay_activity_daily). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_user_top_wallets/snapshot" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_user_total_cashback

All-time total cashback for a specific Gnosis Pay user.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_user_total_cashback/all_time` | GET, POST | tier0 | `wallet_address` | -- | -- |

??? info "`GET/POST /v1/execution/gpay_user_total_cashback/all_time`"
    All-time total cashback for a specific Gnosis Pay user.

    Model: `api_execution_gpay_user_total_cashback` — table `dbt.api_execution_gpay_user_total_cashback`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `wallet_address` | `IN` | `wallet_address` | string_list | Wallet address(es); case: lower; max_items: 50 |

    **Filter policy:** At least one filter required. Must provide one of: `wallet_address`.

    **Pagination:** none (full result set, bare JSON array)

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `wallet_address` | `String` | The Gnosis Pay wallet address. |
    | `value` | `Float64` | The total cashback amount in USD. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_user_total_cashback/all_time?wallet_address=VALUE1,VALUE2"
    ```

## gpay_user_total_payments

All-time total payment count for a specific Gnosis Pay user.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_user_total_payments/all_time` | GET, POST | tier0 | `wallet_address` | -- | -- |

??? info "`GET/POST /v1/execution/gpay_user_total_payments/all_time`"
    All-time total payment count for a specific Gnosis Pay user.

    Model: `api_execution_gpay_user_total_payments` — table `dbt.api_execution_gpay_user_total_payments`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `wallet_address` | `IN` | `wallet_address` | string_list | Wallet address(es); case: lower; max_items: 50 |

    **Filter policy:** At least one filter required. Must provide one of: `wallet_address`.

    **Pagination:** none (full result set, bare JSON array)

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `wallet_address` | `String` | The Gnosis Pay wallet address. |
    | `value` | `UInt64` | The total number of payments. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_user_total_payments/all_time?wallet_address=VALUE1,VALUE2"
    ```

## gpay_user_total_volume

All-time total payment volume for a specific Gnosis Pay user.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_user_total_volume/all_time` | GET, POST | tier0 | `wallet_address` | -- | -- |

??? info "`GET/POST /v1/execution/gpay_user_total_volume/all_time`"
    All-time total payment volume for a specific Gnosis Pay user.

    Model: `api_execution_gpay_user_total_volume` — table `dbt.api_execution_gpay_user_total_volume`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `wallet_address` | `IN` | `wallet_address` | string_list | Wallet address(es); case: lower; max_items: 50 |

    **Filter policy:** At least one filter required. Must provide one of: `wallet_address`.

    **Pagination:** none (full result set, bare JSON array)

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `wallet_address` | `String` | The Gnosis Pay wallet address. |
    | `value` | `Float64` | The total payment volume in USD. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_user_total_volume/all_time?wallet_address=VALUE1,VALUE2"
    ```

## gpay_volume

7-day payment volume with period-over-period change percentage.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_volume/last_7d` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/gpay_volume/last_7d`"
    7-day payment volume with period-over-period change percentage.

    Model: `api_execution_gpay_volume_7d` — table `dbt.api_execution_gpay_volume_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | The total payment volume in USD in the last 7 days. |
    | `change_pct` | `Float64` | The percentage change compared to the previous 7-day period. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_volume/last_7d"
    ```

## gpay_volume_payments_by_token

Daily payment volume by token in USD for Gnosis Pay.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_volume_payments_by_token/daily` | GET | tier1 | `token`, `start_date`, `end_date` | -- | date DESC |
| `/v1/execution/gpay_volume_payments_by_token/weekly` | GET | tier1 | `token`, `start_date`, `end_date` | -- | date DESC |
| `/v1/execution/gpay_volume_payments_by_token/monthly` | GET | tier1 | `token`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/execution/gpay_volume_payments_by_token/daily`"
    Daily payment volume by token in USD for Gnosis Pay.

    Model: `api_execution_gpay_volume_payments_by_token_daily` — table `dbt.api_execution_gpay_volume_payments_by_token_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `label` | string | Token symbol |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The calendar date. |
    | `label` | `String` | The token symbol. |
    | `value` | `Float64` | The payment volume in USD for this token on this date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_volume_payments_by_token/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/gpay_volume_payments_by_token/weekly`"
    Weekly payment volume by token in USD for Gnosis Pay.

    Model: `api_execution_gpay_volume_payments_by_token_weekly` — table `dbt.api_execution_gpay_volume_payments_by_token_weekly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `label` | string | Token symbol |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The first day of the ISO week. |
    | `label` | `String` | The token symbol. |
    | `value` | `Float64` | The payment volume in USD for this token in this week. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_volume_payments_by_token/weekly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/gpay_volume_payments_by_token/monthly`"
    Monthly payment volume by token in USD for Gnosis Pay.

    Model: `api_execution_gpay_volume_payments_by_token_monthly` — table `dbt.api_execution_gpay_volume_payments_by_token_monthly`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `label` | string | Token symbol |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The first day of the month. |
    | `label` | `String` | The token symbol. |
    | `value` | `Float64` | The payment volume in USD for this token in this month. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_volume_payments_by_token/monthly?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## gpay_wallet_balance_composition

Current balance composition of a Gnosis Pay wallet by token.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/gpay_wallet_balance_composition/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/gpay_wallet_balance_composition/latest`"
    Current balance composition of a Gnosis Pay wallet by token.

    Model: `api_execution_gpay_wallet_balance_composition` — table `dbt.api_execution_gpay_wallet_balance_composition`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `name` | `String` | The token symbol or name. |
    | `value` | `Float64` | The balance amount in USD. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/gpay_wallet_balance_composition/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## holders_per_token

This model provides the latest snapshot of the number of holders for each API token, aggregated by token symbol, to support analysis of token holder trends over time.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/holders_per_token/latest` | GET | tier1 | -- | -- | -- |
| `/v1/execution/holders_per_token/daily` | GET | tier1 | `token`, `token_class`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/execution/holders_per_token/latest`"
    This model provides the latest snapshot of the number of holders for each API token, aggregated by token symbol, to support analysis of token holder trends over time.

    Model: `api_execution_tokens_holders_latest_by_token` — table `dbt.api_execution_tokens_holders_latest_by_token`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `token` | `String` | The symbol identifier of the API token. |
    | `value` | `UInt64` | The maximum number of holders for the token up to the most recent date before today. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/holders_per_token/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/holders_per_token/daily`"
    The api_execution_tokens_holders_daily model provides daily aggregated data on the number of unique token holders for each token, supporting analysis of token distribution trends over time.

    Model: `api_execution_tokens_holders_daily` — table `dbt.api_execution_tokens_holders_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `token` | string | Token symbol |
    | `token_class` | `=` | `token_class` | string | Token class (native, stablecoin, bridged, etc.) |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific calendar date for the recorded data point, formatted as YYYY-MM-DD. |
    | `token` | `String` | The symbol identifier of the token, representing the specific digital asset. |
    | `token_class` | `String` | The classification or category of the token, indicating its type or purpose. |
    | `value` | `UInt64` | The number of unique holders for the token on the given date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/holders_per_token/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## projects_and_sectors_count

This view aggregates the total number of distinct projects and sectors crawled, providing a high-level overview of data coverage for the API.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/projects_and_sectors_count/total` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/projects_and_sectors_count/total`"
    This view aggregates the total number of distinct projects and sectors crawled, providing a high-level overview of data coverage for the API.

    Model: `api_crawlers_data_distinct_projects_sectors_totals` — table `dbt.api_crawlers_data_distinct_projects_sectors_totals`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value1` | `Float64` | The total count of unique projects identified in the dataset. |
    | `value2` | `Float64` | The total count of unique sectors associated with the projects. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/projects_and_sectors_count/total"
    ```

## rwa_backedfi_prices

The api_execution_rwa_backedfi_prices_daily model provides daily pricing data for RWA-backed financial instruments to support analytics and reporting.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/rwa_backedfi_prices/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/rwa_backedfi_prices/daily`"
    The api_execution_rwa_backedfi_prices_daily model provides daily pricing data for RWA-backed financial instruments to support analytics and reporting.

    Model: `api_execution_rwa_backedfi_prices_daily` — table `dbt.api_execution_rwa_backedfi_prices_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `bticker` | `String` | Unique identifier for the financial instrument, typically a ticker symbol. |
    | `date` | `Date` | The date of the recorded price, formatted as YYYY-MM-DD. |
    | `price` | `UInt64` | The daily price of the instrument, expressed in its respective currency units. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/rwa_backedfi_prices/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## safe_details

One row per Safe contract with deployment metadata + current-owner-count + current-threshold. Powers the Safe-section summary card in the Account Portfolio tab without needing a second aggregation round-trip. `require_any_of: [safe_address]`.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/safe_details/latest` | GET, POST | tier2 | `safe_address` | limit/offset (envelope) | -- |

??? info "`GET/POST /v1/execution/safe_details/latest`"
    One row per Safe contract with deployment metadata + current-owner-count + current-threshold. Powers the Safe-section summary card in the Account Portfolio tab without needing a second aggregation round-trip. `require_any_of: [safe_address]`.

    Model: `api_execution_safe_details_latest` — table `dbt.api_execution_safe_details_latest`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `safe_address` | `=` | `safe_address` | string | Safe contract address; case: lower |

    **Filter policy:** At least one filter required. Must provide one of: `safe_address`.

    **Pagination:** `limit`/`offset` — default 100, max 1000; response: envelope `{items, pagination}`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `safe_address` | `String` | The Safe proxy address (lowercase, 0x-prefixed). |
    | `creation_version` | `String` | Safe contract version this proxy was set up against. One of 0.1.0, 1.0.0, 1.1.0, 1.1.1, 1.1.1Circles, 1.2.0, 1.3.0, 1.3.0L2, 1.4.1, 1.4.1L2. |
    | `is_l2` | `UInt8` | 1 if the Safe was deployed against a SafeL2 singleton (emits L2-specific transaction events). |
    | `creation_singleton` | `String` | The singleton/mastercopy address the proxy delegatecalls into (lowercase, 0x-prefixed). |
    | `deployment_date` | `Date` | Calendar date of the Safe's creation transaction (block_date of the setup() delegatecall). |
    | `deployment_timestamp` | `DateTime64(0, 'UTC')` | UTC timestamp of the block containing the setup() delegatecall. |
    | `deployment_tx_hash` | `String` | Transaction hash that contained the setup() delegatecall. |
    | `current_owner_count` | `UInt64` | Number of current owners of the Safe (0 when no current-owner rows exist). |
    | `current_threshold` | `Nullable(UInt32)` | Confirmations currently required by this Safe. NULL when no current-owner rows exist. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/safe_details/latest?safe_address=VALUE" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## safes_current_owners

Per-Safe owner list (add-only snapshot). One row per (safe, owner) pair where the last observed event for that pair is `safe_setup` or `added_owner`. Supports filtering on either side so the Account Portfolio tab can query "who owns this safe?" (filter by `safe_address`) and "which safes does thi...

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/safes_current_owners/latest` | GET, POST | tier2 | `safe_address`, `owner_address` | limit/offset (envelope) | became_owner_at DESC |

??? info "`GET/POST /v1/execution/safes_current_owners/latest`"
    Per-Safe owner list (add-only snapshot). One row per (safe, owner) pair where the last observed event for that pair is `safe_setup` or `added_owner`. Supports filtering on either side so the Account Portfolio tab can query "who owns this safe?" (filter by `safe_address`) and "which safes does thi...

    Model: `api_execution_safes_current_owners` — table `dbt.api_execution_safes_current_owners`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `safe_address` | `=` | `safe_address` | string | Safe contract address — returns every current owner of this Safe; case: lower |
    | `owner_address` | `=` | `owner_address` | string | Owner (EOA or contract) address — returns every Safe this address currently owns; case: lower |

    **Filter policy:** At least one filter required. Must provide one of: `safe_address`, `owner_address`.

    **Pagination:** `limit`/`offset` — default 500, max 5000; response: envelope `{items, pagination}`

    **Sort:** `became_owner_at DESC` — user-sortable via `sort_by`: `safe_address`, `owner_address`, `became_owner_at`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `safe_address` | `Nullable(String)` | The Safe address (lowercase, 0x-prefixed). |
    | `owner_address` | `Nullable(String)` | A current owner of the Safe (lowercase, 0x-prefixed). |
    | `became_owner_at` | `DateTime64(0, 'UTC')` | Timestamp of the event that added (or set up) this owner. For an owner who was removed and re-added, this is the re-add time, not the original setup time. |
    | `current_threshold` | `Nullable(UInt32)` | Confirmations currently required by this Safe (denormalised per owner row). |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/safes_current_owners/latest?safe_address=VALUE" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## state_size

The api_execution_state_full_size_daily model provides daily aggregated data on the size of API execution states, facilitating trend analysis and capacity planning.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/state_size/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/state_size/daily`"
    The api_execution_state_full_size_daily model provides daily aggregated data on the size of API execution states, facilitating trend analysis and capacity planning.

    Model: `api_execution_state_full_size_daily` — table `dbt.api_execution_state_full_size_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific calendar date for the recorded data point. |
    | `value` | `Float64` | The size of the execution state in gigabytes, calculated by dividing bytes by 10^9. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/state_size/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## token_balances

Daily per-wallet token balance feed for downstream API consumers. Sourced from int_execution_tokens_balances_daily. The view is wired to the API metadata layer with REQUIRED filters (symbol OR address) and optional date-range filters to prevent unbounded scans.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/token_balances/daily` | GET, POST | tier1 | `symbol`, `address`, `start_date`, `end_date` | limit/offset (list) | date DESC |

??? info "`GET/POST /v1/execution/token_balances/daily`"
    Daily per-wallet token balance feed for downstream API consumers. Sourced from int_execution_tokens_balances_daily. The view is wired to the API metadata layer with REQUIRED filters (symbol OR address) and optional date-range filters to prevent unbounded scans.

    Model: `api_execution_tokens_balances_daily` — table `dbt.api_execution_tokens_balances_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `symbol` | `=` | `symbol` | string | Token symbol |
    | `address` | `IN` | `address` | string_list | Wallet address list; case: lower; max_items: 200 |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** At least one filter required. Must provide one of: `symbol`, `address`.

    **Pagination:** `limit`/`offset` — default 100, max 5000; response: bare JSON array

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | -- |
    | `token_address` | `String` | -- |
    | `symbol` | `String` | -- |
    | `address` | `String` | Holder wallet address (lowercase). |
    | `balance` | `Float64` | Balance in native units. |
    | `balance_usd` | `Float64` | Balance in USD. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/token_balances/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## tokens_overview

Thin API view over fct_execution_tokens_overview_by_class_latest — supply/holders KPI cards per token class with 7-day change.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/tokens_overview/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/tokens_overview/latest`"
    Thin API view over fct_execution_tokens_overview_by_class_latest — supply/holders KPI cards per token class with 7-day change.

    Model: `api_execution_tokens_overview_latest` — table `dbt.api_execution_tokens_overview_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `token_class` | `String` | -- |
    | `label` | `String` | -- |
    | `value` | `Float64` | -- |
    | `change_pct` | `Float64` | -- |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/tokens_overview/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## tokens_supply

This model provides the latest supply values for each API token based on daily recorded data, enabling tracking of token supply trends over time.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/tokens_supply/latest` | GET | tier1 | -- | -- | -- |
| `/v1/execution/tokens_supply/daily` | GET | tier1 | `token`, `token_class`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/execution/tokens_supply/latest`"
    This model provides the latest supply values for each API token based on daily recorded data, enabling tracking of token supply trends over time.

    Model: `api_execution_tokens_supply_latest_by_token` — table `dbt.api_execution_tokens_supply_latest_by_token`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `token` | `String` | The symbol identifier of the API token. |
    | `value` | `Float64` | The most recent supply value of the token, as of the latest date prior to today. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/tokens_supply/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/tokens_supply/daily`"
    The api_execution_tokens_supply_daily model provides daily aggregated data on the supply of different API tokens, supporting analysis of token availability over time.

    Model: `api_execution_tokens_supply_daily` — table `dbt.api_execution_tokens_supply_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `token` | string | Token symbol |
    | `token_class` | `=` | `token_class` | string | Token class (native, stablecoin, bridged, etc.) |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific calendar date for the recorded token supply data. |
    | `token` | `String` | The identifier of the API token, representing different token types or instances. |
    | `token_class` | `String` | The classification or category of the token, indicating its type or usage context. |
    | `value` | `Float64` | The total supply of the token on the given date, measured in units consistent with the supply metric. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/tokens_supply/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## tokens_supply_by_sector

Thin API view over fct_execution_tokens_supply_by_sector_latest — supply distribution by holder sector for the latest day, per token class.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/tokens_supply_by_sector/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/tokens_supply_by_sector/latest`"
    Thin API view over fct_execution_tokens_supply_by_sector_latest — supply distribution by holder sector for the latest day, per token class.

    Model: `api_execution_tokens_supply_by_sector_latest` — table `dbt.api_execution_tokens_supply_by_sector_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `token_class` | `String` | -- |
    | `label` | `String` | Sector name (renamed from sector). |
    | `value` | `Float64` | -- |
    | `value_usd` | `Float64` | -- |
    | `percentage` | `Float64` | -- |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/tokens_supply_by_sector/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## tokens_supply_distribution

Thin API view over fct_execution_tokens_supply_distribution_latest — per-token share of supply within token class on the latest day.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/tokens_supply_distribution/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/tokens_supply_distribution/latest`"
    Thin API view over fct_execution_tokens_supply_distribution_latest — per-token share of supply within token class on the latest day.

    Model: `api_execution_tokens_supply_distribution_latest` — table `dbt.api_execution_tokens_supply_distribution_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `token_class` | `String` | -- |
    | `token` | `String` | -- |
    | `value` | `Float64` | -- |
    | `value_usd` | `Float64` | -- |
    | `percentage` | `Float64` | -- |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/tokens_supply_distribution/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## tokens_top_holders

Thin API view over fct_execution_tokens_top_holders_latest. Returns all holders ranked by balance, with concentration and label columns. Dashboard applies WHERE symbol = {filter} and LIMIT as needed.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/tokens_top_holders/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/tokens_top_holders/latest`"
    Thin API view over fct_execution_tokens_top_holders_latest. Returns all holders ranked by balance, with concentration and label columns. Dashboard applies WHERE symbol = {filter} and LIMIT as needed.

    Model: `api_execution_tokens_top_holders_latest` — table `dbt.api_execution_tokens_top_holders_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `rank` | `UInt64` | Holder rank within token, ordered by balance_usd descending. |
    | `token_address` | `String` | Contract address of the token (lowercase). |
    | `symbol` | `String` | Token symbol. |
    | `token_class` | `String` | Token classification. |
    | `address` | `String` | Holder wallet or contract address. |
    | `label` | `String` | Project label from crawlers_data_labels. NULL if unlabeled. |
    | `label_sector` | `String` | Sector from crawlers_data_labels. NULL if unlabeled. |
    | `balance` | `Float64` | Token balance in native units. |
    | `balance_usd` | `Float64` | Token balance in USD. |
    | `pct_of_total` | `Float64` | Holder's share of total token supply as percentage. |
    | `cumulative_pct` | `Float64` | Running cumulative share of supply from rank 1 downward. |
    | `change_usd_7d` | `Float64` | USD balance change vs 7 days ago. |
    | `unwound_from` | `Array(String)` | Array of container addresses this row was unwound from. Empty for direct holders. |
    | `is_terminal_ubo` | `Nullable(UInt8)` | 1 = label-confirmed end-holder, 0 = undecomposed labeled container, NULL = unclassified. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/tokens_top_holders/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## tokens_ubo_coverage

Thin API view over fct_execution_tokens_ubo_coverage_latest.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/tokens_ubo_coverage/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/tokens_ubo_coverage/latest`"
    Thin API view over fct_execution_tokens_ubo_coverage_latest.

    Model: `api_execution_tokens_ubo_coverage_latest` — table `dbt.api_execution_tokens_ubo_coverage_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `token_address` | `String` | Contract address of the token (lowercase). |
    | `symbol` | `String` | Token symbol. |
    | `token_class` | `String` | Token classification. |
    | `total_usd` | `Float64` | Total USD value of all positive-balance holders for this token on the latest snapshot date. |
    | `pct_direct_terminal` | `Float64` | Share of supply held by direct holders that are label-confirmed terminals. |
    | `pct_unwound_terminal` | `Float64` | Share of supply unwound into label-confirmed terminal addresses. |
    | `pct_unwound_other` | `Float64` | Share of supply unwound but landing on unclassified or container addresses. |
    | `pct_known_container` | `Float64` | Share of supply still held by labeled containers not yet decomposed. |
    | `pct_unclassified` | `Float64` | Share of supply held by addresses with no label. |
    | `pct_unwound_total` | `Float64` | Total share of supply that flowed through any unwind path. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/tokens_ubo_coverage/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## tokens_ubo_venue_breakdown

Thin API view over fct_execution_tokens_ubo_venue_breakdown_latest. One row per (token_address, venue), ordered by token and balance_usd descending, with as_of_date (max date in int_execution_tokens_balances_daily) appended. Tier1 endpoint (api:tokens_ubo_venue_breakdown, granularity:latest).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/tokens_ubo_venue_breakdown/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/tokens_ubo_venue_breakdown/latest`"
    Thin API view over fct_execution_tokens_ubo_venue_breakdown_latest. One row per (token_address, venue), ordered by token and balance_usd descending, with as_of_date (max date in int_execution_tokens_balances_daily) appended. Tier1 endpoint (api:tokens_ubo_venue_breakdown, granularity:latest).

    Model: `api_execution_tokens_ubo_venue_breakdown_latest` — table `dbt.api_execution_tokens_ubo_venue_breakdown_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `token_address` | `String` | Contract address of the token (lowercase). |
    | `symbol` | `String` | Token symbol. |
    | `token_class` | `String` | Token classification. |
    | `venue` | `String` | UBO venue for this slice — a protocol name or the residual 'direct' row. |
    | `balance` | `Float64` | Supply held by this venue for the token, in native units. |
    | `balance_usd` | `Float64` | Supply held by this venue for the token, in USD. |
    | `percentage` | `Float64` | Venue's share of the token's total positive balance, in percent. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/tokens_ubo_venue_breakdown/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## tokens_volume

The api_execution_tokens_volume_daily model provides daily aggregated data on the trading volume of different tokens in both native token units and USD, supporting analysis of token liquidity and trading activity over time.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/tokens_volume/daily` | GET | tier1 | `token`, `token_class`, `start_date`, `end_date` | -- | date DESC |

??? info "`GET /v1/execution/tokens_volume/daily`"
    The api_execution_tokens_volume_daily model provides daily aggregated data on the trading volume of different tokens in both native token units and USD, supporting analysis of token liquidity and trading activity over time.

    Model: `api_execution_tokens_volume_daily` — table `dbt.api_execution_tokens_volume_daily`

    **Declared filters**

    | Parameter | Operator | Column | Type | Notes |
    |-----------|----------|--------|------|-------|
    | `token` | `=` | `token` | string | Token symbol |
    | `token_class` | `=` | `token_class` | string | Token class (native, stablecoin, bridged, etc.) |
    | `start_date` | `>=` | `date` | date | Inclusive start date |
    | `end_date` | `<=` | `date` | date | Inclusive end date |

    **Filter policy:** Unfiltered requests allowed.

    **Pagination:** none (full result set, bare JSON array)

    **Sort:** `date DESC`

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific calendar date for the recorded trading volume data. |
    | `token` | `String` | The identifier of the token for which the volume is reported. |
    | `token_class` | `String` | The classification category of the token, such as utility or security token. |
    | `value_native` | `Float64` | The total trading volume for the token on the given date in native token units. |
    | `value_usd` | `Float64` | The total USD trading volume for the token on the given date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/tokens_volume/daily?start_date=2026-01-01" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## transactions_count

The api_execution_transactions_7d model provides a snapshot of the total number of API execution transactions and their percentage change over the last seven days, supporting operational and performance monitoring.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/transactions_count/last_7d` | GET | tier0 | -- | -- | -- |
| `/v1/execution/transactions_count/all_time` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/transactions_count/last_7d`"
    The api_execution_transactions_7d model provides a snapshot of the total number of API execution transactions and their percentage change over the last seven days, supporting operational and performance monitoring.

    Model: `api_execution_transactions_7d` — table `dbt.api_execution_transactions_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | The total count of API execution transactions recorded over the past 7 days. |
    | `change_pct` | `Float64` | The percentage change in the number of transactions compared to the previous period. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_count/last_7d"
    ```

??? info "`GET /v1/execution/transactions_count/all_time`"
    The api_execution_transactions_total model provides a consolidated count of API execution transactions over the entire available time span, enabling analysis of total transaction volume.

    Model: `api_execution_transactions_total` — table `dbt.api_execution_transactions_total`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | The total number of API execution transactions recorded, representing a cumulative count across all time periods. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_count/all_time"
    ```

## transactions_count_per_project

This view aggregates the total number of API execution transactions across all projects over the entire time period, providing insights into overall transaction volume.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/transactions_count_per_project/all_time` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/transactions_count_per_project/all_time`"
    This view aggregates the total number of API execution transactions across all projects over the entire time period, providing insights into overall transaction volume.

    Model: `api_execution_transactions_by_project_total` — table `dbt.api_execution_transactions_by_project_total`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `label` | `String` | A static label indicating the metric type, in this case 'Transactions'. |
    | `value` | `Float64` | The total count of API execution transactions for all projects over the entire time window. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_count_per_project/all_time"
    ```

## transactions_count_per_project_top20

This view aggregates the top 20 API transaction counts per project within specified time ranges, providing insights into transaction volume distribution and identifying less active projects.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/transactions_count_per_project_top20/in_ranges` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/transactions_count_per_project_top20/in_ranges`"
    This view aggregates the top 20 API transaction counts per project within specified time ranges, providing insights into transaction volume distribution and identifying less active projects.

    Model: `api_execution_transactions_by_project_ranges_top20` — table `dbt.api_execution_transactions_by_project_ranges_top20`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `window` | `String` | The time range for the transaction data, such as 'All', '7D', '30D', or '90D'. |
    | `bucket` | `String` | A categorical label representing individual project identifiers or transaction groupings. |
    | `value` | `Float64` | The total number of transactions for each bucket within the specified time range. |
    | `range` | `String` | Aggregation window (All, 7D, 30D, 90D). |
    | `label` | `String` | Project label (or "Others"). |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_count_per_project_top20/in_ranges"
    ```

## transactions_count_per_project_top5

This view aggregates the top 5 projects by transaction count on a monthly basis, enabling analysis of project activity trends over time.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/transactions_count_per_project_top5/monthly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/transactions_count_per_project_top5/monthly`"
    This view aggregates the top 5 projects by transaction count on a monthly basis, enabling analysis of project activity trends over time.

    Model: `api_execution_transactions_by_project_monthly_top5` — table `dbt.api_execution_transactions_by_project_monthly_top5`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The month and year of the transaction data, formatted as YYYY-MM. |
    | `label` | `String` | The identifier or name of the project associated with the transaction count. |
    | `value` | `Float64` | The number of transactions for the project during the specified month. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_count_per_project_top5/monthly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## transactions_count_per_sector

The api_execution_transactions_by_sector_daily model provides daily aggregated counts of API execution transactions categorized by sector, enabling trend analysis and performance monitoring over time.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/transactions_count_per_sector/daily` | GET | tier1 | -- | -- | -- |
| `/v1/execution/transactions_count_per_sector/weekly` | GET | tier1 | -- | -- | -- |
| `/v1/execution/transactions_count_per_sector/hourly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/transactions_count_per_sector/daily`"
    The api_execution_transactions_by_sector_daily model provides daily aggregated counts of API execution transactions categorized by sector, enabling trend analysis and performance monitoring over time.

    Model: `api_execution_transactions_by_sector_daily` — table `dbt.api_execution_transactions_by_sector_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific date for which the transaction data is recorded, formatted as a date. |
    | `label` | `String` | The sector label associated with the transaction count, representing different business sectors. |
    | `value` | `UInt64` | The total number of API execution transactions for the given sector on the specified date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_count_per_sector/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/transactions_count_per_sector/weekly`"
    The api_execution_transactions_by_sector_weekly model aggregates the number of API execution transactions per sector on a weekly basis to support trend analysis and reporting.

    Model: `api_execution_transactions_by_sector_weekly` — table `dbt.api_execution_transactions_by_sector_weekly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The starting date of the week for which the transaction data is aggregated, formatted as a date. |
    | `label` | `String` | The sector label representing the specific business sector associated with the transactions. |
    | `value` | `UInt64` | The total number of API execution transactions recorded for the sector during the week. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_count_per_sector/weekly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/transactions_count_per_sector/hourly`"
    This view aggregates the total number of API execution transactions per sector on an hourly basis, providing insights into transaction volume trends across different sectors over time.

    Model: `api_execution_transactions_by_sector_hourly` — table `dbt.api_execution_transactions_by_sector_hourly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific hour timestamp representing the time period for the transaction count, in hourly granularity. |
    | `label` | `String` | The sector label categorizing the transactions, used for segmentation analysis. |
    | `value` | `UInt64` | The total number of API execution transactions recorded during the specified hour for the given sector. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_count_per_sector/hourly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## transactions_count_per_type

The api_execution_transactions_cnt_daily model provides a daily summary of successful API transaction counts categorized by transaction type, supporting operational monitoring and trend analysis.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/transactions_count_per_type/daily` | GET | tier1 | -- | -- | -- |
| `/v1/execution/transactions_count_per_type/all_time` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/transactions_count_per_type/daily`"
    The api_execution_transactions_cnt_daily model provides a daily summary of successful API transaction counts categorized by transaction type, supporting operational monitoring and trend analysis.

    Model: `api_execution_transactions_cnt_daily` — table `dbt.api_execution_transactions_cnt_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific calendar date for which the transaction data is aggregated. |
    | `transaction_type` | `String` | The category or type of API transaction being counted. |
    | `value` | `UInt64` | The number of successful transactions of the specified type on the given date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_count_per_type/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/transactions_count_per_type/all_time`"
    This view aggregates the total number of successful API transactions grouped by transaction type across all time, providing insights into transaction volume per category.

    Model: `api_execution_transactions_cnt_total` — table `dbt.api_execution_transactions_cnt_total`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `transaction_type` | `String` | The category or type of API transaction being counted. |
    | `value` | `UInt64` | The total count of successful transactions for the specified transaction type. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_count_per_type/all_time"
    ```

## transactions_fees

The api_execution_transactions_fees_native_7d model provides a snapshot of native transaction fees and their percentage change over the last 7 days, supporting analysis of fee trends and performance metrics.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/transactions_fees/last_7d` | GET | tier0 | -- | -- | -- |
| `/v1/execution/transactions_fees/all_time` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/transactions_fees/last_7d`"
    The api_execution_transactions_fees_native_7d model provides a snapshot of native transaction fees and their percentage change over the last 7 days, supporting analysis of fee trends and performance metrics.

    Model: `api_execution_transactions_fees_native_7d` — table `dbt.api_execution_transactions_fees_native_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | The total amount of native transaction fees collected over the past 7 days. |
    | `change_pct` | `Float64` | The percentage change in native transaction fees compared to the previous period. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_fees/last_7d"
    ```

??? info "`GET /v1/execution/transactions_fees/all_time`"
    The `api_execution_transactions_fees_native_total` model aggregates total native execution transaction fees over all time periods for analytical purposes, supporting business insights into fee accumulation.

    Model: `api_execution_transactions_fees_native_total` — table `dbt.api_execution_transactions_fees_native_total`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | The total amount of native execution transaction fees, represented as a numeric value, aggregated across all relevant transactions. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_fees/all_time"
    ```

## transactions_fees_per_project

This view aggregates total native execution transaction fees per project over the entire available time span, enabling analysis of fee distribution across projects.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/transactions_fees_per_project/all_time` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/transactions_fees_per_project/all_time`"
    This view aggregates total native execution transaction fees per project over the entire available time span, enabling analysis of fee distribution across projects.

    Model: `api_execution_transactions_fees_native_by_project_total` — table `dbt.api_execution_transactions_fees_native_by_project_total`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `label` | `String` | The category label, fixed as 'FeesNative', indicating the metric pertains to native transaction fees. |
    | `value` | `Float64` | The total amount of native execution transaction fees accumulated across all projects, expressed as a numeric value. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_fees_per_project/all_time"
    ```

## transactions_fees_per_project_top20

This view aggregates the top 20 native API transaction fee buckets by project for different time ranges, providing insights into fee distribution and volume.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/transactions_fees_per_project_top20/in_ranges` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/transactions_fees_per_project_top20/in_ranges`"
    This view aggregates the top 20 native API transaction fee buckets by project for different time ranges, providing insights into fee distribution and volume.

    Model: `api_execution_transactions_fees_native_by_project_ranges_top20` — table `dbt.api_execution_transactions_fees_native_by_project_ranges_top20`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `window` | `String` | The time range for the data snapshot, such as 'All', '7D', '30D', or '90D'. |
    | `bucket` | `String` | The specific fee range or category bucket for transactions. |
    | `value` | `Float64` | The total sum of native API transaction fees within the specified bucket and time range. |
    | `range` | `String` | Aggregation window (All, 7D, 30D, 90D). |
    | `label` | `String` | Project label (or "Others"). |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_fees_per_project_top20/in_ranges"
    ```

## transactions_fees_per_project_top5

This view aggregates the top 5 projects by native transaction fees on a monthly basis, providing insights into fee distribution and trends over time.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/transactions_fees_per_project_top5/monthly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/transactions_fees_per_project_top5/monthly`"
    This view aggregates the top 5 projects by native transaction fees on a monthly basis, providing insights into fee distribution and trends over time.

    Model: `api_execution_transactions_fees_native_by_project_monthly_top5` — table `dbt.api_execution_transactions_fees_native_by_project_monthly_top5`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The month and year of the data point, formatted as YYYY-MM. |
    | `label` | `String` | Identifier for the project or category associated with the fee data. |
    | `value` | `Float64` | The total native transaction fees for the project in the specified month, in the relevant currency units. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_fees_per_project_top5/monthly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## transactions_fees_per_sector

This view aggregates daily native transaction fees by sector, providing insights into sector-specific fee trends over time for operational and strategic analysis.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/transactions_fees_per_sector/daily` | GET | tier1 | -- | -- | -- |
| `/v1/execution/transactions_fees_per_sector/weekly` | GET | tier1 | -- | -- | -- |
| `/v1/execution/transactions_fees_per_sector/hourly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/transactions_fees_per_sector/daily`"
    This view aggregates daily native transaction fees by sector, providing insights into sector-specific fee trends over time for operational and strategic analysis.

    Model: `api_execution_transactions_fees_native_by_sector_daily` — table `dbt.api_execution_transactions_fees_native_by_sector_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The calendar date for the recorded transaction fees, formatted as YYYY-MM-DD. |
    | `label` | `String` | The sector name associated with the transaction fees, serving as a categorical identifier. |
    | `value` | `UInt64` | The total sum of native transaction fees for the sector on the given date, expressed in the relevant currency units. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_fees_per_sector/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/transactions_fees_per_sector/weekly`"
    This view aggregates native transaction fees by sector on a weekly basis to support analysis of fee trends across different industry sectors.

    Model: `api_execution_transactions_fees_native_by_sector_weekly` — table `dbt.api_execution_transactions_fees_native_by_sector_weekly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The starting date of the week for which the transaction fees are aggregated, formatted as a date. |
    | `label` | `String` | The name or identifier of the sector associated with the transaction fees. |
    | `value` | `UInt64` | The total sum of native transaction fees for the sector during the specified week, in the relevant currency units. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_fees_per_sector/weekly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/transactions_fees_per_sector/hourly`"
    This view aggregates native transaction fees by sector on an hourly basis, providing insights into fee distribution across different sectors over time.

    Model: `api_execution_transactions_fees_native_by_sector_hourly` — table `dbt.api_execution_transactions_fees_native_by_sector_hourly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific hour for which the transaction fee data is aggregated, formatted as a timestamp. |
    | `label` | `String` | The sector category associated with the transaction fees. |
    | `value` | `UInt64` | The total sum of native transaction fees for the sector during the hour, rounded to two decimal places. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_fees_per_sector/hourly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## transactions_gas_share_per_project

This view calculates the daily share of gas used by each project in relation to the total gas consumption across all projects, providing insights into project-specific gas usage patterns over time.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/transactions_gas_share_per_project/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/transactions_gas_share_per_project/daily`"
    This view calculates the daily share of gas used by each project in relation to the total gas consumption across all projects, providing insights into project-specific gas usage patterns over time.

    Model: `api_execution_transactions_gas_share_by_project_daily` — table `dbt.api_execution_transactions_gas_share_by_project_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific date for which the gas share data is recorded. |
    | `day_gas_used` | `UInt64` | Total gas used across all projects on the given date, measured in gas units. |
    | `label` | `String` | Project label or name associated with the transaction. |
    | `value` | `Float64` | Percentage of gas share for the project on the given date, rounded to 2 decimal places. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_gas_share_per_project/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## transactions_gas_used

This view aggregates daily gas consumption and pricing metrics for successful API transaction executions, facilitating performance and cost analysis at a daily granularity.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/transactions_gas_used/daily` | GET | tier1 | -- | -- | -- |
| `/v1/execution/transactions_gas_used/weekly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/transactions_gas_used/daily`"
    This view aggregates daily gas consumption and pricing metrics for successful API transaction executions, facilitating performance and cost analysis at a daily granularity.

    Model: `api_execution_transactions_gas_used_daily` — table `dbt.api_execution_transactions_gas_used_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The calendar date for the recorded transaction data. |
    | `transaction_type` | `String` | The category or type of API transaction performed on the given date. |
    | `gas_used` | `UInt64` | Total amount of gas consumed by transactions of the specified type on that date, measured in units of gas. |
    | `gas_price_avg` | `Float64` | Average gas price (e.g., in gwei) paid during transactions of the specified type on that date. |
    | `gas_price_median` | `Float64` | Median gas price (e.g., in gwei) paid during transactions of the specified type on that date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_gas_used/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/transactions_gas_used/weekly`"
    This view aggregates weekly gas usage for successful API transactions, categorized by transaction type, to support performance and cost analysis over time.

    Model: `api_execution_transactions_gas_used_weekly` — table `dbt.api_execution_transactions_gas_used_weekly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `DateTime64` | The starting date of the week for which the gas usage data is aggregated. |
    | `label` | `String` | The transaction type or category associated with the gas usage. |
    | `gas_price_avg` | `UInt64` | The average gas price (in wei) during the week for successful transactions, if included. |
    | `gas_price_median` | `Float64` | The median gas price (in wei) during the week for successful transactions, if included. |
    | `value` | `UInt64` | Total gas used in transactions on this date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_gas_used/weekly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## transactions_initiators_count

Daily unique initiator accounts on Gnosis Chain. Uses bitmap merge for accurate deduplication — no double-counting across sectors or projects.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/transactions_initiators_count/daily` | GET | tier1 | -- | -- | -- |
| `/v1/execution/transactions_initiators_count/last_7d` | GET | tier0 | -- | -- | -- |
| `/v1/execution/transactions_initiators_count/all_time` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/transactions_initiators_count/daily`"
    Daily unique initiator accounts on Gnosis Chain. Uses bitmap merge for accurate deduplication — no double-counting across sectors or projects.

    Model: `api_execution_transactions_active_accounts_daily` — table `dbt.api_execution_transactions_active_accounts_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The calendar date. |
    | `value` | `UInt64` | True unique count of addresses that initiated at least one transaction on this date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_initiators_count/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/transactions_initiators_count/last_7d`"
    This view provides a snapshot of the number of active accounts involved in API transactions over the last 7 days, enabling monitoring of account engagement trends.

    Model: `api_execution_transactions_active_accounts_7d` — table `dbt.api_execution_transactions_active_accounts_7d`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | The total count of active accounts within the last 7 days. |
    | `change_pct` | `Float64` | The percentage change in active accounts compared to the previous period. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_initiators_count/last_7d"
    ```

??? info "`GET /v1/execution/transactions_initiators_count/all_time`"
    The `api_execution_transactions_active_accounts_total` model provides a snapshot of the total number of active accounts involved in API execution transactions over all time, supporting business insights into account engagement levels.

    Model: `api_execution_transactions_active_accounts_total` — table `dbt.api_execution_transactions_active_accounts_total`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | The total count of active accounts involved in API execution transactions, representing a numeric value at a specific point in time. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_initiators_count/all_time"
    ```

## transactions_initiators_count_per_project

This view provides a snapshot of the total number of active accounts involved in API execution transactions across all projects, aggregated over the entire time period.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/transactions_initiators_count_per_project/all_time` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/transactions_initiators_count_per_project/all_time`"
    This view provides a snapshot of the total number of active accounts involved in API execution transactions across all projects, aggregated over the entire time period.

    Model: `api_execution_transactions_active_accounts_by_project_total` — table `dbt.api_execution_transactions_active_accounts_by_project_total`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `label` | `String` | A categorical label indicating the metric type, here representing 'ActiveAccounts'. |
    | `value` | `Float64` | The total count of active accounts engaged in API execution transactions, representing an aggregate number. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_initiators_count_per_project/all_time"
    ```

## transactions_initiators_count_per_project_top20

This model identifies the top 20 project ranges with the highest number of active accounts over different time windows, aggregating smaller ranges into an 'Others' category for analysis.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/transactions_initiators_count_per_project_top20/in_ranges` | GET | tier0 | -- | -- | -- |

??? info "`GET /v1/execution/transactions_initiators_count_per_project_top20/in_ranges`"
    This model identifies the top 20 project ranges with the highest number of active accounts over different time windows, aggregating smaller ranges into an 'Others' category for analysis.

    Model: `api_execution_transactions_active_accounts_by_project_ranges_top20` — table `dbt.api_execution_transactions_active_accounts_by_project_ranges_top20`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `window` | `String` | The time window for the snapshot, such as 'All', '7D', '30D', or '90D', indicating the period over which active accounts are measured. |
    | `bucket` | `String` | A specific range or category representing a subset of active accounts, used for segmentation within each time window. |
    | `value` | `Float64` | The count of active accounts within the specified bucket and time window, represented as a floating-point number. |
    | `range` | `String` | Aggregation window (All, 7D, 30D, 90D). |
    | `label` | `String` | Project label (or "Others"). |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_initiators_count_per_project_top20/in_ranges"
    ```

## transactions_initiators_count_per_project_top5

This view aggregates the number of active accounts involved in API execution transactions, focusing on the top 5 projects on a monthly basis to support performance and usage analysis.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/transactions_initiators_count_per_project_top5/monthly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/transactions_initiators_count_per_project_top5/monthly`"
    This view aggregates the number of active accounts involved in API execution transactions, focusing on the top 5 projects on a monthly basis to support performance and usage analysis.

    Model: `api_execution_transactions_active_accounts_by_project_monthly_top5` — table `dbt.api_execution_transactions_active_accounts_by_project_monthly_top5`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The month and year for the recorded metrics, formatted as YYYY-MM. |
    | `label` | `String` | Identifier for the project or category associated with the active accounts, typically representing project names or labels. |
    | `value` | `Float64` | The count of active accounts for the specified project and month. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_initiators_count_per_project_top5/monthly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## transactions_initiators_count_per_sector

This view provides daily counts of active accounts involved in API transaction initiations, segmented by sector, to monitor sector-specific activity trends over time.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/transactions_initiators_count_per_sector/daily` | GET | tier1 | -- | -- | -- |
| `/v1/execution/transactions_initiators_count_per_sector/weekly` | GET | tier1 | -- | -- | -- |
| `/v1/execution/transactions_initiators_count_per_sector/hourly` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/transactions_initiators_count_per_sector/daily`"
    This view provides daily counts of active accounts involved in API transaction initiations, segmented by sector, to monitor sector-specific activity trends over time.

    Model: `api_execution_transactions_active_accounts_by_sector_daily` — table `dbt.api_execution_transactions_active_accounts_by_sector_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The date of the recorded transaction activity, formatted as YYYY-MM-DD. |
    | `label` | `String` | The sector name associated with the transaction activity. |
    | `value` | `UInt64` | The number of unique active accounts for the given sector on the specified date. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_initiators_count_per_sector/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/transactions_initiators_count_per_sector/weekly`"
    This view provides weekly counts of active accounts involved in API execution transactions, segmented by sector, to support monitoring and analysis of transaction activity across different business sectors.

    Model: `api_execution_transactions_active_accounts_by_sector_weekly` — table `dbt.api_execution_transactions_active_accounts_by_sector_weekly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The starting date of the week for which the data is aggregated, formatted as a date. |
    | `label` | `String` | The sector name associated with the transaction activity. |
    | `value` | `UInt64` | The number of active accounts engaged in API execution transactions during the specified week. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_initiators_count_per_sector/weekly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

??? info "`GET /v1/execution/transactions_initiators_count_per_sector/hourly`"
    This view aggregates the count of active accounts involved in API execution transactions, segmented by sector and hourly granularity for performance monitoring and analysis.

    Model: `api_execution_transactions_active_accounts_by_sector_hourly` — table `dbt.api_execution_transactions_active_accounts_by_sector_hourly`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The specific hour timestamp representing the time window of the data, in UTC. |
    | `label` | `String` | The sector label categorizing the accounts based on their business sector. |
    | `value` | `UInt64` | A bitmap-encoded count of unique active accounts within each sector for the given hour. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_initiators_count_per_sector/hourly" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## transactions_xdai_value

This view aggregates daily transaction values for API executions on the xDai network, providing insights into transaction volume and value metrics for operational analysis.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/transactions_xdai_value/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/transactions_xdai_value/daily`"
    This view aggregates daily transaction values for API executions on the xDai network, providing insights into transaction volume and value metrics for operational analysis.

    Model: `api_execution_transactions_value_daily` — table `dbt.api_execution_transactions_value_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | The calendar date for the transaction data, formatted as YYYY-MM-DD. |
    | `transaction_type` | `String` | The category or type of transaction processed on that date. |
    | `xdai_value` | `Float64` | The total value of successful transactions in xDai units for the given date and transaction type. |
    | `xdai_value_avg` | `Float64` | The average transaction value in xDai for successful transactions on that date and type. |
    | `xdai_value_median` | `Float64` | The median transaction value in xDai for successful transactions on that date and type. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/transactions_xdai_value/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## yields_opportunities

Thin API view over fct_execution_yields_opportunities_latest, sorted by yield_apr/yield_apy descending. Powers the yields opportunities table on the yields dashboard (lending markets and LP pools side-by-side).

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/yields_opportunities/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/yields_opportunities/latest`"
    Thin API view over fct_execution_yields_opportunities_latest, sorted by yield_apr/yield_apy descending. Powers the yields opportunities table on the yields dashboard (lending markets and LP pools side-by-side).

    Model: `api_execution_yields_opportunities_latest` — table `dbt.api_execution_yields_opportunities_latest`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `type` | `String` | 'LP' or 'Lending'. |
    | `token` | `String` | Base token symbol (e.g. WETH, USDC.e). |
    | `name` | `String` | Display name. For LPs the pair and address suffix; for lending the token symbol. |
    | `address` | `String` | Contract address. For LPs the pool contract; for lending the reserve token contract. Used for Blockscout links. |
    | `pool_key` | `Nullable(String)` | Exact full pool label for LP opportunities, matching the labels used by pool-filtered metrics. NULL for lending markets. |
    | `rate_trend_14d` | `Array(Float64)` | Last 14 daily yield points ordered oldest to newest. LP rows use fee_apr_7d; lending rows use supply APY. |
    | `yield_apr` | `Nullable(Float64)` | Fee APR (LP rows). |
    | `yield_apy` | `Nullable(Float64)` | Supply APY (lending rows). |
    | `borrow_apy` | `Nullable(Float64)` | Variable borrow APY (lending only, NULL for LPs). |
    | `tvl` | `Nullable(Float64)` | Total value locked in USD (LP pools only, NULL for lending). |
    | `total_supplied` | `Nullable(Float64)` | Total supplied in USD (lending only, NULL for LPs). Sum of all deposit positions. |
    | `total_borrowed` | `Nullable(Float64)` | Total borrowed in USD (lending only, NULL for LPs). Derived from total_supplied * utilization_rate / 100. |
    | `fees_7d` | `Nullable(Float64)` | Fees accrued over the last 7 days in USD (LP only, NULL for lending). |
    | `volume_usd_7d` | `Nullable(Float64)` | Total trading volume in USD over the last 7 days (LP only, NULL for lending). |
    | `net_apr_7d` | `Nullable(Float64)` | Net APR after LVR (fee_apr_7d + lvr_apr_7d). LP only, NULL for lending. |
    | `utilization_rate` | `Nullable(Float64)` | Lending utilization rate as a percentage (total_borrows / total_supply * 100). Lending only, NULL for LPs. |
    | `protocol` | `String` | Protocol name (e.g. Uniswap V3, Swapr V3, Aave V3). |
    | `fee_pct` | `Nullable(Float64)` | Pool swap fee as a percentage (e.g. 0.3 = 0.3%). Static for Uniswap V3, latest dynamic fee for Swapr V3 and Balancer V3. NULL for lending markets. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/yields_opportunities/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## yields_overview_lending_best_apy

Overview KPI card for the best lending supply APY currently available (with the token symbol as label) and 7-day change.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/yields_overview_lending_best_apy/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/yields_overview_lending_best_apy/latest`"
    Overview KPI card for the best lending supply APY currently available (with the token symbol as label) and 7-day change.

    Model: `api_execution_yields_overview_lending_best_apy` — table `dbt.api_execution_yields_overview_lending_best_apy`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | Best supply APY as a percentage. |
    | `change_pct` | `Nullable(Float64)` | Percent change vs the value 7 days earlier. |
    | `label` | `Nullable(String)` | Token symbol offering the best APY. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/yields_overview_lending_best_apy/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## yields_overview_lending_lenders

Overview KPI card for total distinct Aave V3 lenders on Gnosis with 7-day change percentage.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/yields_overview_lending_lenders/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/yields_overview_lending_lenders/latest`"
    Overview KPI card for total distinct Aave V3 lenders on Gnosis with 7-day change percentage.

    Model: `api_execution_yields_overview_lending_lenders` — table `dbt.api_execution_yields_overview_lending_lenders`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | Total distinct Aave V3 lenders (latest). |
    | `change_pct` | `Nullable(Float64)` | Percent change vs the value 7 days earlier. |
    | `label` | `Nullable(String)` | Optional display label for the metric. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/yields_overview_lending_lenders/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## yields_overview_lending_tvl

Overview KPI card for total Aave V3 lending TVL with 7-day change percentage.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/yields_overview_lending_tvl/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/yields_overview_lending_tvl/latest`"
    Overview KPI card for total Aave V3 lending TVL with 7-day change percentage.

    Model: `api_execution_yields_overview_lending_tvl` — table `dbt.api_execution_yields_overview_lending_tvl`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | Total Aave V3 lending TVL in USD (latest). |
    | `change_pct` | `Float64` | Percent change vs the value 7 days earlier. |
    | `label` | `String` | Optional display label for the metric. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/yields_overview_lending_tvl/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## yields_overview_lp_best_apr

Overview KPI card for the best LP fee APR currently available (with the pool name as label) and 7-day change.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/yields_overview_lp_best_apr/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/yields_overview_lp_best_apr/latest`"
    Overview KPI card for the best LP fee APR currently available (with the pool name as label) and 7-day change.

    Model: `api_execution_yields_overview_lp_best_apr` — table `dbt.api_execution_yields_overview_lp_best_apr`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | Best LP fee APR as a percentage. |
    | `change_pct` | `Nullable(Float64)` | Percent change vs the value 7 days earlier. |
    | `label` | `Nullable(String)` | Display name of the pool with the best APR. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/yields_overview_lp_best_apr/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## yields_overview_lp_tvl

Overview KPI card for total LP TVL across Uniswap V3, Swapr V3, Balancer V2/V3 on Gnosis with 7-day change.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/yields_overview_lp_tvl/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/yields_overview_lp_tvl/latest`"
    Overview KPI card for total LP TVL across Uniswap V3, Swapr V3, Balancer V2/V3 on Gnosis with 7-day change.

    Model: `api_execution_yields_overview_lp_tvl` — table `dbt.api_execution_yields_overview_lp_tvl`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | Total LP TVL in USD across all tracked DEX protocols (latest). |
    | `change_pct` | `Nullable(Float64)` | Percent change vs the value 7 days earlier. |
    | `label` | `Nullable(String)` | Optional display label for the metric. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/yields_overview_lp_tvl/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## yields_overview_sdai_apy

Overview KPI card for Savings xDAI (sDAI) APY with 7-day change percentage.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/yields_overview_sdai_apy/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/yields_overview_sdai_apy/latest`"
    Overview KPI card for Savings xDAI (sDAI) APY with 7-day change percentage.

    Model: `api_execution_yields_overview_sdai_apy` — table `dbt.api_execution_yields_overview_sdai_apy`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | Current Savings xDAI (sDAI) APY as a percentage. |
    | `change_pct` | `Nullable(Float64)` | Percent change vs the value 7 days earlier. |
    | `label` | `Nullable(String)` | Optional display label for the metric. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/yields_overview_sdai_apy/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## yields_overview_sdai_supply

Overview KPI card for total sDAI supply with 7-day change percentage.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/yields_overview_sdai_supply/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/yields_overview_sdai_supply/latest`"
    Overview KPI card for total sDAI supply with 7-day change percentage.

    Model: `api_execution_yields_overview_sdai_supply` — table `dbt.api_execution_yields_overview_sdai_supply`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `value` | `Float64` | Total Savings xDAI (sDAI) supply (latest). |
    | `change_pct` | `Nullable(Float64)` | Percent change vs the value 7 days earlier. |
    | `label` | `Nullable(String)` | Optional display label for the metric. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/yields_overview_sdai_supply/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## yields_user_activity

Per-event user activity feed across LP and lending positions (deposits, withdrawals, fee collections, supply/repay, etc.). One row per on-chain action. Sourced from int_execution_yields_user_activity.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/yields_user_activity/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/yields_user_activity/latest`"
    Per-event user activity feed across LP and lending positions (deposits, withdrawals, fee collections, supply/repay, etc.). One row per on-chain action. Sourced from int_execution_yields_user_activity.

    Model: `api_execution_yields_user_activity` — table `dbt.api_execution_yields_user_activity`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `block_timestamp` | `DateTime` | UTC timestamp of the on-chain LP or lending event. |
    | `date` | `Date` | Calendar day of the event (derived from block_timestamp). |
    | `transaction_hash` | `String` | Transaction hash of the event. |
    | `protocol` | `String` | Protocol name — a DEX (Uniswap V3, Swapr V3, Balancer) for LP events or a lending market (Aave V3, SparkLend) for lending events. |
    | `position_address` | `String` | Pool or reserve address depending on the action type. |
    | `wallet_address` | `String` | Wallet address that performed the action. |
    | `action` | `String` | Action label (e.g. 'Deposit', 'Withdraw', 'CollectFees', 'Supply', 'Repay'). |
    | `token_symbol` | `String` | Token symbol of the amount moved. |
    | `token_address` | `String` | Token address of the amount moved (for lending, the reserve address). |
    | `amount` | `Float64` | Action amount in native units. |
    | `amount_usd` | `Nullable(Float64)` | Action amount in USD (NULL when pricing is unavailable). |
    | `source` | `String` | Source model identifier — distinguishes LP vs lending events. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/yields_user_activity/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## yields_user_fee_collections

Thin API view over fct_execution_yields_user_fee_collections_daily — per-day, per-pool LP fee collection amounts for the user portfolio fee-income chart.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/yields_user_fee_collections/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/yields_user_fee_collections/daily`"
    Thin API view over fct_execution_yields_user_fee_collections_daily — per-day, per-pool LP fee collection amounts for the user portfolio fee-income chart.

    Model: `api_execution_yields_user_fee_collections_daily` — table `dbt.api_execution_yields_user_fee_collections_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day of the fee collections. |
    | `provider` | `String` | LP wallet address that collected the fees. |
    | `pool_address` | `String` | Pool contract address the fees were collected from. |
    | `protocol` | `String` | DEX protocol name (Uniswap V3, Swapr V3, Balancer). |
    | `fees_usd` | `Float64` | Total fees collected in USD on this day for this position. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/yields_user_fee_collections/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## yields_user_kpis

Thin API view over fct_execution_yields_user_lifetime_metrics for the "user portfolio KPIs" widget. One row per wallet across LP and lending positions.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/yields_user_kpis/all_time` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/yields_user_kpis/all_time`"
    Thin API view over fct_execution_yields_user_lifetime_metrics for the "user portfolio KPIs" widget. One row per wallet across LP and lending positions.

    Model: `api_execution_yields_user_kpis` — table `dbt.api_execution_yields_user_kpis`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `wallet_address` | `String` | Wallet address (LP provider and/or lending user). |
    | `total_lp_fees_usd` | `Float64` | Lifetime LP fees collected in USD across all pools. |
    | `total_lending_balance_usd` | `Float64` | Current total lending supply balance in USD. |
    | `active_lp_positions` | `UInt64` | Count of currently active LP positions. |
    | `in_range_positions` | `UInt64` | Count of active V3 LP positions where current tick is within range. |
    | `out_of_range_positions` | `UInt64` | Count of active V3 LP positions where current tick is outside range. |
    | `active_lending_positions` | `UInt64` | Count of Aave V3 reserves with positive balance. |
    | `first_yield_date` | `DateTime` | Earliest interaction with any yield source. |
    | `tenure_days` | `Int64` | Days since first yield interaction. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/yields_user_kpis/all_time" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## yields_user_lending_balances

Daily supply balance series per (user, reserve) across Aave V3. Rounded to 6 native decimals and 2 USD decimals for display. Sourced from int_execution_lending_aave_user_balances_daily.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/yields_user_lending_balances/daily` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/yields_user_lending_balances/daily`"
    Daily supply balance series per (user, reserve) across Aave V3. Rounded to 6 native decimals and 2 USD decimals for display. Sourced from int_execution_lending_aave_user_balances_daily.

    Model: `api_execution_yields_user_lending_balances_daily` — table `dbt.api_execution_yields_user_lending_balances_daily`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `date` | `Date` | Calendar day of the supply balance snapshot. |
    | `user_address` | `String` | Address of the aToken holder (lending user). |
    | `reserve_address` | `String` | Address of the underlying reserve token. |
    | `symbol` | `String` | Reserve token symbol from lending_market_mapping. |
    | `balance` | `Float64` | Supply balance in native units. |
    | `balance_usd` | `Float64` | Supply balance in USD. |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/yields_user_lending_balances/daily" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## yields_user_lending_positions

Thin API view over fct_execution_yields_user_lending_positions_latest — current Aave V3 lending positions per user with supply APY.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/yields_user_lending_positions/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/yields_user_lending_positions/latest`"
    Thin API view over fct_execution_yields_user_lending_positions_latest — current Aave V3 lending positions per user with supply APY.

    Model: `api_execution_yields_user_lending_positions` — table `dbt.api_execution_yields_user_lending_positions`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `user_address` | `String` | Address of the aToken holder (lending user). |
    | `reserve_address` | `String` | Address of the underlying reserve token. |
    | `symbol` | `String` | Reserve token symbol from lending_market_mapping. |
    | `balance` | `Float64` | Current supply balance in native token units. |
    | `balance_usd` | `Float64` | Current supply balance in USD. |
    | `supply_apy` | `Nullable(Float64)` | Current supply APY from fct_execution_yields_opportunities_latest. |
    | `protocol` | `String` | Lending protocol name (Aave V3 or SparkLend). |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/yields_user_lending_positions/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## yields_user_lp_positions

Current LP positions per wallet across Uniswap V3, Swapr V3, and Balancer V2/V3. One row per (provider, pool_address[, tick_range]) with capital flows, fees collected, and in-range status. Sourced from int_execution_yields_user_lp_positions.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/yields_user_lp_positions/latest` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/yields_user_lp_positions/latest`"
    Current LP positions per wallet across Uniswap V3, Swapr V3, and Balancer V2/V3. One row per (provider, pool_address[, tick_range]) with capital flows, fees collected, and in-range status. Sourced from int_execution_yields_user_lp_positions.

    Model: `api_execution_yields_user_lp_positions` — table `dbt.api_execution_yields_user_lp_positions`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `provider` | `String` | LP provider wallet address. |
    | `pool_address` | `String` | Pool contract address (lowercase, with 0x prefix). |
    | `protocol` | `String` | DEX protocol name (Uniswap V3, Swapr V3, Balancer V2, Balancer V3). |
    | `tick_lower` | `Nullable(Int64)` | V3 lower tick (NULL for non-V3 pools). |
    | `tick_upper` | `Nullable(Int64)` | V3 upper tick (NULL for non-V3 pools). |
    | `capital_in_usd` | `Float64` | Cumulative USD value of deposits into the position. |
    | `capital_out_usd` | `Float64` | Cumulative USD value of withdrawals from the position. |
    | `fees_collected_usd` | `Float64` | Cumulative LP fees collected in USD. |
    | `is_active` | `UInt8` | 1 if the position currently holds liquidity. |
    | `is_in_range` | `Nullable(UInt8)` | 1 if pool current tick is within [tick_lower, tick_upper] (V3 only). |
    | `pool_current_tick` | `Nullable(Int64)` | Latest tick from Swap events on this pool (V3 only). NULL if no swaps recorded. |
    | `has_unpriced_tokens` | `UInt8` | 1 if at least one token in the pool lacks USD pricing. |
    | `entry_date` | `Date` | Date of the first event for this position. |
    | `last_action_date` | `Date` | Date of the most recent event for this position. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/yields_user_lp_positions/latest" \
      -H "X-API-Key: YOUR_API_KEY"
    ```

## yields_user_top_wallets

Allow-list of ~50 wallet addresses surfaced as "top wallets" on the user portfolio landing dashboard. Combines top Uniswap/Swapr LPs, wallets active in both LP and lending, and top lenders, with stable priority ordering.

| Path | Methods | Tier | Filters | Pagination | Sort |
|------|---------|------|---------|------------|------|
| `/v1/execution/yields_user_top_wallets/snapshot` | GET | tier1 | -- | -- | -- |

??? info "`GET /v1/execution/yields_user_top_wallets/snapshot`"
    Allow-list of ~50 wallet addresses surfaced as "top wallets" on the user portfolio landing dashboard. Combines top Uniswap/Swapr LPs, wallets active in both LP and lending, and top lenders, with stable priority ordering.

    Model: `api_execution_yields_user_top_wallets` — table `dbt.api_execution_yields_user_top_wallets`

    **Legacy endpoint** — GET only, no query parameters, returns the full table.

    **Columns**

    | Column | Type | Description |
    |--------|------|-------------|
    | `wallet_address` | `String` | Wallet address surfaced as a top yields-portfolio wallet. |
    | `as_of_date` | `Date` | Date the snapshot is computed as of (max date in the underlying data). |

    **Example**

    ```bash
    curl "https://api.analytics.gnosis.io/v1/execution/yields_user_top_wallets/snapshot" \
      -H "X-API-Key: YOUR_API_KEY"
    ```
<!-- END AUTO-GENERATED: api-catalog-execution -->
