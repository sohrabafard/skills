# TypeScript Aggregate Consumer Pattern

Read `references/shared-consumer-contract.md` first; the six rules there govern this file and are not repeated. The
descriptor and the drift severity table are in `references/catalog-workflow.md`. `input_shape` is
`typescript_permission_catalog`.

An aggregate consumer owns nothing: it contributes no source observation to ownership drift, and registering one changes
no ownership, no `service_key`, and no bitmap allocation. A permission **owner** instead owns a `service_key` and
receives an artifact holding only its own permissions. The two arrays and the `scope` rule are in
`references/catalog-workflow.md`.

## Emitted surface

```ts
export const PERMISSIONS = { EXAMPLE_GET_THING: "example_get_thing" } as const;
export type PermissionKey = (typeof PERMISSIONS)[keyof typeof PERMISSIONS];
export const PERMISSION_BY_BITMAP_ID = { 7: PERMISSIONS.EXAMPLE_GET_THING } as const satisfies Readonly<Record<number, PermissionKey>>;
export const BITMAP_ID_BY_PERMISSION = { [PERMISSIONS.EXAMPLE_GET_THING]: 7 } as const satisfies Readonly<Record<PermissionKey, number>>;
export const PERMISSION_CATALOG_ACTIVE_COUNT = /* read from the artifact */;
export const PERMISSION_CATALOG_MAX_BITMAP_ID = /* read from the artifact */;
export const PERMISSION_CATALOG_FINGERPRINT = /* read from the artifact */;
```

The identifier is the permission key upper-cased. Active permissions only, ordered by `bitmap_id`, ESM named exports,
strict and framework-free, generated-file header, two-space indent, double quotes, no trailing comma, LF only. The
`satisfies` clauses make both maps exhaustive and type-checked against `PermissionKey` at compile time, so a partial or
mistyped map fails the build rather than a request. The fingerprint is a sha256 over id-and-key pairs, so it moves on a
real change and not on reformatting.

The last three values are placeholders on purpose — read them from the applied artifact, per the never-freeze-the-scale
rule in `SKILL.md`.

## Emitter refusals

Generation throws, and the CLI exits `2`, on each of these. Via the drift analyzer the same failure surfaces as fatal
`AGGREGATE_CONSUMER_GENERATION_FAILED`.

| Condition | Message |
| --- | --- |
| Non-positive bitmap id | `Cannot emit TypeScript for permission [x] with non-positive bitmap id [n].` |
| Key not matching `/^[a-z][a-z0-9_]*$/` | `Permission key [x] cannot be emitted as a TypeScript identifier.` |
| Duplicate key among actives | `Permission key [x] appears more than once in the active catalog.` |
| Two keys colliding on one identifier | `TypeScript identifier collision: [a] and [b] both map to [X].` |
| Any line over 80 columns | `Generated TypeScript line exceeds the client formatter print width of 80 columns: [...]` |

The 80-column cap is the consumer's formatter print width and it caps permission-key length. Shorten the key in the
catalog; never reformat after generation and never widen the cap to fit a key.

## Export surface

Export **names** across the package boundary — `PERMISSIONS`, `PermissionKey`, the decoder, its result type — and keep
`PERMISSION_BY_BITMAP_ID` and `BITMAP_ID_BY_PERMISSION` one level in, so feature code cannot begin reasoning in bit ids.
Application code compares against `PERMISSIONS.*`, never a raw string and never a bitmap id. Keep the generated data and
the logic that reads it in separate files, so the generated artifact stays a pure static registry under the consumer's
file-size rules.

## Frontend decoding is a UI hint, not authorization

A browser client may decode `prm`, `prv`, and `av` from its **own** access token to derive UI capability state. Name the
function so the boundary is unmissable, for example `decodeUnverifiedUiAuthorization`.

- It never verifies the token signature and never gates a security decision. The gateway and the owning service stay
  authoritative, and a deny response is the only authoritative answer.
- It fails closed: malformed input grants nothing and throws nothing.
- Unknown, deprecated, and reserved bits grant nothing, so a token issued against a newer catalog degrades to fewer
  hints.
- **A valid token with an empty bitmap is a legitimate ready state and must never invalidate the session or log the user
  out.** This is the deliberate exception to the fail-closed-on-zero rule, which is server-side only.
- Cap token, payload, and bitmap length; return no raw token and no raw claims; log nothing; persist nothing separately
  from the token. These caps protect the browser only — the server-side cap is in
  `references/shared-consumer-contract.md`.
- Capability changes appear only after login, token refresh, or reissuance, because the token is an issuance-time
  snapshot.
- Never send `X-Access` or any other gateway-owned authorization header from a client. Decoding a claim from your own
  token is not asserting a trusted header; `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) owns that boundary
  and wins on any conflict.

## Wiring into the consumer application

Only the first step is this skill's: a **decoder in the SDK package beside the generated file**, named so the boundary is
unmissable, mapping set bits to names through the generated map and returning a small frozen result — a state, the
recognized permissions, and optional `prv`/`av`.

```ts
export function decodeUnverifiedUiAuthorization(token: string | null | undefined): UnverifiedUiAuthorization;
```

Everything after it is application consumption and is owned by
`alaa-services-contract references/60-frontend-sdk-consumption-contract.md` (`/alaa-services-contract`,
`$alaa-services-contract`): where the single recompute point sits, the typed helpers over the stored snapshot, store
ownership, SSR and hydration, the three UI states, and the app-side anti-patterns. Read it before writing application
code; it wins on conflict. Two rules from this side constrain that code and are not negotiable there: application code
compares against `PERMISSIONS.*` only, and the decode happens once per token change, never per component render.

## Tests

- The shipped `catalog/services.json` still registers this consumer, so it cannot silently stop regenerating.
- Deprecated and reserved permissions are absent from the artifact and ordering is by `bitmap_id`.
- Generation is byte-identical across reversed input ordering and emits no CRLF.
- The emitter rejects an invalid identifier, a duplicate key, and an over-width line.
- Drift fires for each `AGGREGATE_CONSUMER_*` code, including a hand edit that preserves the permission set.
- In the consumer repository: typecheck, unit tests, build, export-surface test, formatter check, and file-size gate,
  per `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`) and `/alaa-mono-package`
  (`$alaa-mono-package`).
