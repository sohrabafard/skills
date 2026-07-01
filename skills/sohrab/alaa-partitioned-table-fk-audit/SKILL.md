---
name: alaa-partitioned-table-fk-audit
description: "Audit a Laravel + PostgreSQL repo for foreign keys that reference a partitioned table through an incomplete key -- the id-only-FK-into-a-partitioned-parent bug class, PostgreSQL error 42830 (no unique constraint matching given keys). Use whenever asked to audit, review, or harden a Laravel service for partitioned-table integrity, whenever a migration or query fails with SQLSTATE 42830, or as a proactive cross-service sweep even when nobody reported a live bug. A clean audit with zero live bugs found is not complete until a durable regression test exists."
---

# Alaa Partitioned Table FK Audit

## Purpose

PostgreSQL requires a foreign key to reference a full unique or primary key on the parent table. A partitioned parent's real key is usually composite (it must include the partition column), so a naive `id`-only reference -- including Laravel's own `->constrained()`/`foreignId()` shorthand, which defaults to `id` -- fails at migration time with `SQLSTATE[42830]: no unique constraint matching given keys`, or worse, was never actually enforced and is silently wrong. This exact audit has already been run, independently, across five different Ala-family Laravel services in this portfolio, always with the same shape: search for partitioned parents, check every reference into them, fix any incomplete one, and -- this is the part that gets skipped under time pressure -- add a permanent regression test regardless of whether a live bug turned up. Treat "no partitioned tables exist today" as an incomplete answer, not a clean bill of health, since the guard is what prevents the bug from ever landing later.

This procedure needs no live database connection. It works entirely from static repository reads (migrations, raw SQL, schema dumps, docs, vendor-published migrations), because a live Postgres host is frequently unreachable from an agent sandbox in this portfolio -- do not treat that as a blocker.

## When to use

- The user asks to audit, review, or harden a Laravel (or any ORM-backed) PostgreSQL repo for partitioned-table foreign-key correctness.
- A migration, seeder, or query fails with `SQLSTATE[42830]` or the phrase "no unique constraint matching given keys."
- Running a recurring or scheduled cross-service data-integrity sweep and this repo uses PostgreSQL.

## When NOT to use

- The repo does not use PostgreSQL, or does not (and will not foreseeably) use table partitioning -- there is nothing for this skill to find.
- An ordinary, non-partitioned table has an `id`-only foreign key. That is completely normal and is not this bug class -- do not flag it.
- Text matching `partition by` inside a SQL window function (e.g. `ROW_NUMBER() OVER (PARTITION BY ...)`) is unrelated query-grammar syntax, not schema DDL -- see `references/10-search-patterns-and-false-positives.md` before flagging any `PARTITION BY` hit.
- A search for `PARTITION BY` finds nothing and the repo predates Postgres's declarative partitioning (added in Postgres 10): check for the legacy `INHERITS` + trigger-based partitioning pattern before concluding this skill doesn't apply -- the same incomplete-key FK problem exists there too, just without a `PARTITION BY` clause to search for.

## Procedure

1. Read the repo's own architecture/data-layer conventions first (`$alaa-data-layer` in Codex, `/alaa-data-layer` in Claude Code) if this repo has one loaded, so the audit respects existing schema conventions.
2. Search migrations, raw SQL files, schema dumps, docs/examples, and any vendor-published migrations for `CREATE TABLE ... PARTITION BY` DDL, and separately for a later `ALTER TABLE <table> PARTITION BY ...` (a common two-step Laravel pattern), to build a complete inventory of partitioned parent tables. Filter out SQL window-function `PARTITION BY` hits -- see `references/10-search-patterns-and-false-positives.md` for the exact patterns and the false-positive filter.
3. For each true partitioned parent, determine its actual primary/unique key shape (which columns, in what order) directly from its `CREATE TABLE`/`PRIMARY KEY`/`UNIQUE` clauses -- do not assume it is `id` alone.
4. Search the whole project -- including vendor-published migrations, matching the scope of step 2 -- for anything that references that parent as a foreign key: raw SQL (`REFERENCES parent(...)`) and every Laravel shorthand form (`->constrained()`, `->foreignId(...)`, `->foreignIdFor(...)`, `->foreignUlid()`/`->foreignUuid()`, `->references('id')->on(...)`). Before flagging a hit, confirm the target table is actually one of the partitioned parents found in step 2 -- a bare `->constrained()` call against an ordinary table is not this bug, no matter how it looks in isolation.
5. If a live bug is found, fix it at the root: make the referencing side's key explicit and complete, matching the parent's real key shape exactly. Do not paper over the symptom by dropping the foreign-key constraint.
6. Regardless of whether step 5 found anything, add a permanent test that reads schema/migration source text -- never a live database query -- to: (a) auto-discover `PARTITION BY` parents itself (not a hardcoded list, so it stays correct as the schema evolves), and (b) fail on any reference into one of those parents that does not carry the parent's full key.
7. Prove the new test actually works, not just that it exists: add one deliberately-broken synthetic fixture (a fake partitioned table plus an incomplete-key reference to it, defined inside the test file or its fixture directory -- do not commit it as a real migration unless this repo's own test conventions require that), confirm the test fails against it, then confirm it passes once the fixture is corrected or removed.
8. Report: which partitioned parents were found (if any), any live bug fixed, the new test's file location, and the actual command output proving it ran against the synthetic case in step 7 -- a claim that it "passed" is not sufficient without showing the run.

## Validation

- The new test's actual run output is shown -- both failing against the broken fixture and passing after the fix/removal, per step 7 -- not just summarized as "passed."
- The full test suite passes after the new test is added.
- No step in this procedure required a live database connection to complete (a local test-runner/toolchain, e.g. PHP + Composer, is still expected for step 7).

## Companion routing

- `$alaa-data-layer` -- the general Postgres/Redis data-layer policy for this pack; read it first for broader schema conventions, then come back here for this specific bug class.
- `$alaa-laravel-architecture` -- pair when a fix here also touches module boundaries or repository/DTO flow.
- `$alaa-codex-runtime-ops` -- if the live database is unreachable and that surprises you, this is expected in this portfolio, not a runtime failure to troubleshoot; proceed with the static-analysis path in this skill instead.

## Reference navigation

- `references/10-search-patterns-and-false-positives.md` -- exact search patterns for partitioned-parent DDL and incomplete-key references, and the window-function false-positive to exclude.
