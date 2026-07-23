#!/usr/bin/env python3
"""
Pure-AST introspection of the cerebro-mcp tool surface.

Extracts the MCP tool inventory (static tools, tier/domain metadata, risk
classes, feature gates, custom YAML tools, agent personas) from the sibling
cerebro-mcp repository WITHOUT importing it — cerebro_mcp's runtime
dependencies are not installed in docs CI, so everything here is done with
`ast` parsing plus a soft yaml import for custom_tools.yaml.

Usage:
    python scripts/mcp_introspect.py                     # sibling ../cerebro-mcp
    python scripts/mcp_introspect.py /path/to/cerebro-mcp
"""

import ast
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TOOLS_SUBDIR = Path("src") / "cerebro_mcp" / "tools"
TOOL_META_FILE = TOOLS_SUBDIR / "tool_meta.py"
SECURITY_FILE = Path("src") / "cerebro_mcp" / "security.py"
SERVER_FILE = Path("src") / "cerebro_mcp" / "server.py"
CONFIG_FILE = Path("src") / "cerebro_mcp" / "config.py"
AGENTS_FILE = TOOLS_SUBDIR / "governance" / "agents.py"
PROMPTS_AGENTS_DIRS = [
    Path("src") / "cerebro_mcp" / "prompts" / "agents",
    Path("prompts") / "agents",
]
CUSTOM_TOOLS_YAML = "custom_tools.yaml"

# Highest-severity-first order used to reduce a tool's risk-class set to one
# primary class (mirrors _RISK_PRIORITY in cerebro_mcp/security.py).
RISK_SEVERITY = [
    "SUBPROCESS",
    "EXTERNAL_WRITE",
    "WORKSPACE_WRITE",
    "APP_ONLY",
    "SERVER_STATE_WRITE",
    "READ_ONLY",
]

# Feature gates that live INSIDE the registrar function (early `return` on a
# settings flag) rather than around the register_* call in server.py, so the
# server.py If-scan cannot see them. Hand-maintained; validated against
# config.py at extraction time.
#
# Confirmed in source:
#   tools/visualization/grafana.py      register_grafana_tools:
#       `if not settings.GRAFANA_TOOLS_ENABLED: return`
#   tools/analytics/custom_queries.py   register_custom_query_tools:
#       `if not settings.CUSTOM_TOOLS_ENABLED or not settings.CUSTOM_TOOLS_PATH: return`
#   tools/semantic/semantic.py          register_semantic_tools:
#       `if not settings.SEMANTIC_ENABLED: return`
#   tools/semantic/find.py              register_find_tool:
#       `if not settings.SEMANTIC_ENABLED: return`
#   tools/visualization/dashboard_builder.py  register_dashboard_tools:
#       `if not settings.DASHBOARD_BUILDER_ENABLED: return`
#   tools/visualization/mini_apps.py    register_load_tools_tool:
#       `load_tools` is always registered, but it is only meaningful when
#       LEAN_CORE_ENABLED is on (the flag drives the lean-core visibility
#       filter that `load_tools` un-hides tools from), so it is documented
#       under that flag.
INTERNALLY_GATED: dict[str, str] = {
    "register_grafana_tools": "GRAFANA_TOOLS_ENABLED",
    "register_custom_query_tools": "CUSTOM_TOOLS_ENABLED",
    "register_load_tools_tool": "LEAN_CORE_ENABLED",
    "register_semantic_tools": "SEMANTIC_ENABLED",
    "register_find_tool": "SEMANTIC_ENABLED",
    "register_dashboard_tools": "DASHBOARD_BUILDER_ENABLED",
}

# Warnings collected by the extractors, drained by introspect().
WARNINGS: list[str] = []


def _warn(message: str) -> None:
    """Record a warning and print it."""
    WARNINGS.append(message)
    print(f"WARNING: {message}")


# ---------------------------------------------------------------------------
# Static tool extraction
# ---------------------------------------------------------------------------

