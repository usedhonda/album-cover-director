# GPT Image execution

## Contents

- Model and host controls
- Prompting contract
- Editing and selection continuity
- Safety and title checks
- Optional formats and sources

This file isolates model-specific behavior so the design grammar can survive future model changes.

## Model role

Use the image tool already exposed by the host; do not require an external MCP
server, an API key, or a new application. Keep this reference filename for
compatibility with existing skill links.

Official guidance checked **2026-11-15**: GPT-Image-2.6 Flare and Sunburst were
released on 2026-11-04. When the host actually offers model selection, consider
`gpt-image-2.6-flare` for concept exploration and
`gpt-image-2.6-sunburst` for detailed production or precise edits. These are
workflow starting points, not a promise that switching models improves a
selected cover. Preserve the chosen composition when moving between stages.

If the host does not expose model identity or selection, use its available
image tool and record the actual model as `unknown-not-exposed`. A preferred
model in the brief is only a request; never report it as the model used without
host evidence. Record exposed controls, requested values, and reported values
separately. See `runtime-adapters.md`.

## Model and host controls

Apply a parameter only when the current host exposes it for the selected model.
Natural-language requests for detail or careful editing are not evidence that a
hidden API parameter was set.

| Control | Use when exposed |
| --- | --- |
| `quality` | Choose rendering fidelity for the task. Inspect the result; a higher setting is not a new art direction. |
| `complexity` | For 2.6, choose `low`, `medium`, or `high` independently of quality. Start with `low` for a focused correction; compare medium/high for dense lettering or many spatial constraints. The documented API default is high when omitted; do not infer a hidden host's value from that default. |
| `background` | Request `opaque` for a complete static cover. Use transparency only for an explicitly requested intermediate or asset; still verify the final cover's pixels. |
| `input_fidelity` | Omit for GPT-Image-2.6. Do not carry a legacy high-fidelity parameter into an unsupported request. |
| `markup` | If the host exposes Image API markup, use a transparent PNG matching the first source image's dimensions after orientation. Mark the intended region and describe the change in words. Do not combine it with `mask`. |

Markup or a mask is edit guidance, not a promise of pixel-exact preservation.
If neither control exists, describe the region and the invariants in the prompt
and inspect the entire result. Keep model settings out of the artistic prompt
when they are explicit tool fields. Measure any latency and cost on the actual
host; do not copy advertised times or another project's bill into the run.

## Prompt clarity retained from earlier runs

Quote the exact title once, then specify its reading order and line breaks.
Remove stale title spellings, text/reference contradictions, and decorative
story details that do not support the chosen composition. Assign every reference
a specific role. Describe visible frame occupancy, contact and depth rather than
relying on camera labels alone; show the action or graphic rule that makes the
title necessary. Inspect crop, detail and lettering after each authorized edit.
The repository's `research/gpt-image-2-5-migration.md` retains the historical
2.5 investigation; it does not override the current host guidance above.

## Prompt order

Write prompts in this order:

1. output type: square album cover;
2. primary pattern and visual thesis;
3. subject/action and spatial composition;
4. visible frame occupancy, contact points, depth order, foreground/midground/background and light for spatial work, or flat fields, edges, figure/ground, and dominant geometry for graphic work;
5. palette with approximate area proportions;
6. physical medium/process or the deliberately flat graphic rule;
7. title-system family, image-native architecture, exact title, glyph count, reading order, material, spatial, character, or graphic relationship, position, color hierarchy, and line break;
8. thumbnail priority;
9. exclusions and rights-safe constraints.

Use concrete visual nouns and verbs. Do not send the model an essay about the song. Translate interpretation into observable image decisions.

## Adult sensual editorial requests

Use this section only when the user explicitly asks for a person-led cover to
feel sexy, sensual, glamorous, alluring, provocative, or similarly adult and
non-explicit. It converts an ambiguous desired effect into art direction; it is
not a safety workaround and does not apply to ordinary portraits by default.

### Interpret the request

State the legitimate cover context first, then use these variables instead of
repeating the ambiguous adjective:

1. **Subject and rights**: a fictional person with a stated adult age, or a
   rights-cleared reference with documented consent for the requested use.
   Do not assign a gender unless the brief does.
