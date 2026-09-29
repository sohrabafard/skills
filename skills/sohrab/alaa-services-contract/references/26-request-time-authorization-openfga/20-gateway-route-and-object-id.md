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
