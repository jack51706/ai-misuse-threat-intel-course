"""Regression checks for deployment mistakes, using temporary real site files."""

from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validate_site import main, validate_site


def html(body: str = "") -> str:
    return ("<!doctype html><html lang='zh-Hant'><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width, initial-scale=1'>"
            f"<title>Course</title></head><body>{body}</body></html>")


class ValidateSiteTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name) / "site"
        self.site.mkdir()

    def write(self, name: str, content: str) -> None:
        path = self.site / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_valid_encoded_paths_queries_and_shell_routes_without_network(self):
        self.write("index.html", html("""
            <a href='lessons/中文%20課程.html?version=2#%E7%AF%84%E5%9C%8D'>Lesson</a>
            <a href='#lessons/中文%20課程.html#%E7%AF%84%E5%9C%8D'>Shell route</a>
            <a href='index.html#shared/analysis.html#evidence'>Analysis</a>
            <a href='https://example.invalid/research'>External research</a>
            <a href='mailto:author@example.invalid'>Mail</a>
            <img src='data:image/png;base64,aGVsbG8='>
            <img src='https://example.invalid/image.png'>
        """))
        self.write("lessons/中文 課程.html", html("<h2 id='範圍'>Scope</h2><img src='../figures/chart.svg?x=1'>"))
        self.write("shared/analysis.html", html("<h2 id='evidence'>Evidence</h2>"))
        self.write("figures/chart.svg", "<svg/>")
        with patch("socket.create_connection", side_effect=AssertionError("must stay offline")):
            result = validate_site(self.site)
        self.assertEqual([], result.errors)
        self.assertEqual(3, result.html_count)
        self.assertEqual(3, result.images)
        self.assertEqual(1, result.image_files)
        self.assertGreater(result.total_bytes, 0)

    def test_missing_image_and_cross_page_anchor_are_reported_with_source(self):
        self.write("index.html", html("<img src='figures/missing.png'><a href='lesson.html#missing'>Read</a>"))
        self.write("lesson.html", html("<h1 id='present'>Present</h1>"))
        errors = "\n".join(validate_site(self.site).errors)
        self.assertIn("index.html:1:", errors)
        self.assertIn("missing local file: figures/missing.png", errors)
        self.assertIn("missing anchor #missing in lesson.html", errors)

    def test_shell_route_validates_target_and_anchor_instead_of_shell_dom(self):
        self.write("index.html", html("<a href='#missing.html'>Missing</a><a href='#lesson.html#absent'>Anchor</a>"))
        self.write("lesson.html", html())
        errors = "\n".join(validate_site(self.site).errors)
        self.assertIn("missing local file: missing.html", errors)
        self.assertIn("missing anchor #absent in lesson.html", errors)

    def test_url_cannot_escape_site_even_when_outside_file_exists(self):
        (self.site.parent / "private.html").write_text(html(), encoding="utf-8")
        for value in ("../private.html", "%2e%2e/private.html", "..%5cprivate.html", "file:///private.html"):
            with self.subTest(value=value):
                self.write("index.html", html(f"<a href='{value}'>Outside</a>"))
                result = validate_site(self.site)
                self.assertFalse(result.ok)
                self.assertTrue(any("unsafe" in error or "escapes" in error for error in result.errors))

    def test_case_mismatch_fails_on_windows_before_deploying_to_linux(self):
        self.write("index.html", html("<a href='Lesson.html'>Lesson</a>"))
        self.write("lesson.html", html())
        self.assertIn("missing local file: Lesson.html", "\n".join(validate_site(self.site).errors))

    def test_legacy_artifact_state_source_and_shared_directory_are_rejected(self):
        self.write("index.html", html("<a href='_shared/analysis.html'>Analysis</a>"))
        for name in ("published-state.json", "publish-manifest.json", "lesson.md", "lesson.meta.json", "build.py"):
            self.write(name, "private")
        self.write("_shared/analysis.html", html())
        errors = "\n".join(validate_site(self.site).errors)
        for name in ("published-state.json", "publish-manifest.json", "lesson.md", "lesson.meta.json", "build.py"):
            self.assertIn(f"{name}: source or build-state", errors)
        self.assertIn("_shared URL must map to shared", errors)

    def test_fragment_only_and_directory_links_with_project_base_path(self):
        self.write("index.html", html("<a href='/course/lessons/'>Lesson</a><a href='#main'>Main</a><main id='main'></main>"))
        self.write("lessons/index.html", html("<a href='../index.html?from=lesson#main'>Back</a>"))
        self.assertEqual([], validate_site(self.site, "/course/").errors)

    def test_incomplete_shell_is_rejected_and_cli_returns_failure(self):
        self.write("index.html", "<title>Incomplete shell</title><iframe src='lesson.html'></iframe>")
        self.write("lesson.html", html())
        result = validate_site(self.site)
        for requirement in ("HTML5 doctype", "html/head/body", "html lang", "UTF-8 charset", "responsive viewport"):
            self.assertTrue(any(requirement in error for error in result.errors), requirement)
        with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
            self.assertEqual(1, main(["--site", str(self.site)]))
        self.write("index.html", html())
        with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
            self.assertEqual(0, main(["--site", str(self.site)]))

    def test_missing_site_does_not_create_files(self):
        missing = self.site / "missing"
        self.assertFalse(validate_site(missing).ok)
        self.assertFalse(missing.exists())


if __name__ == "__main__":
    unittest.main()
