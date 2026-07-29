# Compose authorship

Open this file when authoring or reviewing any Compose file.

Swarm-specific keys and the divergence between a Compose file and a stack file are in this skill's
`references/30-swarm-delivery.md`. The interpolation form of every variable written into either is
in this skill's `references/25-fail-closed-interpolation.md`.

Verified against Docker Compose v5.3.1 (7 July 2026) and the Compose Specification, 2026-07-29.

---

## 1. File-level keys

```yaml
name: comment
```

- **`name:` is written; `version:` is not.** The top-level `version` property is obsolete: it is
  informative only, Compose warns when it is present, and Compose validates against the newest
  schema regardless of what it says
  (https://docs.docker.com/reference/compose-file/version-and-name/, checked 2026-07-29). A file
  carrying `version: "3.8"` is not pinned to anything; it is annotated with a number nothing reads.
- `name:` sets the project name and is exposed back to the file as `COMPOSE_PROJECT_NAME`. It is
  what container names, the default network name and the volume prefix are derived from, so
  changing it orphans existing volumes. Set it once; treat it as an identifier, not a label.
- The hyphenated `docker-compose` binary is gone. Every command in this skill is `docker compose`.

## 2. Service inventory and naming

A fleet Laravel service renders thirteen Compose services. They fall into four classes, and the
class decides which keys a service gets:

| Class | Services in the generated file | Long-lived | Gets a healthcheck | Gets `profiles:` |
|---|---|---|---|---|
| Application | `platform-app-php` | yes | yes | no |
| Background | `worker` or `worker-<queue>`, `scheduler` | yes | yes | no |
| Shared infra | `postgres`, `redis`, `rabbitmq`, `pgbouncer`, `adminer` | yes | yes | `infra` |
| Bootstrap and tooling | `db-provision`, `rabbitmq-provision`, `composer`, `vendor-sync` | no, they exit | no | `bootstrap`, `tools` |

Naming rules that are load-bearing rather than cosmetic:

- The HTTP-serving service key is `platform-app-php` and it holds the canonical DNS alias
  `<service>-platform-app-php`. Workers and schedulers never hold it. Why, and the alias mechanics,
  are in this skill's `references/50-network-dns-and-exposure.md`. The alias values themselves are
  `/alaa-services-contract` (`$alaa-services-contract`)'s register.
- A per-queue worker is `worker-<queue>` and the queue name must be usable as a Compose service-name
  suffix; the generator rejects a queue list containing a name that is not
  (`service-runtime-kit/README.md:122`).
- Container names are not set. A `container_name:` key makes the service unscalable — Docker refuses
  a second container with the same name — and breaks `docker compose up --scale`.

## 3. `profiles:` — what starts by default

A service with no `profiles:` key starts on every `docker compose up`. A service with one starts
only when that profile is requested. This is what keeps a `docker compose up` from starting a
one-shot provisioning job as a long-lived service.

```yaml
  db-provision:
    profiles: ["bootstrap"]
  adminer:
    profiles: ["infra", "tools"]
```

The rule with an observable condition: **a service gets a profile when starting it as part of the
default `up` would be wrong.** That is true for every service that exits (bootstrap, migration,
`composer`, `vendor-sync`), for every operator tool (`adminer`), and for shared infrastructure when
the host already runs a shared-infra project. It is false for the application, its workers and its
scheduler.

A service referenced by `depends_on` is started even when its profile is not requested, so a
bootstrap service that must run before the app can be both profiled and depended on.

## 4. `environment:` versus `env_file:` — what each reaches

| Key | Read at | Reaches Compose interpolation | Reaches the container | Visible in `docker inspect` |
|---|---|---|---|---|
| `environment:` | render time | it *is* the render output | yes | yes |
| `env_file:` | container start | **no** | yes | no (the file is read by the engine, the values appear in the container config) |
| `--env-file` / project `.env` | render time | yes | no, unless also named in `environment:` | n/a |

Three rules follow.

- **`environment:` is for values the container needs that differ from the host's.** In this fleet
  that is the Docker-network hostnames: the service `.env` legitimately carries
  `REDIS_HOST=127.0.0.1` for host-side tooling while the container must reach `redis`, so the
  generated `environment:` overrides it (`service-runtime-kit/README.md:108,110`). Anything that
  does not need overriding does not belong there.
- **`env_file:` is for the bulk of ordinary application configuration.** Listing forty application
  variables under `environment:` adds forty interpolation sites, each of which is a place to get
  the form wrong.
- **Neither key delivers a secret.** Both put the value in the container's environment, where
  `docker inspect`, `/proc/<pid>/environ` and any crash reporter that dumps the environment can
  read it. Secrets are file mounts; this skill's `references/35-secret-delivery.md` states the
  mechanism, and this skill's `references/25-fail-closed-interpolation.md` states which variables
  are affected.

## 5. `depends_on` and start order

The short form guarantees start order and nothing else — the dependency's container is running,
which for a database means the process has been executed, not that it accepts connections.

```yaml
    depends_on:
      postgres:
        condition: service_healthy
      db-provision:
        condition: service_completed_successfully
      redis:
        condition: service_started
```

- `service_healthy` requires the dependency to define a `healthcheck:`. Without one the condition
  can never be satisfied and `up` hangs until the timeout. This is the concrete reason a
  shared-infra service needs a probe even though nothing scrapes it.
- `service_completed_successfully` is the condition for a bootstrap job: the app waits for
  `db-provision` to exit 0.
- `restart: true` under a dependency restarts the dependent when the dependency is recreated, which
  is what you want for a service that caches a connection at boot.

**`depends_on` is a Compose-only key. Swarm ignores it entirely.** Everything ordering-related that
a stack file needs is in this skill's `references/30-swarm-delivery.md`; the practical consequence
is that a bootstrap step expressed as `depends_on` in Compose has no counterpart in the stack file
and must be run before the deploy.

## 6. Runtime hardening keys

These are the Compose-side half of always-loaded rule 2. The image-side half — `USER`, no package
manager in the final stage — is in this skill's `references/10-dockerfile-authorship.md`.

```yaml
    user: "1000:1000"
    read_only: true
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=64m
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    pids_limit: 512
```

- **`user:`** is set on every long-lived service. The image's `USER` is the default and this key is
  the enforcement: an image change cannot silently return the container to root. Today no generated
  app, worker or scheduler service sets it (`user:` appears only on the throwaway `composer` and
  `vendor-sync` services, `render-runtime.sh:1464,1470`), so whether the fleet runs unprivileged
  depends entirely on the ungoverned Dockerfile.
- **`read_only: true`** with an explicit writable set. For a Laravel service the writable paths are
  `/tmp` (tmpfs) and the `storage/` and `bootstrap/cache` trees, which are named volumes or bind
  mounts rather than tmpfs because their contents must survive a restart. The observable condition
  that permits omitting `read_only` is: the process writes to a path that is neither in `tmpfs:` nor
  a mounted volume and the path cannot be moved. Name that path in the merge request; "the app
  needs to write" is not that statement.
- **`cap_drop: [ALL]`** and then `cap_add` only for a capability with a named reason. A PHP or Node
  application server binding port 8000 or 3000 needs none: `NET_BIND_SERVICE` is required only
  below port 1024, which is why the fleet's containers listen on high ports and the proxy publishes
  80 and 443.
- **`security_opt: [no-new-privileges:true]`** is supported by both Compose and Swarm
  unconditionally. It stops a setuid binary inside the container from raising privileges, which is
  the escalation path that survives running as a non-root user.
- **`pids_limit`** caps process creation. Set it on any service that shells out; 512 is the fleet
  default for a PHP or Node service. It is a class-B register member: `0` means unlimited.

Today `security_opt`, `cap_drop`, `read_only`, `tmpfs` and `pids_limit` appear zero times in
`service-runtime-kit/scripts/render-runtime.sh`. Threat classification for a specific capability —
whether adding one back is acceptable — is `/alaa-security-review` (`$alaa-security-review`)'s
call; expressing the key is this skill's.

## 7. Volumes

```yaml
volumes:
  comment-storage-data:
    name: ${DOCKER_VOLUME_PREFIX:-comment}-storage-data
```

- A named volume for anything that must survive `down`; a bind mount only for a file the host owns
  and the container reads (a rendered config, a certificate).
- The volume's `name:` is set explicitly rather than left to the project-name prefix, because the
  prefix changes when `name:` at the top level changes and the data is then orphaned rather than
  deleted — the worst of both outcomes.
- A bind-mounted config file is mounted `:ro`. A container that can rewrite its own configuration
  can persist a change across restarts that no repository records.
- Swarm does not support bind mounts of repository files across nodes; the stack file converts them
  to top-level `configs:` (this skill's `references/30-swarm-delivery.md`).

## 8. Logging

```yaml
    logging:
      driver: json-file
      options:
        max-size: "20m"
        max-file: "5"
        compress: "true"
```

The default `json-file` driver has **no size limit**, so a service logging steadily fills the node's
disk and takes every other container on that node down with it. Every long-lived service sets
`max-size` and `max-file`. What the container should emit, and which signals are required, is
`/alaa-observability-soc` (`$alaa-observability-soc`)'s decision; see this skill's
`references/70-container-observability.md` for the boundary.

## 9. Worked artifact — a fleet Compose file

Reduced to one service of each class, with the environment blocks trimmed to the keys that carry a
rule. The full generated file for a Laravel service has thirteen services and the same shape.

```yaml
name: comment

x-app-common: &app-common
  image: ${COMMENT_DOCKER_IMAGE:?set COMMENT_DOCKER_IMAGE to the built image reference}
  restart: unless-stopped
  user: "1000:1000"
  read_only: true
  security_opt: ["no-new-privileges:true"]
  cap_drop: ["ALL"]
  pids_limit: 512
  tmpfs: ["/tmp:rw,noexec,nosuid,size=64m"]
  env_file: [".env"]
  logging:
    driver: json-file
    options: { max-size: "20m", max-file: "5" }
  networks: [shared]

services:
  # ---- application -------------------------------------------------------
  platform-app-php:
    <<: *app-common
    build:
      context: .
      dockerfile: Dockerfile
      target: runtime
      args:
        IMAGE_PROXY_PREFIX: ${PUBLIC_DOCKER_REGISTRY:-mirror.cdn.ir/}
        OCTANE_BASE_IMAGE: ${OCTANE_BASE_IMAGE:-registry.takhtenegar.ir/docker/octane-base:v1.3.1}
        COMPOSER_VERSION: ${DOCKER_COMPOSER_VERSION:-2.9.5}
        WWWUSER: ${WWWUSER:-1000}
        WWWGROUP: ${WWWGROUP:-1000}
        VCS_REF: ${CI_COMMIT_SHA:-unknown}
    environment:
      CONTAINER_MODE: app
      APP_ENV: ${APP_ENV:-production}
      APP_DEBUG: ${APP_DEBUG:-false}
      APP_KEY: ${APP_KEY:?APP_KEY is missing from the service .env; pass it with --env-file}
      # Container-network endpoints override the host-side values in .env.
      DB_HOST: comment-pgbouncer
      DB_PORT: ${PGBOUNCER_LISTEN_PORT:-6432}
      DB_PASSWORD: ${DB_PASSWORD:?DB_PASSWORD is missing from the service .env}
      REDIS_HOST: ${REDIS_RUNTIME_HOST:-redis}
      RABBITMQ_HOST: ${RABBITMQ_HOST:-rabbitmq}
      RABBITMQ_PASSWORD: ${RABBITMQ_PASSWORD:?RABBITMQ_PASSWORD is missing from the service .env}
      OCTANE_WORKERS: ${OCTANE_WORKERS:-2}
      OCTANE_MAX_REQUESTS: ${OCTANE_MAX_REQUESTS:-1000}
    ports:
      - "127.0.0.1:${APP_PORT_EXTERNAL:-9092}:8000"
    volumes:
      - comment-storage-data:/var/www/html/storage
    healthcheck:
      test: ["CMD", "/usr/local/bin/octane/healthcheck.sh"]
      interval: 10s
      timeout: 2s
      retries: 3
      start_period: 45s
      start_interval: 2s
    stop_grace_period: 30s
    depends_on:
      pgbouncer: { condition: service_healthy }
      redis: { condition: service_healthy }
      db-provision: { condition: service_completed_successfully }
    deploy:
      resources:
        limits: { cpus: "${APP_CPU_LIMIT:-2.0}", memory: "${APP_MEMORY_LIMIT:-2G}" }
        reservations: { cpus: "1.0", memory: "1G" }
    networks:
      shared:
        aliases:
          - ${DOCKER_PROJECT_NAME:-comment}-platform-app-php
          - comment

  # ---- background --------------------------------------------------------
  worker:
    <<: *app-common
    environment:
      CONTAINER_MODE: worker
      APP_KEY: ${APP_KEY:?APP_KEY is missing from the service .env; pass it with --env-file}
      DB_HOST: comment-pgbouncer
      DB_PASSWORD: ${DB_PASSWORD:?DB_PASSWORD is missing from the service .env}
      RABBITMQ_PASSWORD: ${RABBITMQ_PASSWORD:?RABBITMQ_PASSWORD is missing from the service .env}
      QUEUE_WORKER_QUEUES: ${QUEUE_WORKER_QUEUES:-default}
    command:
      - php
      - artisan
      - queue:work
      - rabbitmq
      - --queue=${QUEUE_WORKER_QUEUES:-default}
      - --sleep=1
      - --tries=${QUEUE_WORKER_TRIES:-3}
      - --timeout=${QUEUE_WORKER_TIMEOUT:-90}
    # 30s longer than --timeout, so a job that hits its own timeout still gets to
    # release itself back to the queue before SIGKILL arrives.
    stop_grace_period: 120s
    healthcheck:
      test: ["CMD", "/usr/local/bin/octane/worker-healthcheck.sh"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 60s
    depends_on:
      rabbitmq-provision: { condition: service_completed_successfully }
    deploy:
      resources:
        limits: { cpus: "${WORKER_CPU_LIMIT:-1.0}", memory: "${WORKER_MEMORY_LIMIT:-1G}" }
        reservations: { cpus: "0.25", memory: "256M" }

  # ---- bootstrap ---------------------------------------------------------
  db-provision:
    <<: *app-common
    profiles: ["bootstrap"]
    read_only: false          # writes the provisioning lock file
    restart: "no"
    environment:
      DB_PROVISION_ADMIN_USERNAME: ${DB_PROVISION_ADMIN_USERNAME:-postgres}
      DB_PROVISION_ADMIN_PASSWORD: ${DB_PROVISION_ADMIN_PASSWORD:?admin credential must come from the service .env}
    entrypoint: ["/bin/sh", "/var/www/html/scripts/docker/provision-postgres.sh"]
    depends_on:
      postgres: { condition: service_healthy }

  # ---- shared infra ------------------------------------------------------
  postgres:
    image: ${PUBLIC_DOCKER_REGISTRY:-mirror.cdn.ir/}postgres:18.3
    profiles: ["infra"]
    restart: unless-stopped
    security_opt: ["no-new-privileges:true"]
    environment:
      POSTGRES_USER: ${DB_PROVISION_ADMIN_USERNAME:-postgres}
      POSTGRES_PASSWORD: ${DB_PROVISION_ADMIN_PASSWORD:?admin credential must come from the service .env}
    ports:
      - "127.0.0.1:${POSTGRES_FORWARD_PORT:-15432}:5432"
    volumes:
      - alaa-shared-postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_PROVISION_ADMIN_USERNAME:-postgres} -h 127.0.0.1"]
      interval: 10s
      timeout: 3s
      retries: 5
      start_period: 20s
    logging:
      driver: json-file
      options: { max-size: "20m", max-file: "5" }
    networks: [shared]

volumes:
  comment-storage-data:
    name: ${DOCKER_VOLUME_PREFIX:-comment}-storage-data
  alaa-shared-postgres-data:
    name: alaa-shared-postgres-data
    external: true

networks:
  shared:
    external: true
    name: ${DOCKER_SHARED_NETWORK_NAME:-alaa-shared-network}
```

Note that `x-app-common` uses a YAML anchor. Compose supports anchors; the checkers in this skill
refuse them and exit 2 rather than guess, because an alias changes what a service contains and a
checker that ignored one would report "clean" on content it never read. Run
`docker compose config > /tmp/rendered.yml` outside the repository and check the rendered file, which
is what deploys anyway.

## 10. The delivery wrapper

One wrapper, not a page of commands in a README. `service-runtime-kit/scripts/up-local.sh` and the
copy it generates are the reference implementation and the rules they follow are these:

- One entrypoint per repository, `scripts/docker/up-local.sh <compose|swarm>`. Extra aliases such as
  `dev` or `prod` are permitted when each resolves to exactly one documented mode.
- **Fail fast on an unsupported mode.** Exit non-zero naming the modes that exist; never fall back
  to another mode.
- Create or reuse shared networks and shared infrastructure through idempotent steps only, so
  running the wrapper twice is indistinguishable from running it once.
- Validate the rendered model before acting: `docker compose config` plus the checkers in
  `scripts/`, then `up` or `stack deploy`. Exit 2 from a checker is not a pass.
- Compose mode may build locally where the repository allows it. Swarm mode deploys a prebuilt
  immutable image and a rendered stack file, and does not build: a build during `stack deploy`
  produces an image that exists on one node.
- Print the selected mode, the project or stack name, the image reference being deployed, and the
  result of every precheck. An operator reading the output must be able to answer "what is about to
  change" without reading the script.
- Refuse to run without the service `.env` unless an explicit acknowledgement variable is set to
  exactly `true`, and refuse before invoking Docker, because Compose renders required values as
  empty rather than failing. Shell script structure and portability are `/alaa-bash-shell`
  (`$alaa-bash-shell`)'s subject; the obligations above are this skill's.

## 11. Reviewing a Compose file

| Symptom | First check | Section |
|---|---|---|
| A value is empty in the container but set in `.env` | `docker compose config \| grep VAR` — interpolation does not read `env_file:` | §4, and this skill's `references/25-` |
| `up` hangs on "waiting for dependency" | The dependency has `condition: service_healthy` and no `healthcheck:` | §5 |
| A one-shot job is running as a long-lived service | It has no `profiles:` key | §3 |
| The node ran out of disk | `docker ps -q \| xargs docker inspect --format '{{.LogPath}}' \| xargs -r du -sh` | §8 |
| A container writes where you did not expect | `read_only: true` is absent; add it and read the failures | §6 |
| Volume data vanished after a rename | The volume had no explicit `name:` | §7 |
