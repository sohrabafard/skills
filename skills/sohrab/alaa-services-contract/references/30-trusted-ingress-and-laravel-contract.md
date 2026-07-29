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
- `X-User-Roles`
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

This set is frozen, and the fleet already agrees on it. In the 2026-07-25 fleet survey the gateway projected
`pid -> X-Project-Id`, `sub -> X-User-Id`, `prm -> X-Access`, `rol -> X-User-Roles`, `jti -> X-Access-Token-Id`,
`m -> X-User-Mobile`, `fn`/`ln` -> the name headers, and the location claims to `X-Location-*`, and `comment`,
`content`, `entitlement-api`, and the `alaa-go-chi` kit each read that same spelling.

- The list is closed. A service reads no trusted identity header outside it, plus the correlation headers
  owned by `20-operational-and-observability-contract.md`, the four step-up headers owned by
  `32-auth-totp-and-step-up-contract.md`, and the request-deadline header owned by
  `22-failure-load-and-deprecation-contract.md`. Reading an undeclared header makes the gateway sanitize list
  incomplete, and an unsanitized header is a spoofing surface.
- Not every gateway-set header is an assertion a service may act on. Three of the four step-up headers state
  a verified fact; the fourth, `X-TOTP-PROOF-REJECTED`, is advisory and may change only a message, never an
  allow or deny decision. That file carries the distinction and the enumerated values, so read it rather
  than inferring the rule from the `X-` prefix.
- Adding or removing one of these names requires a gateway claim-projection change plus the deprecation
  procedure in `22-failure-load-and-deprecation-contract.md`, because the gateway sanitize list, the Postman
  generator, the public-surface test, and every reader change together or the header becomes forgeable.
- The obligation to read `X-Access` in any service that authorizes, and the observable that decides it,
  are owned by `28-backend-permission-authorization-and-role-freeze.md`.

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
- map `X-Access` only through the service's generated, committed catalog-owned permission config
- reject `X-Access` when it maps to zero known permissions after service-local mapping
- when an existing integration or explicit passive-metadata requirement consumes `X-User-Roles`, decode it as compact JSON and require an array of at most 16 unique bytewise-sorted strings matching `^[a-z][a-z0-9_]{0,47}$`, with a maximum compact serialized size of 1024 bytes
- keep trusted roles distinct from permissions: `X-User-Roles` projects the verified `rol` role snapshot, while `X-Access` projects the verified `prm` permission bitmap
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

Do not add role state to a new actor-context baseline. An existing service may keep normalized role names in a separate passive-metadata field only for documented observability or future-migration use; the field must not participate in authorization or other runtime decisions.

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
- stable API-error mapping path aligned with `$alaa-trust-gateway-auth`

Implementation rules:
- do not parse raw trusted headers in controllers, policies, resources, or repositories
- keep policy and Gate decisions focused on business authorization after auth context is normalized
- enforce backend access through exact catalog-owned permissions from `X-Access`; use the contract-defined OpenFGA result where resource-level authorization applies
- do not introduce role resolvers, role-to-permission mappings, role-derived fallbacks, or any role-dependent policy, scope, response, route, validation, feature, or workflow behavior while the freeze in `28-backend-permission-authorization-and-role-freeze.md` is active
- if the service persists trusted user data, keep mutable projections separate from immutable snapshots
- do not fabricate display-city fields from compact location ids unless another contract owns that lookup

## Canonical `project_id` boundary

Use this rule for every Ala Laravel service that accepts a client-visible project selector named `project_id`.

Public request rule:
- `project_id` in public request bodies, query parameters, and DTOs is a canonical UUIDv7 string
- the service resolves that UUIDv7 to its internal project key only after validation passes
- positive integer project ids are not accepted from public clients
- services may persist internal numeric project ids when that is their storage model
- which surfaces must carry the UUIDv7 form, that there is no exception to it, what to do when an internal
  id maps to no row, and the observable that decides it are owned by the canonical `project_id` form rule in
  `25-end-to-end-flow-and-boundaries.md`, because that rule binds Go services as well as Laravel ones. This
  file owns only the Laravel resolution mechanics below.

Trusted context rule:
- `X-Project-Id` is injected by the gateway from the verified token `pid` claim
- downstream services normalize trusted `X-Project-Id` once inside their trusted request context builder
- direct backend-only tests may keep numeric compatibility only when the service explicitly documents that local testing mode
- controllers, policies, Resources, repositories, jobs, and observers must not independently parse raw project identifiers

Preferred Laravel naming:
- `App\Support\Auth\TrustedProjectContext` for shared project-boundary helpers
- `App\Rules\MappedProjectUuidV7` for public UUIDv7 validation plus registry lookup
- `resolveInternalProjectId(mixed $value): ?int` to map a public UUIDv7 or documented trusted compatibility value to storage id
- `resolvePublicProjectId(?int $internalProjectId): ?string` to map storage id back to public UUIDv7
- `resolveBoundaryProjectId(mixed $value): int|string|null` only for trusted or serialization boundaries where existing internal compatibility is explicitly allowed

Implementation order:
1. validate the raw public input as string UUIDv7
2. confirm it maps to an approved project row or registry entry
3. store the resolved internal id in request attributes or a typed DTO
4. pass the internal id into services, queries, and policies — the storage-side callers only
5. write the public UUIDv7, never the internal id, into every event body, structured log field, and cache,
   lock, or rate-limit key that carries `project_id`, per `25-end-to-end-flow-and-boundaries.md`
6. expose the public UUIDv7 again at public response or token boundaries

Do not use a trait or request normalizer that converts public `project_id` to an integer before validation. That leaks the storage model into the public contract and allows internal ids such as `1` to become accepted API input.

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
- use top-level `links` only for true document navigation; what a collection response carries is owned by
  the list pagination contract in `25-end-to-end-flow-and-boundaries.md`

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
