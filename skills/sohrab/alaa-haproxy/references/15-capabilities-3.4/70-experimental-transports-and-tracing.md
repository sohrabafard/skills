# Experimental QMux and OpenTelemetry

QMux is experimental in 3.4: QUIC frames over a reliable byte stream, distinct
from UDP QUIC and the `limited-quic` TLS compatibility path. Require `+QUIC`,
the `qmux` protocol in `haproxy -vv`, TLS support, matching endpoints and
`expose-experimental-directives` before TLS `bind`/`server` with `alpn h3`.
It is not enabled by default. Validate a two-proxy chain, negotiated transport,
fallback and failure before using it; a client's UDP HTTP/3 support alone is
insufficient. The cached 3.4.6 image lists QMux, which establishes build presence
only, not interoperability or performance.

OpenTelemetry is a separate experimental component from
[haproxy-opentelemetry](https://github.com/haproxy/haproxy-opentelemetry).
Its client library must be compiled into the HAProxy build; `filter opentelemetry`
also needs event and exporter configuration. It is inactive unless configured.
Check the available filter list in `haproxy -vv` and the component's build/config
documentation; `-OT` is the OpenTracing flag and does not independently establish
OpenTelemetry absence. The observed official 3.4.6 Alpine image has no
OpenTelemetry filter. Do not infer availability from the image tag or add a
nonfunctional filter. A suitably built binary must parse the component configs
and send verified spans to an isolated collector, including collector failure
and overhead tests. Trace requirement, field names and sensitive data policy
remain with the named companion owners.
