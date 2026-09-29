Version-sensitive claims in this topic depend on [Fiber sources and freshness](../SOURCES.md).

## Outbound proxy security (v3.5.0)

Before using proxy middleware, check the resolved Fiber version. In v3.5.0, `SecurityPolicy`
rejects private/loopback targets, non-HTTP(S) schemes and HTTPS-to-HTTP redirect downgrades by
default, and strips hop-by-hop headers. Preserve these protections; an internal upstream needs a
scoped destination allowlist and security review before permitting private addresses. [`TrustProxy`](30-proxy-trust.md) governs inbound headers, not outbound destination safety.

Tagged `middleware/proxy/security.go` guards dial-time resolution for built-in balancer clients
and runtime helpers. A reused per-call client may retain cached pre-guard HostClients;
register a dedicated client with `WithClient` before use. A custom `Balancer Config.Client` owns
its dial validation. Verify these paths against the installed source before claiming DNS-rebinding
protection: the current prose docs describe a broader runtime-helper gap than this tag does.

Set package-wide `WithSecurityPolicy` at boot, never per request: concurrent requests share it. Exercise blocked private/metadata targets, DNS-answer changes,
redirect downgrades, cross-origin credential handling and allowed destinations on the actual client
path. Map rejection through the existing error boundary; never log credential-bearing target URLs.

Sources checked 2026-09-29: https://github.com/gofiber/fiber/releases/tag/v3.5.0,
https://raw.githubusercontent.com/gofiber/fiber/v3.5.0/middleware/proxy/security.go and
https://docs.gofiber.io/middleware/proxy/#security. Tagged source decides this released-version
claim; current docs require reconciliation with the consumer's tag.
