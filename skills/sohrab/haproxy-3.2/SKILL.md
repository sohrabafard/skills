---
name: haproxy-3.2-skill
description: "Complete, operator-grade HAProxy 3.2 LTS skillbook with official docs links, safe defaults, and practical recipes across OS, containers, Kubernetes, Helm, and CI/CD."
---




# HAProxy 3.2 LTS — Master Skill

## Overview
This skillbook is an operator-grade, copy/paste-friendly guide to **designing, configuring, deploying, and troubleshooting HAProxy 3.2.x (LTS)**.

It includes:
- **HAProxy 3.2 highlights** (TLS `ssl-f-use`, experimental ACME, `term_events`, QUIC tuning, `strict-maxconn`, `label`, etc.)
- L4/L7 configuration patterns: ACLs, maps, content switching, balancing strategies
- **TLS/PKI**: `crt-store`, SNI, per-cert policy, mTLS, resumption strategy, ticket key rotation, strict SNI
- **QUIC/HTTP3**: build checks, listener patterns, safe tuning knobs
- **Observability**: log formats, `term_events`, Runtime API, tracing, Prometheus notes
- **Operations**: master-worker, graceful reloads, master CLI, safe shutdown, OS resource limits
- Cross-knowledge: **Linux**, **containers**, **Kubernetes**, **Helm**, **GitLab CI/CD**

This pack also includes:
- `examples/haproxy/` — practical configs by scenario
- `examples/kubernetes/` — manifests to run HAProxy as a Deployment
- `examples/helm/values-example.yaml` — values patterns
- `examples/gitlab-ci/gitlab-ci-snippet.yml` — minimum CI gate

> **Always validate**: `haproxy -c -f <cfg>` and confirm build features: `haproxy -vv`.

---

## Official documentation (bookmark these)
Core docs:
- HAProxy docs portal (3.2 is marked LTS): https://docs.haproxy.org/
- HAProxy 3.2 Configuration Manual: https://docs.haproxy.org/3.2/configuration.html
- HAProxy 3.2 Management Guide: https://docs.haproxy.org/3.2/management.html
- HAProxy 3.2 configuration.txt (printable manual version header): https://www.haproxy.org/download/3.2/doc/configuration.txt

Release highlights:
- Announcing HAProxy 3.2: https://www.haproxy.com/blog/announcing-haproxy-3-2
- [ANNOUNCE] haproxy-3.2.0: https://www.mail-archive.com/haproxy%40formilux.org/msg45917.html
- 3.2 changelog snapshot: https://www.haproxy.org/download/3.2/src/snapshot/CHANGELOG

Containers + Kubernetes:
- Docker Official Image: https://hub.docker.com/_/haproxy/
- HAProxy Technologies Helm charts: https://github.com/haproxytech/helm-charts
- HAProxy Kubernetes Ingress Controller docs: https://www.haproxy.com/documentation/kubernetes-ingress/

TLS ecosystem (official HAProxy content):
- State of SSL Stacks: https://www.haproxy.com/blog/state-of-ssl-stacks
- TLS and HAProxy 3.2 (user spotlight): https://www.haproxy.com/user-spotlight-series/tls-and-haproxy-3-2-from-stunnel-to-native-tls-support

---

## Quick “operator contract”
- **Do not** assume a directive exists until `haproxy -c` confirms it.
- **Do not** expose Runtime API sockets / master CLI publicly.
- **Do not** store TLS private keys or API secrets in git.
- **Do** set explicit timeouts and limits.
- **Do** test reload behavior under traffic before relying on it in prod.

---

## When NOT to use
- do not use this skill for generic reverse-proxy advice when HAProxy 3.2-specific directives, runtime behavior, or operational constraints are not in scope
- do not assume a feature exists in the running build until `haproxy -vv` and `haproxy -c` confirm it
- do not paste recipes from this file into production without trimming them to the repository's real topology, trust boundary, and reload model

# 1) What’s new in HAProxy 3.2 (operator summary)

High-impact changes you’ll actually use:

