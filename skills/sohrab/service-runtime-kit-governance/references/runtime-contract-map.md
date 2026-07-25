# Runtime Contract Map

Use this reference when you need to know which file or variable to change and what effect that change has.

This map reflects the latest `service-runtime-kit` behavior described by the shared renderer and README, including the newer bootstrap support files, repo-support seeding, RabbitMQ compatibility aliases, Redis runtime endpoints, null-port handling, and service-owned logging policy.

## Core Principle

The service repo owns the runtime input contract.

Generated files such as `docker-compose*.yml`, `scripts/docker/*.sh`, `docker/octane/*`, and `docker/pgbouncer/*` are outputs.

Useful shorthand:

- variables ending in `*_DEFAULT` usually change a generated fallback value
- variables ending in `*_ENV` usually change which env variable name generated files read from

### Generated Outputs

The generated set under the globs above is `docker-compose.yml`, `docker-compose.dev.yml`, `docker-compose.swarm.yml`, `scripts/docker/up-local.sh`, `scripts/docker/provision-postgres.sh`, `scripts/docker/provision-rabbitmq.sh`, `scripts/docker/ensure-local-secrets.sh`, `scripts/docker/ensure-swarm-runtime-secrets.sh`, `docker/octane/*`, and `docker/pgbouncer/*`. `SKILL.md` "Non-negotiable Rule" holds the constraint and the one allowed exception.

Generation time and run time differ:

- `scripts/runtime/render-runtime.sh` is the generation-time entrypoint and needs `service-runtime-kit` resolvable.
- Generated outputs are standalone at run time and must not call back into `../service-runtime-kit`; one that does is a shared-kit defect.
- `bash scripts/docker/up-local.sh` defaults to `prod` when given no mode argument.

## Tuning Values This Skill Does Not Choose

These knobs are configurable only here, but the values are doctrine owned elsewhere. Take the value from the owner; do not pick a number from local reasoning. Trigger prefix: `/name` in Claude Code, `$name` in Codex.

- `PGBOUNCER_POOL_MODE_DEFAULT`, `PGBOUNCER_DEFAULT_POOL_SIZE_DEFAULT`, `PGBOUNCER_MAX_CLIENT_CONN_DEFAULT`, `QUEUE_WORKER_TRIES_DEFAULT`, `QUEUE_WORKER_TIMEOUT_DEFAULT`, `DB_PROVISION_LOCK_TIMEOUT_SECONDS_DEFAULT` — `alaa-reliability-sla` for pool-sizing and retry doctrine; `alaa-services-contract` `references/22-failure-load-and-deprecation-contract.md` for Ala values.
- any generated telemetry variable — `alaa-observability-soc`.

## Service-Owned Files And What They Are For

| File | Role | Typical use |
|---|---|---|
| `.env` | normal service application env | app name, app mode, logging channel, DB credentials, RabbitMQ credentials, Redis host, direct app port values |
| `runtime/service.runtime.env` | main runtime generation contract | service identity, image, naming, toggles, kit-consumed defaults, PgBouncer mode, worker and scheduler defaults |
| `runtime/runtime-kit.env` | bootstrap and version pin | where the kit comes from, which ref to use, whether auto-fetch is enabled |
| `runtime/secret-files.env` | local and Swarm file-backed secret contract | secret filenames, source env names, external Swarm secret names |
| `runtime/env.common.extra` | extra env for all generated runtime services | shared app, worker, and scheduler env lines |
| `runtime/env.app.extra` | app-only extra env | web or Octane-only settings |
| `runtime/env.worker.extra` | worker-only extra env | queue worker specific settings |
| `runtime/env.scheduler.extra` | scheduler-only extra env | scheduler specific settings |
| `runtime/README.md` | generated service-facing guide | explains supported runtime entrypoints and extension points; improve in `service-runtime-kit`, not ad hoc in one service |
| `runtime/hooks/before-provision/*` | pre-DB bootstrap hook stage | custom checks or preparation before provisioning |
| `runtime/hooks/after-provision-admin/*` | post-admin connection hook stage | logic that needs admin DB connection to have finished |
| `runtime/hooks/after-provision-db/*` | post-app DB bootstrap hook stage | logic after schema ownership and grants are applied |
| `runtime/hooks/before-migrate/*` | pre-migrate hook stage | custom steps before app migration |
| `runtime/hooks/after-migrate/*` | post-migrate hook stage | custom steps after migration |

