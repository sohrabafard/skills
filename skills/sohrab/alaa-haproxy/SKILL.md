---
name: alaa-haproxy
description: "HAProxy configuration, tuning, troubleshooting, delivery and upgrade work: turning a routing, TLS, caching, rate-limiting, load-balancing or drain decision into HAProxy directives, choosing between supported branches, and reading the Runtime API. Use when authoring or reviewing an haproxy.cfg, when a change must be proved with haproxy -c -f, when stick tables, peers, QUIC, mTLS, compression or the Prometheus exporter are in scope, or when planning a branch upgrade. Do not use to decide caching policy, owned by /alaa-frontend-devops ($alaa-frontend-devops); for HAProxy Lua, owned by /alaa-haproxy-lua ($alaa-haproxy-lua); for Kubernetes chart authorship, owned by /alaa-k8s-helm ($alaa-k8s-helm); for pipeline YAML, owned by /alaa-gitlab-ci-cd ($alaa-gitlab-ci-cd)."
---

# Alaa HAProxy

## What this skill decides

How a routing, caching, TLS, rate-limiting, load-balancing, observability or drain decision is
**expressed as an HAProxy directive**, and which HAProxy branch a config targets. It is the
HAProxy source of truth for this pack.

## What this skill does not decide, and when not to use it

`alaa-haproxy` owns how a cache or routing decision is expressed as an HAProxy directive — the
`http-response set-header Cache-Control` rule, the `cache` section, the `compression` settings, the
path rewrite, the deep-link fallback, and the ACL or map that selects a backend — and it decides
no policy: which `Cache-Control` value belongs to which response class is decided by
`/alaa-frontend-devops` (`$alaa-frontend-devops`), `alaa-frontend-devops
references/30-serving-caching-and-public-path.md`, because that policy follows from whether the
build gave the file a content-hashed name and the build owns that. **When a caching or routing
task arrives here without a stated policy, ask for the policy and emit no directive rather than
choosing a default.**

Every other boundary — the owner, and the condition under which that owner decides — is in
`references/90-companion-boundary.md`. Three that come up in almost every task, so that silence is
never mistaken for authority:

- **HAProxy Lua is not this skill's subject.** `/alaa-haproxy-lua` (`$alaa-haproxy-lua`) owns
  `lua-load`, `http-request lua.<name>`, Lua converters and fetches, and Lua-backed SPOE. Route
  there the moment a task would write or debug any of them.
- **What a timeout, retry or degradation should be** is decided by `/alaa-reliability-sla`
  (`$alaa-reliability-sla`). This skill states which timeouts exist and how they are written.
- **What a change lets through when it fails** is decided by `/alaa-security-review`
  (`$alaa-security-review`) whenever the answer to *when this dependency cannot answer, does
  proceeding without it let something through that must not get through?* is yes.

## Quick start

1. Establish the branch that will actually run the config. `references/10-version-and-branch.md`
   holds the branch table and the upgrade path; **3.4 is the current LTS**.
2. Run `haproxy -vv` on that binary. It answers which features exist before any directive relies
   on one.
3. Open `references/00-topic-map.md`. It maps the task to exactly one reference and names the
   example config to start from.
4. Run `haproxy -c -f <cfg>` on a binary of that branch. A config checked on the wrong branch has
   not been checked.
5. Run both checkers below. `haproxy -c -f` proves the file parses; it does not prove the file is
   correct, and the two most expensive HAProxy mistakes — a `defaults` section that governs a
   proxy you did not intend, and a `peers` section that never activates — both pass it.

## Checkers

```
python3 scripts/check_defaults_scope.py examples/haproxy
python3 scripts/check_examples.py --haproxy $(command -v haproxy)
```

Both take `--help` and `--self-test`. Exit codes are **0 clean, 1 findings, 2 could not run**; a
missing binary or an unreadable path is 2, never 0. Full contract and the gate register:
`references/80-gate-register.md`.

## Maintenance

- Keep this file routing-first. Every rule lives in exactly one reference; a rule written twice is
  a defect.
- Every version-sensitive value in this skill is listed in `references/SOURCES.md` beside the one
  command or URL that re-derives it. Update both together, or neither.
- Add an example only when it represents a production pattern no existing example covers, and give
  it the same header every other example has: charter, minimum branch, preconditions, variables,
  failure mode. `scripts/check_examples.py` enforces that header.
