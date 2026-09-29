# Backend HTTP/3

**Mandatory prerequisite:** before configuring this mode, read [build requirements and binary choices](./10-build-requirements.md); it decides whether the binary and TLS library can support the selected QUIC path.

For current branch selection and dated source precedence, consult [version and branch](../10-version-and-branch.md) and [the source ledger](../SOURCES.md).

## Backend HTTP/3

`14-http3-backend-3.3.cfg`. 3.3 and later, still experimental, so
`expose-experimental-directives` must precede its first use. `server ... quic4@<addr>` sends HTTP/3
to the origin.

Two differences from the frontend case:

- The UDP path to the **origin** is a different firewall rule from the client-side one and is
  frequently forgotten.
- **There is no fallback.** If the origin does not speak HTTP/3 the server stays down and the
  backend loses that capacity outright. That fails hard rather than silently, which is the safer
  shape, but it is not what an operator expects from an "enable HTTP/3" change.

An experimental directive can change name or behaviour across branches, so a config that starts on
3.3 may not start on 3.4 or 3.5. Re-run `haproxy -c -f` against the new binary **as part of** the
upgrade, not after it.
