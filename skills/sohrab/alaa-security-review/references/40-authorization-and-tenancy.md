# Authorization, Tenancy, And Concurrency

Read when the change touches an authentication or authorization decision, tenant derivation, a cache key, a background job, an export, a search index, a rate limit, or a read followed by a dependent write.

## Two decisions, two pieces of code

Every entry point makes an **authentication** decision - who is calling - and an **authorization** decision - whether that caller may perform this operation on this object. They are separate code, and the review names both files. An endpoint that is authorized by the fact that it authenticated has no authorization, and every authenticated caller in the fleet can reach it.

The authorization decision names the exact operation. A check that the caller has "some access to this resource type" is not a check that the caller may perform this operation on this object.

## What may be an authorization input

A component's authorization inputs are exactly these, and nothing else:

1. The identity and permission set that a trust boundary verified and projected under a documented contract.
2. The component's own data: ownership, tenant scope, lifecycle state, business invariants.

**Metadata that describes an already-made allow decision is evidence, not authority.** A decision identifier, a decision code, a policy or model version, an allow reason, an allow modifier, a matched rule name, a free-text explanation, a role list, a verified-purpose label - all of it may be logged, traced, and surfaced in a debug view. None of it may appear in a conditional that changes what data is returned, what is written, or which branch executes.

The distinction that matters in practice: a *projected verified credential* that the contract obliges the component to enforce against - a permission set the boundary verified and forwarded - is input 1 above. A *description of a decision the boundary already made* is not, because the component that receives it cannot verify it, cannot know what question it answered, and will be wrong the moment the route's meaning changes. `/alaa-services-contract` owns which named headers fall on which side for this platform; the class rule above binds a service that has never read it.

Flag when a component branches an authorization outcome on a value whose name describes a prior decision; when a value arrives from a public client whose name the boundary is documented to strip; when a component's only authorization is "the gateway let me be called."

## Exact permission, never a role

**A permission is checked, never derived.**

- Enforce the exact permission the route or business operation requires, decoded through the service's committed permission map.
- Never allow, deny, elevate, downgrade, or select an access level from a role name, a role list, or a role-derived tier - and never let a broad role such as `admin` or `owner` short-circuit an exact permission check or a per-object decision. That path is a privilege escalation waiting for one role assignment to be widened, and it is stop-the-line item 3.
- Never use a role to choose a policy, a query, a response field, a route, a validation rule, a feature branch, or a side effect.
- Never treat the presence, absence, order, or freshness of role metadata as an authorization signal.
- Role metadata may be retained as passive observability data, isolated from every authorization interface, where the repository documents that need.

Where the repository already derives a decision from a role, that is contract drift: name the exact decision and the routes it reaches, report it, and migrate it to the exact permission when the migration is in scope. Do not widen it, normalise it, or add a second instance of it during unrelated work.

## Verified once, at one boundary

A credential the trust boundary verified is verified in exactly one place.

- A downstream service does not re-verify it. It lacks the key material and the request context, so its check is either a no-op that reads as a control in review, or a second and weaker implementation that will drift from the first.
- A downstream service does not accept the boundary's verified-metadata form of a credential when it arrives from a public client. The boundary strips those names from client input, so their presence on an inbound public request is a forgery attempt, not a shortcut - stop-the-line item 7.
- A downstream service still enforces its own permission check, tenant scope, ownership, and business rules. "Verified once" applies to the credential, not to authorization.

## Step-up proofs are scoped to their purpose

**A proof obtained for one action does not satisfy the requirement for another.** The purpose is bound to the proof at issue time by the issuer, and the verifier compares the proof's bound purpose against the purpose the route requires.

- Purposes are stable and action-specific. A purpose that is generic (`default`, `admin`, `write`), derived from a route path that can change, or supplied by the client rather than bound at issue, does not scope anything.
- A proof is never renewed, extended, or refreshed without a fresh presentation of the credential. A refresh path for a step-up proof defeats the reason step-up exists.
- Step-up is in addition to permission and business authorization, never instead of it.

