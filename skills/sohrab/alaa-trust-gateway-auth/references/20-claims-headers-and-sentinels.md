# Compact claims, the header projection, sentinels, and step-up headers

Read this file when you are deciding which claim a value travels in, which header
it arrives as, what an absent value looks like on the wire, or which step-up
headers a service is allowed to read.

The **set** of trusted header names is frozen and owned by `alaa-services-contract`
`references/30-trusted-ingress-and-laravel-contract.md`. If that file and this one
ever disagree about a name, that file wins and this one is the defect. What this
skill owns is the projection below — which verified claim becomes which header —
and the trust rules attached to it.

## The claim set

Standard claims are unchanged: `aud`, `jti`, `iat`, `nbf`, `exp`, `sub`, `scopes`.

Custom compact claims are `m`, `prm`, `rol`, `prv`, `av`, `pid`, `loc`, `fn`, `ln`.

| Claim | Meaning | Projected to |
|---|---|---|
| `pid` | public project boundary, UUIDv7 | `X-Project-Id` |
| `sub` | authenticated user id | `X-User-Id` |
| `m` | mobile | `X-User-Mobile` |
| `prm` | permission bitmap | `X-Access` |
| `rol` | canonical role-name array, issuance-time snapshot | `X-User-Roles` |
| `prv` | permission catalog version | **not forwarded** |
| `av` | authorization version | **not forwarded** |
| `jti` | access-token id | `X-Access-Token-Id` |
| `aud` | token audience | `X-TOKEN-CLIENT-ID` |
| `iat` | issued at | `X-TOKEN-ISSUED-AT` |
| `nbf` | not before | `X-TOKEN-NOT-BEFORE` |
| `exp` | expires at | `X-TOKEN-EXPIRES-AT` |
| `scopes` | token scopes | `X-USER-SCOPES` |
| `fn` | first name | `X-User-Fname` |
| `ln` | last name | `X-User-Lname` |
| `loc.o` | ostan | `X-Location-Ostan` |
| `loc.sr` | shahrestan | `X-Location-Shahrestan` |
| `loc.b` | bakhsh | `X-Location-Bakhsh` |
| `loc.sh` | shahr | `X-Location-Shahr` |
| `loc.br` | shobe | `X-Location-Shobe` |
| `loc.sc` | school | `X-Location-School` |

This is the only projection table in this skill. A second copy would drift, and it
already did: an earlier revision listed the forwarded surface in two places and one
of them omitted `X-User-Roles`, which is how a frozen, sanitized header comes to
look optional to an agent auditing a sanitize list.

`prv` and `av` are never forwarded as headers. They are invalidation and
diagnostics metadata for `prm`. The single sanctioned reader outside the gateway is
the frontend SDK's unverified decoder reading the client's own token to derive UI
hints, and that read is never an authorization decision, never becomes a header,
and never invalidates a session when it yields no permissions. The consumer rules
are owned by `/alaa-permission-generator` (`$alaa-permission-generator`)
`references/typescript-consumer.md`.

Auth is the only runtime issuer of `prm`, `prv` and `av`.

## Worked example of a verified access token

```json
{
  "aud": ["3"],
  "jti": "01JQ8Q7QW6YJ7M9X4D3P2K1H8N",
  "iat": 1775296800,
  "nbf": 1775296800,
  "exp": 1775300400,
  "sub": "1001",
  "scopes": [],
  "prm": "AAABgQ",
  "prv": 1,
  "av": 2,
  "rol": ["school_admin", "teacher"],
  "m": "09123456789",
  "pid": "018f7d8f-8cb0-7a85-9a89-e3f61052f840",
  "loc": {
    "o": 8,
    "sr": 257,
    "b": 12,
    "sh": 2576,
    "br": 12354,
    "sc": 9988
  },
  "fn": "Sohrab",
  "ln": "Aboozarkhanifard"
}
```

`rol` is present in this example deliberately. New and refreshed access tokens
carry it, including `[]` for a user with no roles. A present `rol` is a compact
JSON array of at most 16 unique, bytewise-sorted canonical role names matching
`^[a-z][a-z0-9_]{0,47}$`, serialising to at most 1024 bytes; the gateway rejects a
present invalid claim before forwarding and injects only the normalized array. An
absent `rol` is handled in `references/30-fail-closed-cases.md`, case 4.

## Null sentinels

Auth emits a sentinel rather than omitting a compact field, so the shape of the
claim set stays stable across users:

- `0` means the source value was null for a location id.
- The empty string means the source value was null for a name field.

