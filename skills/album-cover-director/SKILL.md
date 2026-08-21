---
name: album-cover-director
description: Direct album, EP, and single cover artwork from a precise title plus lyrics, a music description, or audio. Use when a musician, producer, label, or designer wants structurally distinct cover concepts, GPT Image 2 prompts or edits, custom title lettering, comparative image evaluation, or release-ready square delivery files. Trigger for explicit `$album-cover-director` calls and natural-language album-cover requests; do not trigger for ordinary photo edits, posters, flyers, logos unrelated to a release, or generic image generation.
---

# Album Cover Director

Treat an album cover as a compact visual system, not a decorated illustration. Move from musical meaning to three structurally different directions, then generate, compare, refine, and deliver with typography as an independent quality gate.

## Required input

Collect or infer:

- exact release title;
- artist name;
- at least one of lyrics, a track description, or audio;
- optional genre, sonic traits, reference images, artist system, avoid list, and destination.

Preserve the exact title string. Ask only when a missing title or artist name would make the deliverable ambiguous. Never invent private artist settings or publish supplied reference images.

## Runtime controls

- `quick`: 3 candidates, one per direction.
- `standard`: 6 candidates, two per direction. Default.
- `deep`: 12 candidates, four per direction.
- Typography: `auto`, `image-native`, or `custom-wordmark`.

Every candidate shown for artistic evaluation is a complete jacket with the exact title visibly integrated into its image. A textless master is an internal production intermediate only: never score, present, or select it as a cover candidate.

If the environment exposes an image-generation tool, use GPT Image 2. If it does not, finish the brief, directions, prompts, and delivery specification, but state clearly that images and final delivery were not produced.

## Workflow

1. Create `creative-brief.yaml` from the title, artist, intended audience, listening context, shelf neighbors, musical evidence, and constraints using `assets/art-direction-brief.yaml`. Name the release's point of difference and rejection criteria.
2. Extract one central contradiction, three sensory qualities, two physical phenomena, and six to ten concrete symbols. Prefer observable nouns, actions, materials, and spatial relations over mood adjectives.
3. Read `references/design-patterns.md` and `references/title-image-architectures.md`. Choose three different primary patterns and, when title-led composition fits the brief, a distinct title-image architecture for each direction. Give each one or two secondary techniques. Keep one genre anchor and betray one genre expectation in every direction.
4. Read `references/verified-principles.md` only to solve a specific lettering or composition problem. Use at most one primary and one supporting principle. Do not research new covers during a production run; an unmatched brief is not a research failure.
5. Separate genre, era, color, material, and rendering method from the primary pattern. Do not let genre select a template by itself.
6. Read `references/typography.md`. Choose the title-image architecture before the typography mode, then define the title's structural role, occupied area, reading route, relation to the central motif, and permitted occlusion before prompting.
7. Write `directions.md` and one prompt per candidate. Each prompt must state composition, depth, palette proportions, material behavior, title treatment, exact allowed text, and exclusions. The title's surface, depth, occlusion, and connection to the dominant image geometry are mandatory. Use `references/gpt-image-2.md` for model-specific execution.
8. Generate the requested number of title-integrated candidates. Record every run or edit in `run-ledger.jsonl` using `assets/run-ledger.yaml` as the field contract.
9. Compare all candidates at 56 px, 256 px, full size, grayscale, and blur. Use `scripts/cover-ops.py contact-sheet` when Pillow is available. Score with `assets/scorecard.yaml` and `references/evaluation-delivery.md`.
10. Select a leader and runner-up. Refine only the leader. Change one variable per edit, for no more than two cycles. If an edit regresses, return to the selected original rather than editing the degraded result.
11. Apply the typography gate. If spelling, spacing, baseline, mixed-script shaping, or letter integrity fails, reject the candidate and return to its title architecture and prompt. Do not add, redraw, typeset, or composite title text after generation. A detached title strip, quiet header, generic label, caption box, or a font layer is a regression, not a fallback.
12. Validate rights, exact title, absence of unapproved readable text, square composition, thumbnail recognition, and technical requirements.
13. Export a 3000 x 3000 PNG and JPG plus a 256 px thumbnail with `scripts/cover-ops.py export`. If the required image library is unavailable, provide the exact export specification and do not claim delivery completion.
14. Write `cover-report.md` with the selected direction, why it won, typography mode, checks, provenance, unresolved human review, and paths.

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
- The title must be exact. No other readable text is allowed unless explicitly approved.
- Every evaluated candidate must show the title as a native part of the generated jacket image. Never add, redraw, typeset, or composite title text after generation.
- A custom wordmark must define skeleton, width, weight, counters, terminals, rhythm, and transformation logic; a font name alone is not a design.
- When title-led composition is selected, use one architecture from `references/title-image-architectures.md`; do not reduce it to a decorative font treatment.
- The selected cover must communicate its main figure, object, or shape at 56 px.
- At 128 px the title must read correctly and still work as a designed form when considered without the image.
- Compare the current artist series across primary pattern, setting, time of day, subject placement, camera distance, palette, dominant geometry, and title zone. If recent covers repeat four or more axes, force a structural change.
- Do not imitate a living artist's style. Translate references into observable traits and design principles.
- Do not include copyrighted cover images in outputs, repositories, or training corpora. Store citations and original observations only.

## Reference routing

- Pattern selection and anti-template logic: `references/design-patterns.md`
- Bounded, verified construction rules: `references/verified-principles.md`
- Title-led composition and reusable prompt grammar: `references/title-image-architectures.md`
- Lettering construction and fallback gate: `references/typography.md`
- Genre and era as independent axes: `references/genre-era-codes.md`
- GPT Image 2 prompting and editing: `references/gpt-image-2.md`
- Scoring, comparison, rights, and export: `references/evaluation-delivery.md`
