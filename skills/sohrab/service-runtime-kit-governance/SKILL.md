---
name: service-runtime-kit-governance
description: Use when working in a Laravel or PHP service repository that consumes `service-runtime-kit` for local Docker Compose or Docker Swarm runtime generation. Trigger for changes to `runtime/*.env`, `runtime/hooks/**`, `runtime/env.*.extra`, `runtime/README.md`, `scripts/runtime/**`, generated `docker-compose*.yml`, generated `scripts/docker/**`, generated `docker/octane/**`, generated `docker/pgbouncer/**`, `.gitattributes`, `.githooks/**`, copied runtime helper scripts such as `scripts/setup-git-hooks-bom.*` or `scripts/validate_runtime.php`, runtime-kit version pinning, bootstrap or auto-fetch behavior, or questions about which layer owns a runtime fix or debug path. Do not use for Kubernetes, OpenShift, Helm, or GitLab CI deployment changes owned by `service-ci-kit`, or for pure application logic unrelated to runtime generation.
---

# Service Runtime Kit Governance

Use this skill before changing any runtime-related file in a service repo that is driven by `service-runtime-kit`.

Read `references/change-routing.md` first when the main question is where the change belongs.

Read `references/runtime-contract-map.md` when you need to know which file, variable, or debug step matches the requested runtime behavior.

Read `references/source-map.md` before relying on latest/current/version/security-sensitive runtime-kit, Docker Compose, Docker Swarm, image, or generated wrapper behavior.

## Goal

Keep runtime changes in the correct layer and keep generated outputs honest.

- `service-runtime-kit` owns shared local runtime generation.
- The service repo owns only supported runtime inputs plus the copied thin wrappers under `scripts/runtime/`.
- Generated files are outputs and must not be the final authoring surface.
- `service-ci-kit` owns GitLab CI/CD for Kubernetes or OpenShift deployment, not local Compose or Swarm runtime behavior.

## When NOT to use

- Do not use for Kubernetes, OpenShift, Helm, or GitLab CI deployment changes.
- Do not use for pure application logic unrelated to runtime generation.
- Do not use to edit generated runtime artifacts without checking runtime-kit ownership.

## Ownership Model

Classify the request before editing anything.

### 1. Service-specific runtime contract change

Choose this when the requested behavior is already supported for one service.

Typical homes:

- `.env`
- `runtime/service.runtime.env`
- `runtime/runtime-kit.env`
- `runtime/secret-files.env`
- `runtime/env.common.extra`
- `runtime/env.app.extra`
- `runtime/env.worker.extra`
- `runtime/env.scheduler.extra`
- `runtime/hooks/**`

Typical examples:

- choose service name or image fallback
- enable or disable worker or scheduler
- choose dedicated, shared, or off PgBouncer mode
- set queue names, worker tries, or worker timeout
- disable host exposure by setting `APP_PORT=null`, `ADMINER_PORT=null`, `POSTGRES_FORWARD_PORT=null`, or `PGBOUNCER_FORWARD_PORT=null`
- add service-only env lines through `runtime/env.*.extra`
- add service-only provisioning or migration behavior through `runtime/hooks/**`
- set `LOG_CHANNEL=stderr` in the service `.env` so Docker logs are visible for that service

### 2. Shared runtime generation change

Choose this when the requested behavior changes how runtime files are generated or how bootstrap support is copied for many services.

This belongs in the sibling `service-runtime-kit` repository, not in the generated file inside the service repo.

Typical examples:

- compose topology or generated service structure
- generated `scripts/docker/*.sh`
- generated `docker/octane/*`
- generated `docker/pgbouncer/*`
- render or validate behavior
- bootstrap wrappers and auto-fetch behavior
- repo-support seeding such as `.gitattributes`, `.githooks/**`, `scripts/setup-git-hooks-bom.*`, `scripts/validate_runtime.php`, and `runtime/README.md`
- new runtime contract fields or new shared fallback behavior
- Redis runtime endpoint wiring
- RabbitMQ queue bootstrap or env alias compatibility

### 3. Deployment concern, not local runtime

Choose this when the request is really about cluster deployment rather than local Compose or Swarm runtime.

This belongs in `service-ci-kit` or deployment files, not in `service-runtime-kit`.

Typical examples:

