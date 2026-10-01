# Historical evidence (26 July 2026; not current proof)

Every entry below was read on **26 July 2026**. A claim in this skill that does not appear here is either derived from a measurement recorded beside it in the file that makes the claim, or is marked unverified.

| Claim | Source read |
|---|---|
| "Only versions 5.3 and above are supported"; searched library names `lua5.5`, `lua55`, `lua5.4`, `lua54`, `lua5.3`, `lua53`, `lua` | `INSTALL` section 4.7, HAProxy tag `v3.4.0`, via `raw.githubusercontent.com/haproxy/haproxy/refs/tags/v3.4.0/INSTALL` |
| `lua-load` loads into a shared context, only one thread runs on the global state at a time, `core.thread` is 0 | configuration manual, HAProxy tag `v3.2.0`, `doc/configuration.txt`, section 3.1 |
| `lua-load-per-thread` gives thread-local globals, loads sequentially in thread order, is the recommended way to register converters and fetches | same file, same section |
| `tune.lua.forced-yield` defaults, and the phrase "the global lua lock" | configuration manual `v3.2.0`, `doc/configuration.txt` |
| `tune.lua.burst-timeout` 1000 ms default; converters and sample fetches named as unyieldable handlers; GC time counted | same |
| `tune.lua.session-timeout` and `tune.lua.service-timeout` 4 s defaults; `tune.lua.task-timeout` unset by default | same |
| `tune.lua.maxmem` defaults to unlimited, and the reason to set it | same |
| `tune.lua.log.loggers` default `on`, `tune.lua.log.stderr` default `auto` | same |
| `tune.lua.bool-sample-conversion` defaults to `pre-3.1-bug` with a warning, and must precede any `lua-load` | same |
| `uuid([<version>])`, "Versions 4 and 7 are supported" | configuration manual, tags `v3.0.0`, `v3.1.0`, `v3.2.0`, `v3.3.0`, `v3.4.0` — identical text in all five |
| the eight Lua execution contexts; initialisation versus runtime mode | `doc/lua-api/index.rst`, tags `v3.2.0` and `v3.4.0` — identical |
| `core.register_*` signatures; converter and fetch prototypes and argument limits | same |
| `core.now()` returns `sec` and `usec`, is refreshed per execution, contexts body/init/task/action | same |
| `core.msleep` and `core.sleep` contexts task/action; `core.yield` and `core.wait` semantics | same |
| `TXN.set_var` `ifexist` recommendation | same |
| Lua-to-HAProxy sample type table, including `nil` becoming boolean false | `doc/lua.txt`, tag `v3.4.0` |
| the runtime-prohibited function list, and the reasons given for each | same |
| "you must use `lua-load-per-thread` instead of `lua-load`" above 32 CPUs | https://www.haproxy.com/documentation/haproxy-configuration-tutorials/performance/performance-tuning/ |
| branches listed as LTS and DEV on the documentation index | https://docs.haproxy.org/ |

`raw.githubusercontent.com/haproxy/haproxy` is the official GitHub mirror of the HAProxy repository and was used because it serves the tagged plain-text manual in one request. Where a claim above is branch-sensitive, the tag is named.

## Measurements taken in this skill's build environment

These are observations, not documentation. Each is reproducible with the command recorded beside it in the reference that uses it. All were taken on **26 July 2026** on **HAProxy 2.8.16-0ubuntu0.24.04.3**, whose `haproxy -vv` reports `Built with Lua version : Lua 5.4.6` and `+LUA` in the feature list.

- Rendering of a `nil` return, an `error()` and a successful return, through `set-var`, `var(name,default)`, `set-header`, and an `-m found` ACL — `references/30-failure-visibility.md`.
- Log output of `error(msg)` against `error(msg, 0)` — same file.
- `os.clock()` spread across forty fresh processes, seed uniqueness, UUID duplicate count, and the ordering inversion — `references/40-time-randomness-identity.md`.
- Per-thread seed separation under `nbthread 4` with `lua-load-per-thread`, clock-derived against `/dev/urandom`-derived — same file.
- `haproxy -c -f` behaviour on a Lua syntax error and a missing Lua file — `references/50-testing.md`.
- `%[uuid(7)]` rejected at configuration parse on 2.8.16 — `references/40-time-randomness-identity.md`.

The 2.8.16 build is older than the branches this pack deploys. Every measurement above is reported as an observation on that build; re-run the same command on the target branch before quoting a number as current for it.

## Marked unverified

- `busted` as a test runner. Installation via `luarocks install busted` failed in this build environment on 26 July 2026 while fetching a transitive dependency, so nothing about its behaviour under this pack has been observed.
- `core.now()` inside a converter. The API reference does not list the converter context; it was observed to work inside a sample fetch on 2.8.16 and was not tested inside a converter.

For scope and related decisions, return to the [parent reference](../SOURCES.md).
