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
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MANIFEST_URL = "https://gnosischain.github.io/dbt-cerebro/manifest.json"
DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
MKDOCS_YML = Path(__file__).resolve().parent.parent / "mkdocs.yml"

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
        meta_api = node.get("config", {}).get("meta", {}).get("api", {})
        models.append({
            "name": name,
            "tags": tags,
            "description": description,
            "columns": columns,
            "meta_api": meta_api,
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

def replace_marker_content(text: str, marker_id: str, new_content: str) -> str:
    """Replace content between BEGIN/END markers. Return updated text."""
    begin = MARKER_BEGIN.format(marker_id)
    end = MARKER_END.format(marker_id)
    pattern = re.compile(
        re.escape(begin) + r"\n.*?" + re.escape(end),
        re.DOTALL,
    )
    replacement = f"{begin}\n{new_content}\n{end}"
    if pattern.search(text):
        return pattern.sub(replacement, text)
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
# API endpoint generation
# ---------------------------------------------------------------------------

def generate_endpoint_table(models: list[dict]) -> str:
    """Generate the API endpoint catalog table."""
    endpoints = []
    for m in models:
        tags = m["tags"]
        if "production" not in tags:
            continue
        # Must have an api:* tag
        api_resource = None
        for tag in tags:
            if tag.startswith("api:"):
                api_resource = tag[4:]
                break
        if not api_resource:
            continue

        category = get_module(tags) or "unknown"

        # Granularity from tag
        granularity = ""
        for tag in tags:
            if tag.startswith("granularity:"):
                granularity = tag[12:]
                break

        # Tier
        tier = "tier0"
        for tag in tags:
            if tag in TIER_TAGS:
                tier = tag
                break

        # Methods
        meta_api = m.get("meta_api", {})
        methods = meta_api.get("methods", ["GET"])
        if isinstance(methods, list):
            methods_str = ", ".join(methods)
        else:
            methods_str = "GET"

        # Build path
        path = f"/v1/{category}/{api_resource}"
        if granularity:
            path += f"/{granularity}"

        desc = m["description"] or "--"
        if len(desc) > 100:
            desc = desc[:97] + "..."

        # Sort key: category, resource, granularity order
        gran_order = (
            GRANULARITY_ORDER.index(granularity)
            if granularity in GRANULARITY_ORDER
            else 99
        )
        endpoints.append({
            "path": path,
            "methods": methods_str,
            "tier": tier,
            "description": desc,
            "sort_key": (category, api_resource, gran_order),
        })

    endpoints.sort(key=lambda e: e["sort_key"])

    lines = [
        "| Path | Methods | Tier | Description |",
        "|------|---------|------|-------------|",
    ]
    for ep in endpoints:
        lines.append(
            f"| `{ep['path']}` | {ep['methods']} | {ep['tier']} | {ep['description']} |"
        )

    return "\n".join(lines)


def update_api(models: list[dict], dry_run: bool = False) -> int:
    """Update the API endpoints page. Returns count of files changed."""
    table = generate_endpoint_table(models)
    filepath = DOCS_DIR / "api" / "endpoints.md"
    if update_file(filepath, "api-endpoints", table, dry_run):
        return 1
    return 0


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

def _add_to_nav(slug: str, display_name: str, dry_run: bool = False) -> None:
    """Add a new module page to mkdocs.yml nav under 'dbt Model Catalog'."""
    if not MKDOCS_YML.exists():
        return

    content = MKDOCS_YML.read_text(encoding="utf-8")
    entry = f"    - {display_name}: models/{slug}.md"

    # Check if already present
    if f"models/{slug}.md" in content:
        return

    # Find the "dbt Model Catalog" section and insert before the last entry
    # Look for the pattern of model entries
    lines = content.split("\n")
    insert_idx = None
    in_catalog = False

    for i, line in enumerate(lines):
        if "dbt Model Catalog" in line:
            in_catalog = True
        elif in_catalog:
            if line.strip().startswith("- ") and "models/" in line:
                insert_idx = i + 1
            elif line.strip().startswith("- ") and "models/" not in line:
                # Left the catalog section
                break

    if insert_idx is not None:
        lines.insert(insert_idx, entry)
        new_content = "\n".join(lines)
        if dry_run:
            print(f"  [DRY-RUN] Would add '{display_name}' to mkdocs.yml nav")
        else:
            MKDOCS_YML.write_text(new_content, encoding="utf-8")
            print(f"  Added '{display_name}' to mkdocs.yml nav")


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
        choices=["models", "api", "dashboard"],
        help="Update only a specific section",
    )
    parser.add_argument(
        "--dashboard-path",
        default=str(Path(__file__).resolve().parent.parent.parent / "metrics-dashboard"),
        help="Path to the metrics-dashboard repo root",
    )
    args = parser.parse_args()

    if args.dry_run:
        print("=== DRY RUN MODE ===\n")

    total_changes = 0

    # Load manifest for models and API
    if args.only != "dashboard":
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

    # Summary
    if args.dry_run:
        print(f"=== DRY RUN COMPLETE: {total_changes} file(s) would change ===")
    else:
        print(f"=== DONE: {total_changes} file(s) updated ===")

    return 0 if total_changes >= 0 else 1


if __name__ == "__main__":
    sys.exit(main())