Hooks must be executable.

## Repo-Support Files Seeded By The Shared Kit

These are copied or refreshed by the shared render and bootstrap flow when missing or when the shared source is authoritative.

| File | Role |
|---|---|
| `.gitattributes` | contains the shared managed BOM/LF block |
| `.githooks/pre-commit` | blocks staged BOM regressions |
| `.githooks/README.md` | explains the local hook setup |
| `scripts/setup-git-hooks-bom.sh` | configures BOM stripping and `core.hooksPath` on Unix-like shells |
| `scripts/setup-git-hooks-bom.ps1` | configures the same for PowerShell usage |
| `scripts/validate_runtime.php` | shared runtime validation helper copied into each service |

Treat these as copied shared support assets. If the behavior should change for all services, fix `service-runtime-kit`.

Current render behavior:

- render seeds or refreshes these files, and any missing `runtime/env.*.extra` starter files, on every run
- render can overwrite generated guidance such as `runtime/README.md`, so a service-local edit to it is lost on the next render; change it in `service-runtime-kit`
- render attempts local git hook setup automatically when Git and Python are both available

## `.env`

Keep normal application env here.

Typical values that belong in `.env`:

- `APP_NAME`
- `APP_ENV`
- `APP_DEBUG`
- `LOG_CHANNEL`
- `DB_HOST`, `DB_PORT`, `DB_DATABASE`, `DB_USERNAME`, `DB_PASSWORD`
- `RABBITMQ_HOST`, `RABBITMQ_PORT`, and RabbitMQ user and password values
- `REDIS_HOST`, `REDIS_PORT`, `REDIS_CACHE_HOST`
- direct app and infra publishing values such as `APP_PORT`, `ADMINER_PORT`, `POSTGRES_FORWARD_PORT`, `PGBOUNCER_FORWARD_PORT`

Important current behavior:

- to make Laravel logs visible in `docker logs`, set `LOG_CHANNEL=stderr` in the service `.env`
- do not solve logging visibility by forcing a shared `LOG_STACK` override in the kit
- for host-side local tooling, `.env` may still use values such as `REDIS_HOST=127.0.0.1`

## `runtime/runtime-kit.env`

| Variable | Change this when | Effect |
|---|---|---|
| `SERVICE_RUNTIME_KIT_PROJECT` | the kit lives in a specific GitLab project path | enables archive download when the kit is not already local |
| `SERVICE_RUNTIME_KIT_PROJECT_NAME` | the kit uses a different repo name in the same namespace | changes the derived archive source |
| `SERVICE_RUNTIME_KIT_REF` | you need a newer or older tagged kit version | changes which kit version is fetched or expected |
| `SERVICE_RUNTIME_KIT_ARCHIVE_URL` | you want a direct archive source instead of project derivation | bypasses derived GitLab archive URL building |
| `SERVICE_RUNTIME_KIT_GITLAB_API_V4_URL` | the GitLab API base URL is not standard | changes archive URL derivation |
| `SERVICE_RUNTIME_KIT_TOKEN` | local download needs an explicit private token | lets wrappers fetch a private archive |
| `SERVICE_RUNTIME_KIT_AUTO_FETCH` | wrappers should download the kit automatically when missing | turns archive fetch on or off |
| `SERVICE_RUNTIME_KIT_AUTO_REFRESH` | wrappers should replace an older local kit automatically when refs differ | allows refresh by ref mismatch |
| `SERVICE_RUNTIME_KIT_PREFER_SHARED_PARENT` | one shared sibling kit should win over a local cache | prefers `../service-runtime-kit` over a repo-local copy when valid |

## `runtime/service.runtime.env`

Use this file for runtime-kit-specific metadata and generation defaults, not for normal service secrets or baseline app env.

### Service Identity And Image

