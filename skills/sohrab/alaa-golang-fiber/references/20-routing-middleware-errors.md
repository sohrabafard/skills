# Routing, Middleware Order, Errors, Proxy Trust

Read this file when you are about to register routes, order middleware, mount probes, map an error
to a status code, or configure CORS, a rate limiter, or proxy trust.

API names and defaults below were verified against the official Fiber v3 docs on **2026-07-26**;
URLs accompany each claim and are collected in `SOURCES.md`.
## Route registration
When registering or reviewing a route group, read [Route registration and middleware order](./20-routing-middleware-errors/10-route-and-middleware-order.md) for route registration and middleware order.

## Middleware order
When ordering middleware or placing probes, read [Route registration and middleware order](./20-routing-middleware-errors/10-route-and-middleware-order.md) for route registration and middleware order.

## Errors
When mapping handler errors or checking public failure responses, read [Errors and correlation](./20-routing-middleware-errors/20-errors-and-correlation.md) for errors and correlation.

## Request ID and correlation
When propagating request IDs or trace context, read [Errors and correlation](./20-routing-middleware-errors/20-errors-and-correlation.md) for errors and correlation.

## Proxy trust
When resolving client addresses from forwarded headers, read [Proxy trust](./20-routing-middleware-errors/30-proxy-trust.md) for proxy trust.

## Outbound proxy security (v3.5.0)
When configuring or reviewing outbound proxy access, read [Outbound proxy security](./20-routing-middleware-errors/40-outbound-proxy-security.md) for outbound proxy security.

## CORS
When serving browser-facing requests, read [CORS, rate limits, and net/http adaptation](./20-routing-middleware-errors/50-edge-controls-and-adaptation.md) for cors, rate limits, and net/http adaptation.

## Rate limiting
When configuring rate limiting, read [CORS, rate limits, and net/http adaptation](./20-routing-middleware-errors/50-edge-controls-and-adaptation.md) for cors, rate limits, and net/http adaptation.

## Adapting `net/http` middleware
When adapting standard-library middleware, read [CORS, rate limits, and net/http adaptation](./20-routing-middleware-errors/50-edge-controls-and-adaptation.md) for cors, rate limits, and net/http adaptation.
