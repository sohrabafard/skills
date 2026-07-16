# Laravel Consumer Pattern

Use `input_shape: service_config` and commit the generated `config/permissions.php`. The generated shape is keyed by
permission name and contains `id`, `name`, and `description`.

## Integration rules

1. Use the repository's established trusted-context middleware, normally `ResolveUserMiddleware`, to decode `X-Access`.
2. Read the committed generated config; do not call auth or the catalog on each request.
3. Keep the shared bit contract: 1-based IDs, `bit_index = id - 1`, LSB-first bytes, raw unpadded base64url.
4. Ignore bitmap bits not present in this service's config, but fail closed when no known permission resolves.
5. Authorize controllers/routes using canonical generated names, not duplicated numeric literals.
6. Remove legacy or alternate permission arrays when the generated config becomes authoritative.
7. Preserve gateway trust rules: clients cannot supply `X-Access`, user identity, project identity, or roles directly.

## Validation

- Run the repository's permission/config tests and protected-route feature tests.
- Test at least one ID above a byte boundary to prove LSB-first indexing.
- Test malformed/padded base64url, unknown-only bitmaps, missing headers, allowed permission, and denied permission.
- Run Laravel config/package validation as required by the repository.
- Re-import in the catalog and require strict drift to remain free of fatal/errors.

Do not add a dynamic runtime config override for emergency convenience. A permission-map change is a catalog change,
generated artifact review, service deployment, auth seed deployment when needed, and permission assignment when needed.

