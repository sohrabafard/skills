# Buffers, acknowledgements, and backpressure

A log pipeline that drops silently under load is an observability outage that hides
itself, which is the exact failure this skill exists to prevent. Everything in this
file exists to make the drop visible, chosen, and bounded.

Verified against Vector `0.57.0` on 2026-07-30. Re-derive with
`curl -s https://raw.githubusercontent.com/vectordotdev/vector/master/website/content/en/docs/architecture/buffering-model.md`
and `vector generate 'demo_logs//clickhouse'`, which prints the defaults the
installed binary actually applies.

## The defaults you get by writing nothing

An agent that writes no `buffer` block has still chosen a buffer. These are the
values it chose, from `vector generate` on 0.57.0:

| Setting | Default | Consequence of leaving it |
| --- | --- | --- |
| `buffer.type` | `memory` | Not durable. Everything in the buffer is lost on crash, restart, and rollout. |
| `buffer.max_events` (sinks) | `500` | Roughly half a second of headroom at 1,000 events/s. |
| `buffer.when_full` | `block` | Backpressure reaches the producing service. See the rule below. |
| `request.retry_attempts` | `9223372036854775807` | Effectively forever. A dead sink never surfaces as a terminal error. |
| `request.retry_initial_backoff_secs` | `1` | |
| `request.retry_max_duration_secs` | `30` | Ceiling on the backoff interval, not on total retrying. |
| `request.timeout_secs` | `60` | |
| `request.concurrency` | `adaptive` | Concurrency is discovered from observed latency, not pinned. |
| `healthcheck.enabled` | `true` | |
| `acknowledgements.enabled` | `false` | |

Every component pair also has an implicit in-memory channel of about 100 events,
independent of the sink buffer. Sinks get the larger 500-event default because
sinks are where backpressure originates: they talk to the network.

## `when_full` has three values, not two

### `block` — the default

Vector waits indefinitely for buffer space. This induces backpressure, which
propagates through transforms to the source and, for a push-based source, **to the
client that is sending the data**. That is the part that matters: `block` on a
telemetry path converts a ClickHouse outage into added latency on the producing
service's request path.

### `drop_newest`

Vector discards the incoming event when the buffer is full. Liveness is preserved
and the loss is deliberate.

**The caveat that makes this non-obvious.** Upstream states that `drop_newest` with
an in-memory buffer is *"not recommended for bursty workloads, where events arrive
in large, periodic batches"* because *"the buffer being immediately filled and the
remaining events being dropped, even when Vector appears to have available
processing capacity."* So `drop_newest` on the 500-event default buffer is not a
mild degradation under burst; it is a cliff. If a path must drop, size the buffer
for the burst first and then let it drop.

### `overflow`

Chains buffers into a **buffer topology**: two or more buffers in sequence, each
overflowing into the next, where the last must `block` or `drop_newest`. The
intended shape is an in-memory buffer for normal operation falling back to a disk
buffer during a sink outage, which is exactly the memory-latency-plus-disk-
durability trade-off that a two-value choice cannot express.

**Do not put it on a production path yet.** Upstream marks it with a danger
notice: *"Overflow buffers are not yet suitable for production workloads and may
contain bugs that ultimately lead to data loss."* Recommending `overflow` for a
high-SLA path would create the silent-drop failure this file exists to prevent.
Record it as the shape to adopt once upstream clears it, and re-check that notice
on every version bump; the pin and its re-derivation command are in
`80-version-and-upgrade-deltas.md`.

## Disk buffers: the numbers and the hard stop

- **`max_size` minimum is 268435488 bytes.** Observed on 0.57.0: `268435456`,
  which is exactly 256 MiB, is **rejected** with `parameter 'max_buffer_size' was
  invalid: must be greater than or equal to 268435488 bytes`. The documented
  "~256MiB" is not a safe value to write.
- `max_size` is honoured rigidly, so it can be used for capacity planning.
- On disk the buffer is append-only files capped at 128 MiB each, deleted once
  fully processed.
- Writes are checksummed. Corruption detected on read recovers as many events as
  decode cleanly and increments a corruption metric.
- Durability is **not** per-event: Vector fsyncs on a 500 ms interval, so up to
  ~500 ms of acknowledged-to-buffer events can be lost in a hard power failure.
- A disk buffer requires the global `data_dir` to exist and be writable.

**A full disk buffer stops Vector.** This is documented upstream behaviour, not a
field hypothesis: *"Vector will forcefully stop itself when an I/O error occurs
during flushing to disk"*, and *"If Vector cannot write to a disk buffer because
of a lack of free space, it must exit, as we can no longer be sure what data has
been written to disk or not."* Vector logs the cause, for example `no storage
space`, before exiting, and usually recovers the uncorrupted buffer on restart.

Two consequences an operator must plan for:

1. **Free space on the `data_dir` volume is a hard dependency of the process, not
   a soft one.** Alert on free bytes, not only on buffer utilisation. Vector exits
   at startup if the configured disk buffers could together exceed the volume, but
   it cannot detect another process consuming the same free space at runtime.
2. Sum `max_size` across every disk-buffered sink and keep the volume larger than
   that total, with headroom no other process can claim.

## Sizing a buffer instead of guessing

A buffer's job is to absorb a sink outage of some duration. State the duration, or
the number is arbitrary:

```
events_to_absorb = ingest_rate_events_per_sec * tolerable_outage_seconds
memory buffer:  max_events >= events_to_absorb
disk buffer:    max_size   >= events_to_absorb * avg_encoded_event_bytes
                             (and >= 268435488)
