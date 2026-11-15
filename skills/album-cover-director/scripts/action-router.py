#!/usr/bin/env python3
"""Choose a deterministic next production action from a failure signal."""

from __future__ import annotations

import argparse
import json


TITLE_ARCHITECTURE = {"title-integrity", "detached-title", "material-anatomy-gap", "character-title-separation", "title-complexity-mismatch"}
PIVOT = {"release-format-confusion", "literal-title-illustration", "generic-genre-template", "musical-evidence-gap", "series-repetition"}


def route(code: str, cycles: int, batch_failures: int, edit_regressed: bool, reference_stalled: bool, stage: str = "production-candidate") -> dict[str, str]:
    if code == "composition-convergence" and stage == "production-candidate":
        if cycles >= 2:
            return {"action": "report-incomplete-set", "reason": "The visual presentation gate failed and the available change budget is exhausted; do not promote a rejected candidate."}
        return {"action": "pivot-direction", "reason": "Observed candidate compositions converge; change the organizing geometry, not only palette or material."}
    if edit_regressed: return {"action": "return-to-parent", "reason": "The selected edit regressed from its parent."}
    if stage == "concept-preview":
        if code in TITLE_ARCHITECTURE: return {"action": "rebuild-title-architecture", "reason": "Rebuild the preview's title mechanism before production."}
        if reference_stalled: return {"action": "reference-assisted", "reason": "The preview needs better-scoped reference evidence."}
        return {"action": "explore-new-mechanism", "reason": "Replace a weak or convergent preview; exploration does not consume production refinement cycles."}
    if cycles >= 2: return {"action": "promote-runner-up", "reason": "The refinement budget is exhausted."}
    if code in TITLE_ARCHITECTURE: return {"action": "rebuild-title-architecture", "reason": "Title/image integration needs a structural rebuild, not an overlay."}
    if reference_stalled: return {"action": "reference-assisted", "reason": "Reference evidence is insufficient for the current direction."}
    if code in PIVOT: return {"action": "pivot-direction", "reason": "The failure affects the direction premise."}
    if batch_failures >= 2: return {"action": "regenerate-prompt", "reason": "Multiple candidates share the failure signal."}
    return {"action": "edit-local", "reason": "One bounded local correction remains available."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--failure-code", default=""); parser.add_argument("--cycles-used", type=int, default=0, help="Production refinement cycles only."); parser.add_argument("--exploration-redos", type=int, default=0); parser.add_argument("--stage", choices=("concept-preview", "production-candidate"), default="production-candidate"); parser.add_argument("--batch-failure-count", type=int, default=0); parser.add_argument("--edit-regressed", action="store_true"); parser.add_argument("--reference-stalled", action="store_true"); args = parser.parse_args()
    if args.cycles_used < 0 or args.batch_failure_count < 0 or args.exploration_redos < 0: parser.error("cycle, exploration, and batch counts must be non-negative")
    print(json.dumps({"failure_code": args.failure_code, "stage": args.stage, "exploration_redos": args.exploration_redos, "production_refinement_cycles_used": args.cycles_used if args.stage == "production-candidate" else 0, **route(args.failure_code, args.cycles_used, args.batch_failure_count, args.edit_regressed, args.reference_stalled, args.stage)}, ensure_ascii=False, indent=2)); return 0


if __name__ == "__main__": raise SystemExit(main())
