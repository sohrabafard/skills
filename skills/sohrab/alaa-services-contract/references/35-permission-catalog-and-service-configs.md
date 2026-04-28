# Permission Catalog And Service Configs

Use this file when an Ala service changes `config/permissions.php`, permission names, bitmap ids, generated permission artifacts, permission drift checks, or `X-Access` decoding behavior.

## Ownership

- `alaa-permission-catalog` is the normative cross-service source of truth for permission names, service ownership, generated permission snapshots, and bitmap ids.
- Auth is the only runtime issuer of JWT authorization claims: `prm`, `prv`, and `av`.
- Backend services are generated-config consumers. Their committed `config/permissions.php` files should come from the catalog output for that service.
- Gateway, `authz-sidecar`, entitlement-platform, and OpenFGA are route or resource authorization infrastructure. They do not own service-local permission-name-to-bitmap-id maps.

## Service Config Rules

- Do not invent, manually renumber, or hand-maintain bitmap ids in `config/permissions.php`.
- Generate service-local permission configs from `alaa-permission-catalog`, review the generated output, then commit the generated file in the target service during an explicit apply phase.
- Use CI drift checks to detect mismatch between the catalog and committed service configs.
- Treat drift as evidence. Do not let normal import or generate commands silently copy generated configs into source repositories.
- Source service CI may run catalog drift checks with temporary generated output, but it must not modify source files, stage files, or reinterpret report-only warnings as failures.

## Apply Phase Rules

- Permission config changes must happen through explicit apply phases, one service at a time.
- Each apply phase must name the service, the generated input path, the destination path, and the focused validation set before copying files.
- Keep unrelated repos untouched. Applying content config must not also apply comment, auth, WA, gateway, JWT semantics, or bitmap encoding changes unless the phase explicitly says so.
- After apply, run service-local tests that prove:
  - `X-Access` decodes against the committed generated config
  - trusted context resolution still rejects missing, malformed, or zero-known-permission bitmaps
  - service authorization behavior still matches local policies, Gates, or middleware
- Run catalog `check-drift` before and after permission-related work when the repo has access to `alaa-permission-catalog`.

## Extraction And Reuse Rules

- Bitmap ids are never reused.
- Removed permissions must become `deprecated` or `reserved`; do not delete published ids from the catalog.
- Service extraction must not reuse old bitmap ids across new service boundaries.
- Legacy VOD ids remain stable for VOD compatibility.
- Extracted `content_*` permissions receive new catalog-owned ids, currently `64-78`, and are not runtime aliases for VOD permissions.

## Current Canonical Outcomes

- Current generated catalog status is `clean` with `91` permissions. Fatal and error drift findings are `0`; current warnings are report-only unless a later policy promotes a scoped warning.
- `wa_get_watch_stats` owns bitmap id `1`; WA service-local config adoption is deferred until WA has a committed permission-consumer shape.
- `comment_get_index` owns bitmap id `18`.
- `comment_get_show` owns bitmap id `40`.
- Extracted content-service permissions own bitmap ids `64-78`.
- ControlledOps content bulk permissions own bitmap ids `79-91`.

## Current Permission Snapshot

Use this compact grouping instead of copying the full catalog into prompts:

| Range         | Owner     | Permissions                                                                                   |
|---------------|-----------|-----------------------------------------------------------------------------------------------|
| `1`           | `wa`      | `wa_get_watch_stats`                                                                          |
| `2-13`        | `vod`     | analytics and study-cell permissions                                                          |
| `14-17`       | `ticket`  | `crm_get_tickets`, `crm_post_ticket_reply`, `crm_put_ticket`, `crm_post_bulk_ticket`          |
| `18-21`, `40` | `comment` | `comment_get_index`, `comment_approve`, `comment_delete`, `comment_reply`, `comment_get_show` |
| `22-39`       | `vod`     | legacy content, content-set, product, copy, and discount permissions                          |
| `41-63`       | `auth`    | profile, sessions, TOTP, admin authz override, and admin catalog permissions                  |
| `64-78`       | `content` | extracted set, content, and course permissions                                                |
| `79-91`       | `content` | ControlledOps content bulk permissions                                                        |

## Companion Skill Boundary

- Use `$alaa-trust-gateway-auth` for JWT claim semantics, `prm` to `X-Access` projection, bitmap packing, trusted-header spoofing defense, and gateway/auth ownership.
- Use this file for service-local generated config adoption, CI drift checks, and one-service-at-a-time apply discipline.
