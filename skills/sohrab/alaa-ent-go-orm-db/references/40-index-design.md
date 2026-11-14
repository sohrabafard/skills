# Query-driven index decisions

This file owns index selection and plan evidence. [Queries](30-ent-queries.md) owns semantics; [migrations](50-migrations.md) owns deployment.

## Workload and recommendation contract

Inspect existing indexes and constraints and the generated SQL. Record bind types and values, filters, joins, order and null placement, projection, LIMIT and paging, frequency, cardinality and selectivity, tenant skew, and the read-to-write balance. Use code and representative requests when telemetry is unavailable; label assumptions unmeasured. Use authorized traces or pg_stat_statements without assuming installation or reconfiguration authority.

Map every recommended index to concrete SQL and code locations, and identify its invariant when applicable. State its definition, the filter, join or order mechanism it serves, the relevant queries it does not support, its overlap, its write and storage cost, its evidence, and its deployment status. Label each benefit as hypothesized or measured. Sequential scans can suit small tables or large result fractions. Never promise instant lookups.

## Concrete candidates

Q1, active content page:

```sql
SELECT id, title, created_at FROM public.contents
WHERE tenant_id = $1 AND status = $2 AND deleted_at IS NULL
ORDER BY created_at DESC, id DESC LIMIT $3;
```

Q2, one tenant's course contents:

```sql
SELECT c.id, c.title FROM public.contents AS c
JOIN public.courses AS p
  ON p.tenant_id = c.tenant_id AND p.id = c.course_id
WHERE p.tenant_id = $1 AND p.id = $2
ORDER BY c.id LIMIT $3;
```

| Candidate | Query | Mechanism and boundary |
| --- | --- | --- |
| `(tenant_id,status,created_at DESC,id DESC) WHERE deleted_at IS NULL` | Q1 | Equality narrows active rows; key order can avoid sorting before LIMIT. Excludes deleted-row queries. |
| `(tenant_id,course_id,id)` | Q2 | Leading join and filter keys locate children; ID supplies order. Full coverage can also serve child-side FK checks. |
| Existing `UNIQUE (tenant_id,id)` on courses | Q2 | It serves the parent lookup and is the composite-FK target; do not duplicate its index. |

Plans can choose other paths. Compare tenant sizes, write load, and existing prefixes. Without ordering, consider a narrower child index. Justify overlaps.

## Ent representation

Use `index.Fields` and a stable StorageKey, and add Unique only for an invariant. Edge-index columns follow fields; expose an FK field when it must lead. In Content.Indexes, with `index` and `entsql` from Ent's `schema/index` and `dialect/entsql` packages:

```go
index.Fields("tenant_id", "status", "created_at", "id").
    StorageKey("contents_active_page_idx").
    Annotations(entsql.DescColumns("created_at", "id"),
        entsql.IndexWhere("deleted_at IS NULL"))
```

Inspect generated SQL against Q1. Annotations define shape, not concurrent rollout. Before use, verify the selected release's IncludeColumns, IndexType and IndexTypes, and OpClass and OpClassColumn APIs. No documented `index.Expr` exists in the verified baseline; use external-object migration ownership for expressions. Match PostgreSQL-normalized partial predicates to avoid repeated diffs.

## Keys, predicates and payload

- Put useful B-tree equality keys before range and order keys. Leading equalities and the first inequality bound the scan; later predicates can reduce heap visits without narrowing that range. Skip-scan opportunities depend on server version, distinct counts, and selectivity; verify the plan.
- Match direction, collation, and NULL order. Backward scans do not satisfy every mixed ASC and DESC order. Matching ORDER BY can reduce LIMIT work; preserve the query's unique cursor tie-breaker.
- Require planning-time implication for partial predicates. `deleted_at IS NULL` can qualify; generic `status=$1` cannot imply `status='published'`. Custom plans can see values. Test actual prepared-plan behavior; parameterization is not universally incompatible.
- INCLUDE is payload, not a search or sort key or a uniqueness member. Consider `IncludeColumns("title")` for Q1 only when projection and measurements justify it. Index-only scans still need visibility-map coverage; changed pages need heap checks. Wide or frequently updated payload can cost more than it saves. GIN cannot provide index-only scans.
- PostgreSQL creates no automatic child-side FK index. Evaluate leading child keys for joins and for parent updates and deletes. Live-row partial indexes omit retained deleted references. Before removal, check constraints, rare operations, observation and reset windows, and coverage. Neither zero scans nor prefix overlap proves redundancy.

## Other access methods

Tie each candidate to concrete generated predicates:

| Query requirement | Candidate and decisive check |
| --- | --- |
| Equality, range or order | B-tree with matching operators, collation, direction, and NULL semantics. |
| Normalized identifier | `(tenant_id,lower(email))`; the generated expression and collation must match. EqualFold alone proves no match. |
| JSON containment or key search | GIN with matching opclass: jsonb_path_ops lacks key-existence support; jsonb_ops supports it. |
| Substring or similarity | pg_trgm GIN or GiST; verify the extension, opclass and operator. No extractable trigrams can mean a full-index scan. |
| Full text | GIN or GiST on a matching tsvector and configuration; keep expression and normalization consistent. |
| Large correlated append data | BRIN; verify correlation, lossy rechecks, summarization, and range size. It is not a point-lookup substitute. |
| Ranges or spatial data | A matching GiST or SP-GiST opclass, operator support, extension, and target version. |

Expression indexes require immutable expressions; never mislabel time-dependent functions. Preserve binding and identifier allowlists when changing predicates.

## Evidence and acceptance

Use estimated EXPLAIN when execution is unauthorized. EXPLAIN ANALYZE executes statements and their function effects; rollback cannot neutralize every side effect. In an authorized bounded environment, capture `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` with actual binds, current statistics, and representative tenant and value distributions.

Compare estimated and actual rows, loops, filtered and scanned work, buffers, heap fetches, sorting and spills, and planning and execution time. Measure the size and write impact. Resolve stale statistics and bad estimates before adding compensating indexes. A plan node proves no speedup. Projection evidence also needs application latency and allocations, because EXPLAIN omits transfer and decoding.

Return the query-to-index matrix, the before and after evidence, and the limits. Without execution, deliver unmeasured candidates and validation instructions. Stop when the selected workload meets its target with preserved semantics.

Consult [Ent indexes](https://entgo.io/docs/schema-indexes/) and [annotation APIs](https://pkg.go.dev/entgo.io/ent/dialect/entsql) for unfamiliar representation. Use target-version PostgreSQL [multicolumn](https://www.postgresql.org/docs/current/indexes-multicolumn.html), [partial](https://www.postgresql.org/docs/current/indexes-partial.html), [index-only](https://www.postgresql.org/docs/current/indexes-index-only-scans.html), and [EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html) guidance when relying on planner behavior. [Source policy](00-sources.md) routes specialized opclasses, extensions and version mismatches.
