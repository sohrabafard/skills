# HAProxy 3.4.6 capability decisions

Use this reference when a change relies on a 3.4 capability. The minimum branch
below means introduction in 3.4.0 unless a patch is named. Target 3.4.6; an
announcement establishes intent, while the target source/manual establishes the
shipped contract. Sources and the dated build receipt are in [SOURCES.md](SOURCES.md).

Before activating a capability, record its workload purpose, prerequisites,
effective defaults and failure behavior. Parse on the intended binary and test the
specific behavior. Leave tuning defaults unchanged until a measurement justifies
the cost; numerical defaults below are source facts, not fleet recommendations.

## Dynamic backend lifecycle

For creation, publication, routing, drain, deletion and recovery, read
[dynamic backend operations](65-dynamic-backends.md). This is a 3.4 lifecycle;
adding a server to an existing backend predates it. `be-unpublished` is a 3.4.4
maintenance addition, not a 3.4.0 directive.

## Capability routes

When setting request budgets or sharing checks, read [Timeouts and health checks](15-capabilities-3.4/10-timeouts-and-healthchecks.md) for placement, effective values, attachment and origin proof.
When changing memory or thread placement, read [Buffers and topology](15-capabilities-3.4/20-buffers-and-topology.md) for defaults, allocation, scheduler and capacity measurement.
When handling malformed or saturated HTTP peers, read [Protocol overload](15-capabilities-3.4/30-protocol-overload.md) for H1 glitches, H2 fairness and multiplexed stream elasticity.
When decrypting tokens or payloads, read [Cryptographic converters](15-capabilities-3.4/40-cryptographic-converters.md) for algorithms, empty-string failure, key and claim boundaries.
When enabling issuance or TLS handshake compression, read [ACME and certificate compression](15-capabilities-3.4/50-acme-and-certificate-compression.md) for CA/library prerequisites and lifecycle proof.
When tuning reuse or collecting diagnostics, read [Pools and diagnostics](15-capabilities-3.4/60-pools-and-diagnostics.md) for pool sharing, H2 logs, memory profiling and exporter changes.
When evaluating QMux or OpenTelemetry, read [Experimental transports and tracing](15-capabilities-3.4/70-experimental-transports-and-tracing.md) for build/component gates, activation and interoperability/export proof.
## Compression and filter ordering

For explicit `comp-req`/`comp-res`, legacy syntax and cache ordering, read
[compression mechanics](50-caching-routing-and-rewrites.md#compression).
The 3.4 announcement's `filter-sequence` mechanism was reverted in 3.4.5: it is
absent from the 3.4.6 contract. Do not emit it. Use declaration order and prove
request/response body behavior with every enabled filter.
