---
name: alaa-keyset-pagination
description: "Keyset (cursor) pagination design for Ala list routes: deciding whether a route paginates and by which sorts, deriving an ordering tuple whose final component is unique, building the index that serves it, and defining a signed cursor that carries its filter and sort context. Use when adding or reviewing a list endpoint, feed, comment thread, notification list, or infinite-scroll surface; when paging through a list repeats or drops rows; when a list query is slow on later pages; when choosing between cursor, offset, and chunked traversal; and before claiming backward pagination works. Do not use for a collection bounded by schema rather than by data, which needs no cursor. Route the collection and error envelopes to /alaa-services-contract; index and query mechanics to /alaa-data-layer; unbounded result sets to /alaa-algorithms-data-structures; cursor tampering to /alaa-security-review; test design to /alaa-testing-strategy."
---

# Alaa Keyset Pagination

Decide whether a route paginates, by which orderings, over which index, with which cursor, and under which failure behaviour. The goal: every list surface in the fleet traverses a growing table without repeating or dropping a row. Correctness is the deliverable, and it is the hard part. A paginated list that silently skips rows returns a well-formed `200` with a plausible row count. It raises no client error and fires no alert. A test that asserts only on status code and schema never sees it.

This skill owns the pagination decision, not the wire envelope, index syntax or framework idiom.
Write cross-skill calls once as `/name`, per the pack's `AGENTS.md`.

## When this applies

Apply this skill to:

- any route that returns a collection whose size grows with tenant data;
- any change to a list route's filters, sort options, ordering, or page size;
- any new feed, comment thread, notification list, activity log, watch history, or infinite-scroll surface;
- any export or background traversal over a table;
- any report that a list repeats rows, drops rows, or degrades on later pages;
- any review of a query that pairs `ORDER BY` with `LIMIT`.

It does not apply to a route whose result set is bounded by schema rather than by data, such as a fixed catalogue of enum values or a per-user list capped by a hard schema limit. That route declares `paginated: false` per `alaa-services-contract` `references/25-end-to-end-flow-and-boundaries.md` and returns `data` with no cursor. A set that grows with tenant data may not use that declaration, however small it is today.

## The two rules that silently corrupt results

Everything else here follows from these two rules. Both fail without an error. For that reason they come before the procedure.

**Ordering must be unique.** Every paginated query orders by a column tuple. The final component of the tuple must be unique within the filtered set. The cursor encodes every component of the tuple. Never make a non-unique column the final component, because the continuation predicate compares strictly: every row that shares the boundary row's sort value is dropped from the following page. The response stays well-formed and the rows are gone. Use `id` as the tie-breaker unless the route documents another column proven unique under the same filters.

**A cursor is valid only for the filter and sort context that produced it.** When the service issues the cursor, it binds the filter values, sort key, sort direction, and tenant or scope into the signed cursor. The service compares the bound context against the context of the request that presents the cursor. The service never reconstructs that context from the request's own parameters. Reason: a boundary computed in one ordering has no meaning in another. A replay under changed filters produces a page that looks entirely correct and is not. A mismatch returns `INVALID_CURSOR_CONTEXT`, never a page.

## Decision procedure

Work in order. Each step names the observable that decides whether it is done. A step whose observable cannot be checked is not done.

**1. Choose the traversal mode.** Route by consumer, not by preference.
- A public or user-facing collection, feed, comment thread, notification list, activity log, watch history, or any collection growing with tenant data: use a keyset cursor. This is the default and needs no justification.
- An export, backfill, reindex, or any traversal the service runs against itself: use chunked primary-key traversal. Never use a paginated public route. `chunk()` is forbidden: it pages by offset and drops rows when the callback mutates the rows it is walking.
- An admin table that genuinely requires exact totals and page numbers: use offset, and only when every one of the five conditions in `references/10-route-mode-and-sort-allowlist.md` holds. "An operator asked for totals" is not one of them.

