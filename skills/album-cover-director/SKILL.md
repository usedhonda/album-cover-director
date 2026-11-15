---
name: album-cover-director
description: Direct album, EP, and single cover artwork from an exact title, with optional lyrics, artist information, and supplied reference images. Use when a musician, producer, label, or designer wants bold cover concepts, labeled thumbnail boards, lyrics or album-title interpretation, GPT Image prompts or edits, custom title lettering, comparative image evaluation, or release-ready square delivery files. Trigger for explicit `$album-cover-director` calls and natural-language album-cover requests; do not trigger for ordinary photo edits, posters, flyers, logos unrelated to a release, or generic image generation.
---

# Album Cover Director

Skill version: 0.3.0

Turn musical meaning into a broad first board of striking, structurally different cover ideas. Let the user choose by a small labeled thumbnail, then carry the chosen mechanism into full production. Do not reserve the strongest ideas for a later “more.” The specialty is image-native title systems: material worlds, spatial phenomena, character-led action, and flat graphic fields. Preserve exact title typography as a final quality gate.

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

Distinguish the exact displayed release title from song-title and album-title context. A single can draw meaning from its parent album without printing that album name. An album can draw from several songs without printing their titles. Only add text the user requested to `allowed_readable_text`; interpretation notes and board labels stay outside the artwork.

## Artist-local artist system and learning

Never remember an artist system globally. Resolve artist information in this
order:

1. artist information or an `artist-system` path explicitly supplied for the current run;
2. `<artist-root>/.album-cover-director/artist-system.md` when present and not explicitly ignored;
3. no artist information.

Use `scripts/artist-info-state.py resolve --artist-root .` to make this
resolution explicit. An explicit path affects one run only. It does not create
global memory, and an artist-local artist system never affects another artist.

When a user wants ongoing learning, read `references/project-local-learning.md`
and initialize the workspace with `scripts/project-workspace.py init
--artist-root .`. Keep artist settings, feedback, user-supplied learning
images, generated candidates, local benchmark outputs, and learned preferences
inside that ignored artist-local directory. Do not commit or upload it.

## Runtime controls

- Intent: `explore` stops at the choice board; `production` proceeds from a
  board to selection, refinement, and delivery; `improve-skill` records a
  controlled local trial. Default is `production` with concept exploration first.
- Initial exploration: `quick` = 4 distinct ideas, `standard` = 12 (default),
  `deep` = 16. Explicit counts and budgets override these defaults. Each is
  a different direction, not another render of the same one.
- After selection: generate 1 production candidate per selected idea for
  `quick`, or 2 for `standard`/`deep`. Keep unused ideas available.
- A request for direct production or an already chosen concept skips the
  board. Legacy three-direction runs retain their 3/6/12 candidate budgets.
- Typography: `auto`, `image-native`, or `custom-wordmark`.
- Title-system family: `auto`, `material-world`, `spatial-field`,
  `character-led`, or `graphic-field`. Default is `auto`.

Use explicit stages: `concept-preview` selects the idea; `production-candidate`
must pass the full quality gates. Both are prompted with the exact native title.
Clearly disclose any preview lettering issue; previews are not vetted delivery
assets. A textless master remains an internal intermediate, never a cover choice.

Use the available image-generation tool. Read `references/runtime-adapters.md`
and `references/gpt-image-2.md` for current GPT Image execution; do not claim an
unexposed model or API control was used. If no image tool exists, finish the
interpretations, directions, prompts, and delivery specification, and state that
images and delivery were not produced. Do not present text cards as generated
visual previews.

## Adult sensual editorial requests

Apply this route only when a user explicitly asks for a person-led cover to feel
sexy, sensual, glamorous, alluring, provocative, or similarly adult and
non-explicit. Read `references/gpt-image-2.md` before prompting. Do not treat
those words as a request for evasive wording or as sufficient art direction.

Translate the requested quality into a clear adult context, a fictional subject
with a specific adult age or rights-cleared reference, self-directed expression and
movement, concrete conventional or stage wardrobe, eye-level non-local framing,
and the lighting, material, color, and spatial conditions that create the
intended tension. Keep the title image-native and in the same hierarchy as the
person and scene.

Never use this route to sexualize a real person without documented consent and
rights, or to create youth cues, nudity, explicit sexual activity, fetish
framing, voyeuristic or incapacitated situations, or body-part-focused crops.
When a request is blocked or produces an unsuitable result, redesign the
specific ambiguous condition; do not retry the same request unchanged or try to
evade safety controls.

