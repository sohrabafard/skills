# Healthchecks, startup and shutdown

Open this file on any startup, readiness, probe or shutdown question.

The `HEALTHCHECK` instruction in the image is in this skill's
`references/10-dockerfile-authorship.md` §10; the Compose `healthcheck:` key that overrides it is
here. How a probe gates a rollout is in this skill's `references/30-swarm-delivery.md` §4.

---

## 1. The five options and what each decides

| Option | Compose key | Documented default | What it decides |
|---|---|---|---|
| `--interval` | `interval` | 30s | How often the probe runs once the container is past its start period. |
| `--timeout` | `timeout` | 30s | How long one probe may take before it counts as a failure. |
| `--start-period` | `start_period` | 0s | A grace window after start during which a failing probe does not count toward `retries`. |
| `--start-interval` | `start_interval` | 5s | How often the probe runs *during* the start period. Available from Docker Engine 25.0. |
| `--retries` | `retries` | 3 | Consecutive failures before the container is marked unhealthy. |

These defaults are long-established and are the values the engine applies when the Dockerfile
declares a `HEALTHCHECK` with no options. Both the Dockerfile reference and the Compose services
reference truncate before the option table in their current published form, so re-derive rather
than trust: build an image with a bare `HEALTHCHECK CMD ...` and read the effective values back
with

```
docker inspect --format '{{json .Config.Healthcheck}}' IMAGE
docker inspect --format '{{json .State.Health}}' CONTAINER
```

The second command also gives the last five probe results with their output and exit codes, which
is the fastest way to diagnose a flapping probe.

`start_period` is the option that matters most in this fleet and the one most often left unset. An
Octane application boots the framework, warms OPcache and caches configuration before it can serve;
with `start_period: 0s` the probe starts failing immediately, burns its three retries, and the
container is marked unhealthy during a completely normal start-up. Under `order: start-first` that
aborts the rollout of a perfectly good image.

`start_interval` is the companion: during the start period the probe runs every `start_interval`
rather than every `interval`, so a container that becomes ready in 12 seconds is detected at 12
seconds rather than at the next 30-second tick. Setting `start_period` generously and
`start_interval` short costs nothing and shortens every rollout.

## 2. A probe exercises the serving path

The rule: **a healthcheck answers "can this container do its job right now", and it answers it by
doing a small version of the job.** It does not ask the framework for its opinion of itself.

The fleet's current template does the opposite.
`service-runtime-kit/templates/generated/docker/octane/healthcheck.sh:13` runs
`php artisan octane:status` for the app role and `:16` runs `php artisan schedule:list` for the
scheduler. Both boot the whole Laravel framework in a new process on every probe. At
`interval: 10s` across three replicas that is a framework boot every 3.3 seconds, consuming the CPU
the container was given to serve requests with — and neither command proves the HTTP listener
accepts a connection, which is the only thing a load balancer cares about.

Four further constraints on a probe:

- **It must not mutate state.** A probe that writes a row, publishes a message or takes a lock runs
  hundreds of times an hour on every replica and becomes a load source and a source of false
  incidents.
- **It must not depend on a downstream that has its own availability.** A probe that queries the
  database marks the whole application unhealthy when the database is briefly slow, so the
  orchestrator kills healthy application containers during a database incident and turns a degraded
  system into an outage. Whether a service should degrade or refuse when a dependency is unavailable
  is `/alaa-reliability-sla` (`$alaa-reliability-sla`)'s decision; the probe simply must not be the
  thing that decides it by accident.
- **It must be cheaper than the work it protects.** Budget: under 50ms of CPU and no allocation
  beyond a few kilobytes.
- **It must have a timeout shorter than the interval.** `timeout` greater than `interval` overlaps
  probes and the container accumulates probe processes.

## 3. Values per role

### HTTP-serving application (Octane/Swoole, Node SSR)

```yaml
    healthcheck:
      test: ["CMD", "/usr/local/bin/octane/healthcheck.sh"]
      interval: 10s
      timeout: 2s
      retries: 3
      start_period: 45s
      start_interval: 2s
```