| Variables | Use for | Generated effect |
|---|---|---|
| `SERVICE_NAME` | stable logical name of the service | used in generated naming and messaging |
| `SERVICE_IMAGE_VAR` | env variable name that holds the service image | changes which env var generated files reference for image selection |
| `SERVICE_IMAGE_DEFAULT` | fallback image tag | changes the default image used when the env override is absent |

### Project, Stack, Volume, And Shared Infra Naming

| Variables | Use for | Generated effect |
|---|---|---|
| `DOCKER_PROJECT_NAME_DEFAULT` | default Compose project name | changes generated `name:` and related naming fallbacks |
| `DOCKER_DEV_PROJECT_NAME_DEFAULT` | default dev project name | changes dev-mode Compose naming fallback |
| `DOCKER_STACK_NAME_DEFAULT` | default Swarm stack name | changes generated Swarm naming fallback |
| `DOCKER_VOLUME_PREFIX_DEFAULT` | default named-volume prefix | changes generated named-volume fallbacks |
| `DOCKER_SHARED_NETWORK_NAME_DEFAULT` | shared network fallback | changes the network name generated files refer to |
| `DOCKER_SHARED_INFRA_PROJECT_DEFAULT` | shared infra project fallback | changes generated cross-project naming references |

### Ports And Exposed Env Variable Names

These defaults are still consumed by the current kit. Service `.env` values can override them.

| Variables | Use for | Generated effect |
|---|---|---|
| `APP_PORT_ENV` | external env variable name for the main app port | changes the variable name referenced by generated files |
| `APP_PORT_DEFAULT` | fallback external app port | changes the default host port for the main app service |
| `DEV_APP_PORT_ENV` | external env variable name for dev app port | changes the variable name used by dev runtime files |
| `DEV_APP_PORT_DEFAULT` | fallback dev app port | changes the default dev host port |
| `ADMINER_PORT_ENV` | external env variable name for Adminer port | changes the variable name referenced by generated files |
| `ADMINER_PORT_DEFAULT` | fallback Adminer host port | changes the default Adminer port |

Current detail:

- setting `APP_PORT=null`, `ADMINER_PORT=null`, `POSTGRES_FORWARD_PORT=null`, or `PGBOUNCER_FORWARD_PORT=null` in `.env` disables host publishing after rerender

### Build And Container Defaults

| Variables | Use for | Generated effect |
|---|---|---|
| `PUBLIC_DOCKER_REGISTRY_DEFAULT` | default image proxy or mirror prefix | changes Docker build arg fallback |
| `OCTANE_BASE_IMAGE_DEFAULT` | default Octane runtime base image | changes Docker build arg fallback |
| `DOCKER_COMPOSER_VERSION_DEFAULT` | default Composer version during build | changes Docker build arg fallback |
| `WWWUSER_DEFAULT`, `WWWGROUP_DEFAULT` | container user and group defaults | changes build args and runtime env fallbacks |
| `TZ_DEFAULT` | timezone fallback | changes generated container env default |

Current detail:

- the current `up-local.sh` path normalizes `PUBLIC_DOCKER_REGISTRY` so both `mirror.cdn.ir` and `mirror.cdn.ir/` work there

### Runtime Topology Toggles

| Variables | Use for | Generated effect |
|---|---|---|
| `RUNTIME_WORKER_ENABLED` | turn generated worker service on or off | worker service is added or omitted |
| `RUNTIME_SCHEDULER_ENABLED` | turn generated scheduler service on or off | scheduler service is added or omitted |
| `RUNTIME_APP_ENABLED` | version-specific app toggle metadata | verify current consumption before relying on it |
| `SCHEDULER_MODE` | service-owned scheduler metadata | use only if adjacent tooling reads it explicitly |
| `K8S_SCHEDULER_MODE` | deployment-adjacent scheduler metadata | do not assume local runtime consumes it |

### Database Provisioning

