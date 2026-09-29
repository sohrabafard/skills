# QUIC tuning and names

**Mandatory prerequisite:** before configuring this mode, read [build requirements and binary choices](./10-build-requirements.md); it decides whether the binary and TLS library can support the selected QUIC path.

For current branch selection and dated source precedence, consult [version and branch](../10-version-and-branch.md) and [the source ledger](../SOURCES.md).

## Tuning and naming

`tune.quic.*` settings bound memory and stream behaviour, and **the namespace has been
reorganised twice**: 3.3 renamed the `tune.quic.frontend.*` family to `tune.quic.fe.*` and renamed
`no-quic` to `tune.quic.listen`, and 3.4 reorganised again — `tune.quic.fe.stream.data-ratio` and
`tune.quic.mem.tx-max` on 3.4 are not the names 3.2 or 3.3 accepted. A name written for one branch
is an `unknown keyword` startup error on another.

Do not copy a `tune.quic.*` line out of a document. Enumerate what the binary in front of you
actually has:

```
haproxy -dKcfg -c -f /dev/null | grep tune.quic
```

A mixed estate puts any such block behind `.if version_atleast(3.4)` or the equivalent for its own
branches. `03-quic-http3.cfg` deliberately ships no tuning line for this reason.

3.4 adds QMux, experimental QUIC over TCP, for networks that block UDP entirely. It is a different
mechanism from `limited-quic`: QMux changes the transport, `limited-quic` changes the TLS
integration.

Whether the latency improvement HTTP/3 buys is worth the operational surface is a service-level
question and belongs to `/alaa-reliability-sla`.
