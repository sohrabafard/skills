# Retry failure classes

Open this guide when choosing retries for a job. For current feature claims, consult the [GitLab source map](../00-source-map.md) and [version notes](../feature-version-notes.md).

## `retry:` and its failure classes

A bare integer retries **every** failure class, including an assertion failure.
That converts a real defect into an intermittent one, and the second run's green
result hides the first run's red one.

```yaml
default:
  retry:
    max: 1
    when:
      - runner_system_failure
      - stuck_or_timeout_failure
```

This retries infrastructure and not logic. Add `api_failure` or
`scheduler_failure` where the instance genuinely produces them; do not add
`script_failure`, which is the class that means "the code is wrong".

Opt a mutating job out of retries entirely unless the operation is idempotent.
Retrying a `semantic-release` that already pushed a tag, or a migration whose
Kubernetes Job deliberately sets `backoffLimit: 0`, does damage that the first
failure did not. `validate_gitlab_ci.py` reports `retry-bare-count`.
