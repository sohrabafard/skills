# Gate Register

Each row is a predicate, the command that evaluates it, and the artifact it inspects. **No
provider syntax appears here.** How a gate is expressed on a runner — the job graph, `rules:`,
`needs:`, artifact retention, the runner image reference — is decided by `/alaa-gitlab-ci-cd`, which owns how a gate is expressed and decides no gate. This file decides
the gates and expresses none of them.

## The HAProxy gates

| # | Predicate | Command | Artifact |
|---|---|---|---|
| G1 | The effective config parses under the binary that will run it. | `haproxy -c -f <cfg>` | the rendered config, plus every map file and certificate path it references — a map or certificate missing at check time is a startup failure, and `-c` reports it |
| G2 | The running build has the features the config uses. | `haproxy -vv` | the feature block, asserted against the directives the config uses: QUIC before a `quic4@` bind, kTLS before `ktls on`, Lua before any `lua-load`, the Prometheus exporter before `use-service prometheus-exporter` |
| G3 | Every `defaults` section is named and every proxy selects one with `from`. | `python3 scripts/check_defaults_scope.py <path>` | any `.cfg` file, or a directory of them |
| G4 | Every shipped example parses under its declared branch, has the build features it declares, and states its own contract. | `python3 scripts/check_examples.py --haproxy <path>` | `examples/haproxy/*.cfg` and `examples/kubernetes/*.yaml` |
| G5 | The pinned branch and image facts still match the official sources. | the re-derivation commands in `SOURCES.md` | `references/10-version-and-branch.md` and every image tag under `examples/` |
| G6 | Standalone HTTP response Content-Length matches raw body bytes. | `python3 scripts/check_http_error_bytes.py <response.http>` | effective checkout bytes, including header separator, newline encoding and UTF-8; also run G1 for HTTP response validity |
| G7 | A dynamic-backend change survives its required routing, drain, removal and recovery scenarios. | `python3 scripts/check_runtime_3_4.py --docker-image <cached-3.4.6-alpine-image>` | isolated template/map/server lifecycle; extend scenario proof for the real controller, health transitions and concurrent reads |

G1 and G2 must run against a binary **of the branch that will serve production**. A config checked
on 3.2 and deployed on 3.4 has not been checked; every breaking change in
`10-version-and-branch.md` is invisible to the wrong binary.

## Gates this skill does not own

Named here only so a pipeline that needs them knows where they are decided:

| Predicate | Owner |
|---|---|
| the chart renders, and lints | `/alaa-k8s-helm` |
| the rendered manifests are accepted by the API server | `/alaa-k8s-helm` |
| the image builds, is scanned, and is pinned | `/alaa-docker-production` |
| a frontend delivery gate — the predicate, the command, the artifact | `/alaa-frontend-devops` |
| the job graph, stages, artifacts and runner images that express any of the above | `/alaa-gitlab-ci-cd` |
| the local invocation that must give the same verdict as the runner | `/alaa-makefile` |
| what proof strength a change requires before it may ship | `/alaa-controlled-ops` |

Two CI files formerly shipped in this skill — a GitHub Actions workflow and a GitLab CI snippet —
have been retired for exactly this reason: they were provider YAML, their HAProxy substance was
four lines out of fifty, and it is stated above as G1 and G2 instead. The obligation they carried
survives as this register; the obligation to keep a provider example in this repository does not,
because it is what manufactured the boundary violation.

## Checker contract

The defaults-scope and examples checkers have these contracts:

1. `--help` describes the rules and the exit codes.
2. `--self-test` runs against fixtures shipped in `scripts/fixtures/` and passes from a fresh
   checkout with no network and no HAProxy binary.
3. Exit codes distinguish outcomes: **`0` clean, `1` findings, `2` could not run.** A missing
   binary or an unreadable path is `2`, never `0`. Syntax/contract findings are
   `1`; a checker that cannot inspect its input does not report it clean.
4. Pure Python 3 with the standard library only, so they run on Windows as well as on Linux and
   macOS. Every file is read as text with newline translation, so a CRLF checkout does not leave a
   carriage return on the last field of a parsed line.