### Performance and scaling
- CPU topology controls: `cpu-set`, `cpu-policy` (NUMA/topology-aware placement).
- Fairness: rules evaluation is batched; tune with `tune.max-rules-at-once`.
- High-thread improvements: `leastconn`, `roundrobin`, queue locking and peer sync contention.
- Linux TCP memory control knobs: `tune.notsent-lowat.client/server`.

### TLS
- `ssl-f-use` for frontends: attach certs and per-cert policy outside `bind`.
- strict SNI support via `ssl-default-bind-options strict-sni`.
- Ticket controls: `tls-tickets`, `no-tls-tickets`, `tls-ticket-keys`.

### ACME (experimental in 3.2)
- Enabled via `expose-experimental-directives`.
- Runtime API: `acme renew`, `acme status`.
- `dpapi` event ring to hand off cert updates to the Data Plane API (save-to-disk workflows).

### QUIC/HTTP3
- Listener syntax includes `quic4@`.
- New tuning knobs for fairness/throughput/memory (e.g., `tune.quic.frontend.stream-data-ratio`, `tune.quic.frontend.max-tx-mem`).
- Pacing behavior adjustments (verify with your build and documentation).

### Observability and debugging
- New log fetch: `term_events` (great for failure root cause).
- Prometheus exporter counter additions/updates (example: `current_session_rate`).
- Runtime API enhancements: `show events -0`, `show quic stream`, `show sess` filters, `show ssl sni`, `trace ssl`.

### Load balancing / protocol handling
- `strict-maxconn` restores strict maxconn semantics for open connections.
- Compression min-size thresholds.
- `hash-preserve-affinity` for consistent hash behavior under saturation.
- `idle-ping` for HTTP/2 idle connection liveness.
- `http-request pause` / `http-response pause`.
- `check-reuse-pool` for health checks using idle pooled connections.
- `bind ... label <label>` to tag sockets.

---

# 2) Quickstart (do this first)

## 2.1 Verify build capabilities
```bash
haproxy -vv
```
Look for:
- SSL library + version
- QUIC availability
- enabled poller (epoll/kqueue/etc.)
- compiled features (Lua, PCRE, threads, etc.)

## 2.2 Validate configuration
```bash
haproxy -c -f /etc/haproxy/haproxy.cfg
```

## 2.3 Start & reload safely (systemd + master-worker)
From the Management Guide:
- SIGTERM: hard stop (immediate close)
- SIGUSR1: graceful stop (unbind + drain)
- master-worker: SIGUSR2 reloads the master (re-execs with `-sf` and spawns new workers)

Classic safe init-style start:
```bash
haproxy -f /etc/haproxy/haproxy.cfg -D -p /run/haproxy.pid -sf $(cat /run/haproxy.pid)
```

**Container (official image):**
```bash
docker kill -s HUP my-running-haproxy
```
The official entrypoint uses the upstream wrapper to do a graceful reload internally.

---

# 3) Baseline configs (use the examples)

Start with these examples and adapt:

- `examples/haproxy/01-baseline-http-tls.cfg`
  - HTTP + TLS termination
  - `crt-store` + `ssl-f-use`
  - safe timeouts
  - `strict-maxconn` on servers (optional)

- `examples/haproxy/02-tcp-l4.cfg`
  - L4 TCP load balancing baseline

---

# 4) Core configuration patterns (best practice)

## 4.1 Timeouts are your #1 reliability lever
Set explicit:
- `timeout connect`
- `timeout client`, `timeout server`
- `timeout http-request`
- `timeout http-keep-alive` (or tunnel timeouts for long-lived streams)

Rule of thumb:
- Too low = false failures under load
- Too high = stuck resources and slow failure detection

## 4.2 HTTP connection modes (HTTP/1.x)
From the config manual:
- keep-alive yields best throughput/latency but keeps idle backend conns.
- `option http-server-close` reduces idle backend conns while keeping client keepalive.
- `option http-pretend-keepalive` can work around broken server behaviors with “Connection: close”.