## Workflow

### 1. Resolve evidence

Resolve lyrics, artist information, reference-image roles, and rights under the
input and artist-local rules. Read local `feedback/learned-preferences.md` when
present. If an ongoing artist has no system, use
`references/artist-system-onboarding.md` to draft one without blocking the run.
Preserve user-authored continuity, while keeping this release's scene, camera,
light, title zone, and geometry free to change.

Create `creative-brief.yaml` from `assets/art-direction-brief.yaml`. Read
`references/concept-exploration.md` to separate the displayed title from song,
lyrics, and album context. Extract relationships, actions, contradictions, and
changes before objects. Build several competing interpretations, each linked to
supplied evidence. For title-only runs, label them as hypotheses; do not invent
music facts. State what makes this release different and what would feel generic.

### 2. Diverge before polishing

Read `references/impact-recipes.md`, `references/design-patterns.md`, and
`references/title-image-architectures.md`. Privately sketch roughly twice the
requested count, then retain the strongest, most distinct ideas. Default to a
12-direction first board. Include bold mechanisms from the first pass: optical
reversal, impossible spatial relations, forceful flat shapes, unexpected scale,
severe negative space, or an ordinary scene with one impossible event, when
supported by the music. More detail is not automatically more impact.

Give each direction an ID, short name, `interpretation_id`, `visual_mechanism`,
`planned_signature`, and `preserve_in_production` list. Record title placement
and scale, figure role, camera, layout, and medium. Reusing a primary pattern is
allowed when the actual structures differ. Do not force equal family quotas,
a literal illustration, or a recurring character into every slot. Read
`references/verified-principles.md` only to solve a specific construction issue;
do not turn a production run into another precedent search.

### 3. Design the native title

Read `references/typography.md` and `references/title-complexity.md`. Classify the
exact title and specify its reading route, protected glyphs, occupied area,
value hierarchy, and relation to the dominant shape. Select a family:

- `material-world`: a lived world engine and material determine the title's
  skeleton, counters, joins, and role; an object inventory is insufficient.
- `spatial-field`: a named phenomenon distributes and transforms the title
  across the square while preserving its reading skeleton.
- `character-led`: the figure's action and title form one causal hierarchy.
- `graphic-field`: positive/negative shape, edge, rhythm, or a flat color rule
  makes the title part of the image's structure; no simulated physical world
  or person is needed.

For live or spatial scenes, lock title hierarchy before allowing physically
caused exposure, occlusion, wear, motion, or crop elsewhere. For intentionally
flat or pristine work, preserve its graphic clarity. The title must be largest
**or most structurally decisive**, not always a giant freestanding word.

### 4. Preflight and generate previews

Start `run-contract.json` from `assets/run-contract.json` with schema version 2
and `stage: concept-preview`. Complete release text, evidence, runtime, rights,
and the chosen directions. Run `scripts/prompt-preflight.py --contract
run-contract.json`. Write `directions.md` and one prompt per concept. Define
composition, depth or flatness, palette proportions, material or graphic rule,
native title treatment, exact allowed text, and exclusions.

Default to excluding unmotivated yellow, parchment, sepia, brass, amber, and
golden casts. If warmth is intentional, name its cause, bounded regions, and
neutral anchor. Do not invent an illumination requirement for a flat graphic
palette. Use `references/gpt-image-2.md` for host-aware execution.

Generate each concept independently, preserving its source file. Do not ask
for one image containing the whole grid. Record stage, prompt, runtime,
references, source dimensions, and result in `run-ledger.jsonl` using
`assets/run-ledger.yaml`. Add each output and any visible lettering issue to
`candidates`. An initial preview may have a disclosed glyph issue, but must
show the intended title mechanism and a readable concept.

### 5. Inspect and present the board

Use `scripts/concept-board.py --contract run-contract.json --output
draft-board.html --draft` for internal visual inspection. Compare the actual
images as a set: silhouette, title zone/scale, figure role, camera, geometry,
medium, and the relationship that makes the title part of the image. Replace
visually convergent ideas before presentation. Different prompts, names,
materials, or perceptual hashes do not prove diversity. Record the observed
failure and next structural change, not just a new label.

Complete the checksum-bound `diversity_review` after inspection, then render
`concept-board.html` without `--draft`. Present the compact thumbnail grid,
with IDs, short names, and the meaning picked up from the music outside each
image. These external labels never become cover typography. Follow
`references/concept-exploration.md` for commands and display fallback.

