"""可重現的離線實作下載包；僅打包 labs 內的教學文字與程式。"""
from hashlib import sha256
import json
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

DOWNLOAD = "downloads/course-labs.zip"
ALLOWED_FILES = frozenset({"run_labs.py", "README.md"} |
    {f"data/{case}/{name}" for case in ("gtg50014", "gtg14020", "gtg50020")
     for name in ("events.jsonl", "scenarios.json", "expected.json")} |
    {f"templates/{name}" for name in (
        "case-50014-response.md", "case-14020-response.md", "case-50020-response.md",
        "module-02-influence.csv", "module-04-governance.csv", "module-05-review.csv",
        "module-06-triage.csv", "module-07-dataflow.csv", "module-08-evaluation.csv",
        "module-09-comparison.csv", "evidence-ledger.csv", "rubric.csv")})


def package_labs(root):
    root = Path(root).resolve()
    source = root / "labs"
    if not source.is_dir():
        return None
    if source.is_symlink() or not source.resolve().is_relative_to(root):
        raise ValueError("labs 必須位於教材目錄內")
    entries = {}
    for path in sorted(source.rglob("*")):
        relative = path.relative_to(source)
        if any(part.startswith(".") or part == "__pycache__" for part in relative.parts):
            continue
        if path.is_symlink() or not path.resolve().is_relative_to(source.resolve()):
            raise ValueError(f"實作下載包不接受連結：{relative}")
        if path.is_file():
            if relative.as_posix() not in ALLOWED_FILES:
                raise ValueError(f"未核可的實作下載檔案：{relative}")
            # 統一換行，Windows 與 Linux 建置得到相同壓縮包。
            entries[relative.as_posix()] = path.read_text(encoding="utf-8").replace("\r\n", "\n").encode("utf-8")
    missing = ALLOWED_FILES - entries.keys()
    if missing:
        raise ValueError("實作下載包缺少必要檔案：" + ", ".join(sorted(missing)))
    manifest = {name: sha256(data).hexdigest() for name, data in entries.items()}
    entries["SHA256SUMS.json"] = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    target = root / "_site" / DOWNLOAD
    if not target.resolve().is_relative_to(root):
        raise ValueError("下載包輸出路徑超出教材目錄")
    target.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(target, "w", compression=ZIP_DEFLATED) as archive:
        for name, data in sorted(entries.items()):
            info = ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    return {"local": target.relative_to(root).as_posix(),
            "sha256": sha256(target.read_bytes()).hexdigest(), "bytes": target.stat().st_size}
