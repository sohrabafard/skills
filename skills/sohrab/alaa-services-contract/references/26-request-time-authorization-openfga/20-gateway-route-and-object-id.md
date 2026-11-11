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
  service key. It also builds a canonical id, but the sidecar ignores it whenever a
  service key is present and rebuilds the object from the target ref
  (`authz-sidecar: internal/decision/engine.go:406-428,482-510`).

### 2. Gateway builds the canonical object id (Lua)

`haproxy/lua/authz-sidecar.lua` builds the object id (`build_canonical_object`,
`:742-757`) and sends it as `X-Authz-Canonical-Object-Id` (`:923-924`):

```
<type>:p_<project_segment>__<tag>_<resource_segment>
```

- `project_segment`: Crockford Base32 of the trusted `X-Project-Id` UUIDv7 bytes
  (`encode_uuid_v7`, `:282-297`).
- `resource_segment`: for `course`, `set` and `content`, Crockford Base32 of the
  content-service UUIDv7 `public_id` from the path (`:35-39,750-751`); for other
  types, Crockford Base32 of the decimal integer id (`:329-355,753`).
- `tag`: `RESOURCE_TAGS` (`:28-34`) — `course`->`crs`, `set`->`set`,
  `content`->`cnt`, `ticket_category`->`tcat`, `product`->`prd`. The contract tag
  list is `authz-openfga: platform/openfga/contracts/authorization-contract.yaml:417-429`.

`31-cross-service-identifier-stability.md` "Identifier form per layer" owns the
segment encodings and every other layer's form; this file states none.

Example: project `019d4d45-54de-72a7-a6c2-c3fb70d82af0`, content public id
`019d4d66-1c02-7b10-b41d-1d5f3d3e8f7f`:
`content:p_06emthamvssaf9p2rfxq1p1ay0__cnt_06emtsgw09xh1d0x3nfktfmffw`.

The sidecar trusts no gateway-built project segment. It re-encodes `X-Project-Id` and
refuses a mismatching canonical id with `400 AUTHZ_OBJECT_ID_INVALID`
(`authz-sidecar: internal/decision/engine.go:302,431-437`;
`internal/contracts/contracts.go:251-263`).
