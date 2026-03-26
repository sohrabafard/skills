# API and Data Shaping

Use this file when frontend work depends on request and response shape, pagination, filtering, sorting, cache behavior, or payload efficiency.

This file owns frontend-facing API contract guidance. It does not replace backend implementation skills.

## Start here

Before changing an API contract, inspect:

- current frontend call sites
- current error-handling conventions
- current pagination and sorting behavior
- payload size and duplicate request patterns
- whether the reported "frontend bug" is really a backend query-shape or aggregation problem

## Contract defaults

- Prefer one stable envelope style per repo.
- If the repo already uses raw resources, JSON:API, or another established envelope, stay consistent.
- If the repo already uses Problem Details for errors, keep using it instead of inventing a second error format.
- Keep list ordering explicit and deterministic.

## Error-shape guidance

Preferred qualities:

- stable machine-readable code or type
- human-readable message or title
- source or field details for validation errors
- request or correlation identifier when the platform supports it

Pattern: Problem Details style error

```json
{
  "type": "https://api.example.com/problems/invalid-filter",
  "title": "Invalid filter",
  "status": 400,
  "detail": "Unsupported sort key: score",
  "instance": "/reports?page[size]=20&sort=score"
}
```

## Pagination defaults

Prefer cursor or keyset pagination when:

- the list is large
- rows can be inserted or deleted while users paginate
- stable low-latency pagination matters

Cursor rules:

- sort by a stable unique order
- if the primary sort field is not unique, append a unique tie-breaker
- reject unsupported sort combinations instead of silently returning unstable pagination

Offset pagination is acceptable when:

- datasets are small
- page-number UX is more important than raw scale
- exact totals are cheap enough and part of the product requirement

## Filtering and sparse payloads

- Allow only explicit filter and sort keys.
- Reject unknown filters with a structured error.
- Prefer sparse fieldsets or projection parameters for list endpoints with large records.
- Prefer explicit include or expand semantics over dumping every related entity into every response.
- Keep nested expansion bounded and documented.

Pattern: lightweight list response

```json
{
  "data": [
    { "id": "42", "title": "Budget 2026", "status": "published" }
  ],
  "meta": {
    "nextCursor": "eyJpZCI6IjQyIn0",
    "hasMore": true
  }
}
```

## Cache and revalidation guidance

- Hashed static assets can be cached aggressively.
- Personalized HTML and authenticated API responses are usually `private`.
- Prefer `no-cache, private` plus validators when the resource may be revalidated safely.
- Reserve `no-store` for truly sensitive responses that must never be written to browser or intermediary caches.
- Use `ETag` or `Last-Modified` when revalidation can save meaningful bandwidth or backend cost.

Pattern: conditional API response shape

```http
GET /api/profile
If-None-Match: "profile-v42"
```

```http
HTTP/1.1 304 Not Modified
ETag: "profile-v42"
Cache-Control: private, no-cache
```

## Frontend-aware DB efficiency rules

When the UI drives backend load, the frontend contract should help the backend stay efficient:

- avoid one-request-per-row patterns
- prefer batch lookups and aggregate endpoints for dashboards
- debounce server-backed search and typeahead
- split list summaries from heavy detail payloads
- avoid exact total counts on hot paths unless they are product-critical
- align cursor and sort behavior with fields the backend can index efficiently
- ask for server-computed facets, counts, or summaries when they replace many client-driven requests

## Patterns

Pattern: explicit include budget

- Good: `GET /posts?include=author,thumbnail`
- Better when large graphs exist: document which includes are allowed and cap the expansion depth

Pattern: list plus detail split

- list endpoint returns compact preview fields
- detail endpoint returns expensive relations only when the user opens the record

Pattern: cache-friendly polling

- repeated reads use validators such as `ETag`
- server returns `304` when data is unchanged
- UI avoids re-render churn on unchanged payloads

## Anti-patterns

- Inventing a new error envelope for one endpoint
- Cursor pagination without a stable unique sort
- Returning giant nested graphs because the frontend "might need them later"
- Forcing the UI to load totals, counts, and heavy details for every list row
- Using offset pagination on hot, fast-changing feeds without understanding the duplicate/skip trade-off
- Marking every authenticated response `no-store` when `private, no-cache` plus validators would work
- Treating a backend query problem as a pure frontend spinner problem

## Pairing guidance

- SSR auth, protected data, or token-aware request flows:
  - Also load `21-ssr-auth-and-session-patterns.md`
- When the real fix is backend schema, index, query-plan, or contract implementation work:
  - Pair with `$alaa-laravel-architecture` for Ala Laravel API implementation work
  - Pair with `$alaa-data-layer` for indexing, pagination cost, or query-shape work

## Useful standards and references

- RFC 9457 Problem Details for HTTP APIs:
  - [https://www.rfc-editor.org/rfc/rfc9457.html](https://www.rfc-editor.org/rfc/rfc9457.html)
- MDN HTTP caching guide:
  - [https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching)
- JSON:API cursor pagination profile:
  - [https://jsonapi.org/profiles/ethanresnick/cursor-pagination/](https://jsonapi.org/profiles/ethanresnick/cursor-pagination/)
