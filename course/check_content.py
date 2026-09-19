"""離線檢查編輯紀錄、來源欄位與導讀範圍；不把通過等同事實已驗證。"""
from datetime import date
import argparse
import json
import re
from pathlib import Path
import sys

from build_html import iter_publishable_markdown, ROOT
from content_quality import content_digest, load_catalog, review_for


def check(root):
    root = Path(root)
    errors, pending = [], []
    catalog = load_catalog(root)
    sources = dict((rel, Path(path)) for path, rel in iter_publishable_markdown(root))
    for relative, entry in catalog["pages"].items():
        if relative not in sources:
            errors.append(f"{relative}: 審核紀錄無對應可發布教材")
        for field in ("checked_on", "source_checked_on"):
            if entry.get(field):
                try:
                    date.fromisoformat(entry[field])
                except (ValueError, TypeError):
                    errors.append(f"{relative}: {field} 必須是 YYYY-MM-DD")
        if entry.get("source_checked_on") and not entry.get("source_check_scope"):
            errors.append(f"{relative}: 來源核對日期必須附指定核對範圍")
        if not entry.get("scope") or not entry.get("pending"):
            errors.append(f"{relative}: 必須保留審核範圍與待驗證事項")
        if not re.fullmatch(r"[a-f0-9]{64}", entry.get("content_sha256", "")):
            errors.append(f"{relative}: 缺少審核版本雜湊")
    for relative, path in sources.items():
        text = path.read_text(encoding="utf-8")
        review = review_for(relative, text, catalog)
        if review["state"] == "pending":
            pending.append(relative)
        if relative.startswith("09-external-research/") and not path.name.startswith("00-"):
            metadata = path.with_suffix(".meta.json")
            if not metadata.exists():
                errors.append(f"{relative}: 缺少研究來源 metadata")
                continue
            try:
                meta = json.loads(metadata.read_text(encoding="utf-8"))
            except (ValueError, OSError) as exc:
                errors.append(f"{relative}: 無法讀取metadata: {exc}")
                continue
            if meta.get("id") != path.stem or not str(meta.get("url", "")).startswith("https://"):
                errors.append(f"{relative}: 來源 id/https URL 不完整")
            if meta.get("source_type") not in {"official-threat-report", "academic", "government", "industry"}:
                errors.append(f"{relative}: source_type 非標準分類")
    return errors, pending, len(sources)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(ROOT))
    parser.add_argument("--fingerprint", help="顯示指定教材的審核雜湊；不修改或批准紀錄")
    args = parser.parse_args(argv)
    if args.fingerprint:
        target = (args.root / args.fingerprint).resolve()
        if not target.is_relative_to(args.root.resolve()):
            parser.error("教材必須在 course 目錄內")
        print(content_digest(target.read_text(encoding="utf-8"), target.relative_to(args.root.resolve()).as_posix()))
        return 0
    errors, pending, total = check(args.root)
    print(f"Content checks: {'FAIL' if errors else 'PASS'} | lessons: {total} | pending editor review: {len(pending)}")
    for item in pending:
        print(f"PENDING (visible on page): {item}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
