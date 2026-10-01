# Standard libraries and dependency review

Verified target: HAProxy 3.4.6. Sources and proof limits are in `references/SOURCES.md`.

## Select libraries before creating any Lua state

`tune.lua.openlibs` accepts `all` (default), `none`, or a comma-separated list from
`table,io,os,string,math,utf8,package,debug`. `none` cannot be mixed with names.
The base and coroutine libraries remain available, including HAProxy's replacement
for `coroutine.create`. Put the setting before **every** `lua-load`,
`lua-load-per-thread`, and `lua-prepend-path`; late placement is a parse error.

This is attack-surface reduction, not a sandbox for hostile Lua. Base functions and
HAProxy APIs still carry authority. Excluding `debug` reduces introspection;
excluding `package` removes the standard module loader; excluding `io` and `os`
removes their whole namespaces. Fork/thread restrictions are separate HAProxy
protections; do not enable `insecure-fork-wanted` to make a module load.

## Derive the allowlist from the dependency closure

1. Inventory each loaded module, required module and native extension, including
   aliases, top-level initialization, error branches, tasks and disabled services.
2. Map calls to libraries: `os.getenv`, `os.date`, and `os.time` all require `os`;
   `require` needs `package`; a loaded module may introduce more requirements.
   A text search is a starting inventory, not proof of a dynamic dependency closure.
3. Separate library presence from operation safety. Retaining `os` for environment
   reads does not authorize process execution. Route runtime I/O to the execution
   model in `references/10-execution-model.md`.
4. Parse the full configuration, run matching-interpreter unit tests, and exercise
   success, missing dependency, malformed input and timeout paths under the candidate
   list. Test both shared and per-thread loading if changing the load model.
5. Remove a required library only with a reviewed redesign and equivalent tests.
   Preserve the old list with the old module/configuration as the rollback unit.

For the bundled token validator, `string` suffices in production: `type`, `tonumber`,
`tostring`, `error`, and iteration are base functions. Its randomized unit test also
needs `math`; that test dependency is not a production module dependency.
Do not copy this list to gateway modules that read environment variables or dates.

Run `python3 scripts/check_runtime.py --image <cached-image>` from this package.
It tests `all`, `none`, a restricted list, the `os` dependency, rejected values and
ordering with HAProxy's own parser. It never downloads an image.
