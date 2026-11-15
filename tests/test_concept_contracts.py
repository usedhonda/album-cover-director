"""Exercise the preview -> reviewed selection -> production delivery boundary."""

from __future__ import annotations

import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "album-cover-director"
sys.path.insert(0, str(SKILL / "scripts"))
from concept_contract import checksum, validate, validate_review, validate_selection_sources


def command(script: str, *arguments: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SKILL / "scripts" / script), *map(str, arguments)], text=True, capture_output=True, check=False)


def concept_contract(count: int = 12, stage: str = "concept-preview") -> dict:
    directions = [{
        "id": f"D{index:02d}", "name": f"Loop {index}", "interpretation_id": "I01",
        "primary_pattern": "Minimal Geometry / Color Field", "title_system_family": "graphic-field",
        "title_system": "The title is the shared positive and negative boundary", "prompt_path": f"prompts/{index}.md",
        "visual_mechanism": f"Figure-ground reading route {index}",
        "preserve_in_production": ["The title and void share one contour", f"Keep route {index}"],
        "planned_signature": {"title_placement": "full field", "title_scale": "structurally dominant", "figure_role": "none", "camera": "orthographic", "layout": f"route {index}", "medium": "two flat colors"},
        "graphic_rule": "one shared contour", "title_shape": "exact native lettering", "figure_ground": "interlocking regions", "reading_route": "left to right",
    } for index in range(count)]
    result = {
        "schema_version": 2, "stage": stage,
        "release": {"exact_title": "まだ帰れない夜に", "allowed_readable_text": ["まだ帰れない夜に"]},
        "constraints": {"title_must_be_image_native": True, "post_typesetting_allowed": False},
        "rights": {"reference_basis": "synthetic test brief"},
        "runtime": {"model_family": "gpt-image", "model_id": "test-model", "host_surface": "test", "skill_version": "test", "capability_profile": {"source_minimum_dimension": 2048, "preview_minimum_dimension": 64}},
        "interpretations": [{"id": "I01", "summary": "The desire to return meets a closed route", "evidence": [{"source": "title", "anchor": "帰れない names the blocked action"}]}],
        "directions": directions, "candidates": [],
    }
    if stage == "concept-preview":
        result["diversity_review"] = {"status": "pending", "reviewed_candidates": [], "compared_axes": [], "summary": ""}
    return result


def reviewed_preview(root: Path, count: int = 2) -> tuple[Path, dict]:
    data = concept_contract(count)
    for index in range(count):
        image = root / f"preview-{index}.png"
        Image.new("RGB", (64, 64), (index * 47 % 255, 75, 160)).save(image)
        data["candidates"].append({"id": f"C{index:02d}", "direction_id": f"D{index:02d}", "output_path": image.name, "preview_notes": ["Title accuracy is not approved for delivery."]})
    data["diversity_review"] = {
        "status": "passed", "compared_axes": ["title placement", "reading route"],
        "summary": "Fixture representing an explicitly recorded visual decision, not an automatic quality score.",
        "reviewed_candidates": [{"id": item["id"], "sha256": checksum(root / item["output_path"]), "observation": f"Observed contour route for {item['id']}"} for item in data["candidates"]],
    }
    path = root / "preview-contract.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return path, data


