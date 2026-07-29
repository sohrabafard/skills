# API and Data Shaping — the client-side half

What a screen asks the API for, and the cost that request imposes. The wire contract itself is not here.

- Envelope shape, error codes, field names, problem-details usage, SDK consumption:
  `/alaa-services-contract` (`$alaa-services-contract`) `references/10-core-service-contract.md` and
  `references/60-frontend-sdk-consumption-contract.md`. Do not invent a second envelope or a second error
  format for one endpoint.
- Cursor and keyset pagination — the cursor format, its integrity, the sort allowlist, the tie-breaker
  rule, the limits and the error for an unsupported sort: `/alaa-keyset-pagination`
  (`$alaa-keyset-pagination`) `references/30-cursor-format-integrity-and-context.md` and
  `references/40-wire-contract-limits-and-errors.md`.
- Query shape, indexes and aggregate cost once the fix crosses into the server: `/alaa-data-layer`
  (`$alaa-data-layer`) and `/alaa-laravel-architecture` (`$alaa-laravel-architecture`).

## Before changing what a screen requests

Inspect the current call sites, the repo's existing error handling, the current pagination and sorting
behaviour, the payload size and the duplicate-request pattern — and ask whether the reported "frontend
bug" is really a query-shape or aggregation problem on the server.

## The client-side cursor delta

The contract is the pagination skill's. What this skill owns is what the client does with it:

- A cursor is opaque. Do not parse it, do not derive a page number from it, and do not construct one.
- Keep the cursor with the list state it belongs to, and drop it when the sort or filter changes — a
  cursor issued under one ordering is meaningless under another.
- Never render a total page count from a cursor-paginated endpoint; the endpoint does not have one.
- Deduplicate on the stable id when appending, because a concurrent insert can return a row the client
  already holds.

## Cost rules the UI owes the backend

- No request per row. A list that fans out one request per item is the N+1 family —
  `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) `references/40-call-in-a-loop.md`
  — and the fix is a batch lookup or an aggregate endpoint, not a faster spinner.
- Debounce server-backed search and typeahead, and abort the superseded request
  (`20-vue-js-ssr-patterns.md`).
- Split a compact list payload from the expensive detail payload; fetch detail when the record opens.
- Do not ask for an exact total count on a hot path unless the product requires the number.
- Keep nested expansion bounded: request named includes, not every relation the screen "might need later".
- Ask for a server-computed facet, count or summary when it replaces many client-driven requests.

## Cache and revalidation, as the client sees it

Hashed static assets cache aggressively. Personalized HTML and authenticated API responses are `private`.
Prefer `private, no-cache` plus a validator where revalidation is safe; reserve `no-store` for a response
that must never be written to any cache. Use `ETag` or `Last-Modified` when revalidation saves meaningful
bandwidth or backend cost.

```http
GET /api/profile
If-None-Match: "profile-v42"
```

```http
HTTP/1.1 304 Not Modified
ETag: "profile-v42"
Cache-Control: private, no-cache
```

On a `304`, the UI reuses the held value and does not re-render — a re-render on unchanged data is the
polling cost that looks like a performance bug. Response bodies kept across a reload belong in
`/alaa-indexeddb-browser-storage` (`$alaa-indexeddb-browser-storage`) `references/70-cache-and-drafts.md`,
not in an ad-hoc module-level map.

## Anti-patterns

Inventing an error envelope for one endpoint. Parsing a cursor. Rendering a total for a cursor endpoint.
Loading totals, counts and heavy details for every list row. Marking every authenticated response
`no-store` when `private, no-cache` plus a validator would work. Treating a backend query problem as a
spinner problem.

## References

- RFC 9457 Problem Details for HTTP APIs:
  [rfc-editor.org](https://www.rfc-editor.org/rfc/rfc9457.html) — read: unverified as of 2026-07-28.
- MDN HTTP caching:
  [developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching) — read:
  unverified as of 2026-07-28.