Observable: the route documentation names exactly one of these three modes, and the call site in the repository matches the mode named.

**2. Fix the sort allowlist.** Enumerate the accepted sort keys as a closed set of named modes, such as `newest` and `popular`. Never accept a raw column name from the request. Resolve each mode server-side to a fixed `(columns, directions)` tuple. Reason: a request-supplied column name is an injection surface and a promise that no index exists to keep. Observable: the handler maps the request value through a constant lookup and rejects an unknown value with `400` / `INPUT_VALIDATION_FAILED`; no request string reaches the query builder's `orderBy`.

**3. Derive the ordering tuple.** For each allowlisted mode, append the unique tie-breaker to the sort column. Give every component the same direction. Mixed directions such as `ORDER BY published_at DESC, id ASC` are forbidden on Ala list routes. Reason: a mixed tuple has no row-value comparison form, so its predicate degrades to the `OR` expansion that step 5 rejects. Observable: every allowlisted mode's `ORDER BY` ends in a unique column and uses one direction throughout.

**4. Build the index that serves it.** Create one index per allowlisted mode: equality-filter columns first, then the ordering tuple in order. Observable: `EXPLAIN (ANALYZE, BUFFERS)` on the route's own query at the route's maximum `limit`, against production-shaped row counts, shows an index scan with no `Sort` node and a buffer count that does not grow with page depth. The `Index Cond` line alone does not prove it. Postgres prints the original qualifier there even when the range is loose. Buffers are the observable, not the plan text. Details and the mixed-direction and `NULLS` cases are in `references/20-ordering-index-and-predicate.md`.

**5. Write the continuation predicate as a row-value comparison.** Example: `WHERE (published_at, id) < ($1, $2)` for a `DESC` traversal. The expanded form `a < $1 OR (a = $1 AND b < $2)` is forbidden on Ala routes. Reason: with `ORDER BY` present, Postgres cannot combine its branches through a bitmap without destroying the ordering, so it falls back to filtering over a full index scan. Measured on a 173k-row table, the `OR` form read 173,475 buffers where the row-value form read 13. Observable: no list query in the repository contains an `OR` between two ordering-column comparisons.

**6. Define the cursor.** The cursor carries the full ordering tuple, the sort mode, the direction, a normalised filter-context hash, a schema version, and an expiry where the data is security-sensitive or reorders rapidly. Sign it with HMAC and keep it opaque. Base64 is an encoding, not a protection: an unsigned cursor is a client-controlled value fed straight into query bindings. Observable: the encoder and decoder live in one shared component, the decoder verifies the signature before it parses any field, and a cursor with a flipped byte is rejected rather than decoded. Layout and versioning are in `references/30-cursor-format-integrity-and-context.md`.

**7. Bind the context and enforce it.** Implement rule two above: compare the cursor's bound context hash to the current request's normalised context, and reject a mismatch. Observable: a test changes one filter value while it replays a valid cursor and asserts `400` / `INVALID_CURSOR_CONTEXT`.

**8. Handle the hard cases before shipping, not after.** `references/50-hard-cases.md` holds the settled platform answer for each of these: nullable sort columns, mutable sort values, backward traversal, and the insert/delete/update consistency semantics. Backward traversal is the feature most often claimed and least often correct. A route does not document backward pagination unless the reversal tests in `references/70-test-list.md` pass.

**9. Set the limits.** Take the default, maximum and measured-exception rule from
`alaa-services-contract references/22-failure-load-and-deprecation-contract.md`, `List page-size values`.
Apply that skill's reject/no-clamp wire rule. Observable: step 4 proved the route's query at its exact maximum.

**10. Prove it.** Cover every item in `references/70-test-list.md`, or waive it explicitly with a reason in the route documentation.

## Platform decisions settled here

