from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/album-cover-director/scripts/contribution-draft.py"


class ContributionDraftTest(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args], check=False, text=True, capture_output=True
        )

    def valid_args(self, root: Path) -> list[str]:
        return [
            "prepare", "--artist-root", str(root), "--release-slug", "private-release",
            "--card-id", "material-governs-skeleton",
            "--title-behavior", "Material governs title anatomy",
            "--title-system-family", "material-world",
            "--world-engine", "A physical process makes each join necessary",
            "--use-when", "A coherent physical process exists",
            "--do-not-use-when", "Material is only decorative texture",
            "--construction-logic", "Map routes to skeleton and counters",
            "--occupied-area", "Most of the square",
            "--silhouette", "One continuous constructed word shape",
            "--reading-route", "Follow the physical route from left to right",
            "--value-priority", "Title is the highest-contrast structure",
            "--prompt-requirement", "Make joins and counters material-dependent",
            "--rejection-test", "Remove material and the letter anatomy must collapse",
            "--private-trial-count", "3",
            "--condition-category", "short Latin title",
            "--condition-category", "mixed-script title",
            "--held-out-brief-passed", "--rights-safe",
        ]

    def test_prepare_keeps_public_draft_abstract_and_local(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "artist"
            root.mkdir()
            private_feedback = root / ".album-cover-director/feedback/private-release/feedback.json"
            private_feedback.parent.mkdir(parents=True)
            private_feedback.write_text('{"user_observations": ["Private Title"]}', encoding="utf-8")

            result = self.run_cli(*self.valid_args(root))
            self.assertEqual(result.returncode, 0, result.stderr)
            output = json.loads(result.stdout)
            draft = Path(output["draft_dir"])
            self.assertEqual(output["network_action"], "none")
            self.assertEqual({path.name for path in draft.iterdir()}, {"title-behavior-card.yaml", "README.md"})
            card_text = (draft / "title-behavior-card.yaml").read_text(encoding="utf-8")
            self.assertNotIn("Private Title", card_text)
            self.assertNotIn("private-release", card_text)

            validated = self.run_cli("validate", "--draft-dir", str(draft))
            self.assertEqual(validated.returncode, 0, validated.stderr)
            self.assertEqual(json.loads(validated.stdout)["status"], "valid")

    def test_rejects_image_or_path_reference_in_public_card(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "artist"
            root.mkdir()
            args = self.valid_args(root)
            index = args.index("Material governs title anatomy")
            args[index] = "Use /" + "Users" + "/private/cover.png as the title texture"
            result = self.run_cli(*args)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)["reason"], "title-behavior-contains-private-or-image-reference")
            self.assertFalse((root / ".album-cover-director").exists())


if __name__ == "__main__":
    unittest.main()
