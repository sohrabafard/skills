# Query-driven index decisions

Own index selection and plan evidence. [Queries](30-ent-queries.md) owns semantics; [migrations](50-migrations.md) owns deployment.

## Workload and recommendation contract

Inspect existing indexes/constraints and generated SQL. Record bind types/values, filters, joins, order/nulls, projection, LIMIT/paging, frequency, cardinality/selectivity, tenant skew, and read/write balance. Use code and representative requests when telemetry is unavailable; label assumptions unmeasured. Use authorized traces or pg_stat_statements without assuming installation/reconfiguration authority.

Map every recommended index to concrete SQL/code locations; identify its invariant when applicable. State definition, filter/join/order mechanism, unsupported relevant queries, overlap, write/storage cost, evidence, and deployment status. Label benefits hypothesized or measured. Sequential scans can suit small tables or large result fractions. Never promise instant lookups.

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
| `(tenant_id,course_id,id)` | Q2 | Leading join/filter keys locate children; ID supplies order. Full coverage can also serve child-side FK checks. |
| Existing `UNIQUE (tenant_id,id)` on courses | Q2 | Parent lookup and composite-FK target; do not duplicate its index. |

Plans can choose other paths. Compare tenant sizes, write load, and existing prefixes. Without ordering, consider a narrower child index. Justify overlaps.

## Ent representation

Use `index.Fields` and stable StorageKey; add Unique only for an invariant. Edge-index columns follow fields; expose an FK field when it must lead. In Content.Indexes, with `index`/`entsql` from Ent's schema/index and dialect/entsql packages:

```go
index.Fields("tenant_id", "status", "created_at", "id").
    StorageKey("contents_active_page_idx").
    Annotations(entsql.DescColumns("created_at", "id"),
        entsql.IndexWhere("deleted_at IS NULL"))
```

Inspect generated SQL against Q1. Annotations define shape, not concurrent rollout. Verify selected-release IncludeColumns, IndexType/IndexTypes, and OpClass/OpClassColumn APIs before use. No documented `index.Expr` exists in the verified baseline; use external-object migration ownership for expressions. Match PostgreSQL-normalized partial predicates to avoid repeated diffs.

## Keys, predicates, payload

- Put useful B-tree equality keys before range/order keys. Leading equalities and the first inequality bound the scan; later predicates can reduce heap visits without narrowing that range. Skip-scan opportunities depend on server version, distinct counts, and selectivity; verify the plan.
- Match direction, collation, and NULL order. Backward scans do not satisfy every mixed ASC/DESC order. Matching ORDER BY can reduce LIMIT work; preserve the query's unique cursor tie-breaker.
- Require planning-time implication for partial predicates. `deleted_at IS NULL` can qualify; generic `status=$1` cannot imply `status='published'`. Custom plans can see values. Test actual prepared-plan behavior; parameterization is not universally incompatible.
- INCLUDE is payload, not a search/sort key or uniqueness member. Consider `IncludeColumns("title")` for Q1 only when projection and measurements justify it. Index-only scans still need visibility-map coverage; changed pages need heap checks. Wide/frequently updated payload can cost more than it saves. GIN cannot provide index-only scans.
- PostgreSQL creates no automatic child-side FK index. Evaluate leading child keys for joins and parent updates/deletes. Live-row partial indexes omit retained deleted references. Before removal, check constraints, rare operations, observation/reset windows, and coverage. Neither zero scans nor prefix overlap proves redundancy.

## Other access methods

Tie each candidate to concrete generated predicates:

| Query requirement | Candidate and decisive check |
| --- | --- |
| Equality/range/order | B-tree with matching operators, collation, direction, and NULL semantics. |
| Normalized identifier | `(tenant_id,lower(email))`; generated expression/collation must match. EqualFold alone proves no match. |
| JSON containment/key search | GIN with matching opclass: jsonb_path_ops lacks key-existence support; jsonb_ops supports it. |
| Substring/similarity | pg_trgm GIN/GiST; verify extension/opclass/operator. No extractable trigrams can mean a full-index scan. |
| Full text | GIN/GiST on matching tsvector/configuration; keep expression and normalization consistent. |
| Large correlated append data | BRIN; verify correlation, lossy rechecks, summarization, and range size. It is not a point-lookup substitute. |
| Ranges/spatial | Matching GiST/SP-GiST opclass, operator support, extension, and target version. |

Expression indexes require immutable expressions; never mislabel time-dependent functions. Preserve binding and identifier allowlists when changing predicates.

## Evidence and acceptance

Use estimated EXPLAIN when execution is unauthorized. EXPLAIN ANALYZE executes statements/function effects; rollback cannot neutralize every side effect. In an authorized bounded environment, capture `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` with actual binds, current statistics, and representative tenant/value distributions.

Compare estimates/actual rows, loops, filtered/scanned work, buffers, heap fetches, sorting/spills, and planning/execution time. Measure size/write impact. Resolve stale statistics/bad estimates before adding compensating indexes. A plan node proves no speedup. Projection evidence also needs application latency/allocations because EXPLAIN omits transfer/decoding.

Return the query-to-index matrix, before/after evidence, and limits. Without execution, deliver unmeasured candidates and validation instructions. Stop when the selected workload meets its target with preserved semantics.

Consult [Ent indexes](https://entgo.io/docs/schema-indexes/) and [annotation APIs](https://pkg.go.dev/entgo.io/ent/dialect/entsql) for unfamiliar representation. Use target-version PostgreSQL [multicolumn](https://www.postgresql.org/docs/current/indexes-multicolumn.html), [partial](https://www.postgresql.org/docs/current/indexes-partial.html), [index-only](https://www.postgresql.org/docs/current/indexes-index-only-scans.html), and [EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html) guidance when relying on planner behavior. [Source policy](00-sources.md) routes specialized opclasses/extensions and version mismatches.
