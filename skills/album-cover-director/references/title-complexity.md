# Title complexity and image-native recovery

Exact image-native title rendering is a creative constraint, not a promise that
every string has equal generation reliability. Classify the requested string
before choosing a title architecture.

## Complexity profiles

- **Compact single-script:** one short visual unit with a clear silhouette.
  Material-world and spatial-field systems can carry most of the title mass.
- **Multi-unit hierarchy:** a long phrase or title with a natural lead-in and
  decisive word. Keep the exact full string, but assign a deliberate reading
  order, line break, and dominant unit.
- **Mixed-script hierarchy:** scripts have different visual color or rhythm.
  Decide which script leads; do not force identical metrics.
- **Fragile glyph set:** dense kanji, small kana, diacritics, punctuation,
  repeated letters, numerals, or marks whose substitution would change the
  metadata. Protect them with a clearer skeleton and less destructive material
  transformation.

These are visual classifications, not universal character-count limits. State
the chosen profile in the brief and title prompt.

## Architecture choice

For a complex title, prefer title grid, script hierarchy, constructed glyph
system, or a custom wordmark with a clear entry point. A physical material or
spatial phenomenon may transform the title only after the exact reading route,
line breaks, and protected glyphs are specified.

For a compact title, a material-world or spatial-field may make the complete
word the dominant structure. Do not force this strategy onto a complex string
when it makes exact reading less likely.

## Recovery without post-typesetting

If title integrity fails, do not add a font layer, redraw letters, or composite
text. Return to the title architecture and change one of these causes:

1. simplify the title's physical transformation while preserving its full
   string;
2. change the hierarchy, line break, or script leadership;
3. protect fragile glyphs from occlusion, reflection, crop, or texture;
4. choose a title behavior whose reading route is less destructive.

Record the failure as `title-integrity` and keep the failed candidate only in
the artist-local learning workspace when it is useful for comparison.
