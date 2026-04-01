# X-Profile Gateway/Auth Request for Change

Implement gateway-trusted `X-Profile` propagation so every downstream backend receives the verified profile claim in a consistent, non-spoofable way.

## Target contract
- Auth-service is the source of truth for the latest user profile.
- Auth-service must place the latest profile into JWT claim `profile` as base64url-encoded UTF-8 JSON.
- Canonical decoded JSON schema uses keys `first_name`, `last_name`, and `shahr` when present. `shahr` keeps the fixed object shape `{id, name}`:
  ```json
  {
    "first_name": null,
    "last_name": null,
    "shahr": {
      "id": null,
      "name": "Mashhad"
    }
  }
  ```
- Auth-service should omit any canonical key whose value is `null`, and it may omit the entire `profile` claim when all three fields are `null`.
- Gateway must sanitize inbound internal headers, verify the JWT, and set `X-Profile` to the exact verified `profile` claim value without decoding or re-encoding it.
- If the token has no `profile` claim, the gateway must not synthesize or fabricate `X-Profile`.

## Auth-service responsibilities
- Extend token issuance so the access token contains claim `profile` whenever trusted downstream services need profile context.
- Build the claim from the latest canonical profile state held by auth-service.
- Encode the claim as base64url(JSON) over UTF-8 bytes.
- Keep canonical keys exactly `first_name`, `last_name`, `shahr` when they are present, omit top-level keys whose value is `null`, and keep `shahr` itself as an object with fixed `id` and `name` keys once present.
- Treat auth-service as the only source of truth for the latest profile state.
- Keep backward-compatible auth response bodies as needed, but do not make downstream services depend on response-body profile data for trusted reads.

## Gateway responsibilities
- Continue stripping all internal auth/context headers from untrusted client input, including `X-Profile`.
- After successful JWT verification, copy verified claim `profile` into upstream header `X-Profile`.
- Do not decode, normalize, rename, pretty-print, or re-encode the claim before forwarding it.
- Do not allow clients to override `X-Profile` manually.
- Do not fabricate `X-Profile` when claim `profile` is absent.
- Preserve the existing trusted-header model for `X-Project-ID`, `X-User-Id`, `X-User-Mobile`, and `X-Access`.

## Downstream service expectations
- Any backend that needs trusted profile data must read `X-Profile` when it is present, base64url-decode it, JSON-decode it, require a JSON object, normalize `first_name` and `last_name` as nullable trimmed strings, and validate `shahr` as either missing or an object with fixed `id` and `name` keys. For `shahr`, missing key => `null`, explicit `null` => `null`, `name` trimmed empty => `AUTH_PROFILE_HEADER_INVALID`, `name` non-empty string => keep, `id` integer or `null` => keep, and any other non-null shape => `AUTH_PROFILE_HEADER_INVALID`.
- If `X-Profile` is absent, downstream services must treat the canonical profile fields as `null` by default.
- Downstream services may store immutable request-time profile snapshots for audit or historical needs.
- Downstream services should keep the latest local user projection in their own `users` read model, but auth-service remains the source of truth for the latest profile.
- `AUTH_PROFILE_HEADER_REQUIRED` remains the canonical reserved error when a downstream route intentionally forces trusted profile presence.
- Services must not assume `X-Profile` is raw JSON and must not trust client-supplied profile data on direct requests.

## Acceptance criteria and validation
- Token issuance test proves claim `profile` exists when profile data is present and decodes to the expected nullable JSON schema.
- Token issuance test also proves auth-service may omit the `profile` claim entirely when all canonical profile fields are `null`.
- Gateway sanitize/inject test proves client-supplied `X-Profile` never reaches upstream unchanged.
- Gateway forwarding test proves upstream receives the exact verified claim value in `X-Profile`.
- Gateway missing-claim test proves no `X-Profile` header is fabricated when `profile` is absent.
- End-to-end downstream test proves a backend can decode `X-Profile`, normalize nullable `first_name` and `last_name`, validate the object-shaped `shahr` contract, refresh the latest local user projection, clear stale local raw profile state when the header is absent, and store an immutable request-time snapshot.
- Rollout note: downstream services that currently assume raw JSON `X-Profile` must migrate to strict base64url decode before the new contract is enabled in production.
