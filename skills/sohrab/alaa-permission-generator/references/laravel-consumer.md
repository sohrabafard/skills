# Laravel Consumer Pattern

Read `references/shared-consumer-contract.md` first; the six rules there govern this file and are not repeated.
`input_shape` is `service_config`.

## The generated config

`config/permissions.php` is a keyed array, one block per permission, `'<name>' => ['id', 'name', 'description']`, with
`declare(strict_types=1);` and **no generated-file header**. The absence of the header does not make it hand-editable.

Only `content` and `comment-service` produce a config at all — see the hardcoding note in
`references/catalog-workflow.md` before onboarding a third Laravel service.

Membership is the union of two sources: observations for that `service_key` from non-auth repositories, with the id
remapped through the catalog **by name**; and catalog entries for that `service_key` that list
`<service_key>:config/permissions.php` in `generated_targets`. Status is not consulted, so a `deprecated` entry stays in
the file — see `references/lifecycle.md`.

## Integration rules

1. Decode the trusted header in the repository's established trusted-context middleware, which is
   `ResolveUserMiddleware` in every Alaa Laravel service. If the repository has no such middleware, stop and ask rather
   than decoding in a controller, a policy, or a service class.
2. Read the committed generated config. Never call auth or the catalog during a request.
3. Authorize controllers and routes by the canonical generated permission name, read from the config. No numeric literal
   and no string literal of a permission name appears anywhere else in the service.
4. When the generated config becomes authoritative, delete every legacy or alternate permission array in the same
   change. Two maps in one service is the failure this skill exists to prevent.
5. Who may assert `X-Access`, user identity, project identity, or roles, and what the gateway sanitises, are owned by
   `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`). Read it before touching the middleware; it wins on any
   conflict.
6. Never add a runtime config override, a cache-backed permission map, or an environment escape hatch, including for an
   incident. A permission-map change is a catalog change, artifact review, service deploy, auth seed deploy when the
   seed changed, and permission assignment when the assignment changed.

## Tests

- A permission whose id is above a byte boundary (an id in the second byte and one above 64) resolves correctly, proving
  least-significant-bit-first indexing rather than a coincidence at low ids.
- Malformed, padded, and invalid-character base64url each grant nothing.
- An unknown-only bitmap is rejected on a protected route; an unknown bit mixed with a known bit keeps the known
  permission.
- A missing trusted header is rejected; an allowed permission passes and a denied permission is refused, each asserting
  the denial carries the failing permission key.
- The committed config matches a fresh generation, so a stale artifact fails the suite rather than passing quietly.

Run the repository-native validation per `/alaa-laravel-architecture` (`$alaa-laravel-architecture`) and
`/alaa-php-clean-code` (`$alaa-php-clean-code`); design-pattern selection is
`alaa-php-clean-code references/design-patterns.md`.
