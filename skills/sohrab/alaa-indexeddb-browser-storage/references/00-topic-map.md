# Topic map — the router for this skill

One router exists and it is this file. `SKILL.md` carries a single pointer to it and no table.

Match the row whose left column describes what you are about to do. Load that one file. Load a second
only when the first names it by path.

## Reference rows

| You are about to … | Read |
|---|---|
| repeat a browser-version, quota or "current behaviour" claim to a caller, or you are unsure whether a figure in this pack has expired | `05-source-priority-and-freshness.md` |
| choose between IndexedDB, Cache API, OPFS, `sessionStorage` and `localStorage` for a value you are about to store | `10-indexeddb-mental-model-and-boundaries.md` |
| branch code on a browser, or write a feature that must still work when `navigator.storage` is absent | `20-browser-compatibility-and-capability-tiers.md` |
| give one data class a different eviction priority than another, or you read the words "storage bucket" in a design and need the API behind them | `25-storage-buckets-api.md` |
| size an offline feature, set a cap in bytes or records, or answer "how much can we store here" | `30-quota-model-and-budgets.md` |
| write a `put`, `add` or `delete` that can run while the device is low on disk, or you are holding a `QuotaExceededError` | `31-quota-exceeded-and-cleanup.md` |
| open the database on app boot and find it missing, empty, or older than you wrote it; or an offline asset the user downloaded is gone mid-session | `32-eviction-and-recovery.md` |
| add, rename or drop an object store or index, or raise the database version integer | `40-schema-and-migrations.md` |
| write from a service worker, run a download while tabs are open, see `blocked` on an open request, or need one tab to do a job the others do not | `41-multitab-versionchange-and-locks.md` |
| write a read that scans, a loop that writes, or a cursor over a collection that grows with the user's history | `50-transactions-performance-and-query-patterns.md` |
| decide whether a specific field may be written to browser storage at all, or the device is shared | `60-data-classification.md` |
| store a token, a JWT claim, a permission bitmap, an entitlement or a gateway header, or you are about to read one back and act on it | `61-authority-boundary.md` |
| read a record back and use it, purge on logout or account switch, or reason about a compromised script in the origin | `62-poisoning-and-purge.md` |
| cache an API response locally, or hold a user's unsent work on the device | `70-cache-and-drafts.md` |
| queue a mutation that must survive a reload or an offline period, or an outbox row is stuck | `71-browser-outbox.md` |
| store downloaded media for offline playback, or reason about a partial or evicted download | `72-offline-media-store.md` |
| decide what proof a storage change owes before it merges, or write a test for a storage path | `80-testing-and-proof-levels.md` |
| hold a live symptom — missing data, an inactive transaction, a hung upgrade, a slow route | `81-debugging-runbook.md` |
| hand a storage task to another agent, or shape the answer you are about to return | `90-agent-workflows-prompts-and-output-contracts.md` |
| name a store, an index or a database in the `client` repository, or place a storage module in it | `95-alaa-integration-playbook.md` |
| update a figure in this pack, or record where one came from | `99-sources-and-maintenance.md` |

## Code examples — inventory, not a router

| Example | Purpose |
|---|---|
| `examples/idb-core.ts` | open, upgrade, transaction-completion and bounded-read helpers |
| `examples/browser-capabilities.ts` | runtime capability probe and tier selection |
| `examples/fallback-memory-store.ts` | the Tier 0 substitute, behind the shared `KeyValueStore` interface |
| `examples/migration-pattern.ts` | versioned upgrade branches and the migration journal |
| `examples/quota-manager.ts` | estimate, persistence request, and the configured budget thresholds |
| `examples/alaa-client-storage.ts` | app-level facade, indexed account purge, quota-aware write |
| `examples/outbox-pattern.ts` | claim, send, classify, and the configured retry surface |
| `examples/outbox-reaper.ts` | recovery of rows orphaned in `inflight` by a reload |
| `examples/offline-asset-guard.ts` | detecting a partial or evicted offline media asset |
| `examples/vitest-idb-pattern.test.ts` | unit lane: upgrade, blocked, quota, purge |
| `examples/playwright-quota-smoke.spec.ts` | browser lane: a real induced `QuotaExceededError` |

## Templates and assets — inventory, not a router

| Asset | Purpose |
|---|---|
| `assets/indexeddb-decision-record-template.md` | ADR for a storage feature |
| `assets/indexeddb-feature-plan-template.md` | implementation plan skeleton |
| `assets/storage-budget-policy-template.md` | the per-feature budget file that `examples/quota-manager.ts` reads |
| `assets/browser-test-matrix.yaml` | test lanes, each carrying the tiers and features it covers |
| `assets/data-classification-policy.yaml` | the data-class taxonomy, with the owning skill per row |
| `assets/capability-tier-contract.json` | the capability contract the conformance harness enforces |
| `assets/alaa-indexeddb-adr.md` | ADR starter bound to the `client` repository |
