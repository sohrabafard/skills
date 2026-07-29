# IndexedDB mental model and storage-API choice

## What it is

An origin-scoped, asynchronous, transactional store of structured-clone-compatible values, in object stores
addressed by primary key and by secondary indexes. Available in the window, in dedicated and shared workers,
and in service workers (`WorkerGlobalScope.indexedDB`); MDN, read 2026-07-28. Every operation is
asynchronous; no synchronous API exists.

```text
Origin: https://app.example
└── Browser-managed storage bucket
    ├── IndexedDB databases → object stores → indexes → records
    ├── Cache API entries
    ├── OPFS files
    └── other origin storage
```

**The bucket, not the database, is the unit of quota and of eviction.** That single fact drives most of this
pack: a large Cache API download shrinks what IndexedDB can hold, and an eviction takes both at once.

No joins, no query planner, no cross-origin transactions, no permission model inside one origin, and no
guarantee a value survives the user clearing site data.

## Core constructs

**Database** — a name and a positive integer version, not a semantic string. **Object store** — a keyed
collection; the key is inline via `keyPath` or supplied out of line. **Index** — a secondary lookup over
one key path or an array key path, maintained on every write. **Transaction** — `readonly`, `readwrite` or
`versionchange`, scoped to a named set of stores. **Request** — one asynchronous operation. **Cursor** —
streaming iteration over keys, values or a range. **Structured clone** — the serialisation; functions, DOM
nodes and prototype-bearing class instances do not survive it.

## Choosing the storage API

Decide by how you will retrieve the value, not by how large it feels.

| You will retrieve it by … | Store it in | Because |
|---|---|---|
| primary key or index, as a structured record | IndexedDB | the only origin store with secondary indexes and transactions |
| matching an HTTP `Request` to a `Response` | Cache API | request/response pairs; routing is `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`) |
| byte range, or streaming a large file | OPFS `navigator.storage.getDirectory()` | random access and sync access handles in workers; Chrome 86+, Firefox 111+, Safari 15.2+, caniuse read 2026-07-28 |
| a fixed key, one tab, tiny, dies with the tab | `sessionStorage` | synchronous and tab-scoped |
| a fixed key, tiny, and a synchronous main-thread read is affordable | `localStorage` | it blocks the main thread; keep it under a few kilobytes |

**Do not write a value larger than 1 MB to IndexedDB unless that value has a line in the feature's
`storage-budget-policy.md`.** Large values amplify clone cost, quota consumption and engine quirks;
`assets/storage-budget-policy-template.md` is the file that line goes in.

Media downloaded for offline playback is its own case: `72-offline-media-store.md`.

## What must never be stored here

Any script in the origin reads this database. Tokens, session secrets, decoded JWT claims, permission
bitmaps, entitlement decisions and trusted gateway headers therefore have no correct form here.
`61-authority-boundary.md` states the replacement for each and names its owner.

## Before you create an object store

Answer all six in `assets/indexeddb-decision-record-template.md`.

1. Can this value be reconstructed from a server response? If not, name the user-visible recovery.
2. What does the user see the moment the browser deletes the whole origin?
3. Which class in `assets/data-classification-policy.yaml` does it fall in?
4. What bounds its size — a record count, a byte cap, or a retention window?
5. Which index answers the read you are adding it for, and what is that read's stated bound?
6. Does anything branch on this value to decide what a user may do? If yes, stop: that is an authorization
   decision and it belongs to `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`).

## Progressive enhancement, stated as behaviour

The same core task completes on every supported browser. What changes across tiers is how much is retained
and how fast it returns, never whether the user can finish.
`20-browser-compatibility-and-capability-tiers.md` gives the tiers and the probe that selects one.
