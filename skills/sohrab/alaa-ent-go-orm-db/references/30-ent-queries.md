# Ent queries and projections

Use for CRUD, predicates, projections, graph loading, aggregation, pagination, or upserts. Resolve APIs from the actual module: schemas use `entgo.io/ent`; clients/entities/predicates/error helpers use generated packages. Avoid shadowing predicate imports. Consult [feature integration](80-advanced-ent.md) before adding feature-dependent APIs.

## Operations

Use cancellable request contexts. Preserve errors; avoid panic-based X terminals in ordinary error-returning application paths.

| Need | Operation and boundary |
| --- | --- |
| Create | `Create().Set...().Save(ctx)`; `Exec(ctx)` when the entity is unused. |
| Read by ID | `Get(ctx,id)` loads the entity; it supplies no tenant/owner predicate itself. Use scoped projection when fewer fields suffice. |
| Exactly one / first | `Only(ctx)` distinguishes absent/multiple rows. Use deterministic `Order(...).First(ctx)` to select a particular row. |
| Rows / existence / scalar | Bounded `Select(...).All(ctx)`/`Scan(ctx,&dto)`; use `Exist`, `IDs`, or scalar terminals matching generated types when sufficient. |
| Update one / many | `UpdateOneID(id).Where(...).Set...().Save/Exec(ctx)` may return NotFound. `Update().Where(...).Save(ctx)` returns a count; check it when correctness depends on it. |
| Delete one / many | `DeleteOneID(id).Where(...).Exec(ctx)` returns error; `Delete().Where(...).Exec(ctx)` returns count/error. Preserve scoped filters. |

Distinguish omitted input, NULL, and zero. `SetNillableX(nil)` skips assignment; `ClearX` explicitly clears an optional field. Prefer atomic AddX/conditional updates to unsafe read-modify-write. Handle empty filters/ID lists without dropping required predicates.

Edge setters accept persisted entities/IDs, not Create builders. Inspect plural Clear/Add/Remove methods; do not assume SetPets. Authorize association IDs; transact related creation/association when atomicity is required.

Bound CreateBulk by parameters, payload, and memory. Decide atomicity versus partial completion; report committed batches after failure. Do not parallelize dependent work through one transaction. Use generated error helpers and driver SQLSTATE/constraint metadata: IsConstraintError alone cannot identify duplicate email.

## Minimum correct projection

For every changed read, list response, authorization, and application requirements. Select only required columns plus identity, association-mapping, and cursor keys. Filtering/joining alone does not require returning those columns. Justify extra expressions required by DISTINCT, ordering, grouping, or generated loaders.

Use field constants and explicit Select. Prefer DTO Scan for flat outputs; preserve NULL semantics. Use scalar/ID/count terminals when sufficient. Entity All remains appropriate with explicit projection.

Unselected entity fields retain zero/nil values; defaults and Optional/Nillable do not restore loadedness. Never use omitted values for decisions or write them back as zero. Fetch missing required data explicitly.

Entity `Select(...).All` can add IDs and eager-loader FK columns. Inspect emitted SQL and association wiring. DTO/scalar Scan implies no added IDs; `Select(...).Scan` does not hydrate `With...` edges. Project eager children separately.

Example: Task has int64 ID/tenant ID, title, created_at, and optional deleted_at. Validate pageSize and resolve trusted tenantID first. `sql` is `entgo.io/ent/dialect/sql`.

```go
var rows []struct {
    ID        int64     `json:"id"`
    Title     string    `json:"title"`
    CreatedAt time.Time `json:"created_at"`
}
err := client.Task.Query().
    Where(task.TenantIDEQ(tenantID), task.DeletedAtIsNil()).
    Order(task.ByCreatedAt(sql.OrderDesc()), task.ByID(sql.OrderDesc())).
    Limit(pageSize + 1).
    Select(task.FieldID, task.FieldTitle, task.FieldCreatedAt).
    Scan(ctx, &rows)
```

CreatedAt/ID support the cursor. Exclude secrets and large JSON/BLOB values unless required. Sensitive affects generated printing/encoding, not SQL selection or debug logs. Map requested fields/sorts through server allowlists; never accept arbitrary SQL identifiers.

## Upsert and custom predicates

Verify `sql/upsert`, the unique constraint/index, and PostgreSQL conflict target, including tenant scope and partial predicates. Allowlist conflict-update fields; protect identity, immutable metadata, and unrelated values. Resolve duplicate conflict keys within a bulk upsert.

Upserts run create hooks, not update hooks; preserve equivalent policy/invariants. Inspect pinned Ignore/DoNothing implementation and SQL: Ignore may differ from DO NOTHING. DO NOTHING can return no row; never promise an existing ID or use a no-op update to bypass authorization.

Use typed predicates and deliberate And/Or/Not, HasEdgeWith, and QueryEdge semantics. Use IsNil/NotNil for NULL; relation existence grants no authorization. Bind custom values through dialect-aware builders; qualify selector columns with `s.C(field)`. Wrap sqljson predicates in `s.Where(...)` within `func(*sql.Selector)`. `sql.P` takes builder functions. ExprP preserves literal SQL and does not rebind PostgreSQL `?`; use Builder.Arg/Ident with trusted syntax/identifiers. Verify JSON operator/value shape: containment is not automatically "contains any". Reassess indexes after casts/functions. Route raw execution to [security](60-transactions-security.md).

## Loading, pagination, aggregation

Replace per-row relation fetches with bounded eager/batch loading when needed. Eager loading adds association queries; it promises no single JOIN. Bound parents, child fan-out, and depth. Ordinary child Limit is not per-parent top-K; verify window/edge-limit logic with multiple parents. Use generated `Edges.XOrErr` to distinguish unloaded from empty.

Use a deterministic total order with a unique tie-breaker. Encode every sort key; validate cursors against ordering, filters, and tenant scope. Descending `(created_at,id)` seeks:

`created_at < cursorTime OR (created_at = cursorTime AND id < cursorID)`.

Reverse comparisons for ascending order; define NULL/mixed-direction behavior. Select cursor keys, cap page size, fetch limit+1, and handle empties. Build cursors from the last retained row. Keyset avoids large OFFSET, but concurrent updates can change the view. Count/page can also differ; request Count/Exist only when semantics need them. Clone before branching; never share mutable builders concurrently.

For aggregates, establish row grain and prevent join multiplication. Use GroupBy/Aggregate with explicit DTO aliases; filter rows before grouping and groups with HAVING. Handle NULL/range and inspect joins/window SQL.

## Evidence and consultation

Check values, shape/order/limits, tenant scope, omitted/NULL/zero states, and relations. Inspect SQL columns/predicates, statement count, and cursor/FK keys. Cover relevant empty, multiple-row, and multi-parent cases. [Index design](40-index-design.md) owns plans; [runtime verification](70-runtime-testing.md) owns executed-test evidence.

Consult [CRUD](https://entgo.io/docs/crud/), [predicates](https://entgo.io/docs/predicates/), [eager loading](https://entgo.io/docs/eager-load/), [pagination](https://entgo.io/docs/paging/), or [aggregation](https://entgo.io/docs/aggregate/) for unfamiliar APIs. Projection/eager-loader details were checked against [v0.14.6 query templates](https://github.com/ent/ent/blob/v0.14.6/entc/gen/template/dialect/sql/query.tmpl) on 2026-11-05. Inspect selected-release templates when behavior differs; do not infer unsupported methods. Check PostgreSQL [INSERT](https://www.postgresql.org/docs/current/sql-insert.html) for unfamiliar conflict behavior.