- GitLab CI jobs or stages
- Helm values or chart structure
- Kubernetes or OpenShift manifests
- deploy-time secrets, mounts, RBAC, ingress, HPA, or rollout logic

## Non-negotiable Rule

Treat these as generated outputs unless the repo explicitly documents otherwise:

- `docker-compose.yml`
- `docker-compose.dev.yml`
- `docker-compose.swarm.yml`
- `scripts/docker/up-local.sh`
- `scripts/docker/provision-postgres.sh`
- `scripts/docker/provision-rabbitmq.sh`
- `scripts/docker/ensure-local-secrets.sh`
- `scripts/docker/ensure-swarm-runtime-secrets.sh`
- `docker/octane/*`
- `docker/pgbouncer/*`

Inspect them freely. Use them to confirm current behavior. But do not keep the final fix there.

## Current Shared Runtime Facts Agents Must Know

- `bash scripts/docker/up-local.sh` defaults to `prod`.
- Generated runtime outputs are standalone at runtime and should not call back into `../service-runtime-kit`.
- `scripts/runtime/render-runtime.sh` is the generation-time entrypoint and still depends on `service-runtime-kit`.
- `render-runtime.sh` now fails early when required service `.env` values are missing.
- `render-runtime.sh` also seeds or refreshes repo-support files such as `.gitattributes`, `.githooks`, BOM helper scripts, `scripts/validate_runtime.php`, `runtime/README.md`, and missing `runtime/env.*.extra` starter files.
- Render attempts local git hook setup automatically when Git and Python are available.
- `scripts/runtime/ensure-runtime-kit.sh` may prefer a valid sibling `../service-runtime-kit` over a stale repo-local `.service-runtime-kit` cache when `SERVICE_RUNTIME_KIT_PREFER_SHARED_PARENT=true`.
- Generated container env exports both `RABBITMQ_USER` / `RABBITMQ_PASS` and `RABBITMQ_USERNAME` / `RABBITMQ_PASSWORD`.
- Generated container-to-container Redis wiring uses `REDIS_RUNTIME_HOST`, `REDIS_RUNTIME_CACHE_HOST`, and `REDIS_RUNTIME_PORT`.
- Logging visibility is service-owned. Use service `.env` values such as `LOG_CHANNEL=stderr`; do not solve that by forcing a shared `LOG_STACK` override.
- PgBouncer mode supports `dedicated`, `shared`, and `off`.
- `APP_PORT`, `ADMINER_PORT`, `POSTGRES_FORWARD_PORT`, and `PGBOUNCER_FORWARD_PORT` can be set to `null` in `.env` to suppress host publishing after rerender.
- Adminer is shared local infra, not a service-owned application service.
- When `QUEUE_CONNECTION=rabbitmq`, local bootstrap now provisions queues before workers begin polling.

## Working Method

### When the change is service-specific

1. Edit the correct service-owned runtime input.
2. Regenerate runtime outputs.
3. Validate runtime outputs.
4. Review the generated diff and keep only the intended change.

Commands:

```bash
bash scripts/runtime/render-runtime.sh
bash scripts/runtime/validate-runtime.sh
```

### When the change belongs to `service-runtime-kit`

1. Make the shared change in the sibling `service-runtime-kit` repo.
2. Update the service kit pin or copied wrapper files if the bootstrap layer changed.
3. Regenerate in the service repo.
4. Validate in the service repo.
5. Commit the regenerated outputs in the service repo.

### When wrappers cannot find the kit

Use one of the supported sources:

- keep the kit at `../service-runtime-kit`
- set `SERVICE_RUNTIME_KIT_DIR` to a valid local path
- configure `SERVICE_RUNTIME_KIT_PROJECT` or `SERVICE_RUNTIME_KIT_ARCHIVE_URL` in `runtime/runtime-kit.env`

Do not fix missing-kit problems by editing generated outputs manually.

## Decision Rules That Avoid Common Mistakes

