#!/usr/bin/env python3
"""
Auto-update documentation from dbt manifest, API metadata, and dashboard config.

Replaces content between marker comments:
    <!-- BEGIN AUTO-GENERATED: section-id -->
    ...
    <!-- END AUTO-GENERATED: section-id -->

Hand-written prose outside markers is preserved.

Usage:
    python scripts/update_docs.py                            # fetch live manifest
    python scripts/update_docs.py --manifest ./manifest.json # use local manifest
    python scripts/update_docs.py --dry-run                  # preview changes
    python scripts/update_docs.py --only models              # update only model pages
    python scripts/update_docs.py --only api                 # update only API endpoints
    python scripts/update_docs.py --only dashboard           # update only dashboard sectors
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MANIFEST_URL = "https://gnosischain.github.io/dbt-cerebro/manifest.json"
GRAPH_DATA_URL = "https://gnosischain.github.io/dbt-cerebro/graph_data.json"
SEMANTIC_REGISTRY_URL = "https://gnosischain.github.io/dbt-cerebro/semantic_registry.json"
API_BASE_URL = "https://api.analytics.gnosis.io"
DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
MKDOCS_YML = Path(__file__).resolve().parent.parent / "mkdocs.yml"
CATALOG_DIR = DOCS_DIR / "api" / "catalog"
CATALOG_JSON = DOCS_DIR / "api" / "catalog_data.json"
GRAPH_DATA_FILE = (
    DOCS_DIR / "data-pipeline" / "transformation" / "semantic-layer" / "graph_data.json"
)
GRAPH_PAGE = DOCS_DIR / "data-pipeline" / "transformation" / "semantic-layer" / "graph.md"

MARKER_BEGIN = "<!-- BEGIN AUTO-GENERATED: {} -->"
MARKER_END = "<!-- END AUTO-GENERATED: {} -->"

LAYER_ORDER = {"stg": 0, "int": 1, "fct": 2, "api": 3}
LAYER_NAMES = {"stg": "Staging", "int": "Intermediate", "fct": "Fact", "api": "API"}

SYSTEM_TAGS = {
    "production", "view", "table", "incremental", "staging", "intermediate",
    "ephemeral", "seed", "snapshot",
}

TIER_TAGS = {"tier0", "tier1", "tier2", "tier3"}

GRANULARITY_ORDER = [
    "latest", "daily", "weekly", "monthly",
    "last_7d", "last_30d", "in_ranges", "all_time",
]

# Known module slugs and their display names.
# Only tags listed here (or mapped via TAG_TO_MODULE) produce docs pages.
MODULE_DISPLAY = {
    "execution": "Execution",
    "consensus": "Consensus",
    "bridges": "Bridges",
    "p2p": "P2P Network",
    "contracts": "Contracts",
    "esg": "ESG",
    "probelab": "ProbeLab",
    "crawlers": "Crawlers",
    "celo": "Celo (Gnosis Pay)",
    "revenue": "Revenue",
    "quarterly_data": "Quarterly Data",
    "mixpanel_ga": "Web Analytics (Mixpanel/GA)",
    "mta": "MTA (Attribution)",
    "mmm": "MMM (Marketing Mix)",
}

# Map non-obvious tags to canonical module slugs.
# Models with these tags are grouped under the mapped module.
TAG_TO_MODULE = {
    "crawlers_data": "crawlers",
    "nebula_discv4": "p2p",
    "nebula_discv5": "p2p",
    "discv4": "p2p",
    "discv5": "p2p",
    "gpay": "execution",
    "yields": "execution",
    "circles": "contracts",
    "tokens": "execution",
    "dev": None,  # exclude dev/internal models from docs
    "dune": "crawlers",
    "aave": "contracts",
    "spark": "contracts",
}

# ---------------------------------------------------------------------------
# API mirror constants
#
# These mirror cerebro-api's DynamicRouter semantics (app/factory.py). They are
# intentionally DIFFERENT from the docs-module constants above: the API derives
# its category from the first non-system bare tag, while the docs model catalog
# groups by curated module mappings. Keep this set in sync with
# DynamicRouter._extract_category.
# ---------------------------------------------------------------------------

API_SYSTEM_TAGS = {
    "production", "view", "table", "incremental", "staging",
    "intermediate", "daily", "weekly", "monthly", "hourly",
    "latest", "in_ranges", "last_30d", "last_7d", "all_time",
}

TIER_TAG_RE = re.compile(r"^tier\d+$")

CATEGORY_DISPLAY = {
    "execution": "Execution",
    "consensus": "Consensus",
    "celo": "Celo",
    "revenue": "Revenue",
    "quarterly_data": "Quarterly Data",
    "bridges": "Bridges",
    "p2p": "P2P",
    "esg": "ESG",
    "mta": "MTA",
    "mmm": "MMM",
    "crawlers_data": "Crawlers Data",
}


# ---------------------------------------------------------------------------
# Manifest loading
# ---------------------------------------------------------------------------

def load_manifest(path_or_url: str) -> dict:
    """Load dbt manifest from a local file or URL."""
    if os.path.isfile(path_or_url):
        print(f"Loading manifest from local file: {path_or_url}")
        with open(path_or_url, "r") as f:
            return json.load(f)

    if not requests:
        print("ERROR: 'requests' package required for URL fetch. pip install requests")
        sys.exit(1)

    print(f"Fetching manifest from {path_or_url} ...")
    resp = requests.get(path_or_url, timeout=60)
    resp.raise_for_status()
    print(f"Downloaded manifest ({len(resp.content)} bytes).")
    return resp.json()


def extract_models(manifest: dict) -> list[dict]:
    """Extract model metadata from manifest nodes."""
    models = []
    for key, node in manifest.get("nodes", {}).items():
        if node.get("resource_type") != "model":
            continue
        name = node.get("name", "")
        tags = node.get("tags", [])
        description = node.get("description", "").strip()
        columns = node.get("columns", {})

        # Mirror cerebro-api extract_raw_api_metadata: config.meta.api wins,
        # then node-level meta.api; track presence separately from content so
        # legacy models (no meta.api) are distinguishable from empty ones.
        meta_api_exists = False
        meta_api = {}
        config_meta = node.get("config", {}).get("meta")
        node_meta = node.get("meta")
        if isinstance(config_meta, dict) and "api" in config_meta:
            meta_api_exists = True
            meta_api = config_meta.get("api") or {}
        elif isinstance(node_meta, dict) and "api" in node_meta:
            meta_api_exists = True
            meta_api = node_meta.get("api") or {}
        if not isinstance(meta_api, dict):
            meta_api = {}

        relation = node.get("relation_name") or ""
        if not relation:
            schema = node.get("schema", "")
            alias = node.get("alias") or name
            relation = f"{schema}.{alias}" if schema else alias

        models.append({
            "name": name,
            "tags": tags,
            "description": description,
            "columns": columns,
            "meta_api": meta_api,
            "meta_api_exists": meta_api_exists,
            "relation_name": relation.replace("`", "").replace('"', ""),
        })
    return models


# ---------------------------------------------------------------------------
# Model classification helpers
# ---------------------------------------------------------------------------

def get_layer(name: str) -> tuple[str, str]:
    """Return (layer_prefix, display_name) for a model name."""
    prefix = name.split("_")[0] if "_" in name else ""
    return prefix, LAYER_NAMES.get(prefix, prefix.upper())


def get_module(tags: list[str]) -> str | None:
    """Derive the module from tags (first recognized module tag).

    Uses TAG_TO_MODULE for aliases and MODULE_DISPLAY for known modules.
    Unknown tags are ignored -- only known modules produce docs pages.
    """
    for tag in tags:
        if tag in SYSTEM_TAGS or tag in TIER_TAGS:
            continue
        if ":" in tag:
            continue
        # Check explicit mapping first
        if tag in TAG_TO_MODULE:
            return TAG_TO_MODULE[tag]  # may be None to exclude
        # Check known modules
        if tag in MODULE_DISPLAY:
            return tag
    return None


def get_entity(name: str) -> str:
    """Extract entity from model name (3rd segment).

    Example: int_execution_blocks_daily -> blocks
    """
    parts = name.split("_")
    if len(parts) >= 3:
        # For stg_ models with double underscore: stg_execution__blocks -> blocks
        # Rejoin and split on __ first
        full = name
        if "__" in full:
            after = full.split("__", 1)[1]
            return after.split("_")[0]
        return parts[2]
    return name


def get_granularity_from_name(name: str) -> str:
    """Guess granularity from the model name suffix."""
    for gran in GRANULARITY_ORDER:
        if name.endswith(f"_{gran}"):
            return gran
    return ""


# ---------------------------------------------------------------------------
# Marker-based file editing
# ---------------------------------------------------------------------------

# Freshness stamp emitted as the first line inside every marker block.
# update_file compares stamp-stripped text so a date-only difference never
# dirties a file (keeps repeated runs idempotent).
STAMP_RE = re.compile(r"<!-- generated: \d{4}-\d{2}-\d{2} -->\n")


def replace_marker_content(text: str, marker_id: str, new_content: str) -> str:
    """Replace content between BEGIN/END markers. Return updated text."""
    begin = MARKER_BEGIN.format(marker_id)
    end = MARKER_END.format(marker_id)
    pattern = re.compile(
        re.escape(begin) + r"\n.*?" + re.escape(end),
        re.DOTALL,
    )
    stamp = f"<!-- generated: {date.today().isoformat()} -->\n"
    replacement = f"{begin}\n{stamp}{new_content}\n{end}"
    if pattern.search(text):
        return pattern.sub(replacement.replace("\\", "\\\\"), text)
    # Markers not found -- do nothing
    return text


def update_file(filepath: Path, marker_id: str, new_content: str,
                dry_run: bool = False) -> bool:
    """Update a file's marker section. Returns True if content changed."""
    if not filepath.exists():
        return False

    original = filepath.read_text(encoding="utf-8")
    updated = replace_marker_content(original, marker_id, new_content)

    if updated == original:
        return False
    # Ignore date-only differences (stamp refresh without content change),
    # but still write when THIS marker's block has no stamp yet (initial
    # adoption). Files may hold several marker blocks, so scope the check.
    block_stamped = f"{MARKER_BEGIN.format(marker_id)}\n<!-- generated: " in original
    if (block_stamped
            and STAMP_RE.sub("", updated) == STAMP_RE.sub("", original)):
        return False

    if dry_run:
        print(f"  [DRY-RUN] Would update {filepath.relative_to(DOCS_DIR.parent)}"
              f" (marker: {marker_id})")
    else:
        filepath.write_text(updated, encoding="utf-8")
        print(f"  Updated {filepath.relative_to(DOCS_DIR.parent)}"
              f" (marker: {marker_id})")
    return True


