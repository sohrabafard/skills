# Ingest shape and part pressure

## The ingest path on this fleet

Rows reach ClickHouse through the Vector topology in `wa`, not through application code.
`/vector-rust-observability-pipelines` `references/75-ala-ingest-pipeline.md` describes that
topology and owns its source, transform, buffer and sink semantics. This skill owns what the table
must be to receive the rows and what the write does to storage. Three properties of the topology
bind table design:

- **The table's column set is the transform's output contract.** The sinks set
  `skip_unknown_fields: true`, so a field the transform emits and the table does not declare is
  dropped with no error at either end. Change the transform and the DDL in the same effort, and
  prove the pair with the round-trip check in `80-proof-and-validation.md`.
- **A transform abort produces no ClickHouse row.** The source's success status cannot tell a
  delivered row from a dropped event. Look for missing data in Vector's internal logs and
  dropped-event routing.
- **Delivery is proved end to end.** Prove the source response and the database contents on success,
  on transform abort and on sink failure. Finalizer and acknowledgement semantics:
  `vector-rust-observability-pipelines` `references/30-buffers-acks-and-backpressure.md`.

**A service-side `INSERT` is a new ingest path.** A Go or PHP service that must record an event
posts it to the pipeline's source. A direct `INSERT` from a service needs the table owner's
ratification first, and then meets every rule in this file.

## Batch size and insert rate

| Quantity | Official guidance | This pipeline |
| --- | --- | --- |
| rows per insert | "at least 1,000 rows, and ideally between 10,000–100,000 rows" | `batch.max_events: 5000` per sink |
| insert queries per second | "around one insert query per second" | `batch.timeout_secs: 2` per sink for a partial batch; a full batch flushes sooner |
| bytes per insert | not prescribed | `batch.max_bytes: 10485760` |

Measure peak inserts per second, rows per insert and parts per partition under load. Full batches,
retries and concurrent requests raise the insert rate above what the timeout implies.

When an ingest path falls below 1,000 rows per insert, fix the path before you touch a table
setting. Use the first remedy that the path allows:

1. **Batch on the client or the collector.** Only this reduces both part count and merge CPU.
2. **Server-side async inserts,** when many independent producers each send small payloads. At the
   floor `async_insert` is on by default, so the server already buffers small inserts. Keep
   `wait_for_async_insert=1`: with `0` the server acknowledges before the data is durable, and the
   official text is "there's no guarantee the data will be persisted".
3. **A queue or collector in front,** when producers cannot coordinate and backpressure must stay
   away from them. The Vector topology has that role here.

Never raise `parts_to_throw_insert` to make a `TOO_MANY_PARTS` error stop. The error reports that
merges cannot keep up; a higher ceiling removes the report and keeps the cause.

## Retried inserts

An insert can reach the server before the client times out. The retry then duplicates the source
rows or leaves the rollups out of step with them.

- At the floor, insert deduplication and deduplication in dependent materialized views are enabled
  at query level by default. They act only inside the table's deduplication window.
- A `Replicated*` table has a window by default. A plain `MergeTree` table has none until the table
  sets `non_replicated_deduplication_window`. A query setting or a token cannot create a window the
  table lacks.
- Check that the writer's effective insert mode uses the window. A synchronous insert into a plain
  `MergeTree` table with a window deduplicated on the floor binary. An asynchronous insert into such
  a table is unverified (`90-source-map.md`), and async inserts are the default; prove it with the
  real writer or have the writer identity insert synchronously.
- Size the window to cover every insert into the table over the writer's whole retry horizon,
  buffered replay after an outage included. A retry that arrives after the window closed duplicates.
- A retry deduplicates only when it repeats the same rows in the same order, with the same block
  boundaries and the same insert settings. When the writer can send `insert_deduplication_token`,
  it reuses the token for the same logical insert and never for a new one.
- Prove it against the real writer, engines and settings: replay after a lost acknowledgement and
  after a partial failure of a dependent view. Assert the rows in the source and the aggregates in
  every view target.

Until that proof exists, treat the table as exposed to duplicates. On `wa` the owner accepted that
exposure for ingest (`15-fleet-clickhouse-boundary.md`); the table-side window stays the owner's
choice. Count logical events by a stable
event identifier where the measure is an event count; a sum and an already-written rollup row need
reconciliation or a bounded rebuild. File the table change with its owner
(`10-authority-and-change-path.md`).

## Part-pressure symptoms

| Symptom | What it tells you | First move |
| --- | --- | --- |
| `TOO_MANY_PARTS` on insert | merges are slower than inserts | measure rows per insert and inserts per second first |
| active part count rises at a steady insert rate | too many partitions, or merges starved of CPU or IO | count parts per partition, not per table |
| ingest latency spikes with no query load | the server delays inserts near `parts_to_delay_insert` | as in row one |
| query latency degrades only after write surges | reads scan many small unmerged parts | fix the ingest shape; add no index |
| disk grows faster than the row count | write amplification from mutations or oversized merges | `60-operations-and-diagnostics.md` |

Retry, timeout, and backoff doctrine for producers: `/alaa-reliability-sla`
`references/20-retries.md`. Idempotency-key design: `references/60-idempotency.md` in that skill.
