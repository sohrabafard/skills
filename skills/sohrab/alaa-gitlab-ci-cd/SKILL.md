---
name: alaa-gitlab-ci-cd
description: GitLab CI/CD pipeline generation, validation, review, and debugging for reusable CI components, runner configs, and container-build workflows for GitLab Runner shell, Docker, and Kubernetes executors. Use when the task involves one or more `.gitlab-ci.yml` files, included CI files, CI components, GitLab Runner `config.toml`, Helm `values.yaml`, GitLab Docker or Kubernetes executor behavior, Docker or daemonless image builds, cache keys, artifact retention, variables or inputs, job routing via tags, pipeline security, or CI failure triage. Prefer it for both authoring and debugging. Do not use it for unrelated Kubernetes manifests (use /alaa-k8s-helm), unrelated Dockerfiles (use /alaa-docker-production), or non-GitLab CI systems, and do not use it to decide whether a check should block a pipeline; that belongs to the skill that owns the stack.
---

Act like a production GitLab CI/CD specialist, not a generic YAML writer.

## What this skill owns, and when not to use it

`alaa-gitlab-ci-cd` owns **how a gate is expressed on a runner**: the job graph, `rules:` and `needs:`, every
expression of a cache key, artifact retention and `expire_in`, and the runner image reference. It **decides no gate**.
The skill that owns the stack decides which checks must exist, what each check asserts, and whether a non-zero exit
blocks or informs. That owner is `/alaa-frontend-devops` for a frontend repository and `/alaa-cicd-laravel-postgres`
for a PHP or Laravel service. When a request asks this skill to decide whether a check should block, name that owner
and write the mechanism, not the verdict.

Do not use this skill for non-GitLab CI systems, for Kubernetes, Helm or Docker work where GitLab pipeline behaviour
is not the main concern, or for application changes that do not affect CI/CD.

Three consequences apply to every task:

- Write how a timeout or a retry is expressed. Never write the value; `/alaa-reliability-sla` owns it.
- Write the build job. Never write the image contents; `/alaa-docker-production` owns them.
- Ship the hardened form of a risky path. Never ship the exception; `/alaa-security-review` owns it.

## Start fast

Collect only the facts that change the design:

- GitLab.com, Dedicated or self-managed, and the instance version;
- the runner type, shared or dedicated, and the trust model;
- whether the job needs Docker daemon behaviour or only an image build;
- the registry, cloud or secret manager involved;
- the failure symptom, if this is a debugging task.

When a fact is missing, apply these defaults and say which ones you assumed:

- Design against the current stable GitLab and Runner line, not a version number you did not check.
- Use dedicated runners for privileged work.
- Use protected refs for release and deploy jobs.

## Core workflow

Before you classify or act on any GitLab CI/CD task, read `references/00-topic-map.md`. It routes each task situation to one file. Open the
narrowest file that matches and do not read the rest.

1. Classify the task: generate, review, validate, debug, or migrate.
2. Verify every version-sensitive claim against the official page that the source map names before you write the claim
   down.
3. Produce the smallest correct solution, then harden it.
4. Validate with the bundled checkers. Then run CI Lint or `glab ci lint` when project access exists and `include:`
   must be resolved.
5. Close with the output contract below.

## Variable and input rules

Use `spec:inputs` for a value that must be validated before the pipeline is created. Use a CI/CD variable for a
runtime value. Use a file variable for content that a tool reads from a path. Never write a secret literal into YAML.

GitLab expands `$VAR` and `${VAR}` only. So `${VAR:-default}` in a `variables:` value yields an empty string and
overwrites any predefined variable of that name.

## Runner rules

Outside the Ala fleet the Kubernetes executor is the default. Read the target Runner's executor before you write a
job. For each Ala Runner's executor, job image and tool limits, read
`/alaa-services-contract` `references/16-infrastructure-services-and-delivery-artifacts.md`, section "Runner shapes
and the CI job image". A shell runner is correct only when all three conditions hold: the host serves no other tenant, the runner is tagged so
only the intended projects reach it, and the jobs that use it run on protected refs.

`values.yaml` is YAML, and the `runners.config` inside it is TOML.

## Container build strategy rules

Before you write YAML, choose the first eligible build path in this order:

1. rootless BuildKit;
2. Podman or Buildah;
3. a shell runner against a host daemon, when all four of its stated preconditions hold;
4. Docker-in-Docker on a dedicated privileged runner.

Do not use kaniko, because GitLab states that it is unmaintained.

## Security rules

Use the shortest-lived credential the platform offers. Let no credential outlive the job on a runner whose workspace
persists. For example, a token written by `git remote set-url` stays in `.git/config` for the next job on that host.

## Debugging rules

Classify the failure before you edit anything. The five classes are YAML or schema, pipeline creation, runner
matching, executor startup, and runtime. Editing a script when the pipeline was never created wastes a full cycle.

## Output contract

- The final YAML, TOML or `values.yaml`.
- A variable table: name, type, source, sensitivity, default, consumer.
- Runner prerequisites and tags.
- What was validated statically and what still needs a live GitLab context.
- Assumptions, the version line targeted, and any feature gate.
- Which checks block and which inform, attributed to the skill that decided that.
- A hardening note when the design uses privileged mode, a shell runner, a host daemon, or a sensitive credential.

## Built-in assets

Templates are in `assets/templates/`. Adapt each one; do not copy it: `app-basic.gitlab-ci.yml`,
`component-with-inputs.gitlab-ci.yml`, `k8s-buildkit-rootless.gitlab-ci.yml`, `k8s-dind-tls.gitlab-ci.yml`,
`shell-runner-host-daemon.gitlab-ci.yml`, `shell-runner-trusted-host.gitlab-ci.yml`, `values-k8s-runner.yaml`,
`config-shell-runner.toml`.

## Validation scripts

```bash
python3 scripts/validate_gitlab_ci.py <file> [more files]
python3 scripts/validate_runner_config.py <file> [more files]
```

Both accept `--help`, `--json` and `--fail-on-warnings`. Both exit **0 clean, 1 findings, 2 could not run**. Exit 2 is
never a clean result. Invoke them by absolute path when the working directory is not the skill root.

## Failure-mode handling

- Without live GitLab access, say what was validated locally and what still needs CI Lint or project context.
- When the request combines incompatible goals, present the safer architecture. State the trade-off and who would have
  to accept it.

## Subagent strategy

Split work across agents only when multi-agent mode is available and the task spans more than one of these concerns:
pipeline semantics, runner or executor configuration, security, and version verification. Keep a single-concern task
in one agent, because each lane adds a dispatch and a merge. Merge only after the version-sensitive and
security-sensitive findings agree. Describe a lane by the judgment it needs, not by a tier. Deciding trade-offs across
a pipeline needs the escalated lane. Read-only inventory or mechanical validation does not.

Take every model and reasoning-effort choice from `/alaa-prompting-guide` `references/50-effort-and-thinking.md`. Name
no model here, because a model name written into a skill goes stale silently and is copied forward because it looks
authoritative.