5. Each resolves its own location by ascending from its own directory until it finds `SKILL.md`,
   rather than by counting parent directories, and writes any temporary file to the system
   temporary directory rather than inside the repository.

Run them:

```
python3 scripts/check_defaults_scope.py --self-test
python3 scripts/check_defaults_scope.py examples/haproxy
python3 scripts/check_examples.py --self-test
python3 scripts/check_examples.py --structure-only
python3 scripts/check_examples.py --haproxy <path-to-haproxy>
python3 scripts/check_examples.py --docker-image <cached-image>
python3 scripts/check_http_error_bytes.py --self-test
python3 scripts/check_http_error_bytes.py <response.http>
python3 scripts/check_runtime_3_4.py --docker-image <cached-3.4.6-alpine-image>
python3 scripts/test_runner_contracts.py
```

Commands are relative to the package directory. The Docker parser adapter uses
host Python and OpenSSL to generate temporary fixture inputs and invokes the
cached binary with `--pull never`; the image need not contain Python. It checks
the effective ConfigMap config as well as `.cfg` examples. External-path fixtures
and loopback DNS are parser inputs, not certificate or resolver operation proof.

The byte checker reads bytes without newline conversion or repair. Its eight
fixtures cover LF, CRLF, UTF-8, checkout length mismatch, duplicate/missing length,
absurd decimal length and leading zeroes. A `.gitattributes` rule preserves bytes. Exit 1 means a
length/shape finding; exit 2 means unreadable input.

The runtime probe requires a cached HAProxy 3.4.6 Alpine image, Docker and its
`sh`/`nc`/`wget` and `+LUA` for a controlled delayed streaming origin. It has
`--help`, not `--self-test`. It uses read-only fixtures,
one CPU, 256 MiB, no network access or published ports and cleans up its temporary
container. Positive origin routing, unpublished fallback, preserved active-stream
drain, successful wait replies, deletion refusal,
reload loss and reconstruction must all pass before claiming its lifecycle proof.
Only the observed health-transition HTTP 503 is tolerated within a bounded
readiness deadline; other operation errors fail immediately. Exit 1 is an
assertion failure, exit 2 an unavailable prerequisite/operation. Current task
failures are preserved in `SOURCES.md`; a shipped harness is not evidence it passed.

`test_runner_contracts.py` runs twelve synthetic cases without Docker or scratch
writes: environment isolation, owned-name cleanup after success/failure/timeout,
cleanup error handling, lifecycle creation diagnostics, exact patch matching,
wait replies, active-stream counter selection, parser warning rejection and absurd decimal length handling.
Only explicitly constructed parser fixture variables reach Docker arguments;
inherited `HAPROXY_*` values are not forwarded. Unique owned names permit bounded,
return-code-checked cleanup even when Docker creation times out.

`check_examples.py` without `--structure-only` requires an HAProxy binary and exits `2` when one
is absent, or when an example could not be parsed because the binary's branch is older than the
example's `# Minimum branch:` header or its feature list does not satisfy the example's
`# Requires-build:` header. `--allow-skips` downgrades that second case to a `SKIPPED` line.

The `# Requires-build:` header is gate G2 written into the file: it names the `haproxy -vv` feature
tokens the build must have, and, with a leading `!`, the tokens it must not have. A file needing a
real QUIC API rather than the OpenSSL compatibility layer declares
`# Requires-build: QUIC !QUIC_OPENSSL_COMPAT`.
Alternative compression providers may be declared `ZLIB|SLZ`; either positive
feature satisfies that requirement. OpenTelemetry needs filter-list inspection,
because the `OT` feature token denotes OpenTracing.

Unresolved warnings from `haproxy -c -f` are `HP-EX-WARNING` findings and block the
gate with exit1, even when the parser exits0. A warning can indicate an ineffective
control today. No deprecation exception is currently approved. Accept one only with
an exact message and branch, authoritative support/safety evidence, and a checker
fixture; matching the word deprecated alone never grants an exception.
