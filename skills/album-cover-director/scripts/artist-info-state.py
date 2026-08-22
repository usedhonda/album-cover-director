#!/usr/bin/env python3
"""Resolve an explicit or project-local Album Cover Director artist system."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


LOCAL_DIR = ".album-cover-director"
ARTIST_SYSTEM = "artist-system.md"


def readable_file(raw_path: str) -> Path | None:
    path = Path(raw_path).expanduser().resolve()
    if path.is_file() and os.access(path, os.R_OK):
        return path
    return None


def project_root(raw_path: str) -> Path | None:
    path = Path(raw_path).expanduser().resolve()
    return path if path.is_dir() else None


def emit(**payload: object) -> None:
    print(json.dumps(payload, ensure_ascii=False))


def resolve(explicit_path: str | None, raw_project_root: str, ignore_project_local: bool) -> int:
    root = project_root(raw_project_root)
    if root is None:
        emit(source="none", path=None, reason="project-root-unreadable")
        return 2

    if explicit_path:
        resolved = readable_file(explicit_path)
        if resolved is None:
            emit(source="none", path=None, reason="explicit-path-unreadable")
            return 2
        emit(source="explicit", path=str(resolved), reason=None)
        return 0

    if ignore_project_local:
        emit(source="none", path=None, reason="project-local-ignored")
        return 0

    local_system = readable_file(str(root / LOCAL_DIR / ARTIST_SYSTEM))
    if local_system is None:
        emit(source="none", path=None, reason="no-project-local-artist-system")
        return 0
    emit(source="project-local", path=str(local_system), reason=None)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    resolve_parser = subparsers.add_parser("resolve")
    resolve_parser.add_argument("--artist-system")
    resolve_parser.add_argument("--project-root", default=".")
    resolve_parser.add_argument("--ignore-project-local", action="store_true")
    args = parser.parse_args()
    return resolve(args.artist_system, args.project_root, args.ignore_project_local)


if __name__ == "__main__":
    raise SystemExit(main())
