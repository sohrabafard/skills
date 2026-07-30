# Table design: types, ordering, partitioning, engine

Read this before writing or reviewing a `CREATE TABLE`. Run `scripts/review_clickhouse_ddl.py`
against the result; it checks the mechanical half of the rules below and prints what it cannot
check.

## 1. Tenancy comes first, in the sort key and in every query

Put the tenant column first in `ORDER BY` on every table that holds rows for more than one tenant.
The pipeline on this fleet does exactly that and ratified it: `project_id` leads the sort key of
both raw tables (`<repo>/clickhouse/ddl/001_init.sql:157` and `:256`), and
`<repo>/docs/DECISIONS.md` section 3 gives the reason — "A project-first sort key aligns with the
main selective filter without carrying a duplicate mirror column in the MergeTree order."

Three obligations follow, and none of them is optional:

1. Every query against a tenant-scoped table carries an equality predicate on the tenant column.
   Without it the query reads every tenant's granules to answer one tenant's question, and the
   result is both slow and a cross-tenant read waiting for a bug in the application filter.
2. The tenant value comes from a trusted source, never from the request body. On this pipeline the
   value is the HAProxy-supplied `X-Project-Id` header, and `<repo>/docs/DECISIONS.md` section 5
   forbids deriving stored `project_id` from payload fields when the trusted header is missing.
3. Any table, view, or rollup that a request path reads is reviewed for tenant isolation before it
   ships: `/alaa-security-review` (`$alaa-security-review`)
   `references/40-authorization-and-tenancy.md`. ClickHouse has no row-level security in play here,
   so isolation is a property of the query and the grant, and both are reviewable artifacts.

## 2. Column types

Choose types before tuning anything else; a type mistake is paid on every read forever.

- Use the narrowest numeric type that holds the domain's maximum. A `UInt16` screen height and a
  `UInt64` screen height answer the same questions at four times the bytes.
- Use `LowCardinality(String)` for a string dimension with fewer than roughly 10,000 distinct
  values, which is the threshold in the official data-type guidance. Above that the dictionary
  stops paying for itself.
- Declare a column `Nullable(T)` only when a named query must distinguish "the producer sent no
  value" from "the producer sent the empty or zero value", and write that query's name in a comment
  on the column. Otherwise declare `T DEFAULT <empty value>`: `LowCardinality(String) DEFAULT ''`
  for a repeated string dimension, `String DEFAULT ''` for a free-form string, `UInt32 DEFAULT 0`
  for a count, `Float32 DEFAULT 0` for a measurement whose absence and zero mean the same thing to
  every reader. Official reason: a `Nullable` column "creates a separate column of `UInt8` type",
  "this additional column has to be processed every time a user works with a Nullable column", and
  it "leads to additional storage space used and almost always negatively affects performance".
- Compress a large opaque column explicitly. The raw event JSON on this pipeline is
  `raw_payload String CODEC(ZSTD(3))` (`<repo>/clickhouse/ddl/001_init.sql:148`), the right shape:
  one wide, rarely-filtered column carrying the provenance copy, compressed harder than the
  defaults because it is read far less often than it is written.
- Derive, do not duplicate. `event_time` and `event_date` on this pipeline are `MATERIALIZED`
  expressions over `event_ts_ms` (`:124-125`), so the partition key and the sort key cannot disagree
  with the stored timestamp.

### Finding in the pipeline's DDL, reported and not fixed

`wa_raw.events_raw` declares fifteen `Nullable(...)` columns and `wa_raw.watch_segments_raw` three
more, eighteen in total, one fewer than before because `<repo>/docs/DECISIONS.md` section 27 removed
the nullability of `network_save_data` alone; `scripts/review_clickhouse_ddl.py` lists every
remaining one with its line. Four of them — `device_os`,
`device_browser`, `network_effective_type`, `session_locale` — are repeated low-cardinality string
dimensions sitting within a few lines of `device_type LowCardinality(String) DEFAULT ''` and
`network_type LowCardinality(String) DEFAULT ''`, which solve the identical problem without the
null mask. The ingest transform already writes `?? null` for these fields and `?? ""` for their
neighbours, so the split is in the pipeline as well as the table. The replacement, whenever the
owning repository chooses to make it, is `LowCardinality(String) DEFAULT ''` on the table and `??
""` in the transform. This is reported to the owning repository under
`10-authority-and-change-path.md`; do not edit that file from this skill.

## 3. ORDER BY

The sort key decides what a query can skip. Build it in this order, and stop when the next column
earns nothing:

1. The tenant column, per section 1.
2. The column that excludes the largest fraction of rows in the most common query. On event data
   that is almost always the date or a coarse time bucket.
3. The dimensions the common queries filter on, most-excluding first. Columns correlated with data
   already in the key are worth more than uncorrelated ones because contiguous storage compresses
   better.
4. A tie-breaker only if rows must be uniquely ordered for a deduplicating engine.

Keep the key to five columns or fewer. The official primary-key guidance states that "4-5 [keys are]
typically sufficient". Beyond that, each extra column must be justified by a real query that filters
on it **and** on every column before it, because the sparse index prunes on a prefix: a filter on
the seventh column alone prunes nothing, and the column is then pure write cost and index memory.

A high-cardinality column near the end of the key is the common failure. If a column's distinct
count approaches the row count, it can only tie-break; it cannot prune unless every preceding
column is also constrained.

