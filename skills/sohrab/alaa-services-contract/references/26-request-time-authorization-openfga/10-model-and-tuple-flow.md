## Why this layer exists

Authentication answers "who is this user?" The compact JWT and the gateway's
trusted headers (`X-User-Id`, `X-Project-Id`, `X-Access`) settle identity. They do
not answer "is this user allowed to open course 12, set 55, content 901?" That is a
relationship between a user and a specific object, and it changes constantly as
people buy, get granted, or get denied access. Encoding that in a token would make
tokens huge and stale. So the platform keeps it in OpenFGA and asks at request time.

The decision is fail-closed on the wire: on a deny, and on any status in the `503 AUTHZ_*` row of the
table below, the gateway answers and the backend is never called. `/alaa-security-review` owns the general
fail-closed doctrine and the review trigger; this file owns the exact statuses, codes, and headers that
implement it here. Timeouts and the no-retry rule for this hop are in
`22-failure-load-and-deprecation-contract.md`.

## The two paths (and the single seam)

OpenFGA is the seam between a write path and a read path. Understand both, because a
bug is almost always "the tuple was never written" (write path) or "the route asked
the wrong question" (read path).

- **Write path (truth -> graph):** `entitlement-api` owns business truth (who was
  granted or denied what). On every change it emits an event. `projector` consumes
  the event and writes or deletes the matching OpenFGA tuples. `projector` is the
  **only** tuple writer.
- **Read path (request -> decision):** the gateway authenticates, builds a canonical
  object id, and asks `authz-sidecar` (or `entitlement-spoa`). The sidecar resolves
  the route to a final `can_*` permission and runs one OpenFGA `check`. The sidecar
  is **read-only**.

```
entitlement-api --event--> projector --write tuples--> OpenFGA
                                                          ^
gateway --HEAD /internal/authz/check--> authz-sidecar --check--+
```

Grant vs permission, the easiest thing to misread:
- `projector` writes **grant**/**deny** relations: `grant_view`, `deny_access`, ...
- the OpenFGA **model** derives the final **`can_*`** permissions from those, applying
  inheritance (a course grant reaches its sets and contents) and deny precedence.
- the sidecar always checks a final **`can_*`** relation, never a raw grant.

So a "view" purchase on content 901 is stored as a `grant_view` tuple, and a later
`can_view` check passes because the model resolves `can_view` from `grant_view`
unless a deny overrides it.
