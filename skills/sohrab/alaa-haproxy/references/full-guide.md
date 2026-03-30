# Alaa HAProxy Full Guide

## Version and branch discipline

- Check `https://docs.haproxy.org/` first to confirm which branches are `LTS`, `EOL`, or development.
- Check `https://www.haproxy.org/download/3.2/src/` and `https://www.haproxy.org/download/3.3/src/` next to confirm the latest released patch in each branch.
- At the time of this refresh:
  - the docs index marks `3.2` as `LTS`
  - the docs index lists `3.3` without the `LTS` label
  - the official release directories show `3.2.15` and `3.3.6`, both dated `2026-03-19`
- Use `haproxy -vv` to confirm the actual binary features before enabling QUIC, advanced TLS policy, Lua, tracing, or experimental directives.
- Use `haproxy -c -f <cfg>` for every config change.

## Production baseline

- Prefer master-worker mode in practice, but note that `3.3` deprecates the `master-worker` global directive in favor of command-line `-W` or `-Ws`.
- Keep Runtime API and stats access on local unix sockets with strict permissions.
- Set explicit values for:
  - `timeout connect`
  - `timeout client`
  - `timeout server`
  - `timeout http-request`
  - `timeout http-keep-alive` or tunnel-specific timeouts
- Use `hard-stop-after` when graceful shutdown could otherwise hang on long-lived sessions.
- Prefer maps for large host or path routing tables.

## Core configuration decisions

### HTTP connection behavior

- Keep normal keep-alive when backend reuse is helpful and server capacity is proven.
- Use `option http-server-close` when backend idle connections are the real bottleneck.
- Review `http-reuse`, queue behavior, and `strict-maxconn` together.

### Multi-tier proxy chains

- Only enable `accept-proxy` when the upstream really sends PROXY protocol.
- Only enable `send-proxy` or `send-proxy-v2` when the downstream explicitly expects it.
- Document each hop in mixed cloud-LB and HAProxy chains.

### Stick tables and peers

- Use stick tables for request-rate, connection-rate, and escalation counters close to the edge.
- Add peers when abuse state or affinity must survive node-level balancing.
- Test peer recovery and node loss before calling it production-ready.

## TLS, mTLS, and certificates

### Baseline

- Prefer `crt-store` plus `ssl-f-use` for modern `3.2` and `3.3` deployments that manage more than one certificate or per-cert policy.
- Keep TLS 1.2 and TLS 1.3 policy separate.
- Use strict SNI in multi-tenant environments unless a required legacy client proves incompatible.

### Ticket policy

- `no-tls-tickets` is the simple safe default when operational simplicity matters more than peak resumption performance.
- If you enable tickets, rotate keys intentionally and document the rotation path.

### mTLS

- Terminate client authentication at HAProxy when it reduces trust spread downstream.
- Log enough certificate context for incident response, but do not leak unnecessary certificate detail broadly.

### ACME

- In `3.2`, ACME is still an experimental flow.
- In `3.3`, ACME grows to include DNS-01 workflow support through the HAProxy Data Plane API path.
- In `3.3`, the Data Plane API can also save the issued certificates to the filesystem automatically, but the official blog recommends this only for single-load-balancer deployments.
- For Kubernetes-heavy estates, cert-manager may still be simpler unless you have a strong reason to keep issuance inside the HAProxy toolchain.

### `3.3` TLS and security additions

- Backend TLS can now infer SNI from the `Host` header automatically. Use `no-sni-auto` to disable it or `sni-auto` to state it explicitly.
- Health checks can control the same behavior with `check-sni-auto` and `no-check-sni-auto`.
- `ssl-passphrase-cmd` lets HAProxy unlock passphrase-protected private keys via a script.
- `jwt_verify_cert` reduces manual certificate-key extraction when HAProxy validates JWT signatures against certificates instead of bare public keys.
- `tcp-md5sig` matters mostly in router or BGP-adjacent TCP proxy scenarios.
- ECH and kTLS are useful `3.3` additions, but both should be treated as branch-specific and environment-validated features, not default assumptions.

## HTTP/3 and QUIC

### HAProxy 3.2

- `3.2` is the first LTS branch in this repository's scope with the newer HTTP/3 and QUIC-focused workflow.
- Verify QUIC support from `haproxy -vv` before using `quic4@...` listeners.
- Keep HTTP/2 and HTTP/1.1 fallback listeners clear.

### HAProxy 3.3

- `3.3` adds experimental backend HTTP/3 over QUIC support.
- It also introduces newer QUIC naming preferences: some global directives prefixed with `tune.quic.frontend` are deprecated in favor of `tune.quic.fe`.
- Use `3.3` examples only when the running estate is actually on `3.3`.

## Observability and runtime control

### Runtime API

- Keep the admin socket local and permission-restricted.
- Common first checks:
  - `show info`
  - `show stat`
  - `show errors`
  - `show events`
- Treat Runtime API as privileged control, not a public API.

### Logging

- Use structured or at least consistently parseable log formats.
- Add `%[term_events]` during incident-heavy periods or keep it in a richer debug profile for fast failure attribution.
- Preserve a request identifier at the edge and pass it downstream.

