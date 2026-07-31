# What the gateway verifies, and what enters behind it

Read this file when you are changing gateway verification order, the public-route
list, path-prefix stripping, or the sanitize step; when you need to know where
`X-Project-Id` on a request came from; or when you need to know which route shape
a piece of code is written against.

## Verification order on a protected route

The gateway (HAProxy) applies these checks in this order:

1. A bearer token exists.
2. The JWT `alg` value is on the allow-list. **This runs before verification**, not
   after, because an allow-list applied after the algorithm has already been used
   to select a verifier does not prevent algorithm confusion.
3. The signature is valid for the mounted public key.
4. The token has a usable `exp`.
5. The token is not expired, within the configured clock skew.
6. The token is not before `nbf`, within the configured clock skew.
7. Every required claim is present.
8. Issuer and audience checks run when configured.

Deployment values observed in the current render: allowed algorithm `RS256`, clock
skew 30 seconds, required claims `pid` and `sub`. Issuer and audience validation
exist in the template and are inactive because both lists are empty. Re-derive
these from the gateway repository before relying on them; they are deployment
values, not contract.

## What the gateway does not do

- It does not perform business authorization and does not decide whether a user may
  perform a domain action.
- It does not evaluate `X-Access` or `X-USER-SCOPES` for route permission.
- It does not consume any service's generated permission map and owns no
  permission-name-to-bitmap-id mapping.
- It does not derive tenant from hostname, path prefix, body or query string. A
  service behind it may read a body field or a query parameter on a route that
  admits tokenless requests; that is the service reading, not the gateway deriving,
  and the rule for it is under "Where `X-Project-Id` comes from" below.
- It does not introspect opaque tokens. **If any README or design note still
  describes opaque-token passthrough, or the retired profile-blob header contract,
  that text is drift to remove rather than a compatibility state to preserve.** A
  service built against either will fail closed at the first request, because
  neither is implemented anywhere in the current path.

## Sanitize runs on every route

The gateway deletes every spoofable inbound auth and context header before
proxying, and this step runs on public routes as well as protected ones. A public
route skips token verification; it does not skip sanitizing. Without that, a
public route is a direct channel for a client to hand a backend a chosen
`X-User-Id`.

The delete list covers the whole trusted-header set — the identity, token-metadata,
name and location headers, `X-User-Roles`, and the three backend-only `X-TOTP-*`
names — plus a wildcard sweep of `x-location-*`, `x-authz-*` and `x-totp-*`, which
spares only the public proof carrier `X-TOTP-Proof`. The authoritative list of
names lives with the gateway configuration; the frozen contract-level set is owned
by `alaa-services-contract` `references/30-trusted-ingress-and-laravel-contract.md`.

**Every header the gateway injects also appears in the delete list, and the delete
list runs unconditionally.** A header that is injected but not deleted is forgeable
by any public client, and no amount of service-side care detects the forgery,
because the forged value is byte-identical to a real one. Prose cannot catch this
class of defect — the two lists live hundreds of lines apart in one template.
`scripts/trust_boundary_check.py --gateway-config <path>...` checks the symmetry
mechanically, and a finding there is fixed in the gateway configuration before any
service-side change ships.

## Public routes

The gateway currently treats these paths as public and skips token verification:

- `/auth/api/v3/otp/request`, `/auth/api/v3/otp/verify`, `/auth/api/v3/token/refresh`,
  `/auth/api/v3/logout`
- `/auth/api/ready`, `/auth/api/health`
- `/vod/api/ready`, `/vod/api/health`
- `/comment/api/ready`, `/comment/api/health`
- `/ticket/api/ready`, `/ticket/api/health`
- `/wa/api/ready`
- `/healthz`
- `/wa/ingest/v1/events`

A public path at the gateway is not permission to trust the caller. The service
behind it applies its own route-level rules, and it receives no trusted context to
lean on.

