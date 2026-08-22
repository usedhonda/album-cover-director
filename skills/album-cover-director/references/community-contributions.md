# Sharing a local discovery

Use this route when a user says that a locally useful cover lesson should help
other Album Cover Director users. It turns a private result into a **draft**
for a public title behavior card. It lets musicians and producers contribute
without asking them to learn the repository internals.

## Boundary

The source may be artist-local feedback, but the output must be a new,
abstract rule. Never copy or expose the release title, artist system, lyrics,
prompt, local path, feedback wording, reference image, generated image, or
private trial ID. Do not infer consent to share merely because a cover was
liked: the user must explicitly ask to share the lesson.

Use a contribution for one reusable behavior only. Good candidates explain how
a title's anatomy, scene, or reading route should behave. They do not propose a
genre look, a personal palette preference, or a copy of a reference.

## Prepare a draft

1. Read local feedback only to identify the contrast between success and
   failure. Abstract that contrast into a behavior, boundary, construction
   logic, and rejection tests.
2. Read `production-learning.md`. When the public promotion gate is not met,
   make a draft marked as needing evidence; do not represent it as validated.
3. Run `scripts/contribution-draft.py prepare`. The result remains under the
   release's private feedback folder and contains only a public card and review
   note. The script does not read feedback contents into the package or upload
   anything.
4. Show the user the exact draft and its evidence status. Ask only before an
   external GitHub action.

```bash
python scripts/contribution-draft.py prepare \
  --artist-root . \
  --release-slug private-release \
  --card-id material-governs-skeleton \
  --title-behavior "Material governs title anatomy" \
  --title-system-family material-world \
  --world-engine "A physical process makes each join necessary." \
  --construction-logic "Map routes to the title skeleton and counters." \
  --use-when "The concept has a coherent physical process." \
  --do-not-use-when "The material is only decorative texture." \
  --occupied-area "Most of the square" \
  --silhouette "One continuous constructed word shape" \
  --reading-route "Left to right through the physical route" \
  --value-priority "Title remains the highest-contrast structure" \
  --prompt-requirement "Make material determine joins and counters." \
  --rejection-test "Remove material: letter anatomy must collapse." \
  --condition-category "short Latin title" \
  --condition-category "mixed-script title" \
  --private-trial-count 3 \
  --held-out-brief-passed \
  --rights-safe
```

The generated `title-behavior-card.yaml` uses JSON syntax, which is valid YAML.
It is intentionally small enough to attach to a GitHub issue or copy into a
pull request.

## Publish only after review

`prepare` has no network capability. A user may inspect or edit the draft;
only a subsequent explicit request authorizes creating an issue, branch, or
pull request. Before that external action, run:

```bash
python scripts/contribution-draft.py validate --draft-dir <draft-directory>
```

Copy only `title-behavior-card.yaml` and its review note into the contribution.
Never upload the surrounding local feedback folder.
