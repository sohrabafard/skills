# Authoring defaults

Open this guide when setting the pipeline authoring defaults. For current feature claims, consult the [GitLab source map](../00-source-map.md) and [version notes](../feature-version-notes.md).

## Authoring defaults

- Start with `workflow:rules` so pipeline creation is explicit rather than
  incidental.
- Use `stages` as the readable spine and `needs:` where a job's real precondition
  is narrower than a whole stage.
- Put shared setup in `default:` or a hidden job instead of repeating
  `before_script`, `cache` or `retry` in every job. A top-level `image:`,
  `services:`, `cache:`, `before_script:` or `after_script:` does the same thing
  and is deprecated; write `default:`.
- Keep job scripts deterministic and non-interactive: no prompt, no reliance on a
  TTY, no dependency on a file the previous job happened to leave behind.
- Split one job into two when the two halves fail for different reasons and a
  reader would triage them differently. Keep them as one when the split only adds
  a stage boundary.
