#!/usr/bin/env python3
"""Create a delivery handoff manifest from a validated run contract."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image


def checksum(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""): digest.update(chunk)
    return digest.hexdigest()


def record(path: Path, role: str) -> dict[str, object]:
    if not path.is_file():
        raise ValueError(f"delivery-asset-missing:{role}")
    with Image.open(path) as image:
        width, height, mode = image.size[0], image.size[1], image.mode
    expected = {"thumbnail": 256, "cover-png": 3000, "cover-jpg": 3000}.get(role)
    if expected is not None and (width, height) != (expected, expected):
        raise ValueError(f"delivery-asset-size-invalid:{role}")
    return {"role": role, "path": str(path), "width": width, "height": height, "mode": mode, "sha256": checksum(path)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--contract", required=True, type=Path); parser.add_argument("--selected-candidate", required=True); parser.add_argument("--delivery-dir", required=True, type=Path); parser.add_argument("--output", required=True, type=Path); parser.add_argument("--human-text-status", choices=("passed", "failed", "unresolved"), required=True); parser.add_argument("--exact-title-confirmed", action="store_true"); parser.add_argument("--extra-readable-text-absent", action="store_true"); parser.add_argument("--observed-readable-text", action="append", default=[]); args = parser.parse_args()
    try: contract = json.loads(args.contract.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc: parser.error(f"contract unreadable: {exc}")
    candidates = {item.get("id"): item for item in contract.get("candidates", []) if isinstance(item, dict)}
    candidate = candidates.get(args.selected_candidate)
    if not candidate: parser.error("selected candidate is not in contract.candidates")
    directions = {item.get("id"): item for item in contract.get("directions", []) if isinstance(item, dict)}
    raw_source = Path(candidate.get("output_path", "")); source = raw_source if raw_source.is_absolute() else args.contract.parent / raw_source
    try:
        source_record = record(source, "source")
        assets = [record(args.delivery_dir / "cover-3000.png", "cover-png"), record(args.delivery_dir / "cover-3000.jpg", "cover-jpg"), record(args.delivery_dir / "thumbnail-256.png", "thumbnail")]
    except ValueError as exc:
        parser.error(str(exc))
    human = {"status": args.human_text_status, "exact_title_confirmed": args.exact_title_confirmed, "extra_readable_text_absent": args.extra_readable_text_absent, "observed_readable_text": args.observed_readable_text}
    complete = args.human_text_status == "passed" and args.exact_title_confirmed and args.extra_readable_text_absent
    manifest = {"schema_version": 1, "release": contract.get("release", {}), "runtime": contract.get("runtime", {}), "selected_candidate": {"id": candidate.get("id"), "direction": directions.get(candidate.get("direction_id"), {}), "source": source_record}, "delivery_assets": assets, "human_text_verification": human, "delivery_complete": complete}
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"); print(json.dumps({"status": "delivery-complete" if complete else "delivery-incomplete", "path": str(args.output)}, ensure_ascii=False)); return 0 if complete else 2


if __name__ == "__main__": raise SystemExit(main())
