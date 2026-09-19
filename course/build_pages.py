#!/usr/bin/env python
"""從發布清單組裝 GitHub Pages 到 _pages/，保留 _site/ 的 Artifact 狀態。

Pages 請設 EMBED=0，再依序執行 build_html.py、build_site.py、本檔與
validate_site.py。只發布清單上的 HTML 和 HTML 實際引用的本機圖片。
"""
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
import tempfile
from urllib.parse import unquote, urlsplit
from build_site import rewrite_links

ROOT = Path(__file__).resolve().parent


def contained(root, relative):
    """拒絕發布清單/HTML 指向工作目錄之外（含 symlink）。"""
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f"路徑超出教材目錄：{relative}")
    return path


class ImageSources(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sources = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            src = dict(attrs).get("src")
            if src:
                self.sources.append(src)


def assemble(root=ROOT):
    root = Path(root).resolve()
    output = root / "_pages"
    if output.is_symlink() or output.resolve() != root / "_pages":
        raise ValueError("_pages 必須是教材目錄內的實體建置目錄")
    manifest = json.loads((root / "_site/publish-manifest.json").read_text(encoding="utf-8"))["files"]
    if "index.html" not in manifest or "00-index.html" not in manifest:
        raise ValueError("發布清單缺少首頁或總索引，請先執行 build_site.py")

    # 先完成暫存複製；缺檔或非法路徑時保留上次成功產物。
    with tempfile.TemporaryDirectory(prefix=".pages-build-", dir=root) as temporary:
        stage = Path(temporary)
        images = set()
        for published, info in manifest.items():
            target = contained(stage, published)
            source = contained(root, info["local"])
            if target.suffix != ".html" or source.suffix != ".html":
                raise ValueError(f"發布清單不是 HTML：{published}")
            document = rewrite_links(source.read_text(encoding="utf-8"))
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(document, encoding="utf-8", newline="\n")
            parser = ImageSources()
            parser.feed(document)
            for value in parser.sources:
                url = urlsplit(value)
                if url.scheme or url.netloc:
                    continue
                if url.path.startswith("/"):
                    raise ValueError(f"圖片必須使用相對路徑：{value}")
                asset = contained(stage, target.parent.relative_to(stage) / unquote(url.path))
                relative = asset.relative_to(stage)
                if not re.fullmatch(r"figures/page-\d+\.png", relative.as_posix()):
                    raise ValueError(f"非報告圖片路徑：{value}")
                images.add(relative)
        for relative in sorted(images):
            source = contained(root, relative)
            target = stage / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        (stage / ".nojekyll").touch()
        # output 由固定 ROOT/_pages 推導，上方已驗證絕對位置與 symlink。
        if output.exists():
            shutil.rmtree(output)
        shutil.copytree(stage, output)
    size = sum(p.stat().st_size for p in output.rglob("*") if p.is_file())
    print(f"Pages 組裝完成：_pages/，{len(manifest)} 份 HTML、{len(images)} 張圖片、{size:,} bytes")
    return output


if __name__ == "__main__":
    assemble()
