from __future__ import annotations

import json
import copy
import hashlib
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

    def stage_contract(self, source: Path) -> dict:
        return {
            "schema_version": 2,
            "stage": "concept-preview",
            "release": {"exact_title": "Moon Signal", "allowed_readable_text": ["Moon Signal"]},
            "constraints": {"title_must_be_image_native": True, "post_typesetting_allowed": False},
            "rights": {"reference_basis": "fictional test fixture"},
            "runtime": {
                "model_family": "gpt-image", "model_id": "unknown-not-exposed",
                "host_surface": "test", "skill_version": "test",
                "capability_profile": {"source_minimum_dimension": 2048, "preview_minimum_dimension": 512},
            },
            "interpretations": [{"id": "I1", "summary": "A signal persists after its source leaves.",
                                 "evidence": [{"source": "title", "anchor": "Signal"}]}],
            "directions": [{
                "id": "A", "name": "Frozen signal", "interpretation_id": "I1",
                "primary_pattern": "Abstract Material / Process", "title_system_family": "material-world",
                "title_system": "frost", "prompt_path": "prompts/A.md", "world_engine": "freezing",
                "material_vocabulary": "ice", "title_anatomy": "frozen strokes", "world_role": "memory",
                "visual_mechanism": "The signal survives as frozen letter shapes.",
                "preserve_in_production": ["asymmetric frozen strokes", "large empty upper field"],
                "planned_signature": {"title_placement": "lower left", "title_scale": "half width",
                                      "figure_role": "absent", "camera": "overhead", "layout": "asymmetric",
                                      "medium": "ice"},
            }],
            "candidates": [{"id": "A1", "direction_id": "A", "output_path": source.name}],
            "diversity_review": {"status": "pending"},
        }

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
            with Image.open(root / "sheet.png") as generated:
                self.assertEqual(generated.height, 1628)
            rejected = self.run_cli("export", str(wide), "--out-dir", str(root / "bad"))
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("must be square", rejected.stderr)

    def test_source_preflight_uses_stage_minimum_and_keeps_text_human_review(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            source = root / "source.png"
            Image.new("RGB", (512, 512), "black").save(source)
            data = self.stage_contract(source)
            contract = root / "contract.json"
            contract.write_text(json.dumps(data))
            preview = self.run_cli("preflight-source", str(source), "--contract", str(contract))
            self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)
            payload = json.loads(preview.stdout)
            self.assertEqual(payload["text_verification"]["status"], "visual_review_required")
            self.assertEqual(payload["text_verification"]["expected_title"], "Moon Signal")

            data["stage"] = "production-candidate"
            contract.write_text(json.dumps(data))
            too_small = self.run_cli("preflight-source", str(source), "--contract", str(contract))
            self.assertEqual(too_small.returncode, 2, too_small.stderr)
            self.assertIn("below-minimum-size", json.loads(too_small.stdout)["objective_failures"])
            Image.new("RGB", (2048, 2048), "black").save(source)
            production = self.run_cli("preflight-source", str(source), "--contract", str(contract))
            self.assertEqual(production.returncode, 0, production.stdout + production.stderr)

    def test_source_preflight_rejects_invalid_stage_capability_and_unregistered_images(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            source = root / "source.png"
            Image.new("RGB", (512, 512), "black").save(source)
            baseline = self.stage_contract(source)
            contract = root / "contract.json"
            mutations = {
                "missing-stage": lambda data: data.pop("stage"),
                "invalid-stage": lambda data: data.update(stage="finished"),
                "missing-preview-minimum": lambda data: data["runtime"]["capability_profile"].pop("preview_minimum_dimension"),
                "zero-preview-minimum": lambda data: data["runtime"]["capability_profile"].update(preview_minimum_dimension=0),
                "negative-preview-minimum": lambda data: data["runtime"]["capability_profile"].update(preview_minimum_dimension=-1),
                "boolean-preview-minimum": lambda data: data["runtime"]["capability_profile"].update(preview_minimum_dimension=True),
                "unknown-preview-minimum": lambda data: data["runtime"]["capability_profile"].update(preview_minimum_dimension="unknown-not-exposed"),
                "before-generation": lambda data: data.update(candidates=[]),
                "unregistered-image": lambda data: data["candidates"][0].update(output_path="other.png"),
                "ambiguous-image": lambda data: data["candidates"].append({"id": "A2", "direction_id": "A", "output_path": source.name}),
            }
            for name, mutate in mutations.items():
                with self.subTest(case=name):
                    data = copy.deepcopy(baseline)
                    mutate(data)
                    contract.write_text(json.dumps(data))
                    result = self.run_cli("preflight-source", str(source), "--contract", str(contract))
                    self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                    self.assertTrue(json.loads(result.stdout)["objective_failures"])

    def test_source_preflight_preserves_legacy_minimum_without_preview_registration(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            source = root / "source.png"
            contract = root / "contract.json"
            data = {"release": {"exact_title": "Moon Signal"},
                    "runtime": {"capability_profile": {"source_minimum_dimension": 2048}}}
            for version in (None, 1):
                with self.subTest(version=version):
                    if version is not None:
                        data["schema_version"] = version
                    contract.write_text(json.dumps(data))
                    Image.new("RGB", (512, 512), "black").save(source)
                    small = self.run_cli("preflight-source", str(source), "--contract", str(contract))
                    self.assertEqual(small.returncode, 2, small.stderr)
                    self.assertIn("below-minimum-size", json.loads(small.stdout)["objective_failures"])
                    Image.new("RGB", (2048, 2048), "black").save(source)
                    result = self.run_cli("preflight-source", str(source), "--contract", str(contract))
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_source_preflight_rejects_changed_selected_preview(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw).resolve()
            preview = root / "preview.png"
            Image.new("RGB", (512, 512), "black").save(preview)
            data = self.stage_contract(preview)
            preview_sha = hashlib.sha256(preview.read_bytes()).hexdigest()
            data["diversity_review"] = {
                "status": "passed", "compared_axes": ["layout", "medium"],
                "summary": "Fictional fixture reviewed for this test.",
                "reviewed_candidates": [{"id": "A1", "sha256": preview_sha,
                                         "observation": "Fictional source fixture retained."}],
            }
            preview_contract = root / "preview-contract.json"
            preview_contract.write_text(json.dumps(data))
            production = copy.deepcopy(data)
            production["stage"] = "production-candidate"
            production.pop("diversity_review")
            source = root / "production.png"
            Image.new("RGB", (2048, 2048), "black").save(source)
            production["candidates"] = [{"id": "A-final", "direction_id": "A", "output_path": source.name,
                                          "preview_candidate_id": "A1"}]
            direction = data["directions"][0]
            production["selection"] = {
                "source_contract_path": str(preview_contract),
                "source_contract_sha256": hashlib.sha256(preview_contract.read_bytes()).hexdigest(),
                "selected_candidate_ids": ["A1"], "reason": "Retain the selected visual mechanism.",
                "sources": [{"candidate_id": "A1", "direction_id": "A", "source_path": str(preview),
                             "source_sha256": preview_sha, "reason": "Retain the asymmetric composition.",
                             "visual_mechanism": direction["visual_mechanism"],
                             "preserve_in_production": direction["preserve_in_production"],
                             "planned_signature": direction["planned_signature"]}],
            }
            contract = root / "production-contract.json"
            contract.write_text(json.dumps(production))
            accepted = self.run_cli("preflight-source", str(source), "--contract", str(contract))
            self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)
            Image.new("RGB", (512, 512), "white").save(preview)
            stale = self.run_cli("preflight-source", str(source), "--contract", str(contract))
            self.assertEqual(stale.returncode, 2, stale.stdout + stale.stderr)
            self.assertIn("selection-source-changed", json.loads(stale.stdout)["objective_failures"])

if __name__ == "__main__":
    unittest.main()
