#!/usr/bin/env python3
"""Start production from selected, visually reviewed concept previews."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image

from concept_contract import DONOR_AXES, PREVIEW, PRODUCTION, checksum, failure, resolve_asset, validate, validate_review


def select(contract: dict, contract_path: Path, candidate_ids: list[str], reason: str, donor_id: str | None = None, donor_traits: list[str] | None = None) -> dict:
    if contract.get("schema_version") != 2 or contract.get("stage") != PREVIEW:
        raise ValueError("selection-requires-concept-preview")
    if not candidate_ids or len(set(candidate_ids)) != len(candidate_ids):
        raise ValueError("selection-ids-must-be-unique")
    if not reason.strip():
        raise ValueError("selection-reason-required")
    traits: list[dict[str, str]] = []
    if bool(donor_id) != bool(donor_traits):
        raise ValueError("donor-and-scoped-trait-required-together")
    if donor_id and (len(candidate_ids) != 1 or donor_id in candidate_ids):
        raise ValueError("donor-needs-one-distinct-primary-candidate")
    for value in donor_traits or []:
        axis, separator, instruction = value.partition(":")
        if not separator or axis not in DONOR_AXES or not instruction.strip():
            raise ValueError("donor-trait-must-be-color-lighting-or-texture-with-an-instruction")
        traits.append({"axis": axis, "instruction": instruction.strip()})
    candidates = {item["id"]: item for item in contract["candidates"]}
    missing = [candidate_id for candidate_id in candidate_ids + ([donor_id] if donor_id else []) if candidate_id not in candidates]
    if missing:
        raise ValueError(f"selection-candidate-not-found: {', '.join(missing)}")
    direction_map = {item["id"]: item for item in contract["directions"]}
    review_map = {item["id"]: item for item in contract["diversity_review"]["reviewed_candidates"]}
    sources: list[dict] = []
    donors: list[dict] = []
    directions: list[dict] = []
    included: set[str] = set()
    minimum = contract["runtime"]["capability_profile"]["preview_minimum_dimension"]
    for candidate_id in candidate_ids + ([donor_id] if donor_id else []):
        candidate = candidates[candidate_id]
        direction = direction_map[candidate["direction_id"]]
        path = resolve_asset(contract_path, candidate["output_path"])
        with Image.open(path) as image:
            if image.width != image.height or image.width < minimum:
                raise ValueError(f"selection-preview-size-invalid: {candidate_id}")
            image.verify()
        digest = checksum(path)
        if digest != review_map[candidate_id]["sha256"].lower():
            raise ValueError(f"selection-preview-changed: {candidate_id}")
        if candidate_id == donor_id:
            donors.append({
                "candidate_id": candidate_id, "direction_id": direction["id"],
                "source_path": str(path), "source_sha256": digest, "traits": traits,
                "direction_snapshot": copy.deepcopy(direction),
                "interpretation_snapshot": copy.deepcopy(next(item for item in contract["interpretations"] if item["id"] == direction["interpretation_id"])),
            })
            continue
        sources.append({
            "candidate_id": candidate_id,
            "direction_id": direction["id"],
            "source_path": str(path),
            "source_sha256": digest,
            "reason": reason,
            "visual_mechanism": direction["visual_mechanism"],
            "preserve_in_production": copy.deepcopy(direction["preserve_in_production"]),
            "planned_signature": copy.deepcopy(direction["planned_signature"]),
            "preview_prompt_path": str(resolve_asset(contract_path, direction["prompt_path"])),
        })
        if direction["id"] not in included:
            selected_direction = copy.deepcopy(direction)
            selected_direction["prompt_path"] = f"prompts/production-{len(directions) + 1:02d}.md"
            directions.append(selected_direction)
            included.add(direction["id"])
    production = copy.deepcopy(contract)
    production["stage"] = PRODUCTION
    production["directions"] = directions
    used_interpretations = {direction["interpretation_id"] for direction in directions}
    production["interpretations"] = [item for item in production["interpretations"] if item["id"] in used_interpretations]
    production["candidates"] = []
    production.pop("diversity_review", None)
    production["selection"] = {
        "source_contract_path": str(contract_path.resolve()),
        "source_contract_sha256": checksum(contract_path),
        "selected_candidate_ids": candidate_ids,
        "reason": reason,
        "selected_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "review_basis": "recorded-visual-review-bound-to-image-hashes",
        "sources": sources,
    }
    if donors:
        production["selection"]["donors"] = donors
    return production


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", required=True, type=Path)
    parser.add_argument("--candidate", required=True, action="append", dest="candidate_ids", help="A stable preview candidate ID; repeat to select more than one.")
    parser.add_argument("--reason", required=True, help="Why these concepts were selected and what must survive finishing.")
    parser.add_argument("--donor", help="One different preview whose scoped color, lighting, or texture may inform the primary candidate.")
    parser.add_argument("--donor-trait", action="append", help="A scoped trait, such as lighting:soft side light; repeat for more traits. Requires exactly one primary candidate.")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        raw = args.contract.read_bytes()
        contract = json.loads(raw)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "fail", "failures": [failure("contract-unreadable", "contract", str(exc))]}))
        return 2
    failures = validate(contract)
    if not failures:
        if contract.get("schema_version") != 2 or contract.get("stage") != PREVIEW:
            failures.append(failure("selection-requires-concept-preview", "stage", "Select from a schema 2 concept-preview contract."))
        else:
            failures.extend(validate_review(contract, args.contract))
    if failures:
        print(json.dumps({"status": "fail", "failures": failures}, ensure_ascii=False, indent=2))
        return 2
    try:
        if args.output.resolve() == args.contract.resolve():
            raise ValueError("selection-output-would-overwrite-preview-contract")
        production = select(contract, args.contract, args.candidate_ids, args.reason, args.donor, args.donor_trait)
        if checksum(args.contract) != hashlib.sha256(raw).hexdigest():
            raise ValueError("preview-contract-changed-during-selection")
        failures = validate(production)
        if failures:
            print(json.dumps({"status": "fail", "failures": failures}, ensure_ascii=False, indent=2))
            return 2
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(json.dumps(production, ensure_ascii=False, indent=2) + "\n")
    except (OSError, ValueError, Image.DecompressionBombError) as exc:
        print(json.dumps({"status": "fail", "failures": [failure("selection-failed", "selection", str(exc))]}, ensure_ascii=False))
        return 2
    print(json.dumps({"status": "production-contract-created", "path": str(args.output), "selected_candidate_ids": args.candidate_ids, "directions": [item["id"] for item in production["directions"]], "production_images_generated": False}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