```

Both inputs are measurements, not estimates: `ingest_rate` comes from
`component_sent_events_total` and the encoded size from
`component_sent_bytes_total / component_sent_events_total`, both named in
`60-internal-monitoring.md`. If a throughput or batching bound needs deriving
rather than measuring, that belongs to `/alaa-algorithms-data-structures`
(`$alaa-algorithms-data-structures`), which owns complexity budgets and the
method for stating a bound.

## End-to-end acknowledgements

With `acknowledgements.enabled: true` a source withholds its own acknowledgement
to its upstream until every sink has durably handled the event.

**Not every source can acknowledge, and Vector says so at validate time.** A
`demo_logs` source with an acknowledging sink produces:

```
WARN vector::config: Source has acknowledgements enabled by a sink, but
acknowledgements are not supported by this source. Silent data loss could occur.
```

That warning is a finding, not noise — it means the durability the config appears
to buy does not exist. `scripts/check-vector-configs.mjs` runs with
`--deny-warnings` so this class fails the check rather than scrolling past.
Sources that do participate include `file`, `kafka`, and `aws_sqs`; `socket` does
not. Confirm the specific source before enabling acks.

**Fanout uses the worst status.** Upstream: *"If an event is sent to three sinks,
and is only processed successfully by two of them, we mark that event as having
failed which ensures it can be sent again"*, and *"Vector only notifies the source
once all copies of an event have been processed … the 'worst' status is the status
reported to the source."*

The consequence is concrete and is the reason to isolate paths: **one failing sink
in a fanout causes re-delivery to the sinks that already succeeded**, so a single
broken destination produces duplicates everywhere else. If a destination cannot
tolerate duplicates, it does not share an acknowledging source with a
less-reliable sink. Split the topology instead — see
`10-topology-and-delivery-contract.md`.

Acknowledgements also cost throughput, because the source cannot advance until the
slowest sink confirms. That is a real cost to state, not a reason to avoid them.

## What happens when ClickHouse is gone

This is the chain the whole skill exists to describe. With the 0.57.0 defaults and
a ClickHouse endpoint that stops answering:

1. The sink's request fails and retries, initially after 1 s, backing off to a
   ceiling of `retry_max_duration_secs` (30 s), for `retry_attempts` times — which
   defaults to `i64::MAX`, so **it never gives up on its own**.
2. Unacknowledged events accumulate in the sink buffer. With defaults that is 500
   events in memory: at 1,000 events/s the buffer is full in about half a second.
3. `when_full` now decides, and this is the only decision that changes the outcome:
   - `block` → backpressure reaches the source and then the producing client. The
     telemetry outage becomes a product-latency incident.
   - `drop_newest` → events are discarded from this moment until ClickHouse
     returns. Telemetry is lost; the product is untouched.
   - a disk buffer → durable for as long as free space lasts, and when the volume
     fills **Vector exits**, which is a total telemetry stop rather than a partial
     one.
4. `healthcheck.enabled: true` marks the sink unhealthy, which is visible in
   `vector top` and in the internal metrics, but does not by itself change
   delivery behaviour.

**The default configuration therefore blocks forever and retries forever.** Nothing
about that is announced; it is what writing no `buffer` and no `request` block
selects. Bound it deliberately: set `retry_attempts` to a finite number so a dead
sink becomes a reportable error, and choose `when_full` from the rule below.

## Choosing the policy: this skill does not decide it

The fleet has already decided, and this skill's job is to name the Vector option
that expresses that decision — not to re-open it.

`/alaa-observability-soc` (`$alaa-observability-soc`) states the requirement:
*"Telemetry is fail-open for product traffic: a failed backend, Collector, Vector
sidecar, or SOC destination degrades observability and never the hot path.
Fail-closed telemetry ships only on a written operator request."* SOC owns
requirement level, so this is binding and the mechanism must follow it.

| The path carries | SOC's requirement | The Vector option that expresses it |
| --- | --- | --- |
| Product application logs, metrics, traces | Fail open | `when_full: drop_newest`, sized for the burst. Never `block`. |
| Audit or SOC evidence, where losing a record leaves an action unrecorded | Fail closed, and only on a written operator request | Disk buffer, `when_full: block`, `acknowledgements.enabled: true`, an ack-capable source, and monitored free space |

**`block` on a product-telemetry path is a defect, not a trade-off.** It converts a
sink outage into a product outage, which is precisely what SOC's rule forbids.
Vector's own default is `block`, so this must be set explicitly on every such
path; the safe value is not the default one.

Boundaries, so this file is not read as the owner of things it is not:

- **Why a fail-open/fail-closed mechanism exists, and how to choose its shape in
  general:** `/alaa-reliability-sla` (`$alaa-reliability-sla`). It states no Ala
  number.
- **Every Ala value** — timeout, retry budget, burst allowance, tolerable outage
  duration: `/alaa-services-contract` (`$alaa-services-contract`)
  `references/22-failure-load-and-deprecation-contract.md`. Do not invent one here.
- **Whether telemetry is required at all, and at what gate:**
  `/alaa-observability-soc` (`$alaa-observability-soc`).
- **This skill owns only** which Vector option implements the chosen shape, and
  what the pipeline does when the sink is unreachable.

That is the third half of a boundary whose other two halves already exist:
reliability owns the reasoning, the services contract owns the numbers, and this
file owns the mechanism.
