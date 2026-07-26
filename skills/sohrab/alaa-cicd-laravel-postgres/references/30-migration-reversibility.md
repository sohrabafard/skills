# Migration reversibility gate

Read when a change adds, edits or reorders a migration, and when wiring the job that migrates. Migrations tested forward only are migrations whose reversal is first attempted during an incident.

## The up-down-up gate

Against a Postgres instance of the production major and minor, never SQLite — the construct whose reversal is in doubt is usually the one SQLite does not implement:

1. **Shape the schema.** Apply the migration set at the merge base, so the diff's migrations run against the schema they will meet in production rather than against an empty database. An empty database hides every migration that depends on existing objects.
2. **Forward.** `php artisan migrate --force --isolated` exits zero.
3. **Back.** `php artisan migrate:rollback --force --step=<number of migrations the diff adds>` exits zero, and the schema afterwards equals the merge-base schema. Compare with `pg_dump --schema-only --no-owner --no-privileges` on both, normalised the same way; a textual difference is a gate failure, because a leftover index, default, sequence or constraint is exactly what makes the next forward run fail.
4. **Forward again.** `php artisan migrate --force --isolated` exits zero. This is the step that catches a `down()` which drops a table but leaves its type, or leaves the migrations row behind.

## What every migration owes

Each migration the diff adds declares a `down()` that reverses what `up()` did. A `down()` that is empty, or throws, or is a comment fails the gate.

Where the change is genuinely irreversible — dropping a column that holds data, a destructive type change — the migration is **split**: one reversible schema migration, and one separate data step whose restore path is named in the deviation register of `10-gate-register.md`. "Irreversible, so no `down()`" is not an exit; splitting is the replacement.

## Release reversibility

Rolling an artifact back to N-1 requires the schema at N to still serve the application at N-1 for the whole rollback window. Therefore: **a migration that drops or renames a column, table or constraint in the same release that stops using it fails the gate.** The removal goes in a later release, after the artifact that stopped using it has outlived the rollback window. The window's value belongs to `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`; the expand-then-contract shape belongs to `/alaa-data-layer` (`$alaa-data-layer`) `references/20-schema-migrations-and-performance.md`.

## What this gate does not decide

- Lock behaviour, `CREATE INDEX CONCURRENTLY`, `NOT VALID` then validate, batched and resumable backfills, and table-rewrite timing belong to `/alaa-data-layer` (`$alaa-data-layer`) `references/20-schema-migrations-and-performance.md`.
- A migration touching a partitioned table or a foreign key onto one is audited by `/alaa-partitioned-table-fk-audit` (`$alaa-partitioned-table-fk-audit`) before this gate runs, because a reversal that succeeds on an unpartitioned copy tells you nothing about the partitioned original.
- A migration that must run against production data outside a pipeline is a controlled operation: `/alaa-controlled-ops` (`$alaa-controlled-ops`) owns the approval and the proof-strength vocabulary.

## Gate predicate

All four hold: the merge-base schema was applied first; each of the three migration invocations exited zero; the normalised schema dump after rollback matches the merge-base dump exactly; and no migration in the diff removes a surface the previous release still uses. A failure obliges fixing the migration — never marking the job advisory, and never re-running it to see whether it passes the second time.
