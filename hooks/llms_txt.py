from __future__ import annotations

import posixpath
import re
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any


DEFAULT_SECTION_RULES = {
    "Docs": [
        "index.md",
        "getting-started/",
        "api/",
        "data-pipeline/",
        "models/",
        "mcp/",
    ],
    "Research": [
        "research/",
        "protocols/",
        "esg-reporting/",
    ],
    "Optional": [
        "dashboard/",
        "operations/",
        "reference/",
        "developer/",
    ],
}
SECTION_ORDER = ("Docs", "Research", "Optional")
ASSET_EXTENSIONS = {
    ".avif",
    ".bmp",
    ".css",
    ".gif",
    ".ico",
    ".jpeg",
    ".jpg",
    ".js",
    ".json",
    ".pdf",
    ".png",
    ".svg",
    ".txt",
    ".webp",
    ".xml",
    ".yaml",
    ".yml",
}
LINK_RE = re.compile(r"(!?\[[^\]]*\])\(([^)]+)\)")
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
CODE_FENCE_RE = re.compile(r"^(```|~~~)")


@dataclass
class PageRecord:
    src_uri: str
    location: str
    section: str
    nav_title: str
    title: str
    description: str
    html_path: str
    html_url: str
    markdown_path: str
    markdown_url: str
    body: str
    mirror_body: str = ""


@dataclass
class HookState:
    site_url: str = ""
    project_title: str = ""
    project_summary: str = ""
    intro: str = ""
    fallback_section: str = "Optional"
    section_rules: dict[str, list[str]] = field(default_factory=dict)
    order_by_src_uri: dict[str, int] = field(default_factory=dict)
    nav_title_by_src_uri: dict[str, str] = field(default_factory=dict)
    markdown_path_by_src_uri: dict[str, str] = field(default_factory=dict)
    pages_by_src_uri: dict[str, PageRecord] = field(default_factory=dict)


STATE = HookState()


def normalize_path(path: str) -> str:
    cleaned = PurePosixPath(path).as_posix()
    if cleaned in (".", ""):
        return ""
    return cleaned.lstrip("/")


def ensure_site_root_path(path: str) -> str:
    normalized = normalize_path(path)
    return f"/{normalized}" if normalized else "/"


def absolute_url(site_url: str, path: str) -> str:
    normalized = normalize_path(path)
    base = site_url.rstrip("/") + "/"
    return base if not normalized else base + normalized


def mirror_path_from_dest_uri(dest_uri: str) -> str:
    return normalize_path(f"{dest_uri}.md")


def location_from_dest_uri(dest_uri: str) -> str:
    normalized = normalize_path(dest_uri)
    if normalized == "index.html":
        return ""
    if normalized.endswith("/index.html"):
        return normalized[: -len("index.html")]
    if normalized.endswith(".html"):
        return normalized
    return normalized


def resolve_relative_path(src_uri: str, target: str) -> str:
    target = target.strip()
    if target.startswith("/"):
        return normalize_path(target)
    base_dir = posixpath.dirname(normalize_path(src_uri))
    combined = posixpath.join(base_dir, target) if base_dir else target
    return normalize_path(posixpath.normpath(combined))


def classify_section(src_uri: str, section_rules: dict[str, list[str]], fallback: str) -> str:
    normalized = normalize_path(src_uri)
    for section in SECTION_ORDER:
        for rule in section_rules.get(section, []):
            normalized_rule = normalize_path(rule)
            if rule.endswith("/"):
                if normalized.startswith(normalized_rule):
                    return section
            elif normalized == normalized_rule:
                return section
    for section, rules in section_rules.items():
        if section in SECTION_ORDER:
            continue
        for rule in rules:
            normalized_rule = normalize_path(rule)
            if rule.endswith("/"):
                if normalized.startswith(normalized_rule):
                    return section
            elif normalized == normalized_rule:
                return section
    return fallback


def extract_title(meta: dict[str, Any], markdown: str, nav_title: str) -> str:
    meta_title = str(meta.get("title", "")).strip()
    if meta_title:
        return meta_title
    match = H1_RE.search(markdown)
    if match:
        return match.group(1).strip()
    return nav_title


