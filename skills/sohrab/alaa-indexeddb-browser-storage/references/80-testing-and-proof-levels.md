# Testing and proof levels

Test design and the proof-level ladder are `/alaa-testing-strategy` (`$alaa-testing-strategy`). This file
places browser-storage artifacts on that ladder and states what each level can and cannot prove.

| Level | Artifact | Proves | Cannot prove |
|---|---|---|---|
| 2 — unit | `examples/vitest-idb-pattern.test.ts` with `fake-indexeddb` in the test setup | schema branches run; indexes are queried with the intended ranges; the reaper transitions rows; the purge deletes by range; quota classification branches when the error is injected | anything about a real engine — timing, transaction inactivity, real quota, real eviction |
| 3 — parity | `scripts/capability_contract_conformance.py` | `examples/browser-capabilities.ts`, `assets/capability-tier-contract.json` and `assets/browser-test-matrix.yaml` agree; every tier is reachable; every declared feature has a lane; every index key path names declared fields | that any of them matches a real browser |
| 4 — local smoke | `examples/playwright-quota-smoke.spec.ts` | a real engine opens, upgrades, writes, and raises a real `QuotaExceededError` | Safari or iOS behaviour, unless the lane runs WebKit |
| 5 — in-runtime | the device lanes in `assets/browser-test-matrix.yaml` | WebKit transaction timing, real device quota, private mode, background and foreground, the offline-critical flow | anything beyond the device it ran on |

**`fake-indexeddb` does not reproduce WebKit** — not transaction-inactivity timing, not quota, not private
mode, not eviction. A green unit suite bounds the logic and nothing else; a storage change shipping on unit
tests alone has proved the branch, not the behaviour.

## What every storage change must exercise

| Scenario | Level |
|---|---|
| fresh install at the current version | 2 |
| upgrade from the previous version, and from the oldest supported version | 2 |
| a second connection blocks the upgrade and the blocked path is taken | 2 branch, 4 real event |
| the old connection receives `versionchange` and closes | 4 |
| the database is unavailable and the fallback store is used | 2 |
| `QuotaExceededError` on an optional cache write, and cleanup frees room | 2 classify, 4 real error |
| `QuotaExceededError` on a draft save, and the user is told | 2 and 4 |
| storage cleared between sessions, and boot recovery runs | 2 state machine, 5 real eviction |
| an offline write flushes when the network returns | 2 and 4 |
| a 401 pauses without burning attempts; a 403 abandons | 2 |
| a row orphaned in `sending` is reaped on the next boot | 2 |
| logout purge removes every record for the previous account, verified by a ranged count | 2, and 4 for atomicity under an interrupted run |
| an older-schema record and a malformed record are rejected on read | 2 |
| private or ephemeral storage degrades to tier 0 | 4 private lane, 5 real device |
| a route's read stays inside its stated bound at a realistic record count | 4 with a seeded store |

## Reproducing a quota condition locally

The failure this skill cares most about needs a recipe, or nobody exercises it.

- **Unit, any engine.** Inject a store double whose `put` fires an abort carrying
  `new DOMException('…', 'QuotaExceededError')`. Exercises the classification and the ladder without cost;
  this is the version that runs on every commit.
- **Playwright, Chromium.** Write increasingly large records into a throwaway store until the transaction
  aborts, then assert the error name and that the cleanup ladder ran. Slow — it belongs in the smoke lane.
- **Real device.** Fill the disk until the browser is under pressure. Manual, in the iOS and low-end
  Android lanes.

The unit form proves the branch; the Playwright form proves the engine raises what the branch expects.
Neither substitutes for the other.

## Debug surfaces per engine

**Chrome and Edge** — DevTools → Application → IndexedDB; Application → Storage for usage and "Clear site
data"; `navigator.storage.estimate()` from the console. **Firefox** — DevTools → Storage Inspector; the
persistent-storage prompt appears here and nowhere else, so Firefox is the lane that exercises the prompt
path. **Safari and WebKit** — Web Inspector → Storage; whether recent Safari moved some surfaces to
Develop → Inspect Apps and Devices is `unverified as of 2026-07-28`, so look there before concluding data
is absent.

## Performance budgets to assert

Measured on the lowest-capability lane in `assets/browser-test-matrix.yaml`; a feature may state its own.

```text
database open on application boot: < 100 ms p75, < 500 ms p95
route-level cached read:           < 50 ms p75
migration without progress UI:     < 2 s, or ship progress and a retry
outbox flush batch:                outboxBatchSize, default 25
```

The complexity bound behind each is in `50-transactions-performance-and-query-patterns.md`. A measured
number that meets its budget on a small store and states no bound will stop meeting it as the store grows.

## Release checklist

- [ ] Decision record names the data class and source of truth for every store touched.
- [ ] Every index key path verified against the record type it indexes.
- [ ] Every read's bound stated; no `O(n)` read on a user-facing route.
- [ ] Capability detection implemented and the tier persisted.
- [ ] Quota error path exercised at level 2 and level 4.
- [ ] Cleanup implemented for every refetchable class, with a cap in the budget file.
- [ ] Logout purge indexed, atomic or journalled, verified by a ranged count.
- [ ] Multi-tab upgrade and the service-worker connection both exercised.
- [ ] A WebKit lane completed if the product supports Safari or iOS.
- [ ] Private-mode checked; no offline promise at tier 0 or 1.
- [ ] Older-schema and malformed records rejected on read.
- [ ] Telemetry per failure class, registered and bucketed, with no payload.
- [ ] User-facing copy matches the wording table in `70-cache-and-drafts.md`.
