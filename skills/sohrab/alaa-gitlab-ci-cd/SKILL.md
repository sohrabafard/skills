---
name: alaa-gitlab-ci-cd
description: GitLab CI/CD pipeline generation, validation, review, and debugging for reusable CI components, runner configs, and container-build workflows for GitLab Runner shell, Docker, and Kubernetes executors. Use when the task involves one or more `.gitlab-ci.yml` files, included CI files, CI components, GitLab Runner `config.toml`, Helm `values.yaml`, GitLab Docker or Kubernetes executor behavior, Docker or daemonless image builds, cache keys, artifact retention, variables or inputs, job routing via tags, pipeline security, or CI failure triage. Prefer it for both authoring and debugging. Do not use it for unrelated Kubernetes manifests, unrelated Dockerfiles, or non-GitLab CI systems, and do not use it to decide whether a check should block a pipeline; that belongs to the skill that owns the stack.
---

Act like a production GitLab CI/CD specialist, not a generic YAML writer.

## What this skill owns, and when not to use it

`alaa-gitlab-ci-cd` owns **how a gate is expressed on a runner** — the job graph,
`rules:` and `needs:`, every expression of a cache key, artifact retention and
`expire_in`, and the runner image reference — and **decides no gate**. Which
checks must exist, what each asserts, and whether a non-zero exit blocks or
informs belong to the skill that owns that stack: `/alaa-frontend-devops` for a frontend repository, `/alaa-cicd-laravel-postgres` for a PHP or Laravel service. When a request asks
this skill to decide whether a check should block, name that owner and write the
mechanism, not the verdict.

Three consequences apply to every task:

- Write how a timeout or a retry is expressed. Never write the value; `/alaa-reliability-sla` owns it.
- Write the build job. Never write the image contents; `/alaa-docker-production` owns them.
- Ship the hardened form of a risky path. Never ship the exception; `/alaa-security-review` owns it.

`references/90-companion-boundary.md` holds the full table.

## Start fast

Collect only the facts that change the design: GitLab.com, Dedicated or self-managed, and the instance version; runner type, shared or dedicated, and the trust model; whether the job needs Docker daemon behaviour or only an image build; the registry, cloud or secret manager involved; and the failure symptom, if this is a debugging task.

Where a fact is missing, apply these defaults and say which you assumed: design against the current stable GitLab and Runner line, not a version number you did not check; use dedicated runners for privileged work; use protected refs for release and deploy jobs.

`references/feature-version-notes.md` gives the cadence that computes the
current line and the URL that confirms it.

Do not use this skill for non-GitLab CI systems, for Kubernetes, Helm or Docker
work where GitLab pipeline behaviour is not the main concern, for application
changes that do not affect CI/CD, or to decide whether a check should block.

## Core workflow

`references/00-topic-map.md` is the router: one trigger condition per file. Open
the narrowest file that matches and do not read the rest.

1. Classify the task: generate, review, validate, debug, or migrate.
2. Verify every version-sensitive claim against the official page named in
   `references/00-source-map.md` before writing it down.
3. Produce the smallest correct solution, then harden it.
4. Validate with the bundled checkers, then CI Lint or `glab ci lint` when
   project access exists and `include:` must be resolved.
5. Close with the output contract below.

## Authoring rules

- Write `workflow:rules` with a terminal arm (defined in
  `references/pipeline-authoring/10-pipeline-creation-and-paths.md`) so pipeline creation is explicit.
- Put the condition that decides whether a job should run into `rules:`, not into a script that exits zero.
- Reuse through a hidden job, `extends`, an include or a component only when the same text appears in three or more jobs or
  when two jobs must change together.

Open `references/pipeline-authoring.md` for workflow and job rules, environments and rollback, includes and components; `references/job-graph-and-scheduling.md` for `needs:`, `resource_group`, `interruptible`, job `timeout:`, `retry:` and `parallel:`; `references/cache-artifacts-and-pinning.md` for any cache key, `policy:`, `fallback_keys`, `expire_in` or image pin.

## Variable and input rules

Use `spec:inputs` for a value that should be validated before the pipeline is created, a CI/CD variable for a runtime value, and a file variable for content a tool reads from a path. Never write a secret literal into YAML.