**Every dimension a rollup groups by belongs in that rollup's `ORDER BY`.** For
`AggregatingMergeTree`, `SummingMergeTree`, `ReplacingMergeTree` and every other merging engine the
sort key *is* the merge key, so two rows differing only in a `GROUP BY` column the key omits merge
into one row and their measures are combined. A filter on that column then answers wrongly in both
directions: rows that should match are gone, and the survivor carries measures belonging to values
it does not name. The one exception is a column functionally determined by a column already in the
key, and it is an exception only when the determination is **enforced in code on the write path** by
an allowlist or a rejection that a test covers. A comment asserting the invariant is not
enforcement, a naming convention is not enforcement, and a producer that copies the value from
client input enforces nothing.

### Finding in the pipeline's rollups, reported and not fixed

`object_type` is a `GROUP BY` dimension in all three content-grained materialized views
(`<repo>/clickhouse/ddl/002_agg.sql:110`, `:168`, `:289`) and appears in none of their target
`ORDER BY` clauses (`:78-80`, `:138-140`, `:261-263`). The DDL states the justification at `:55-58`
— "Functionally determined by content_id (one UUIDv7 belongs to exactly one object type)" — but no
step on the write path enforces it: `<repo>/vector/wa-vector.yaml:283-287` copies `object_type` out
of the client body with no allowlist and no rejection, so any non-empty string reaches the column.
A `WHERE object_type = 'news'` read over these rollups can therefore return an arbitrary survivor of
a merge across the discriminator, which is a wrong answer rather than an error. Either replacement
closes it: an allowlist on the ingest path that folds an unknown value to the default and counts it,
or `object_type` added to the three sort keys. Reported to the owning repository under
`10-authority-and-change-path.md`; not fixed from here.

### Finding in the pipeline's DDL, reported and not fixed

Both raw tables carry nine-column sort keys. `events_raw` is `(project_id, event_date, event_type,
content_id, set_id, course_id, play_id, event_time, event_id)`
(`<repo>/clickhouse/ddl/001_init.sql:157`):
the first three prune well, and the five members after `event_type` are high-cardinality
identifiers that prune only for a query already constrained on everything to their left. The
repository's own verification queries (`samples/verification_queries.sql`) group by `content_id`,
`set_id`, and `course_id` without constraining `event_type`, which is precisely the shape that
cannot use that tail. A shorter key plus a projection or rollup for the identifier-first access
path is the replacement; `50-mvs-projections-and-ttl.md` covers the choice. Reported, not fixed.

## 4. PRIMARY KEY

Leave `PRIMARY KEY` implicit — equal to `ORDER BY` — unless the sparse index is measurably large,
and then declare a prefix of `ORDER BY`. That keeps the full physical sort for compression while
shrinking the in-memory index. `PRIMARY KEY` in ClickHouse never enforces uniqueness; if an answer
depends on uniqueness, the mechanism is an engine choice in section 6, not the key.

## 5. PARTITION BY

Partitioning is a data-management tool, and the official partitioning guidance states it "is
primarily a data management technique and not a query optimization tool". Choose it for the
lifecycle operation you will actually perform — dropping a retention window, moving cold data,
detaching a range for export — and let `ORDER BY` do the pruning.

- Keep the total distinct partition count in the range the official guidance calls usually optimal:
  fewer than 100 to 1,000 distinct values.
- Never partition by a user, session, tenant, or event identifier. ClickHouse does not merge parts
  across partitions, so a high-cardinality key accumulates unmergeable small parts until an insert
  trips `parts_to_throw_insert` or `max_parts_in_total` and the ingest path starts failing.
- Monthly partitioning by event date is the pipeline's ratified choice
  (`<repo>/docs/DECISIONS.md` section 3, `PARTITION BY toYYYYMM(event_date)`): twelve a year stays
  far inside the recommended range and still allows a whole month to be dropped in one operation.
- Before changing a partition key, note that it cannot be altered in place. The change is: create a
  new table, move data, swap names. Budget it as a migration, not a tweak.

## 6. Engine

| Choose | When | Cost you accept |
| --- | --- | --- |
| `MergeTree` | rows are append-only and never corrected | none beyond merges |
| `ReplacingMergeTree` | a later row supersedes an earlier one with the same sort key, and readers tolerate seeing both until a merge runs | `FINAL` at read time, or an aggregation that is correct over duplicates |
| `CollapsingMergeTree` / `VersionedCollapsingMergeTree` | the producer already emits a sign, or a sign and a version, per row | the producer must never lose a cancelling row |
| `AggregatingMergeTree` | the table stores aggregate states written by a materialized view | every reader must use `-Merge` combinators |
| `SummingMergeTree` | the only aggregate anyone needs is a sum over a fixed key | any future non-sum aggregate needs a different table |

Deduplication that a table engine performs is eventual: it happens during background merges, on a
schedule nobody controls. If a reader needs exactly-once semantics at read time, that is `FINAL` and
its cost, or a rollup that is idempotent under duplicates — not an assumption that merges have run.

**When a writer retries, exactness is won or lost at the table, and the engine is what decides it.**
ClickHouse's insert deduplication ignores a repeated identical block, and it is enabled by default
only for the `Replicated*MergeTree` family. On a plain `MergeTree` a sink retry that follows an
insert which actually landed writes those rows a second time, and no retry, backoff or timeout
setting on the writer changes that. So a requirement that counts and sums be exact is a requirement
on the engine and the table settings, and "make the pipeline retry more carefully" is not an answer
to it. Which setting is available when `ReplicatedMergeTree` is blocked, and what a rollup inherits
from a duplicated raw insert: `30-ingest-and-parts.md`. Which skill decides which half of this, and
the fleet instance where the requirement and the engine currently disagree:
`15-fleet-clickhouse-boundary.md`.

`Replicated*` variants and what the single-node-to-cluster transition requires:
`10-authority-and-change-path.md`.