## 4.3 PROXY protocol correctness
If you’re behind another LB:
- Upstream sends PROXY → HAProxy must `accept-proxy` on bind
- HAProxy sends PROXY to backend → `send-proxy` on server lines

Never enable PROXY protocol unless both sides agree; it will break traffic.

## 4.4 Map-driven routing
Maps are preferred for large routing tables (easier reviews, smaller diffs, less ACL sprawl).
See `examples/haproxy/01-baseline-http-tls.cfg` and extend with maps.

## 4.5 Consistent hashing under saturation
Use `hash-preserve-affinity { always | maxconn | maxqueue }` (3.2) when `balance hash` is used and you want predictable behavior when a target server is saturated or queued.
See `examples/haproxy/08-consistent-hash-affinity.cfg`.

## 4.6 Drop trailers (reduce metadata leakage)
- `option http-drop-request-trailers`
- `option http-drop-response-trailers`

Useful when your environment might carry sensitive metadata in trailers (chunked encoding).

## 4.7 Bound graceful shutdown time
`hard-stop-after <time>` sets a maximum soft-stop time (useful when long-lived TCP connections could keep HAProxy alive indefinitely).

---

# 5) TLS/PKI mastery (3.2 patterns)

## 5.1 `crt-store` + `ssl-f-use`
- `crt-store` describes where certificates/keys live.
- `ssl-f-use` attaches certs and per-cert policy to a frontend.
This enables expressive per-cert settings (min TLS version, ALPN, ciphers, sigalgs, etc).

## 5.2 Cipher configuration
HAProxy docs separate:
- TLS 1.2 and earlier ciphers (`ssl-default-bind-ciphers`)
- TLS 1.3 ciphersuites (`ssl-default-bind-ciphersuites`)

The config manual explicitly references Mozilla guidance and generators; use those as a policy baseline.

## 5.3 Resumption policy and ticket key rotation
- `no-tls-tickets` disables stateless tickets (forces stateful resumption; higher CPU).
- If you keep tickets enabled, rotate keys:
  - `tls-ticket-keys <keyfile>` OR periodic reload with rotated keys.

## 5.4 strict-sni
- Enable strict SNI to avoid “default cert confusion” in multi-tenant TLS.
- If global strict-sni breaks legacy clients, selectively disable with `no-strict-sni` on specific binds.

## 5.5 mTLS
Terminate mTLS at the edge:
- `bind ... ca-file ... verify required`
- Gate requests based on `{ ssl_c_used }` and other cert fetches.
See `examples/haproxy/07-mtls.cfg`.

## 5.6 ACME (experimental)
HAProxy 3.2 introduces experimental ACME support.
- Requires `expose-experimental-directives`.
- Runtime API can issue renewals and query status.
- dpapi ring enables cert update handoff to Data Plane API.
In Kubernetes, cert-manager is still the default choice for many teams due to topology and lifecycle maturity.

---

# 6) QUIC / HTTP/3 (3.2)

## 6.1 Listener patterns
Docs show QUIC listeners use address family prefixes like:
- `quic4@<ip>:<port>`

See `examples/haproxy/03-quic-http3.cfg`.

## 6.2 ALPN on QUIC
Per config manual:
- HTTPS typically uses `h2,http/1.1` (or `h2` only)
- QUIC defaults to `h3` and supports only specific QUIC ALPN values

## 6.3 QUIC tuning knobs
- `tune.quic.frontend.stream-data-ratio`: fairness vs throughput (per-stream tx)
- `tune.quic.frontend.max-tx-mem`: cap tx buffer usage (pair with `maxconn`)
- `quic-cc-algo`: select congestion control algorithm; pacing can be disabled via `tune.quic.disable-tx-pacing` if needed

---

# 7) Stick tables and rate limiting

Stick tables are HAProxy’s native state store for:
- req/sec and conn/sec
- GPC/GPT counters for graduated penalties
- shared state across HAProxy nodes via peers

See: `examples/haproxy/04-rate-limit-stick-table.cfg`.

