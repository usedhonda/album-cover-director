#!/usr/bin/env python3
"""Record artist-local cover feedback and promote repeated local preferences."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


LOCAL_DIR = ".album-cover-director"
SLUG = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")
GENERATED_START = "<!-- album-cover-director:generated:start -->"
GENERATED_END = "<!-- album-cover-director:generated:end -->"


def artist_root(raw_path: str) -> Path:
    root = Path(raw_path).expanduser().resolve()
    if not root.is_dir():
        raise ValueError("artist-root-unreadable")
    return root


def workspace(root: Path) -> Path:
    local = root / LOCAL_DIR
    local.mkdir(mode=0o700, exist_ok=True)
    (local / "feedback").mkdir(mode=0o700, exist_ok=True)
    return local


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path, fallback: object) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return fallback


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def preference_from(args: argparse.Namespace) -> dict[str, object] | None:
    if not args.preference_key:
        return None
    if not args.preference_statement:
        raise ValueError("preference-statement-required")
    return {
        "key": args.preference_key,
        "statement": args.preference_statement,
        "applies_when": args.applies_when,
        "reject_when": args.reject_when,
    }


def save_images(raw_paths: list[str], image_dir: Path, local: Path) -> list[str]:
    resolved = [Path(raw_path).expanduser().resolve() for raw_path in raw_paths]
    unreadable = [str(path) for path in resolved if not path.is_file()]
    if unreadable:
        raise ValueError("feedback-image-unreadable")
    image_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    saved = []
    for index, source in enumerate(resolved, start=1):
        destination = image_dir / f"{index:02d}-{source.name}"
        shutil.copy2(source, destination)
        saved.append(destination.relative_to(local).as_posix())
    return saved


def record(args: argparse.Namespace) -> dict[str, object]:
    if not SLUG.fullmatch(args.release_slug):
        raise ValueError("release-slug-invalid")
    root = artist_root(args.artist_root)
    local = workspace(root)
    release_dir = local / "feedback" / args.release_slug
    path = release_dir / "feedback.json"
    document = read_json(path, {"schema_version": 1, "release_slug": args.release_slug, "events": []})
    if not isinstance(document, dict) or not isinstance(document.get("events"), list):
        raise ValueError("feedback-record-invalid")
    event = {
        "recorded_at": now(),
        "selected_candidate_id": args.selected_candidate_id,
        "rejected_candidate_ids": args.rejected_candidate_id,
        "user_observations": args.observation,
        "failure_codes": args.failure_code,
        "saved_image_paths": save_images(args.image, release_dir / "images", local),
        "preference": preference_from(args),
        "runtime": {
            "model_family": args.model_family,
            "model_id": args.model_id,
            "host_surface": args.host_surface,
        },
        "user_validated": args.user_validated,
    }
    document["events"].append(event)
    write_json(path, document)
    summary = refresh(root)
    return {"status": "recorded", "feedback_path": str(path), "event": event, **summary}


def feedback_events(local: Path) -> list[tuple[str, dict[str, object]]]:
    events: list[tuple[str, dict[str, object]]] = []
    for path in sorted((local / "feedback").glob("*/feedback.json")):
        document = read_json(path, {})
        if not isinstance(document, dict):
            continue
        release_slug = document.get("release_slug")
        for event in document.get("events", []):
            if isinstance(release_slug, str) and isinstance(event, dict):
                events.append((release_slug, event))
    return events


def render_preferences(local: Path) -> dict[str, object]:
    grouped: dict[str, list[tuple[str, dict[str, object]]]] = defaultdict(list)
    for release_slug, event in feedback_events(local):
        preference = event.get("preference")
        if event.get("user_validated") is True and isinstance(preference, dict) and isinstance(preference.get("key"), str):
            grouped[preference["key"]].append((release_slug, preference))

    promoted = []
    for key, values in grouped.items():
        release_slugs = sorted({slug for slug, _ in values})
        if len(release_slugs) < 3:
            continue
        latest = values[-1][1]
        statement = latest.get("statement")
        if not isinstance(statement, str) or not statement:
            continue
        applies = "; ".join(latest.get("applies_when", [])) or "only when supported by the current release brief"
        reject = "; ".join(latest.get("reject_when", [])) or "do not force this onto unrelated releases"
        promoted.append({
            "key": key,
            "statement": statement,
            "release_slugs": release_slugs,
            "applies_when": applies,
            "reject_when": reject,
        })

    path = local / "feedback" / "learned-preferences.md"
    existing = path.read_text(encoding="utf-8") if path.exists() else "# Learned preferences\n\n"
    manual = existing.split(GENERATED_START, 1)[0].rstrip()
    if not manual:
        manual = "# Learned preferences"
    lines = [manual, "", GENERATED_START, "## Repeated feedback", ""]
    if promoted:
        for item in promoted:
            lines.extend([
                f"- **{item['statement']}**",
                f"  - Evidence: {', '.join(item['release_slugs'])}",
                f"  - Applies when: {item['applies_when']}",
                f"  - Reject when: {item['reject_when']}",
            ])
    else:
        lines.append("No preference has repeated across three releases yet.")
    lines.extend(["", GENERATED_END, ""])
    path.write_text("\n".join(lines), encoding="utf-8")
    return {"learned_preferences_path": str(path), "promoted_preference_keys": [item["key"] for item in promoted]}


def refresh(root: Path) -> dict[str, object]:
    return render_preferences(workspace(root))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    record_parser = subparsers.add_parser("record")
    record_parser.add_argument("--artist-root", default=".")
    record_parser.add_argument("--release-slug", required=True)
    record_parser.add_argument("--selected-candidate-id")
    record_parser.add_argument("--rejected-candidate-id", action="append", default=[])
    record_parser.add_argument("--observation", action="append", default=[])
    record_parser.add_argument("--failure-code", action="append", default=[])
    record_parser.add_argument("--image", action="append", default=[])
    record_parser.add_argument("--preference-key")
    record_parser.add_argument("--preference-statement")
    record_parser.add_argument("--applies-when", action="append", default=[])
    record_parser.add_argument("--reject-when", action="append", default=[])
    record_parser.add_argument("--model-family", default="")
    record_parser.add_argument("--model-id", default="")
    record_parser.add_argument("--host-surface", default="")
    record_parser.add_argument("--user-validated", action="store_true")
    refresh_parser = subparsers.add_parser("refresh")
    refresh_parser.add_argument("--artist-root", default=".")
    args = parser.parse_args()
    try:
        result = record(args) if args.command == "record" else refresh(artist_root(args.artist_root))
    except ValueError as exc:
        print(json.dumps({"status": "error", "reason": str(exc)}))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
