---
name: alaa-indexeddb-browser-storage
description: "Use this skill when designing, implementing, reviewing, testing, or debugging IndexedDB/browser-storage features for Alaa or similar web apps: offline state, local cache, outbox sync, schema migrations, quota handling, browser compatibility, storage security, and progressive enhancement."
---

# Alaa IndexedDB Browser Storage

## Purpose

Use this skill to make agents reliable at IndexedDB and browser-storage work across Chrome/Edge, Firefox, Safari/WebKit, iOS/iPadOS, Android, desktop, private modes, embedded webviews, and older browser versions.

This skill is intentionally abstract and player-agnostic. It teaches rules for IndexedDB itself: storage modeling, quotas, persistence, migrations, transactions, performance, privacy/security, compatibility, testing, and graceful degradation.

## Ownership

`alaa-indexeddb-browser-storage` owns:

- IndexedDB architecture and implementation guardrails.
- Browser storage quota, eviction, and persistence behavior.
- Cross-browser capability detection and progressive enhancement.
- Client-side schema versioning, migrations, concurrency, multi-tab handling, and fallbacks.
- Local cache, offline state, draft persistence, and outbox/sync patterns.
- Security, privacy, data classification, and token-storage boundaries for browser storage.
- Testing and observability for browser-storage features.
- Alaa-specific frontend storage decisions that still treat backend services as source of truth.

It does not own exact Vue, Quasar, service-worker, API-gateway, or backend implementation details. Pair with the relevant companion skill when those become primary.

## When to use

Use this skill when the task includes any of the following:

- IndexedDB, `indexedDB`, `IDBDatabase`, `IDBTransaction`, object stores, indexes, cursors, `getAll`, `getAllKeys`, `getAllRecords`, `IDBKeyRange`, `idb`, Dexie, local-first storage, or browser database logic.
- Offline-first or resilient frontend state: learning progress, drafts, quiz answers, local catalog, pending uploads, analytics outbox, notification read state, or cache metadata.
- Browser storage quotas, `navigator.storage.estimate()`, `navigator.storage.persist()`, `QuotaExceededError`, eviction, private browsing, or storage pressure.
- Multi-tab or versioned database upgrades: `onupgradeneeded`, `blocked`, `versionchange`, upgrade deadlocks, schema migration, or data backfill.
- Browser/version differences across Chromium, Firefox, Safari/WebKit, iOS/iPadOS, Android, webviews, old versions, or incognito/private modes.
- Security/privacy decisions around local storage, token storage, PII, local encryption, logout purge, shared devices, and third-party scripts.
- Testing IndexedDB with fake-indexeddb, Playwright, real Safari/iOS, browser DevTools, crash/reload scenarios, or storage instrumentation.

## When NOT to use

Do not use this skill when:

- The task is backend-only with no client-side persistence.
- The task is only a media-player API contract and not about browser storage itself.
- The task is pure Service Worker/Cache API routing with no IndexedDB metadata or coordination.
- The task is exact Quasar/Vue syntax lookup with no storage design risk.
- The task asks for server-side database architecture only.

## Quick start workflow

1. Read the repo-local `AGENTS.md` and project instructions first.
2. For any browser-version, quota, Safari/WebKit, or “latest/current” claim, refresh official sources before acting.
3. Load `references/00-topic-map.md` and then only the smallest relevant reference files.
4. Start every design with this classification:
   - source of truth: server or client?
   - data sensitivity: public/cache/user-private/PII/secret?
   - lifetime: ephemeral/session/durable/offline-critical?
   - recovery path: recompute, refetch, resync, or user loss?
5. Prefer progressive enhancement: same core UX on all supported browsers; better UX on stronger devices and newer browsers.
6. Use feature detection and capability probes. Do not rely on user-agent sniffing except for documented product analytics or known WebKit/iOS mitigations.
7. Treat IndexedDB as a client-side cache/outbox/offline layer, not an authorization or identity authority.
8. Validate changes with unit tests, browser tests, and at least one real browser path for each risky compatibility class.

## Routing map

- Source priority, freshness, and compatibility research rules:
  - `references/05-source-priority-and-freshness.md`
- IndexedDB mental model, boundaries, and storage choice framework:
  - `references/10-indexeddb-mental-model-and-boundaries.md`
- Browser compatibility, versions, capability tiers, and progressive enhancement:
  - `references/20-browser-compatibility-and-capability-tiers.md`
