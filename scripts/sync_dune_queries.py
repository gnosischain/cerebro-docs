#!/usr/bin/env python3
"""
Sync Dune Analytics queries and generate a documentation reference page.

Fetches all queries owned by gnosischain_team via the Dune API and generates
docs/reference/dune-queries.md with searchable query listings and collapsible
SQL code blocks.

Usage:
    DUNE_API_KEY=your_key python scripts/sync_dune_queries.py
    python scripts/sync_dune_queries.py --cache dune_cache.json    # use cached data
    python scripts/sync_dune_queries.py --dry-run                  # preview only
"""

import argparse
import json
import os
import re
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DUNE_API_BASE = "https://api.dune.com/api/v1"
QUERIES_LIST_LIMIT = 100
OWNER = "gnosischain_team"
OUTPUT_FILE = Path(__file__).resolve().parent.parent / "docs" / "reference" / "dune-queries.md"


# ---------------------------------------------------------------------------
# Dune API client
# ---------------------------------------------------------------------------

def get_api_key() -> str:
    """Get Dune API key from environment."""
    key = os.environ.get("DUNE_API_KEY", "")
    if not key:
        print("ERROR: DUNE_API_KEY environment variable not set.")
        sys.exit(1)
    return key


def list_all_queries(api_key: str) -> list[dict]:
    """Paginate through all queries owned by gnosischain_team."""
    if not requests:
        print("ERROR: 'requests' package required. pip install requests")
        sys.exit(1)

    headers = {"X-Dune-Api-Key": api_key}
    all_queries = []
    offset = 0

    while True:
        url = f"{DUNE_API_BASE}/queries"
        params = {
            "limit": QUERIES_LIST_LIMIT,
            "offset": offset,
        }
        print(f"  Fetching queries (offset={offset})...")
        resp = requests.get(url, headers=headers, params=params, timeout=30)
        resp.raise_for_status()

        data = resp.json()
        results = data.get("results", data.get("queries", []))

        if not results:
            break

        all_queries.extend(results)
        offset += len(results)

        # Check if we've got all of them
        total = data.get("total_count", data.get("count"))
        if total and offset >= total:
            break

        # Rate limiting: be polite
        time.sleep(0.2)

    return all_queries


def fetch_query_details(api_key: str, query_id: int) -> dict:
    """Fetch full details for a single query."""
    headers = {"X-Dune-Api-Key": api_key}
    url = f"{DUNE_API_BASE}/query/{query_id}"
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()


# ---------------------------------------------------------------------------
# Cache management
# ---------------------------------------------------------------------------

def save_cache(data: list[dict], cache_path: str) -> None:
    """Save fetched queries to a JSON cache file."""
    with open(cache_path, "w") as f:
        json.dump({"queries": data, "fetched_at": datetime.now(timezone.utc).isoformat()}, f, indent=2)
    print(f"  Cached {len(data)} queries to {cache_path}")


def load_cache(cache_path: str) -> list[dict] | None:
    """Load queries from a cache file if it exists."""
    if not os.path.exists(cache_path):
        return None
    with open(cache_path) as f:
        data = json.load(f)
    queries = data.get("queries", [])
    fetched_at = data.get("fetched_at", "unknown")
    print(f"  Loaded {len(queries)} queries from cache (fetched: {fetched_at})")
    return queries


# ---------------------------------------------------------------------------
# Query grouping
# ---------------------------------------------------------------------------

def group_queries(queries: list[dict]) -> dict[str, list[dict]]:
    """Group queries by naming prefix.

    Examples:
        gnosis_circles_invitation_links_v -> Circles
        gnosis_gp_v2_batches -> GP V2
        api_consensus_validators -> Consensus
    """
    groups = defaultdict(list)

    for q in queries:
        name = q.get("name", q.get("query_name", ""))
        group = _infer_group(name)
        groups[group].append(q)

    # Sort queries within each group by name
    for group in groups:
        groups[group].sort(key=lambda q: q.get("name", q.get("query_name", "")))

    return dict(sorted(groups.items()))


def _infer_group(name: str) -> str:
    """Infer a group name from the query name prefix."""
    name_lower = name.lower()

    # Try known prefixes
    prefixes = [
        ("gnosis_circles", "Circles"),
        ("gnosis_circlesv2", "Circles V2"),
        ("gnosis_gp", "Gnosis Protocol"),
        ("gnosis_safe", "Safe"),
        ("gnosis_pay", "Gnosis Pay"),
        ("gnosis_app", "Gnosis App"),
        ("gnosis_bridge", "Bridges"),
        ("gnosis_chain", "Gnosis Chain"),
        ("gnosis_beacon", "Beacon Chain"),
        ("gnosis_esg", "ESG"),
        ("gnosis_defi", "DeFi"),
        ("gnosis_nft", "NFTs"),
        ("gnosis_token", "Tokens"),
        ("gnosis_validator", "Validators"),
        ("gnosis_staking", "Staking"),
        ("api_", "API Models"),
    ]

    for prefix, group in prefixes:
        if name_lower.startswith(prefix):
            return group

    # Generic gnosis_ prefix
    if name_lower.startswith("gnosis_"):
        # Extract the word after gnosis_
        parts = name_lower.split("_")
        if len(parts) >= 2:
            return parts[1].title()

    return "Other"