class _ToolVisitor(ast.NodeVisitor):
    """Collect @*.tool-decorated functions, tracking the enclosing-function stack."""

    def __init__(self, rel_path: Path):
        self.rel_path = rel_path          # path relative to tools/ dir
        self.func_stack: list[str] = []
        self.tools: list[dict] = []

    def _tool_decorator(self, dec: ast.expr) -> ast.expr | None:
        """Return the decorator node if it is `<recv>.tool` or `<recv>.tool(...)`."""
        if isinstance(dec, ast.Attribute) and dec.attr == "tool":
            return dec
        if (
            isinstance(dec, ast.Call)
            and isinstance(dec.func, ast.Attribute)
            and dec.func.attr == "tool"
        ):
            return dec
        return None

    def _handle_function(self, node) -> None:
        for dec in node.decorator_list:
            match = self._tool_decorator(dec)
            if match is None:
                continue
            if isinstance(match, ast.Call):
                for kw in match.keywords:
                    if kw.arg == "name":
                        raise SystemExit(
                            f"ERROR: {self.rel_path}:{node.lineno}: @tool decorator on "
                            f"'{node.name}' uses a name= override. mcp_introspect.py "
                            "assumes tool names equal function names; a rename would "
                            "silently corrupt the generated docs. Remove the override "
                            "or teach scripts/mcp_introspect.py about it."
                        )
            docstring = ast.get_docstring(node) or ""
            summary = docstring.strip().splitlines()[0].strip() if docstring.strip() else ""
            parts = self.rel_path.parts
            package = parts[0] if len(parts) > 1 else "(root)"
            self.tools.append({
                "name": node.name,
                "summary": summary,
                "package": package,
                "module": self.rel_path.stem,
                "registrar": self.func_stack[-1] if self.func_stack else "",
            })
            break

        self.func_stack.append(node.name)
        self.generic_visit(node)
        self.func_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._handle_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._handle_function(node)


def extract_static_tools(mcp_repo: Path) -> list[dict]:
    """Walk src/cerebro_mcp/tools/**/*.py and collect @mcp.tool-decorated functions."""
    tools_dir = mcp_repo / TOOLS_SUBDIR
    if not tools_dir.is_dir():
        _warn(f"tools directory not found: {tools_dir}")
        return []

    tools: list[dict] = []
    for py_file in sorted(tools_dir.rglob("*.py")):
        if "__pycache__" in py_file.parts:
            continue
        rel_path = py_file.relative_to(tools_dir)
        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"))
        except SyntaxError as exc:
            _warn(f"could not parse {py_file}: {exc}")
            continue
        visitor = _ToolVisitor(rel_path)
        visitor.visit(tree)
        tools.extend(visitor.tools)

    missing = [t["name"] for t in tools if not t["summary"]]
    if missing:
        _warn(f"{len(missing)} tool(s) missing docstrings: {', '.join(sorted(missing))}")
    return tools


# ---------------------------------------------------------------------------
# tool_meta.py — TOOL_META + CORE_TOOL_NAMES
# ---------------------------------------------------------------------------

def _assign_targets(node: ast.stmt) -> list[str]:
    """Return target names of an Assign/AnnAssign statement."""
    if isinstance(node, ast.Assign):
        return [t.id for t in node.targets if isinstance(t, ast.Name)]
    if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
        return [node.target.id]
    return []


def extract_tool_meta(mcp_repo: Path) -> tuple[dict, frozenset]:
    """Parse tools/tool_meta.py for TOOL_META and CORE_TOOL_NAMES (pure literals)."""
    meta_file = mcp_repo / TOOL_META_FILE
    if not meta_file.is_file():
        _warn(f"tool_meta.py not found: {meta_file}")
        return {}, frozenset()

    tree = ast.parse(meta_file.read_text(encoding="utf-8"))
    tool_meta: dict = {}
    core_names: frozenset = frozenset()

    for node in tree.body:
        targets = _assign_targets(node)
        value = getattr(node, "value", None)
        if value is None:
            continue
        if "TOOL_META" in targets:
            try:
                tool_meta = ast.literal_eval(value)
            except ValueError as exc:
                _warn(f"TOOL_META is not a pure literal dict: {exc}")
        elif "CORE_TOOL_NAMES" in targets:
            # Assigned as `frozenset({...})`; literal_eval the inner Set node.
            if (
                isinstance(value, ast.Call)
                and isinstance(value.func, ast.Name)
                and value.func.id == "frozenset"
                and value.args
            ):
                core_names = frozenset(ast.literal_eval(value.args[0]))
            else:
                try:
                    core_names = frozenset(ast.literal_eval(value))
                except ValueError as exc:
                    _warn(f"CORE_TOOL_NAMES has unexpected shape: {exc}")

    if not tool_meta:
        _warn("TOOL_META extraction produced an empty dict")
    if not core_names:
        _warn("CORE_TOOL_NAMES extraction produced an empty set")
    return tool_meta, core_names


