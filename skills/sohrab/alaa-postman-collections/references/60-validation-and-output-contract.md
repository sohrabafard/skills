# Validation And Output Contract

Read this file before validating a Postman artifact.

## Offline artifact validation

Validate local artifacts with the bundled scripts and already-installed tools. Use local
Postman tools, Newman, or the Postman Collection SDK where applicable. Keep collection,
environment, and credential data local. Do not use online validators, cloud workspaces,
login, upload, or sync for validation. Use installed executables directly. Do not use
package runners that can download or install tools.

### Offline schema mode

Use `--schema-url file:///absolute/path/to/collection-schema.json --require-schema` when
an authentic local Postman v2.1 schema and installed `jsonschema` are available. Use a copy
whose references resolve locally.

Require this schema mode in CI and wherever the repository requires schema validation.
If a required input is unavailable, report the schema gate blocked and continue the other
local checks. For an ad hoc check where schema validation is optional, use `--skip-schema`
when an input is unavailable and report the reason.

Use the explicit flag even on a connected host. The script's default schema URL is remote.
The canonical `info.schema` export marker remains unchanged. Record mechanical checks,
official schema validation, and collection execution as separate results.

## Validation ladder

Validate from cheapest to strongest:

1. confirm the repository truth and the artifact intent still match
2. when the repo owns a public HTTP API, confirm parity with the canonical public contract
   and its route-and-variant coverage matrix
3. when artifacts are generator-owned, rerun the repo generator and review the diff
4. run `scripts/validate_postman_artifacts.py` with the flags the artifact's purpose calls
   for, below
5. run `scripts/audit_collection_contract.py` as the closing gate on a frontend,
   penetration-test, SDK, or aggregate handoff
6. run any repo-specific contract, OpenAPI, route-manifest, generated-client, or smoke
   check that materially reduces risk