2. **Agency and action**: self-possessed gaze, controlled posture, a stage
   action, dance movement, or another intentional gesture; never vulnerability,
   incapacity, surveillance, or surprise as the source of allure.
3. **Wardrobe and silhouette**: name opaque, conventional fashion or stagewear,
   its material, and how tailoring or movement makes the silhouette legible.
4. **Composition**: use an eye-level frame with balanced attention to face,
   garment, title, and setting. Avoid intimate, voyeuristic, or body-part-led
   crops.
5. **Light, color, and space**: make allure come from a named lighting setup,
   texture, palette relationship, and a public or professional setting such as
   a stage, soundstage, foyer, or editorial set.

Keep the existing prompt order and title-system requirements. The exact title
must remain generated within the image and share a hierarchy with the subject;
do not reserve detached text space or add typography afterward.

### Boundaries and recovery

Include one short, concrete boundary statement when it resolves a real
ambiguity: adult subject, fully clothed opaque wardrobe, non-nude,
non-explicit, and no real-person sexualization. Prefer positive wardrobe and
composition details over a long negative list.

Reject a concept that combines youth cues, private or voyeuristic settings,
unaware or incapacitated subjects, transparent or displaced clothing, or
body-part emphasis. Redesign the scene rather than substituting euphemisms.

If the host exposes a moderation error, record whether it identifies the input
or output and change the relevant condition: clarify adult status and rights,
replace ambiguous clothing or setting, widen a crop, restore agency, or make
the intended source of allure explicit. Do not retry an unchanged request. An
API `moderation` setting is host-specific and never disables policy or replaces
this design check.

## Palette-temperature guard (existing quality guard)

Image output can drift toward parchment, sepia, brass, amber, or warm-yellow
light when the brief does not explicitly control the neutral point. Treat this
as an existing quality guard, not a demonstrated universal model bias or an artist preference. Every direction must name
its intended neutral, dominant and accent colors, and palette temperature.

Default to neutral or release-derived temperature and explicitly exclude an
unmotivated yellow, parchment, sepia, brass, amber, or golden cast. This is not
a default cool-blue look: use the release's actual color script. Warmth is
allowed only when the brief intentionally calls for it—such as sunset,
candlelight, sodium vapor, gold, autumn foliage, or a warm-print process. In
that case name the physical cause, the warm regions, and the intended neutral
anchor so warmth does not contaminate the whole square. For a selected image
that is otherwise correct, treat temperature as a small correction only:
preserve composition, drawing, title, material, and value structure; do not
reimagine the cover with an all-blue, neon, or night-time palette.

## Controlled irregularity

When the direction claims a live, physical, documentary, or spatial event,
write a hierarchy lock before requesting any irregularity. Lock the title's
occupied area, silhouette, reading route, and value priority, along with any
subject whose recognition is essential. Then choose one or two irregularities
that have a physical cause: uneven exposure, falling-off light, smoke, a
moving body, scratched reflection, crop, occlusion, wear, or accidental
darkness. Name the cause, the background region where it acts, and the one
specific variation it permits.

This is not a request for generic grain, blur, dirt, or randomness. Do not
apply smoke, motion blur, dimming, gaps, or distortion to the locked title
silhouette unless a small, named title-edge effect is explicitly required; it
may never alter the title's reading route, occupied area, or dominance. Let
surrounding detail become partial only where the named cause makes that
believable. Do not apply this rule to a deliberately pristine graphic,
diagrammatic, or product-like direction.

## Variants

Generate independent candidates during `concept-preview`. Do not use one image
and request palette-only variants when the brief requires structural diversity.
Every preview is still a complete cover with the exact image-native title.
Record its interpretation, visual mechanism, composition signature, prompt,
actual source file, and SHA-256; a contact-sheet thumbnail is not that source.

After selection, use the selected preview as the parent of a
`production-candidate`. Record `preview_candidate_id` and the selected source
path/SHA-256 before editing. Check that the source still matches its recorded
hash. Keep title silhouette, occupied area, reading route, negative space,
figure role, camera, medium, palette relationships, and the selected visual
mechanism as invariants. Raise fidelity or correct a named defect while keeping
those invariants. Do not automatically center the title, smooth deliberate
texture, add a scenic background, or make a flat graphic more photographic in
the name of polish.

