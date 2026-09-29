# Pipeline creation and path rules

Open this guide when the task involves pipeline creation rules and path filtering. The topic map routes to this file.

For current feature claims and release qualifications, use the [source map](../00-source-map.md) and [version notes](../feature-version-notes.md).

## `workflow:rules` and job `rules:`

`workflow:rules` decides whether a pipeline is created at all. Job `rules:`
decides which jobs are inside the pipeline that was created.

```yaml
workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_TAG
    - if: $CI_COMMIT_BRANCH && $CI_OPEN_MERGE_REQUESTS && $CI_PIPELINE_SOURCE == "push"
      when: never
    - if: $CI_COMMIT_BRANCH
    - when: never
```

Two properties to check on any `workflow:rules` block you write or review:

- **Its fallback is deliberate.** With `workflow:rules`, no matching rule means
  no pipeline. A final `when: never` makes that default explicit; `when: always`
  deliberately opens the remaining cases. Source: https://docs.gitlab.com/ci/yaml/workflow/.
- **It prevents duplicate pipelines.** Where jobs use merge-request-aware rules
  and no `workflow:` block exists, one push can create both a branch pipeline and
  a merge request pipeline that run the same jobs twice.
  `validate_gitlab_ci.py` reports `workflow-missing`.

Inside a job, `rules:` arms are evaluated in order and the first match wins. Give
a terminal arm only when it clarifies the intended fallback; no matching job rule
omits that job.

Write predicates as `$VAR`, not `${VAR}`; inside `rules:if`, the brace form is
not expanded. Quote literal strings: `$CI_COMMIT_BRANCH == "main"`.

Two predicates that are not the same thing, and are confused often enough to be
worth writing out:

- `$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH` — this commit is on the default
  branch.
- `$CI_COMMIT_REF_PROTECTED == "true"` — this ref is protected, which is what
  decides whether a protected variable or a protected runner is reachable.

A deploy job that needs a protected credential tests the second, and usually
both. `only`/`except` are deprecated for all of this; `only:refs` becomes
`rules:if` and `only:changes` becomes `rules:changes`.

## `rules:changes` and path filters

`rules:changes` selects jobs by which files a push touched. Its limits:

- Variables are supported. In `changes`, an undefined `$VAR` remains literal
  path text. The checker reports `rules-path-var` as a note because it cannot
  resolve instance variables or prove matching. Source: https://docs.gitlab.com/ci/yaml/#ruleschanges.
- On a new branch, and on some non-push pipeline sources, `changes` has no
  meaningful base to compare against and evaluates more broadly than expected.
  Pair it with `if:` so the broad case is still bounded.
- A trailing slash inside an interpolated path expands into a pattern that
  matches nothing.

Where path selection must be exact and auditable, write the literal paths.
