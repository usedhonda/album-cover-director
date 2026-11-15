# GPT Image 2.5 migration note

This note records bounded research for the album-cover-director prompt and
runtime contract. It is not a model selector, benchmark, or production claim.
No third-party images or private user data are stored here.

## Official facts

OpenAI's [image prompting guide](https://developers.openai.com/api/docs/guides/image-prompting)
describes two GPT Image 2.5 variants: **Flare** is faster with quality
comparable to GPT Image 2, while **Sunburst** is higher quality. The same guide
describes improved precise editing and subject preservation for both. The
documented `xhigh`/`max` quality controls and API dimension rules belong to the
API surface; they are not assumed for a built-in host tool. These statements do
not identify the hidden runtime behind any host.

## Investigator report (not a general guarantee)

[Framesail's comparison](https://framesail.com/blog/gpt-image-2-5-vs-gpt-image-2)
reports 123 matched 2048x1152 low-quality pairs. It observed text overriding
conflicting references, while close-up labels were weaker than explicit frame
occupancy and extra props could enter the scene. This is vendor-reported
investigation evidence, not a controlled guarantee for this skill's square
covers or host surface.

[PromptFrenzy's benchmark](https://www.promptfrenzy.com/benchmark/gpt-image-2-5-vs-gpt-image-2)
reports mixed outcomes with differing settings and baselines. It should not be
used to claim a universal gain.

## Anecdotes and disputed claims

Reddit reports include good complex edits alongside progressive crop/softening
and an unknown variant:
[complex-edit discussion](https://www.reddit.com/r/ChatGPT/comments/1wi6tca/how_do_you_find_gptimage25_so_far/).
Another thread's claim that text is categorically improved was disputed by
readers and tied to a promotional link, so it is not accepted as evidence:
[text comparison discussion](https://www.reddit.com/r/ChatGPT/comments/1wbno1l/gpt_image_2_vs_gpt_image_25/).

## Prompt and contract adaptations

- Use the host's exposed built-in image tool. Record an exact model only when
  exposed; otherwise `model_id: host-undisclosed` and `model_or_tool: image_gen`.
- Describe visible frame occupancy, contact points, depth order, and the action
  that causes lettering. Quote the exact title once, then specify reading order
  and line break.
- Give every reference a role (identity, pose, garment, composition, material,
  or palette). Remove stale text, contradictory reference instructions, and
  story or decorative props that do not support the chosen structure.
- For edits, list invariants and one scoped change; inspect crop/detail and
  thumbnail; keep the existing two-cycle limit and selected-original rollback.
- Preserve image-native title generation and the no-post-lettering rule. Keep
  adult-safety boundaries and the palette-temperature quality guard; the latter
  is not evidence of a universal GPT Image 2.5 temperature bias.

## Open uncertainties

The host may expose neither a variant name nor API quality controls. Outcomes
can vary with prompt, reference set, crop, dimensions, and tool routing. These
notes therefore guide prompt clarity and provenance only; they do not activate
a new adapter or change historical fixtures.
