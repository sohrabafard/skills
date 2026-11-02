---
name: alaa-indexeddb-browser-storage
description: "The browser's own storage substrate for the Ala fleet: IndexedDB semantics, origin quota and its per-engine figures, best-effort versus persistent storage, eviction and what survives it, schema versions and upgrade branching, multi-tab and service-worker concurrency around one database, index and cursor cost, which data classes may land on a device, and the browser-side cache, draft, outbox and offline-media stores. Use when writing or reviewing a client-side read or write, sizing an offline feature, holding a QuotaExceededError or a blocked upgrade, or deciding whether a value may be persisted on a shared device. Do not use for service-worker routing or the Cache API (/alaa-quasar-app-vite-v3), what a media player stores (/alaa-shaka-player), token or session handling (/alaa-trust-gateway-auth), or server-side store selection (/alaa-data-layer)."
---

# Alaa IndexedDB and Browser Storage

This skill owns the substrate: what the browser lets you keep, for how long, under what concurrency, and at what cost to read back. One property holds through every rule below: **the device is a cache and a buffer, never the record.** Every value written here has a server path that can reconstruct it, or a user-visible recovery when it cannot. No value written here decides whether a user is allowed to do something.

## Hard constraints

1. **Issue every `put`, `add` and `delete` inside a function that awaits transaction completion and routes `QuotaExceededError` through the cleanup ladder in `references/31-quota-exceeded-and-cleanup.md`.** A write that observes only request success reports done on a transaction that later aborts.
2. **Write no access token, refresh token, session secret, decoded JWT claim, permission bitmap, entitlement decision or trusted gateway header to browser storage.** Any script in the origin reads this database, so writing one there converts one XSS into account takeover. Read the positive replacement in `references/61-authority-boundary.md`.
3. **Every connection sets an `onversionchange` handler that closes the connection, and every open request handles `blocked`.** Without both, one stale tab hangs the upgrade for every other tab, with no error and no timeout.
4. **Put no `await` of non-IndexedDB work inside an open transaction.** Gather first, then open the transaction, then queue every request synchronously. WebKit ends an idle transaction sooner than Chromium, so this shows up as a Safari-only `TransactionInactiveError`.
5. **Every read that grows with a user's history states a bound and reads through an index or a bounded cursor, not a full-store scan.** `references/50-transactions-performance-and-query-patterns.md` states the budget per read shape. A scan with no bound is what makes a route fine in staging and slow on a two-year-old account.
6. **Storage is best-effort until `navigator.storage.persisted()` returns `true`, and the user can evict it even then.** Ship the recovery path in the same change as the feature that stores, never after.
7. **Every configurable value — database name and version, store and index names, quota thresholds, retention windows, batch sizes — is named in `alaa-services-contract` and read from configuration, never written as a literal at a call site.** `references/95-alaa-integration-playbook.md` lists the ones the `client` repository already fixes.

## References

Load `references/00-topic-map.md` and read the one row that matches what you are about to do.

## When not to use this skill, and what owns each thing instead

- Service-worker registration, routing, Workbox strategies, the Cache API, Background Sync and the PWA update flow: `/alaa-quasar-app-vite-v3`, `references/30-service-worker-excellence.md`. This skill owns only the IndexedDB a service worker touches and the concurrency around it.
- What a media player stores offline, how it fetches and licenses it, `shaka.offline.Storage`, `offline.trackSelectionCallback`, download progress and persistent DRM licences: `/alaa-shaka-player`. This skill owns the substrate under it: `references/72-offline-media-store.md`.
- Retry, backoff, timeout, attempt caps, deadlines and degradation as doctrine: `/alaa-reliability-sla`. This skill states only where an outbox row keeps the counter.
- The server-side outbox, its row states, consumer-side dedupe and dead-letter replay: `/alaa-async-messaging`, `references/20-publishing-and-the-outbox.md`. The browser outbox is deliberately a different state set. `references/71-browser-outbox.md` states why.
- Every registered event, metric, log-field, database, store, index and configuration **name**, and every platform **value**: `/alaa-services-contract`.
- Requirement levels and observability gates on the events this skill emits: `/alaa-observability-soc`.
- Security-review triggers, threat classes and fail-closed doctrine: `/alaa-security-review`.
- Test design and the proof levels a change owes: `/alaa-testing-strategy`.
- The permission-bitmap contract and its canonical TypeScript decoder: `/alaa-permission-generator`. The trust property of any client-held value: `/alaa-trust-gateway-auth`.
- Complexity-budget doctrine and structure choice: `/alaa-algorithms-data-structures`. Paginating an unbounded collection over the network: `/alaa-keyset-pagination`.
- Server-side store selection, query shape and indexes: `/alaa-data-layer`.
- Digit and text normalization of anything a user typed, before it is stored or compared: `/alaa-input-normalization`. Domain identifier codecs: `/alaa-crockford-base32-codecs`.
- Vue and TypeScript code shape, naming and file size: `/alaa-vue-typescript-clean-code`. Vue and Quasar feature implementation: `/alaa-frontend-developer`.
- The quality bar: `/alaa-project-constitution`. Model and effort: `/alaa-prompting-guide`, `references/50-effort-and-thinking.md`.

## Gate scripts

```sh
python3 scripts/validate_skill_pack.py --root .
python3 scripts/check_references.py --root .
python3 scripts/capability_contract_conformance.py --root .
```

The Vitest examples require the consumer's installed `vitest` and `fake-indexeddb`. Do not install dependencies implicitly.

- Exit **0**: no findings.
- Exit **1**: findings, each with file and line. Resolve every one before you report completion.
- Exit **2**: could not run (a required file is missing or unreadable), never a pass. Run the checks by hand and report each.

## What you report

Report each item below, or state why it does not apply:

- the data class and its source of truth
- the capability tier the path assumes, and what it does one tier down
- the stores and indexes touched, and the stated bound on every read
- the budget the feature draws against, and the cleanup that frees it
- the migration branch, and what a second open tab sees
- the recovery the user gets when the browser evicts the whole origin
