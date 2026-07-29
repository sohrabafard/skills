# Eviction, truncation, and boot-time recovery

The application must survive complete loss of origin storage, at any moment, with no warning.

## How eviction works, MDN read 2026-07-28

- **All-or-nothing per origin.** "When an origin's data is evicted by the browser, all of its data, not
  parts of it, is deleted at the same time." IndexedDB and Cache API go together; partial eviction is
  explicitly avoided because it would create inconsistency.
- **LRU across origins.** Under storage pressure the browser deletes the least recently used origin's data,
  then the next, until pressure resolves.
- **Persistent origins are skipped.** The sweep "skips over origins that have been granted data persistence
  by using `navigator.storage.persist()`".
- **An origin under its own quota is still evictable**, because the browser enforces a whole-browser ceiling
  — Chrome at most 80% of total disk — and evicts best-effort origins to stay under it.

WebKit states the same LRU shape and adds that origins with active pages, and origins in persistent mode,
are excluded (WebKit 14403, read 2026-07-28).

## WebKit truncation after seven days without interaction

MDN, read 2026-07-28, verbatim: "Safari proactively evicts data when cross-site tracking prevention is
turned on. If an origin has no user interaction, such as click or tap, in the last seven days of browser
use, its data created from script will be deleted. Cookies set by server are exempt from this eviction."

Five consequences. **This skill owns the figure**; a sibling stating it should point here rather than repeat.

1. The clock counts **seven days of browser use**, not calendar days. A user who does not open the browser
   does not advance it.
2. The trigger is **absence of user interaction with the origin**, not absence of network activity. A
   background sync does not reset it.
3. **Only script-created storage is deleted.** Server-set cookies survive, which is why a user can appear
   signed in on a device whose IndexedDB is empty. Boot-time recovery must handle exactly that state.
4. Whether `persist()` exempts an origin from this sweep, as distinct from the pressure sweep, is
   `unverified as of 2026-07-28`. Design as though it does not.
5. **Never promise indefinite offline availability on any WebKit browser.**

## Boot-time recovery

Run this before the first user-scoped view renders. It is a state machine on what the open reports.

| The open reports | State | Action |
|---|---|---|
| `oldVersion === 0`, no prior session recorded | first run | create the schema, write `meta.lastSuccessfulOpenAt`, proceed |
| `oldVersion === 0`, a prior session **is** recorded outside IndexedDB | **evicted or truncated** | create the schema; mark local-only features unavailable until resync; resync incrementally; emit the eviction event; if the user had unsynced work, **tell them it is gone** |
| `oldVersion > 0` and below the code's version | upgrade | `40-schema-and-migrations.md` |
| `oldVersion > 0` and above the code's version | a newer build ran here | do not downgrade, do not delete; show the reload prompt |
| the open rejects | storage unavailable | class 5 of `31-quota-exceeded-and-cleanup.md`; drop to tier 0 |

**The prior-session marker must live outside IndexedDB**, or it is evicted along with everything it would
have detected. A server session or a cookie is reliable; `localStorage` shares the origin bucket and can go
with it.

Also check `logoutPurgePending` here, per `62-poisoning-and-purge.md`.

## What must never be assumed to have survived

- **Any entitlement, grant, permission or access decision.** Re-derive from the server every boot —
  `61-authority-boundary.md`.
- **A sync cursor.** Missing means resync from the server's earliest safe point, not "start from now" —
  starting from now silently loses the window.
- **An offline media asset.** Verify it is still listed before offering playback —
  `72-offline-media-store.md`.
- **An outbox row.** An evicted outbox lost user mutations. If the feature cannot tolerate that, the
  mutation should not have been queued locally — `71-browser-outbox.md`.

## Reducing the chance of eviction

In order of effect, and none is a guarantee. **Stay small** — the budgets in
`30-quota-model-and-budgets.md` are the lever, and the whole-browser ceiling binds sooner for large
origins. **Request persistence after real user intent** and check `persisted()` rather than trusting the
request. **Get real user interaction before storing anything important on WebKit**, because interaction is
what resets the seven-day clock. **Keep the server authoritative**, so eviction costs latency rather than
data.