7. follow [Executing the collection](#executing-the-collection) and report the result for
   this task
8. static-check Insomnia portability, and record whether a real import was done
9. when k6 is a target, convert the collection and inspect the generated URLs, auth,
   bodies, variables, checks, and dynamic correlation

Do not re-implement a scripted check by eye. Both scripts encode rules that are cheap to
run and easy to miss by reading.

## `scripts/validate_postman_artifacts.py`

The broad sweep and the mechanical enforcement of this skill's rules. Run it every time a
local collection or environment JSON file changed.

Both scripts take every input as an argument, so they run from any working directory and
any install location.

**Python 3.9 is the floor.** The validator calls `str.removeprefix`, added in 3.9, so an
older interpreter raises `AttributeError` part-way through a run, which reads as a crash in
the collection rather than in the interpreter. Check `python3 -V` on an unfamiliar host.

**Launcher.** Use `python3`, never `python`, which is absent on many hosts and is Python 2 on
some. `$SKILL_DIR` below is the directory holding this skill's `SKILL.md`.

### Always checked, with no flag

- the collection parses, is a JSON object, and has `info`, a non-empty `item` array, and a
  v2.1 schema value
- the collection contains at least one request item, not only folders. A collection of empty
  folders satisfies the `item` check and gives every `--require-*` flag nothing to fire on,
  so without this the strongest invocation reports a pass on an artifact with no requests in
  it
- `info.schema` equals the Postman v2.1 export marker exactly, which is what Insomnia's
  importer compares against
- every `{{variable}}` referenced anywhere is declared in the collection or in a supplied
  environment — pass `--allow-external-var NAME` for one that is intentionally external
- every variable a script writes is declared
- no executable script sits under `request.event`
- one `prerequest` and one `test` event per scope
- no deprecated `postman.*` interface and no `pm.globals.*`
- each saved response has a numeric `code`, a `body`, and an `originalRequest` whose
  method and endpoint URL (scheme, host, and path) match the request. A named response may
  use a different query variant when its `originalRequest` records the query that actually
  produces that example
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
| `--require-schema` | official schema validation actually ran; a skip becomes exit `2` |
| `--forbid-pinned-vendor-identifier` | no committed collection or environment value pins a vendor model, engine, deployment, or embedding identifier |

Use `--max-findings N` to cap findings per section (default 200). Use `--json` for a
machine-readable report with `schema_skipped`.

Use these mechanical flags for a standalone implementation contract. This example uses
the optional schema skip. For CI or a local schema, substitute the flags from
[Offline schema mode](#offline-schema-mode).

```shell
python3 "$SKILL_DIR/scripts/validate_postman_artifacts.py" path/to/collection.json \
  --skip-schema \
  --env path/to/environment.json \
  --require-saved-responses \
  --require-success-example \
  --require-error-examples 1 \
  --require-tests \
  --require-correlation-assertion \
  --require-token-capture \
  --require-success-guarded-captures \
  --require-secret-typing \
  --forbid-pinned-vendor-identifier \
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

### What a run costs

The stated bound: one pass over the document plus a bounded number of regex passes per
request item, so work is linear in document bytes, and the whole collection is held in memory
as parsed JSON, so peak memory is a small multiple of file size. Treat a run whose cost is not
linear in file size as a defect in the script.

Aggregates are the artifacts that get large — a live gateway aggregate of roughly 8 MB over 73
requests is the size this skill was built for. Two costs grow there: undeclared-variable
detection scans every string including prose and example bodies, so it tracks total bytes
rather than request count. Schema validation processes the local schema and collection.

`alaa-algorithms-data-structures` (`/alaa-algorithms-data-structures`,
`$alaa-algorithms-data-structures`) owns complexity budgets and structure choice. Read it
before adding a check that walks items inside another walk over items, or before changing a
generator to emit a collection whose size grows with tenants, routes, or history.

### Exit codes

| Code | Meaning | What it obliges you to do |
|---|---|---|
| `0` | no errors; warnings may be present and are printed | resolve each warning or state in the task output which one you accepted and why |
| `1` | at least one rule violation in the collection or an environment | fix the artifact, or the generator input when it is generated, and rerun |
| `2` | could not run: a file could not be read, is not a JSON object, a flag value is invalid, or `--require-schema` was passed and schema validation could not run; message on stderr | fix the path, the flag, or the host; the artifact was not fully validated, so do not report a pass |
| `3` | official Postman v2.1 schema validation ran and failed | fix the structural violation the schema reported; a rule pass does not substitute |
| `4` | a committed artifact carries a value that looks like a real credential | treat as a security incident first: rotate the exposed value, then replace it with a declared variable and a placeholder |

When several apply, the highest-priority code wins in this order: `2`, `4`, `3`, `1`, `0`.
So a run that exits `4` may also have rule errors that are not the exit code — read the
printed sections, not only the code.

Never lower a threshold or drop a flag to make a run pass. When a threshold is genuinely
wrong for the repository, say so in the task output and leave the decision to the owner.

If `jsonschema` is unavailable or the schema cannot be read, the validator skips that
check and prints a warning. With `--require-schema` the skip exits `2`. With
`--skip-schema`, exit `0` covers the local mechanical checks only.

## `scripts/audit_collection_contract.py`

The strict gate. Every finding it reports is an error, so exit `1` is blocking and exit `0`
means zero findings.

| Code | Meaning | What it obliges you to do |
|---|---|---|
| `0` | no findings | nothing |
| `1` | at least one finding; all findings block | fix the artifact, or the generator input when it is generated, and rerun |
| `2` | could not run: an input file could not be read or is not a JSON object; message on stderr | fix the path; no collection was audited, so do not report a pass |

Earlier versions of this script returned `1` for a file it could not read, and an earlier
version of this file documented that as intended. It was not: a harness that cannot tell
"the collection is bad" from "the gate never ran" records a missing file as a fixable finding
and a broken gate as a broken collection. If a consumer repository still holds a copy that
exits `1` on an unreadable input, that copy predates this correction —
`70-aggregate-collections-and-consumer-repos.md` owns the re-sync.

**The auditor's capture guard is weaker than the validator's, on purpose.** The auditor
tests for a success guard by searching the test script's text, which cannot distinguish a
guarded write from a mandated `pm.expect(pm.response.code).to.eql(200)` assertion elsewhere in
the same script. The validator's `--require-success-guarded-captures` is structural and does
distinguish them. The auditor keeps the textual form because every consumer copy would have
to be re-synced with a new analyser, so **the validator is the gate that proves the guard**;
treat an auditor pass on that rule as no evidence either way.

It enforces the exact v2.1 export marker, a minimum request-description length, one saved
response per request with a numeric code, a body, and an `originalRequest` with the same method
and endpoint URL while allowing accurately recorded query variants, event
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

## Choosing between the scripts

The validator checks local artifact rules and reports warnings. The auditor treats each
finding as blocking. Use the contract parity and coverage checks to establish completeness.

## Executing the collection

Execute the collection when a compatible Newman and a local test runtime or fixture are
available. Check that requests, scripts, and their inputs target that environment before
running them. For assertion design, follow `43-response-tests.md`.

```shell
newman run path/to/collection.json \
  --environment path/to/environment.json \
  --reporters cli
```

Newman exits `0` when every request and assertion passed and non-zero when any assertion
failed or any request errored. A non-zero exit is a finding to fix; a run that could not start
— unreachable host, missing environment values — is a could-not-run to report, never a pass.

If no compatible local runner or environment is available, report why execution was
skipped. Record the installed runner version when execution runs.
`50-insomnia-compatibility-and-free-plan-rules.md` owns the v2.1 compatibility decision.

## Other external checks

`50-insomnia-compatibility-and-free-plan-rules.md` owns Insomnia portability, including the
fact that no maintained command-line Postman-to-Insomnia converter exists and what to run
instead.

For k6, use an installed Postman-to-k6 converter and review the generated
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
3. what changed in the canonical public API contract, or which skill owns it and what the
   parity check against it reported
4. route-and-variant coverage evidence
5. the exact validation commands run, their exit codes, and their counts
6. the local collection execution result and runner version, or why execution was skipped
7. whether Insomnia portability was static-checked only or import-verified, and on which
   Insomnia version
8. whether official schema validation ran or was skipped, and why
9. what still needs manual follow-up
10. any explicit contract, implementation, Insomnia portability, or schema-validation gap
