# Ent operations, queries, and projections

Contents: [API scope](#api-scope) · [Operations](#operations) · [Upsert](#upsert) · [Projection](#projection) · [Predicates](#predicates) · [Loading and pagination](#loading-and-pagination) · [Acceptance](#acceptance)

Read for changed reads, mutations, projections, graph loading, predicates, aggregation, pagination or upserts. Keep work within the affected use case. The main skill owns authorization, freshness, retry limits and completion reporting.

Reviewed 2026-11-05. Projection and eager-loading semantics were also checked against Ent v0.14.6 generated templates.

## API scope

Resolve generated packages from the actual module. Schema APIs belong to `entgo.io/ent`; clients, entities and error helpers belong to the generated project package. Avoid shadowing predicate imports with variables. Inspect generated methods before using them.

Check existing feature flags: `sql/upsert` for upsert, `sql/modifier` for Modify, `sql/lock` for locks, `sql/execquery` for raw execution. Enable only required features. [API](https://entgo.io/docs/crud/) · [Flags](https://entgo.io/docs/feature-flags/)

## Operations

Use request contexts with cancellation/deadlines. Preserve errors; avoid panic-based X terminals in normal error-returning application paths.

| Need | Operation | Contract |
| --- | --- | --- |
| Create | `Create().Set...().Save(ctx)` | Entity; use `Exec(ctx)` when unused |
| Read by ID | `Get(ctx,id)` or scoped projected `Query().Where(...).Only(ctx)` | Get loads the whole entity and grants no authorization |
| Exactly one | `Only(ctx)` | Distinguish absent and multiple rows |
| First match | `Order(...).First(ctx)` | Order matters when selecting a particular row |
| Rows | `Select(...).Limit(...).All(ctx)` or `Scan(ctx,&dto)` | Bound rows and columns |
| Existence | `Exist(ctx)` | Avoid entity loading or full counting |
| IDs/scalar | `IDs(ctx)` or `Select(field).Strings/Ints/...` | Match the generated schema type |
| Update one | `UpdateOneID(id).Where(...).Set...().Save/Exec(ctx)` | An unmet condition can produce NotFound |
| Update many | `Update().Where(...).Set...().Save(ctx)` | Check affected-row count when correctness requires it |
| Delete one | `DeleteOneID(id).Where(...).Exec(ctx)` | Returns error |
| Delete many | `Delete().Where(...).Exec(ctx)` | Returns (count,error); preserve scoped filters |

Use Get only when the complete entity is needed. Distinguish omitted input, NULL and zero. `SetNillableX(nil)` does not clear; use `ClearX` for an explicit optional-field NULL. Prefer atomic AddX or conditional updates over unsafe read-modify-write. Handle empty filters/ID lists deliberately; never discard a required filter.

Edge setters accept existing entities/IDs, not Create builders. Persist related entities and associate them transactionally when atomicity is required. Inspect plural Clear/Add/Remove methods; do not assume SetPets or authority to attach arbitrary IDs.

Bound CreateBulk by parameters, payload and memory. Decide whole-operation atomicity versus partial completion; report committed batches on later failure. Do not parallelize dependent operations through one transaction.

Use generated error helpers. Distinguish PostgreSQL conflicts by driver SQLSTATE/constraint metadata; IsConstraintError alone does not identify duplicate email. [CRUD](https://entgo.io/docs/crud/) · [Error metadata](https://www.postgresql.org/docs/current/errcodes-appendix.html)

## Upsert

Confirm insert-or-conflict-update semantics, `sql/upsert`, the existing unique constraint/index and PostgreSQL conflict target. Preserve tenant business-key scope and matching partial-index predicates. Whitelist conflict-update fields; protect identity, immutable metadata and unrelated values.

Upsert runs create hooks, not ordinary update hooks. Enforce equivalent policy/invariants. Inspect the pinned implementation and SQL for Ignore/DoNothing: it can differ from genuine DO NOTHING. DO NOTHING can return no row; do not promise an existing ID. Never use no-op updates as authorization shortcuts. Resolve duplicate conflict keys within a bulk upsert.

[Ent upsert](https://entgo.io/docs/crud/#upsert-one) · [PostgreSQL INSERT](https://www.postgresql.org/docs/current/sql-insert.html)

## Projection

For each changed read, list required response fields and application decisions first. Add only necessary identity, relation-mapping and cursor fields. Filtering/joining alone does not require returning its columns. Justify extra expressions required by DISTINCT/order/grouping or generated loaders; preserve result semantics.

Use field constants and explicit Select. Prefer `Select(...).Scan` into response DTOs for flat outputs. Use dedicated ID/scalar/count terminals when applicable. `All(ctx)` collects rows; it remains appropriate with explicit entity projection.

Unselected entity fields retain zero/nil values; database defaults do not refill them. Optional/Nillable affect schema/Go representation, not general loadedness. Preserve DTO NULL semantics. Never save omitted fields as zero or use them for decisions; fetch required missing data explicitly.

Entity `Select(...).All` can add IDs and eager-loader FK columns. Inspect actual SQL and wiring. DTO/scalar `Scan` does not imply ID insertion, and `Select(...).Scan` does not hydrate `With...` associations. Include cursor/mapping keys where the actual path needs them.

Illustration: Task has int64 id/tenant_id, string title, time.Time created_at and optional deleted_at. Symbols are generated locally; `sql` is `entgo.io/ent/dialect/sql`. Validate pageSize and obtain tenantID from trusted context first.

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

CreatedAt/ID support a cursor; body/private metadata are omitted. Project each eager child separately. Exclude secrets and large JSON/BLOB fields unless required. Sensitive controls generated printing/encoding, not selection or debug logs. Allowlist client-requested fields/sorts with server-owned mappings; never accept arbitrary SQL identifiers.

[Field selection](https://entgo.io/docs/crud/#field-selection) · [Nillable](https://entgo.io/docs/schema-fields/#nillable) · [v0.14.6 query template](https://github.com/ent/ent/blob/v0.14.6/entc/gen/template/dialect/sql/query.tmpl)

## Predicates

Prefer typed predicates and deliberate And/Or/Not, HasEdgeWith and QueryEdge semantics. Use IsNil/NotNil for SQL NULL. Relation existence alone grants no authorization.

Bind custom values. Use `func(*sql.Selector)`, qualified `s.C(field)` and SQL builders. Wrap sqljson predicates in `s.Where(...)` inside that callback. `sql.P` accepts builder functions. ExprP preserves literal SQL; it does not rebind `?` for PostgreSQL. Use dialect-aware Builder.Arg/Ident for composed expressions; keep syntax/identifiers trusted.

Modify requires `sql/modifier`. Route raw execution through the security reference. Verify JSON operators/value shape: containment is not automatically "contains any". Check index compatibility when adding casts/functions.

[Predicates](https://entgo.io/docs/predicates/) · [SQL builder](https://github.com/ent/ent/blob/v0.14.6/dialect/sql/builder.go)

## Loading and pagination

Replace per-row relation fetches with bounded eager loading or batch queries when needed. Eager loading issues additional association queries; it does not guarantee one JOIN. Bound parents, child fan-out and traversal depth. Ordinary child Limit is not per-parent top-K. Use verified window/edge-limit logic and test multiple parents. Use generated `Edges.XOrErr` to distinguish unloaded from empty.

Use deterministic total ordering with a unique tie-breaker. Encode all sort keys; validate cursors against order, filters and tenant scope. For descending (created_at,id), seek:

`created_at < cursorTime OR (created_at = cursorTime AND id < cursorID)`.

Reverse comparisons for ascending order; define NULL/mixed-direction behavior. Select cursor keys, cap page size, fetch limit+1, handle empties, and cursor from the last retained row. Keyset avoids large OFFSET; it does not guarantee a snapshot under concurrent updates.

Use Count/Exist only when required by result semantics. Count/page can differ under concurrent writes. Clone builders before branching; never share one mutable builder concurrently.

For aggregation, establish row grain and prevent join multiplication. Use GroupBy/Aggregate with explicit DTO aliases. Filter rows before grouping and groups with HAVING. Handle NULL aggregates and numeric range. Review SQL for custom joins/window functions.

[Eager loading](https://entgo.io/docs/eager-load/) · [Ordering](https://entgo.io/docs/paging/) · [Aggregation](https://entgo.io/docs/aggregate/)

## Acceptance

Check affected values, shape, order, limits, tenant scope, NULL/zero/omitted states and relations. Inspect emitted columns, predicates, statement count and relation/cursor keys. Include relevant empty, multiple-row and multi-parent cases. Route index/plan evidence to the index reference. Separate source/static inspection from compiled/database tests. State unavailable generation, compilation or PostgreSQL execution; claim no unobserved compatibility or performance result.

