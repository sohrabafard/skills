# Reverse Proxy and Gateway Guidance

## Contents

- [Core Rule](#core-rule)
- [Non-Negotiable Behaviors](#non-negotiable-behaviors)
- [Choose Nginx When](#choose-nginx-when)
- [Choose HAProxy When](#choose-haproxy-when)
- [Nginx Notes](#nginx-notes)
- [HAProxy Notes](#haproxy-notes)
- [Sticky Sessions and Horizontal Scale](#sticky-sessions-and-horizontal-scale)
- [Auth Placement](#auth-placement)
- [Timeouts](#timeouts)
- [Pre-Production Verification Checklist](#pre-production-verification-checklist)


## Core Rule

Either Nginx or HAProxy is a valid front door for tusd. The correct choice depends on the platform that already owns ingress, auth, stickiness, and operational tooling.

Do not hard-code Nginx-only guidance unless the user explicitly asked for Nginx.

## Non-Negotiable Behaviors

Whichever proxy or gateway sits in front of tusd must preserve all of these behaviors:

- disable request buffering,
- preserve `Host`, `X-Forwarded-Host`, `X-Forwarded-Proto`, and a trusted client IP chain,
- forward correlation or request IDs,
- keep auth and ownership checks on every client request,
- protect `/metrics` and any profiling endpoints separately,
- align timeouts with real upload duration,
- keep sticky sessions available when scaling stock tusd horizontally.

Also remember to set `-behind-proxy` on tusd itself.

For upstream proxy-to-tusd transport, default to HTTP/1.1 unless the team has explicitly tested another mode for large uploads. Avoid clever protocol changes in the hot path unless they are proven under load.

## Choose Nginx When

- the platform already uses Nginx or Nginx Ingress heavily,
- auth is already implemented with `auth_request` or established Nginx modules,
- the team wants a familiar reverse-proxy template with minimal new operational surface,
- the deployment is simple and does not need advanced load-balancer behavior beyond standard proxying.

Use `assets/nginx/tusd-reverse-proxy.conf` as the baseline.

## Choose HAProxy When

- the platform already standardizes on HAProxy for edge or internal load balancing,
- multi-instance stock tusd needs an explicit stickiness strategy,
- the team wants load-balancer-centric routing, ACLs, or canary control in one place,
- the SOC or platform team already consumes HAProxy logs and metrics as first-class signals.

Use `assets/haproxy/tusd-reverse-proxy.cfg` as the baseline.

## Nginx Notes

When adapting Nginx:

- keep `proxy_request_buffering off`,
- keep `proxy_buffering off`,
- preserve forwarded host and scheme,
- review `proxy_read_timeout`, `proxy_send_timeout`, and `send_timeout` for long uploads,
- add stickiness only if you truly run multiple stock tusd instances.

## HAProxy Notes

When adapting HAProxy:

- keep `option forwardfor`,
- explicitly set `X-Forwarded-Proto` and `X-Forwarded-Host`,
- do not enable `option http-buffer-request`,
- tune `timeout client` and `timeout server` for slow or large uploads,
- use `balance source` or cookie-based persistence when stock tusd runs on multiple nodes,
- keep `/metrics` behind an ACL or a private listener.

## Sticky Sessions and Horizontal Scale

For stock tusd, stickiness is usually the lowest-risk way to scale before you commit to custom distributed locking.

Good rule of thumb:

- one instance: no stickiness needed,
- multiple stock instances with shared storage: add stickiness,
- multi-node active-active without stickiness: only if the team explicitly owns a stronger custom design.

## Auth Placement

Treat the proxy or gateway as the enforcement point for request-by-request ownership.

That means:

- authenticate `POST`, `PATCH`, `HEAD`, and `DELETE`,
- map upload ID to the application upload record,
- verify the caller can still access that upload,
- only then forward to tusd.

## Timeouts

Timeout mistakes are a common production failure mode.

Review these explicitly:

- client header timeout,
- upstream connect timeout,
- client body streaming timeout,
- upstream response timeout,
- graceful shutdown timeout.

The effective timeout budget must reflect the longest legitimate `PATCH` duration on slow links, not just average request time.

## Pre-Production Verification Checklist

Before calling the gateway setup production-ready, verify all of these with real uploads:

- a large upload does not get buffered at the proxy,
- `HEAD` returns correct offsets through the proxy,
- `PATCH` resume works after network interruption,
- `Location` and other headers are correct under TLS termination,
- auth is enforced on `POST`, `PATCH`, `HEAD`, and `DELETE`,
- `/metrics` is protected,
- graceful shutdown does not corrupt active uploads,
- stickiness keeps the same upload on the same stock tusd instance when required.
