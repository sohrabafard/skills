# Rollups, alternate layouts, retention, and deletes

## Pick the cheapest mechanism that answers the question

Work down this table and stop at the first row whose condition the task actually meets. Each row
below the first costs more to build, more to operate, or both.

| Mechanism | Use it when | It cannot |
| --- | --- | --- |
| a `MATERIALIZED` column | an expression is recomputed by many queries and depends only on columns of the same row | change what a query can prune unless it is also in the sort key |
| a data-skipping index | the sort key already prunes well and one extra predicate needs block-level pruning | help a predicate that is not selective within a granule |
| a projection | one table needs a second physical ordering, and you want the optimizer to pick it without any query changing | join, filter its own definition, chain, serve `FINAL` queries, or exist on a non-MergeTree engine |
| an incremental materialized view | rows must be reshaped, filtered, joined, or aggregated at insert time into a table you name | react to `UPDATE` or `DELETE` on the source table |
| a new base table fed by its own route | the two workloads want different sort keys, different retention, and different columns | share storage; you now maintain two ingest paths |

The pipeline on this fleet already took the last row deliberately: `docs/DECISIONS.md:5-11` splits
`watch_segment` events into their own table because "Segment workloads (heatmap/completion/rewatch)
are hot-path analytics and benefit from typed columns and dedicated sort order." Two tables with two
sort keys was the right answer there; it is not free, and it is not the default.

## Materialized view versus projection

Verified against the official comparison page:

- A projection is **"automatically selected by ClickHouse's query optimizer"** and is **"transparent
  in the sense that the user doesn't have to modify their queries"**. A materialized view's target
  table is a different table and the query must name it.
- A projection is **"automatically maintained and kept-in-sync"** with the base table. A
  materialized view **"doesn't automatically react to `UPDATE` or `DELETE` operations"** on the
  source, so a correction applied to the base table leaves the rollup wrong until it is rebuilt.
- Projections are **"only available for MergeTree family table engines"**, cannot be chained, and
  **"don't work with FINAL queries"**. They are also **"incompatible with `DELETED` rows (especially
  lightweight deletes)"** by default.
- Materialized views support `WHERE` filtering before materialization, joins, arbitrary target
  engines, and chaining — **"the target table of one materialized view can be the source for another
  materialized view, enabling multi-stage pipelines"**.

Choose a projection when the base table's ordering is wrong for one access path and you cannot
change it. Choose a materialized view when the shape of the answer differs from the shape of the
row.

## Building a materialized view without a self-inflicted incident

- A materialized view fires on each inserted block, not on rows already present. Creating it changes
  nothing about history; the backfill is a separate, explicit operation.
- Backfill by partition, oldest first, and verify each partition's totals against the source before
  starting the next. A single `INSERT … SELECT` over a full raw table is the memory failure everyone
  has already had.
- On this pipeline a materialized view over the raw tables inherits their duplicate exposure from
  retried inserts (`30-ingest-and-parts.md`), so build the aggregation to be correct under
  duplicates — `uniqExact` over the event identifier rather than `count()` — or fix deduplication on
  the base table first.
- Every rollup that a request path will read must carry the tenant column in its own sort key, for
  the same reason the base table does.

## TTL

**On this pipeline, retention is an open decision, not a missing feature.**
`clickhouse/ddl/001_init.sql:9` and `docs/DECISIONS.md:13-18` state "NO TTL by design (retention
policy is a later decision)", because retention "is a policy decision that should not be hardcoded
in bootstrap DDL" and omitting it "prevents accidental data deletion during early product
iteration". Do not add a TTL clause to a table on this pipeline. When a task raises retention,
produce the options and their consequences and hand them to the repository owner
(`10-authority-and-change-path.md`).

When a retention policy does exist, these are the mechanics it will use:

- A `TTL … DELETE` expression removes rows during merges, so deletion is eventual and disk does not
  drop at the moment the expression becomes true.
- A `TTL … TO DISK` or `TO VOLUME` expression tiers data instead of deleting it, and needs a storage
  policy defined on the server before the table can reference it.
- A column-level TTL expires one column's values while keeping the row, which suits a wide
  provenance column such as `raw_payload` far better than deleting whole events.
- Adding a TTL to a populated table triggers merges across the affected parts. Apply it during a
  window where that IO is acceptable, and state which window in the change request.

## Deleting data

In ascending cost, and the cheapest that fits is the right one:

1. **`DROP PARTITION`.** Whole parts are removed with no merge and no rewrite. This is the reason
   the partition key is a lifecycle decision (`20-table-design.md` section 5), and on a
   monthly-partitioned table it is the natural way to expire a month.
2. **Lightweight `DELETE`.** Verified: it "is implemented as a mutation that marks rows as deleted
   but does not immediately physically delete them", using a hidden `_row_exists` column, and the
   rows "will only happen during the next merge" to be removed physically. It is synchronous by
   default, it does not work on tables with projections by default, and "deleting large volumes of
   data with the lightweight `DELETE` statement can negatively affect `SELECT` query performance".
3. **`ALTER TABLE … DELETE` / `UPDATE` (a mutation).** Verified: mutations "rewrite entire data
   parts affected by the change", cause "a substantial spike in disk I/O", and "can't be rolled back
   once submitted". Reserve them for one-off corrections with a named approver, and watch them
   through `system.mutations` (`60-operations-and-diagnostics.md`).

When a workload needs recurring corrections, the answer is an engine change — `ReplacingMergeTree`
or a collapsing engine, per `20-table-design.md` section 6 — not a recurring mutation. The official
guidance is explicit: prefer "alternative table engines such as ReplacingMergeTree or
CollapsingMergeTree, which are designed to handle data corrections more efficiently".