### 6. Carry the chosen idea into production

Accept a candidate ID, multiple IDs, or a scoped combination such as one
concept's structure with another's atmosphere. If the user delegated choice,
select from the inspected board and record why; otherwise let the board be the
choice point. Do not require a second long brief.

Use `scripts/concept-selection.py` to create `production-contract.json` from
the selected previews. It preserves their source paths/checksums, evidence,
mechanisms, composition signatures, and invariants. For a combination, name
one primary composition and scope the donor trait; do not average all ideas.
Use the primary image as a reference/edit source when supported. Record the
primary `preview_candidate_id` on each resulting production candidate.

Switch to `stage: production-candidate`, apply the source-resolution capability
for the actual runtime, preflight the production contract, and generate the
selected idea(s) at production quality. Keep the exact reason for selection:
flat stays flat, negative space stays spacious, and an illusion keeps its
viewing relationship. Do not polish the work into a conventional centered
hero, add objects, or make the title a separate headline.

### 7. Compare, refine, and deliver

Compare production candidates and their selected previews at 56 px, 128 px,
256 px, full size, grayscale, and blur. Use `scripts/cover-ops.py contact-sheet`,
`preflight-source`, and `compare`. Score with `assets/scorecard.yaml` and
`references/evaluation-delivery.md`; image metadata is automated, visual
quality and text correctness are not. A human must record exact-title and
unapproved-readable-text results before final handoff. Reject generic poster,
advertisement, app tile, or concept-art results that lack a music-release identity.

Choose a leader and a runner-up when alternatives exist. Use
`scripts/action-router.py` for a recorded failure. Change one variable per edit,
for at most two production refinement cycles. Exploration replacements do not
consume those cycles. Compare against the selected original and return to it
when an edit regresses. Never add, redraw, typeset, or composite title text to
repair the image. Fix the native title architecture and regenerate instead.

Check the exact title, extra readable text, rights, square composition,
thumbnail impact, retained selected mechanism, and runtime source requirements.
Export 3000 x 3000 PNG/JPG and a 256 px thumbnail with `scripts/cover-ops.py
export`. Run delivery preflight for the 3000 px masters and verify the thumbnail
size. Create `handoff-manifest.json` with `scripts/handoff-manifest.py` only after
source-to-export lineage and structured human text verification are complete.
A concept preview cannot pass as a production handoff. Disclose any resizing.
If a required capability is absent, report the exact missing step.

Write `cover-report.md` with the selected ID and reason, evidence, retained
mechanism, typography checks, provenance, unresolved review, and output paths.
On selection/correction feedback, use `assets/project-feedback.yaml` and
`scripts/feedback-store.py record` with every reviewed image and supplied
reference via `--image`. It creates `feedback/<release-slug>/feedback.json`,
copies images, and refreshes `feedback/learned-preferences.md`. Normalize a
reusable preference only when it applies beyond this release. Keep all of it artist-local.

## Skill-learning mode

Ordinary cover runs never become public training data. A reviewed run may improve only that artist's private `feedback/learned-preferences.md` under the rules in `references/project-local-learning.md`. When the user explicitly asks to improve this public skill, read `references/production-learning.md`, `references/title-behavior-cards.md`, and use `assets/learning-observation.yaml` for controlled, rights-safe trials. Compare winners against rejected candidates, compare one-variable edits against their parents, and validate proposed rules on held-out briefs. Promote only abstract, reproducible design decisions; never promote private lyrics, artist information, reference images, generated images, or one user's taste as a universal rule.

When a user explicitly says that a local lesson should be shared with the Album
Cover Director community, read `references/community-contributions.md`. Draft
one abstract title behavior card, then call `scripts/contribution-draft.py
prepare` to keep the draft under that release's private feedback folder. Show
the draft and evidence status to the user. Never upload it or create a GitHub
Issue, branch, or pull request without a later explicit request.

## Output contract

```text
album-cover/<release-slug>/
├── creative-brief.yaml
├── run-contract.json                  # concept-preview
├── concept-board.html
├── production-contract.json           # selected concepts
├── directions.md
├── prompts/
├── run-ledger.jsonl
├── selected-master.png
├── delivery/cover-3000.png
├── delivery/cover-3000.jpg
├── delivery/thumbnail-256.png
├── handoff-manifest.json
└── cover-report.md
```

## Non-negotiable gates

