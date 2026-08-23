#!/usr/bin/env python3
"""Maintain private, model-specific learning confidence for cover production."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def now() -> str: return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
def location(root: Path) -> Path:
    path = root.resolve() / ".album-cover-director" / "learning"; path.mkdir(parents=True, mode=0o700, exist_ok=True); return path / "model-evidence.json"
def confidence(success: int, total: int, validated: int) -> str:
    if total >= 6 and success / total >= 0.8 and validated >= 2: return "high"
    if total >= 3 and success / total >= 0.7 and validated >= 1: return "medium"
    return "low"

def effective_confidence(record: dict[str, object], as_of: datetime) -> str:
    value = str(record.get("confidence", "low")); timestamp = str(record.get("last_validated_at", ""))
    try: age = (as_of - datetime.fromisoformat(timestamp.replace("Z", "+00:00"))).days
    except ValueError: return "low"
    if age < 90 or value == "low": return value
    return "medium" if value == "high" else "low"

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); sub = parser.add_subparsers(dest="command", required=True)
    record_parser = sub.add_parser("record"); record_parser.add_argument("--artist-root", default="."); record_parser.add_argument("--rule-id", required=True); record_parser.add_argument("--model-family", required=True); record_parser.add_argument("--model-id", required=True); record_parser.add_argument("--host-surface", required=True); record_parser.add_argument("--outcome", choices=("success", "failure"), required=True); record_parser.add_argument("--user-validated", action="store_true")
    assess_parser = sub.add_parser("assess"); assess_parser.add_argument("--artist-root", default="."); assess_parser.add_argument("--as-of", default="")
    args = parser.parse_args()
    path = location(Path(args.artist_root)); document = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"schema_version": 1, "records": {}}
    if args.command == "assess":
        as_of = datetime.fromisoformat(args.as_of.replace("Z", "+00:00")) if args.as_of else datetime.now(timezone.utc)
        records = [{**record, "effective_confidence": effective_confidence(record, as_of)} for record in document["records"].values()]
        print(json.dumps({"status": "assessed", "records": records}, ensure_ascii=False, indent=2)); return 0
    key = "|".join((args.rule_id, args.model_family, args.model_id, args.host_surface)); record = document["records"].get(key, {"rule_id": args.rule_id, "model_family": args.model_family, "model_id": args.model_id, "host_surface": args.host_surface, "successes": 0, "trials": 0, "user_validations": 0, "validated_successes": 0})
    record["trials"] += 1; record["successes"] += int(args.outcome == "success"); record["user_validations"] += int(args.user_validated); record["validated_successes"] += int(args.user_validated and args.outcome == "success"); record["last_validated_at"] = now(); record["confidence"] = confidence(record["successes"], record["trials"], record["validated_successes"]); document["records"][key] = record
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"); print(json.dumps({"status": "recorded", "path": str(path), "record": record}, ensure_ascii=False)); return 0


if __name__ == "__main__": raise SystemExit(main())
