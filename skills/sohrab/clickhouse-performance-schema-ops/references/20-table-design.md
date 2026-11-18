# Table design: types, ordering, partitioning, engine

Run `scripts/review_clickhouse_ddl.py` against every `CREATE TABLE` this file produces
(`80-proof-and-validation.md`). The checker covers the mechanical half of these rules and prints
what it cannot check.

## 1. Tenancy comes first, in the sort key and in every query

Put the tenant column first in `ORDER BY` on every table that holds rows of more than one tenant.
`<repo>/docs/DECISIONS.md` section 3 ratifies this for the pipeline, where the tenant column is
`project_id`. Three obligations follow:

1. Every query against a tenant-scoped table carries an equality predicate on the tenant column.
   Without it the query reads the granules of every tenant, and a bug in the application filter
   becomes a cross-tenant read.
2. The tenant value comes from a trusted source, never from the request body. On this pipeline it is
   the gateway-supplied `X-Project-Id` header. `<repo>/docs/DECISIONS.md` section 5 forbids deriving
   the stored `project_id` from a payload field when the header is missing.
3. Review every table, view, or rollup that a request path reads for tenant isolation before it
   ships: `/alaa-security-review` `references/40-authorization-and-tenancy.md`. No row policy is in
   use here, so isolation is a property of the query and the grant.

## 2. Column types

- Use `LowCardinality(String)` for a string dimension below about 10,000 distinct values, the
  threshold in the official data-type guidance.
- Declare a column `Nullable(T)` only when a named query must tell "the producer sent no value" from
  "the producer sent the empty or zero value". Write that query's name in a comment on the column's
  line that starts `nullable:`. Otherwise declare `T DEFAULT <empty value>`. Reason: a `Nullable`
  column stores a separate `UInt8` mask that every access must process.
- Change a nullable dimension in the table and in the ingest transform together. A transform that
  still emits `null` for a non-nullable column changes what the insert does.
- Give a wide opaque column an explicit codec, for example `CODEC(ZSTD(3))` on a raw payload column.
  Compare bytes and write CPU before you change an explicit codec.
- Derive a date or time column that a key uses with `MATERIALIZED` from the stored timestamp, so the
  partition key and the sort key cannot disagree with it.

## 3. ORDER BY

For a raw table, order for pruning. For an aggregate rollup, keep the full merge identity in
`ORDER BY` and tune the effective `PRIMARY KEY`. Choose index columns in this order:

1. The tenant column (section 1).
2. The column that excludes the most rows in the common query. For event data this is often time.
3. Other dimensions that common filters use.
4. A tie-breaker, only when the raw table needs it for merge or deduplication semantics.

Use five index columns or fewer. Justify each further column with a real query that constrains it
and every column before it. That evidence belongs to design review; it does not clear CH006 or raise
the checker's five-column limit. An identifier column in the tail prunes only for a query that
constrains every column to its left. Serve an identifier-first access path with a projection or a
rollup (`50-mvs-projections-and-ttl.md`).

**Every dimension a rollup groups by belongs in that rollup's `ORDER BY`.** On every merging engine
the sort key is the merge key. Two rows that differ only in a `GROUP BY` column the key omits merge
into one row, and their measures combine. A filter on that column then answers wrongly: matching
rows are gone, and the survivor carries measures of values it does not name.

To claim that a dimension is functionally dependent on the key, show that every write path enforces
a single value for each retained key, and test conflicting writes across producers and rebuilds. A
client-supplied field that the transform copies with no allowlist enforces nothing. The checker
requires every independently grouped dimension in `ORDER BY` and grants no dependency exemption.

Metadata-only `MODIFY ORDER BY` cannot add an existing column to the sort key or change the primary
key. A rollup that lost a dimension needs a rebuild: `80-proof-and-validation.md`.

## 4. PRIMARY KEY

An implicit `PRIMARY KEY` indexes all of `ORDER BY`. When the sparse index is large, declare a
leading prefix that the real read workload justifies. On an aggregating engine, keep the full merge
identity in `ORDER BY` when you shorten the index. Apply the five-column and identifier-tail rules
to the effective sparse index. Supply the target read SQL to the checker
(`80-proof-and-validation.md`). `PRIMARY KEY` enforces no uniqueness.

## 5. PARTITION BY

Choose the partition key for the lifecycle operation you will perform: dropping a retention window,
moving cold data, detaching a range. `ORDER BY` does the pruning.

- Keep the total distinct partition count inside what the official guidance calls usually optimal:
  fewer than 100 to 1,000 distinct values.
- Never partition by a user, session, tenant, or event identifier. Parts never merge across
  partitions, so such a key accumulates small parts until inserts fail on `parts_to_throw_insert`
  or `max_parts_in_total`.
- Monthly partitioning by event date is the pipeline's ratified choice
  (`<repo>/docs/DECISIONS.md` section 3, `PARTITION BY toYYYYMM(event_date)`). For a finer key, state
  the retention window and show that the window divided by the granularity stays under 1,000.
- A partition key cannot be altered in place. Changing it means a new table, a data move and a name
  swap. Budget it as a migration.

## 6. Engine

| Choose | When | Cost you accept |
| --- | --- | --- |
| `MergeTree` | rows are append-only and never corrected | none beyond merges |
| `ReplacingMergeTree` | a later row supersedes an earlier row with the same sort key, and readers tolerate both until a merge runs | `FINAL` at read time, or an aggregation that is correct over duplicates |
| `CollapsingMergeTree` / `VersionedCollapsingMergeTree` | the producer already emits a sign, or a sign and a version, per row | the producer must never lose a cancelling row |
| `AggregatingMergeTree` | the table stores aggregate states that a materialized view writes | every reader must use `-Merge` combinators |
| `SummingMergeTree` | the only aggregate anyone needs is a sum over a fixed key | a later non-sum aggregate needs a different table |

In `replicated` mode each row takes its `Replicated*` variant: `25-topology-and-replication.md`.

Row merging by an engine is eventual; it runs in background merges on no schedule you control. A
reader that needs deduplicated rows at read time pays for `FINAL`, or reads a rollup that is correct
over duplicates. Never assume that merges have run.

Row merging and insert deduplication are separate mechanisms. For insert retries, use
`30-ingest-and-parts.md`.

The floor rejects, at `CREATE`, a qualifying `AggregatingMergeTree` whose dimension is outside the
sorting key. The merge-tree setting `allow_dimensions_outside_sorting_key` controls the guard and is
off by default. Never enable it to make a `CREATE` pass. Verify its effective value on the target,
because a `compatibility` value below 26.7 restores the permissive behaviour. The guard rejects some
mistakes only; still review the full merge grain under section 3. See the
[guard implementation](https://github.com/ClickHouse/ClickHouse/pull/108087).