**Wire decisions.** `alaa-services-contract references/25-end-to-end-flow-and-boundaries.md` owns
request/response keys, their exclusions and the offset exception. `references/40-wire-contract-limits-and-errors.md`
keeps the algorithm rationale and cursor-failure handling. It defines no second envelope.

**Laravel's native `cursorPaginate` is not the shipped paginator on an Ala list route.** It fails four platform rules at once, verified against framework source rather than inferred. Read `references/60-per-stack.md` for the evidence and the required replacement.

**Row-value comparison is mandatory**, per step 5. It is what forbids mixed-direction sort tuples in step 3.

## Stop conditions

Stop and raise the question. Do not decide alone when:

- the only unique tie-breaker available is a private database identifier that the route must not expose, and the cursor cannot be signed (`alaa-services-contract` permits private identifiers inside a signed opaque cursor, and not otherwise);
- a requested sort key has no column that is unique under the route's filters;
- a route needs both exact totals and cursor traversal;
- an existing live route already emits a different collection shape, and changing it would break a published consumer.

## References

- Traversal-mode routing, the five conditions permitting offset, and sort-allowlist construction — read when deciding whether a route paginates at all or what it may sort by: `references/10-route-mode-and-sort-allowlist.md`
- Ordering tuples, composite index construction, row-value versus `OR` predicates, mixed directions, `NULLS` placement — read when writing the query or the migration: `references/20-ordering-index-and-predicate.md`
- Cursor payload, encoding, HMAC signing, schema version, expiry, context hashing — read when implementing or changing the cursor codec: `references/30-cursor-format-integrity-and-context.md`
- Request parameters, response keys, limits, and the exact error codes with their statuses — read when defining the route's wire surface or its rejection behaviour: `references/40-wire-contract-limits-and-errors.md`
- Nullable sort columns, mutable sort values and ranking epochs, backward traversal, insert/delete/update consistency semantics — read when the sort column can be null, can change, or when backward paging is requested: `references/50-hard-cases.md`
- Laravel and Go implementation verdicts, including why `cursorPaginate` is rejected and what replaces it — read before writing paginator code in either stack: `references/60-per-stack.md`
- The covered-behaviour list a paginated route must satisfy — read when writing or reviewing the route's tests: `references/70-test-list.md`
- Primary sources, versions, retrieval dates, and what remains unverified — read before repeating any version-sensitive claim in this skill: `references/90-source-map.md`

## When NOT to use

- The collection is bounded by schema rather than by data: a fixed enum, a per-record set that a constraint
  caps, a list whose maximum length is enforced at write time. It cannot grow, so it needs no cursor.
- The route returns a single record, or one aggregate computed over a window the server chooses.
- The traversal is an internal export or backfill that may hold a snapshot and read to the end.
- The question is the collection or error envelope, the index mechanics behind the ordering, or cursor
  tampering, rather than how the route traverses. The section "What this skill does not own" names each owner.

## What this skill does not own

- **The collection envelope, the error envelope, identifier exposure, and the reject-don't-clamp rule**: `/alaa-services-contract`. This skill decides what goes in `meta` for a keyset list. It defers to that skill on the envelope those keys sit in.
- **Index and query mechanics in general**: `/alaa-data-layer`. This skill states which index a paginated route needs and why. That skill owns index design, migration safety, and query tuning beyond pagination.
- **Why an unbounded result set is a defect**: `/alaa-algorithms-data-structures`. This skill sets the page ceiling. That skill owns the complexity argument behind bounding a result set at all.
- **Cursor tampering as a trust-boundary concern**: `/alaa-security-review`. This skill requires the cursor to be signed and states what the signature must cover. That skill owns threat classification, key handling, and fail-closed doctrine.
- **What makes a test a test**: `/alaa-testing-strategy`. `references/70-test-list.md` names what must be covered. That skill judges whether a given test actually proves it and at which layer it belongs.
- **Model and effort selection, and every runtime capability claim**: `/alaa-prompting-guide`.
