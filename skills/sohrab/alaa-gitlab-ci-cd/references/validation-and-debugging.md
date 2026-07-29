# Validation and debugging

## Table of contents

- Validation ladder
- The bundled checkers: what they assert and what they cannot see
- Gate-eligible versus advisory, and who chooses
- Live GitLab validation
- The five failure classes
- Symptom map
- Debugging across multiple files

## Validation ladder

Use the cheapest check that can still answer the question.

1. Static local validation with the bundled checkers.
2. CI Lint or `glab ci lint` in project context, which resolves `include:`.
3. Runner and executor inspection.
4. Job log and artifact inspection.

## The bundled checkers: what they assert and what they cannot see

```bash
python3 scripts/validate_gitlab_ci.py .gitlab-ci.yml ci/*.yml
python3 scripts/validate_runner_config.py config.toml values.yaml
python3 scripts/validate_gitlab_ci.py --self-test
python3 scripts/validate_runner_config.py --self-test
```

Both take `--help`, `--json`, `--fail-on-warnings` and `--self-test`, and both
use the same exit codes: **0 clean, 1 findings, 2 could not run.** Exit 2 means
the checker could not produce a verdict — a missing dependency, a missing file,
an unparsable input, or the wrong kind of file — and is never a clean result.
When an agent is unsure whether the working directory is the skill root, invoke
the scripts by an absolute path.

### `validate_gitlab_ci.py`

Asserts, per file: stage list shape and uniqueness; job names that do not collide
with reserved keywords; a concrete job having an action; `only`/`except`;
undefined stage; invalid `when`; unresolved `extends`, `needs` and
`dependencies`; `${VAR}` inside `rules:if`; variable syntax inside path filters;
image and service pinning including the registry-with-a-port form and any tag
with no version component; cache key presence, `key:files` over its two-path
limit, `fallback_keys` over five, a key not derived from a lockfile, and a
missing `policy:`; artifacts without `expire_in`; a bare `retry:`; inherited
`interruptible: true` on a mutating job; one `resource_group` saturating a
`needs:` graph; a job nothing needs that a later job can outrun; a missing job
`timeout:` where a resource group or an environment is present; deprecated
top-level keywords; `allow_failure: true` and script suffixes that swallow a
failure; a script that skips itself with `exit 0`; a credential written into a
URL or a Git remote; `CI_DEBUG_TRACE`; `set -x`; `docker login` without
`--password-stdin`; a hardcoded-looking secret; GitLab-unsupported
`${VAR:-default}` syntax in a `variables:` value; and the absence of any
recognised test, lint, static-analysis or dependency-audit command.

It **cannot see**:

- anything behind `include:`. When `include:` is present, every cross-file name
  check is downgraded to a note and one `unresolved-include` note is emitted, so
  the fleet's standard thin wrapper produces notes rather than errors. Use
  `glab ci lint --dry-run` for a merged verdict.
- the body of a script the pipeline invokes by path. `bash ci/scripts/deploy.sh`
  is one opaque line to it; everything inside that file is out of scope.
- anything the runner supplies. A pipeline with no `image:` key gets a
  `runner-supplied-image` note pointing at the runner config, which is where that
  pin lives.
- whether a value is correct. It reports that `retry:` is bare, not what the
  count should be.

### `validate_runner_config.py`

Asserts: `concurrent` unset or non-positive; every `[[runners]]` having an
executor; shell executor isolation and explicit `builds_dir`/`cache_dir`; for the
Kubernetes executor — privileged mode and node isolation, `allowed_images` and
`allowed_services` presence and breadth, `allowed_pull_policies`, a `pull_policy`
that contradicts the allowlist, `image_pull_secrets`, an unpinned or unset
`image` and `helper_image`, `namespace_per_job`, `pod_spec`, and a missing
`[runners.cache]` `Type`; and, for Helm values — `gitlabUrl`, legacy
registration tokens, a missing runner token, `rbac.create: false` with no named
service account, privileged job pods, and a `runners.config` block that is
present and valid TOML.

It routes on **content**, not on file extension. Handed a `.gitlab-ci.yml`, it
exits 2 and names `validate_gitlab_ci.py` rather than inventing findings about a
file it does not understand.

## Gate-eligible versus advisory, and who chooses

`--fail-on-warnings` turns this skill's checker into something that can fail a
pipeline. This skill does not decide that it should.

- **Error severity** marks a finding that is wrong under every configuration:
  invalid `when`, a stage that does not exist, `cache:key:files` over its limit,
  a `${VAR:-default}` GitLab cannot expand, a `pull_policy` outside its own
  allowlist. These are gate-eligible on any project.
- **Warning severity** marks a finding whose correct handling depends on the
  project: an unpinned image, a bare `retry:`, an interruptible mutating job, a
  saturated resource group, an advisory check, an absent code gate. Whether each
  of these blocks is the calling skill's decision — `/alaa-frontend-devops`
  (`$alaa-frontend-devops`) for a frontend repository,
  `/alaa-cicd-laravel-postgres` (`$alaa-cicd-laravel-postgres`) for a PHP or
  Laravel service.
- **Note severity** is never a gate. It marks something a reader should know.

When an answer proposes running either checker in a pipeline, state which
severity blocks and name the skill that decided it. A checker that can fail a
pipeline while nobody has written down what it is asserting is the same illusion
as an advisory job named like a gate.

## Live GitLab validation

