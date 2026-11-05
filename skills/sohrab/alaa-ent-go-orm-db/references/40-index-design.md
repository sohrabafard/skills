# Design indexes from the queries they serve

Read for index addition, change, removal, or evaluation. This file owns selection and plan evidence. Use [30-ent-queries.md](30-ent-queries.md) for queries/projections and [50-migrations.md](50-migrations.md) for rollout.

## Contents

- [Capture the workload](#capture-the-workload)
- [Map queries to candidate indexes](#map-queries-to-candidate-indexes)
- [Represent an index in Ent](#represent-an-index-in-ent)
- [Choose keys, predicates, and payload](#choose-keys-predicates-and-payload)
- [Choose other access methods](#choose-other-access-methods)
- [Measure and report](#measure-and-report)

## Capture the workload

Collect generated SQL, sanitized bind types, and representative values for relevant operations. Record filters, joins, ordering/nulls, projection, LIMIT/paging, frequency, cardinality, selectivity, tenant skew, and read/write balance. Inspect existing indexes and constraints first. Without telemetry, use code and representative requests; mark frequency/selectivity assumptions unmeasured.

Use accessible `pg_stat_statements` or application traces. An index request does not automatically authorize extension installation or server reconfiguration. Sequential scans can suit small tables or large result fractions. Promise no “instant lookups”; state expected work reduction and required evidence.

For each index, report its definition, query IDs/code locations, filter/join/order support, mechanism, write/storage cost, evidence, and deployment status. Label benefits hypothesized or measured. Identify unsupported relevant queries when this affects selection.

Sources: [PostgreSQL plan interpretation](https://www.postgresql.org/docs/current/using-explain.html), [statement statistics](https://www.postgresql.org/docs/current/pgstatstatements.html).

## Map queries to candidate indexes

These candidates serve the shown workloads using [20-schema-design.md](20-schema-design.md). Do not add them indiscriminately.

Q1, active content page:

```sql
SELECT id, title, created_at
FROM public.contents
WHERE tenant_id = $1 AND status = $2 AND deleted_at IS NULL
ORDER BY created_at DESC, id DESC
LIMIT $3;
```

Q2, contents of one tenant's course:

```sql
SELECT c.id, c.title
FROM public.contents AS c
JOIN public.courses AS p
  ON p.tenant_id = c.tenant_id AND p.id = c.course_id
WHERE p.tenant_id = $1 AND p.id = $2
ORDER BY c.id
LIMIT $3;
```

| Index candidate | Query served | Mechanism and boundary |
|---|---|---|
| `(tenant_id, status, created_at DESC, id DESC) WHERE deleted_at IS NULL` | Q1 | Equality narrows the active range; key order can avoid sorting before LIMIT. Queries including deleted rows cannot rely on this partial index. |
| `(tenant_id, course_id, id)` | Q2 | Leading join/filter keys locate one course's children; the ID suffix can supply ordering. The full index can also serve child-side FK maintenance. |
| Existing parent `UNIQUE (tenant_id,id)` | Q2 | Supports parent lookup and the composite FK target. Do not add an identical ordinary index. |

Plans may choose another path. Compare measured cost, existing prefixes, tenant sizes, and write load. Without ordered retrieval, consider the narrower child index. Justify retaining both overlapping indexes.

## Represent an index in Ent

Use `index.Fields(...)`, a stable `StorageKey`, and `Unique()` only for a required invariant. Ent appends edge-index columns after field columns. Expose an FK field when it must lead.

```go
// Add to the existing schema package and Content schema.
// Imports: entgo.io/ent, entgo.io/ent/schema/index,
//          entgo.io/ent/dialect/entsql.
func (Content) Indexes() []ent.Index {
    return []ent.Index{
        index.Fields("tenant_id", "status", "created_at", "id").
            StorageKey("contents_active_page_idx").
            Annotations(
                entsql.DescColumns("created_at", "id"),
                entsql.IndexWhere("deleted_at IS NULL"),
            ),
        index.Fields("tenant_id", "course_id", "id").
            StorageKey("contents_course_id_idx"),
    }
}
```

The first declaration targets this database shape:

```sql
CREATE INDEX contents_active_page_idx
ON public.contents (tenant_id, status, created_at DESC, id DESC)
WHERE deleted_at IS NULL;
```

Inspect generated SQL. Index annotations define shape, not production rollout. Use [50-migrations.md](50-migrations.md) for concurrent builds.

Documented annotations include `entsql.IncludeColumns`, `IndexType`, `IndexTypes`, `OpClass`, and `OpClassColumn`. Verify pinned APIs for the required access method/opclass. Use the external-object migration path for expression parts; the documented API has no `index.Expr`. Match database-normalized partial predicates to avoid repeated diffs.

Sources: [Ent indexes](https://entgo.io/docs/schema-indexes/), [Ent SQL annotation API](https://pkg.go.dev/entgo.io/ent/dialect/entsql).

## Choose keys, predicates, and payload

Align B-tree leading equality keys, then useful range/order keys. Leading equalities and the first non-equality key bound the scan. Later predicates can reduce heap visits without narrowing that range. Missing leading predicates do not make an index universally unusable. PostgreSQL 18 supports beneficial skip scans for suitable distinct counts/selectivity; verify version and plan before relying on them.

Respect direction, collation, and null ordering. Backward scans do not make all-ascending multicolumn indexes satisfy every mixed ASC/DESC order. Matching ORDER BY can reduce LIMIT work. Preserve a deterministic unique pagination tiebreaker through [30-ent-queries.md](30-ent-queries.md).

Require planning-time proof of partial predicates. Fixed `deleted_at IS NULL` can qualify; generic `status=$1` cannot imply `status='published'`. Custom plans can see bound values. Test actual driver/prepared-plan behavior and relevant values. Parameterized queries are not universally incompatible with partial indexes.

INCLUDE supplies payload, not search/sort keys or uniqueness. Add `entsql.IncludeColumns("title")` to Q1 only when exact projection and measurements justify covering. Index-only scans also require suitable visibility-map state; recently changed pages need heap checks. Wide/frequently updated payload can outweigh benefits. GIN cannot provide index-only scans. Use [30-ent-queries.md](30-ent-queries.md) for projection changes.

PostgreSQL creates no automatic child-side FK index. Evaluate leading child keys for joins and parent updates/deletes. A live-row partial index cannot cover FK checks involving deleted children that retain references. Preserve integrity when considering removal. Check observation/reset windows, constraints, rare operations, and coverage; zero scans or prefix overlap alone proves no redundancy.

Sources: [multicolumn](https://www.postgresql.org/docs/current/indexes-multicolumn.html), [ordering](https://www.postgresql.org/docs/current/indexes-ordering.html), [partial indexes](https://www.postgresql.org/docs/current/indexes-partial.html), [prepared plans](https://www.postgresql.org/docs/current/sql-prepare.html), [covering indexes](https://www.postgresql.org/docs/current/indexes-index-only-scans.html), [foreign keys](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK).

## Choose other access methods

| Need | Candidate | Check |
|---|---|---|
| Equality/range and sorted retrieval | B-tree | Operators, collation, direction and null semantics match. |
| Case-normalized identifier | Expression index such as `(tenant_id, lower(email))` | Generated SQL must apply the same expression/collation. `EqualFold` does not prove that it does. |
| JSONB containment or key search | GIN | Match the operator class. `jsonb_path_ops` does not support key existence; default `jsonb_ops` does. |
| Substring or similarity search | `pg_trgm` GIN/GiST | Extension availability, opclass, query operator. Patterns with no extractable trigrams can cause full-index scans. |
| Full-text search | GIN/GiST on a matching tsvector expression or stored representation | Text-search configuration and expression must match the query; keep normalization consistent. |
| Large correlated append data | BRIN | Verify physical correlation, lossy rechecks, summarization, and range size. It is not a point-lookup substitute. |
| Ranges/spatial relationships | Matching GiST/SP-GiST opclass | Verify operator support, extension prerequisites and target version. |

Expression indexes require immutable expressions; do not mislabel time-dependent functions. Preserve value binding and allowlist dynamic identifiers when changing predicates.

Sources: [access methods](https://www.postgresql.org/docs/current/indexes-types.html), [expressions](https://www.postgresql.org/docs/current/indexes-expressional.html), [JSONB indexes](https://www.postgresql.org/docs/current/datatype-json.html#JSON-INDEXING), [trigrams](https://www.postgresql.org/docs/current/pgtrgm.html), [BRIN](https://www.postgresql.org/docs/current/brin.html), [text search](https://www.postgresql.org/docs/current/textsearch-indexes.html).

## Measure and report

Use estimated EXPLAIN when execution is unauthorized. `EXPLAIN ANALYZE` executes statements and function side effects; rollback does not make every effect safe. Require an authorized environment and bounded execution for measurements. Capture representative `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` with actual binds, current statistics, and relevant tenant/value distributions.

Compare estimated/actual rows, loops, scanned/filtered work, buffers, heap fetches, sorting/spills, and planning/execution time. Check index size and write impact. Resolve stale statistics/bad estimates before masking planner problems with indexes. A node name proves no improvement. For projections, measure application latency/allocations too; EXPLAIN excludes transfer and decoding.

Return the query-to-index matrix, before/after evidence, and limits. Without execution, deliver candidate schema/migration and validation instructions labeled unmeasured. Stop when the selected workload meets its target with preserved behavior. Route index removal/live rollout through [50-migrations.md](50-migrations.md) and main-skill authorization.

Sources: [EXPLAIN command](https://www.postgresql.org/docs/current/sql-explain.html), [planner statistics](https://www.postgresql.org/docs/current/planner-stats.html).
