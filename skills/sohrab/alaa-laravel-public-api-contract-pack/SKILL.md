---
name: alaa-laravel-public-api-contract-pack
description: "Build and audit a Laravel service's public API contract pack from executable repository truth: route inventory, versioning and breaking-change classification, per-route write and retry semantics, pagination and limits, OpenAPI, Postman and TypeScript SDK input docs, and a gate that refuses to emit a pack while a route's version, deprecation, or sunset date is unresolved. Use when a public API surface must be documented, versioned, pinned, or reconciled with drifted docs, and when separating public client input from trusted gateway headers. Do not use to decide fleet contract values: envelopes, header names, identifiers, deprecation windows and platform numbers belong to /alaa-services-contract; pagination mechanism to /alaa-keyset-pagination; collection generation to /alaa-postman-collections; trust semantics to /alaa-trust-gateway-auth; Laravel code changes to /alaa-laravel-architecture."
---

# Laravel Public API Contract Pack

Build a public client API contract pack from executable repository truth. An SDK or frontend engineer
can then implement transport, types, errors, pagination, retries and versioning without reading backend
source, and a caller that this service cannot deploy in lockstep with can pin what it built against.

The work is docs-only. Change no application code, test or runtime behaviour unless the user
explicitly expands scope. When a change outside docs is needed, report it as out of scope instead of making it.

## When this applies

Apply this skill when any of these holds:

- A public API contract pack is requested for a Laravel service.
- The output feeds a TypeScript SDK, a frontend, Postman, Insomnia or an OpenAPI consumer.
- Committed artifacts may have drifted from the routes.
- A public route changes.
- Public input must be separated from trusted input.

Not this skill: implementing backend behaviour (`/alaa-laravel-architecture`); a narrow Postman edit (`/alaa-postman-collections`); what a trusted header means (`/alaa-trust-gateway-auth`).

## The emission gate

**Trigger:** any file of the pack is about to be created or updated.

**Refusal condition:** any route in the inventory whose API version, deprecation status, or —
when deprecated — sunset date cannot be established from a cited repository artifact or a cited
entry in the owning reference file of `alaa-services-contract` (`/alaa-services-contract`).

**Instead:** write no file of the pack. For each unresolved route, report its method, its path, which
of the three fields is unresolved, and the one named artifact or owner decision that resolves it.
Then stop and ask.

**Not satisfiable by** a marker, placeholder, empty string, `null`, `TBD`, or omitted field in
those three; by emitting only the artifacts whose routes resolved; by writing to a draft path; or
by recording the gap in a backlog and proceeding. The markers below cover consumer-facing values
the repository does not fix; in these three fields a marker is a refusal to emit.

**Resolving it is ordinary work.** A route is `deprecated: false` when neither the repository nor
the owning reference file records a deprecation for that surface. That absence is something you check and cite.
`deprecated: true` needs the announcement and removal dates that `/alaa-services-contract` already recorded.
Copy those dates; never compute them.

**Observable:** `python3 scripts/contract_pack_audit.py --routes <inventory.json> --openapi
<pack>/openapi.yaml --postman <collection.json> --meta <pack>/contract.meta.json` exits `0`.
Exit `5` means the pack may not be emitted; `--help` holds the exit table and its obligations.

## Workflow

1. **Choose the target path** by the first rule that applies, and record it in `contract.meta.json` in
   the same change: `contract_root` from an existing `contract.meta.json`; else the path the user named;
   else `docs/contracts/<service>`, using the canonical service identity that
   `alaa-services-contract references/10-core-service-contract.md` owns.
2. **Read** the repo-local `AGENTS.md`, existing contract docs, route files, public API tests,
   committed OpenAPI and Postman artifacts, and any repo-native audit command.
3. **Capture the inventory to a file** with `php artisan route:list --json`. Everything downstream
   compares against that file. If the command cannot run, the inventory is unresolved and the
   gate refuses. A hand-assembled list is not an inventory.
4. **Classify each route's family** as public, trusted internal or operational. Document only
   what the public family promises.
5. **Extract the public-versus-trusted boundary** by the method below.
6. **Answer the per-route questions** that the references own: version and change class, write and
   retry semantics, and pagination and limits.
7. **Emit** endpoint docs, OpenAPI and SDK input notes from verified behavior. Invoke
   `/alaa-postman-collections` to generate or align the collection and environment from that same
   contract. All of these remain required pack deliverables. Generate each shared statement once.
8. **Validate against the floor** in `references/40-consumer-discovery-pinning-and-secret-hygiene.md`,
   and report each command with its result.

## Source priority, as a constraint

A lower rank never overrides a higher one, and a claim resting only on rank 4 or below is not a
contract claim.

