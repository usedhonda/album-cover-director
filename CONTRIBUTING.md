# Contributing

Contributions should improve reusable image-native title systems rather than
add artist-specific preferences. A contribution may strengthen either
material-world or character-led work, but must not reintroduce ordinary title
placement.

## Corpus changes

- Add bibliographic information, source links, and original observations only.
- Do not commit album-cover images or other third-party raster assets.
- Mark uncertain designer credits as uncredited in reviewed source.
- Keep genre, era, palette, material, and rendering separate from the primary organizing pattern.
- Run python research/build_corpus.py after editing source records.

## Skill changes

- Keep SKILL.md as the workflow router and place detailed guidance in references/.
- Preserve exact-title, title-image integration, provenance, and technical delivery gates.
- Keep material-world anatomy and character-led figure/title hierarchy explicit.
- Do not add external MCP or API-key requirements without a separate design discussion.

## Checks

~~~bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
~~~
