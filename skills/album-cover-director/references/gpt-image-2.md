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
7. title-system family, image-native architecture, exact title, glyph count, reading order, material or character connection, position, color hierarchy, and line break;
8. thumbnail priority;
9. exclusions and rights-safe constraints.

Use concrete visual nouns and verbs. Do not send the model an essay about the song. Translate interpretation into observable image decisions.

## Adult sensual editorial requests

Use this section only when the user explicitly asks for a person-led cover to
feel sexy, sensual, glamorous, alluring, provocative, or similarly adult and
non-explicit. It converts an ambiguous desired effect into art direction; it is
not a safety workaround and does not apply to ordinary portraits by default.

### Interpret the request

State the legitimate cover context first, then use these variables instead of
repeating the ambiguous adjective:

1. **Subject and rights**: a fictional person with a stated adult age, or a
   rights-cleared reference with documented consent for the requested use.
   Do not assign a gender unless the brief does.
2. **Agency and action**: self-possessed gaze, controlled posture, a stage
   action, dance movement, or another intentional gesture; never vulnerability,
   incapacity, surveillance, or surprise as the source of allure.
3. **Wardrobe and silhouette**: name opaque, conventional fashion or stagewear,
   its material, and how tailoring or movement makes the silhouette legible.
4. **Composition**: use an eye-level frame with balanced attention to face,
   garment, title, and setting. Avoid intimate, voyeuristic, or body-part-led
   crops.
5. **Light, color, and space**: make allure come from a named lighting setup,
   texture, palette relationship, and a public or professional setting such as
   a stage, soundstage, foyer, or editorial set.

Keep the existing prompt order and title-system requirements. The exact title
must remain generated within the image and share a hierarchy with the subject;
do not reserve detached text space or add typography afterward.

### Boundaries and recovery

Include one short, concrete boundary statement when it resolves a real
ambiguity: adult subject, fully clothed opaque wardrobe, non-nude,
non-explicit, and no real-person sexualization. Prefer positive wardrobe and
composition details over a long negative list.

Reject a concept that combines youth cues, private or voyeuristic settings,
unaware or incapacitated subjects, transparent or displaced clothing, or
body-part emphasis. Redesign the scene rather than substituting euphemisms.

If the host exposes a moderation error, record whether it identifies the input
or output and change the relevant condition: clarify adult status and rights,
replace ambiguous clothing or setting, widen a crop, restore agency, or make
the intended source of allure explicit. Do not retry an unchanged request. An
API `moderation` setting is host-specific and never disables policy or replaces
this design check.

## Palette-temperature guard

GPT Image 2 can drift toward parchment, sepia, brass, amber, or warm-yellow
light when the brief does not explicitly control the neutral point. Treat this
as a default quality risk, not an artist preference. Every direction must name
its intended neutral, dominant and accent colors, and palette temperature.

Default to neutral or release-derived temperature and explicitly exclude an
unmotivated yellow, parchment, sepia, brass, amber, or golden cast. This is not
a default cool-blue look: use the release's actual color script. Warmth is
allowed only when the brief intentionally calls for it—such as sunset,
candlelight, sodium vapor, gold, autumn foliage, or a warm-print process. In
that case name the physical cause, the warm regions, and the intended neutral
anchor so warmth does not contaminate the whole square. For a selected image
that is otherwise correct, treat temperature as a small correction only:
preserve composition, drawing, title, material, and value structure; do not
reimagine the cover with an all-blue, neon, or night-time palette.

## Controlled irregularity

When the direction claims a live, physical, documentary, or spatial event,
write a hierarchy lock before requesting any irregularity. Lock the title's
occupied area, silhouette, reading route, and value priority, along with any
subject whose recognition is essential. Then choose one or two irregularities
that have a physical cause: uneven exposure, falling-off light, smoke, a
moving body, scratched reflection, crop, occlusion, wear, or accidental
darkness. Name the cause, the background region where it acts, and the one
specific variation it permits.

This is not a request for generic grain, blur, dirt, or randomness. Do not
apply smoke, motion blur, dimming, gaps, or distortion to the locked title
silhouette unless a small, named title-edge effect is explicitly required; it
may never alter the title's reading route, occupied area, or dominance. Let
surrounding detail become partial only where the named cause makes that
believable. Do not apply this rule to a deliberately pristine graphic,
diagrammatic, or product-like direction.

## Variants

Treat each candidate as an independent generation. Do not use one image and request palette-only variants when the brief requires structural diversity. Log direction ID, candidate ID, prompt, inputs, model, size, quality, output, and human notes.

## Reference images

Use only user-provided or rights-cleared images. Describe what each reference controls: identity, pose, garment, composition, material, or palette. Do not ask for a direct replica. Preserve critical identity with high-fidelity input when the host supports it, while changing only the scoped variables.

## Edits

Edit one variable at a time. State invariants before the requested change: subject identity, crop, title string, title position, palette, and background. Permit at most two refinement cycles. If the result regresses, return to the selected original file instead of using the latest edit as the next input.

## Text strategy

Generate every artistic candidate with the exact title visibly integrated into the jacket. Generate all title lettering in the same image as the scene: never add, redraw, typeset, or composite letters afterward. For complex-script or long titles, state each glyph exactly once, its reading order, placement, relative scale, color hierarchy, and relation to the scene. If letter accuracy fails, reject the candidate and use one of the two allowed refinement cycles to regenerate from a more explicit prompt. Never present a textless master, a detached title banner, generic caption box, or font layer as a cover candidate.

For `material-world`, state the world engine before the component vocabulary:
the act, relation, ritual, memory, weather, or spatial pressure that makes the
material necessary. Then state exactly how the material forms strokes,
counters, joins, terminals, spacing, and the title's role in that world.
Explicitly reject product shots, component catalogues, and equipment merely
arranged into letters. For `spatial-field`, state the causal phenomenon, title
hierarchy lock, protected letter skeleton, reading route, and the spatial
planes that transform the title; ordinary-looking letters are permitted only
as native scene structure, never as a flat overlay. For `character-led`, state the figure's action, the title's shared
scale/hierarchy, contact points, and depth order. In either case, explicitly
forbid ordinary typography placed on a finished scene.

## Required provenance

Record the model identifier or host tool, date, prompt, reference-image ownership statement, edit parent, and delivery transformations. Never imply that an ungenerated prompt is a completed cover.
