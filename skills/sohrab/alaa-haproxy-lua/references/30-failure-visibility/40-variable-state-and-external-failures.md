# Variables are not rolled back on failure

A failed sample does not constitute a request rejection or an atomic rollback of
prior writes. Clear or initialize the decision before invoking the handler; do not
allow a previous value to satisfy `-m found`. `TXN.set_var(..., true)` only writes a
variable whose name was defined elsewhere; it does not itself initialize or validate
that variable. Use `txn` scope for a transaction, `req`/`res` only in their valid
phase, and avoid `sess`/`proc` for request-specific decisions.

## Failures that are not your handler's

Two failure paths sit outside the handler and are still yours to design for.

- **Load failure.** A Lua syntax error, a missing file, or an error raised in the file body aborts startup. `haproxy -c -f <config>` reproduces it before deployment and exits non-zero; see `references/50-testing.md`.
- **Timeout.** A handler that exceeds `tune.lua.burst-timeout` is aborted mid-execution. Any state it left half-written in a HAProxy variable stays half-written, so write the variable once, at the end, from a value that is already complete.

For scope and related decisions, return to the [parent reference](../30-failure-visibility.md).