### Metrics

- Use the built-in Prometheus exporter when you need HAProxy-native counters quickly.
- In `3.3`, persistent stats across reloads become available as an experimental feature. This improves continuity for dashboards and alerting if you opt in and keep identifiers stable.
- In `3.3`, `show stat typed` now shows whether a metric is volatile or persistent, which is useful when validating shared-memory stats rollout.

### Deep debugging

- Use runtime tracing selectively and only for bounded investigations.
- Scale back heavy debug features after the incident to avoid unnecessary overhead.
- In `3.3`, `acme` and `ssl` trace sources are available for more focused diagnosis.

## Important `3.2 -> 3.3` upgrade notes

### Why move to `3.3`

- expanded ACME support, including DNS-01 workflow
- backend HTTP/3 over QUIC support
- persistent stats across reloads
- automatic SNI handling controls
- `ssl-passphrase-cmd`, `jwt_verify_cert`, and `tcp-md5sig`
- experimental ECH
- Linux kTLS support
- more observability and performance work

### Why stay on `3.2`

- you want the official LTS branch
- your estate values lower change velocity more than new features
- your current configs rely on `3.2` naming or behavior and do not need `3.3` additions yet

### Specific upgrade cautions

- `master-worker` as a global directive is deprecated in `3.3`; prefer command-line `-W` or `-Ws`.
- `tune.quic.frontend.*` names are deprecated in `3.3`; prefer `tune.quic.fe.*`.
- `no-quic` is renamed to `tune.quic.listen`.
- `dispatch` and `option transparent` are deprecated in `3.3`.
- The `linux-glibc` build target baseline changes in `3.3`; confirm host compatibility before fleet rollout.
- The `program` section is removed in `3.3`.
- Duplicate names across `frontend`, `backend`, `listen`, `defaults`, `log-forward`, and duplicate `server` names are now startup errors in `3.3`.
- In `3.3`, the default load-balancing algorithm becomes `random` when you do not set `balance` explicitly, so be explicit in configs where algorithm choice matters.
- In `3.3`, `mode http` backends now default to `option abortonclose`, which can change request-cancellation behavior.
- Re-run `haproxy -c` and `haproxy -vv` on the actual `3.3` binary before promoting any config copied from a `3.2` estate.

### Safe mixed-estate practice

- Keep `3.2` and `3.3` examples separate in reviews and rollout notes.
- Avoid sharing one config fragment across both branches when it uses deprecated or experimental directives.
- On `3.3`, prefer branch-aware inspection commands such as `haproxy -vq`, `haproxy -vqs`, and `haproxy -vqb` when scripts need stable version parsing.

## Containers, Kubernetes, Helm, and CI

### Containers

- The official image uses `/usr/local/etc/haproxy/haproxy.cfg` by default.
- Prefer high ports or explicit capability handling instead of assuming privileged-port access.
- Validate reload and signal behavior in the actual container entrypoint you deploy.

### Kubernetes

- For standalone HAProxy workloads, keep config in a dedicated ConfigMap and make rollouts config-aware.
- Readiness should fail before termination completes so traffic drains before the pod fully exits.
- Use a PodDisruptionBudget when HAProxy is part of an externally visible edge path.

### Helm and CI

- Validate both HAProxy syntax and chart rendering in CI.
- Minimum useful CI gates:
  - `haproxy -vv`
  - `haproxy -c -f ...`
  - `helm lint`
  - `helm template`

## Troubleshooting map

### 502 or 503 bursts

- Check backend health, queue growth, and timeout mismatches first.
- Add `term_events` if the reason is not obvious from current logs.
- Review whether `strict-maxconn`, rate limiting, or queue caps are protecting the backend or simply moving failure around.

### Tail latency spikes

- Look at rule count, regex cost, CPU pressure, and peer sync overhead.
- Replace repeated ACL trees with maps where possible.
- Benchmark topology controls instead of assuming they help.

### Too many open files

- Check process limits and system limits together.
- Confirm the service manager and container runtime both apply the intended FD ceilings.

### DNS or dynamic backend churn

- Review resolver hold times, retry behavior, and `server-template` expectations.
- Keep service discovery conservative enough to avoid constant backend flapping.

## Example usage notes

- `10-prometheus-runtime-api.cfg` is the clean starting point when you need both local admin control and a scrape endpoint.
- `11-proxy-protocol-chain.cfg` is the first file to copy when HAProxy sits behind another load balancer.
- `12-peers-global-rate-limit.cfg` is the first file to copy when local stick tables are no longer enough.
- `13-canary-map-routing.cfg` is the safest rollout starting point when release control needs reviewable and reversible diffs.
- `14-http3-backend-3.3.cfg` is only for estates already running `3.3`.
- `15-persistent-stats-3.3.cfg` is the cleanest starting point when you need uninterrupted dashboards across reloads.
- `16-server-tls-sni-auto-3.3.cfg` is useful when HAProxy talks TLS to virtual-hosted backends and you want less manual `sni req.hdr(host)` plumbing.
- `17-ktls-3.3.cfg` is only for Linux estates where the build, TLS library, and kernel capabilities were confirmed first.
