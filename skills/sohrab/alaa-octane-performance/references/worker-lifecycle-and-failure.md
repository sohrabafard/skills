# Worker lifecycle, reload, and failure

## Workers hold the booted application

A worker holds the application it booted: your code, your service providers, environment
variables and configuration as they were at boot. **Changing any of them has no effect on a
running worker until `octane:reload`, a full restart, or a run started with `--watch`.** Use
`--watch` only in local development; it requires a file watcher and restarts on every write.

Consequence for debugging: a fix that "did not work" in a long-lived environment has usually
not been loaded. Confirm the reload happened before investigating the fix.

## `octane:reload` drain semantics and in-flight loss

`octane:reload` replaces workers; it does not restart the master, so the listening socket stays
open and no connection is refused.

- A worker finishes the request it is serving, then exits and is replaced. On Swoole a worker
  that is still running after `max_wait_time` is **force-killed**: the client receives a reset
  connection, not a response, and therefore not the error envelope owned by
  `alaa-services-contract references/10-core-service-contract.md`.
- Any request whose duration can exceed `max_wait_time` must be offloaded to a queue rather
  than served synchronously; otherwise every deploy drops some of them silently.
- Task workers are replaced by the same reload. Work in flight on a task worker is lost unless
  the job is idempotent and re-dispatchable — `/alaa-async-messaging` (`$alaa-async-messaging`).

## Crash, and crash-loop

An uncaught fatal — a PHP fatal error, exhausting `memory_limit`, a segfault in an extension —
terminates the worker process. The master respawns it, and **the request in flight receives no
response at all**. The observable is the worker-restart signal rising with no deploy
(`references/worker-observability.md`).

A worker that dies before serving its first request is a boot failure, not a leak. The two
common causes are a provider reading cache, sessions or Redis in `register()`/`boot()`, and a
PHP warning at request startup under FrankenPHP — both in `references/full-guide.md`.

## Memory-limit eviction — two different limits

- **PHP `memory_limit`** is per request inside the worker. Hitting it aborts that one request
  with a fatal and, because the fatal is uncaught, takes the worker with it.
- **The container memory limit** is per process tree. Hitting it has the kernel OOM-kill the
  process, destroying every in-flight request on that worker with no PHP-level trace.

`workers × PHP memory_limit` must stay under the container memory limit, with headroom for the
master and task workers. The container limit is declared per `/alaa-docker-production`
(`$alaa-docker-production`) and `/alaa-k8s-helm` (`$alaa-k8s-helm`).

`max_requests` recycles a worker **between** requests, so it never drops a request. It is the
last line of defence against slow accumulation, not a fix for a leak: a leak still serves wrong
data to every request before the recycle. Selecting its value:
`references/load-and-backpressure.md`.

## Swoole `max_request_execution_time`

Swoole kills a worker whose current request exceeds `max_request_execution_time`. Set it above
the service's request deadline, or it will kill requests the deadline would have permitted, and
the caller gets a reset connection instead of the timeout response. The deadline doctrine is
`/alaa-reliability-sla` (`$alaa-reliability-sla`); its value is in `alaa-services-contract
references/22-failure-load-and-deprecation-contract.md`.

## Graceful deploy sequence

1. Mark the instance not-ready so the load balancer stops sending new requests. The readiness
   shape is owned by `alaa-services-contract references/10-core-service-contract.md`.
2. Wait out the drain window — at least the longest synchronous request the service permits.
3. `octane:reload`, or replace the container.
4. Confirm new workers booted: the requests-served-per-worker signal restarts from zero and the
   worker-restart signal shows exactly the expected step.
5. Hold the previous image until per-worker RSS and latency-by-worker-age are flat
   (`references/worker-observability.md`).

Steps 1 and 2 are what make step 3 lossless. Running `octane:reload` without them converts
every request longer than `max_wait_time` into a dropped connection.