```bash
glab ci lint
glab ci lint .gitlab-ci.yml --dry-run --include-jobs
glab ci lint path/to/pipeline.yml --dry-run --include-jobs --ref main
```

Use the CI Lint API when you need merged-configuration inspection from a script,
or pipeline simulation when includes, local project files or project context
matter. This is the only local-ish check that resolves `include:`.

## The five failure classes

Classify before editing anything. Editing a script when the pipeline was never
created wastes a full cycle.

### 1. YAML or schema failure

*Symptoms:* parse error; "config should be an array of hashes"; an unknown
keyword; a referenced job or stage that does not exist.

*Diagnose:* run `validate_gitlab_ci.py` on the file; then CI Lint for the merged
result. A `!reference` tag is valid GitLab syntax — a tool reporting it as a
syntax error is the tool's defect, not the file's.

*Smallest retry:* fix the file and push; configuration changes take effect on a
new pipeline, not on a re-run of an existing job.

*Escalate when:* the merged configuration is valid and the file alone is not —
the problem is in an included file, which is class 2.

### 2. Pipeline creation or rule evaluation failure

*Symptoms:* no pipeline created; jobs unexpectedly missing; a parent pipeline
exists and the child does not; two pipelines for one push.

*Diagnose:* read `workflow:rules` top to bottom for the actual event, then the
job's own `rules:`. Check whether `include:` resolved and whether the component
or input defaults are what you think. Check the pipeline source: the value in
`$CI_PIPELINE_SOURCE` for this run is often not the one the rule assumed.

*Smallest retry:* trigger the same event again — a push, or a merge request
update — rather than re-running an existing pipeline.

*Escalate when:* the rules are provably correct for the event and the pipeline
still does not appear; that is an instance or permission problem.

### 3. Runner matching failure

*Symptoms:* job stuck in pending with no runner; "This job is stuck because you
don't have any active runners".

*Diagnose:* compare job `tags:` against every runner's tag set; check whether the
runner is paused, offline, or out of `concurrent` slots; check protected-ref
against protected-runner; check the project or group scope the runner is
assigned to.

*Smallest retry:* nothing to retry — the job has not started. Fix placement.

*Escalate when:* a runner matches on paper and still does not pick the job up;
that is a runner-registration or instance problem.

### 4. Executor startup failure

*Symptoms:* pod never becomes ready; "timed out waiting for pod to start"; image
pull errors with no job log; a shell runner that starts with the wrong
environment; a DinD service that never responds.

*Diagnose, Kubernetes:* `poll_timeout`; cluster capacity for the runner's
namespace; API-server latency; admission webhooks; image pull time and registry
reachability from the cluster; `image_pull_secrets` on **all** the pod's
containers, not only the build container; RBAC on the service account;
`namespace_per_job` rights; whether the cluster's restricted security context
needs `logs_base_dir` and `scripts_base_dir`.

*Diagnose, DinD:* privileged mode on the runner; the service alias and port
matching `DOCKER_HOST`; TLS variables consistent with `DOCKER_TLS_CERTDIR`; the
shared certificate volume present in the runner config.

*Diagnose, shell:* the runner user's environment, the `builds_dir` contents left
by a previous job, and host tooling versions.

*Smallest retry:* re-run the single job once the runner configuration changed;
runner configuration is read per job, unlike pipeline configuration.

*Escalate when:* pods are created and killed by something outside the runner — a
quota, a PodSecurity policy, an admission webhook. That is a cluster question,
and for a managed platform it belongs to that platform's skill.

### 5. Runtime failure

*Symptoms:* the script runs and the toolchain fails; registry authentication
fails; a secret is empty; the filesystem is read-only; a variable is empty only
in a merge request pipeline.

*Diagnose:* image contents and entrypoint; variable scope, masking and protection;
file-variable paths; writable directories; network policy and DNS from the pod.
For an empty variable, walk the six-question order in `variables-and-inputs.md`
before changing anything.

*Smallest retry:* re-run the one job. If it passes on the second run with no
change, that is a flake and the bare-`retry:` rule in
`job-graph-and-scheduling.md` explains why it must not be hidden by a retry.

*Escalate when:* the same script passes locally and fails on the runner with
identical inputs — the difference is in the image or the runner, not the script.

## Symptom map

| Literal message | Class | First thing to check |
|---|---|---|
| `job is pending, no runners` | 3 | job `tags:` against runner tags |
| `no stages / stage does not exist` | 1 | `stages` list and the job's `stage` |
| `config should be an array of hashes` | 1 | a mapping written where a list belongs |
| `timed out waiting for pod to start` | 4 | cluster capacity, webhooks, `poll_timeout` |
| `Cannot connect to the Docker daemon` | 4 | DinD alias, port, privileged mode, TLS variables |
| `unauthorized: authentication required` | 4 or 5 | registry credentials, job-token scope, `image_pull_secrets` |
| `ErrImagePull` / `ImagePullBackOff`, no job log | 4 | `image_pull_secrets` on every container in the job pod |
| variable empty only in a merge request pipeline | 5 | protected variable against `$CI_COMMIT_REF_PROTECTED`, or fork pipeline |
| a green job that did nothing | 2 | a script-level `exit 0` where a `rules:` condition belonged |

## Debugging across multiple files

- Validate each file statically, then validate the merged result in project
  context; only the merged result knows what `include:` produced.
- Show the include graph in the answer.
- Debug parent and child pipelines as separate problems.
- Re-running a job uses the configuration that created its pipeline. To test a
  configuration change, start a new pipeline.
