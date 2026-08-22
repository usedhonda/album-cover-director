# Project-local learning

Album Cover Director learns a user's recurring taste and artist continuity
inside that user's project, never inside the installed skill or public
repository. Initialize the workspace at the project root:

```bash
python scripts/project-workspace.py init --project-root .
```

It creates this ignored local surface:

```text
.album-cover-director/
├── artist-system.md
├── learned-preferences.md
├── feedback/
├── learning-images/
├── reference-inbox/
├── observations/
└── benchmarks/title-integrity-v1.yaml
```

All files under this directory are project-local. Do not commit, upload, or
copy them into a public skill, corpus, issue, or pull request.

## Inputs and separation

- `artist-system.md` contains stable identity and continuity constraints. It is
  read for this project only. An explicitly supplied artist-system path wins
  for one run but is never remembered globally.
- `reference-inbox/` is for user-supplied images to inspect locally. Classify
  each image as `identity-reference`, `source-asset`, or `visual-direction`
  and record its rights basis in the release brief.
- `learning-images/<release-slug>/` stores generated candidates, comparisons,
  and user-approved learning images. They may guide future local analysis but
  are not public training data.
- `feedback/<release-slug>.yaml` records the user's selection and correction
  using `assets/project-feedback.yaml`.
- `learned-preferences.md` is a compact local summary. Promote an observation
  into it only after repeated feedback under different release conditions.

## Every reviewed run

When a user selects, rejects, or corrects candidates:

1. Copy or retain the relevant generated candidates in the release's
   `learning-images/` folder if the user wants them available for future local
   learning.
2. Write one feedback record. Preserve the user wording in
   `user_observations`; add stable failure codes only where they fit.
3. Treat the feedback as `one-release` by default. Do not change the artist
   system or public skill solely because one image won.
4. When an observation repeats across at least three releases with materially
   different titles, structures, or music evidence, summarize it in
   `learned-preferences.md` with an `applies_when` and `reject_when` boundary.
5. Use `learned-preferences.md` as evidence in future directions, but allow the
   current release brief to override it explicitly.

## Local evaluation and public promotion

Run the project-local benchmark before a consequential skill update, not on
every cover run. It is a small, owned-input matrix for title integrity across
scripts and title complexity. Store generated outputs and comparisons only in
the local workspace.

Public promotion remains stricter than local learning. Use
`production-learning.md`: a public rule needs three independent trials,
materially different conditions, a held-out brief, and no private images,
lyrics, artist information, or artist-specific preference. A local preference
is useful even when it can never become a public rule.
