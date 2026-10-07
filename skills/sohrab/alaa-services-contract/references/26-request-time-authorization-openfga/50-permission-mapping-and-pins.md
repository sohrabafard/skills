## Endpoint category -> permission mapping

The sidecar resolves each endpoint category and target type to exactly one final
`can_*` permission. Source of truth:
authz-openfga `<repo>/platform/openfga/contracts/endpoint-permissions.yaml`.

Author there. Consumers import immutable generated bundles pinned by
`contracts.lock.json`; never hand-edit imported snapshots or pins. Local integrity
does not prove upstream equality; verify against the reviewed canonical export
(authz-openfga `<repo>/docs/readme/10-contract-bundle-export.md`).

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
