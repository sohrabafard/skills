# Pipeline authoring

## Table of contents

- Authoring defaults
- Rules and workflow patterns
- DAG and stage design
- Reuse with hidden jobs, includes, and components
- Child pipelines and multi-file layouts
- Authoring checklist

## Authoring defaults

Use these defaults unless the project context clearly points elsewhere:

- Start with `workflow:rules` so pipeline creation is explicit.
- Use `stages` for readability, then add `needs` only where it improves throughput.
- Put shared setup in `default:` or hidden jobs instead of repeating `before_script`, `cache`, or retry policy.
- Use `interruptible: true` on lint, test, and build jobs that are safe to cancel.
- Use pinned images, explicit caches, and `artifacts:expire_in`.
- Prefer small jobs with clear responsibilities over giant all-in-one scripts.

## Rules and workflow patterns

### Branch, merge request, and tag pipelines

Use `workflow:rules` to decide whether a pipeline should exist at all. Then use job `rules` to place jobs inside that pipeline.

Safe baseline:

```yaml
workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_TAG
    - if: $CI_COMMIT_BRANCH
```

This avoids accidental "no pipeline created" outcomes and makes it easier to prevent duplicate pipelines.

### Prevent duplicate pipelines

When jobs use `rules`, add a top-level `workflow:rules` block. Without it, the same push can sometimes create both branch and merge request pipelines.

### Scheduled and manual jobs

- Keep schedule-specific jobs behind `if: $CI_PIPELINE_SOURCE == "schedule"`.
- Use `when: manual` for human approval points.
- Use `manual_confirmation` when you want a clearer prompt in the UI.
- Do not make a manual job the only path to create a pipeline unless that is intentional.

### `rules:changes`

Use `rules:changes` for path-based job selection, but remember:

- It does not behave like a generic variable-aware path matcher.
- New branches and some non-push pipeline sources can make it evaluate more broadly than expected.
- Trailing slashes inside path variables can expand into bad path patterns.

If path selection must be exact and auditable, show the literal paths in the final YAML instead of building them dynamically.

## DAG and stage design

### When to use `needs`

Use `needs` when a downstream job can start as soon as a specific upstream job is done.

Good use cases:

- Fast feedback from lint or unit-test jobs.
- Independent build targets.
- Deploy jobs that only require a single artifact producer.

Avoid adding `needs` everywhere. Over-specified DAGs are harder to maintain and easier to break during refactors.

### `dependencies` vs `needs`

- `needs` controls execution order and can also fetch artifacts.
- `dependencies` only controls artifact download behavior.

If a job uses `needs`, decide whether artifact download should follow the default or be restricted explicitly.

### Resource serialization

Use `resource_group` for any job that mutates a shared target:

- Production deploys.
- Release publishing.
- Database schema changes.
- Shared test environments.

## Reuse with hidden jobs, includes, and components

### Hidden jobs

Use hidden jobs for local reuse inside one file:

```yaml
.default-test:
  stage: test
  interruptible: true
  retry:
    max: 1
    when:
      - runner_system_failure
      - stuck_or_timeout_failure
```

Then extend it only where the shared behavior is real.

### Includes

Split files when it improves ownership or reuse, not just to make the main YAML shorter.

Good boundaries:

- `ci/lint.yml`
- `ci/test.yml`
- `ci/build.yml`
- `ci/deploy.yml`
- `ci/components/*.yml`

When a task spans multiple files, show the include graph in the response.

### CI components and `spec:inputs`

Use components plus typed inputs when you need reusable, parameterized CI logic across projects or repos.

Prefer inputs when you want:

- Compile-time validation.
- Better defaults and documentation.
- Less runtime ambiguity than free-form variables.

Prefer variables when the value is runtime-only, secret, or naturally environment-scoped.

## Child pipelines and multi-file layouts

Use child pipelines when:

- The pipeline is large enough to benefit from isolated concerns.
- Different subtrees or products have materially different jobs.
- You need generated CI configuration.

Keep these rules:

- Make the parent responsible for orchestration and gating.
- Keep child pipelines focused and named clearly.
- Be explicit about variable forwarding.
- Debug parent creation and child execution separately.

## Authoring checklist

Before you finish a pipeline design, check:

- Is pipeline creation controlled by `workflow:rules`?
- Are jobs pinned to the right runner tags?
- Are images pinned?
- Are secrets externalized?
- Are `artifacts` and `cache` scoped deliberately?
- Is `needs` helping throughput rather than adding confusion?
- Is the pipeline easy to explain to another engineer in a few lines?
