from __future__ import annotations

import base64
import hashlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/album-cover-director/scripts/concept-board.py"


class ParsedBoard(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.images = []
        self.candidates = []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        values = dict(attrs)
        if tag == "img":
            self.images.append(values)
        if tag == "figure":
            self.candidates.append(values.get("data-candidate-id"))


def make_fixture(root: Path, count: int = 16) -> dict:
    """Fictional covers; the repeated broad pattern is intentional, not a quality claim."""
    interpretations = [
        {"id": f"I{index}", "summary": f"夜の海に残る記憶を、解釈{index}として描く。",
         "evidence": [{"source": "description", "anchor": f"架空のテスト用ブリーフ {index}"}]}
        for index in range(1, 5)
    ]
    directions, candidates, reviewed = [], [], []
    for index in range(1, count + 1):
        direction_id = f"D{index:02d}"
        candidate_id = f"A{index:02d}"
        image_path = root / f"candidate-{index:02d}.png"
        image = Image.new("RGB", (512, 512), (index * 13 % 255, 60, 190))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, 511, 511), outline="white", width=10)
        draw.line((0, index * 17 % 512, 511, 511), fill="black", width=7)
        image.save(image_path)
        directions.append({
            "id": direction_id, "name": f"波の記憶・第{index}案",
            "primary_pattern": "Abstract Material / Process",
            "title_system_family": "material-world", "title_system": "water trace",
            "prompt_path": f"prompts/{direction_id}.md",
            "world_engine": "drying water", "material_vocabulary": "salt and paper",
            "title_anatomy": "water traces", "world_role": "memory",
            "interpretation_id": f"I{(index - 1) % 4 + 1}",
            "visual_mechanism": f"水が引いた跡を文字として読む。構図{index}。",
            "preserve_in_production": ["濡れた紙の質感", "文字が素材の一部であること"],
            "planned_signature": {
                "title_placement": f"余白の端 {index}", "title_scale": f"比率 {index}",
                "figure_role": "人物なし", "camera": f"視点 {index}",
                "layout": f"配置 {index}", "medium": "紙と水の跡",
            },
        })
        candidates.append({
            "id": candidate_id, "direction_id": direction_id, "operation": "initial",
            "output_path": image_path.name,
            "preview_notes": ["細かな文字は未確認です。", "仕上げ時にコントラストを確認。"],
        })
        reviewed.append({
            "id": candidate_id, "sha256": hashlib.sha256(image_path.read_bytes()).hexdigest(),
            "observation": f"架空のテスト記録。候補{index}の配色と線の位置を確認。",
        })
    return {
        "schema_version": 2, "stage": "concept-preview",
        "release": {"exact_title": "波の記憶", "allowed_readable_text": ["波の記憶"]},
        "constraints": {"title_must_be_image_native": True, "post_typesetting_allowed": False},
        "rights": {"reference_basis": "fictional test fixture"},
        "runtime": {
            "model_family": "gpt-image", "model_id": "gpt-image-2.6-flare",
            "host_surface": "test", "skill_version": "test",
            "capability_profile": {"source_minimum_dimension": 2048, "preview_minimum_dimension": 512},
        },
        "interpretations": interpretations, "directions": directions, "candidates": candidates,
        "diversity_review": {
            "status": "passed", "reviewed_candidates": reviewed,
            "compared_axes": ["layout", "camera", "title_scale"],
            "summary": "架空のテスト記録。候補間の色と線の位置を比較。",
        },
    }


def write_contract(root: Path, data: dict) -> Path:
    path = root / "run-contract.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return path


