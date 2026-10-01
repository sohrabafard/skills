# How Lua is embedded

HAProxy links a Lua interpreter into its own process when built with `USE_LUA=1`. Confirm both facts on the target binary before writing code:

```
haproxy -vv | grep -E '\+LUA|Built with Lua version'
```

The feature list must contain `+LUA` and the `Built with Lua version` line names the exact interpreter your module will run under. A build without `+LUA` rejects `lua-load` at configuration parse time, so this check is what turns a runtime surprise into a pre-work fact.

## Which Lua version

HAProxy's `INSTALL` file, section 4.7, states: "Only versions 5.3 and above are supported", and lists the library names it searches as `lua5.5`, `lua55`, `lua5.4`, `lua54`, `lua5.3`, `lua53`, `lua`. Two consequences follow.

- **LuaJIT is not a supported target.** LuaJIT implements Lua 5.1, below the supported floor, so a module does not need a 5.1 compatibility path for HAProxy. Write for 5.3 and above.
- **Lua 5.3 introduced bitwise operators, integer division, `math.tointeger` and `math.type`.** The first two are syntax; the latter require the math library to be enabled. They are *not* available when someone unit-tests the module with a stray `lua5.1` binary, which fails with `unexpected symbol near '>'` on the first `>>`. Record the minimum version in a comment at the top of every module so the test environment is chosen deliberately rather than by whichever `lua` is first on `PATH`.

The `Built with Lua version` line is the authority for which interpreter to run tests under. Do not infer it from the distribution's `lua` package.

## Compatibility target

HAProxy 3.4 supports compilation against Lua 5.5; that does not upgrade an image's
interpreter. The inspected 3.4.6 image embeds Lua 5.4.8, so its unit harness uses
that interpreter. Library omission can remove `math.type` or `math.tointeger`
even though the language supports them. Read the dependency policy before assuming
any optional standard-library function exists.

For scope and related decisions, return to the [parent reference](../10-execution-model.md).
