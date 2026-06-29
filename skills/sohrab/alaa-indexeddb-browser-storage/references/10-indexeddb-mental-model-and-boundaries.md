# IndexedDB mental model and boundaries

## What IndexedDB is

IndexedDB is a browser-provided, asynchronous, transactional, object-oriented database scoped to an origin. It stores
structured-clone-compatible JavaScript values, including objects and blobs, inside object stores keyed by primary keys
and optional indexes.

Think of it as:

```text
Origin: https://app.example
└── Browser-managed storage bucket
    ├── IndexedDB databases
    │   ├── object stores
    │   ├── indexes
    │   └── records
    ├── Cache API entries
    ├── OPFS files
    └── other origin storage
```

IndexedDB is not SQL. It has no joins, no server-grade query planner, no global transactions across origins, no
permission model inside one origin, and no guarantee that data survives user deletion or browser eviction.

## Core constructs

- Database: named database with integer version.
- Object store: keyed collection of records; key can be inline via keyPath or out-of-line.
- Index: secondary lookup structure over one key path or array key path.
- Transaction: readonly/readwrite/versionchange scope over one or more object stores.
- Request: asynchronous operation with success/error events.
- Cursor: streaming iteration over keys/values/ranges.
- Structured clone: serialization mechanism; not all JS values are storable.
- Origin: scheme + host + port boundary; quota generally applies to the origin/bucket, not a single DB.

## What IndexedDB is good for

Use IndexedDB for:

- Durable-ish app data that is too large or structured for `localStorage`.
- Offline state, drafts, local user progress, and pending sync outbox.
- Metadata catalogs for cached resources.
- Queryable local collections with indexes.
- App-state snapshots that can be refetched or resynced.
- Cross-worker/main-window storage coordination when designed carefully.

## What IndexedDB is not good for

Do not use IndexedDB for:

- Access tokens, refresh tokens, session secrets, payment secrets, or private keys that become dangerous if JavaScript
  can read them.
- JWT claims, `X-Access`, OpenFGA/authz decisions, or source-of-truth entitlement, authorization, billing, identity,
  project, or irreversible business truth.
- Large raw files when Cache API or OPFS is a better abstraction.
- Full-text search without an index/search layer.
- Analytics data lake replacement.
- Highly relational query workloads that need joins and server-side constraints.
- Guaranteed write-on-unload behavior.

## Storage API decision framework

| Need                                               | Preferred API                                                  | Notes                                                                                      |
|----------------------------------------------------|----------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| Structured records, indexes, offline state, outbox | IndexedDB                                                      | Primary focus of this skill                                                                |
| Static network resources and HTTP response caching | Cache API                                                      | Usually via Service Worker                                                                 |
| File-like large binary content                     | OPFS or Cache API                                              | Use IndexedDB for metadata when needed                                                     |
| Small tab-scoped values                            | sessionStorage                                                 | Synchronous; keep tiny                                                                     |
| Small cross-navigation non-sensitive strings       | localStorage only if unavoidable                               | Synchronous; blocks main thread; tiny only                                                 |
| Public client request context                      | SDK/gateway contract                                           | Alaa browser code sends only approved public headers through `@alaa/sdk` / `@alaa/sdk-vue` |
| Credentials/session authority                      | SDK-owned bearer attachment plus gateway/auth refresh contract | Not IndexedDB; do not add app-side token persistence or app-managed refresh                |

## Source-of-truth rule

Before creating an IndexedDB object store, answer:

1. Can this data be reconstructed from the server?
2. What is the user-visible harm if it disappears?
3. Is there a resync path?
4. Is the backend still authoritative?
5. Is the data safe to expose to any script running in the origin?
6. For Alaa, is this only a cache/display hint rather than auth, project, entitlement, or identity authority?

If the answer to 5 is no, do not store it in IndexedDB without a security review.
If the answer to 6 is no, do not store it in IndexedDB; use the Alaa SDK/gateway/server contract instead.

## Progressive enhancement principle

Design for consistent core behavior:

- Baseline browsers get core functionality and safe degradation.
- Modern browsers get persistent-storage requests, better quota estimates, improved bulk APIs, background sync, workers,
  or OPFS where applicable.
- Powerful devices get larger local budgets, larger prefetch windows, and better local search/indexing.
- Low-end or private-mode environments get smaller budgets, fewer retained records, and clear UX about reduced offline
  reliability.

## Agent design default

When a user asks for an IndexedDB feature, the agent should produce a decision record before code:

```text
Feature:
Data classes:
Source of truth:
Required lifetime:
Object stores:
Indexes:
Quota budget:
Eviction recovery:
Security posture:
Browser capability tiers:
Migration plan:
Test matrix:
```
