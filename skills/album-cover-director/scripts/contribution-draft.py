#!/usr/bin/env python3
"""Prepare and validate privacy-safe public title-behavior contribution drafts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


LOCAL_DIR = ".album-cover-director"
SLUG = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")
UNSAFE_TEXT = re.compile(
    r"(?:^~|^/|[A-Za-z]:\\\\|/" + "Users" + r"/|\\.album-cover-director|artist-system\\.md|"
    r"\.(?:png|jpe?g|gif|webp|tiff?)\b)",
    re.IGNORECASE,
)


def fail(reason: str) -> None:
    raise ValueError(reason)


def artist_root(raw_path: str) -> Path:
    root = Path(raw_path).expanduser().resolve()
    if not root.is_dir():
        fail("artist-root-unreadable")
    return root


def safe_slug(value: str, field: str) -> str:
    if not SLUG.fullmatch(value):
        fail(f"{field}-invalid")
    return value


def safe_text(value: str, field: str) -> str:
    value = value.strip()
    if not value:
        fail(f"{field}-required")
    if UNSAFE_TEXT.search(value):
        fail(f"{field}-contains-private-or-image-reference")
    return value


def safe_texts(values: list[str], field: str, required: bool = True) -> list[str]:
    cleaned = [safe_text(value, field) for value in values]
    if required and not cleaned:
        fail(f"{field}-required")
    return cleaned


def card_from(args: argparse.Namespace) -> dict[str, object]:
    if args.private_trial_count < 0:
        fail("private-trial-count-invalid")
    if args.held_out_brief_passed and args.private_trial_count < 1:
        fail("held-out-brief-requires-trial")
    if args.held_out_brief_passed and not args.rights_safe:
        fail("held-out-brief-requires-rights-safe")
    return {
        "schema_version": 1,
        "card": {
            "id": safe_slug(args.card_id, "card-id"),
            "title_behavior": safe_text(args.title_behavior, "title-behavior"),
            "use_when": safe_texts(args.use_when, "use-when"),
            "do_not_use_when": safe_texts(args.do_not_use_when, "do-not-use-when"),
            "title_system_family": args.title_system_family,
            "world_engine": safe_text(args.world_engine, "world-engine"),
            "construction_logic": safe_texts(args.construction_logic, "construction-logic"),
            "protected_title_properties": {
                "occupied_area": safe_text(args.occupied_area, "occupied-area"),
                "silhouette": safe_text(args.silhouette, "silhouette"),
                "reading_route": safe_text(args.reading_route, "reading-route"),
                "value_priority": safe_text(args.value_priority, "value-priority"),
            },
            "prompt_requirements": safe_texts(args.prompt_requirement, "prompt-requirement"),
            "rejection_tests": safe_texts(args.rejection_test, "rejection-test"),
            "evidence_summary": {
                "private_trial_count": args.private_trial_count,
                "condition_categories": safe_texts(args.condition_category, "condition-category", required=False),
                "held_out_brief_passed": args.held_out_brief_passed,
            },
            "rights_safe": args.rights_safe,
        },
    }


def render_note(card: dict[str, object]) -> str:
    details = card["card"]
    evidence = details["evidence_summary"]
    gate_met = (details["rights_safe"] and evidence["private_trial_count"] >= 3
                and len(evidence["condition_categories"]) >= 2
                and evidence["held_out_brief_passed"])
    status = "eligible for public review" if gate_met else "needs more private evidence before public review"
    return "\n".join([
        "# Public contribution draft", "", f"Status: **{status}**.", "",
        "This package contains an abstract behavior card only. It contains no release title, artist system, lyrics, prompt, local feedback, images, paths, or trial IDs.", "",
        "Review `title-behavior-card.yaml` before sharing it. This command performed no upload, issue creation, branch creation, or pull request.", "",
        "To submit it later, copy only these two draft files into an Issue or pull request and follow CONTRIBUTING.md.", "",
    ])


def prepare(args: argparse.Namespace) -> dict[str, object]:
    root = artist_root(args.artist_root)
    release_slug = safe_slug(args.release_slug, "release-slug")
    card = card_from(args)
    draft_dir = root / LOCAL_DIR / "feedback" / release_slug / "contribution-drafts" / card["card"]["id"]
    draft_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    card_path = draft_dir / "title-behavior-card.yaml"
    note_path = draft_dir / "README.md"
    card_path.write_text(json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    note_path.write_text(render_note(card), encoding="utf-8")
    return {"status": "prepared", "draft_dir": str(draft_dir), "files": [str(card_path), str(note_path)], "network_action": "none"}


def validate(args: argparse.Namespace) -> dict[str, object]:
    draft_dir = Path(args.draft_dir).expanduser().resolve()
    if not draft_dir.is_dir():
        fail("draft-dir-unreadable")
    expected = {"title-behavior-card.yaml", "README.md"}
    found = {path.name for path in draft_dir.iterdir() if path.is_file()}
    if found != expected:
        fail("draft-files-invalid")
    payload = json.loads((draft_dir / "title-behavior-card.yaml").read_text(encoding="utf-8"))
    card = payload.get("card") if isinstance(payload, dict) else None
    if not isinstance(card, dict):
        fail("draft-card-invalid")
    safe_slug(str(card.get("id", "")), "card-id")
    safe_text(str(card.get("title_behavior", "")), "title-behavior")
    if card.get("rights_safe") is not True:
        fail("draft-rights-not-confirmed")
    return {"status": "valid", "draft_dir": str(draft_dir), "network_action": "none"}


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)
    prepare_parser = commands.add_parser("prepare")
    prepare_parser.add_argument("--artist-root", default=".")
    prepare_parser.add_argument("--release-slug", required=True)
    prepare_parser.add_argument("--card-id", required=True)
    prepare_parser.add_argument("--title-behavior", required=True)
    prepare_parser.add_argument("--title-system-family", choices=("material-world", "spatial-field", "character-led"), required=True)
    prepare_parser.add_argument("--world-engine", required=True)
    prepare_parser.add_argument("--use-when", action="append", default=[])
    prepare_parser.add_argument("--do-not-use-when", action="append", default=[])
    prepare_parser.add_argument("--construction-logic", action="append", default=[])
    prepare_parser.add_argument("--occupied-area", required=True)
    prepare_parser.add_argument("--silhouette", required=True)
    prepare_parser.add_argument("--reading-route", required=True)
    prepare_parser.add_argument("--value-priority", required=True)
    prepare_parser.add_argument("--prompt-requirement", action="append", default=[])
    prepare_parser.add_argument("--rejection-test", action="append", default=[])
    prepare_parser.add_argument("--private-trial-count", type=int, default=0)
    prepare_parser.add_argument("--condition-category", action="append", default=[])
    prepare_parser.add_argument("--held-out-brief-passed", action="store_true")
    prepare_parser.add_argument("--rights-safe", action="store_true")
    validate_parser = commands.add_parser("validate")
    validate_parser.add_argument("--draft-dir", required=True)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        result = prepare(args) if args.command == "prepare" else validate(args)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "reason": str(exc)}))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
