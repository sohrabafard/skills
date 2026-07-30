# Ingest shape and part pressure

## The ingest path on this fleet

Rows reach ClickHouse through a Vector topology, not through application code. The shape, read from
`<repo>/vector/wa-vector.yaml` in `wa`, is:

1. An `http_server` source, `POST` only on a single strict path, returning `202`, which lifts three
   trusted headers set by the gateway: `X-Project-Id`, `X-User-Id`, `X-Request-Id`.
2. A `remap` that parses the envelope and **aborts** the whole batch when `X-Project-Id` or
   `X-Request-Id` is absent, when the body is not a JSON object, or when `envelope.events` is
   missing, non-array, or empty.
3. An `unnest` that emits one row per element of `envelope.events[]`.
4. A `remap` that flattens each row into exactly the column set of the target table and re-encodes
   the whole envelope plus the single event into `raw_payload`.
5. A `route` on `event_type`: `watch_segment` to `watch_segments_raw`, everything else to
   `events_raw` (`<repo>/docs/DECISIONS.md` section 4).
6. Two `clickhouse` sinks, `json_each_row`, `skip_unknown_fields: true`, gzip, disk buffer,
   acknowledgements on.

Three consequences bind table design, and each is checkable in the config:

- **The table's column set is the transform's output contract.** `skip_unknown_fields: true` means a
  field the transform emits that the table does not declare is dropped silently, with no error at
  either end. Adding a column to the transform without adding it to the DDL produces no failure and
  no data. Whenever one side changes, change both in the same effort and prove it with the
  round-trip check in `80-proof-and-validation.md`.
- **A rejected batch leaves no row anywhere.** The abort paths drop the batch after the source has
  already answered `202`, and no dead-letter sink is configured, so the only surviving record of a
  rejected batch is Vector's internal log stream. Treat "rows are missing for a period" as a
  question to answer from that log stream, not from ClickHouse.
- **The client never sees a write failure.** With `acknowledgements: enabled: true` and a blocking
  disk buffer, the `202` is the pipeline's promise to deliver, and sustained ClickHouse
  unavailability surfaces as backpressure and a filling buffer, not as an error to the caller.

Source, transform, buffer, and sink semantics themselves belong to
`/vector-rust-observability-pipelines` (`$vector-rust-observability-pipelines`). The boundary: that
skill owns what the pipeline writes and how it behaves; this skill owns what the table must be to
receive it and what the write does to storage.

## Batch size and insert rate

These are the officially published numbers; use them as the bar a proposed ingest shape must clear.

| Quantity | Official guidance | This pipeline |
| --- | --- | --- |
| rows per insert | "at least 1,000 rows, and ideally between 10,000–100,000 rows" | `batch.max_events: 5000` per sink |
| insert queries per second | "around one insert query per second" | `batch.timeout_secs: 2` per sink, so at most one insert per two seconds per sink, two sinks |
| bytes per insert | not prescribed | `batch.max_bytes: 10485760` |

Both sinks sit inside the recommended envelope, and the ratio matters more than either number
alone: a batch that flushes on the timeout rather than on `max_events` is a low-volume batch, and a
low-volume pipeline that inserts once per two seconds writes about 43,000 parts per table per day
before merges — well inside what background merging absorbs, but the number to recompute whenever
the timeout is shortened.

When a proposed ingest path falls below 1,000 rows per insert, fix the ingest path before touching
any table setting. The order of preference is fixed:

1. **Batch on the client or the collector.** Fewer, larger inserts is the only remedy that reduces
   both part count and merge CPU.
2. **`async_insert=1` with `wait_for_async_insert=1`,** when many independent producers each send
   small payloads and client-side batching genuinely cannot be arranged. The server buffers and
   flushes. Keep `wait_for_async_insert=1`: with `0` the server acknowledges before the data is
   durable, so "there's no guarantee the data will be persisted" and errors go undetected.
3. **A queue or collector in front**, when producer coordination is impossible and backpressure
   must be isolated from the producers. That is the role the Vector topology already plays here.

