# Agent workflows, prompt patterns, and output contracts

## How to work a storage task

In order, because each step constrains the next. Skipping to the schema produces stores nobody can purge
and indexes nobody can use.

1. **Classify the data and name its source of truth** (`60-data-classification.md`). If the class is
   forbidden, stop and say so; there is no schema to design.
2. **State the capability tier assumed and what happens one tier down**
   (`20-browser-compatibility-and-capability-tiers.md`).
3. **Design the schema from the reads**; each read names its index and its stated bound
   (`50-transactions-performance-and-query-patterns.md`).
4. **State the budget and the cleanup that frees it** (`30-quota-model-and-budgets.md`).
5. **State the migration branch and what a second tab and the service worker see**
   (`40-schema-and-migrations.md`, `41-multitab-versionchange-and-locks.md`).
6. **State the recovery when the origin is evicted** (`32-eviction-and-recovery.md`).

Then implement, then prove at the levels in `80-testing-and-proof-levels.md`.

## Output contracts

**Architecture answer**

```markdown
## Decision
## Data class and source of truth
## Capability tier and one-tier-down behaviour
## Schema — database and version, object stores, indexes each with the read it serves and that read's bound, record types
## Budget, cleanup, and eviction recovery
## Authority boundary — what is stored, what is never stored, what a stored value may decide
## Migration and concurrency — branches, blocked UX, service-worker connection
## Failure classes and what the user sees for each
## Proof — the level of each test and what it does not bound
## Risks and open decisions
```

**Code review**

```markdown
## Verdict
## Confirmed defects, each with file and line
## Index key paths checked against their record types
## Reads without a stated bound
## Failure classes not handled
## Authority-boundary violations
## Concurrency — versionchange, blocked, service worker, locks
## Configuration values written as literals
## Required tests, by level
```

**Implementation plan**

```markdown
## Goal
## Assumptions
## Files to change
## Schema change and migration branch
## Capability detection
## Read and write paths, with bounds
## Budget and cleanup
## Failure handling per class
## Tests, by level
## Telemetry and rollout
```

## Prompt patterns

Both trigger forms appear in each; use the one your runtime accepts.

**Feature design**

```text
Use /alaa-indexeddb-browser-storage ($alaa-indexeddb-browser-storage).
Design the browser storage for [feature].
Constraints: supported browsers [list]; data classes [list]; offline requirement
[none | best-effort | critical]; expected records and bytes per account after one year [estimate].
Return the architecture-answer contract from references/90. State the bound on every read.
Do not write implementation code unless I ask for it.
```

**Implementation**

```text
Use /alaa-indexeddb-browser-storage ($alaa-indexeddb-browser-storage).
Implement [feature] in this repository. Read AGENTS.md and the existing storage module before editing.
Every write awaits transaction completion and classifies QuotaExceededError.
Every index key path is verified against the record type it indexes.
Every configurable value is read from configuration, not written as a literal.
Store no token, JWT claim, permission bitmap, entitlement or trusted gateway header.
Add tests for fresh install, upgrade, blocked upgrade, quota error, and logout purge.
Report files changed, the bound on each read added, and remaining risks.
```

**Browser compatibility audit**

```text
Use /alaa-indexeddb-browser-storage ($alaa-indexeddb-browser-storage).
Audit this storage code for Chromium, Gecko, WebKit, private mode and embedded webviews.
Re-read the source for every version or quota claim before repeating it; mark anything you cannot
verify as unverified with today's date rather than dropping or asserting it.
Return capability gaps, the fallback for each, the test lanes required, and the code changes.
```

**Quota and eviction audit**

```text
Use /alaa-indexeddb-browser-storage ($alaa-indexeddb-browser-storage).
Audit quota and eviction resilience for [feature]: the budget file, the cleanup order,
QuotaExceededError handling on every write, when persistence is requested, boot recovery after
eviction, and what the user is told in each case.
Return concrete patches and the tests that would have caught each gap.
```

**Storage security audit**

```text
Use /alaa-indexeddb-browser-storage ($alaa-indexeddb-browser-storage).
Review browser storage for stored secrets, JWT claims, permission bitmaps, trusted gateway headers,
entitlement used as authority, PII, unvalidated reads, shared-device exposure, and the logout purge.
Route anything needing a security decision rather than a fact to /alaa-security-review
($alaa-security-review) instead of deciding it here.
Return must-fix defects with file and line, the acceptable data classes, and the revised policy.
```

## Asking versus assuming

Ask only when the answer changes the architecture or the safety posture: whether the data is secret or PII;
whether offline is critical or a convenience; whether WebKit and iOS are supported; expected volume per
account after a year; whether the server offers idempotency and conflict responses. Otherwise proceed and
mark each assumption. An assumption stated is checkable; a question asked is a turn spent.

## Agent anti-patterns

Writing schema before classifying the data. Assuming quota is unlimited or `estimate()` exact. Promising
offline durability without checking `persisted()`. Shipping a feature exercised only in Chrome. Storing a
token because "IndexedDB is not localStorage". Persisting or decoding a permission bitmap in storage code.
Ignoring `blocked` and `versionchange`. A `fetch` inside a transaction. A cursor scan where an index would
answer. Reporting a check that was not run.
