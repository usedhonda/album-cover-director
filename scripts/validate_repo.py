#!/usr/bin/env python3
"""Validate the public plugin, skill, corpus, and repository safety contract."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    "Portrait / Identity",
    "Documentary Moment",
    "Narrative Tableau",
    "Symbolic Object / Still Life",
    "Typographic Hero / Wordmark",
    "Minimal Geometry / Color Field",
    "Abstract Material / Process",
    "Archive / Collage / Found Material",
    "Illustration / Character World",
    "Landscape / Architecture / Absence",
    "Diagram / Grid / Data / Repetition",
    "Package Object / Intervention / Anti-cover",
}
ERA_COUNTS = {
    "1940-1979": 30,
    "1980-1999": 30,
    "2000-2014": 30,
    "2015-present": 30,
}
EAST_ASIA = {"Japan", "South Korea", "China", "Hong Kong", "Taiwan"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".tif", ".tiff"}
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".jsonl", ".py", ".toml", ".txt"}
FORBIDDEN = [
    re.compile("/" + "Users" + "/"),
    re.compile(r"(?i)(api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*['\"][^'\"]+"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
]


class ValidationError(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def validate_manifest() -> None:
    manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
    require(manifest["name"] == "album-cover-director", "plugin name mismatch")
    require(manifest["version"] == "0.1.0", "plugin version mismatch")
    require(manifest.get("skills") == "./skills/", "skills path mismatch")
    require("$album-cover-director" in manifest["interface"]["defaultPrompt"], "default prompt must invoke skill")


def validate_skill() -> None:
    skill = (ROOT / "skills/album-cover-director/SKILL.md").read_text()
    match = re.match(r"\A---\n(.*?)\n---\n", skill, re.DOTALL)
    require(match is not None, "SKILL.md frontmatter missing")
    frontmatter = match.group(1)
    require("name: album-cover-director" in frontmatter, "skill name mismatch")
    require("description:" in frontmatter, "skill description missing")
    require("ordinary photo edits" in frontmatter, "negative trigger boundary missing")


def validate_corpus() -> None:
    corpus = json.loads((ROOT / "research/corpus.yaml").read_text())
    require(corpus.get("schema_version") == 1, "corpus schema version mismatch")
    works = corpus.get("works", [])
    require(len(works) == 120, f"expected 120 works, found {len(works)}")
    require(len({work["id"] for work in works}) == 120, "corpus IDs must be unique")
    require(Counter(work["era"] for work in works) == Counter(ERA_COUNTS), "era distribution must be 30 each")
    east_asia_count = sum(work["region"] in EAST_ASIA for work in works)
    require(east_asia_count >= 24, f"need at least 24 East Asian works, found {east_asia_count}")
    present_patterns = {work["primary_pattern"] for work in works}
    require(present_patterns == PATTERNS, f"pattern coverage mismatch: {PATTERNS - present_patterns}")

    required = {
        "id", "title", "artist", "year", "era", "region", "genre", "designer",
        "source_url", "source_kind", "subject", "composition", "typography_role",
        "color_ratio", "materiality", "thumbnail_performance", "genre_anchor",
        "genre_betrayal", "transferable_principle", "primary_pattern", "secondary_techniques",
    }
    for work in works:
        missing = required - work.keys()
        require(not missing, f"{work.get('id', '?')} missing fields: {sorted(missing)}")
        require(work["primary_pattern"] in PATTERNS, f"unknown pattern in {work['id']}")
        require(1 <= len(work["secondary_techniques"]) <= 2, f"secondary technique count in {work['id']}")
        parsed = urlparse(work["source_url"])
        require(parsed.scheme == "https" and parsed.netloc, f"invalid source URL in {work['id']}")
        require(1940 <= int(work["year"]) <= 2026, f"year outside corpus range in {work['id']}")


def validate_invocation_cases() -> None:
    cases = json.loads((ROOT / "tests/invocation-cases.json").read_text())
    positive = [case for case in cases if case["expected_trigger"]]
    negative = [case for case in cases if not case["expected_trigger"]]
    require(len(positive) >= 8, "need at least eight positive invocation cases")
    require(len(negative) >= 3, "need at least three negative invocation cases")
    tags = {tag for case in positive for tag in case["coverage"]}
    required_tags = {"japanese", "english", "mixed-script", "instrumental", "type-hero", "reference-image", "series-system"}
    require(required_tags <= tags, f"invocation coverage missing: {sorted(required_tags - tags)}")


def validate_public_safety() -> None:
    image_files = []
    violations = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() in IMAGE_SUFFIXES:
            image_files.append(path.relative_to(ROOT).as_posix())
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {"LICENSE"}:
            text = path.read_text(errors="replace")
            for pattern in FORBIDDEN:
                if pattern.search(text):
                    violations.append(f"{path.relative_to(ROOT)} matches {pattern.pattern}")
    require(not image_files, f"repository must not contain third-party raster images: {image_files}")
    require(not violations, "public-safety violations: " + "; ".join(violations))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    checks = [validate_manifest, validate_skill, validate_corpus, validate_invocation_cases, validate_public_safety]
    try:
        for check in checks:
            check()
            print(f"PASS {check.__name__}")
    except (ValidationError, KeyError, json.JSONDecodeError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
