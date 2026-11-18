# Rollups, alternate layouts, retention, and deletes

## Pick the cheapest mechanism that answers the question

Work down the table and stop at the first row whose condition the task meets. Each later row costs
more to build, to operate, or both.

| Mechanism | Use it when | It cannot |
| --- | --- | --- |
| a `MATERIALIZED` column | many queries recompute an expression that depends only on columns of the same row | change what a query can prune, unless it is also in the sort key |
| a data-skipping index | the sort key already prunes well and one more predicate needs block-level pruning | help a predicate that is not selective within a granule |
| a projection | one table needs a second physical ordering and no query may change | join, filter its own definition, chain, serve a `FINAL` query, or exist on a non-MergeTree engine |
| an incremental materialized view | rows must be reshaped, filtered, joined, or aggregated at insert time into a table you name | react to an `UPDATE` or `DELETE` on the source table |
| a new base table fed by its own route | two workloads need different sort keys, retention and columns | share storage; you maintain two ingest paths |

The pipeline took the last row once, on purpose: `<repo>/docs/DECISIONS.md` section 1 splits
`watch_segment` events into their own table. That is not the default.

## Materialized view versus projection

- Choose a projection when the base table's ordering is wrong for one access path and you cannot
  change it. The optimizer selects it and the server keeps it in step with the base table.
- Choose a materialized view when the shape of the answer differs from the shape of the row. Its
  target is a different table that the query must name. A correction to the source leaves the
  rollup wrong until someone rebuilds it.
- A projection blocks a lightweight `DELETE` by default: the floor's
  `lightweight_mutation_projection_mode` is `throw`.
- `ALTER TABLE … MODIFY PROJECTION` changes projection settings, and merges apply them lazily.
  Check the materialized parts and the optimizer's selection before you claim convergence.

## Building a materialized view

- A view fires on each inserted block, not on rows already present. The backfill is a separate,
  explicit operation.
- Pause and drain the source writers before you create the live view, and keep them paused until
  backfill and parity checks finish. For an online backfill, prove a disjoint boundary first: give
  the live view and the historical backfill complementary predicates, and account for in-flight and
  late rows. Compare counts and exact unique-event counts per rollup key on both sides of the
  boundary. Insert one batch at the boundary to catch double counting that a unique count hides.
- `CREATE MATERIALIZED VIEW … POPULATE` is atomic at the floor only for a snapshot-capable source
  and inserts through the same server, with `materialized_views_populate_atomically=1` in effect.
  Use an explicit backfill for a `Replicated` database, for remote inserts and for
  `CREATE OR REPLACE`.
- Declare the view's identity with `DEFINER = <user> SQL SECURITY DEFINER`. Grant that user `SELECT`
  on the source and `INSERT` on the target, and grant the migration identity `SET DEFINER` scoped to
  it where the server requires that. After the first apply and after every rerun, verify the stored
  clauses with `SHOW CREATE TABLE` and the effective grants, because `IF NOT EXISTS` leaves an older
  definition in place. Fail on drift and reconcile through an approved migration. Prove that the
  writer triggers the view and cannot write the target directly. Keep `SQL SECURITY NONE` out of
  fleet templates.
- A view over a table that is exposed to duplicate inserts inherits the exposure
  (`30-ingest-and-parts.md`). Until the base table deduplicates, write the aggregation to be correct
  over duplicates: `uniqExact` over the event identifier, not `count()`.
- Put the tenant column first in the sort key of every rollup a request path reads.
- Keep every independent grouping dimension in the target's merge key: `20-table-design.md`
  sections 3 and 6.
- In `replicated` mode the target is replicated too: `25-topology-and-replication.md`.

## TTL

**On the `wa` pipeline the retention decision forbids a TTL** (`10-authority-and-change-path.md`).
The rules below serve a pipeline whose owner ratified a policy that deletes or tiers data.

- `TTL … DELETE` removes rows during merges. Disk does not drop when the expression becomes true.
- `TTL … TO DISK` or `TO VOLUME` tiers data and needs a storage policy on the server first.
- A column-level TTL expires one column and keeps the row. It suits a wide provenance column better
  than deleting whole events.
- A TTL added to a populated table starts merges across the affected parts. Name the window in which
  that IO is acceptable in the change request.

## Deleting data

Use the first mechanism that fits; each later one costs more.

1. **`DROP PARTITION`.** It removes whole parts with no merge and no rewrite. This is why the
   partition key is a lifecycle decision (`20-table-design.md` section 5).
2. **Lightweight `DELETE`.** It marks rows through the hidden `_row_exists` column, and a later
   merge removes them physically. At the floor it waits for all replicas by default
   (`lightweight_deletes_sync=2`). It fails on a table with projections by default. A large
   lightweight delete slows `SELECT` until merges catch up.
3. **`ALTER TABLE … DELETE` or `UPDATE`, a mutation.** It rewrites every affected part, causes an IO
   spike and, in the official words, "can't be rolled back once submitted". Reserve it for a
   one-off correction with a named approver, and watch it in `system.mutations`
   (`60-operations-and-diagnostics.md`).

A workload that needs recurring corrections needs an engine change to `ReplacingMergeTree` or a
collapsing engine (`20-table-design.md` section 6), not a recurring mutation.
