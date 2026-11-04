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

## Prove retries at the source and every dependent view

An insert can reach the server before a client timeout. A retry can then duplicate the source
rows or leave its rollups out of sync. Check the target server's effective deduplication
settings, the base and target engines, and the count and time windows for every affected table.

- A replicated engine normally has a deduplication window. For plain MergeTree, check
  `non_replicated_deduplication_window` and whether the selected insert mode uses that window on this version. A query-level
  deduplication default or a token cannot create a disabled table window.
- ClickHouse 26.1 added async deduplication with dependent materialized views. In 26.3,
  async inserts and consistent sync, async, and dependent-view deduplication became defaults.
  Check the writer's effective settings and the server profile instead of inheriting those
  defaults on 24.8. For the hash transition and legacy startup guard, see `90-source-map.md`.
- Preserve the original row order and block boundaries across retries. If the writer can issue
  `insert_deduplication_token`, reuse the same token for the same logical insert and use a
  different token for every new insert. Size the window for all intervening writes over the
  retry horizon. An expired window or a retry with a changed block identity can duplicate rows.
- Keep async acknowledgement after flush with `wait_for_async_insert=1`. Prove retry after a
  lost acknowledgement and a partial dependent-view failure against the actual writer,
  engines, and settings. Assert rows in the source and aggregates in each destination.

The WA snapshot described here uses plain MergeTree without an explicit non-replicated
deduplication window. Preserve the duplicate risk until effective settings and replay proof
establish otherwise. Count logical events by stable event ID where the measure is event count.
Sums and already-written rollup rows require separate reconciliation or a bounded rebuild.
File schema changes with the owner in `10-authority-and-change-path.md`.

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
