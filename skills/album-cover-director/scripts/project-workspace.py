#!/usr/bin/env python3
"""Initialize or inspect a private artist-local Album Cover Director workspace."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


LOCAL_DIR = ".album-cover-director"
DIRECTORIES = ("feedback",)
TEMPLATES = {
    "artist-system.md": """# Artist system\n\n## Identity in one sentence\n\nWrite a working description of the artist's musical and visual point of view. It may be incomplete at first.\n\n## What should remain recognisable\n\n- Recurring identity, character, or viewpoint:\n- Emotional or sonic territory:\n- Title-design behavior worth preserving:\n\n## What must vary release to release\n\n- Scene, action, camera, and dominant geometry:\n- Palette, light, and material:\n- Title-system family or title behavior:\n\n## Avoid\n\n-\n\n## Evidence and change log\n\nRecord only repeated, artist-wide observations. Link each entry to local feedback release slugs and state when it should not apply.\n""",
    "feedback/learned-preferences.md": """# Learned preferences\n\nPrivate, artist-local observations promoted from repeated feedback.\nEach entry must name its evidence and boundary; do not copy a one-off preference here.\n""",
}


def root_for(raw_path: str) -> Path:
    root = Path(raw_path).expanduser().resolve()
    if not root.is_dir():
        raise ValueError("artist-root-unreadable")
    return root


def local_paths(root: Path) -> dict[str, str]:
    local = root / LOCAL_DIR
    return {
        "root": str(local),
        "artist_system": str(local / "artist-system.md"),
        "learned_preferences": str(local / "feedback/learned-preferences.md"),
        "feedback": str(local / "feedback"),
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
        child.add_argument("--artist-root", default=".")
    args = parser.parse_args()
    try:
        root = root_for(args.artist_root)
    except ValueError as exc:
        print(json.dumps({"status": "error", "reason": str(exc)}))
        return 2
    result = initialize(root) if args.command == "init" else {"status": "ok", "paths": local_paths(root)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
