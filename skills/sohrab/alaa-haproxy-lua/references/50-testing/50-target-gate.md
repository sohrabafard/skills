# Package gates for a 3.4.6 target

Run these from the skill directory:

```text
python3 scripts/check_haproxy_lua.py examples/haproxy-lua/token-guard.lua
haproxy -c -f <config>
```

The checker exits 0 when no lexical finding stands. It exits 1 on findings and 2 when it could not run.
`haproxy -c -f` compiles every Lua file that the configuration loads. Run it with the target build.
Check that `haproxy -vv` reports HAProxy 3.4.6 and embedded Lua 5.4.8. Another build is a prerequisite mismatch, not a fallback.

Reach proof level 4 with a loopback HAProxy and one request per accepted and rejected case.
Cover both sample modes, nil from a converter or fetch, booleans, sanitized error levels, stale variables, action error denial with `act.DENY`, the 12/13 argument boundary, library dependencies and order. Use HAProxy itself for parser checks.
Run the module's unit test with the interpreter that `haproxy -vv` reported. Deployments with custom HTTP error files still need byte-level Content-Length checks owned by `/alaa-haproxy`.

The lexical checker cannot prove guard conditions, helper reachability, dynamic
registration, dependency closure or every clock or seed alias. HL007 examines
resolved runtime callbacks rather than misclassifying init helpers. HL008 is retired
because coarse timestamp unit conversion is valid. HL002 rejects direct clock seeds
without trusting the presence of an entropy filename as provenance. Treat these
limits as review obligations and retain a runtime probe.

For scope and related decisions, return to the [parent reference](../50-testing.md).
