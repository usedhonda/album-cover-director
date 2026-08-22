# Artist-local learning

Album Cover Director learns a user's recurring taste and artist continuity
inside that artist's root, never inside the installed skill or public
repository. Initialize the workspace at the artist root:

```bash
python scripts/project-workspace.py init --artist-root .
```

It creates this ignored local surface:

```text
.album-cover-director/
├── artist-system.md
├── feedback/
│   ├── learned-preferences.md
│   └── <release-slug>/
│       ├── feedback.json
│       └── images/
```

All files under this directory are artist-local. Do not commit, upload, or
copy them into a public skill, corpus, issue, or pull request.

## Inputs and separation

- `artist-system.md` contains stable identity and continuity constraints. It is
  read for this artist only. An explicitly supplied artist-system path wins
  for one run but is never remembered globally.
- `feedback/<release-slug>/feedback.json` records the user's selection and
  correction using `assets/project-feedback.yaml`.
- `feedback/<release-slug>/images/` automatically stores the reviewed
  candidates and supplied reference images for that release. Users do not sort
  images into separate input and trial folders.
- `feedback/learned-preferences.md` is an automatic compact summary. A
  normalized preference is promoted only after it repeats across three release
  folders under different conditions.

Read `artist-system-onboarding.md` when the artist system is absent or needs a
safe update. Users may start with a title, song, or reference image; they do
not need to write the system themselves.

## Every reviewed run

When a user selects, rejects, or corrects candidates:

1. Call `scripts/feedback-store.py record` with every reviewed candidate and
   supplied reference image as `--image`. It copies them into the release's
   feedback folder automatically.
2. Preserve the user wording in `user_observations`; add stable failure codes
   only where they fit.
3. Treat the feedback as `one-release` by default. Do not change the artist
   system or public skill solely because one image won.
4. When the same normalized preference repeats across at least three releases,
   the store refreshes `feedback/learned-preferences.md` with an
   `applies_when` and `reject_when` boundary.
5. Use that summary as evidence in future directions, but allow the
   current release brief to override it explicitly.

## Local evaluation and public promotion

Run the artist-local benchmark before a consequential skill update, not on
every cover run. It is a small, owned-input matrix for title integrity across
scripts and title complexity. Store generated outputs and comparisons only in
the local workspace.

Public promotion remains stricter than local learning. Use
`production-learning.md`: a public rule needs three independent trials,
materially different conditions, a held-out brief, and no private images,
lyrics, artist information, or artist-specific preference. A local preference
is useful even when it can never become a public rule.
