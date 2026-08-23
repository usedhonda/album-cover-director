#!/usr/bin/env python3
"""Inspect, compare, preflight, and export square album-cover images."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
except ImportError as exc:  # pragma: no cover
    Image = None
    PIL_IMPORT_ERROR = exc
else:
    PIL_IMPORT_ERROR = None


def require_pillow() -> None:
    if Image is None:
        raise SystemExit("Pillow is required for image operations. Install Pillow, or return the export specification without claiming delivery completion.") from PIL_IMPORT_ERROR


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def image_record(path: Path) -> dict[str, object]:
    require_pillow()
    with Image.open(path) as image:
        width, height = image.size
        alpha = "A" in image.getbands() or image.info.get("transparency") is not None
        return {"path": str(path), "format": image.format, "mode": image.mode, "width": width,
                "height": height, "square": width == height, "has_alpha": alpha,
                "bytes": path.stat().st_size, "sha256": sha256(path)}


def inspect_images(paths: list[Path]) -> int:
    records = [image_record(path) for path in paths]
    print(json.dumps(records, ensure_ascii=False, indent=2))
    return 0 if all(record["square"] for record in records) else 2


def label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], value: str) -> None:
    draw.text(xy, value, fill=(235, 235, 235), font=ImageFont.load_default())


def prepare_square(image: Image.Image, size: int) -> Image.Image:
    return ImageOps.fit(image.convert("RGB"), (size, size), method=Image.Resampling.LANCZOS)


def contact_sheet(paths: list[Path], output: Path) -> None:
    require_pillow()
    cell, gap, label_height = 256, 20, 38
    rows = ["56 px", "128 px", "256 px", "grayscale", "blur"]
    sheet = Image.new("RGB", (gap + len(paths) * (cell + gap), gap + label_height + len(rows) * (cell + label_height + gap)), (24, 24, 24))
    draw = ImageDraw.Draw(sheet)
    for column, path in enumerate(paths):
        x = gap + column * (cell + gap)
        label(draw, (x, gap), path.stem[:36])
        with Image.open(path) as opened:
            base = prepare_square(opened, cell)
        variants = [prepare_square(base, 56), prepare_square(base, 128), base,
                    ImageOps.grayscale(base).convert("RGB"), base.filter(ImageFilter.GaussianBlur(radius=12))]
        for row, (row_name, variant) in enumerate(zip(rows, variants)):
            y = gap + label_height + row * (cell + label_height + gap)
            if column == 0:
                label(draw, (gap, y - 18), row_name)
            sheet.paste(variant, (x + (cell - variant.width) // 2, y + (cell - variant.height) // 2))
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, format="PNG")
    print(json.dumps({"output": str(output), "sha256": sha256(output)}, indent=2))


def perceptual_hash(path: Path) -> int:
    require_pillow()
    with Image.open(path) as image:
        sample = ImageOps.grayscale(image.convert("RGB")).resize((8, 8), Image.Resampling.LANCZOS)
    values = list(sample.getdata())
    threshold = sum(values) / len(values)
    return sum((value >= threshold) << index for index, value in enumerate(values))


def compare_images(paths: list[Path], threshold: int) -> int:
    hashes = {path: perceptual_hash(path) for path in paths}
    pairs = []
    for left, right in itertools.combinations(paths, 2):
        distance = bin(hashes[left] ^ hashes[right]).count("1")
        pairs.append({"left": str(left), "right": str(right), "distance": distance, "warning": distance <= threshold})
    print(json.dumps({"algorithm": "ahash-8x8", "warning_threshold": threshold, "pairs": pairs}, ensure_ascii=False, indent=2))
    return 0


def preflight_image(path: Path, minimum_size: int, expected_title: str, exact_size: bool = False) -> int:
    record = image_record(path)
    failures = []
    if not record["square"]: failures.append("non-square")
    if (record["width"] != minimum_size if exact_size else record["width"] < minimum_size): failures.append("wrong-delivery-size" if exact_size else "below-minimum-size")
    if record["mode"] not in {"RGB", "RGBA"}: failures.append("unsupported-color-mode")
    print(json.dumps({"image": record, "objective_failures": failures,
                      "text_verification": {"status": "human_required", "expected_title": expected_title,
                                            "reason": "OCR is not configured for this skill"}}, ensure_ascii=False, indent=2))
    return 2 if failures else 0


def source_preflight(path: Path, contract_path: Path) -> int:
    try:
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        runtime = contract["runtime"]
        minimum = runtime["capability_profile"]["source_minimum_dimension"]
        expected_title = contract["release"]["exact_title"]
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "fail", "objective_failures": ["contract-capability-unreadable"], "detail": str(exc)})); return 2
    return preflight_image(path, minimum, expected_title)


def export_cover(source: Path, out_dir: Path, size: int, jpg_quality: int) -> None:
    require_pillow()
    with Image.open(source) as opened:
        width, height = opened.size
        if width != height: raise SystemExit(f"Source must be square; got {width}x{height}: {source}")
        master = opened.convert("RGBA").resize((size, size), Image.Resampling.LANCZOS)
    out_dir.mkdir(parents=True, exist_ok=True)
    png_path, jpg_path, thumb_path = out_dir / "cover-3000.png", out_dir / "cover-3000.jpg", out_dir / "thumbnail-256.png"
    master.save(png_path, format="PNG", optimize=True)
    rgb = Image.new("RGB", master.size, "white"); rgb.paste(master, mask=master.getchannel("A"))
    rgb.save(jpg_path, format="JPEG", quality=jpg_quality, optimize=True, progressive=True)
    rgb.resize((256, 256), Image.Resampling.LANCZOS).save(thumb_path, format="PNG", optimize=True)
    print(json.dumps({"source": image_record(source), "scaled": width != size,
                      "outputs": [image_record(path) for path in (png_path, jpg_path, thumb_path)]}, ensure_ascii=False, indent=2))


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__); commands = root.add_subparsers(dest="command", required=True)
    inspect = commands.add_parser("inspect", help="Print image metadata and checksum"); inspect.add_argument("images", nargs="+", type=Path)
    sheet = commands.add_parser("contact-sheet", help="Create comparison sheet"); sheet.add_argument("images", nargs="+", type=Path); sheet.add_argument("--output", required=True, type=Path)
    export = commands.add_parser("export", help="Write distributor-ready square assets"); export.add_argument("source", type=Path); export.add_argument("--out-dir", required=True, type=Path); export.add_argument("--size", type=int, default=3000); export.add_argument("--jpg-quality", type=int, default=95)
    preflight = commands.add_parser("preflight", help="Legacy generic objective image check"); preflight.add_argument("image", type=Path); preflight.add_argument("--minimum-size", type=int, default=3000); preflight.add_argument("--expected-title", default="")
    source = commands.add_parser("preflight-source", help="Check a generated source against its run contract"); source.add_argument("image", type=Path); source.add_argument("--contract", required=True, type=Path)
    delivery = commands.add_parser("preflight-delivery", help="Check a 3000px delivery asset"); delivery.add_argument("image", type=Path); delivery.add_argument("--expected-title", default="")
    compare = commands.add_parser("compare", help="Warn about visually similar candidates"); compare.add_argument("images", nargs="+", type=Path); compare.add_argument("--warning-threshold", type=int, default=8)
    return root


def main() -> int:
    args = parser().parse_args()
    if args.command == "inspect": return inspect_images(args.images)
    if args.command == "contact-sheet": contact_sheet(args.images, args.output); return 0
    if args.command == "compare": return compare_images(args.images, args.warning_threshold)
    if args.command == "preflight": return preflight_image(args.image, args.minimum_size, args.expected_title)
    if args.command == "preflight-source": return source_preflight(args.image, args.contract)
    if args.command == "preflight-delivery": return preflight_image(args.image, 3000, args.expected_title, exact_size=True)
    if args.command == "export":
        if args.size <= 0 or not 1 <= args.jpg_quality <= 100: raise SystemExit("--size must be positive and --jpg-quality must be 1..100")
        export_cover(args.source, args.out_dir, args.size, args.jpg_quality); return 0
    raise AssertionError(args.command)


if __name__ == "__main__": raise SystemExit(main())