**Gateway rule.** The gateway forwards the sentinel the token carried and never
invents a value that is not in the verified claims. If the claim is absent
entirely, the gateway injects nothing; it does not substitute a sentinel.

**Service rule.** Convert both sentinels once, at ingress, into the shape the
repository uses for absence. Raw sentinel handling spread across policies,
controllers and repositories is how `0` ends up saved as a real school id.

## What the gateway may and may not fabricate

- The gateway injects a header only from a claim it verified in the token it just
  checked.
- The gateway injects only claims that are present. An absent optional claim
  produces no header rather than an empty one, because an empty header and an
  absent header decide differently in most parsers and only one of them is the
  contract.
- The gateway does not derive tenant from hostname, path prefix, request body or
  query string. A service behind it may read a body field or a query parameter on a
  route that admits tokenless requests; `references/10-verification-and-ingress.md`
  states when, and states that the gateway still reads neither.
- The gateway does not decode `prm` and does not consume any service's generated
  permission map. It projects the claim and stops.
- `Authorization` is stripped after successful verification in the current
  deployment values, so no service receives the raw bearer.
- `X-Request-ID` is preserved when the client sent one and generated otherwise. It
  is correlation only and is neither an auth nor a tenant header.
- The gateway overwrites `X-Forwarded-Proto` to `https` because TLS terminates
  upstream. The gateway repository shows no equivalent sanitization or re-issuance
  for `X-Forwarded-For` or `X-Real-IP`, so a service that needs a client address
  for a security decision establishes that gap's current state itself before
  relying on either header.

## TOTP step-up headers

A service reads exactly three step-up headers. Reading any other `X-TOTP-*` name
leaves that name off the sanitize list, and an unsanitized header is forgeable by
any public client.

| Header | Set by | Carries |
|---|---|---|
| `X-TOTP-PURPOSE` | gateway, only on full validity | the proof's `purpose` claim, verbatim |
| `X-TOTP-VERIFIED-UNTIL` | gateway | the proof `exp` as **Unix epoch seconds** |
| `X-TOTP-PROOF-ID` | gateway | the proof `jti`, a UUID |

- **The presence of all three is the observable that stands in for every gateway
  check**, because the gateway injects them only when signature, algorithm
  allow-list, `typ`, `aud`, `iss`, required-claim completeness, `exp`/`nbf` with
  clock skew, and the binding of the proof's `sub` and `pid` to the already-verified
  access token all passed.
- **Compare `X-TOTP-PURPOSE` to the purpose the operation requires before allowing
  the operation**, because the gateway forwards a proof issued for one operation to
  every other operation unchanged, and only this comparison keeps them apart.
- **Read `X-TOTP-VERIFIED-UNTIL` as Unix epoch seconds and reject the request when
  that instant is past**, because the response body carries the same instant as an
  ISO 8601 string and a parser written against the body reads the header wrong.
- **`X-TOTP-PROOF-ID` is the `jti` and is the correlation key in audit records.** A
  service that needs one-shot semantics records consumed `jti` values itself,
  because the gateway enforces no single-use rule and holds no replay table; the
  proof is reusable until its own `exp`, exactly like an access token.
- **Never accept a step-up header from a public client.** The gateway deletes all
  three and sweeps every inbound `x-totp-*` except the public carrier, so any value
  a service sees arrived from the gateway.
- **The raw proof travels only in `X-TOTP-Proof`, and only from a public client to
  the gateway**, which consumes and deletes it. No service receives the token and
  no service verifies a proof signature itself.
- **No service other than auth validates a raw TOTP code or a recovery code**,
  because doing so needs the user's TOTP secret and widens that secret's blast
  radius from one service to every service.

The proof lifetime defaults to 300 seconds.

The claim set of the proof token, the step-up response body, the purpose-naming
rules and the client-side proof-cache rules are owned by `/alaa-services-contract`
(`$alaa-services-contract`) `references/32-auth-totp-and-step-up-contract.md`.
Denial behaviour for every step-up failure is in
`references/30-fail-closed-cases.md`.

**One correction to record.** `alaa-services-contract`
`references/32-auth-totp-and-step-up-contract.md:125` states that the gateway
verifies the proof's `purpose`. The gateway checks that the claim is present and
forwards it verbatim; it compares it to nothing, because it holds no list of
step-up-required routes. Only the backend compares. Verified against the gateway
repository on 2026-07-27 at `charts/gateway/templates/configmap.yaml:487-583` and
`docs/totp-proof-gateway-contract.md:53`.
