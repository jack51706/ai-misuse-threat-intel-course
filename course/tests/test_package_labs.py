from hashlib import sha256
import json
from pathlib import Path
import sys
import tempfile
import unittest
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from package_labs import package_labs, DOWNLOAD, ALLOWED_FILES
from build_pages import assemble


class LabPackageTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / "labs").mkdir()
        for name in ALLOWED_FILES:
            path = self.root / "labs" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("synthetic fixture\n")
        (self.root / "labs/README.md").write_text("Offline only\n")
        (self.root / "labs/run_labs.py").write_text("print('synthetic')\n")

    def test_reproducible_archive_excludes_cache_and_hidden_files(self):
        (self.root / "labs/.env").write_text("secret")
        (self.root / "labs/__pycache__").mkdir()
        (self.root / "labs/__pycache__/bad.py").write_text("excluded")
        first = package_labs(self.root)
        (self.root / "labs/README.md").write_bytes(b"Offline only\r\n")
        self.assertEqual(first, package_labs(self.root))
        with ZipFile(self.root / first["local"]) as archive:
            self.assertEqual(set(archive.namelist()), ALLOWED_FILES | {"SHA256SUMS.json"})
            for name, digest in json.loads(archive.read("SHA256SUMS.json")).items():
                self.assertEqual(sha256(archive.read(name)).hexdigest(), digest)

    def test_missing_entry_point_is_rejected(self):
        (self.root / "labs/run_labs.py").unlink()
        with self.assertRaises(ValueError):
            package_labs(self.root)

    def test_unknown_notes_and_reserved_manifest_are_rejected(self):
        for name in ("working-notes.csv", "SHA256SUMS.json", "stray.exe"):
            path = self.root / "labs" / name
            path.write_text("not approved")
            with self.assertRaises(ValueError):
                package_labs(self.root)
            path.unlink()

    def test_link_to_outside_labs_is_rejected(self):
        outside = self.root / "private.json"
        outside.write_text('{"fixture":"do not publish"}')
        try:
            (self.root / "labs/linked.json").symlink_to(outside)
        except OSError:
            self.skipTest("Host cannot create symlinks")
        with self.assertRaises(ValueError):
            package_labs(self.root)

    def test_pages_copies_only_named_archive_and_checks_digest(self):
        info = package_labs(self.root)
        (self.root / "00-index.html").write_text('<a href="downloads/course-labs.zip">Download</a>')
        (self.root / "_site/index.html").write_text("<p>Index</p>")
        files = {"index.html": {"local": "_site/index.html"},
                 "00-index.html": {"local": "00-index.html"}, DOWNLOAD: info}
        for entry in files.values():
            entry["sha256"] = sha256((self.root / entry["local"]).read_bytes()).hexdigest()
        manifest = self.root / "_site/publish-manifest.json"
        manifest.write_text(json.dumps({"files": files}))
        output = assemble(self.root)
        self.assertEqual((output / DOWNLOAD).read_bytes(), (self.root / info["local"]).read_bytes())
        (self.root / info["local"]).write_bytes(b"tampered")
        with self.assertRaises(ValueError):
            assemble(self.root)
        self.assertTrue((output / DOWNLOAD).is_file())


if __name__ == "__main__":
    unittest.main()
