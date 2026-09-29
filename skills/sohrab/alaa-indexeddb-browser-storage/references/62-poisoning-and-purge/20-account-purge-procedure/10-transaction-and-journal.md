# Transaction and journal

The logout and account-switch purge is a security operation. A purge run as several independent
transactions leaves the previous account's records readable if the tab crashes, the browser is killed,
or the device sleeps between them.

**One transaction across every user-scoped store** — correct and simple when the counts are small:

Use `AlaaClientStorage.deleteByAccount` in `examples/alaa-client-storage.ts`. Include `storage_items`
and purge its account index independently of data rows, so orphan metadata cannot retain identifiers
or timestamps. Preflight every required store and index before deleting. Register the transaction
completion and abort handlers before queueing requests. Queue the requests synchronously, attach each
request's error handler as it is created, and then await transaction completion. Abort on synchronous
or request failure; report success only after commit.
The return count includes data rows only, never metadata. Missing schema/indexes fail the purge and
retain the pending marker; upgrade through `../../40-schema-and-migrations.md` before retrying.

**Or a journalled purge**, when the counts are large enough that one transaction would block the UI. Write
the intent first, purge, then clear it:

```ts
await putMeta('logoutPurgePending', { accountKey, startedAt: nowIso });  // own transaction, before anything
// purge each store, chunked, each in its own transaction
await deleteMeta('logoutPurgePending');                                   // only after every store reports done
```
