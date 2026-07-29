# Resource limits, worker sizing and OS tuning

Open this file when sizing a container, tuning a long-lived PHP or Node process, or diagnosing a
service that is slower or less stable under load than its resource allocation suggests.

Why a timeout, retry, backoff, circuit breaker, backpressure or degradation mechanism exists, and
what shape it takes, is `/alaa-reliability-sla` (`$alaa-reliability-sla`)'s decision. This file
states how the resulting numbers are expressed as container keys and process settings, and gives the
values this fleet uses.

---

## 1. `limits` and `reservations` do different jobs

```yaml
    deploy:
      resources:
        limits:
          cpus: "2.0"
          memory: 2G
        reservations:
          cpus: "1.0"
          memory: 1G
```

- **`limits`** is a ceiling enforced by cgroups on the running container. Exceeding the memory limit
  is an OOM kill by the kernel; exceeding the CPU limit is throttling, not an error, which is why
  CPU pressure shows up as latency rather than as a failure.
- **`reservations`** is what the scheduler guarantees. Without it, Swarm will place a task on a node
  with no capacity left and the task starts, competes, and performs badly with every metric
  reporting "running". `reservations` is absent from every generated service today.

Sizing rule: set `reservations` to the steady-state consumption you have measured, and `limits` to
the peak you are willing to pay for. A reservation equal to the limit wastes capacity; a reservation
of zero — which is what absence means — makes placement arbitrary.

Fleet defaults, which `service-runtime-kit` already carries as tracked values
(`README.md:113`, `contracts/service.runtime.env.example:40-47`):

| Role | `limits.cpus` | `limits.memory` | `reservations.cpus` | `reservations.memory` |
|---|---|---|---|---|
| Application (`platform-app-php`) | 2.0 | 2G | 1.0 | 1G |
| Queue worker (each) | 1.0 | 1G | 0.25 | 256M |
| Scheduler | 0.5 | 512M | 0.1 | 128M |
| PgBouncer | 0.5 | 256M | 0.1 | 64M |

Override the limits from the service `.env` with `APP_CPU_LIMIT`, `APP_MEMORY_LIMIT`,
`WORKER_CPU_LIMIT`, `WORKER_MEMORY_LIMIT`, `SCHEDULER_CPU_LIMIT`, `SCHEDULER_MEMORY_LIMIT`. Which
variables exist and what their tracked defaults are is `/service-runtime-kit-governance`
(`$service-runtime-kit-governance`)'s ground; the numbers above and the requirement to also set
`reservations` are this skill's.

Measuring, so a change is a correction rather than a guess:

```
docker stats --no-stream --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}'
docker inspect --format '{{.HostConfig.NanoCpus}} {{.HostConfig.Memory}}' CONTAINER
docker inspect --format '{{.State.OOMKilled}}' CONTAINER
```

`OOMKilled: true` on a container that "just restarted" is the answer to the whole investigation, and
it is the first thing to check when a container restarts with no error in its own logs.

## 2. The `nproc` trap

**A CPU quota does not change what `nproc` returns inside the container.** Docker's CPU limit is a
CFS quota — the process is throttled, not given fewer CPUs — so `/proc/cpuinfo`, `nproc`,
`swoole_cpu_num()`, `os.cpus().length` and Go's `runtime.NumCPU()` all report the *host's* core
count. On a 32-core node, a container limited to 2.0 CPUs still sees 32.

Every runtime that auto-sizes a worker pool from the core count therefore gets it wrong by an order
of magnitude, and the failure is not an error: it is a container that creates 32 worker processes,
each with its own memory, inside a 2G limit, and then either OOMs or thrashes.

Consequences, all mandatory rather than advisable:

- **`OCTANE_WORKERS` is set explicitly on every application service.** `service-runtime-kit` already
  does this (`OCTANE_WORKERS=${OCTANE_WORKERS:-2}`, `README.md:113,128`). The default of 2 matches
  `APP_CPU_LIMIT=2.0`. **When `APP_CPU_LIMIT` changes, `OCTANE_WORKERS` changes with it.** The two
  are one decision expressed in two places, and changing one alone is the defect.
- Sizing: `OCTANE_WORKERS = floor(APP_CPU_LIMIT)`, minimum 1. Swoole workers are single-threaded and
  CPU-bound per request, so more workers than CPU quota adds context switching without throughput.
- `OCTANE_MAX_REQUESTS=1000` recycles a worker after 1000 requests. This bounds the effect of a slow
  leak in a long-lived process: without it a worker that leaks 200 kB per request grows unbounded
  and the container is OOM-killed at an unpredictable time.
