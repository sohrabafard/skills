# Storage write failures, by failure class

Organised by what you observe, not as a procedure. Find the symptom, take the smallest retry, escalate only
if it fails. Retry counts, backoff shapes, deadlines and attempt caps are **doctrine, and doctrine is
`/alaa-reliability-sla` (`$alaa-reliability-sla`)**; this file states what to retry, what to free first,
and what the user is told.

## Every write is wrapped

```ts
try {
  const tx = db.transaction(storeName, 'readwrite');
  tx.objectStore(storeName).put(record);
  await txDone(tx);
} catch (error) {
  await handleStorageWriteFailure(error, { dataClass, storeName, operation: 'put' });
}
```

`txDone` is in `examples/idb-core.ts`. A write not wrapped this way fails review, because a write observing
only request success reports done on a transaction that later aborts.

## Class 1 — `QuotaExceededError`

**Symptom.** The transaction aborts with a `DOMException` named `QuotaExceededError`. On some engines it
surfaces on the request, on others only on the transaction — which is why the wrapper awaits the
transaction.

**Diagnosis.** At tier 2 and above, read `estimate()` and compare `usage` against the feature's `softStop`
and `hardStop`. At tier 1 there is no estimate: treat any `QuotaExceededError` as a hard stop.

**Smallest retry.** Free space in this order, then retry the write **once**:

1. Expired refetchable cache entries. 2. Prefetched records the user has not opened. 3. LRU API-cache
entries by `lastAccessedAt`, oldest first, until the feature is under its cap. 4. Completed outbox rows
already acknowledged. 5. Low-priority telemetry past its retention window — **only the classes the budget
file marks droppable; if it marks none, do not drop.**

**Never free a user-generated unsynced draft to make room for anything.**

**Escalation.** If the single retry also fails: drop one capability tier for the session, stop every
optional write, and branch on the data class. Refetchable cache or prefetch — fail silently, log, serve
from the network. **User-generated unsynced work — tell the user before they rely on it**: "This device is
out of space, so your draft is not saved here. Submit it now or free space." Silence here is the loss this
file exists to prevent. An offline media download — `72-offline-media-store.md`.

## Class 2 — eviction under storage pressure

**Symptom.** The database opens with `oldVersion === 0` on a device where the application previously ran,
or a store that had records is empty.

**Diagnosis.** The browser evicted the whole origin. Eviction is all-or-nothing across the bucket, so check
whether Cache API entries also vanished; both gone is eviction rather than a schema fault.

**Smallest retry.** None; the data is gone. Recreate the schema and resync —
`32-eviction-and-recovery.md`.

**Escalation.** If the same origin is evicted twice within one measured retention window the feature is
over budget for the device class: **reduce its cap**, do not raise the persistence request.

## Class 3 — a blocked `versionchange`

**Symptom.** `open()` fires `blocked` and never resolves. No error, no timeout, no rejection.

**Diagnosis.** Another connection — in another tab, or in the service worker — holds the old version and
did not close on `versionchange`.

**Smallest retry.** Broadcast the upgrade on the shared channel and wait for the other contexts to close.
Full sequence, including the service-worker case, in `41-multitab-versionchange-and-locks.md`.

**Escalation.** Show the reload prompt. **Never resolve a blocked open by deleting the database.**

## Class 4 — the transaction aborts mid-flight

**Symptom.** `tx.onabort` fires; `tx.error` names the cause.

| `tx.error.name` | Cause | Response |
|---|---|---|
| `QuotaExceededError` | class 1 | the ladder above |
| `ConstraintError` | a unique index rejected a duplicate key | an application bug: the key derivation is wrong, or two writers raced. Do not retry; fix the key. |
| `AbortError` | the application called `tx.abort()`, or the connection closed | intentional; verify the caller meant it |
| `TransactionInactiveError` | a request was queued after the transaction went idle | an `await` sits inside the transaction (`50-transactions-performance-and-query-patterns.md`). Retry only after the code is fixed. |
| `UnknownError` | engine-level failure, often disk | treat as class 1 escalation: one retry, then degrade |

Only `QuotaExceededError` and `UnknownError` are retryable, once. The other three are defects and retrying
them loops.

**Escalation.** A `readwrite` transaction that aborts partway wrote nothing — that is the guarantee. Do not
attempt partial repair; re-run the whole unit of work.

## Class 5 — private browsing, or a truncated store

**Symptom.** The open-and-write probe succeeds, then records written in a previous session are absent; or
`indexedDB` exists and `open()` rejects immediately.

**Diagnosis.** Private mode; a policy or extension blocking storage; or the WebKit seven-day truncation
(`32-eviction-and-recovery.md`).

**Smallest retry.** Fall back to the in-memory store **behind the same interface**
(`examples/fallback-memory-store.ts`). The shared interface is the point: the caller does not branch.

**Escalation.** Drop to tier 0 for the session, remove every offline promise from the UI, never show a
"download for offline" affordance. A subtle notice only where the user is about to rely on persistence.

## Class 6 — an offline asset is gone mid-session

Owned by `72-offline-media-store.md`, because the response involves the player. The storage-side rule:
**detect by verifying the asset is still listed before playback begins, never by waiting for a playback
error.**

## Logging

Each class emits one event with a bucketed size and no record payload, no PII, no URL query strings. Event
**names** are `/alaa-services-contract` (`$alaa-services-contract`) and are registered before the code
merges; the **requirement level** and any release gate are `/alaa-observability-soc`
(`$alaa-observability-soc`). This skill states only that **each class above must be distinguishable in
telemetry from the others**, because a quota failure and an eviction demand different product responses and
an undifferentiated "storage error" counter cannot tell them apart.
