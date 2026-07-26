# What a paginated route must cover

This file names the behaviours that must be covered. It does not judge whether a given test proves its behaviour, which layer it belongs at, or what evidence a reviewer may accept — that is `alaa-testing-strategy` (`/alaa-testing-strategy`, `$alaa-testing-strategy`), and every item here is subject to its core rule. In particular: a test that asserts only the HTTP status and the response schema does not cover any item on this list, because every failure this skill exists to prevent returns a well-formed `200`.

A route is not shippable until each item is covered or explicitly waived with a reason recorded in the route documentation.

## Traversal correctness

1. **Ties at the page boundary.** Seed more rows sharing one sort value than fit in a page, so a tie straddles the boundary. Traverse fully and assert the set of returned identifiers equals the seeded set exactly — no duplicates, no omissions. This is the test that fails when the tie-breaker is missing, and the only one that does.
2. **Full forward traversal.** Page from the first cursorless request to `next_cursor === null`, collecting identifiers. Assert exact set equality with the seeded set, and assert the concatenated order matches the declared ordering.
3. **First page.** A request with no cursor returns the ordering's first rows and a non-null `next_cursor`.
4. **Final page.** The last page returns `next_cursor === null`. Cover the case where the final page is exactly full: a full page must still report `null` when nothing follows, which is what the `limit + 1` fetch exists to get right.
5. **Empty result set.** `data` is `[]`, `next_cursor` is `null`, and the response is `200`.
6. **Single-page result.** Fewer rows than `limit`: both cursors `null`, all rows returned.

## Backward traversal

Cover these only if the route emits `prev_cursor`; if it cannot pass them, it does not emit one.

7. **Backward returns the previous page exactly.** Page forward twice, then follow `prev_cursor`, and assert the page returned equals page one — same identifiers, same order. This is the test that fails when the application-side row reversal is missing.
8. **Round trip is stable.** Forward, backward, forward again returns to the same page rather than drifting or oscillating.
9. **Backward from the first page.** `prev_cursor` is `null` on page one, and a backward cursor at the start of the collection returns an empty page rather than wrapping.

## Cursor integrity

10. **Malformed cursor.** Not valid base64, and valid base64 that is not valid payload: both `400` with `INVALID_CURSOR`.
11. **Tampered cursor.** Flip one byte of the payload of a genuine cursor: `400` with `INVALID_CURSOR`, and assert the query was never executed — a rejected cursor that still ran the query means the check sits after the work.
12. **Forged cursor.** Construct a well-formed payload and sign it with a wrong key: rejected. Covers the case where the code verifies the payload's shape but not its signature.
13. **Expired cursor.** Where `exp` is used: `400` with `CURSOR_EXPIRED`.
14. **Unsupported version.** A cursor with an unknown `v`: `400` with `CURSOR_VERSION_UNSUPPORTED`, and no attempt to interpret its `k` values.
15. **No internal detail leaks.** For every rejection above, assert the response body contains neither a decoded field name nor a column name nor a signature fragment. Assert on absence, not on the error code alone.

## Context binding

16. **Changed filter.** Replay a valid cursor with one filter value changed: `400` with `INVALID_CURSOR_CONTEXT`, not a page.
17. **Changed sort mode.** Replay a valid cursor under a different allowlisted sort: `400` with `INVALID_CURSOR_CONTEXT`.
18. **Changed direction.** Same, for direction.
19. **Cross-tenant or cross-scope replay.** A cursor issued in one tenant or audience scope, replayed in another, is rejected. Assert that no row from the issuing scope appears in the response — the leak, not just the status code.
20. **Equivalent filters still work.** Two spellings of the same filter — `2026-07-25` and `2026-07-25T00:00:00Z`, or parameters in a different order — produce the same `ctx` and traversal continues. This is the test that catches over-strict canonicalisation, which breaks valid clients intermittently.

## Input validation

21. **`limit` above the maximum** is rejected with `400` and `INPUT_VALIDATION_FAILED`, not clamped. Assert the response is an error, not a short page.
22. **`limit` of zero, negative, and non-numeric** are each rejected.
23. **Unknown sort value** is rejected, and the rejected string never reaches the query.
24. **Offset parameters are inert.** Sending `page`, `per_page`, `offset`, or `skip` does not change the response — a route that quietly honours one is the route a client builds page-number navigation against.

## Concurrent modification

Each of these seeds a page, mutates between requests, and asserts the documented semantics from `40-wire-contract-limits-and-errors.md` — the point is that behaviour matches what the route promises, not that nothing changed.

25. **Insert between pages**, ahead of the cursor: the new row does not appear in the current traversal, and no existing row is dropped.
26. **Delete between pages**: the traversal completes without error and returns every surviving row.
27. **Update of an ordering column between pages**: assert the documented outcome. If the route claims a row cannot move, this test must fail when the mutable-value rule in `50-hard-cases.md` is violated.

## Performance

28. **Deep-page cost is flat.** `EXPLAIN (ANALYZE, BUFFERS)` at the route's maximum `limit`, at the first page and at a deep cursor, against production-shaped row counts. Assert no `Sort` node and a buffer count that does not grow with depth. Assert on buffers rather than on the `Index Cond` text, which stays identical even when the index range is loose.
