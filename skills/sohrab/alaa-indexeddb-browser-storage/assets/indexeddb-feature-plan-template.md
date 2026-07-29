# IndexedDB feature plan — <feature>

Fill every heading. An empty heading is a finding.

## Goal, assumptions, non-goals

## Storage API choice

Which API, and the retrieval shape that decides it —
`references/10-indexeddb-mental-model-and-boundaries.md`. If any value exceeds 1 MB, name its
line in the budget file.

## Data model

Record types with `id`, `schema`, `accountKey` where user-scoped, `createdAt`, `updatedAt`.

## Authority boundary

- Nothing stored from `secret_or_credential`, `trusted_gateway_context` or
  `authorization_truth`: `<confirm>` — `references/61-authority-boundary.md`
- `accountKey` used only as a storage partition: `<confirm>`
- Every cached value renders and never decides: `<confirm>`
- Owner of anything this plan cannot decide: `/alaa-trust-gateway-auth`
  (`$alaa-trust-gateway-auth`), `/alaa-permission-generator` (`$alaa-permission-generator`),
  `/alaa-security-review` (`$alaa-security-review`)

## Capability detection

Which tier this path requires; what it does one tier down.

## Schema change

Version, branch, indexes with the read each serves, and the key-path verification against the
record type.

## Read path, with the bound on each read

## Write path, with the failure class of each write

Quota, eviction, blocked upgrade, aborted transaction, unavailable storage —
`references/31-quota-exceeded-and-cleanup.md`.

## Offline and sync behaviour

## Quota, budget and persistence

Budget file path; when persistence is requested; recovery after eviction.

## Concurrency

Tabs, workers, the service worker; Web Lock names; `BroadcastChannel` messages.

## Migration

## Tests, by proof level

`/alaa-testing-strategy` (`$alaa-testing-strategy`); lanes in
`assets/browser-test-matrix.yaml`.

## Telemetry

Names `/alaa-services-contract` (`$alaa-services-contract`); levels
`/alaa-observability-soc` (`$alaa-observability-soc`).

## Rollout and open questions