# ---------------------------------------------------------------------------
# security.py — TOOL_RISK_REGISTRY reduced to one primary class per tool
# ---------------------------------------------------------------------------

def _riskclass_attrs_from_frozenset_call(value: ast.expr) -> set[str] | None:
    """Return RiskClass attr names from a `frozenset({RiskClass.X, ...})` call."""
    if not (
        isinstance(value, ast.Call)
        and isinstance(value.func, ast.Name)
        and value.func.id == "frozenset"
        and value.args
        and isinstance(value.args[0], ast.Set)
    ):
        return None
    attrs: set[str] = set()
    for elt in value.args[0].elts:
        if isinstance(elt, ast.Attribute):
            attrs.add(elt.attr)
    return attrs or None


def _primary_risk(attrs: set[str]) -> str:
    """Reduce a set of RiskClass attr names to the single most severe, lowercased."""
    for name in RISK_SEVERITY:
        if name in attrs:
            return name.lower()
    return "read_only"


def extract_risk_registry(mcp_repo: Path) -> dict[str, str]:
    """Parse security.py: TOOL_RISK_REGISTRY -> {tool_name: primary_risk_class}."""
    security_file = mcp_repo / SECURITY_FILE
    if not security_file.is_file():
        _warn(f"security.py not found: {security_file}")
        return {}

    tree = ast.parse(security_file.read_text(encoding="utf-8"))

    # Pass 1: module-level frozenset aliases (_RO, _SW, _WS, _AO, _EW).
    aliases: dict[str, set[str]] = {}
    registry_node: ast.expr | None = None
    for node in tree.body:
        targets = _assign_targets(node)
        value = getattr(node, "value", None)
        if value is None or not targets:
            continue
        attrs = _riskclass_attrs_from_frozenset_call(value)
        if attrs is not None:
            for target in targets:
                aliases[target] = attrs
        if "TOOL_RISK_REGISTRY" in targets:
            registry_node = value

    if registry_node is None or not isinstance(registry_node, ast.Dict):
        _warn("TOOL_RISK_REGISTRY dict not found in security.py")
        return {}

    # Pass 2: resolve each registry entry (alias Name or inline frozenset call).
    risks: dict[str, str] = {}
    for key_node, value_node in zip(registry_node.keys, registry_node.values):
        if not (isinstance(key_node, ast.Constant) and isinstance(key_node.value, str)):
            continue
        tool_name = key_node.value
        attrs: set[str] | None = None
        if isinstance(value_node, ast.Name):
            attrs = aliases.get(value_node.id)
            if attrs is None:
                _warn(f"TOOL_RISK_REGISTRY['{tool_name}'] references unknown alias "
                      f"'{value_node.id}'")
        else:
            attrs = _riskclass_attrs_from_frozenset_call(value_node)
            if attrs is None:
                _warn(f"TOOL_RISK_REGISTRY['{tool_name}'] has an unrecognized value shape")
        if attrs:
            risks[tool_name] = _primary_risk(attrs)

    if not risks:
        _warn("risk registry extraction produced no entries")
    return risks


# ---------------------------------------------------------------------------
# server.py + registrar-internal gates — registrar function -> env flag
# ---------------------------------------------------------------------------

def _settings_flag_from_test(test: ast.expr) -> str:
    """Return the first `settings.<FLAG>` attribute name found in an If test."""
    for node in ast.walk(test):
        if (
            isinstance(node, ast.Attribute)
            and isinstance(node.value, ast.Name)
            and node.value.id == "settings"
        ):
            return node.attr
    return ""


