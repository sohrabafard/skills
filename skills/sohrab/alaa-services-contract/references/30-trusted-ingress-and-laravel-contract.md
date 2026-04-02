# Trusted Ingress And Laravel Contract

## Service modes

### Mode B - Laravel backend service
Apply the Laravel response and middleware rules in this file.

### Mode C - Laravel downstream trusted service
Apply the full trusted-ingress contract in this file when the service consumes sanitized Ala gateway headers.

### Mode D - Laravel auth-boundary service
A Laravel service that owns the trust boundary may satisfy the trusted-ingress semantics with request guards or `Auth::viaRequest(...)` instead of a literal class named `ResolveUserMiddleware`, but its outward behavior must still match this contract.

## Trusted header names

Use these exact header names unless a temporary migration is explicitly documented:
- `X-Project-ID`
- `X-User-Id`
- `X-Access`
- `X-User-Mobile`
- `X-Profile`

## `ResolveUserMiddleware` contract

Responsibility:
- parse trusted headers once
- validate them once
- build one normalized actor context
- synchronize request-time user access across request helpers, facades, and legacy guards still in use

Required validation behavior:
- validate `X-Project-ID` as UUIDv7
- validate `X-User-Id` as a positive integer
- decode `X-Access` as the base64url permission bitmap
- reject `X-Access` when it maps to zero known permissions after service-local mapping
- handle `X-User-Mobile` exactly according to `$alaa-trust-gateway-auth`
- decode `X-Profile` as base64url JSON
- require `X-Profile` to be an object when present
- normalize `first_name` and `last_name` as nullable trimmed strings
- normalize `shahr` exactly according to `$alaa-trust-gateway-auth`
- use the exact auth error codes owned by `$alaa-trust-gateway-auth`

Actor context must be able to hold at least:
- trusted project identifier
- trusted user identifier
- normalized permission names
- normalized profile payload
- trusted mobile when present
- `request_id`
- `trace_id`
- optional derived role when the service uses role inference

Auth synchronization rules:
- keep `$request->user()` and `Auth::user()` consistent
- also synchronize documented legacy guards that the repository still reads
- do not rebuild the actor independently in controllers or policies
- keep synchronization request-scoped and Octane-safe

Required support components:
- trusted request context helper
- trusted actor context value object or DTO
- permission bitmap decoder and mapper
- trusted profile parser and normalizer
- auth-state synchronizer
- optional role-derivation helper when needed
- stable API-error mapping path aligned with `$alaa-trust-gateway-auth`

Implementation rules:
- do not parse raw trusted headers in controllers, policies, resources, or repositories
- keep policy and Gate decisions focused on business authorization after auth context is normalized
- if the service persists trusted profile data, keep mutable projections separate from immutable snapshots

## Laravel success-response contract

Treat Resources as the public success-response boundary for Laravel `/api/*` success responses.

Rules:
- use `JsonResource` or `ResourceCollection`
- keep controllers responsible for HTTP status and transport serialization
- keep services returning domain data or typed DTOs, not transport-shaped arrays
- keep Resources responsible for public field shaping
- keep controllers thin and deterministic

Exact success envelope rules:
- every successful `/api/*` JSON response must use a top-level `data` key unless a documented exception exists
- `data` must be an object for one resource or one compound result
- `data` must be an array for collections
- nested child resources stay inline and do not get their own nested `data` wrapper
- use top-level `meta` only for transport metadata
- use top-level `links` only for pagination or true document navigation concerns

Boundary rules:
- do not return transport-shaped arrays from services
- do not leak raw models, internal IDs, persistence-only fields, or temporary implementation fields through controllers
- attach transport headers at the Resource response boundary when needed

Default implementation guidance:
- preserve an existing success envelope only when it already matches the current contract or the contract is being intentionally revised in the same effort
- keep current error responses aligned by default unless a stricter contract is explicitly in scope
- inspect existing repository patterns before changing response serialization
- use Laravel Boost `search-docs` first for version-specific Resource guidance when it is available
- keep docs, examples, and Postman artifacts aligned with the shipped Resource shape when the contract changes

Why this rule exists:
- it keeps response shapes consistent across endpoints
- it makes tests simpler because assertions target one transport boundary
- it makes docs and Postman examples easier to keep synchronized
- it prevents accidental leakage of internal IDs, persistence details, or backend-only fields
- it makes contract review safer because the public success shape is centralized instead of scattered

Auth reference precedent:
- auth repository commit `40d7e6e` is the approved reference precedent for this rule
- that precedent established Resource-first success responses for `/api/*`
- it also established service or domain DTOs under the controller boundary, controller-owned HTTP status and serialization, and removal of backend-only public leakage such as `access_token_id`

Laravel implementation rules:
- inspect middleware order relative to `SubstituteBindings`
- use request-scoped auth normalization compatible with Laravel guards
- use current Laravel request-based auth mechanisms when appropriate
- use current Laravel logging-context sharing mechanisms
- keep Octane request state isolated per request
- keep controllers thin and Resources explicit
