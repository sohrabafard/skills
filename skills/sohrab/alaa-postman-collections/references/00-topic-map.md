# Alaa Postman Collections Topic Map

Use this file to choose the smallest relevant reference file.

## Read first for every task

- `references/10-scope-and-trigger-rules.md`

## Read whenever the repository owns a public HTTP API

- `references/25-public-api-contract-and-sdk-readiness.md`

## Read by the thing you are about to write

| About to write | Read |
|---|---|
| collection layout, folders, naming, `info` block | `references/20-collection-structure-and-docs.md` |
| a saved example, or deciding which errors a route must show | `references/41-response-contract-and-error-coverage.md` |
| a script, or a value one request must pass to another | `references/42-scripts-and-state-capture.md` |
| assertions on a response | `references/43-response-tests.md` |
| a request description | `references/44-request-documentation-blocks.md` |
| a mock server | `references/45-mock-servers.md` |
| a variable, an environment file, or an auth block | `references/30-variables-auth-and-environments.md` |
| anything that must survive Insomnia import | `references/50-insomnia-compatibility-and-free-plan-rules.md` |
| a merge of several services' collections, or a repo copy of a script from here | `references/70-aggregate-collections-and-consumer-repos.md` |

## Read before closing the task

- `references/60-validation-and-output-contract.md`

## Read when source or version behavior matters

- `references/90-source-map.md`

## Fill-in templates

- `assets/token-capture-post-response.js` — the token or resource-id capture script
- `assets/response-tests-post-response.js` — the assertions on a response
- `assets/request-documentation-block.md` — the eight-heading request description

## Bundled scripts

- `scripts/validate_postman_artifacts.py` — the broad sweep and the mechanical gate for
  every rule in this skill that a script can check. Run it whenever a local collection or
  environment JSON file changed.
- `scripts/audit_collection_contract.py` — the strict pass/fail gate. Run it last on a
  frontend, penetration-test, SDK, or aggregate handoff, and whenever a repository's CI
  already runs it, using that CI's flags.
- `references/60-validation-and-output-contract.md` holds every flag, both exit-code
  tables, and what each failure obliges you to do.

## Working rule

- Load only the smallest files needed for the current repository and task.
- Re-open `references/10-scope-and-trigger-rules.md` if the source of truth becomes
  ambiguous.