# ---------------------------------------------------------------------------
# Model catalog generation
# ---------------------------------------------------------------------------

def generate_module_tables(models: list[dict], module: str) -> str:
    """Generate markdown tables for a module, grouped by entity."""
    # Filter models belonging to this module
    module_models = []
    for m in models:
        mod = get_module(m["tags"])
        if mod == module:
            module_models.append(m)

    if not module_models:
        return "*No models found for this module.*\n"

    # Group by entity
    entities: dict[str, list[dict]] = defaultdict(list)
    for m in module_models:
        entity = get_entity(m["name"])
        entities[entity].append(m)

    lines = []
    for entity in sorted(entities.keys()):
        ent_models = entities[entity]
        # Sort by layer order then name
        ent_models.sort(key=lambda m: (
            LAYER_ORDER.get(m["name"].split("_")[0], 99),
            m["name"],
        ))

        lines.append(f"**{entity.replace('_', ' ').title()}**\n")
        lines.append("| Model | Layer | Description |")
        lines.append("|-------|-------|-------------|")
        for m in ent_models:
            _, layer_name = get_layer(m["name"])
            desc = m["description"] or "--"
            # Truncate long descriptions
            if len(desc) > 120:
                desc = desc[:117] + "..."
            lines.append(f"| `{m['name']}` | {layer_name} | {desc} |")
        lines.append("")

    return "\n".join(lines)


def generate_module_summary(models: list[dict]) -> str:
    """Generate the module summary table for models/index.md."""
    module_counts: dict[str, int] = defaultdict(int)
    for m in models:
        mod = get_module(m["tags"])
        if mod:
            module_counts[mod] += 1

    # Merge known modules with discovered ones
    all_modules = set(MODULE_DISPLAY.keys()) | set(module_counts.keys())

    lines = [
        "| Module | Models | Description |",
        "|--------|:------:|-------------|",
    ]
    for mod in sorted(all_modules):
        count = module_counts.get(mod, 0)
        display = MODULE_DISPLAY.get(mod, mod.replace("_", " ").title())
        # Link to module page
        slug = mod.lower().replace(" ", "-")
        lines.append(f"| [{display}]({slug}.md) | ~{count} | -- |")

    return "\n".join(lines)


def update_models(models: list[dict], dry_run: bool = False) -> int:
    """Update all model catalog pages. Returns count of files changed."""
    changes = 0
    models_dir = DOCS_DIR / "models"

    # 1. Module summary in index.md
    summary = generate_module_summary(models)
    if update_file(models_dir / "index.md", "models-summary", summary, dry_run):
        changes += 1

    # 2. Per-module pages
    module_set: set[str] = set()
    for m in models:
        mod = get_module(m["tags"])
        if mod:
            module_set.add(mod)

    for module in sorted(module_set):
        slug = module.lower().replace(" ", "-")
        filepath = models_dir / f"{slug}.md"
        marker_id = f"models-{slug}"

        # Auto-create new module pages if they don't exist
        if not filepath.exists():
            display = MODULE_DISPLAY.get(module, module.replace("_", " ").title())
            template = (
                f"# {display} Module\n\n"
                f"{MARKER_BEGIN.format(marker_id)}\n"
                f"{MARKER_END.format(marker_id)}\n"
            )
            if dry_run:
                print(f"  [DRY-RUN] Would create new module page: {filepath.name}")
            else:
                filepath.write_text(template, encoding="utf-8")
                print(f"  Created new module page: {filepath.name}")
            _add_to_nav(slug, display, dry_run)
            changes += 1

        tables = generate_module_tables(models, module)
        if update_file(filepath, marker_id, tables, dry_run):
            changes += 1

    return changes


# ---------------------------------------------------------------------------
# API endpoint catalog generation
#
# Mirrors cerebro-api's DynamicRouter (app/factory.py) + api_metadata.py so
# the documented paths/behavior match the live API exactly. The API also
# supports manual overrides via an api_config.yaml deployed alongside the
# service; none is committed, so overrides are not modeled here.
# ---------------------------------------------------------------------------

def api_category(tags: list[str]) -> str:
    """First non-system, non-tier, colon-free tag, lowercased (factory._extract_category)."""
    for tag in tags:
        tag_lower = tag.lower()
        if tag_lower in API_SYSTEM_TAGS:
            continue
        if TIER_TAG_RE.match(tag_lower):
            continue
        if ":" in tag:
            continue
        return tag_lower
    return "general"


