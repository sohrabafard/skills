# Store selection, Postgres design, and tenant boundaries

## A) Which store owns this fact

Decide the store before the schema, once per fact, and record the decision where the service documents its data
model. Reason: a fact that ends up in two stores acquires two truths, and nobody can say afterwards which one the
business meant.

- **Postgres owns every business fact the service must be able to state authoritatively after a total cache loss.**
  This is the default and needs no justification.
- **Redis holds only copies Postgres can rebuild** — cache entries, locks, rate-limit counters, edge dedupe keys.
  `rediskit/doc.go:12-13` states the same invariant for the Go kit: Redis is a cache and a cross-pod freshness
  signal, never a source of truth.
- **ClickHouse holds the analytical lane**: append-heavy event and metric data read by aggregate, never read
  row-by-row to answer a request that must reflect a write that just committed. On this kit the ClickHouse lane is
  read-only by construction — `chkit/config.go:128-132` pins the session setting `readonly: 2`, the client exposes
  no `Exec`, and `chkit/client_integration_test.go:123-127` fails the build if a `CREATE TABLE` succeeds over it.
  The kit therefore contains no ClickHouse DDL, migration, or materialized-view surface at all. Schema, engine,
  `ORDER BY`, materialized views, projections, and TTL are `/clickhouse-performance-schema-ops`
  (`$clickhouse-performance-schema-ops`), and the DDL ships outside the kit.
- **MongoDB is used where the repository already uses it, or where the request explicitly asks for it**, under
  `/alaa-mongodb-patterns` (`$alaa-mongodb-patterns`).
- **Do not add a store the request did not ask for.** Reason: every added store adds an availability dependency, a
  backup and restore obligation, and a consistency seam that then has to be designed rather than discovered.

How much staleness a derived copy may carry is a consistency budget owned by `/alaa-system-design`
(`$alaa-system-design`) `references/30-data-and-consistency.md`. Bring it the read's freshness requirement; it
decides. Who may write a given table, and where the component boundary falls, is the same skill's.

**Not every service in this fleet has Postgres.** `alaa-go-chi docs/CONSUMERS.md:23` records `wa-api` running the
ClickHouse lane with no pgkit, no rediskit, no mqkit, and no outboxkit. Read the service's configured lanes before
applying any rule below to it; a Postgres rule applied to a service with no Postgres produces confident nonsense.

## B) The write-model is the source of truth

- Design core OLTP tables in 3NF, or BCNF where that is no harder to read.
- Keep exactly one authoritative column for any value that can be edited. Two editable copies diverge, and the
  divergence is discovered by a customer.
- Denormalization in a core truth table requires a measured query pattern that shows it is necessary, recorded
  beside the schema as a deliberate trade-off. Reason: denormalization moves a correctness obligation from the
  database into every future writer.

## C) Enforce integrity in the database, not only in code

- Encode invariants as `NOT NULL`, `FOREIGN KEY`, `UNIQUE`, and `CHECK` constraints. Application-level validation
  runs only where the application runs; the constraint holds against a migration, a backfill script, and a console
  session too.
- State the referential action explicitly and record the intent: `ON DELETE RESTRICT` / `CASCADE` / `SET NULL`,
  `ON UPDATE RESTRICT` / `CASCADE`.
- Default to `RESTRICT`. A cascade deletes rows nobody is looking at during the delete.
- A foreign key pointing into a partitioned parent has its own failure class, SQLSTATE 42830 — that is
  `/alaa-partitioned-table-fk-audit` (`$alaa-partitioned-table-fk-audit`).

## D) Multi-tenant boundary

- Every tenant-scoped table carries `tenant_id NOT NULL`. A row without it is a bug, not a special case.
- Every uniqueness rule on a tenant-scoped table is tenant-aware: `UNIQUE (tenant_id, …)` unless global uniqueness
  is the stated requirement.
- Every index serving a frequent query leads with `tenant_id`, so a plan that loses the predicate cannot scan
  another tenant's rows cheaply.
- Every query filters by tenant. Cross-tenant access goes through one explicit, audited system path.
- Reason for all four: the failure mode is a cross-tenant read that returns `200` with well-formed data, so no
  client error is raised and no test asserting on status and schema will see it. Tenant isolation as a trust
  boundary is `/alaa-security-review` (`$alaa-security-review`).

Tenancy strategy: use shared schema plus `tenant_id` and document it. Row-level security is adoptable only where
the repository already runs it, and on the Go kit it is not adoptable at all today — see the `SET LOCAL` rule in
`30-concurrency-projections-and-pooling.md`.

## E) Read performance without corrupting truth

- Build read-models explicitly as a view, a materialized view, or a summary table. Truth tables stay normalized and
  authoritative; projections are derived, rebuildable, and may be eventually consistent.
- Every derived field — a count, a last-state, an aggregate — ships with its update strategy and that strategy is
  idempotent, because the update runs at least once. The strategies are in
  `30-concurrency-projections-and-pooling.md`.

## F) Audit and operations

- Keep history in append-only or audit tables. Do not overwrite a business-critical fact without an audit trail:
  the overwrite is discovered during an investigation, when the evidence is already gone.
- Index to match real query patterns; make migrations lock-safe and reversible per
  `20-schema-migrations-and-performance.md`.

## G) Identifier naming policy

- New persistence identifiers are lower_snake_case: tables, columns, indexes, constraints, sequences, join tables,
  foreign-key names, check-constraint names.
- Do not introduce a mixed-case identifier that PostgreSQL then requires double quotes to address. Every future
  hand-written query has to remember the quoting, and the one that forgets fails at runtime.
- Do not mirror a camelCase API or PHP name into a schema identifier for ORM convenience.
- Existing quoted mixed-case identifiers are legacy debt: plan the cleanup, and document any compatibility layer
  with its exact removal path rather than extending the mixed-case surface.
- Where Doctrine DBAL, Laravel schema tooling, and raw SQL meet, pick one canonical unquoted spelling and keep it
  stable across migrations, models, tests, and docs.

## H) Performance principles

- Prefer simple, predictable queries and a stable, minimal index set. Every index is justified by a named query or
  invariant, because an index nobody can name a query for is write cost with no read benefit.
- Avoid N+1: fetch in batches or eager-load deliberately. When the loop's iteration count grows with tenants, rows,
  or history, `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) owns which of the four
  resolutions applies and the maximum the batch must carry; this file owns the query and index shape the
  resolution lands on.
- **A list route over a collection that grows with tenant data does not paginate by `OFFSET`.**
  `/alaa-keyset-pagination` (`$alaa-keyset-pagination`) owns the cursor, the ordering tuple, the prev/next
  envelope, and the conditions under which offset is still permitted. This file owns the index that serves the
  ordering that skill derives, and states the rule nowhere else.
- Constraints are an optimization tool as well as a correctness tool: the planner uses uniqueness and
  not-null-ness.
