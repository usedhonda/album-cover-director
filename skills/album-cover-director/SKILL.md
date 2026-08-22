---
name: album-cover-director
description: Direct album, EP, and single cover artwork from an exact title, with optional lyrics, artist information, and supplied reference images. Use when a musician, producer, label, or designer wants structurally distinct cover concepts, GPT Image 2 prompts or edits, custom title lettering, comparative image evaluation, or release-ready square delivery files. Trigger for explicit `$album-cover-director` calls and natural-language album-cover requests; do not trigger for ordinary photo edits, posters, flyers, logos unrelated to a release, or generic image generation.
---

# Album Cover Director

Treat an album cover as a compact visual system, not a decorated illustration. Move from musical meaning to three structurally different directions, then generate, compare, refine, and deliver with typography as an independent quality gate. Its core specialty is image-native title systems: either the title becomes a physical world, or a character, gesture, and title share one image structure.

## Input contract

The only required input is:

- exact song, album, or release title.

Lyrics and artist information are optional. Accept lyrics either inline in the prompt or from a readable file path. Accept artist information inline or from a readable file path; it may contain the artist name, genre, sonic character, points to emphasize, recurring identity or character rules, visual language, palette, typography, avoid list, references, and series-continuity guidance. Audio, a track description, destination, and other context are also optional.

Supplied images are optional. Accept one or more attached images or readable image file paths and classify each requested use:

- `identity-reference`: keep a recognizable person, character, mascot, costume, or other recurring identity while creating a new song-specific pose, action, setting, composition, light, and title relationship;
- `source-asset`: directly edit, transform, or incorporate the supplied image itself; use this only when the user asks to use the actual image and has the necessary rights;
- `visual-direction`: derive non-exclusive traits such as palette balance, material behavior, camera distance, or compositional energy without copying distinctive content.

Interpret “use this person/character” as `identity-reference`, “use or edit this actual image” as `source-asset`, and “use this only as mood/reference” as `visual-direction` when the request is clear. Do not let a recurring identity force the same pose, scene, palette, or title placement across releases. Record the use mode and rights basis in the brief.

Proceed from the title alone when no optional input is supplied. Preserve the exact title string, and do not invent an artist name or private artist settings. The exact title is the only readable cover text allowed by default; an artist name or other text requires explicit approval.

## Remembered artist-information path

Remember only the most recently supplied, readable artist-information file path. Use `scripts/artist-info-state.py` to store it as `last_artist_information_path` under `$CODEX_HOME/album-cover-director/state.yaml` when `CODEX_HOME` is set, or `~/.codex/album-cover-director/state.yaml` otherwise. Never store the artist-information contents, lyrics, lyrics path, title, supplied images, image paths, references, or generated brief in this state file.

Resolve artist information in this order:

1. an artist-information file path explicitly supplied for the current run;
2. the remembered path, when it still exists and is readable;
3. no artist information.

When a new readable artist-information path is supplied, replace the remembered path. Inline artist information applies only to the current run and is not persisted. If the remembered path is missing or unreadable, continue from the remaining inputs without blocking and report that the remembered artist information was not used. Honor an explicit request to ignore it for one run or forget it entirely.

## Runtime controls

- `quick`: 3 candidates, one per direction.
- `standard`: 6 candidates, two per direction. Default.
- `deep`: 12 candidates, four per direction.
- Typography: `auto`, `image-native`, or `custom-wordmark`.
- Title-system family: `auto`, `material-world`, or `character-led`. Default is `auto`.

Every candidate shown for artistic evaluation is a complete jacket with the exact title visibly integrated into its image. A textless master is an internal production intermediate only: never score, present, or select it as a cover candidate.

If the environment exposes an image-generation tool, use GPT Image 2. If it does not, finish the brief, directions, prompts, and delivery specification, but state clearly that images and final delivery were not produced.

## Workflow

