import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_content import check
from content_quality import content_digest


class ContentChecksTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / "editorial").mkdir()
        (self.root / "00-index.md").write_text("# Index\n")
        self.entry = {"content_sha256": content_digest("# Index\n"), "checked_on": "2026-09-19",
                      "scope": "Structure only", "pending": ["Source verification"]}

    def catalog(self):
        (self.root / "editorial/catalog.json").write_text(json.dumps(
            {"schema_version": 1, "pages": {"00-index.md": self.entry}}))

    def test_unreviewed_and_changed_pages_are_pending_without_false_certification(self):
        self.assertEqual(check(self.root), ([], ["00-index.md"], 1))
        self.catalog()
        self.assertEqual(check(self.root), ([], [], 1))
        (self.root / "00-index.md").write_text("# Index\nNew fact")
        self.assertEqual(check(self.root), ([], ["00-index.md"], 1))

    def test_source_date_requires_scope_and_valid_dates_and_digest(self):
        self.entry.update(source_checked_on="not-a-date", content_sha256="z" * 64)
        self.catalog()
        errors, _, _ = check(self.root)
        self.assertEqual(len(errors), 3)

    def test_external_source_metadata_is_required_and_classified(self):
        folder = self.root / "09-external-research"
        folder.mkdir()
        page = folder / "example.md"
        page.write_text("# External\n")
        errors, _, _ = check(self.root)
        self.assertEqual(len(errors), 1)
        page.with_suffix(".meta.json").write_text(json.dumps(
            {"id": "wrong", "url": "http://example.org", "source_type": "rumour"}))
        self.assertEqual(len(check(self.root)[0]), 2)


if __name__ == "__main__":
    unittest.main()
