# Album Cover Director

$album-cover-director is a Codex skill and plugin bundle for directing distinctive, release-ready album, EP, and single covers. It turns musical evidence into three structurally different visual directions, generates and compares candidates with GPT Image 2, treats lettering as its own design system, and prepares 3000 px delivery assets.

The project is for musicians, track makers, producers, independent labels, and designers. It has no artist-specific identity, no required MCP server, and no required API key.

## See what it makes

|  |  |
| --- | --- |
| ![A giant SECRETARY CHI title becomes a navigable office world.](docs/examples/title-map-secretary-chi.png) | ![A tsundere Secretary Chi points a red pen through a high-energy Japanese title field.](docs/examples/tsundere-secretary-chi.png) |
| **Title map** — the word is the world. | **Kinetic wordmark** — gesture and title are one action. |
| ![Secretary Chi framed by a giant integrated SECRETARY CHI wordmark.](docs/examples/hero-wordmark-secretary-chi.png) | ![Secretary Chi serving coffee with 社長室の across the top and a giant 朝 at lower left.](docs/examples/japanese-title-shachoshitsu-no-asa.png) |
| **Hero wordmark** — person and title share one hierarchy. | **Japanese hierarchy** — a lead-in yields to one giant character. |

Every title above is generated within the image itself. It is never repaired with a font overlay, redraw, or post-typesetting.

## What makes it different

- A work-specific research pipeline for covers acclaimed for visual design, with typography-dominant examples screened independently from music reputation.
- Twelve organizing patterns that describe what controls the square, rather than a menu of visual styles.
- Three-direction divergence: every run must change image structure, not just color or rendering.
- A title-integrated typography gate: every evaluated candidate is a complete jacket; title lettering must be generated as part of the image, never added afterward.
- Five reusable title-image architectures: map, enclosing contour, kinetic wordmark and evidence field, palimpsest intervention, and emblem orbit.
- Comparative checks at 56 px, 128 px, 256 px, full size, grayscale, and blur.
- One-variable edits, at most two cycles, always returning to the selected original after regression.
- Reproducible 3000 x 3000 PNG/JPG and 256 px thumbnail export.

## Install

### Ask Codex to install the skill

Give Codex this repository path:

~~~text
Install the album-cover-director skill from
https://github.com/usedhonda/album-cover-director/tree/main/skills/album-cover-director
~~~

### Manual skill install

~~~bash
git clone https://github.com/usedhonda/album-cover-director.git
mkdir -p ~/.agents/skills
ln -s "$PWD/album-cover-director/skills/album-cover-director" ~/.agents/skills/album-cover-director
~~~

Restart Codex after installation. The repository root is also a validation-ready Codex Plugin bundle through .codex-plugin/plugin.json; it can be listed by a Codex plugin marketplace without repackaging its skill.

## Use

Explicit:

~~~text
$album-cover-director
Title: Glass Weather
Artist: Example Artist
Mode: standard
Lyrics: ...
Avoid: neon city, centered face
~~~

Natural language:

~~~text
Direct six structurally different cover candidates for my new single.
Use the attached audio, make the title exact, and deliver a 3000px square.
~~~

Required input:

- exact release title;
- artist name;
- lyrics, a track description, or audio.

Optional input includes genre, sonic traits, rights-cleared reference images, an existing artist system, an avoid list, destination, run volume, and typography mode.

Run volumes:

- quick: 3 candidates;
- standard: 6 candidates, default;
- deep: 12 candidates.

Typography modes:

- auto;
- image-native;
- custom-wordmark.

## Output

~~~text
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
~~~

If image generation or Pillow is unavailable, the skill returns the finished brief, directions, prompts, and exact export specification, but does not claim that delivery is complete.

## Pattern system

The twelve primary patterns are:

1. Portrait / Identity
2. Documentary Moment
3. Narrative Tableau
4. Symbolic Object / Still Life
5. Typographic Hero / Wordmark
6. Minimal Geometry / Color Field
7. Abstract Material / Process
8. Archive / Collage / Found Material
9. Illustration / Character World
10. Landscape / Architecture / Absence
11. Diagram / Grid / Data / Repetition
12. Package Object / Intervention / Anti-cover

Genre, era, palette, material, and rendering method are separate axes. A direction keeps one genre anchor and betrays one expected code.

## Image utility

Pillow is the only optional runtime dependency:

~~~bash
python -m pip install Pillow
python scripts/cover-ops.py inspect selected-master.png
python scripts/cover-ops.py contact-sheet candidates/*.png --output comparison.png
python scripts/cover-ops.py export selected-master.png --out-dir delivery
~~~

The export command refuses non-square sources and records dimensions, scaling, byte size, and SHA-256. `cover-ops.py` intentionally does not add or typeset title text: title typography must be native to the generated cover image.

## Research and copyright

[research/corpus.yaml](research/corpus.yaml) is a superseded draft and is not a production reference. The current bounded teaching set is distilled in [verified-principles.md](skills/album-cover-director/references/verified-principles.md) from the evidence-complete entries in [typographic-candidates.yaml](research/typographic-candidates.yaml). It exists to improve cover decisions now; it is not a reason to keep collecting precedents during a cover run. The repository contains no third-party album-cover images.

The replacement method requires each admitted work to have cover-specific acclaim evidence, typography dominance at T4 or T5, a direct visual check, and a work-specific transferable principle. Every final record must also name its country, label, and at least two candidate-verified evidence-source IDs. Validation rejects a final corpus if one designer supplies more than three works, one label more than six, one country more than sixteen, one genre more than eighteen, or one source supports more than twelve works. Music rankings, sales, and album fame do not count as cover-design evidence. Future expansion is failure-driven: add research only when repeated real cover runs reveal a missing construction rule, not to enumerate music genres.

[genre-diverse-title-intake.md](research/genre-diverse-title-intake.md) is a separate, capped six-item discovery intake. Its links and observations are not production rules until a private cover trial proves a distinct title-image relationship.

Reference images supplied during use must be owned, licensed, public-domain, or used only as non-reproduced analytical input. Do not request direct imitation of a living artist.

## Validate

~~~bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
python /path/to/skill-creator/scripts/quick_validate.py skills/album-cover-director
python /path/to/plugin-creator/scripts/validate_plugin.py .
~~~

CI verifies the skill frontmatter, plugin manifest, explicit superseded/final corpus state, research checkpoint contract and distribution, URL syntax, absence of third-party raster images, and absence of secrets or local absolute paths.

## License

Code, instructions, schemas, and original observations are released under the [MIT License](LICENSE). Third-party album artwork is not included or relicensed.
