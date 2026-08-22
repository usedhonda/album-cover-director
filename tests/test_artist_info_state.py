from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIST_RESOLVER = ROOT / "skills/album-cover-director/scripts/artist-info-state.py"
WORKSPACE = ROOT / "skills/album-cover-director/scripts/project-workspace.py"


class ProjectLocalArtistInfoTest(unittest.TestCase):
    def run_cli(self, script: Path, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(script), *args], check=False, text=True, capture_output=True
        )

    def test_project_local_artist_system_is_scoped_to_project(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            project = root / "project"
            project.mkdir()
            local_artist = project / ".album-cover-director/artist-system.md"
            local_artist.parent.mkdir()
            local_artist.write_text("private artist information", encoding="utf-8")

            resolved = self.run_cli(ARTIST_RESOLVER, "resolve", "--project-root", str(project))
            self.assertEqual(resolved.returncode, 0, resolved.stderr)
            self.assertEqual(json.loads(resolved.stdout), {
                "source": "project-local", "path": str(local_artist.resolve()), "reason": None,
            })
            self.assertFalse((root / "codex-home").exists())

            ignored = self.run_cli(
                ARTIST_RESOLVER, "resolve", "--project-root", str(project), "--ignore-project-local"
            )
            self.assertEqual(json.loads(ignored.stdout)["reason"], "project-local-ignored")

    def test_explicit_artist_system_wins_without_global_memory(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            project = root / "project"
            project.mkdir()
            explicit_artist = root / "artist.md"
            explicit_artist.write_text("private explicit artist information", encoding="utf-8")

            result = self.run_cli(
                ARTIST_RESOLVER, "resolve", "--project-root", str(project),
                "--artist-system", str(explicit_artist),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout), {
                "source": "explicit", "path": str(explicit_artist.resolve()), "reason": None,
            })
            self.assertFalse((project / ".album-cover-director/state.yaml").exists())

    def test_unreadable_explicit_path_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            project = Path(raw) / "project"
            project.mkdir()
            result = self.run_cli(
                ARTIST_RESOLVER, "resolve", "--project-root", str(project),
                "--artist-system", str(project / "missing.md"),
            )
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)["reason"], "explicit-path-unreadable")

    def test_workspace_init_creates_private_learning_surface(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            project = Path(raw) / "project"
            project.mkdir()
            result = self.run_cli(WORKSPACE, "init", "--project-root", str(project))
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            local = project / ".album-cover-director"
            self.assertEqual(payload["status"], "initialized")
            self.assertEqual((local / ".gitignore").read_text(encoding="utf-8"), "*\n!.gitignore\n")
            for relative in (
                "artist-system.md", "learned-preferences.md", "feedback/README.md",
                "learning-images", "reference-inbox", "observations", "benchmarks/title-integrity-v1.yaml",
            ):
                self.assertTrue((local / relative).exists(), relative)


if __name__ == "__main__":
    unittest.main()
