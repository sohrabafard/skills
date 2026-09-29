# Symptom diagnosis

Open this procedure when the task matches its trigger. The topic map routes to this file.

## Diagnosing by symptom

### 502 or 503 in bursts

Look at `show stat` first: `econ` (connection errors), `eresp` (response errors), `qcur` (queue
depth) and `wretr` (retries) separate a backend that is down from a backend that is saturated.
Add `%[term_events]` to the log format when the counters do not distinguish them. Smallest first
step: confirm `option redispatch` is present, because without it a single failed server produces
this exact pattern. Escalate to `/alaa-reliability-sla` when the answer
is that the backend has no capacity, because that is a degradation decision, not a proxy one.

### Tail latency spikes with normal median

Look at rule count and regex cost on the hot path, then at queue depth (`qtime` in the log), then
at CPU. Smallest first step: move any repeated ACL chain to a map. Peer sync is a candidate only
when `peers` is configured and `show peers` shows recent activity. Escalate to
`/alaa-algorithms-data-structures` when the cost is in the
shape of the lookup rather than in its constant.

### Too many open files

The ceiling is the minimum of `global maxconn` implied descriptors, the process `RLIMIT_NOFILE`,
and the container or service-manager limit. All three must be raised together; raising one is the
usual reason this recurs after it was "fixed". Smallest first step: read `ulimit -n` inside the
running container, not on the host. Container limits are decided by `/alaa-docker-production` and `/alaa-k8s-helm`.

### Backends flapping in and out of rotation

Read `show servers state`. Resolver hold times shorter than the churn rate cause this; so does a
health check stricter than the backend's own startup. Smallest first step: raise `hold valid`
before raising `resolve_retries`, because retries lengthen the outage while hold length prevents
it. Escalate to `/alaa-system-design` when the backend's addresses change
faster than any hold time can absorb.
