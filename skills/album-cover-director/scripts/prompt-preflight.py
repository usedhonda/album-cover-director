#!/usr/bin/env python3
"""Validate a release-local preview or production contract before generation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from concept_contract import FAMILIES, PATTERNS, failure, validate


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", required=True, type=Path)
    args = parser.parse_args()
    try:
        contract = json.loads(args.contract.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "fail", "failures": [failure("contract-unreadable", "contract", str(exc))]}))
        return 2
    failures = validate(contract)
    print(json.dumps({"status": "pass" if not failures else "fail", "failures": failures}, ensure_ascii=False, indent=2))
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
