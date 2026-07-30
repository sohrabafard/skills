# Source Map

Use this file when Postman artifact work depends on current schema behavior, Postman or
Insomnia compatibility, or API source truth.

## Source priority

1. Target repo truth: routes, controllers/handlers, validators, DTOs,
   serializers/resources, OpenAPI files, tests, runtime examples, current docs, and
   existing Postman/Insomnia artifacts.
2. Ala companion skills for the domain: `alaa-services-contract` for the envelopes, codes,
   and required headers; `alaa-trust-gateway-auth` for the trust boundary and `AUTH_*`
   codes; `alaa-repo-docs`, `alaa-security-review`, and the framework skills. Trigger with
   `/name` in Claude Code, `$name` in Codex.
3. Primary tool sources, in this order: the tool's own source code when the behavior is a
   parser or importer detail, then the tool's official documentation, then a release note.
   An importer's source settles what it reads; documentation often omits a silent drop.
4. Community posts, StackOverflow answers, and issue comments only for troubleshooting a
   concrete import, schema, or script failure. An issue report ages: check the current
   source before repeating its claim.

## Primary sources for this skill

Postman:

- Collection Format v2.1 docs — https://schema.postman.com/json/collection/v2.1.0/docs/index.html
- Collection v2.1 JSON Schema, for validation — https://schema.getpostman.com/collection/json/v2.1.0/draft-04/collection.json
- Learning Center — https://learning.postman.com/docs/
- sandbox API reference — https://learning.postman.com/docs/tests-and-scripts/write-scripts/postman-sandbox-api-reference/
- variable scopes and methods — https://learning.postman.com/docs/tests-and-scripts/write-scripts/postman-sandbox-reference/pm-variables/
- authorization types — https://learning.postman.com/docs/use/send-requests/authorization/authorization-types
- mock server matching algorithm — https://learning.postman.com/docs/design-apis/mock-apis/matching-algorithm/
- collection schema versions, including 3.0.0 and which runner reads which — https://learning.postman.com/docs/use/use-collections/collections-schemas
- pricing and Free-plan limits — https://www.postman.com/pricing/

Insomnia:

- Postman collection importer source — `packages/insomnia/src/main/importers/importers/postman.ts` in https://github.com/Kong/insomnia
- Postman environment importer source — `packages/insomnia/src/main/importers/importers/postman-env.ts` in the same repository
- scripting response object source, which settles `code` versus `status` — `packages/insomnia-scripting-environment/src/objects/response.ts` in the same repository. This package was formerly named `insomnia-sdk`; that path now returns 404 and there is no `insomnia-sdk` package on npm, so search the workspace list in the repository's root `package.json` rather than guessing a path.
- releases, for the version a claim is pinned to — https://github.com/Kong/insomnia/releases
- pricing and free-tier limits — https://insomnia.rest/pricing
- scripting surface — https://developer.konghq.com/insomnia/scripts/
- import and export reference — https://developer.konghq.com/insomnia/import-export/
- Postman migration guide — https://developer.konghq.com/how-to/migrate-collections-and-environments-from-postman-to-insomnia/

JSON Schema — https://json-schema.org/

npm registry, for whether a pinned package still exists and is still supported. `insomnia-importers` and `insomnia-inso` are both deprecated; Newman is not:

```shell
curl -s https://registry.npmjs.org/PACKAGE | python3 -c "import json,sys; d=json.load(sys.stdin); l=d['dist-tags']['latest']; print(l, d['time'][l], d['versions'][l].get('deprecated'))"
```

`50-insomnia-compatibility-and-free-plan-rules.md` carries the verification date and the
Insomnia release every claim in it was read at. When a claim there cannot be verified from
source, it says so in place of asserting it.

## Freshness triggers

Re-check the primary sources and repo truth when the task mentions:

- latest or current Postman behavior: collection schema, environment format, test sandbox,
  auth inheritance, script APIs, mock servers
- Insomnia import or export behavior, or a construct's survival across tools
- stale examples, changed route paths, a changed auth flow, new variables, removed
  endpoints, or a changed response envelope
- free-plan compatibility, collection import failures, schema validation failures, or
  secret handling

Re-read Insomnia's importer and scripting-object source rather than its documentation when
the question is "does this construct survive import" or "does this member exist". The source
is the answer; the documentation is a summary of it, and has been observed to be both
incomplete and behind. Read a **release tag**, not `master`: a claim read from `master` cannot
be tied to a version anyone can install, and this skill's compatibility table is
version-pinned.

Before trusting any pinned package version or free-plan number in this skill, re-run the
re-derivation command that sits beside it. Every such claim in this skill carries one.

## Domain-bounded anti-pattern

Bad: restructuring a whole collection to match a blog's preferred folder layout, losing
stable `_postman_id` values and existing examples.

Good: preserve stable IDs, update only stale requests, examples, and scripts, and validate
JSON, variables, schema, and Insomnia portability.