1. Resolve the optional lyrics and artist information according to the input and remembered-path rules. Classify every supplied image as `identity-reference`, `source-asset`, or `visual-direction`, and record its rights basis. Create `creative-brief.yaml` from the title and whatever optional evidence is available using `assets/art-direction-brief.yaml`.
2. Build the interpretation from the available evidence:
   - With lyrics or a description, extract one central contradiction, three sensory qualities, two physical phenomena, and six to ten concrete symbols. Prefer observable nouns, actions, materials, and spatial relations over mood adjectives.
   - With artist information, separate continuity requirements from variables that must change for this release. Treat genre, sonic character, and emphasis as evidence, not as a template selector.
   - With the title alone, write three clearly labeled hypotheses: a literal reading, a metaphorical tension, and a formal reading based on the title's sound, script, length, or geometry. Select one hypothesis per direction and do not present inferred story details as facts about the music.
   - For every material-world direction, name a **world engine** before naming components: a human act, social relation, ritual, memory, weather, spatial pressure, or another lived condition that makes the material necessary. An inventory of objects is not a world engine.
   Name the release's point of difference and rejection criteria from this evidence. Lack of optional input is never a reason to stop.
3. Read `references/design-patterns.md` and `references/title-image-architectures.md`. Choose three different primary patterns and a title-system family for each direction. `auto` chooses `material-world` when the title can become a physical system; it chooses `character-led` when a supplied artist system, rights-cleared identity reference, or brief calls for a central figure. Give each one or two secondary techniques. Keep one genre anchor and betray one genre expectation in every direction.
4. Read `references/verified-principles.md` only to solve a specific lettering or composition problem. Use at most one primary and one supporting principle. Do not research new covers during a production run; an unmatched brief is not a research failure.
5. Separate genre, era, color, material, and rendering method from the primary pattern. Do not let genre select a template by itself.
6. Read `references/typography.md`. Choose the title-system family before the typography mode, then define the title's structural role, occupied area, reading route, relation to the central motif, and permitted occlusion before prompting. For `material-world`, define the world engine, material vocabulary, mapping from material to skeleton/counters/joins/terminals, and the title's role in that world. For `character-led`, define the central figure's action, the title's shared hierarchy, and the physical or gestural connection between them.
7. Write `directions.md` and one prompt per candidate. Each prompt must state composition, depth, palette proportions, material behavior, title treatment, exact allowed text, and exclusions. The title's surface, depth, occlusion, and connection to the dominant image geometry are mandatory. For `material-world`, forbid normal fonts, wordmarks, letters merely placed on a scene, and a clean catalog of components that does not enact the world engine. For `character-led`, forbid a figure with a detached title header, footer, label, or caption. Use `references/gpt-image-2.md` for model-specific execution.
8. Generate the requested number of title-integrated candidates. Record every run or edit in `run-ledger.jsonl` using `assets/run-ledger.yaml` as the field contract.
9. Compare all candidates at 56 px, 128 px, 256 px, full size, grayscale, and blur. Use `scripts/cover-ops.py contact-sheet` when Pillow is available. Score with `assets/scorecard.yaml` and `references/evaluation-delivery.md`. Reject work that reads primarily as a poster, advertisement, editorial illustration, app tile, game splash screen, or generic AI concept image rather than a durable music-release identity.
10. Select a leader and runner-up. Refine only the leader. Change one variable per edit, for no more than two cycles. If an edit regresses, return to the selected original rather than editing the degraded result.
11. Apply the typography gate. If spelling, spacing, baseline, mixed-script shaping, or letter integrity fails, reject the candidate and return to its title architecture and prompt. For `material-world`, also reject a candidate when its material could be removed without changing the letter anatomy, when the scene could remain after removing the title, or when it still reads as a product catalogue after removing the title. For `character-led`, reject it when removing the figure leaves a normal wordmark, or removing the title leaves a conventional character illustration. Do not add, redraw, typeset, or composite title text after generation. A detached title strip, quiet header, generic label, caption box, or a font layer is a regression, not a fallback.
12. Validate rights, exact title, absence of unapproved readable text, square composition, thumbnail recognition, and technical requirements.
13. Export a 3000 x 3000 PNG and JPG plus a 256 px thumbnail with `scripts/cover-ops.py export`. If the required image library is unavailable, provide the exact export specification and do not claim delivery completion.
14. Write `cover-report.md` with the selected direction, why it won, typography mode, checks, provenance, unresolved human review, and paths.

