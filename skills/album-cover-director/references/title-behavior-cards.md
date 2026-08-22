# Title behavior cards

A title behavior card describes what lettering does in an image, not a genre,
palette, artist style, or famous-cover imitation. Existing architecture cards
are built-in behavior cards; this format lets a project test new ones without
turning every accepted image into a universal rule.

Use `assets/title-behavior-card.yaml` for a proposed card. A valid card names:

1. the lived condition or world engine that makes the behavior necessary;
2. how its components determine title anatomy or spatial transformation;
3. the protected title properties: occupied area, silhouette, reading route,
   and value priority;
4. when it helps and when it should be rejected;
5. private, rights-safe trials that tested it under different conditions.

Examples of behavior names are `route-field`, `light-distribution`,
`gesture-vector`, `terrain-lettering`, and `specimen-growth`. They are not
styles to copy; each still needs its own world engine and release evidence.

Keep new cards artist-local until they pass the public promotion gate in
`production-learning.md`. A public contribution must never include a user's
artist system, lyrics, prompts with private content, reference images, or
generated candidate images.
