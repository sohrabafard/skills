# Testing

An HAProxy Lua module is ordinary Lua with one global injected. That single fact makes it unit-testable outside HAProxy, and it is the highest-leverage technique in this skill: it turns "deploy and watch the logs" into a test that runs in milliseconds.

What makes a test a test, which layer a behaviour belongs at, and how strong a given proof is, are owned by `/alaa-testing-strategy` (`$alaa-testing-strategy`). This file states only what is specific to HAProxy Lua.

## Unit tests with a mock `core`

HAProxy injects one global, `core`. Set it yourself before loading the module, and the module's registration branch runs against your table instead of HAProxy's.

```lua
local mock_core = { converters = {}, fetches = {}, logs = {} }

function mock_core.register_converters(name, handler)
    mock_core.converters[name] = handler
end

function mock_core.log(level, message)
    mock_core.logs[#mock_core.logs + 1] = { level = level, message = message }
end

_G.core = mock_core

local module = dofile("token-guard.lua")
```

This works only if the module obeys two rules, which is the practical reason they exist:

1. **Every `core` reference in the file body sits inside the `if core ~= nil and core.register_… ~= nil then` guard.** An unguarded `core.register_converters(...)` at file scope raises `attempt to index a nil value (global 'core')` the moment a test loads the file.
2. **The module returns its table.** `return M` at the end of the file gives the test direct access to the functions, so a test can call `M.validate` without going through the registration table.

The mock is a double, and a double can drift from the real object. Record what binds it: here, the binding is that the registration names asserted in the test are the same strings the configuration uses under the `lua.` prefix, and `haproxy -c -f` fails when they disagree.

## Which runner

**Use the interpreter that `haproxy -vv` reports on the `Built with Lua version` line.** Testing under a different Lua tests a different language: `lua5.1` rejects `>>` with `unexpected symbol near '>'` and has no `math.tointeger`, while HAProxy supports only 5.3 and above. A test failure caused by the wrong interpreter looks exactly like a module defect and wastes the review.

**Ship the test as a plain Lua script with no dependencies**, runnable as `lua5.4 <module>.test.lua`, so it runs on any machine that has the interpreter and needs no package manager inside a container image. `examples/haproxy-lua/token-guard.test.lua` is that shape: 28 checks, a table-driven case set, a property case, `os.exit(0)` on success and `os.exit(1)` on any failure.

`busted`, installed with `luarocks install busted`, is the conventional Lua test framework and gives assertions, spies, and structured output for a suite that outgrows a single file. Its installation was attempted in this skill's build environment on 26 July 2026 and failed while fetching a transitive dependency, so its behaviour under this pack is **unverified**; verify it in your own environment before making a suite depend on it.

## Table-driven cases

One table, one row per input, one loop. The value is that adding a case is adding a row, so nobody skips the awkward input because writing another function felt expensive.

```lua
local rejected = {
    { name = "empty string",     token = "" },
    { name = "too short",        token = "abc" },
    { name = "uppercase byte",   token = "abcdefgH" },
    { name = "embedded newline", token = "abcdef\ngh" },
    { name = "embedded NUL",     token = "abcdef\0gh" },
    { name = "non-string sample", token = 12345 },
}

for _, case in ipairs(rejected) do
    local ok, message = pcall(module.validate, case.token)
    check("rejects " .. case.name, ok == false, tostring(message))
end
```

Include the embedded newline and the embedded NUL in every case set for a handler that touches network bytes, because those two are what turn a validation gap into header injection.

## Prove the failure path, not the happy path

A converter's failure path decides whether a forged value reaches the backend, so it is the half that must be tested. Three assertions per rejection, all present in the shipped example:

1. **The call raised.** `pcall` returned `false`.
2. **The message carries no source position.** `message:match("^[^\n]-%.lua:%d+:") == nil` fails when someone writes `error(msg)` instead of `error(msg, 0)`, which is otherwise invisible until it appears in a production alert.
3. **The message does not echo the rejected value.** `message:find(case.token, 1, true) == nil` keeps attacker-controlled bytes out of the operator log.

Prove the assertions bite, by removal. Two mutations of the example module, each run against the unchanged test on 26 July 2026:

| Mutation | Test result |
|---|---|
| `error("… not a string", 0)` → `error("… not a string")` | 27 of 28 checks passed, exit 1, failing check names the leaked path |
| dropping `length < MIN_LENGTH` from the length guard | 22 of 25 checks passed, exit 1, three checks fail including the property |

A test suite that still passes after you break the module is measuring nothing.

## Collision and ordering property tests

A smoke test that generates one identifier passes on a generator with a few hundred distinct seeds per second, because one identifier is indistinguishable from a correct one. Two properties catch what a smoke test cannot.

**Collision, across process boundaries.** Run the generator in *N* freshly started processes, not *N* times in one process, because the defect lives in per-state seeding:

```
for i in $(seq 1 40); do lua5.4 gen.lua; done | sort | uniq -d
```

Any output line is a duplicate. Run the same loop against the module under `lua-load-per-thread` with `nbthread` set to the production value, since each thread seeds separately inside the same second.

**Ordering, under uneven CPU load.** Generate a value in a CPU-heavy caller and then in a CPU-light caller inside one wall-clock second, and assert the derived timestamps are non-decreasing in the order the calls actually happened. This is the assertion that fails on a CPU-time-derived timestamp and passes on `core.now()`.

**Keep a property case set non-vacuous.** A property that accepts nothing holds for the wrong reason. Draw candidates from a pool that is mostly valid, and assert the acceptance count as its own check — the shipped example accepts 309 of 5000 candidates and asserts that at least 100 were accepted.

**Seed test randomness with a fixed constant and print it.** A test that seeds from the clock cannot be re-run on the input that failed.

## Integration check against a real HAProxy

`haproxy -c -f <config>` loads and compiles every Lua file named by `lua-load` and `lua-load-per-thread`, so it is a real check of the module and not only of the configuration. Verified on HAProxy 2.8.16 on 26 July 2026:

| Fault | Result |
|---|---|
| valid configuration and module | `Configuration file is valid`, exit 0 |
| Lua syntax error in a loaded file | `error in Lua file '…': …: unexpected symbol near 'end'`, exit 1 |
| `lua-load` naming a file that does not exist | `error in Lua file '…': cannot open …: No such file or directory`, exit 1 |

`haproxy -c -f` does **not** execute your handlers, so it proves the module loads and registers, never that it behaves. The smallest configuration that gives the next level of proof is a frontend with `http-request return`, exercised with one request per case; the example bundle is that shape. Config validation discipline for HAProxy generally is owned by `/alaa-haproxy` (`$alaa-haproxy`).

## The proof level an HAProxy Lua change needs

Classify each claim with `/alaa-testing-strategy` (`$alaa-testing-strategy`) `references/40-proof-strength.md` and report it at the level actually reached, never higher. For this kind of change, four levels are reachable and each one is required before a module ships:

1. **Static** — `python3 scripts/check_haproxy_lua.py <module.lua>` exits 0. Reached without running anything.
2. **Unit** — the mock-`core` test exits 0 under the interpreter `haproxy -vv` named, and every failure path has a case.
3. **Local smoke** — `haproxy -c -f` exits 0 on the real configuration.
4. **In-runtime** — a running HAProxy on a loopback bind answers the accepted case and the rejected cases as designed. Reach this level for any handler whose failure decides whether a request is served, because levels 1 to 3 cannot observe the rendered sample.

Anything a live dependency would have to prove — a real backend, a real client population, a real reload — is above what this list reaches; say so rather than implying it was covered.
