---
name: alaa-laravel-public-api-contract-pack
description: "Build and audit a Laravel service's public client API contract pack from executable repository truth: route inventory, versioning and breaking-change classification, per-route write and retry semantics, consumer-visible pagination and limits, OpenAPI plus Postman plus TypeScript SDK input docs, and a gate that refuses to emit a pack while any route's version, deprecation status, or sunset date is unresolved. Use when a Laravel public API surface must be documented, versioned, pinned, or reconciled with drifted docs, and when separating public client input from trusted gateway headers. Do not use to decide fleet contract values: envelopes, header names, identifiers, deprecation windows and every platform number belong to /alaa-services-contract ($alaa-services-contract); pagination mechanism to /alaa-keyset-pagination; collection and environment generation to /alaa-postman-collections; trust semantics to /alaa-trust-gateway-auth; Laravel code changes to /alaa-laravel-architecture."
---

# Laravel Public API Contract Pack

Build a public client API contract pack from executable repository truth, so an SDK or frontend
engineer implements transport, types, errors, pagination, retries and versioning without reading
backend source, and so a caller this service cannot deploy in lockstep with can pin what it
built against.

The work is docs-only: no application code, test, or runtime behaviour changes unless the user
explicitly expands scope, and the skill says so rather than doing it.

## When this applies

A public API contract pack is requested for a Laravel service; the output feeds a TypeScript
SDK, a frontend, Postman, Insomnia, or an OpenAPI consumer; committed artifacts may have drifted
from routes; a public route changes; or public input must be separated from trusted input.

Not this skill: implementing backend behaviour (`/alaa-laravel-architecture`,
`$alaa-laravel-architecture`); a narrow Postman edit (`/alaa-postman-collections`,
`$alaa-postman-collections`); what a trusted header means (`/alaa-trust-gateway-auth`,
`$alaa-trust-gateway-auth`).

## The emission gate

**Trigger:** any file of the pack is about to be created or updated.

**Refusal condition:** any route in the inventory whose API version, deprecation status, or —
when deprecated — sunset date cannot be established from a cited repository artifact or a cited
entry in the owning reference file of `alaa-services-contract` (`/alaa-services-contract`,
`$alaa-services-contract`).

**Instead:** write no file of the pack. Report per unresolved route its method, its path, which
of the three fields is unresolved, and the one named artifact or owner decision that resolves it.
Then stop and ask.

**Not satisfiable by** a marker, placeholder, empty string, `null`, `TBD`, or omitted field in
those three; by emitting only the artifacts whose routes resolved; by writing to a draft path; or
by recording the gap in a backlog and proceeding. The markers below cover consumer-facing values
the repository does not fix; in these three fields a marker is a refusal to emit.

**Resolving it is ordinary work:** a route is `deprecated: false` when neither the repository nor
the owning reference file records a deprecation for that surface — an absence you check and cite.
`deprecated: true` needs the announcement and removal dates that skill already recorded, copied,
never computed.

**Observable:** `python3 scripts/contract_pack_audit.py --routes <inventory.json> --openapi
<pack>/openapi.yaml --postman <collection.json> --meta <pack>/contract.meta.json` exits `0`.
Exit `5` means the pack may not be emitted; `--help` holds the exit table and its obligations.

## Workflow

1. **Target path**, in order, recorded in `contract.meta.json` in the same change: `contract_root`
   from an existing `contract.meta.json`; else the path the user named; else
   `docs/contracts/<service>` using the canonical service identity owned by
   `alaa-services-contract references/10-core-service-contract.md`.
2. **Read** repo-local `AGENTS.md`, existing contract docs, route files, public API tests,
   committed OpenAPI and Postman artifacts, and any repo-native audit command.
3. **Capture the inventory to a file**: `php artisan route:list --json`. Everything downstream
   compares against that file. If the command cannot run, the inventory is unresolved and the
   gate refuses; a hand-assembled list is not an inventory.
4. **Classify each route's family** — public, trusted internal, operational — and document only
   what the public family promises.
5. **Extract the public-versus-trusted boundary** by the method below.
6. **Answer the per-route questions** the references own: version and change class, write and
   retry semantics, pagination and limits.
7. **Emit** endpoint docs, OpenAPI, Postman collection and environment, and SDK input notes as
   projections of one verified behaviour. A statement in two artifacts is generated once.
8. **Validate against the floor** in `references/40-consumer-discovery-pinning-and-secret-hygiene.md`
   and report each command with its result.

