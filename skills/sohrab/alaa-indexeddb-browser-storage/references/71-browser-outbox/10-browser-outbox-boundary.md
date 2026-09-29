# This is not the server-side outbox, and the difference is structural

## This is not the server-side outbox, and the difference is structural

`/alaa-async-messaging`, `references/20-publishing-and-the-outbox.md`, owns the
server-side outbox. Its states are **`pending`, `claimed`, `published` — three and no more** — and it claims
with `DELETE … FOR UPDATE SKIP LOCKED … RETURNING`, committing the delete only after the publish is
acknowledged, so a relay that dies mid-publish rolls back and the row is claimable again. It has **no
timeout, no attempt counter, no backoff and no quarantine**.

The browser cannot do any of that. It has no supervisor process, no transaction that spans the network
call, and no database-level skip-lock. It claims by mutating a status field in place, which creates a
failure class the server outbox is structurally incapable of having: **a row left claimed by a context that
ceased to exist** — a closed tab, a terminated service worker, a sleeping device.

| Concept | Server-side | Browser-side | Shared? |
|---|---|---|---|
| not yet claimed | `pending` | `queued` | concept shared, token deliberately not |
| a worker holds it | `claimed`, released by rollback | `sending`, released **only by the reaper** | **not shared** — the release mechanism differs |
| the server accepted it | `published` | `sent` | concept shared |
| needs a human decision | not modelled | `conflict` | **browser-only** |
| given up on | not modelled; no attempt cap exists | `abandoned` | **browser-only** |

**Shared vocabulary:** `idempotencyKey` and at-least-once delivery mean the same thing on both sides,
because the server's dedupe is what makes a browser retry safe. **Browser-only:** `sending`, the reaper,
`conflict`, `abandoned`, and the attempt counter.

Say this in review: the browser outbox is **more elaborate than the server outbox it feeds**. That is not
an inconsistency to fix by adding knobs server-side; it follows from the browser having no supervisor, an
untrusted client-side network, and a user who can be told something went wrong. Reusing
`pending/inflight/done/failed/dead` would invite an agent who knows the server side to assume the claim is
self-releasing and skip the reaper — the rows would sit claimed, the queue would look like it was draining,
and the mutations would be silently lost.
