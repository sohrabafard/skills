# Hard cases

Four cases where a route that looks finished is not. Each has a settled platform answer, because each was previously left to judgement and judgement produced a different answer per service.

## Nullable sort columns

**Rule: no column in an ordering tuple is nullable on an Ala list route.**

Two independent failures, both verified against PostgreSQL:

- A row-value comparison containing a null evaluates to **unknown**, not true or false. PostgreSQL's documented semantics compare elements left to right and stop at the first unequal *or null* pair; if either element of that pair is null the whole comparison is null. `WHERE (published_at, id) < ($1, $2)` with a null `$1` therefore matches nothing, and every row past the boundary is silently dropped. No error is raised. Confirmed empirically: `(1, NULL) < (1, 2)` returns `NULL`.
- Serving a non-default null placement costs the index. `ORDER BY col DESC NULLS LAST` needs a purpose-built `(col DESC NULLS LAST)` index that then cannot serve plain `ORDER BY col` — see `20-ordering-index-and-predicate.md`.

**Required replacement, not merely a prohibition.** Where the domain column is genuinely nullable, add a `NOT NULL` sort column beside it, order on that, and index that:

```sql
ALTER TABLE contents ADD COLUMN sort_published_at timestamptz NOT NULL DEFAULT '-infinity';
-- backfill: sort_published_at = COALESCE(published_at, '-infinity')
CREATE INDEX contents_sort_published_at_id_idx ON contents (sort_published_at, id);
```

`'-infinity'` is a real `timestamptz` value, so unpublished rows sort last under `DESC` with no `NULLS` clause and no special-case predicate. Keep the two columns consistent with a stored generated column where the expression qualifies as immutable in the target PostgreSQL version, and with a trigger or an application-layer write path otherwise — verify which applies in the migration rather than assuming, because a generated-column expression that is merely stable is rejected at `CREATE`.

Observable: `information_schema.columns` reports `is_nullable = 'NO'` for every column named in any allowlisted sort mode's ordering tuple.

## Mutable sort values

**Rule: the ordering columns of an allowlisted sort mode do not change value for a row while a traversal that could reach it is in flight.**

A row whose sort value changes mid-traversal moves across the boundary: it is returned twice if it moves backward, or never if it moves forward. Keyset pagination cannot detect this, because the boundary is a value and the value moved.

Columns that satisfy the rule directly: `id`, `created_at`, `published_at` — set once and not rewritten.

Columns that do not: live view counts, engagement scores, "trending" ranks, anything a counter or a recommendation job updates continuously. Ordering by these is forbidden as a live column.

**Required replacement: ranking epochs.** Compute the ranking in a batch that writes a new epoch rather than mutating the current one. Each row carries `(ranking_epoch_id, rank, id)`; the ordering tuple is `rank, id` filtered to one `ranking_epoch_id`; the epoch is part of `ctx` in the cursor. A traversal therefore completes against the epoch it started in, and a cursor from a retired epoch fails with `INVALID_CURSOR_CONTEXT` rather than silently reordering under the client. Retain at least the previous epoch for as long as a cursor may live, or every publish invalidates every traversal in flight.

Where an epoch is not affordable, the ranking belongs in the search engine and paginates by that engine's own mechanism, not by a database keyset. Do not compromise by ordering on a live counter with a tie-breaker: the tie-breaker fixes ties, not movement.

Observable: for every allowlisted sort mode, either every ordering column is write-once, or the mode's ordering is filtered by an epoch identifier that also appears in `ctx`.

## Backward traversal

This is the feature most often claimed and least often correct, so the platform rule is about the claim: **a route documents backward pagination only when the reversal tests in `70-test-list.md` pass against it.** Emitting a `prev_cursor` is a claim.

Correct backward traversal has three steps, and the third is the one that gets dropped:

1. Invert the comparison operator — `>` where the forward page uses `<`.
2. Invert the `ORDER BY` direction, so the database still returns the rows adjacent to the boundary and `LIMIT` still cuts at the right end.
3. **Reverse the returned rows in the application before serialising**, so the response is in the route's declared order rather than in the internal scan order.

Skipping step 3 yields a page whose rows are individually correct and collectively backwards — which reads as a rendering bug and gets chased in the client.

Both cursors are recomputed from the returned page's own first and last rows after that reversal, never carried over from the request. A `prev_cursor` derived from the pre-reversal ordering points the wrong way, and the traversal oscillates between two pages.

The same index serves both directions when the tuple is single-direction, because a B-tree index scanned backward satisfies the reversed ordering — one more reason mixed directions are forbidden.

## Insert, delete, and update during traversal

Keyset is materially more stable here than offset, which is why the platform chose it, but it is not a snapshot and must not be documented as one. The three semantics a route documents are listed in `40-wire-contract-limits-and-errors.md`.

Where a traversal genuinely requires a consistent snapshot — a financial export, a reconciliation run — it is not a paginated route at all. It is a chunked traversal inside a repeatable-read transaction, or a traversal bounded by an explicit `created_at <= $snapshot` predicate carried in `ctx` so that later inserts cannot enter the result set. Choose the bound explicitly; do not obtain it by accident from a filter that happens to exclude new rows today.