class ConceptContractTests(unittest.TestCase):
    def test_preview_counts_are_variable_and_repeated_patterns_are_not_visual_proof(self):
        for count in (1, 4, 12, 16, 24):
            with self.subTest(count=count):
                self.assertEqual(validate(concept_contract(count)), [])
        self.assertIn("direction-count-invalid", {item["code"] for item in validate(concept_contract(25))})
        self.assertEqual(validate(concept_contract(1, "production-candidate")), [])
        # A metadata-valid set is still unreviewed and cannot be presented/selected.
        self.assertEqual(validate_review(concept_contract(12), Path("unused.json"))[0]["code"], "visual-review-required")

    def test_interpretation_links_graphic_rules_and_exact_title_remain_required(self):
        mutations = [
            (lambda data: data["directions"][0].update(interpretation_id="missing"), "interpretation-reference-invalid"),
            (lambda data: data["interpretations"][0].update(evidence=[]), "interpretation-evidence-required"),
            (lambda data: data["directions"][0].pop("graphic_rule"), "graphic-field-direction-incomplete"),
            (lambda data: data["release"].update(allowed_readable_text=["wrong title"]), "title-not-allowed"),
            (lambda data: data["constraints"].update(post_typesetting_allowed=True), "post-typesetting-prohibited"),
            (lambda data: data["runtime"]["capability_profile"].pop("preview_minimum_dimension"), "preview-capability-required"),
            (lambda data: data.pop("stage"), "stage-required"),
        ]
        for mutate, expected in mutations:
            with self.subTest(expected=expected):
                data = concept_contract(1)
                mutate(data)
                self.assertIn(expected, {item["code"] for item in validate(data)})
        malformed = concept_contract(1)
        malformed["directions"][0].update(primary_pattern=[], interpretation_id=[], title_system_family=[])
        self.assertTrue(validate(malformed))  # Structured failures, not an unhashable-value crash.

    def test_review_must_cover_current_ids_and_unchanged_images(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path, data = reviewed_preview(root)
            self.assertEqual(validate_review(data, path), [])
            missing = copy.deepcopy(data)
            missing["diversity_review"]["reviewed_candidates"].pop()
            self.assertIn("review-candidate-coverage", {item["code"] for item in validate_review(missing, path)})
            duplicate = copy.deepcopy(data)
            duplicate["diversity_review"]["reviewed_candidates"].append(copy.deepcopy(duplicate["diversity_review"]["reviewed_candidates"][0]))
            self.assertIn("review-id-duplicate", {item["code"] for item in validate_review(duplicate, path)})
            Image.new("RGB", (64, 64), "white").save(root / "preview-0.png")
            self.assertIn("review-source-changed", {item["code"] for item in validate_review(data, path)})

    def test_selection_preserves_multiple_candidates_in_one_direction_without_renumbering(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path, data = reviewed_preview(root)
            data["candidates"][1]["direction_id"] = "D00"
            path.write_text(json.dumps(data), encoding="utf-8")
            original_hash = checksum(path)
            output = root / "production" / "run-contract.json"
            result = command("concept-selection.py", "--contract", path, "--candidate", "C01", "--candidate", "C00", "--reason", "Keep the impossible contour and the two readings.", "--output", output)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            selected = json.loads(output.read_text())
            self.assertEqual(validate(selected), [])
            self.assertEqual(validate_selection_sources(selected), [])
            self.assertEqual(selected["stage"], "production-candidate")
            self.assertEqual(selected["candidates"], [])
            self.assertEqual([item["id"] for item in selected["directions"]], ["D00"])
            self.assertEqual(selected["selection"]["selected_candidate_ids"], ["C01", "C00"])
            self.assertEqual([item["candidate_id"] for item in selected["selection"]["sources"]], ["C01", "C00"])
            self.assertTrue(all(Path(item["source_path"]).is_absolute() for item in selected["selection"]["sources"]))
            self.assertEqual(selected["runtime"]["capability_profile"]["source_minimum_dimension"], 2048)
            self.assertEqual(checksum(path), original_hash)

    def test_selection_rejects_unknown_duplicate_pending_and_stale_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path, data = reviewed_preview(root)
            base = ("--contract", path, "--reason", "Chosen composition", "--output", root / "production.json")
            for ids in (("missing",), ("C00", "C00")):
                arguments = [value for candidate_id in ids for value in ("--candidate", candidate_id)]
                result = command("concept-selection.py", *base, *arguments)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertFalse((root / "production.json").exists())
            data["diversity_review"]["status"] = "pending"
            path.write_text(json.dumps(data))
            pending = command("concept-selection.py", *base, "--candidate", "C00")
            self.assertIn("visual-review-required", pending.stdout)
            data["diversity_review"]["status"] = "passed"
            path.write_text(json.dumps(data))
            Image.new("RGB", (64, 64), "white").save(root / "preview-0.png")
            stale = command("concept-selection.py", *base, "--candidate", "C00")
            self.assertIn("review-source-changed", stale.stdout)

    def test_selected_mechanism_and_source_provenance_cannot_silently_drift(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path, _ = reviewed_preview(root, 1)
            output = root / "production.json"
            result = command("concept-selection.py", "--contract", path, "--candidate", "C00", "--reason", "Keep the contour", "--output", output)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            production = json.loads(output.read_text())
            changed = copy.deepcopy(production)
            changed["directions"][0]["visual_mechanism"] = "ordinary caption beside a figure"
            self.assertIn("selected-design-changed", {item["code"] for item in validate(changed)})
            changed["selection"]["sources"][0]["visual_mechanism"] = changed["directions"][0]["visual_mechanism"]
            self.assertIn("selection-origin-mismatch", {item["code"] for item in validate_selection_sources(changed)})
            Image.new("RGB", (64, 64), "white").save(root / "preview-0.png")
            self.assertIn("selection-source-changed", {item["code"] for item in validate_selection_sources(production)})

    def test_selection_keeps_the_recorded_production_source_policy(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path, data = reviewed_preview(root, 1)
            data["runtime"]["capability_profile"]["source_minimum_dimension"] = 1024
            path.write_text(json.dumps(data))
            output = root / "production.json"
            result = command("concept-selection.py", "--contract", path, "--candidate", "C00", "--reason", "Keep the primary composition", "--output", output)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            production = json.loads(output.read_text())
            self.assertEqual(production["runtime"]["capability_profile"], data["runtime"]["capability_profile"])

    def test_scoped_donor_keeps_primary_composition_and_separate_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path, data = reviewed_preview(root, 2)
            output = root / "production.json"
            result = command("concept-selection.py", "--contract", path, "--candidate", "C00", "--donor", "C01", "--donor-trait", "lighting:borrow only the soft side light", "--donor-trait", "texture:restrained paper grain", "--reason", "Primary contour with the donor's lighting", "--output", output)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            production = json.loads(output.read_text())
            self.assertEqual(validate(production), [])
            self.assertEqual(validate_selection_sources(production), [])
            self.assertEqual(production["selection"]["selected_candidate_ids"], ["C00"])
            self.assertEqual([item["id"] for item in production["directions"]], ["D00"])
            for key in ("visual_mechanism", "planned_signature", "preserve_in_production"):
                self.assertEqual(production["directions"][0][key], data["directions"][0][key])
            donor = production["selection"]["donors"][0]
            self.assertEqual(donor["candidate_id"], "C01")
            self.assertEqual(donor["direction_snapshot"], data["directions"][1])
            self.assertEqual(donor["interpretation_snapshot"], data["interpretations"][0])
            self.assertEqual([item["axis"] for item in donor["traits"]], ["lighting", "texture"])
            self.assertTrue(Path(donor["source_path"]).is_absolute())

    def test_donor_rejects_unscoped_traits_and_ambiguous_primary_selection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path, _ = reviewed_preview(root, 2)
            base = ("--contract", path, "--candidate", "C00", "--reason", "Borrow a scoped trait", "--output", root / "production.json")
            invalid = [
                ("--donor", "C01"),
                ("--donor-trait", "color:blue"),
                ("--donor", "C01", "--donor-trait", "composition:move the title beside a figure"),
                ("--donor", "C01", "--donor-trait", "lighting:"),
                ("--candidate", "C01", "--donor", "C01", "--donor-trait", "color:blue"),
                ("--donor", "C00", "--donor-trait", "color:blue"),
                ("--donor", "missing", "--donor-trait", "color:blue"),
            ]
            for arguments in invalid:
                with self.subTest(arguments=arguments):
                    result = command("concept-selection.py", *base, *arguments)
                    self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                    self.assertFalse((root / "production.json").exists())

    def test_donor_images_and_original_evidence_remain_bound_to_review(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path, _ = reviewed_preview(root, 2)
            output = root / "production.json"
            result = command("concept-selection.py", "--contract", path, "--candidate", "C00", "--donor", "C01", "--donor-trait", "color:cool accent only", "--reason", "Primary contour with donor color", "--output", output)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            production = json.loads(output.read_text())
            changed = copy.deepcopy(production)
            changed["selection"]["donors"][0]["direction_snapshot"]["visual_mechanism"] = "invented replacement"
            self.assertIn("selection-origin-mismatch", {item["code"] for item in validate_selection_sources(changed)})
            Image.new("RGB", (64, 64), "white").save(root / "preview-1.png")
            self.assertIn("selection-source-changed", {item["code"] for item in validate_selection_sources(production)})
            production["selection"]["donors"][0]["source_sha256"] = checksum(root / "preview-1.png")
            self.assertIn("selection-review-mismatch", {item["code"] for item in validate_selection_sources(production)})

    def test_handoff_rejects_preview_even_when_delivery_files_and_text_flags_exist(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path, _ = reviewed_preview(root, 1)
            delivery = root / "delivery"
            self.assertEqual(command("cover-ops.py", "export", root / "preview-0.png", "--out-dir", delivery).returncode, 0)
            result = command("handoff-manifest.py", "--contract", path, "--selected-candidate", "C00", "--delivery-dir", delivery, "--output", root / "handoff.json", "--human-text-status", "passed", "--exact-title-confirmed", "--extra-readable-text-absent")
            self.assertEqual(result.returncode, 2)
            self.assertIn("concept-preview-is-not-deliverable", result.stderr)
            self.assertFalse((root / "handoff.json").exists())

    def test_selected_production_reruns_source_and_text_gates_before_handoff(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            preview_path, _ = reviewed_preview(root, 1)
            path = root / "production.json"
            selected = command("concept-selection.py", "--contract", preview_path, "--candidate", "C00", "--reason", "Keep the contour", "--output", path)
            self.assertEqual(selected.returncode, 0, selected.stdout + selected.stderr)
            data = json.loads(path.read_text())
            source = root / "finished.png"
            Image.new("RGB", (2048, 2048), "navy").save(source)
            data["candidates"] = [{"id": "P01", "direction_id": "D00", "preview_candidate_id": "C00", "output_path": source.name}]
            path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            delivery = root / "delivery"
            self.assertEqual(command("cover-ops.py", "export", source, "--out-dir", delivery).returncode, 0)
            base = ("--contract", path, "--selected-candidate", "P01", "--delivery-dir", delivery, "--output", root / "handoff.json", "--exact-title-confirmed", "--extra-readable-text-absent")
            unresolved = command("handoff-manifest.py", *base, "--human-text-status", "unresolved")
            self.assertEqual(unresolved.returncode, 2)
            self.assertFalse(json.loads((root / "handoff.json").read_text())["delivery_complete"])
            wrong_text = command("handoff-manifest.py", *base, "--human-text-status", "passed", "--observed-readable-text", "extra unapproved words")
            self.assertEqual(wrong_text.returncode, 2)
            passed = command("handoff-manifest.py", *base, "--human-text-status", "passed", "--observed-readable-text", data["release"]["exact_title"])
            self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)
            manifest = json.loads((root / "handoff.json").read_text())
            self.assertTrue(manifest["delivery_complete"])
            self.assertEqual(manifest["selected_candidate"]["preview_candidate_id"], "C00")
            Image.new("RGB", (512, 512), "navy").save(source)
            too_small = command("handoff-manifest.py", *base, "--human-text-status", "passed")
            self.assertEqual(too_small.returncode, 2)
            self.assertIn("production-source-below-minimum-size", too_small.stderr)

    def test_exploration_redos_do_not_exhaust_production_edits(self):
        result = command("action-router.py", "--stage", "concept-preview", "--exploration-redos", "5", "--cycles-used", "2", "--failure-code", "visual-convergence")
        self.assertEqual(result.returncode, 0, result.stderr)
        routed = json.loads(result.stdout)
        self.assertEqual(routed["action"], "explore-new-mechanism")
        self.assertEqual(routed["production_refinement_cycles_used"], 0)
        self.assertEqual(routed["exploration_redos"], 5)
        production = command("action-router.py", "--stage", "production-candidate", "--cycles-used", "2")
        self.assertEqual(json.loads(production.stdout)["action"], "promote-runner-up")

    def test_handoff_output_cannot_replace_selected_provenance_or_source_hardlinks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            preview_path, _ = reviewed_preview(root, 2)
            path = root / "production.json"
            selected = command("concept-selection.py", "--contract", preview_path, "--candidate", "C00", "--donor", "C01", "--donor-trait", "lighting:soft side light", "--reason", "Keep the primary contour", "--output", path)
            self.assertEqual(selected.returncode, 0, selected.stdout + selected.stderr)
            data = json.loads(path.read_text())
            source = root / "finished.png"
            Image.new("RGB", (2048, 2048), "navy").save(source)
            data["candidates"] = [{"id": "P01", "direction_id": "D00", "preview_candidate_id": "C00", "output_path": source.name}]
            path.write_text(json.dumps(data), encoding="utf-8")
            delivery = root / "delivery"
            self.assertEqual(command("cover-ops.py", "export", source, "--out-dir", delivery).returncode, 0)
            alias = root / "source-alias.json"
            os.link(source, alias)
            inputs = [preview_path, root / "preview-0.png", root / "preview-1.png", source, path]
            before = {item: checksum(item) for item in inputs}
            base = ("--contract", path, "--selected-candidate", "P01", "--delivery-dir", delivery, "--human-text-status", "passed", "--exact-title-confirmed", "--extra-readable-text-absent")
            for output in (preview_path, root / "preview-0.png", root / "preview-1.png", alias):
                with self.subTest(output=output.name):
                    result = command("handoff-manifest.py", *base, "--output", output)
                    self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                    self.assertIn("handoff-output-would-overwrite-input", result.stderr)
                    self.assertEqual({item: checksum(item) for item in inputs}, before)
            completed = command("handoff-manifest.py", *base, "--output", root / "handoff.json")
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            self.assertTrue(json.loads((root / "handoff.json").read_text())["delivery_complete"])
            self.assertEqual(list(root.glob(".handoff.json.*.tmp")), [])

    def test_shared_contract_scripts_travel_with_the_skill_package(self):
        with tempfile.TemporaryDirectory() as directory:
            copied = Path(directory) / "album-cover-director"
            shutil.copytree(SKILL, copied)
            path = Path(directory) / "preview.json"
            path.write_text(json.dumps(concept_contract(1)))
            result = subprocess.run([sys.executable, str(copied / "scripts" / "prompt-preflight.py"), "--contract", str(path)], text=True, capture_output=True, check=False, cwd=directory)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            selection = subprocess.run([sys.executable, str(copied / "scripts" / "concept-selection.py"), "--help"], text=True, capture_output=True, check=False, cwd=directory)
            self.assertEqual(selection.returncode, 0, selection.stderr)


if __name__ == "__main__":
    unittest.main()
