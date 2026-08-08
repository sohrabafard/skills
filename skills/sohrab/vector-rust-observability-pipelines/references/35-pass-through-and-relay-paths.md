# Pass-through and relay paths

A path is usually called pass-through because it *currently* answers fast, not
because anything in the config keeps it that way. The property then disappears the
first time a buffer fills — which is the destination outage the buffer was bought
for. **Pass-through is a configured property or it is a coincidence.**

Verified against Vector `0.57.0`. Runtime observations in this file were made on
image `timberio/vector:0.57.0-alpine`, digest
`sha256:19e3526faf4d4b1ed0c28a0d68d4cc3a1e13e437099986a5b7a768707907497c`, build
`0.57.0 (x86_64-unknown-linux-musl 8832452 2026-07-14 20:58:30)`, on 2026-08-08.

## The mode, stated once

A **pass-through** (relay) path is one whose source must return immediately and
must never slow the upstream client that is sending to it. Two independent settings
decide it, and closing one of them leaves the path able to stall.

| Setting | What it decides | Standing of that statement |
| --- | --- | --- |
| `acknowledgements.enabled` reaching the source | Whether the **response** waits for durability: the source withholds its acknowledgement until every sink has confirmed | Documented upstream, recorded in `30-buffers-acks-and-backpressure.md`. Not measured here |
| `buffer.when_full` on any sink fed by that source | What a **full sink buffer** does. `block` waits for space, and backpressure propagates from there toward the source | Documented upstream, recorded in `30-`. Where it becomes visible to a client, and after how much traffic, is **not** established |

Two settings answering two questions, and a path claiming pass-through has answered
both. That much is safe to say.

**What is not safe to say, and an earlier revision of this file said it.** That
`when_full: block` reaches the client "regardless of acknowledgements"; that the
stall lands on the next request rather than on the current one. Neither was
observed, in either direction, and an attempt to force the stall point on 0.57.0
did not reach it — see the saturation attempt below. **Assert neither.** State the
mechanism, which is that a full blocking buffer propagates backpressure toward the
source, and stop there.

## Is this path pass-through? Five checkable conditions

All five, or the claim is an assertion:

1. **The source does not wait.** No `acknowledgements.enabled: true` on the source
   and none at top level. Sink-side acknowledgements alone do not make an
   `http_server` source hold the request open — observed below.
2. **No sink fed by this source can block.** Every one sets `when_full` to something
   other than `block`, or is provably unable to saturate within the outage duration
   the delivery contract states. `block` is the default, so writing no `buffer` block
   selects the single value that breaks pass-through.
3. **The fanout cannot stall it either.** Any *other* sink on the same source with
   `when_full: block` stalls the source, and therefore this path. Sink isolation is a
   topology decision — `10-topology-and-delivery-contract.md`.
4. **Headroom is stated as a duration — and the buffer block understates it.** The
   path must absorb the longest destination outage the contract tolerates. Start from
   the sizing arithmetic in `30-buffers-acks-and-backpressure.md`, then treat its
   answer as a **lower bound on the real queue depth**, not as the depth. The
   saturation attempt below found 198 events parked outside the sink buffer entirely,
   against a buffer configured to hold one. What actually queues is larger and less
   legible than any number in the `buffer` block.
5. **A monitor fires before the headroom is gone**, per the metrics below — and one
   gauge is not enough.

## What was observed

Two runs on 0.57.0, both on image `timberio/vector:0.57.0-alpine` at the digest
above.

### Run 1 — the `wa` topology with its destination unreachable

Config measured: the committed `wa` config **with two deviations**, without which it
does not start on 0.57.0 — `api.graphql` and `api.playground` deleted, and
`VECTOR_DANGEROUSLY_ALLOW_ENV_VAR_INTERPOLATION=true` set. Both deviations and their
exit codes are in `75-ala-ingest-pipeline.md` rule 4. Otherwise unchanged:
`acknowledgements.enabled: true` on both ClickHouse sinks, no `acknowledgements` key
on the `http_server` source, `when_full: block`, 4 GiB disk buffer, ClickHouse at an
unreachable address.

```
POST /ingest/v1/events   202 in 15 ms, then 4, 3, 3, 3, 3 ms   (six consecutive)
GET  /health (API port)  200 {"ok":true}                        (same run)
```

