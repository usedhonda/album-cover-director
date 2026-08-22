# Album Cover Director

$album-cover-director is a Codex skill and plugin bundle for distinctive, release-ready album, EP, and single covers. Its specialty is image-native title design: the exact title can become a physical world, take over a whole space through light/reflection/atmosphere, or share one visual hierarchy with a central figure. It turns musical evidence into three structurally different directions, generates and compares candidates with GPT Image 2, and prepares 3000 px delivery assets.

The project is for musicians, track makers, producers, independent labels, and designers. It has no artist-specific identity, no required MCP server, and no required API key.

## See what it makes

### Titles as physical worlds

|  |  |
| --- | --- |
| ![ALBUM COVER DIRECTOR becomes a dense oceanographic line system.](docs/examples/oceanographic-title-system.png) | ![ALBUM COVER DIRECTOR becomes a pirate captain's treasure chart.](docs/examples/treasure-chart-title-system.png) |
| **Oceanographic system** — contour lines, routes, and soundings determine the title's anatomy. | **Treasure chart** — folds, compass wells, rope, and red routes make a navigable title artifact. |
| ![ALBUM COVER DIRECTOR becomes a playable board-game machine.](docs/examples/board-game-title-system.png) | ![ALBUM COVER DIRECTOR becomes a pinned botanical specimen.](docs/examples/botanical-specimen-title-system.png) |
| **Board game** — tiles, tracks, bridges, and game pieces turn title letters into a playable system. | **Botanical specimen** — roots, pressed leaves, petals, pins, and thread grow the letters. |
![ALBUM COVER DIRECTOR becomes a mechanized acoustic system.](docs/examples/mechanized-title-system.png)

**Mechanized system** — tubes, springs, resonators, and wiring construct a dense acoustic title artifact.

### Titles as spatial events

![Two equal-sized spatial title systems: a rotating club-light field and an ink landscape field.](docs/examples/spatial-field-pair.png)

**Rotating light field** — a small mirror ball, projected letters, smoke, and dancers turn the entire club into one title environment. The letter skeleton stays readable while light, air, and movement distribute it through the image.

**Ink landscape field** — the exact title's brush-letter skeleton spreads through mountains, roofs, bridge rails, riverbanks, mist, and water.

### Character-led title systems

|  |  |
| --- | --- |
| ![A giant SECRETARY CHI title becomes a navigable office world.](docs/examples/title-map-secretary-chi.png) | ![A tsundere Secretary Chi points a red pen through a high-energy Japanese title field.](docs/examples/tsundere-secretary-chi.png) |
| **Title map** — the word is the world. | **Kinetic wordmark** — gesture and title are one action. |
| ![Secretary Chi framed by a giant integrated SECRETARY CHI wordmark.](docs/examples/hero-wordmark-secretary-chi.png) | ![Secretary Chi serving coffee with 社長室の across the top and a giant 朝 at lower left.](docs/examples/japanese-title-shachoshitsu-no-asa.png) |
| **Hero wordmark** — person and title share one hierarchy. | **Japanese hierarchy** — a lead-in yields to one giant character. |

Every title above is generated within the image itself. It is never repaired with a font overlay, redraw, or post-typesetting: its material, structure, and image are one design decision.

The gallery demonstrates three equal title-system families. Choose **material-world** when routes, artifacts, games, specimens, or another physical system should form the title's anatomy. Choose **spatial-field** when light, reflection, smoke, motion, weather, or architecture should distribute and transform the title across the full square. Choose **character-led** when a supplied artist system or brief calls for a figure whose pose, action, setting, and title must work as one structure. A spatial field may use a familiar-looking letter skeleton to establish reading, but it must be generated inside the image and physically altered by the scene; it is never a flat overlay.

## What makes it different

- A work-specific research pipeline for covers acclaimed for visual design, with typography-dominant examples screened independently from music reputation.
- Three image-native title-system families: material-world, spatial-field, and character-led; each has specific construction cards and rejection tests.
- Twelve supporting organizing patterns that describe what controls the square, rather than a menu of visual styles.
- Three-direction divergence: every run must change image structure, not just color or rendering.
- A title-integrated typography gate: every evaluated candidate is a complete jacket; title lettering must be generated as part of the image, never added afterward.
- Material title-world cards for route fields, constructed artifacts, playable rule systems, and living specimens; a spatial light-and-atmosphere field; plus character-led hero, gesture, and script-hierarchy systems.
- Hierarchy locks for live or spatial images: title area, silhouette, reading route, and value priority are fixed before controlled irregularity is applied to surrounding light, smoke, motion, reflection, or crop.
- Comparative checks at 56 px, 128 px, 256 px, full size, grayscale, and blur.
- One-variable edits, at most two cycles, always returning to the selected original after regression.
- Reproducible 3000 x 3000 PNG/JPG and 256 px thumbnail export.
- Project-local artist systems, feedback, learning images, and benchmarks that improve future covers without publishing user work.

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
Mode: standard
Lyrics: ...
Artist information: /path/to/artist-information.md
Reference image: /path/to/character.png
Image use: keep the character identity, but redesign the scene and composition
~~~

Natural language:

~~~text
Direct six structurally different cover candidates for my new single.
Use the attached audio, make the title exact, and deliver a 3000px square.
~~~

The only required input is:

- an exact song, album, or release title.

Lyrics and artist information are optional. Lyrics may be pasted inline or supplied as a readable file path. Artist information may include the artist name, genre, sonic character, points to emphasize, recurring character or identity rules, visual language, palette, typography, avoid list, and references. With no optional input, the skill proceeds from the title alone.

Reference images are optional. Attach an image or supply a readable file path, then use it as a recurring person or character identity, as an actual image to edit or incorporate, or only as visual direction. When the request is clear, the skill infers the use mode. A recurring character does not freeze the whole cover: pose, action, setting, composition, light, palette, and title architecture remain release-specific. Direct use of the actual image requires the necessary rights.

For a continuing artist project, initialize `.album-cover-director/` at that project's root. Its `artist-system.md` is used only by that project; an explicit artist-information path is used only for the current run. The skill never remembers an artist system globally or carries it into another project.

Run volumes:

- quick: 3 candidates;
- standard: 6 candidates, default;
- deep: 12 candidates.

Run intents:

- explore: directions and candidates for an early choice;
- production: comparison, refinement, and delivery, the default;
- improve-skill: a controlled project-local learning trial.

Typography modes:

- auto;
- image-native;
- custom-wordmark.

Title-system families:

- auto: chooses from the brief;
- material-world: title anatomy is made by a physical system;
- spatial-field: a protected title skeleton is distributed and transformed by light, reflection, atmosphere, motion, or architecture;
- character-led: central figure and title share a single hierarchy.

## Project-local learning

Initialize once from the artist or release project's root:

~~~bash
python scripts/project-workspace.py init --project-root .
~~~

This creates an ignored `.album-cover-director/` directory containing the
artist system, feedback records, an inbox for user-supplied learning images,
generated learning images, observations, and a small title-integrity benchmark.
Nothing in that folder is committed or uploaded by this skill.

After a user chooses or rejects candidates, record the selection and the reason
in `feedback/<release-slug>.yaml`. A repeated, bounded observation can become
that project's `learned-preferences.md`; one-off taste never becomes a global
rule. A rule can enter the public skill only after independent, varied trials
and a held-out brief pass. See [project-local-learning.md](skills/album-cover-director/references/project-local-learning.md).

For complex Japanese, mixed-script, long, or punctuation-heavy titles, the
skill classifies the title before generation and changes its native hierarchy,
line break, or protected glyph treatment if it fails. It never repairs text
with later typesetting. See [title-complexity.md](skills/album-cover-director/references/title-complexity.md).

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

[typography-led-genre-intake.yaml](research/typography-led-genre-intake.yaml) is a cross-genre visual intake selected through image search and direct screening. It stores no third-party images: only release metadata, source pages, observations about how type organizes the square, and transfer questions. Candidates remain discovery-only until production comparisons and held-out briefs reproduce the result.

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
