# Insomnia Compatibility And Free Plan Rules

Read this file when Insomnia portability is a requirement, when choosing an auth type or
an auth level, or when a construct's survival across tools is in question.

## The constraint

The deliverable is a valid Postman Collection Format v2.1 collection. Within that
constraint, carry everything Insomnia additionally preserves, and never choose a Postman
construct that breaks the Insomnia path when an equally valid Postman construct survives
it.

Insomnia is not a second output format. There is one artifact, and Insomnia is a second
reader of it.

## What Insomnia preserves and what it drops

Verified 25 July 2026 by reading Insomnia's own importer at
`packages/insomnia/src/main/importers/importers/postman.ts` and
`packages/insomnia/src/main/importers/importers/postman-env.ts` on the `master` branch of
`https://github.com/Kong/insomnia`, and Insomnia's documentation at
`https://developer.konghq.com/insomnia/scripts/`,
`https://developer.konghq.com/insomnia/import-export/`, and
`https://developer.konghq.com/how-to/migrate-collections-and-environments-from-postman-to-insomnia/`.

| Postman construct | Insomnia on import | Consequence for authoring |
|---|---|---|
| request method, URL, query params, path variables, headers, body | preserved | nothing to avoid |
| `info.description`, folder `description`, request `description`, header `description` | preserved | request documentation survives; write it in the description, not in a script comment |
| collection-level `auth` | preserved, applied to the collection's imported folder | collection-level auth is usable again; the 2023 report that it was silently dropped no longer matches the code |
| folder-level and request-level `auth` | preserved | nothing to avoid |
| `auth.type` of `basic`, `bearer`, `apikey`, `digest`, `oauth1`, `oauth2`, `awsv4` | mapped | use only these seven |
| any other `auth.type`, including `hawk`, `ntlm`, `edgegrid`, `asap`, and `jwt` | falls to a default branch that yields empty authentication | never use one when a mapped type expresses the same auth |
| an explicit `Authorization` header | preserved in every branch | a request that must authenticate in Insomnia under an unmapped type keeps working only because of this header |
| collection-level `variable` | imported as an Insomnia environment named `Variables`, wired as the collection's Base Environment | declare shared non-secret defaults here |
| folder-level and item-level `variable` | not read | never put a value only in a folder or item `variable` block |
| `event` scripts at collection, folder, and item scope | the **first** `prerequest` and the **first** `test` event per scope are imported; any further event with the same listener is dropped | exactly one `prerequest` and one `test` event per scope |
| script contents | rewritten: legacy forms are translated, then `pm.` is textually replaced with `insomnia.` | see the scripting rules below |
| `item.response`, the saved examples | **not read at all** | every saved example, and therefore the whole error catalogue, is Postman-side only |
| `protocolProfileBehavior` | not read | never rely on it for behaviour a request needs |
| mock servers | not imported; Insomnia's documentation says they must be recreated manually | `45-mock-servers.md` treats a mock as Postman-side convenience only |

## The saved-example consequence

Insomnia's Postman importer never reads `item.response`. This is the single largest gap
between the two tools, and it changes where a fact has to live.

- Keep attaching examples for every response, per
  `41-response-contract-and-error-coverage.md`. They are how Postman documents the route,
  how a mock server serves it, and how an SDK author reads the real shape.
- Never let an example be the **only** place a fact is stated. Every status, code, and
  caller action in the examples also appears in the request's `## Errors` table, because
  the description survives import and the example does not.
- When Insomnia is the primary client for a consumer, say in the task output that saved
  examples do not reach them, so nobody plans around examples they will not receive.

## Importer detection: the exact `info.schema` value

Insomnia's `convert()` accepts a Postman collection only when `info.schema` is exactly
one of these four strings:

```text
https://schema.getpostman.com/json/collection/v2.0.0/collection.json
https://schema.postman.com/json/collection/v2.0.0/collection.json
https://schema.getpostman.com/json/collection/v2.1.0/collection.json
https://schema.postman.com/json/collection/v2.1.0/collection.json
```

Any other value returns null and Insomnia reports `No importers found for file`. This is
a string comparison, not a URL resolution, so a reachable and valid schema URL still
fails when it is not on that list.

Use this one, which is the Postman export marker and the v2.1 member of the list:

