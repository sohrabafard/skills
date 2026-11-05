# Runtime integration and verification

## Contents

- [Client and connection ownership](#client-and-connection-ownership)
- [Observability and resource bounds](#observability-and-resource-bounds)
- [Checks by change](#checks-by-change)
- [Evidence and acceptance](#evidence-and-acceptance)

## Client and connection ownership

Reuse a long-lived Ent client and bounded pool per database configuration. Never open a pool per request.
Assign shutdown ownership to the service lifecycle. Close resources created during failed setup, but never close a borrowed pool.
Preserve the existing supported PostgreSQL driver.
For new pgx integration, use `github.com/jackc/pgx/v5/stdlib` with Ent's SQL driver; verify the selected pgx version.
The driver name `"pgx"` is distinct from Ent's dialect name `dialect.Postgres`.

For an already configured, lifecycle-owned `*database/sql.DB` named `db`, the adapter is:

```go
drv := entsql.OpenDB(dialect.Postgres, db)
client := ent.NewClient(ent.Driver(drv))
```

Imports: the application's generated `ent`, `entgo.io/ent/dialect`, and `entgo.io/ent/dialect/sql` aliased as `entsql`.
Test connectivity with an authorized bounded `PingContext`; successful client construction does not prove access.
Close the client once its users have stopped, according to the pool ownership contract.

Budget `MaxOpenConns` across replicas, workers, deployment overlap, and operational reserve.
Account separately for application connections and PgBouncer server pools.
Set idle limits, idle lifetime, and maximum lifetime from observed load and infrastructure limits.
Unlimited defaults are not a capacity plan. Do not invent universal connection counts.
An active transaction occupies its connection until it ends.

Prepared-statement behavior depends on pgx, PgBouncer version, pooling mode, and `max_prepared_statements`.
Do not prescribe simple protocol or disable caches by default.
Inspect actual configuration and current maintainer compatibility guidance before changing protocol mode.
Preserve established runtime, migration, and administrative role separation.
Use bound parameters, verified TLS settings, and the configured secret provider. Never include a real DSN in an artifact.

Sources: [Ent database/sql integration](https://entgo.io/docs/sql-integration/), [Go connection pools](https://go.dev/doc/database/manage-connections), [pgx](https://github.com/jackc/pgx), [PgBouncer configuration](https://www.pgbouncer.org/config.html).

## Observability and resource bounds

Propagate request context into Ent terminal operations. Do not share mutable query or mutation builders across goroutines.
Bound page sizes, eager-loaded edges, batch sizes, bulk writes, and worker concurrency.
Derive deadlines and lock/statement timeouts from request budgets and existing reliability policy.
Use the [transaction reference](60-transactions-security.md) for write retry rules.

Use registered project logs and metrics. Inspect latency distributions, affected rows, pool wait, errors, and query count when relevant.
Ent debug logging can expose parameters. Redact sensitive values according to project policy.
Prefer normalized fingerprints and safe parameter classes in performance reports.
Treat tracing, database catalogs, and `pg_stat_statements` as optional authorized evidence sources, not mandatory installations.
Increasing a connection limit does not diagnose a slow query or lock convoy.

## Checks by change

Choose checks for changed behavior. Reuse project commands implementing the same gate.

| Change | Evidence required when the environment is available |
| --- | --- |
| Schema, generator, or feature flags | Generation succeeds; affected code builds; generated diff and migration SQL reviewed |
| Types, nullability, constraints, or relationships | PostgreSQL cases for valid, invalid, boundary, and referential behavior |
| Tenant access or policy | Relevant cross-tenant reads, mutations, associations, uniqueness, and raw-SQL bypass cases |
| Projection or eager loading | Response contract unchanged; SQL columns/query count inspected; cursor/FK dependencies retained |
| Index or predicate | Same query and representative parameters/data; plan evidence; write/storage tradeoff |
| Migration or backfill | Fresh schema and representative upgrade; transaction/lock boundaries; recovery procedure |
| Transactions or concurrency | Commit, rollback, cancellation, contention, duplicate requests, and retry semantics |

Run targeted Go tests first, then required repository gates. Typical commands are:

```bash
go test ./path/to/changed/package/...
go vet ./path/to/changed/package/...
```

Use `go test -race` for changed concurrency when platform/CGO prerequisites are available.
Run `govulncheck` when required by project policy or the dependency change's risk.
Do not install absent test tools without authorization. Report skipped commands as skipped.

Use the target PostgreSQL major version for dialect-sensitive tests.
SQLite can test basic Ent behavior; it does not prove PostgreSQL types, indexes, constraints, locks, or migrations.
Use a verified disposable database, synthetic fixtures, bounded sizes, and explicit cleanup ownership.
Never repurpose a live database merely because it is reachable.

Sources: [Ent testing](https://entgo.io/docs/testing/), [Go test command](https://pkg.go.dev/cmd/go#hdr-Test_packages), [Go race detector](https://go.dev/doc/articles/race_detector).

## Evidence and acceptance

For a performance claim, record the query, parameter classes, data distribution, database version, plan, and measurement conditions.
Separate planning and execution. Note cache state, concurrency, result volume, and instrumentation overhead when material.
Compare workload costs and latency distributions, not one favorable timing.
An index in a plan proves selection for that plan, not end-to-end speedup.

Stop after applicable gates pass. Repeat checks only for changes, failures, or unresolved evidence affecting them.
When execution is unavailable, deliver reviewable code or a plan and mark runtime acceptance incomplete.
Never weaken a failed required gate to finish the task.
