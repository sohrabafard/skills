# Request-Time Authorization With OpenFGA

Use this file when the task touches fine-grained, per-resource authorization: a
route that must answer "may *this* user act on *this* object?" before the backend
runs. This is the layer that sits on top of gateway authentication. `25-end-to-end-flow-and-boundaries.md`
explains *who owns what*; this file explains *how the request-time decision is
actually made*, what data crosses each hop, how to add a new protected route, and
how to debug one.

Pair with `$alaa-trust-gateway-auth` for the trusted-header boundary, `$alaa-haproxy`
when the gateway route config or Lua is in scope, and `$openfga` when the model or
tuples are in scope.

## Why this layer exists

Authentication answers "who is this user?" The compact JWT and the gateway's
trusted headers (`X-User-Id`, `X-Project-Id`, `X-Access`) settle identity. They do
not answer "is this user allowed to open course 12, set 55, content 901?" That is a
relationship between a user and a specific object, and it changes constantly as
people buy, get granted, or get denied access. Encoding that in a token would make
tokens huge and stale. So the platform keeps it in OpenFGA and asks at request time.

The decision is **fail-closed**: if the answer is "no" or the decision cannot be
reached, the backend is never called.

## The two paths (and the single seam)

OpenFGA is the seam between a write path and a read path. Understand both, because a
bug is almost always "the tuple was never written" (write path) or "the route asked
the wrong question" (read path).

- **Write path (truth -> graph):** `entitlement-api` owns business truth (who was
  granted or denied what). On every change it emits an event. `projector` consumes
  the event and writes or deletes the matching OpenFGA tuples. `projector` is the
  **only** tuple writer.
- **Read path (request -> decision):** the gateway authenticates, builds a canonical
  object id, and asks `authz-sidecar` (or `entitlement-spoa`). The sidecar resolves
  the route to a final `can_*` permission and runs one OpenFGA `check`. The sidecar
  is **read-only**.

```
entitlement-api --event--> projector --write tuples--> OpenFGA
                                                          ^
gateway --HEAD /internal/authz/check--> authz-sidecar --check--+
```

