from __future__ import annotations

import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/album-cover-director/scripts/artist-info-state.py"


class ArtistInfoStateTest(unittest.TestCase):
    def run_cli(self, codex_home: Path, *args: str) -> subprocess.CompletedProcess:
        environment = os.environ.copy()
        environment["CODEX_HOME"] = str(codex_home)
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            check=False,
            text=True,
            capture_output=True,
            env=environment,
        )

    def test_remembers_only_last_readable_path(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            codex_home = root / "codex-home"
            artist_info = root / "artist.md"
            artist_info.write_text("private artist information", encoding="utf-8")

            explicit = self.run_cli(codex_home, "resolve", "--path", str(artist_info))
            self.assertEqual(explicit.returncode, 0, explicit.stderr)
            self.assertEqual(json.loads(explicit.stdout)["source"], "explicit")

            state = codex_home / "album-cover-director" / "state.yaml"
            payload = json.loads(state.read_text(encoding="utf-8"))
            self.assertEqual(payload, {"last_artist_information_path": str(artist_info.resolve())})
            self.assertEqual(stat.S_IMODE(state.stat().st_mode), 0o600)
            self.assertNotIn("private artist information", state.read_text(encoding="utf-8"))

            remembered = self.run_cli(codex_home, "resolve")
            self.assertEqual(remembered.returncode, 0, remembered.stderr)
            self.assertEqual(json.loads(remembered.stdout)["source"], "remembered")

            ignored = self.run_cli(codex_home, "resolve", "--ignore-remembered")
            self.assertEqual(json.loads(ignored.stdout)["reason"], "remembered-path-ignored")

            forgotten = self.run_cli(codex_home, "forget")
            self.assertEqual(forgotten.returncode, 0, forgotten.stderr)
            self.assertFalse(state.exists())

    def test_unreadable_explicit_path_is_not_persisted(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            codex_home = Path(raw) / "codex-home"
            result = self.run_cli(codex_home, "resolve", "--path", str(Path(raw) / "missing.md"))
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)["reason"], "explicit-path-unreadable")
            self.assertFalse((codex_home / "album-cover-director" / "state.yaml").exists())


if __name__ == "__main__":
    unittest.main()
