# Quota model and storage budgets

IndexedDB has no fixed size limit. Quota is computed for the origin's storage bucket, shared with the Cache
API and OPFS, and varies with engine, disk size, persistence mode and embedder.

## Per-engine quota, read 2026-07-28

MDN *Storage quotas and eviction criteria* and WebKit blog 14403 (published 2023-08-10, applies from
Safari 17 / iOS 17 / macOS Sonoma), both read 2026-07-28. Planning estimates, not promises.

| Engine | Best-effort | Persistent |
|---|---|---|
| Firefox | the smaller of 10% of the disk holding the profile, or the **10 GiB group limit** shared by all origins on the same site | up to **50% of disk, capped at 8 TiB**, exempt from the group limit |
| Chromium | up to **60% of total disk** per origin | the same 60%; mode does not change the origin figure |
| WebKit browser app, macOS 14 / iOS 17+ | around **60% of total disk** per origin | same; persistence changes eviction, not capacity |
| WebKit embedded, non-browser app | around **15% of total disk** per origin | same. A site saved to the Home Screen or Dock gets the browser figure, around 60%. |
| WebKit cross-origin frame | **roughly one tenth of its parent's origin quota** | same |
| Safari before macOS 14 / iOS 17 | initial **1 GiB**, then the browser asks the user to allow more | not applicable |

Browser-wide ceilings sit above the per-origin figure and are what makes an under-quota origin evictable:
Chromium uses at most **80% of total disk** across all origins (web.dev *Storage for the web*, page updated
2024-09-23, read 2026-07-28); WebKit **80%** for browser apps and **20%** for non-browser apps displaying
web content (WebKit 14403).

Private and incognito: MDN says browsers "may apply different quotas" and that data is usually deleted at
session end, with no figure. The per-engine reduction is `unverified as of 2026-07-28` — probe, do not
assume.

## What `estimate()` returns

MDN, read 2026-07-28: "The returned values are not exact: between compression, deduplication, and
obfuscation for security reasons, they will be imprecise." `quota` is a conservative approximation that
varies by origin with visit frequency, site-popularity data, and engagement signals such as bookmarking,
home-screen installation and push permission. `usageDetails` breaks `usage` down by storage system.
Available in Web Workers; Baseline since 2023-09.

Three consequences bind:

1. **Never display the raw number to a user as a capacity.** Show a band; `examples/quota-manager.ts` emits
   bands.
2. **Never gate a write on `usage < quota` alone.** The write can still throw, and the handler in
   `31-quota-exceeded-and-cleanup.md` is what makes the path correct.
3. **Never send the exact pair to telemetry.** Bucketed only; the exact pair is a fingerprinting surface.
   The requirement level on that event is `/alaa-observability-soc` (`$alaa-observability-soc`).

## Best-effort versus persistent

Default storage is best-effort: it lives while the origin is under quota, the device has room, and the user
does not clear it. `navigator.storage.persist()` requests persistent mode and resolves `true` only if
granted (MDN, read 2026-07-28). Persistent storage is exempt from the LRU eviction in
`32-eviction-and-recovery.md`; the user can still delete it.

What grants it, read 2026-07-28: **Firefox** prompts the user (MDN). **Safari and Chromium** decide
automatically from interaction history with no prompt (MDN); WebKit states its heuristic includes "whether
the website is opened as a Home Screen Web App" (WebKit 14403). **The precise Chromium condition is not
published by Google** — third-party testing reports bookmarking, installing and granting notifications each
failing to produce a grant, so treat it as `unverified as of 2026-07-28`: request, check `persisted()`, and
design for `false`.

Call `persist()` only after the user has done something implying they want the data kept — enabled offline
mode, started a download, created durable local work. A call on first paint is denied on the engines that
judge by engagement and wastes the one signal you have.

**`persist()` is not available in Web Workers** (MDN, read 2026-07-28). Request it from the window; the
worker reads the result from the `capabilities` store.

## Budgets

Every feature storing more than a single small record ships a budget file from
`assets/storage-budget-policy-template.md`: one row per data class, with a cap and the cleanup that frees
it. The caps are **house policy, not vendor figures** — they exist so one feature cannot consume the
origin's quota and evict another.

| Data class | Default cap | Cleanup at the cap |
|---|---:|---|
| config and feature-flag cache | 2 MB | replace on TTL expiry |
| learning state | 20 MB | keep the most recently updated N per account |
| drafts | 50 MB | never silently deleted; surface to the user |
| analytics outbox | 2,000 items or 20 MB, whichever binds first | drop `priority: 'low'` only, per `71-browser-outbox.md` |
| API response cache | 100 MB | LRU by `lastAccessedAt`, then TTL |
| offline media metadata | 5 MB | follows the asset; `72-offline-media-store.md` |

Percentage thresholds, evaluated against `estimate()` at tier 2 and above:

```text
softStop = min(200 MB, 5% of estimated quota)   # stop optional prefetch and cache writes
hardStop = min(500 MB, 10% of estimated quota)  # stop every write except user-generated unsynced work
```

Both are house policy. `examples/quota-manager.ts` reads them from configuration and embeds neither. Their
names are `/alaa-services-contract` (`$alaa-services-contract`).

## User-facing storage controls

A feature storing more than its soft cap ships all four: a banded "storage used" figure, a "clear offline
data" action, a per-feature delete, and one sentence stating that the browser, private mode or clearing
site data can remove local data. The wording table is in `70-cache-and-drafts.md`.
