#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
產生 Artifact 站台的殼頁與發布清單。

  python build_html.py                    # 先把所有 .md 轉成 .html
  python build_site.py                    # 再產生殼頁與發布清單（皆在 course/ 目錄下執行）
  python build_site.py --mark-published   # 發布成功後執行，記錄「已發布」的版本

輸出（都在 course/_site/）：
  index.html              側欄導覽 + iframe 檢視器；發布到 Artifact 根目錄的 index.html
  content/                依發布路徑正規化連結的教材副本（保留原 HTML 供本機閱讀）
  publish-manifest.json   全部可發布檔案：發布路徑 -> {local, sha256, bytes}
  publish-pending.json    與 published-state.json 相比新增或變動的檔案（發布時只送這些）
  published-state.json    上次成功發布的版本（只由 --mark-published 寫入）

另外會同步 09-external-research/00-external-research-intro.md 裡
<!-- LEDGER:START --> 與 <!-- LEDGER:END --> 之間的收錄清單表（來源：同資料夾的 *.meta.json），
並重新轉出該頁的 .html。

重跑安全：只讀 .html / .png / .meta.json，只寫 _site/ 與導論頁的清單區段。
"""
import os, re, sys, json, glob, hashlib, html, datetime
from html.parser import HTMLParser
from urllib.parse import urlsplit, urlunsplit

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "_site")
EXTERNAL = "09-external-research"
INTRO_MD = os.path.join(ROOT, EXTERNAL, "00-external-research-intro.md")

MODULES = [  # (資料夾, 側欄標題)；順序即側欄順序
    ("_shared", "跨案例／專題"),
    ("01-cyber", "網路行動"),
    ("02-influence", "影響力行動"),
    ("03-surveillance", "監控行動"),
    ("04-weapons", "常規武器"),
    ("05-bio", "生物濫用"),
    ("06-scams", "詐騙"),
    ("07-distillation", "非法蒸餾"),
    ("08-capability-research", "能力評測"),
    (EXTERNAL, "延伸研究"),
]


def pub(rel):
    """專案相對路徑 -> Artifact 發布路徑（_shared 發布為 shared）"""
    rel = rel.replace("\\", "/")
    return "shared/" + rel[len("_shared/"):] if rel.startswith("_shared/") else rel


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def esc(s):
    return html.escape(str(s), quote=True)


def rewrite_links(document):
    """僅正規化 HTML 屬性的本機 _shared 路徑，不改內文、腳本或外部網址。"""
    attribute = re.compile(r'''(\s+)([^\s/=<>]+)(\s*=\s*)("[^"]*"|'[^']*'|[^\s>]+)''')

    def replace(match):
        if match.group(2).lower() not in ("href", "src"):
            return match.group(0)
        raw = match.group(4)
        quote = raw[0] if raw[0] in "\"'" else ""
        value = html.unescape(raw[1:-1] if quote else raw)
        try:
            url = urlsplit(value)
        except ValueError:
            return match.group(0)
        if url.scheme or url.netloc or "_shared" not in url.path.split("/"):
            return match.group(0)
        path = "/".join("shared" if part == "_shared" else part for part in url.path.split("/"))
        value = urlunsplit((url.scheme, url.netloc, path, url.query, url.fragment))
        quote = quote or '"'
        return match.group(1) + match.group(2) + match.group(3) + quote + esc(value) + quote

    class LinkParser(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=False)
            self.offsets = [0] + [match.end() for match in re.finditer("\n", document)]
            self.edits = []

        def handle_starttag(self, tag, attrs):
            raw = self.get_starttag_text()
            updated = attribute.sub(replace, raw)
            if raw != updated:
                line, column = self.getpos()
                start = self.offsets[line - 1] + column
                self.edits.append((start, start + len(raw), updated))

        handle_startendtag = handle_starttag

    parser = LinkParser()
    parser.feed(document)
    parser.close()
    for start, end, value in reversed(parser.edits):
        document = document[:start] + value + document[end:]
    return document


def published_copy(relative):
    """從原教材重建發布副本；雜湊永遠對應實際送出的位元組。"""
    local = "_site/content/" + pub(relative)
    destination = os.path.join(ROOT, local)
    with open(os.path.join(ROOT, relative), encoding="utf-8") as source:
        document = rewrite_links(source.read())
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    with open(destination, "w", encoding="utf-8", newline="\n") as output:
        output.write(document)
    return {"local": local, "sha256": sha256(destination), "bytes": os.path.getsize(destination)}


def load_meta():
    """讀 09-external-research/*.meta.json，鍵 = 檔名（不含 .meta.json）"""
    metas = {}
    for p in glob.glob(os.path.join(ROOT, EXTERNAL, "*.meta.json")):
        key = os.path.basename(p)[: -len(".meta.json")]
        try:
            with open(p, encoding="utf-8") as f:
                metas[key] = json.load(f)
        except Exception as e:  # 壞掉的 meta 不應讓整個建置失敗
            print(f"warn: bad meta {p}: {e}", file=sys.stderr)
    return metas


def label_for(folder, name, meta):
    """側欄每一列顯示的 (代號, 描述)"""
    if folder == EXTERNAL:
        if meta:
            code = f'{meta.get("org", "")} {str(meta.get("published", ""))[:7]}'.strip()
            return code, meta.get("title_zh") or name
        if name.startswith("00-"):
            return "導論", "延伸研究導論與收錄清單"
    m = re.match(r"^(GTG-[\d-]+)-(.+)$", name)
    if m:
        return m.group(1), m.group(2).replace("-", " ")
    if re.match(r"^\d\d-", name):
        return "導論", re.sub(r"^\d\d-", "", name).replace("-", " ")
    if name.startswith("case"):
        return "Case", name.replace("-", " ")
    return "", name.replace("-", " ")


def title_from_markdown(path):
    """取教材第一個 H1 的可讀文字；側欄與搜尋共用繁中標題。"""
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            match = re.match(r"^#\s+(.+?)\s*#*\s*$", line)
            if match:
                title = re.sub(r"!?\[([^\]]+)\]\([^)]*\)", r"\1", match.group(1))
                title = re.sub(r"<[^>]+>", "", title)
                return html.unescape(re.sub(r"[*`~]", "", title)).strip()
    return ""


def sync_intro(metas):
    """把收錄清單表寫回導論頁的 LEDGER 區段，並重新轉出該頁 html"""
    if not os.path.exists(INTRO_MD):
        return
    rows = ["| 機構 | 發布 | 原文標題 | 教材 |", "|---|---|---|---|"]
    for m in sorted(metas.values(), key=lambda m: str(m.get("published", "")), reverse=True):
        org = m.get("org_zh") or m.get("org", "")
        if m.get("org_zh") and m.get("org"):
            org = f'{m["org_zh"]}（{m["org"]}）'
        title = m.get("title", "")
        link = f'[{title}]({m["url"]})' if m.get("url") else title
        rows.append(f'| {org} | {m.get("published", "")} | {link} | [{m.get("title_zh") or m["id"]}]({m["id"]}.html) |')
    table = "\n".join(rows) if metas else "（尚無收錄）"
    with open(INTRO_MD, encoding="utf-8") as f:
        text = f.read()
    new = re.sub(
        r"(<!-- LEDGER:START -->).*?(<!-- LEDGER:END -->)",
        lambda mm: f"{mm.group(1)}\n{table}\n{mm.group(2)}",
        text, count=1, flags=re.S,
    )
    if new != text:
        with open(INTRO_MD, "w", encoding="utf-8", newline="\n") as f:
            f.write(new)
    # 重新轉這一頁（沿用 build_html 的轉換器，樣式與其他教材一致）
    sys.path.insert(0, ROOT)
    import build_html  # noqa: E402
    rel = os.path.relpath(INTRO_MD, ROOT).replace("\\", "/")
    out = build_html.convert_one(INTRO_MD, rel)
    with open(INTRO_MD[:-3] + ".html", "w", encoding="utf-8", newline="\n") as f:
        f.write(out)


def collect():
    """走訪各模組，回傳 (側欄結構, 統計, 發布清單)"""
    metas = load_meta()
    nav, manifest = [], {}
    pages = mermaid = external_pages = 0
    last_update = None
    for folder, title in MODULES:
        d = os.path.join(ROOT, folder)
        if not os.path.isdir(d):
            continue
        items = []
        for md_name in sorted(os.listdir(d)):
            if not md_name.endswith(".md") or md_name.startswith("_"):
                continue
            if folder == "_shared" and md_name == "00-agent-brief.md":
                continue
            name = md_name[:-3]
            fn = name + ".html"
            full = os.path.join(d, fn)
            if not os.path.isfile(full):
                raise FileNotFoundError(f"尚未建置教材：{folder}/{fn}；請先執行 build_html.py")
            rel = f"{folder}/{fn}"
            manifest[pub(rel)] = published_copy(rel)
            with open(full, encoding="utf-8", errors="ignore") as f:
                mermaid += f.read().count('<pre class="mermaid">')
            pages += 1
            meta = metas.get(name) if folder == EXTERNAL else None
            code, desc = label_for(folder, name, meta)
            desc = title_from_markdown(os.path.join(d, md_name)) or desc
            items.append({"src": pub(rel), "code": code, "desc": desc, "name": name,
                          "sort": str((meta or {}).get("published", ""))})
            if meta:
                external_pages += 1
                a = meta.get("added") or meta.get("published")
                if a and (last_update is None or str(a) > last_update):
                    last_update = str(a)
        if folder == EXTERNAL:  # 導論在前，其餘依發布日期新到舊
            intro = [i for i in items if i["name"].startswith("00-")]
            rest = sorted([i for i in items if not i["name"].startswith("00-")],
                          key=lambda i: i["sort"], reverse=True)
            items = intro + rest
        if items:
            nav.append({"title": title, "items": items})
    idx = os.path.join(ROOT, "00-index.html")
    if os.path.isfile(os.path.join(ROOT, "00-index.md")) and os.path.isfile(idx):
        manifest["00-index.html"] = published_copy("00-index.html")
    figs = sorted(glob.glob(os.path.join(ROOT, "figures", "page-*.png")))
    # 圖片已 base64 內嵌於各教材 HTML；不再發布獨立 PNG（省發布容量、避免相對路徑在 Artifact iframe 失效）
    stats = {
        "pages": pages,
        "figures": len(figs) + mermaid,
        "external": external_pages,
        "last_update": last_update or datetime.date.today().isoformat(),
    }
    return nav, stats, manifest, metas


SHELL = r"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="繁體中文 AI 濫用威脅情報課程：逐案分析、跨案例專題與外部研究。">
<title>AI 濫用威脅情報</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>
:root{
  --bg:#e9edf3; --panel:#ffffff; --panel2:#f3f6fa; --fg:#151a24; --muted:#5a6377;
  --line:#d5dbe6; --accent:#b06d12; --accent-soft:#f3e3c9; --intel:#1c5793;
  --sev:#c0392b; --scroll:#c3cbd8;
  --sans:"IBM Plex Sans","Microsoft JhengHei","PingFang TC","Noto Sans TC",system-ui,sans-serif;
  --mono:"IBM Plex Mono","Cascadia Code",Consolas,monospace;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#0d1119; --panel:#141a24; --panel2:#1a212d; --fg:#e3e8f1; --muted:#8790a4;
  --line:#252d3b; --accent:#d69a3e; --accent-soft:#3a2f18; --intel:#5695d6;
  --sev:#e06a5c; --scroll:#2c3543;
}}
:root[data-theme="dark"]{
  --bg:#0d1119; --panel:#141a24; --panel2:#1a212d; --fg:#e3e8f1; --muted:#8790a4;
  --line:#252d3b; --accent:#d69a3e; --accent-soft:#3a2f18; --intel:#5695d6;
  --sev:#e06a5c; --scroll:#2c3543;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--sans);height:100vh;height:100dvh;overflow:hidden}
.app{display:flex;height:100vh;height:100dvh}
.sidebar{width:320px;flex-shrink:0;background:var(--panel);border-right:1px solid var(--line);
  display:flex;flex-direction:column;height:100vh;height:100dvh}
.brand{padding:18px 20px 14px;border-bottom:1px solid var(--line)}
.brand .kicker{font-family:var(--mono);font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--accent);font-weight:600}
.brand h1{margin:.35em 0 .15em;font-size:19px;font-weight:700;letter-spacing:-.01em;line-height:1.2}
.brand .sub{font-size:11.5px;color:var(--muted);line-height:1.5}
.brand .updated{font-family:var(--mono);font-size:10.5px;color:var(--muted);margin-top:8px}
.stats{display:flex;gap:0;margin-top:12px;border:1px solid var(--line);border-radius:7px;overflow:hidden}
.stats div{flex:1;padding:7px 2px;text-align:center;background:var(--panel2)}
.stats div+div{border-left:1px solid var(--line)}
.stats .n{font-family:var(--mono);font-size:14px;font-weight:600;color:var(--intel)}
.stats .l{font-size:9.5px;color:var(--muted);margin-top:1px}
.search{padding:12px 16px 8px}
.search input{width:100%;padding:8px 11px;border:1px solid var(--line);border-radius:7px;
  background:var(--panel2);color:var(--fg);font-family:var(--sans);font-size:13px;outline:none}
.search input:focus{border-color:var(--intel);box-shadow:0 0 0 3px color-mix(in srgb,var(--intel) 18%,transparent)}
.search-status{margin:6px 1px 0;font-size:11px;color:var(--muted)}
nav{flex:1;min-height:0;overflow-y:auto;padding:4px 10px 40px}
nav::-webkit-scrollbar{width:9px}nav::-webkit-scrollbar-thumb{background:var(--scroll);border-radius:5px;border:2px solid var(--panel)}
.mod{margin:10px 0 4px}
.mod-h{font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--muted);font-weight:600;padding:6px 8px 4px;position:sticky;top:0;background:var(--panel)}
nav a{display:block;text-decoration:none;color:var(--fg);font-size:12.5px;line-height:1.35;
  padding:6px 9px;border-radius:6px;border-left:2px solid transparent;transition:background .12s}
nav a .code{font-family:var(--mono);font-weight:600;color:var(--intel);font-size:11.5px}
nav a .desc{color:var(--muted);font-size:11px}
nav a:hover{background:var(--panel2)}
nav a.active{background:var(--accent-soft);border-left-color:var(--accent)}
nav a.active .code{color:var(--accent)}
nav a.hidden{display:none}
.home-link{margin:4px 0 12px;font-weight:600}
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
a:focus-visible,button:focus-visible{outline:2px solid var(--intel);outline-offset:2px}
.skip-link{position:fixed;left:12px;top:8px;z-index:40;padding:8px;background:var(--panel);color:var(--intel);transform:translateY(-160%)}
.skip-link:focus{transform:none}
.viewer-wrap{flex:1;display:flex;flex-direction:column;min-width:0}
.topbar{height:42px;flex-shrink:0;display:flex;align-items:center;gap:14px;padding:0 18px;
  background:var(--panel);border-bottom:1px solid var(--line)}
.topbar .now{font-family:var(--mono);font-size:12px;color:var(--fg);font-weight:500;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.topbar .hint{margin-left:auto;font-size:11px;color:var(--muted)}
.topbar .menu-btn{display:none;background:none;border:1px solid var(--line);border-radius:6px;
  color:var(--fg);font-size:16px;padding:2px 9px;cursor:pointer}
iframe{flex:1;width:100%;border:0;background:var(--bg)}
.scrim{display:none}
.drawer-close{display:none}
@media (max-width:760px){
  .sidebar{position:fixed;z-index:20;left:0;top:0;width:min(320px,88vw);visibility:hidden;transform:translateX(-100%);transition:transform .2s;box-shadow:0 0 40px rgba(0,0,0,.3)}
  .app.open .sidebar{visibility:visible}
  .app.open .sidebar{transform:translateX(0)}
  .app.open .scrim{display:block;position:fixed;inset:0;z-index:15;background:rgba(0,0,0,.4)}
  .topbar .menu-btn{display:block;min-width:44px;min-height:44px}
  .topbar{height:52px;gap:10px;padding:0 12px}
  .topbar .hint{display:none}
  .brand{padding-right:54px}
  .drawer-close{display:block;position:absolute;right:6px;top:6px;width:44px;height:44px;border:1px solid var(--line);border-radius:6px;background:var(--panel);color:var(--fg);font-size:24px;cursor:pointer}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style>
</head>
<body>
<a class="skip-link" href="#viewer" id="skip">跳至教材內容</a>
<div class="app" id="app">
  <aside class="sidebar" id="sidebar" aria-label="課程導覽">
    <button class="drawer-close" id="close-menu" type="button" aria-label="關閉教材導覽">×</button>
    <div class="brand">
      <div class="kicker">Threat Intelligence · 2026-09</div>
      <h1>AI 濫用威脅情報</h1>
      <div class="sub">Anthropic《Detecting and countering misuse of AI: September 2026》逐案課程教材，加上其他機構同類研究的延伸模組</div>
      <div class="stats">
        <div><div class="n">@@PAGES@@</div><div class="l">教材</div></div>
        <div><div class="n">@@FIGURES@@</div><div class="l">圖表</div></div>
        <div><div class="n">7+1</div><div class="l">危害領域</div></div>
        <div><div class="n">@@EXTERNAL@@</div><div class="l">延伸研究</div></div>
      </div>
      <div class="updated">最近更新 @@UPDATED@@</div>
    </div>
    <div class="search">
      <label class="sr-only" for="q">搜尋教材標題、GTG 代號、機構或模組</label>
      <input id="q" type="search" placeholder="搜尋中文主題、GTG 代號或機構…" autocomplete="off" aria-describedby="search-status">
      <p class="search-status" id="search-status" role="status" aria-live="polite"></p>
    </div>
    <nav id="nav" aria-label="教材清單">
      <a class="home-link" href="00-index.html" data-src="00-index.html" data-code="首頁" data-desc="課程總索引" data-module="課程總索引">⌂ 課程總索引</a>
@@NAV@@
    </nav>
  </aside>
  <div class="scrim" id="scrim"></div>
  <main class="viewer-wrap" id="main">
    <div class="topbar">
      <button class="menu-btn" id="menu" type="button" aria-label="開啟教材導覽" aria-expanded="false" aria-controls="sidebar">☰</button>
      <span class="now" id="now">課程總索引</span>
      <span class="hint">選擇教材 · 可分享目前章節網址</span>
    </div>
    <iframe id="viewer" name="viewer" title="教材內容：課程總索引" src="00-index.html" tabindex="0"></iframe>
  </main>
</div>

<script>
(function(){
  'use strict';
  var nav=document.getElementById('nav'), viewer=document.getElementById('viewer'),
      now=document.getElementById('now'), app=document.getElementById('app'),
      sidebar=document.getElementById('sidebar'), menu=document.getElementById('menu'),
      closeMenu=document.getElementById('close-menu'),
      main=document.getElementById('main'), search=document.getElementById('q'),
      status=document.getElementById('search-status'), mobile=matchMedia('(max-width:760px)'),
      siteRoot=new URL('./',location.href), links=Array.from(nav.querySelectorAll('a[data-src]')),
      allowed=new Map(), current='', attachedDocument=null;
  links.forEach(function(a){
    allowed.set(a.dataset.src,a);
    a.dataset.hay=(a.dataset.code+' '+a.dataset.desc+' '+a.dataset.module+' '+a.dataset.src).toLocaleLowerCase();
  });
  function setDrawer(open, restoreFocus){
    open=!!open && mobile.matches;
    app.classList.toggle('open',open);
    sidebar.inert=mobile.matches && !open;
    main.inert=open;
    menu.setAttribute('aria-expanded',String(open));
    menu.setAttribute('aria-label',open?'關閉教材導覽':'開啟教材導覽');
    if(open){search.focus();}
    else if(restoreFocus){menu.focus();}
  }
  function route(src, anchor){
    return allowed.has(src)?{src:src,anchor:anchor||''}:null;
  }
  function readHash(){
    var raw=location.hash.slice(1), split=raw.indexOf('#'), src=split<0?raw:raw.slice(0,split);
    try{src=decodeURIComponent(src);}catch(e){return null;}
    return route(src||'00-index.html',split<0?'':raw.slice(split+1));
  }
  function fromURL(href, base){
    var url;
    try{url=new URL(href,base);}catch(e){return null;}
    if(url.origin!==siteRoot.origin || !url.pathname.startsWith(siteRoot.pathname)){return null;}
    var src;
    try{src=decodeURIComponent(url.pathname.slice(siteRoot.pathname.length));}catch(e){return null;}
    if(src==='' || src==='index.html'){return route('00-index.html',url.hash.slice(1));}
    if(src.startsWith('_shared/')){src='shared/'+src.slice(8);}
    return route(src,url.hash.slice(1));
  }
  function encoded(r){
    return r.src.split('/').map(encodeURIComponent).join('/')+(r.anchor?'#'+r.anchor:'');
  }
  function show(r, historyMode){
    if(!r){r=route('00-index.html');historyMode='replace';}
    var a=allowed.get(r.src), target=encoded(r), wasOpen=app.classList.contains('open');
    links.forEach(function(link){
      var selected=link===a;
      link.classList.toggle('active',selected);
      if(selected){link.setAttribute('aria-current','page');}else{link.removeAttribute('aria-current');}
    });
    now.textContent=a.dataset.desc;
    viewer.title='教材內容：'+a.dataset.desc;
    document.title=a.dataset.desc+' · AI 濫用威脅情報';
    if(historyMode && location.hash!=='#'+target){
      history[historyMode==='push'?'pushState':'replaceState'](null,'','#'+target);
    }
    setDrawer(false,false);
    if(current!==target){
      current=target;
      // replace prevents the iframe from adding a second browser-history entry.
      try{viewer.contentWindow.location.replace(new URL(target,siteRoot).href);}
      catch(e){viewer.src=target;}
    }
    if(wasOpen){viewer.focus();}
  }
  function ordinaryClick(e,a){
    return a && !e.defaultPrevented && e.button===0 && !e.ctrlKey && !e.metaKey &&
      !e.shiftKey && !e.altKey && !a.hasAttribute('download') && a.target!=='_blank';
  }
  nav.addEventListener('click',function(e){
    var a=e.target.closest('a[data-src]');
    if(!ordinaryClick(e,a)){return;}
    e.preventDefault();show(route(a.dataset.src),'push');
  });
  function attachFrame(){
    var doc;
    try{doc=viewer.contentDocument;}catch(e){return;}
    if(!doc || doc===attachedDocument){return;}
    attachedDocument=doc;
    doc.addEventListener('click',function(e){
      var a=e.target.closest('a[href]');
      if(!ordinaryClick(e,a)){return;}
      var next=fromURL(a.getAttribute('href'),doc.baseURI);
      if(next){e.preventDefault();show(next,'push');}
    });
  }
  viewer.addEventListener('load',attachFrame);
  function filter(){
    var words=search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean), count=0;
    links.forEach(function(a){
      var matches=words.every(function(word){return a.dataset.hay.includes(word);});
      // Always keep a route back to the course index.
      a.classList.toggle('hidden',!matches && a.dataset.src!=='00-index.html');
      if(matches && a.dataset.src!=='00-index.html'){count++;}
    });
    nav.querySelectorAll('.mod').forEach(function(mod){mod.hidden=!mod.querySelector('a:not(.hidden)');});
    status.textContent=words.length?(count?'找到 '+count+' 份教材':'找不到符合的教材，請試試其他關鍵字。'):'';
  }
  search.addEventListener('input',filter);
  menu.addEventListener('click',function(){setDrawer(!app.classList.contains('open'),false);});
  closeMenu.addEventListener('click',function(){setDrawer(false,true);});
  document.getElementById('scrim').addEventListener('click',function(){setDrawer(false,true);});
  document.getElementById('skip').addEventListener('click',function(e){e.preventDefault();viewer.focus();});
  document.addEventListener('keydown',function(e){
    if(!app.classList.contains('open')){return;}
    if(e.key==='Escape'){e.preventDefault();setDrawer(false,true);return;}
    if(e.key==='Tab'){
      var focusable=[closeMenu,search].concat(links.filter(function(a){return !a.classList.contains('hidden');})),
          first=focusable[0],last=focusable[focusable.length-1];
      if(e.shiftKey && document.activeElement===first){e.preventDefault();last.focus();}
      else if(!e.shiftKey && document.activeElement===last){e.preventDefault();first.focus();}
    }
  });
  mobile.addEventListener('change',function(){setDrawer(false,sidebar.contains(document.activeElement) && mobile.matches);});
  window.addEventListener('popstate',function(){show(readHash(),null);});
  window.addEventListener('hashchange',function(){show(readHash(),null);});
  setDrawer(false,false);
  show(readHash(),'replace');
  attachFrame();
})();
</script>
</body></html>
"""


def render_nav(nav):
    out = []
    for mod in nav:
        out.append(f'<div class="mod"><div class="mod-h">{esc(mod["title"])}</div>')
        for it in mod["items"]:
            out.append(
                f'<a href="{esc(it["src"])}" data-src="{esc(it["src"])}" data-code="{esc(it["code"])}" '
                f'data-desc="{esc(it["desc"])}" data-module="{esc(mod["title"])}"><span class="code">{esc(it["code"])}</span> '
                f'<span class="desc">{esc(it["desc"])}</span></a>'
            )
        out.append("</div>")
    return "\n".join(out)


def main():
    metas = load_meta()
    sync_intro(metas)  # 先同步導論頁清單，再走訪（這樣導論 html 的雜湊才是最新的）
    nav, stats, manifest, metas = collect()
    os.makedirs(SITE, exist_ok=True)
    shell = (SHELL.replace("@@NAV@@", render_nav(nav))
             .replace("@@PAGES@@", str(stats["pages"]))
             .replace("@@FIGURES@@", str(stats["figures"]))
             .replace("@@EXTERNAL@@", str(stats["external"]))
             .replace("@@UPDATED@@", esc(stats["last_update"])))
    shell_path = os.path.join(SITE, "index.html")
    with open(shell_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(shell)
    manifest["index.html"] = {"local": "_site/index.html", "sha256": sha256(shell_path), "bytes": os.path.getsize(shell_path)}

    now = datetime.datetime.now().isoformat(timespec="seconds")
    with open(os.path.join(SITE, "publish-manifest.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"generated": now, "stats": stats, "files": manifest}, f, ensure_ascii=False, indent=1)

    state_path = os.path.join(SITE, "published-state.json")
    state = {}
    if os.path.exists(state_path):
        with open(state_path, encoding="utf-8") as f:
            state = json.load(f).get("files", {})
    if "--mark-published" in sys.argv:
        with open(state_path, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"published": now, "files": manifest}, f, ensure_ascii=False, indent=1)
        pending = {}
    else:
        pending = {k: v for k, v in manifest.items() if state.get(k, {}).get("sha256") != v["sha256"]}
    with open(os.path.join(SITE, "publish-pending.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"generated": now, "count": len(pending), "files": pending}, f, ensure_ascii=False, indent=1)

    print(f"shell: _site/index.html | pages {stats['pages']} | figures {stats['figures']} | "
          f"external {stats['external']} | last update {stats['last_update']}")
    print(f"manifest {len(manifest)} files | pending {len(pending)} files"
          + (" | marked as published" if "--mark-published" in sys.argv else ""))


if __name__ == "__main__":
    main()
