#!/usr/bin/env python3
"""Initialize or inspect a private project-local Album Cover Director workspace."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


LOCAL_DIR = ".album-cover-director"
DIRECTORIES = ("feedback", "learning-images", "reference-inbox", "observations", "benchmarks")
TEMPLATES = {
    "artist-system.md": """# Artist system\n\nStable identity, recurring constraints, and what must remain recognisable.\nKeep release-specific ideas in the release brief, not here.\n""",
    "learned-preferences.md": """# Learned preferences\n\nPrivate, project-local observations promoted from repeated feedback.\nEach entry must name its evidence and boundary; do not copy a one-off preference here.\n""",
    "feedback/README.md": """# Feedback records\n\nOne YAML record per reviewed release. Use the skill's `assets/project-feedback.yaml` contract.\n""",
    "benchmarks/title-integrity-v1.yaml": """schema_version: 1\nsuite: title-integrity-v1\nstatus: not-run\nprivacy: project-local\ncases:\n  - id: short-latin\n    title: SILT\n    title_profile: compact-single-script\n  - id: japanese\n    title: 夜の余白\n    title_profile: compact-japanese\n  - id: mixed-script\n    title: 透明なSignal\n    title_profile: mixed-script-hierarchy\n  - id: long-title\n    title: A SMALL ROOM FULL OF WEATHER\n    title_profile: multi-unit-hierarchy\n""",
}


def root_for(raw_path: str) -> Path:
    root = Path(raw_path).expanduser().resolve()
    if not root.is_dir():
        raise ValueError("project-root-unreadable")
    return root


def local_paths(root: Path) -> dict[str, str]:
    local = root / LOCAL_DIR
    return {
        "root": str(local),
        "artist_system": str(local / "artist-system.md"),
        "learned_preferences": str(local / "learned-preferences.md"),
        "feedback": str(local / "feedback"),
        "learning_images": str(local / "learning-images"),
        "reference_inbox": str(local / "reference-inbox"),
        "observations": str(local / "observations"),
        "benchmarks": str(local / "benchmarks"),
    }


def initialize(root: Path) -> dict[str, object]:
    local = root / LOCAL_DIR
    local.mkdir(mode=0o700, exist_ok=True)
    for directory in DIRECTORIES:
        (local / directory).mkdir(mode=0o700, exist_ok=True)
    ignore = local / ".gitignore"
    if not ignore.exists():
        ignore.write_text("*\n!.gitignore\n", encoding="utf-8")
    created = []
    for relative, contents in TEMPLATES.items():
        target = local / relative
        if not target.exists():
            target.write_text(contents, encoding="utf-8")
            created.append(relative)
    return {"status": "initialized", "created": created, "paths": local_paths(root)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("init", "paths"):
        child = subparsers.add_parser(command)
        child.add_argument("--project-root", default=".")
    args = parser.parse_args()
    try:
        root = root_for(args.project_root)
    except ValueError as exc:
        print(json.dumps({"status": "error", "reason": str(exc)}))
        return 2
    result = initialize(root) if args.command == "init" else {"status": "ok", "paths": local_paths(root)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
