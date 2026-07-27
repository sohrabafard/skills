# Reading the detector, and the forms it cannot see

Read this when `scripts/partitioned_fk_audit.py` names a parent you do not recognise, when you must judge a
`PARTITION BY` hit by hand because the detector could not run, or before you report a repository as clean.

The detector owns the mechanics. This file owns what its output means, which of its answers you must corroborate,
and what it deliberately does not detect.

## The evidence kinds, and how far each one settles the question

The detector prints one or more evidence lines per parent. They are not equally strong.

| Evidence kind | What it proves | What you still owe |
|---|---|---|
| `create-table-partition-by` | The parent is declaratively partitioned, and the partition columns are known | Nothing; this is conclusive |
| `create-table-partition-of` | A partition of this parent exists, so the parent is partitioned | Find the parent's own `CREATE TABLE` if its key came back `UNKNOWN` |
| `alter-table-attach-partition` | A partition is attached to this parent, so the parent is partitioned | The same; the parent's DDL may live outside the roots you passed |
| `inherits-legacy-partitioning` | A child inherits from this parent and carries a `CHECK` constraint or an insert-routing trigger | Confirm it is partitioning rather than plain table inheritance, and read the legacy limitation below |
| `alter-table-partition-by-INVALID-SYNTAX` | Nothing about the schema; PostgreSQL has no such statement | Treat the file as a migration that cannot run, and fix or delete it |

That last kind exists because `ALTER TABLE <t> PARTITION BY <method> (...)` is written often and accepted never.
PostgreSQL 16.13 answers `ERROR: syntax error at or near "PARTITION"`, and the PostgreSQL 18 `ALTER TABLE`
synopsis lists only `ATTACH PARTITION` and `DETACH PARTITION`
(https://www.postgresql.org/docs/current/sql-altertable.html, read 2026-07-26). An existing table cannot be
partitioned in place; the real two-step Laravel pattern is `Schema::create` for the ordinary tables plus a
`DB::statement("CREATE TABLE ... PARTITION BY ...")` for the partitioned one, which is why the detector reads DDL
inside PHP string literals as well as inside `.sql` files.

## The parent's key must contain every partition column

```sql
CREATE TABLE events (
    id          bigint GENERATED ALWAYS AS IDENTITY,
    tenant_id   bigint NOT NULL,
    created_at  timestamptz NOT NULL,
    PRIMARY KEY (tenant_id, id, created_at)      -- includes created_at, the partition column
) PARTITION BY RANGE (created_at);
```

Dropping `created_at` from that key does not merely weaken it; PostgreSQL refuses the statement outright with
`ERROR: unique constraint on partitioned table must include all partitioning columns` (measured on PostgreSQL
16.13, 2026-07-26; documented at https://www.postgresql.org/docs/current/ddl-partitioning.html, read 2026-07-26).
The detector therefore discards any declared key missing a partition column and reports it as
`parent-key-omits-partition-column`, because treating it as usable would make an `id`-only reference into that
parent look satisfied when the parent's own migration cannot run.

## The window-function false positive

`PARTITION BY` inside `OVER (...)` or `WINDOW w AS (...)` is query grammar and never a partitioned table:

```sql
SELECT *, ROW_NUMBER() OVER (PARTITION BY tenant_id ORDER BY created_at DESC) AS rn FROM events;
```

The detector blanks the body of every such clause before searching, so these never reach its output. When you are
searching by hand instead, apply the same rule: a real hit is attached to a `CREATE TABLE` block as its
table-level clause, and a hit inside `OVER (` or a named window is always the query form.

## Laravel shorthand forms that default to a single `id` column

Each form below creates a foreign key referencing `id` alone, so each is the bug whenever its target is a
partitioned parent, and each is ordinary and correct whenever its target is not.

- `->foreignId('parent_id')->constrained()` — target table inferred from the column name, key defaults to `id`.
- `->foreignId('parent_id')->constrained('parent_table')` — target named explicitly, key still defaults to `id`.
- `->foreignIdFor(Model::class)` — same shape, and invisible to a grep for the literal string `foreignId(`.
- `->foreignUlid()` / `->foreignUuid()` followed by `->constrained()` — same default, for ULID/UUID keys.
- `->foreign('parent_id')->references('id')->on('parent_table')` — explicit, and still incomplete against a
  composite parent key.

`->foreignId('parent_id')` on its own declares a column and creates no constraint, so the detector does not flag
it and neither do you. None of these forms expresses a composite foreign key in one call: a composite
reference needs a raw `DB::statement(...)` migration or an explicit multi-column
`foreign([...])->references([...])->on(...)`.

## What the detector does not detect, and what that obliges you to do

- **A reference built at runtime** — a table or column name assembled from a variable, a config value, or string
  concatenation. The detector reads literals only. Grep the repository for `DB::statement` and raw connection
  calls whose argument is not a single literal, and read each one.
- **A constraint created outside the roots you passed** — a psql script run by hand, an operator runbook, a
  platform-managed schema. Pass those roots or record them as unaudited; the detector cannot report a file it was
  never given.
- **A schema that exists only in the database** — a table created before the migration history began. Every
  answer here is level 1 static, so a parent present in the engine and absent from source is invisible; say so
  rather than reporting the repository clean.
- **A non-PostgreSQL engine's partitioning.** The detector's grammar is PostgreSQL's; MySQL and others are out of
  scope for this skill entirely.

Each of these obliges the same thing: name it in the report as unaudited, at the severity it carries, rather than
letting the detector's exit code stand for a question it never examined.
