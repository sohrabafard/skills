# ADR — browser storage for <feature> in the `client` repository

Date: `<ISO date>` · Owner: `<name>` · Status: `proposed | accepted | superseded`

Use this when the change meets an ADR trigger in `references/95-alaa-integration-playbook.md`.
For a change below those triggers, `assets/indexeddb-decision-record-template.md` is enough.

## Where this sits in the platform

- Client traffic reaches the platform through the gateway; the gateway and auth path is the
  trust boundary. Storage code owns none of it — `/alaa-trust-gateway-auth`
  (`$alaa-trust-gateway-auth`).
- Identity, profile and session truth are server-side.
- Content and course truth are owned by their services; analytics ingestion by its own.
- `accountKey` is a local storage partition only, never authority.
- Existing storage in this repository, which this change must fit rather than duplicate:
  `src/storage/browserKeyValueStorage.ts`, `src/sdk/browserResponseCache.ts`,
  `src/content-show/waOutboxStorage.ts`.

## Decision

`<...>`

## What is stored, and why it may be

| Store | Data | Class | Source of truth | Account-scoped | TTL or cap |
|---|---|---|---|---|---|
| `<...>` | `<...>` | `<...>` | `<...>` | `<yes/no>` | `<...>` |

Answered explicitly: no token, decoded JWT claim, trusted gateway header, permission bitmap or
authorization decision is stored `<confirm>`; every cached value is used to render and never to
decide `<confirm>` — `references/61-authority-boundary.md`.

## Server interaction

- APIs used, and the SDK client through them: `<...>`
- Idempotency keys, and where they are generated: `<...>` — codec is
  `/alaa-crockford-base32-codecs` (`$alaa-crockford-base32-codecs`)
- Conflict handling and revalidation: `<...>`
- Any direct call to a service-local route, an authorization sidecar or a policy engine?
  **`<must be: no>`**

## Names registered before merge

Every one is `/alaa-services-contract` (`$alaa-services-contract`).

| Kind | Name | Registered |
|---|---|---|
| database | `<...>` | `<yes>` |
| object store | `<...>` | `<yes>` |
| index | `<...>` | `<yes>` |
| configuration key | `<...>` | `<yes>` |
| event | `<...>` | `<yes>` |

## Budget, quota and eviction

- Filled budget file: `<path>`
- Persistence requested at: `<the user action>` — and what the UI says when it is refused: `<...>`
- Recovery when the origin is evicted: `<...>`

## Browser support

- Minimum tier at which the feature is offered: `<...>`
- Behaviour one tier down: `<...>`
- WebKit and iOS notes, and the lane that proves them: `<...>`

## Migration and concurrency

`<version, branch, blocked UX, service-worker connection, Web Lock names>`

## Proof and rollout

`<levels, lanes, and what a green run does not bound>`

## Consequences

`<what this makes easy, what it makes hard, what it forecloses>`
