# Sources and maintenance

Every browser claim in this pack was read on **2026-07-28**. A claim with no source and no read date is a
defect; report it. Three statuses are used and they are distinct: **verified** (someone read that source on
that date), **unverified as of 2026-07-28** (retained for the caution it carries, never asserted, never
dropped), and **not documented (searched 2026-07-28)** (searched and not found, which is not proof of
absence).

## Sources, all read 2026-07-28

| Area | Source |
|---|---|
| IndexedDB semantics | MDN IndexedDB API and Using IndexedDB; W3C Indexed Database API 3.0 — https://www.w3.org/TR/IndexedDB/ |
| quota, persistence, eviction | MDN *Storage quotas and eviction criteria* — https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria ; MDN `StorageManager.estimate` and `StorageManager.persist` ; WebKit *Updates to Storage Policy*, published 2023-08-10 for Safari 17 / iOS 17 / macOS Sonoma — https://webkit.org/blog/14403/updates-to-storage-policy/ ; web.dev *Storage for the web*, page updated 2024-09-23 — https://web.dev/articles/storage-for-the-web |
| buckets and coordination | Chrome for Developers *Storage Buckets* — https://developer.chrome.com/docs/web-platform/storage-buckets ; caniuse `wf-storage-buckets`, `mdn-api_lockmanager`, `broadcastchannel` ; MDN Web Locks API |
| API availability | Chrome for Developers *IndexedDB durability defaults to relaxed* — https://developer.chrome.com/blog/indexeddb-durability-mode-now-defaults-to-relaxed ; MDN `IDBObjectStore.getAllRecords`, `IDBFactory.databases` ; caniuse `mdn-api_idbfactory_databases`, `mdn-api_idbtransaction_durability`, `mdn-api_idbtransaction_commit`, `mdn-api_storagemanager_getdirectory`, `background-sync` |
| Shaka v5.2.3 | `shaka.offline.Storage` never calls `navigator.storage.persist()`, and no resume or repair API exists for an interrupted `store()`. Researched by the `/alaa-shaka-player` (`$alaa-shaka-player`) lane, read 2026-07-28. Consumed in `72-offline-media-store.md`. |

## Claim register

**Verified 2026-07-28**, from MDN's quota page and WebKit 14403 unless noted: Firefox best-effort is the
smaller of 10% of profile disk or the 10 GiB site group limit, persistent up to 50% capped at 8 TiB and
exempt from the group limit; Chromium 60% of disk per origin in both modes, with a browser-wide ceiling of
80% (web.dev); WebKit from macOS 14 / iOS 17 around 60% per origin for browser apps, around 15% embedded,
with a Home Screen app getting the browser figure, and browser-wide 80% / non-browser 20%; a WebKit
cross-origin frame gets **roughly one tenth of its parent's origin quota** — this replaces the previous
unquantified "a fraction"; earlier Safari an initial 1 GiB then a permission prompt. Eviction is
all-or-nothing per origin; the order is **LRU across origins, skipping persistent ones** — this fills a
gap where the pack previously stated no cross-origin order; an origin under its own quota is still evicted
to keep the browser under its own ceiling. WebKit deletes script-created data after **seven days of browser
use with no user interaction** when tracking prevention is on, with server-set cookies exempt — this skill
owns that figure and a sibling stating it should point here. Persistent storage is not silently evicted and
the user can still delete it. Firefox prompts for persistence; Safari and Chromium decide silently from
interaction history; WebKit's heuristic includes whether the site is a Home Screen Web App.
`estimate()` values are imprecise by compression, deduplication and deliberate obfuscation, is Baseline
since 2023-09 and works in workers; `persist()` is Baseline since 2021-12, requires a secure context, and
is **not available in Web Workers**. Chrome 121 made the default `readwrite` durability relaxed.
Quota estimates are padded to reduce fingerprinting.

