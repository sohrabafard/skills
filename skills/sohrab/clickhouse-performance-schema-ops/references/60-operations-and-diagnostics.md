# Operations and diagnostics

Start from a measurement, not a hypothesis. The queries below live in
`assets/templates/diagnostic_queries.sql`; run them and paste the result before proposing a change,
because a ClickHouse symptom has several causes that look identical from the outside.

## Where the evidence is

| Question | Table |
| --- | --- |
| what did this query actually read, and how long did it run | `system.query_log` |
| where did the time go inside one query | `system.query_thread_log` |
| how many parts exist, per table and per partition, and how big | `system.parts` |
| when were parts written, merged, or removed, and how long did merges take | `system.part_log` |
| is a mutation running, stuck, or failing | `system.mutations` |
| is a merge running right now and how much memory is it using | `system.merges` |
| is a replica behind, or is its queue growing | `system.replicas`, `system.replication_queue` |
| what is the effective value of a setting on this server | `system.settings`, `system.merge_tree_settings` |
| what does the deployed schema actually look like | `system.tables`, `system.columns` |

Note which of these are enabled before relying on them: `query_log`, `query_thread_log`, and
`part_log` are server-configured and can be off or truncated by retention. Establish that first, so
an empty result reads as "logging is off" rather than "nothing happened".

## Playbook: inserts are failing with `TOO_MANY_PARTS`

Entry condition: an insert returns the too-many-parts error, or part counts climb while the insert
rate is flat.

1. Count active parts per partition, not per table. A table with 40 partitions and 30 parts each is
   a partitioning problem; one partition with 900 parts is an insert-shape problem.
2. Measure rows per insert and inserts per second at the writer. Compare against the published bar
   in `30-ingest-and-parts.md`: at least 1,000 rows per insert, ideally 10,000–100,000, and around
   one insert per second.
3. If rows per insert is below the bar, fix the writer. That is the whole remedy in the large
   majority of cases.
4. If the writer is already batching well, check whether one insert is spraying across many
   partitions — an insert touching N partitions writes at least N parts. Narrow the partition key or
   the batch's key range.
5. Check `system.merges` and host CPU and IO before concluding that merges are starved rather than
   overloaded.
6. Only after 1–5 are answered, and with the owner's agreement recorded, consider merge-tree
   settings. Raising `parts_to_throw_insert` silences the report and keeps the cause.

## Playbook: a mutation is not finishing

Entry condition: a row in `system.mutations` with `is_done = 0` older than the time the owner
expected, or a non-empty `latest_fail_reason`.

1. Read `latest_fail_reason` first. A failing mutation retries forever and holds the queue.
2. Establish the blast radius: how many parts the mutation must rewrite, and how large they are. A
   mutation rewrites entire parts, so a one-column update on a 500 GB table is a 500 GB rewrite.
3. Decide with the table's owner whether to let it finish or to kill it. `KILL MUTATION` is a
   shared-system action: name the mutation, name who approved it, and record what state the table is
   left in, because a killed mutation leaves the table partly mutated.
4. Ask why a mutation existed. Recurring mutations mean the engine choice is wrong
   (`20-table-design.md` section 6) or the deletion mechanism is wrong
   (`50-mvs-projections-and-ttl.md`).

## Playbook: one query is slow

Entry condition: a named query exceeds the latency the owner expects, and you have its exact text.

1. Pull its `system.query_log` row and compute `read_rows / result_rows`.
2. Follow the four steps in `40-query-tuning-and-read-lane.md`, in order.
3. Prove the fix by re-running the query and comparing `read_rows` and `read_bytes`, not wall time.
   Wall time moves with cache state and with whatever else the cluster is doing; bytes read is the
   quantity the design controls.

## Playbook: disk is growing faster than rows

Entry condition: `sum(bytes_on_disk)` from `system.parts` grows faster than `sum(rows)` over the
same window.

1. Separate active from inactive parts. Inactive parts are retained for a configured period after a
   merge and are not a leak.
2. Look for mutation write amplification in `system.mutations` and `system.part_log`.
3. Look for a partition whose parts never merge to a large size — the too-many-partitions shape.
4. Check the compression actually achieved per column against what the types imply. A wide
   free-form `String` where a `LowCardinality(String)` belongs shows up here first.

## `OPTIMIZE FINAL` is not a performance fix

Verified against the official guidance: `OPTIMIZE FINAL` "forces ClickHouse to merge all active
parts into a single part", it **ignores** the roughly 150 GB merge-size safeguard, and it risks
"long merge times, memory pressure, or even out-of-memory errors". It also creates one oversized
part that is then hard to merge further, "potentially causing issues like duplicates accumulating
for a ReplacingMergeTree".

The only uses the official guidance sanctions are "finalizing data before freezing a table or
exporting". Outside those two, let background merges run.

Keep the two ideas apart, because they share a word and nothing else: query-time `FINAL` gives one
`SELECT` a deduplicated view of a collapsing or replacing engine and changes no stored bytes;
`OPTIMIZE TABLE … FINAL` rewrites the table on disk.

## Sharp edges that recur

- **`PRIMARY KEY` never enforces uniqueness**, and it is a sparse index over granules rather than a
  row-addressable structure. An answer that depends on uniqueness needs an engine, not a key.
- **A data-skipping index is not a secondary index.** It stores a summary per block and lets whole
  blocks be skipped; it cannot find rows, and it earns nothing when the values it summarizes are
  spread evenly across blocks.
- **A materialized view does not see `UPDATE` or `DELETE` on its source.** Any correction to the
  base table requires an explicit rebuild of the rollup.
- **A dropped column is not a dropped cost until parts merge.** Storage falls as merges rewrite
  parts, not at the moment of the `ALTER`.
- **`skip_unknown_fields` on the writer hides a schema mismatch.** The write succeeds and the column
  is empty (`30-ingest-and-parts.md`).

## Using community sources

Stack Overflow, GitHub issues, forum posts, and vendor blogs are legitimate for one purpose:
generating hypotheses about an observed failure. Before any of it becomes a recommendation, confirm
it against the official pages in `90-source-map.md` or against evidence from the cluster in front of
you, and cite which one confirmed it. Version-specific behaviour changes, and an accepted answer
carries no date the reader can see.