def extract_description(meta: dict[str, Any], markdown: str) -> str:
    meta_description = str(meta.get("description", "")).strip()
    if meta_description:
        return " ".join(meta_description.split())
    blocks = re.split(r"\n\s*\n", markdown)
    saw_h1 = False
    for block in blocks:
        stripped = block.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            saw_h1 = True
            continue
        if not saw_h1:
            continue
        first_line = stripped.splitlines()[0].strip()
        if first_line.startswith(("#", "```", "~~~", "!!!", "???", "<", ">", "|", "-", "*")):
            continue
        if re.match(r"^\d+\.\s", first_line):
            continue
        return " ".join(stripped.split())
    return ""


def ensure_title_heading(markdown: str, title: str) -> str:
    if H1_RE.search(markdown):
        return markdown
    return f"# {title}\n\n{markdown.lstrip()}"


def split_link_target(target: str) -> tuple[str, str]:
    stripped = target.strip()
    for pattern in (r'\s+(?="[^"]*"$)', r"\s+(?='[^']*'$)"):
        match = re.search(pattern, stripped)
        if match:
            return stripped[: match.start()].strip(), stripped[match.start() :].strip()
    return stripped, ""


def is_external_link(target: str) -> bool:
    lowered = target.lower()
    return lowered.startswith(
        (
            "http://",
            "https://",
            "mailto:",
            "tel:",
            "data:",
        )
    )


def rewrite_markdown_links(
    markdown: str,
    src_uri: str,
    markdown_path_by_src_uri: dict[str, str],
) -> str:
    rewritten_lines: list[str] = []
    in_fence = False
    for line in markdown.splitlines():
        if CODE_FENCE_RE.match(line.strip()):
            in_fence = not in_fence
            rewritten_lines.append(line)
            continue
        if in_fence:
            rewritten_lines.append(line)
            continue

        def replace(match: re.Match[str]) -> str:
            label, raw_target = match.groups()
            link_target, suffix = split_link_target(raw_target)
            wrapped = False
            if link_target.startswith("<") and link_target.endswith(">"):
                wrapped = True
                link_target = link_target[1:-1].strip()

            if (
                not link_target
                or link_target.startswith("#")
                or link_target.startswith("/")
                or is_external_link(link_target)
            ):
                return match.group(0)

            path_part, anchor = (link_target.split("#", 1) + [""])[:2]
            resolved = resolve_relative_path(src_uri, path_part)
            extension = PurePosixPath(resolved).suffix.lower()
            replacement_target = ""

            if extension == ".md" and resolved in markdown_path_by_src_uri:
                replacement_target = markdown_path_by_src_uri[resolved]
            elif extension in ASSET_EXTENSIONS:
                replacement_target = ensure_site_root_path(resolved)
            else:
                return match.group(0)

            if anchor:
                replacement_target = f"{replacement_target}#{anchor}"
            if wrapped:
                replacement_target = f"<{replacement_target}>"
            if suffix:
                replacement_target = f"{replacement_target} {suffix}"
            return f"{label}({replacement_target})"

        rewritten_lines.append(LINK_RE.sub(replace, line))
    return "\n".join(rewritten_lines) + ("\n" if markdown.endswith("\n") else "")


def render_llms_index(project_title: str, summary: str, intro: str, pages: list[PageRecord]) -> str:
    lines = [f"# {project_title}", ""]
    if summary:
        lines.extend([f"> {summary}", ""])
    if intro:
        lines.extend([intro, ""])

    grouped = {section: [] for section in SECTION_ORDER}
    for page in pages:
        grouped.setdefault(page.section, []).append(page)

    for section in SECTION_ORDER:
        lines.append(f"## {section}")
        lines.append("")
        for page in grouped.get(section, []):
            if page.description:
                lines.append(f"- [{page.title}]({page.markdown_url}): {page.description}")
            else:
                lines.append(f"- [{page.title}]({page.markdown_url})")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def render_context(project_title: str, pages: list[PageRecord], include_optional: bool) -> str:
    lines = [
        f"# {project_title} Context",
        "",
        "This file is generated from the public MkDocs navigation.",
        "",
    ]
    for page in pages:
        if not include_optional and page.section == "Optional":
            continue
        lines.extend(
            [
                f"## {page.title}",
                "",
                f"- Section: {page.section}",
                f"- Page URL: {page.html_url}",
                f"- Markdown URL: {page.markdown_url}",
                "",
                page.mirror_body.strip(),
                "",
                "---",
                "",
            ]
        )
    while lines and lines[-1] == "":
        lines.pop()
    if lines and lines[-1] == "---":
        lines.pop()
    return "\n".join(lines).rstrip() + "\n"


