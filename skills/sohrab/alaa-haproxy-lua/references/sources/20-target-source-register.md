# Current compatibility evidence - 1 October 2026

Target remains **3.4.6**. Release currency, Docker tag/index metadata and build
features beyond Lua are owned by `/alaa-haproxy` `references/SOURCES.md`.
The web branch manual identified itself as 3.4.6-1; it is moving documentation,
not an immutable release. GitHub tag URLs returned 404 through the web tool and
shell retrieval hit TLS credentials, so the authorized official release archive
was used for exact source verification:

- https://www.haproxy.org/download/3.4/src/haproxy-3.4.6.tar.gz
- SHA-256: `791e1815f8af6e8b850a227a9a0a190f3d3478c9e8d38a0f51c98b7f4bfe368b`
- `VERSION`: `3.4.6`; repository receipt: `<repo>/outputs/20261001-haproxy-346/source-manifest.json`.
- Lua language: https://www.lua.org/manual/5.4/manual.html (matching the observed interpreter).

| Reverified claim | Exact release-source owner / inspected location |
|---|---|
| nil/table/function/userdata become false samples; booleans are valid returns | `src/hlua.c` `hlua_lua2smp`, lines 1265-1306 |
| mode changes HAProxy boolean -> Lua boolean versus number, not nil returns | `hlua_smp2lua`, lines 1139-1152; configuration `tune.lua.bool-sample-conversion` |
| action result consumed as `act.*`; ordinary action runtime error continues | `hlua_action`, lines 10881-11066; API `Act` class, lines 4077-4145 |
| twelve optional string arguments in target source | registration `ARG12`, lines 10751 and 10837; API prose still says five/nine, so it is not the authority for this limit |
| openlibs names/default and state-initialization ordering | `hlua_openlibs_tbl`, `hlua_cfg_parse_openlibs` lines 13366-13434, configuration directive |
| Lua floor and 5.5 compilation support versus image interpreter | `INSTALL` section 4.7; actual `haproxy -vv` |
| API contexts, core.now refresh, Socket inactivity timeout, variables | `doc/lua-api/index.rst` lines 431-443, 2824-2852, 3251-3268 |
| memory is accounted through shared allocator | `hlua_global_allocator`, `hlua_alloc`, `lua_newstate` in `src/hlua.c`; configuration `tune.lua.maxmem` |
| non-blocking architecture usage restrictions, not universal interception | `doc/lua.txt` lines 145-186; library/fork protections in configuration manual |
| clock, error level, pcall, lexical scope and patterns | Lua 5.4 manual sections 2, 3.5, 6.1, 6.4.1, 6.7, 6.9 |

### Introductions versus maintenance

`CHANGELOG` records openlibs during 3.4 development (3.4-dev9), and Lua 5.5
support during 3.4-dev2: both are in the 3.4.0 capability baseline, not invented
by 3.4.6. State loading, action codes, sockets and converters are established API
mechanisms, not presented as 3.4 inventions. The target includes later fixes such
as deferred VM initialization (3.4.0), socket timeout handling (3.4.3), Channel send
resumption (3.4.4), and cosocket GC/per-thread body state fixes (3.4.5). The 3.4.6
entry contains no Lua-specific new API. Backport availability cannot be inferred
from this branch's changelog; inspect the consumer branch before relying on one.

For scope and related decisions, return to the [parent reference](../SOURCES.md).
