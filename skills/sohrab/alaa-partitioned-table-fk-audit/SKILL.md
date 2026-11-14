---
name: alaa-partitioned-table-fk-audit
description: "Audit PostgreSQL repositories for incomplete foreign keys into partitioned tables, including id-only references, SQLSTATE 42830, and 'no unique constraint matching given keys'. Ships a source detector that discovers partitioned parents, reads their keys, and flags incomplete raw-SQL and Laravel-shorthand references. Use when asked to audit or harden partitioned-table integrity, when a migration or query fails with 42830, before a partitioned-table migration reaches its reversibility gate, or for a proactive sweep. Report source results and durable guard status separately; installation or CI wiring in a target repository requires authorization. Do not use for general lock safety, index design, or tenancy -- use /alaa-data-layer -- or for an ordinary id-only foreign key into a non-partitioned table."
---

# Alaa Partitioned Table FK Audit

## Purpose

PostgreSQL requires a foreign key's referenced columns to match a full unique or primary key on the referenced
table. A partitioned parent's key must contain every partition column, so the key is composite. An `id`-only
reference into it fails with `SQLSTATE[42830]: no unique constraint matching given keys`, or it was
never enforced and is silently wrong. `scripts/partitioned_fk_audit.py` decides this from schema source alone.
An unreachable database blocks no step here.

Report the detector's source result and the repository's durable regression-guard status separately.
A missing guard is a finding. It is not a reason to suppress detector results or to install files without
authorization. This audit is a **level 1 static** proof. Proving that the constraint holds in the engine is
level 6, unreachable here. Report it as a gap in the words "level 6, unreachable here".

## When to use

- Asked to audit, review, or harden a PostgreSQL repository for partitioned-table foreign-key correctness.
- A migration, seeder, or query fails with `SQLSTATE[42830]` or "no unique constraint matching given keys".
- A migration touches a partitioned table or adds a foreign key onto one, before its reversibility gate runs.

## When NOT to use

- The repository uses no PostgreSQL and no design under review proposes it. There is nothing to find.
- An ordinary non-partitioned table carries an `id`-only foreign key. That is normal, and flagging it is this
  skill's named anti-pattern.
- The question is general schema or migration design rather than a reference into a partitioned parent.
  The routing table below names its owner.

## Procedure

1. Read `/alaa-data-layer` `references/20-schema-migrations-and-performance.md` before you propose a fix.
   Reason: a fix that ignores its lock and phasing rules trades one outage for another.
2. Run `python3 scripts/partitioned_fk_audit.py <root> [<root> ...]` over every root that holds schema source:
   migrations, raw `.sql`, schema dumps, docs showing DDL, vendor-published migrations.
   Reason: a root you do not pass is not audited.
   Act on the exit code's obligation line in `--help`.
3. Confirm each parent the detector printed. Reason: its evidence kinds differ in strength, and one of them
   means the migration that produced it cannot run at all.
4. Review each flagged reference. Then search by hand for the forms the detector cannot see.
   Reason: an unparsed form produces silence, and silence reads as clean.
5. Fix each live bug on the referencing side, so its key equals one of the parent's full keys.
   Never drop the foreign key to clear a finding. Reason: that removes the enforcement this audit exists to prove.
6. Size the lock window before you run that fix against a database that holds rows.
   Reason: the statement locks the parent and every partition against writes until it completes.
7. Check whether the target repository has a durable regression guard. Report its path and selector
   separately. The detector scans only supplied roots. It does not verify guard installation.
   If no guard exists, report that as a finding. It does not block reporting the detector's source findings.
   Install and wire the shipped detector only when the request explicitly authorizes changes to the named
   test and runner paths. Never re-implement it.
8. After installation is authorized, prove the test with a deliberately broken synthetic fixture: a fake
   partitioned parent plus an incomplete-key reference. Put it in the test's fixture directory. Never make it
   a real migration. Confirm the run exits 2. Then confirm it exits 0 once corrected.
   Report the detector result, guard status, parents found, bugs fixed, test path, and both runs separately.

## Validation

- When guard installation is authorized, run the installed test through its selector. Run the repository
  suite once after adding it.
- The report names the proof level reached and each claim it could not reach.

## Routing

| You are about to | Read |
|---|---|
| Judge a `PARTITION BY` hit by hand, or check a parent the detector reported | `references/10-search-patterns-and-false-positives.md` |
| Run a foreign-key fix against a partitioned table holding rows | `references/20-lock-safety-and-the-fix.md` |
| Change schema shape, index design, tenancy, or migration phasing | `/alaa-data-layer` `references/20-schema-migrations-and-performance.md` |
| State what a test proved, or a level you could not reach | `/alaa-testing-strategy` `references/40-proof-strength.md` |
| Judge whether the finished work is shippable | `/alaa-project-constitution` `references/quality-bar.md` |
| Hand the migration to the gate proving it reverses | `/alaa-cicd-laravel-postgres` `references/30-migration-reversibility.md`, which runs after this audit |
| Move a fix across module or repository/DTO boundaries | `/alaa-laravel-architecture` |
| Report why the database could not be reached, in Codex | `/alaa-codex-runtime-ops` |
| Choose a model or an effort level | `/alaa-prompting-guide` |
