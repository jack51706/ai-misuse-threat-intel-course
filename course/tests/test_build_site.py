"""Navigation data and browser-routing regression tests (no network access)."""
import importlib.util
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location("build_site", Path(__file__).resolve().parents[1] / "build_site.py")
build_site = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(build_site)


class BuildSiteTests(unittest.TestCase):
    def test_title_uses_readable_chinese_heading(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "lesson.md"
            path.write_text("前言\n# **監控**與 [防禦](https://example.invalid) `GTG-1` ###\n", encoding="utf-8")
            self.assertEqual(build_site.title_from_markdown(path), "監控與 防禦 GTG-1")

    def test_collect_only_publishes_lessons_with_markdown_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for folder in ("01-cyber", "_shared", build_site.EXTERNAL):
                (root / folder).mkdir()
            for relative in ("01-cyber/GTG-1-test", "_shared/00-agent-brief", "_shared/01-topic"):
                (root / (relative + ".md")).write_text("# 繁體中文教材\n", encoding="utf-8")
                (root / (relative + ".html")).write_text("<h1>教材</h1>", encoding="utf-8")
            (root / "01-cyber/deleted.html").write_text("stale", encoding="utf-8")
            (root / build_site.EXTERNAL / "orphan.meta.json").write_text('{"title":"orphan"}', encoding="utf-8")
            with patch.object(build_site, "ROOT", directory):
                nav, stats, manifest, _ = build_site.collect()
            self.assertEqual(set(manifest), {"01-cyber/GTG-1-test.html", "shared/01-topic.html"})
            self.assertEqual(stats["pages"], 2)
            self.assertEqual(stats["external"], 0)
            self.assertEqual(nav[0]["items"][0]["desc"], "繁體中文教材")

    def test_missing_built_lesson_fails_before_publish(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory) / "01-cyber"
            folder.mkdir()
            (folder / "lesson.md").write_text("# 尚未建置", encoding="utf-8")
            with patch.object(build_site, "ROOT", directory), self.assertRaises(FileNotFoundError):
                build_site.collect()

    def test_manifest_uses_fresh_normalized_copies_without_changing_originals(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "01-cyber").mkdir()
            (root / "_shared").mkdir()
            samples = {
                "00-index": '<a href="_shared/01-cross-cutting-analysis.html#defense">跨案例</a>',
                "01-cyber/lesson": '<a href="../_shared/01-cross-cutting-analysis.html?q=1&amp;x=2#defense">防禦</a>',
                "_shared/01-cross-cutting-analysis": '<img src="../figures/page-001.png"><h1>防禦</h1>',
            }
            for name, document in samples.items():
                (root / (name + ".md")).write_text("# 跨案例教材", encoding="utf-8")
                (root / (name + ".html")).write_text(document, encoding="utf-8")
            stale = root / "_site/content/01-cyber/lesson.html"
            stale.parent.mkdir(parents=True)
            stale.write_text("stale copy", encoding="utf-8")
            with patch.object(build_site, "ROOT", directory):
                _, _, manifest, _ = build_site.collect()
            for published, info in manifest.items():
                self.assertEqual(info["local"], "_site/content/" + published)
                payload = (root / info["local"]).read_bytes()
                self.assertEqual(info["sha256"], hashlib.sha256(payload).hexdigest())
                self.assertEqual(info["bytes"], len(payload))
            self.assertIn('href="../shared/01-cross-cutting-analysis.html?q=1&amp;x=2#defense"', stale.read_text(encoding="utf-8"))
            self.assertIn('href="shared/01-cross-cutting-analysis.html#defense"', (root / manifest["00-index.html"]["local"]).read_text(encoding="utf-8"))
            for name, document in samples.items():
                self.assertEqual((root / (name + ".html")).read_text(encoding="utf-8"), document)
            original = root / "01-cyber/lesson.html"
            original.write_text('<a href="../_shared/01-cross-cutting-analysis.html#updated">新版本</a>', encoding="utf-8")
            with patch.object(build_site, "ROOT", directory):
                _, _, rebuilt, _ = build_site.collect()
            self.assertNotEqual(manifest["01-cyber/lesson.html"]["sha256"], rebuilt["01-cyber/lesson.html"]["sha256"])
            self.assertIn("#updated", stale.read_text(encoding="utf-8"))

    def test_link_rewrite_only_changes_real_local_attributes(self):
        untouched = '''<code>href="../_shared/notes.html"</code>
<script>const example = 'href="../_shared/notes.html"';</script>
<!-- <a href="../_shared/notes.html">comment</a> -->
<a href="https://example.invalid/_shared/notes.html">_shared/text</a>
<a href="//example.invalid/_shared/notes.html">external</a>
<span data-example="href='../_shared/notes.html'">example</span>'''
        self.assertEqual(build_site.rewrite_links(untouched), untouched)
        source = untouched + '\n<a href="../_shared/topic.html?a=1&amp;b=2#intro">local</a><img src=../_shared/pic.png>'
        rewritten = build_site.rewrite_links(source)
        self.assertTrue(rewritten.startswith(untouched))
        self.assertIn('href="../shared/topic.html?a=1&amp;b=2#intro"', rewritten)
        self.assertIn('src="../shared/pic.png"', rewritten)
        self.assertEqual(build_site.rewrite_links(rewritten), rewritten)

    def test_navigation_escapes_labels_and_carries_module_search_text(self):
        nav = [{"title": '網路 "行動"', "items": [{"src": "01-cyber/a.html", "code": "GTG-1", "desc": '<img onerror="alert(1)">'}]}]
        markup = build_site.render_nav(nav)
        self.assertIn('data-module="網路 &quot;行動&quot;"', markup)
        self.assertIn('&lt;img onerror=&quot;alert(1)&quot;&gt;', markup)
        self.assertNotIn("<img", markup)

    def test_shell_is_a_complete_mobile_document(self):
        self.assertTrue(build_site.SHELL.startswith("<!doctype html>"))
        self.assertIn('<html lang="zh-Hant">', build_site.SHELL)
        self.assertIn('<meta charset="utf-8">', build_site.SHELL)
        self.assertIn('name="viewport" content="width=device-width,initial-scale=1"', build_site.SHELL)
        self.assertTrue(build_site.SHELL.rstrip().endswith("</body></html>"))


# A small DOM boundary lets the real shipped script run without fetching fonts,
# Mermaid, course content, or threat indicators. Tests exercise observable state.
DOM_HARNESS = r"""
const assert = require('node:assert/strict');
const vm = require('node:vm');
const input = JSON.parse(require('node:fs').readFileSync(0, 'utf8'));
const events = {};
const nodes = {};
function element(id, dataset={}) {
  const classes = new Set();
  return {
    id, dataset, events:{}, attributes:{}, style:{}, value:'', target:'', inert:false,
    classList:{contains:x=>classes.has(x), add:x=>classes.add(x), remove:x=>classes.delete(x),
      toggle(x,on){if(on===undefined)on=!classes.has(x);if(on)classes.add(x);else classes.delete(x);return on;}},
    addEventListener(name,fn){this.events[name]=fn;},
    setAttribute(name,value){this.attributes[name]=value;},
    getAttribute(name){return this.attributes[name]??null;},
    removeAttribute(name){delete this.attributes[name];},
    hasAttribute(name){return Object.hasOwn(this.attributes,name);},
    focus(){document.activeElement=this;},
    closest(){return this;},
    contains(node){return this===node || (id==='sidebar' && (node===nodes.q || links.includes(node)));}
  };
}
for(const id of ['nav','viewer','now','app','sidebar','menu','close-menu','main','q','search-status','scrim','skip'])nodes[id]=element(id);
const links=[
  element('home',{src:'00-index.html',code:'首頁',desc:'課程總索引',module:'課程總索引'}),
  element('a',{src:'01-cyber/a.html',code:'GTG-1',desc:'台灣網路防禦',module:'網路行動'}),
  element('b',{src:'shared/b.html',code:'GTG-2',desc:'資料安全',module:'跨案例專題'})
];
const moduleNode=element('module');
moduleNode.querySelector=()=>links.slice(1).find(a=>!a.classList.contains('hidden'))||null;
nodes.nav.querySelectorAll=selector=>selector==='.mod'?[moduleNode]:links;
global.location=new URL('https://example.invalid/course/'+input.hash);
const replacements=[], historyCalls=[];
const frameDoc={baseURI:'https://example.invalid/course/00-index.html',events:{},addEventListener(name,fn){this.events[name]=fn;}};
nodes.viewer.contentDocument=frameDoc;
nodes.viewer.contentWindow={location:{replace(url){replacements.push(url);frameDoc.baseURI=url;}}};
global.document={title:'',activeElement:null,getElementById:id=>nodes[id],addEventListener(name,fn){events[name]=fn;}};
global.window={addEventListener(name,fn){events[name]=fn;}};
const media={matches:input.mobile,addEventListener(name,fn){this.listener=fn;}};
global.matchMedia=()=>media;
global.history={
  pushState(a,b,url){historyCalls.push(['push',url]);global.location=new URL(url,location);},
  replaceState(a,b,url){historyCalls.push(['replace',url]);global.location=new URL(url,location);}
};
function click(node, overrides={}){
  const event={target:node,button:0,defaultPrevented:false,preventDefault(){this.defaultPrevented=true;},...overrides};
  nodes.nav.events.click(event);return event;
}
vm.runInThisContext(input.script);
vm.runInThisContext(input.scenario);
"""


@unittest.skipUnless(shutil.which("node"), "Node.js is required for browser script regression tests")
class NavigationScriptTests(unittest.TestCase):
    def run_scenario(self, scenario, hash_value="", mobile=False):
        script = re.search(r"<script>(.*?)</script>", build_site.SHELL, re.S).group(1)
        result = subprocess.run(
            [shutil.which("node"), "-e", DOM_HARNESS],
            input=json.dumps({"script": script, "scenario": scenario, "hash": hash_value, "mobile": mobile}),
            text=True, encoding="utf-8", capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_history_and_article_anchor_are_restored(self):
        self.run_scenario(r"""
          assert.equal(replacements.at(-1),'https://example.invalid/course/01-cyber/a.html#defense');
          assert.equal(links[1].attributes['aria-current'],'page');
          click(links[2]);
          assert.deepEqual(historyCalls.at(-1),['push','#shared/b.html']);
          global.location=new URL('https://example.invalid/course/#01-cyber/a.html#defense');
          events.popstate();
          assert.equal(replacements.at(-1),'https://example.invalid/course/01-cyber/a.html#defense');
          const count=replacements.length;events.hashchange();assert.equal(replacements.length,count);
        """, "#01-cyber/a.html#defense")

    def test_invalid_route_never_loads_arbitrary_url(self):
        for hash_value in ("#https://evil.invalid/x", "#../private.html", "#%ZZ", '#x"]'):
            with self.subTest(hash_value=hash_value):
                self.run_scenario("assert.equal(replacements.at(-1),'https://example.invalid/course/00-index.html');", hash_value)

    def test_iframe_links_and_index_return_keep_single_shell(self):
        self.run_scenario(r"""
          click(links[1]);
          const anchor=element('article-link');anchor.attributes.href='../_shared/b.html#section';
          const event={target:anchor,button:0,preventDefault(){this.defaultPrevented=true;}};
          frameDoc.events.click(event);
          assert.equal(event.defaultPrevented,true);
          assert.equal(location.hash,'#shared/b.html#section');
          anchor.attributes.href='../index.html';frameDoc.events.click({target:anchor,button:0,preventDefault(){this.defaultPrevented=true;}});
          assert.equal(location.hash,'#00-index.html');
        """)

    def test_search_matches_chinese_module_and_multiple_terms(self):
        self.run_scenario(r"""
          nodes.q.value='網路 GTG-1';nodes.q.events.input();
          assert.equal(links[1].classList.contains('hidden'),false);
          assert.equal(links[2].classList.contains('hidden'),true);
          assert.equal(nodes['search-status'].textContent,'找到 1 份教材');
          nodes.q.value='不存在的教材';nodes.q.events.input();
          assert.match(nodes['search-status'].textContent,/找不到/);
          assert.equal(links[0].classList.contains('hidden'),false);
        """)

    def test_mobile_drawer_restores_keyboard_focus(self):
        self.run_scenario(r"""
          assert.equal(nodes.sidebar.inert,true);
          nodes.menu.events.click();
          assert.equal(nodes.menu.attributes['aria-expanded'],'true');
          assert.equal(nodes.main.inert,true);assert.equal(document.activeElement,nodes.q);
          nodes['close-menu'].focus();
          events.keydown({key:'Tab',shiftKey:true,preventDefault(){}});
          assert.equal(document.activeElement,links[2]);
          events.keydown({key:'Escape',preventDefault(){}});
          assert.equal(nodes.sidebar.inert,true);assert.equal(nodes.main.inert,false);
          assert.equal(document.activeElement,nodes.menu);
          nodes.menu.events.click();nodes['close-menu'].events.click();
          assert.equal(nodes.menu.attributes['aria-expanded'],'false');
          assert.equal(document.activeElement,nodes.menu);
        """, mobile=True)

    def test_modified_click_keeps_browser_new_tab_behavior(self):
        self.run_scenario(r"""
          const count=replacements.length;
          assert.equal(click(links[1],{ctrlKey:true}).defaultPrevented,false);
          assert.equal(replacements.length,count);
        """)


if __name__ == "__main__":
    unittest.main()
