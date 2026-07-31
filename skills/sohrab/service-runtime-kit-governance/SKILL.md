---
name: service-runtime-kit-governance
description: "Ownership and debug governance for `service-runtime-kit`-generated local Docker Compose and Swarm runtime in Laravel or PHP service repositories. Use when working in a repo that consumes `service-runtime-kit`, or when changing `runtime/*.env`, `runtime/hooks/**`, `scripts/runtime/**`, generated `docker-compose*.yml`, generated `docker/octane/**` or `docker/pgbouncer/**`, copied helpers such as `validate_runtime.php`, runtime-kit version pinning, bootstrap or auto-fetch behavior, or Windows Git Bash path conversion of slash-valued Compose env vars, and when deciding which layer owns a runtime fix or debug path. Do not use for application logic unrelated to runtime generation. Route Kubernetes, OpenShift, and Helm deployment to /caas-arvan-kuber; GitLab CI/CD pipelines owned by `service-ci-kit` to /alaa-gitlab-ci-cd; the shared-infra and deployment contract to /alaa-services-contract."
---

# Service Runtime Kit Governance

Load before changing any runtime-related file in a service repo driven by `service-runtime-kit`. Trigger prefix for skills named below: `/name` in Claude Code, `$name` in Codex.

- `references/change-routing.md` — where a change belongs; the regenerate command pair.
- `references/runtime-contract-map.md` — which file or variable produces a behavior; which paths are generated; which knob owns a tuning value; how to check the pinned kit.
- `references/debug-playbook.md` — a runtime path fails and the cause is not located.
- `references/cross-runtime-shared-infra.md` — shared Postgres, Redis, RabbitMQ, or Adminer is touched, or a Go service on the `alaa-go-chi` kit is in scope.
- `references/windows-git-bash-compose.md` — a slash-valued Compose env var looks corrupted on Windows.
- `references/source-map.md` — before relying on latest, current, or security-sensitive behavior.

## Goal

Every generated file in the repository is byte-identical to what a fresh render would produce from the current inputs, and every runtime change lands in the layer that owns it.

`service-runtime-kit` owns shared runtime generation; the service repo owns its supported runtime inputs and the copied thin wrappers under `scripts/runtime/`, nothing more.

## Ownership Model

Classify before editing. `references/change-routing.md` holds the routing table and examples.

1. **Service-specific runtime contract change.** Choose this when the behavior is already supported for one service by an existing input file or variable.
2. **Shared runtime generation change.** Choose this when the request changes how runtime files are generated, or bootstrap support is copied, for many services. The fix belongs in the sibling `service-runtime-kit` repo, never in the generated file.
3. **Deployment concern, not local runtime.** Choose this when the request is cluster deployment rather than local Compose or Swarm.

Normal application env always goes in the service `.env` and never in `runtime/service.runtime.env`, because that file carries only generation-time metadata and the application never reads it at runtime.

## Non-negotiable Rule

Every path catalogued as a generated output in `references/runtime-contract-map.md` is an output, not an authoring surface. Only `AGENTS.md` or `CLAUDE.md` at the service repo root may declare an exception; absent a statement there, treat the path as generated.

Editing a generated file to reproduce or isolate a fault is allowed. Then: revert that edit, fix the owning layer, rerender, and confirm the regenerated file carries the change.

## Shared Runtime Contract Ownership

`alaa-services-contract` `references/15-deployment-and-runtime-contract.md` owns the canonical shared-infra identity, the reuse-or-fail-fast obligation, and the host-published port defaults. That contract outranks any single generator, so do not restate its values here. This skill owns only which generator variable expresses each: `DOCKER_SHARED_INFRA_PROJECT_DEFAULT`, `DOCKER_SHARED_NETWORK_NAME_DEFAULT`, `DOCKER_VOLUME_PREFIX_DEFAULT`, and the `*_FORWARD_PORT` knobs.

