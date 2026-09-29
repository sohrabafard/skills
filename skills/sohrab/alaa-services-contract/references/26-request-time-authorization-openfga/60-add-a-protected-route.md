## Adding a new request-time-authorized route

This is the common task. It spans **two repositories**, and the order matters:
prepare the authorization contract first, then expose the route. A route that is
enforced before its permission rule and tuples exist will fail closed for everyone.

In `entitlement-platform` (the model and contract):
1. Confirm the OpenFGA model has the target **type** and the final **`can_*`** relation
   you need. If they are new, add them to the model, upload it, and re-pin
   `OPENFGA_AUTHORIZATION_MODEL_ID` (and bump `OPENFGA_MODEL_LABEL`) for both
   `projector` and `authz-sidecar`.
2. Add the `endpoint_category` + `target_type` -> `final_permission` rule to
   `platform/openfga/contracts/endpoint-permissions.yaml`. The endpoint category name
   must match what the gateway will send.
3. Make sure `projector` writes the grant/deny tuples for that scope type (its
   per-scope managed-relation set) and that `entitlement-api` emits the change events.
   Without tuples, every `can_*` check returns `allowed: false`.

In `gateway` (the route surface):
4. Add an entry to `authzRouteGroups` in `charts/gateway/values.yaml` and every active
   overlay (`docker/values.shared-network.yaml`, the Kubernetes overlay): `name`,
   `enabled: true`, `enforcer: sidecar`, `method`, an anchored `publicPathRegex` that
   captures the resource id, `endpointCategory` (matching step 2), and `identityMode`.
5. For `canonical_from_param`: extend the Lua extractor `extract_public_path_context`
   in `haproxy/lua/authz-sidecar.lua` with a branch for the new route-group name that
   pulls the resource id out of the path. The `captures` field in values is
   documentation; the Lua extractor is what actually reads the id. Forgetting this
   branch is the most common reason a new canonical route fails with
   `AUTHZ_REQUEST_CONTEXT_INVALID`.
6. If the target type is new, add its tag to `RESOURCE_TAGS` in the same Lua file (for
   example `assessment = "asm"`) so the object id can be built.
7. Confirm the trusted headers the sidecar needs are in `authzSidecar.requestHeaderAllowlist`.
8. Validate: render the chart and run the gateway authz smoke harness; verify the
   store/model pins match across `projector` and `authz-sidecar`.

A `comment_service_bundle`-style route skips steps 5-6 but must be a supported
normalization target in the contract.
