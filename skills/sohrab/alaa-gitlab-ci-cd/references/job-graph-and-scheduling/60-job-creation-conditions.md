# Job creation conditions

Open this guide when deciding whether a job belongs in a pipeline at all. For current feature claims, consult the [GitLab source map](../00-source-map.md) and [version notes](../feature-version-notes.md).

## Skipping inside a script versus not creating the job

A job whose script begins "if this is not a release, `exit 0`" reports success and
did nothing. A reader sees twelve green jobs and cannot tell which of them ran.
The pipeline is green whether or not anything was verified.

Put the condition in `rules:` so the job is not created:

```yaml
deploy:
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH && $CI_COMMIT_REF_PROTECTED == "true"
    - when: never
```

Then a pipeline with no deploy job shows that no deploy was attempted, and a
pipeline with a green deploy job shows that one succeeded. Use a script-level
skip only where the condition is unknowable until the job runs — a value produced
by an earlier job through a dotenv report, for example — and say so in a comment
on the line. `validate_gitlab_ci.py` reports `script-skips-with-exit-0`.
