# Proof and limits

Command from this package: `python3 scripts/check_runtime.py --image haproxy:3.4.6-alpine`.
Observed build: `3.4.6-56332c5`, `+LUA`, embedded Lua `5.4.8`; cached image ID
`sha256:7af8255207ee9964ccb4eec8ce4b7a40b777769665e3ae83897fb01b24d8a43a`.
The image has no Lua CLI; embedded-unit execution uses the exact linked interpreter.
Final expanded gate exited **0**: 34/34 embedded-unit assertions (5000 seeded
property candidates, 309 accepted); five library availability/default cases; seven
negative parser cases (missing os, three late ordering cases, invalid name, mixed
none, 13 arguments); both mode HTTP matrices (nil converter/fetch, false/true,
12 arguments, stale variable versus explicit reset, error-level logs, action error
denial, `act.DENY` and success); token example parsing and four HTTP cases.
One prior attempt failed before tests because Windows checkout/writing produced
CRLF shell input. The runner now normalizes only shell transport to LF on stdin;
one repaired retry passed. Lua/configuration source remains mounted read-only.

Independent verification on **1 October 2026** ran the final runner successfully
at `19:00:12Z` (34/34 embedded checks and all runtime probes); the synthetic cleanup
suite passed 4/4 at `18:59:44Z`. Its 38-file before/after manifests matched.
Repository archive: `<repo>/outputs/20261001-haproxy-346/verification/verification-report.md`;
raw output and input manifests are beside that receipt. This is a repository
evidence path, not an installed-package dependency. Later documentation-only
clustering does not assert that its changed Markdown matches that earlier manifest.

`python3 scripts/check_haproxy_lua.py --self-test`: 16/16 cases passed. The original
HL008 fixture now asserts valid coarse unit conversion; init I/O is a green
regression and the clock-seed fixture includes a misleading entropy path literal.
`python3 scripts/check_haproxy_lua.py examples/haproxy-lua/token-guard.lua` is the
production-example static gate; observed exit 0 with zero findings. The independent repository verifier owns broad
pack checks and final receipt capture; these focused results are not those gates.


The checker is lexical, never a replacement HAProxy parser. CPU clock, error-level
and registration checks are Alaa policy conventions; upstream execution and library
restrictions are identified separately. Current nil and error probes replace no
historical numeric timing/entropy captures. No live gateway behavior, egress
failure, load/performance, filter/CLI/task lifecycle, drain or deployment is proved.

For scope and related decisions, return to the [parent reference](../SOURCES.md).
