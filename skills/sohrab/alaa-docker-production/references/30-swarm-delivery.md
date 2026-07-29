# Swarm delivery and rollout control

Open this file when writing a Swarm stack file or diagnosing a rollout.

Swarm mode is current and supported: "Use Swarm mode if you intend to use Swarm as a production
runtime environment" (https://docs.docker.com/engine/swarm/, checked 2026-07-29). The discontinued
product is *Classic* Swarm, which is a different thing and is not what `docker stack deploy` uses.

The checker is `scripts/check-stack-rollout.mjs`. Its rule ids are used below.

---

## 1. The finding that motivates this file

`service-runtime-kit` v2.3.0 renders a stack file with four long-lived services and, across all
four: no `update_config`, no `rollback_config`, no `replicas`, no `placement`, no `reservations`,
no `stop_grace_period`, and exactly one `healthcheck` key whose value is `["NONE"]`
(`render-runtime.sh:1693-1697,1264-1265`). Run against that file:

```
$ node scripts/check-stack-rollout.mjs docker-compose.swarm.yml
docker-compose.swarm.yml:6: healthcheck-missing: service "platform-app-php" has no healthcheck...
docker-compose.swarm.yml:96: no-update-config: service "platform-app-php" has no deploy.update_config,
  so stack deploy uses order: stop-first, parallelism 1, failure_action: pause
...
25 finding(s)
```

What that means in production, stated as an arithmetic fact rather than a risk: with no `replicas`
the service runs one task; with no `update_config` the order is `stop-first`; therefore every
`docker stack deploy` stops the only task, waits for the new image to pull and the process to boot,
and only then has a serving container again. For an Octane service that is tens of seconds of hard
downtime **per service, per deploy**. For a fleet with a 99.99% target — 4 minutes 23 seconds of
unavailability per month, total — a handful of deploys exhausts the entire annual budget.

## 2. What `stack deploy` does when you say nothing

