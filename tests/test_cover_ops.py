from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/cover-ops.py"


class CoverOpsTest(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            check=False,
            text=True,
            capture_output=True,
        )

    def test_inspect_and_export_square(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            source = root / "source.png"
            Image.new("RGB", (512, 512), (20, 90, 160)).save(source)
            inspected = self.run_cli("inspect", str(source))
            self.assertEqual(inspected.returncode, 0, inspected.stderr)
            record = json.loads(inspected.stdout)[0]
            self.assertTrue(record["square"])
            self.assertEqual(record["width"], 512)

            exported = self.run_cli("export", str(source), "--out-dir", str(root / "delivery"), "--size", "3000")
            self.assertEqual(exported.returncode, 0, exported.stderr)
            payload = json.loads(exported.stdout)
            self.assertEqual([item["width"] for item in payload["outputs"]], [3000, 3000, 256])

    def test_contact_sheet_and_non_square_gate(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            square = root / "square.png"
            wide = root / "wide.png"
            Image.new("RGB", (400, 400), (200, 30, 50)).save(square)
            Image.new("RGB", (500, 400), (30, 200, 50)).save(wide)
            sheet = self.run_cli("contact-sheet", str(square), str(wide), "--output", str(root / "sheet.png"))
            self.assertEqual(sheet.returncode, 0, sheet.stderr)
            self.assertTrue((root / "sheet.png").exists())
            rejected = self.run_cli("export", str(wide), "--out-dir", str(root / "bad"))
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("must be square", rejected.stderr)


if __name__ == "__main__":
    unittest.main()
