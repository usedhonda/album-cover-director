# GPT Image 2 execution

This file isolates model-specific behavior so the design grammar can survive future model changes.

## Model role

Use `gpt-image-2` for generation and edits when available. It supports image generation, image editing, and high-fidelity image inputs. Use the current tool or API surface exposed by the host; do not require an external MCP server or API key from the user.

Official model reference: <https://developers.openai.com/api/docs/models/gpt-image-2>

## Prompt order

Write prompts in this order:

1. output type: square album cover;
2. primary pattern and visual thesis;
3. subject/action and spatial composition;
4. foreground, midground, background, light, and dominant geometry;
5. palette with approximate area proportions;
6. physical medium and production process;
7. image-native title architecture, exact title, glyph count, reading order, material, position, color hierarchy, and line break;
8. thumbnail priority;
9. exclusions and rights-safe constraints.

Use concrete visual nouns and verbs. Do not send the model an essay about the song. Translate interpretation into observable image decisions.

## Variants

Treat each candidate as an independent generation. Do not use one image and request palette-only variants when the brief requires structural diversity. Log direction ID, candidate ID, prompt, inputs, model, size, quality, output, and human notes.

## Reference images

Use only user-provided or rights-cleared images. Describe what each reference controls: identity, pose, garment, composition, material, or palette. Do not ask for a direct replica. Preserve critical identity with high-fidelity input when the host supports it, while changing only the scoped variables.

## Edits

Edit one variable at a time. State invariants before the requested change: subject identity, crop, title string, title position, palette, and background. Permit at most two refinement cycles. If the result regresses, return to the selected original file instead of using the latest edit as the next input.

## Text strategy

Generate every artistic candidate with the exact title visibly integrated into the jacket. Generate all title lettering in the same image as the scene: never add, redraw, typeset, or composite letters afterward. For complex-script or long titles, state each glyph exactly once, its reading order, placement, relative scale, color hierarchy, and relation to the scene. If letter accuracy fails, reject the candidate and use one of the two allowed refinement cycles to regenerate from a more explicit prompt. Never present a textless master, a detached title banner, generic caption box, or font layer as a cover candidate.

## Required provenance

Record the model identifier or host tool, date, prompt, reference-image ownership statement, edit parent, and delivery transformations. Never imply that an ungenerated prompt is a completed cover.
