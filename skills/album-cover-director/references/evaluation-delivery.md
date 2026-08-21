# Evaluation and delivery

Selection is comparative. Never score one candidate in isolation while ignoring the alternatives.

## Viewing conditions

Compare every candidate under five conditions:

1. 56 px square: main signal and silhouette;
2. 256 px square: title and secondary structure;
3. full size: craft, glyphs, artifacts, and material credibility;
4. grayscale: value hierarchy independent of hue;
5. blur: dominant masses, focal competition, and visual center.

Use `cover-ops.py contact-sheet` to create reproducible sheets. Select a leader and runner-up, and write why the rest lost.

## Scoring

Score 0–5 for concept specificity, structural distinction, composition, color/value, material credibility, typography, thumbnail recognition, artist fit, rights/provenance, and technical readiness. Typography, rights/provenance, and technical readiness are gates: a candidate scoring below 4 in any of them cannot be delivered without repair.

A high total does not excuse an incorrect title, unlicensed reference, extra text, non-square master, or unreadable thumbnail.

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

For deterministic post-typesetting, use:

~~~bash
python scripts/cover-ops.py typeset selected-master.png --output typeset-master.png \
  --text "Exact Release Title" --font /path/to/licensed-font.ttf --font-size 260 \
  --x 1500 --y 2400 --align center --tracking 8
~~~

The command applies the supplied string character-by-character, records its exact value, font file, placement, alignment, tracking, leading, and output checksum. It does not establish font licensing or complex-script shaping correctness by itself; those remain human review gates.

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
