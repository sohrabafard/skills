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
  one wide, rarely-filtered column carrying the provenance copy with an explicit codec.
  Since 26.9, implicit MergeTree column compression is size-dependent at write time. It
  can already be ZSTD(3) on large parts. Compare bytes and write CPU before changing an
  explicit codec. Check the upgrade caveats for extracted tuple subcolumns in
  `90-source-map.md` before changing the server version under existing keys or indexes.
- Prove the input format's effective null handling before changing a column type. In 26.10,
  `input_format_null_as_default=0` rejects JSON null for non-nullable numeric columns.
  `ALTER ADD/MODIFY COLUMN` now honors `data_type_default_nullable`; state the intended
  nullability and compare the resulting type on the target.
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

For raw tables, tune `ORDER BY` for pruning. For aggregate rollups, tune the effective
`PRIMARY KEY` and keep the full merge identity in `ORDER BY`. An implicit `PRIMARY KEY`
indexes the entire sort key. Choose index columns in this order:

1. The tenant column, per section 1.
2. The column that excludes the most rows in the common query. For event data, this is often time.
3. Other dimensions used in common filters. Correlated columns can also improve compression.
4. A tie-breaker only when the raw table needs it for its merge or deduplication semantics.

Use five index columns or fewer by default. Justify each additional index column with a real
query that constrains it and every preceding index column. Use that workload evidence in design
review. It does not clear CH006 or raise the checker's five-column limit. An identifier tail can only tie-break
when the query leaves earlier columns unconstrained. Keep merge dimensions even when they do
not earn sparse-index space.

**Every dimension a rollup groups by belongs in that rollup's `ORDER BY`.** For
`AggregatingMergeTree`, `SummingMergeTree`, `ReplacingMergeTree` and every other merging engine the
sort key *is* the merge key, so two rows differing only in a `GROUP BY` column the key omits merge
into one row and their measures are combined. A filter on that column then answers wrongly in both
directions: rows that should match are gone, and the survivor carries measures belonging to values
it does not name. To claim a functional dependency, show that every write path enforces a single
value for each retained key. Test conflicting writes across producers and rebuilds. Enum membership
or unknown-value folding can still admit two valid values for the same key. The checker requires
every independently grouped dimension in `ORDER BY` and grants no dependency exemption.

### Finding in the pipeline's rollups, reported and not fixed

`object_type` is a `GROUP BY` dimension in all three content-grained materialized views
(`<repo>/clickhouse/ddl/002_agg.sql:110`, `:168`, `:289`) and appears in none of their target
`ORDER BY` clauses (`:78-80`, `:138-140`, `:261-263`). The DDL states the justification at `:55-58`
— "Functionally determined by content_id (one UUIDv7 belongs to exactly one object type)" — but no
step on the write path enforces it: `<repo>/vector/wa-vector.yaml:283-287` copies `object_type` out
of the client body with no allowlist and no rejection, so any non-empty string reaches the column.
A `WHERE object_type = 'news'` read over these rollups can therefore return an arbitrary survivor of
a merge across the discriminator. Include `object_type` in all three merge keys. Metadata-only
`MODIFY ORDER BY` cannot add that existing column to the sort key or change the primary key.
The schema owner selects a rebuild or replacement and proves recovery under
`80-proof-and-validation.md`. See the [ALTER ORDER BY contract](https://clickhouse.com/docs/reference/statements/alter/order-by).

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

An implicit `PRIMARY KEY` indexes all of `ORDER BY`. If the sparse index is large, declare a leading
prefix justified by the real read workload. For aggregating engines, keep the full merge identity in
`ORDER BY` when shortening the index. Apply the key width and identifier-tail checks to the effective
sparse index. Supply the target read SQL to the checker as specified in `80-proof-and-validation.md`.
ClickHouse `PRIMARY KEY` does not enforce uniqueness.

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

ClickHouse 26.7 adds a CREATE-time guard for off-key dimensions on qualifying
`AggregatingMergeTree` schemas. Verify the effective `allow_dimensions_outside_sorting_key`
setting on the target. A compatibility value of 26.6 or earlier can restore permissive
behavior. Keep the guard enabled for new designs. Review the full merge grain even when the
guard rejects some mistakes. On 24.8, prove it with rows differing only in the candidate
omitted dimension. Upgrading cannot reconstruct dimensions already lost during merges.
See the [guard implementation](https://github.com/ClickHouse/ClickHouse/pull/108087).

In 26.10, query-time `FINAL` on `SummingMergeTree` keeps rows whose summed columns are all
zero. Background merges and `OPTIMIZE TABLE … FINAL` still remove them. If the result contract
excludes all-zero groups, filter after summing the declared measures, and test with the same
keys before and after a merge.

For insert retry exactness, use the version, engine, deduplication window, and dependent-view
checks in `30-ingest-and-parts.md`. Background row merging and insert deduplication are
separate mechanisms.

`Replicated*` variants and what the single-node-to-cluster transition requires:
`10-authority-and-change-path.md`.
