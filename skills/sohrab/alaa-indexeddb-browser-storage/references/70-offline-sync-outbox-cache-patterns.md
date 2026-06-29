# Offline sync, outbox, cache, and drafts

## Golden rule

IndexedDB is a local reliability layer, not the product's source of truth. Server services own canonical data. Client storage improves UX under flaky networks, tab reloads, and low-latency reads.

## Pattern catalog

### 1. Read-through cache

Use for server data that can be refetched.

Record:

```ts
type ApiCacheEntry<T> = {
  key: string;
  accountKey?: string;
  urlFingerprint: string;
  value: T;
  etag?: string;
  serverRevision?: string;
  fetchedAt: string;
  expiresAt: string;
  lastAccessedAt: string;
  bytesApprox: number;
};
```

Rules:

- Use TTL and server validators (`ETag`, revision, `updatedAt`) when available.
- Do not cache sensitive payloads without data-classification approval.
- Invalidate by domain event or version when possible.
- On stale cache, show stale-while-revalidate only when UX accepts it.

### 2. Write-behind outbox

Use for events or user actions that must survive offline/retry.

Record:

```ts
type OutboxItem = {
  id: string;
  accountKey: string;
  endpointKey: string;
  method: 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  body: unknown;
  idempotencyKey: string;
  status: 'pending' | 'inflight' | 'done' | 'failed' | 'dead';
  priority: 'critical' | 'normal' | 'low';
  attempts: number;
  nextAttemptAt: string;
  createdAt: string;
  updatedAt: string;
  lastError?: string;
  expiresAt?: string;
};
```

Rules:

- Every network mutation must be idempotent or have a client mutation ID.
- Never enqueue secrets.
- Keep queue bounded by item count, bytes, and age.
- Sync outside the transaction that reads queue items.
- Mark item state in a short transaction before and after network call.
- Use backoff with jitter.
- Use server conflict response to resolve, not blind overwrite.

### 3. Local draft

Use for user-generated unsent work.

Rules:

- Drafts are user-visible and protected from silent deletion.
- Include `accountKey`, `entityType`, `entityId`, `draftType`, and `updatedAt`.
- Purge on submit success only after server acknowledgment.
- On logout, ask before discarding unsynced drafts or bind them to a guest/account policy.

### 4. Learning state snapshot

Use for local resume/progress UI.

Rules:

- Backend remains source of truth for learning progress when submitted.
- Store local snapshot for instant resume.
- Enqueue progress events to outbox if network fails.
- Resolve server/client conflicts by monotonic progress policy and server rules.

### 5. Upload resume metadata

Use for resumable upload state metadata only.

Rules:

- Store upload session ID, target domain, file fingerprint, offset, status, and expiry.
- Do not make the upload service own target domain authorization.
- Target service must still claim/attach uploaded asset server-side.
- Purge expired/completed upload metadata.

## Sync lifecycle

Trigger sync on:

- app boot
- network `online`
- visibility change to visible
- successful auth/session refresh
- route entering relevant area
- manual retry
- background sync where available and tested

Do not depend only on background sync; browser support varies.

## Outbox sync algorithm

```text
1. Acquire sync lease for account/scope.
2. Read next due items by status + nextAttemptAt.
3. Mark batch as inflight with syncRunId.
4. Commit transaction.
5. Send network requests with idempotency keys.
6. For each result:
   - success -> mark done, store server ack/revision
   - retryable error -> pending with backoff
   - conflict -> failed/conflict and create UI resolution task
   - unauthorized -> pause account sync and require auth refresh
   - forbidden -> dead/failed after server confirmation
7. Release lease.
8. Emit metrics.
```

## Conflict resolution

Define per entity:

| Entity | Recommended strategy |
|---|---|
| Analytics/watch events | Idempotent append with event IDs; server dedupe |
| Draft answer/comment | Server revision + user conflict UI if remote changed |
| Preferences | Last-write-wins acceptable if low risk |
| Upload attach | Server-authoritative state machine |
| Learning progress | Server rule, often max progress with event ordering |

## Cache invalidation

Use layered invalidation:

- TTL expiration.
- Server revision/ETag mismatch.
- User logout/account switch.
- App build/storage schema version change.
- Domain event: course changed, comment updated, ticket status changed.
- Manual “clear local data”.

## Offline UX wording

Use precise UX language:

- “Saved on this device” for local drafts.
- “Will sync when online” for outbox-backed items.
- “Available offline on this device” only after persistence and storage checks if the content is truly usable offline.
- “May be removed by browser storage settings/private mode” for best-effort storage-heavy features.

## Data loss policy

- Refetchable cache may be deleted automatically.
- Completed telemetry may be compacted/deleted after upload.
- Low-priority telemetry may be dropped after retention/backlog limits if product accepts it.
- User-generated unsynced drafts must not be silently deleted.
- If local data cannot be saved due to quota, tell the user before they rely on it.

## Background jobs

Optional jobs:

- cleanup expired cache
- flush outbox
- revalidate stale cache
- compact completed outbox
- lazy migrate old records
- recompute storage metadata

Run jobs opportunistically and cancel safely. Use leases to avoid multiple tabs doing the same expensive work.
