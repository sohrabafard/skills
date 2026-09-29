# Request-Time Authorization With OpenFGA

Use this file when the task touches fine-grained, per-resource authorization: a
route that must answer "may *this* user act on *this* object?" before the backend
runs. This is the layer that sits on top of gateway authentication. `25-end-to-end-flow-and-boundaries.md`
explains *who owns what*; this file explains *how the request-time decision is
actually made*, what data crosses each hop, how to add a new protected route, and
how to debug one.

Pair with `/alaa-trust-gateway-auth` for the trusted-header boundary, `/alaa-haproxy`
when the gateway route config or Lua is in scope, and `/openfga` when the model or
tuples are in scope.

## Why this layer exists

When distinguishing gateway identity from a resource permission, read [Model and tuple flow](./26-request-time-authorization-openfga/10-model-and-tuple-flow.md) for the writer/reader seam and grant-to-permission rule.

## The two paths (and the single seam)

When tracing whether a grant reached the decision graph, read [Model and tuple flow](./26-request-time-authorization-openfga/10-model-and-tuple-flow.md) for event projection and read-only sidecar ownership.

## Read path, hop by hop (the contract)

The worked example throughout is `GET /vod/api/v3/course/12/set/55/content/901` for
user `91`. The gateway repo's `docs/authz-openfga-flow.md` holds the full diagrams;
the exact wire contract is below.

The request is decided in the ordered hops below. Load each hop that you are reviewing; use all five when validating an end-to-end decision.

### 1. Gateway matches a route group

When reviewing this hop, read [the matching decision contract](./26-request-time-authorization-openfga/20-gateway-route-and-object-id.md) for its inputs, transformation, and output.

### 2. Gateway builds the canonical object id (Lua)

When reviewing this hop, read [the matching decision contract](./26-request-time-authorization-openfga/20-gateway-route-and-object-id.md) for its inputs, transformation, and output.

### 3. Gateway -> authz-sidecar

When reviewing this hop, read [the matching decision contract](./26-request-time-authorization-openfga/30-sidecar-and-openfga-check.md) for its inputs, transformation, and output.

### 4. authz-sidecar -> OpenFGA

When reviewing this hop, read [the matching decision contract](./26-request-time-authorization-openfga/30-sidecar-and-openfga-check.md) for its inputs, transformation, and output.

### 5. Decision back to the gateway, then enforcement

When reviewing this hop, read [the matching decision contract](./26-request-time-authorization-openfga/40-decision-and-enforcement.md) for its inputs, transformation, and output.

## Endpoint category -> permission mapping

When mapping endpoint categories or coordinating model/store rollout, read [Permission mapping and pins](./26-request-time-authorization-openfga/50-permission-mapping-and-pins.md) for the canonical relation map and shared identifiers.

## The store, the model, and pinning

Before changing a model or store pin, read [Permission mapping and pins](./26-request-time-authorization-openfga/50-permission-mapping-and-pins.md) for the shared writer/reader version rule.

## Adding a new request-time-authorized route

When adding a protected route, follow [Add a protected route](./26-request-time-authorization-openfga/60-add-a-protected-route.md) for the cross-repository order and validation steps.

## Debugging an authz decision

When diagnosing an authz decision, read [Debugging and source owners](./26-request-time-authorization-openfga/70-debugging-and-source-owners.md) for hop-ordered diagnosis and source ownership.

## Anti-patterns

When reviewing prohibited call paths or trust boundaries, read [Debugging and source owners](./26-request-time-authorization-openfga/70-debugging-and-source-owners.md) for the anti-patterns and canonical owners.

## Source of truth

When locating implementation evidence, read [Debugging and source owners](./26-request-time-authorization-openfga/70-debugging-and-source-owners.md) for repository source paths.
