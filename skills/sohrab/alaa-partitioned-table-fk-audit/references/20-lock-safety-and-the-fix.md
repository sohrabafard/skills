# Lock safety when fixing a partitioned-table foreign key

Read before executing a foreign-key fix against any database that holds rows. Skip it only for a database with no
rows to lock — a fresh test database or a schema that has never been deployed.

`/alaa-data-layer` (`$alaa-data-layer`) `references/20-schema-migrations-and-performance.md` owns migration lock
safety, `NOT VALID` then `VALIDATE CONSTRAINT`, `CREATE INDEX CONCURRENTLY`, and phased rollout. This file owns
only which of those behave differently because the table is partitioned, since applying the general rule to a
partitioned parent is where the outage comes from.

## What the fix actually locks

Measured on PostgreSQL 16.13 on 2026-07-26, adding a foreign key whose referenced table is a partitioned parent
with three partitions:

```
ALTER TABLE child ADD CONSTRAINT child_event_fk
  FOREIGN KEY (tenant_id, event_id, event_at) REFERENCES events (tenant_id, id, created_at);

    relname     |         mode          | granted
----------------+-----------------------+---------
 child          | ShareRowExclusiveLock | t
 events         | ShareRowExclusiveLock | t
 events_2026_01 | ShareRowExclusiveLock | t
 events_2026_02 | ShareRowExclusiveLock | t
 events_2026_03 | ShareRowExclusiveLock | t
```

Three facts follow, and each changes what you must plan for.

**The lock reaches every partition, not just the parent.** A parent with two hundred partitions takes two hundred
and one locks in one statement, so the blast radius is the whole table family and the statement waits for the
slowest of them.

**The mode is `SHARE ROW EXCLUSIVE`, not `ACCESS EXCLUSIVE`.** It conflicts with `ROW EXCLUSIVE`, so every
`INSERT`, `UPDATE` and `DELETE` against the parent and every partition blocks for the duration. It does not
conflict with `ACCESS SHARE`, so reads continue. Plan for a write outage and do not claim a read outage; the
documented statement is "`ADD FOREIGN KEY` requires only a `SHARE ROW EXCLUSIVE` lock … also acquires a `SHARE ROW
EXCLUSIVE` lock on the referenced table" (https://www.postgresql.org/docs/current/sql-altertable.html, read
2026-07-26).

**`NOT VALID` does not lower that lock.** The same measurement with `NOT VALID` appended took
`ShareRowExclusiveLock` on the parent and on all three partitions exactly as above. What `NOT VALID` removes is
the scan of the referencing table's existing rows, so it shortens how long the lock is held rather than weakening
it. Use it for that, and never on the assumption that it makes the statement lock-free.

## Which general lock-safety mechanisms still apply here

| Mechanism | On a partitioned parent |
|---|---|
| `ADD CONSTRAINT … NOT VALID` then `VALIDATE CONSTRAINT` | Applies, and is the default shape. `VALIDATE CONSTRAINT` took `SHARE UPDATE EXCLUSIVE` on the referencing table and only `ACCESS SHARE` on the parent and its partitions in the same measurement, so validation does not block writes |
| `NOT VALID` where the **referencing** side is itself partitioned | Version-gated. PostgreSQL 16.13 answers `ERROR: cannot add NOT VALID foreign key on partitioned table … This feature is not yet supported on partitioned tables`. PostgreSQL 18 lists "Allow `NOT VALID` foreign key constraints on partitioned tables" (https://www.postgresql.org/docs/current/release-18.html, read 2026-07-26). Check the server's major version before planning on it |
| `CREATE INDEX CONCURRENTLY` | Does **not** apply directly. PostgreSQL 16.13 answers `ERROR: cannot create index on partitioned table "events" concurrently`. The documented path is `CREATE INDEX ON ONLY <parent>`, then `CREATE INDEX CONCURRENTLY` per partition, then `ALTER INDEX … ATTACH PARTITION`; the parent index stays invalid until every partition is attached (https://www.postgresql.org/docs/current/ddl-partitioning.html, read 2026-07-26) |
| Expand-then-contract phasing, batched resumable backfills, avoiding peak-hour rewrites | Apply unchanged; `/alaa-data-layer` (`$alaa-data-layer`) `references/20-schema-migrations-and-performance.md` owns them and this file adds nothing |

## The legacy inheritance parent cannot be fixed by key shape alone

Where the parent is partitioned the old way — `INHERITS` plus `CHECK` constraints plus an insert-routing trigger —
correcting the referencing side's key shape is necessary and still not sufficient. A foreign key onto an
inheritance parent is enforced against that parent's own rows only, never against rows living in its children.
Measured on PostgreSQL 16.13 on 2026-07-26: a row inserted into the child was visible through
`SELECT count(*) FROM measurement` yet a correct composite reference to `(city_id, logdate)` was still rejected —
`insert or update on table "readings2" violates foreign key constraint … Key (city_id, logdate)=(1, 2026-01-15) is
not present in table "measurement"`.

Therefore, on a legacy parent, do not report the reference as fixed once its key matches. Either migrate the
parent to declarative partitioning first, or record the constraint as unenforceable and name where the invariant
is enforced instead. Which of the two is right is a schema decision owned by `/alaa-data-layer`
(`$alaa-data-layer`), not by this audit.

## Before the fix leaves your hands

State the lock mode, the number of partitions it will reach, and the measured or estimated duration in the change
description, because a reviewer cannot size a write outage from the statement text alone. Then hand the migration
to `/alaa-cicd-laravel-postgres` (`$alaa-cicd-laravel-postgres`) `references/30-migration-reversibility.md`, whose
gate proves the migration reverses and which is specified to run after this audit.
