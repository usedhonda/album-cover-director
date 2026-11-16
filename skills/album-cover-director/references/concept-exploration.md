# Concept exploration and selection

## Contents

- Evidence and competing readings
- A bold first board
- Preview generation
- Visual diversity before presentation
- Board and selection commands
- Preserve the reason for selection

Use this workflow for a new release or a request for more variety. A direction
is an idea with its own meaning and visual mechanism; four renders of one
direction are four variants, not four ideas. The board is a choice of concepts,
not a claim that each thumbnail is ready for distribution. Keep exploration broad: material, spatial, character-led, graphic and optical
ideas are available without a separate style-permission step. Choose the
mechanism from the music, not a preferred family. The title must participate in
that mechanism instead of decorating a finished scene.

## Evidence and competing readings

Keep `release.exact_title` separate from `song_title`, `album_title`, track
sequence, and album context. For a single, the album name can inform the image
without appearing in it. For an album, individual song titles can be evidence
without becoming extra cover text. Preserve case, punctuation, script, and
spacing in the displayed title. Only add readable text to
`allowed_readable_text` when the user asks for it.

Read lyrics through relationships and change before selecting objects:

| Evidence | Questions that generate different readings |
| --- | --- |
| Song title | Is there a double meaning, contradiction, verb, sound, unusual spelling, or visual rhythm? |
| Lyrics | Who wants what? What resists it? What changes between beginning and end? Is the speaker reliable? |
| Album title and context | What holds the tracks together? Where does this song sit in that arc? What should recur and what should change? |
| Sound, when accessible | What do rhythm, density, silence, attack, texture, or a structural break actually do? |
| Artist information | Which identity traits are stable, and which scene, camera, or title choices belong only to this release? |

Write several genuinely competing readings, normally four to six for a
12-concept board. Store each as `interpretations[].id`, `summary`, and
`evidence: [{source, anchor}]`. An anchor identifies a supplied phrase, verse,
title feature, described sound, or album context; prefer a short paraphrase to
copying whole lyrics. Label title-only interpretations as hypotheses. Never
invent lyrics, heard audio, album narratives, or artist intentions.

Turn each reading into an operation: connect, resist, erase, return, split,
hold, compress, invert, escape. Then find a visible mechanism that enacts it.
Do not make every noun into a prop. A single decisive relation is often
stronger than an inventory of symbols. Check whether changing the title to an
unrelated release would leave the image equally appropriate; if so, make the
interpretation more specific.

Fictional example: a song called **帰路** on an album called **ほどける地図**,
with the supplied description “I want to return, but I no longer fit the place.”
Possible readings include return as a trap, identity exceeding its old outline,
and proximity that never becomes arrival. Those could produce an impossible
return path, a figure/ground outline that cannot contain its subject, and an
anamorphic title that aligns only from the wrong side. The album title is
context, not additional readable cover text. These are hypotheses from that
fictional description, not a prescribed interpretation of any real song.

## A bold first board

Use these defaults unless the user specifies count, budget, or an existing
direction:

| Volume | Distinct preview directions | Production after selection |
| --- | ---: | --- |
| quick | 4 | 1 candidate per selected concept |
| standard | 12 | 1 standalone candidate for the selected concept |
| deep | 16 | 1 standalone candidate per selected concept |

For the standard 12, use [`select1from12`](../skills/select1from12/SKILL.md):
generate three 2×2 sheets of four distinct concepts, select one, then produce it
as a standalone cover.
Explicit counts override the defaults; use groups of up to four for other counts.
Split larger requests into boards of at most 24, preserving IDs
across rounds. The legacy direct-production route can still use three
directions with 3/6/12 total candidates; use it only when requested or when an
existing choice makes exploration unnecessary.

For each idea, connect a specific conflict, change or other cue from the music
to the visual rule that expresses it and to how the exact title makes that
rule work. A title-only interpretation is a hypothesis, not a lyric claim. Name the actual stroke, counter, occlusion, reflection or spatial
relationship when relevant, rather than saying merely "integrated". In a
flat design, the title can instead determine weight, negative space or
reading order. Different
meanings do not establish different compositions: if the same subject,
title and negative-space hierarchy dominates, change the image's organizing
rule, viewpoint, depth, or role of the lettering before generation. For an
optical idea, specify where to look, what changes in perception, and the
intended thumbnail size; claim success only if that effect is visible there
without an explanatory label. Ordinary headlines that could replace the title
without affecting the image's meaning, spatial relationship or reading fail.

