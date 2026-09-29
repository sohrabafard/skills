# Reuse and composition

Open this guide when composing hidden jobs, includes, components or child pipelines. For current feature claims, consult the [GitLab source map](../00-source-map.md) and [version notes](../feature-version-notes.md).

## Reuse: hidden jobs, `extends`, `!reference`, includes and components

Reuse when the same text appears in three or more jobs, or when two jobs must
change together and a reader would otherwise have to notice that by reading both.
Do not abstract a one-off job: a hidden template with one user costs a reader one
extra hop and buys nothing.

**Hidden jobs and `extends:`** for reuse inside one file:

```yaml
.default-test:
  stage: test
  interruptible: true
  timeout: 15 minutes
  retry:
    max: 1
    when:
      - runner_system_failure
      - stuck_or_timeout_failure

unit:
  extends: .default-test
  script: [php artisan test]
```

`extends:` merges maps and replaces arrays, and resolves up to eleven levels.
YAML anchors (`&name` / `<<: *name`) do the same job at the parser level and work
only within one file; `extends:` also works across `include:` boundaries, so
prefer it in any file that is included or that includes.

**`!reference [.job, key]`** splices one key out of another job, including across
includes, without inheriting the rest of it. Use it when a job needs one
`before_script` from a template and none of its other keys.

**Includes** split a pipeline across files when that improves ownership or reuse.
Splitting a file only to make it shorter moves the reading cost without removing
it. Good boundaries follow who changes the file: `ci/lint.yml`, `ci/test.yml`,
`ci/build.yml`, `ci/deploy.yml`. When an answer spans several files, show the
include graph.

**Components with `spec:inputs`** for reuse across projects. Components and the
CI/CD Catalog have been generally available since GitLab 17.0. Reference a
published component by commit SHA or by tag; a branch reference makes the
component's content change under the consumer. Use typed inputs when the value
should be validated before the pipeline is created, and variables when the value
is runtime-only, secret, or environment-scoped — the full boundary is in
`variables-and-inputs.md`.
