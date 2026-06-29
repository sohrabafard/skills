# Topic map

Load the smallest reference that answers the current task. Do not load the full guide unless necessary.

## Decision/routing

| Need | Load |
|---|---|
| Authoritative source order, freshness, current browser claims | `05-source-priority-and-freshness.md` |
| Decide whether IndexedDB is the right storage API | `10-indexeddb-mental-model-and-boundaries.md` |
| Browser/version compatibility, progressive enhancement, feature probes | `20-browser-compatibility-and-capability-tiers.md` |
| Quotas, persistent storage, eviction, private mode, cleanup budgets | `30-storage-quota-persistence-and-eviction.md` |
| DB schema, object stores, migrations, multi-tab upgrade safety | `40-schema-versioning-migrations-and-concurrency.md` |
| Transactions, performance, indexes, read/write patterns, durability | `50-transactions-performance-and-query-patterns.md` |
| Security, privacy, auth-token, PII, logout purge, shared device | `60-security-privacy-and-data-classification.md` |
| Offline sync, outbox, drafts, local cache, conflict handling | `70-offline-sync-outbox-cache-patterns.md` |
| Testing, DevTools, instrumentation, release readiness | `80-testing-debugging-and-observability.md` |
| Agent workflow, prompt patterns, output templates | `90-agent-workflows-prompts-and-output-contracts.md` |
| Alaa integration and service-boundary mapping | `95-alaa-integration-playbook.md` |
| Source map and maintenance schedule | `99-sources-and-maintenance.md` |

## Code examples

| Example | Purpose |
|---|---|
| `examples/browser-capabilities.ts` | Runtime capability detection and probes |
| `examples/idb-core.ts` | Low-level Promise wrappers, open/upgrade, transaction helpers |
| `examples/migration-pattern.ts` | Versioned schema/migration pattern |
| `examples/quota-manager.ts` | Storage estimate, persistence request, budget checks |
| `examples/outbox-pattern.ts` | Idempotent offline outbox sync pattern |
| `examples/alaa-client-storage.ts` | App-level storage facade and store naming |
| `examples/fallback-memory-store.ts` | Minimal fallback when IDB is unavailable |
| `examples/vitest-idb-pattern.test.ts` | Unit-test pattern with fake IndexedDB style APIs |
| `examples/playwright-quota-smoke.spec.ts` | Browser smoke tests for storage behavior |

## Templates/assets

| Asset | Purpose |
|---|---|
| `assets/indexeddb-decision-record-template.md` | ADR template for a storage feature |
| `assets/indexeddb-feature-plan-template.md` | Implementation plan skeleton |
| `assets/storage-budget-policy-template.md` | Quota/budget cleanup policy |
| `assets/browser-test-matrix.yaml` | Cross-browser manual/automated test matrix |
| `assets/data-classification-policy.yaml` | Storage security classification template |
| `assets/capability-tier-contract.json` | Capability tier contract |
| `assets/alaa-indexeddb-adr.md` | Alaa-specific ADR starter |
