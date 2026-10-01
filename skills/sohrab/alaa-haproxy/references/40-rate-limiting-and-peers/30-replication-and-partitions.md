# Replication and partition enforcement

## Peers: what replication does and does not do

`12-peers-global-rate-limit.cfg` is the worked file and its header states the three preconditions.
This section states the mechanism.

### Peers replicate. They do not sum.

A node pushes an updated entry to its connected peers, and a receiving peer applies the received
value to its local entry. **There is no aggregation step.** The vendor's own product boundary
confirms it: HAProxy Enterprise ships a Global Profiling Engine whose entire purpose is the
summation that peers does not perform — it takes two requests seen on one balancer and three on
another and pushes the total of five to both. If plain peers summed counters, that module would
have nothing to do.

The threshold is enforced locally, not atomically across the cluster. Aggregate
admission depends on isolation, measurement windows, penalties and traffic
distribution; the partition bound below is not an unconditional multiplier.
State the assumed node count beside any per-node budget calculation.

### Partitions and approximate per-node arithmetic

During a partition each node counts local traffic; a client distributing requests
across N isolated nodes can approach N times a per-node threshold, subject to
measurement windows, bursts, penalties, table capacity and traffic distribution.
This is a planning bound, not an exact observed multiplier or a hard cluster quota.
Dividing an agreed cluster budget by node count is a conservative local setting;
replication still does not make enforcement atomic.

Inspect `show peers` for session state, heartbeat and acknowledged updates. A
partition is not reliably visible from request-rate panels alone. On reconnect,
current state is synchronized rather than an admission journal; concurrent updates
and expired entries prevent reconstructing a reliable global admitted-request total.
Test partition/reconnect with representative keys and measurement windows before
claiming limiter behavior. Signal/alert policy stays with `/alaa-observability-soc`.

### Deciding what to do about it

`alaa-haproxy` states the mechanical fact — a partition can approach the aggregate of isolated per-node
limits — and does not decide the response. Ask the discriminating question: **when this dependency
cannot answer, does proceeding without it let something through that must not get through?**

- If the limiter protects a backend from overload, the answer is availability. Degradation and
  fail-open doctrine are decided by `/alaa-reliability-sla`.
- If the limiter is the only control in front of a credential endpoint, the answer is yes,
  something gets through. Fail-closed doctrine is decided by `/alaa-security-review`.

### A stick-table limit with peers is a damper, not a quota

Concurrent updates can lose increments; partitioned nodes enforce independent
local limits under the window and penalty assumptions above. That
is enough to blunt abuse and it is not enough to enforce a contractual quota. **If the requirement
is a hard global quota, open-source HAProxy peers cannot provide it.** The requirement then needs
a shared counter store and a design, which is `/alaa-system-design`.
