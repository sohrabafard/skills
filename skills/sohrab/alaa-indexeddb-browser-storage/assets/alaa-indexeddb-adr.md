# ADR: Alaa IndexedDB feature

Date:
Owner:
Feature:
Status: proposed

## Context in Alaa architecture

- Client traffic enters through Gateway.
- Browser clients use `@alaa/sdk` / `@alaa/sdk-vue` for protected calls; storage code does not own token attach, refresh, trusted-header rejection, or route composition.
- Auth/profile/session truth remains server-side.
- `project_id` is a public UUIDv7 body field only where an API contract requires it; `accountKey` is only a local storage namespace.
- Content/course truth remains in content/domain services.
- Watch/analytics ingestion belongs to wa.
- Upload transfer lifecycle belongs to upload service; domain attachment belongs to target service.

## Decision

## Data stored locally

| Store | Data | Source of truth | Account-scoped? | TTL | Security class |
|---|---|---|---|---|---|

## Server interaction

- APIs used:
- SDK/gateway client used:
- Idempotency keys:
- Conflict handling:
- Revalidation:
- Direct service-local/authz/OpenFGA calls? no

## Browser support

- Minimum core behavior:
- Enhanced behavior:
- Fallbacks:
- Safari/iOS notes:

## Quota/storage budget

## Migration/versioning

## Security/privacy

- Tokens, decoded JWT claims, trusted gateway headers, and authz decisions stored? no
- Local entitlement/profile/project data used only as cache/display hints? yes

## Tests and rollout

## Observability

## Consequences
