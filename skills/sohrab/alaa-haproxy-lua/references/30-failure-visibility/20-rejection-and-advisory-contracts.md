# The Alaa error contract

**For a converter or fetch using the rejection contract, signal failure with `error(message, 0)`.** The sample then fails, an initially unset target remains unset, and a configuration rule can act on that. Actions and services have separate failure contracts in `references/25-actions-services-and-subrequests.md`; neither an error log nor an absent sample is a rejection by itself.

**At a call site using the rejection contract, pair a fallible converter or fetch with explicit rejection**, because setting a variable is not a decision. Advisory call sites may use the owner-approved sentinel contract below.

```
http-request unset-var(txn.token)
http-request set-var(txn.token) var(txn.raw_token),lua.token_guard(64)
http-request deny deny_status 400 unless { var(txn.token) -m found }
```

The `deny` line is what makes the failure closed. Without it, a rejected value is merely absent and the request proceeds.

**Decide the failure mode per call site, not per module.** Two shapes exist and choosing between them is a judgement about what the value is for:

- **Reject** — the value gates access, identifies a caller, or is written to a header a backend will trust. The handler raises and the configuration denies. This is the default; take it unless the second case is argued.
- **Explicit sentinel** — the value is advisory, the request is still valid without it, and a downstream consumer can distinguish "absent" from "present". The handler returns a string the configuration recognises, never `nil` and never the empty string, because the empty string is also what a failed sample renders as in a header.

Which of the two applies is a fail-closed question owned by `/alaa-security-review`; the sentinel *value* itself is a contract name owned by `/alaa-services-contract`.

For scope and related decisions, return to the [parent reference](../30-failure-visibility.md).