def command(contract: Path, output: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--contract", str(contract), "--output", str(output), *args],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )


class ConceptBoardTests(unittest.TestCase):
    def test_sixteen_real_thumbnails_keep_labels_outside_unchanged_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = make_fixture(root)
            path = write_contract(root, data)
            before = {image.name: image.read_bytes() for image in root.glob("*.png")}
            output = root / "board.html"
            result = command(path, output)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            document = output.read_text(encoding="utf-8")
            parsed = ParsedBoard(); parsed.feed(document)
            self.assertEqual(parsed.candidates, [f"A{index:02d}" for index in range(1, 17)])
            self.assertEqual(len(parsed.images), 16)
            self.assertEqual(parsed.tags.count("figcaption"), 16)
            self.assertIn("夜の海に残る記憶", document)
            self.assertIn("コンセプト案・未校了", document)
            self.assertIn("repeat(4, minmax(0, 1fr))", document)
            self.assertFalse(json.loads(result.stdout)["delivery_complete"])
            self.assertEqual(before, {image.name: image.read_bytes() for image in root.glob("*.png")})
            # The thumbnail contains only resized artwork, including its entire border.
            encoded = parsed.images[0]["src"].split(",", 1)[1]
            with Image.open(io.BytesIO(base64.b64decode(encoded))) as actual:
                expected = Image.open(root / "candidate-01.png").convert("RGBA")
                expected.thumbnail((320, 320), Image.Resampling.LANCZOS)
                self.assertEqual(actual.size, (320, 320))
                self.assertIsNone(ImageChops.difference(actual, expected).getbbox())

    def test_board_rejects_reviewed_preview_that_cannot_be_selected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = make_fixture(root, 1)
            data["runtime"]["capability_profile"]["preview_minimum_dimension"] = 1024
            path = write_contract(root, data)
            source = root / "candidate-01.png"
            before = source.read_bytes()
            for options in ((), ("--draft",)):
                with self.subTest(options=options):
                    output = root / "board.html"
                    result = command(path, output, *options)
                    self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                    self.assertIn("preview-below-minimum-size", result.stdout)
                    self.assertFalse(output.exists())
                    self.assertEqual(source.read_bytes(), before)

    def test_pending_review_only_renders_as_internal_draft(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = make_fixture(root, 1)
            data["diversity_review"] = {"status": "pending"}
            data["candidates"][0]["preview_notes"] = None
            path = write_contract(root, data)
            output = root / "board.html"
            rejected = command(path, output)
            self.assertEqual(rejected.returncode, 2, rejected.stderr)
            self.assertFalse(output.exists())
            draft = command(path, output, "--draft")
            self.assertEqual(draft.returncode, 0, draft.stdout + draft.stderr)
            self.assertEqual(json.loads(draft.stdout)["status"], "draft")
            self.assertIn("内部確認用ドラフト", output.read_text(encoding="utf-8"))

    def test_stale_or_incomplete_review_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = make_fixture(root, 2)
            path = write_contract(root, data)
            Image.new("RGB", (512, 512), "red").save(root / "candidate-01.png")
            output = root / "board.html"
            stale = command(path, output)
            self.assertEqual(stale.returncode, 2, stale.stderr)
            self.assertFalse(output.exists())
            data["diversity_review"]["reviewed_candidates"] = []
            write_contract(root, data)
            incomplete = command(path, output)
            self.assertEqual(incomplete.returncode, 2, incomplete.stderr)
            self.assertFalse(output.exists())

    def test_missing_invalid_and_non_square_images_do_not_create_a_board(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = make_fixture(root, 1)
            path = write_contract(root, data)
            image = root / "candidate-01.png"
            for condition in ("missing", "invalid", "non-square"):
                with self.subTest(condition=condition):
                    if condition == "missing":
                        image.unlink(missing_ok=True)
                    elif condition == "invalid":
                        image.write_text("not an image", encoding="utf-8")
                    else:
                        Image.new("RGB", (512, 400), "blue").save(image)
                    original = image.read_bytes() if image.exists() else None
                    output = root / f"{condition}.html"
                    result = command(path, output, "--draft")
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertFalse(output.exists())
                    if original is not None:
                        self.assertEqual(image.read_bytes(), original)
                    if condition == "non-square":
                        self.assertIn("non-square-source", result.stdout)

    def test_duplicate_ids_bad_references_and_remote_paths_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for condition in ("duplicate", "bad-direction", "remote-image"):
                with self.subTest(condition=condition):
                    data = make_fixture(root, 2)
                    if condition == "duplicate":
                        data["candidates"][1]["id"] = data["candidates"][0]["id"]
                    elif condition == "bad-direction":
                        data["candidates"][0]["direction_id"] = "missing"
                    else:
                        data["candidates"][0]["output_path"] = "https://example.com/image.png"
                    path = write_contract(root, data)
                    output = root / f"{condition}.html"
                    result = command(path, output, "--draft")
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertFalse(output.exists())

    def test_metadata_is_escaped_and_the_board_loads_no_external_content(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = make_fixture(root, 1)
            hostile = '<script>alert("海")</script><img src="https://example.com/tracker">&'
            data["release"]["exact_title"] = hostile
            data["release"]["allowed_readable_text"] = [hostile]
            data["directions"][0]["name"] = hostile
            data["directions"][0]["visual_mechanism"] = hostile
            data["interpretations"][0]["summary"] = hostile
            data["candidates"][0]["preview_notes"] = [hostile]
            output = root / "board.html"
            result = command(write_contract(root, data), output)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            document = output.read_text(encoding="utf-8")
            self.assertIn("&lt;script&gt;", document)
            parsed = ParsedBoard(); parsed.feed(document)
            self.assertNotIn("script", parsed.tags)
            self.assertNotIn("link", parsed.tags)
            self.assertTrue(all(image["src"].startswith("data:image/png;base64,") for image in parsed.images))
            self.assertEqual(len(parsed.images), 1)

    def test_contract_and_image_overwrite_are_rejected_including_file_aliases(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = make_fixture(root, 1)
            contract_path = write_contract(root, data)
            source = root / "candidate-01.png"
            symlink = root / "source-link.html"; symlink.symlink_to(source)
            hardlink = root / "source-hardlink.html"; hardlink.hardlink_to(source)
            before_contract, before_source = contract_path.read_bytes(), source.read_bytes()
            for output in (contract_path, source, symlink, hardlink):
                with self.subTest(output=output.name):
                    result = command(contract_path, output, "--draft")
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertIn("protected-output", result.stdout)
                    self.assertEqual(contract_path.read_bytes(), before_contract)
                    self.assertEqual(source.read_bytes(), before_source)

    def test_malformed_contract_and_excess_columns_fail_without_partial_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "run-contract.json"
            path.write_text("{broken", encoding="utf-8")
            output = root / "board.html"
            malformed = command(path, output)
            self.assertEqual(malformed.returncode, 2, malformed.stderr)
            self.assertFalse(output.exists())
            path = write_contract(root, make_fixture(root, 1))
            columns = command(path, output, "--columns", "5")
            self.assertEqual(columns.returncode, 2, columns.stderr)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
