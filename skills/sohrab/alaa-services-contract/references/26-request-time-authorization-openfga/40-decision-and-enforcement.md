### 5. Decision back to the gateway, then enforcement

| Sidecar status | Decision code (examples) | Gateway action | Event |
|---|---|---|---|
| `204` | `AUTHZ_ALLOWED` | copy allow-only `X-Authz-*` metadata downstream, forward to backend | `http.request.completed` |
| `403` | `AUTHZ_DENIED`, `AUTHZ_TARGET_RULE_MISMATCH` | gateway-owned `403`, backend not called | `authz.denied` |
| `401` | `AUTH_CONTEXT_MISSING` | gateway-owned `401` | `auth.context.invalid` |
| `400` | `AUTHZ_REQUEST_CONTEXT_INVALID`, `AUTHZ_ENDPOINT_CATEGORY_INVALID`, `AUTHZ_OBJECT_ID_INVALID`, `AUTHZ_NORMALIZATION_FAILED` | gateway-owned `400` | `input.validation.failed` |
| `503` | `AUTHZ_SERVICE_TIMEOUT`, `AUTHZ_SERVICE_UNAVAILABLE`, `AUTHZ_STORE_NOT_PINNED`, `AUTHZ_MODEL_NOT_PINNED` | gateway-owned `503` | `http.request.failed` |

On allow the sidecar returns exactly these headers: `X-Authz-Decision-Id`,
`X-Authz-Decision-Code`, `X-Authz-Model-Id`, `X-Authz-Model-Label`, `X-Authz-Allow-Reason`,
`X-Authz-Allow-Modifiers`, and a base64url `X-Authz-Decision-Artifact`.

A backend reads the allow-side `X-Authz-*` headers only to log them, and enforces its own business
authorization independently. `/alaa-security-review` owns the general rule that allow-side authorization
metadata is never an authorization input, and the review trigger for a change that would make it one; this
file owns the exact header names above and the fact that they arrive on allow only.