- If the request is about normal app configuration such as `APP_NAME`, `APP_ENV`, `APP_DEBUG`, `LOG_CHANNEL`, DB credentials, RabbitMQ credentials, Redis connection values, or direct app port values, prefer the service `.env`.
- If the request is about runtime-kit metadata, toggles, or defaults consumed by generation, use `runtime/service.runtime.env`.
- If the request changes a fallback value already supported by the contract, edit the relevant `*_DEFAULT` variable.
- If the request changes which env var name generated files read from, edit the relevant `*_ENV` variable.
- If the request adds service-only env lines, prefer `runtime/env.*.extra`.
- If the request adds service-specific pre or post provisioning logic, prefer `runtime/hooks/**`.
- If the request requires a new generated file shape or a new contract field, change `service-runtime-kit`.
- If the request is about `.gitattributes`, `.githooks`, BOM stripping, or copied helper scripts for every service, that is a shared `service-runtime-kit` concern.
- If the request is about Kubernetes, OpenShift, Helm, or GitLab CI, route it away from this skill.

## Debug Playbook

When debugging a service that uses `service-runtime-kit`, check these in order.

### 1. Confirm ownership

- Is this a service `.env` issue?
- Is this a supported `runtime/` contract issue?
- Is this a shared generator issue?
- Is this actually a deploy concern outside local runtime?

### 2. Confirm the service is using the expected kit source

- inspect `runtime/runtime-kit.env`
- inspect `scripts/runtime/ensure-runtime-kit.sh`
- check whether the repo is using a stale `.service-runtime-kit` cache
- prefer the sibling shared kit when the team intentionally works that way

### 3. Regenerate before trusting generated output

```bash
bash scripts/runtime/render-runtime.sh
bash scripts/runtime/validate-runtime.sh
```

Do not assume a generated file still reflects the latest `.env` or runtime contract until rerender has completed successfully.

### 4. Read the right layer for common failures

- app cannot connect to Redis inside containers:
  check generated `REDIS_RUNTIME_*` values and the service `.env` split between host-side Redis and container-side Redis
- worker cannot authenticate to RabbitMQ:
  confirm the service config expects `RABBITMQ_USER` or `RABBITMQ_USERNAME`, then verify the generated env block exports both naming variants
- worker crashes because queue does not exist:
  confirm `QUEUE_CONNECTION=rabbitmq`, queue names, and generated RabbitMQ bootstrap flow
- render still behaves like an old bug after a shared fix:
  suspect stale wrapper files or a stale local `.service-runtime-kit` cache
- service logs are not visible in Docker:
  prefer `LOG_CHANNEL=stderr` in the service `.env`, not a shared forced logging override
- corrected `.env` still appears ignored:
  rerender first, then inspect whether the actual generated file reads `.env` directly or a runtime default from `runtime/service.runtime.env`

### 5. Validate the original failing path again

Do not stop at a successful rerender. Re-run the exact bootstrap or runtime path that was failing.

## Expected Response Behavior

When using this skill, state the ownership decision clearly.

Use direct language such as:

- `This is a service-specific runtime contract change; I will update .env or runtime/.`
- `This is a shared runtime generation change; the real fix belongs in service-runtime-kit.`
- `This is a deployment concern; it belongs in service-ci-kit or deployment files, not runtime generation.`

## Validation Standard

A runtime change is not complete until all of these are true:

- the correct ownership layer was chosen
- generated files were not hand-edited as the final fix
- runtime outputs were regenerated
- `bash scripts/runtime/validate-runtime.sh` passed, or the blocker was explicitly identified
- the resulting diff matches the intended behavior

## Failure Modes To Watch For

- editing `docker-compose*.yml` directly instead of changing the contract or the shared kit
- editing `scripts/docker/*.sh` directly instead of changing hooks or the shared kit
- putting normal app env into `runtime/service.runtime.env` when it belongs in `.env`
- forcing shared logging behavior when the service should own `LOG_CHANNEL`
- forgetting that render now seeds repo-support files and can overwrite generated guidance such as `runtime/README.md`
- assuming a stale local `.service-runtime-kit` cache is harmless
- mixing `service-runtime-kit` and `service-ci-kit` responsibilities
- assuming every variable present in `runtime/service.runtime.env` is consumed without checking the actual shared kit version

## Subagent Strategy

For broad runtime work, parallelize exploration only after classification.

- Use one read-only lane to inspect service-owned runtime inputs and the generated output diff.
- Use one read-only lane to inspect the sibling `service-runtime-kit` renderer, templates, or bootstrap files when the change looks shared.
- Keep the final ownership decision, implementation, rerender, and validation in the main lane so the change does not split across the wrong layer.
