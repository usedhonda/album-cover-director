#!/usr/bin/env python3
"""Remember or resolve only Album Cover Director's last artist-info file path."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path


def state_path() -> Path:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    return codex_home / "album-cover-director" / "state.yaml"


def readable_file(raw_path: str) -> Path | None:
    path = Path(raw_path).expanduser().resolve()
    if path.is_file() and os.access(path, os.R_OK):
        return path
    return None


def load_state(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    remembered = value.get("last_artist_information_path")
    if isinstance(remembered, str):
        return {"last_artist_information_path": remembered}
    return {}


def save_path(path: Path, artist_info: Path) -> None:
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    payload = {"last_artist_information_path": str(artist_info)}
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        prefix="state-",
        suffix=".tmp",
        delete=False,
    ) as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        temporary = Path(handle.name)
    temporary.chmod(0o600)
    os.replace(temporary, path)


def emit(**payload: object) -> None:
    print(json.dumps(payload, ensure_ascii=False))


def resolve(explicit_path: str | None, ignore_remembered: bool) -> int:
    local_state = state_path()
    if explicit_path:
        resolved = readable_file(explicit_path)
        if resolved is None:
            emit(source="none", path=None, reason="explicit-path-unreadable")
            return 2
        save_path(local_state, resolved)
        emit(source="explicit", path=str(resolved), reason=None)
        return 0

    if ignore_remembered:
        emit(source="none", path=None, reason="remembered-path-ignored")
        return 0

    remembered = load_state(local_state).get("last_artist_information_path")
    if not remembered:
        emit(source="none", path=None, reason="no-remembered-path")
        return 0
    resolved = readable_file(remembered)
    if resolved is None:
        emit(source="none", path=None, reason="remembered-path-unreadable")
        return 0
    emit(source="remembered", path=str(resolved), reason=None)
    return 0


def forget() -> int:
    local_state = state_path()
    try:
        local_state.unlink()
    except FileNotFoundError:
        pass
    emit(status="forgotten")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    resolve_parser = subparsers.add_parser("resolve")
    resolve_parser.add_argument("--path")
    resolve_parser.add_argument("--ignore-remembered", action="store_true")
    subparsers.add_parser("forget")
    args = parser.parse_args()

    if args.command == "resolve":
        return resolve(args.path, args.ignore_remembered)
    return forget()


if __name__ == "__main__":
    raise SystemExit(main())