def extract_feature_gates(mcp_repo: Path) -> dict[str, str]:
    """Map registrar function name -> feature flag gating its registration."""
    gates: dict[str, str] = {}

    server_file = mcp_repo / SERVER_FILE
    if server_file.is_file():
        tree = ast.parse(server_file.read_text(encoding="utf-8"))
        # Walk the whole module: covers `if settings.X:` gates in the module
        # body AND inside any setup function (e.g. main()).
        for node in ast.walk(tree):
            if not isinstance(node, ast.If):
                continue
            flag = _settings_flag_from_test(node.test)
            if not flag:
                continue
            for stmt in node.body:
                for call in ast.walk(stmt):
                    if (
                        isinstance(call, ast.Call)
                        and isinstance(call.func, ast.Name)
                        and call.func.id.startswith("register_")
                    ):
                        gates[call.func.id] = flag
    else:
        _warn(f"server.py not found: {server_file}")

    # Gates living inside the registrar functions themselves (early return on
    # a settings flag) — invisible to the server.py scan above.
    gates.update(INTERNALLY_GATED)

    # Validate every flag name against config.py — catches flag renames.
    config_file = mcp_repo / CONFIG_FILE
    if config_file.is_file():
        config_text = config_file.read_text(encoding="utf-8")
        for registrar, flag in sorted(gates.items()):
            if flag not in config_text:
                _warn(f"feature flag '{flag}' (gating {registrar}) not found in "
                      f"{config_file} — was it renamed?")
    else:
        _warn(f"config.py not found, cannot validate feature flags: {config_file}")

    return gates


# ---------------------------------------------------------------------------
# custom_tools.yaml — dynamically registered parameterized query tools
# ---------------------------------------------------------------------------

def extract_custom_tools(mcp_repo: Path) -> list[dict]:
    """Parse custom_tools.yaml at the repo root into [{name, summary, parameters, database}]."""
    yaml_file = mcp_repo / CUSTOM_TOOLS_YAML
    if yaml is None:
        _warn("PyYAML not installed — skipping custom_tools.yaml")
        return []
    if not yaml_file.is_file():
        _warn(f"custom_tools.yaml not found: {yaml_file}")
        return []

    data = yaml.safe_load(yaml_file.read_text(encoding="utf-8")) or {}
    entries = data.get("tools", []) if isinstance(data, dict) else []
    custom_tools = []
    for entry in entries:
        if not isinstance(entry, dict) or not entry.get("name"):
            continue
        description = " ".join(str(entry.get("description", "")).split())
        first_sentence = re.split(r"(?<=[.!?])\s", description)[0] if description else ""
        parameters = entry.get("parameters") or {}
        custom_tools.append({
            "name": entry["name"],
            "summary": first_sentence,
            "parameters": list(parameters.keys()) if isinstance(parameters, dict) else [],
            "database": entry.get("database", ""),
        })
    return custom_tools


# ---------------------------------------------------------------------------
# Agent personas — _VALID_ROLES + prompts/agents/<role>.md one-liners
# ---------------------------------------------------------------------------

_MD_LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")

# Shared-include preamble lines (e.g. "apply every rule in
# _shared_quality_rules.md") are boilerplate, not persona summaries, and
# their targets are agent-internal files that don't exist in the docs.
_PERSONA_BOILERPLATE_MARKERS = ("_shared_quality_rules", "_forensic_standards")


def _persona_one_liner(prompt_file: Path) -> str:
    """First substantive line of a persona prompt (headings and shared-include
    boilerplate skipped, markdown links flattened), truncated to 140 chars."""
    for line in prompt_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if any(marker in stripped for marker in _PERSONA_BOILERPLATE_MARKERS):
            continue
        return _MD_LINK_RE.sub(r"\1", stripped)[:140]
    return ""


def extract_personas(mcp_repo: Path) -> list[dict]:
    """Parse governance/agents.py for _VALID_ROLES and pair each with a prompt one-liner."""
    agents_file = mcp_repo / AGENTS_FILE
    if not agents_file.is_file():
        _warn(f"agents.py not found: {agents_file}")
        return []

    tree = ast.parse(agents_file.read_text(encoding="utf-8"))
    roles: list[str] = []
    for node in tree.body:
        if "_VALID_ROLES" in _assign_targets(node):
            try:
                roles = sorted(ast.literal_eval(node.value))
            except ValueError as exc:
                _warn(f"_VALID_ROLES is not a pure literal: {exc}")
            break
    if not roles:
        _warn("no roles extracted from _VALID_ROLES")
        return []

    prompt_dirs = [mcp_repo / d for d in PROMPTS_AGENTS_DIRS if (mcp_repo / d).is_dir()]
    personas = []
    for role in roles:
        summary = ""
        for prompt_dir in prompt_dirs:
            prompt_file = prompt_dir / f"{role}.md"
            if prompt_file.is_file():
                summary = _persona_one_liner(prompt_file)
                break
        else:
            _warn(f"no prompt file found for persona '{role}'")
        personas.append({"role": role, "summary": summary})
    return personas


