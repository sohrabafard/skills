# Sources, versions, and what is unverified

Every version-sensitive claim in this skill is listed here with its primary source and retrieval date. Re-verify before repeating any of it in a new context; a number or a framework behaviour copied forward without a date is stale the day it is written.

## Origin of the ruleset

The seventeen-section production rules document supplied by the platform owner, ratified 2026-07-25, is the raw material for this skill. Where it says "prefer", "avoid", or "consider", this skill states the constraint instead and records why the alternative was rejected. Two of its proposals were rejected outright and the reasons are in `40-wire-contract-limits-and-errors.md`: the `pagination` response object, and the `after`/`before` request parameters.

## Laravel

All retrieved **2026-07-25**. Source read from `laravel/framework` branch `13.x` (`Application::VERSION = 13.22.0`); `paginateUsingCursor` verified byte-identical on `12.x`, and `Cursor::encode()` identical on `11.x`, `12.x`, `13.x`.

- Cursor encoding is unpadded URL-safe base64 of JSON, with no signature or integrity field — `Illuminate\Pagination\Cursor::encode()` / `fromEncoded()`: https://raw.githubusercontent.com/laravel/framework/13.x/src/Illuminate/Pagination/Cursor.php
- The cursor's payload is the ordering-column values plus `_pointsToNextItems` and nothing else — `AbstractCursorPaginator::getParametersForItem()`: https://raw.githubusercontent.com/laravel/framework/13.x/src/Illuminate/Pagination/AbstractCursorPaginator.php
- The generated predicate is a nested `OR` expansion, not a row-value comparison; the tie-breaker is injected only when the query has no ordering; a null ordering value raises `InvalidArgumentException` — `Illuminate\Database\Concerns\BuildsQueries::paginateUsingCursor` and `Query\Builder::ensureOrderForCursorPagination` / `invalidOperatorAndValue`: https://raw.githubusercontent.com/laravel/framework/13.x/src/Illuminate/Database/Concerns/BuildsQueries.php and https://raw.githubusercontent.com/laravel/framework/13.x/src/Illuminate/Database/Query/Builder.php
- The exact SQL quoted in `60-per-stack.md` is Laravel's own asserted expectation — `testCursorPaginateMultipleOrderColumns` in https://raw.githubusercontent.com/laravel/framework/13.x/tests/Database/DatabaseQueryBuilderTest.php
- The documented limitation list, unchanged across `8.x`–`13.x`: https://laravel.com/docs/13.x/pagination#cursor-pagination
- Null ordering values, open since 2021: https://github.com/laravel/framework/issues/38220

## PostgreSQL

Documentation pages are the `current` series, **PostgreSQL 18**, retrieved **2026-07-25**. Measured plans were produced on **PostgreSQL 16.13** (Ubuntu 16.13-0ubuntu0.24.04.1).

- Row-constructor comparison semantics — left-to-right, stopping at the first unequal or null pair, yielding unknown when that pair contains a null: https://www.postgresql.org/docs/current/functions-comparisons.html#ROW-WISE-COMPARISON
- A row comparison is usable as an index constraint for a matching multicolumn index: PostgreSQL 8.2 release notes, "Migration to Version 8.2": https://www.postgresql.org/docs/release/8.2.0/
- A single index scan uses only `AND`-joined clauses; a bitmap combination loses ordering and forces a sort: https://www.postgresql.org/docs/current/indexes-bitmap-scans.html
- Leading equality constraints plus the first inequality bound the scanned index range: https://www.postgresql.org/docs/current/indexes-multicolumn.html
- A `(x, y)` index satisfies `ORDER BY x, y` forward and `ORDER BY x DESC, y DESC` backward; a mixed-direction ordering needs a mixed-direction index: https://www.postgresql.org/docs/current/indexes-ordering.html
- `ASC` implies `NULLS LAST`, `DESC` implies `NULLS FIRST`: https://www.postgresql.org/docs/current/queries-order.html

Measured figures quoted in this skill, all on PostgreSQL 16.13:

- Row-value predicate 4 buffers against 927 for the `OR` form, without `ORDER BY`, on a 100,010-row table with a `(c, id)` index.
- Row-value predicate 13 buffers against 173,475 for the `OR` form under `ORDER BY ... LIMIT 10`, with 172,800 rows removed by filter in the `OR` case.
- The same row-value predicate against a mixed-direction `(c ASC, id DESC)` index read 387 buffers instead of 4, while printing an identical `Index Cond` line — the basis for the rule that buffers, not plan text, are the observable.
- `ORDER BY c DESC, id ASC` over a `(created_at, id)` index planned an `Incremental Sort`; `ORDER BY c DESC NULLS LAST` over a default index planned a full `Sort` over a `Seq Scan`.

## Unverified — do not assert these

- **PostgreSQL 18 behaviour for the buffer measurements above.** All plans were measured on 16.13. B-tree scan-key preprocessing changed in 17 and 18, including the skip-scan optimisation. The documented semantics cited are from the 18 docs; the *measurements* are 16.13 only.
- **No current PostgreSQL documentation page states that row comparisons use a multicolumn index.** The index and B-tree chapters do not mention row constructors. The explicit statement exists only in the 8.2 release notes, corroborated by planner source and by the observed plans above. Treat the claim as verified by behaviour, not by current documentation.
- **PostgreSQL source quotations** were read from the official `postgres/postgres` GitHub mirror rather than `git.postgresql.org`, which refuses automated fetch. Content is expected to be identical; it is one remove from the canonical host.
- **Final merge state of `laravel/framework#38250`**, the attempted null-handling fix. What is confirmed is that no null handling exists in `13.x`.
- **Laravel's intended behaviour for `cursorPaginate` with `distinct`, `groupBy`, or `having`.** Neither the docs nor the code address it. Since this skill forbids `cursorPaginate` on list routes, nothing depends on it.
- **The `chunk()` versus `chunkById()` distinction** in `10-route-mode-and-sort-allowlist.md` is stated from Laravel's documented guidance and was **not independently re-verified in this session**.
- **The `-infinity` sentinel and generated-column immutability** in `50-hard-cases.md`: `'-infinity'` is a valid `timestamptz` value, but whether a specific `COALESCE` expression qualifies as immutable for a stored generated column was not tested and must be checked in the migration.
