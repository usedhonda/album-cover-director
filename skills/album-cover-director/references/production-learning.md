# Controlled production learning

Use this mode only when the user explicitly asks to improve Album Cover Director. Ordinary cover requests remain private production work and are not public training data. Read `project-local-learning.md` first when the evidence came from a user's project.

## Why this complements precedent research

Verified precedent research can reveal construction ideas, but it cannot prove that this skill applies them well. Production learning tests the skill's own decisions. It learns from contrast: selected versus rejected candidates, an edit versus its parent, and a proposed rule versus a held-out brief.

The goal is not to accumulate styles or imitate successful covers. The goal is to identify small decision rules that repeatedly improve release identity, musical specificity, title integrity, structural distinction, and thumbnail behavior.

## Evidence order

Use evidence in this order:

1. explicit user selection or correction;
2. objective gates such as exact title, unapproved text, square format, rights, and export validity;
3. comparative multi-scale evaluation using the scorecard;
4. one-variable edit outcomes;
5. verified precedent principles used to explain, not override, production evidence.

Never convert one user's aesthetic preference into a universal rule. Artist-specific continuity belongs in that user's artist-information file.
Artist-local feedback belongs in that artist's `.album-cover-director/` workspace; promote it to a public rule only through the gate below.

## Trial matrix

Test a proposed rule against deliberately different briefs. Include title-only and evidence-rich cases, short and long titles, Latin and non-Latin scripts, quiet and high-density music, material-world, spatial-field, and character-led systems, and at least one case outside the conditions that produced the rule.

Use rights-cleared, synthetic, or maintainer-owned inputs. Keep generated trial images outside the public repository. The repository may contain only abstract observations, checksums or local trial IDs, and the resulting decision rule.

## Efficient image-search discovery

Use image search to widen the visual vocabulary before controlled trials, not to copy a cover or declare a production rule. Start with the major groups represented in `research/typography-led-genre-intake.yaml`: jazz, hip-hop, pop, Latin pop/reggaeton, rock/punk, electronic, metal, R&B/soul, Japanese pop/rock/electronic, and Afrobeat.

For each genre group, use three query shapes:

1. `<genre> album cover bold typography large title`;
2. `<genre> record sleeve oversized lettering typographic design`;
3. a query naming one underrepresented structural role, such as `vertical title rail`, `repeated title field`, `title as symbol`, or `environmental signage`.

Screen in three passes:

1. At search-thumbnail size, reject templates, fan art, posters, ordinary portrait-plus-caption layouts, and covers where text has no structural role.
2. Open the square and identify what the lettering physically does: fill, rail, orbit, repeat, collide, become material, become a sign, govern a crop, or bind a scene.
3. Open the source page and verify the release title and artist. Record the source page and an original visual observation, but do not download or commit the cover image.

Keep two to four candidates per genre group, prioritizing a new typography role over another famous album. Deduplicate by `typography_role`, not by genre or font appearance. Stop a genre search after two query variants produce no new structural role. A visually useful candidate remains `visual-pass-private-trial-needed`; image-search popularity, music acclaim, or repeated appearance in listicles is not evidence of design quality.

## Contrastive record

Record one comparison at a time with `assets/learning-observation.yaml`:

- the exact decision being tested;
- winner and rejected candidate IDs without embedding images;
- the decisive observable differences;
- scorecard deltas;
- objective failures;
- the single changed variable for edit pairs;
- conditions where the proposed rule should and should not apply;
- privacy and rights confirmation.

Do not record lyrics, artist-information contents, reference images, prompts containing private details, or generated image files in a public learning record.

## Promotion gate

A proposed rule may enter a production reference only when all are true:

1. It improves at least two predefined evaluation criteria without regressing a non-negotiable gate.
2. The result repeats in at least three independent release trials.
3. Those trials span at least two materially different title, script, evidence, or sonic conditions.
4. It succeeds on one held-out brief that did not shape the rule.
5. The rule names its boundary and rejection condition.
6. The rule contains no private identity, copyrighted image, living-artist imitation, or style prescription.

If the held-out trial fails, retain the observation as a bounded failure note or discard it. Do not weaken the gate merely to promote the rule.

## Failure taxonomy

Use stable failure codes so repeated weaknesses become visible:

- `release-format-confusion`: reads as poster, ad, editorial, app tile, game splash, or generic concept art;
- `literal-title-illustration`: depicts the title without creating a release identity;
- `generic-genre-template`: interchangeable genre decoration;
- `musical-evidence-gap`: visual claim has no supplied evidence or labeled title hypothesis;
- `title-integrity`: spelling, spacing, script, or reading-route failure;
- `detached-title`: title behaves as header, footer, caption, or overlay;
- `material-anatomy-gap`: material does not determine letter anatomy;
- `character-title-separation`: figure and title remain two independent designs;
- `thumbnail-collapse`: dominant identity or title fails at small size;
- `palette-default`: unmotivated recurring palette or warm cast;
- `series-repetition`: recent covers repeat four or more structural axes;
- `unapproved-text`: readable text beyond the approved title;
- `rights-or-provenance`: reference or identity use cannot be cleared.
- `title-complexity-mismatch`: the chosen title behavior or transformation made an exact long, mixed-script, or fragile title less reliable.
- `local-preference-overreach`: a one-release or artist-specific preference was treated as a public rule.

## Learning boundaries

- Do not automatically upload observations or use user work for public research.
- Do not move artist-local feedback, image history, artist systems, or internal evaluation outputs into this repository. Public observations must be abstracted and privacy-safe.
- Do not create global cross-run runtime memory from trial records or artist settings. Reusable learning stays inside the relevant artist's `.album-cover-director/` directory.
- Do not keep adding precedent examples when the failure is execution quality rather than a missing construction principle.
- Do not promote a rule based only on aggregate score; a gate failure always wins.
