# Pre-repair counterexamples

Observed by the parent during the independent review on 2026-10-18, before the corrective run.
These experiments establish the failure mechanisms; they do not prove that an agent follows the repaired instructions.
The fixtures used a temporary module, a private build cache, the installed Go toolchain,
`GOTOOLCHAIN=local`, `GOPROXY=off`, `GOSUMDB=off`, `GOWORK=off`, `GOENV=off`, empty `GOFLAGS`, and `GOMAXPROCS=2`.
No dependency download or repository source mutation was involved.

| Case | Fixture and command | Observed result |
|---|---|---|
| Cached external-dependency result | In `<fixture>/external`, a test reads a loopback HTTP endpoint. Run `go test -p 2 .`, change only the server response from `ok` to `bad`, then repeat the command. | First run exit 0; second run exit 0 with `(cached)`, without observing the changed dependency. |
| Fresh external-dependency result | On the same changed endpoint, run `go test -p 2 -count=1 .`. | Exit 1: `dependency="bad" err=<nil>`. Bypassing result caching exposes the failure while retaining build caching. |
| Missing executable entrypoint | In `<fixture>/mainpkg`, `package main` defines and tests an ordinary function but has no application `main`. Run `go test -p 2 .`, then `go build -p 2 .`. | Test exit 0; build exit 1: `function main is undeclared in the main package`. |
| Negated build constraint | In `<fixture>/tags`, put `unit_test.go` behind `!integration` and `integration_test.go` behind `integration`. Run `go list -f '{{.TestGoFiles}}' .`, then `go list -tags=integration -f '{{.TestGoFiles}}' .`. | Normal selection: `[unit_test.go]`; tagged selection: `[integration_test.go]`. The tagged configuration is not a superset. |
| Incomplete Quasar shell command | Replace the small-UI snippet's package-manager and changed-file placeholders with `pnpm` and `src/App.vue`; feed that one command to Git Bash with `--noprofile --norc -n`. | Exit 2: `syntax error: unexpected end of file`. The trailing comment consumes the build command after `&&`. |

The initial sandboxed fixture attempt failed before test execution with a temporary-directory write-permission error.
The same bounded fixture script succeeded through the exact escalated retry. The test failures in this table are expected counterexamples, not failed verification of the corrected candidate.
