# Source map and freshness

Read this before repeating any version-sensitive or platform-sensitive claim from this skill.

## Source order

1. **The kit's Go source**, for every claim about how an Ala Go service actually behaves: `alaa-go-chi`'s
   `pgkit/`, `rediskit/`, `chkit/`, `outboxkit/`, `configkit/keys.go`, `linttools/`, and `docs/CONSUMERS.md`. A
   decision log, a changelog entry, or a design document records what was agreed; only source records what runs.
   Two knobs in this skill were ratified and are still absent from code — see
   `60-configuration-and-kit-gaps.md`.
2. **The service's own repository**: migrations, models, factories, seeders, tests, query call sites, database and
   Redis configuration, `.env.example`, and runtime documentation. Plus the live schema and real `EXPLAIN` output
   where database access exists. Repository truth outranks every table in this skill.
3. **Official PostgreSQL documentation** (current release):
   - https://www.postgresql.org/docs/current/
   - `CREATE INDEX`: https://www.postgresql.org/docs/current/sql-createindex.html
   - Row security policies: https://www.postgresql.org/docs/current/ddl-rowsecurity.html
   - Explicit locking: https://www.postgresql.org/docs/current/explicit-locking.html
   - Transaction isolation: https://www.postgresql.org/docs/current/transaction-iso.html
   - `EXPLAIN`: https://www.postgresql.org/docs/current/using-explain.html
   - Error codes (the SQLSTATEs named in `30-concurrency-projections-and-pooling.md`):
     https://www.postgresql.org/docs/current/errcodes-appendix.html
4. **Official Redis and Laravel documentation**:
   - Redis: https://redis.io/docs/latest/
   - Redis distributed locks: https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/
   - Laravel database: https://laravel.com/docs/13.x/database
   - Laravel migrations: https://laravel.com/docs/13.x/migrations
   - Laravel cache, including the `failover` driver, `flexible`, locks, and funnel:
     https://laravel.com/docs/13.x/cache
   - Laravel Redis, including client, retry and backoff, serializer options: https://laravel.com/docs/13.x/redis
   - Laravel Octane: https://laravel.com/docs/13.x/octane
   - phpredis releases: https://pecl.php.net/package/redis
   - predis releases: https://github.com/predis/predis/releases
5. **Official Go client documentation**:
   - go-redis v9, the client `rediskit` wraps: https://pkg.go.dev/github.com/redis/go-redis/v9
   - go-redis production guidance: https://redis.io/docs/latest/develop/clients/go/produsage/
   - pgx v5, whose context handling `30-…` relies on: https://pkg.go.dev/github.com/jackc/pgx/v5
6. **PgBouncer documentation**, for transaction-pooling behaviour and `max_prepared_statements`:
   https://www.pgbouncer.org/config.html
7. **Community posts and StackOverflow**: use for troubleshooting an unusual error or finding search keywords
   only. Re-check every operational claim against an official source and the actual query plan.

## Packages this skill names but the kit does not contain

`singleflight`, `gobreaker`, `redsync`, `redis_rate`, and `rueidis` are absent from `alaa-go-chi` — from every
`.go` file, from `go.mod`, and from `go.sum`; `golang.org/x/sync` is present only as an indirect dependency.
Adopting any of them is a new direct dependency, so the package choice goes to `/alaa-golang` (`$alaa-golang`)
`references/40-production-ready-package-catalog.md`, and whether the mechanism belongs in the kit rather than in
one service goes to `/alaa-go-chi-development` (`$alaa-go-chi-development`). Do not read their appearance in this
skill as evidence that they are available.

## Freshness triggers

Verify against a primary source before acting when the task mentions:

- `latest`, `current`, `upgrade`, `security`, a CVE, a new PostgreSQL or Redis major version, or a managed-service
  version change.
- RLS, tenant isolation, concurrent indexes, partitioning, replication, locks, deadlocks, transaction isolation,
  pooling, PgBouncer, cache serialization, or Redis eviction.
- A query or a migration expected to run against a large table.
- phpredis or predis client choice, the Laravel cache `failover` driver, Octane connection handling, go-redis pool
  and timeout defaults, or any Redis-down fallback design. Client behaviour changes across versions; verify before
  relying on it.
- Any `rediskit`, `pgkit`, `chkit`, or `outboxkit` behaviour this skill states. Re-read the cited file; the line
  numbers move.

## Recorded as unverified

- The Laravel-side framework versions in `50-redis-laravel-octane.md` (Laravel 13.x, phpredis 6.3.x, predis 3.5.x,
  Redis server 8.x) were recorded 2026-07 and were not re-verified when this file was last written. Confirm each
  named cache API exists in the service's installed version before writing it into code.
- The kit facts in this skill were read from `alaa-go-chi` source on 2026-07-26, with file and line cited at each
  claim. Line numbers drift with every kit release; the file and the symbol are the durable part of the citation.

## One example, because it is the mistake that costs most

On a table with production row counts:

```sql
CREATE INDEX CONCURRENTLY users_project_id_created_at_idx
    ON users (project_id, created_at);
```

and not:

```sql
CREATE INDEX users_project_id_created_at_idx
    ON users (project_id, created_at);
```

The non-concurrent form takes a lock that blocks writes for the duration of the build. The concurrent form cannot
run inside a transaction, so it needs its own migration or a runner that does not wrap — see
`20-schema-migrations-and-performance.md`.