- Node: `NODE_OPTIONS=--max-old-space-size=<MiB>` set to roughly 75% of the memory limit, because
  V8's default heap is also sized from host memory. For a 1G limit that is 768.
- PHP-FPM, where used: `pm=static` with `pm.max_children = floor(cpu_limit) * 4` for an IO-bound
  workload, and `memory_limit * pm.max_children` must fit inside the container memory limit with
  25% headroom.
- Go: `GOMAXPROCS` set to the integer CPU limit, for the same reason.

Verifying inside a running container:

```
docker compose exec platform-app-php sh -c 'nproc; cat /sys/fs/cgroup/cpu.max; cat /sys/fs/cgroup/memory.max'
```

`cpu.max` reads `200000 100000` for a 2.0 CPU limit — quota over period. That is the number the
process should size itself from, and none of the runtimes above read it by default.

## 3. OPcache and JIT for a long-lived worker

An Octane worker keeps the framework in memory across requests, which changes what OPcache is for:
the file cache is populated once at boot and never needs revalidating.

```ini
; /usr/local/etc/php/conf.d/10-opcache.ini
opcache.enable=1
opcache.enable_cli=1

; The worker is long-lived and the code cannot change under it: the image is
; immutable. Revalidating on every include costs a stat() per file per request and
; buys nothing. This is the single highest-value setting in this file.
opcache.validate_timestamps=0

; Sized for a Laravel application with its dependencies. Below this, OPcache
; evicts and recompiles under load, which appears as random latency spikes.
opcache.memory_consumption=512
opcache.interned_strings_buffer=64

; A Laravel application plus vendor is typically 12k-18k files. Under the real
; count OPcache thrashes; the prime number is the hash-table size.
opcache.max_accelerated_files=32531

; The application is preloaded, so nothing is compiled during a request.
opcache.preload=/var/www/html/storage/opcache/preload.php
opcache.preload_user=www-data

; JIT. `tracing` is the mode that helps a long-lived process; 256M is enough for
; a Laravel codebase and the buffer is separate from memory_consumption.
opcache.jit=tracing
opcache.jit_buffer_size=256M

; Never on in production: it doubles compile work to detect a corruption that a
; read-only immutable image cannot develop.
opcache.consistency_checks=0
```

`opcache.validate_timestamps=0` is safe precisely because the container is immutable and read-only.
It is unsafe on a bind-mounted development tree, which is why the development Compose file overrides
it to `1`. Verify the setting took effect rather than assuming:

```
docker compose exec platform-app-php php -i | grep -E 'opcache\.(validate_timestamps|jit|memory_consumption|max_accelerated_files)'
docker compose exec platform-app-php php -r 'print_r(opcache_get_status(false)["opcache_statistics"]);'
```

`opcache_statistics.num_cached_scripts` close to `max_accelerated_files`, or a non-zero
`oom_restarts`, means the buffer is too small.

Octane-specific tuning beyond these settings — which extensions to load, how to structure a
long-lived application so state does not leak between requests, `octane:reload` semantics — is
`/alaa-octane-performance` (`$alaa-octane-performance`)'s subject.

## 4. `nofile` and the sysctls that matter

A Swoole or Node server holds one file descriptor per connection plus its own files. The default
`nofile` soft limit of 1024 is reached at roughly 900 concurrent connections and the failure is
`accept: too many open files`, which appears as connection refusals under load and nothing at all
below it.

Threshold with a number: **set `nofile` explicitly on any service expected to exceed 500 concurrent
connections, or any service whose observed peak descriptor count exceeds half the current soft
limit.** Measure it, do not assume:

```
docker compose exec platform-app-php sh -c 'ls /proc/1/fd | wc -l; cat /proc/1/limits | grep "open files"'
```

Values:

| Role | `nofile` soft | `nofile` hard | Why |
|---|---|---|---|
| Octane/Swoole application | 65535 | 65535 | One descriptor per connection plus the framework's open files |
| Node SSR | 65535 | 65535 | Same |
| Queue worker | 8192 | 8192 | A handful of connections; the limit exists to bound a descriptor leak |
| PgBouncer | 65535 | 65535 | One descriptor per client connection plus one per server connection |
| Scheduler | 4096 | 4096 | Lowest of the long-lived roles |

Where to set it, because Compose and Swarm differ:

- Compose: `ulimits: {nofile: {soft: 65535, hard: 65535}}` on the service.
- **Swarm ignores `ulimits:` entirely.** Set it in the image, or set `default-ulimits` in
  `/etc/docker/daemon.json` on every node:
  ```json
  { "default-ulimits": { "nofile": { "Name": "nofile", "Soft": 65535, "Hard": 65535 } } }
  ```
  This is host configuration and belongs in the node provisioning role, not in the repository.
  Whether it is applied through Ansible is `/ansible-generator` (`$ansible-generator`)'s
  ground; that the value is required is this skill's.

