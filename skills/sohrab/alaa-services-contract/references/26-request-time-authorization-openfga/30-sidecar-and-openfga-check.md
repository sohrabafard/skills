### 3. Gateway -> authz-sidecar

A **`HEAD`** subrequest to a fixed internal path, carrying trusted context as an
allowlisted header set (`authzSidecar.requestHeaderAllowlist`). Empty values are not
sent. `HEAD` is used because the whole decision rides in the status and headers.

```http
HEAD /internal/authz/check HTTP/1.1
Host: authz-sidecar
X-Project-Id: 019d4d45-54de-72a7-a6c2-c3fb70d82af0
X-User-Id: 0190f7d8-f840-7a85-9a89-e3f61052f840
X-Request-Id: <uuid>
traceparent: 00-<trace>-<span>-01
X-Authz-Endpoint-Category: watch_content
X-Authz-Canonical-Object-Id: content:p_06emthamvssaf9p2rfxq1p1ay0__cnt_06emtsgw09xh1d0x3nfktfmffw
X-Access: <compact-permission-bitmap>
X-Location-Ostan: 8
X-Location-Shahrestan: 257
X-Location-Bakhsh: 12
X-Location-Shahr: 2576
X-Location-Shobe: 12354
X-Location-School: 9988
```

For `comment_service_bundle` routes the gateway instead sends `X-Authz-Service-Key`,
`X-Authz-Comment-Target-Ref`, `X-Authz-Comment-Lineage-Ref`, and
`X-Authz-Comment-Story-Ref`, and the sidecar builds the object (step 2). These `X-Authz-*`
headers are stripped from client input at the edge, so a client cannot forge them.

### Location context

The gateway forwards the six `X-Location-*` headers in the allowlist (`gateway: charts/gateway/values.yaml:309-314`).
Auth emits all six `loc` fields and turns a null or non-positive level into `0`
(`auth: app/Services/Auth/TokenService.php:688,726-753`). The gateway injects a header only for a positive
value, so `0` arrives as an absent header (`gateway: charts/gateway/templates/configmap.yaml:1549-1554`).

The sidecar classifies all six headers before any OpenFGA call
(`authz-sidecar: internal/decision/location.go:82-137`; `internal/decision/engine.go:311-313`):

- Absent: `AUTH_NAME_OR_LOCATION_HEADER_REQUIRED`. Absent wins over malformed.
- Duplicate, empty, longer than 20 bytes, leading zero, or non-digit: `AUTH_NAME_OR_LOCATION_HEADER_INVALID`.
- `0`: valid source-null. A positive value is a membership input.

Consequence: a token with any zero level is refused on every sidecar-protected route, and the all-zero path
below is unreachable through the gateway. The owner accepts this gap for now. Rules that do not depend on
location for such users await a cross-service feature request.

Leaf and derivation rule (`authz-sidecar: internal/decision/geography.go:143-224,307-378`):

- Positive `shobe` and `school` values are leaves. Otherwise the leaf is the deepest positive of `ostan`,
  `shahrestan`, `bakhsh`, `shahr`.
- Each leaf rides only as the contextual tuple `<type>:<id>#member@user:<uuid>`. It is never stored.
- Ancestors come from stored `child_*` edges. Each `shobe` or `school` leaf gets one `ListObjects` for `shahr`.
  Each leaf other than `ostan` gets one for `ostan`. Each call must return exactly one object, else
  `AUTHZ_LOCATION_TOPOLOGY_DEFECT`.
- One `BatchCheck` carries a `member` item for each positive header ancestor above each leaf (false:
  `AUTHZ_LOCATION_CONTRADICTORY`), a `country:ctry_1` `member` item per leaf (false:
  `AUTHZ_LOCATION_TOPOLOGY_DEFECT`), and the final `can_*` item with the leaf tuples. Two leaves that derive
  different `shahr` objects are contradictory.
- All six `0`: one plain Check with no tuple and no derivation call
  (`authz-sidecar: internal/decision/decision_cache.go:144-168`).
- Membership flows upward only (`authz-openfga: platform/openfga/model.fga:39-77`). Rules on the leaf and its
  ancestors apply; rules on its descendants do not.

`40-decision-and-enforcement.md` owns the status of each code above.

Pending redesign: `authz-openfga: docs/_agent_plans/20261031-033500_full-geography-topology-seed-below-ostan.md`.
Items 1-3 await owner approval: a contextual tuple for every positive level and country, gap detection, no
per-request contradiction items, and a new `AUTHZ_LOCATION_INCOMPLETE`. Items 4-5, the full stored seed below
`ostan`, were approved on 2026-10-31. The sidecar still implements the leaf-only rule above.

### 4. authz-sidecar -> OpenFGA

The sidecar validates the context (`X-Project-Id` and `X-User-Id` are canonical
UUIDv7 strings, endpoint category is known, object id matches the contract
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
    "user": "user:0190f7d8-f840-7a85-9a89-e3f61052f840",
    "relation": "can_view",
    "object": "content:p_06emthamvssaf9p2rfxq1p1ay0__cnt_06emtsgw09xh1d0x3nfktfmffw"
  }
}
```

- `user` is `user:` joined with the trusted canonical user UUIDv7 from `X-User-Id`, as defined by
  `25-end-to-end-flow-and-boundaries.md`. Preserve the object's existing encoding.
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
reflector-only writes and fail-closed behavior above are unchanged.