1. the captured route inventory
2. passing public API tests and repo-native audit commands
3. route, controller, FormRequest, Resource, middleware and policy source
4. committed OpenAPI and Postman artifacts
5. committed docs and comments
6. memory or a prior run

**Conflict across ranks:** the higher rank becomes the contract. Put the lower source in the
pack's drift list with its path and its competing claim. **Conflict within one rank** (two
tests, two controllers or two middleware paths that disagree): do not resolve it by choosing. Record
both readings and treat the route as unresolved for the gate.

**Promoting prose:** a doc claim becomes a contract claim only when a rank 1 to 3 source states the
same thing at the same specificity. A field's type needs the FormRequest rule or Resource cast
producing it; a status needs the return statement or a passing test asserting it. A controller
that mentions a field does not support a claim about its type.

## The two uncertainty markers

`NEEDS_BACKEND_CONFIRMATION` needs both of these conditions:

1. A cited repository artifact proves the surface exists and runs: a route declaration, a registered
   middleware, a config key that is read, or a passing test.
2. The same repository does not fix the value or shape a consumer needs.

The entry names the artifact, records that citation, and records the exact question a backend or
gateway owner must answer. Without a citation, write no marker.

`not_implemented` is a requested or previously documented surface with no route, controller, or
passing test. Emit no request shape, response shape, or example for it.

Every marker appears in `contract.meta.json`'s `uncertainty_list` and beside the claim it
qualifies. The recurring three — gateway-facing base path, cookie and session policy, published
rate-limit quota — are marked this way or resolved; a prose aside does not discharge them.

## Extracting the public-versus-trusted boundary

The method is this skill's; header names, identifier forms, and trust semantics are not.

1. Take each route's middleware stack from the captured inventory, not from `bootstrap/app.php`
   or a group alias, because an alias hides what runs.
2. List every header, cookie, and request attribute the handler reads: context-resolving
   middleware, FormRequest rules, and every `$request->header(...)` and
   `->attributes->get(...)` call site on the path.
3. Split that list per value and per route into **public input** the client sends,
   **trusted-injected** values the gateway sets after verification, and **forbidden input** the
   service reads that a client could set but must not.
4. State what a public client sends for identity: the credential the gateway accepts on that
   route, with its refresh behaviour. Read it from the gateway repository's route table and the
   service's auth middleware. Never document a trusted header as client input in any example. Label
   a local-testing recipe that needs one as backend-only local testing, in its own section.
5. Per forbidden-input value, document the status the service returns when a client sets it,
   proven by a middleware line or a test.

**Observable:** every value any handler reads appears in exactly one of the three lists and none
in two. A value in no list is unresolved.

The upstream `laravel-best-practices/rules/architecture.md` shipped with a service repository
teaches taking tenant identity from a client header. That repository does not own this ground and
the example is wrong here: never document a client-set header as tenant or user identity.

## Which reference to read

| You are about to | Read |
|---|---|
| add, remove, or rename a route, change a request or response shape, or decide what a version bump means | `references/10-versioning-and-breaking-change-classification.md` |
| document a route that is not a read, or answer whether a consumer may repeat a request | `references/20-write-semantics-and-idempotency.md` |
| document a route returning a collection, or a request field accepting more than one value | `references/30-pagination-and-limits-for-consumers.md` |
| create a pack, bump its version, write any pack file to disk, or validate one — this file holds the deliverables floor and the validation floor | `references/40-consumer-discovery-pinning-and-secret-hygiene.md` |
| state a rule, make a decision or edit code on ground this skill does not own | `references/50-ownership-boundary.md` |

## When NOT to use

- The task is to decide a fleet contract value rather than to document one: an envelope shape, a header
  name, an identifier format, a deprecation window, or any platform number.
- The API has no external client and no contract to emit, pin, or reconcile.
- The change is Laravel code with no effect on any route's public shape, version, deprecation status, or
  sunset date.
- The task is generating a Postman collection, or choosing the pagination mechanism itself.
  `references/50-ownership-boundary.md` names each owner.

## Ownership boundary

Cross-skill calls follow the single `/name` convention in the [pack instructions](../AGENTS.md).
Where this skill and an owner could state one rule, the owner states it and this skill points.
On conflict the owner wins. Before you state a rule, make a decision or edit code on ground this skill does not own, read
`references/50-ownership-boundary.md`; it names the owner for each concern.

Owned here and stated nowhere else: the pack's file set and `contract.meta.json` shape; the
emission gate; the source-priority ladder and its conflict rule; the boundary extraction method;
the per-route version, retry-safety and pagination-mode statements in the emitted artifacts; the
pack's secret-provenance and pre-emission scan rules; and `scripts/contract_pack_audit.py`.
