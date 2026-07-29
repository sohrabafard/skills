# Gate Register

Each row is a predicate, the command that evaluates it, and the artifact it inspects. **No
provider syntax appears here.** How a gate is expressed on a runner — the job graph, `rules:`,
`needs:`, artifact retention, the runner image reference — is decided by `/alaa-gitlab-ci-cd`
(`$alaa-gitlab-ci-cd`), which owns how a gate is expressed and decides no gate. This file decides
the gates and expresses none of them.

## The HAProxy gates

| # | Predicate | Command | Artifact |
|---|---|---|---|
| G1 | The effective config parses under the binary that will run it. | `haproxy -c -f <cfg>` | the rendered config, plus every map file and certificate path it references — a map or certificate missing at check time is a startup failure, and `-c` reports it |
| G2 | The running build has the features the config uses. | `haproxy -vv` | the feature block, asserted against the directives the config uses: QUIC before a `quic4@` bind, kTLS before `ktls on`, Lua before any `lua-load`, the Prometheus exporter before `use-service prometheus-exporter` |
| G3 | Every `defaults` section is named and every proxy selects one with `from`. | `python3 scripts/check_defaults_scope.py <path>` | any `.cfg` file, or a directory of them |
| G4 | Every shipped example parses under its declared branch, has the build features it declares, and states its own contract. | `python3 scripts/check_examples.py --haproxy <path>` | `examples/haproxy/*.cfg` and `examples/kubernetes/*.yaml` |
| G5 | The pinned branch and image facts still match the official sources. | the re-derivation commands in `SOURCES.md` | `references/10-version-and-branch.md` and every image tag under `examples/` |

G1 and G2 must run against a binary **of the branch that will serve production**. A config checked
on 3.2 and deployed on 3.4 has not been checked; every breaking change in
`10-version-and-branch.md` is invisible to the wrong binary.

## Gates this skill does not own

Named here only so a pipeline that needs them knows where they are decided:

| Predicate | Owner |
|---|---|
| the chart renders, and lints | `/alaa-k8s-helm` (`$alaa-k8s-helm`) |
| the rendered manifests are accepted by the API server | `/alaa-k8s-helm` (`$alaa-k8s-helm`) |
| the image builds, is scanned, and is pinned | `/alaa-docker-production` (`$alaa-docker-production`) |
| a frontend delivery gate — the predicate, the command, the artifact | `/alaa-frontend-devops` (`$alaa-frontend-devops`) |
| the job graph, stages, artifacts and runner images that express any of the above | `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`) |
| the local invocation that must give the same verdict as the runner | `/alaa-makefile` (`$alaa-makefile`) |
| what proof strength a change requires before it may ship | `/alaa-controlled-ops` (`$alaa-controlled-ops`) |

Two CI files formerly shipped in this skill — a GitHub Actions workflow and a GitLab CI snippet —
have been retired for exactly this reason: they were provider YAML, their HAProxy substance was
four lines out of fifty, and it is stated above as G1 and G2 instead. The obligation they carried
survives as this register; the obligation to keep a provider example in this repository does not,
because it is what manufactured the boundary violation.

## Checker contract

Both checkers in `scripts/` satisfy the same five properties:

1. `--help` describes the rules and the exit codes.
2. `--self-test` runs against fixtures shipped in `scripts/fixtures/` and passes from a fresh
   checkout with no network and no HAProxy binary.
3. Exit codes distinguish outcomes: **`0` clean, `1` findings, `2` could not run.** A missing
   binary, an unreadable path or an unparsable input is `2`, never `0`. A checker that cannot
   inspect its input does not report the input clean.
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
python3 scripts/check_examples.py --haproxy /usr/sbin/haproxy
```

`check_examples.py` without `--structure-only` requires an HAProxy binary and exits `2` when one
is absent, or when an example could not be parsed because the binary's branch is older than the
example's `# Minimum branch:` header or its feature list does not satisfy the example's
`# Requires-build:` header. `--allow-skips` downgrades that second case to a `SKIPPED` line.

The `# Requires-build:` header is gate G2 written into the file: it names the `haproxy -vv` feature
tokens the build must have, and, with a leading `!`, the tokens it must not have. A file needing a
real QUIC API rather than the OpenSSL compatibility layer declares
`# Requires-build: QUIC !QUIC_OPENSSL_COMPAT`.

Warnings from `haproxy -c -f` are printed as `NOTE` lines rather than counted as findings, because
a warning is a fix due before the branch after next and a finding is a fix due now.
