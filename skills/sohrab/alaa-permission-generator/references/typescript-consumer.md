# TypeScript Aggregate Consumer Pattern

Use `input_shape: typescript_permission_catalog`. This is the **aggregate consumer** shape: the consumer reads every
active permission and owns none of them. The client frontend monorepo is the first of them.

## Aggregate consumer versus permission owner

A permission **owner** owns a `service_key` and a slice of the catalog. It appears in the `services` array of
`catalog/services.json`, contributes source observations to ownership drift, and receives a generated artifact
containing only its own permissions.

An aggregate **consumer** owns nothing. It appears in a separate `aggregate_consumers` array so no import or drift rule
can mistake it for an owner. Registering one never changes permission ownership, `service_key` values, or bitmap
allocation.

```json
{
    "consumer_key": "client",
    "owner_repo": "client",
    "source_path": "packages/sdk-auth/src/generated/permission-catalog.ts",
    "input_shape": "typescript_permission_catalog",
    "generated_target": "generated/client/packages/sdk-auth/src/generated/permission-catalog.ts",
    "scope": "all_active"
}
```

`scope: all_active` is the only supported scope. Do not add the consumer to any permission's `generated_targets`: that
field uses `service_key:path` syntax and an aggregate consumer has no `service_key`. Coverage is derived from the scope,
so a new permission reaches the consumer with no per-permission bookkeeping.

## Generated surface

```ts
export const PERMISSIONS = { CONTENT_GET_SETS: "content_get_sets" } as const;
export type PermissionKey = (typeof PERMISSIONS)[keyof typeof PERMISSIONS];
export const PERMISSION_BY_BITMAP_ID = { 64: PERMISSIONS.CONTENT_GET_SETS } as const satisfies Readonly<Record<number, PermissionKey>>;
export const BITMAP_ID_BY_PERMISSION = { [PERMISSIONS.CONTENT_GET_SETS]: 64 } as const satisfies Readonly<Record<PermissionKey, number>>;
export const PERMISSION_CATALOG_ACTIVE_COUNT = 119;
export const PERMISSION_CATALOG_MAX_BITMAP_ID = 119;
export const PERMISSION_CATALOG_FINGERPRINT = "sha256:…";
```

Active permissions only, ordered by `bitmap_id`, `bit_index = bitmap_id - 1`, ESM named exports, strict and
framework-free, generated-file warning header, LF endings. The `satisfies` clauses make the reverse map exhaustive at
compile time. The fingerprint is a sha256 over `bitmap_id` and `permission_key` pairs, so it moves on real changes and
not on reformatting.

## Integration rules

1. Generation writes only inside `alaa-permission-catalog`, to `generated/<owner-repo>/<source-path>`. Applying to the
   consumer repository is a separate, explicitly authorized step, exactly as for Laravel and Go consumers.
2. Commit the applied artifact at the exact `source_path`. Never hand-edit it and never fetch the catalog at runtime.
3. Match the consumer's formatter profile in the emitter, not by reformatting after generation. Generation fails loudly
   on a line wider than the consumer's print width, on a permission key that is not a valid identifier, on a duplicate
   key, and on two keys that collide on one generated identifier.
4. Keep a single generated map. Do not add a hand-written duplicate, an environment override, or a runtime fetch.
5. Expose permission **names** across the consumer's public boundary; keep the raw bitmap tables internal. Application
   code compares against `PERMISSIONS.*`, never raw strings and never bitmap ids.
6. Generated data and the logic that reads it live in separate files, so the generated artifact stays a pure static
   registry under the consumer's file-size rules.

## Frontend decoding is a UI hint, not authorization

A browser client may decode `prm`, `prv`, and `av` from its **own** access token to derive UI capability state. Name the
function so the boundary is unmissable — for example `decodeUnverifiedUiAuthorization`.

- It never verifies the token signature and must never gate a security decision. The gateway and the owning service stay
  authoritative; a deny response is the only authoritative answer.
- It fails closed: malformed input grants nothing and never throws.
- Unknown, deprecated, and reserved bits grant nothing, so a token issued against a newer catalog degrades to fewer
  hints instead of failing.
- A valid token with an empty bitmap is a legitimate ready state. **An empty frontend permission set must never
  invalidate the session or log the user out.** This is the opposite of the downstream-service rule, where a protected
  request resolving to zero known permissions is rejected — that rule is server-side trusted-context normalization.
