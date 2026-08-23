#!/usr/bin/env python3
"""Validate a release-local run contract before image generation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


FAMILIES = {"material-world", "spatial-field", "character-led"}


def failure(code: str, path: str, message: str) -> dict[str, str]:
    return {"code": code, "path": path, "message": message}


def validate(contract: object) -> list[dict[str, str]]:
    if not isinstance(contract, dict):
        return [failure("contract-invalid", "$", "Contract must be a JSON object.")]
    failures: list[dict[str, str]] = []
    release = contract.get("release")
    if not isinstance(release, dict) or not isinstance(release.get("exact_title"), str) or not release["exact_title"].strip():
        failures.append(failure("title-required", "release.exact_title", "An exact release title is required."))
        title = ""
    else:
        title = release["exact_title"].strip()
    allowed = release.get("allowed_readable_text") if isinstance(release, dict) else None
    if not isinstance(allowed, list) or not all(isinstance(value, str) and value.strip() for value in allowed):
        failures.append(failure("allowed-text-invalid", "release.allowed_readable_text", "Allowed readable text must be a non-empty string list."))
    elif title and title not in allowed:
        failures.append(failure("title-not-allowed", "release.allowed_readable_text", "The exact title must be explicitly allowed."))
    constraints = contract.get("constraints")
    if not isinstance(constraints, dict) or constraints.get("title_must_be_image_native") is not True:
        failures.append(failure("image-native-title-required", "constraints.title_must_be_image_native", "The title must be image-native."))
    if not isinstance(constraints, dict) or constraints.get("post_typesetting_allowed") is not False:
        failures.append(failure("post-typesetting-prohibited", "constraints.post_typesetting_allowed", "Post-typesetting must remain disabled."))
    rights = contract.get("rights")
    if not isinstance(rights, dict) or not isinstance(rights.get("reference_basis"), str) or not rights["reference_basis"].strip():
        failures.append(failure("rights-basis-required", "rights.reference_basis", "Record the reference or asset rights basis."))
    directions = contract.get("directions")
    if not isinstance(directions, list) or len(directions) != 3:
        failures.append(failure("three-directions-required", "directions", "Exactly three structurally distinct directions are required."))
        return failures
    patterns: set[str] = set()
    for index, direction in enumerate(directions):
        base = f"directions[{index}]"
        if not isinstance(direction, dict):
            failures.append(failure("direction-invalid", base, "Each direction must be an object.")); continue
        pattern, family = direction.get("primary_pattern"), direction.get("title_system_family")
        if not isinstance(pattern, str) or not pattern.strip(): failures.append(failure("primary-pattern-required", f"{base}.primary_pattern", "Provide one primary pattern."))
        elif pattern in patterns: failures.append(failure("primary-pattern-duplicate", f"{base}.primary_pattern", "Primary patterns must differ."))
        else: patterns.add(pattern)
        if family not in FAMILIES: failures.append(failure("title-family-invalid", f"{base}.title_system_family", "Use material-world, spatial-field, or character-led.")); continue
        if family == "material-world" and not (direction.get("world_engine") and direction.get("title_anatomy")):
            failures.append(failure("material-direction-incomplete", base, "Material directions require world_engine and title_anatomy."))
        if family == "spatial-field" and not direction.get("world_engine"):
            failures.append(failure("spatial-direction-incomplete", base, "Spatial directions require world_engine."))
        if family == "character-led" and not direction.get("character_title_relation"):
            failures.append(failure("character-direction-incomplete", base, "Character directions require character_title_relation."))
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--contract", required=True, type=Path); args = parser.parse_args()
    try: contract = json.loads(args.contract.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc: print(json.dumps({"status": "fail", "failures": [failure("contract-unreadable", "contract", str(exc))]})); return 2
    failures = validate(contract); print(json.dumps({"status": "pass" if not failures else "fail", "failures": failures}, ensure_ascii=False, indent=2)); return 0 if not failures else 2


if __name__ == "__main__": raise SystemExit(main())