**When a route must always carry an access token, remove it from the public list.**
Do not teach a downstream service to partially trust missing auth context, because
that moves the decision from one auditable list into every service's middleware.

## Where `X-Project-Id` comes from

Maintainer ruling, 2026-07-31. All four cases are settled, and this page is
implementable. The case is fixed by two observables: whether the route requires
authentication, and whether the request carried an access token. When it carried
none, one further observable picks the transport: whether the request has a body.

| Case | Route requires auth | Request carries a token | Where the project id comes from |
|---|---|---|---|
| 1 | yes | yes | the gateway injects `X-Project-Id` from the verified `pid` claim |
| 2 | no | yes | the gateway injects `X-Project-Id` from the verified `pid` claim |
| 3 | no | no, and the request has a body | the request body field `project_id` |
| 4 | no | no, and the request has no body | the query parameter `project_id` |

**Case 2 verifies the token it was given.** A token presented on a route that does
not require authentication runs the same verification order listed above, and a
token failing any step is denied exactly as it would be on a protected route. Read
"the route does not require authentication" as "the route admits a request
carrying no token", never as "a token that arrives is not checked". An
implementation that skips verification because the route is not protected lets a
caller forge `pid` by presenting a malformed token, which is the failure this rule
exists to prevent.

**Cases 3 and 4 are one rule with two transports.** The transport is chosen by
whether there is a body to carry the value, and by nothing else: a GET and a HEAD
have none, so the value travels in the query string. What the route then does with
the value — attribute a write, scope a read — is a separate question, answered by
its own rule below, and it never changes the transport. A POST whose operation is a
read, such as a search that posts its filter, carries the value in the body under
case 3 and is still governed by the read rule.

**No case relaxes anything else on this page.** The delete list still runs
unconditionally, the gateway still injects only from a claim it verified, and a
route admits a tokenless request only because its path is written into the public
list above.

## Cases 3 and 4: a tokenless request carries its own project id

**Ratified by the maintainer on 2026-07-31, both transports. Implement from this
section.** On a route that admits a tokenless request and whose operation must be
attributed or scoped to a project, the project id travels as `project_id`, sourced
from the client's `PROJECT_ID` application configuration: in the request body when
the request has one, and in the query string when it has none. The gateway injects
no header, reads no body and reads no query string on this path. The service the
route proxies to reads that value, and rejects the request when neither channel
carries one.

The body channel is the one the client already uses before authentication: the
pre-auth OTP request and verify calls send `project_id` in the body from that
configuration (`<repo>/src/auth/authEntryAdapter.ts` in the client repository).
Re-derive with `rg -n "project_id" src/auth/authEntryAdapter.ts` in that repository.
The query channel needs no new transport: the SDK already serializes query input at
`<repo>/packages/sdk-core/src/request/query.ts` in the same repository.

**Nothing user-visible changes when the value moves into a query string.** The
parameter is on the SDK's own HTTP call to the gateway, not on the page address the
visitor sees, so no browser URL gains a project id and no page link has to carry
one.

**Scope.** This section says how a guest request carries a project id. It opens no
route to guests; opening one is a gateway change raised under
`<repo>/docs/requests-for-change/` in the gateway repository. A route with no
tenant-scoped operation, such as a health or readiness probe, reads no project id
and requires none.

### Every prohibition in force stays in force, and the ruling confirms them

- The gateway derives tenant from no hostname, no path prefix, no body and no query
  string. On a guest route it reads nothing at all; the service does the reading.
  The query string deserves the same sentence as the body and for a stronger
  reason: HAProxy can read a query parameter trivially and this gateway
  demonstrably does not. No query-string fetch appears anywhere in the template,
  route and rate-limit matching use the `path` fetch, which excludes the query
  string, and prefix stripping uses `set-path`, which leaves the query string
  intact so it reaches the backend unchanged.
