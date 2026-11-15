# Runtime adapters

## Contents

- Capability discovery and truthful settings
- Contract boundary
- Static-cover scope
- Local evidence

Use the host's existing **GPT Image** generation/editing capability. This is a
skill adapter, not an API client: do not create an application, require an API
key, or install an external image service to unlock optional controls.

Model guidance checked **2026-11-15**: when the host exposes model selection,
consider `gpt-image-2.6-flare` for concept previews and
`gpt-image-2.6-sunburst` for detailed production or precise edits. If a host
exposes only its built-in image tool, use that surface and record the actual
model as `unknown-not-exposed`. Do not infer a model ID from a launch date,
product name, visual appearance, or a requested model name.

Do not enable another provider merely because a contract is portable. Keep
observations scoped to the actual model, host, settings, and stage.

## Capability discovery and truthful settings

Read the current tool schema before calling it. Distinguish three things:

- **Requested:** the model and settings explicitly sent through supported tool
  fields. A preference in an art-direction brief is not a submitted setting.
- **Exposed:** controls the host actually permits, such as model selection,
  source-image editing, quality, complexity, size, or markup. Record their names;
  do not invent unavailable fields or translate prose into claimed API values.
- **Reported:** model/settings confirmed by the host response. Use
  `unknown-not-exposed` when the host does not report them, even if an API default
  is documented elsewhere. Inspect dimensions and transparency from the file
  itself when possible.

Keep `runtime.model_id` as the actual reported identity, never the preferred
model. Use the ledger's `runtime.requested_model_id`, `exposed_controls`,
`requested_settings`, and `reported_settings` to preserve the distinction.
An empty `exposed_controls` list means no optional model/quality/complexity/etc.
control was exposed; it does not mean the image tool itself was unavailable.

For 2.6, quality and complexity are independent. Start a focused edit at low
complexity only if that field exists. Omit unsupported `input_fidelity` rather
than copying a legacy request. Use markup only through a supported host field;
keep the first source image and annotation layer aligned and never combine
markup with a mask. Full parameter details and official sources are in
`gpt-image-2.md`.

Measure latency only from an actual call. Record billed cost or usage only when
reported; otherwise leave the ledger's optional values null. A new model,
matching token rate, or vendor speed claim does not establish this run's cost
or elapsed time.

## Contract boundary

Record the version declared in `SKILL.md` as `runtime.skill_version`; the
repository plugin manifest carries the same version. The template's source
minimums are working requirements, not evidence of host capability. When size
controls are absent, inspect the first generated file and reconcile the
production requirement with the documented export policy before proceeding.
Do not claim native 3000 px output from a smaller source. Explicit user source
requirements take precedence; if the host cannot meet one, report that gap.

- `run-contract.json` records the release title, allowed readable text, rights
  basis, interpretations, a variable set of directions, runtime identity, stage, and
  candidates.
- `concept-preview` produces title-integrated concept images for selection,
  with any unresolved lettering issues disclosed. These are not vetted finals. Use its declared
  preview minimum dimension, not the production requirement, for preview checks.
- `production-candidate` uses a selected preview's original source and SHA-256.
  Keep its `preview_candidate_id`, interpretation, visual mechanism,
  `preserve_in_production` list, and composition signature. Preserve the selected
  intent rather than asking a higher-quality model to invent a cleaner design.
- `prompt-preflight.py` checks the contract before generation. Production source
  minimums belong in the capability profile; do not pretend a host can meet them
  merely because the template requests them.
- `cover-ops.py preflight` verifies objective image properties; readable text
  requires an agent or human visual check, with source checksum and evidence;
  objective preflight does not verify text and this skill does not use OCR.
- `handoff-manifest.py` records the selected production candidate and its
  delivery evidence. A preview or prompt-only result is not final delivery.

If the host cannot edit the selected file or cannot meet production dimensions,
retain the selected concept and report what remains incomplete. Do not create a
different image, silently upscale it, or substitute a contact-sheet crop and
claim it is the selected source. Preserve the existing export policy and record
any authorized delivery transformations.

## Static-cover scope

Keep artistic previews and production candidates square, with the exact title
requested inside the generated image. Preview glyph issues may be disclosed;
production lettering must pass the full text gate. Do not repair lettering with
an external type layer. Preserve `graphic-field` flatness when selected, just as
you preserve a material world or a character's action.

SVG/GIF are documented capabilities of supported 2.6 APIs, not implemented
adapters in this repository. Consider them only for an explicit advanced
request, after verifying host access, and do not count them as static-cover
delivery or imply that this skill already provides those pipelines.

## Local evidence

Use `learning-state.py` only in an artist-local `.album-cover-director/` directory. Confidence is model- and host-specific, requires repeated outcomes, and never promotes private evidence into this public skill automatically.

Official references checked **2026-11-15**:

- <https://developers.openai.com/api/docs/models/gpt-image-2.6-flare>
- <https://developers.openai.com/api/docs/models/gpt-image-2.6-sunburst>
- <https://developers.openai.com/api/docs/guides/image-generation>