def api_resource(tags: list[str]) -> str | None:
    """Value of the first non-empty api:* tag, stripped (factory._extract_api_resource)."""
    for tag in tags:
        if tag.startswith("api:"):
            resource = tag[4:].strip()
            if resource:
                return resource
    return None


def api_granularity(tags: list[str]) -> str:
    for tag in tags:
        if tag.startswith("granularity:"):
            granularity = tag[12:].strip().lower()
            if granularity:
                return granularity
    return ""


def api_window(tags: list[str]) -> str:
    for tag in tags:
        if tag.startswith("window:"):
            window = tag[7:].strip().lower()
            if window:
                return window
    return ""


def api_tier(tags: list[str]) -> str:
    for tag in tags:
        if TIER_TAG_RE.match(tag.lower()):
            return tag.lower()
    return "tier0"  # settings.DEFAULT_ENDPOINT_TIER


def build_api_path(category: str, resource: str, granularity: str, window: str) -> str:
    """Mirror factory._build_url_path (mounted under /v1)."""
    parts = [category, resource]
    if granularity:
        parts.append(granularity)
    if window and window != granularity:
        parts.append(window)
    return "/v1/" + "/".join(parts)


def parse_meta_api(model: dict, warnings: list[str]) -> dict | None:
    """Mirror of api_metadata.build_api_behavior.

    Returns None when the metadata would make the live API raise
    ApiMetadataError and skip the endpoint — documenting such a model would
    describe a route that 404s in production. The specific validations
    mirrored here are the ones observed failing in the wild (unknown
    columns, unfiltered contract violations); each skip is warned loudly so
    the upstream dbt model can be fixed.
    """
    legacy = {
        "legacy": True,
        "methods": ["GET"],
        "allow_unfiltered": True,
        "require_any_of": [],
        "exclude_from_api": False,
        "parameters": [],
        "pagination": {"enabled": False, "default_limit": None,
                       "max_limit": None, "response": "list"},
        "sort": [],
        "sortable_fields": [],
    }
    if not model.get("meta_api_exists"):
        return legacy

    raw = model.get("meta_api") or {}
    name = model["name"]
    column_names = set((model.get("columns") or {}).keys())

    def invalid(reason: str):
        warnings.append(
            f"{name}: meta.api invalid ({reason}) — the live API skips this "
            "endpoint; excluded from docs. Fix the dbt model."
        )
        return None

    try:
        methods = []
        for m in raw.get("methods", ["GET"]) or ["GET"]:
            method = str(m).strip().upper()
            if method not in ("GET", "POST"):
                return invalid(f"unsupported method '{method}'")
            if method not in methods:
                methods.append(method)
        if not methods:
            return invalid("empty methods list")

        parameters = []
        for p in raw.get("parameters") or []:
            if not isinstance(p, dict) or not p.get("name") or not p.get("column"):
                return invalid("parameter entry missing name/column")
            column = str(p["column"]).strip()
            if column not in column_names:
                return invalid(f"parameter '{p['name']}' references unknown column '{column}'")
            op = str(p.get("operator", "=")).strip().upper()
            if op not in ("=", ">=", "<=", "ILIKE", "IN"):
                return invalid(f"parameter '{p['name']}' uses unsupported operator '{op}'")
            param_type = str(p.get("type", "string")).strip().lower()
            if param_type not in ("string", "date", "string_list"):
                return invalid(f"parameter '{p['name']}' uses unsupported type '{param_type}'")
            if op == "IN" and param_type != "string_list":
                return invalid(f"parameter '{p['name']}' uses IN without type string_list")
            if p.get("case") and param_type not in ("string", "string_list"):
                return invalid(f"parameter '{p['name']}' case mode on non-string type")
            if p.get("max_items") is not None and param_type != "string_list":
                return invalid(f"parameter '{p['name']}' max_items on non-string_list type")
            parameters.append({
                "name": str(p["name"]).strip(),
                "column": column,
                "op": op,
                "type": param_type,
                "desc": (p.get("description") or "").strip(),
                "case": p.get("case"),
                "max_items": p.get("max_items"),
            })

        allow_unfiltered = bool(raw.get("allow_unfiltered", False))
        require_any_of = [str(x).strip() for x in raw.get("require_any_of") or []]
        param_names = {p["name"] for p in parameters}
        missing_required = [n for n in require_any_of if n not in param_names]
        if missing_required:
            return invalid(f"require_any_of references undeclared parameters {missing_required}")
        if not allow_unfiltered and not parameters:
            return invalid("allow_unfiltered=false with no declared parameters")

        raw_pag = raw.get("pagination") or {}
        pagination = {
            "enabled": bool(raw_pag.get("enabled", False)),
            "default_limit": raw_pag.get("default_limit"),
            "max_limit": raw_pag.get("max_limit"),
            "response": str(raw_pag.get("response", "list")).strip().lower(),
        }
        if pagination["enabled"] and (
            not isinstance(pagination["default_limit"], int)
            or not isinstance(pagination["max_limit"], int)
            or pagination["default_limit"] > pagination["max_limit"]
        ):
            return invalid("pagination enabled with invalid default_limit/max_limit")
        if not pagination["enabled"]:
            pagination["default_limit"] = None
            pagination["max_limit"] = None

        sort = []
        for s in raw.get("sort") or []:
            if not isinstance(s, dict) or not s.get("column"):
                return invalid("sort entry missing column")
            column = str(s["column"]).strip()
            if column not in column_names:
                return invalid(f"sort references unknown column '{column}'")
            sort.append({
                "column": column,
                "dir": str(s.get("direction", "ASC")).strip().upper(),
            })

        sortable_fields = []
        for f in raw.get("sortable_fields") or []:
            field = str(f).strip()
            if field not in column_names:
                return invalid(f"sortable_fields references unknown column '{field}'")
            if field not in sortable_fields:
                sortable_fields.append(field)

        return {
            "legacy": False,
            "methods": methods,
            "allow_unfiltered": allow_unfiltered,
            "require_any_of": require_any_of,
            "exclude_from_api": bool(raw.get("exclude_from_api", False)),
            "parameters": parameters,
            "pagination": pagination,
            "sort": sort,
            "sortable_fields": sortable_fields,
        }
    except (ValueError, TypeError, AttributeError) as exc:
        return invalid(str(exc))


def _truncate(text: str, limit: int) -> str:
    text = " ".join((text or "").split())
    if len(text) > limit:
        return text[: limit - 3] + "..."
    return text


def _md_cell(text: str) -> str:
    """Make text safe inside a markdown table cell."""
    return (text or "").replace("|", "\\|").replace("\n", " ").strip() or "--"


