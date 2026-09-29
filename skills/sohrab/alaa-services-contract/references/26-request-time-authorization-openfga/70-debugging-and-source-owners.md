## Debugging an authz decision

Work the path in order. The structured logs make this fast because every hop shares
`X-Request-Id` and `traceparent`.

1. **Read the gateway access log** for the request. Check `endpoint_category`,
   `canonical_object_id`, `sidecar_status`, and `sidecar_decision_code`. The decision
   code usually names the problem outright.
2. **`400 AUTHZ_OBJECT_ID_INVALID` / `AUTHZ_REQUEST_CONTEXT_INVALID`:** the gateway
   built a bad or empty object id. Suspect a missing Lua extractor branch (step 5
   above), a wrong `publicPathRegex`, or a missing resource tag. Check
   `canonical_object_id` in the log — empty or malformed confirms it.
3. **`400 AUTHZ_ENDPOINT_CATEGORY_INVALID`:** the gateway's `endpointCategory` does not
   exist in `endpoint-permissions.yaml`. The two repos disagree on the name.
4. **`403 AUTHZ_TARGET_RULE_MISMATCH`:** the category exists but has no rule for that
   target type. Add the target rule to the contract.
5. **`403 AUTHZ_DENIED`:** the contract resolved a `can_*`, but OpenFGA said no. This
   is a write-path question: does the expected `grant_*` tuple exist? Reproduce the
   `check` against OpenFGA (the `entitlement-platform` Postman `openfga-runtime` group
   has ready requests), then `read` the tuples for that user and object. If the tuple
   is missing, look at `projector` (did the event arrive and validate?) and
   `entitlement-api` (was the grant actually created?).
6. **`401 AUTH_CONTEXT_MISSING`:** identity did not reach the sidecar. The JWT/trusted
   header step upstream is the suspect, not authorization.
7. **`503 AUTHZ_*`:** a dependency or pin failure. `STORE_NOT_PINNED` /
   `MODEL_NOT_PINNED` mean env config; `SERVICE_TIMEOUT` / `SERVICE_UNAVAILABLE` mean
   OpenFGA or the sidecar is unreachable. The gateway fails closed here by design.
8. **Allowed but the backend still rejects:** that is backend business authorization,
   not this layer. The allow-side `X-Authz-*` headers are not an authorization input.

Cross-check the sidecar's own `authz decision` log line (`relation`, `object`,
`allowed`, `cache_status`, `authorization_model_id`) and confirm the
`authorization_model_id` matches the model that actually holds your tuples — a stale
pin is a subtle cause of "the tuple exists but the check still denies."

## Anti-patterns

- Calling OpenFGA, `authz-sidecar`, or `entitlement-spoa` directly from a frontend or a
  normal backend. Only the gateway calls the sidecar; only the sidecar checks OpenFGA;
  only `projector` writes tuples.
- Checking a `grant_*` or `deny_*` relation at request time instead of a `can_*`.
- Adding a gateway route group before the permission rule and tuples exist.
- Adding a `canonical_from_param` route group without the Lua extractor branch.
- Treating allow-side `X-Authz-*` headers as authorization input in a backend.
- Letting `projector` and `authz-sidecar` drift onto different model ids.

## Source of truth

- Gateway read path, full diagrams and worked example: gateway repo
  `docs/authz-openfga-flow.md`.
- Write path and reconciliation: gateway repo `docs/entitlement-projector.md`.
- Route groups and Lua: gateway `charts/gateway/values.yaml`,
  `charts/gateway/templates/configmap.yaml`, `haproxy/lua/authz-sidecar.lua`.
- Model, object-id encoding, conditions, endpoint mapping: `entitlement-platform`
  `platform/openfga/contracts/authorization-contract.yaml` and
  `endpoint-permissions.yaml`.
- Runnable OpenFGA `check`/`read`/`write`: `entitlement-platform` Postman collection.
