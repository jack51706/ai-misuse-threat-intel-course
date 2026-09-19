import json
from hashlib import sha256
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_pages


class PagesBuildTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "_site").mkdir()
        (self.root / "_site/index.html").write_text('<iframe src="00-index.html"></iframe>')
        (self.root / "00-index.html").write_text('<a href="_shared/topic.html#intro">Read</a>')
        self.files = {"index.html": {"local": "_site/index.html"},
                      "00-index.html": {"local": "00-index.html"}}

    def build(self):
        for info in self.files.values():
            source = self.root / info["local"]
            if source.is_file():
                info.setdefault("sha256", sha256(source.read_bytes()).hexdigest())
        (self.root / "_site/publish-manifest.json").write_text(json.dumps({"files": self.files}))
        return build_pages.assemble(self.root)

    def test_only_manifest_and_referenced_images_are_published(self):
        (self.root / "_shared").mkdir()
        (self.root / "figures").mkdir()
        (self.root / "_shared/topic.html").write_text('<img src="../figures/page-001.png">')
        (self.root / "figures/page-001.png").write_bytes(b"PNG fixture")
        (self.root / "figures/page-002.png").write_bytes(b"unused")
        self.files["shared/topic.html"] = {"local": "_shared/topic.html"}
        state = self.root / "_site/published-state.json"
        state.write_text('{"preserve":true}')
        (self.root / "_site/stale.html").write_text("deleted lesson")
        output = self.build()
        self.assertEqual({p.relative_to(output).as_posix() for p in output.rglob("*") if p.is_file()},
                         {"index.html", "00-index.html", "shared/topic.html", "figures/page-001.png", ".nojekyll"})
        self.assertIn('href="shared/topic.html#intro"', (output / "00-index.html").read_text())
        self.assertEqual(state.read_text(), '{"preserve":true}')
        (output / "old.html").write_text("old")
        self.build()
        self.assertFalse((output / "old.html").exists())

    def test_failed_build_preserves_previous_output(self):
        output = self.build()
        self.files["missing.html"] = {"local": "missing.html"}
        with self.assertRaises(FileNotFoundError):
            self.build()
        self.assertTrue((output / "index.html").is_file())

    def test_path_escape_is_rejected(self):
        self.files["../outside.html"] = {"local": "00-index.html"}
        with self.assertRaises(ValueError):
            self.build()

    def test_changed_html_is_rejected_without_replacing_previous_site(self):
        output = self.build()
        original = (output / "00-index.html").read_bytes()
        (self.root / "00-index.html").write_text("changed after manifest")
        with self.assertRaises(ValueError):
            self.build()
        self.assertEqual((output / "00-index.html").read_bytes(), original)

    def test_non_html_manifest_entry_is_rejected(self):
        self.files["published-state.json"] = {"local": "_site/published-state.json"}
        with self.assertRaises(ValueError):
            self.build()

    def test_external_urls_and_text_are_not_remapped(self):
        source = '<a href="https://example.org/_shared/page.html">_shared/text</a>'
        self.assertEqual(build_pages.rewrite_links(source), source)
        self.assertIn('../shared/a.html?q=1&amp;x=2#h', build_pages.rewrite_links(
            '<a href="../_shared/a.html?q=1&amp;x=2#h">Read</a>'))


if __name__ == "__main__":
    unittest.main()
