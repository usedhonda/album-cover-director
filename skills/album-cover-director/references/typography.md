# Typography and custom wordmarks

Typography is a separate design system and acceptance gate. Font selection is one input, never the whole solution.

## Research screening: when typography truly controls the cover

Use this test when selecting precedent, not only when judging a final lockup. A
cover is typography-dominant only when its lettering, numeral, glyph, or
wordmark is an organizing force rather than an identifying caption.

- **T5 — type is the image.** Remove the photographic or illustrative layer:
  the remaining title system still identifies and organizes the square. This
  includes custom-lettered titles, numeral systems, encoded text, and
  deliberately authored wordmarks.
- **T4 — type is the strongest mass.** Image and lettering can interact, but
  the first fixation, largest mass, or governing grid belongs to type. The
  image depends on that structure rather than merely sharing space with it.
- **Reject as T3.** A small title on a photograph, a label pasted onto a color
  field, or corner metadata on a geometric image is not T4/T5, even when the
  cover is historically important or visually acclaimed. Do not promote it
  because it is minimal, uses a good font, or appears in a museum collection.

Perform three quick falsification checks before recording T4/T5:

1. At 56 px, does the title shape, numeral, or lettering mass survive as the
   strongest recognition signal?
2. Hide the image layer. Does the remaining lettering system still make a
   distinctive square rather than an ordinary caption?
3. Hide the lettering layer. If the image still supplies the cover's primary
   identity, classify it as T3 unless the type governs the image's geometry.

Record borderline examples as `visual-second-pass`; do not use them as final
corpus evidence until the full-size and thumbnail tests agree.

## Choose a mode

### `image-native`

Use when letters must belong physically to the scene: painted on glass, cast as metal, formed by shadows, stitched into cloth, bent into architecture, or damaged by the same process as the image. Require exact text and prohibit all other readable text. Use this mode for conceptual integration, but inspect every glyph.

### `post-typeset`

Use when exact spelling, multilingual shaping, label delivery, or small-size precision is more important than physical integration. Generate a textless or deliberately cleared master. Preserve a quiet title zone or an intentional collision area, then typeset with a deterministic tool.

### `custom-wordmark`

Use when the title itself is the image or needs ownable identity. Define the construction system below. A wordmark may be generated as a concept study, but final spelling and spacing must be redrawn or typeset if any letter is unstable.

### `auto`

Choose `image-native` only when physical integration is concept-critical and the title is short enough to inspect. Choose `custom-wordmark` when letters organize the square. Otherwise default to `post-typeset`, especially for Japanese/Latin mixed text, long titles, credits, or strict metadata matching.

## Wordmark construction specification

Define all seven variables before prompting or drawing:

1. **Skeleton** — geometric, calligraphic, modular, monoline, contrast-stroke, constructed, or hybrid.
2. **Width** — compressed, normal, extended, or intentionally variable; define the reason.
3. **Weight** — hairline, light, book, bold, black, or asymmetric; describe where mass accumulates.
4. **Counters** — open, closed, pinched, oversized, cut through, filled, or converted to image windows.
5. **Terminals** — blunt, sheared, rounded, tapered, torn, folded, or process-derived.
6. **Rhythm** — regular, syncopated, accelerating, stepped, stacked, or interrupted; include spacing behavior.
7. **Transformation** — one repeatable operation such as cut, offset, interlock, reflection, melt, stretch, or weave. Avoid random per-letter effects.

Also specify case, line breaks, alignment, tracking, leading, baseline behavior, optical corrections, language/script handling, and relation to the image.

## Information fields are not automatically wordmarks

A cover can make all of its text into one visual field: handwriting can cover a
ground, metadata can become a calibration ring, and lyrics can operate as a
spatial score. Treat this as **type-as-material**, not as a successful title
system by default. It passes only when the viewer can still find one intended
title entry point at 128 px through at least one controlled distinction:

- scale, weight, contrast, color, or empty space;
- a unique baseline, orientation, or placement rule;
- a repeated title glyph or monogram that survives reduction; or
- a stated reading route such as edge-to-center, spiral, or vertical column.

If every line has equal visual priority, preserve the field as a texture and
add a separate exact title lockup. Never rely on a dense information field to
carry spelling accuracy by itself.

## Mixed-script titles

Do not force Japanese and Latin glyphs to share identical metrics. Match perceived color, stroke energy, vertical center, and counter openness. Decide which script leads. Test punctuation, prolonged sound marks, diacritics, small kana, and spaces against the exact metadata string.

For vertical Japanese, decide how Latin letters, numerals, punctuation, prolonged sound marks, and brackets rotate or remain upright. Test the actual title in the chosen composition; do not assume a horizontal lockup can be rotated.

## Grid, hierarchy, and lockup

Define a grid before choosing a font:

- outer margin and optical safe area;
- columns, rows, or a baseline rhythm;
- title block width and maximum line count;
- title, artist, series mark, and optional label hierarchy;
- alignment edge or intentional misalignment rule;
- protected zones around faces, hands, and focal objects;
- whether type sits behind, in front of, through, or physically inside the image.

Build one lockup, not a pile of independent labels. At least one shared alignment, repeated interval, or proportional relationship must connect all approved text. Test the lockup on the image, on a neutral field, and as a one-color silhouette.

## Spacing and optical correction

Mechanical metrics are a starting point. Inspect problematic pairs, punctuation, round-to-straight joins, diagonal letters, kana with large internal white space, and line endings. Correct perceived gaps rather than applying one global tracking value. Balance cap height against Japanese visual center, not only the font bounding box.

Avoid accidental tangencies: a title that nearly touches a face, frame edge, horizon, or object often looks less intentional than either clear separation or a decisive overlap.

## Post-typeset finishing

Keep the image master and type layer separate. Prefer vector or live type until approval. Before raster delivery:

1. confirm the exact metadata string by copy comparison;
2. resolve missing glyphs and language shaping;
3. perform optical kerning and baseline correction;
4. inspect at 100%, 128 px, and 56 px;
5. convert to outlines only in a duplicate working file when the destination requires it;
6. preserve an editable source and record the font name, version, license, and modifications;
7. rasterize once at final dimensions and inspect edge quality.

Do not use a font merely because it is installed. Verify desktop, commercial artwork, embedding, modification, and redistribution rights as applicable. A generated wordmark can still resemble a protected logo; perform a similarity and trademark review before commercial delivery.

## Image-native prompt block

State:

- `The only readable text is exactly: “<TITLE>”.`
- the material and fabrication logic;
- where the text sits in depth, what casts or receives shadow, and what may occlude it;
- the exact line break;
- `No artist name, labels, signs, captions, watermarks, logos, numbers, or pseudo-text.`

Do not ask the model to render several competing text systems in one image.

## Typography gate

Inspect at full size and 128 px:

- exact spelling and capitalization;
- no substituted, duplicated, fused, or missing glyph;
- intentional tracking and leading;
- stable baseline or deliberately specified baseline movement;
- consistent stroke and terminal logic;
- no accidental tangent with a face, edge, or focal object;
- title reads at 128 px;
- title silhouette and rhythm remain distinctive when the image is hidden.

If any accuracy item fails, do not spend repeated generation cycles repairing individual letters. Switch to the selected textless master and exact post-typesetting. The image can keep shadows, embossing, empty signage, or surface deformation prepared for the later title.
