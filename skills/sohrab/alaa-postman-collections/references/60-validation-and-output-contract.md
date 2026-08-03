# Validation And Output Contract

Read this file before closing any task that touched a Postman artifact.

## Validation ladder

Validate from cheapest to strongest:

1. confirm the repository truth and the artifact intent still match
2. when the repo owns a public HTTP API, confirm parity with the canonical public contract
   and its route-and-variant coverage matrix
3. when artifacts are generator-owned, rerun the repo generator and review the diff
4. run `scripts/selftest.py --self-test` whenever either bundled script changed, before
   trusting anything either one reports
5. run `scripts/validate_postman_artifacts.py` with the flags the artifact's purpose calls
   for, below
6. run `scripts/audit_collection_contract.py` as the closing gate on a frontend,
   penetration-test, SDK, or aggregate handoff
7. run any repo-specific contract, OpenAPI, route-manifest, generated-client, or smoke
   check that materially reduces risk
8. execute the collection with Newman when a runnable environment exists, per the section
   below, or record that the tests have never been executed
9. static-check Insomnia portability, and record whether a real import was done
10. when k6 is a target, convert the collection and inspect the generated URLs, auth,
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

**The launcher differs by platform, and the wrong one fails silently on Windows.** On macOS
and Linux use `python3`, never `python`, which is absent on many hosts and is Python 2 on
some. On Windows use `py -3`: Windows ships a Microsoft Store alias named `python3` that
opens the Store page and exits without running anything, so a CI step invoking `python3`
there reports no error and validates nothing. Every command block in this skill is written
with `python3`; substitute `py -3` on Windows. `scripts/selftest.py` sidesteps this for its
child processes by re-invoking through `sys.executable`. `$SKILL_DIR` below is the directory
holding this skill's `SKILL.md`; it interpolates in PowerShell and POSIX shells, not `cmd.exe`.

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
rather than request count, and schema validation fetches a separate document over the network,
usually the slowest step and the one `--require-schema` makes non-optional in CI.

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

Schema validation is skipped, with a warning, when `jsonschema` is not installed or the
schema URL cannot be fetched. **A skip is not a pass**, and without a flag the run still
exits `0`, so an air-gapped CI runner would report success while the strongest structural
check never ran. Pass `--require-schema` in any CI job: it turns a skip into exit `2`, which
the harness records as could-not-run rather than clean. Locally, either pass it or report the
skip as a validation gap; never describe the schema as validated when it was skipped.

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

## `scripts/selftest.py`

Runs both bundled scripts against the committed fixtures in `test/fixtures/`, which include a
violating input for every assertion those scripts make. Run it whenever either script or a
fixture changed.

```shell
python3 "$SKILL_DIR/scripts/selftest.py" --self-test
```

| Code | Meaning | What it obliges you to do |
|---|---|---|
| `0` | every case behaved as expected | nothing |
| `1` | a case FAILED: the target ran and gave the wrong answer | fix the script or the expectation, and rerun |
| `2` | a case was BLOCKED, or the harness itself could not run | fix the host or the paths; a blocked case is no evidence about the scripts |

A case whose target exits `2` when `2` was not the expected code records **BLOCKED, not
FAIL**, and any blocked case makes the whole run exit `2`. A CI gate must therefore never read
a broken checker as a red test. Adding a rule to either script without adding a fixture that
violates it leaves that rule unproven; `SKILL.md` states this as a maintenance rule.

### Choosing between them

They overlap deliberately and answer different questions. The validator answers "is this a
correct, safe, portable, complete artifact", where a portability concern can be a warning
you knowingly accept. The auditor answers "does this pass the gate", where everything
blocks. A collection that passes only the validator is valid Postman; a collection that
also passes the auditor is a usable contract.

## Executing the collection

Every check above is static. A static check proves the artifact is well-formed; it cannot
prove a single assertion in it would fail against a broken implementation, which is the
property `43-response-tests.md` exists to produce. Execute the collection when a runnable
environment exists:

```shell
npx --yes newman@6.2.2 run path/to/collection.json \
  --environment path/to/environment.json \
  --reporters cli
```

Newman exits `0` when every request and assertion passed and non-zero when any assertion
failed or any request errored. A non-zero exit is a finding to fix; a run that could not start
— unreachable host, missing environment values — is a could-not-run to report, never a pass.

- **Execution is reportable, not required.** A repository with no runnable environment must
  still be able to use this skill. When the collection was not executed, say so in the output
  contract below rather than leaving the tests' status unstated.
- **Newman runs 2.1 and cannot run 3.0**; a 3.0 collection needs the Postman CLI.
  `50-insomnia-compatibility-and-free-plan-rules.md` explains why this skill pins 2.1.

Re-derive the pin before changing it:

```shell
curl -s https://registry.npmjs.org/newman | python3 -c "import json,sys; d=json.load(sys.stdin); l=d['dist-tags']['latest']; print(l, d['time'][l], d['versions'][l].get('engines'))"
```

Newman 6.2.2 was published 16 January 2026 and declares `node >=16`; verified 30 July 2026.

## Other external checks

`50-insomnia-compatibility-and-free-plan-rules.md` owns Insomnia portability, including the
fact that no maintained command-line Postman-to-Insomnia converter exists and what to run
instead.

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
3. what changed in the canonical public API contract, or which skill owns it and what the
   parity check against it reported
4. route-and-variant coverage evidence
5. the exact validation commands run, their exit codes, and their counts
6. whether the collection was executed with Newman, and its result; when it was not executed,
   say so rather than leaving the tests' status unstated
7. whether Insomnia portability was static-checked only or import-verified, and on which
   Insomnia version
8. whether official schema validation ran or was skipped, and why
9. what still needs manual follow-up
10. any explicit contract, implementation, Insomnia portability, or schema-validation gap
