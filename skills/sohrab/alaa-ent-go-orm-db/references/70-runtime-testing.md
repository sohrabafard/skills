# Runtime integration and verification

Own client/pool setup, instrumentation, and acceptance evidence. Choose checks for changed behavior; reuse equivalent repository gates.

## Client and pool ownership

Reuse a long-lived Ent client and bounded pool per database configuration, never per request. Assign service-lifecycle shutdown ownership. Clean up failed setup without closing borrowed pools. Preserve the supported PostgreSQL driver.

For new pgx integration, verify selected `github.com/jackc/pgx/v5/stdlib`. Driver name `"pgx"` differs from `dialect.Postgres`. For a lifecycle-owned `*database/sql.DB`:

```go
drv := entsql.OpenDB(dialect.Postgres, db)
client := ent.NewClient(ent.Driver(drv))
```

Here ent is the generated package; entsql aliases `entgo.io/ent/dialect/sql`. Import `entgo.io/ent/dialect`. Use authorized bounded PingContext; construction proves no access. `client.Close()` delegates to `driver.Close()` and closes the wrapped `*sql.DB`. A borrowed DB remains its lifecycle owner's responsibility. Close owned resources only after users stop.

Budget MaxOpenConns across replicas, workers, deployment overlap, and reserve. Distinguish application/PgBouncer server pools. Derive idle limits/lifetimes from observed load/infrastructure. Invent no universal counts; unlimited defaults are not a plan. Transactions occupy connections until completion.

Before changing protocol/caching, inspect pgx/PgBouncer versions, pooling mode, max_prepared_statements, and current maintainer guidance. Do not default to simple protocol or disabled caches. Preserve application/migration/admin role separation, bound values, verified TLS, and the secret provider. Include no real DSN in artifacts.

## Driver type mapping

When types, bindings, driver modes, or pool construction change, trace values through the actual Ent/driver path.
Record concrete Go types/packages, scalar/array bindings, PostgreSQL types, codecs, and execution mode. Include used named, pointer, and collection variants.
Generated schema types and compilation do not prove encoding or decoding compatibility.

pgx `QueryExecModeExec` infers parameter types from Go values without server parameter descriptions. SQL casts cannot supply missing client encoding plans.
Scalar `driver.Valuer` support does not establish array support. Inspect bindings: ordinary `IDIn` expands scalars; a custom array predicate binds a collection.
Changing binding shape also changes parameter counts and can change plans; verify those costs before substituting it.

Check the pinned driver's codecs and Go-type mappings before registering anything. Register only missing mappings supported by the selected codec.
Resolve unknown PostgreSQL codecs and their dependencies first. Initialize every new connection through its actual factory.
Configure hooks before constructing pools; changing a configuration copy changes neither the factory nor existing connections.
Use `pgxpool.Config.AfterConnect` for that pool or `stdlib.OptionAfterConnect` with `stdlib.OpenDB` configuration.
`stdlib.OpenDBFromPool` uses the existing pool's initialization. A separate `sql.Open` pool inherits neither its connections nor hooks.

Test affected generated/raw paths with actual parameter/scan types, execution mode, and applicable scalar, collection, empty, nil, and boundary values.
Exercise multiple and replacement connections when initialization changes. Preserve the deployed protocol/proxy semantics.
For regressions, demonstrate failure before the fix and success after under the same configuration; an easier type/mode is insufficient.
Local codec tests isolate encoding; authorized disposable PostgreSQL integration verifies the full path. Report unavailable execution through the acceptance rules below.

Checked against pgx v5.12.0 and Ent v0.14.6 on 2026-11-05; this does not require upgrading existing dependencies.
For unfamiliar mappings or changed versions, consult [execution modes](https://pkg.go.dev/github.com/jackc/pgx/v5#QueryExecMode), [type mappings](https://pkg.go.dev/github.com/jackc/pgx/v5/pgtype#Map.RegisterDefaultPgType), and [connection hooks](https://pkg.go.dev/github.com/jackc/pgx/v5/stdlib#OptionAfterConnect).

## Resources and observability

Propagate context into terminal operations. Bound page/edge/batch sizes, bulk writes, and worker concurrency. For builder sharing/projections, read [queries](30-ent-queries.md); for deadlines/retries, read [transactions](60-transactions-security.md).

Use project logs/metrics for relevant latency distributions, affected rows, query count, pool waits, and errors. Ent debug logs can expose parameters; redact per policy. Prefer fingerprints/safe parameter classes. Traces, catalogs, and pg_stat_statements are optional authorized evidence, not mandatory installations. Raising connection limits does not diagnose slow queries or lock convoys.

## Checks by change

| Change | Evidence when execution is available |
| --- | --- |
| Schema/generator/flags | Generation/build succeeds; generated diff and migration SQL reviewed. |
| Driver/type/mode/pool wiring | Actual Ent/raw types and bindings, relevant nil/empty/boundary values, and new/replacement connections under the intended protocol/proxy setup. |
| Types/nullability/constraints/edges | PostgreSQL valid, invalid, boundary, and referential cases. |
| Tenant policy | Relevant cross-tenant reads/writes/associations, uniqueness, and raw bypass cases. |
| Projection/eager loading | Response contract, SQL columns/query count, cursor/FK dependencies. |
| Index/predicate | Same query/representative binds and data; plans plus write/storage costs. |
| Migration/backfill | Fresh schema/current-revision upgrade, lock/transaction boundaries, recovery. |
| Transactions/concurrency | Commit/rollback, cancellation, contention, duplicate requests, retry semantics. |

Run targeted `go test ./path/to/changed/package/...`, applicable go vet, and required repository gates. Use `go test -race` for changed concurrency when platform/CGO prerequisites exist. Run govulncheck when policy or dependency risk requires it. Report unavailable tools/checks as skipped.

Use verified disposable PostgreSQL with target major/extensions, synthetic bounded fixtures, and cleanup ownership. Reachability proves no disposable status. SQLite smoke tests prove no PostgreSQL types, indexes, constraints, locks, or migrations.

## Acceptance and consultation

For performance claims, record query, parameter classes, distribution, database version, plan, and measurement conditions. Separate planning/execution; record material cache, concurrency, volume, and instrumentation effects. Compare workload costs/latency distributions, not one favorable timing. Index selection proves no end-to-end improvement.

Stop after applicable gates pass; repeat only for changes, failures, or unresolved evidence. Without execution, deliver reviewable code/plan and mark runtime acceptance incomplete. Never weaken a failed required gate.

Consult [Ent SQL integration](https://entgo.io/docs/sql-integration/) and [Go pools](https://go.dev/doc/database/manage-connections) for unfamiliar ownership/configuration. Check [pgx](https://github.com/jackc/pgx) and [PgBouncer](https://www.pgbouncer.org/config.html) before protocol changes. Use [Ent testing](https://entgo.io/docs/testing/) and [race-detector prerequisites](https://go.dev/doc/articles/race_detector) for unfamiliar test setups.