Defaults from the Compose Deploy Specification
(https://docs.docker.com/reference/compose-file/deploy/, checked 2026-07-29):

| Key | Default when absent | Consequence |
|---|---|---|
| `replicas` | 1 | One task. Nothing can be rolling. |
| `update_config.order` | `stop-first` | The old task is stopped before the new one starts. |
| `update_config.parallelism` | 1 | With one replica this is the whole service. |
| `update_config.delay` | 0s | Tasks are replaced back to back with no settling time. |
| `update_config.monitor` | 0s | A task that dies one second after starting counts as a success. |
| `update_config.failure_action` | `pause` | A bad image leaves the stack half-updated, indefinitely, with no alarm. |
| `rollback_config.order` | `stop-first` | The automatic rollback has the outage the update avoided. |
| `rollback_config.failure_action` | `pause` | A failing rollback also stops silently. |
| `restart_policy.delay` | 0s | A task that exits on start restarts as fast as the node can fork it. |
| `endpoint_mode` | `vip` | Correct for HTTP; see §6. |

Every one of those defaults is the wrong choice for a long-lived service in this fleet. That is not
a criticism of Docker: the defaults are conservative for a single-node development stack. They are
simply not the values a production stack wants, and silence selects them.

## 3. The rollout block, with values

```yaml
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        order: start-first
        delay: 10s
        monitor: 60s
        failure_action: rollback
        max_failure_ratio: 0
      rollback_config:
        parallelism: 1
        order: start-first
        delay: 5s
        monitor: 30s
        failure_action: pause
      restart_policy:
        condition: any
        delay: 10s
        max_attempts: 0
        window: 120s
      placement:
        max_replicas_per_node: 1
        constraints:
          - node.labels.tier == app
      resources:
        limits:      { cpus: "2.0", memory: 2G }
        reservations: { cpus: "1.0", memory: 1G }
```

Why each value, so it can be changed with an argument rather than copied:

- **`replicas: 3`, not 2.** `start-first` with `parallelism: 1` means one task is replaced at a
  time, so during a rollout `replicas - 1` tasks serve the old version and one serves the new. At
  two replicas a rollout runs the service at half capacity; at three it runs at two-thirds. Set it
  so that `replicas - 1` still carries peak traffic. A service that genuinely cannot run more than
  one task — a singleton scheduler — sets `replicas: 1` explicitly and accepts that its rollout is
  an outage, and says so in the merge request.
- **`order: start-first`.** The new task starts, passes its healthcheck, and only then is the old
  task stopped. This requires a healthcheck; see §4.
- **`parallelism: 1`** on any service with fewer than six replicas. Above that,
  `ceil(replicas / 4)` keeps the rollout from taking longer than the deploy window without
  replacing a quarter of capacity at once.
- **`delay: 10s`** between task groups. It exists so that a task which fails after warm-up — an
  OPcache-primed Octane worker that dies on its first real request — fails inside the rollout rather
  than after it.
- **`monitor: 60s`** is the window in which a task's death counts as a failed update. Set it longer
  than `start_period + interval * retries` from the healthcheck, or a container that is still
  starting is counted as converged. For the app values in this skill's
  `references/40-healthcheck-and-lifecycle.md` (`start_period: 45s`, `interval: 10s`,
  `retries: 3`), 45 + 30 = 75s, so `monitor: 90s` is the safer choice for the app and 60s suits a
  worker.
- **`failure_action: rollback`**, never `pause`. `pause` is a half-updated stack that nothing
  reports. `rollback` returns to the previous task spec automatically, and the deploy command's exit
  status tells the pipeline the truth.
- **`max_failure_ratio: 0`** on a service with three or fewer replicas: any failure is the whole
  rollout. At larger replica counts `0.1` tolerates one failing task in ten without rolling back a
  good deploy for one bad node.
- **`rollback_config.failure_action: pause`** is correct here and only here: a rollback that is
  itself failing must stop and wait for a human rather than loop.
- **`restart_policy.delay: 10s`** and `window: 120s`. Without a delay a task that exits at start —
  a missing queue, a bad credential — restarts continuously, which saturates the node and floods
  the logs. `service-runtime-kit/README.md:126` documents exactly this for `rabbitmq:consume`
  workers started against a queue that does not exist yet.
- **`max_attempts: 0`** means unlimited retries, which is correct with a delay and a window: a
  service that is down because a dependency is down must come back when the dependency does. It is
  wrong without a delay.
- **`placement.max_replicas_per_node: 1`** so three replicas are three nodes. Without it Swarm may
  place all three on one node and a node failure is a full outage with a replica count that looks
  healthy.
- **`resources.reservations`** so the scheduler will not place a task on a node that cannot run it.
  `limits` alone constrains the task and tells the scheduler nothing. Sizing is in this skill's
  `references/60-resource-limits-and-load.md`.

## 4. A rollout with no healthcheck is a timer

`start-first` means "start the replacement, wait for it to be healthy, then stop the old one".
With no healthcheck, "healthy" degrades to "the process has been executed", so the rollout advances
as soon as the container starts and before the application can serve anything. The outage is
shorter than `stop-first` but it is still an outage, and it is harder to see because the deploy
reports success.

Therefore: **`update_config` is only meaningful on a service that has a `healthcheck`.** Fixing the
rollout without fixing the probe produces a stack that looks configured and behaves almost as badly.
The checker reports both, and the order to fix them is probe first.

`healthcheck: test: ["NONE"]` is worse than an absent key, because it also disables any probe the
image declares. It has exactly one correct use: a service whose image ships a `HEALTHCHECK` that is
wrong for this deployment and that cannot be changed. In that case the stack file replaces the
probe rather than disabling it. The generated worker services carry `["NONE"]`
(`render-runtime.sh:1264-1265`) and there is no such inherited probe to suppress.

## 5. Compose versus stack: the divergence table

Read this before assuming a key you used in `docker-compose.yml` does anything in the stack file.

| Key | Compose | Swarm stack | What to do instead in Swarm |
|---|---|---|---|
| `build:` | builds the image | **ignored** | Build in the pipeline, deploy an immutable reference |
| `depends_on:` | orders start-up, supports conditions | **ignored** | Run bootstrap steps before `stack deploy`; make the service tolerate a missing dependency and retry |
| `restart:` | container restart policy | **ignored** | `deploy.restart_policy` |
| `container_name:` | names the container | **ignored** | Never use it in either |
| `profiles:` | selects what starts | **ignored** | Render a stack file that contains only what should run |
| `volumes:` bind mounts of repo files | works | **works per node, silently wrong** | Top-level `configs:` or `secrets:` |
| `env_file:` | read at container start | works, and the file must exist at that path on every node | Use `environment:` plus `configs:`/`secrets:`; `env_file:` is correct only when the same file is provisioned to every node by the node role |
| `ports: "127.0.0.1:9092:8000"` | binds the host loopback | long form only; `mode: ingress` publishes on **every** node | `mode: host` for a node-local bind; see this skill's `references/50-network-dns-and-exposure.md` |
| `deploy:` | only `resources` is honoured | the whole block is honoured | This is where every rollout key lives |
| `healthcheck:` | works | works, and gates the rollout | Required, per §4 |
| `stop_grace_period:` | works | works | Size it against the longest unit of work |
| `init: true` | works | works | Only when the process cannot reap children |
| `cap_drop`, `security_opt`, `read_only`, `pids_limit` | work | work | Same values as Compose |
| `logging:` | works | works | Same values as Compose |
| `secrets:` short form | reads `file:` | requires `external: true` or a `file:` on the manager | Long form with `uid`, `gid`, `mode` |
| `network_mode:` | works | **not supported** | Attachable overlay network |
| `extra_hosts:` | works | works | — |
| `sysctls:` | works | works (per-task) | See this skill's `references/60-resource-limits-and-load.md` |
| `ulimits:` | works | **ignored** | Set the limit in the image or via the daemon's `default-ulimits` |
| `privileged: true` | works | **not supported** | Do not; drop capabilities instead |

Two of these bite hardest in this fleet. The generated stack file has no `rabbitmq-provision`
service because bootstrap services are dropped, and `depends_on` would not have worked anyway, so
**every queue in `QUEUE_WORKER_QUEUES` must be declared before the stack is deployed** or
`rabbitmq:consume` workers crash-loop (`service-runtime-kit/README.md:126`). And `ulimits:` being
ignored is why the `nofile` discussion in this skill's `references/60-resource-limits-and-load.md`
lands on the image and the daemon rather than the stack file.

## 6. `endpoint_mode`, and when `dnsrr` beats `vip`

`vip` is the default and is correct for an HTTP backend: the service name resolves to one stable
virtual IP and Swarm's routing mesh load-balances connections across tasks. A proxy configured
against the service name keeps working as tasks come and go, which is the property this fleet
depends on.

`dnsrr` returns the task IPs directly, with no virtual IP. Use it in exactly two cases:

- The client does its own load balancing and needs to see individual endpoints — a gRPC client with
  connection-level balancing, or a database driver with a server list.
- The service must not be reachable through the routing mesh at all.

`dnsrr` cannot be combined with published ports in `ingress` mode. Writing `endpoint_mode: vip`
explicitly, as the generator does (`render-runtime.sh:1694`), asks for nothing that is not already
the default, but it is harmless and it documents the choice.

## 7. `configs:` — the Swarm replacement for a bind-mounted file

```yaml
services:
  pgbouncer:
    configs:
      - source: pgbouncer_ini_v4
        target: /etc/pgbouncer/pgbouncer.ini
        uid: "70"
        gid: "70"
        mode: 0440

configs:
  pgbouncer_ini_v4:
    file: ./docker/pgbouncer/pgbouncer.ini
```

- A config is immutable once created. Changing the file's contents requires a **new name**, which is
  why the name carries a version suffix. Redeploying with the same name silently keeps the old
  content, and the symptom is a configuration change that "did not take".
- Set `uid`, `gid` and `mode`. The default is root-owned `0444`, which is readable by every process
  in the container.
- A config is not a secret: it is stored in the Raft log unencrypted at rest in older engines and is
  readable through the API by anyone with manager access. Credentials go in `secrets:`; this skill's
  `references/35-secret-delivery.md` covers rotation, which for secrets has the same
  create-a-new-name shape.

## 8. Worked artifact — a Swarm stack file with real rollout control

This is the file the fleet should deploy. It is the generated stack file with the rollout,
placement, probe and hardening keys the generator omits.

```yaml
# docker-compose.swarm.yml
name: comment

services:
  platform-app-php:
    image: ${COMMENT_DOCKER_IMAGE:?set COMMENT_DOCKER_IMAGE to an immutable image reference}
    user: "1000:1000"
    read_only: true
    tmpfs: ["/tmp:rw,noexec,nosuid,size=64m"]
    security_opt: ["no-new-privileges:true"]
    cap_drop: ["ALL"]
    stop_grace_period: 30s
    environment:
      CONTAINER_MODE: app
      APP_ENV: ${APP_ENV:-production}
      APP_DEBUG: ${APP_DEBUG:-false}
      APP_KEY_FILE: /run/secrets/app_key
      DB_HOST: comment-pgbouncer
      DB_PORT: ${PGBOUNCER_LISTEN_PORT:-6432}
      DB_PASSWORD_FILE: /run/secrets/db_password
      RABBITMQ_HOST: ${RABBITMQ_HOST:-rabbitmq}
      RABBITMQ_PASSWORD_FILE: /run/secrets/rabbitmq_password
      OCTANE_WORKERS: ${OCTANE_WORKERS:-2}
      OCTANE_MAX_REQUESTS: ${OCTANE_MAX_REQUESTS:-1000}
    secrets:
      - { source: comment_app_key_v3,           target: app_key,           uid: "1000", gid: "1000", mode: 0400 }
      - { source: comment_db_password_v2,       target: db_password,       uid: "1000", gid: "1000", mode: 0400 }
      - { source: comment_rabbitmq_password_v2, target: rabbitmq_password, uid: "1000", gid: "1000", mode: 0400 }
    healthcheck:
      test: ["CMD", "/usr/local/bin/octane/healthcheck.sh"]
      interval: 10s
      timeout: 2s
      retries: 3
      start_period: 45s
      start_interval: 2s
    ports:
      - target: 8000
        published: ${APP_PORT_EXTERNAL:-9092}
        protocol: tcp
        mode: ingress
    logging:
      driver: json-file
      options: { max-size: "20m", max-file: "5" }
    deploy:
      replicas: 3
      endpoint_mode: vip
      update_config:
        parallelism: 1
        order: start-first
        delay: 10s
        monitor: 90s
        failure_action: rollback
        max_failure_ratio: 0
      rollback_config:
        parallelism: 1
        order: start-first
        delay: 5s
        monitor: 30s
        failure_action: pause
      restart_policy:
        condition: any
        delay: 10s
        max_attempts: 0
        window: 120s
      placement:
        max_replicas_per_node: 1
        constraints: ["node.labels.tier == app"]
      resources:
        limits:       { cpus: "${APP_CPU_LIMIT:-2.0}", memory: "${APP_MEMORY_LIMIT:-2G}" }
        reservations: { cpus: "1.0", memory: "1G" }
    networks:
      shared:
        aliases:
          - ${DOCKER_PROJECT_NAME:-comment}-platform-app-php
          - comment

  worker:
    image: ${COMMENT_DOCKER_IMAGE:?set COMMENT_DOCKER_IMAGE to an immutable image reference}
    user: "1000:1000"
    read_only: true
    tmpfs: ["/tmp:rw,noexec,nosuid,size=64m"]
    security_opt: ["no-new-privileges:true"]
    cap_drop: ["ALL"]
    command: ["php","artisan","queue:work","rabbitmq","--queue=${QUEUE_WORKER_QUEUES:-default}","--sleep=1","--tries=${QUEUE_WORKER_TRIES:-3}","--timeout=${QUEUE_WORKER_TIMEOUT:-90}"]
    # 30s beyond --timeout=90 so a job that hits its own timeout still releases
    # itself to the queue before SIGKILL. Sized against the longest unit of work,
    # not against a round number.
    stop_grace_period: 120s
    environment:
      CONTAINER_MODE: worker
      APP_KEY_FILE: /run/secrets/app_key
      DB_HOST: comment-pgbouncer
      DB_PASSWORD_FILE: /run/secrets/db_password
      RABBITMQ_PASSWORD_FILE: /run/secrets/rabbitmq_password
      QUEUE_WORKER_QUEUES: ${QUEUE_WORKER_QUEUES:-default}
    secrets:
      - { source: comment_app_key_v3,           target: app_key,           uid: "1000", gid: "1000", mode: 0400 }
      - { source: comment_db_password_v2,       target: db_password,       uid: "1000", gid: "1000", mode: 0400 }
      - { source: comment_rabbitmq_password_v2, target: rabbitmq_password, uid: "1000", gid: "1000", mode: 0400 }
    healthcheck:
      test: ["CMD", "/usr/local/bin/octane/worker-healthcheck.sh"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 60s
    logging:
      driver: json-file
      options: { max-size: "20m", max-file: "5" }
    deploy:
      replicas: 2
      update_config:
        parallelism: 1
        order: start-first
        delay: 15s
        monitor: 60s
        failure_action: rollback
      rollback_config:
        parallelism: 1
        order: start-first
        monitor: 30s
      restart_policy:
        condition: any
        delay: 15s
        window: 300s
      placement:
        max_replicas_per_node: 1
      resources:
        limits:       { cpus: "${WORKER_CPU_LIMIT:-1.0}", memory: "${WORKER_MEMORY_LIMIT:-1G}" }
        reservations: { cpus: "0.25", memory: "256M" }
    networks: [shared]

  # A scheduler is a deliberate singleton, so two rollout rules are waived here with their
  # argument written down. A waiver with no reason= is itself a finding.
  # rollout-waiver: scheduler update-order-stop-first reason=two schedulers would run every due job twice; the gap is bounded by start_period
  # rollout-waiver: scheduler no-replicas reason=replicas is set to 1 deliberately; see the update_config comment below
  scheduler:
    image: ${COMMENT_DOCKER_IMAGE:?set COMMENT_DOCKER_IMAGE to an immutable image reference}
    user: "1000:1000"
    read_only: true
    tmpfs: ["/tmp:rw,noexec,nosuid,size=32m"]
    security_opt: ["no-new-privileges:true"]
    cap_drop: ["ALL"]
    stop_grace_period: 60s
    environment:
      CONTAINER_MODE: scheduler
      APP_KEY_FILE: /run/secrets/app_key
      DB_HOST: comment-pgbouncer
      DB_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - { source: comment_app_key_v3,     target: app_key,     uid: "1000", gid: "1000", mode: 0400 }
      - { source: comment_db_password_v2, target: db_password, uid: "1000", gid: "1000", mode: 0400 }
    healthcheck:
      test: ["CMD", "/usr/local/bin/octane/scheduler-healthcheck.sh"]
      interval: 60s
      timeout: 5s
      retries: 2
      start_period: 30s
    logging:
      driver: json-file
      options: { max-size: "20m", max-file: "5" }
    deploy:
      # A scheduler is a singleton by design: two tasks would run every due job
      # twice. start-first would therefore overlap two schedulers, so this is the
      # one service in the stack that is deliberately stop-first, and its rollout
      # gap is bounded by start_period rather than hidden.
      replicas: 1
      update_config:
        parallelism: 1
        order: stop-first
        delay: 5s
        monitor: 60s
        failure_action: rollback
      rollback_config:
        parallelism: 1
        order: stop-first
        monitor: 30s
      restart_policy:
        condition: any
        delay: 10s
        window: 120s
      resources:
        limits:       { cpus: "${SCHEDULER_CPU_LIMIT:-0.5}", memory: "${SCHEDULER_MEMORY_LIMIT:-512M}" }
        reservations: { cpus: "0.1", memory: "128M" }
    networks: [shared]

networks:
  shared:
    external: true
    name: ${DOCKER_SHARED_NETWORK_NAME:-alaa-shared-network}

secrets:
  comment_app_key_v3:           { external: true }
  comment_db_password_v2:       { external: true }
  comment_rabbitmq_password_v2: { external: true }
```

The scheduler comment is the shape every deviation takes: name the constraint, name the alternative
you rejected, and state what bounds the cost.

## 9. Operating a rollout

```
docker stack deploy -c docker-compose.swarm.yml --with-registry-auth --prune comment
docker service ls --filter label=com.docker.stack.namespace=comment
docker service ps --no-trunc comment_platform-app-php
docker service inspect --format '{{json .UpdateStatus}}' comment_platform-app-php
docker service logs --since 10m --raw comment_platform-app-php
```

- `--with-registry-auth` sends the local registry credentials to the manager. Without it, worker
  nodes cannot pull from a private registry and tasks sit in `Pending` with no obvious cause.
- `--prune` removes services that are no longer in the file. Without it a service renamed in the
  file leaves the old one running forever.
- `UpdateStatus.State` is the authoritative answer to "did the deploy finish": `completed`,
  `updating`, `paused`, `rollback_completed`. A pipeline that runs `stack deploy` and exits has not
  waited for the rollout; poll this until it leaves `updating`.

| Symptom | Likely cause | Where |
|---|---|---|
| Deploy reports success, service was briefly down | `order: stop-first`, or no healthcheck so `start-first` did not wait | §3, §4 |
| Tasks stuck `Pending` | No node satisfies `placement.constraints`, or `reservations` exceed every node's free capacity | §3 |
| Tasks stuck `Preparing` | Image pull failing; `--with-registry-auth` missing or the digest is not on the mirror | §9, this skill's `references/45-registry-and-mirrors.md` |
| Rollout stopped half-way and nothing alerted | `failure_action: pause` (the default) | §2, §3 |
| Task restarts in a tight loop | `restart_policy` with no `delay`; often a missing queue or a bad credential underneath | §3 |
| A config change "did not take" | The `configs:` entry kept the same name | §7 |
| Jobs lost on every deploy | `stop_grace_period` shorter than the longest job, or PID 1 ignores SIGTERM | §8, this skill's `references/40-healthcheck-and-lifecycle.md` |
