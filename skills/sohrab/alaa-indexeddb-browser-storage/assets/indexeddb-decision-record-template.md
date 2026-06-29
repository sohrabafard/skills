# IndexedDB decision record

Date:
Owner:
Feature:
Status: proposed | accepted | rejected | superseded

## Context

## Decision

## Data classification

| Data | Class | Source of truth | Lifetime | Recoverable? |
|---|---|---|---|---|

## Alaa SDK and gateway boundary

- SDK/gateway client:
- Protected API path:
- Browser-sent headers limited to `Authorization: Bearer`, `X-Request-Id`, and `traceparent`? yes/no
- Trusted gateway headers, decoded JWT claims, and authz decisions stored? no
- `project_id` used only as public UUIDv7 body field when required? yes/no
- `accountKey` used only as local namespace? yes/no

## Browser capability tiers

| Tier | Behavior | Fallback |
|---|---|---|

## Schema

### DB

### Object stores

### Indexes

### Record types

## Quota and eviction plan

- Estimated records:
- Estimated bytes:
- Soft budget:
- Hard budget:
- Cleanup order:
- Persistence request timing:

## Security and privacy

- Secrets stored? no
- Tokens/JWT claims/trusted headers/authz decisions stored? no
- Local entitlement/profile/project data used as authority? no
- PII stored?
- Logout purge:
- Account switch behavior:
- Record validation:

## Migration and concurrency

- New DB version:
- Upgrade path:
- Blocked/versionchange UX:
- Multi-tab coordination:

## Sync/conflict/recovery

## Test matrix

## Observability

## Risks

## Follow-up
