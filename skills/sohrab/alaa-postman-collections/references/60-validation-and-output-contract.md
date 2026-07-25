# Validation And Output Contract

Read this file before closing any task that touched a Postman artifact.

## Validation ladder

Validate from cheapest to strongest:

1. confirm the repository truth and the artifact intent still match
2. when the repo owns a public HTTP API, validate the canonical public contract and its
   route-and-variant coverage matrix
3. when artifacts are generator-owned, rerun the repo generator and review the diff
4. run `scripts/validate_postman_artifacts.py` with the flags the artifact's purpose calls
   for, below
5. run `scripts/audit_collection_contract.py` as the closing gate on a frontend,
   penetration-test, SDK, or aggregate handoff
6. run any repo-specific contract, OpenAPI, route-manifest, generated-client, or smoke
   check that materially reduces risk
7. run the Insomnia importer check when Insomnia portability matters, or state the gap
8. when k6 is a target, convert the collection and inspect the generated URLs, auth,
   bodies, variables, checks, and dynamic correlation

Do not re-implement a scripted check by eye. Both scripts encode rules that are cheap to
run and easy to miss by reading.

## `scripts/validate_postman_artifacts.py`

The broad sweep and the mechanical enforcement of this skill's rules. Run it every time a
local collection or environment JSON file changed.

Both scripts take every input as an argument, so they run from any working directory and
any install location. Invoke with `python3`; `python` is absent on many hosts and resolves
to Python 2 on some. `$SKILL_DIR` below is the directory holding this skill's `SKILL.md`.

### Always checked, with no flag

- the collection parses, is a JSON object, and has `info`, a non-empty `item` array, and a
  v2.1 schema value
- `info.schema` equals the Postman v2.1 export marker exactly, which is what Insomnia's
  importer compares against
- every `{{variable}}` referenced anywhere is declared in the collection or in a supplied
  environment — pass `--allow-external-var NAME` for one that is intentionally external
- every variable a script writes is declared
- no executable script sits under `request.event`
- one `prerequest` and one `test` event per scope
- no deprecated `postman.*` interface and no `pm.globals.*`
- each saved response has a numeric `code`, a `body`, and an `originalRequest` whose
  method and URL match the request
- no two saved examples on one request share a status and a name
- every committed environment declares `"_postman_variable_scope": "environment"` and no
  duplicate keys
- no committed value in a collection variable, an environment value, an auth block, a
  header, a request body, a saved example, or a script looks like a real credential

### Flags

| Flag | What it requires |
|---|---|
| `--require-saved-responses` | every request has at least one saved example |
| `--require-success-example` | every request has a saved example with a 2xx status |
| `--require-error-examples N` | every request has at least `N` saved examples with a 4xx/5xx status |
| `--require-tests` | every request carries at least one `pm.test` |
| `--require-correlation-assertion` | every request's tests reference `X-Request-Id` |
| `--require-token-capture` | a request whose success example returns a token writes a token variable |
| `--require-success-guarded-captures` | every capture script has an explicit HTTP success guard |
| `--require-doc-section HEADING` | every request description carries that heading; repeatable |
| `--require-secret-typing` | every secret-like environment variable is typed `"type": "secret"` |
| `--min-description-chars N` | every request description is at least `N` characters |

Utility flags: `--skip-schema` on a host with no network access, `--schema-url` to point at
another copy of the schema, `--max-findings N` to cap printed findings per section
(default 200), and `--json` for a machine-readable report to attach as evidence.

The full-strength invocation, for a collection that must stand alone as an implementation
contract:

```shell
python3 "$SKILL_DIR/scripts/validate_postman_artifacts.py" path/to/collection.json \
  --env path/to/environment.json \
  --require-saved-responses \
  --require-success-example \
  --require-error-examples 1 \
  --require-tests \
  --require-correlation-assertion \
  --require-token-capture \
  --require-success-guarded-captures \
  --require-secret-typing \
  --min-description-chars 400 \
  --require-doc-section Purpose \
  --require-doc-section "Flow position" \
  --require-doc-section Request \
  --require-doc-section Response \
  --require-doc-section Access \
  --require-doc-section Errors \
  --require-doc-section "Frontend notes" \
  --require-doc-section "Security notes"
```

### Exit codes

