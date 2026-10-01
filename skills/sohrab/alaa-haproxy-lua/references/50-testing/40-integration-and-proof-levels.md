# Integration check against a real HAProxy

`haproxy -c -f <config>` loads and compiles every Lua file named by `lua-load` and `lua-load-per-thread`, so it is a real check of the module and not only of the configuration. Verified on HAProxy 2.8.16 on 26 July 2026:

| Fault | Result |
|---|---|
| valid configuration and module | `Configuration file is valid`, exit 0 |
| Lua syntax error in a loaded file | `error in Lua file '…': …: unexpected symbol near 'end'`, exit 1 |
| `lua-load` naming a file that does not exist | `error in Lua file '…': cannot open …: No such file or directory`, exit 1 |

`haproxy -c -f` does **not** execute your handlers, so it proves the module loads and registers, never that it behaves. The smallest configuration that gives the next level of proof is a frontend with `http-request return`, exercised with one request per case; the example bundle is that shape. Config validation discipline for HAProxy generally is owned by `/alaa-haproxy`.

## The proof level an HAProxy Lua change needs

Classify each claim with `/alaa-testing-strategy` `references/40-proof-strength.md` and report it at the level actually reached, never higher. For this kind of change, four levels are reachable and each one is required before a module ships:

1. **Static** — `python3 scripts/check_haproxy_lua.py <module.lua>` exits 0. Reached without running anything. Before trusting that exit code on a branch or a module shape the checker has not seen, run `python3 scripts/check_haproxy_lua.py --self-test`, which re-runs every rule against the committed fixtures in `test/fixtures/`: one red fixture per rule that must report it, plus a converter-shaped and an action-shaped module that must report nothing. A rule with no fixture that makes it fire is decoration, and a clean exit from a checker whose rules were never shown to fire is not evidence.
2. **Unit** — the mock-`core` test exits 0 under the interpreter `haproxy -vv` named, and every failure path has a case.
3. **Local smoke** — `haproxy -c -f` exits 0 on the real configuration.
4. **In-runtime** — a running HAProxy on a loopback bind answers the accepted case and the rejected cases as designed. Reach this level for any handler whose failure decides whether a request is served, because levels 1 to 3 cannot observe the rendered sample.

Anything a live dependency would have to prove — a real backend, a real client population, a real reload — is above what this list reaches; say so rather than implying it was covered.

For scope and related decisions, return to the [parent reference](../50-testing.md).
