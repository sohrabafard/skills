# Wire surface, limits, and errors

`alaa-services-contract references/25-end-to-end-flow-and-boundaries.md` owns pagination request/response
keys and cursor error-code rows; its reference 10 owns the error envelope and reference 22 the page-size
values. This file owns algorithm rationale, consistency documentation and safe cursor-failure handling.

## Request

Read the owning contract's `Request rules` and `List page-size values` before exposing parameters;
do not choose a local default or maximum.

**Why not `after` / `before`.** The owner's source document proposes them; this platform rejects them. Direction is a property of the boundary, not of the request: it is written into the signed cursor when the cursor is issued, so the client simply echoes back whichever of `next_cursor` or `prev_cursor` it holds. A parameter-name split lets a client pair a forward boundary with `before`, producing an incoherent request the server would then have to detect and reject — a failure mode that does not exist when direction is inside the cursor. Renaming `cursor` to `after` would additionally break two live services through the deprecation procedure for no semantic gain.

## Response

Use the owning contract's `Response rules`, including its null/presence semantics and excluded keys.
Keep one collection parser across services; a sibling envelope would require consumers to select a parser
by service. Cursor boundaries are computed from the trimmed, correctly ordered page, as the traversal
references require, rather than by independently guessing whether more rows exist.

**Why no totals.** A cursor response must not imply an exact total it did not compute. Where an exact count is genuinely required, expose it through a separate aggregate endpoint or the analytics system, so its cost is visible and paid only when asked for.

## Consistency semantics the route must document

Keyset traversal is stable under concurrent writes in a way offset is not, but it is not a snapshot. State these in the route documentation so clients design for them:

- Rows inserted ahead of the current boundary are not returned during the current traversal.
- Rows deleted during the traversal disappear from later pages.
- A row whose ordering column is updated may move across the boundary and be returned twice or not at all.

Naming these is the deliverable. A client that knows a row may appear twice deduplicates by identifier; a client that assumes exactly-once renders duplicates.

## Errors

Use `alaa-services-contract references/25-end-to-end-flow-and-boundaries.md`, `Cursor rejection codes`,
for each condition's registered code/status and its reference 10 for the error envelope. Sort and limit
validation use the owning input-validation contract. This file defines no parallel code registry.

**A malformed cursor is a client error, not a server error.** It returns `400`, never `500`, and never an empty `200`. An empty `200` is the worst of the three: the client sees "no more results" and stops, so a broken cursor looks like the end of the feed.

**Distinguish tampering from expiry in the code, not in the message.** The four cursor codes are separate because a client's recovery is the same but an operator's diagnosis is not: a rise in `INVALID_CURSOR` is a tampering or key-rotation signal, a rise in `CURSOR_VERSION_UNSUPPORTED` is a deploy signal. Emit them as distinct codes so the two are separable in metrics.

**Never leak cursor internals.** `message` is one operational English sentence and never contains the decoded payload, the column names, the signature, the expected hash, or a database structure fragment. Do not put decoded fields in `error.meta` either — an error body is exactly where an attacker probing a cursor codec reads its structure.