# ---------------------------------------------------------------------------
# Markdown generation
# ---------------------------------------------------------------------------

def generate_docs_page(queries: list[dict]) -> str:
    """Generate the full Dune queries reference page."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    groups = group_queries(queries)

    lines = [
        "---",
        "title: Dune Queries Reference",
        "description: Complete catalog of Gnosis Chain Dune Analytics queries",
        "---",
        "",
        "# Dune Queries Reference",
        "",
        f"**Total:** {len(queries)} queries | **Owner:** {OWNER} | **Last synced:** {now}",
        "",
        "This page is auto-generated by `scripts/sync_dune_queries.py`. "
        "Do not edit manually.",
        "",
        "## Overview",
        "",
        "| Group | Queries |",
        "|-------|:-------:|",
    ]

    for group_name, group_queries_list in groups.items():
        anchor = group_name.lower().replace(" ", "-").replace("_", "-")
        lines.append(f"| [{group_name}](#{anchor}) | {len(group_queries_list)} |")

    lines.append("")

    # Generate per-group sections
    for group_name, group_queries_list in groups.items():
        lines.append(f"## {group_name}")
        lines.append("")
        lines.append(f"*{len(group_queries_list)} queries*")
        lines.append("")

        for q in group_queries_list:
            query_id = q.get("query_id", q.get("id", ""))
            name = q.get("name", q.get("query_name", "unnamed"))
            description = q.get("description", "")
            sql = q.get("query_sql", q.get("sql", ""))
            updated = q.get("updated_at", q.get("last_update", ""))
            tags = q.get("tags", [])
            params = q.get("parameters", [])

            # Format updated date
            if updated:
                try:
                    dt = datetime.fromisoformat(updated.replace("Z", "+00:00"))
                    updated_str = dt.strftime("%Y-%m-%d")
                except (ValueError, AttributeError):
                    updated_str = str(updated)[:10]
            else:
                updated_str = "--"

            # Header
            lines.append(f"### {name}")
            lines.append("")
            lines.append(f"**Query ID:** {query_id} | **Updated:** {updated_str}")

            if tags:
                tag_str = ", ".join(f"`{t}`" for t in tags)
                lines.append(f" | **Tags:** {tag_str}")

            lines.append("")

            if description:
                lines.append(f"{description}")
                lines.append("")

            # Parameters
            if params:
                lines.append("**Parameters:**")
                lines.append("")
                for p in params:
                    pname = p.get("key", p.get("name", ""))
                    ptype = p.get("type", "")
                    pdefault = p.get("value", p.get("default", ""))
                    lines.append(f"- `{pname}` ({ptype}): `{pdefault}`")
                lines.append("")

            # SQL in collapsible section
            if sql:
                lines.append('??? note "SQL"')
                lines.append("    ```sql")
                for sql_line in sql.strip().split("\n"):
                    lines.append(f"    {sql_line}")
                lines.append("    ```")
                lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Sync Dune Analytics queries and generate documentation."
    )
    parser.add_argument(
        "--cache",
        help="Path to cache file for saving/loading API responses",
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Show what would be generated without writing files",
    )
    parser.add_argument(
        "--output", "-o",
        default=str(OUTPUT_FILE),
        help=f"Output file path (default: {OUTPUT_FILE})",
    )
    parser.add_argument(
        "--skip-details",
        action="store_true",
        help="Skip fetching full query details (SQL, params). Only list metadata.",
    )
    args = parser.parse_args()

    queries = None

    # Try cache first
    if args.cache:
        queries = load_cache(args.cache)

    # Fetch from API if no cache
    if queries is None:
        api_key = get_api_key()
        print(f"Fetching queries from Dune API (owner: {OWNER})...")
        queries = list_all_queries(api_key)
        print(f"  Found {len(queries)} queries.")

        # Fetch full details (SQL, params, tags) unless --skip-details
        if not args.skip_details:
            print("  Fetching full details for each query...")
            detailed = []
            for i, q in enumerate(queries):
                qid = q.get("query_id", q.get("id"))
                if qid:
                    try:
                        detail = fetch_query_details(api_key, qid)
                        detailed.append(detail)
                        if (i + 1) % 50 == 0:
                            print(f"    {i + 1}/{len(queries)} fetched...")
                        time.sleep(0.1)
                    except Exception as e:
                        print(f"    WARNING: Failed to fetch query {qid}: {e}")
                        detailed.append(q)
            queries = detailed
            print(f"  Fetched details for {len(queries)} queries.")

        # Save to cache
        cache_path = args.cache or "dune_cache.json"
        save_cache(queries, cache_path)

    # Generate docs
    print("\nGenerating documentation page...")
    content = generate_docs_page(queries)

    output_path = Path(args.output)
    if args.dry_run:
        print(f"\n[DRY-RUN] Would write {len(content)} chars to {output_path}")
        groups = group_queries(queries)
        print(f"\nGroups ({len(groups)}):")
        for name, qs in groups.items():
            print(f"  {name}: {len(qs)} queries")
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")
        print(f"Wrote {len(content)} chars to {output_path}")

    print(f"\nTotal: {len(queries)} queries synced.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