# ---------------------------------------------------------------------------
# Mini-app surfaces — distinct ui://cerebro/<slug> resource URIs
# ---------------------------------------------------------------------------

_UI_URI_RE = re.compile(r"ui://cerebro/([a-z_]+)")

# The bare chart canvas is an inline rendering surface, not a mini-app;
# the docs count mini-apps + the Report Renderer.
_NON_APP_SURFACES = {"visualization"}


def extract_ui_surfaces(mcp_repo: Path) -> list[str]:
    """Distinct mini-app resource slugs found under tools/ (sorted)."""
    slugs: set[str] = set()
    tools_dir = mcp_repo / "src" / "cerebro_mcp" / "tools"
    for py in tools_dir.rglob("*.py"):
        slugs.update(_UI_URI_RE.findall(py.read_text(encoding="utf-8")))
    return sorted(slugs - _NON_APP_SURFACES)


# ---------------------------------------------------------------------------
# Top-level convenience
# ---------------------------------------------------------------------------

def introspect(mcp_repo: Path) -> dict:
    """Run all extractors and return the enriched tool surface + warnings."""
    WARNINGS.clear()

    tools = extract_static_tools(mcp_repo)
    tool_meta, core_names = extract_tool_meta(mcp_repo)
    risks = extract_risk_registry(mcp_repo)
    gates = extract_feature_gates(mcp_repo)
    custom_tools = extract_custom_tools(mcp_repo)
    personas = extract_personas(mcp_repo)
    ui_surfaces = extract_ui_surfaces(mcp_repo)

    for tool in tools:
        meta = tool_meta.get(tool["name"], {})
        tool["tier"] = meta.get("tier", "advanced")
        tool["domain"] = meta.get("domain", "(inferred)")
        tool["core"] = tool["name"] in core_names
        # security.py's get_risk_classes() defaults unknown tools to read_only.
        tool["risk"] = risks.get(tool["name"], "read_only")
        tool["gate"] = gates.get(tool["registrar"], "")

    return {
        "tools": tools,
        "custom_tools": custom_tools,
        "personas": personas,
        "ui_surfaces": ui_surfaces,
        "core_tool_names": sorted(core_names),
        "warnings": list(WARNINGS),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    if len(sys.argv) > 1:
        mcp_repo = Path(sys.argv[1]).resolve()
    else:
        mcp_repo = (Path(__file__).resolve().parent.parent.parent / "cerebro-mcp").resolve()

    print(f"Introspecting MCP repo: {mcp_repo}")
    if not mcp_repo.is_dir():
        print(f"ERROR: repo directory not found: {mcp_repo}")
        return 1

    result = introspect(mcp_repo)
    tools = result["tools"]

    per_package: dict[str, int] = defaultdict(int)
    per_tier: dict[str, int] = defaultdict(int)
    per_risk: dict[str, int] = defaultdict(int)
    per_gate: dict[str, int] = defaultdict(int)
    for tool in tools:
        per_package[tool["package"]] += 1
        per_tier[tool["tier"]] += 1
        per_risk[tool["risk"]] += 1
        if tool["gate"]:
            per_gate[tool["gate"]] += 1

    print(f"\nStatic tools: {len(tools)}")
    print("  Per package:")
    for package, count in sorted(per_package.items()):
        print(f"    {package}: {count}")
    print("  Per tier:")
    for tier, count in sorted(per_tier.items()):
        print(f"    {tier}: {count}")
    print("  Per risk class:")
    for risk, count in sorted(per_risk.items()):
        print(f"    {risk}: {count}")
    print("  Gated tools per flag:")
    if per_gate:
        for flag, count in sorted(per_gate.items()):
            print(f"    {flag}: {count}")
    else:
        print("    (none)")

    print(f"\nCustom YAML tools: {len(result['custom_tools'])}")
    print(f"Agent personas: {len(result['personas'])}")
    print(f"Core tool names: {len(result['core_tool_names'])}")

    if result["warnings"]:
        print(f"\nWarnings ({len(result['warnings'])}):")
        for warning in result["warnings"]:
            print(f"  - {warning}")
    else:
        print("\nNo warnings.")

    if not tools:
        print("ERROR: no static tools found — introspection is broken or repo moved.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
