# Validation And Output Contract

## Validation ladder

Validate from cheapest to strongest:

1. confirm the repository truth and the artifact intent still match
2. when artifacts are generator-owned, rerun the repo generator and review the generated diff
3. parse the collection and environment JSON locally
4. run `scripts/validate_postman_artifacts.py` when local JSON artifacts exist
5. validate against the official Postman Collection Format v2.1 schema when practical
6. verify variable references, auth inheritance, scripts, and saved responses
7. run any repo-specific smoke check that materially reduces risk
8. if local Insomnia import validation is available, use it; otherwise state the gap explicitly

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
- runner-only workflow APIs, package-library scripts, Visualizer, Flows, and mock servers are absent or explicitly optional
- saved response examples exist where the task asked for Postman documentation or response examples

## Helper script

Use `scripts/validate_postman_artifacts.py` when the repo has local collection and environment files.

The helper is intended to:

- parse Postman JSON
- cross-check variable references
- flag suspicious secret-like committed values
- warn about deprecated script interfaces
- attempt official schema validation when the environment can do so

If the helper cannot perform full schema validation because `jsonschema` is unavailable or the schema fetch fails, record that as a validation gap instead of pretending the check happened.

When local Node/network access is available and Insomnia portability matters, run the same importer family before closing:

```shell
npx --yes insomnia-importers@3.6.0 path/to/collection.postman_collection.json
```

A successful conversion is stronger evidence than generic JSON/schema validation for the `No importers found for file` failure mode.

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