def build_api_catalog(models: list[dict]) -> dict:
    """Build the endpoint catalog shared by the static pages and explorer JSON."""
    warnings: list[str] = []
    skipped_by_category: dict[str, int] = defaultdict(int)
    endpoints = []
    for m in models:
        tags = m["tags"]
        if "production" not in tags:
            continue
        resource = api_resource(tags)
        if not resource:
            continue
        behavior = parse_meta_api(m, warnings)
        if behavior is None:
            skipped_by_category[api_category(tags)] += 1
            continue
        if behavior["exclude_from_api"]:
            continue

        category = api_category(tags)
        granularity = api_granularity(tags)
        window = api_window(tags)
        path = build_api_path(category, resource, granularity, window)

        columns = []
        for col_name, col in (m.get("columns") or {}).items():
            columns.append({
                "name": col_name,
                "type": (col or {}).get("data_type") or "",
                "desc": _truncate((col or {}).get("description") or "", 160),
            })

        gran_rank = (
            GRANULARITY_ORDER.index(granularity) + 1
            if granularity in GRANULARITY_ORDER
            else (0 if not granularity else len(GRANULARITY_ORDER) + 1)
        )
        endpoints.append({
            "path": path,
            "category": category,
            "resource": resource,
            "granularity": granularity,
            "window": "" if window == granularity else window,
            "tier": api_tier(tags),
            "methods": behavior["methods"],
            "legacy": behavior["legacy"],
            "model": m["name"],
            "table": m.get("relation_name", ""),
            "description": _truncate(m["description"], 300),
            "columns": columns,
            "filters": [
                {**p, "desc": _truncate(p["desc"], 120)}
                for p in behavior["parameters"]
            ],
            "allow_unfiltered": behavior["allow_unfiltered"],
            "require_any_of": behavior["require_any_of"],
            "pagination": behavior["pagination"],
            "sort": behavior["sort"],
            "sortable_fields": behavior["sortable_fields"],
            "doc": f"catalog/{category}/#{resource.lower()}",
            "_sort_key": (category, resource.lower(), gran_rank, granularity, path),
        })

    endpoints.sort(key=lambda e: e["_sort_key"])
    for ep in endpoints:
        del ep["_sort_key"]

    categories = []
    by_cat: dict[str, list[dict]] = defaultdict(list)
    for ep in endpoints:
        by_cat[ep["category"]].append(ep)
    for cat in sorted(by_cat):
        eps = by_cat[cat]
        categories.append({
            "id": cat,
            "endpoints": len(eps),
            "resources": len({e["resource"] for e in eps}),
        })

    for w in warnings:
        print(f"  WARNING: {w}")
    space_paths = [e["path"] for e in endpoints if " " in e["path"]]
    if space_paths:
        print(f"  WARNING: {len(space_paths)} paths contain spaces: {space_paths[:5]}")

    path_models: dict[str, list[str]] = defaultdict(list)
    for ep in endpoints:
        path_models[ep["path"]].append(ep["model"])
    dup_paths = {p: ms for p, ms in path_models.items() if len(ms) > 1}
    if dup_paths:
        print(f"  WARNING: {len(dup_paths)} paths are claimed by multiple models "
              "(only one serves in production — fix the api:/granularity tags upstream):")
        for p, ms in sorted(dup_paths.items()):
            print(f"    {p}: {', '.join(ms)}")

    return {
        "base_url": API_BASE_URL,
        "categories": categories,
        "endpoints": endpoints,
        "skipped_by_category": dict(skipped_by_category),
    }


def _curl_example(ep: dict) -> str:
    """Build a copy-pasteable curl example (same rules as api-catalog.js)."""
    base = API_BASE_URL + ep["path"]
    filters = ep["filters"]
    sample = next((f for f in filters if f["type"] == "date"), filters[0] if filters else None)

    def placeholder(f):
        return {"date": "2026-01-01", "string_list": "VALUE1,VALUE2"}.get(f["type"], "VALUE")

    auth = '' if ep["tier"] == "tier0" else ' \\\n  -H "X-API-Key: YOUR_API_KEY"'
    if "GET" not in ep["methods"]:
        body = "{}" if not sample else json.dumps({sample["name"]: placeholder(sample)})
        return (f'curl -X POST "{base}"{auth} \\\n'
                f'  -H "Content-Type: application/json" \\\n  -d \'{body}\'')
    query = "" if not sample else f'?{sample["name"]}={placeholder(sample)}'
    return f'curl "{base}{query}"{auth}'


def _endpoint_detail_block(ep: dict) -> list[str]:
    """Collapsible per-endpoint details (content indented 4 spaces for ???)."""
    inner: list[str] = []
    if ep["description"] and ep["description"] != "--":
        inner += [ep["description"], ""]
    inner += [f"Model: `{ep['model']}` — table `{ep['table']}`", ""]

    if ep["legacy"]:
        inner += ["**Legacy endpoint** — GET only, no query parameters, returns the full table.", ""]
    else:
        if ep["filters"]:
            inner += ["**Declared filters**", "",
                      "| Parameter | Operator | Column | Type | Notes |",
                      "|-----------|----------|--------|------|-------|"]
            for f in ep["filters"]:
                notes = []
                if f["desc"]:
                    notes.append(f["desc"])
                if f.get("case"):
                    notes.append(f"case: {f['case']}")
                if f.get("max_items"):
                    notes.append(f"max_items: {f['max_items']}")
                inner.append(
                    f"| `{f['name']}` | `{f['op']}` | `{f['column']}` "
                    f"| {f['type']} | {_md_cell('; '.join(notes))} |"
                )
            inner.append("")
        policy = ("Unfiltered requests allowed." if ep["allow_unfiltered"]
                  else "At least one filter required.")
        if ep["require_any_of"]:
            policy += " Must provide one of: " + ", ".join(f"`{p}`" for p in ep["require_any_of"]) + "."
        inner += [f"**Filter policy:** {policy}", ""]
        pag = ep["pagination"]
        if pag["enabled"]:
            shape = ("envelope `{items, pagination}`" if pag["response"] == "envelope"
                     else "bare JSON array")
            inner += [f"**Pagination:** `limit`/`offset` — default {pag['default_limit']}, "
                      f"max {pag['max_limit']}; response: {shape}", ""]
        else:
            inner += ["**Pagination:** none (full result set, bare JSON array)", ""]
        if ep["sort"]:
            fixed = ", ".join(f"`{s['column']} {s['dir']}`" for s in ep["sort"])
            inner += [f"**Sort:** {fixed}"
                      + (" — user-sortable via `sort_by`: "
                         + ", ".join(f"`{c}`" for c in ep["sortable_fields"])
                         if ep["sortable_fields"] else ""), ""]
        elif ep["sortable_fields"]:
            inner += ["**Sort:** user-sortable via `sort_by`: "
                      + ", ".join(f"`{c}`" for c in ep["sortable_fields"]), ""]

    if ep["columns"]:
        inner += ["**Columns**", "",
                  "| Column | Type | Description |",
                  "|--------|------|-------------|"]
        for c in ep["columns"]:
            inner.append(f"| `{c['name']}` | `{_md_cell(c['type'])}` | {_md_cell(c['desc'])} |")
        inner.append("")

    inner += ["**Example**", "", "```bash", _curl_example(ep), "```"]

    method_label = "/".join(ep["methods"])
    lines = [f'??? info "`{method_label} {ep["path"]}`"']
    lines += [
        ("    " + line).rstrip()
        for chunk in inner
        for line in chunk.split("\n")
    ]
    return lines


def generate_category_page_content(cat: str, endpoints: list[dict],
                                   skipped: int = 0) -> str:
    """Markdown for one category's marker block."""
    resources: dict[str, list[dict]] = defaultdict(list)
    for ep in endpoints:
        resources[ep["resource"]].append(ep)

    lines = [
        f"_{len(endpoints)} endpoints across {len(resources)} resources. "
        f"Generated from the dbt manifest — edits inside this block will be overwritten. "
        f"Regenerate with `python scripts/update_docs.py --only api`._",
        "",
    ]
    if skipped:
        lines += [
            f'!!! warning "{skipped} additional model(s) not live"',
            f"    {skipped} more model(s) in this category declare `api:` tags "
            "but their `meta.api` metadata fails validation, so the live API "
            "skips them. See the generator log for the model names; the fix "
            "belongs in the dbt model.",
            "",
        ]
    for resource in sorted(resources, key=str.lower):
        eps = resources[resource]
        lines += [f"## {resource}", ""]
        desc = next((e["description"] for e in eps if e["description"]), "")
        if desc:
            lines += [desc, ""]
        lines += ["| Path | Methods | Tier | Filters | Pagination | Sort |",
                  "|------|---------|------|---------|------------|------|"]
        for ep in eps:
            filt = ", ".join(f"`{f['name']}`" for f in ep["filters"]) or "--"
            pag = ep["pagination"]
            pag_cell = (f"limit/offset ({pag['response']})" if pag["enabled"] else "--")
            sort_cell = ", ".join(f"{s['column']} {s['dir']}" for s in ep["sort"]) or "--"
            lines.append(
                f"| `{ep['path']}` | {', '.join(ep['methods'])} | {ep['tier']} "
                f"| {filt} | {pag_cell} | {_md_cell(sort_cell)} |"
            )
        lines.append("")
        for ep in eps:
            lines += _endpoint_detail_block(ep)
            lines.append("")
    return "\n".join(lines).rstrip()


