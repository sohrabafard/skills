## Upgrade tests

Eight, every version. Lanes are in `assets/browser-test-matrix.yaml`; proof levels are
`/alaa-testing-strategy`.

1. Fresh install opens at the current version. 2. Upgrade from the previous version. 3. Upgrade from the
oldest supported version, running every branch. 4. A second tab open fires `blocked` and the UX appears.
5. The old tab receives `versionchange` and closes. 6. A migration that throws leaves the previous
version's data readable. 7. A reload during a chunked copy resumes from the journal. 8. An upgrade under a
quota-limited profile fails without corrupting the previous version.


## Example v4 account-metadata index

`examples/migration-pattern.ts` adds `storage_items.byAccount` over `['accountKey']` only in
`oldVersion < 4`. Existing stores, records and indexes remain. These names are demonstration-local;
register the consumer schema/version/index names before integration merges, following
`95-alaa-integration-playbook.md`. This example is not a platform registry entry.

After v4 commits, an old opener explicitly requesting v3 receives `VersionError`. Roll back only to
v4-compatible application code, or roll forward; never delete the database to reopen at v3. Abort or
quota failure during upgrade must leave v3 readable. Report upgrade duration, blocked/versionchange
outcomes and quota/abort categories through existing observability budgets; never report account keys.

Prove fresh v4, v1-to-v4 and v3-to-v4 preservation, indexing of existing metadata, blocked upgrade and
versionchange closure, old-v3 rejection and aborted-upgrade preservation. Purge proof additionally
covers every data store, orphan metadata, other accounts, data-only counts, repeat calls, missing-index
preflight and rollback after a queued deletion. `80-testing-and-proof-levels.md` names the browser
harness; source-function doubles alone do not prove IndexedDB engine atomicity.