```text
https://schema.getpostman.com/json/collection/v2.1.0/collection.json
```

Do not put `https://schema.getpostman.com/collection/json/v2.1.0/draft-04/collection.json`
in `info.schema`. It is the URL for validating a collection against the JSON Schema, and
it is not in Insomnia's accepted list.

## Scripting rules that follow from the rewrite

Insomnia rewrites `pm.` to `insomnia.` as text, then runs the result against its own
object. A `pm.*` call therefore works in Insomnia exactly when the matching
`insomnia.*` member exists.

- Use `insomnia`-backed members only: `pm.test`, `pm.expect`, `pm.response`, `pm.request`,
  `pm.environment`, `pm.variables`, `pm.collectionVariables`, `pm.cookies`,
  `pm.sendRequest`.
- Never use `pm.globals.*`. Insomnia's documentation states plainly that
  `insomnia.globals` "is not supported yet", so the rewritten call has nothing to resolve
  against.
- Never use the deprecated `postman.*` interfaces. Insomnia's documentation states they
  "are not supported yet"; the importer translates several of them, but relying on a
  translation table for correctness is relying on an implementation detail.
- Never use `pm.vault`, `pm.require`, `pm.state`, `pm.datasets`, or `pm.visualizer`. They
  have no Insomnia counterpart, and a package-library import is not carried in the
  exported file at all.
- Prefer `pm.expect(pm.response.code).to.eql(200)` over `pm.response.to.have.status(200)`.
  Insomnia's own documented example is
  `insomnia.expect(insomnia.response.code).to.eql(201)`; whether the chai-style
  `insomnia.response.to.have.*` chain resolves is **not documented and was not verified**.
- Postman dynamic variables such as `{{$guid}}` are rewritten into Insomnia's
  `{% faker 'guid' %}` tag, so they survive. A variable name containing a hyphen is
  rewritten into bracket notation, so name every variable in `snake_case` with no hyphen.

## Environment file rules that follow from the environment importer

Insomnia's Postman-environment importer reads three fields and ignores the rest.

- `_postman_variable_scope` must be exactly `environment` or `globals`, or the file is
  rejected outright. Always export with `"_postman_variable_scope": "environment"`.
- Only entries whose `enabled` is truthy are imported. A variable left `"enabled": false`
  to park it silently disappears on the Insomnia side; delete it or give it a placeholder
  value instead.
- A value's `type` and `description` are ignored. `"type": "secret"` therefore protects
  the value in Postman's UI and gives no protection in Insomnia, which is one more reason
  no committed file carries a real secret value at all —
  `30-variables-auth-and-environments.md` owns that rule.
- A collection that reads variables from a Postman **global** environment needs the
  imported environment selected as the collection's Base Environment in Insomnia, per
  Insomnia's migration guide. Avoid depending on globals so that step is unnecessary.

## Postman free-plan rules that matter here

Postman's Free plan includes the API client, collections and environments, collection
generation and sync, Native Git, the Postman CLI, and unlimited Collection Runner and
Performance Testing runs. Paid plans add custom-branded documentation, custom domains,
broader collaboration, and enterprise governance. Therefore:

- never require paid documentation branding, a custom domain, or team-only governance
- keep the workflow local and file-based by default
- treat mock-server call volume as metered and never make correctness depend on it

## Insomnia free-plan rules that matter here

Insomnia's free tier includes unlimited Cloud and Local projects, unlimited collection
runs, unlimited environments, Inso CLI access, and plugin access. Therefore:

- never assume a paid Insomnia plan is needed to import or run the artifact
- keep validation steps runnable locally
- treat enterprise-only storage controls, RBAC, SSO, and vault integrations as out of
  scope

## Features that stay optional

Postman monitors, Postman cloud publishing, custom-branded documentation, custom domains,
enterprise governance and vault integrations, and Insomnia enterprise storage controls or
SSO. A committed artifact works without every one of them.

## Proving portability

Run the importer family before closing when local Node and network access are available:

```shell
npx --yes insomnia-importers@3.6.0 path/to/collection.postman_collection.json
```

A successful conversion is stronger evidence than JSON or schema validation for the
`No importers found for file` failure mode. When the host cannot run it, state that exact
gap in the task output rather than describing portability as verified.