Grant vs permission, the easiest thing to misread:
- `projector` writes **grant**/**deny** relations: `grant_view`, `deny_access`, ...
- the OpenFGA **model** derives the final **`can_*`** permissions from those, applying
  inheritance (a course grant reaches its sets and contents) and deny precedence.
- the sidecar always checks a final **`can_*`** relation, never a raw grant.

So a "view" purchase on content 901 is stored as a `grant_view` tuple, and a later
`can_view` check passes because the model resolves `can_view` from `grant_view`
unless a deny overrides it.

## Read path, hop by hop (the contract)

The worked example throughout is `GET /vod/api/v3/course/12/set/55/content/901` for
user `91`. The gateway repo's `docs/authz-openfga-flow.md` holds the full diagrams;
the exact wire contract is below.

### 1. Gateway matches a route group

Protected routes are declared in `authzRouteGroups` (gateway
`charts/gateway/values.yaml` and overlays). Each entry binds a method + public path
regex to an endpoint category and an identity mode:

```yaml
- name: vod_watch_content
  enabled: true
  enforcer: sidecar
  method: GET
  publicPathRegex: ^/vod/api/v3/course/([^/]+)/set/([^/]+)/content/([^/]+)$
  endpointCategory: watch_content
  identityMode:
    type: canonical_from_param   # gateway builds the object id from a path param
    targetType: content
  captures:
    resourceId: \3               # which capture group is the resource id
```

There are two identity modes:
- `canonical_from_param` (VOD, ticket): the gateway extracts the resource id from the
  path and builds the canonical object id itself.
- `comment_service_bundle` (comment): the gateway forwards a typed target ref plus
  service key, and the sidecar normalizes the object.

### 2. Gateway builds the canonical object id (Lua)

For `canonical_from_param`, the Lua helper `haproxy/lua/authz-sidecar.lua` builds the
object id in the platform's fixed shape:

```
<type>:p_<project_segment>__<tag>_<resource_segment>
```

- `project_segment`: lowercase Crockford Base32 of the project UUIDv7 (26 chars,
  reversible, never truncated).
- `resource_segment`: lowercase Crockford Base32 of the service-native integer id.
- `tag`: per-type short tag. `course`->`crs`, `set`->`set`, `content`->`cnt`,
  `assessment`->`asm`, `ticket_category`->`tcat`, `product`->`prd`.

Content `901` -> `cnt_w5`, so the object is
`content:p_01hzy0f6m4p7n8q9r0s1t2v3wx__cnt_w5`.

### 3. Gateway -> authz-sidecar

A **`HEAD`** subrequest to a fixed internal path, carrying trusted context as an
allowlisted header set (`authzSidecar.requestHeaderAllowlist`). Empty values are not
sent. `HEAD` is used because the whole decision rides in the status and headers.

```http
HEAD /internal/authz/check HTTP/1.1
Host: authz-sidecar
X-Project-Id: <project-uuidv7>
X-User-Id: 91
X-Request-Id: <uuid>
traceparent: 00-<trace>-<span>-01
X-Authz-Endpoint-Category: watch_content
X-Authz-Canonical-Object-Id: content:p_01hzy0f6m4p7n8q9r0s1t2v3wx__cnt_w5
X-Access: <compact-permission-bitmap>
```

For `comment_service_bundle` routes the gateway instead sends `X-Authz-Service-Key`,
`X-Authz-Comment-Target-Ref`, `X-Authz-Comment-Lineage-Ref`, and
`X-Authz-Comment-Story-Ref`, and the sidecar builds the object. These `X-Authz-*`
headers are stripped from client input at the edge, so a client cannot forge them.

### 4. authz-sidecar -> OpenFGA

The sidecar validates the context (`X-Project-Id` is a UUIDv7, `X-User-Id` is a
non-zero integer, endpoint category is known, object id matches the contract
pattern), resolves the final permission from `endpoint-permissions.yaml`
(`watch_content` + `content` -> `can_view`), confirms the store and model are
pinned, checks its short-TTL decision cache, and on a miss calls OpenFGA:

```http
POST {OPENFGA_API_URL}/stores/{OPENFGA_STORE_ID}/check
Content-Type: application/json
Authorization: Bearer <preshared-key>   # only when OPENFGA_AUTHN_METHOD=preshared
```

```json
{
  "authorization_model_id": "<OPENFGA_AUTHORIZATION_MODEL_ID>",
  "tuple_key": {
    "user": "user:91",
    "relation": "can_view",
    "object": "content:p_01hzy0f6m4p7n8q9r0s1t2v3wx__cnt_w5"
  }
}
```

- `user` is `user:` joined with the trusted numeric `X-User-Id`.
- `relation` is the resolved `can_*` permission.
- `object` is the canonical object id.
- OpenFGA replies `{ "allowed": true | false }`. Any non-`200` is a dependency failure.
- The runtime check sends no `context`; the optional `context` object (used for
  conditional tuples such as time-limited `not_expired` grants) is only added for
  manual testing. Tooling examples may show `"context": {}`, which is equivalent for
  an unconditional check.

### 5. Decision back to the gateway, then enforcement

| Sidecar status | Decision code (examples) | Gateway action | Event |
|---|---|---|---|
| `204` | `AUTHZ_ALLOWED` | copy allow-only `X-Authz-*` metadata downstream, forward to backend | `http.request.completed` |
| `403` | `AUTHZ_DENIED`, `AUTHZ_TARGET_RULE_MISMATCH` | gateway-owned `403`, backend not called | `authz.denied` |
| `401` | `AUTH_CONTEXT_MISSING` | gateway-owned `401` | `auth.context.invalid` |
| `400` | `AUTHZ_REQUEST_CONTEXT_INVALID`, `AUTHZ_ENDPOINT_CATEGORY_INVALID`, `AUTHZ_OBJECT_ID_INVALID`, `AUTHZ_NORMALIZATION_FAILED` | gateway-owned `400` | `input.validation.failed` |
| `503` | `AUTHZ_SERVICE_TIMEOUT`, `AUTHZ_SERVICE_UNAVAILABLE`, `AUTHZ_STORE_NOT_PINNED`, `AUTHZ_MODEL_NOT_PINNED` | gateway-owned `503` | `http.request.failed` |

On allow the sidecar returns `X-Authz-Decision-Id`, `X-Authz-Decision-Code`,
`X-Authz-Model-Id`, `X-Authz-Model-Label`, `X-Authz-Allow-Reason`,
`X-Authz-Allow-Modifiers`, and a base64url `X-Authz-Decision-Artifact`. The allow-side
`X-Authz-*` headers copied to the backend are **observability only** — a backend must
never treat them as an authorization input, and must still enforce its own business
rules.

## Endpoint category -> permission mapping

The sidecar resolves each endpoint category and target type to exactly one final
`can_*` permission. Source of truth:
`entitlement-platform/platform/openfga/contracts/endpoint-permissions.yaml`.

| Endpoint category | Target type | Final permission |
|---|---|---|
| `course_page` | `course` | `can_preview` |
| `set_page` | `set` | `can_preview` |
| `watch_content` | `content` | `can_view` |
| `list_comments` | `course` / `set` | `can_preview` |
| `list_comments` | `content` | `can_view` |
| `post_comment` | `course` / `set` / `content` | `can_comment` |
| `open_ticket_category` | `ticket_category` | `can_use_ticket` |
| `take_assessment` | `assessment` | `can_take` |

Runtime callers check `can_*` only. Never wire a route to a raw `grant_*` or `deny_*`
relation.

## The store, the model, and pinning

Three identifiers must agree across `projector` and `authz-sidecar`:

- `OPENFGA_STORE_ID`: the isolated authorization namespace that holds tuples and model
  versions. It is the `/stores/{store_id}/...` path segment. `OPENFGA_STORE_NAME` is
  the human-friendly name; the opaque id is what services pin.
- `OPENFGA_AUTHORIZATION_MODEL_ID`: a specific, immutable model version (the schema of
  types and relations). Pinning it means a model edit never silently changes live
  decisions.
- `OPENFGA_MODEL_LABEL` (default `authz_v1`): a human-readable label for that pinned
  version, echoed in logs and the `X-Authz-Model-Label` header.

Rule: `projector` (writer) and `authz-sidecar` (reader) must use the **same** store
id, model id, and label. Upload a new model id before writing new tuple shapes, and
roll back the label and model id together.

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