If the host cannot edit the selected source, retain the concept and clearly
report the production limitation. Do not substitute an unrelated new
generation and label it a refinement of the selected image.

## Reference images

Use only user-provided or rights-cleared images. Describe what each reference
controls: identity, pose, garment, composition, material, or palette. Do not ask
for a direct replica. Supply the actual reference image through the host's
supported image input, state the identity traits to preserve, and change only
the scoped variables. Do not equate identity preservation with an
`input_fidelity` setting that the current model does not support.

## Edits

Edit one variable at a time. State invariants before the requested change:
subject identity, crop, title string and anatomy, title position and scale,
palette, medium, negative space, and background. Carry the selected preview's
visual mechanism and `preserve_in_production` list into every edit. Permit at
most two refinement cycles. Compare each result with the selected original at
full size and thumbnail size; improved detail does not excuse a weaker concept.
If the result regresses, return to the selected original file instead of using
the latest edit as the next input. Do not silently replace the selected parent
or recompute its stored hash to accept a different file.

## Text strategy

Generate every artistic candidate with the exact title visibly integrated into the jacket. Generate all title lettering in the same image as the scene: never add, redraw, typeset, or composite letters afterward. For complex-script or long titles, state each glyph exactly once, its reading order, placement, relative scale, color hierarchy, and relation to the scene. For production, failed lettering requires a native architecture repair within the two-cycle refinement budget. For concept previews, disclose a limited glyph issue only when the concept and intended title mechanism remain clear; do not claim a completed cover. Exploration replacements use their own budget. Never present a textless master, a detached title banner, generic caption box, or font layer as a cover candidate.

For `material-world`, state the world engine before the component vocabulary:
the act, relation, ritual, memory, weather, or spatial pressure that makes the
material necessary. Then state exactly how the material forms strokes,
counters, joins, terminals, spacing, and the title's role in that world.
Explicitly reject product shots, component catalogues, and equipment merely
arranged into letters. For `spatial-field`, state the causal phenomenon, title
hierarchy lock, protected letter skeleton, reading route, and the spatial
planes that transform the title; ordinary-looking letters are permitted only
as native scene structure, never as a flat overlay. For `character-led`, state the figure's action, the title's shared
scale/hierarchy, contact points, and depth order. In each case, explicitly
forbid ordinary typography placed on a finished scene.

For `graphic-field`, state the flat positive and negative masses, figure-ground
relationship, title skeleton, color-area balance, and reading route. Generate
the exact title as part of the same image's graphic structure. Preserve the
deliberate flatness, crop, empty areas, and shape collisions; do not translate
them into a photographed object, a three-dimensional material scene, or a
character merely to make the design appear more elaborate.

## Optional formats

The default deliverable remains a static square cover. The 2.6 API documents
SVG and animated GIF output, but this skill does not implement an SVG/GIF
production or delivery pipeline. Consider either only for an explicit advanced
request after checking the actual host's controls and access. GIF availability
can depend on preview access; SVG uses a separate authoring model. Do not claim
these are available because the underlying image family supports them, and do
not use them to bypass the image-native title rule.

## Required provenance

Record the model identifier or host tool, date, prompt, reference-image ownership
statement, edit parent, and delivery transformations. Use
`assets/run-ledger.yaml` for stage, interpretation, visual mechanism, selected
source, invariants, actual settings, and output evidence. Leave unreported cost
or latency empty and explain their absence; never estimate an observed result.
Never imply that an ungenerated prompt is a completed cover.

## Official sources

Checked **2026-11-15**. The workflow above is this skill's production policy;
the linked pages establish model capabilities and parameter contracts.

- Release date: <https://developers.openai.com/api/docs/changelog>
- Flare role: <https://developers.openai.com/api/docs/models/gpt-image-2.6-flare>
- Sunburst role: <https://developers.openai.com/api/docs/models/gpt-image-2.6-sunburst>
- Complexity, markup, and limitations: <https://developers.openai.com/api/docs/guides/image-generation>
- Input-fidelity compatibility and edit fields: <https://developers.openai.com/api/reference/resources/images/methods/edit>
- Output formats and their access requirements: <https://developers.openai.com/api/reference/resources/images/methods/generate>
- Prompt specificity and preservation across edits: <https://developers.openai.com/api/docs/guides/image-prompting>