def generate_catalog_index_content(catalog: dict) -> str:
    lines = [
        "| Category | Endpoints | Resources | Public (tier0) | Reference |",
        "|----------|:---------:|:---------:|:--------------:|-----------|",
    ]
    by_cat = {c["id"]: c for c in catalog["categories"]}
    tier0 = defaultdict(int)
    for ep in catalog["endpoints"]:
        if ep["tier"] == "tier0":
            tier0[ep["category"]] += 1
    for cat_id in sorted(by_cat):
        c = by_cat[cat_id]
        display = CATEGORY_DISPLAY.get(cat_id, cat_id.replace("_", " ").title())
        lines.append(
            f"| {display} | {c['endpoints']} | {c['resources']} "
            f"| {tier0.get(cat_id, 0)} | [{cat_id}.md]({cat_id}.md) |"
        )
    total = len(catalog["endpoints"])
    lines.append("")
    lines.append(f"**{total} endpoints** across {len(by_cat)} categories.")
    skipped_total = sum(catalog.get("skipped_by_category", {}).values())
    if skipped_total:
        lines.append("")
        lines.append(
            f"_{skipped_total} additional models declare `api:` tags but fail "
            "`meta.api` validation and are skipped by the live API; they are "
            "excluded here until the dbt models are fixed._"
        )
    return "\n".join(lines)


def generate_endpoints_summary_content(catalog: dict) -> str:
    """Compact category summary for docs/api/endpoints.md (replaces the flat table)."""
    lines = [
        "| Category | Endpoints | Resources | Catalog |",
        "|----------|:---------:|:---------:|---------|",
    ]
    for c in catalog["categories"]:
        display = CATEGORY_DISPLAY.get(c["id"], c["id"].replace("_", " ").title())
        lines.append(
            f"| {display} | {c['endpoints']} | {c['resources']} "
            f"| [catalog/{c['id']}.md](catalog/{c['id']}.md) |"
        )
    lines.append("")
    lines.append(
        f"{len(catalog['endpoints'])} endpoints total. Browse them interactively in the "
        "[Metrics Explorer](explorer.md) or per category in the "
        "[Endpoint Catalog](catalog/index.md)."
    )
    return "\n".join(lines)


def generate_catalog_pages(catalog: dict, dry_run: bool = False) -> int:
    """Write catalog index + per-category pages. Returns changed-file count."""
    changes = 0
    if not dry_run:
        CATALOG_DIR.mkdir(parents=True, exist_ok=True)

    index_path = CATALOG_DIR / "index.md"
    if not index_path.exists() and not dry_run:
        index_path.write_text(
            "# Endpoint Catalog\n\n"
            "Per-category reference for every REST endpoint, generated from the dbt\n"
            "manifest: descriptions, columns, declared filters, pagination and sort\n"
            "contracts, and ready-to-run examples. For free-text search use the\n"
            "[Metrics Explorer](../explorer.md).\n\n"
            f"{MARKER_BEGIN.format('api-catalog-index')}\n"
            f"{MARKER_END.format('api-catalog-index')}\n",
            encoding="utf-8",
        )
        print(f"  Created {index_path.relative_to(DOCS_DIR.parent)}")
        changes += 1
    if update_file(index_path, "api-catalog-index",
                   generate_catalog_index_content(catalog), dry_run):
        changes += 1

    by_cat: dict[str, list[dict]] = defaultdict(list)
    for ep in catalog["endpoints"]:
        by_cat[ep["category"]].append(ep)

    for cat in sorted(by_cat):
        display = CATEGORY_DISPLAY.get(cat, cat.replace("_", " ").title())
        filepath = CATALOG_DIR / f"{cat}.md"
        marker_id = f"api-catalog-{cat}"
        if not filepath.exists():
            template = (
                f"# {display} API Endpoints\n\n"
                f"{MARKER_BEGIN.format(marker_id)}\n"
                f"{MARKER_END.format(marker_id)}\n"
            )
            if dry_run:
                print(f"  [DRY-RUN] Would create catalog page: {filepath.name}")
            else:
                filepath.write_text(template, encoding="utf-8")
                print(f"  Created catalog page: {filepath.name}")
            # Indent is coupled to the nesting depth of "Endpoint Catalog" in
            # mkdocs.yml (tab > section > entry = 6 spaces). Keep in lockstep
            # with the nav layout; the section title must stay unique in the file.
            _add_nav_entry(
                "Endpoint Catalog",
                f"      - {display}: api/catalog/{cat}.md",
                "api/catalog/",
                dry_run,
            )
            changes += 1
        skipped = catalog.get("skipped_by_category", {}).get(cat, 0)
        if update_file(filepath, marker_id,
                       generate_category_page_content(cat, by_cat[cat], skipped),
                       dry_run):
            changes += 1

    # Categories whose every model failed meta.api validation (no live
    # endpoints) — refresh any existing page with an honest empty state
    # instead of leaving stale endpoint listings behind.
    orphan_cats = set(catalog.get("skipped_by_category", {})) - set(by_cat)
    for cat in sorted(orphan_cats):
        filepath = CATALOG_DIR / f"{cat}.md"
        if not filepath.exists():
            continue
        skipped = catalog["skipped_by_category"][cat]
        note = (
            f'!!! warning "No live endpoints"\n'
            f"    All {skipped} model(s) in this category declare `api:` tags, "
            "but their `meta.api` metadata currently fails validation, so the "
            "live API skips every one of them. See the generator log for the "
            "model names; the fix belongs in the dbt models."
        )
        if update_file(filepath, f"api-catalog-{cat}", note, dry_run):
            changes += 1

    return changes


def write_catalog_json(catalog: dict, dry_run: bool = False) -> int:
    """Write the explorer's data file. Returns 1 if changed."""
    payload = {k: v for k, v in catalog.items() if k != "skipped_by_category"}
    data = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
    size_kb = len(data.encode("utf-8")) / 1024
    print(f"  catalog_data.json: {len(catalog['endpoints'])} endpoints, {size_kb:.0f} KB")
    if size_kb > 1024:
        print("  WARNING: catalog_data.json exceeds 1 MB — consider tighter truncation.")

    if CATALOG_JSON.exists() and CATALOG_JSON.read_text(encoding="utf-8") == data:
        return 0
    if dry_run:
        print(f"  [DRY-RUN] Would write {CATALOG_JSON.relative_to(DOCS_DIR.parent)}")
    else:
        CATALOG_JSON.write_text(data, encoding="utf-8")
        print(f"  Wrote {CATALOG_JSON.relative_to(DOCS_DIR.parent)}")
    return 1


