#!/usr/bin/env python3
"""Create a delivery handoff manifest from a production run contract."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path

from PIL import Image

from concept_contract import PREVIEW, PRODUCTION, checksum, failure, resolve_asset, validate, validate_selection_sources


def record(path: Path, role: str) -> dict[str, object]:
    if not path.is_file():
        raise ValueError(f"delivery-asset-missing:{role}")
    with Image.open(path) as image:
        width, height, mode, image_format = image.width, image.height, image.mode, image.format
        image.verify()
    expected = {"thumbnail": 256, "cover-png": 3000, "cover-jpg": 3000}.get(role)
    if expected is not None and (width, height) != (expected, expected):
        raise ValueError(f"delivery-asset-size-invalid:{role}")
    if width != height:
        raise ValueError(f"delivery-asset-not-square:{role}")
    if mode not in {"RGB", "RGBA"} or (role == "cover-jpg" and mode != "RGB"):
        raise ValueError(f"delivery-asset-color-mode-invalid:{role}")
    formats = {"thumbnail": "PNG", "cover-png": "PNG", "cover-jpg": "JPEG"}
    if role in formats and image_format != formats[role]:
        raise ValueError(f"delivery-asset-format-invalid:{role}")
    return {"role": role, "path": str(path.resolve()), "width": width, "height": height, "mode": mode, "format": image_format, "sha256": checksum(path)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", required=True, type=Path)
    parser.add_argument("--selected-candidate", required=True)
    parser.add_argument("--delivery-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--human-text-status", choices=("passed", "failed", "unresolved"), required=True)
    parser.add_argument("--exact-title-confirmed", action="store_true")
    parser.add_argument("--extra-readable-text-absent", action="store_true")
    parser.add_argument("--observed-readable-text", action="append", default=[])
    args = parser.parse_args()
    try:
        contract = json.loads(args.contract.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        parser.error(f"contract unreadable: {exc}")
    if isinstance(contract, dict) and contract.get("stage") == PREVIEW:
        parser.error("concept-preview-is-not-deliverable: select a concept and create a production-candidate contract first")
    failures = validate(contract)
    if not failures:
        failures.extend(validate_selection_sources(contract))
    if failures:
        print(json.dumps({"status": "fail", "failures": failures}, ensure_ascii=False, indent=2))
        return 2
    raw_candidates = contract.get("candidates")
    if not isinstance(raw_candidates, list):
        parser.error("contract.candidates must be a list")
    candidates: dict[str, dict] = {}
    for item in raw_candidates:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"] or item["id"] in candidates:
            parser.error("candidate IDs must be non-empty and unique")
        candidates[item["id"]] = item
    candidate = candidates.get(args.selected_candidate)
    if candidate is None:
        parser.error("selected candidate is not in contract.candidates")
    directions = {item["id"]: item for item in contract["directions"]}
    if not isinstance(candidate.get("direction_id"), str) or candidate["direction_id"] not in directions:
        parser.error("selected candidate has no valid direction")
    if not isinstance(candidate.get("output_path"), str) or not candidate["output_path"].strip():
        parser.error("selected candidate has no source image path")
    try:
        source = resolve_asset(args.contract, candidate["output_path"])
        source_record = record(source, "source")
        minimum = contract["runtime"]["capability_profile"]["source_minimum_dimension"]
        if source_record["width"] < minimum:
            raise ValueError("production-source-below-minimum-size")
        if candidate.get("sha256") is not None and candidate["sha256"] != source_record["sha256"]:
            raise ValueError("production-source-changed")
        assets = [
            record(args.delivery_dir / "cover-3000.png", "cover-png"),
            record(args.delivery_dir / "cover-3000.jpg", "cover-jpg"),
            record(args.delivery_dir / "thumbnail-256.png", "thumbnail"),
        ]
        protected_paths = {args.contract.resolve(), source.resolve(), *(Path(asset["path"]) for asset in assets)}
        for item in candidates.values():
            if isinstance(item.get("output_path"), str) and item["output_path"].strip():
                protected_paths.add(resolve_asset(args.contract, item["output_path"]))
        selection = contract.get("selection")
        if isinstance(selection, dict):
            protected_paths.add(Path(selection["source_contract_path"]).resolve())
            for item in selection["sources"] + selection.get("donors", []):
                protected_paths.add(Path(item["source_path"]).resolve())
        aliases_input = args.output.resolve() in protected_paths
        if args.output.exists():
            aliases_input = aliases_input or any(path.exists() and args.output.samefile(path) for path in protected_paths)
        if aliases_input:
            raise ValueError("handoff-output-would-overwrite-input")
    except (OSError, ValueError, Image.DecompressionBombError) as exc:
        parser.error(str(exc))
    title = contract["release"]["exact_title"]
    allowed = contract["release"]["allowed_readable_text"]
    observed_matches = not args.observed_readable_text or (
        args.observed_readable_text.count(title) == 1
        and all(value in allowed for value in args.observed_readable_text)
    )
    human = {
        "status": args.human_text_status,
        "exact_title_confirmed": args.exact_title_confirmed,
        "extra_readable_text_absent": args.extra_readable_text_absent,
        "observed_readable_text": args.observed_readable_text,
        "observed_text_matches_contract": observed_matches,
    }
    complete = args.human_text_status == "passed" and args.exact_title_confirmed and args.extra_readable_text_absent and observed_matches
    selected = {"id": candidate["id"], "direction": directions[candidate["direction_id"]], "source": source_record}
    if "preview_candidate_id" in candidate:
        selected["preview_candidate_id"] = candidate["preview_candidate_id"]
    manifest = {
        "schema_version": contract.get("schema_version", 1),
        "stage": PRODUCTION,
        "release": contract["release"],
        "runtime": contract["runtime"],
        "source_contract": {"path": str(args.contract.resolve()), "sha256": checksum(args.contract)},
        "selected_candidate": selected,
        "delivery_assets": assets,
        "human_text_verification": human,
        "delivery_complete": complete,
    }
    if "selection" in contract:
        manifest["selection"] = contract["selection"]
    temporary_path: Path | None = None
    try:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", prefix=f".{args.output.name}.", suffix=".tmp", dir=args.output.parent, delete=False) as handle:
            temporary_path = Path(handle.name)
            handle.write(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, args.output)
    except OSError as exc:
        parser.error(f"manifest-write-failed: {exc}")
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    print(json.dumps({"status": "delivery-complete" if complete else "delivery-incomplete", "path": str(args.output)}, ensure_ascii=False))
    return 0 if complete else 2


if __name__ == "__main__":
    raise SystemExit(main())
