from html.parser import HTMLParser
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from content_quality import content_digest, load_catalog, reading_layers, render_learning_panel, review_for


class QualityTests(unittest.TestCase):
    def test_new_or_changed_lesson_cannot_inherit_a_verification_date(self):
        text = "# Lesson\n## Evidence\nold"
        catalog = {"pages": {"01-cyber/a.md": {
            "content_sha256": content_digest(text), "checked_on": "2026-09-19",
            "source_checked_on": "2026-09-19", "scope": "Only the date was checked"}}}
        self.assertEqual(review_for("01-cyber/a.md", text, catalog)["state"], "scoped")
        changed = review_for("01-cyber/a.md", text + " new claim", catalog)
        self.assertEqual(changed["state"], "pending")
        self.assertNotIn("source_checked_on", changed)
        self.assertEqual(review_for("01-cyber/new.md", text, catalog)["state"], "pending")

    def test_generated_ledger_does_not_recertify_editorial_content(self):
        before = "intro\n<!-- LEDGER:START -->old<!-- LEDGER:END -->\nmethod"
        after = "intro\n<!-- LEDGER:START -->new<!-- LEDGER:END -->\nmethod"
        relative = "09-external-research/00-external-research-intro.md"
        self.assertEqual(content_digest(before, relative), content_digest(after, relative))
        self.assertNotEqual(content_digest(before, relative), content_digest(after + " unsupported conclusion", relative))
        self.assertNotEqual(content_digest(before, "01-cyber/a.md"), content_digest(after, "01-cyber/a.md"))
        catalog = {"pages": {"01-cyber/a.md": {"content_sha256": content_digest(before),
                    "source_checked_on": "2026-09-19"}}}
        self.assertEqual(review_for("01-cyber/a.md", after, catalog)["state"], "pending")

    def test_reading_links_only_use_headings_that_exist(self):
        tokens = [{"level": 2, "id": "summary", "name": "一頁速覽", "children": []},
                  {"level": 2, "id": "evidence", "name": "證據與限制", "children": []},
                  {"level": 2, "id": "appendix", "name": "技術附錄", "children": []}]
        layers = reading_layers(tokens)
        self.assertEqual([h["id"] for h in layers["快速理解"]], ["summary"])
        self.assertEqual([h["id"] for h in layers["課堂必讀"]], ["evidence"])
        self.assertEqual([h["id"] for h in layers["技術／分析進階"]], ["appendix"])
        with tempfile.TemporaryDirectory() as root:
            panel = render_learning_panel("01-cyber/a.md", "# a", tokens, root)
        self.assertIn('href="#evidence"', panel)
        self.assertIn("待審：新教材", panel)
        self.assertIn("../10-practice/00-practice-guide.html", panel)

    def test_review_text_is_escaped_and_dates_not_invented(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "editorial").mkdir()
            catalog = {"schema_version": 1, "pages": {"a.md": {
                "content_sha256": content_digest("# a"), "checked_on": "2026-09-19",
                "scope": '<script>alert(1)</script>', "pending": ['<img src="x">'],
                "changes": [], "source_checked_on": None}}}
            (root / "editorial/catalog.json").write_text(json.dumps(catalog))
            panel = render_learning_panel("a.md", "# a", [], root)
            self.assertNotIn("<script>", panel)
            self.assertIn("&lt;script&gt;", panel)
            self.assertIn("来源逐項查證：尚未完成".replace("来源", "來源"), panel)
            self.assertEqual(load_catalog(root), catalog)


if __name__ == "__main__":
    unittest.main()
