# Validation And Output Contract

## Validation ladder

Validate from cheapest to strongest:

1. confirm the repository truth and the artifact intent still match
2. when the repo owns a public HTTP API, validate the canonical public contract and its route-and-variant coverage matrix
3. when artifacts are generator-owned, rerun the repo generator and review the generated diff
4. parse the collection and environment JSON locally
5. run `scripts/validate_postman_artifacts.py` when local JSON artifacts exist
6. validate against the official Postman Collection Format v2.1 schema when practical
7. verify variable references, auth inheritance, scripts, and saved responses
8. reject scripts misplaced under `request.event`; executable request scripts belong to the request item's top-level `event`
9. audit response-to-variable dependencies so later requests never require undocumented manual copy/paste
10. compare public paths, operations, statuses, schemas, error codes, and examples across the canonical contract and Postman artifacts
11. for frontend/pentest/SDK handoffs, run strict per-request documentation and saved-response coverage checks
12. run any repo-specific contract, OpenAPI, route-manifest, generated-client, or smoke check that materially reduces risk
13. if local Insomnia import validation is available, use it; otherwise state the gap explicitly
14. when k6 is a target, convert the collection and inspect generated URLs, auth, bodies, variables, checks, and dynamic correlation

## What to check

At minimum, verify:

- the collection is valid JSON
- `info`, `item`, and the v2.1 schema link are present
- `info.schema` uses the conventional Postman export marker `https://schema.getpostman.com/json/collection/v2.1.0/collection.json` so Insomnia can detect the Postman importer
- referenced variables are defined in collection variables, environment files, or explicitly external sources
- committed values do not look like real secrets
- auth inheritance is coherent and not fighting request-level overrides
- examples match the current code and contract closely enough to be trusted
- scripts use readable `pm.*` patterns and avoid deprecated Postman interfaces
- executable scripts exist only at collection, folder, or item `event` scope; no scripts remain under `request.event`
- every response-derived variable used by a later request is declared and captured by an executable, success-guarded script
- runner-only workflow APIs, package-library scripts, Visualizer, Flows, and mock servers are absent or explicitly optional
- saved response examples exist where the task asked for Postman documentation or response examples
- no script is stored under `request.event`
- every response value consumed later is saved by an executable success-guarded script or explicitly documented as operator input
- frontend/pentest handoffs give every request purpose, access boundary, prerequisites, input constraints, response/error semantics, retry/idempotency notes, and relevant security tests
- every request has a coherent saved success response when the collection is required to be a self-contained implementation contract
- every public operation appears in the canonical contract and Postman collection with the same externally reachable method and path
- every meaningful request and response branch is represented by a schema and source-backed example, or is recorded as an explicit implementation/contract gap
- an SDK implementer can derive auth, input/output types, error handling, pagination, idempotency, retries, caching, and asynchronous workflows without reading service code

## Helper script

Use `scripts/validate_postman_artifacts.py` when the repo has local collection and environment files.

For a self-contained implementation contract, enable the strict coverage gates:

```shell
python scripts/validate_postman_artifacts.py collection.json --env environment.json --min-description-chars 120 --require-saved-responses --require-success-guarded-captures
```

The helper is intended to:

- parse Postman JSON
- cross-check variable references
- flag suspicious secret-like committed values
- warn about deprecated script interfaces
- reject executable scripts misplaced under `request.event`
- optionally enforce minimum request-description and saved-response coverage for strict contract collections
- attempt official schema validation when the environment can do so

If the helper cannot perform full schema validation because `jsonschema` is unavailable or the schema fetch fails, record that as a validation gap instead of pretending the check happened.

When local Node/network access is available and Insomnia portability matters, run the same importer family before closing:

```shell
npx --yes insomnia-importers@3.6.0 path/to/collection.postman_collection.json
```

A successful conversion is stronger evidence than generic JSON/schema validation for the `No importers found for file` failure mode.

When k6 compatibility is required, use the current supported Postman-to-k6 conversion path and review the generated JavaScript. Conversion success alone does not prove that Postman response scripts became correct k6 correlation logic; confirm dependent values, checks, auth, cookies, and request ordering explicitly.

## Manual follow-up checks

Do a short manual review for:

- naming clarity
- folder depth
- request descriptions
- error example realism
- pagination and filter notes
- environment placeholder safety
- Insomnia portability risks such as collection-level auth or highly Postman-specific scripts

## Stop-before-close checks

Do not close the task if any of these remain unresolved without being called out:

- contradictory contract sources
- unclear auth behavior with security risk
- undefined critical variables
- saved examples that are clearly stale or fabricated
- unvalidated Insomnia portability assumptions presented as fact

## Output contract

When using this skill, output:

1. files changed
2. what changed in the collection and environment artifacts
3. what changed in the canonical public API contract, or why no public contract was in scope
4. route-and-variant coverage evidence
5. what validation ran
6. what still needs manual follow-up
7. any explicit contract, implementation, Insomnia portability, or schema-validation gaps