def update_api(models: list[dict], dry_run: bool = False) -> int:
    """Update the API endpoint catalog (summary, pages, JSON)."""
    catalog = build_api_catalog(models)
    changes = 0
    if update_file(DOCS_DIR / "api" / "endpoints.md", "api-endpoints",
                   generate_endpoints_summary_content(catalog), dry_run):
        changes += 1
    changes += generate_catalog_pages(catalog, dry_run)
    changes += write_catalog_json(catalog, dry_run)
    return changes


# ---------------------------------------------------------------------------
# Dashboard sector generation
# ---------------------------------------------------------------------------

def load_dashboard_config(dashboard_path: Path) -> dict:
    """Load dashboard.yml and per-sector YAML configs."""
    try:
        import yaml
    except ImportError:
        yaml = None

    main_config = dashboard_path / "public" / "dashboard.yml"
    if not main_config.exists():
        return {}

    if yaml:
        with open(main_config) as f:
            config = yaml.safe_load(f) or {}
    else:
        # Simple YAML-like parser for the flat dashboard.yml structure
        config = _simple_yaml_parse(main_config)

    return config


def _simple_yaml_parse(filepath: Path) -> dict:
    """Minimal parser for dashboard.yml (no nested mappings beyond one level)."""
    result = {}
    current_key = None
    current_block = {}

    with open(filepath) as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            # Top-level key (no leading whitespace)
            if not line[0].isspace() and stripped.endswith(":"):
                if current_key:
                    result[current_key] = current_block
                current_key = stripped[:-1]
                current_block = {}
            elif current_key and ":" in stripped:
                k, v = stripped.split(":", 1)
                current_block[k.strip()] = v.strip().strip('"').strip("'")

    if current_key:
        result[current_key] = current_block
    return result


def load_query_files(queries_path: Path) -> list[dict]:
    """Parse JavaScript query files to extract metric metadata."""
    if not queries_path.exists():
        return []

    queries = []
    for js_file in sorted(queries_path.glob("*.js")):
        content = js_file.read_text(encoding="utf-8")
        meta = _parse_query_js(content, js_file.stem)
        if meta:
            queries.append(meta)
    return queries


def _parse_query_js(content: str, filename: str) -> dict | None:
    """Extract id, name, description, chartType from a query JS file."""
    result = {"filename": filename}

    # Extract fields using regex
    for field in ("id", "name", "description", "metricDescription", "chartType"):
        match = re.search(rf"{field}\s*:\s*['\"]([^'\"]+)['\"]", content)
        if match:
            result[field] = match.group(1)

    if "id" not in result:
        result["id"] = filename

    return result


def generate_dashboard_sectors(dashboard_path: Path) -> str:
    """Generate dashboard sector metrics tables."""
    config = load_dashboard_config(dashboard_path)
    queries = load_query_files(dashboard_path / "src" / "queries")

    if not config and not queries:
        return "*Dashboard data not available. Set --dashboard-path to the metrics-dashboard repo root.*\n"

    # Map query IDs to their metadata
    query_map = {q["id"]: q for q in queries}

    # Load per-sector YAML to get metric IDs
    sectors = []
    for sector_key, sector_info in sorted(
        config.items(), key=lambda x: int(x[1].get("order", 99))
    ):
        if not isinstance(sector_info, dict):
            continue
        name = sector_info.get("name", sector_key)
        source = sector_info.get("source", "")
        sectors.append({
            "key": sector_key,
            "name": name,
            "order": int(sector_info.get("order", 99)),
            "source": source,
        })

    lines = []
    for sector in sectors:
        lines.append(f"### {sector['name']}\n")

        # Try to load sector YAML for metric IDs
        source_file = sector.get("source", "")
        if source_file:
            sector_yaml_path = dashboard_path / "public" / source_file.lstrip("/")
            metric_ids = _load_sector_metric_ids(sector_yaml_path)
        else:
            metric_ids = []

        # Match sector queries by prefix or explicit metric IDs
        sector_queries = []
        prefix = sector["name"].lower().replace(" ", "_")
        alt_prefix = sector["key"].lower().replace(" ", "_")

        for q in queries:
            qid = q.get("id", "")
            if qid in metric_ids:
                sector_queries.append(q)
            elif qid.startswith(prefix) or qid.startswith(alt_prefix):
                if qid not in [sq["id"] for sq in sector_queries]:
                    sector_queries.append(q)

        if sector_queries:
            lines.append("| Metric | Chart Type | Description |")
            lines.append("|--------|-----------|-------------|")
            for q in sorted(sector_queries, key=lambda x: x.get("id", "")):
                chart_type = q.get("chartType", "--")
                desc = q.get("metricDescription", q.get("description", "--"))
                if len(desc) > 100:
                    desc = desc[:97] + "..."
                lines.append(f"| `{q['id']}` | {chart_type} | {desc} |")
        else:
            lines.append(f"*No query files found for {sector['name']}.*")

        lines.append("")

    return "\n".join(lines)


def _load_sector_metric_ids(filepath: Path) -> list[str]:
    """Extract metric IDs from a sector YAML file."""
    if not filepath.exists():
        return []

    ids = []
    content = filepath.read_text(encoding="utf-8")
    for match in re.finditer(r"id:\s*(\S+)", content):
        ids.append(match.group(1))
    return ids


def update_dashboard(dashboard_path: Path, dry_run: bool = False) -> int:
    """Update dashboard sectors page. Returns count of files changed."""
    content = generate_dashboard_sectors(dashboard_path)
    filepath = DOCS_DIR / "dashboard" / "sectors.md"
    if update_file(filepath, "dashboard-sectors", content, dry_run):
        return 1
    return 0


# ---------------------------------------------------------------------------
# Nav management
# ---------------------------------------------------------------------------

def _add_nav_entry(section_match: str, entry_line: str, path_fragment: str,
                   dry_run: bool = False) -> None:
    """Insert entry_line after the last nav line containing path_fragment
    inside the section whose header line contains section_match."""
    if not MKDOCS_YML.exists():
        return

    content = MKDOCS_YML.read_text(encoding="utf-8")

    # Already present? (match on the doc path portion of the entry)
    doc_path = entry_line.split(":")[-1].strip()
    if doc_path and doc_path in content:
        return

    lines = content.split("\n")
    insert_idx = None
    in_section = False

    for i, line in enumerate(lines):
        if section_match in line:
            in_section = True
        elif in_section:
            if line.strip().startswith("- ") and path_fragment in line:
                insert_idx = i + 1
            elif line.strip().startswith("- ") and path_fragment not in line:
                # Left the section
                break

    if insert_idx is not None:
        lines.insert(insert_idx, entry_line)
        if dry_run:
            print(f"  [DRY-RUN] Would add '{doc_path}' to mkdocs.yml nav")
        else:
            MKDOCS_YML.write_text("\n".join(lines), encoding="utf-8")
            print(f"  Added '{doc_path}' to mkdocs.yml nav")
    else:
        print(f"  WARNING: nav section '{section_match}' not found; "
              f"add '{doc_path}' to mkdocs.yml manually.")


def _add_to_nav(slug: str, display_name: str, dry_run: bool = False) -> None:
    """Add a new module page to mkdocs.yml nav under 'dbt Model Catalog'."""
    # Indent is coupled to the nesting depth of "dbt Model Catalog" in
    # mkdocs.yml (tab > section > entry = 6 spaces). Keep in lockstep with
    # the nav layout; the section title must stay unique in the file.
    _add_nav_entry(
        "dbt Model Catalog",
        f"      - {display_name}: models/{slug}.md",
        "models/",
        dry_run,
    )


# ---------------------------------------------------------------------------
# Semantic graph freshness
# ---------------------------------------------------------------------------

