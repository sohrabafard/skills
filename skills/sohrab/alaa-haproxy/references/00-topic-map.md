# HAProxy Topic Map

Open this file first. It maps a task to exactly one reference below and names the example config
to start from. Every rule in this skill is stated in exactly one of these files.

## Task to reference

| Open this | When the task is |
|---|---|
| `10-version-and-branch.md` | choosing a branch, reading `haproxy -vv`, planning an upgrade, or checking whether a directive exists in the branch that will run the config |
| `20-core-config-and-timeouts.md` | structuring a config, the `defaults` association rule, timeouts, retries, connection ceilings, maps, environment variables and the config preprocessor, or diagnosing a live symptom |
| `25-tls-and-mtls.md` | certificates, `crt-store`, `ssl-f-use`, TLS version and ticket policy, SNI, client certificates, backend TLS, or ACME |
| `30-quic-http3.md` | QUIC or HTTP/3 on either side, or deciding what to do when `haproxy -vv` reports no QUIC |
| `40-rate-limiting-and-peers.md` | stick tables, rate limiting, abuse counters, `peers`, or what a limiter does when a peer is gone |
| `50-caching-routing-and-rewrites.md` | caching, `Cache-Control`, compression, path rewrites, deep-link fallback, or backend selection |
| `60-observability-and-runtime.md` | the Runtime API, the Prometheus exporter, the `log-format` string, tracing, or persistent stats |
| `70-delivery-and-drain.md` | container paths, writable directories, signals, reload, readiness and the drain ordering |
| `80-gate-register.md` | what must be proved before a config change ships, and which command proves it |
| `90-companion-boundary.md` | any decision that may not belong to this skill |
| `SOURCES.md` | re-deriving a version-sensitive fact from an official source |

## Executable checks

Run both before shipping a config change. Full contract in `80-gate-register.md`.

- `scripts/check_defaults_scope.py` — enforces the `defaults` association rule.
- `scripts/check_examples.py` — parses every shipped example and checks its in-file contract.

## Example index

Every file states its charter, its minimum branch, its preconditions, its variables and its
failure mode in its own header. The `-3.3` suffix means **3.3 or later**, not 3.3 only.

| File | Charter | Minimum branch |
|---|---|---|
| `01-baseline-http-tls.cfg` | HTTP and TLS edge baseline | 3.2 |
| `02-tcp-l4.cfg` | pure L4 TCP proxy | 3.2 |
| `03-quic-http3.cfg` | frontend HTTP/3 with an HTTP/2 fallback listener | 3.2 |
| `04-rate-limit-stick-table.cfg` | single-node rate damper and the rate-limit key rule | 3.2 |
| `05-syslog-log-forward.cfg` | syslog relay to a collector pair | 3.2 |
| `06-dns-service-discovery.cfg` | resolver-driven backends with `server-template` | 3.2 |
| `07-mtls.cfg` | client-certificate termination at the edge | 3.2 |
| `08-consistent-hash-affinity.cfg` | stable affinity, and what consistent hashing costs | 3.2 |
| `09-connection-reuse.cfg` | backend connection reuse and `idle-ping` placement | 3.2 |
| `10-prometheus-runtime-api.cfg` | Runtime API socket and a local scrape endpoint | 3.2 |
| `11-proxy-protocol-chain.cfg` | PROXY protocol in and out, and its trust requirement | 3.2 |
| `12-peers-global-rate-limit.cfg` | replicated stick table, and the fail-open arithmetic | 3.2 |
| `13-canary-map-routing.cfg` | map-driven canary routing | 3.2 |
| `14-http3-backend-3.3.cfg` | HTTP/3 towards the origin | 3.3 |
| `15-persistent-stats-3.3.cfg` | counters that survive a reload | 3.3 |
| `16-server-tls-sni-auto-3.3.cfg` | backend SNI from the Host header, and its consequence | 3.3 |
| `17-ktls-3.3.cfg` | kernel TLS on both sides of a bridge | 3.3 |
| `18-tiered-edge-gateway.cfg` | outer load balancer to gateway, with header hygiene | 3.2 |
| `19-tls-bridge-mtls-backend.cfg` | TLS bridge with a client certificate towards the backend | 3.2 |
| `20-static-asset-cache-and-rewrite.cfg` | caching, compression and rewrites as directives | 3.2 |

Kubernetes bundle: `examples/kubernetes/` — configmap, deployment, service, networkpolicy, pdb,
hpa, servicemonitor. The seven files share three port numbers and are only correct together.

Helm value patterns: `examples/helm/values-example.yaml` and `values-production-example.yaml`.

## First file to copy

| The task | Start from |
|---|---|
| a new HTTP or HTTPS edge | `01-baseline-http-tls.cfg` |
| a protocol HAProxy must not parse | `02-tcp-l4.cfg` |
| HTTP/3 for clients | `03-quic-http3.cfg` |
| an abuse problem on one node | `04-rate-limit-stick-table.cfg` |
| an abuse problem across nodes | `12-peers-global-rate-limit.cfg`, header first |
| HAProxy behind another load balancer | `11-proxy-protocol-chain.cfg` |
| both local admin control and a scrape endpoint | `10-prometheus-runtime-api.cfg` |
| a release step that must be reviewable and reversible | `13-canary-map-routing.cfg` |
| serving static assets, caching or a path rewrite | `20-static-asset-cache-and-rewrite.cfg` |
| dashboards that must survive a reload | `15-persistent-stats-3.3.cfg` |
| TLS to virtual-hosted origins | `16-server-tls-sni-auto-3.3.cfg` |
| moving TLS work into the kernel | `17-ktls-3.3.cfg` |
