#!/usr/bin/env python3
"""Inspect, compare, and export square album-cover images."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
except ImportError as exc:  # pragma: no cover - exercised by dependency-free hosts
    Image = None
    PIL_IMPORT_ERROR = exc
else:
    PIL_IMPORT_ERROR = None


def require_pillow() -> None:
    if Image is None:
        raise SystemExit(
            "Pillow is required for image operations. Install it with "
            "`python -m pip install Pillow`, or return the export specification "
            "without claiming delivery completion."
        ) from PIL_IMPORT_ERROR


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
        return {
            "path": str(path),
            "format": image.format,
            "mode": image.mode,
            "width": width,
            "height": height,
            "square": width == height,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }


def inspect_images(paths: list[Path]) -> int:
    records = [image_record(path) for path in paths]
    print(json.dumps(records, ensure_ascii=False, indent=2))
    return 0 if all(record["square"] for record in records) else 2


def label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], value: str) -> None:
    font = ImageFont.load_default()
    draw.text(xy, value, fill=(235, 235, 235), font=font)


def prepare_square(image: Image.Image, size: int) -> Image.Image:
    return ImageOps.fit(image.convert("RGB"), (size, size), method=Image.Resampling.LANCZOS)


def contact_sheet(paths: list[Path], output: Path) -> None:
    require_pillow()
    cell = 256
    gap = 20
    label_height = 38
    rows = ["56 px", "128 px", "256 px", "grayscale", "blur"]
    width = gap + len(paths) * (cell + gap)
    height = gap + label_height + len(rows) * (cell + label_height + gap)
    sheet = Image.new("RGB", (width, height), (24, 24, 24))
    draw = ImageDraw.Draw(sheet)

    for column, path in enumerate(paths):
        x = gap + column * (cell + gap)
        label(draw, (x, gap), path.stem[:36])
        with Image.open(path) as opened:
            base = prepare_square(opened, cell)
        variants = [
            prepare_square(base, 56),
            prepare_square(base, 128),
            base,
            ImageOps.grayscale(base).convert("RGB"),
            base.filter(ImageFilter.GaussianBlur(radius=12)),
        ]
        for row, (row_name, variant) in enumerate(zip(rows, variants)):
            y = gap + label_height + row * (cell + label_height + gap)
            if column == 0:
                label(draw, (gap, y - 18), row_name)
            if variant.size != (cell, cell):
                px = x + (cell - variant.width) // 2
                py = y + (cell - variant.height) // 2
                sheet.paste(variant, (px, py))
            else:
                sheet.paste(variant, (x, y))

    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, format="PNG")
    print(json.dumps({"output": str(output), "sha256": sha256(output)}, indent=2))


def export_cover(source: Path, out_dir: Path, size: int, jpg_quality: int) -> None:
    require_pillow()
    with Image.open(source) as opened:
        width, height = opened.size
        if width != height:
            raise SystemExit(f"Source must be square; got {width}x{height}: {source}")
        master = opened.convert("RGBA").resize((size, size), Image.Resampling.LANCZOS)

    out_dir.mkdir(parents=True, exist_ok=True)
    png_path = out_dir / "cover-3000.png"
    jpg_path = out_dir / "cover-3000.jpg"
    thumb_path = out_dir / "thumbnail-256.png"
    master.save(png_path, format="PNG", optimize=True)
    rgb = Image.new("RGB", master.size, "white")
    rgb.paste(master, mask=master.getchannel("A"))
    rgb.save(jpg_path, format="JPEG", quality=jpg_quality, optimize=True, progressive=True)
    rgb.resize((256, 256), Image.Resampling.LANCZOS).save(thumb_path, format="PNG", optimize=True)

    result = {
        "source": image_record(source),
        "scaled": width != size,
        "outputs": [image_record(path) for path in (png_path, jpg_path, thumb_path)],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    subparsers = root.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser("inspect", help="Print image metadata and SHA-256")
    inspect_parser.add_argument("images", nargs="+", type=Path)

    sheet_parser = subparsers.add_parser("contact-sheet", help="Create 56/128/256/grayscale/blur comparison")
    sheet_parser.add_argument("images", nargs="+", type=Path)
    sheet_parser.add_argument("--output", required=True, type=Path)

    export_parser = subparsers.add_parser("export", help="Write distributor-ready square assets")
    export_parser.add_argument("source", type=Path)
    export_parser.add_argument("--out-dir", required=True, type=Path)
    export_parser.add_argument("--size", type=int, default=3000)
    export_parser.add_argument("--jpg-quality", type=int, default=95)

    return root


def main() -> int:
    args = parser().parse_args()
    if args.command == "inspect":
        return inspect_images(args.images)
    if args.command == "contact-sheet":
        contact_sheet(args.images, args.output)
        return 0
    if args.command == "export":
        if args.size <= 0 or not 1 <= args.jpg_quality <= 100:
            raise SystemExit("--size must be positive and --jpg-quality must be 1..100")
        export_cover(args.source, args.out_dir, args.size, args.jpg_quality)
        return 0
    raise AssertionError(args.command)


if __name__ == "__main__":
    sys.exit(main())