```sh
#!/bin/sh
# healthcheck.sh — app role. Opens a TCP connection to the listener and requests a
# route that touches no dependency. Proves the listener accepts connections and the
# HTTP layer answers, which is exactly what the load balancer needs to know.
set -eu
PORT="${OCTANE_PORT:-8000}"
exec /usr/bin/curl -fsS --max-time 2 -o /dev/null "http://127.0.0.1:${PORT}/healthz"
```

The route returns a fixed body and does not query the database, the cache or the broker. Where
`curl` is absent from the image, the equivalent without it:

```sh
exec /bin/sh -c 'exec 3<>/dev/tcp/127.0.0.1/'"${PORT}"' && printf "GET /healthz HTTP/1.0\r\n\r\n" >&3 && head -1 <&3 | grep -q " 200 "'
```

`interval: 10s` with `retries: 3` means an unhealthy container is detected within 30 seconds.
`start_period: 45s` covers framework boot plus OPcache warm-up on a cold node; measure it once with
`docker inspect --format '{{json .State.Health}}'` and set it to twice the observed time to healthy.

### Queue worker

```yaml
    healthcheck:
      test: ["CMD", "/usr/local/bin/octane/worker-healthcheck.sh"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 60s
```

```sh
#!/bin/sh
# worker-healthcheck.sh — worker role. A queue worker has no listener, so the
# liveness signal is a heartbeat file the worker touches at the top of each loop
# iteration. Stale beyond a threshold means the worker is wedged, not merely idle.
set -eu
BEAT="${WORKER_HEARTBEAT_FILE:-/tmp/worker.beat}"
MAX_AGE="${WORKER_HEARTBEAT_MAX_AGE:-120}"
[ -f "$BEAT" ] || exit 1
NOW=$(date +%s); THEN=$(stat -c %Y "$BEAT" 2>/dev/null || echo 0)
[ $((NOW - THEN)) -le "$MAX_AGE" ]
```

`MAX_AGE` is longer than the worker's longest single job plus its poll sleep, or a worker legitimately
busy on a long job is killed mid-job. With `--timeout=90` and `--sleep=1`, 120 seconds is the
smallest safe value.

**`test: ["NONE"]` on a worker is a defect, not an exemption.** It disables any probe the image
declares and leaves `restart_policy: condition: any` as the only failure detection in the system —
which detects a crash and cannot detect a wedge. A worker blocked on a dead AMQP channel is running,
consuming nothing, and reporting nothing, and that is the state a heartbeat probe exists to catch.

`["NONE"]` is correct in exactly one case: the image declares a `HEALTHCHECK` that is wrong for this
deployment and cannot be changed, and the deployment has no probe of its own to substitute. Write
the reason beside it.

### Scheduler

```yaml
    healthcheck:
      test: ["CMD", "/usr/local/bin/octane/scheduler-healthcheck.sh"]
      interval: 60s
      timeout: 5s
      retries: 2
      start_period: 30s
```

Same heartbeat shape as the worker, touched once per scheduler tick, with `MAX_AGE` at 120 seconds
for a one-minute tick. Do not use `php artisan schedule:list`: it proves the framework boots and
proves nothing about whether the scheduler loop is still running.

### Shared infrastructure

```yaml
  postgres:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_PROVISION_ADMIN_USERNAME:-postgres} -h 127.0.0.1"]
      interval: 10s
      timeout: 3s
      retries: 5
      start_period: 20s
  redis:
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
      start_period: 10s
  rabbitmq:
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "-q", "check_port_connectivity"]
      interval: 15s
      timeout: 10s
      retries: 5
      start_period: 60s
```

`rabbitmq-diagnostics -q check_running` boots the Erlang remote shell and takes seconds;
`check_port_connectivity` is the cheap form and is what a client actually needs. `start_period: 60s`
because a RabbitMQ node recovering a large mnesia table genuinely takes that long.

