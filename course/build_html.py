#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
把 course/ 下的所有 .md 教材轉成自包含 HTML：
- 內文的 ```mermaid 區塊用 mermaid.js（CDN）渲染成圖
- 每個教材自動嵌入它頁段對應的報告原圖（course/figures/page-XXX.png）
- 產生 index.html 導覽全部
用法：python build_html.py    （在 course/ 目錄下執行）
重跑安全：只讀 .md、只寫 .html，不改動任何 .md。
"""
import os, re, html, glob, base64
import markdown

ROOT = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(ROOT, "figures")
EMBED = os.environ.get("EMBED", "1") != "0"   # 預設把圖片內嵌成 base64（Artifact 用）；EMBED=0 可關

_b64cache = {}
def _b64(fn):
    if fn not in _b64cache:
        try:
            _b64cache[fn] = base64.b64encode(open(os.path.join(FIG_DIR, fn), "rb").read()).decode()
        except Exception:
            _b64cache[fn] = None
    return _b64cache[fn]

def embed_imgs(s):
    if not EMBED:
        return s
    def rep(m):
        d = _b64(m.group(1))
        return f'src="data:image/png;base64,{d}"' if d else m.group(0)
    return re.sub(r'src="\.\./figures/(page-\d+\.png)"', rep, s)

# figures/ 裡實際存在的頁碼
fig_pages = set()
for p in glob.glob(os.path.join(FIG_DIR, "page-*.png")):
    m = re.search(r"page-(\d+)\.png", os.path.basename(p))
    if m:
        fig_pages.add(int(m.group(1)))

# 每個教材檔名關鍵字 -> 一手 PDF 頁段（用來挑該案相關的報告原圖）
PAGE_RANGES = {
    "00-cyber-trends": [(4, 5), (38, 40)],
    "GTG-20006": [(5, 11)], "GTG-50014": [(11, 24)], "GTG-10007": [(24, 29)],
    "GTG-50021": [(28, 31)], "GTG-50020": [(30, 34)], "GTG-50029": [(34, 38)],
    "00-influence-intro": [(41, 44)], "GTG-04001": [(44, 47)], "GTG-54002": [(47, 53)],
    "GTG-84005": [(53, 58)], "GTG-24015": [(58, 62)], "GTG-34001": [(62, 67)],
    "GTG-54006": [(67, 70)], "GTG-84006": [(70, 75)], "GTG-54004": [(75, 78)],
    "GTG-84002": [(78, 81)],
    "00-surveillance-intro": [(81, 82)], "GTG-54009": [(82, 86)], "GTG-14010": [(86, 89)],
    "GTG-14020": [(89, 93)], "GTG-14021": [(93, 98)], "GTG-14022": [(98, 101)],
    "GTG-34007": [(101, 103)], "GTG-50027": [(103, 105)],
    "GTG-30004": [(105, 110)],
    "00-weapons-intro": [(111, 112)], "GTG-87001": [(112, 115)], "GTG-17001": [(115, 117)],
    "GTG-27005": [(117, 119)], "GTG-17002": [(119, 123)], "GTG-27006": [(123, 126)],
    "GTG-17003": [(126, 129)],
    "00-bio-intro": [(129, 131), (137, 138)], "case1": [(131, 133)], "case2": [(133, 135)],
    "case3": [(135, 136)], "case4-5": [(136, 137)],
    "GTG-15001": [(139, 142)],
    "00-distillation-intro": [(143, 147), (153, 154)], "GTG-16005": [(147, 148)],
    "GTG-16002": [(148, 149)], "GTG-16001": [(149, 150)], "GTG-16006": [(150, 151)],
    "GTG-16008": [(151, 152)], "GTG-16012": [(152, 153)],
}

def figs_for(fname):
    """回傳該教材該嵌入的報告原圖頁碼（頁段 ∩ figures 存在的頁）"""
    for key, ranges in PAGE_RANGES.items():
        if key in fname:
            pages = []
            for a, b in ranges:
                pages += [p for p in range(a, b + 1) if p in fig_pages]
            return sorted(set(pages))
    return []

CSS = """
:root{--fg:#1a1a1a;--bg:#fff;--muted:#666;--line:#e2e2e2;--link:#0b5cad;--code-bg:#f5f5f5;--accent:#0b5cad}
@media(prefers-color-scheme:dark){:root{--fg:#e6e6e6;--bg:#141414;--muted:#9a9a9a;--line:#333;--link:#6cb6ff;--code-bg:#1e1e1e;--accent:#6cb6ff}}
*{box-sizing:border-box}
body{max-width:900px;margin:0 auto;padding:2rem 1.2rem 6rem;font-family:"Segoe UI","Microsoft JhengHei","PingFang TC","Noto Sans TC",system-ui,sans-serif;line-height:1.75;color:var(--fg);background:var(--bg);font-size:16px}
h1,h2,h3,h4{line-height:1.3;margin-top:1.8em}
h1{font-size:1.7rem;border-bottom:2px solid var(--accent);padding-bottom:.3em}
h2{font-size:1.35rem;border-bottom:1px solid var(--line);padding-bottom:.2em}
h3{font-size:1.12rem}
a{color:var(--link)}
code{background:var(--code-bg);padding:.1em .35em;border-radius:4px;font-family:"Cascadia Code",Consolas,"Courier New",monospace;font-size:.9em}
pre{background:var(--code-bg);padding:1em;border-radius:8px;overflow-x:auto;font-size:.86em;line-height:1.5}
pre code{background:none;padding:0}
pre.mermaid{background:transparent;text-align:center}
table{border-collapse:collapse;width:100%;margin:1em 0;font-size:.92em;display:block;overflow-x:auto}
th,td{border:1px solid var(--line);padding:.5em .7em;text-align:left;vertical-align:top}
th{background:var(--code-bg)}
blockquote{border-left:4px solid var(--accent);margin:1em 0;padding:.4em 1em;color:var(--muted);background:var(--code-bg)}
img{max-width:100%;height:auto;border:1px solid var(--line);border-radius:6px;margin:.5em 0}
.figgallery{margin-top:2em;border-top:2px solid var(--accent);padding-top:1em}
.figgallery figure{margin:1.5em 0}
.figgallery figcaption{color:var(--muted);font-size:.9em;margin-top:.3em}
.topbar{position:sticky;top:0;background:var(--bg);border-bottom:1px solid var(--line);padding:.6em 0;margin:-2rem -1.2rem 1.5rem;padding-left:1.2rem;font-size:.9em}
.topbar a{text-decoration:none;margin-right:1em}
hr{border:none;border-top:1px solid var(--line);margin:2em 0}
"""

MERMAID_JS = """
<script src="https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"></script>
<script>
(function(){
  var dark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  if (window.mermaid) {
    mermaid.initialize({startOnLoad:true, theme: dark ? 'dark' : 'default', securityLevel:'loose', flowchart:{useMaxWidth:true}});
  }
})();
</script>
"""

def convert_one(md_path, rel_to_root):
    with open(md_path, encoding="utf-8") as f:
        text = f.read()

    # 1) 抽出 mermaid 區塊，換成 placeholder（避免 markdown 轉義破壞語法）
    blocks = []
    def stash(m):
        blocks.append(m.group(1))
        return f"\nMERMAIDPLACEHOLDER{len(blocks)-1}ENDPLACEHOLDER\n"
    text = re.sub(r"```mermaid\s*\n(.*?)```", stash, text, flags=re.DOTALL)

    # 1b) 圖片處理：把「引用圖檔：路徑」等文字說明轉成真圖、清掉裸路徑，並在首次提及各頁處插圖
    fname = os.path.basename(md_path)
    pages = figs_for(fname)
    placed = set()
    newlines = []
    for ln in text.split("\n"):
        # 已是 markdown 圖片：保留並標記該頁
        mimg = re.search(r"!\[[^\]]*\]\(\.\./figures/page-0*(\d+)\.png", ln)
        if mimg:
            placed.add(int(mimg.group(1)))
            newlines.append(ln)
            continue
        # 這行含裸露的圖檔路徑（inline code 或純文字）
        mp = re.search(r"\.\./figures/page-0*(\d+)\.png", ln)
        if mp:
            p = int(mp.group(1))
            # 表格行：路徑換成頁碼，保留表格結構，不插圖
            if ln.count("|") >= 2:
                newlines.append(re.sub(r"`?\.\./figures/page-0*(\d+)\.png`?", lambda m: "p."+str(int(m.group(1))), ln))
                continue
            c = re.sub(r"[（(]?\s*[，、]?\s*`?\.\./figures/page-\d+\.png`?\s*[）)]?", "", ln)  # 移除路徑（含緊貼標點/括號）
            c = re.sub(r"(\*\*)?\s*(課程)?(引用|對應)?圖[檔片][:：]\s*(\*\*)?", "", c)          # 移除「引用圖檔：」標籤
            c = re.sub(r"（\s*160\s*DPI\s*）", "", c)
            c = c.strip().lstrip("-*•　 ").rstrip("、,，．. 　（(")
            if p in pages and p not in placed:
                if len(c) < 4:   # 原本主要就是路徑說明
                    newlines.append(f"![報告原圖 · 第 {p} 頁（一手 PDF）](../figures/page-{p:03d}.png)")
                else:
                    newlines.append(c)
                    newlines.append(f"\n![報告原圖 · 第 {p} 頁（一手 PDF）](../figures/page-{p:03d}.png)\n")
                placed.add(p)
            else:
                if len(c) >= 4:   # 交叉引用他案圖或已插過：只留清理後文字，不插圖
                    newlines.append(c)
            continue
        # 一般行：以 p.XX / 第XX頁 錨定插圖（僅限本檔頁段有的頁）
        newlines.append(ln)
        if pages:
            for p in pages:
                if p in placed:
                    continue
                if re.search(rf"[pP]\.?\s*0*{p}\b|第\s*0*{p}\s*頁", ln):
                    newlines.append(f"\n![報告原圖 · 第 {p} 頁（一手 PDF）](../figures/page-{p:03d}.png)\n")
                    placed.add(p)
                    break
    text = "\n".join(newlines)

    # 2) markdown -> html
    body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "toc", "sane_lists", "attr_list", "nl2br"],
    )

    # 3) 換回 mermaid（純文字，交給 mermaid.js 渲染）
    def unstash(m):
        code = html.escape(blocks[int(m.group(1))])
        return f'<pre class="mermaid">{code}</pre>'
    body = re.sub(r"<p>MERMAIDPLACEHOLDER(\d+)ENDPLACEHOLDER</p>", unstash, body)
    body = re.sub(r"MERMAIDPLACEHOLDER(\d+)ENDPLACEHOLDER", unstash, body)

    # 3b) 清掉孤立的「引用圖檔：」標籤（其路徑已在 1b 清除或轉為圖片）
    body = re.sub(r'(<strong>)?\s*(課程)?(引用|對應)?圖[檔片][:：](</strong>)?\s*。?(?=\s*(<|$))', '', body)

    # 4) 文末補上「沒能在內文錨定」的報告原圖
    remaining = [p for p in pages if p not in placed]
    gallery = ""
    if remaining:
        items = "".join(
            f'<figure><img src="../figures/page-{p:03d}.png" alt="報告 p.{p}" loading="lazy">'
            f'<figcaption>報告原圖 · 第 {p} 頁</figcaption></figure>'
            for p in remaining
        )
        gallery = f'<div class="figgallery"><h2>報告原圖（未在內文對應者）</h2>{items}</div>'

    body = embed_imgs(body)
    gallery = embed_imgs(gallery)
    title = fname.replace(".md", "")
    depth = rel_to_root.count("/") + rel_to_root.count("\\")
    up = "../" * depth
    home = f'{up}index.html' if depth else 'index.html'
    topbar = f'<div class="topbar"><a href="{home}">◀ 課程索引</a></div>'

    return f"""<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<style>{CSS}</style></head>
<body>{topbar}{body}{gallery}{MERMAID_JS}</body></html>"""

def main():
    mds = []
    for dirpath, _, files in os.walk(ROOT):
        for fn in files:
            if fn.endswith(".md") and not fn.startswith("_"):
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, ROOT).replace("\\", "/")
                mds.append((full, rel))
    mds.sort(key=lambda x: x[1])

    made = []
    for full, rel in mds:
        htmlpath = full[:-3] + ".html"
        out = convert_one(full, rel)
        with open(htmlpath, "w", encoding="utf-8") as f:
            f.write(out)
        made.append(rel[:-3] + ".html")

    # index.html
    groups = {}
    for h in made:
        top = h.split("/")[0] if "/" in h else "（根目錄）"
        groups.setdefault(top, []).append(h)
    order = ["00-index.html", "_shared", "01-cyber", "02-influence", "03-surveillance",
             "04-weapons", "05-bio", "06-scams", "07-distillation", "08-capability-research"]
    def gkey(k):
        return order.index(k) if k in order else 99
    lines = ['<h1>課程教材索引（HTML 版）</h1>',
             '<p>此 HTML 版由 build_html.py 從 Markdown 自動產生：Mermaid 圖已渲染、報告原圖已內嵌。用瀏覽器開啟即可，無需任何擴充套件。</p>']
    for g in sorted(groups, key=gkey):
        lines.append(f'<h2>{html.escape(g)}</h2><ul>')
        for h in sorted(groups[g]):
            name = h.split("/")[-1].replace(".html", "")
            lines.append(f'<li><a href="{h}">{html.escape(name)}</a></li>')
        lines.append('</ul>')
    idx = f"""<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>課程索引</title><style>{CSS}</style></head>
<body>{''.join(lines)}</body></html>"""
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(idx)

    print(f"produced {len(made)} html files + index.html")
    print(f"figures available: {len(fig_pages)} pages")

if __name__ == "__main__":
    main()
