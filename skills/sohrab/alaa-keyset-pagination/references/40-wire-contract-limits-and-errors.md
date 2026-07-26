# Wire surface, limits, and errors

`alaa-services-contract` (`/alaa-services-contract`, `$alaa-services-contract`) owns the collection envelope and the error envelope. This file states only what keyset pagination adds inside them, and why each addition was chosen over the alternative.

## Request

Exactly two parameters. Both are already bound by the contract.

- `cursor` — the opaque string a previous response returned, echoed back unchanged. Absent means "first page". The client never constructs one and never parses one.
- `limit` — positive integer. Default 20. Maximum 100 unless the route documents a measured reason and the contract records the higher value.

`page`, `per_page`, `offset`, `skip`, `after`, and `before` are not accepted. An out-of-range `limit` is rejected with `400` and `INPUT_VALIDATION_FAILED`, never clamped — a client that asked for 500 and silently received 100 cannot tell it received a partial answer.

**Why not `after` / `before`.** The owner's source document proposes them; this platform rejects them. Direction is a property of the boundary, not of the request: it is written into the signed cursor when the cursor is issued, so the client simply echoes back whichever of `next_cursor` or `prev_cursor` it holds. A parameter-name split lets a client pair a forward boundary with `before`, producing an incoherent request the server would then have to detect and reject — a failure mode that does not exist when direction is inside the cursor. Renaming `cursor` to `after` would additionally break two live services through the deprecation procedure for no semantic gain.

## Response

```json
{
  "data": [],
  "meta": {
    "next_cursor": "…",
    "prev_cursor": null
  }
}
```

Both keys are always present. `null` means no page exists in that direction. A key that is omitted rather than null cannot distinguish "last page" from "this service forgot the cursor".

**Why `meta` and not a `pagination` object.** `meta` is already the fleet's collection envelope and two services emit it today. A sibling `pagination` object would give the platform two collection shapes, so every consumer would carry two parsers and every reviewer would have to know which services use which — the same failure the single error envelope exists to prevent. `prev_cursor` and `next_cursor` are keyset-native, not offset artifacts, so they are admissible under the contract's existing rule barring `total`, `total_pages`, `current_page`, `last_page`, and `per_page` from `meta`.

**Why no `has_more`.** It is derivable: `has_more === (next_cursor !== null)`, always, by construction. A second spelling of one fact diverges the day a service computes `has_more` from `count($rows) > $limit` while computing `next_cursor` from something else, and consumers then split over which to trust. If it is ever added, it must be defined as exactly that expression and never computed independently.

**Why no `type` and no `limit` echo.** Every Ala list route is keyset, so `type: "cursor"` is constant across the fleet and carries no information while inviting clients to branch on it. The `limit` echo is equally empty: the client knows what it sent, and an invalid value produced a `400` rather than a page.

**Why no totals.** A cursor response must not imply an exact total it did not compute. Where an exact count is genuinely required, expose it through a separate aggregate endpoint or the analytics system, so its cost is visible and paid only when asked for.

## Consistency semantics the route must document

Keyset traversal is stable under concurrent writes in a way offset is not, but it is not a snapshot. State these in the route documentation so clients design for them:

- Rows inserted ahead of the current boundary are not returned during the current traversal.
- Rows deleted during the traversal disappear from later pages.
- A row whose ordering column is updated may move across the boundary and be returned twice or not at all.

Naming these is the deliverable. A client that knows a row may appear twice deduplicates by identifier; a client that assumes exactly-once renders duplicates.

## Errors

Every one uses the exact envelope in `alaa-services-contract` `references/10-core-service-contract.md` — one top-level `error` key carrying `status`, `code`, `message`, and `meta`, with no key omitted.

| Condition | Status | `code` |
|---|---|---|
| Cursor is not decodable, or the signature fails | 400 | `INVALID_CURSOR` |
| Cursor schema version is not supported | 400 | `CURSOR_VERSION_UNSUPPORTED` |
| Cursor has expired | 400 | `CURSOR_EXPIRED` |
| Cursor's bound filter, sort, or scope context does not match the request | 400 | `INVALID_CURSOR_CONTEXT` |
| `limit` out of range, or `sort` not in the allowlist | 400 | `INPUT_VALIDATION_FAILED` |

**A malformed cursor is a client error, not a server error.** It returns `400`, never `500`, and never an empty `200`. An empty `200` is the worst of the three: the client sees "no more results" and stops, so a broken cursor looks like the end of the feed.

**Distinguish tampering from expiry in the code, not in the message.** The four cursor codes are separate because a client's recovery is the same but an operator's diagnosis is not: a rise in `INVALID_CURSOR` is a tampering or key-rotation signal, a rise in `CURSOR_VERSION_UNSUPPORTED` is a deploy signal. Emit them as distinct codes so the two are separable in metrics.

**Never leak cursor internals.** `message` is one operational English sentence and never contains the decoded payload, the column names, the signature, the expected hash, or a database structure fragment. Do not put decoded fields in `error.meta` either — an error body is exactly where an attacker probing a cursor codec reads its structure.
