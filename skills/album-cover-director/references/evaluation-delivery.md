# Evaluation and delivery

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

Score 0–5 for concept specificity, structural distinction, composition, color/value, material credibility, typography, title-image integration, thumbnail recognition, artist fit, rights/provenance, and technical readiness. Typography, title-image integration, rights/provenance, and technical readiness are gates: a candidate scoring below 4 in any of them cannot be delivered without repair.

A high total does not excuse an incorrect title, unlicensed reference, extra text, non-square master, or unreadable thumbnail.

For a material title-world, score title-image integration by removing one half
of the idea in thought: remove the title, then remove the material system. If
either removal leaves an ordinary scene, a normal wordmark, or a viable cover,
the candidate fails. The material must visibly determine the title's skeleton,
counters, joins, terminals, spacing, and role in the image.

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

Default outputs:

- 3000 x 3000 PNG, RGB/RGBA, lossless;
- 3000 x 3000 JPG, RGB, quality 95, optimized;
- 256 x 256 PNG thumbnail;
- selected original master preserved unchanged;
- SHA-256 and image metadata in `cover-report.md`.

Title integrity is judged only in the native generated image. If the string is missing, duplicated, fused, substituted, or unreadable, reject the candidate and regenerate from a more explicit title-image prompt; do not repair it with a font layer or compositing.

Do not upscale an image that is too small without disclosure. The export utility records source dimensions and whether scaling occurred. Distributor rules vary; confirm the destination's current requirements before consequential submission.

Also inspect:

- RGB color mode and the destination's accepted profile;
- unintended alpha or transparent pixels;
- edge halos after compositing;
- OCR or manual text extraction for extra readable marks;
- safe placement under platform crops and UI overlays;
- a one-color and low-contrast preview;
- version identifier, selected-source checksum, export checksum, and parent/edit lineage.

For print editions, treat CMYK conversion, total ink, proofing, bleed, trim, spine, dielines, and overprint as a separate prepress workflow. A streaming-ready RGB square is not proof of print readiness.

## Completion language

Say `delivery complete` only when the image files exist and pass inspection. If generation, typography, human rights review, or export is unavailable, name the missing gate and deliver the completed brief/prompt/specification without overstating status.
