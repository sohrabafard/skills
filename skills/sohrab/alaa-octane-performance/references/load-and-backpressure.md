# Load, backpressure, and worker sizing

## The worker count *is* the concurrency ceiling

One worker serves one request at a time. With N request workers the service can have N requests
in flight, and a single slow request occupies 1/N of total capacity for its whole duration. This
is why blocking a request worker on external IO is a capacity decision, not a latency detail.

Shedding, admission control and breaker doctrine are owned by `/alaa-reliability-sla`
(`$alaa-reliability-sla`), `references/40-admission-and-shedding.md`. Every value — shed
threshold, retry budget, acquire wait, pool bound — is in `alaa-services-contract
references/22-failure-load-and-deprecation-contract.md`, which already fixes the rule that
synchronous ingress sheds and asynchronous work queues. The Octane-specific consequence: beyond
the runtime's own accept backlog there is no application-level queue, and the accept backlog is
not one — a request sitting in it is consuming the caller's deadline with nothing working on it.

## Deriving the worker count from the CPU limit

**Reading host vCPU inside a CPU-limited container is an oversubscription incident.** `nproc`,
`/proc/cpuinfo` and `swoole_cpu_num()` report the host's cores, not the container's quota, so
`workers ≈ vCPU × 2` computed from them can start dozens of workers on a quota of one CPU. Read
the cgroup quota instead:

```bash
# cgroup v2
awk '{ if ($1 == "max") print "unlimited"; else print $1 / $2 }' /sys/fs/cgroup/cpu.max
# cgroup v1
echo $(( $(cat /sys/fs/cgroup/cpu/cpu.cfs_quota_us) / $(cat /sys/fs/cgroup/cpu/cpu.cfs_period_us) ))
```

Derive request workers from that number. Where the quota reports `unlimited`, the container has
no CPU limit and `nproc` is then correct. Task workers are derived the same way and are reduced,
not increased, when the database is the bottleneck. The limit itself is declared per
`/alaa-docker-production` (`$alaa-docker-production`) and `/alaa-k8s-helm` (`$alaa-k8s-helm`).

**Before raising any worker count**, re-check the connection-count ceiling in
`references/full-guide.md`. Worker count multiplies every per-worker connection.

## Selecting `max_requests` from a measurement

Do not pick a value from a range. Procedure:

1. Start with one worker and no recycle limit.
2. Drive the service at steady load and sample per-worker RSS against requests served
   (`references/worker-observability.md`, and the sampling command in
   `references/diagnostic-drills.md`).
3. If RSS is flat, there is no accumulation and `max_requests` exists only as a defence against
   a future regression; set it and record that RSS was flat.
4. If RSS rises linearly, the slope in bytes per request gives the request count at which a
   worker reaches its share of the container memory limit
   (`references/worker-lifecycle-and-failure.md`). Set `max_requests` below that count — and
   open a leak investigation, because a rising slope means an Invariant 2 violation exists.
5. Record the slope and the chosen count in the operations document
   (`references/full-guide.md`).

Change one knob at a time and re-measure. A knob changed together with a code change cannot be
attributed.

## Lock contention under long-lived workers

- A `Cache::lock` held across an external call blocks every other worker that wants it, so the
  effective concurrency for that path drops to one across the whole fleet. Critical sections
  cover a single atomic operation, never a workflow.
- A lock owner token is request state (Invariant 1): it is passed to a job as a value, never
  held on a singleton. Lock and rate-limiter mechanics, and their fail-open versus fail-closed
  decision, are owned by `alaa-data-layer references/50-redis-laravel-octane.md`
  (`/alaa-data-layer`, `$alaa-data-layer`).
- Row-level contention: see the read-modify-write prohibition in `references/full-guide.md`.