- Quota, persistence, eviction, storage pressure, private mode, and budgets:
  - `references/30-storage-quota-persistence-and-eviction.md`
- Schema versions, migrations, multi-tab upgrades, concurrency, and blocked connections:
  - `references/40-schema-versioning-migrations-and-concurrency.md`
- Transactions, performance, query design, batching, durability, indexes, and workers:
  - `references/50-transactions-performance-and-query-patterns.md`
- Security, privacy, data classification, auth-token rules, logout purge, and local encryption boundaries:
  - `references/60-security-privacy-and-data-classification.md`
- Offline sync, outbox, cache, drafts, learning state, and conflict handling:
  - `references/70-offline-sync-outbox-cache-patterns.md`
- Testing, browser-debugging, observability, and release readiness:
  - `references/80-testing-debugging-and-observability.md`
- Agent workflows, prompt patterns, output contracts, and GPT/Claude-compatible skill usage:
  - `references/90-agent-workflows-prompts-and-output-contracts.md`
- Alaa-specific integration playbook:
  - `references/95-alaa-integration-playbook.md`
- Source map and maintenance policy:
  - `references/99-sources-and-maintenance.md`

## Mandatory rules

- Never store access tokens, refresh tokens, session secrets, entitlement authority, payment secrets, or irreversible private keys in IndexedDB.
- Never make security or entitlement decisions solely from IndexedDB. Revalidate through trusted server/gateway paths.
- Always handle `QuotaExceededError` and storage unavailability.
- Always assume data can be evicted unless persistent storage was granted, and even then assume the user can delete it.
- Always design a server resync, recompute, or user-visible recovery path.
- Always close old DB connections on `versionchange`; handle `blocked` on upgrades.
- Keep transactions short. Do not await unrelated async work inside an active transaction.
- Keep migrations idempotent and test fresh install plus upgrade from every supported historical schema.
- Separate large file/media storage decisions from IndexedDB metadata decisions; prefer IndexedDB for structured records and metadata, and choose Cache API or OPFS when those are the right abstraction.
- Use explicit storage budgets per feature and per data class before implementing large offline features.
- For browser-specific claims after the research date in `references/99-sources-and-maintenance.md`, refresh official sources.

## Companion skill pairing

| Main risk | Pair with |
|---|---|
| Vue/Quasar implementation, SSR, hydration, boot files | `$alaa-frontend-developer` |
| Service Worker, Cache API, PWA update flow | `$alaa-frontend-developer` and exact PWA/Quasar skill if available |
| Gateway/auth/session/trusted headers | `$alaa-trust-gateway-auth` |
| API contracts, envelopes, pagination, cache validators | `$alaa-services-contract` |
| Watch/analytics event design | Alaa observability/analytics skill if available |
| Upload lifecycle/resumable upload metadata | Alaa upload/tusd/service-contract skill if available |
| Browser automation validation | `$playwright` or `$playwright-interactive` |
| Current OpenAI/Claude skill-format claims | official OpenAI/Anthropic documentation skill/source |

## Search terms inside this skill

Use exact searches such as:

- `QuotaExceededError`, `navigator.storage.estimate`, `navigator.storage.persist`, `best-effort`, `persistent storage`, `eviction`, `storage pressure`, `Safari proactive eviction`
- `onupgradeneeded`, `blocked`, `versionchange`, `IDBOpenDBRequest`, `IDBTransaction`, `durability`, `readwrite`, `strict`, `relaxed`
- `getAllRecords`, `getAllKeys`, `getAll`, `cursor`, `IDBKeyRange`, `compound key`, `multiEntry`, `structured clone`
- `private browsing`, `incognito`, `webview`, `iOS WebKit`, `cross-origin frame`, `partitioned storage`
- `outbox`, `idempotency key`, `conflict resolution`, `last sync cursor`, `offline draft`
- `data classification`, `logout purge`, `token storage`, `XSS`, `CSP`, `local encryption`

## Output default

When answering an IndexedDB task, produce:

1. Decision summary.
2. Data classification and source-of-truth statement.
3. Capability tier and fallback behavior.
4. Schema/object-store/index plan.
5. Quota and eviction plan.
6. Security/privacy plan.
7. Migration and multi-tab plan.
8. Test matrix.
9. Code changes or pseudocode only when implementation is requested.
