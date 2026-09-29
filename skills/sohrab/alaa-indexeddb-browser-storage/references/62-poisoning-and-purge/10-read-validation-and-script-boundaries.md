# Read validation and script boundaries

## Validation on read

Every read validates before use, including reads inside cleanup jobs.

```ts
function parseLearningState(value: unknown): LearningStateRecord | null {
  if (!isObject(value)) return null;
  if (value.schema !== LEARNING_STATE_SCHEMA) return null;   // wrong or absent version
  if (typeof value.id !== 'string') return null;
  if (typeof value.accountKey !== 'string') return null;
  // ... every field the caller will read
  return value as LearningStateRecord;
}
```

- **A `schema` field on every record, checked on every read.** An older-schema record is migrated
  (`../40-schema-and-migrations.md`) or discarded. Never used as-is.
- **A record whose `accountKey` differs from the current session is not read.** It is deleted.
- **A validation failure deletes the record and continues.** A poisoned record that survives to be read
  again is a permanent failure; a deleted one is transient.
- **Never interpolate a cached value into HTML.** A cached string reaching `v-html` or `innerHTML` is
  stored XSS with a persistence layer the product built itself.
- **Verify the server revision before using a cached value for anything the user acts on.** A stale price,
  entitlement or deadline is worse than a spinner.

## Third-party scripts

Every script in the origin reads and writes this database. Keep third-party scripts off routes that read
`user_generated_unsynced` or `pii_moderate_high` data. Ship a Content Security Policy, and Trusted Types
where the framework allows — the policy itself is `/alaa-security-review` ground.
Audit tag managers: a tag manager is arbitrary script execution granted to whoever holds its console.
Isolate untrusted content in a sandboxed or cross-origin iframe, which gets its own storage partition.