- Re-derive that paragraph with
  `rg -n "url_param|urlp|set-pathq|replace-pathq" charts/gateway/templates/configmap.yaml`
  in the gateway repository. A hit on `url_param`, `urlp`, `set-pathq` or
  `replace-pathq` falsifies it, and the prohibition then needs a scope qualifier it
  does not need today.
- The delete list still runs unconditionally, so an `X-Project-Id` presented by a
  client is deleted before proxying on a public route exactly as on a protected one.
- The client still sends no trusted header. `x-project-id` stays in the forbidden
  trusted-header set at `<repo>/packages/sdk-core/src/request/headers.ts`, and the
  WA path enforces that same set at `<repo>/packages/sdk-wa/src/security/headers.ts`,
  both in the client repository.
- `alaa-services-contract references/60-frontend-sdk-consumption-contract.md` carries
  this as the general client rule, not as an OTP special case.
- No component substitutes a configured project id on an HTTP path. That fallback
  stays confined to console and queue execution, per
  `references/30-fail-closed-cases.md` case 3.

### What a client-asserted project id may do, and what it may never do

Any caller reaching the route may name any project, and the service has nothing to
check the value against. It has exactly two permitted uses:

1. **Tenant attribution on an anonymous write** that the route performs.
2. **Scoping an anonymous read** on a route that is on the read list below.

**It authorizes nothing.** It grants no capability, admits no route, and never
widens what a caller may see beyond what the named project already serves
anonymously. A route that would return more than that is not made lawful by being
listed, because it never passes the test below.

Before opening a route that writes, name the row it writes and name who would have
to discount that row after a forged batch. A route whose answer to either is
unknown is not opened.

The observable that tells you which rule you are under: send two requests differing
only in the asserted `project_id` and compare the responses. If any field other than
a correlation identifier differs, the route is scoping output by a client-asserted
value, so the read rule applies and the route must be on the list. If nothing
differs, the route only attributes.

### The read rule: forgeability is not disclosure

The question is not whether the value can be forged — it can — but whether forging
it reveals anything. A project's public feed is already served to anyone who visits
that project's own site with no credential. Asking for it by naming that project
returns the same bytes to the same anonymous caller, so nothing was disclosed. The
reading that says otherwise — the value is forgeable, therefore a client-asserted
tenant read is cross-tenant disclosure — is wrong, and this is its counter-example.
What decides is the response, not the caller.

**The public-surface test.** For everything the route returns to a caller with no
token — every body field, the HTTP status, and any header the route sets — name the
route on that same project's own anonymous public surface that already returns it to
a caller with no token. Anything for which no such route can be named fails, and one
failing item fails the whole route.

- **Passes.** A caller naming another project's id obtains only what that project
  already publishes to anonymous visitors. The route may scope by the
  client-asserted value.
- **Fails.** The route discloses on a value anyone can choose. It needs a verified
  `pid` claim, which means it is not a tokenless route at all and stays off the
  gateway's public list.

Answer the test for every project the route can be asked about, not for one
convenient project. A project that publishes nothing anonymously has no route to
name for any item, including the fact that it exists, so a route that can be asked
about such a project fails.

Three items implementers skip, each of which fails a route on its own:

- **The status code.** A route answering `404` for an unknown project and `200` for
  a known one has returned whether the project exists.
- **Counts and aggregates.** A total, a rank or a member count is an item in its own
  right; the public list it summarizes being public does not make it public.
- **Anything added for the caller's convenience** — an internal id, a debug block,
  an error message naming a resource.

### The read list: explicit routes, never a pattern and never a default

The routes permitted to scope a read by a client-asserted project id are an explicit
list of individual routes. Not a path prefix, not a route group, not a default, and
not a per-handler flag. A route joins the list once it has passed the
public-surface test; a route that is not on the list does not read the value, and
the ingress layer ignores the parameter for it.

A prefix is forbidden because it admits routes that do not exist yet, and the test
is a statement about a response that does not exist yet either.

