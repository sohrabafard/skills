# Testing and proof levels

Test design and the proof-level ladder are `/alaa-testing-strategy`. This file
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

When planning or reviewing storage-change coverage, read [Required scenarios](./80-testing-and-proof-levels/10-required-scenarios.md) for the complete storage-change scenario matrix and minimum proof levels.

## Reproducing a quota condition locally

When reproducing or validating a quota failure, read [Quota reproduction](./80-testing-and-proof-levels/20-quota-reproduction.md) for unit, Playwright, and real-device reproduction steps.

## Debug surfaces per engine

When diagnosing storage behavior in a browser, read [Debug surfaces](./80-testing-and-proof-levels/30-debug-surfaces.md) for engine-specific inspection tools and their limits.

## Performance budgets to assert

When setting or measuring storage latency, read [Performance budgets](./80-testing-and-proof-levels/40-performance-budgets.md) for measured latency and batch limits.

## Release checklist

Before releasing a storage change, read [Release checklist](./80-testing-and-proof-levels/50-release-checklist.md) for the required storage-change review and release checks.

## Real IndexedDB regression harness

Before release, when running the real IndexedDB regression suite, read the [Real IndexedDB harness](./80-testing-and-proof-levels/60-real-indexeddb-harness.md) for isolated browser regression setup, execution, and retained evidence.
