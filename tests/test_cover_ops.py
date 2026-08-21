from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageFont

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

    def test_typeset_records_exact_text_and_preserves_square_master(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            source = root / "source.png"
            output = root / "typeset.png"
            Image.new("RGB", (512, 512), (20, 90, 160)).save(source)
            font = ImageFont.load_default()
            font_bytes = getattr(font.path, "getvalue", lambda: None)()
            if not font_bytes:
                self.skipTest("Pillow does not expose its bundled test font")
            font_path = root / "test-font.ttf"
            font_path.write_bytes(font_bytes)
            result = self.run_cli(
                "typeset", str(source), "--output", str(output),
                "--text", "Exact Title", "--font", str(font_path),
                "--font-size", "48", "--x", "256", "--y", "180",
                "--align", "center", "--tracking", "2",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["typography"]["exact_text"], "Exact Title")
            self.assertEqual(payload["typography"]["align"], "center")
            self.assertEqual(payload["output"]["width"], 512)
            self.assertTrue(output.exists())


if __name__ == "__main__":
    unittest.main()
