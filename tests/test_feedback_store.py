from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/album-cover-director/scripts/feedback-store.py"


class FeedbackStoreTest(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args], check=False, text=True, capture_output=True
        )

    def test_feedback_keeps_images_and_promotes_repeated_preference(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "artist"
            root.mkdir()
            image = Path(raw) / "candidate.png"
            image.write_bytes(b"candidate")
            for slug in ("first", "second", "third"):
                result = self.run_cli(
                    "record", "--artist-root", str(root), "--release-slug", slug,
                    "--observation", "Cooler palette feels more specific.",
                    "--preference-key", "cooler-palette",
                    "--preference-statement", "Prefer a cool palette over an unmotivated warm cast.",
                    "--applies-when", "the song does not call for warmth",
                    "--reject-when", "warm light is musically motivated",
                    "--image", str(image),
                    "--user-validated",
                )
                self.assertEqual(result.returncode, 0, result.stderr)

            feedback = root / ".album-cover-director/feedback"
            for slug in ("first", "second", "third"):
                record = feedback / slug / "feedback.json"
                payload = json.loads(record.read_text(encoding="utf-8"))
                self.assertEqual(payload["release_slug"], slug)
                self.assertTrue((feedback / slug / "images/01-candidate.png").is_file())
            summary = (feedback / "learned-preferences.md").read_text(encoding="utf-8")
            self.assertIn("Prefer a cool palette", summary)
            self.assertIn("first, second, third", summary)

    def test_invalid_slug_does_not_write_outside_feedback(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "artist"
            root.mkdir()
            result = self.run_cli("record", "--artist-root", str(root), "--release-slug", "../escape")
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)["reason"], "release-slug-invalid")
            self.assertFalse((root / "escape").exists())


if __name__ == "__main__":
    unittest.main()
