# Pipeline authoring

Which pipeline exists, which jobs are in it, and how the file is composed. Which
job runs when is `job-graph-and-scheduling.md`; cache and artifact expression is
`cache-artifacts-and-pinning.md`.

## Table of contents

- Authoring defaults
- `workflow:rules` and job `rules:`
- `rules:changes` and path filters
- Environments and rollback
- Reuse: hidden jobs, `extends`, `!reference`, includes and components
- Child pipelines and multi-file layouts
- Authoring checklist

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

## `workflow:rules` and job `rules:`

`workflow:rules` decides whether a pipeline is created at all. Job `rules:`
decides which jobs are inside the pipeline that was created.

```yaml
workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_TAG
    - if: $CI_COMMIT_BRANCH
    - when: never
```

Two properties to check on any `workflow:rules` block you write or review:

- **It ends with a terminal arm.** Without `- when: never` at the end, an event
  that matches nothing falls through to GitLab's default, which is to create the
  pipeline. State the closed set.
- **It prevents duplicate pipelines.** Where jobs use merge-request-aware rules
  and no `workflow:` block exists, one push can create both a branch pipeline and
  a merge request pipeline that run the same jobs twice.
  `validate_gitlab_ci.py` reports `workflow-missing`.

Inside a job, `rules:` arms are evaluated in order and the first match wins. Give
every `rules:` list a terminal arm for the same reason.

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

- **No variable expansion inside the path patterns.** A path built from a
  variable is matched literally, including the dollar sign.
  `validate_gitlab_ci.py` reports `rules-path-var`.
- On a new branch, and on some non-push pipeline sources, `changes` has no
  meaningful base to compare against and evaluates more broadly than expected.
  Pair it with `if:` so the broad case is still bounded.
- A trailing slash inside an interpolated path expands into a pattern that
  matches nothing.

Where path selection must be exact and auditable, write the literal paths.

## Environments and rollback

A deploy job that does not declare an `environment:` is invisible: GitLab has no
record of what is deployed where, the environment page is empty, and there is no
"re-deploy this earlier version" path.

```yaml
deploy_production:
  stage: deploy
  timeout: 20 minutes
  interruptible: false
  resource_group: production
  environment:
    name: production
    url: https://app.example.com
    on_stop: stop_production
    deployment_tier: production
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH && $CI_COMMIT_REF_PROTECTED == "true"
    - when: never
  script:
    - ./scripts/deploy.sh

stop_production:
  stage: deploy
  timeout: 10 minutes
  environment:
    name: production
    action: stop
  rules:
    - when: manual
  script:
    - ./scripts/teardown.sh
```

- **`name:`** identifies the target. A dynamic name (`review/$CI_COMMIT_REF_SLUG`)
  creates one environment per branch; pair it with `auto_stop_in:` so review
  environments do not accumulate.
- **`url:`** is what makes the environment page usable and is read by merge
  request widgets.
- **`action:`** takes `start` (default), `prepare`, `stop`, `verify` or `access`.
  `prepare` records the job against the environment without creating a
  deployment, which is the correct value for a job that only fetches
  environment-scoped variables.
- **`on_stop:`** names the job that tears the environment down. That job must
  declare the same `environment:name` with `action: stop`, and must be creatable
  in the same pipeline.
- **`deployment_tier:`** classifies the environment when the name does not make
  the tier obvious.

**Rollback** in GitLab is re-running the deployment job of an earlier successful
pipeline against the same environment. That only works if two things are true,
and both are this skill's half to express:

1. The deploy job is **idempotent for a given input version**: running it twice
   with the same version produces the same result. A job that derives its version
   from "whatever is newest" cannot be rolled back by re-running it.
2. The version the job deploys is **an explicit input**, not a value the job
   discovers. Pass it as a variable or read it from a `reports:dotenv` artifact of
   the pipeline being rolled back to.

Where a rollback also needs a data step — reversing a migration, restoring a
snapshot — that is not a re-run and must be a separate job with its own
`environment:action`. Whether a change is safely reversible at all belongs to
`/alaa-controlled-ops` (`$alaa-controlled-ops`), and migration reversibility for a
PHP or Laravel service belongs to `/alaa-cicd-laravel-postgres`
(`$alaa-cicd-laravel-postgres`).

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

## Child pipelines and multi-file layouts

Use a child pipeline when the subtree has materially different jobs, when the
configuration must be generated, or when the parent's job list would otherwise be
unreadable. Keep the parent responsible for orchestration and gating; keep each
child focused and named for its subtree; be explicit about which variables are
forwarded. Debug parent creation and child execution as two separate problems.

## Authoring checklist

Before finishing a pipeline design:

- Is pipeline creation controlled by `workflow:rules` with a terminal arm?
- Does every job that mutates a shared target set `interruptible: false` and a
  `resource_group` named after that target?
- Does every job set `timeout:`?
- Is `retry:` narrowed to infrastructure classes?
- Does every deploy job declare an `environment:` with a `url:`?
- Are images pinned in every place they appear, including runner-side?
- Are cache keys derived from what makes the cache stale, with an explicit
  `policy:`?
- Does every artifact set `expire_in`?
- Is every job's real precondition expressed as a `needs:` edge?
- Does the answer state which checks are gates and name the skill that decided
  that, rather than deciding it here?