## Skill-learning mode

Ordinary cover runs do not become training data and do not create cross-run memory beyond the artist-information path above. When the user explicitly asks to improve this skill, read `references/production-learning.md` and use `assets/learning-observation.yaml` for controlled, rights-safe trials. Compare winners against rejected candidates, compare one-variable edits against their parents, and validate proposed rules on held-out briefs. Promote only abstract, reproducible design decisions; never promote private lyrics, artist information, reference images, generated images, or one user's taste as a universal rule.

## Output contract

```text
album-cover/<release-slug>/
├── creative-brief.yaml
├── directions.md
├── prompts/
├── run-ledger.jsonl
├── selected-master.png
├── delivery/cover-3000.png
├── delivery/cover-3000.jpg
├── delivery/thumbnail-256.png
└── cover-report.md
```

## Non-negotiable gates

- Three directions must differ in image-organizing structure, not merely palette or rendering style.
- A supplied identity reference may stabilize who appears, but it must not stabilize the whole cover. Pose, action, setting, camera distance, dominant geometry, light, palette, and title architecture remain release-specific unless explicitly fixed.
- The selected image must read as a music-release identity, not as a poster, advertisement, editorial illustration, app tile, game splash screen, or generic concept art. Its square must have one dominant identity signal, intentional edge behavior, controlled information density, and a reason to exist beyond illustrating the title literally.
- The title must be exact. No other readable text is allowed unless explicitly approved.
- Every evaluated candidate must show the title as a native part of the generated jacket image. Never add, redraw, typeset, or composite title text after generation.
- A custom wordmark must define skeleton, width, weight, counters, terminals, rhythm, and transformation logic; a font name alone is not a design.
- When title-led composition is selected, use one architecture from `references/title-image-architectures.md`; do not reduce it to a decorative font treatment.
- A material title-world must make the chosen material determine the title's skeleton, counters, joins, terminals, spacing, and image role. Reject a normal typeface with a texture fill, or a title merely placed over its material scene.
- A material title-world also needs a world engine beyond its components. Reject a clean inventory, product mockup, or equipment catalogue even when its title anatomy is correct.
- A character-led title system must make the figure's action, setting, and title occupy one hierarchy. Reject a conventional illustration with a title positioned above, below, or beside it.
- The selected cover must communicate its main figure, object, or shape at 56 px.
- At 128 px the title must read correctly and still work as a designed form when considered without the image.
- Compare the current artist series across primary pattern, setting, time of day, subject placement, camera distance, palette, dominant geometry, and title zone. If recent covers repeat four or more axes, force a structural change.
- Do not imitate a living artist's style. Translate references into observable traits and design principles.
- Do not include copyrighted cover images in outputs, repositories, or training corpora. Store citations and original observations only.

## Reference routing

- Pattern selection and anti-template logic: `references/design-patterns.md`
- Bounded, verified construction rules: `references/verified-principles.md`
- Title-led composition, material title-worlds, and reusable prompt grammar: `references/title-image-architectures.md`
- Lettering construction and fallback gate: `references/typography.md`
- Genre and era as independent axes: `references/genre-era-codes.md`
- GPT Image 2 prompting and editing: `references/gpt-image-2.md`
- Scoring, comparison, rights, and export: `references/evaluation-delivery.md`
- Controlled production learning and rule-promotion gates: `references/production-learning.md`
