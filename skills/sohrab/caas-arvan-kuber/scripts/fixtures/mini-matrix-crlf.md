# Mini capability matrix fixture

## Capture stamp

- **Spec capture date: unknown.**
- **Matrix last reconciled against the spec: 2026-07-29.**
- **Vendor cross-check: 2026-07-29.**

## Generated block

<!-- BEGIN GENERATED: summarize-openapi.sh -->
- `openapi`: `3.0.3`
- `info.title`: `Mini CaaS`
- `info.version`: `1.25`
- Paths: `5`
- Operations: `17`
- Namespaced paths: `5/5`
- Servers:
  - `https://example.invalid/caas/v2/zones/test-1`

| API resource | Collection | Item | Subresources |
|---|---|---|---|
| `apps/v1/deployments` | `[delete,get,post]` | `[delete,get,patch,put]` | `scale=[get,patch,put]` |
| `core/v1/configmaps` | `[delete,get,post]` | `[delete,get,patch,put]` | `-` |
<!-- END GENERATED -->

## Hand-written interpretation

This section must survive --update untouched.
