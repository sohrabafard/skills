# Set up Ent or adopt it in an existing service

Read when adding Ent to a Go project or replacing handwritten PostgreSQL access. This file owns adoption sequencing and parity. Before bootstrap or version choices, read [10-go-and-generation.md](10-go-and-generation.md). It owns the Go minimum, freshness checks, dependency alignment, and generation commands.

## Establish the adoption boundary

Distinguish new-project setup from existing-database adoption. Replacing application SQL does not require changing the stored schema. Resolve the module, use cases, repository interfaces, PostgreSQL version, and acceptance evidence. Inspect workspace/module files, generators, database setup, query call sites, migrations, and tests. Trace consumers through repository methods to responses, jobs, and transactions.

For each use case, record inputs, selected columns, filters, ordering, pagination, effects, errors, and transaction boundaries. Preserve tenant, authorization, soft-delete, concurrency, and public-response behavior. Identify other writers, including jobs, triggers, services, and SQL outside the selected repository. Start with the smallest useful vertical slice; continue until the requested scope is covered.

Apply the main skill's scoped installation and database authority rules.

## New project

1. Resolve the module path. Initialize only a missing module; preserve existing modules/workspaces.
2. Run the pinned bootstrap commands in [10-go-and-generation.md](10-go-and-generation.md). Select the PostgreSQL driver through the runtime reference.
3. Define the first entity through [20-schema-design.md](20-schema-design.md). Regenerate through the generation owner.
4. Wire a service-owned client using [70-runtime-testing.md](70-runtime-testing.md). Follow existing configuration, secret, context, and lifecycle conventions.
5. Prepare schema creation or migration through [50-migrations.md](50-migrations.md), using only an authorized target. Code generation alone requires no database.
6. Implement one complete use case through [30-ent-queries.md](30-ent-queries.md), then perform applicable checks through the runtime reference.

## Adopt an existing schema before changing queries

Reconcile migration history with authorized inspection or a trusted schema export. Record relevant schemas/tables, columns, types, nullability, defaults, IDs/sequences, relationships, constraint names, indexes, views, triggers, RLS, and extensions. Do not infer deployed structure from structs or tutorials. A partial model must not become desired state that deletes unmodeled objects.

Map Ent names onto existing storage through [20-schema-design.md](20-schema-design.md). Preserve IDs, sequence/default ownership, nullability, enum/type semantics, FK direction, and join tables. This fragment maps `app.customer_records(customer_id, full_name)`; it is not a complete schema:

```go
// In Customer.Fields():
field.Int64("id").StorageKey("customer_id"),
field.String("name").StorageKey("full_name"),

// In Customer.Annotations():
entsql.Annotation{Table: "customer_records"},
entsql.Schema("app"),
```

Here `field` is `entgo.io/ent/schema/field` and `entsql` is `entgo.io/ent/dialect/entsql`. Match actual column types and nullability. For non-default schemas, read [80-advanced-ent.md](80-advanced-ent.md) before configuring runtime schema qualification; verify `sql/schemaconfig` in the pinned generator and inspect emitted SQL. A schema annotation alone does not prove the client accesses the intended schema.

For unfamiliar storage mappings, consult [field storage keys](https://entgo.io/docs/schema-fields/#storage-key), [table annotations](https://entgo.io/docs/schema-annotations/#custom-table-name), and [schema configuration](https://entgo.io/docs/multischema-migrations/#controlling-the-ent-client).

Retain the migration runner and assign one owner per object. Do not recreate tables, run automatic schema creation, reset history, or change storage for generated naming. Deliver application-only adoption when storage is unchanged. Before transferring migration ownership, read [50-migrations.md](50-migrations.md) for baseline handling. Verify the baseline matches existing state. Do not replay creation DDL against populated tables or mark unverified revisions applied. Inspect every diff, including external objects.

## Make SQL and Ent coexist safely

Read [70-runtime-testing.md](70-runtime-testing.md) before client integration. Reuse its `*sql.DB` adapter when that pool already exists. Native `*pgxpool.Pool` and `pgx.Tx` are different types; do not pass them to `entsql.OpenDB`. For a shared native pool, inspect the selected pgx version's [stdlib adapter](https://pkg.go.dev/github.com/jackc/pgx/v5/stdlib#OpenDBFromPool). Verify its pool, idle-connection, and close semantics before choosing it over a separately budgeted pool. Preserve one lifecycle owner.

Sharing a pool does not share a transaction. Move an entire atomic use case to an Ent transaction, or use a verified adapter for the existing transaction. Read [60-transactions-security.md](60-transactions-security.md) before mixing Ent and raw SQL. Keep both on the same transaction executor. Do not split an atomic operation across independent transactions or invent a native-pgx transaction conversion. Preserve isolation, locks, cancellation, retries, and rollback outcomes.

## Convert and prove one vertical slice

Keep the repository/service contract stable while replacing its implementation. Translate each query through [30-ent-queries.md](30-ent-queries.md). Map Ent errors back to existing domain errors. Preserve absence versus multiplicity, NULL versus zero versus omitted input, deterministic ordering, cursor semantics, affected-row expectations, and tenant/lifecycle predicates.

Inspect emitted SQL for returned columns, predicates, joins, statements, and locks. Use the projection contract in the query reference and the query-to-index contract in [40-index-design.md](40-index-design.md). Do not add an index solely because the builder changed.

Retain bounded raw SQL when Ent cannot preserve the operation or a database feature requires it. Record its reason and owner. Follow the raw-SQL security procedure for binding, authorization, and transactions; never substitute weaker behavior to eliminate SQL syntax.

Run old and new implementations against equivalent synthetic PostgreSQL fixtures. Compare public values, response shape, errors, side effects, and relevant concurrency outcomes. Use separate test state or rollback so writes do not contaminate the comparison. Never dual-execute live writes as a parity test. Include relevant missing rows, duplicate keys, NULLs, zero/clear updates, ordering ties, cross-tenant access, and transaction failures. Follow [70-runtime-testing.md](70-runtime-testing.md) for applicable execution and performance evidence.

Switch the selected callers only after applicable parity gates pass. Retain rollback capability during a staged rollout where required. Remove the old path and now-unused dependencies only after checking all consumers and the rollback requirement. Keep externally owned SQL objects and intentional escape hatches. Report converted paths, remaining SQL, mapping/migration decisions, actual checks, and untested behavior.

## Stop conditions

Stop the affected conversion if storage mapping, required invariants, transaction ownership, or behavior parity remains unresolved. Stop schema work on unexpected DDL or an unverified baseline. Continue independent source/code preparation when tools or database evidence are unavailable; mark runtime acceptance incomplete. Follow the main retry bound. Finish when the requested adoption scope and applicable parity gates pass; do not expand into an unrelated ORM rewrite.
