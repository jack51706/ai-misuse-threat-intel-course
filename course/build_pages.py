#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
把課程站台組裝成 GitHub Pages 可直接部署的目錄（course/_site/）。

先跑 build_html.py（各 .md -> .html，圖已 base64 內嵌）與 build_site.py（產生殼頁
_site/index.html），再跑本檔把散在各模組的 .html 收攏進 _site/，並套用與 Artifact
相同的 `_shared/ -> shared/` 對映，最後放一個 .nojekyll（GitHub Pages 不要跑 Jekyll，
否則底線開頭的檔案/目錄會被忽略）。

  cd course
  python build_html.py && python build_site.py && python build_pages.py
  # 之後 _site/ 就是完整可部署的站台（GitHub Actions 會上傳它）

重跑安全：只寫入 _site/。
"""
import os, glob, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "_site")

MODULES = [
    "01-cyber", "02-influence", "03-surveillance", "04-weapons",
    "05-bio", "06-scams", "07-distillation", "08-capability-research",
    "09-external-research",
]


def copy_html(src_dir, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    n = 0
    for h in glob.glob(os.path.join(src_dir, "*.html")):
        shutil.copy2(h, os.path.join(dst_dir, os.path.basename(h)))
        n += 1
    return n


def main():
    if not os.path.exists(os.path.join(SITE, "index.html")):
        raise SystemExit("找不到 _site/index.html，請先跑 build_site.py")

    total = 0

    # 總索引頁
    idx = os.path.join(ROOT, "00-index.html")
    if os.path.exists(idx):
        shutil.copy2(idx, os.path.join(SITE, "00-index.html"))
        total += 1

    # 八＋一個模組
    for m in MODULES:
        src = os.path.join(ROOT, m)
        if os.path.isdir(src):
            total += copy_html(src, os.path.join(SITE, m))

    # _shared -> shared（與 build_site.py 的發布對映一致，殼頁 nav 指向 shared/）
    total += copy_html(os.path.join(ROOT, "_shared"), os.path.join(SITE, "shared"))

    # 報告原圖：圖已 base64 內嵌，理論上用不到；仍複製一份當安全網（相對路徑 ../figures/ 可解析）
    figs_src = os.path.join(ROOT, "figures")
    if os.path.isdir(figs_src):
        figs_dst = os.path.join(SITE, "figures")
        os.makedirs(figs_dst, exist_ok=True)
        for p in glob.glob(os.path.join(figs_src, "*.png")):
            shutil.copy2(p, os.path.join(figs_dst, os.path.basename(p)))

    # 關掉 Jekyll，避免底線開頭的路徑被忽略、確保原樣送出
    open(os.path.join(SITE, ".nojekyll"), "w").close()

    # 這幾個是建置中繼檔，不需要對外服務（留著無害，這裡順手移除保持乾淨）
    for junk in ("publish-manifest.json", "publish-pending.json"):
        p = os.path.join(SITE, junk)
        if os.path.exists(p):
            os.remove(p)

    htmls = len(glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True))
    print(f"Pages 站台組裝完成 -> _site/（教材 html 收攏 {total} 份，_site 內 html 共 {htmls} 份）")


if __name__ == "__main__":
    main()
