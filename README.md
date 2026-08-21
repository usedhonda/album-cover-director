# Album Cover Director

$album-cover-director is a Codex skill and plugin bundle for directing distinctive, release-ready album, EP, and single covers. It turns musical evidence into three structurally different visual directions, generates and compares candidates with GPT Image 2, treats lettering as its own design system, and prepares 3000 px delivery assets.

The project is for musicians, track makers, producers, independent labels, and designers. It has no artist-specific identity, no required MCP server, and no required API key.

## What makes it different

- A 120-cover observation corpus spanning four eras, multiple regions, major and independent contexts, and 24+ Japan/East Asia releases.
- Twelve organizing patterns that describe what controls the square, rather than a menu of visual styles.
- Three-direction divergence: every run must change image structure, not just color or rendering.
- A typography gate with deterministic fallback to post-typesetting.
- Comparative checks at 56 px, 256 px, full size, grayscale, and blur.
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
- post-typeset;
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

The export command refuses non-square sources and records dimensions, scaling, byte size, and SHA-256.

## Research and copyright

[research/corpus.yaml](research/corpus.yaml) contains bibliographic information, source links, and original visual observations. It contains no third-party album-cover images. Color proportions are visual estimates, and unverified designer credits are explicitly marked as uncredited.

The research method begins with institutional and label-level context such as [Cooper Hewitt’s Art of Noise](https://www.cooperhewitt.org/exhibition/art-of-noise/) and [Blue Note Records’ visual archive](https://www.bluenote.com/blue-note-wall-art/), then examines individual releases.

Reference images supplied during use must be owned, licensed, public-domain, or used only as non-reproduced analytical input. Do not request direct imitation of a living artist.

## Validate

~~~bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
python /path/to/skill-creator/scripts/quick_validate.py skills/album-cover-director
python /path/to/plugin-creator/scripts/validate_plugin.py .
~~~

CI verifies the skill frontmatter, plugin manifest, corpus schema and distribution, URL syntax, absence of third-party raster images, and absence of secrets or local absolute paths.

## License

Code, instructions, schemas, and original observations are released under the [MIT License](LICENSE). Third-party album artwork is not included or relicensed.