def _fetch_json(url: str):
    if not requests:
        print("ERROR: 'requests' package required for URL fetch. pip install requests")
        return None
    print(f"Fetching {url} ...")
    try:
        resp = requests.get(url, timeout=120)
        resp.raise_for_status()
    except Exception as exc:
        print(f"  WARNING: fetch failed ({exc}); skipping.")
        return None
    return resp.json()


def _quality_tier(entry: dict) -> str:
    if not isinstance(entry, dict):
        return ""
    tier = entry.get("quality_tier")
    if not tier:
        tier = (
            entry.get("config", {}).get("meta", {}).get("cerebro", {}).get("quality_tier")
            if isinstance(entry.get("config"), dict) else ""
        )
    return tier or ""


def update_graph(dry_run: bool = False) -> int:
    """Refresh the interactive semantic graph data + coverage numbers from gh-pages."""
    changes = 0

    graph_data = _fetch_json(GRAPH_DATA_URL)
    if graph_data is not None:
        data = json.dumps(graph_data, separators=(",", ":"), ensure_ascii=False)
        current = GRAPH_DATA_FILE.read_text(encoding="utf-8") if GRAPH_DATA_FILE.exists() else ""
        if current != data:
            if dry_run:
                print(f"  [DRY-RUN] Would update {GRAPH_DATA_FILE.relative_to(DOCS_DIR.parent)}")
            else:
                GRAPH_DATA_FILE.write_text(data, encoding="utf-8")
                print(f"  Updated {GRAPH_DATA_FILE.relative_to(DOCS_DIR.parent)}")
            changes += 1

    registry = _fetch_json(SEMANTIC_REGISTRY_URL)
    if registry is not None:
        # Mirrors the "Coverage at a glance" block emitted by dbt-cerebro's
        # scripts/semantic/generate_graph_diagram.py so CI keeps the numbers
        # fresh between manual full-page regenerations.
        metrics = registry.get("metrics", {}) or {}
        rels = registry.get("relationships", []) or []
        if isinstance(rels, dict):
            rels = list(rels.values())
        approved = sum(1 for m in metrics.values() if _quality_tier(m) == "approved")
        axes = {r.get("via_entity") or "(unspecified)" for r in rels}
        axes.discard("(unspecified)")
        spine_axes = {"day", "week", "month"}
        pseudo_nodes = {
            m
            for r in rels
            if r.get("via_entity") == "user_pseudonym"
            for m in (r.get("left_model"), r.get("right_model"))
            if m
        }
        spine_count = sum(1 for r in rels if r.get("via_entity") in spine_axes)

        coverage = (
            f"- **Approved metrics**: {approved} / {len(metrics)} total\n"
            f"- **Cross-sector relationships**: {len(rels)} total across "
            f"{len(axes)} axes\n"
            f"- **User-pseudonym graph nodes**: {len(pseudo_nodes)}\n"
            f"- **Time-spine bridges**: {spine_count} relationships joining "
            f"sector marts to `dim_time_spine_*`"
        )
        if update_file(GRAPH_PAGE, "semantic-graph-coverage", coverage, dry_run):
            changes += 1

    return changes


# ---------------------------------------------------------------------------
# MCP tool reference generation (reads the sibling cerebro-mcp repo)
# ---------------------------------------------------------------------------

MCP_TOOLS_PAGE_ORDER = [
    ("analytics", "mcp-tools-analytics"),
    ("semantic", "mcp-tools-semantic"),
    ("visualization", "mcp-tools-visualization"),
    ("web3", "mcp-tools-web3"),
    ("governance", "mcp-tools-governance"),
    ("research", "mcp-tools-research"),
    ("storyteller", "mcp-tools-storyteller"),
    ("workflow", "mcp-tools-workflow"),
]

MCP_MODULE_TITLES = {
    "query": "Query execution",
    "query_async": "Async queries",
    "schema": "Schema & sampling",
    "dbt": "Model discovery & lineage",
    "lineage_graph": "Lineage graphs",
    "model_lineage_app": "Model Lineage mini-app",
    "metadata": "Metadata & reference",
    "saved_queries": "Saved queries",
    "sandbox": "Simulation sandboxes",
    "custom_queries": "Custom query tools",
    "list_unifier": "Unified listing",
    "semantic": "Governed metrics",
    "find": "Discovery router",
    "data_catalog": "Data Catalog",
    "graph_explorer": "Graph Explorer",
    "charts": "Charts & reports",
    "metric_lab": "Metric Lab mini-app",
    "portfolio": "Portfolio mini-app",
    "mini_apps": "Mini-app infrastructure",
    "dashboard_builder": "Dashboard builder",
    "grafana": "Grafana publishing",
    "web_apps": "Web app delivery",
    "rpc": "Contract inspection",
    "rpc_scan": "Bulk RPC scans",
    "contract_explorer": "Contract Explorer mini-app",
    "cross_check": "Verification",
    "reasoning": "Reasoning & tracing",
    "agents": "Agent personas",
    "research": "Research workflow",
    "storyteller": "Storyteller workflow",
    "resume": "Workflow resume",
}


def _mcp_tool_table(tools: list[dict]) -> list[str]:
    lines = [
        "| Tool | Summary | Tier | Risk | Gate |",
        "|------|---------|------|------|------|",
    ]
    for t in tools:
        gate = f"`{t['gate']}`" if t.get("gate") else "--"
        lines.append(
            f"| `{t['name']}` | {_md_cell(t['summary'])} | {t['tier']} "
            f"| {t['risk']} | {gate} |"
        )
    return lines


def generate_mcp_package_content(package: str, tools: list[dict]) -> str:
    by_module: dict[str, list[dict]] = defaultdict(list)
    for t in tools:
        by_module[t["module"]].append(t)

    lines: list[str] = []
    app_only: list[dict] = []
    for module in sorted(by_module):
        module_tools = by_module[module]
        visible = [t for t in module_tools if t["risk"] != "app_only"]
        app_only += [t for t in module_tools if t["risk"] == "app_only"]
        if not visible:
            continue
        title = MCP_MODULE_TITLES.get(module, module.replace("_", " ").title())
        lines += [f"**{title}** (`{module}.py`)", ""]
        lines += _mcp_tool_table(visible)
        lines.append("")

    if app_only:
        lines += [
            "<details>",
            f"<summary>App-internal tools ({len(app_only)}) — called by mini-app "
            "UIs, not meant for direct use</summary>",
            "",
        ]
        lines += _mcp_tool_table(app_only)
        lines += ["", "</details>", ""]
    return "\n".join(lines).rstrip()


def generate_mcp_summary_content(info: dict) -> str:
    tools = info["tools"]
    by_pkg: dict[str, list[dict]] = defaultdict(list)
    for t in tools:
        by_pkg[t["package"]].append(t)

    lines = [
        f"**{len(tools)} static tools** across {len(by_pkg)} packages, plus "
        f"**{len(info['custom_tools'])} dynamic SQL-templated tools** from "
        "`custom_tools.yaml`.",
        "",
        "| Package | Tools | Core | Advanced |",
        "|---------|:-----:|:----:|:--------:|",
    ]
    for pkg in sorted(by_pkg):
        pkg_tools = by_pkg[pkg]
        core = sum(1 for t in pkg_tools if t["core"])
        lines.append(f"| {pkg} | {len(pkg_tools)} | {core} | {len(pkg_tools) - core} |")

    risk_counts: dict[str, int] = defaultdict(int)
    for t in tools:
        risk_counts[t["risk"]] += 1
    lines += ["", "| Risk class | Tools |", "|------------|:-----:|"]
    for risk in sorted(risk_counts):
        lines.append(f"| {risk} | {risk_counts[risk]} |")

    gate_counts: dict[str, int] = defaultdict(int)
    for t in tools:
        if t.get("gate"):
            gate_counts[t["gate"]] += 1
    if gate_counts:
        lines += ["", "| Feature flag | Tools gated |", "|--------------|:-----------:|"]
        for gate in sorted(gate_counts):
            lines.append(f"| `{gate}` | {gate_counts[gate]} |")

    return "\n".join(lines)


