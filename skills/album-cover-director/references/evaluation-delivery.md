# Evaluation and delivery

## Contents

- Evaluation sequence
- Delivery requirements
- Rights and provenance

Selection is comparative. Never score one candidate in isolation while ignoring the alternatives.

## Viewing conditions

Compare every candidate under six conditions:

1. 56 px square: main signal and silhouette;
2. 128 px square: exact title reading and title-form integrity;
3. 256 px square: title and secondary structure;
4. full size: craft, glyphs, artifacts, and material credibility;
5. grayscale: value hierarchy independent of hue;
6. blur: dominant masses, focal competition, and visual center.

Use `cover-ops.py contact-sheet` to create reproducible sheets. Select a leader and runner-up, and write why the rest lost.

## Scoring

Score 0–5 for release identity, musical specificity, concept specificity, structural distinction, composition, color/value, material credibility, typography, title-image integration, thumbnail recognition, artist fit, rights/provenance, and technical readiness. Release identity, typography, title-image integration, rights/provenance, and technical readiness are gates: a candidate scoring below 4 in any of them cannot be delivered without repair.

`release identity` asks whether the square feels like a durable identity for a piece of music rather than a poster, advertisement, editorial illustration, app tile, game splash screen, or generic AI concept image. It needs one dominant identity signal, intentional edge and crop behavior, controlled information density, and a visual reason to exist beyond literal illustration. `musical specificity` asks whether the choices trace to supplied evidence or to a clearly labeled title hypothesis rather than interchangeable genre decoration.

For a live, physical, documentary, or spatial direction, inspect the hierarchy
lock before inspecting controlled irregularity. The title's occupied area,
silhouette, reading route, and value priority must still match the brief.
Then verify that irregularity has a named cause, background region, and
permitted variation. Reject the synthetic finish where every subject, surface,
color, and effect is equally sharp, saturated, and available to read; also
reject a refinement that solves this by weakening the title. Uneven exposure,
smoke, motion, reflection, cropping, wear, or occlusion should create selective
uncertainty outside the locked hierarchy. Do not require this test for
deliberately pristine graphic, diagrammatic, or product-like directions.

A high total does not excuse an incorrect title, unlicensed reference, extra text, non-square master, or unreadable thumbnail.

For color/value, inspect temperature as well as hue balance. Reject a
whole-image warm-yellow, parchment, sepia, brass, amber, or golden cast unless
the brief named a physical or production cause, its bounded warm regions, and a
neutral anchor. Do not solve a temperature failure by blindly turning the cover
blue; preserve the selected composition and use the intended release color
script.

For a material title-world, score title-image integration by removing one half
of the idea in thought: remove the title, then remove the material system. If
either removal leaves an ordinary scene, a normal wordmark, or a viable cover,
the candidate fails. The material must visibly determine the title's skeleton,
counters, joins, terminals, spacing, and role in the image.

Also replace the components in thought with a neatly photographed equivalent
product. If the cover would still work as a product catalogue or equipment
advertisement, it fails. The material must be evidence of a human act, social
relation, ritual, memory, weather, spatial pressure, or another world engine
that the cover needs.

For a spatial-field title system, remove the named light, reflection, smoke,
motion, weather, or architectural phenomenon in thought. If the title becomes
a normal flat headline or the scene remains the same event, it fails. The
phenomenon must distribute and transform the title across the locked reading
route without weakening its occupied area, silhouette, or value priority.

For a character-led title system, remove the figure and then remove the title
in thought. If either leaves a conventional wordmark or conventional character
illustration, it fails. The figure's action, pose, props, and surrounding
world must visibly make the title's hierarchy, shape, or reading route work.

## One-variable refinement

Before an edit, write:

- the single variable being changed;
- the measured failure it addresses;
- all invariants;
- the acceptance observation.

Compare the edit against the selected original, not only against memory. Stop after two cycles.

## Rights and text checklist

- References are user-owned, licensed, public-domain, or used only as non-reproduced analytical input.
- No living artist imitation is requested.
- Exact title matches release metadata, including case, punctuation, spaces, and script.
- No accidental signatures, logos, labels, signs, numbers, pseudo-text, or watermarks appear.
- Artist name appears only when explicitly approved.
- Faces, trademarks, and third-party designs have documented permission where needed.

## Technical delivery

Treat source and delivery as separate stages. Source preflight validates the selected native image and its `run-contract.json` lineage before export. It does not require the source to already be 3000 x 3000. Delivery preflight validates the exported distributor assets after export.

Default delivery outputs:

- 3000 x 3000 PNG, RGB/RGBA, lossless;
- 3000 x 3000 JPG, RGB, quality 95, optimized;
- 256 x 256 PNG thumbnail;
- selected original master preserved unchanged;
- selected-source checksum, export checksums, and image metadata in `cover-report.md` and `handoff-manifest.json`;
- source-to-export lineage and structured human text verification in `handoff-manifest.json`.

Title integrity is judged only in the native generated image. If the string is missing, duplicated, fused, substituted, or unreadable, reject the candidate and regenerate from a more explicit title-image prompt; do not repair it with a font layer or compositing.

Do not upscale an image that is too small without disclosure. The export utility records source dimensions and whether scaling occurred. Distributor rules vary; confirm the destination's current requirements before consequential submission. A source may be smaller than delivery dimensions when the runtime cannot create a larger native square; disclose that lineage rather than failing a valid source check.

Also inspect:

- RGB color mode and the destination's accepted profile;
- unintended alpha or transparent pixels;
- edge halos after compositing;
- a human review that records the exact-title result and any unapproved readable marks;
- safe placement under platform crops and UI overlays;
- a one-color and low-contrast preview;
- version identifier, selected-source checksum, export checksums, and parent/edit lineage.

For print editions, treat CMYK conversion, total ink, proofing, bleed, trim, spine, dielines, and overprint as a separate prepress workflow. A streaming-ready RGB square is not proof of print readiness.

## Completion language

Say `delivery complete` only when the image files exist, delivery preflight passes, and `handoff-manifest.json` contains source-to-export lineage plus structured human text verification. If generation, typography, human rights review, text verification, or export is unavailable, name the missing gate and deliver the completed brief/prompt/specification without overstating status.
