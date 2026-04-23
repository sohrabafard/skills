# Source Map

Use this map when schema, query, locking, Redis, tenant isolation, or current database behavior matters.

## Source order

1. Repository truth:
   - migrations, models, factories, seeders, tests, query call sites, DB config, Redis config, `.env.example`, and production/runtime docs.
   - Actual schema and `EXPLAIN` output when DB access is available.
2. Official PostgreSQL sources:
   - Current PostgreSQL docs: https://www.postgresql.org/docs/current/
   - `CREATE INDEX`: https://www.postgresql.org/docs/current/sql-createindex.html
   - Row security policies: https://www.postgresql.org/docs/current/ddl-rowsecurity.html
   - Explicit locking: https://www.postgresql.org/docs/current/explicit-locking.html
   - Transaction isolation: https://www.postgresql.org/docs/current/transaction-iso.html
   - `EXPLAIN`: https://www.postgresql.org/docs/current/using-explain.html
3. Official Redis and Laravel sources:
   - Redis docs: https://redis.io/docs/latest/
   - Redis distributed locks pattern: https://redis.io/docs/latest/develop/use/patterns/distributed-locks/
   - Laravel database docs: https://laravel.com/docs/13.x/database
   - Laravel migrations docs: https://laravel.com/docs/13.x/migrations
   - Laravel cache docs: https://laravel.com/docs/13.x/cache
   - Laravel Redis docs: https://laravel.com/docs/13.x/redis
4. Community posts and StackOverflow answers:
   - Use only for troubleshooting unusual errors or finding keywords.
   - Re-check every operational claim against official docs and the actual query plan.

## Freshness triggers

Verify official docs or the live database before acting when the task mentions:

- `latest`, `current`, `upgrade`, `security`, `CVE`, new PostgreSQL/Redis major versions, or managed-service version changes.
- RLS, tenant isolation, concurrent indexes, partitioning, replication, locks, deadlocks, transaction isolation, pooling, PgBouncer, cache serialization, or Redis eviction.
- A query or migration expected to run on a large table.

## Small example

For a large live table, prefer a phased index rollout:

```sql
CREATE INDEX CONCURRENTLY users_project_id_created_at_idx
    ON users (project_id, created_at);
```

Anti-pattern:

```sql
CREATE INDEX users_project_id_created_at_idx
    ON users (project_id, created_at);
```

The non-concurrent form can block writes on a busy table. Use the repository migration framework carefully because PostgreSQL concurrent index creation cannot run inside a transaction.
