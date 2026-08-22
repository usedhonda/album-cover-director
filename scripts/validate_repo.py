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
DEMO_IMAGES = {
    "docs/examples/title-map-secretary-chi.png",
    "docs/examples/hero-wordmark-secretary-chi.png",
    "docs/examples/japanese-title-shachoshitsu-no-asa.png",
    "docs/examples/tsundere-secretary-chi.png",
    "docs/examples/oceanographic-title-system.png",
    "docs/examples/treasure-chart-title-system.png",
    "docs/examples/board-game-title-system.png",
    "docs/examples/botanical-specimen-title-system.png",
    "docs/examples/mechanized-title-system.png",
    "docs/examples/rotating-club-title-system.png",
    "docs/examples/ink-landscape-title-field.png",
    "docs/examples/spatial-field-pair.png",
}
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".jsonl", ".py", ".toml", ".txt"}
FORBIDDEN = [
    re.compile("/" + "Users" + "/"),
    re.compile(r"(?m)^(?!#!).*?/" + r"(?:home|System" + r"/Library|usr" + r"/share)/"),
    re.compile(r"(?i)(api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*['\"][^'\"]+"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
]


class ValidationError(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def validate_anti_concentration(works: list[dict], limits: dict[str, int]) -> None:
    fields = {
        "designer": "designer",
        "label": "label",
        "country": "country",
        "genre": "genre",
    }
    for limit_name, field in fields.items():
        values = Counter(work[field] for work in works)
        highest_value, highest_count = values.most_common(1)[0]
        require(highest_count <= limits[limit_name],
                f"{limit_name} concentration exceeds {limits[limit_name]}: {highest_value} has {highest_count}")

    source_counts = Counter(source_id for work in works for source_id in work["evidence_source_ids"])
    highest_source, highest_source_count = source_counts.most_common(1)[0]
    require(highest_source_count <= limits["source"],
            f"source concentration exceeds {limits['source']}: {highest_source} has {highest_source_count}")


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
    require("The only required input is:" in skill, "title-only input contract missing")
    require("lyrics either inline" in skill, "inline-or-path lyrics contract missing")
    require("last_artist_information_path" in skill, "artist-information path memory contract missing")
    for use_mode in ("identity-reference", "source-asset", "visual-direction"):
        require(use_mode in skill, f"reference-image use mode missing: {use_mode}")
    require("image paths" in skill, "reference-image non-persistence contract missing")


def validate_corpus() -> None:
    corpus = json.loads((ROOT / "research/corpus.yaml").read_text())
    require(corpus.get("schema_version") == 1, "corpus schema version mismatch")
    if corpus.get("research_status") == "superseded-draft":
        require(corpus.get("production_use") is False, "superseded corpus must disable production use")
        require(bool(corpus.get("replacement")), "superseded corpus must name its replacement state")
        return
    require(corpus.get("research_status") == "final", "production corpus must declare research_status=final")
    require(corpus.get("production_use") is True, "final corpus must enable production use")
    ledger = json.loads((ROOT / "research/typographic-candidates.yaml").read_text())
    anti_concentration_limits = ledger["checkpoint_contract"].get("anti_concentration_limits", {})
    require(anti_concentration_limits == {
        "designer": 3,
        "label": 6,
        "country": 16,
        "genre": 18,
        "source": 12,
    }, "final anti-concentration limits mismatch")
    evidence_complete = {
        candidate["id"]
        for candidate in ledger.get("candidates", [])
        if candidate.get("status") == "evidence-complete"
    }
    works = corpus.get("works", [])
    require(len(works) == 120, f"expected 120 works, found {len(works)}")
    require(len({work["id"] for work in works}) == 120, "corpus IDs must be unique")
    require(Counter(work["era"] for work in works) == Counter(ERA_COUNTS), "era distribution must be 30 each")
    east_asia_count = sum(work["region"] in EAST_ASIA for work in works)
    require(east_asia_count >= 24, f"need at least 24 East Asian works, found {east_asia_count}")
    present_patterns = {work["primary_pattern"] for work in works}
    require(present_patterns == PATTERNS, f"pattern coverage mismatch: {PATTERNS - present_patterns}")

    required = {
        "id", "title", "artist", "year", "era", "region", "country", "label", "genre", "designer",
        "source_url", "source_kind", "subject", "composition", "typography_role",
        "color_ratio", "materiality", "thumbnail_performance", "genre_anchor",
        "genre_betrayal", "transferable_principle", "primary_pattern", "secondary_techniques",
        "candidate_id", "evidence_source_ids",
    }
    for work in works:
        missing = required - work.keys()
        require(not missing, f"{work.get('id', '?')} missing fields: {sorted(missing)}")
        require(work["primary_pattern"] in PATTERNS, f"unknown pattern in {work['id']}")
        require(1 <= len(work["secondary_techniques"]) <= 2, f"secondary technique count in {work['id']}")
        require(work["candidate_id"] in evidence_complete,
                f"final corpus work {work['id']} must reference an evidence-complete candidate")
        candidate = next(candidate for candidate in ledger["candidates"] if candidate["id"] == work["candidate_id"])
        candidate_sources = {
            source_id
            for role_sources in candidate["evidence_roles"].values()
            for source_id in role_sources
        }
        evidence_source_ids = work["evidence_source_ids"]
        require(isinstance(evidence_source_ids, list) and len(set(evidence_source_ids)) >= 2,
                f"final corpus work {work['id']} needs two distinct evidence source IDs")
        require(set(evidence_source_ids) <= candidate_sources,
                f"final corpus work {work['id']} includes evidence not verified for its candidate")
        require(all(isinstance(work[field], str) and work[field].strip()
                    for field in ("country", "label", "designer", "genre")),
                f"final corpus work {work['id']} has empty anti-concentration metadata")
        parsed = urlparse(work["source_url"])
        require(parsed.scheme == "https" and parsed.netloc, f"invalid source URL in {work['id']}")
        require(1940 <= int(work["year"]) <= 2026, f"year outside corpus range in {work['id']}")
    validate_anti_concentration(works, anti_concentration_limits)


def validate_typographic_candidates() -> None:
    ledger = json.loads((ROOT / "research/typographic-candidates.yaml").read_text())
    require(ledger.get("schema_version") == 1, "typographic candidate schema version mismatch")
    require(ledger["selection_contract"].get("music_quality_is_not_evidence") is True,
            "music quality must not count as cover evidence")
    source_ids = {source["id"] for source in ledger.get("source_registry", [])}
    require(len(source_ids) == len(ledger.get("source_registry", [])), "candidate source IDs must be unique")
    for source in ledger.get("source_registry", []):
        parsed = urlparse(source["url"])
        require(parsed.scheme == "https" and parsed.netloc, f"invalid candidate source URL: {source['id']}")
    checkpoints = ledger.get("checkpoint_contract", {})
    evidence_contract = ledger["selection_contract"].get("final_evidence_contract", {})
    required_evidence_roles = set(evidence_contract.get("required_roles", []))
    require(required_evidence_roles == {"visual", "acclaim", "credit"},
            "final evidence contract must require visual, acclaim, and credit roles")
    minimum_distinct_sources = evidence_contract.get("minimum_distinct_sources")
    require(minimum_distinct_sources == 2, "final evidence contract must require two sources")
    require(checkpoints.get("candidate_pool_target") == 180, "candidate-pool target must be 180")
    require(checkpoints.get("visual_checkpoints") == [40, 80, 120], "visual checkpoints must be 40/80/120")
    require(checkpoints.get("final_corpus_target") == 120, "final corpus target must be 120")
    require(Counter(checkpoints.get("final_era_counts", {})) == Counter(ERA_COUNTS),
            "candidate ledger final-era contract must be 30 each")
    candidates = ledger.get("candidates", [])
    require(len(candidates) >= 80, f"need at least 80 visually screened candidates, found {len(candidates)}")
    require(len({candidate["id"] for candidate in candidates}) == len(candidates),
            "typographic candidate IDs must be unique")
    require(len({candidate["region"] for candidate in candidates}) >= 10,
            "80-work checkpoint must cover at least ten regions")
    require(len({candidate["genre"] for candidate in candidates}) >= 16,
            "80-work checkpoint must cover at least sixteen genre labels")
    require(any(candidate["region"] == "East Asia" for candidate in candidates),
            "seed candidates must include East Asia")
    require(any(candidate["region"] == "South Asia" for candidate in candidates),
            "seed candidates must include South Asia")
    require(any(candidate["region"] == "Africa" for candidate in candidates),
            "seed candidates must include Africa")
    require(any(candidate["region"] == "Middle East and North Africa" for candidate in candidates),
            "80-work checkpoint must include Middle East and North Africa")
    require(any(candidate["region"] == "Oceania" for candidate in candidates),
            "80-work checkpoint must include Oceania")
    eras = Counter(
        "1940-1979" if candidate["year"] <= 1979 else
        "1980-1999" if candidate["year"] <= 1999 else
        "2000-2014" if candidate["year"] <= 2014 else
        "2015-present"
        for candidate in candidates
    )
    require(set(eras) == set(ERA_COUNTS), f"80-work checkpoint must cover all eras, found {sorted(eras)}")
    require(min(eras.values()) >= 6, f"80-work checkpoint needs at least six candidates per era, found {dict(eras)}")
    require(sum(candidate["dominance"] == "T5" for candidate in candidates) >= 40,
            "80-work checkpoint needs at least forty T5 candidates")
    for candidate in candidates:
        require(candidate["dominance"] in {"T4", "T5"},
                f"{candidate['id']} is below the typography-dominance threshold")
        require(candidate["evidence_ids"], f"{candidate['id']} has no design-acclaim evidence")
        require(bool(candidate.get("design_credit")), f"{candidate['id']} has no design credit")
        require(bool(candidate.get("screening_observation")), f"{candidate['id']} has no visual observation")
        require(bool(candidate.get("transfer_question")), f"{candidate['id']} has no transfer question")
        unknown = set(candidate["evidence_ids"]) - source_ids
        require(not unknown, f"{candidate['id']} references unknown evidence: {sorted(unknown)}")
        require(candidate["status"] in {"visual-pass", "visual-second-pass", "evidence-complete"},
                f"{candidate['id']} has invalid screening status")
        if candidate["status"] == "evidence-complete":
            evidence_roles = candidate.get("evidence_roles", {})
            require(set(evidence_roles) == required_evidence_roles,
                    f"{candidate['id']} evidence-complete roles must be {sorted(required_evidence_roles)}")
            cited_sources = set()
            for role, role_sources in evidence_roles.items():
                require(isinstance(role_sources, list) and role_sources,
                        f"{candidate['id']} has no sources for evidence role {role}")
                unknown_role_sources = set(role_sources) - source_ids
                require(not unknown_role_sources,
                        f"{candidate['id']} evidence role {role} references unknown sources: {sorted(unknown_role_sources)}")
                cited_sources.update(role_sources)
            require(len(cited_sources) >= minimum_distinct_sources,
                    f"{candidate['id']} needs at least {minimum_distinct_sources} distinct evidence sources")


def validate_typography_genre_intake() -> None:
    intake = json.loads((ROOT / "research/typography-led-genre-intake.yaml").read_text())
    require(intake.get("schema_version") == 1, "typography genre intake schema version mismatch")
    require(intake.get("research_status") == "visual-discovery",
            "typography genre intake must remain visual-discovery")
    require(intake.get("production_use") is False,
            "typography genre intake must not be a production reference")
    require(intake.get("image_storage") is False,
            "typography genre intake must not store third-party images")
    contract = intake.get("selection_contract", {})
    candidates = intake.get("candidates", [])
    require(len(candidates) >= contract.get("minimum_candidates", 20),
            "typography genre intake has too few candidates")
    require(len({candidate["genre_group"] for candidate in candidates}) >= contract.get("minimum_genre_groups", 8),
            "typography genre intake has too few genre groups")
    require(len({candidate["id"] for candidate in candidates}) == len(candidates),
            "typography genre intake IDs must be unique")
    required = {
        "id", "genre_group", "artist", "title", "year", "source_url", "source_kind",
        "visual_observation", "typography_role", "transferable_question", "screening_status",
    }
    for candidate in candidates:
        missing = required - candidate.keys()
        require(not missing, f"typography intake candidate missing fields: {sorted(missing)}")
        require(candidate["screening_status"] == "visual-pass-private-trial-needed",
                f"typography intake candidate has invalid status: {candidate['id']}")
        require(1940 <= int(candidate["year"]) <= 2026,
                f"typography intake year outside range: {candidate['id']}")
        parsed = urlparse(candidate["source_url"])
        require(parsed.scheme == "https" and parsed.netloc,
                f"typography intake source URL invalid: {candidate['id']}")
        require("image_url" not in candidate,
                f"typography intake must not retain image URL: {candidate['id']}")


def validate_invocation_cases() -> None:
    cases = json.loads((ROOT / "tests/invocation-cases.json").read_text())
    positive = [case for case in cases if case["expected_trigger"]]
    negative = [case for case in cases if not case["expected_trigger"]]
    require(len(positive) >= 8, "need at least eight positive invocation cases")
    require(len(negative) >= 3, "need at least three negative invocation cases")
    tags = {tag for case in positive for tag in case["coverage"]}
    required_tags = {
        "japanese", "english", "mixed-script", "instrumental", "type-hero", "reference-image",
        "series-system", "title-only", "lyrics-path", "artist-information-path", "reference-image",
        "identity-reference", "source-asset", "visual-direction",
    }
    require(required_tags <= tags, f"invocation coverage missing: {sorted(required_tags - tags)}")


def validate_forward_cases() -> None:
    cases = json.loads((ROOT / "tests/forward-cases.json").read_text())
    require(len(cases) >= 8, "need at least eight forward cases")
    required_keys = {
        "name", "title", "evidence_kind", "mode", "typography_mode",
        "title_system_family", "title_system", "expected_candidates", "directions",
    }
    volumes = {"quick": 3, "standard": 6, "deep": 12}
    evidence_kinds = {
        "title-only", "lyrics-inline", "lyrics-path", "track-description", "audio",
        "artist-information-path", "reference-image",
    }
    typography_modes = {"auto", "image-native", "custom-wordmark"}
    names = set()
    covered_modes = set()
    covered_title_families = set()
    for case in cases:
        missing = required_keys - case.keys()
        require(not missing, f"forward case missing fields: {sorted(missing)}")
        require(case["name"] not in names, f"duplicate forward case name: {case['name']}")
        names.add(case["name"])
        require(bool(case["title"].strip()), f"forward case title missing: {case['name']}")
        if "artist" in case:
            require(bool(case["artist"].strip()), f"optional artist is empty: {case['name']}")
        require(case["evidence_kind"] in evidence_kinds,
                f"unsupported evidence kind: {case['name']}")
        if case["evidence_kind"] == "reference-image":
            require(case.get("reference_image_use") in {"identity-reference", "source-asset", "visual-direction"},
                    f"reference-image use mode missing: {case['name']}")
        require(case["mode"] in volumes, f"unsupported volume: {case['name']}")
        covered_modes.add(case["mode"])
        require(case["expected_candidates"] == volumes[case["mode"]],
                f"candidate count does not match mode: {case['name']}")
        require(case["typography_mode"] in typography_modes,
                f"unsupported typography mode: {case['name']}")
        require(case["title_system_family"] in {"material-world", "spatial-field", "character-led"},
                f"unsupported title-system family: {case['name']}")
        require(bool(case["title_system"].strip()),
                f"title system missing: {case['name']}")
        covered_title_families.add(case["title_system_family"])
        require(len(case["directions"]) == 3 and len(set(case["directions"])) == 3,
                f"forward case must specify three distinct directions: {case['name']}")
        require(set(case["directions"]) <= PATTERNS,
                f"forward case uses unknown pattern: {case['name']}")
    require(covered_modes == set(volumes), "forward cases must cover quick, standard, and deep")
    require(any(case["evidence_kind"] == "title-only" for case in cases),
            "forward cases need title-only coverage")
    require(any(case["evidence_kind"] == "lyrics-path" for case in cases),
            "forward cases need lyrics-path coverage")
    require(any(case["evidence_kind"] == "artist-information-path" for case in cases),
            "forward cases need artist-information-path coverage")
    require(any(case["evidence_kind"] == "reference-image" for case in cases),
            "forward cases need reference-image coverage")
    require(any(case["evidence_kind"] == "audio" for case in cases), "forward cases need instrumental/audio coverage")
    require(any(case["typography_mode"] == "custom-wordmark" for case in cases),
            "forward cases need custom-wordmark coverage")
    require(any(case["typography_mode"] == "image-native" for case in cases),
            "forward cases need image-native coverage")
    require(covered_title_families == {"material-world", "spatial-field", "character-led"},
            "forward cases must cover all image-native title-system families")


def validate_public_safety() -> None:
    image_files = []
    found_demo_images = set()
    violations = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() in IMAGE_SUFFIXES:
            relative = path.relative_to(ROOT).as_posix()
            if relative in DEMO_IMAGES:
                found_demo_images.add(relative)
            else:
                image_files.append(relative)
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {"LICENSE"}:
            text = path.read_text(errors="replace")
            for pattern in FORBIDDEN:
                if pattern.search(text):
                    violations.append(f"{path.relative_to(ROOT)} matches {pattern.pattern}")
    require(not image_files, f"repository must not contain undocumented raster images: {image_files}")
    require(found_demo_images == DEMO_IMAGES,
            f"demonstration gallery is incomplete: {sorted(DEMO_IMAGES - found_demo_images)}")
    require(not violations, "public-safety violations: " + "; ".join(violations))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    checks = [
        validate_manifest,
        validate_skill,
        validate_corpus,
        validate_typographic_candidates,
        validate_typography_genre_intake,
        validate_invocation_cases,
        validate_forward_cases,
        validate_public_safety,
    ]
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
