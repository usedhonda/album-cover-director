import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "album-cover-director"


def command(script, *arguments):
    return subprocess.run([sys.executable, str(SKILL / "scripts" / script), *arguments], text=True, capture_output=True, check=False)


def contract():
    return {
        "release": {"exact_title": "Moon Signal", "allowed_readable_text": ["Moon Signal"]},
        "constraints": {"title_must_be_image_native": True, "post_typesetting_allowed": False},
        "rights": {"reference_basis": "original brief"},
        "runtime": {"model_or_tool": "gpt-image-2"},
        "directions": [
            {"id": "A", "primary_pattern": "material", "title_system_family": "material-world", "world_engine": "ice", "title_anatomy": "frozen letters"},
            {"id": "B", "primary_pattern": "spatial", "title_system_family": "spatial-field", "world_engine": "light field"},
            {"id": "C", "primary_pattern": "character", "title_system_family": "character-led", "character_title_relation": "garment seam"},
        ],
        "candidates": [{"id": "A1", "direction_id": "A", "operation": "initial", "output_path": ""}],
    }


class ProductionContractTests(unittest.TestCase):
    def test_prompt_preflight_accepts_complete_contract_and_rejects_duplicate_pattern(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "contract.json"; path.write_text(json.dumps(contract()))
            passed = command("prompt-preflight.py", "--contract", str(path)); self.assertEqual(passed.returncode, 0, passed.stderr)
            invalid = contract(); invalid["directions"][1]["primary_pattern"] = "material"; path.write_text(json.dumps(invalid))
            failed = command("prompt-preflight.py", "--contract", str(path)); self.assertEqual(failed.returncode, 2); self.assertIn("primary-pattern-duplicate", failed.stdout)

    def test_router_protects_title_architecture_and_refinement_budget(self):
        title = command("action-router.py", "--failure-code", "title-integrity", "--cycles-used", "3")
        self.assertEqual(json.loads(title.stdout)["action"], "rebuild-title-architecture")
        budget = command("action-router.py", "--failure-code", "thumbnail-collapse", "--cycles-used", "2")
        self.assertEqual(json.loads(budget.stdout)["action"], "promote-runner-up")

    def test_image_preflight_and_similarity_are_objective_only(self):
        with tempfile.TemporaryDirectory() as directory:
            image = Path(directory) / "cover.png"; Image.new("RGB", (3000, 3000), "black").save(image)
            checked = command("cover-ops.py", "preflight", str(image), "--expected-title", "Moon Signal")
            self.assertEqual(checked.returncode, 0); self.assertIn("human_required", checked.stdout)
            duplicate = Path(directory) / "duplicate.png"; duplicate.write_bytes(image.read_bytes())
            comparison = command("cover-ops.py", "compare", str(image), str(duplicate))
            self.assertEqual(comparison.returncode, 0); self.assertIn('"warning": true', comparison.stdout)


if __name__ == "__main__":
    unittest.main()