def _reset_state(config: Any) -> None:
    extra = config.get("extra", {})
    llms = extra.get("llms", {})
    section_rules = {
        section: list(paths)
        for section, paths in llms.get("sections", DEFAULT_SECTION_RULES).items()
    }
    STATE.site_url = str(config.get("site_url", "")).rstrip("/") + "/"
    STATE.project_title = str(llms.get("title", config.get("site_name", "Documentation"))).strip()
    STATE.project_summary = str(llms.get("summary", "")).strip()
    STATE.intro = str(llms.get("intro", "")).strip()
    STATE.fallback_section = str(llms.get("fallback_section", "Optional")).strip() or "Optional"
    STATE.section_rules = section_rules
    STATE.order_by_src_uri.clear()
    STATE.nav_title_by_src_uri.clear()
    STATE.markdown_path_by_src_uri.clear()
    STATE.pages_by_src_uri.clear()


def on_config(config, **kwargs):  # noqa: ANN001
    _reset_state(config)
    return config


def on_nav(nav, *, config, files):  # noqa: ANN001
    for index, page in enumerate(getattr(nav, "pages", [])):
        src_uri = normalize_path(page.file.src_uri)
        STATE.order_by_src_uri[src_uri] = index
        STATE.nav_title_by_src_uri[src_uri] = page.title or src_uri
        STATE.markdown_path_by_src_uri[src_uri] = ensure_site_root_path(
            mirror_path_from_dest_uri(page.file.dest_uri)
        )
    return nav


def on_page_markdown(markdown, *, page, config, files):  # noqa: ANN001
    src_uri = normalize_path(page.file.src_uri)
    if src_uri not in STATE.order_by_src_uri:
        return markdown

    nav_title = STATE.nav_title_by_src_uri.get(src_uri, page.title or src_uri)
    title = extract_title(page.meta, markdown, nav_title)
    description = extract_description(page.meta, markdown)
    location = location_from_dest_uri(page.file.dest_uri)
    html_path = ensure_site_root_path(page.file.dest_uri)
    html_url = absolute_url(STATE.site_url, location)
    markdown_path = STATE.markdown_path_by_src_uri[src_uri]
    markdown_url = absolute_url(STATE.site_url, markdown_path.lstrip("/"))
    section = classify_section(src_uri, STATE.section_rules, STATE.fallback_section)

    STATE.pages_by_src_uri[src_uri] = PageRecord(
        src_uri=src_uri,
        location=location,
        section=section,
        nav_title=nav_title,
        title=title,
        description=description,
        html_path=html_path,
        html_url=html_url,
        markdown_path=markdown_path,
        markdown_url=markdown_url,
        body=markdown,
    )
    return markdown


def on_post_build(*, config):  # noqa: ANN001
    site_dir = Path(config["site_dir"])
    ordered_pages = [
        page
        for src_uri, page in sorted(
            STATE.pages_by_src_uri.items(),
            key=lambda item: STATE.order_by_src_uri.get(item[0], 10**9),
        )
    ]

    for page in ordered_pages:
        rewritten = rewrite_markdown_links(
            ensure_title_heading(page.body, page.title),
            page.src_uri,
            STATE.markdown_path_by_src_uri,
        )
        page.mirror_body = rewritten
        destination = site_dir / page.markdown_path.lstrip("/")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(rewritten, encoding="utf-8")

    (site_dir / "llms.txt").write_text(
        render_llms_index(
            STATE.project_title,
            STATE.project_summary,
            STATE.intro,
            ordered_pages,
        ),
        encoding="utf-8",
    )
    (site_dir / "llms-ctx.txt").write_text(
        render_context(STATE.project_title, ordered_pages, include_optional=False),
        encoding="utf-8",
    )
    (site_dir / "llms-ctx-full.txt").write_text(
        render_context(STATE.project_title, ordered_pages, include_optional=True),
        encoding="utf-8",
    )
