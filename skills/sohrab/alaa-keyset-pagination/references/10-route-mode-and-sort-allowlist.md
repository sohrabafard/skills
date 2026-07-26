# Traversal mode and sort allowlist

## Choosing the mode

Three modes exist on this platform. A route uses exactly one, and its documentation names which.

**Keyset cursor — the default.** Every public or user-facing collection, every feed, comment thread, notification list, activity log, watch history, and every collection whose size grows with tenant data. No justification is required to choose it; a justification is required to choose anything else.

**Chunked primary-key traversal — service-internal only.** Exports, backfills, reindexes, migrations, and any traversal the service runs against itself. These never go through a paginated public route, because a public route applies authorization, serialisation, and rate limits per page, and an export that pages through it multiplies all three by the row count.

Use `chunkById` or `lazyById` in Laravel, or a repeated keyset query over the primary key in Go. `chunk()` is forbidden: it pages by `OFFSET`, so when the callback updates or deletes rows in the chunk it just read, the offset for the next chunk points past rows that were never visited. `chunkById` re-anchors on the last primary key it saw and is therefore stable under that mutation.

Observable: no export, command, or job in the repository calls a paginator that accepts a page number, and no call to `chunk(` exists on a traversal whose callback writes.

**Offset — narrow exception.** `alaa-services-contract` `references/25-end-to-end-flow-and-boundaries.md` currently forbids offset pagination on any list a client can page through. The owner has ratified a narrow exception for admin tables that genuinely require exact totals and page numbers. Until that contract text records the exception, a new offset route needs the contract change first; do not ship one against the current text and do not treat this paragraph as the amendment.

The exception applies only when all five conditions hold:

1. The route is mounted under an admin-only path and requires an admin permission checked at request time.
2. The route is absent from the public gateway route table and from every published SDK and client bundle.
3. The route's own documentation records `pagination: offset` together with the named operational requirement that justifies it — which report, which operator workflow. "Totals are nice to have" is not a requirement.
4. The route enforces a maximum reachable offset, documented and rejected above that value. Deep `OFFSET` makes the database read and discard every skipped row on every request, so an unbounded offset route is a load defect that grows with the table.
5. The exact-total query is bounded by the same filters as the page query and is measured at production row counts. An unbounded `COUNT(*)` over a growing table is itself the defect.

Observable that decides compliance: a route emitting `total`, `total_pages`, `current_page`, `last_page`, or `per_page` that is reachable without an admin permission, or that appears in the public gateway route table, is a violation regardless of what its documentation says. Because those keys are forbidden inside `meta` by the contract, an offset route does not use the `meta` collection envelope at all; it uses a distinct envelope its documentation declares, so no consumer can mistake one for the other.

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
