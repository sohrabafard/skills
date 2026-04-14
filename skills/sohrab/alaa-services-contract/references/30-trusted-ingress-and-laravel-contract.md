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
- `X-Project-Id`
- `X-User-Id`
- `X-Access`
- `X-Access-Token-Id`
- `X-User-Mobile`
- `X-User-Fname`
- `X-User-Lname`
- `X-Location-Ostan`
- `X-Location-Shahrestan`
- `X-Location-Bakhsh`
- `X-Location-Shahr`
- `X-Location-Shobe`
- `X-Location-School`

## How trusted ingress relates to entitlement-platform

- the gateway owns authentication and trusted header injection
- a request-time authorization runtime such as `authz-sidecar` or `entitlement-spoa` may already have enforced the route-level fine-grained decision
- the backend still owns normalized request handling and business authorization inside the service

Rules:
- trust the gateway allow or deny result for the route
- do not use allow-side `X-Authz-*` metadata as a credential
- do not bypass the shared platform contract with ad hoc direct OpenFGA checks from a normal downstream backend
- keep service-local policies and Gates focused on business rules after trusted context normalization

## `ResolveUserMiddleware` contract

Responsibility:
- parse trusted headers once
- validate them once
- build one normalized actor context
- synchronize request-time user access across request helpers, facades, and legacy guards still in use

Required validation behavior:
- validate `X-Project-Id` as UUIDv7
- validate `X-User-Id` as a positive integer
- decode `X-Access` as the base64url permission bitmap
- reject `X-Access` when it maps to zero known permissions after service-local mapping
- normalize `X-Access-Token-Id` as an optional non-empty trusted token identifier when present
- handle `X-User-Mobile` exactly according to `$alaa-trust-gateway-auth`
- normalize `X-User-Fname` and `X-User-Lname` as nullable trimmed strings
- validate each `X-Location-*` header as a non-negative integer when present
- use the exact auth error codes owned by `$alaa-trust-gateway-auth`

Actor context must be able to hold at least:
- trusted project identifier
- trusted user identifier
- normalized permission names
- trusted access-token identifier when present
- normalized first and last name values
- normalized location object with `ostan`, `shahrestan`, `bakhsh`, `shahr`, `shobe`, and `school`
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
- compact trusted user-projection normalizer
- auth-state synchronizer
- optional role-derivation helper when needed
- stable API-error mapping path aligned with `$alaa-trust-gateway-auth`

Implementation rules:
- do not parse raw trusted headers in controllers, policies, resources, or repositories
- keep policy and Gate decisions focused on business authorization after auth context is normalized
- if the service persists trusted user data, keep mutable projections separate from immutable snapshots
- do not fabricate display-city fields from compact location ids unless another contract owns that lookup

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
