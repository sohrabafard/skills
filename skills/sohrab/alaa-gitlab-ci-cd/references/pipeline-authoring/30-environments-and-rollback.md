# Environments and rollback

Open this guide when the task involves deployment environments or re-running an earlier deployment. The topic map routes to this file.

For current feature claims and release qualifications, use the [source map](../00-source-map.md) and [version notes](../feature-version-notes.md).

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
`/alaa-controlled-ops`, and migration reversibility for a
PHP or Laravel service belongs to `/alaa-cicd-laravel-postgres`.
