# Traversal mode and sort allowlist

## Choosing the mode

Three modes exist on this platform. A route uses exactly one, and its documentation names which.

**Keyset cursor — the default.** Every public or user-facing collection, every feed, comment thread, notification list, activity log, watch history, and every collection whose size grows with tenant data. No justification is required to choose it; a justification is required to choose anything else.

**Chunked primary-key traversal — service-internal only.** Exports, backfills, reindexes, migrations, and any traversal the service runs against itself. These never go through a paginated public route, because a public route applies authorization, serialisation, and rate limits per page, and an export that pages through it multiplies all three by the row count.

Use `chunkById` or `lazyById` in Laravel, or a repeated keyset query over the primary key in Go. `chunk()` is forbidden: it pages by `OFFSET`, so when the callback updates or deletes rows in the chunk it just read, the offset for the next chunk points past rows that were never visited. `chunkById` re-anchors on the last primary key it saw and is therefore stable under that mutation.

Observable: no export, command, or job in the repository calls a paginator that accepts a page number, and no call to `chunk(` exists on a traversal whose callback writes.

**Offset — narrow exception.** Apply all five conditions in
`alaa-services-contract references/25-end-to-end-flow-and-boundaries.md`, `Admin-table offset exception`.
That section alone authorizes offset and its distinct envelope; this file maintains no second list.
Deep `OFFSET` reads and discards skipped rows on every request, and an unbounded exact-total query
hides an independent scan behind a bounded page. Those costs are why both page/offset bounds and
filtered, production-shaped total-query measurements remain required by the owner.

## Building the sort allowlist

A route accepts sort as a closed set of named modes. It never accepts a column name.

Reason: a request-supplied column name is two defects at once. It reaches the query builder's `orderBy`, which is an injection surface in every framework that interpolates identifiers; and it promises an ordering for which no index exists, so the first client to use an unindexed sort turns a bounded query into a full scan under `ORDER BY`.

Each mode resolves server-side, through a constant lookup, to a fixed tuple of `(columns, direction)`. Adding a mode is a code change and a migration, never a configuration value a client can widen.

Every allowlisted mode carries all four of the following, or it is not allowlisted:

- a deterministic ordering whose final component is unique under the route's filters;
- one direction shared by every component of the tuple;
- a cursor schema listing exactly the tuple's columns;
- a committed index that serves the tuple under the route's filters, proven by `EXPLAIN (ANALYZE, BUFFERS)` at the route's maximum `limit`.

Worked example for a content feed:

```
newest   -> ORDER BY published_at DESC, id DESC
popular  -> ORDER BY popularity_score DESC, id DESC
```

Both end in `id`, both are single-direction, and each needs its own index. `popular` additionally orders on a value that changes, which routes it through the ranking-epoch rule in `50-hard-cases.md`; a mutable sort column is allowlisted only once that rule is satisfied.

Observable: the handler maps the request's sort value through a constant lookup with a default, rejects an unrecognised value with `400` and `INPUT_VALIDATION_FAILED`, and no string originating in a request reaches `orderBy`, `orderByRaw`, or an interpolated `ORDER BY`. A grep for the request parameter's name finding it inside a query-builder ordering call is the failure this rule exists to prevent.

## Filters follow the same rule

A filter a client can send is allowlisted the same way and for the same reason: each allowlisted filter combination that a route accepts must be servable by a committed index alongside the ordering. A route that accepts an open set of filter columns cannot state which index serves it, and therefore cannot satisfy step 4 of the decision procedure.