Shared-infra probes are not optional even though nothing scrapes them: `depends_on:
condition: service_healthy` cannot be satisfied without one, so an absent probe makes every
dependent service hang on `up`.

### One-shot job

No probe. Mark it, so "no healthcheck" is never ambiguous:

```dockerfile
# healthcheck-exempt: one-shot provisioning image; it exits, so there is no steady state to probe
```

## 4. Shutdown: the signal chain

When Docker stops a container it sends `STOPSIGNAL` (default SIGTERM) to PID 1, waits
`stop_grace_period` (default 10s), then sends SIGKILL, which cannot be caught.

Three things must be true for a graceful stop, and all three are needed:

1. **PID 1 receives the signal.** It is the container's main process, not a shell wrapping it. Exec
   form everywhere; `exec "$@"` at the end of an entrypoint. This skill's
   `references/10-dockerfile-authorship.md` §9 states the Dockerfile side.
2. **PID 1 handles the signal.** PID 1 has no default handlers: an unhandled SIGTERM to PID 1 is
   discarded. Octane and Laravel's queue worker install handlers; a bare `sh -c` loop does not.
3. **`stop_grace_period` is longer than the longest unit of work.** Not a round number — a
   derivation:

| Role | Longest unit of work | `stop_grace_period` | Why |
|---|---|---|---|
| HTTP app | longest request, bounded by the proxy timeout | 30s | Drain in-flight requests; a request still running after the proxy gave up has no reader |
| Queue worker | `--timeout` (90s in this fleet) | 120s | The job's own timeout plus 30s for the worker to release it back to the queue |
| Scheduler | longest scheduled task run inline | 60s | A due task started one second before the stop must finish or be released |
| Proxy | longest connection drain | 30s | Existing connections close; new ones go to another task |
| Shared infra (Postgres) | checkpoint | 60s | A SIGKILL mid-checkpoint forces crash recovery on next start |

A grace period that is too short is invisible: the container stops, the deploy succeeds, and the
only evidence is a job that was reserved and never completed. Verify with

```
time docker stop CONTAINER
```

If it takes exactly `stop_grace_period`, the signal was ignored — cause 1 or 2. If it takes
noticeably less, the process handled it.

## 5. `init: true`

```yaml
    init: true
```

Runs a minimal init process as PID 1, which reaps zombies and forwards signals. Use it when, and
only when, the container's main process spawns children it does not itself reap — a wrapper script
that backgrounds a helper, a tool that forks. It is not a substitute for correct signal handling: it
forwards the signal to the main process, which still has to act on it.

Do not add a full supervisor (`supervisord`, `s6`) to run several processes in one container. One
container, one process: with two, a healthcheck cannot say which one failed and a restart takes down
the one that was fine.

## 6. Diagnosing a probe

```
docker inspect --format '{{json .State.Health}}' CONTAINER | python3 -m json.tool
docker events --filter event=health_status --since 1h
docker service ps --no-trunc SERVICE          # Swarm: shows the task's error column
```

| Symptom | Cause | Fix |
|---|---|---|
| Unhealthy for the first minute, then healthy | `start_period` shorter than boot time | Set it to twice the observed time to healthy |
| Flaps between healthy and unhealthy under load | The probe competes with the workload, or `timeout` is close to the p99 probe latency | Make the probe cheaper (§2); raise `timeout` only after that |
| All replicas unhealthy the moment the database is slow | The probe queries a downstream | Remove the dependency from the probe (§2) |
| Container is `running` and serving nothing | No probe, or `test: ["NONE"]` | Add the role probe from §3 |
| `up` hangs on "waiting for dependency to be healthy" | The dependency has no `healthcheck:` | Add the infra probe from §3 |
| Rollout completes but requests fail | Probe passes before the app is ready — it checks the process, not the serving path | §2 |
| Jobs lost on every deploy | `stop_grace_period` too short, or PID 1 ignores SIGTERM | §4 |
| `docker stop` always takes exactly the grace period | Signal not reaching or not handled | §4, causes 1 and 2 |