This settles condition 1: sinks acknowledging while the source does not still
returns immediately, so the durability configured on those sinks reaches no client.
It says nothing about `block`, because six requests against 4 GiB never approached
the buffer's limit.

### Run 2 — a topology built to reach the stall point, which did not reach it

`http_server` source → `http` sink at an unroutable address so the request genuinely
hangs; `buffer: {type: memory, max_events: 1, when_full: block}`,
`batch.max_events: 1`, `request.concurrency: 1`, `retry_attempts: 1000000`, and **no
acknowledgements anywhere**. 200 POSTs.

```
all 200 answered 202 in 1–6 ms — the source never stalled

relay_in  component_received_events_total = 200
relay_in  component_sent_events_total     = 200
stuck     component_received_events_total = 2
stuck     buffer_size_events              = 2   (buffer_max_size_events = 1)
component_discarded_events_total          = absent — nothing was dropped
```

**The stall point was not reached**, so this run establishes no client-visible
consequence of `block`. What it does establish is where the events went: 198 of them
sat between the source and the sink, outside the sink buffer, undropped and
uncounted by any buffer gauge. The sink buffer held 2 against a configured maximum of
1.

## The metrics that predict the moment it stops — plural

An earlier revision of this file called the buffer-utilisation ratio "the only signal
with lead time". **Run 2 falsifies that.** `buffer_size_events` read `2` against
`buffer_max_size_events` of `1` — already past its own maximum — while 198 events
were backed up upstream of it and the path was still answering in milliseconds. An
operator watching only that ratio sees a gauge that is both saturated and useless: it
described one small queue, not the backlog.

Watch both, and neither alone:

1. **Buffer utilisation** — `buffer_size_bytes / buffer_max_size_bytes` and the
   `_events` pair, with `source_buffer_utilization_mean` and
   `transform_buffer_utilization_mean` as the smoothed series. Alert on the ratio
   **climbing monotonically** across a window longer than the longest expected burst,
   not on a level.
2. **The source-to-sink differential** — `component_sent_events_total` at the source
   against `component_received_events_total` at each sink. In run 2 this is what
   showed the backlog: 200 out of the source, 2 into the sink. A widening gap is the
   backlog, wherever it is parked, and it does not depend on the queue being inside a
   buffer that reports itself.

`60-internal-monitoring.md` owns those names. Free bytes on the `data_dir` volume is
the third alert and is process liveness rather than a Vector metric — a disk buffer
that fills its volume stops Vector outright.

## What pass-through costs, in the delivery contract

**An immediate `202` is a receipt for *accepted for parsing*, not for *stored*.**
Everything between acceptance and the sink can still lose the event: a rollout, a
drain, an ephemeral buffer volume, a transform that aborts. Write that sentence into
the path's delivery contract in `10-topology-and-delivery-contract.md` in those
words, or the first person to read a `202` will read it as durability.

A path that cannot honestly carry that sentence is not a pass-through path. It is a
gate that has not been configured as one, and `75-ala-ingest-pipeline.md` states
what a gate owes its client instead.

## Two 0.57.0 controls that belong to this decision

| Control | Default | What it is |
| --- | --- | --- |
| `--chunk-size-events` / `VECTOR_CHUNK_SIZE_EVENTS` | `1000` events | Source-level event batching, added 0.57.0 |
| `--max-decompressed-size-bytes` / `VECTOR_MAX_DECOMPRESSED_SIZE_BYTES` | 100 MiB | Decompression-bomb mitigation across the HTTP-based, `logstash`, `fluent`, `vector` and `opentelemetry` sources, added 0.57.0 |

Those are the documented defaults and nothing more. **The release notes claim no
throughput effect for either, so do not supply one.** The decompression cap is a
rejection threshold, and on a relay accepting compressed bodies it is a new failure
mode: a legitimate sender above 100 MiB decompressed is refused.

## There is no Vector feature that does this for you

Across `0.54.0`–`0.57.0` no source-side never-block or backpressure-decoupling
capability is stated as new — no async-ack-then-drop mode, no `http_server`
non-blocking response option. All four release pages, the `/highlights/` index and
both upgrade guides in range were fetched. **UNCONFIRMED, and that means "not stated
as new", not "does not exist".** Infer neither direction from the silence.

Pass-through on 0.57.0 is built from the two settings above plus stated headroom.
The full capability inventory for the range is `82-capability-surface.md`.
