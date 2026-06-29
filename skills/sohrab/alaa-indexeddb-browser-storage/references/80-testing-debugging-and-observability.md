# Testing, debugging, and observability

## Test layers

### Unit tests

Use for:

- schema adapters
- record validation
- outbox state transitions
- quota error classification
- cleanup ordering
- migration functions

`fake-indexeddb`-style tests are useful but not enough. They do not reproduce Safari/WebKit quota/transaction timing/private mode behavior.

### Integration tests in real browsers

Use Playwright/WebDriver/BrowserStack/Sauce/real devices for:

- DB open/upgrade
- multi-tab `blocked`/`versionchange`
- private/incognito behavior
- quota/low-storage simulation where possible
- Safari/WebKit behavior
- mobile webviews/Capacitor if applicable

### Manual/device tests

Required for high-value offline or quota-heavy features:

- iOS Safari real device
- iPadOS if target users use tablets
- Android Chrome/Android WebView
- Firefox ESR if enterprise/school deployments matter
- low-end Android with constrained storage
- private/incognito sessions

## Core test matrix

Every IndexedDB feature should test:

- Fresh install.
- Existing DB same version.
- Upgrade from each supported old version.
- Upgrade blocked by old tab.
- Old tab receives `versionchange` and closes.
- DB unavailable/open failure.
- Quota exceeded during optional cache write.
- Quota exceeded during user draft save.
- Storage cleared between app sessions.
- Offline write then online sync.
- Unauthorized/expired session during sync.
- Logout/account switch purge.
- Stale/malicious old record validation.
- Private mode or ephemeral storage.
- Low-end performance with realistic record counts.

## Browser debug tools

Chrome/Edge:

- DevTools → Application → IndexedDB.
- DevTools → Application → Storage / Clear site data.
- `navigator.storage.estimate()` from console.

Firefox:

- DevTools → Storage Inspector.
- Test persistent permission prompt behavior.

Safari/WebKit:

- Safari Web Inspector → Storage.
- Test on real iOS/iPadOS when the feature depends on persistence or large quota.
- Validate behavior after app inactivity where relevant.

## Storage observability events

Emit privacy-safe telemetry:

```ts
type StorageTelemetryEvent =
  | { name: 'idb_open_success'; dbVersion: number; durationMs: number; capabilityTier: string }
  | { name: 'idb_open_error'; errorName: string; phase: 'open' | 'upgrade' | 'probe' }
  | { name: 'idb_upgrade_blocked'; fromVersion: number; toVersion: number }
  | { name: 'idb_upgrade_success'; fromVersion: number; toVersion: number; durationMs: number }
  | { name: 'storage_quota_estimate'; usageBucket: string; quotaBucket: string; persisted: boolean | 'unknown' }
  | { name: 'storage_quota_exceeded'; dataClass: string; operation: string }
  | { name: 'storage_cleanup_run'; deletedCount: number; bytesBucket: string; reason: string }
  | { name: 'outbox_backlog'; countBucket: string; oldestAgeBucket: string }
  | { name: 'outbox_sync_result'; successCount: number; retryCount: number; failCount: number };
```

Do not log raw record payloads, PII, tokens, URLs with sensitive query strings, or exact large storage estimates if fingerprinting/privacy risk matters.

## Performance budgets

Define per feature:

- DB open budget on app boot.
- Route-level read budget.
- Write debounce interval.
- Max transaction duration.
- Max records read per UI interaction.
- Migration duration threshold.
- Outbox sync batch size.

Example:

```text
DB open: < 100ms p75, < 500ms p95 on target devices
Route cache read: < 50ms p75 for recent learning state
Outbox flush batch: 25-100 items depending on payload size
Migration blocking: no user-blocking migration > 2s without progress/retry UX
```

## Failure-mode tests

Simulate:

- Transaction abort due to duplicate unique index.
- `QuotaExceededError` on write.
- Browser reload during outbox sync.
- Network success but local mark-done fails.
- Local mark-inflight succeeds but network never starts.
- Server accepts idempotency key twice.
- `onblocked` because another tab is open.
- DB deleted while app tab is open.

## Release checklist

Before shipping:

- [ ] Storage decision record exists.
- [ ] Data classification approved.
- [ ] Object stores/indexes documented.
- [ ] Feature detection implemented.
- [ ] Quota estimate and quota error paths tested.
- [ ] Cleanup policy implemented for refetchable data.
- [ ] Logout/account switch purge tested.
- [ ] Multi-tab upgrade behavior tested.
- [ ] Safari/iOS or WebKit test completed if supported.
- [ ] Private/incognito behavior checked.
- [ ] Unit tests cover migrations and stale records.
- [ ] Browser tests cover the user-critical flow.
- [ ] Observability events added without PII.
- [ ] User-visible copy is accurate about persistence/offline reliability.

## Debugging decision tree

```text
Problem: data missing
  -> Was storage cleared/evicted? Check meta lastSuccessfulOpenAt and server sync state.
  -> Is accountKey different? Check logout/account switch.
  -> Is schema version fresh? Check migration logs.
  -> Is private mode active? Check capability/probe.
  -> Did cleanup remove it? Check storage_items/audit event.

Problem: transaction inactive
  -> Did code await unrelated async work inside transaction?
  -> Is Safari/WebKit involved?
  -> Are IDB requests queued synchronously?

Problem: quota exceeded
  -> Estimate usage/quota.
  -> Identify data class.
  -> Cleanup refetchable cache first.
  -> Retry once.
  -> Reduce capability tier.

Problem: upgrade hangs
  -> Another tab has old connection.
  -> Ensure old tabs close on versionchange.
  -> Show blocked reload message.

Problem: slow route
  -> Avoid full-store getAll.
  -> Use index/range/cursor/count.
  -> Batch/debounce writes.
  -> Move heavy work to worker.
```