GitLab expands `$VAR` and `${VAR}` only. So `${VAR:-default}` in a `variables:` value yields an
empty string and overwrites any predefined variable of that name. Open
`references/variables-and-inputs.md` for precedence, masking, `id_tokens:`, the
`secrets:` block, secure files, dotenv and downstream forwarding.

## Runner rules

Outside the Ala fleet the Kubernetes executor is the default. Read the target
Runner's executor before writing a job. For each Ala Runner's executor, job image
and tool limits, read
`/alaa-services-contract` `references/16-infrastructure-services-and-delivery-artifacts.md`,
section "Runner shapes and the CI job image". A shell runner is correct only where the host serves no other tenant, the runner is tagged so only the intended projects reach it, and the jobs that use it run on protected refs.

`values.yaml` is YAML and the `runners.config` inside it is TOML. Open
`references/runner-shell-and-kubernetes.md` for executor choice, `config.toml`,
`concurrent`, `image_pull_secrets`, `helper_image`, distributed cache, RBAC,
namespaces and restricted clusters.

## Container build strategy rules

Choose the first eligible build path, in this order, before writing YAML: rootless BuildKit, then Podman or Buildah, then a shell runner against a host daemon when its four stated preconditions all hold, then Docker-in-Docker on a dedicated privileged runner.

Do not use kaniko; GitLab states it is unmaintained. Open
`references/container-build-strategies.md` before designing any image-build job.

## Security rules

Use the shortest-lived credential the platform offers. Let no credential
outlive the job on a runner whose workspace persists. A token written by
`git remote set-url` stays in `.git/config` for the next job on that host. Open
`references/security-and-hardening.md` for the threat model per runner type, the
credential order, fork and merge-request exposure, and pull policy.

## Debugging rules

Classify the failure before editing anything: YAML or schema, pipeline creation,
runner matching, executor startup, or runtime. Editing a script when the pipeline
was never created wastes a full cycle. Open
`references/validation-and-debugging.md` for the five classes with their symptoms,
diagnosis, smallest retry and escalation point, and for the symptom map.

## Output contract

- The final YAML, TOML or `values.yaml`.
- A variable table: name, type, source, sensitivity, default, consumer.
- Runner prerequisites and tags.
- What was validated statically and what still needs a live GitLab context.
- Assumptions, the version line targeted, and any feature gate.
- Which checks block and which inform, attributed to the skill that decided that.
- A hardening note when the design uses privileged mode, a shell runner, a host
  daemon, or a sensitive credential.

## Built-in assets

Templates in `assets/templates/`. Adapt each one; do not copy it:
`app-basic.gitlab-ci.yml`, `component-with-inputs.gitlab-ci.yml`,
`k8s-buildkit-rootless.gitlab-ci.yml`, `k8s-dind-tls.gitlab-ci.yml`,
`shell-runner-host-daemon.gitlab-ci.yml`,
`shell-runner-trusted-host.gitlab-ci.yml`, `values-k8s-runner.yaml`,
`config-shell-runner.toml`. Every image pin in them carries the URL that
re-derives it.

## Validation scripts

```bash
python3 scripts/validate_gitlab_ci.py <file> [more files]
python3 scripts/validate_runner_config.py <file> [more files]
```

Both accept `--help`, `--json` and `--fail-on-warnings`, and exit **0 clean, 1 findings, 2 could not run**. Exit 2 is never a clean result.
Invoke them by absolute path when the working directory is not the skill root.
What each asserts, what neither can see, and which findings are gate-eligible are
in `references/validation-and-debugging.md`.

## Failure-mode handling

- Without live GitLab access, say what was validated locally and what still needs
  CI Lint or project context.
- Where the request combines incompatible goals, present the safer architecture
  and state the trade-off and who would have to accept it.

## Subagent strategy

Where multi-agent mode is available and the task is large, split by concern:
pipeline semantics, runner or executor configuration, security and version
verification. Merge only after the version-sensitive and security-sensitive
findings agree. Describe a lane by the judgment it needs, not by a tier. Deciding
trade-offs across a pipeline needs the escalated lane. Read-only inventory or
mechanical validation does not.

Take every model and reasoning-effort choice from `/alaa-prompting-guide` `references/50-effort-and-thinking.md`. Name no
model here. A model name written into a skill goes stale silently and is
copied forward because it looks authoritative.