- The first board must offer different image-organizing mechanisms, not palette or rendering variants. Inspect actual images and record diversity before presentation; preflight cannot make that visual judgment.
- A supplied identity reference may stabilize who appears, but it must not stabilize the whole cover. Pose, action, setting, camera distance, dominant geometry, light, palette, and title architecture remain release-specific unless explicitly fixed.
- The selected image must read as a music-release identity, not as a poster, advertisement, editorial illustration, app tile, game splash screen, or generic concept art. Its square must have one dominant identity signal, intentional edge behavior, controlled information density, and a reason to exist beyond illustrating the title literally.
- For a live, physical, documentary, or spatial direction, reserve unevenness for a named visual cause such as exposure, motion, smoke, reflection, wear, crop, or occlusion. Lock the title's occupied area, silhouette, reading route, and value priority before varying anything else. Reject a scene in which every face, surface, color, and effect is equally polished, bright, and legible; do not let controlled irregularity reduce title dominance.
- The title must be exact. No other readable text is allowed unless explicitly approved.
- Classify the title's complexity before generation. If it fails, change the
  native title architecture, hierarchy, or protected glyph treatment; never
  fall back to post-typesetting, redraw, or compositing.
- Every cover choice must show its title natively within the generated image. Preview imperfections must be labeled and cannot bypass production gates. Never add, redraw, typeset, or composite title text after generation; comparison labels belong outside the cover.
- A custom wordmark must define skeleton, width, weight, counters, terminals, rhythm, and transformation logic; a font name alone is not a design.
- When title-led composition is selected, use one architecture from `references/title-image-architectures.md`; do not reduce it to a decorative font treatment.
- A material title-world must make the chosen material determine the title's skeleton, counters, joins, terminals, spacing, and image role. Reject a normal typeface with a texture fill, or a title merely placed over its material scene.
- A material title-world also needs a world engine beyond its components. Reject a clean inventory, product mockup, or equipment catalogue even when its title anatomy is correct.
- Reject an unmotivated warm-yellow, parchment, sepia, brass, amber, or golden cast. A warm palette must have a release-specific physical or production cause, bounded warm regions, and a named neutral anchor.
- A spatial-field title system must make a named spatial phenomenon distribute and transform the native title across the square. A conventional letter skeleton is allowed only as the protected reading structure, never as a flat overlay.
- A character-led title system must make the figure's action, setting, and title occupy one hierarchy. Reject a conventional illustration with a title positioned above, below, or beside it.
- A graphic-field title system must make native letterforms, figure/ground, and graphic rule inseparable. Reject a generic font caption on an otherwise independent graphic. Preserve flatness when that is the selected idea.
- A finished candidate must retain the selected preview's visual mechanism and invariants; higher detail alone is not an improvement.
- The selected cover must communicate its main figure, object, or shape at 56 px.
- At 128 px the title must read correctly and still work as a designed form when considered without the image.
- Compare the current artist series across primary pattern, setting, time of day, subject placement, camera distance, palette, dominant geometry, and title zone. If recent covers repeat four or more axes, force a structural change.
- Do not imitate a living artist's style. Translate references into observable traits and design principles.
- Do not include copyrighted cover images in outputs, repositories, or training corpora. Store citations and original observations only.

## Reference routing

- Lyrics/title/album interpretation, boards, and selection: `references/concept-exploration.md`
- Optical, graphic, and event-based exploration: `references/impact-recipes.md`
- Pattern selection and anti-template logic: `references/design-patterns.md`
- Bounded, verified construction rules: `references/verified-principles.md`
- Title-led composition, material title-worlds, and reusable prompt grammar: `references/title-image-architectures.md`
- Lettering construction and fallback gate: `references/typography.md`
- Genre and era as independent axes: `references/genre-era-codes.md`
- Current GPT Image prompting and editing: `references/gpt-image-2.md`
- Artist-local settings, feedback, image history, and learned preferences: `references/project-local-learning.md`
- First-draft and safe update rules for `artist-system.md`: `references/artist-system-onboarding.md`
- Automatic local feedback, image history, and preference promotion: `scripts/feedback-store.py`
- Complex and mixed-script title architecture: `references/title-complexity.md`
- Testing and adding reusable title behaviors: `references/title-behavior-cards.md`
- Scoring, comparison, rights, and export: `references/evaluation-delivery.md`
- Controlled production learning and rule-promotion gates: `references/production-learning.md`
- Runtime identity and portable contract boundary: `references/runtime-adapters.md`
- Turn a local lesson into a reviewable community draft: `references/community-contributions.md`
