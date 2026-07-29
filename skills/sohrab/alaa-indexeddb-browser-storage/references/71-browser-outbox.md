# The browser-side outbox

A mutation the user made that must survive a reload, a tab close, or an offline period.

## This is not the server-side outbox, and the difference is structural

`/alaa-async-messaging` (`$alaa-async-messaging`), `references/20-publishing-and-the-outbox.md`, owns the
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

## The record

```ts
export type BrowserOutboxStatus = 'queued' | 'sending' | 'sent' | 'conflict' | 'abandoned';

export interface BrowserOutboxItem<TBody = unknown> {
  id: string;                    // domain identifier; /alaa-crockford-base32-codecs
  accountKey: string;
  endpointKey: string;           // a registered key, never a raw URL
  body: TBody;
  idempotencyKey: string;        // generated at enqueue; shared contract with the server
  status: BrowserOutboxStatus;
  priority: 'critical' | 'normal' | 'low';
  attempts: number;
  nextAttemptAt: string;         // second segment of the scheduling index
  sendingSince?: string;         // set on claim, read by the reaper
  createdAt: string;
  updatedAt: string;
  lastError?: string;
  expiresAt?: string;
}
```

The scheduling index is `['status', 'nextAttemptAt']`, and both segments are declared fields on this type.
Confirm that before creating it — an index over an absent field is silently empty and the queue never
drains (`40-schema-and-migrations.md`).

**The sort invariant, stated because the code depends on it.** The claim cursors `['queued', …]` and writes
`'sending'` into the indexed `status` field while iterating. `'sending'` sorts before `'queued'`, so an
updated record moves behind the cursor and is not visited twice. **Renaming either token without
re-checking that ordering produces an infinite claim loop.** The test in
`examples/vitest-idb-pattern.test.ts` asserts it.

## The flush

1. **Acquire the Web Lock** `alaa:outbox-flush` with `ifAvailable: true`. Without it, several tabs and the
   service worker flush the same rows — `41-multitab-versionchange-and-locks.md`.
2. **Run the reaper first**, before claiming anything.
3. **Claim a batch** in one short `readwrite` transaction: cursor the scheduling index over
   `['queued', ''] … ['queued', nowIso]`, set `status: 'sending'` and `sendingSince`, stop at
   `outboxBatchSize`. Commit.
4. **Send outside the transaction**, each request carrying its `idempotencyKey` and an `AbortSignal` bound
   to a timeout. A send with no timeout never settles and never reports.
5. **Classify each result** and write the outcome in a short transaction.
6. **Release the lock** and emit the metrics.

## Classification

| Result | Status written | Attempts | Note |
|---|---|---|---|
| 2xx | `sent` | unchanged | record the acknowledgement, then delete or compact |
| network error, timeout, 5xx, 429 | `queued` | `+1` | reschedule per the retry policy |
| 409 or a documented conflict body | `conflict` | unchanged | surface to the user; never retried automatically |
| 401 | `queued`, **attempts unchanged** | unchanged | **pause the whole flush.** The session expired and refresh must run first. Counting a 401 as an attempt burns a valid mutation's budget on an authentication problem. |
| 403 | `abandoned` | unchanged | the server has stated this actor may not do this; retrying cannot change it |
| other 4xx | `abandoned` | unchanged | a malformed request stays malformed |

Classifying 401 and 403 identically is the defect this table exists to prevent: one is transient and one is
permanent, and treating either as the other loses data or loops.

## Retry, and who owns it

**Backoff shape, jitter, cap, attempt limit and request timeout are doctrine, and doctrine is
`/alaa-reliability-sla` (`$alaa-reliability-sla`).** This skill states only that the row carries `attempts`
and `nextAttemptAt` so the policy can be applied, and that every value is read from configuration and named
in `/alaa-services-contract` (`$alaa-services-contract`): `outboxBatchSize` (default **25**),
`outboxSendTimeoutMs`, `outboxMaxAttempts`, `outboxBackoffBaseMs`, `outboxBackoffCapMs`,
`outboxReaperStaleAfterMs`. **No literal for any of these appears at a call site** —
`examples/outbox-pattern.ts` takes a policy object and embeds none of them.

A row reaching `outboxMaxAttempts` becomes `abandoned` **and is reported**, never silently dropped.

## The reaper — the failure class the server outbox does not have

**Symptom.** A row sits in `sending` and nothing moves; the queue depth does not fall; no error is logged,
because the context that would have logged it no longer exists.

**Diagnosis.** `sendingSince` is older than `outboxReaperStaleAfterMs` (default **120,000**, which must
exceed `outboxSendTimeoutMs` by a clear margin or the reaper races a live send).

**Action.** Return the row to `queued`, increment `attempts`, reschedule, and set `lastError: 'reaped'`.
This is safe precisely because the request carried an `idempotencyKey`: if the original send did reach the
server, the duplicate is deduped there.

**When.** At the start of every flush before any claim, and on application boot. Never on a timer alone — a
closed device has no timer, and boot is when the orphans are guaranteed visible.
`examples/outbox-reaper.ts` is the implementation.

**Never resolve a stuck row by deleting it.** A deleted row is a user mutation that no longer exists and
nothing will detect its absence.

## Bounds, triggers, reporting

The queue is bounded by item count and bytes from the feature's budget file
(`30-quota-model-and-budgets.md`). **Drop items with `priority: 'low'` once the queue exceeds the
`hardStop` value in that file, and only for the classes it marks droppable. If it marks none, do not drop.**
`critical` and `normal` are never dropped to make room; stop accepting new ones and tell the user instead.

Flush triggers: boot; `online`; visibility change to visible; a successful session refresh; entering the
owning route; a manual retry control. Background Sync is a bonus where it exists — Chromium only, absent in
every Firefox and Safari/iOS, read 2026-07-28 — owned by `/alaa-quasar-app-vite-v3`
(`$alaa-quasar-app-vite-v3`); never the only trigger.

Report queue depth and oldest-row age bucketed, rows reaped per pass, per-status counts, and the
classification of every non-2xx. `outbox_reaped` is what separates "slow network" from "contexts are dying
mid-send"; without it the loss is invisible. Names are `/alaa-services-contract`
(`$alaa-services-contract`); requirement level is `/alaa-observability-soc` (`$alaa-observability-soc`).

Never enqueue a secret, token, decoded claim, trusted header or authorization decision in a body —
`61-authority-boundary.md`.