| Variables | Use for | Generated effect |
|---|---|---|
| `DB_CONNECTION_DEFAULT` | default DB driver | changes generated `DB_CONNECTION` fallback |
| `DB_DATABASE_DEFAULT`, `DB_USERNAME_DEFAULT`, `DB_PASSWORD_DEFAULT` | service DB defaults | change generated DB env fallbacks and provisioning defaults |
| `DB_PROVISION_ENABLED_DEFAULT` | enable or disable generated DB bootstrap behavior | changes generated provisioning behavior |
| `DB_PROVISION_HOST_DEFAULT`, `DB_PROVISION_PORT_DEFAULT` | where provisioning connects | change generated provisioning defaults and PgBouncer database entries |
| `DB_PROVISION_ADMIN_DATABASE_DEFAULT`, `DB_PROVISION_ADMIN_USERNAME_DEFAULT`, `DB_PROVISION_ADMIN_PASSWORD_DEFAULT` | admin connection defaults for bootstrap | change generated provisioning defaults |
| `DB_PROVISION_LOCK_TIMEOUT_SECONDS_DEFAULT` | advisory-lock timeout fallback | changes generated provisioning script behavior |

Debug note:

- if changing `DB_HOST` alone does not fix provisioning, inspect whether generated provisioning uses `DB_PROVISION_HOST` or its defaults instead

### PgBouncer

| Variables | Use for | Generated effect |
|---|---|---|
| `PGBOUNCER_MODE` | choose dedicated, shared, or off | changes whether the generated runtime points the app at dedicated PgBouncer, shared PgBouncer, or direct Postgres |
| `SHARED_PGBOUNCER_HOST_DEFAULT`, `SHARED_PGBOUNCER_PORT_DEFAULT` | shared PgBouncer target defaults | change app DB host and port fallbacks in shared mode |
| `PGBOUNCER_LISTEN_PORT_DEFAULT` | dedicated PgBouncer listen port | changes generated dedicated PgBouncer service config |
| `PGBOUNCER_POOL_MODE_DEFAULT`, `PGBOUNCER_DEFAULT_POOL_SIZE_DEFAULT`, `PGBOUNCER_MAX_CLIENT_CONN_DEFAULT` | pool behavior defaults | change generated `docker/pgbouncer/pgbouncer.ini` |
| `PGBOUNCER_AUTH_TYPE_DEFAULT`, `PGBOUNCER_ADMIN_USERS_DEFAULT`, `PGBOUNCER_STATS_USERS_DEFAULT` | auth and operator defaults | change generated PgBouncer config |

Selecting `PGBOUNCER_MODE` is a runtime-topology decision this skill owns: `dedicated` when the service must not share a pooler's client-connection budget with peers, `shared` when it targets the canonical shared PgBouncer, `off` when the app connects straight to Postgres. `PGBOUNCER_POOL_MODE_DEFAULT` is a different decision — see "Tuning Values This Skill Does Not Choose".

### Queue And RabbitMQ

| Variables | Use for | Generated effect |
|---|---|---|
| `QUEUE_CONNECTION_DEFAULT` | default queue backend | changes generated queue env fallback |
| `RABBITMQ_USERNAME_DEFAULT`, `RABBITMQ_PASSWORD_DEFAULT`, `RABBITMQ_VHOST_DEFAULT` | broker credentials and vhost fallbacks | change generated queue env fallbacks |
| `RABBITMQ_QUEUE_DEFAULT` | default queue name | changes default queue names used by generated runtime |
| `QUEUE_WORKER_QUEUES_DEFAULT` | worker queue list fallback | changes worker command or env defaults |
| `QUEUE_WORKER_TRIES_DEFAULT`, `QUEUE_WORKER_TIMEOUT_DEFAULT` | worker behavior defaults | change generated worker runtime behavior |

Current detail:

- generated env exports both `RABBITMQ_USER` / `RABBITMQ_PASS` and `RABBITMQ_USERNAME` / `RABBITMQ_PASSWORD`
- local bootstrap provisions the declared RabbitMQ queues before workers start polling when `QUEUE_CONNECTION=rabbitmq`

### Redis

| Variables | Use for | Generated effect |
|---|---|---|
| `REDIS_HOST_DEFAULT`, `REDIS_PORT_DEFAULT`, `REDIS_CACHE_HOST_DEFAULT` | service-level fallback values | change generated host-side Redis fallbacks |
| `REDIS_RUNTIME_HOST_DEFAULT`, `REDIS_RUNTIME_CACHE_HOST_DEFAULT`, `REDIS_RUNTIME_PORT_DEFAULT` | container-side Redis runtime endpoints | change generated container-to-container Redis connection defaults |

