import json
import subprocess
import sys
import tempfile
import unittest
import shutil
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
        "runtime": {"model_family": "gpt-image", "model_id": "gpt-image-2", "host_surface": "test", "skill_version": "test", "capability_profile": {"source_minimum_dimension": 2048}},
        "directions": [
            {"id": "A", "primary_pattern": "Abstract Material / Process", "title_system_family": "material-world", "title_system": "ice", "prompt_path": "a.md", "world_engine": "ice", "material_vocabulary": "frost", "title_anatomy": "frozen letters", "world_role": "signal"},
            {"id": "B", "primary_pattern": "Minimal Geometry / Color Field", "title_system_family": "spatial-field", "title_system": "light", "prompt_path": "b.md", "causal_phenomenon": "light field", "hierarchy_lock": "center", "title_skeleton": "beam", "spatial_extension": "air"},
            {"id": "C", "primary_pattern": "Portrait / Identity", "title_system_family": "character-led", "title_system": "seam", "prompt_path": "c.md", "central_action": "turning", "shared_hierarchy": "center", "character_title_relation": "garment seam"},
        ],
        "candidates": [{"id": "A1", "direction_id": "A", "operation": "initial", "output_path": ""}],
    }


class ProductionContractTests(unittest.TestCase):
    def test_prompt_preflight_accepts_complete_contract_and_rejects_duplicate_pattern(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "contract.json"; path.write_text(json.dumps(contract()))
            passed = command("prompt-preflight.py", "--contract", str(path)); self.assertEqual(passed.returncode, 0, passed.stderr)
            invalid = contract(); invalid["directions"][1]["primary_pattern"] = "Abstract Material / Process"; path.write_text(json.dumps(invalid))
            failed = command("prompt-preflight.py", "--contract", str(path)); self.assertEqual(failed.returncode, 2); self.assertIn("primary-pattern-duplicate", failed.stdout)

    def test_router_protects_title_architecture_and_refinement_budget(self):
        title = command("action-router.py", "--failure-code", "title-integrity", "--cycles-used", "3")
        self.assertEqual(json.loads(title.stdout)["action"], "promote-runner-up")
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

    def test_end_to_end_source_export_delivery_and_handoff(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); source = root / "source.png"; Image.new("RGB", (2048, 2048), "black").save(source)
            data = contract(); data["candidates"][0]["output_path"] = "source.png"; contract_path = root / "run-contract.json"; contract_path.write_text(json.dumps(data))
            self.assertEqual(command("prompt-preflight.py", "--contract", str(contract_path)).returncode, 0)
            self.assertEqual(command("cover-ops.py", "preflight-source", str(source), "--contract", str(contract_path)).returncode, 0)
            delivery = root / "delivery"; self.assertEqual(command("cover-ops.py", "export", str(source), "--out-dir", str(delivery)).returncode, 0)
            self.assertEqual(command("cover-ops.py", "preflight-delivery", str(delivery / "cover-3000.png"), "--expected-title", "Moon Signal").returncode, 0)
            manifest = root / "handoff-manifest.json"; completed = command("handoff-manifest.py", "--contract", str(contract_path), "--selected-candidate", "A1", "--delivery-dir", str(delivery), "--output", str(manifest), "--human-text-status", "passed", "--exact-title-confirmed", "--extra-readable-text-absent")
            self.assertEqual(completed.returncode, 0, completed.stderr); self.assertTrue(json.loads(manifest.read_text())["delivery_complete"])

    def test_skill_package_runs_after_copy(self):
        with tempfile.TemporaryDirectory() as directory:
            copied = Path(directory) / "album-cover-director"; shutil.copytree(SKILL, copied)
            completed = subprocess.run([sys.executable, str(copied / "scripts" / "cover-ops.py"), "--help"], text=True, capture_output=True, check=False)
            self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_learning_confidence_requires_user_validated_success(self):
        with tempfile.TemporaryDirectory() as directory:
            arguments = ("record", "--artist-root", directory, "--rule-id", "title-rule", "--model-family", "gpt-image", "--model-id", "gpt-image-2", "--host-surface", "test", "--outcome", "success")
            for _ in range(6): self.assertEqual(command("learning-state.py", *arguments).returncode, 0)
            assessed = command("learning-state.py", "assess", "--artist-root", directory)
            self.assertEqual(json.loads(assessed.stdout)["records"][0]["confidence"], "low")
            for _ in range(2): self.assertEqual(command("learning-state.py", *arguments, "--user-validated").returncode, 0)
            assessed = command("learning-state.py", "assess", "--artist-root", directory)
            self.assertEqual(json.loads(assessed.stdout)["records"][0]["confidence"], "high")


if __name__ == "__main__":
    unittest.main()