Sysctls, one per line with its reason. Change one at a time and record which one:

| Sysctl | Value | When it matters |
|---|---|---|
| `net.core.somaxconn` | 4096 | The accept queue. At the default 128 a burst of connections is refused before the server ever sees it. Set with the server's own backlog, which must be equal or lower. |
| `net.ipv4.tcp_max_syn_backlog` | 8192 | Half-open connections during a connection burst. |
| `net.ipv4.ip_local_port_range` | `10000 65535` | Outbound port exhaustion on a service making many short-lived downstream connections. |
| `net.ipv4.tcp_tw_reuse` | 1 | Reuse of TIME_WAIT sockets for outbound connections; pairs with the above. |
| `vm.overcommit_memory` | 1 | Redis specifically: without it a background save can fail on a fork. Host-level, not per-container. |
| `kernel.shmmax` | node-dependent | PostgreSQL shared buffers on a dedicated node. |

`sysctls:` in a service applies namespaced sysctls per task. `net.core.somaxconn` and the `net.ipv4`
entries are namespaced and can be set per service; `vm.*` and `kernel.*` are not and must be set on
the host.

```yaml
    sysctls:
      net.core.somaxconn: 4096
      net.ipv4.tcp_max_syn_backlog: 8192
```

## 5. Connection pool sizing against the container

PgBouncer sits between the application and PostgreSQL and its pool must be sized against both.

```
default_pool_size   = min( postgres max_connections * 0.8 / number_of_services , app_concurrency )
max_client_conn     = sum over services of ( replicas * OCTANE_WORKERS ) * 2
pool_mode           = transaction
```

- `pool_mode = transaction` returns a server connection to the pool at the end of each transaction,
  which is what makes a pool smaller than the client count possible. It forbids session-level state:
  prepared statements across transactions, session variables and advisory locks held between
  transactions all break. This is why the fleet sets `DB_PGSQL_DISABLE_PREPARES=true` on generated
  services.
- `max_client_conn` must exceed the total number of application workers or a worker blocks waiting
  for a client slot, which looks like database slowness and is not.
- A pool larger than PostgreSQL's `max_connections` moves the failure from PgBouncer, where it is a
  queue, to PostgreSQL, where it is a connection error.

The kit's tracked defaults are `PGBOUNCER_DEFAULT_POOL_SIZE_DEFAULT=50` and
`PGBOUNCER_MAX_CLIENT_CONN_DEFAULT=1000` (`contracts/service.runtime.env.example:95-96`). With three
app replicas at two Octane workers each, plus two workers and a scheduler, the client count is 9 and
1000 is generous; the number to check is `default_pool_size` against PostgreSQL's `max_connections`
divided across every service sharing the instance. Query and index shape, and whether a query should
hold a connection at all, are `/alaa-data-layer` (`$alaa-data-layer`)'s ground.

## 6. Complexity budgets

A container limit bounds resource use; it does not make a path scale. Whether a loop, query or
fan-out has a stated complexity bound as tenants, rows or events grow is
`/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`)'s decision, and a service
that has outgrown its design needs `/alaa-system-design` (`$alaa-system-design`) rather than a
larger `memory:` value. Raising a limit to fix a growth problem hides it until the next size up.

## 7. Diagnosing a load problem

| Symptom | First check | Section |
|---|---|---|
| Container restarts with nothing in its logs | `docker inspect --format '{{.State.OOMKilled}}'` | §1 |
| Latency rises with no CPU saturation on the host | CPU throttling: `cat /sys/fs/cgroup/cpu.stat` and read `throttled_usec` | §1, §2 |
| Memory climbs steadily and resets on restart | Worker recycling absent: `OCTANE_MAX_REQUESTS` unset | §2 |
| 32 worker processes in a 2-CPU container | `nproc` auto-sizing; `OCTANE_WORKERS` unset | §2 |
| Random latency spikes with no traffic change | OPcache thrashing: `opcache_get_status()` shows evictions | §3 |
| `accept: too many open files` | `nofile` at the 1024 default | §4 |
| Connections refused before the app logs anything | `net.core.somaxconn` at 128 | §4 |
| Application waits on the database, database is idle | PgBouncer `max_client_conn` or `default_pool_size` too small | §5 |
| Node process OOM-killed well under its heap size | `--max-old-space-size` sized from host memory | §2 |
