import unittest

from hooks.llms_txt import (
    classify_section,
    extract_description,
    extract_title,
    location_from_dest_uri,
    mirror_path_from_dest_uri,
    rewrite_markdown_links,
)


SECTION_RULES = {
    "Docs": ["index.md", "getting-started/", "api/"],
    "Research": ["research/"],
    "Optional": ["reference/"],
}


class LlmsHookTests(unittest.TestCase):
    def test_classify_section_uses_rules_in_order(self):
        self.assertEqual(
            classify_section("getting-started/quickstart.md", SECTION_RULES, "Optional"),
            "Docs",
        )
        self.assertEqual(
            classify_section("research/mmm/index.md", SECTION_RULES, "Optional"),
            "Research",
        )
        self.assertEqual(
            classify_section("unknown/page.md", SECTION_RULES, "Optional"),
            "Optional",
        )

    def test_mirror_and_location_paths_follow_mkdocs_destinations(self):
        self.assertEqual(mirror_path_from_dest_uri("index.html"), "index.html.md")
        self.assertEqual(mirror_path_from_dest_uri("api/index.html"), "api/index.html.md")
        self.assertEqual(location_from_dest_uri("index.html"), "")
        self.assertEqual(location_from_dest_uri("api/index.html"), "api/")

    def test_extract_title_and_description_prefer_front_matter(self):
        markdown = "# Fallback Title\n\nFirst paragraph.\n\n## Details\n"
        meta = {"title": "Front Matter Title", "description": "Short summary"}
        self.assertEqual(extract_title(meta, markdown, "Nav Title"), "Front Matter Title")
        self.assertEqual(extract_description(meta, markdown), "Short summary")

    def test_extract_description_falls_back_to_first_paragraph_after_h1(self):
        markdown = "# Title\n\n```bash\nexample\n```\n\nFirst real paragraph.\n\n- Item\n"
        self.assertEqual(extract_description({}, markdown), "First real paragraph.")

    def test_rewrite_markdown_links_uses_site_root_paths(self):
        markdown = (
            "# Quick Start\n\n"
            "[API](../api/index.md)\n\n"
            "[Local anchor](../api/index.md#auth)\n\n"
            "![Logo](../assets/gnosis-logo.svg)\n\n"
            "[External](https://example.com)\n\n"
            "```md\n[Code link](../api/index.md)\n```\n"
        )
        rewritten = rewrite_markdown_links(
            markdown,
            "getting-started/quickstart.md",
            {
                "api/index.md": "/api/index.html.md",
                "getting-started/quickstart.md": "/getting-started/quickstart/index.html.md",
            },
        )
        self.assertIn("[API](/api/index.html.md)", rewritten)
        self.assertIn("[Local anchor](/api/index.html.md#auth)", rewritten)
        self.assertIn("![Logo](/assets/gnosis-logo.svg)", rewritten)
        self.assertIn("[External](https://example.com)", rewritten)
        self.assertIn("[Code link](../api/index.md)", rewritten)


if __name__ == "__main__":
    unittest.main()

