#!/usr/bin/env python3
"""Create a delivery handoff manifest from a validated run contract."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def checksum(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""): digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--contract", required=True, type=Path); parser.add_argument("--selected-candidate", required=True); parser.add_argument("--delivery-dir", required=True, type=Path); parser.add_argument("--output", required=True, type=Path); args = parser.parse_args()
    try: contract = json.loads(args.contract.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc: parser.error(f"contract unreadable: {exc}")
    candidates = {item.get("id"): item for item in contract.get("candidates", []) if isinstance(item, dict)}
    candidate = candidates.get(args.selected_candidate)
    if not candidate: parser.error("selected candidate is not in contract.candidates")
    directions = {item.get("id"): item for item in contract.get("directions", []) if isinstance(item, dict)}
    output_path = Path(candidate.get("output_path", ""))
    output = {"path": str(output_path), "sha256": checksum(output_path) if output_path.is_file() else None}
    manifest = {"schema_version": 1, "release": contract.get("release", {}), "runtime": contract.get("runtime", {}), "selected_candidate": {"id": candidate.get("id"), "direction": directions.get(candidate.get("direction_id"), {}), "output": output}, "delivery_directory": str(args.delivery_dir), "verification": {"objective_preflight": candidate.get("objective_preflight", {}), "text_verification": "human_required"}}
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"); print(json.dumps({"status": "written", "path": str(args.output)}, ensure_ascii=False)); return 0


if __name__ == "__main__": raise SystemExit(main())
