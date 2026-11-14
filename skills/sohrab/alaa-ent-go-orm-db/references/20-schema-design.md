# Stored-data contract

This file owns fields, relationships, identity, tenancy, and lifecycle. Route access paths to [indexes](40-index-design.md), rollout to [migrations](50-migrations.md), and policy to [security](60-transactions-security.md).

## Model and constraints

Establish identity, ownership, lifecycle, cardinality, and important queries. Preserve existing IDs, storage names, public identifiers, and null semantics. Explain new choices within the requested scope.

Normalize repeated facts and relationships. Use edge schemas for relationship attributes, and store meaningful ordering explicitly. Denormalize only for a measured query with a reconciliation owner. JSONB does not enforce embedded references.

For each material field, record its type and unit, requiredness, default owner, mutability, uniqueness scope, and deletion behavior. Separate application validation from all-writer invariants:

- Enforce uniqueness in PostgreSQL, because concurrent writers can pass application prechecks.
- Pair CHECK with NOT NULL when null is invalid. CHECK accepts a null result.
- Use UNIQUE, FK, or exclusion constraints for invariants across rows or tables; do not query other rows inside CHECK.
- Ordinary UNIQUE permits multiple NULLs. Verify target-version `NULLS NOT DISTINCT` or another constraint when nulls must conflict.

Use lower_snake_case and stable constraint names. Avoid quoted mixed-case names and truncation collisions. Inspect generated DDL before claiming enforcement.

## Type decisions

| Data | Choose or verify |
| --- | --- |
| Integer ID | For a new 64-bit Go contract, use `field.Int64("id")`; inspect the SQL type and the sequence or identity behavior. |
| Public or distributed ID | Use PostgreSQL `uuid`, a declared Go dependency, and a generation owner. Preserve required UUIDv7 semantics; never silently substitute v4. |
| Instant | Use `timestamptz` with a UTC boundary convention, and a separate IANA timezone when future local-calendar rules need it. |
| Civil date or time | Use `date`, local time, or local timestamp according to meaning; a birthday is not a UTC instant. |
| Duration | Use a documented integer unit or a deliberately mapped interval; floating-point seconds require a precision contract. |
| Exact quantity | Use integer minor units plus a currency or unit, or NUMERIC plus an exact Go scanner and value type. SQL NUMERIC cannot repair Go float rounding. |
| Text | Use `text` or `varchar` with semantic bounds; arbitrary lengths or fixed char offer no assumed speed advantage. |
| Optional value | Define null versus zero or empty. `Optional().Nillable()` preserves that distinction in entities. |
| Document | Use JSONB for variable documents. Use typed columns or relations for constrained, frequently joined identifiers. |
| Finite state | Choose Ent string enum, CHECK, lookup table, or native PostgreSQL enum; include compatibility for changing or removing a value. |
| Arrays, ranges, network or spatial types | Verify mapping and driver scanner. Use relationships when elements need FKs or attributes. |

Ent supplies an integer SQL ID. PostgreSQL 18 documents [`uuidv7()`](https://www.postgresql.org/docs/current/functions-uuid.html); verify another generator on earlier servers. Go versions prove no database-function availability. UUIDv7 is not an authorization secret. Handle generator errors without panic defaults.

Test timestamp equality and cursor round trips at PostgreSQL's microsecond resolution. `timestamptz` loses the source timezone name. Keep application defaults separate from database defaults: `UpdateDefault(time.Now)` does not update external writes.

## Ent representation

Verify `SchemaType`, `GoType` and scanner conversions in generated output. `Optional()` changes requiredness; `Nillable()` changes representation without permitting SQL NULL alone. `Immutable()` removes update setters, not direct SQL access. Ent validators do not establish database constraints. Ent enums default to string storage; inspect the DDL for state enforcement or native enums.

When SQL or Go types or their representations change, read [runtime type mapping](70-runtime-testing.md#driver-type-mapping) before claiming driver compatibility.

A duration invariant needs both declarations, using `field` and `entsql` from their Ent schema and annotation packages:

```go
// In Fields():
field.Int64("duration_ms").Default(0).Min(0)
// In Annotations():
entsql.Checks(map[string]string{
    "contents_duration_nonnegative": "duration_ms >= 0",
})
```

Use `entsql.DefaultExpr(...)` for database expression defaults; verify create-builder omission and returned values. PostgreSQL DEFAULT cannot reference another column. Choose a generated column, application assignment, or trigger instead.

Use mixins only for identical shared behavior, and inspect all affected tables. During code renames, preserve storage names with supported `StorageKey` or table annotations.

## Relationships and tenants

Set cardinality and ownership before edge methods. Match FK type and optionality to the referenced ID and edge. For many contents per course:

```go
// Course: edge.To("contents", Content.Type)
edge.From("course", Course.Type).
    Ref("contents").Field("course_id").Unique().Required()
```

Use `entgo.io/ent/schema/edge` and a matching Course schema. Keep FKs unless an approved alternative enforces integrity. Independent tenant and parent FKs permit cross-tenant pairing. Require tenant fields on tenant-owned rows; enforce tenant-parent pairs in PostgreSQL:

```sql
-- Desired-state sketch; rollout belongs to 50-migrations.md.
ALTER TABLE public.courses
  ADD CONSTRAINT courses_tenant_id_id_key UNIQUE (tenant_id, id);
ALTER TABLE public.contents
  ADD CONSTRAINT contents_tenant_course_fk
  FOREIGN KEY (tenant_id, course_id)
  REFERENCES public.courses (tenant_id, id);
```

Require NOT NULL on mandatory pair members and choose ON DELETE behavior. If Ent cannot represent this FK, assign a migration-extension or SQL owner and preserve it in later diffs. Query filters cannot replace pair integrity. Use generator-supported IDs; edge-schema composite IDs do not establish ordinary node composite-ID support.

## Lifecycle and acceptance

Define hard or soft deletion, archival, retention, restoration, and whether deleted natural keys remain reserved. Live-row uniqueness can conflict during restore; define handling before implementation. Route filters and hooks to security and index predicates to index design.

Partition only for justified size, retention, pruning, or maintenance needs. Verify target-version unique and FK restrictions; assign creation, retention, and pruning owners. Keep schema and search paths explicit; reject request-controlled schema selection. Use [advanced integration](80-advanced-ent.md) for views or multiple schemas.

Return fields and edges, the invariant-to-constraint mapping, representation gaps, and migration impact. Test relevant duplicate, null, state, tenant-pair, deletion, restore, and exact-value cases through [runtime verification](70-runtime-testing.md). Block dependent changes on unresolved ownership, null semantics, or representation; name the missing decision.

Consult [Ent fields](https://entgo.io/docs/schema-fields/), [edges](https://entgo.io/docs/schema-edges/), and [SQL annotations](https://pkg.go.dev/entgo.io/ent/dialect/entsql) for unfamiliar mappings. Consult target-version PostgreSQL [types](https://www.postgresql.org/docs/current/datatype.html), [constraints](https://www.postgresql.org/docs/current/ddl-constraints.html), and [CREATE TABLE](https://www.postgresql.org/docs/current/sql-createtable.html) for defaults, special types, null uniqueness, or partition restrictions. Apply [source policy](00-sources.md) when selected versions differ.