## Fail-closed: where to look

`SKILL.md` states the doctrine and the full set of "cannot reach a decision" states. The review's job here is per control: **for each control the change touches, name the code path taken when its dependency is unavailable, and the status the caller receives.** A control whose unavailable-dependency path you cannot find in the code is FAIL / not determined.

The controls this applies to: the authentication middleware; the authorization check, local or remote; tenant and project derivation; step-up verification; the rate limiter and the lockout store; the revocation or session-state check; the permission-map or policy loader; the key or key-set loader; a feature flag that gates any of the above; and an entitlement, licence, or quota check that gates access rather than billing.

## Tenant context derivation

**Tenant context is derived on the server from the verified identity. No request-supplied field participates in that derivation.**

Where the caller must name which tenant or project it is acting in - because it belongs to several - the request-supplied identifier is a **selection among the caller's verified memberships**: the server resolves the caller's membership set from its own store, in the same request, and rejects the request when the named identifier is not in that set. The request field selects; it never grants.

Flag when: a tenant or project identifier from a header, body, query parameter, path segment, or token claim reaches a query predicate without a membership check in the same request; a membership set is resolved once at login and cached where the client can influence it; a membership check exists in one entry point and the same identifier reaches a second entry point that has none.

Every read and write is tenant-scoped in the **query**, by a predicate the data layer applies rather than by a filter applied to results in application code. A result-set filter has already fetched the other tenant's rows, so a logging, caching, count, or error path can still emit them.

## The five places multi-tenant data actually leaks

A tenant predicate on the interactive query is the easy half. These five are where the leaks happen, and each is a separate verdict item.

### 1. Caches

Every cache key contains the tenant identifier, and that component comes from server-derived context. A key built from a resource identifier alone serves tenant A's value to tenant B the moment two tenants share an identifier space.

Flag when: a cache key, memoisation map, or request-scoped singleton is keyed by a resource id, query string, or route path with no tenant component; a process-level structure populated during one tenant's request is read during another's - a package-level variable, a static map, a mutated config object, a connection-attached prepared statement or session variable; a permission or entitlement cache has a TTL longer than the revocation staleness bound stated in `50-credentials-and-cryptography.md`, or is not invalidated when a grant changes.

### 2. Background jobs and queue consumers

A job carries the tenant identifier in its immutable payload, and the consumer re-derives its data scope from that identifier through the same tenant-scoped accessor the request path uses. A consumer never runs as an unscoped superuser on the grounds that it was enqueued correctly.

Flag when: a job queries without a tenant predicate; a job takes tenant context from a thread-local, a global, a container-scoped singleton, or the last request that worker handled; a batch job iterates every tenant inside one transaction and one scoped context; a retry re-derives tenant from a mutable source rather than from the payload; a dead-letter re-drive replays a payload into a different tenant's context; a job's payload carries data instead of identifiers, so a stale payload replays a value the tenant has since had revoked.

### 3. Exports, reports, and bulk endpoints

An export applies the same tenant predicate **and** the same per-row authorization as the interactive endpoint it mirrors, in the query. The generated artifact is stored under a tenant-scoped key and served through an authorization check (`30-outbound-fetch-and-files.md`).

Flag when: an export or report query uses a raw-SQL path that bypasses the scoped repository or the framework's global scope; a "download all" pages with limit and offset over an unscoped base query; an aggregate or count is computed across all tenants and then divided or filtered; a generated file is written to a shared temporary directory under a predictable name; a report is attached to an email or a notification before the recipient's tenant is confirmed to match the data's; a scheduled report reuses a previous run's artifact.

### 4. Search indexes

Tenant is a filter the **server** applies on every query. Either one tenant per index or namespace, or every document carries a tenant field the server sets at index time and filters on at query time. No part of that filter comes from client text.

