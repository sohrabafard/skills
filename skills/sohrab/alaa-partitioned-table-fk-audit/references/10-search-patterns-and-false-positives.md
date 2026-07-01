# Search Patterns and False Positives

These patterns are starting points, not a complete substitute for reading the matches. Adjust the file globs to whatever this repo actually uses for schema sources (Laravel migrations, raw `.sql` schema dumps, vendor-published migrations under `vendor/`, docs/examples that show DDL).

## 1. Find partitioned parent tables

```
rg -n -i "partition\s+by" database/ migrations/ docs/ vendor/ 2>/dev/null
```

A real hit looks like DDL attached to a `CREATE TABLE` statement, e.g.:

```sql
CREATE TABLE events (
    id bigint,
    tenant_id bigint,
    created_at timestamptz,
    PRIMARY KEY (tenant_id, id)
) PARTITION BY RANGE (created_at);
```

### False positive to exclude

Laravel's query grammar, and raw Postgres SQL in general, also uses `PARTITION BY` inside window functions -- this is completely unrelated to table partitioning:

```sql
SELECT *, ROW_NUMBER() OVER (PARTITION BY tenant_id ORDER BY created_at DESC) AS rn
FROM events;
```

Distinguish by context, not by the bare string match: a real partitioned-parent hit is either (a) attached directly to a `CREATE TABLE ... (...)` block as its table-level clause, or (b) a separate, later `ALTER TABLE <table> PARTITION BY ...` statement -- a common Laravel pattern where the table is created in one migration/`Schema::create` call and partitioned in a following `DB::statement(...)` call. Do not assume only form (a) counts; a hit that isn't textually attached to a `CREATE TABLE` block can still be a real partitioned parent if it's an `ALTER TABLE ... PARTITION BY`. If a hit is inside `OVER(`, it is always the window-function form -- skip only that one.

### False negative to watch for: legacy inheritance-based partitioning

Repos that predate Postgres 10 (or that never migrated off the old pattern) may partition tables via `INHERITS` plus `CHECK` constraints and insert-routing triggers, with no `PARTITION BY` clause anywhere. A `PARTITION BY` search finds nothing in this case even though the same incomplete-key FK problem can exist. If step 2 of the procedure comes back empty, do a second pass searching for `INHERITS\s*\(` before concluding the repo has no partitioned tables.

## 2. For each true partitioned parent, get its real key shape

Read the `PRIMARY KEY (...)` or `UNIQUE (...)` clause on the same `CREATE TABLE` statement. A partitioned parent's real key must include every column used in the partition expression, so it is almost always composite (e.g. `(tenant_id, id)`, not just `(id)`).

## 3. Find references into that parent that supply an incomplete key

```
rg -n "references\s*\(\s*['\"]?id['\"]?\s*\)" app/ database/
rg -n "foreignId\s*\(|foreignIdFor\s*\(|foreignUlid\s*\(|foreignUuid\s*\(" app/ database/
rg -n "->constrained\s*\(" app/ database/
rg -n "REFERENCES\s+\w+\s*\(\s*id\s*\)" database/ vendor/ 2>/dev/null
```

Laravel shorthand forms that default to referencing `id` alone, and therefore need scrutiny against a partitioned parent:

- `->foreignId('parent_id')->constrained()` -- defaults to `id` on the inferred table.
- `->foreignId('parent_id')->constrained('parent_table')` -- still defaults to `id` unless a composite reference is spelled out.
- `->foreignIdFor(Model::class)` -- same shape as `foreignId()`, easy to miss in a grep that only looks for the literal string `foreignId(`.
- `->foreignUlid()`/`->foreignUuid()` followed by `->constrained()` -- same default-to-`id` behavior, for repos using ULID/UUID primary keys.
- `->foreign('parent_id')->references('id')->on('parent_table')` -- explicit but still incomplete if the parent's real key is composite.

None of these forms natively express a composite foreign key in a single call -- a composite FK against a partitioned parent typically needs a raw `DB::statement(...)` migration, or an explicit multi-column `foreign([...])->references([...])->on(...)` call (available in newer Laravel versions). If the repo has neither, and a partitioned parent has a composite key, any shorthand-form reference into it is very likely the bug.

**Do not stop at the grep hit.** Every pattern above will also match completely ordinary foreign keys into non-partitioned tables -- that is expected and is not a bug. Before reporting anything as a finding, cross-check the referenced table name against the partitioned-parent inventory from steps 2-3 of the procedure. A `->constrained()` call is only worth flagging when its target table is actually on that list.

## 4. Regression test shape

The test should not hardcode which tables are partitioned -- it should discover them the same way step 1 does (parse `CREATE TABLE ... PARTITION BY` from the same schema sources the app ships), then check every FK reference in the codebase against each discovered parent's real key. That way the test keeps working as the schema evolves, and the synthetic-fixture proof (procedure step 7) is simply adding one deliberately-broken fixture table + reference to confirm the detector's logic actually flags it before deleting the fixture again (or keeping it as a permanent "does the detector still work" canary, if this repo's test conventions prefer that).
