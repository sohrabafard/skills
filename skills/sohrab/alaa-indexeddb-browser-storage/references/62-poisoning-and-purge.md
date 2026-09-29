# Reading records back, and purging them

Two paths, one premise: **a record read out of IndexedDB is untrusted input.** It may be stale, from a
schema you no longer ship, or written by an attacker who had script execution in this origin an hour ago
and no longer does. Validation on read is what makes that earlier compromise non-persistent.

## Validation on read

Every read validates before use, including reads inside cleanup jobs. Keep third-party scripts away from
routes that handle sensitive records, and treat logout, account-switch, and account-deletion cleanup as
security operations.

When reading or cleaning stored records, follow [Read validation and script boundaries](./62-poisoning-and-purge/10-read-validation-and-script-boundaries.md) for schema checks, XSS prevention, third-party isolation, and validation failure handling.

## Third-party scripts

When reviewing a tag manager or script on a route that reads sensitive records, see [Read validation and script boundaries](./62-poisoning-and-purge/10-read-validation-and-script-boundaries.md) for isolation and storage-access limits.

## The logout and account-switch purge

Choose an atomic transaction when its work is small enough to avoid blocking the UI; otherwise use the
journalled, chunked sequence. Before implementation or review, follow [Account purge procedure](./62-poisoning-and-purge/20-account-purge-procedure.md) for transaction ordering, recovery, bounded cursors, drafts, account deletion, and reporting.

### It must be atomic, or journalled

For exact transaction and recovery requirements, read [Account purge procedure](./62-poisoning-and-purge/20-account-purge-procedure.md).

### It must be bounded

For account-index requirements and purge complexity, read [Account purge procedure](./62-poisoning-and-purge/20-account-purge-procedure.md).

### The sequence

For the ordered purge steps and verification condition, read [Account purge procedure](./62-poisoning-and-purge/20-account-purge-procedure.md).

### Unsynced drafts

For the rule protecting work the user has not submitted, read [Account purge procedure](./62-poisoning-and-purge/20-account-purge-procedure.md).

### Account deletion

For deferred cleanup after server-side deletion, read [Account purge procedure](./62-poisoning-and-purge/20-account-purge-procedure.md).

## What is reported

For purge counts, deferred-purge reporting, and logging restrictions, read [Account purge procedure](./62-poisoning-and-purge/20-account-purge-procedure.md).
