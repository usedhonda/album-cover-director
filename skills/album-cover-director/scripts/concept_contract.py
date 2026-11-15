"""Shared contracts for concept previews, selection, and production handoff.

Schema checks do not judge visual diversity. A recorded visual review is a
human/agent art-direction decision; file hashes only bind it to its inputs.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


PREVIEW = "concept-preview"
PRODUCTION = "production-candidate"
MAX_PREVIEWS = 24
FAMILIES = {"material-world", "spatial-field", "character-led"}
PATTERNS = {"Portrait / Identity", "Documentary Moment", "Narrative Tableau", "Symbolic Object / Still Life", "Typographic Hero / Wordmark", "Minimal Geometry / Color Field", "Abstract Material / Process", "Archive / Collage / Found Material", "Illustration / Character World", "Landscape / Architecture / Absence", "Diagram / Grid / Data / Repetition", "Package Object / Intervention / Anti-cover"}
SIGNATURE_AXES = ("title_placement", "title_scale", "figure_role", "camera", "layout", "medium")
EVIDENCE_SOURCES = {"title", "song-title", "album-title", "lyrics", "description", "audio"}
DONOR_AXES = {"color", "lighting", "texture"}
FAMILY_FIELDS = {
    "material-world": ("world_engine", "material_vocabulary", "title_anatomy", "world_role"),
    "spatial-field": ("causal_phenomenon", "hierarchy_lock", "title_skeleton", "spatial_extension"),
    "character-led": ("central_action", "shared_hierarchy", "character_title_relation"),
    "graphic-field": ("graphic_rule", "title_shape", "figure_ground", "reading_route"),
}


def failure(code: str, path: str, message: str) -> dict[str, str]:
    return {"code": code, "path": path, "message": message}


def text_value(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def text_list(value: object) -> bool:
    return isinstance(value, list) and bool(value) and all(text_value(item) for item in value)


def positive_integer(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def valid_sha(value: object) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-fA-F]{64}", value) is not None


def checksum(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_asset(contract_path: Path, value: str) -> Path:
    source = Path(value)
    return (source if source.is_absolute() else contract_path.resolve().parent / source).resolve()


def _required_strings(document: dict, keys: tuple[str, ...], base: str, code: str, failures: list) -> None:
    for key in keys:
        if not text_value(document.get(key)):
            failures.append(failure(code, f"{base}.{key}", "Record a non-empty string."))


def _signature(value: object, base: str, failures: list) -> None:
    if not isinstance(value, dict):
        failures.append(failure("planned-signature-required", base, "Record the planned composition signature."))
        return
    _required_strings(value, SIGNATURE_AXES, base, "planned-signature-incomplete", failures)


def _review_shape(review: object, failures: list) -> None:
    if not isinstance(review, dict) or review.get("status") not in ("pending", "passed"):
        failures.append(failure("diversity-review-invalid", "diversity_review", "Record a pending or passed visual review."))
        return
    if review["status"] == "pending":
        return
    if not text_list(review.get("compared_axes")):
        failures.append(failure("review-axes-required", "diversity_review.compared_axes", "Record which visual axes were actually compared."))
    if not text_value(review.get("summary")):
        failures.append(failure("review-summary-required", "diversity_review.summary", "Record the visual decision, not only its status."))
    entries = review.get("reviewed_candidates")
    if not isinstance(entries, list) or not entries:
        failures.append(failure("review-candidates-required", "diversity_review.reviewed_candidates", "Record every reviewed candidate and its source hash."))
        return
    ids: set[str] = set()
    for index, entry in enumerate(entries):
        base = f"diversity_review.reviewed_candidates[{index}]"
        if not isinstance(entry, dict):
            failures.append(failure("review-entry-invalid", base, "Review entries must be objects."))
            continue
        candidate_id = entry.get("id")
        if not text_value(candidate_id):
            failures.append(failure("review-id-required", f"{base}.id", "Record a candidate ID."))
        elif candidate_id in ids:
            failures.append(failure("review-id-duplicate", f"{base}.id", "A candidate may be reviewed only once in this set."))
        else:
            ids.add(candidate_id)
        if not valid_sha(entry.get("sha256")):
            failures.append(failure("review-hash-required", f"{base}.sha256", "Record the reviewed image's SHA-256."))
        if not text_value(entry.get("observation")):
            failures.append(failure("review-observation-required", f"{base}.observation", "Describe the actual image, not just its direction label."))


def _selection_shape(contract: dict, direction_ids: set[str], failures: list) -> None:
    selection = contract.get("selection")
    if selection is None:
        return  # Explicit direct production remains supported.
    if contract.get("stage") != PRODUCTION or not isinstance(selection, dict):
        failures.append(failure("selection-stage-invalid", "selection", "Selection provenance belongs to a production contract."))
        return
    _required_strings(selection, ("source_contract_path", "reason"), "selection", "selection-field-required", failures)
    if text_value(selection.get("source_contract_path")) and not Path(selection["source_contract_path"]).is_absolute():
        failures.append(failure("selection-path-not-absolute", "selection.source_contract_path", "Preserve the absolute preview-contract path."))
    if not valid_sha(selection.get("source_contract_sha256")):
        failures.append(failure("selection-contract-hash-required", "selection.source_contract_sha256", "Preserve the preview-contract SHA-256."))
    sources = selection.get("sources")
    selected_ids = selection.get("selected_candidate_ids")
    if not text_list(selected_ids) or len(set(selected_ids)) != len(selected_ids):
        failures.append(failure("selection-ids-invalid", "selection.selected_candidate_ids", "Select unique candidate IDs."))
    if not isinstance(sources, list) or not sources:
        failures.append(failure("selection-sources-required", "selection.sources", "Preserve each selected image and its design decisions."))
        return
    source_ids: list[str] = []
    covered_directions: set[str] = set()
    for index, source in enumerate(sources):
        base = f"selection.sources[{index}]"
        if not isinstance(source, dict):
            failures.append(failure("selection-source-invalid", base, "Each selected source must be an object."))
            continue
        _required_strings(source, ("candidate_id", "direction_id", "source_path", "reason", "visual_mechanism"), base, "selection-source-incomplete", failures)
        if text_value(source.get("candidate_id")):
            source_ids.append(source["candidate_id"])
        if not text_value(source.get("direction_id")) or source["direction_id"] not in direction_ids:
            failures.append(failure("selection-direction-invalid", f"{base}.direction_id", "Selected sources must reference a production direction."))
        else:
            covered_directions.add(source["direction_id"])
        if text_value(source.get("source_path")) and not Path(source["source_path"]).is_absolute():
            failures.append(failure("selection-path-not-absolute", f"{base}.source_path", "Preserve absolute selected-source paths."))
        if not valid_sha(source.get("source_sha256")):
            failures.append(failure("selection-source-hash-required", f"{base}.source_sha256", "Preserve the selected image's SHA-256."))
        if not text_list(source.get("preserve_in_production")):
            failures.append(failure("selection-preservation-required", f"{base}.preserve_in_production", "Preserve the selected design invariants."))
        _signature(source.get("planned_signature"), f"{base}.planned_signature", failures)
        direction = next((item for item in contract["directions"] if isinstance(item, dict) and item.get("id") == source.get("direction_id")), None)
        if direction is not None:
            for key in ("visual_mechanism", "preserve_in_production", "planned_signature"):
                if source.get(key) != direction.get(key):
                    failures.append(failure("selected-design-changed", f"{base}.{key}", "The production direction must retain the selected mechanism and composition."))
    if len(source_ids) != len(set(source_ids)) or (text_list(selected_ids) and set(source_ids) != set(selected_ids)):
        failures.append(failure("selection-source-coverage", "selection.sources", "Selected IDs and source records must match exactly."))
    if covered_directions != direction_ids:
        failures.append(failure("selection-direction-coverage", "directions", "Every production direction must come from the selection."))
    donors = selection.get("donors", [])
    if not isinstance(donors, list) or len(donors) > 1:
        failures.append(failure("selection-donors-invalid", "selection.donors", "Use at most one scoped donor for a primary composition."))
        return
    if donors and (not text_list(selected_ids) or len(selected_ids) != 1):
        failures.append(failure("donor-primary-required", "selection.selected_candidate_ids", "A scoped donor needs exactly one primary candidate."))
    for index, donor in enumerate(donors):
        base = f"selection.donors[{index}]"
        if not isinstance(donor, dict):
            failures.append(failure("donor-invalid", base, "A donor must record its image, traits, and original direction."))
            continue
        _required_strings(donor, ("candidate_id", "direction_id", "source_path"), base, "donor-incomplete", failures)
        if text_value(donor.get("candidate_id")) and donor["candidate_id"] in source_ids:
            failures.append(failure("donor-is-primary", f"{base}.candidate_id", "Choose a donor distinct from the primary candidate."))
        if text_value(donor.get("source_path")) and not Path(donor["source_path"]).is_absolute():
            failures.append(failure("selection-path-not-absolute", f"{base}.source_path", "Preserve the absolute donor image path."))
        if not valid_sha(donor.get("source_sha256")):
            failures.append(failure("donor-hash-required", f"{base}.source_sha256", "Preserve the donor image's SHA-256."))
        traits = donor.get("traits")
        if not isinstance(traits, list) or not traits:
            failures.append(failure("donor-trait-required", f"{base}.traits", "Name the color, lighting, or texture to borrow."))
        else:
            for trait_index, trait in enumerate(traits):
                if not isinstance(trait, dict) or not isinstance(trait.get("axis"), str) or trait["axis"] not in DONOR_AXES or not text_value(trait.get("instruction")):
                    failures.append(failure("donor-trait-invalid", f"{base}.traits[{trait_index}]", "Only scoped color, lighting, or texture instructions are supported; keep the primary composition."))
        snapshot = donor.get("direction_snapshot")
        interpretation = donor.get("interpretation_snapshot")
        if not isinstance(snapshot, dict) or snapshot.get("id") != donor.get("direction_id"):
            failures.append(failure("donor-direction-snapshot-required", f"{base}.direction_snapshot", "Keep the original donor direction as evidence, not as the production layout."))
        if not isinstance(interpretation, dict) or not isinstance(snapshot, dict) or interpretation.get("id") != snapshot.get("interpretation_id"):
            failures.append(failure("donor-interpretation-snapshot-required", f"{base}.interpretation_snapshot", "Keep the donor's original interpretation and evidence."))


def validate(contract: object) -> list[dict[str, str]]:
    """Validate metadata without claiming that generated images are diverse."""
    if not isinstance(contract, dict):
        return [failure("contract-invalid", "$", "Contract must be a JSON object.")]
    failures: list[dict[str, str]] = []
    version = contract.get("schema_version", 1)
    if type(version) is not int or version not in (1, 2):
        return [failure("schema-version-invalid", "schema_version", "Use schema version 1 or 2.")]
    stage = contract.get("stage")
    if version == 2 and stage not in (PREVIEW, PRODUCTION):
        failures.append(failure("stage-required", "stage", "Use concept-preview or production-candidate."))
    if version == 1 and stage is not None:
        failures.append(failure("stage-version-mismatch", "stage", "Stage-aware contracts require schema_version 2."))
    release = contract.get("release")
    if not isinstance(release, dict) or not text_value(release.get("exact_title")):
        failures.append(failure("title-required", "release.exact_title", "An exact release title is required."))
        title = ""
    else:
        title = release["exact_title"]
    allowed = release.get("allowed_readable_text") if isinstance(release, dict) else None
    if not text_list(allowed):
        failures.append(failure("allowed-text-invalid", "release.allowed_readable_text", "Allowed readable text must be a non-empty string list."))
    elif title and title not in allowed:
        failures.append(failure("title-not-allowed", "release.allowed_readable_text", "The exact title must be explicitly allowed."))
    constraints = contract.get("constraints")
    if not isinstance(constraints, dict) or constraints.get("title_must_be_image_native") is not True:
        failures.append(failure("image-native-title-required", "constraints.title_must_be_image_native", "The title must be image-native."))
    if not isinstance(constraints, dict) or constraints.get("post_typesetting_allowed") is not False:
        failures.append(failure("post-typesetting-prohibited", "constraints.post_typesetting_allowed", "Post-typesetting must remain disabled."))
    rights = contract.get("rights")
    if not isinstance(rights, dict) or not text_value(rights.get("reference_basis")):
        failures.append(failure("rights-basis-required", "rights.reference_basis", "Record the reference or asset rights basis."))
    runtime = contract.get("runtime")
    if not isinstance(runtime, dict):
        runtime = {}
    _required_strings(runtime, ("model_family", "model_id", "host_surface", "skill_version"), "runtime", "runtime-identity-required", failures)
    capability = runtime.get("capability_profile")
    if not isinstance(capability, dict) or not positive_integer(capability.get("source_minimum_dimension")):
        failures.append(failure("source-capability-required", "runtime.capability_profile.source_minimum_dimension", "Record a positive production source minimum dimension."))
    if isinstance(capability, dict) and "preview_minimum_dimension" in capability and not positive_integer(capability["preview_minimum_dimension"]):
        failures.append(failure("preview-capability-invalid", "runtime.capability_profile.preview_minimum_dimension", "Preview minimum dimension must be positive."))
    if version == 2 and stage == PREVIEW and (not isinstance(capability, dict) or not positive_integer(capability.get("preview_minimum_dimension"))):
        failures.append(failure("preview-capability-required", "runtime.capability_profile.preview_minimum_dimension", "Record a separate preview minimum dimension; previews are not delivery sources."))
    interpretations: set[str] = set()
    if version == 2:
        entries = contract.get("interpretations")
        if not isinstance(entries, list) or not entries:
            failures.append(failure("interpretations-required", "interpretations", "Record meaning and evidence before visual mechanisms."))
        else:
            for index, item in enumerate(entries):
                base = f"interpretations[{index}]"
                if not isinstance(item, dict):
                    failures.append(failure("interpretation-invalid", base, "Interpretations must be objects."))
                    continue
                _required_strings(item, ("id", "summary"), base, "interpretation-incomplete", failures)
                if text_value(item.get("id")):
                    if item["id"] in interpretations:
                        failures.append(failure("interpretation-id-duplicate", f"{base}.id", "Interpretation IDs must be unique."))
                    interpretations.add(item["id"])
                evidence = item.get("evidence")
                if not isinstance(evidence, list) or not evidence:
                    failures.append(failure("interpretation-evidence-required", f"{base}.evidence", "Tie the interpretation to title, lyrics, or supplied context."))
                    continue
                for evidence_index, entry in enumerate(evidence):
                    if not isinstance(entry, dict) or not isinstance(entry.get("source"), str) or entry["source"] not in EVIDENCE_SOURCES or not text_value(entry.get("anchor")):
                        failures.append(failure("interpretation-evidence-invalid", f"{base}.evidence[{evidence_index}]", "Record a supported evidence source and a short anchor."))
    directions = contract.get("directions")
    if version == 1 and (not isinstance(directions, list) or len(directions) != 3):
        failures.append(failure("three-directions-required", "directions", "Legacy contracts require exactly three directions."))
        return failures
    if version == 2 and (not isinstance(directions, list) or not directions or (stage == PREVIEW and len(directions) > MAX_PREVIEWS)):
        failures.append(failure("direction-count-invalid", "directions", "Use one or more directions, with at most 24 in a preview board."))
        return failures
    patterns: set[str] = set()
    direction_ids: set[str] = set()
    for index, direction in enumerate(directions):
        base = f"directions[{index}]"
        if not isinstance(direction, dict):
            failures.append(failure("direction-invalid", base, "Each direction must be an object."))
            continue
        direction_id, pattern, family = direction.get("id"), direction.get("primary_pattern"), direction.get("title_system_family")
        if not text_value(direction_id):
            failures.append(failure("direction-id-required", f"{base}.id", "Each direction needs an ID."))
        elif direction_id in direction_ids:
            failures.append(failure("direction-id-duplicate", f"{base}.id", "Direction IDs must differ."))
        else:
            direction_ids.add(direction_id)
        if not isinstance(pattern, str) or pattern not in PATTERNS:
            failures.append(failure("primary-pattern-invalid", f"{base}.primary_pattern", "Use a defined primary pattern."))
        elif version == 1 and pattern in patterns:
            failures.append(failure("primary-pattern-duplicate", f"{base}.primary_pattern", "Legacy primary patterns must differ."))
        else:
            patterns.add(pattern)
        _required_strings(direction, ("title_system", "prompt_path"), base, "direction-field-required", failures)
        if not isinstance(family, str) or family not in (set(FAMILY_FIELDS) if version == 2 else FAMILIES):
            failures.append(failure("title-family-invalid", f"{base}.title_system_family", "Use a supported title-system family."))
        else:
            _required_strings(direction, FAMILY_FIELDS[family], base, f"{family}-direction-incomplete", failures)
        if version == 2:
            _required_strings(direction, ("name", "visual_mechanism"), base, "concept-direction-incomplete", failures)
            if not text_value(direction.get("interpretation_id")) or direction["interpretation_id"] not in interpretations:
                failures.append(failure("interpretation-reference-invalid", f"{base}.interpretation_id", "Reference a recorded interpretation."))
            if not text_list(direction.get("preserve_in_production")):
                failures.append(failure("production-invariants-required", f"{base}.preserve_in_production", "Name the mechanism and composition to preserve when finishing."))
            _signature(direction.get("planned_signature"), f"{base}.planned_signature", failures)
    if version == 1:
        return failures
    candidates = contract.get("candidates")
    if not isinstance(candidates, list) or (stage == PREVIEW and len(candidates) > MAX_PREVIEWS):
        failures.append(failure("candidate-list-invalid", "candidates", "Record a candidate list, with at most 24 previews."))
        candidates = []
    ids: set[str] = set()
    for index, item in enumerate(candidates):
        base = f"candidates[{index}]"
        if not isinstance(item, dict):
            failures.append(failure("candidate-invalid", base, "Each candidate must be an object."))
            continue
        _required_strings(item, ("id", "output_path"), base, "candidate-field-required", failures)
        if text_value(item.get("id")):
            if item["id"] in ids:
                failures.append(failure("candidate-id-duplicate", f"{base}.id", "Candidate IDs must be unique."))
            ids.add(item["id"])
        if not text_value(item.get("direction_id")) or item["direction_id"] not in direction_ids:
            failures.append(failure("candidate-direction-invalid", f"{base}.direction_id", "Reference an existing direction."))
        notes = item.get("preview_notes")
        if notes is not None and not isinstance(notes, str) and not (isinstance(notes, list) and all(isinstance(note, str) for note in notes)):
            failures.append(failure("preview-notes-invalid", f"{base}.preview_notes", "Use text or a list of text notes."))
    if stage == PREVIEW or "diversity_review" in contract:
        _review_shape(contract.get("diversity_review"), failures)
    _selection_shape(contract, direction_ids, failures)
    selection = contract.get("selection")
    if isinstance(selection, dict) and isinstance(selection.get("sources"), list):
        sources = {item["candidate_id"]: item for item in selection["sources"] if isinstance(item, dict) and text_value(item.get("candidate_id"))}
        for index, candidate in enumerate(candidates):
            if not isinstance(candidate, dict):
                continue
            source = sources.get(candidate.get("preview_candidate_id")) if isinstance(candidate.get("preview_candidate_id"), str) else None
            if source is None or source.get("direction_id") != candidate.get("direction_id"):
                failures.append(failure("candidate-preview-lineage-invalid", f"candidates[{index}].preview_candidate_id", "Reference the selected preview for this direction."))
    return failures


def validate_review(contract: dict, contract_path: Path) -> list[dict[str, str]]:
    """Check recorded review coverage and unchanged files, not artistic quality."""
    failures: list[dict[str, str]] = []
    review = contract.get("diversity_review")
    _review_shape(review, failures)
    if failures:
        return failures
    if review.get("status") != "passed":
        return [failure("visual-review-required", "diversity_review.status", "Compare the actual images and record a passed visual review before presentation or selection.")]
    candidates = contract.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        return [failure("review-images-required", "candidates", "Generate preview images before reviewing them.")]
    candidate_map: dict[str, dict] = {}
    for index, item in enumerate(candidates):
        if not isinstance(item, dict) or not text_value(item.get("id")) or item["id"] in candidate_map:
            failures.append(failure("review-candidate-ids-invalid", f"candidates[{index}]", "Candidate IDs must be present and unique."))
        else:
            candidate_map[item["id"]] = item
    reviewed = {entry["id"]: entry for entry in review["reviewed_candidates"]}
    if set(reviewed) != set(candidate_map):
        failures.append(failure("review-candidate-coverage", "diversity_review.reviewed_candidates", "The review must cover exactly the current candidate set."))
    for candidate_id, item in candidate_map.items():
        if candidate_id not in reviewed:
            continue
        if not text_value(item.get("output_path")):
            failures.append(failure("review-source-missing", f"candidates.{candidate_id}.output_path", "Record a source image path."))
            continue
        try:
            source = resolve_asset(contract_path, item["output_path"])
            digest = checksum(source)
        except (OSError, ValueError, RuntimeError) as exc:
            failures.append(failure("review-source-unreadable", f"candidates.{candidate_id}.output_path", str(exc)))
            continue
        if digest != reviewed[candidate_id]["sha256"].lower():
            failures.append(failure("review-source-changed", f"candidates.{candidate_id}.output_path", "The image changed after its recorded visual review; review it again."))
    return failures


def validate_selection_sources(contract: dict) -> list[dict[str, str]]:
    """Keep selected originals and their source contract available and unchanged."""
    selection = contract.get("selection")
    if not isinstance(selection, dict):
        return []
    failures: list[dict[str, str]] = []
    records = [("selection.source_contract_path", selection.get("source_contract_path"), selection.get("source_contract_sha256"))]
    sources = selection.get("sources", [])
    donors = selection.get("donors", [])
    if not isinstance(sources, list) or not isinstance(donors, list):
        return [failure("selection-provenance-incomplete", "selection.sources", "Selected sources must be a list.")]
    groups = (("sources", sources), ("donors", donors))
    for group, entries in groups:
        records.extend((f"selection.{group}[{index}].source_path", source.get("source_path"), source.get("source_sha256")) for index, source in enumerate(entries) if isinstance(source, dict))
    for field, raw_path, expected in records:
        if not text_value(raw_path) or not valid_sha(expected):
            failures.append(failure("selection-provenance-incomplete", field, "Selected source path and checksum are required."))
            continue
        try:
            actual = checksum(Path(raw_path))
        except (OSError, ValueError) as exc:
            failures.append(failure("selection-source-unreadable", field, str(exc)))
            continue
        if actual != expected.lower():
            failures.append(failure("selection-source-changed", field, "A selected source changed after selection; repeat the selection from reviewed originals."))
    if failures:
        return failures
    try:
        source_path = Path(selection["source_contract_path"])
        original = json.loads(source_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as exc:
        return [failure("selection-contract-unreadable", "selection.source_contract_path", str(exc))]
    if not isinstance(original, dict) or original.get("schema_version") != 2 or original.get("stage") != PREVIEW or validate(original):
        return [failure("selection-contract-invalid", "selection.source_contract_path", "Selection must originate in a valid concept-preview contract.")]
    if original.get("diversity_review", {}).get("status") != "passed":
        return [failure("selection-review-missing", "selection.source_contract_path", "The original preview set needs a recorded visual review.")]
    if contract.get("release", {}).get("exact_title") != original["release"]["exact_title"]:
        failures.append(failure("selection-title-changed", "release.exact_title", "The production title differs from the selected release."))
    candidates = {item["id"]: item for item in original["candidates"]}
    directions = {item["id"]: item for item in original["directions"]}
    interpretations = {item["id"]: item for item in original["interpretations"]}
    reviewed = {item["id"]: item for item in original["diversity_review"].get("reviewed_candidates", [])}
    for group, entries in groups:
        for index, source in enumerate(entries):
            base = f"selection.{group}[{index}]"
            if not isinstance(source, dict):
                continue
            candidate = candidates.get(source.get("candidate_id")) if isinstance(source.get("candidate_id"), str) else None
            if candidate is None or candidate["direction_id"] != source.get("direction_id"):
                failures.append(failure("selection-origin-mismatch", base, "The selected candidate or direction is not in the original contract."))
                continue
            direction = directions[candidate["direction_id"]]
            if str(resolve_asset(source_path, candidate["output_path"])) != source.get("source_path"):
                failures.append(failure("selection-origin-mismatch", f"{base}.source_path", "The selected image path differs from the original candidate."))
            review = reviewed.get(candidate["id"])
            if review is None or review["sha256"].lower() != source["source_sha256"].lower():
                failures.append(failure("selection-review-mismatch", f"{base}.source_sha256", "The selected image must match the original visual-review hash."))
            if group == "donors":
                for key, expected in (("direction_snapshot", direction), ("interpretation_snapshot", interpretations[direction["interpretation_id"]])):
                    if source.get(key) != expected:
                        failures.append(failure("selection-origin-mismatch", f"{base}.{key}", "Donor evidence must match the original direction and interpretation."))
            else:
                for key in ("visual_mechanism", "preserve_in_production", "planned_signature"):
                    if source.get(key) != direction.get(key):
                        failures.append(failure("selection-origin-mismatch", f"{base}.{key}", "The selected design snapshot differs from its original direction."))
    return failures
