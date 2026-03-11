---
title: Rate Limits
description: Per-tier rate limits, throttling behavior, and best practices
---

# Rate Limits

The Gnosis Analytics API enforces per-tier rate limits to ensure fair usage and platform stability. Rate limiting is implemented using `slowapi` with in-memory storage and a **fixed-window** strategy.

## Per-Tier Limits

| Tier | Access Level | Rate Limit | Window | Keyed By |
|------|-------------|------------|--------|----------|
| `tier0` | Public | 20 requests/min | 60 seconds | IP address (no key) or API key (if provided) |
| `tier1` | Partner | 100 requests/min | 60 seconds | API key |
| `tier2` | Premium | 500 requests/min | 60 seconds | API key |
| `tier3` | Internal | 10,000 requests/min | 60 seconds | API key |

## How Rate Limiting Works

### Fixed-Window Strategy

Rate limits use a **fixed-window** algorithm. Each 60-second window starts from the first request and resets after 60 seconds elapse. All requests within a window are counted, and the counter resets completely when the window expires.

```
Window 1 (00:00 - 01:00): 0/100 ... 97/100 ... 100/100 ... 429!
Window 2 (01:00 - 02:00): 0/100 (counter resets)
```

### Rate Limit Key

The rate limit key determines which requests share a counter:

- **Authenticated requests:** The rate limit is keyed by the `X-API-Key` header value. Each API key has its own independent counter.
- **Unauthenticated requests:** When no API key is provided (tier0 endpoints), the rate limit is keyed by the client's IP address.

!!! tip "Use your API key on public endpoints"
    If you provide a valid API key on a tier0 endpoint, the rate limit is keyed by your API key instead of your IP. This gives you your own dedicated rate-limit bucket, separate from other users sharing the same IP (e.g., behind a NAT or corporate proxy).

## 429 Response

When the rate limit is exceeded, the API responds with HTTP **429 Too Many Requests**:

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
Retry-After: 42

{
  "detail": "Rate limit exceeded. Try again in 42 seconds."
}
```

### Response Headers

Responses include standard rate limit headers to help clients monitor their usage:

| Header | Present On | Description |
|--------|-----------|-------------|
| `X-RateLimit-Limit` | All responses | Maximum requests allowed in the current window |
| `X-RateLimit-Remaining` | All responses | Requests remaining in the current window |
| `X-RateLimit-Reset` | All responses | Unix timestamp when the current window resets |
| `Retry-After` | 429 responses only | Seconds to wait before the next request will be accepted |

### Reading Rate Limit Headers

```bash
curl -v "https://api.analytics.gnosis.io/v1/consensus/blob_commitments/latest" 2>&1 | grep -i ratelimit
```

Example response headers:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1709251260
```

## Handling Rate Limits in Code

=== "Python"

    ```python
    import time
    import requests

    API_KEY = "sk_live_your_key_here"
    BASE_URL = "https://api.analytics.gnosis.io/v1"

    def fetch_with_retry(url, headers, max_retries=3):
        for attempt in range(max_retries):
            response = requests.get(url, headers=headers)

            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 60))
                print(f"Rate limited. Retrying in {retry_after}s...")
                time.sleep(retry_after)
                continue

            response.raise_for_status()
            return response.json()

        raise Exception("Max retries exceeded")

    data = fetch_with_retry(
        f"{BASE_URL}/consensus/blob_commitments/daily?start_date=2024-01-01",
        headers={"X-API-Key": API_KEY},
    )
    ```

=== "JavaScript"

    ```javascript
    const API_KEY = "sk_live_your_key_here";
    const BASE_URL = "https://api.analytics.gnosis.io/v1";

    async function fetchWithRetry(url, headers, maxRetries = 3) {
      for (let attempt = 0; attempt < maxRetries; attempt++) {
        const response = await fetch(url, { headers });

        if (response.status === 429) {
          const retryAfter = parseInt(response.headers.get("Retry-After") || "60");
          console.log(`Rate limited. Retrying in ${retryAfter}s...`);
          await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
          continue;
        }

        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return await response.json();
      }
      throw new Error("Max retries exceeded");
    }

    const data = await fetchWithRetry(
      `${BASE_URL}/consensus/blob_commitments/daily?start_date=2024-01-01`,
      { "X-API-Key": API_KEY }
    );
    ```

=== "curl (with retry)"

    ```bash
    #!/bin/bash
    URL="https://api.analytics.gnosis.io/v1/consensus/blob_commitments/daily?start_date=2024-01-01"
    API_KEY="sk_live_your_key_here"
    MAX_RETRIES=3

    for i in $(seq 1 $MAX_RETRIES); do
      RESPONSE=$(curl -s -w "\n%{http_code}" \
        -H "X-API-Key: $API_KEY" "$URL")

      HTTP_CODE=$(echo "$RESPONSE" | tail -1)
      BODY=$(echo "$RESPONSE" | sed '$d')

      if [ "$HTTP_CODE" = "429" ]; then
        echo "Rate limited. Retrying in 60s..."
        sleep 60
        continue
      fi

      echo "$BODY"
      break
    done
    ```

## Best Practices

### Reduce Request Volume

- **Cache responses** locally, especially for endpoints with infrequently changing data (`daily`, `weekly`, `monthly`, `all_time` granularities). Daily data only changes once per day -- there is no need to re-fetch it every minute.
- **Use pagination** to fetch data incrementally rather than requesting large result sets repeatedly. Combine with `offset` to resume where you left off.
- **Batch list filters** using POST with `string_list` parameters. Instead of making 100 separate requests for 100 addresses, send a single POST with all addresses in the `address` array.

### Monitor Your Usage

- **Check `X-RateLimit-Remaining`** before making additional requests. When it approaches zero, slow down or wait for the window to reset.
- **Read `X-RateLimit-Reset`** to know exactly when your counter resets, rather than guessing.

### Handle Throttling Gracefully

- **Always respect `Retry-After`** on 429 responses. Do not retry immediately -- the retry will also be rate-limited and waste your allocation in the next window.
- **Implement exponential backoff** as a fallback if `Retry-After` is not present.
- **Avoid tight polling loops.** If you need real-time-ish data, poll the `/latest` endpoint at a reasonable interval (e.g., every 30 seconds) rather than as fast as possible.

### Request Efficient Data

- **Use the most specific granularity** for your use case. If you only need the current value, use `/latest` instead of fetching the entire `/daily` history and taking the last row.
- **Apply date filters** to limit the result set. Requesting `?start_date=2024-01-01` is much cheaper than fetching all-time data.
- **Use the lowest sufficient tier.** Tier0 endpoints are free and require no key. Only use higher tiers when you need the data they expose.

## Upgrading Your Tier

If your application consistently hits rate limits, consider upgrading to a higher tier:

| Current | Upgrade To | Rate Increase |
|---------|-----------|---------------|
| tier0 (20/min) | tier1 | 5x (100/min) |
| tier1 (100/min) | tier2 | 5x (500/min) |
| tier2 (500/min) | tier3 | 20x (10,000/min) |

Contact the Gnosis Analytics team to discuss tier upgrades. See [Authentication](authentication.md) for details on the tier hierarchy and how to obtain keys.

## Next Steps

- [Authentication](authentication.md) -- Understand the tier system and key management.
- [Error Handling](errors.md) -- Full reference of error codes including 429 responses.
- [Filtering & Pagination](filtering.md) -- Reduce request volume by fetching exactly the data you need.
