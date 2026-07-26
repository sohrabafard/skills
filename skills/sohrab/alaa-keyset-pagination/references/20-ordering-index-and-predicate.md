# Ordering, index, and continuation predicate

All PostgreSQL behaviour below was verified against primary sources and measured plans; versions, URLs, and retrieval dates are in `90-source-map.md`. `alaa-data-layer` (`/alaa-data-layer`, `$alaa-data-layer`) owns index design and query tuning generally — this file owns only what pagination constrains.

## The ordering tuple

Form: `ORDER BY <sort column> <dir>, <unique tie-breaker> <same dir>`.

**The final component is unique under the route's filters.** `id` unless the route documents another proven-unique column. Reason is in `SKILL.md`; the mechanism is that the continuation predicate is strict, so ties at the page boundary are dropped rather than repeated.

**Every component shares one direction.** `ORDER BY published_at DESC, id ASC` is forbidden on Ala list routes. Two independent reasons, both verified:

- A row-value comparison is lexicographic in one direction by definition, so a mixed tuple has no row-value form and must be written as the `OR` expansion this file rejects below.
- PostgreSQL cannot serve a mixed-direction `ORDER BY` from a plain composite index in either scan direction. Measured on PostgreSQL 16.13: `ORDER BY created_at DESC, id ASC` over an index on `(created_at, id)` planned an `Incremental Sort` above the index scan. Serving it without a sort requires a purpose-built `(created_at DESC, id ASC)` index, which then can no longer serve the ordinary same-direction ordering.

## The index

One index per allowlisted sort mode. Column order: equality-filter columns first, then the ordering tuple in tuple order.

```sql
CREATE INDEX contents_status_published_at_id_idx
  ON contents (status, published_at, id);
```

This serves `WHERE status = $1 ORDER BY published_at DESC, id DESC` through a backward index scan with no sort node. A `DESC`-declared index is not needed for a same-direction tuple: PostgreSQL's documentation states a two-column index on `(x, y)` satisfies `ORDER BY x, y` scanned forward and `ORDER BY x DESC, y DESC` scanned backward. Prefer the plain ascending index, because it serves both directions and therefore also serves backward traversal.

Equality filters belong to the left of the ordering columns because PostgreSQL uses equality constraints on leading columns plus the first inequality to bound the index range; a filter column placed to the right of the ordering columns is checked but does not narrow the scanned range.

**Observable: buffers, not plan text.** Run `EXPLAIN (ANALYZE, BUFFERS)` on the route's real query, at the route's maximum `limit`, against production-shaped row counts. Require no `Sort` or `Incremental Sort` node, and require the buffer count to stay flat as the cursor advances deeper into the table. Do not accept the `Index Cond` line as proof: PostgreSQL prints the original qualifier there even when it could only use a loose bound. Measured case — the same row-value predicate against a mixed-direction index still printed an identical `Index Cond` while reading 387 buffers instead of 4.

## The continuation predicate

Write it as a row-value comparison, matching the traversal direction:

```sql
-- forward page of ORDER BY published_at DESC, id DESC
WHERE (published_at, id) < ($1, $2)
ORDER BY published_at DESC, id DESC
LIMIT $3
```

Row-value comparison in PostgreSQL compares elements left to right, stopping at the first unequal or null pair — the documented lexicographic semantics keyset pagination needs. It can be used as an index constraint for a multicolumn B-tree index matching the row value, which is what makes the scan start exactly at the boundary row.

**The expanded `OR` form is forbidden:**

```sql
-- FORBIDDEN on Ala list routes
WHERE published_at < $1 OR (published_at = $1 AND id < $2)
```

A single index scan can only use clauses joined by `AND`; an `OR` needs a bitmap combination, and a bitmap visits rows in physical order, which destroys the ordering the query then has to restore with a sort. With `ORDER BY ... LIMIT` present the planner therefore does not use the bitmap at all — it scans the index in order and applies the `OR` as a filter. Measured on PostgreSQL 16.13 over the same table and index: the `OR` form read **173,475 buffers** and discarded 172,800 rows by filter; the row-value form read **13 buffers** and fetched 10 rows. Without `ORDER BY`, the `OR` form instead produced a `BitmapOr` of two scans against the same index where the row-value form produced one.

Observable: no list query in the repository contains an `OR` between two comparisons on ordering columns. This is greppable and should be a review gate.

**Direction must match the scan.** Pair `<` with `ORDER BY ... DESC` and `>` with `ORDER BY ... ASC`. A row-value comparison pointing against the scan direction is not a tight range: measured on PostgreSQL 16.13, `(c, id) < (1, 5)` under a forward scan read 387 buffers, while the same predicate under `ORDER BY c DESC, id DESC` read 4. In correct keyset pagination the two always agree, so this shows up only when someone hand-writes the predicate and the ordering separately.

## NULLS placement

PostgreSQL's defaults: `ASC` implies `NULLS LAST`, `DESC` implies `NULLS FIRST`. A B-tree index stores entries ascending with nulls last, so a plain index serves those two defaults and no others.

`ORDER BY col DESC NULLS LAST` therefore requires `CREATE INDEX ... (col DESC NULLS LAST)` — and that index can no longer serve plain `ORDER BY col`. Measured on PostgreSQL 16.13: `ORDER BY c DESC NULLS LAST` against a default index planned a full `Sort` over a `Seq Scan`.

This is one of two reasons nullable sort columns are forbidden on Ala list routes. The other — that a row-value comparison containing a null evaluates to unknown and silently excludes the row — is in `50-hard-cases.md`, together with the required replacement.
