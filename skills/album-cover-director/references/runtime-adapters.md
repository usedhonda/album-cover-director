# Runtime adapters

The production contract is runtime-neutral, but this skill currently enables **GPT Image 2** only. Record the exact model identifier and host surface in the run contract so local observations stay scoped to the environment that produced them.

Do not enable another image model merely because a contract is portable. A new runtime requires separate validation of title rendering, transparency, safety behavior, and delivery output before it can become an active adapter.

## Contract boundary

- `run-contract.json` records the release title, allowed readable text, rights basis, three directions, runtime identity, and candidates.
- `prompt-preflight.py` blocks an incomplete contract before generation.
- `cover-ops.py preflight` verifies objective image properties; readable text remains a human check because this skill does not use OCR.
- `handoff-manifest.py` records the selected candidate and its delivery evidence.

## Local evidence

Use `learning-state.py` only in an artist-local `.album-cover-director/` directory. Confidence is model- and host-specific, requires repeated outcomes, and never promotes private evidence into this public skill automatically.
