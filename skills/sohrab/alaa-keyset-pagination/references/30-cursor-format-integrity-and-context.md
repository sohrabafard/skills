# Cursor payload, integrity, and context binding

`alaa-security-review` (`/alaa-security-review`, `$alaa-security-review`) owns threat classification, key custody, and fail-closed doctrine. This file owns what the cursor must contain and what the service must check before trusting it.

## Payload

One shared codec per service. Every paginated route uses it; a route that hand-rolls its own encoding is the route whose cursor is later found unsigned.

```json
{
  "v": 1,
  "sort": "newest",
  "dir": "forward",
  "k": { "published_at": "2026-07-25T18:30:00Z", "id": 84521 },
  "ctx": "9f2c…",
  "exp": 1785000000
}
```

- `v` — cursor schema version. Required. An unrecognised version is rejected with a stable error, never best-effort parsed, because a cursor issued before an ordering change encodes a boundary in the old ordering.
- `sort` — the allowlisted sort mode name, not a column list.
- `dir` — `forward` or `backward`. Direction lives here, not in the request parameter, so a client cannot pair a forward boundary with a backward traversal.
- `k` — every component of the ordering tuple, keyed by column, with the values read from the boundary row. A cursor built only as `after_id` is correct only when the ordering is permanently `id` alone; write the full tuple even when it is currently a single column, because adding a sort column later would otherwise silently reinterpret every cursor in flight.
- `ctx` — the normalised filter-context hash. See below.
- `exp` — absolute expiry. Required where the data is security-sensitive or reorders rapidly; optional otherwise. An expiry bounds how long a boundary computed under an old snapshot can be replayed.

**Nothing else.** No user identity beyond what `ctx` already covers as scope, no permission decision, no internal table or column names beyond the ordering columns, and no value the client is not already entitled to see the effect of. The cursor may carry private database identifiers — `alaa-services-contract` `references/25-end-to-end-flow-and-boundaries.md` permits that specifically inside a signed opaque cursor and nowhere else — which is a further reason the signature is not optional.

## Encoding and integrity

Encode the payload compactly, sign it with HMAC-SHA256 over the exact encoded bytes, and emit signature and payload together in one URL-safe string.

**Base64 is an encoding, not a protection.** An unsigned cursor is a client-controlled value whose ordering-column contents are bound directly into a query. Treat every cursor as untrusted input on arrival.

Verification order is load-bearing: **verify the signature first, then parse.** A decoder that parses fields before checking the MAC has already fed attacker-chosen structure to the parser, and any type confusion or resource exhaustion in parsing happens before the check that would have prevented it.

After the signature verifies, still validate: `v` is supported; `sort` is in the allowlist; `dir` is one of the two values; `k` contains exactly the columns the named sort mode declares, each of the declared type; `exp`, when present, is in the future. A signed cursor proves the service issued it, not that it is still meaningful.

Key handling — rotation, storage, and the shared-secret boundary — is `alaa-security-review`'s. Sign with a service-held secret, not a value derivable by a client, and support verifying against a previous key during rotation so a rotation does not invalidate every cursor in flight at once.

## Context binding

**Rule: a cursor is valid only for the filter and sort context that produced it, and the service enforces that from the cursor's contents, never from the request's own parameters.**

Compute `ctx` as a hash over a canonical serialisation of everything that changes which rows exist and in what order:

- every applied filter value, in a fixed key order, with values normalised — a date range serialised identically whether the client sent `2026-07-25` or `2026-07-25T00:00:00Z`;
- the sort mode and direction;
- the tenant, scope, or audience that bounds the result set.

Canonicalisation matters more than the hash function. Two requests that mean the same query must produce the same `ctx`, or valid pagination breaks intermittently and only for clients that format parameters differently; two requests that mean different queries must not collide, or the rule does not hold.

On each request carrying a cursor, recompute `ctx` from the current request and compare. A mismatch returns `400` with `INVALID_CURSOR_CONTEXT` and the message form in `40-wire-contract-limits-and-errors.md`.

Why the check cannot be skipped by simply re-deriving filters from the cursor instead: the request also carries filters, and a service that ignores them silently serves a different query than the one the client asked for. Comparing, and rejecting on mismatch, is the only behaviour where the client learns what happened.

**Do not exempt the sort mode from `ctx` on the grounds that `sort` is already a field.** Both are present deliberately: `sort` tells the service which ordering to resolve, `ctx` proves the client has not changed it since the boundary was computed.

## Versioning and expiry behaviour

Bump `v` whenever the ordering tuple of any sort mode changes, whenever a column's serialised type changes, or whenever the `ctx` canonicalisation changes. Old versions fail predictably with `CURSOR_VERSION_UNSUPPORTED` rather than being migrated in place — an in-place migration would have to guess a boundary in the new ordering, which is the corruption the version field exists to prevent.

Clients recover from every one of these rejections the same way: drop the cursor and request the first page. State that in the route documentation so the recovery path is designed rather than discovered.
