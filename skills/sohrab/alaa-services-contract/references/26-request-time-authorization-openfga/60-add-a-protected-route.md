## Adding a new request-time-authorized route

Prepare contracts before exposing the route; enforcement before its permission
rule and tuples exist fails closed for everyone.

In `authz-openfga` (canonical model and contracts):
1. Confirm the target **type** and final **`can_*`** relation exist. For new ones,
   add/upload the model, re-pin `OPENFGA_AUTHORIZATION_MODEL_ID` and bump
   `OPENFGA_MODEL_LABEL` for both `projector` and `authz-sidecar`.
2. Add the `endpoint_category` + `target_type` -> `final_permission` rule to
   `<repo>/platform/openfga/contracts/endpoint-permissions.yaml`; the category must
   match the gateway.

In `entitlement-api` and `entitlement-projector`:
3. Ensure the API emits change events and the projector writes that scope type's
   grant/deny tuples (its per-scope managed-relation set). Without tuples, every
   `can_*` check returns `allowed: false`.

`entitlement-api`, `entitlement-projector`, `authz-sidecar`: import reviewed bundles;
verify canonical equality/shared pins before exposure. API runtime model SHA must
match its validated manifest; follow `<repo>/docs/contracts/importer-provenance.md`
migration/admission gates. Compatible consumer versions may differ.

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
