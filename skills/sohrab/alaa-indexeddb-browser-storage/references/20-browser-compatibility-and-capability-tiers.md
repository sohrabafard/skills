# Browser compatibility and capability tiers

Branch on the object returned by `detectBrowserStorageCapabilities()`
(`examples/browser-capabilities.ts`), never on `navigator.userAgent`.

**A user-agent check is permitted only when a test in this repository reproduces the engine bug it works
around, the code comment links that test by path, and the change that fixes or retires the bug deletes the
check.** Product analytics may read the user agent; storage behaviour must not branch on it.

## API support, read 2026-07-28

From caniuse.com or MDN on 2026-07-28. Re-read before repeating any of them
(`05-source-priority-and-freshness.md`).

| Capability | Support | Rule |
|---|---|---|
| `indexedDB` global | universal | check existence, then run a real open-and-write probe; presence of the global is not evidence the store works |
| `getAll` / `getAllKeys` | widely available | only with a bound or count; cursor fallback in `examples/idb-core.ts` |
| `getAllRecords` | **not Baseline**, limited availability (MDN) | never require it; ship the `getAll`+`getAllKeys` or cursor fallback in the same change |
| `IDBTransaction.durability` | Chrome 83+, Firefox 126+, Safari 15+ (93.54%) | feature-detect the options object; fall back to the engine default |
| `IDBTransaction.commit()` | Chrome 76+, Firefox 74+, Safari 15+ (94.18%) | optional; auto-commit is correct without it |
| `indexedDB.databases()` | Chrome 72+, Edge 79+, Safari 14+, **Firefox 126+** (93.61%) | diagnostics and cleanup only, never a control-flow dependency |
| `navigator.storage.estimate()` | Baseline since 2023-09; available in workers | both numbers are approximations — `30-quota-model-and-budgets.md` |
| `navigator.storage.persist()` / `persisted()` | Baseline since 2021-12; secure context; **not available in Web Workers** | what actually grants it is in `30-quota-model-and-budgets.md` |
| `BroadcastChannel` | Chrome 54+, Firefox 38+, Safari 15.4+ (94.82%) | baseline for this fleet; ship no `storage`-event or polling fallback |
| Web Locks (`navigator.locks`) | Chrome 69+, Firefox 96+, Safari 15.4+ (94.21%); workers and service workers | baseline; the lease-record fallback in `41-multitab-versionchange-and-locks.md` applies only to a runtime the probe reports without it |
| OPFS `getDirectory()` | Chrome 86+, Firefox 111+, Safari 15.2+ (93.51%) | large binary content; pair with a persistence request |
| Storage Buckets | Chromium 122+ only; **absent in every Firefox and every Safari** (70.28%) | `25-storage-buckets-api.md`; never a requirement |
| Background Sync | Chrome 49+, Edge 79+; **absent in every Firefox and every Safari/iOS** (77.48%) | owned by `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`); never the only flush trigger |

## Engine notes, read 2026-07-28

- **Chromium.** Default `readwrite` durability became `relaxed` in **Chrome 121**. Do not assume a
  completed transaction is on disk after a power loss.
- **Gecko.** Prompts the user when a site requests persistent storage. Firefox reached relaxed default
  durability before Chrome did; the exact version is `unverified as of 2026-07-28` and the previously
  stated "Firefox 40" is withdrawn for want of a source.
- **WebKit.** The quota model changed at macOS 14 / iOS 17 (`30-quota-model-and-budgets.md`). WebKit ends
  an idle transaction sooner than Chromium; the version boundary and a bug reference are
  `unverified as of 2026-07-28`, so prove it with the `inactivity-return-check` lane rather than citing it.
- **Embedded webviews** (WKWebView, Android WebView, Capacitor). A non-browser WebKit app gets roughly a
  quarter of the browser-app origin quota. Test the embedded runtime, not the mobile browser.
- **Private and incognito.** Storage usually works and is usually deleted at session end. MDN gives no
  figure for a reduced quota, so that claim is `unverified as of 2026-07-28`: probe, never promise
  persistence.

iOS and iPadOS third-party browsers were historically all WebKit; whether alternate engines now ship there
under EU rules is `unverified as of 2026-07-28`. Detect behaviour at runtime; do not brand-detect.

## Capability tiers

The probe returns a tier and the application persists it to the `capabilities` store. **Any code path that
writes to IndexedDB and is reachable by a user calls the probe before its first write.**

| Tier | Condition, as the probe observes it | What the product may promise |
|---|---|---|
| 0 | `indexedDB` absent, or the open-and-write probe fails | in-memory state for this tab only; server-first operations; **no offline language anywhere in the UI** |
| 1 | probe succeeds; `estimate` absent | drafts, preferences, small caches, a bounded outbox; sizes fixed by the budget file rather than by measurement |
| 2 | tier 1 plus `estimate` | measured budgets, LRU cleanup against real free space, a persistence request after real user intent, storage-usage UI |
| 3 | tier 2 plus a worker, plus OPFS or Cache API, plus `BroadcastChannel` and Web Locks | offline media, large prefetch, worker-side serialisation and local index rebuilds |

Tier 3 is reachable: `examples/browser-capabilities.ts` returns it when those probes pass, and
`scripts/capability_contract_conformance.py` fails if any tier in `assets/capability-tier-contract.json`
has no reachable code path or no lane in `assets/browser-test-matrix.yaml`.

**The capability object's field set is declared once**, in `examples/browser-capabilities.ts`. This file
does not restate it; the harness enforces that the example, the JSON contract and the test matrix agree.

What changes across tiers is how much is retained and how fast it returns — never whether the user can
finish the task. Offline media is offered at tier 3 only, with the eviction warning in
`72-offline-media-store.md`.
