"""Regression tests for published lesson structure and safe navigation."""
import re
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_html


class Elements(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.elements = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

    def attributes(self, tag):
        return [attrs for name, attrs in self.elements if name == tag]


class LessonRenderingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.original = (build_html.ROOT, build_html.EMBED, build_html.fig_pages)
        build_html.ROOT = str(self.root)
        build_html.EMBED = False
        build_html.fig_pages = {15, 16, 17}

    def tearDown(self):
        build_html.ROOT, build_html.EMBED, build_html.fig_pages = self.original
        self.temp.cleanup()

    def source(self, rel, text="# 教材\n"):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def render(self, rel, text):
        path = self.source(rel, text)
        return build_html.convert_one(str(path), rel)

    def test_page_references_do_not_split_tables_or_headings(self):
        result = self.render("01-cyber/GTG-50014-test.md", """# 測試教材

## p.16 圖表判讀

| 項目 | 證據 |
| --- | --- |
| 活動期間 | Figure 2（p.15） |
| 下一列 | 仍應在同一表格 |
| 圖檔 | `../figures/page-017.png` |
""")
        self.assertEqual(result.count("<table>"), 1)
        self.assertEqual(result.count("<tr>"), 4)
        table = re.search(r"<table>.*?</table>", result, re.S).group()
        self.assertNotIn("<img", table)
        self.assertIn("下一列", table)
        self.assertIn(">p.16 圖表判讀</h2>", result)
        self.assertEqual(len(Elements(result).attributes("img")), 3)

    def test_explicit_figures_are_lazy_and_code_examples_stay_code(self):
        result = self.render("01-cyber/GTG-50014-test.md", """# 圖片

![圖 15](../figures/page-015.png)

`../figures/page-016.png`

```text
../figures/page-017.png
```
""")
        images = Elements(result).attributes("img")
        self.assertEqual(len(images), 3)
        self.assertTrue(all(i["loading"] == "lazy" for i in images))
        self.assertTrue(all(i["decoding"] == "async" for i in images))
        self.assertIn('<code class="language-text">../figures/page-017.png', result)

    def test_navigation_preserves_hash_and_query_without_linking_iocs(self):
        self.source("_shared/01-topic.md")
        self.source("_shared/00-agent-brief.md")
        result = self.render("01-cyber/lesson.md", """# **中文**標題

## 章節

[教材](../_shared/01-topic.md?mode=read#section)
[外部文件](https://example.com/readme.md?x=1#part)
`../_shared/01-topic.md`
`../_shared/00-agent-brief.md`
`../_wip/draft.md`
`example[.]com`
""")
        links = Elements(result).attributes("a")
        self.assertIn("<title>中文標題</title>", result)
        self.assertIn("../00-index.html", [a.get("href") for a in links])
        self.assertIn("../_shared/01-topic.html?mode=read#section", [a.get("href") for a in links])
        self.assertIn("../_shared/01-topic.html", [a.get("href") for a in links])
        external = next(a for a in links if a.get("href", "").startswith("https:"))
        self.assertEqual(external["href"], "https://example.com/readme.md?x=1#part")
        self.assertEqual(external["target"], "_blank")
        self.assertEqual(set(external["rel"].split()), {"noopener", "noreferrer"})
        self.assertIn("<code>../_shared/00-agent-brief.md</code>", result)
        self.assertIn("<code>../_wip/draft.md</code>", result)
        self.assertIn("<code>example[.]com</code>", result)
        self.assertIn('aria-label="本頁章節"', result)
        ids = {a.get("id") for _, a in Elements(result).elements if a.get("id")}
        for a in links:
            if a.get("href", "").startswith("#"):
                self.assertIn(a["href"][1:], ids)

    def test_code_blocks_are_not_changed_into_lesson_links(self):
        self.source("_shared/01-topic.md")
        result = self.render("01-cyber/lesson.md", "# 範例\n\n```text\n../_shared/01-topic.md\n```\n")
        self.assertNotIn('href="../_shared/01-topic.html"', result)

    def test_link_labels_do_not_become_nested_links(self):
        self.source("_shared/01-topic.md")
        result = self.render("01-cyber/lesson.md", "# 連結\n\n[`../_shared/01-topic.md`](../_shared/01-topic.md)\n")
        self.assertIn('<a href="../_shared/01-topic.html"><code>../_shared/01-topic.md</code></a>', result)

    def test_mermaid_loads_only_for_diagrams_with_strict_security(self):
        plain = self.render("01-cyber/plain.md", "# 純文字\n")
        self.assertNotIn("mermaid.min.js", plain)
        diagram = self.render("01-cyber/diagram.md", '# 圖\n\n```mermaid\ngraph LR\nA["<script>alert(1)</script>"] --> B\n```\n')
        self.assertIn("mermaid.min.js", diagram)
        self.assertIn("securityLevel:'strict'", diagram)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", diagram)
        self.assertNotIn("MERMAIDPLACEHOLDER", diagram)

    def test_only_explicit_course_sources_are_publishable(self):
        allowed = ["00-index.md", "01-cyber/lesson.md", "_shared/01-topic.md", "09-external-research/study.md"]
        excluded = ["notes.md", "_shared/00-agent-brief.md", "09-external-research/_brief.md",
                    "_slides_generator/node_modules/library/README.md", "_site/copy.md",
                    "_wip/draft.md", "01-cyber/nested/draft.md", "node_modules/README.md"]
        for rel in allowed + excluded:
            self.source(rel)
        found = [rel for _, rel in build_html.iter_publishable_markdown()]
        self.assertEqual(sorted(found), sorted(allowed))
        build_html.main()
        self.assertTrue(all((self.root / rel).with_suffix(".html").exists() for rel in allowed))
        self.assertFalse(any((self.root / rel).with_suffix(".html").exists() for rel in excluded))


class ExistingCourseRegressionTests(unittest.TestCase):
    def test_existing_affected_tables_keep_every_row(self):
        root = Path(__file__).resolve().parents[1]
        lessons = [
            "01-cyber/GTG-50014-shinyhunters.md",
            "02-influence/GTG-54002-influence-as-a-service.md",
            "02-influence/GTG-84005-malaysia-election-platform.md",
            "03-surveillance/GTG-14010-uyghurs-syria.md",
            "03-surveillance/GTG-14021-weiwen-transnational-repression.md",
        ]
        original_embed = build_html.EMBED
        build_html.EMBED = False
        try:
            for rel in lessons:
                with self.subTest(lesson=rel):
                    path = root / rel
                    source = path.read_text(encoding="utf-8")
                    baseline = build_html.markdown.markdown(source, extensions=["tables", "fenced_code"])
                    result = build_html.convert_one(str(path), rel)
                    self.assertEqual(result.count("<tr>"), baseline.count("<tr>"))
        finally:
            build_html.EMBED = original_embed


if __name__ == "__main__":
    unittest.main()
