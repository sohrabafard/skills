---
name: alaa-indexeddb-browser-storage
description: "The browser's own storage substrate for the Ala fleet: IndexedDB semantics, origin quota and its per-engine figures, best-effort versus persistent storage, eviction and what survives it, schema versions and upgrade branching, the multi-tab and service-worker concurrency around a single database, index and cursor cost, which data classes may land on a device at all, and the browser-side cache, draft, outbox and offline-media stores. Use it when writing or reviewing a client-side read or write, sizing an offline feature, holding a QuotaExceededError or a blocked upgrade, or deciding whether a value may be persisted on a shared device. Do not use it for service-worker routing or the Cache API, which are /alaa-quasar-app-vite-v3; for what a media player stores and licenses, which is /alaa-shaka-player; for token, session or trusted-header handling, which is /alaa-trust-gateway-auth; or for server-side store selection and query shape, which are /alaa-data-layer."
---

# Alaa IndexedDB and Browser Storage

This skill owns the substrate: what the browser will let you keep, for how long, under what concurrency,
and at what cost to read back. One property holds through every rule below — **the device is a cache and a
buffer, never the record.** Every value written here has a server path that can reconstruct it, or a
user-visible recovery when it cannot, and no value written here decides whether a user is allowed to do
something.

## Hard constraints

1. **Every `put`, `add` and `delete` is issued inside a function that awaits transaction completion and
   routes `QuotaExceededError` through the cleanup ladder in `references/31-quota-exceeded-and-cleanup.md`.**
   A write that observes only request success reports done on a transaction that later aborts.
2. **No access token, refresh token, session secret, decoded JWT claim, permission bitmap, entitlement
   decision or trusted gateway header is written to browser storage.** Any script in the origin reads this
   database, so writing one there converts one XSS into account takeover. Read the positive replacement in
   `references/61-authority-boundary.md`.
3. **Every connection sets `onversionchange` to close itself, and every open request handles `blocked`.**
   Without both, one stale tab hangs the upgrade for every other tab with no error and no timeout.
4. **No `await` of non-IndexedDB work sits inside an open transaction.** Gather first, then open the
   transaction, then queue every request synchronously. WebKit ends an idle transaction sooner than
   Chromium, so this shows up as a Safari-only `TransactionInactiveError`.
5. **Every read that grows with a user's history states its bound, and reads through an index or a bounded
   cursor rather than a full-store scan.** `references/50-transactions-performance-and-query-patterns.md`
   states the budget per read shape; a scan with no bound is what makes a route fine in staging and slow on
   a two-year-old account.
6. **Storage is best-effort until `navigator.storage.persisted()` returns `true`, and evictable even then by
   the user.** Ship the recovery path in the same change as the feature that stores, never after.
7. **Every configurable value — database name and version, store and index names, quota thresholds,
   retention windows, batch sizes — is named in `alaa-services-contract` and read from configuration, never
   written as a literal at a call site.** `references/95-alaa-integration-playbook.md` lists the ones the
   `client` repository already fixes.

## References

Load `references/00-topic-map.md` and read the one row that matches what you are about to do.

## When not to use this skill, and what owns each thing instead

- Service-worker registration, routing, Workbox strategies, the Cache API, Background Sync and the PWA
  update flow: `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`), `references/30-service-worker-excellence.md`.
  This skill owns only the IndexedDB a service worker touches and the concurrency around it.
- What a media player stores offline, how it fetches and licenses it, `shaka.offline.Storage`,
  `offline.trackSelectionCallback`, download progress and persistent DRM licences: `/alaa-shaka-player`
  (`$alaa-shaka-player`). This skill owns the substrate under it —
  `references/72-offline-media-store.md`.
- Retry, backoff, timeout, attempt caps, deadlines and degradation as doctrine: `/alaa-reliability-sla`
  (`$alaa-reliability-sla`). This skill states only where an outbox row keeps the counter.
- The server-side outbox, its row states, consumer-side dedupe and dead-letter replay:
  `/alaa-async-messaging` (`$alaa-async-messaging`), `references/20-publishing-and-the-outbox.md`. The
  browser outbox is deliberately a different state set — `references/71-browser-outbox.md` states why.
- Every registered event, metric, log-field, database, store, index and configuration **name**, and every
  platform **value**: `/alaa-services-contract` (`$alaa-services-contract`).
- Requirement levels and observability gates on the events this skill emits: `/alaa-observability-soc`
  (`$alaa-observability-soc`).
- Security-review triggers, threat classes and fail-closed doctrine: `/alaa-security-review`
  (`$alaa-security-review`).
- Test design and the proof levels a change owes: `/alaa-testing-strategy` (`$alaa-testing-strategy`).
- The permission-bitmap contract and its canonical TypeScript decoder: `/alaa-permission-generator`
  (`$alaa-permission-generator`). The trust property of any client-held value:
  `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`).
- Complexity-budget doctrine and structure choice: `/alaa-algorithms-data-structures`
  (`$alaa-algorithms-data-structures`). Paginating an unbounded collection over the network:
  `/alaa-keyset-pagination` (`$alaa-keyset-pagination`).
- Server-side store selection, query shape and indexes: `/alaa-data-layer` (`$alaa-data-layer`).
- Digit and text normalization of anything a user typed, before it is stored or compared:
  `/alaa-input-normalization` (`$alaa-input-normalization`). Domain identifier codecs:
  `/alaa-crockford-base32-codecs` (`$alaa-crockford-base32-codecs`).
- Vue and TypeScript code shape, naming and file size: `/alaa-vue-typescript-clean-code`
  (`$alaa-vue-typescript-clean-code`). Vue and Quasar feature implementation:
  `/alaa-frontend-developer` (`$alaa-frontend-developer`).
- The quality bar: `/alaa-project-constitution` (`$alaa-project-constitution`). Model and effort:
  `/alaa-prompting-guide` (`$alaa-prompting-guide`), `references/50-effort-and-thinking.md`.

## Gate scripts

```sh
python3 scripts/validate_skill_pack.py --root .
python3 scripts/check_references.py --root .
python3 scripts/capability_contract_conformance.py --root .
```

Exit **0** no findings. Exit **1** findings, each with file and line: resolve every one before reporting the
change complete. Exit **2** could not run — a required file is missing or unreadable: exit 2 is never a pass,
so run the checks by hand and report each. `--self-test` runs each script's own fixtures and proves it fails
when it should.

## What you report

Report each, or that it does not apply and why: the data class and its source of truth; the capability tier
the path assumes and what it does one tier down; the stores and indexes touched and the stated bound on
every read; the budget the feature draws against and the cleanup that frees it; the migration branch and
what a second open tab sees; and the recovery the user gets when the browser evicts the whole origin.
