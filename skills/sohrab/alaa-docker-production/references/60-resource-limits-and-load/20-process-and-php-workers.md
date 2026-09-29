# 20 Process And Php Workers

When sizing process limits, PHP-FPM, OPcache, or JIT for workers, read this reference.

## 2. The `nproc` trap

CPU quota, CPU affinity and runtime concurrency are different measurements. Do not
size a pool from a host CPU count without checking the runtime version and its
container behavior. A quota can throttle execution without reducing an API's
logical-CPU count; an oversized pool can then waste CPU and memory.

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
- Go: Linux runtimes from Go 1.25 can derive default `GOMAXPROCS` from cgroup
  bandwidth and update it as limits change. An explicit `GOMAXPROCS` or relevant
  `GODEBUG` override disables this behavior. Check toolchain/module defaults and
  effective runtime settings before overriding it; route tuning to `/alaa-golang`.
  See [Go 1.25 runtime changes](https://go.dev/doc/go1.25#runtime), read 2026-09-29.

Verifying inside a running container:

```
docker compose exec platform-app-php sh -c 'nproc; cat /sys/fs/cgroup/cpu.max; cat /sys/fs/cgroup/memory.max'
```

`cpu.max` reads `200000 100000` for a 2.0 CPU limit — quota over period. That is the number the
runtime must account for. Confirm its effective setting rather than assuming every
runtime ignores cgroups or imposing a new consumer-version floor.

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
`/alaa-octane-performance`'s subject.
