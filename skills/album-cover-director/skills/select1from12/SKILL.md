---
name: select1from12
description: Present twelve distinct album-cover concepts on three four-panel preview sheets, then develop the one the user selects into a standalone cover.
---

# Select one from twelve

This is the album-cover-director's initial selection workflow, not a final
artwork generator. Use the parent skill's music interpretation, title, rights,
preview contract, visual review, and production delivery requirements.

1. Plan twelve genuinely different square-cover ideas from the music. Give
   each a stable direction ID and a short visual rule, including how its title
   works. Reserve a concrete optical idea where the brief permits it. Do not
   make twelve color or material variations of one composition.
2. Generate three separate 2×2 sheets, four ideas per image. In each sheet's
   prompt map the four direction IDs to top-left, top-right, bottom-left and
   bottom-right; request distinct self-contained square covers, clear panel
   boundaries and the exact title in each, without panel labels in the art.
   Send shared release requirements once plus only those four directions.
3. Keep the original images and exact prompts. Record each sheet's path and
   SHA-256 and its quadrant-to-direction map in the existing ledger. Inspect
   the actual panels, crop each complete square panel without alteration or
   upscaling, and register its path under the corresponding candidate ID.
   Record the crop's hash and its sheet and quadrant in the ledger. Do not
   assume equal quadrants if the generated boundaries differ. If panels are
   missing, merged, or too unclear, say which ideas are incomplete; do not
   present invented or duplicated panels as twelve successful concepts.
4. Compare the real panels without labels, using the existing board and
   diversity review. Check that ideas differ in visual structure, not merely
   color; judge an optical effect only if it is visible at its intended size.
   Show the three sheets or the twelve panels with IDs outside the art, and ask
   the user to choose one. Disclose preview title errors and weak mechanisms.
5. Use `concept-selection.py` to preserve the selected panel and direction.
   With that panel as the visual reference, generate one new standalone square
   jacket that preserves its composition, title relationship and selected
   mechanism. Keep the original sheet and crop as provenance. A crop is a
   preview, never the final deliverable. Apply the parent skill's production
   checks and disclose any failure to preserve the chosen concept.

Use the existing generation budget; do not generate a test batch or silently
retry. Three sheets reduce image outputs compared with twelve individual
previews, but total token and cost savings are not guaranteed: dimensions,
quality, prompt inputs, the later standalone image and retries matter. Each
panel has less resolution; do not claim final text or optical quality from an
unclear preview. Follow explicit user changes to count, budget or selection.
