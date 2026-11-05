# Design the Ent schema and PostgreSQL invariants

Read for entity, field, relationship, key, tenant, or lifecycle changes. This file owns the stored-data contract. Use [40-index-design.md](40-index-design.md) for access paths and [50-migrations.md](50-migrations.md) for rollout. Use [60-transactions-security.md](60-transactions-security.md) for authorization and hooks.

## Contents

- [Establish the stored-data contract](#establish-the-stored-data-contract)
- [Map types deliberately](#map-types-deliberately)
- [Represent fields in Ent](#represent-fields-in-ent)
- [Keep relationships and tenants consistent](#keep-relationships-and-tenants-consistent)
- [Choose lifecycle and physical boundaries](#choose-lifecycle-and-physical-boundaries)
- [Accept the schema](#accept-the-schema)

## Establish the stored-data contract

Identify entity identity, ownership, lifecycle, cardinality, and important queries before choosing columns. Separate invariants for all database writers from application-only validation. Preserve existing IDs, table names, public identifiers, and null semantics unless requested otherwise. Explain new choices. An optimization request does not authorize unrelated redesign.

Normalize relationships and repeated facts. Use edge schemas for relationship attributes: role, position, enrollment time, or attempt status. Denormalize only for a measured access pattern with an assigned reconciliation owner. JSONB does not enforce embedded references. Store ordering explicitly when it has business meaning.

Specify each material field's requiredness, type, unit, default owner, mutability, uniqueness scope, and deletion behavior. Name constraints used in reporting or recovery. Enforce uniqueness in PostgreSQL; concurrent writers can pass application prechecks. CHECK accepts null results; add NOT NULL where null is invalid. Enforce cross-row/table invariants with suitable UNIQUE, FK, or exclusion constraints, not CHECK expressions reading other rows.

Use lower_snake_case for new storage identifiers and stable constraint names. Avoid quoted mixed-case identifiers and truncation collisions.
UNIQUE ordinarily permits multiple NULLs. When NULL must conflict, verify version-supported `NULLS NOT DISTINCT` or another suitable constraint.
Inspect generated DDL before claiming either null-uniqueness behavior.

Sources: [Ent schema](https://entgo.io/docs/schema-def/), [Ent edges](https://entgo.io/docs/schema-edges/), [PostgreSQL constraints](https://www.postgresql.org/docs/current/ddl-constraints.html).

## Map types deliberately

| Data | Decision |
|---|---|
| Internal integer identifier | Preserve existing types. For a new 64-bit Go contract, declare `field.Int64("id")`. Verify generated SQL type and sequence/identity behavior. |
| Public or distributed identifier | Use PostgreSQL `uuid` with a declared Go dependency and generation owner. Preserve required UUIDv7 semantics; do not substitute v4. |
| Instant | Use `timestamptz` and an explicit UTC convention at boundaries. Preserve a separate IANA timezone if future local-calendar rules need it. |
| Civil date or local time | Choose `date`, local time, or local timestamp according to meaning. Do not convert a birthday into a midnight UTC instant. |
| Duration | Store a documented integer unit or a deliberately mapped interval. Do not use floating-point seconds without an explicit precision contract. |
| Exact money or measured decimal | Use integer minor units with currency/unit, or NUMERIC with an exact Go scanner/value type. SQL numeric does not fix Go float rounding. |
| Text | Use text or varchar with a justified semantic length. Do not choose fixed char or arbitrary varchar limits for an assumed performance advantage. |
| Optional value | Decide null versus zero/empty meaning. Use `Optional().Nillable()` where the generated entity must preserve that difference. |
| JSON document | Use JSONB for suitable variable document content. Keep stable, constrained, frequently joined identifiers in typed columns or relations. |
| Finite state | Decide between Ent's string-backed enum, CHECK, a lookup table, and a native PostgreSQL enum. Include change/removal compatibility in the decision. |
| Arrays, ranges, network, spatial types | Use a supported typed mapping and driver scanner. Use relationship tables when elements need individual FKs or attributes. |

Ent provides a built-in integer SQL ID. PostgreSQL 18 documents `uuidv7()`; verify another generator for earlier servers. Go version does not establish database function availability. UUIDv7 is time-ordered, not an authorization secret. Handle application generator errors instead of using panic-based defaults.

PostgreSQL timestamps have microsecond resolution; check equality and cursor round trips. Timestamptz does not preserve the source timezone name. Define application and database defaults separately. `UpdateDefault(time.Now)` does not update external writes through a database trigger.

Sources: [Ent fields](https://entgo.io/docs/schema-fields/), [numeric types](https://www.postgresql.org/docs/current/datatype-numeric.html), [date/time types](https://www.postgresql.org/docs/current/datatype-datetime.html), [character types](https://www.postgresql.org/docs/current/datatype-character.html), [JSON types](https://www.postgresql.org/docs/current/datatype-json.html), [UUID functions](https://www.postgresql.org/docs/current/functions-uuid.html).

## Represent fields in Ent

Edit schema source, not generated entities. Verify `SchemaType` storage and `GoType`/scanner conversion in generated output. `Optional()` changes requiredness. `Nillable()` changes Go representation; alone it does not permit SQL NULL. `Immutable()` removes update setters but permits direct SQL changes. Ent validators such as `Min`, `MaxLen`, and `NotEmpty` do not prove database enforcement; inspect DDL.

This illustrative model requires an `int64` Course ID before adding its edge. Preserve existing identifier types when adapting it.

```go
package schema

import (
    "time"

    "entgo.io/ent"
    "entgo.io/ent/dialect"
    "entgo.io/ent/dialect/entsql"
    entschema "entgo.io/ent/schema"
    "entgo.io/ent/schema/field"
)

type Content struct{ ent.Schema }

func (Content) Fields() []ent.Field {
    return []ent.Field{
        field.Int64("id"),
        field.Int64("tenant_id").Immutable(),
        field.Int64("course_id"),
        field.String("title").NotEmpty().MaxLen(240),
        field.Enum("status").Values("draft", "published").Default("draft"),
        field.Int64("duration_ms").Default(0).Min(0),
        field.Time("created_at").
            Default(func() time.Time { return time.Now().UTC() }).
            Immutable().
            SchemaType(map[string]string{dialect.Postgres: "timestamptz"}),
        field.Time("deleted_at").Optional().Nillable().
            SchemaType(map[string]string{dialect.Postgres: "timestamptz"}),
    }
}

func (Content) Annotations() []entschema.Annotation {
    return []entschema.Annotation{
        entsql.Checks(map[string]string{
            "contents_duration_nonnegative": "duration_ms >= 0",
        }),
    }
}
```

The example validates duration in Ent and PostgreSQL. Decide other invariants explicitly. Ent enums use PostgreSQL string storage by default; inspect migrations before claiming native enums or state constraints. Use `entsql.DefaultExpr(...)` for database expression defaults; verify create-builder omission and returned values. PostgreSQL DEFAULT cannot reference another column. Use a suitable generated column, application assignment, or trigger instead.

Use mixins only for behavior shared by every adopting schema. Inspect generated changes across affected tables after a mixin edit. Preserve storage names through supported `StorageKey` or table annotations during code-level renames.

Sources: [Ent field API](https://pkg.go.dev/entgo.io/ent/schema/field), [Ent SQL annotations](https://pkg.go.dev/entgo.io/ent/dialect/entsql), [PostgreSQL CREATE TABLE defaults](https://www.postgresql.org/docs/current/sql-createtable.html).

## Keep relationships and tenants consistent

Specify cardinality and ownership before choosing edge methods. Match explicit FK type and optionality to the referenced ID and edge. For many contents belonging to one course:

```go
// Course declares edge.To("contents", Content.Type).
edge.From("course", Course.Type).
    Ref("contents").Field("course_id").Unique().Required()
```

Import `entgo.io/ent/schema/edge` and define the matching Course schema. This ID relationship does not prove tenant-pair integrity. Keep FKs enabled unless an approved architecture provides another integrity mechanism.

For shared tables, obtain tenant identity through the trusted application boundary. Require tenant fields on tenant-owned rows. Independent tenant/course FKs permit cross-tenant pairing. Inspect migrations for the composite relationship, illustrated by this desired-state sketch:

```sql
ALTER TABLE public.courses
  ADD CONSTRAINT courses_tenant_id_id_key UNIQUE (tenant_id, id);
ALTER TABLE public.contents
  ADD CONSTRAINT contents_tenant_course_fk
  FOREIGN KEY (tenant_id, course_id)
  REFERENCES public.courses (tenant_id, id);
```

Require NOT NULL on mandatory pair members and choose ON DELETE behavior. Use [50-migrations.md](50-migrations.md) before applying this sketch. If Ent cannot express the composite FK, assign a migration extension or SQL owner. Preserve that object in future diffs; a query filter cannot replace pair integrity. Use IDs supported by the pinned generator. Edge-schema composite IDs do not establish general composite node-ID support.

Sources: [Ent edge fields](https://entgo.io/docs/schema-edges/#edge-field), [PostgreSQL FK constraints](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK).

## Choose lifecycle and physical boundaries

Choose hard delete, soft delete, archival, and restoration semantics. Decide whether deleted natural keys remain reserved or become reusable. Live-row partial uniqueness permits later restoration conflicts; define their handling before implementing restore. Use [60-transactions-security.md](60-transactions-security.md) for filters/hooks and [40-index-design.md](40-index-design.md) for index predicates.

Partition only for justified size, retention, pruning, or maintenance needs. Check version-specific unique/FK restrictions before choosing the partition key. Assign partition creation, retention, and pruning owners. Keep schema names and migration search paths explicit; reject request-controlled schema selection. Use [80-advanced-ent.md](80-advanced-ent.md) for views, external objects, and multi-schema integration.

## Accept the schema

Return the field/edge contract, invariant-to-constraint mapping, representability gaps, and migration impact. Generate and inspect DDL before claiming enforcement. Use [70-runtime-testing.md](70-runtime-testing.md) for runtime checks. Cover relevant duplicates, nulls, invalid states, cross-tenant edges, deletion restrictions, restore conflicts, and exact-value round trips. Block dependent changes when ownership, null semantics, or representability remains unresolved. Name the missing decision. Code generation does not prove production readiness.
