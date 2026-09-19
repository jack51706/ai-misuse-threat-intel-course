#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Read-only checks for the assembled GitHub Pages site; never fetch any URL.

    python course/validate_site.py
    python course/validate_site.py --site course/_pages
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
import posixpath
import sys
from urllib.parse import unquote, urlsplit


DEFAULT_SITE = Path(__file__).resolve().parent / "_pages"
HTML_SUFFIXES = {".html", ".htm"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".svg", ".ico"}
SOURCE_SUFFIXES = {".md", ".markdown", ".py", ".pyc", ".pyo", ".ipynb", ".toml",
                   ".yaml", ".yml", ".ts", ".tsx", ".jsx", ".map", ".sh", ".ps1"}
PRIVATE_NAMES = {"publish-manifest.json", "publish-pending.json", "published-state.json"}
PRIVATE_DIRECTORIES = {"_shared", "_site", "__pycache__", ".git", ".github", "tests"}


@dataclass
class Reference:
    attribute: str
    value: str
    line: int


class Document(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[Reference] = []
        self.anchors: set[str] = set()
        self.starts: set[str] = set()
        self.ends: set[str] = set()
        self.doctype = False
        self.lang = False
        self.charset = False
        self.viewport = False
        self.has_base = False
        self.images = 0

    def handle_decl(self, decl: str) -> None:
        if decl.lower() == "doctype html":
            self.doctype = True

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        self.starts.add(tag)
        if values.get("id"):
            self.anchors.add(values["id"])
        if tag == "a" and values.get("name"):
            self.anchors.add(values["name"])
        if tag == "html":
            self.lang = bool((values.get("lang") or "").strip())
        if tag == "meta":
            self.charset |= (values.get("charset") or "").lower() in {"utf-8", "utf8"}
            self.viewport |= ((values.get("name") or "").lower() == "viewport"
                              and "width=device-width" in (values.get("content") or "").replace(" ", "").lower())
        if tag == "base" and "href" in values:
            self.has_base = True
        if tag == "img":
            self.images += 1
        for attribute in ("href", "src"):
            if values.get(attribute) is not None:
                self.references.append(Reference(attribute, values[attribute], self.getpos()[0]))

    def handle_endtag(self, tag: str) -> None:
        self.ends.add(tag)


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    html_count: int = 0
    references: int = 0
    images: int = 0
    image_files: int = 0
    total_bytes: int = 0

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_site(site: Path, base_path: str = "/") -> ValidationResult:
    """Check local references against an exact-case file inventory within ``site``.

    Root-relative URLs may include ``base_path`` (e.g. a GitHub project name).
    Relative ``..`` segments are allowed only while they remain inside the site.
    """
    result = ValidationResult()
    root = Path(site).resolve()
    if not root.is_dir():
        result.errors.append(f"Site directory does not exist: {root}")
        return result

    files: dict[str, Path] = {}
    for path in sorted(root.rglob("*")):
        name = path.relative_to(root).as_posix()
        if path.is_symlink():
            result.errors.append(f"{name}: symbolic links must not be deployed")
            continue
        if not path.is_file():
            continue
        if not path.resolve().is_relative_to(root):
            result.errors.append(f"{name}: file escapes the site directory")
            continue
        files[name] = path
        result.total_bytes += path.stat().st_size
        result.image_files += path.suffix.lower() in IMAGE_SUFFIXES
        if (path.suffix.lower() in SOURCE_SUFFIXES or path.name in PRIVATE_NAMES
                or path.name.endswith(".meta.json")
                or any(part in PRIVATE_DIRECTORIES for part in PurePosixPath(name).parts)):
            result.errors.append(f"{name}: source or build-state file must not be deployed (_shared must map to shared)")

    if "index.html" not in files:
        result.errors.append("index.html: site entry point is missing")

    documents: dict[str, Document] = {}
    for name, path in files.items():
        if path.suffix.lower() not in HTML_SUFFIXES:
            continue
        result.html_count += 1
        document = Document()
        try:
            document.feed(path.read_text(encoding="utf-8-sig"))
            document.close()
        except (OSError, UnicodeError) as exc:
            result.errors.append(f"{name}: cannot read UTF-8 HTML: {exc}")
            continue
        documents[name] = document
        result.images += document.images
        result.references += len(document.references)
        requirements = {
            "HTML5 doctype": document.doctype,
            "html/head/body opening and closing tags": {"html", "head", "body"} <= document.starts & document.ends,
            "html lang": document.lang,
            "UTF-8 charset": document.charset,
            "responsive viewport": document.viewport,
        }
        for requirement, present in requirements.items():
            if not present:
                result.errors.append(f"{name}: missing {requirement}")
        if document.has_base:
            result.errors.append(f"{name}: base href is unsupported; use explicit site-relative links")

    prefix = "/" + base_path.strip("/") + "/" if base_path.strip("/") else "/"

    def resolve_local(source: str, raw_path: str) -> str:
        path = unquote(raw_path)
        if "\\" in path or ":" in path or "\0" in path:
            raise ValueError("invalid or unsafe local path")
        if not path:
            return source
        if path.startswith("/"):
            if prefix != "/" and path.startswith(prefix):
                path = path[len(prefix):]
            else:
                path = path.lstrip("/")
        else:
            path = posixpath.join(posixpath.dirname(source), path)
        path = posixpath.normpath(path)
        if path == ".." or path.startswith("../"):
            raise ValueError("local path escapes the site directory")
        if "_shared" in PurePosixPath(path).parts:
            raise ValueError("_shared URL must map to shared")
        # Directory URLs follow the same index.html convention as GitHub Pages.
        if path == ".":
            path = "index.html"
        elif path not in files and any(name.startswith(path + "/") for name in files):
            path += "/index.html"
        return path

    def check_reference(source: str, reference: Reference) -> None:
        label = f"{source}:{reference.line}: {reference.attribute}={reference.value!r}"
        try:
            url = urlsplit(reference.value.strip())
            if url.scheme or url.netloc:
                # This branch does not resolve hosts or make any network request.
                if url.scheme.lower() in {"file", "javascript", "vbscript"}:
                    raise ValueError("unsafe URL scheme")
                return
            target = resolve_local(source, url.path)
            fragment = unquote(url.fragment)
            if target == "index.html" and fragment:
                route_path, separator, route_fragment = fragment.partition("#")
                route = urlsplit(route_path)
                if PurePosixPath(route.path).suffix.lower() in HTML_SUFFIXES:
                    if route.scheme or route.netloc:
                        raise ValueError("shell route must reference a local page")
                    target = resolve_local(target, route.path)
                    fragment = unquote(route_fragment) if separator else ""
            if target not in files:
                raise ValueError(f"missing local file: {target} (paths are case-sensitive)")
            anchor = fragment.split(":~:", 1)[0]
            if (anchor and anchor.lower() != "top" and target in documents
                    and anchor not in documents[target].anchors):
                raise ValueError(f"missing anchor #{anchor} in {target}")
        except ValueError as exc:
            result.errors.append(f"{label}: {exc}")

    for name, document in documents.items():
        for reference in document.references:
            check_reference(name, reference)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, default=DEFAULT_SITE, help="assembled site directory")
    parser.add_argument("--base-path", default="/", help="optional root URL prefix, e.g. /ai-misuse-threat-intel-course/")
    args = parser.parse_args(argv)
    result = validate_site(args.site, args.base_path)
    print(f"Site validation: {'PASS' if result.ok else 'FAIL'} | HTML: {result.html_count} | "
          f"href/src: {result.references} | images: {result.images} "
          f"({result.image_files} files) | bytes: {result.total_bytes:,}")
    for error in result.errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