Before rendering, give each planned idea one line in `directions.md`:
**what the music contributes → who/what leads and what happens → how square
composition and title relate**. Hide color, material and drawing style when
comparing the whole set. If the subject relationship and visible event stay
the same, rewrite that idea rather than generating another treatment. Reuse
the existing interpretation/signature notes; no parallel classification or
multi-axis score table. Use `impact-recipes.md` to change the event, not only
the surface.
Do not fill the first board with safe literal scenes and reserve the strongest
ideas for “more.” Include multiple immediately striking ideas from the start:
optical reversal, anamorphic alignment, reflection-completed lettering, unexpected scale, a single specific impossible spatial event, or severe negative space, as the evidence supports. Restraint can be
bold; adding detail, saturation, smoke, chrome, or cinematic lighting is not
the default way to increase impact. Unless the user excludes optical ideas,
plan at least one optical concept with a concrete change of reading or alignment
in the first broad exploration. Call it an illusion only when the actual image
shows that relationship, not just a recipe with that name. Do not trade title/world interaction for a
simple poster merely to make all requested slots different.

Use the existing `planned_signature` fields to retain the chosen composition,
not as a numerical difference score. Broad patterns may repeat when the actual
image events differ. No family quotas or compulsory character in every image.

For “もっと,” first identify the weak axis: too conventional a mechanism,
weak thumbnail impact, weak connection to the song, or repeated composition.
Generate another set of mechanisms, keeping previous IDs available. Freeze any
selected board contract and its images; use a new round contract for later
exploration so existing production lineage stays intact. Do not
interpret it as “polish the same scene” unless that is what the user means.

## Preview generation

Create a schema-v2 `run-contract.json` with `stage: concept-preview` from
`assets/run-contract.json`. Complete its evidence, directions, and runtime,
then run `prompt-preflight.py`. The required fields are agent working notes,
not a questionnaire for the user.

An album jacket is the end use: a memorable musical identity in a small
square, not a promotional poster, an illustrated synopsis, or an optical-test
sheet. Keep one dominant signal and a title/image relationship particular to
the release. Do not make difference by adding copy, frames or clutter.

Prompt each 2×2 sheet as four separate square album-jacket ideas, each with
the exact allowed title natively integrated. Assign each direction to a fixed
quadrant in the prompt; request clear boundaries and no external labels inside
the artwork. Keep the four concepts' composition, palette, viewpoint, and title
mechanism independent, not variations on a shared scene. Request opaque output
unless transparency is intentional. Specify visible letter anatomy, contact points,
plane crossings, occlusion and depth for material/spatial/character concepts.
A normal title printed on a dimensional sign is not letter-level integration.
Preview quality may reduce fine finish, not erase the mechanism or postpone
its optical relationship to production. Save each original sheet and record its
path, SHA-256, exact sent prompt, and quadrant-to-direction mapping in the
existing ledger. Inspect the sheet; crop each actual square panel without
altering or upscaling it and register the crop as that candidate's preview
`output_path`, retaining its sheet provenance. Use those panel files in the
existing board and selection scripts. Do not assume perfectly equal quadrants
if the image did not produce them; a missing, merged, or unreadable panel is
not a successful candidate. Preview size/quality follow the available host; a 256 px
displayed thumbnail does not imply a 256 px generation request.

When controls are exposed, use a fast iteration model and a suitable preview
quality, then spend final-resolution work on selected ideas. When controls
are not exposed, use the available image tool and record what is known.
Three sheets mean three output images instead of twelve, but actual token and
cost savings depend on host, image size, quality, inputs and retries; do not
promise a percentage. Each panel has less detail than a full-size output.
Do not promise exact API model selection, cost, latency, or batch concurrency
from a prompt-only host. Consult `references/gpt-image-2.md`.

During generation, notice whether compositions start converging and adjust
remaining ideas before spending more calls. Keep this a light observation in
the same run, not a fixed pilot batch or a per-image scoring/review loop. Stay
within count and budget; do not buy extra test images or silently spend more.

Each candidate records a stable ID, direction ID, and local `output_path`.
Mark visible title issues in `preview_notes`. A promising composition may be
shown with a clearly disclosed glyph issue; it has not passed the final text
gate. A textless illustration, collapsed mechanism, or unreadable concept is
not a useful cover preview. Do not repair either with an external title layer.

## Visual diversity before presentation

Inspect actual generated images together at thumbnail scale before presenting
the board, first looking only at the squares without labels or explanations.
Replace only the weaker member of a similar pair, keeping the distinct ideas.
A JSON validator, prompt difference, family name, or perceptual
hash cannot certify semantic diversity. Use a draft board for inspection:

```bash
python scripts/concept-board.py --contract run-contract.json --output draft-board.html --draft
```

Compare title placement/scale, figure role, camera, layout, and medium. In
particular, check for the repeated giant-title-plus-adjacent-person structure,
even when materials differ. Also compare silhouette, occupied area, value
structure, and how the title causes or is caused by the scene. Type-led work
is eligible when that relationship differs meaningfully.

