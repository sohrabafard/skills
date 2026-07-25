# Postgres design policy (Production, Multi-Tenant)

## A) Core principle — write-model is the source of truth
- Design core OLTP tables in 3NF (or BCNF when it is easy and doesn’t harm clarity).
- Avoid duplicate “editable” truth:
    - If a value can be edited, keep exactly one authoritative column for it in the write-model.
- Denormalization is forbidden in core truth tables unless:
    - you can point to measured query patterns proving it is necessary, AND
    - the exception is documented as a deliberate design trade-off.

## B) Enforce integrity in the DB (not only in code)
Use DB constraints to encode invariants:
- `NOT NULL`, `FK`, `UNIQUE`, `CHECK`
- Prefer explicit referential actions and document intent:
    - `ON DELETE RESTRICT` / `CASCADE` / `SET NULL`
    - `ON UPDATE RESTRICT` / `CASCADE`

Rule of thumb: default to `RESTRICT` unless the business/domain model clearly requires cascades.

## C) Multi-tenant boundary (must be enforced)
Baseline rules:
- Every tenant-scoped table MUST include `tenant_id` (NOT NULL). Any row without `tenant_id` is a bug.
- Any uniqueness rule MUST be tenant-aware:
    - use `UNIQUE (tenant_id, ...)` unless global uniqueness is explicitly required.
- Frequent query indexes MUST lead with `tenant_id` to prevent cross-tenant scans.
- Every query MUST be tenant-scoped by default (`WHERE tenant_id = ?`).
    - Cross-tenant access requires an explicit, audited “system/admin” path (not an accidental code path).

Tenancy strategy:
- Use ONE clear strategy and document it:
    - default: shared schema + `tenant_id` (recommended)
    - if using RLS: define policies and require `SET LOCAL` tenant context per request/transaction

## D) Read performance without corrupting truth
- Build read-models explicitly:
    - `VIEW` / `MATERIALIZED VIEW` / summary tables (CQRS-light)
- Separate truth tables vs projections:
    - truth tables are normalized and authoritative
    - projections are derived, rebuildable, and may be eventually consistent

Derived fields (counts, last_state, aggregates):
- Must have a defined update strategy:
    - async/outbox consumer updates (preferred for scale)
    - controlled triggers (only if proven safe; document overhead and locking)
- Updates must be idempotent (at-least-once safe).

## E) Audit & operations
- Prefer append-only/audit tables for history.
- Do not overwrite business-critical facts without an audit trail.
- Indexing must match real query patterns; migrations must be lock-safe and rollback-aware.

## F) Identifier naming policy (mandatory)
- For PostgreSQL-first repositories, new persistence identifiers MUST default to lower_snake_case:
    - tables, columns, indexes, constraints, sequences, join tables, foreign-key names, and check-constraint names
- Do not introduce new mixed-case identifiers that require double quotes in PostgreSQL.
- Do not treat ORM convenience as a reason to mirror camelCase API or PHP names into schema identifiers.
- If a repository already has quoted mixed-case identifiers, treat them as explicit legacy debt:
    - prefer a planned cleanup or rebuild path over extending the mixed-case surface
    - document any temporary compatibility layer and the exact removal path
- When using Doctrine DBAL, Laravel schema tooling, or raw SQL together, choose one canonical unquoted identifier spelling and keep it stable across migrations, models, tests, and docs.

# Postgres performance principles (performance-first)
- Prefer simple, predictable queries and stable indexes.
- Avoid OFFSET pagination on large tables; use keyset pagination.
- Avoid N+1; fetch in batches and/or eager-load deliberately. When the loop's iteration count grows with tenants, rows, or history, `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) owns which of the four resolutions applies and the maximum the batch itself must carry; this file owns the query and index shape the resolution lands on.
- Indexes speed reads but slow writes; keep the minimum effective set.
- Prefer constraints (PK/FK/UNIQUE/CHECK) to encode invariants; they are also an optimization tool.
