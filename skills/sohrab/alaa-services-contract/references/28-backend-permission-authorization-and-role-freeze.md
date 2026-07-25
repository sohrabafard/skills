# Backend Permission Authorization And Role Freeze

Use this file whenever an Ala backend task touches authorization, access levels, policies, Gates, middleware, trusted `X-Access`, trusted `X-User-Roles`, the compact `prm` or `rol` claims, or user-role storage.

## Current decision

User-role semantics are not finalized for backend decision-making. Until this skill explicitly replaces this section with a finalized role contract, every Ala backend service must treat user roles as non-authoritative metadata.

For backend decision semantics, this file takes precedence over older companion-skill examples that derive a service-local role or permission tier. Companion skills still own claim verification, trusted-header projection, and parsing details, but those details do not authorize new role-derived backend behavior.

Backend services must:
- enforce coarse service access with catalog-owned permission bits received through the gateway-trusted `X-Access` projection of verified `prm`
- decode `X-Access` through the service's generated, committed permission map from `alaa-permission-catalog`
- check the exact permission required by the route or business operation
- continue to rely on the contract-defined gateway/OpenFGA path for resource-level authorization where that path applies
- keep business invariants, tenant/project boundaries, ownership checks, and data-scope rules explicit after trusted-context normalization

Observable that decides compliance: in a service that makes any backend authorization decision, an
executable read of `X-Access` exists at ingress, and the request is denied when the header is absent or
decodes to zero known permissions. A repository where a search for `X-Access` returns documentation, a
contract file, or a permissions guide but no executable read, while its routes still allow and deny, is
deciding access from something else — a role name, a framework guard, a local table — and is non-conforming
even when every route currently returns the answer an operator expects. A service that makes no
authorization decision at all, such as a pure ingest pipeline, records that in its own `AGENTS.md`, and this
rule does not apply to it.

Backend services must not:
- allow, deny, elevate, downgrade, or select an access level from `rol`, `X-User-Roles`, a role name, or a role-derived tier
- use roles to choose policies, Gates, scopes, queries, response fields, routes, validation, feature behavior, workflow branches, or side effects
- add new role resolvers, role-to-permission maps, role-derived permission fallbacks, role middleware, or role-based tests
- infer permissions from a role or use a broad role such as `admin` to bypass an exact permission or OpenFGA decision
- treat the presence, absence, order, or freshness of role metadata as an authorization signal

## Allowed passive role handling

A backend is not required to consume or store `X-User-Roles`. If a service already receives role metadata, or has an explicit observability or future-migration need, it may retain the normalized role snapshot only as passive metadata.

Passive handling means:
- accept role data only from the sanitized gateway path; never from public client input
- preserve the normalized bounded array without deriving an authorization tier or permission set from it
- keep absence or staleness from changing request outcomes
- keep the data request-scoped by default; persist an immutable snapshot only when the service has a documented observability or future-migration purpose
- apply the platform's privacy, retention, and redaction rules
- do not place user ids or role arrays in metric labels; use bounded structured logs or trace attributes only when operationally justified

Code added solely for passive role capture must remain isolated from authorization interfaces so a future role contract can activate or remove it without changing current access behavior.

## Existing role-dependent code

Do not silently expand or normalize legacy role-based behavior during unrelated work. When current repository code already uses roles for a backend decision:
- identify the exact decision and affected routes
- treat it as contract drift
- migrate it to exact catalog-owned permissions and applicable OpenFGA checks when that migration is in scope
- otherwise preserve behavior only as an explicit blocker and do not add new role-dependent paths

## Activation gate

Role-based backend behavior remains frozen until this skill explicitly records all of the following as finalized:
- authoritative role ownership and lifecycle
- exact role semantics and allowed backend use cases
- precedence between roles, permission bits, and OpenFGA decisions
- freshness, refresh, revocation, and compatibility behavior
- service rollout and migration rules
- required tests, observability, privacy, and failure semantics

The existence of `rol`, `X-User-Roles`, stored role snapshots, frontend role hints, or documentation outside this explicit gate does not activate role-based backend decision-making.