def generate_mcp_custom_content(info: dict) -> str:
    lines = [
        "| Tool | Summary | Parameters | Database |",
        "|------|---------|------------|----------|",
    ]
    for t in info["custom_tools"]:
        params = ", ".join(f"`{p}`" for p in t.get("params", [])) or "--"
        lines.append(
            f"| `{t['name']}` | {_md_cell(t.get('summary', ''))} | {params} "
            f"| {t.get('database') or '--'} |"
        )
    return "\n".join(lines)


def generate_mcp_at_a_glance(info: dict) -> str:
    tools = info["tools"]
    gates = sorted({t["gate"] for t in tools if t.get("gate")})
    return "\n".join([
        "| Surface | Count |",
        "|---------|:-----:|",
        f"| Static MCP tools | {len(tools)} |",
        f"| Dynamic YAML tools | {len(info['custom_tools'])} |",
        f"| Core (lean) tool surface | {len(info['core_tool_names'])} |",
        f"| Agent personas | {len(info['personas'])} |",
        f"| Interactive mini-app surfaces | {len(info.get('ui_surfaces', [])) or '--'} |",
        f"| Feature-gated families | {', '.join(f'`{g}`' for g in gates)} |",
    ])


def generate_mcp_personas_content(info: dict) -> str:
    lines = [
        f"{len(info['personas'])} personas are registered "
        "(`get_agent_persona` accepts these roles):",
        "",
        "| Role | Focus |",
        "|------|-------|",
    ]
    for p in info["personas"]:
        lines.append(f"| `{p['role']}` | {_md_cell(p.get('summary', ''))} |")
    return "\n".join(lines)


def update_mcp(mcp_repo: Path, dry_run: bool = False) -> int:
    """Regenerate the MCP tool reference from the sibling cerebro-mcp repo.

    Requires a local checkout (not available in CI — committed output is the
    CI deliverable). Regenerate with:
        python scripts/update_docs.py --only mcp
    """
    try:
        from mcp_introspect import introspect
    except ImportError as exc:
        print(f"  WARNING: cannot import mcp_introspect ({exc}); skipping MCP updates.")
        return 0

    info = introspect(mcp_repo)
    tools = info["tools"]
    print(f"  Introspected {len(tools)} static tools, "
          f"{len(info['custom_tools'])} custom tools, "
          f"{len(info['personas'])} personas.")
    for warning in info.get("warnings", []):
        print(f"  WARNING: {warning}")

    changes = 0
    tools_page = DOCS_DIR / "mcp" / "tools.md"
    if update_file(tools_page, "mcp-tools-summary",
                   generate_mcp_summary_content(info), dry_run):
        changes += 1

    by_pkg: dict[str, list[dict]] = defaultdict(list)
    for t in tools:
        by_pkg[t["package"]].append(t)
    for package, marker_id in MCP_TOOLS_PAGE_ORDER:
        content = generate_mcp_package_content(package, by_pkg.get(package, []))
        if update_file(tools_page, marker_id, content, dry_run):
            changes += 1
    unknown_pkgs = set(by_pkg) - {p for p, _ in MCP_TOOLS_PAGE_ORDER}
    if unknown_pkgs:
        print(f"  WARNING: packages without a tools.md section: {sorted(unknown_pkgs)}")

    if update_file(tools_page, "mcp-tools-custom",
                   generate_mcp_custom_content(info), dry_run):
        changes += 1
    if update_file(DOCS_DIR / "mcp" / "index.md", "mcp-at-a-glance",
                   generate_mcp_at_a_glance(info), dry_run):
        changes += 1
    if update_file(DOCS_DIR / "mcp" / "agents.md", "mcp-personas",
                   generate_mcp_personas_content(info), dry_run):
        changes += 1
    return changes


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Update documentation from dbt manifest and dashboard config."
    )
    parser.add_argument(
        "--manifest", "-m",
        default=MANIFEST_URL,
        help="Path or URL to dbt manifest.json (default: GitHub Pages URL)",
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Show what would change without writing files",
    )
    parser.add_argument(
        "--only",
        choices=["models", "api", "dashboard", "mcp", "graph"],
        help="Update only a specific section",
    )
    parser.add_argument(
        "--dashboard-path",
        default=str(Path(__file__).resolve().parent.parent.parent / "metrics-dashboard"),
        help="Path to the metrics-dashboard repo root",
    )
    parser.add_argument(
        "--mcp-repo",
        default=str(Path(__file__).resolve().parent.parent.parent / "cerebro-mcp"),
        help="Path to the cerebro-mcp repo root (sibling checkout)",
    )
    args = parser.parse_args()

    if args.dry_run:
        print("=== DRY RUN MODE ===\n")

    total_changes = 0

    # Load manifest for models and API
    if args.only in (None, "models", "api"):
        manifest = load_manifest(args.manifest)
        models = extract_models(manifest)
        print(f"Loaded {len(models)} models from manifest.\n")
    else:
        models = []

    # Update models
    if args.only in (None, "models"):
        print("--- Updating model catalog pages ---")
        changes = update_models(models, args.dry_run)
        print(f"  {changes} file(s) {'would be ' if args.dry_run else ''}changed.\n")
        total_changes += changes

    # Update API endpoints
    if args.only in (None, "api"):
        print("--- Updating API endpoint catalog ---")
        changes = update_api(models, args.dry_run)
        print(f"  {changes} file(s) {'would be ' if args.dry_run else ''}changed.\n")
        total_changes += changes

    # Update dashboard
    if args.only in (None, "dashboard"):
        print("--- Updating dashboard sectors ---")
        dashboard_path = Path(args.dashboard_path)
        if dashboard_path.exists():
            changes = update_dashboard(dashboard_path, args.dry_run)
            print(f"  {changes} file(s) {'would be ' if args.dry_run else ''}changed.\n")
            total_changes += changes
        else:
            print(f"  WARNING: Dashboard path not found: {dashboard_path}")
            print("  Skipping dashboard updates. Use --dashboard-path to specify.\n")

    # Update MCP tool reference (requires local cerebro-mcp checkout; skipped in CI)
    if args.only in (None, "mcp"):
        print("--- Updating MCP tool reference ---")
        mcp_repo = Path(args.mcp_repo)
        if mcp_repo.exists():
            changes = update_mcp(mcp_repo, args.dry_run)
            print(f"  {changes} file(s) {'would be ' if args.dry_run else ''}changed.\n")
            total_changes += changes
        else:
            print(f"  WARNING: cerebro-mcp path not found: {mcp_repo}")
            print("  Skipping MCP updates. Use --mcp-repo to specify.\n")

    # Update semantic graph data + coverage (URL fetch; runs in CI)
    if args.only in (None, "graph"):
        print("--- Updating semantic graph data ---")
        changes = update_graph(args.dry_run)
        print(f"  {changes} file(s) {'would be ' if args.dry_run else ''}changed.\n")
        total_changes += changes

    # Summary
    if args.dry_run:
        print(f"=== DRY RUN COMPLETE: {total_changes} file(s) would change ===")
    else:
        print(f"=== DONE: {total_changes} file(s) updated ===")

    return 0 if total_changes >= 0 else 1


if __name__ == "__main__":
    sys.exit(main())