Replace a convergent concept by changing its mechanism and dominant geometry;
changing its label or color is insufficient. Record the observed convergence
and the next structural change in the ledger. Preserve requested identity,
but vary its action, scale, crop, or presence when allowed. Bound internal
replacement work to the available generation budget; if only fewer distinct
concepts are ready, show that smaller set and explain the shortfall.

Before passing the board, inspect both concept quality and coverage. Identify
which candidate actually demonstrates the optical idea, its intended viewing
condition, and the visible result (two readings, aligned fragments, reflection
completion, a specific impossible join, or a near/far change). Inspect the
result at that condition as well as normal thumbnails. Record the observation
in `diversity_review.summary` and the relevant candidate's `observation`.
Prompts, labels and merely broken geometry do not count. If the mechanism
fails, revise it within budget; if none succeeds, report the missing optical
idea and an incomplete exploration rather than claiming the full brief passed.
For material/spatial/character concepts, record where lettering itself and the
world interact, not only where the figure touches a sign carrying the title.

Record `diversity_review` only after visual inspection: `status: passed`,
`compared_axes`, `summary`, and one `reviewed_candidates` entry per image with
its `id`, actual SHA-256, and a concrete `observation`. Obtain checksums with
`cover-ops.py inspect`. These records bind the review to those image files;
they do not turn a human or assistant visual judgment into an automated proof.
If an image changes, inspect it again and update its review. `--draft` is for
internal inspection only, not a way to present an unreviewed board as reviewed.

## Board and selection commands

```bash
python scripts/concept-board.py --contract run-contract.json --output concept-board.html
python scripts/concept-selection.py --contract run-contract.json --candidate C07 --reason "The return path makes the song's contradiction visible" --output production-contract.json
python scripts/prompt-preflight.py --contract production-contract.json
```

Use the installed skill's `scripts/` directory for these commands. In this
repository the full path begins `skills/album-cover-director/scripts/`.
Paths inside a contract resolve relative to that contract, not the shell's
working directory.

The self-contained HTML board embeds thumbnails and uses browser fonts for
Japanese and mixed-script labels. Its default four-column layout shows:
**candidate ID + short concept name + the interpretation it picks up**.
Labels belong outside the artwork; they never enter `allowed_readable_text`.
Keep longer mechanisms and preview notes secondary. Attach or open the board
in the host's supported preview surface. If HTML cannot be displayed, show
the same panel thumbnails with their external labels; do
not replace the requested visual comparison with a list of descriptions.

The default choice is one of the twelve, e.g. “C07”; the user may also say
“C02 and C09” or ask for another round. Repeat
`--candidate` for multiple independent selections. If the user requested
automatic art direction, select from the inspected board and record the
reason without asking for unnecessary confirmation. Otherwise the board is
the natural choice point before full production.

## Preserve the reason for selection

The selection utility creates a production contract and retains the selected
preview paths/checksums, evidence links, mechanisms, planned composition, and
`preserve_in_production` invariants. It starts with an empty production
candidate list; the previews cannot masquerade as finished candidates.

Use the selected panel as the composition reference when the host supports
editing or image references. Generate a new standalone square cover, not a
cropped panel presented as a final. Preserve the original sheet, panel crop and
their mapping; the crop is the selected preview source, not the generated sheet
or the finished cover. Make the first production prompt an explicit
translation of the selected concept: what to preserve, what needs work, and
what must not be normalized. Do not translate “properly finish this” into
more objects, a centered hero, glossy realism, or giant standalone lettering.
For a graphic-field choice, preserve its flatness, negative-space ratio, and
figure/ground relationship. For an illusion, preserve the precise viewing
condition and relationship that makes it work.

A request such as “C02's structure with C09's atmosphere” needs one primary
composition and one scoped donor. Use the CLI to retain both sources:

```bash
python scripts/concept-selection.py --contract run-contract.json --candidate C02 --donor C09 --donor-trait "lighting:soft side light" --donor-trait "color:cool blue accents" --reason "Keep C02's reversal; borrow C09's atmosphere" --output combined-production-contract.json
```

The donor path supports one primary and one donor, with explicit `color`,
`lighting`, or `texture` traits. It preserves the primary direction and stores
both images/checksums plus the donor's original direction and evidence. Carry
those scoped instructions into the native image prompt; record C02 as the
production candidate's `preview_candidate_id`. Do not average compositions.
The utility records the combination; it does not blend or generate images.
If the user wants a different structural hybrid, explore it as a new concept
and review it before selection instead of silently changing the chosen design.

Record each new production image in `candidates`, including its
`preview_candidate_id` when it derives from a selection. Compare the finished
candidate to the selected preview, not just to other finished renders. Run
the full production typography, release-identity, source, and delivery gates.
Exploration replacements are separate from the two-cycle production edit
budget. If refinement regresses, return to the selected original source.