Flag when: any part of a filter expression comes from client-supplied text; a shared index holds documents with no server-set tenant field; a re-index or backfill writes documents without the tenant field; an autocomplete, suggester, or "more like this" path queries the index without the tenant filter; a facet or aggregate count is computed across the whole index; a highlight or snippet returns text from a document the caller may not read; a deletion in the primary store leaves the document in the index.

### 5. The paths that cross tenants on purpose

Admin views, support tooling, platform metrics, and billing. Each is an explicitly named path with its own exact permission, and it is the **only** way a cross-tenant read happens.

Flag when: a general-purpose repository method exposes an `includeAllTenants`, `withoutGlobalScopes`, or `unscoped` option reachable from a normal route; a support impersonation path does not record who impersonated whom, for what reason, and for how long; a metric or dashboard exposed to tenants carries another tenant's identifier; a cross-tenant path's permission is a role rather than an exact permission.

## Check-then-act, races, and idempotency

A decision followed by a dependent action is atomic, or the action re-asserts the decision's predicate as a condition of its own write. Two requests that interleave between the check and the act must not both succeed.

- **Authorization**: where the authorization predicate is data the same transaction writes - membership, ownership, lifecycle state - the decision and the write are in one transaction, at an isolation level that prevents the predicate changing underneath, or the write carries the predicate in its `WHERE` clause and a zero-row result is treated as a denial.
- **Single-use credentials** - one-time codes, password-reset and invitation tokens, refresh credentials - are consumed by a conditional update that fails on the second attempt (`UPDATE ... SET used_at = now() WHERE id = ? AND used_at IS NULL`), and the caller acts only if one row changed. A `SELECT` followed by an `UPDATE` lets two concurrent presentations both succeed.
- **Quotas, balances, and stock** are decremented by a conditional update or under a row lock taken before the read, never by reading a value, computing, and writing the result.
- **Counters for rate limits and lockouts** are incremented atomically with the expiry set in the same operation. A read, then a decision, then a write, resets to zero under concurrency, which is exactly the condition an attacker creates.
- **Idempotency keys**: the reservation of the key and the effect are atomic, so two concurrent requests carrying the same key perform the effect once. The key is scoped to the tenant and the caller - an unscoped key namespace lets one caller read another's stored response by guessing a key. A replayed key returns the stored response for the original request; it never performs the effect again and never returns a response computed for different parameters.
- **Concurrent refresh** of the same credential is decided explicitly and tested, because the default response to reuse - revoke the family - turns a mobile client's two parallel requests into a forced logout. Whichever behaviour the service chooses, the review finds it stated in code or test rather than inferring it.
- **File handling**: the bytes validated are the bytes stored and served (`30-outbound-fetch-and-files.md`).

## Abuse controls

**Every rate limit has three scopes and all three exist**: per credential or account, per tenant, and per endpoint across the fleet. A limit only on the actor is defeated by creating actors. A limit only on the source address is defeated by a proxy pool and punishes every user behind one NAT. A limit only per tenant lets one member of a tenant exhaust it for the rest.

Endpoints that must be limited, because each one is brute-forceable or amplifying: login, credential refresh, password reset, one-time-code send and verify, step-up verification, invitation and signup, any endpoint that sends an SMS or an email, search, export and bulk read, aggregation and reporting, file upload, and any endpoint that triggers an outbound fetch.

- Ceilings live in configuration, per environment, and are validated at boot (`60-deep-review-and-hardening.md`).
- The limiter store is subject to the fail-closed doctrine: unreachable means the limited endpoint refuses, not that the limit is skipped.
- Credential-guessing endpoints have progressive delay or lockout in addition to a rate limit, and the lockout is keyed so that an attacker cannot use it to lock a victim out at will - the review names how that is prevented.
- A limit's response tells the caller when to retry and does not reveal whether the account exists (`25-browser-trust-and-output.md`).
