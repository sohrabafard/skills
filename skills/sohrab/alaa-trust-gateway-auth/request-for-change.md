# Compact Gateway/Auth Request For Change

Implement the compact trusted-identity contract so downstream services receive only sanitized gateway headers derived from verified JWT claims.

## Target contract

- Standard claims remain unchanged: `aud`, `jti`, `iat`, `nbf`, `exp`, `sub`, `scopes`
- Custom claims are `m`, `prm`, `prv`, `av`, `pid`, `loc`, `fn`, and `ln`
- `pid` is the public project boundary
- `loc` carries the compact location bundle with `o`, `sr`, `b`, `sh`, `br`, and `sc`
- `fn` and `ln` carry the trusted first and last names
- `0` means the source value was null for a location id
- empty string means the source value was null for a name field
- `prv` and `av` remain raw JWT metadata only and are not forwarded as headers by default
- public and service-facing payloads keep the field name `project_id`; only the compact JWT claim uses `pid`

## Gateway behavior

- sanitize inbound auth/context headers before proxying
- inject trusted headers only from verified claims
- keep required protected-route claims limited to `pid` and `sub`
- inject `X-PROJECT-ID`, `X-USER-ID`, `X-USER-MOBILE`, `X-ACCESS`, `X-ACCESS-TOKEN-ID`, `X-TOKEN-CLIENT-ID`, `X-TOKEN-ISSUED-AT`, `X-TOKEN-NOT-BEFORE`, `X-TOKEN-EXPIRES-AT`, `X-USER-SCOPES`, `X-User-Fname`, `X-User-Lname`, and the `X-Location-*` headers from the matching claims
- do not fabricate missing compact values

## Auth-service behavior

- emit the compact claim set in both initial token issuance and refresh paths
- keep the public project boundary semantics stable under `pid`
- normalize missing location ids to `0`
- normalize missing names to `""`

## Validation goals

- gateway tests prove spoofed inbound trusted headers are stripped and replaced
- gateway tests prove compact claim values reach upstream headers
- downstream tests prove identity and location headers are parsed once into a trusted request context
- token tests prove the emitted JWT uses only the compact custom claim contract
