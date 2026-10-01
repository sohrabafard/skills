# Reproducible 3.4.6 package gate

From this package run:

```text
python3 scripts/check_haproxy_lua.py --self-test
python3 scripts/check_haproxy_lua.py examples/haproxy-lua/token-guard.lua
python3 -B test/test_runtime_runner.py
python3 scripts/check_runtime.py --image <cached-3.4.6-image>
```

The runtime runner requires Docker access, the already-cached target image and its
BusyBox shell/wget. It never pulls: `--pull=never`, no external network, one CPU,
128 MiB, read-only package mount, no host ports, scratch only inside the disposable
container. Version checks require HAProxy 3.4.6 and embedded Lua 5.4.8; another
build is a prerequisite mismatch (exit 2), not an implicit fallback. The exact-image
unit test uses an isolated Lua environment and mock core while HAProxy loads it;
this is embedded-unit proof, not a standalone Lua CLI run. The host test process
has a 90-second deadline. Exit 0 means assertions passed, 1 means failure, 2 means
missing runtime/prerequisite. Preserve stderr for a nonzero result before repair.

The runner checks both sample modes, nil from converter/fetch, booleans, sanitized
error levels, stale variables, action error denial and `act.DENY`, 12/13 argument
boundaries, library dependencies/order and the complete token example. Parser
checks use HAProxy itself. Fixtures use generated responses, so no hand-written
Content-Length body crosses CRLF conversion. Deployments with custom HTTP error
files still need byte-level Content-Length checks owned by `/alaa-haproxy`.

The lexical checker cannot prove guard conditions, helper reachability, dynamic
registration, dependency closure or every clock/seed alias. HL007 now examines
resolved runtime callbacks rather than misclassifying init helpers; HL008 is retired
because coarse timestamp unit conversion is valid. HL002 rejects direct clock seeds
without trusting the presence of an entropy filename as provenance. Treat these
limits as review obligations and retain the runtime gate.

For scope and related decisions, return to the [parent reference](../50-testing.md).
