# Needs and artifacts

Open this guide when the task involves `needs:` limits or artifact downloads. The topic map routes to this file.

For current feature claims and release qualifications, use the [source map](../00-source-map.md) and [version notes](../feature-version-notes.md).

## `needs:` size and artifact fetching

`needs:` accepts a maximum number of jobs per job. It is a **plan limit**
(`ci_needs_size_limit`), not a constant of the YAML language: it differs between
GitLab.com plans and is adjustable on self-managed instances through the Plan
Limits API or the Rails console. Do not write a number into a design; state that
the limit exists, is instance-dependent, and must be checked against the target
instance if a job approaches a few dozen edges.

`needs:` also controls artifact download. Be explicit:

```yaml
deploy:
  needs:
    - job: build          # ordering and artifacts
      artifacts: true
    - job: security_scan  # ordering only
      artifacts: false
```

`dependencies:` controls artifact download and nothing else. If a job declares
`needs:`, express artifact fetching through `needs:artifacts:` and do not add a
second `dependencies:` list saying something different.