Never raise `parts_to_throw_insert` to make a "too many parts" error stop appearing. The error is
the merge subsystem reporting that it cannot keep up; raising the ceiling removes the report and
keeps the cause.

## Retries create duplicates on a non-replicated table

This is the sharpest edge in the current pipeline and it is a design fact, not a bug report.

- The sinks retry aggressively: `retry_attempts: 20`, `retry_max_duration_secs: 90`,
  `timeout_secs: 30`. A request that timed out on the client but committed on the server will be
  retried.
- ClickHouse deduplicates identical insert blocks by `block_id`, a hash of the block's data, but
  **"for `*ReplicatedMergeTree` engines, insert deduplication is enabled by default"** and it is not
  enabled by default for non-replicated engines; `non_replicated_deduplication_window` is the
  setting that turns it on.
- Both tables here are plain `MergeTree` (`<repo>/clickhouse/ddl/001_init.sql:150` and `:249`), and
  neither sets `non_replicated_deduplication_window`.
- The requirement this collides with is ratified, not hypothetical: `<repo>/docs/DECISIONS.md`
  section 29 states that counts and sums derived from `wa_raw` "must be exact" because watch time is
  sold and teacher contracts are priced on it. An upper bound over-bills.

So a retried insert against these tables inserts the rows again. Two properties follow that any
consumer of this data must satisfy, and a rollup that violates them is wrong rather than merely
imprecise:

- Count-style metrics computed with `count()` over raw rows are upper bounds, not counts. Use
  `uniqExact(event_id)` — the pipeline carries a per-event identifier for this purpose — wherever an
  exact count is claimed.
- A rollup materialized view over these tables inherits the duplication, because a materialized view
  fires per inserted block and re-inserting the block fires it again.

Three ways close it, and which are available depends on the topology rather than on preference:

1. **`non_replicated_deduplication_window` on the table.** The only one of the three available on a
   single node with no ClickHouse Keeper, which is this deployment today. It makes the server hash
   each inserted block and reject a repeat of the last N blocks, which is exactly the
   retry-after-success shape. Its bound is a count of recent blocks, not a span of time, so size it
   above the number of blocks that can be in flight across every sink at once, and note that it
   catches only a byte-identical replay — not two genuinely separate submissions of the same event.
2. **An `insert_deduplication_token` per batch,** so deduplication does not depend on the block hash.
   This needs the writer to mint and preserve a token across its own retries, which makes it a joint
   change with the pipeline owner rather than a table-only one.
3. **`ReplicatedMergeTree`,** the only variant where block deduplication is on by default. Blocked
   until ClickHouse Keeper exists and the shared-ClickHouse owner decides, and it is an engine change
   on populated tables rather than a settings flip (`10-authority-and-change-path.md`).

None of the three retroactively corrects rollup rows a materialized view already wrote from a
duplicated insert; that needs a bounded rebuild of the affected ranges, and it is not optional. Each
is a change to the ingest-pipeline repository, so it is filed as a request, not applied from here
(`10-authority-and-change-path.md`). Which skill owns which half of this decision:
`15-fleet-clickhouse-boundary.md`.

## Part-pressure symptoms and what each one means

| Symptom | What it is telling you | First move |
| --- | --- | --- |
| `TOO_MANY_PARTS` on insert | merges are slower than inserts | measure rows per insert and inserts per second before anything else |
| active part count rising with steady insert rate | too many partitions, or merges are CPU or IO starved | count parts per partition, not per table |
| ingest latency spikes with no query load | the merge subsystem is delaying inserts near `parts_to_delay_insert` | same as row one |
| query latency degrading only after write surges | reads are scanning many small unmerged parts | fix ingest shape; do not add indexes |
| disk growing faster than row count | write amplification from mutations or from oversized merges | `60-operations-and-diagnostics.md` |

Retry, timeout, and backoff doctrine for the producers themselves: `/alaa-reliability-sla`
(`$alaa-reliability-sla`) `references/20-retries.md`. Idempotency-key design:
`references/60-idempotency.md` in that same skill.
