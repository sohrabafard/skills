# Buffers, scheduler and CPU topology

## Buffers, scheduler, CPU topology and memory

`tune.bufsize.small` defaults to 1024 bytes. HTTP/3 uses small buffers for response
headers; `option use-small-buffers` enables them on selected proxies and a full
buffer replaces one when necessary. `tune.bufsize.large` has no default activation;
setting it allocates three internal large buffers per thread at startup. It does
not enlarge every stream's header limit. Keep regular `tune.bufsize` and
`tune.maxrewrite` in the capacity analysis, including HTTP/2's buffer requirement.
Validate large headers, uploads, concurrent streams, allocation and RSS under load
and reload overlap before claiming memory savings.

3.4 adds `cpu-affinity` (`per-group`, `per-core`, `per-thread`, `per-ccx`) and
`cpu-policy ... threads-per-core {auto|1}`. Automatic topology uses the available
CPU set; `per-group` is the affinity default, with `per-core` when selecting one
thread per core without explicit affinity. `max-threads-per-group` bounds group
size. Inspect container cpusets, quotas, NUMA and NIC IRQ placement before changing
these; visible host CPUs do not establish available CPU time. Validate affinity,
run queues, p99 latency and throughput on the actual deployment shape.

`tune.sched.low-latency on` prioritizes lower-priority task classes at the cost of
bulk processing; default `off`. It predates 3.4, whose scheduler has additional
improvements. Do not describe it as a new 3.4 directive. Compare latency and bulk
throughput under the same saturation load. Process/container memory, descriptor
limits, stick tables, caches, TLS sessions and old workers still consume capacity;
route limit implementation to `/alaa-docker-production` or `/alaa-k8s-helm`.