**Support figures verified 2026-07-28** from caniuse: `indexedDB.databases()` Chrome 72+, Edge 79+, Safari
14+, Firefox 126+ (93.61%); `IDBTransaction.durability` Chrome 83+, Firefox 126+, Safari 15+ (93.54%);
`IDBTransaction.commit()` Chrome 76+, Firefox 74+, Safari 15+ (94.18%); `BroadcastChannel` Chrome 54+,
Firefox 38+, Safari 15.4+ (94.82%); Web Locks Chrome 69+, Firefox 96+, Safari 15.4+ (94.21%), available in
workers and service workers — baseline enough that the lease-record fallback is now conditional rather than
default; OPFS `getDirectory()` Chrome 86+, Firefox 111+, Safari 15.2+ (93.51%); Background Sync Chrome 49+,
Edge 79+ and **absent in every Firefox and every Safari/iOS** (77.48%); Storage Buckets Chromium 122+ and
**absent in every Firefox and every Safari** (70.28%) — a capability the pack previously did not mention at
all. MDN: `getAllRecords()` is **not Baseline**, limited availability; `getAllKeys()` widely available;
IndexedDB is available in Web Workers and service workers.

**Unverified as of 2026-07-28**, retained and not asserted:

| Claim | Why it is unverified |
|---|---|
| private-mode quota is reduced | MDN says quotas "may" differ and gives no figure per engine |
| `persist()` exempts an origin from the seven-day tracking-prevention sweep, as distinct from the pressure sweep | no source states either way; design as though it does not |
| the precise Chromium condition that grants `persist()` | not published by Google; third-party testing reports bookmarking, installing and granting notifications each failing to produce a grant |
| Firefox reached relaxed default durability at version 40 | no source supports the version; Chrome's post says only that Firefox and Safari were already relaxed. The number is withdrawn. |
| WebKit is stricter about transaction inactivity than Chromium | no version boundary and no bug reference found; prove it in the `inactivity-return-check` lane rather than citing it |
| recent Safari moved some storage inspection to Develop → Inspect Apps and Devices | look there before concluding data is absent |
| iOS/iPadOS alternate browser engines under EU rules | a regulatory claim that has moved; detect engine behaviour, do not brand-detect |

**Not documented (searched 2026-07-28):** an `expires` option on `navigator.storageBuckets.open()`; treat
it as absent.

**House policy, not vendor fact**, and labelled as such wherever stated: `softStop`, `hardStop`, every
default cap in the budget table, `outboxBatchSize`, `outboxMaxAttempts`, `outboxSendTimeoutMs`,
`outboxReaperStaleAfterMs`, `cleanupBatchSize`, `writeChunkSize`, `draftDebounceMs`, `leaseTtlMs`. Their
**names** are `/alaa-services-contract` (`$alaa-services-contract`); their retry semantics are
`/alaa-reliability-sla` (`$alaa-reliability-sla`).

## Reproducing the retired `full-guide.md`

`references/full-guide.md` was a mechanical concatenation of the topic files at 99.75% whitespace-normalized
identity, unreachable from every router, 38.1% of the pack's bytes, and it carried a duplicate of a stale
citation that then had to be fixed in two places. Retired 2026-07-28. It is reproducible on demand and does
not need to be stored:

```sh
cat references/[0-9]*.md > /tmp/full-guide.md
```

That is how it was generated. Do not commit the output.

## Refresh triggers

Six months since the read date; a WebKit, iOS or Safari storage-policy publication; a Chromium or Gecko
change to durability, quota or buckets; **Storage Buckets shipping in a second engine**, which turns
`25-storage-buckets-api.md` from "never a requirement" into a real portability question; a regression in
Web Locks or `BroadcastChannel` support; a production incident exposing an engine-specific storage failure;
or the `client` repository adding a store or changing storage ownership.

## Refresh procedure

1. Re-read every source above and record the new date.
2. Update the register row by row. An unverifiable row becomes `unverified as of <date>` — never deleted,
   never asserted.
3. Update `assets/browser-test-matrix.yaml` and `assets/capability-tier-contract.json` together; they share
   a joining dimension and the harness enforces it.
4. Run all three scripts with `--self-test`, per `SKILL.md`.
5. Exercise the pack on five real prompts: design an outbox; fix a migration whose index is empty; audit
   quota handling; answer a token-storage proposal; plan offline media for iOS.