## Source priority, as a constraint

A lower rank never overrides a higher one, and a claim resting only on rank 4 or below is not a
contract claim.

1. the captured route inventory
2. passing public API tests and repo-native audit commands
3. route, controller, FormRequest, Resource, middleware, policy source
4. committed OpenAPI and Postman artifacts
5. committed docs and comments
6. memory or a prior run

**Conflict across ranks:** the higher rank becomes the contract; the lower source goes in the
pack's drift list with its path and its competing claim. **Conflict within one rank** — two
tests, two controllers, two middleware paths disagreeing — is not resolved by choosing: record
both readings and treat the route as unresolved for the gate.

**Promoting prose:** a doc claim becomes a contract claim only when a rank 1-3 source states the
same thing at the same specificity. A field's type needs the FormRequest rule or Resource cast
producing it; a status needs the return statement or a passing test asserting it. A controller
that mentions a field does not support a claim about its type.

## The two uncertainty markers

`NEEDS_BACKEND_CONFIRMATION` needs both, and its entry names the artifact: a cited repository
artifact proves the surface exists and runs — a route declaration, a registered middleware, a
config key that is read, a passing test — **and** the same repository does not fix the value or
shape a consumer needs. The entry records that citation and the exact question a backend or
gateway owner must answer. No citation, no marker.

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
   route, read from the gateway repository's route table and the service's auth middleware, with
   its refresh behaviour. A trusted header is never documented as client input in any example; a
   local-testing recipe needing one is labelled backend-only local testing in its own section.
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

## Ownership boundary

`/name` for Claude Code, `$name` for Codex. Where this skill and an owner could state one rule,
the owner states it and this skill points; on conflict the owner wins.

| Not owned here | Owner |
|---|---|
| Envelopes, health and readiness shapes, trusted header names, public identifier forms, event and code names, deprecation windows, and every platform number — timeout, retry count, pool bound | `/alaa-services-contract` (`$alaa-services-contract`) |
| Why a caller retries; budgets, backoff, breakers, degradation, error budgets | `/alaa-reliability-sla` (`$alaa-reliability-sla`) |
| Pagination mechanism: ordering, index, predicate, cursor codec, page-size bound, reversal tests | `/alaa-keyset-pagination` (`$alaa-keyset-pagination`) |
| Complexity budgets, structure choice, the N+1 family, unbounded result sets | `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) |
| Collection and environment generation, saved-example and error-coverage completeness, Insomnia portability | `/alaa-postman-collections` (`$alaa-postman-collections`) |
| Gateway trust boundary, JWT verification, header sanitisation, tenant derivation | `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) |
| Object-level relationship authorization | `/openfga` (`$openfga`) |
| Threat classes, review triggers, the fail-closed discriminator | `/alaa-security-review` (`$alaa-security-review`) |
| What makes a test a test, which layer it belongs at, proof levels | `/alaa-testing-strategy` (`$alaa-testing-strategy`) |
| Observability names | `/alaa-services-contract`; requirement levels and gates `/alaa-observability-soc` (`$alaa-observability-soc`) |
| Laravel structure, PHP naming, design-pattern selection | `/alaa-laravel-architecture` (`$alaa-laravel-architecture`), `/alaa-php-clean-code` (`$alaa-php-clean-code`) and its `references/design-patterns.md` |
| Pre-implementation design once a scope expansion changes an interface, a writer, or what a caller sees when a dependency fails | `/alaa-system-design` (`$alaa-system-design`) |
| Multi-file runs and durable handoff; risky operations and proof strength | `/alaa-workflow` (`$alaa-workflow`), `/alaa-controlled-ops` (`$alaa-controlled-ops`) |
| Lane planning and subagent roles; model and reasoning-effort choice | `/alaa-cc-orchestrator` (`$alaa-codex-orchestrator`), `/alaa-prompting-guide` (`$alaa-prompting-guide`) |
| The ten-criterion quality bar; Farsi docs and backlog wording | `alaa-project-constitution references/quality-bar.md`, `/alaa-repo-docs` (`$alaa-repo-docs`) |

Owned here and stated nowhere else: the pack's file set and `contract.meta.json` shape; the
emission gate; the source-priority ladder and its conflict rule; the boundary extraction method;
the per-route version, retry-safety and pagination-mode statements in the emitted artifacts; the
pack's secret-provenance and pre-emission scan rules; and `scripts/contract_pack_audit.py`.
