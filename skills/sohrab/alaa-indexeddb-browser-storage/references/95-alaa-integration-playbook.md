# Alaa integration playbook

## Architectural alignment

Alaa-style client storage must respect platform service ownership:

- Client applications call public routes through the gateway.
- Gateway/auth paths remain the trust boundary for identity and protected access.
- `auth` owns identity/profile/session truth.
- `content` owns course/set/content learning-content truth.
- legacy playback/domain responsibilities may still exist during migration.
- `wa` owns watch/analytics ingestion.
- `tusd` owns resumable upload transfer lifecycle, while target services own domain attachment.
- Comments, tickets, notifications, and other domains own their own state.

IndexedDB should improve frontend resilience and UX, not replace these service boundaries.

## Recommended Alaa client DB

```text
DB: alaa-client-storage
Version: integer
Namespace: accountKey = projectId:userId or anonymous-session
```

Suggested stores:

| Store | Owner concept | Use |
|---|---|---|
| `meta` | client storage | schema/capability metadata |
| `storage_items` | client storage | quota cleanup metadata |
| `api_cache_entries` | gateway-backed APIs | TTL/ETag/revision cache metadata |
| `learning_state` | content/learning UX | local resume, last viewed, local progress snapshot |
| `wa_outbox` | wa | watch/analytics events waiting for ingestion |
| `drafts` | comment/ticket/quiz/etc | unsynced user drafts |
| `upload_resume_state` | tusd + target service | upload session metadata and cleanup |
| `notification_state` | notification/realtime | local read/unread display cache |
| `sync_cursors` | client sync | per-service cursors/checkpoints |
| `capabilities` | client storage | runtime feature probe result |

## Use cases

### Learning state

Store:

- courseId, setId, contentId, lessonId
- local position/progress snapshot
- last opened timestamp
- server revision when available
- sync status

Rules:

- The backend remains source of truth for official progress.
- Local state can make resume instant.
- Conflicts follow server progress rules.
- Purge on logout/account switch.

### Watch analytics outbox

Store events when offline or network fails:

```ts
type WatchAnalyticsOutboxItem = {
  id: string;
  accountKey: string;
  eventType: string;
  contentId: string;
  occurredAt: string;
  body: unknown;
  idempotencyKey: string;
  status: 'pending' | 'inflight' | 'done' | 'failed' | 'dead';
  attempts: number;
  nextAttemptAt: string;
};
```

Rules:

- Use idempotency keys.
- Bound queue by count/age/bytes.
- Drop only according to analytics retention policy.
- Never block learning UI on low-priority event flush.
- Do not store unnecessary PII in event payload.

### API/cache metadata

For course/content metadata:

- Cache only server-shaped DTOs or normalized records.
- Use TTL and server validators.
- Do not cache access authority as truth.
- Invalidate when project/account/content revision changes.

### Drafts

For comments, tickets, quiz answers, support messages:

- Save local drafts with explicit accountKey and target entity.
- Never silently delete unsynced drafts.
- On submit success, delete only after server acknowledgment.
- On account switch/logout, apply user-visible policy.

### Upload resume metadata

For resumable uploads:

- Store upload URL/session ID, target service, local file fingerprint, offset, expiresAt.
- Target service must authorize/claim attachment server-side.
- Cleanup expired/completed sessions.
- Do not store full sensitive attachments in IndexedDB unless reviewed.

### Notifications/realtime

For local notification state:

- Cache read/unread and last delivered cursor for UX.
- Server remains source of truth.
- Reconcile on app boot and reconnect.
- Use IndexedDB to avoid losing local read interactions under flaky network.

## Alaa security rules

- Do not store auth tokens in IndexedDB.
- Do not trust client-cached entitlement for protected access.
- All protected API calls go through the gateway/session model.
- Any local record read from IndexedDB must be treated as untrusted input.
- User-scoped data must include accountKey and be purged on logout/account switch.

## Recommended package boundary

Create a frontend package/module such as:

```text
src/storage/
  index.ts
  db.ts
  capabilities.ts
  quota.ts
  schemas.ts
  migrations.ts
  stores/
    learning-state.ts
    wa-outbox.ts
    drafts.ts
    api-cache.ts
    upload-resume-state.ts
  sync/
    outbox-runner.ts
    leases.ts
  testing/
    fixtures.ts
```

Expose only domain-safe methods:

```ts
storage.learningState.save(snapshot)
storage.learningState.getLast(accountKey)
storage.waOutbox.enqueue(event)
storage.waOutbox.flush({ signal })
storage.drafts.save(draft)
storage.drafts.listByTarget(accountKey, target)
storage.quota.getStatus()
storage.clearUserData(accountKey)
```

Avoid exposing raw `IDBDatabase` to feature code unless the storage module itself is being developed.

## Implementation sequence

1. Add storage capability probe.
2. Add storage facade and schema v1.
3. Add data classification and accountKey enforcement.
4. Implement one low-risk store first, e.g., learning state or drafts.
5. Add quota metadata and cleanup.
6. Add outbox pattern for analytics/events.
7. Add multi-tab upgrade UX.
8. Add real browser tests, including Safari/iOS if target users require it.
9. Add privacy-safe telemetry.
10. Expand to more features only after reliability evidence.

## Alaa-specific ADR trigger

Create an ADR when:

- feature stores more than 50 MB per user/device
- feature stores user-generated unsynced data
- feature relies on offline mode
- feature stores moderate/high PII
- feature needs Safari/iOS parity
- feature needs background sync
- schema migration is destructive
- local data affects billing/access/entitlement UI

Use `assets/alaa-indexeddb-adr.md`.