- Bound the work (token, payload, and bitmap length caps), return no raw token and no raw claims, log nothing, and
  persist nothing separately from the token.
- Capability changes appear only after login, token refresh, or reissuance, because the token is an issuance-time
  snapshot. Never send `X-Access` or any other gateway-owned authz header; decoding a claim from your own token is not
  the same as asserting a trusted header.

## Wiring the artifact into the consumer application

Onboarding shape, in dependency order. The generated file is data; everything below is the consumer repository's code.

1. **Decoder** in the SDK package, next to the generated file, named so the boundary is unmissable. It maps set bits to
   names via the generated map and returns a small frozen result — a state, the recognized permissions, and optional
   `prv`/`av`.
2. **One recompute point** in the application, wherever the access token is set. Every lifecycle path (login, refresh,
   cross-tab sync, hydration, logout) already funnels through that setter, so a single call there covers all of them
   with no extra wiring and no watchers.
3. **Typed helpers** over the stored snapshot — a single-permission check, an any-of check, and an all-of check — each
   taking generated `PERMISSIONS.*` values and each returning false unless the snapshot decoded successfully.
4. **Application code** calls only the helpers. It does not call the decoder, read the permission array directly, or
   import the generated maps.

```ts
// SDK package: exported once
export function decodeUnverifiedUiAuthorization(token: string | null | undefined): UnverifiedUiAuthorization;

// Application: one recompute point
setAccessToken(token) {
  this.accessToken = normalize(token);
  this.uiAuthorization = decodeUnverifiedUiAuthorization(this.accessToken);
}

// Application: typed helpers, used by feature code
hasPermission(PERMISSIONS.CONTENT_PUT_SET);
```

Export **names** across the consumer's public boundary (`PERMISSIONS`, the key type, the decoder, its result type) and
keep the bitmap maps one level in, so feature code cannot start reasoning in bit ids.

Two failure modes to expect when an agent debugs this later:

- *"The backend granted the permission but the UI still hides the control."* The token is an issuance-time snapshot;
  the hint updates only on the next login, refresh, or reissuance. This is correct behavior, not a decoder bug.
- *"The decode returned nothing, so we logged the user out."* Wrong by construction — see the UI-hint rules above.

## Ownership boundary

This file owns the catalog side: the descriptor, generation, the emitted surface, drift, apply, and the decoder's
security contract. How the **application** consumes the result — store ownership, helper semantics, SSR and hydration,
the three UI states, and the app-side anti-patterns — belongs to `$alaa-services-contract`
`references/60-frontend-sdk-consumption-contract.md`. Read that before writing application code; do not restate its
rules here, and do not let the two drift.

## Drift interpretation

Aggregate drift is strict, not warning-only. The applied artifact must match generated output byte for byte.

| Code | Severity |
| --- | --- |
| `AGGREGATE_CONSUMER_ARTIFACT_NOT_APPLIED` | warning — not yet applied, does not block |
| `AGGREGATE_CONSUMER_PERMISSION_MISSING` | fatal |
| `AGGREGATE_CONSUMER_PERMISSION_EXTRA` | fatal |
| `AGGREGATE_CONSUMER_BITMAP_ID_MISMATCH` | fatal |
| `AGGREGATE_CONSUMER_IDENTIFIER_COLLISION` | fatal |
| `AGGREGATE_CONSUMER_MAP_DESYNC` | fatal |
| `AGGREGATE_CONSUMER_MALFORMED` | fatal |
| `AGGREGATE_CONSUMER_GENERATION_FAILED` | fatal |
| `AGGREGATE_CONSUMER_STALE_METADATA` | error |
| `AGGREGATE_CONSUMER_MANUAL_EDIT` | error |

CRLF is normalized before comparison, so a Windows checkout does not report false drift.

## Tests

- Assert the shipped `catalog/services.json` still registers the consumer, so the proposal cannot silently stop
  regenerating.
- Assert deprecated and reserved permissions are excluded and that ordering is by `bitmap_id`.
- Assert generation is deterministic across input ordering and emits no CRLF.
- Assert the emitter rejects invalid identifiers, duplicate keys, and over-width output.
- Assert drift fires for each code above, including a hand edit that preserves the permission set.
- In the consumer repository: typecheck, unit tests, build, export-surface tests, formatter check, and file-size gate.
- Re-run catalog import and strict drift after applying, and confirm the aggregate findings drop to zero.