| Code | Meaning | What it obliges you to do |
|---|---|---|
| `0` | no errors; warnings may be present and are printed | resolve each warning or state in the task output which one you accepted and why |
| `1` | at least one rule violation in the collection or an environment | fix the artifact, or the generator input when it is generated, and rerun |
| `2` | input failure: a file could not be read, is not a JSON object, or a flag value is invalid; message on stderr | fix the path or the flag; nothing was validated, so do not report a pass |
| `3` | official Postman v2.1 schema validation ran and failed | fix the structural violation the schema reported; a rule pass does not substitute |
| `4` | a committed artifact carries a value that looks like a real credential | treat as a security incident first: rotate the exposed value, then replace it with a declared variable and a placeholder |

When several apply, the highest-priority code wins in this order: `2`, `4`, `3`, `1`, `0`.
So a run that exits `4` may also have rule errors that are not the exit code — read the
printed sections, not only the code.

Never lower a threshold or drop a flag to make a run pass. When a threshold is genuinely
wrong for the repository, say so in the task output and leave the decision to the owner.

If schema validation was skipped because `jsonschema` is missing or the fetch failed,
report that as a validation gap rather than describing the schema as validated.

## `scripts/audit_collection_contract.py`

The strict gate. Every finding it reports is an error, so exit `1` is blocking; exit `0`
means zero findings. An input it cannot read also exits `1` with a message on stderr, so
read both streams before concluding a collection passed.

It enforces the exact v2.1 export marker, a minimum request-description length, one saved
response per request with a numeric code, a body, and a matching `originalRequest`, event
structure with no duplicate listener in a scope and `script.exec` as an array of strings,
no scripts under `request.event`, no deprecated Postman interfaces, no script writing an
undeclared variable, an explicit success guard on any non-correlation capture, and the
absence of caller-supplied forbidden text. It reports per-collection counts of requests,
saved responses, and scripted requests.

```shell
python3 "$SKILL_DIR/scripts/audit_collection_contract.py" \
  --require-saved-responses \
  --require-success-guarded-captures \
  --min-description-chars 120 \
  --forbid-description-hint "direct backend" \
  --environment path/to/environment.json \
  "aggregate=path/to/collection.json"
```

Add `--json` for a machine-readable report and `--summary-only` to keep the counts and the
exit status while suppressing individual findings.

Run it with the exact flags a repository's CI runs, so a local pass predicts the CI result.

### Why this script does not grow

A repository whose CI runs this script keeps a byte-identical copy, and that copy cannot
be updated from here. New mechanical rules therefore go into
`validate_postman_artifacts.py`, which no repository copies.
`70-aggregate-collections-and-consumer-repos.md` owns the copy-sync rule and the command
that proves the copies match.

### Choosing between them

They overlap deliberately and answer different questions. The validator answers "is this a
correct, safe, portable, complete artifact", where a portability concern can be a warning
you knowingly accept. The auditor answers "does this pass the gate", where everything
blocks. A collection that passes only the validator is valid Postman; a collection that
also passes the auditor is a usable contract.

## External portability checks

These two use tools this skill does not ship. Run each when its target matters, and state
the exact gap when the host cannot run it.

```shell
npx --yes insomnia-importers@3.6.0 path/to/collection.postman_collection.json
```

`50-insomnia-compatibility-and-free-plan-rules.md` explains what a successful conversion
does and does not prove.

For k6, use the current supported Postman-to-k6 conversion path and review the generated
JavaScript. Conversion success alone does not prove that Postman response scripts became
correct k6 correlation logic; confirm dependent values, checks, auth, cookies, and request
ordering explicitly.

## Manual follow-up checks

Neither script judges these. Read them by eye before closing:

- naming clarity and folder depth
- whether an error example is realistic rather than merely present
- whether a test would catch a wrong value and not only a missing one
- whether the request order lets a plain top-to-bottom run succeed
- whether a description answers its eight headings rather than filling them

## Stop-before-close checks

Do not close while any of these is unresolved and uncalled-out:

- contradictory contract sources
- unclear auth behavior with security risk
- undefined critical variables
- saved examples that are clearly stale or fabricated
- unvalidated Insomnia portability assumptions presented as fact

## Output contract

When using this skill, output, in this order:

1. files changed
2. what changed in the collection and environment artifacts
3. what changed in the canonical public API contract, or why no public contract was in scope
4. route-and-variant coverage evidence
5. the exact validation commands run, their exit codes, and their counts
6. what still needs manual follow-up
7. any explicit contract, implementation, Insomnia portability, or schema-validation gap