Keep one list, in one place, read at ingress, for the same reason the public-route
list above is one list: a per-route decision spread through middleware is a decision
nobody can audit.

A Go service on the shared kit already has that list and needs no second copy: the
`Anonymous` route family is it. Every route is registered into exactly one family,
`RouteTable` returns each route with its family, and a route registered outside every
family fails router construction with `ErrUnlabeledRoute`. Passing the
public-surface test is what gates membership of that family, and a service test
comparing the family's rows against the committed list fails the build when a route
joins one without joining the other. The declarations are in
`<repo>/httpkit/router.go` and `<repo>/httpkit/route_inventory.go` of the shared Go
kit repository. Re-derive with
`rg -n "RouteFamilyAnonymous|ErrUnlabeledRoute|func RouteTable" httpkit/` there.

**A listed route can stop qualifying, and nothing else will notice.** Record beside
each entry the artifact that renders the route's anonymous response — the
serializer, resource class or response struct. A change to that artifact re-opens
the test for that route, and an item added there with no counterpart on the
project's public surface takes the route off the list. In review, a diff that
touches a named response artifact and does not touch the list is the defect: the
route answers `200` throughout, so no test and no alert fires.

### Rate and scraping: what a per-project quota cannot do

A forged project id lets one caller pull many projects' public feeds from one place.
That is an abuse and cost question rather than a disclosure one, and it does not
change the verdict above. It does decide the shape of any limit: **a quota keyed on
a client-asserted project id is evaded by editing one query parameter, and it
reports assurance it does not have.** The gateway's own limiter is keyed on the
source address and matches on the path only, so the query parameter neither selects
nor evades it. Re-derive with
`rg -n "stick-table|track-sc0|is_rate_limited_path" charts/gateway/templates/configmap.yaml`
in the gateway repository.

Whether such a route carries a limit at all belongs to `/alaa-reliability-sla`
(`$alaa-reliability-sla`), and the Ala number it carries belongs to
`alaa-services-contract references/22-failure-load-and-deprecation-contract.md`.
Bounding the page a public feed returns as a project's content grows is a complexity
question for `/alaa-algorithms-data-structures`
(`$alaa-algorithms-data-structures`).

### Precedence: a verified claim wins, and the asserted value is not read

A service reads the body field or the query parameter only on the branch where no
trusted `X-Project-Id` is present. On the branch where the header is present neither
is read, so there is no comparison to make and none is added. A service that prefers
the client-asserted value on a request that also carried a valid token has built a
privilege escalation, and it is worse on a read than on a write: a write attributed
to the wrong project is a row somebody can find and discount, while a read scoped to
the wrong project hands one tenant another tenant's response and leaves nothing
behind to find.

Comparing the two and denying on mismatch is wrong as well, and it fails
differently: a client build whose `PROJECT_ID` lags a tenant migration would have
every authenticated request denied over a value the service was never going to use.
Ignore the field on that branch instead.

This creates no exception to the client-selector rule in
`references/40-downstream-normalization.md`. A field the route reads to choose scope
while trusted context is present is a selector, and a selector disagreeing with
trusted context still denies with `TENANT_CONTEXT_INVALID`. The tokenless
`project_id` is not read on that branch, which is exactly what keeps it from being a
selector.

**A cache in front of such a route keys on the effective project, not on the URL.**
Because the token branch ignores the query parameter, one URL returns different
bytes to different callers, and a cache keyed on the URL alone serves one tenant's
response to another. The gateway renders no cache of its own today, so this binds
whatever cache is introduced next, at the gateway or at a CDN. Re-derive with
`rg -n "cache-use|filter cache" charts/gateway/templates/` in the gateway
repository; it returns nothing today.

### Rejecting a guest request that carries no project id

The service returns `400` with `TENANT_CONTEXT_MISSING` — the same code an absent
trusted header produces, because the observable is the same: the operation has no
tenant and cannot be attributed or scoped. Do not mint a second code for this case,
and do not substitute a default.

