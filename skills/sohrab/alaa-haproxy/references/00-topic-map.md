# Alaa HAProxy Topic Map

Use this file to load only the part of `full-guide.md` that matches the task.

## Version and branch checks

- LTS vs non-LTS branch status
- latest `3.2.x` and `3.3.x` release lookup
- running-binary checks with `haproxy -vv` and `haproxy -c`

## Core configuration patterns

- timeouts and retry discipline
- maps, ACLs, and backend switching
- connection reuse, queueing, and `strict-maxconn`
- PROXY protocol and multi-tier load-balancer chains

## TLS and edge security

- `crt-store` and `ssl-f-use`
- TLS versions, ciphers, and ticket policy
- strict SNI and mTLS
- admin socket and stats exposure safety

## HTTP/3 and QUIC

- frontend HTTP/3 in `3.2`
- backend HTTP/3 in `3.3`
- build checks and safe tuning
- QUIC rename and deprecation notes in `3.3`

## Observability and operations

- Runtime API and stats socket usage
- Prometheus exporter patterns
- logging with `term_events`
- graceful reloads, drains, and shutdown bounds
- persistent stats across reloads in `3.3`

## Platform delivery

- container image and reload behavior
- Kubernetes standalone deployment patterns
- Helm values patterns
- CI validation and dry-run rollout gates

## Security and observability checklist

- admin socket exposure
- TLS and mTLS boundaries
- log format and correlation IDs
- metrics, ServiceMonitor, and runtime traces
- drain and reload safety

## Upgrade and mixed-estate guidance

- when to stay on `3.2`
- when to adopt `3.3`
- `3.2 -> 3.3` deprecations and rollout notes
- `3.3` breaking changes that can fail startup after an upgrade

## Example index

- `01-baseline-http-tls.cfg`: baseline HTTP and TLS edge
- `02-tcp-l4.cfg`: pure TCP proxy
- `03-quic-http3.cfg`: frontend HTTP/3 baseline
- `04-rate-limit-stick-table.cfg`: local rate limiting
- `05-syslog-log-forward.cfg`: remote syslog forwarding
- `06-dns-service-discovery.cfg`: resolver-driven backend discovery
- `07-mtls.cfg`: client certificate verification
- `08-consistent-hash-affinity.cfg`: stable affinity under saturation
- `09-connection-reuse.cfg`: backend connection reuse tuning
- `10-prometheus-runtime-api.cfg`: metrics and local admin socket
- `11-proxy-protocol-chain.cfg`: multi-tier proxy correctness
- `12-peers-global-rate-limit.cfg`: shared abuse state with peers
- `13-canary-map-routing.cfg`: map-driven canary rollout
- `14-http3-backend-3.3.cfg`: `3.3` backend HTTP/3 over QUIC
- `15-persistent-stats-3.3.cfg`: persistent stats across reloads
- `16-server-tls-sni-auto-3.3.cfg`: backend TLS with automatic SNI
- `17-ktls-3.3.cfg`: Kernel TLS and splice-assisted TLS bridging
- `18-tiered-edge-gateway.cfg`: multi-layer edge to internal gateway
- `19-tls-bridge-mtls-backend.cfg`: TLS bridge with client auth to backend
