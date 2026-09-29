# Schema versioning and migrations

Before implementing or reviewing any schema or migration change, read [Version and schema foundations](./40-schema-and-migrations/10-version-and-schema-foundations.md) for idempotency and its ADR exception, upgrade-transaction limits, destructive-migration boundaries, and the required oldVersion branches. This applies before any strategy or example below.

## Non-negotiable rules

When implementing or reviewing any schema or migration change, read [Version and schema foundations](./40-schema-and-migrations/10-version-and-schema-foundations.md) for version, transaction, name ownership, and metadata requirements.

## Names, and who owns them

When choosing database, store, or index names, read [Version and schema foundations](./40-schema-and-migrations/10-version-and-schema-foundations.md) for shared ownership and account partition boundaries.

## The `meta` store

When reading or updating metadata, read [Version and schema foundations](./40-schema-and-migrations/10-version-and-schema-foundations.md) for canonical keys and version writes.

## The upgrade shape

When implementing an upgrade, read [Upgrade and migration strategies](./40-schema-and-migrations/20-upgrade-and-migration-strategies.md) for request order and index validation.

## Migration strategies

When choosing a migration style, read [Upgrade and migration strategies](./40-schema-and-migrations/20-upgrade-and-migration-strategies.md) for additive, lazy, and shadow-copy options.

## Migration journal

When persisting migration progress, read [Journal and other contexts](./40-schema-and-migrations/30-journal-and-other-contexts.md) for resumable state and fields.

## What an upgrade owes other contexts

Before upgrading with other tabs or a service worker open, read [Journal and other contexts](./40-schema-and-migrations/30-journal-and-other-contexts.md) for connection coordination.

## Upgrade tests

When planning or completing migration-test design or review, read [Version and schema foundations](./40-schema-and-migrations/10-version-and-schema-foundations.md) for the universal migration rules and [Upgrade tests and example](./40-schema-and-migrations/40-upgrade-tests-and-example.md) for all eight upgrade lanes.

## Example v4 account-metadata index

When reviewing the sample index or rollback limits, read [Upgrade tests and example](./40-schema-and-migrations/40-upgrade-tests-and-example.md) for its schema and proof requirements.
