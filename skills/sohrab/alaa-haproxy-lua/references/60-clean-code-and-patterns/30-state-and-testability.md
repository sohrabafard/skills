# Pure codec versus stateful handler

Separate them inside the file, and the separation decides where every test assertion goes.

A **pure function** takes its inputs as arguments, touches no `core` object and no `TXN`, and returns a value or raises. It is testable with no mock at all, it can be reused by a fetch and an action alike, and it is where all of the logic belongs.

A **stateful handler** reads the transaction, calls the pure function, and writes the result. It should contain no branching beyond the call and the write:

```lua
core.register_action("stamp_token", { "http-req" }, function(txn)
    local raw = txn:get_var("txn.raw_token")
    txn:set_var("txn.token", M.validate(raw), true)
end)
```

When a handler is more than a few lines, the logic has leaked out of the pure function and the tests are about to become HAProxy-dependent.

## Per-request state

Module-level locals are per Lua state and live for the lifetime of the process or thread. Putting request data there leaks it between unrelated requests, and under `lua-load` between unrelated threads.

- Per-request Lua values: `TXN.set_priv` and `TXN.get_priv`.
- Values the configuration must see: `TXN.set_var` with `ifexist` set to `true`.
- Values shared between threads: a module-level table under `lua-load` only, and only after accounting for the global Lua lock.

## Keeping the module testable

**Never touch `core` at load time outside the guard.** This package's testability convention is checked by HL006; HAProxy itself permits load-time core access, and dependency injection is also a valid testing design.

**Never read a file, open a socket, or resolve a name at the top level unconditionally.** Do it inside `core.register_init`, or guard it so the test path skips it. A test that has to create `/etc/haproxy/...` to load a module will not be written.

**Never call `os.exit` from module code.** It ends the HAProxy process, and it must not be relied on as an intercepted/harmless call.

For scope and related decisions, return to the [parent reference](../60-clean-code-and-patterns.md).
