# Frontend HTTP/3

**Mandatory prerequisite:** before configuring this mode, read [build requirements and binary choices](./10-build-requirements.md); it decides whether the binary and TLS library can support the selected QUIC path.

For current branch selection and dated source precedence, consult [version and branch](../10-version-and-branch.md) and [the source ledger](../SOURCES.md).

## Frontend HTTP/3

`03-quic-http3.cfg`. Three things must all be true or clients silently stay on HTTP/2:

- a `quic4@` (or `quic6@`) `bind` line exists alongside the TCP listener;
- **UDP on that port is open end to end**, including every firewall, security group and cloud load
  balancer in the path. A path that passes TCP 443 and drops UDP 443 is the single most common
  cause of an HTTP/3 rollout that appears to do nothing;
- an `Alt-Svc` response header advertises the endpoint, because most clients do not attempt QUIC
  unless told the server speaks it.

**Keep the TCP listener.** HTTP/3 is advertised, never required: a client that cannot reach UDP
must have somewhere to fall back to, and that fallback is what makes a QUIC misconfiguration a
performance event rather than an outage.

Confirm the rollout from the `alpn` or protocol field in the access log, not from the config. The
config proves the listener exists; only the log proves a client used it.