Current detail:

- generated containers use `REDIS_RUNTIME_*` values for Docker-network access
- this lets service `.env` keep host-side values such as `REDIS_HOST=127.0.0.1`

### Compatibility Flags And Legacy Aliases

| Variables | Use for | Generated effect |
|---|---|---|
| `LEGACY_DB_BOOTSTRAP_SCRIPT_ALIASES` | keep older script names available | causes the renderer to emit compatibility alias scripts |
| `COMPAT_COMPOSE_ALIASES` | keep older compose file names available | causes the renderer to emit compatibility alias files |

## `runtime/secret-files.env`

| Variables | Use for | Generated effect |
|---|---|---|
| `RUNTIME_SECRET_FILES_ENABLED` | enable file-backed secret flow | generated secret helpers and compose mounts use file-backed secret behavior |
| `SECRET_BUNDLE_KIND` | identify the expected secret bundle pattern | informs the secret contract used by helpers and humans |
| `SECRET_LOCAL_DIR` | local secret directory | generated secret helpers read and write under this directory |
| `APP_KEY_FILENAME`, `PASSPORT_PRIVATE_FILENAME`, `PASSPORT_PUBLIC_FILENAME` | local filenames | change which files the helpers expect and mount |
| `APP_KEY_SOURCE_ENV`, `PASSPORT_PRIVATE_SOURCE_ENV`, `PASSPORT_PUBLIC_SOURCE_ENV` | env variable names that point to source files | change which source env vars the helpers read |
| `APP_KEY_SWARM_SECRET_ENV`, `PASSPORT_PRIVATE_SWARM_SECRET_ENV`, `PASSPORT_PUBLIC_SWARM_SECRET_ENV` | env variable names used for external Swarm secret names | change which env vars generated Swarm files reference |
| `APP_KEY_SWARM_SECRET_DEFAULT`, `PASSPORT_PRIVATE_SWARM_SECRET_DEFAULT`, `PASSPORT_PUBLIC_SWARM_SECRET_DEFAULT` | fallback external Swarm secret names | change generated default Swarm secret names |

## `runtime/env.*.extra`

These files are the right place for extra environment lines that do not justify changing the shared kit.

| File | Applied to |
|---|---|
| `runtime/env.common.extra` | app, worker, and scheduler |
| `runtime/env.app.extra` | app only |
| `runtime/env.worker.extra` | worker only |
| `runtime/env.scheduler.extra` | scheduler only |

These files are optional to use, but the latest bootstrap flow seeds them so developers can discover the extension points immediately.

## Hooks

The current kit supports these provisioning and migration hook stages:

- `before-provision`
- `after-provision-admin`
- `after-provision-db`
- `before-migrate`
- `after-migrate`

Use hooks for service-specific behavior. Do not fork generated helper scripts just to add a per-service command.

## Kit Version And Staleness

A stale kit emits correct-looking output for the wrong contract, so treat staleness as a first suspect.

- A repo-local `.service-runtime-kit` cache is not harmless: after a fix lands in the shared kit, a stale cache keeps reproducing the old behavior. Confirm which source the wrapper resolved before concluding the shared fix failed.
- Do not assume a variable present in `runtime/service.runtime.env` is consumed by the kit this service is pinned to. To check one, resolve the kit source in use and search that kit's renderer and templates for the variable name. A variable no template reads is dead configuration, and setting it changes nothing.

## Required `.env` Validation During Render

The current render flow fails early when required service `.env` values are missing.

At a minimum, expect validation of:

- `APP_NAME`
- `APP_ENV`
- `APP_DEBUG`
- `DB_CONNECTION`
- DB host, port, database, and username when the selected DB connection needs them
- `QUEUE_CONNECTION`
- RabbitMQ host, port, and one complete auth pair when `QUEUE_CONNECTION=rabbitmq`

If render fails on missing values, fix the service `.env` first. Do not patch generated outputs to bypass that validation.
