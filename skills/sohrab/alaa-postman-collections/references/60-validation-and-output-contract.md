# Validation And Output Contract

## Validation ladder

Validate from cheapest to strongest:

1. confirm the repository truth and the artifact intent still match
2. when artifacts are generator-owned, rerun the repo generator and review the generated diff
3. parse the collection and environment JSON locally
4. run `scripts/validate_postman_artifacts.py` when local JSON artifacts exist
5. validate against the official Postman Collection Format v2.1 schema when practical
6. verify variable references, auth inheritance, scripts, and saved responses
7. reject scripts misplaced under `request.event`; executable request scripts belong to the request item's top-level `event`
8. audit response-to-variable dependencies so later requests never require undocumented manual copy/paste
9. for frontend/pentest handoffs, run strict per-request documentation and saved-response coverage checks
10. run any repo-specific smoke check that materially reduces risk
11. if local Insomnia import validation is available, use it; otherwise state the gap explicitly
12. when k6 is a target, convert the collection and inspect generated URLs, auth, bodies, variables, checks, and dynamic correlation
9. when k6 use is required, convert the collection and review the generated script for URL, auth, body, variable, check, and correlation correctness

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
3. what validation ran
4. what still needs manual follow-up
5. any explicit Insomnia portability or schema-validation gaps
