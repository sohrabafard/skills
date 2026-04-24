# Variables Auth And Environments

## Variable model

Use the smallest stable scope that keeps the collection understandable:

- collection variables for shared, non-secret reusable values
- environment variables for environment-specific hosts, tenants, tokens, IDs, and feature flags
- request-local or script-local values only when they are truly request-specific

Postman variables resolve through scope, and `pm.variables.get()` returns the highest-precedence value. Use that to keep shared scripts portable when scope may change later.

## Dynamic and data variables

Use dynamic variables and runner data only when they keep examples realistic without inventing contract truth:

- dynamic values such as generated UUIDs or timestamps are useful for safe local request bodies
- collection-runner data files can be useful for scenario testing, but they should remain local optional inputs
- do not make the committed collection unusable without an external data file unless the repo also commits that safe data file
- prefer explicit environment variables for IDs that users commonly need to edit or that scripts save from create responses

## Safety rules for values

- Keep secrets out of committed collection variables.
- Export environment files with safe placeholders, never real secrets.
- Prefer placeholders such as `<replace-me>` or `https://api.example.test` over sample production values.
- Do not make the workflow depend on Postman Vault features. Vault is not the portability baseline for this skill.
- Treat Postman Vault, package-private values, uploaded runner data, and cloud-only sharing as optional operator conveniences, not as required artifact behavior.

## Team and cloud behavior

Postman documents that collection, environment, and global variable values are local by default. Shared values sync to the Postman cloud and can also appear in published documentation. Because committed artifacts must stay portable and safe:

- prefer local file exports with placeholder values
- avoid relying on shared cloud values
- never share or publish sensitive values through collection docs

## Environment file rules

- If a repo already contains exported Postman environment JSON, preserve its stable IDs and overall shape when safe.
- If no environment artifact exists, create the smallest useful environment file with clear placeholders and descriptions.
- Keep environment names explicit, such as `Local`, `Staging`, or `Production Placeholder`.
- Separate clearly different hosts or auth contexts into separate environments when that improves clarity.

## Auth inheritance

Use inheritance deliberately:

- prefer collection-level auth when the whole collection truly shares one auth model and Postman is the only meaningful target
- prefer folder-level auth when auth varies by bounded context or when free Insomnia import clarity matters
- override auth at the request level only when a request genuinely differs

## Insomnia-aware auth rule

Official Insomnia docs say Insomnia does not support setting authentication headers at the collection level in its native model, and recommends folder-level auth as the workaround. Because this skill is Postman-first but must preserve clean Insomnia import:

- keep collection-level auth only when it is clearly worth the Postman-first simplicity
- otherwise favor folder-level auth for shared groups so the imported artifact stays easier to understand in Insomnia

## Common auth patterns

Model only what the repo proves:

- Bearer token
- API key
- Basic auth
- custom headers
- tenant headers
- gateway or trust headers

Keep auth values realistic but safe. Use variables for tokens and tenant IDs, not hardcoded secrets.

## Variable documentation

Document important variables where a future reader will actually see them:

- collection description for the main environment contract
- folder or request description when a variable is only relevant there
- environment descriptions or adjacent notes when the file format allows it in the existing repo style
