# ADR: Alaa IndexedDB feature

Date:
Owner:
Feature:
Status: proposed

## Context in Alaa architecture

- Client traffic enters through Gateway.
- Auth/profile/session truth remains server-side.
- Content/course truth remains in content/domain services.
- Watch/analytics ingestion belongs to wa.
- Upload transfer lifecycle belongs to upload service; domain attachment belongs to target service.

## Decision

## Data stored locally

| Store | Data | Source of truth | Account-scoped? | TTL | Security class |
|---|---|---|---|---|---|

## Server interaction

- APIs used:
- Idempotency keys:
- Conflict handling:
- Revalidation:

## Browser support

- Minimum core behavior:
- Enhanced behavior:
- Fallbacks:
- Safari/iOS notes:

## Quota/storage budget

## Migration/versioning

## Security/privacy

## Tests and rollout

## Observability

## Consequences
