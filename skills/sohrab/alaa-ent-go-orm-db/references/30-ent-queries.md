# Ent queries and projections

Read this file for CRUD, predicates, projections, graph loading, aggregation, pagination, or upserts. Resolve APIs from the actual module: schemas use `entgo.io/ent`; clients, entities, predicates and error helpers use generated packages. Avoid shadowing predicate imports. Consult [feature integration](80-advanced-ent.md) before adding feature-dependent APIs.

## Operations

Use cancellable request contexts. Preserve errors; avoid panic-based X terminals in ordinary error-returning application paths.

| Need | Operation and boundary |
| --- | --- |
| Create | `Create().Set...().Save(ctx)`; `Exec(ctx)` when the entity is unused. |
| Read by ID | `Get(ctx,id)` loads the entity; it supplies no tenant or owner predicate itself. Use scoped projection when fewer fields suffice. |
| Exactly one, or first | `Only(ctx)` distinguishes absent rows from multiple rows. Use deterministic `Order(...).First(ctx)` to select a particular row. |
| Rows, existence or scalar | Use a bounded `Select(...).All(ctx)` or `Scan(ctx,&dto)`; use `Exist`, `IDs`, or scalar terminals matching generated types when sufficient. |
| Update one or many | `UpdateOneID(id).Where(...).Set...().Save/Exec(ctx)` may return NotFound. `Update().Where(...).Save(ctx)` returns a count; check it when correctness depends on it. |
| Delete one or many | `DeleteOneID(id).Where(...).Exec(ctx)` returns an error; `Delete().Where(...).Exec(ctx)` returns a count and an error. Preserve scoped filters. |

Distinguish omitted input, NULL, and zero. `SetNillableX(nil)` skips assignment; `ClearX` explicitly clears an optional field. Prefer atomic AddX or conditional updates to unsafe read-modify-write. Handle empty filters and ID lists without dropping required predicates.

Edge setters accept persisted entities or IDs, not Create builders. Inspect the plural Clear, Add and Remove methods; do not assume SetPets. Authorize association IDs. When atomicity is required, run related creation and association in one transaction.

Bound CreateBulk by parameters, payload, and memory. Decide atomicity versus partial completion; report committed batches after failure. Do not parallelize dependent work through one transaction. Use generated error helpers and driver SQLSTATE and constraint metadata: IsConstraintError alone cannot identify duplicate email.

## Minimum correct projection

For every changed read, list response, authorization, and application requirements. Select only required columns plus identity, association-mapping, and cursor keys. Filtering or joining alone does not require returning those columns. Justify extra expressions required by DISTINCT, ordering, grouping, or generated loaders.

Use field constants and explicit Select. Prefer DTO Scan for flat outputs; preserve NULL semantics. Use scalar, ID or count terminals when sufficient. Entity All remains appropriate with explicit projection.

Unselected entity fields retain zero or nil values; defaults and `Optional` or `Nillable` do not restore loadedness. Never use omitted values for decisions or write them back as zero. Fetch missing required data explicitly.

Entity `Select(...).All` can add IDs and eager-loader FK columns. Inspect emitted SQL and association wiring. A DTO or scalar Scan implies no added IDs; `Select(...).Scan` does not hydrate `With...` edges. Project eager children separately.

Example: Task has an int64 ID and tenant ID, a title, created_at, and an optional deleted_at. Validate pageSize and resolve trusted tenantID first. `sql` is `entgo.io/ent/dialect/sql`.

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

CreatedAt and ID support the cursor. Exclude secrets and large JSON or BLOB values unless required. Sensitive affects generated printing and encoding, not SQL selection or debug logs. Map requested fields and sorts through server allowlists; never accept arbitrary SQL identifiers.

## Upsert and custom predicates

Verify `sql/upsert`, the unique constraint or index, and PostgreSQL conflict target, including tenant scope and partial predicates. Allowlist conflict-update fields; protect identity, immutable metadata, and unrelated values. Resolve duplicate conflict keys within a bulk upsert.

Upserts run create hooks, not update hooks; preserve equivalent policy and invariants. Inspect the pinned Ignore and DoNothing implementation and SQL: Ignore may differ from DO NOTHING. DO NOTHING can return no row; never promise an existing ID or use a no-op update to bypass authorization.

Use typed predicates and deliberate And/Or/Not, HasEdgeWith, and QueryEdge semantics. Use IsNil or NotNil for NULL; relation existence grants no authorization. Bind custom values through dialect-aware builders; qualify selector columns with `s.C(field)`. Wrap sqljson predicates in `s.Where(...)` within `func(*sql.Selector)`. `sql.P` takes builder functions. ExprP preserves literal SQL and does not rebind PostgreSQL `?`; use Builder.Arg or Builder.Ident with trusted syntax and identifiers. Verify the JSON operator and value shape: containment is not automatically "contains any". Reassess indexes after adding casts or functions. Route raw execution to [security](60-transactions-security.md).

## Loading, pagination and aggregation

Replace per-row relation fetches with bounded eager or batch loading when needed. Eager loading adds association queries; it promises no single JOIN. Bound parents, child fan-out, and depth. Ordinary child Limit is not per-parent top-K; verify window or edge-limit logic with multiple parents. Use generated `Edges.XOrErr` to distinguish unloaded from empty.

Use a deterministic total order with a unique tie-breaker. Encode every sort key; validate cursors against ordering, filters, and tenant scope. Descending `(created_at,id)` seeks:

`created_at < cursorTime OR (created_at = cursorTime AND id < cursorID)`.

Reverse comparisons for ascending order; define the behavior for NULL and mixed directions. Select cursor keys, cap page size, fetch limit+1, and handle empties. Build cursors from the last retained row. Keyset avoids large OFFSET, but concurrent updates can change the view. Count and page can also differ; request Count/Exist only when semantics need them. Clone before branching; never share mutable builders concurrently.

For aggregates, establish row grain and prevent join multiplication. Use GroupBy and Aggregate with explicit DTO aliases; filter rows before grouping and groups with HAVING. Handle NULL and range cases, and inspect join and window SQL.

## Evidence and consultation

Check values, shape, order and limits, tenant scope, the omitted, NULL and zero states, and relations. Inspect SQL columns and predicates, statement count, and cursor and FK keys. Cover relevant empty, multiple-row, and multi-parent cases. [Index design](40-index-design.md) owns plans; [runtime verification](70-runtime-testing.md) owns executed-test evidence.

Consult [CRUD](https://entgo.io/docs/crud/), [predicates](https://entgo.io/docs/predicates/), [eager loading](https://entgo.io/docs/eager-load/), [pagination](https://entgo.io/docs/paging/), or [aggregation](https://entgo.io/docs/aggregate/) for unfamiliar APIs. Projection and eager-loader details were checked against [v0.14.6 query templates](https://github.com/ent/ent/blob/v0.14.6/entc/gen/template/dialect/sql/query.tmpl) on 2026-11-05. Inspect selected-release templates when behavior differs; do not infer unsupported methods. Check PostgreSQL [INSERT](https://www.postgresql.org/docs/current/sql-insert.html) for unfamiliar conflict behavior.
