# Test-database isolation

Read when enabling or changing parallel tests, when changing the test database or its name, and when two jobs or two workers collide on one database. This is the ground no other skill owns: `/alaa-testing-strategy` (`$alaa-testing-strategy`) owns per-test hermeticity; this file owns the database the workers get.

## One strategy, not a choice

**One Postgres database per parallel worker, created by the framework's own parallel-testing mechanism, dropped by the job that created it.** Schema-per-worker is not an alternative here: Laravel's parallel testing keys the isolation off the database name, so a schema layout means reimplementing what the framework already does, and reimplementation is what breaks on the next framework major. A single shared database with truncation between tests is also excluded — it serialises every worker on the same rows and turns a parallel suite into a slower serial one with cross-worker failures.

## Naming

The name is `<prefix>_test_<token>`, where the token is the worker token the framework supplies and the prefix is a CI variable derived from the job's own identity, not from the application name. A prefix of just the application name gives two concurrently running pipelines the same `app_test_1`, and they will corrupt each other's rows while both suites report unexplained assertion failures. The prefix is unique per job on the Postgres instance the job uses.

## Who creates and who removes

- The **base** database is created by the service container's own initialisation, or by one explicit creation step before the suite. Never by a test, and never lazily on first connection.
- The **per-worker** databases are created by `php artisan test --parallel --recreate-databases`. No test creates a database.
- **Teardown** is a step that runs on success, failure, cancellation and timeout, and drops every database matching this job's prefix. Dropping at the *start* of the next run is not teardown: it leaves the instance holding every database from every cancelled job, and the first run after a quota is reached fails for a reason unrelated to the change under test.
- `--parallel` without `--recreate-databases` reuses the worker databases and is faster. It is permitted only where the teardown above already exists, because reuse without teardown is how a schema from an abandoned branch decides a later run.

## Connection budget

Each worker holds at least one connection; the migration step holds one more; the instance keeps a reserve for administrative access. **The worker count is derived from the test instance's connection limit, declared as a CI variable, and validated at job start: when `workers x connections-per-worker + reserve` exceeds the limit, the job fails immediately with that arithmetic in the message.** Failing at the start is the point — a budget exceeded mid-suite surfaces as an intermittent connection error on a random test and is filed as a flake. The connection and worker numbers themselves come from `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`.

## Concurrent migration

Every job that migrates runs `php artisan migrate --force --isolated`. Without `--isolated` two jobs migrating the same database interleave and one fails part-way through, leaving a schema that is neither version. `--isolated` takes its lock through the cache store, so the migrating job's cache store must be one whose lock is visible to every process contending for it: an `array` store is per-process and provides no lock at all, and a `file` store is not shared between containers.

## Where a pooler sits in front

Where production reaches Postgres through a connection pooler, the schema and migration path connects to Postgres **directly**, because transaction-pooling mode does not carry the session state that migrations and advisory locks require. Application-path test connections keep production's prepared-statement settings, so a statement that fails only behind the pooler also fails in CI.

## The gate predicate

The isolation gate passes only when all four hold, each checkable:

1. No two concurrently running jobs or workers can resolve the same database name.
2. Every database the job created is absent after the job's teardown step, whatever the job's outcome.
3. The suite refuses to start when the connection budget is exceeded, naming the arithmetic.
4. Every migrating invocation carries `--isolated`, against a cache store whose lock is shared across processes.

Tenancy columns, index shape and query cost belong to `/alaa-data-layer` (`$alaa-data-layer`); `60-ownership-boundary.md` states what wins.
