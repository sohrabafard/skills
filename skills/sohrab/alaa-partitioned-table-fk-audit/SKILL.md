---
name: alaa-partitioned-table-fk-audit
description: "Audit a PostgreSQL repository (Laravel, raw SQL, or Go migrations) for foreign keys referencing a partitioned table through an incomplete key: the id-only-FK-into-a-partitioned-parent bug class, SQLSTATE 42830, 'no unique constraint matching given keys'. Ships a tested detector that discovers partitioned parents from source, reads each parent's real key shape, and flags every raw-SQL and Laravel-shorthand reference supplying less than that key. Use when asked to audit or harden a service for partitioned-table integrity, when a migration or query fails with 42830, before a partitioned-table migration reaches its reversibility gate, or as a proactive sweep with none reported. A clean audit is incomplete without a durable regression test. Do not use for general lock safety, index design, or tenancy -- that is /alaa-data-layer ($alaa-data-layer) -- nor for an ordinary id-only foreign key into a non-partitioned table, which is normal."
---

# Alaa Partitioned Table FK Audit

## Purpose

PostgreSQL requires a foreign key's referenced columns to match a full unique or primary key on the referenced
table. A partitioned parent's key must contain every partition column, so it is composite, so an `id`-only
reference into it fails with `SQLSTATE[42830]: no unique constraint matching given keys` — or was never enforced
and is silently wrong. `scripts/partitioned_fk_audit.py` decides this from schema source alone, so an unreachable
database blocks no step here.

Treat "no partitioned tables exist today" as incomplete rather than clean, because the regression test is what
stops the bug landing later. This audit is a **level 1 static** proof and the test it leaves is **level 2**;
proving the constraint holds in the engine is level 6, unreachable here, and reported as a gap in those words.

## When to use

- Asked to audit, review, or harden a PostgreSQL repository for partitioned-table foreign-key correctness.
- A migration, seeder, or query fails with `SQLSTATE[42830]` or "no unique constraint matching given keys".
- A migration touches a partitioned table or adds a foreign key onto one, before its reversibility gate runs.

## When NOT to use

- The repository uses no PostgreSQL and no design under review proposes it — there is nothing to find.
- An ordinary non-partitioned table carries an `id`-only foreign key. That is normal, and flagging it is this
  skill's named anti-pattern.
- The question is general schema or migration design rather than a reference into a partitioned parent; the
  routing table below names its owner.

## Procedure

1. Read `/alaa-data-layer` (`$alaa-data-layer`) `references/20-schema-migrations-and-performance.md` before
   proposing a fix, because a fix ignoring its lock and phasing rules trades one outage for another.
2. Run `python3 scripts/partitioned_fk_audit.py <root> [<root> ...]` over every root holding schema source —
   migrations, raw `.sql`, schema dumps, docs showing DDL, vendor-published migrations — because a root you do not
   pass is not audited. Act on the exit code's obligation line in `--help`.
3. Confirm each parent the detector printed, because its evidence kinds differ in strength and one of them means
   the migration that produced it cannot run at all.
4. Review each flagged reference, then search by hand for the forms the detector cannot see, because an unparsed
   form produces silence and silence reads as clean.
5. Fix each live bug on the referencing side so its key equals one of the parent's full keys. Never drop the
   foreign key to clear a finding, because that removes the enforcement this audit exists to prove.
6. Size the lock window before running that fix against a database holding rows, because the statement locks the
   parent and every partition against writes until it completes.
7. Install the shipped detector as the repository's permanent test —
   `python3 scripts/partitioned_fk_audit.py --install <repo test path>` — and wire the repository's runner to
   invoke it over the step-2 roots. Never re-implement it, because a re-implementation drifts from the fixtures
   that prove it.
8. Prove that test works: add one deliberately broken synthetic fixture — a fake partitioned parent plus an
   incomplete-key reference, in the test's fixture directory and never as a real migration — confirm the run exits
   2, then confirm it exits 0 once corrected. Report the parents found, each bug fixed, the test's path, and both
   runs pasted as output.

## Validation

- `python3 scripts/partitioned_fk_audit.py --self-test` exits 0 before any finding of yours is reported.
- The repository's full suite passes after the installed test is added.
- The report names the proof level reached and each claim it could not reach.

## Routing

| You are about to | Read |
|---|---|
| Judge a `PARTITION BY` hit by hand, or check a parent the detector reported | `references/10-search-patterns-and-false-positives.md` |
| Run a foreign-key fix against a partitioned table holding rows | `references/20-lock-safety-and-the-fix.md` |
| Change schema shape, index design, tenancy, or migration phasing | `/alaa-data-layer` (`$alaa-data-layer`) `references/20-schema-migrations-and-performance.md` |
| State what a test proved, or a level you could not reach | `/alaa-testing-strategy` (`$alaa-testing-strategy`) `references/40-proof-strength.md` |
| Judge whether the finished work is shippable | `/alaa-project-constitution` (`$alaa-project-constitution`) `references/quality-bar.md` |
| Hand the migration to the gate proving it reverses | `/alaa-cicd-laravel-postgres` (`$alaa-cicd-laravel-postgres`) `references/30-migration-reversibility.md`, which runs after this audit |
| Move a fix across module or repository/DTO boundaries | `/alaa-laravel-architecture` (`$alaa-laravel-architecture`) |
| Report why the database could not be reached | `/alaa-codex-runtime-ops` (`$alaa-codex-runtime-ops`) |
| Choose a model or an effort level | `/alaa-prompting-guide` (`$alaa-prompting-guide`) |