Generator behavior is this skill's: a wrapper reuses an already-running shared instance untouched rather than recreating it, and on an indeterminable state it refuses to recreate rather than clobber a peer's data.

## Working Method

**Service-specific change.** Edit the service-owned input, regenerate and validate with the command pair in `references/change-routing.md`, then review the generated diff and keep only the intended change.

**Shared `service-runtime-kit` change.**

1. Change the sibling `service-runtime-kit` repo.
2. Bump the pin in `runtime/runtime-kit.env`, or refresh the copied `scripts/runtime/*` wrappers, when the bootstrap layer changed.
3. Rerender and validate in the service repo.
4. Confirm no generated file about to be committed carries secret material — no `APP_KEY` value, no Passport key contents, no DB or broker password, no token — because generated outputs are committed, so a secret rendered into one is a secret published. `alaa-services-contract` `references/15-deployment-and-runtime-contract.md:184-191` holds the contract; `alaa-security-review` owns the doctrine.
5. Commit the regenerated outputs.

**Change to the shared contract both generators implement.** That contract is `alaa-services-contract`'s, and a change to it must land in both `service-runtime-kit` and the `alaa-go-chi` kit, or the Laravel and Go fleets stop reusing one shared instance. When the `alaa-go-chi` kit is not in the workspace: change nothing in the shared contract, report which generator you can reach and which you cannot, and stop.

## Load-Dependent Configuration

This skill owns which generated file and variable carries a tuning value, never the value. Pool sizing, worker retry, and lock-timeout values come from `alaa-reliability-sla` for doctrine and `alaa-services-contract` `references/22-failure-load-and-deprecation-contract.md` for Ala values; generated telemetry values come from `alaa-observability-soc`. Choose no number here. `references/runtime-contract-map.md` maps each knob to its owner and holds the `PGBOUNCER_MODE` topology rule.

## Expected Response Behavior

State the ownership decision in one explicit sentence before editing, such as:

- `This is a service-specific runtime contract change; I will update .env or runtime/.`
- `This is a shared runtime generation change; the real fix belongs in service-runtime-kit.`
- `This is a deployment concern; it belongs in the deployment layer, not runtime generation.`

## Validation Standard

Complete only when all hold: the correct layer was chosen; no generated file was hand-edited as the final fix; outputs were regenerated; `bash scripts/runtime/validate-runtime.sh` exited `0` or the blocker was named explicitly; the diff matches the intended behavior and carries no secret material.

## Failure Modes To Watch For

- editing `docker-compose*.yml` directly instead of the contract or the shared kit
- editing `scripts/docker/*.sh` directly instead of hooks or the shared kit
- putting normal app env into `runtime/service.runtime.env` when it belongs in `.env`
- mixing `service-runtime-kit` and `service-ci-kit` responsibilities

## When NOT to use

- The change is application logic — a controller, a job, a migration, a test — with no effect on generated
  runtime files, `runtime/*.env` values, hooks, or the kit pin.
- The repository does not consume `service-runtime-kit` and no task proposes adopting it.
- The target is a Kubernetes, OpenShift, or Helm deployment, or a CI pipeline, rather than local Compose or
  Swarm runtime. The ownership section below names each owner.

## What This Skill Does Not Own

The description names the deployment-side boundaries. Within local runtime, hand off image and container hardening to `alaa-docker-production`, Laravel queue-worker and RabbitMQ application behavior to `alaa-laravel-job-rabbitmq`, Postgres/PgBouncer/Redis data-layer design to `alaa-data-layer`, and model or effort selection to `alaa-prompting-guide`.

## Subagent Strategy

Parallelize only after the ownership class is decided, and only when the task spans both the service repo and the sibling kit, or touches more than three generated files. One read-only lane inspects service-owned inputs and the generated diff; one read-only lane inspects the sibling renderer, templates, or bootstrap files. Keep the ownership decision, the edit, the rerender, and the validation in the main lane so the change cannot split across two layers.
