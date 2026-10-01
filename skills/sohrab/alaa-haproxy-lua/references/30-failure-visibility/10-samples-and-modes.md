# What a Lua return value becomes

HAProxy converts the Lua value your handler returns into a sample. `doc/lua.txt` gives the mapping:

| Lua type | HAProxy sample type |
|---|---|
| `number` | `sint` |
| `boolean` | `bool` |
| `string` | `str` |
| `userdata` | `bool` (false) |
| `nil` | `bool` (false) |
| `table` | `bool` (false) |
| `function` | `bool` (false) |
| `thread` | `bool` (false) |

**`nil` is not "no value". `nil` is boolean false.** A converter that returns `nil` returns a successful sample whose value is false, which renders as the string `0`.

## Measured rendering

Historical observations on HAProxy 2.8.16/Lua 5.4.6 (26 July 2026), retained below. On 1 October 2026 the bundled harness rechecked nil/false/true rendering, failed-sample rejection and action failure on HAProxy 3.4.6/Lua 5.4.8; see SOURCES.md. The empty-header case remains a historical observation:

| Handler behaviour | `var(txn.x)` after it | `var(txn.x,DEFAULT)` | `set-header` result | ACL `var(txn.x) -m found` |
|---|---|---|---|---|
| returns a string | the string | the string | header set to the string | matches |
| returns `nil` | `0` | `0` | header set to `0` | **matches** |
| calls `error(...)` | unset | `DEFAULT` | header **added with an empty value** | does not match |

Two conclusions follow, and both invert the intuitive reading.

1. **Returning `nil` is the most dangerous failure shape available.** The variable is set, the default in `var(name,default)` never fires, and `-m found` matches. A guard written as `deny unless { var(txn.token) -m found }` passes a value the handler explicitly rejected.
2. **A failing sample does not reject anything on its own.** `http-request set-header` still adds the header, with an empty value. The rejection has to be a separate rule.

## Booleans are ambiguous across versions

`tune.lua.bool-sample-conversion` exists because HAProxy-to-Lua conversion historically turned booleans into integers. The manual states that when the option is not set explicitly and a Lua script is loaded, HAProxy emits a warning and defaults to `pre-3.1-bug`, and that the setting "must be set before any `lua-load` or `lua-load-per-thread` directive for it to be considered, else it is ignored".

Booleans are valid Lua-to-HAProxy samples in both modes. The setting controls the
opposite direction: HAProxy boolean samples read by Lua become booleans in `normal`
and integers 0/1 in `pre-3.1-bug`. Lua treats numeric zero as truthy. Select the mode
explicitly before loading scripts and audit comparisons, native fetches and variable
reads together. Do not convert everything to strings or blindly switch legacy code.
The 3.4.6 runtime harness checks both modes. Nil still becomes false in both modes;
it is not a failed sample. This setting is not a switch for nil handling.

For scope and related decisions, return to the [parent reference](../30-failure-visibility.md).
