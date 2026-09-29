Version-sensitive claims in this topic depend on [Fiber sources and freshness](../SOURCES.md).

## Proxy trust

Two config fields, both defaulting to off
(https://docs.gofiber.io/api/fiber, verified 2026-07-26):

- `TrustProxy bool`, default `false`.
- `TrustProxyConfig TrustProxyConfig`, default `{}`, with fields `Proxies` (trusted IPs and CIDR
  ranges), `Loopback`, `Private` and `LinkLocal`.
- `ProxyHeader string`, default `""`, names the header the client IP is read from.

With `TrustProxy` false, Fiber ignores forwarded headers. With it true, Fiber checks the request
against `TrustProxyConfig` before reading proxy headers.

The rule: set `TrustProxy: true` and populate `TrustProxyConfig.Proxies` with the gateway's IPs or
CIDR ranges, taken from deployment configuration. Do not set `Private: true` or `Loopback: true` as
a shortcut in an environment where anything other than the gateway can reach the pod, because those
flags trust an address class rather than a specific peer.

Client IP, host and scheme may be derived from forwarded headers only under that configuration.
Identity, tenant, project and authorization context are never derived from a client-supplied
header under any configuration; they come from the gateway trust contract, owned by
`/alaa-trust-gateway-auth`, with gateway topology owned by
`/alaa-haproxy`.
