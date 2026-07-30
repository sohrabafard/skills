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

Verified 30 July 2026 against **Insomnia 12.6.0, released 22 May 2026**, the current stable
release. The importer claims were read from
`packages/insomnia/src/main/importers/importers/postman.ts` and
`packages/insomnia/src/main/importers/importers/postman-env.ts`, and the scripting-object
claims from `packages/insomnia-scripting-environment/src/objects/response.ts`, all at tag
`core@12.6.0` of `https://github.com/Kong/insomnia`. Read a tag rather than `master`: a
`master` reading cannot be tied to a release a reader can install. Also verified against
Insomnia's documentation at
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

## Why this skill pins v2.1 when v3.0.0 exists

Postman's current collection schema is **3.0.0**, not 2.1. Its stated design goal is a
collection spread over multiple YAML files so people, agents, and tooling can read, diff, and
review it — which is this skill's own premise. The pin on 2.1 is nonetheless deliberate, and
rests on two constraints 3.0 does not satisfy:

- Insomnia's `convert()` accepts only the four v2.0 and v2.1 schema strings listed above. A
  3.0 collection is rejected with `No importers found for file`, so the Insomnia leg of this
  skill's portability requirement cannot be met by 3.0 at all.
- Newman runs a collection exported to 2.1 and cannot run 3.0; running a 3.0 collection
  requires the Postman CLI. Pinning 2.1 keeps the artifact runnable by both.

Re-derive both facts before changing the pin:

```shell
curl -s https://raw.githubusercontent.com/Kong/insomnia/core@12.6.0/packages/insomnia/src/main/importers/importers/postman.ts | grep -A4 POSTMAN_SCHEMA_URLS_V2_1
```

and read the schema-version and Newman-compatibility statements at
`https://learning.postman.com/docs/use/use-collections/collections-schemas`. Change the pin
only when both constraints have changed, and record the date and the source with the change.

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
- `insomnia.response.code` is the numeric HTTP status and `insomnia.response.status` is the
  reason phrase. Both members exist; they are not two spellings of one value. Insomnia's
  `Response` class declares `code: number` and `status: string`, and sets
  `this.status = options.reason || RESPONSE_CODE_REASONS[options.code] || ''`. So
  `pm.response.code` rewrites to the number to compare against `200`, and Insomnia's current
  documentation example `const status = insomnia.response.status;` reads the phrase, not the
  code. Comparing `status` to a number always fails on both sides.
- The chai-style `pm.response.to.*` chain does resolve, for exactly the members Insomnia
  registers on the response object: the properties `withBody`, `error`, `ok` and `json`, and
  the methods `status(code)`, `header(name)`, `body(text)`, `jsonBody(key)` and
  `jsonSchema(schema)`. `status(code)` compares against `code` internally, so
  `pm.response.to.have.status(200)` is correct in both tools. Any other member on that chain
  is unresolved after the rewrite; `validate_postman_artifacts.py` warns on the members
  outside this list and stays silent on the ones in it. `43-response-tests.md` states which
  form to write and why.
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

Postman's Free plan, read 30 July 2026, includes the API client and core tools, specs and
mock servers, Native Git, the Postman CLI, the local vault, the secret scanner, manual
Flows, and unlimited Collection Runner and Performance Testing runs. Its limits that bear on
a committed artifact are `1 user`, `10,000` monthly Postman API calls, `1,000 requests` of
monthly API monitoring, `Up to 5` integrations, `50 AI credits`, and a `1 day` collection
recovery window. Paid plans add custom-branded documentation, custom domains, broader
collaboration, and enterprise governance. Therefore:

- never require paid documentation branding, a custom domain, or team-only governance
- keep the workflow local and file-based by default, because a `1 day` recovery window means
  the committed file, not Postman's cloud, is what the artifact's durability rests on
- never build a workflow around the Postman API or around monitors: both are metered per
  month at the numbers above, and a workflow that needs them stops working mid-month

## Insomnia free-plan rules that matter here

Insomnia's free tier, branded **Essentials** and read 30 July 2026, includes unlimited
Cloud and Local projects for all users, unlimited collection runs, unlimited environments,
Inso CLI access for CI, end-to-end encryption, and unlimited plugins. Two limits bear on a
committed artifact: `Unlimited Git Sync projects for up to 3 users`, and `1,000 mock server
requests per month`. Therefore:

- never assume a paid Insomnia plan is needed to import or run the artifact
- keep validation steps runnable locally
- never make a collection's correctness depend on a mock server on either side: Insomnia
  meters mock requests at `1,000` a month, and `45-mock-servers.md` treats a mock as a
  convenience rather than a contract
- treat enterprise-only storage controls, RBAC, SSO, and vault integrations as out of scope,
  and treat Git Sync as unavailable above three users

## Features that stay optional

Postman monitors, Postman cloud publishing, custom-branded documentation, custom domains,
enterprise governance and vault integrations, and Insomnia enterprise storage controls or
SSO. A committed artifact works without every one of them.

## Proving portability

**There is no maintained command-line Postman-to-Insomnia converter.** Both npm packages
this file used to prescribe are deprecated: `insomnia-importers` and `insomnia-inso` were
each last published 27 September 2022 and both now carry
`Package no longer supported. Use at your own risk.` Do not put either in a validation
ladder or a CI job. Re-check before trusting this paragraph:

```shell
curl -s https://registry.npmjs.org/insomnia-importers | python3 -c "import json,sys; d=json.load(sys.stdin); l=d['dist-tags']['latest']; print(l, d['time'][l], d['versions'][l].get('deprecated'))"
```

What replaces it is two checks, in this order:

1. **The static check, automated and always available.** `validate_postman_artifacts.py`
   compares `info.schema` against the exact export marker with no flag needed. That string
   comparison is the whole of Insomnia's detection logic, so it fully proves the
   `No importers found for file` failure mode — the one the deprecated converter was run to
   catch.
2. **A real import into Insomnia, by a person, when portability is contractual.** It is the
   only way to observe what the importer silently drops. Record the Insomnia version, because
   this file's table is version-pinned.

When neither has been done, say in the task output that Insomnia portability is
static-checked but not import-verified. Never describe it as verified.
