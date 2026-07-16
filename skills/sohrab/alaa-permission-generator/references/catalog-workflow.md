# Catalog Workflow and Governance

## Ownership model

`alaa-permission-catalog` owns canonical coarse permission keys, stable global bitmap IDs, descriptions, service
ownership, status, and generated targets. Auth consumes the generated seed and owns runtime token issuance. Laravel and
Go services consume committed generated maps. The gateway forwards the verified bitmap as trusted `X-Access`; it does
not own the catalog. OpenFGA owns a different object-level decision vocabulary.

## Repository surfaces

- `catalog/permissions.json`: canonical registry and only ID allocation surface.
- `catalog/services.json`: importer/generator descriptors for consumer repositories.
- `generated/auth/database/seeders/data/permissions.php`: proposed auth seed snapshot.
- `generated/<owner-repo>/<source-path>`: proposed service artifact; simple repositories may use a shorter equivalent.
- `generated/reports/permission-drift-report.md`: primary human drift review.
- `generated/reports/permission-drift-report.json`: automation-friendly drift detail.
- `RUN_BOOK.md`: canonical operator procedure.

Each permission entry must include `bitmap_id`, `bit_index`, `permission_key`, `service_key`, `description`, `status`,
`aliases`, `legacy_keys`, `owner_repo`, `generated_targets`, `source_refs`, `notes`, and `display_name`. Use `active` for
issued permissions, `deprecated` for published permissions no longer granted, and `reserved` for burned IDs. Preserve
old spellings in `legacy_keys` when they explain history; do not introduce runtime aliases casually.

## Service descriptors

Laravel:

```json
{
  "service_key": "example",
  "owner_repo": "example",
  "source_path": "config/permissions.php",
  "input_shape": "service_config",
  "generated_target": "generated/example/config/permissions.php"
}
```

Go, including a service inside a monorepo:

```json
{
  "service_key": "example",
  "owner_repo": "platform-repo",
  "source_path": "services/example/internal/authz/permissions_gen.go",
  "input_shape": "go_service_permission_map",
  "generated_target": "generated/platform-repo/services/example/internal/authz/permissions_gen.go"
}
```

For every active downstream entry, include both targets:

```json
"generated_targets": [
  "auth:database/seeders/data/permissions.php",
  "example:services/example/internal/authz/permissions_gen.go"
]
```

The prefix before `:` is the catalog `service_key`; the remainder is the source-repository path.

## Drift interpretation

- Fatal/error findings block apply.
- `DANGEROUS_BITMAP_COLLISION` requires ownership correction; never solve it by silently remapping a consumer.
- `CONSUMER_PERMISSION_MISSING_FROM_AUTH` means auth cannot issue a consumed permission and blocks release.
- `AUTH_PERMISSION_UNUSED_BY_INSPECTED_SERVICES` is warning-only only when the catalog policy explicitly accepts the
  unonboarded or auth-local permission.
- After applying a generated consumer artifact, run import and strict drift again. The source observation must match the
  catalog ID/name pair.

## Apply boundaries

Generation writes review artifacts only. Copy/apply is explicit. Auth seed apply is separate from downstream service
apply, and assigning a permission to an admin, role, or user is a further auth-owned state mutation. Do not combine these
without explicit scope.

