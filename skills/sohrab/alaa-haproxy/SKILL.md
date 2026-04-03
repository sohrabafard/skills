---
name: alaa-haproxy
description: "Use this skill when the task involves HAProxy design, config, tuning, troubleshooting, observability, security, or production delivery. It is the HAProxy source of truth for this pack and covers both the current HAProxy 3.2 LTS line and the newer 3.3 line, with live official-source verification for version-sensitive guidance."
---

# Alaa HAProxy

## Purpose

Use this skill when the task needs HAProxy-specific design, configuration, deployment, tuning, observability, troubleshooting, upgrade planning, or security guidance.

This skill is the HAProxy source of truth for this pack. It covers both:

- HAProxy `3.2`, which is still marked `LTS` in the official docs index
- HAProxy `3.3`, which is newer but not marked `LTS`

## Live version policy

- Check `https://docs.haproxy.org/` first to confirm branch status.
- Check `https://www.haproxy.org/download/3.2/src/` and `https://www.haproxy.org/download/3.3/src/` next to confirm the latest released patch in each branch.
- At the time of this refresh:
  - `3.2` is still labeled `LTS` in the docs index
  - `3.2.15` is present in the official `3.2` release directory dated `2026-03-19`
  - `3.3.6` is present in the official `3.3` release directory dated `2026-03-19`
- Do not assume a distro package, Docker tag, or old memory is fresher than those official locations.

## When to use

- HAProxy config authoring or review
- L4 or L7 load-balancing design
- TLS termination, mTLS, certificate loading, SNI, HTTP/2, or HTTP/3 work
- Runtime API, stats socket, logs, metrics, traces, or incident triage
- performance tuning, connection reuse, stick tables, peers, maps, canaries, or rate limiting
- container, Kubernetes, Helm, or CI delivery patterns for HAProxy
- upgrade planning or mixed-estate guidance across `3.2` and `3.3`

## When NOT to use

- do not use this skill for generic reverse-proxy advice when HAProxy-specific behavior is not the decision surface
- do not assume a directive exists just because it exists in another HAProxy branch
- do not expose admin sockets, master CLI access, or certificate material to untrusted paths

## Source priority

Use sources in this order:

1. Live official HAProxy branch status and release directories
2. Official HAProxy `3.2` or `3.3` configuration and management manuals for the branch you actually run
3. Official HAProxy container, ingress, and chart docs
4. This skill's `references/` files
5. This skill's bundled examples

If sources conflict:

- live official docs beat older memory
- `haproxy -vv` and `haproxy -c -f ...` beat assumptions
- repository topology and trust boundaries beat generic snippets

## Quick start

1. Confirm whether the target estate is `3.2`, `3.3`, or mixed.
2. Inspect the running build with `haproxy -vv`.
3. Validate config changes with `haproxy -c -f <cfg>`.
4. Start from the closest bundled example.
5. Read the upgrade section before moving anything from `3.2` to `3.3`.

## Branch strategy

- Prefer `3.2` when the requirement is "stay on LTS".
- Use `3.3` when you explicitly want newer features and you accept that it is not the current LTS branch.
- For mixed estates, keep branch-specific examples and upgrade notes visible in review comments and rollout plans.

## Important `3.3` additions to account for

- expanded ACME workflow, including DNS-01 support via the HAProxy Data Plane API workflow
- backend HTTP/3 over QUIC support
- persistent stats across reloads
- automatic backend SNI handling controls
- `ssl-passphrase-cmd` for passphrase-protected private keys
- `jwt_verify_cert` for certificate-backed JWT verification flows
- `tcp-md5sig` for TCP proxying in router or BGP-adjacent scenarios
- experimental ECH support
- Linux kTLS support
- some `3.2` naming or operational patterns now have deprecations or preferred replacements in `3.3`

## Companion routing

- `$caas-arvan-kuber`
  - Pair when HAProxy runs on Arvan CaaS or Kubernetes delivery is the main constraint.
- `$alaa-docker-production`
  - Pair when image hardening, container attack surface, or Dockerfile behavior matters.
- `$alaa-observability-soc`
  - Pair when logs, metrics, traces, alerting, or incident evidence requirements extend beyond HAProxy itself.
- `$alaa-security-review`
  - Pair when HAProxy changes alter trust boundaries, mTLS policy, exposure, or admin surface.
- `$alaa-trust-gateway-auth`
  - Pair when HAProxy is part of an Ala gateway auth or trusted-header path.
- `$alaa-crockford-base32-codecs`
  - Pair when HAProxy Lua work needs shared Crockford Base32, UUIDv7, or pure codec helpers that must match backend, frontend, or CLI code.

## Reference navigation

- Fast router and example map:
  - `references/00-topic-map.md`
- Full preserved guidance, production checklists, branch comparison, and upgrade notes:
  - `references/full-guide.md`
- Platform delivery patterns for containers, Kubernetes, Helm, and CI:
  - `references/20-platform-delivery.md`
- Security and observability checklist:
  - `references/30-security-observability.md`
- Official links and live-source checkpoints:
  - `references/SOURCES.md`

## Example bundles

- HAProxy configs:
  - `examples/haproxy/01-baseline-http-tls.cfg`
  - `examples/haproxy/03-quic-http3.cfg`
  - `examples/haproxy/04-rate-limit-stick-table.cfg`
  - `examples/haproxy/10-prometheus-runtime-api.cfg`
  - `examples/haproxy/11-proxy-protocol-chain.cfg`
  - `examples/haproxy/12-peers-global-rate-limit.cfg`
  - `examples/haproxy/13-canary-map-routing.cfg`
  - `examples/haproxy/14-http3-backend-3.3.cfg`
  - `examples/haproxy/15-persistent-stats-3.3.cfg`
  - `examples/haproxy/16-server-tls-sni-auto-3.3.cfg`
  - `examples/haproxy/17-ktls-3.3.cfg`
  - `examples/haproxy/18-tiered-edge-gateway.cfg`
  - `examples/haproxy/19-tls-bridge-mtls-backend.cfg`
- Kubernetes:
  - `examples/kubernetes/haproxy-configmap.yaml`
  - `examples/kubernetes/haproxy-deployment.yaml`
  - `examples/kubernetes/haproxy-service.yaml`
  - `examples/kubernetes/haproxy-pdb.yaml`
  - `examples/kubernetes/haproxy-networkpolicy.yaml`
  - `examples/kubernetes/haproxy-hpa.yaml`
  - `examples/kubernetes/haproxy-servicemonitor.yaml`
- Helm:
  - `examples/helm/values-example.yaml`
  - `examples/helm/values-production-example.yaml`
- CI:
  - `examples/gitlab-ci/gitlab-ci-snippet.yml`
  - `examples/github-actions/haproxy-validate.yml`

## Maintenance rules

- Keep this file routing-first and plain.
- Put dense operational detail into `references/full-guide.md`.
- Keep source dates and branch status aligned with current official HAProxy sources.
- Add new examples only when they represent a distinct production pattern.
