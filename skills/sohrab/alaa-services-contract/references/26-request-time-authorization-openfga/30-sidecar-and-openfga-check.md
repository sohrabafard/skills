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

The omitted consistency preference uses OpenFGA's default `MINIMIZE_LATENCY`, which permits server-cache
results only when caching is enabled; upstream's disabled-by-default cache does not prove deployed settings.
`HIGHER_CONSISTENCY` bypasses OpenFGA query caches, not unprojected events or the sidecar decision cache
([official consistency guide](https://openfga.dev/docs/interacting/consistency), read 2026-09-29). This
capability does not authorize caching beyond `22-failure-load-and-deprecation-contract.md`. Before claiming
revoke visibility, verify projection completion and lag, sidecar/server cache settings, deployed server/SDK
semantics and the agreed end-to-end budget; missing evidence remains unknown. The request, pins, TTLs,
projector-only writes and fail-closed behavior above are unchanged.
