# Contributing

Contributions should improve reusable image-native title systems rather than
add artist-specific preferences. A contribution may strengthen material-world,
spatial-field, or character-led work, but must not reintroduce ordinary title
placement.

## Share a local lesson

You do not need to be a repository developer to contribute. If a private cover
run revealed a reusable title-design principle, ask the skill to share that
lesson. It creates a local, privacy-safe draft under the relevant release's
`.album-cover-director/feedback/` folder. Review it before sharing; this step
does not upload files or create a GitHub object.

The public draft has only two files: `title-behavior-card.yaml` and a review
note. Copy those files into an issue or pull request after you confirm that the
card is abstract, rights-safe, and does not contain names, titles, lyrics,
prompts, images, local paths, or artist-specific feedback. See
[`community-contributions.md`](skills/album-cover-director/references/community-contributions.md).

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
- Add a reusable title behavior, not a genre look or a copy of a reference. Use
  `assets/title-behavior-card.yaml` and include its world engine, construction
  logic, protected title properties, rejection tests, and privacy-safe evidence
  summary.
- Keep user `.album-cover-director/` workspaces private. Never include artist
  systems, feedback, learning images, generated candidates, benchmark outputs,
  private prompts, or lyrics in a contribution.
- Public rule changes require the promotion gate in `references/production-learning.md`:
  three independent trials, varied conditions, a held-out brief, and an explicit
  boundary. One accepted image is an observation, not a universal rule.
- Do not add external MCP or API-key requirements without a separate design discussion.

## Checks

~~~bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
~~~