Operational tips:
- Start with **429** responses and logging, then tighten.
- Prefer “slow down” (`pause`) for borderline spikes, and “deny” for sustained abuse.

---

# 8) Observability and Runtime API

## 8.1 Runtime API basics (secure it)
```bash
echo "show info" | socat stdio /run/haproxy/admin.sock
echo "show stat" | socat stdio /run/haproxy/admin.sock | head
```
Treat admin sockets as root access: unix socket + strict permissions.

## 8.2 `term_events` for failure analysis (3.2)
Add `%[term_events]` to your log-format during incidents to capture richer termination state chains.

## 8.3 Helpful “late binding” headers
- `http-send-name-header` sets a header to the selected server name right before sending upstream (useful for debugging/retries).

## 8.4 HTTP/2 idle liveness with `idle-ping`
`idle-ping <delay>` enables periodic liveness checks on idle frontend connections.
The config manual notes it is currently implemented by the H2 mux only.

---

# 9) OS tuning (Linux essentials)

From the Management Guide:
- Ensure you have enough file descriptors (`ulimit -n`).
- Linux system-wide FD limit: `fs.file-max`
- Per-process hard FD ceiling: `fs.nr_open`

Basic checks:
```bash
ulimit -n
sysctl fs.file-max fs.nr_open
```

---

# 10) Containers, Kubernetes, Helm, GitLab CI/CD

## 10.1 Containers (official image)
- Default config location: `/usr/local/etc/haproxy/haproxy.cfg`
- Reload: `docker kill -s HUP <container>` (graceful reload via wrapper)
- Non-root ports:
  - Use high ports (recommended in K8s), or
  - Use capabilities, or
  - Use sysctl `net.ipv4.ip_unprivileged_port_start=0` (kernel support required per official image docs)

## 10.2 Kubernetes (standalone HAProxy)
See:
- `examples/kubernetes/haproxy-configmap.yaml`
- `examples/kubernetes/haproxy-deployment.yaml`
- `examples/kubernetes/haproxy-service.yaml`
- `examples/kubernetes/haproxy-pdb.yaml`

Key patterns:
- ConfigMap + checksum annotation to trigger rollout on change.
- Readiness probe should fail before shutdown (preStop hook patterns).
- Use PDB to survive node drains.

## 10.3 Official Helm charts (HAProxy Technologies)
Repo instructions:
```bash
helm repo add haproxytech https://haproxytech.github.io/helm-charts
helm repo update
helm search repo haproxytech/
```

## 10.4 GitLab CI minimum validation gates
See `examples/gitlab-ci/gitlab-ci-snippet.yml`:
- `haproxy -vv`
- `haproxy -c -f ...`
- (Optionally) `helm template` + `helm lint` before deployment stages

---

# 11) Troubleshooting playbooks (fast triage)

## 11.1 502/503 spikes
Checks:
- `show stat`: are servers down? queues full?
- logs with `term_events`
- timeout mismatches: connect/server timeouts vs upstream latency

Fixes:
- tighten/repair health checks
- tune timeouts
- protect backends with `strict-maxconn`, queue limits, rate limiting

## 11.2 Tail latency spikes
Checks:
- CPU saturation + softirq/IRQ
- huge rule sets? consider batching and reducing regex
- check peer sync contention if using stick tables + peers

Fixes:
- `cpu-policy` / `cpu-set` benchmarking
- reduce ACL/regex cost and move routing into maps
- tune rule batching (`tune.max-rules-at-once`)

## 11.3 “Too many open files”
Checks:
- `ulimit -n`, `fs.file-max`, `fs.nr_open`
Fix:
- raise limits + verify HAProxy starts as root then drops privileges properly

---

## Appendix: example file index
- HAProxy configs: `examples/haproxy/`
- K8s manifests: `examples/kubernetes/`
- Helm patterns: `examples/helm/values-example.yaml`
- GitLab CI: `examples/gitlab-ci/gitlab-ci-snippet.yml`
- Source links: `references/SOURCES.md`
