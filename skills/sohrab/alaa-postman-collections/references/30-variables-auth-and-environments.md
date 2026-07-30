# Variables Auth And Environments

Read this file when declaring a variable, writing or reviewing an environment file, or
choosing where auth lives.

`42-scripts-and-state-capture.md` owns which scope a **script writes** to and why. This
file owns declaration, naming, safety, per-developer versus shared, the environment file's
shape, and auth inheritance.

## Environment completeness

An environment is complete when all six hold. Each one is checkable.

1. **Every referenced variable is declared.** Every `{{name}}` that appears anywhere in the
   collection — a URL, a header, a query value, a body, an auth block, a saved example, a
   script — exists either in the collection's `variable` block or in at least one committed
   environment file. An undeclared variable resolves to empty and the request fails with a
   malformed URL or a missing field, which reads as a broken API.
2. **Every variable a script writes is declared** before the script ships, under the exact
   name the script writes.
3. **Every secret-like variable is typed as a secret and carries a placeholder.** In the
   exported environment JSON that is `"type": "secret"` alongside a placeholder `value`.
   The type masks the value in Postman's UI; the placeholder is what keeps the real value
   out of git. Both are required, because the type alone protects nothing —
   `50-insomnia-compatibility-and-free-plan-rules.md` records that Insomnia's importer
   ignores `type` entirely.
4. **Every non-secret variable carries a value that works,** where a working default exists.
   A base URL, a route prefix, a page size, or a feature flag with a real default lets a
   new developer send the first request without editing anything.
5. **Every entry is enabled.** Insomnia's environment importer drops any entry whose
   `enabled` is falsy, so a variable parked as disabled is present in Postman and absent in
   Insomnia. Delete it or give it a placeholder instead.
6. **No committed value is an implementation constant the generator should own.** An
   environment value is operator input: a host, a route prefix, a page size, a credential
   placeholder, or an identifier the operator supplies. A pinned vendor model, engine,
   deployment, or embedding identifier is not operator input — it is a constant the
   generating script or service configuration owns, and freezing it in a committed
   environment means the artifact silently keeps pinning it after the service moves on.
   The positive replacement: declare the value as an input of the generator that emits the
   environment, reference it here as a `{{variable}}` or leave it out of the committed file
   entirely, and route which identifier to use to `/alaa-prompting-guide`
   (`$alaa-prompting-guide`). This skill states no model, engine, or vendor name of its own.
   `validate_postman_artifacts.py --forbid-pinned-vendor-identifier` is the gate;
   `60-validation-and-output-contract.md` holds the flag table.

## Per-developer versus shared

Apply one test: **if two developers running this collection at the same time would need
different values, the variable is per-developer.**

- **Shared** — committed with a real working value: host and base URL, service route
  prefixes, API version segments, page sizes, feature flags, and identifiers of resources
  that exist in every seeded environment.
- **Per-developer** — committed with a placeholder, then populated by a capture script or
  by that developer's own local edit: every credential and token, every session and device
  identifier, the developer's own account and contact identifiers, any one-time code, and
  any identifier of a resource that developer's own run created.

Say which is which in the collection description, so a new developer knows the short list
of values they have to supply by hand before the first request works.

## Safety rules for committed values

- No real secret in a committed collection variable, a committed environment file, a saved
  example, a request body, or a script.
- Placeholders are obviously placeholders: `<replace-me>`, `https://api.example.test`,
  `09120000000`. A realistic-looking sample value gets copied into a real system.
- Never a production hostname as a committed default.
- Postman no longer maintains a separate initial value and current value; a variable has one
  value that is local by default. So the value in the exported file is the value that lands
  in git — there is no shared-versus-local split to hide a real secret behind.
- Postman Vault, package-private values, uploaded runner data, and cloud-only sharing are
  operator conveniences. Never make the artifact's correctness depend on any of them; the
  portability baseline is the committed file.

## Naming

- `snake_case`, no hyphen. Insomnia's importer rewrites a hyphenated `{{name}}` into
  bracket notation, so a hyphen produces two spellings of one variable.
- Name for what the value is, not where it came from: `access_token`, not `token_from_login`.
- In an aggregate collection, namespace per contributing service.
  `70-aggregate-collections-and-consumer-repos.md` owns that rule.

## Environment file shape

- `"_postman_variable_scope": "environment"` on every environment file. Insomnia's
  environment importer rejects a file without it.
- Preserve an existing file's stable `id` and overall shape when it already exists and is
  safe to keep.
- Name environments for what they point at: `Local`, `Staging`, `Production Placeholder`.
- One file per genuinely different host or auth context. Two environments that differ only
  in one identifier belong in one file.

## Dynamic and data variables

- Dynamic values such as `{{$guid}}` and `{{$timestamp}}` are safe for local request bodies
  and survive Insomnia import as faker tags.
- A collection-runner data file stays an optional local input. Never make the committed
  collection unusable without an external data file unless the repository also commits that
  file with safe values.
- Prefer an explicit declared variable over a dynamic value for any identifier a developer
  commonly needs to see or edit, or that a script populates from a create response.

## Auth inheritance

Model only what the repository proves: bearer token, API key, basic auth, an explicit
custom header, a tenant header, or a gateway trust header. Use a variable for every token
and tenant identifier.

Choose the level by how the auth actually varies, not by convenience:

- **collection-level auth** when the whole collection genuinely shares one auth model
- **folder-level auth** when auth varies by bounded context or by service
- **request-level auth** only when one request genuinely differs, including `noauth` on a
  public route inside an otherwise protected folder

All three levels survive Insomnia import, so the level is now a clarity decision rather
than a portability one. The portability constraint that remains is the auth **type**: use
only `basic`, `bearer`, `apikey`, `digest`, `oauth1`, `oauth2`, or `awsv4`, because
Insomnia maps no others. `50-insomnia-compatibility-and-free-plan-rules.md` has the source
and the full table.

## Variable documentation

Document a variable where the reader who needs it will be looking:

- collection description for the environment contract and the per-developer short list
- folder or request description when the variable matters only there
- the request's `## Flow position` block for which request populates it
