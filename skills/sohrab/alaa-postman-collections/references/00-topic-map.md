# Alaa Postman Collections Topic Map

Use this file to choose the smallest relevant reference file.

## Read first for every task

- `references/10-scope-and-trigger-rules.md`

## Read whenever the repository owns a public HTTP API

- `references/25-public-api-contract-and-sdk-readiness.md`

## Read when you need collection layout or documentation rules

- `references/20-collection-structure-and-docs.md`

## Read when you need variables, auth, or environment guidance

- `references/30-variables-auth-and-environments.md`

## Read when you need examples, scripts, or tests

- `references/40-examples-tests-and-scripts.md`

## Read when you must preserve free-plan or Insomnia portability

- `references/50-insomnia-compatibility-and-free-plan-rules.md`

## Read before closing the task

- `references/60-validation-and-output-contract.md`

## Read when source or version behavior matters

- `references/90-source-map.md`

## Optional helper

- `scripts/validate_postman_artifacts.py`
  - run when a local collection or environment JSON file exists and you want deterministic validation of JSON structure, variable references, secret placeholders, and schema coverage where available

## Working rule

- Load only the smallest files needed for the current repository and task.
- Re-open `references/10-scope-and-trigger-rules.md` if the source of truth becomes ambiguous.