Read exactly one channel per request: the body when the request has a body, the
query string when it has none. A service that reads both and takes whichever is
present has two sources for one value on one request, and a caller can then make
them disagree.

A present value gets no shortcut because it arrived on a guest route. Validate it as
UUIDv7 and resolve it through the same public `project_id` path as any other public
input. That path, the header name, its value form, and the provenance statement a
downstream service may rely on are owned by `/alaa-services-contract`
(`$alaa-services-contract`) in
`alaa-services-contract references/30-trusted-ingress-and-laravel-contract.md`, with
the canonical public form in
`alaa-services-contract references/25-end-to-end-flow-and-boundaries.md`.

### What the gateway log cannot tell you about a guest request

The gateway's structured log takes its project id from the verified claim only, and
records the request URI without its query string. A tokenless request therefore
appears in the gateway log with an empty project id and no `project_id` parameter,
whichever transport it used. Attributing guest traffic to a project is possible only
from the receiving service's own logs, so a service serving tokenless tenant-scoped
routes emits that attribution itself. Re-derive with
`rg -n "jwt_claim_pid|http.path" charts/gateway/templates/configmap.yaml` in the
gateway repository.

The field name and its value form are owned by `/alaa-services-contract`
(`$alaa-services-contract`); whether the emission is required, and at what level,
is owned by `/alaa-observability-soc` (`$alaa-observability-soc`).

## Gateway-facing routes versus service-local routes

This distinction is mandatory, and getting it wrong produces a service whose
documented routes do not exist.

- A client calls the gateway-facing route, which carries the service prefix the
  gateway routes on: `/auth`, `/vod`, `/comment`, `/ticket`, `/wa`.
- When `stripPathPrefix: true`, the gateway removes that prefix before proxying.
- The backend therefore implements and documents the **service-local** shape.

Gateway-facing `/auth/api/v3/otp/request` is service-local `/api/v3/otp/request`.
Gateway-facing `/auth/api/health` is service-local `/api/health`.

Write gateway-facing routes when the subject is the gateway. Write service-local
routes when the subject is a backend. A backend carries the gateway prefix in its
own route definitions only when the gateway's routing configuration for that
service sets `stripPathPrefix: false`; read that value before writing either
shape, because guessing produces routes that answer 404 in one environment and
work in another.

## The tenant boundary and its names

`tenant_id`, `tenant_public_id`, `project_id` and the compact claim `pid` are one
concept expressed at four layers. The canonical form per layer is fixed:

| Layer | Canonical name |
|---|---|
| Compact JWT claim | `pid` |
| Public API field | `project_id` |
| Trusted header | `X-Project-Id` |

Rename `tenant_id` and `tenant_public_id` to `project_id` at public API and
service-domain boundaries, and to `pid` only inside compact JWT claim mapping.
Rename `X-Tenant-Public-Id` to `X-Project-Id`. Keep trust semantics unchanged
while renaming: a rename that also changes who may assert the value is not a
rename.

Validate the public boundary value as UUIDv7 after gateway verification. Example:
`018f7d8f-8cb0-7a85-9a89-e3f61052f840`.

A service that still keeps an internal numeric project key translates the trusted
public boundary into that key at ingress and keeps the numeric key out of trusted
headers, public API examples and every other public-facing contract. The numeric
key is service-local storage, not the boundary.

Where a legacy alias still appears in OpenAPI, a README or a service doc, mark it
explicitly as legacy and equivalent to the public boundary rather than documenting
it as a second concept.

## Auth-service route drift that must not be copied forward

Auth-service is `v3` only and exposes no `/api/v2` routes. Any gateway or repository
document still naming `/auth/api/v2/*` is drift to remove, not active client
guidance. Do not reintroduce `/api/v2`, and do not teach a new service or caller to
depend on a retired auth v2 route or a one-step `/login` path.

Route families and the current client flow are in
`references/60-auth-service-v3-contract.md`.
