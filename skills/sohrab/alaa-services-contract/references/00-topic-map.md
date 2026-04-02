# Alaa Services Contract Topic Map

Use this file to choose the smallest relevant reference file before loading the full guide.

## Service modes

- `Mode A - Any Ala backend service`
  - Use when the task is about `service` identity, route families, `/api/health`, `/api/ready`, readiness checks, response headers, or observability event naming.
  - Read `10-core-service-contract.md` and `20-operational-and-observability-contract.md` first.
- `Mode A+ - Platform flow and onboarding view`
  - Use when the task is about client -> gateway -> service flow, frontend or gateway orientation, internal HTTP hops, async boundaries, or which layer owns what.
  - Read `25-end-to-end-flow-and-boundaries.md` after the core contract.
- `Mode B - Laravel backend service`
  - Use when the task is about Laravel API response boundaries, Resources, middleware order, or Laravel-specific route and command expectations.
  - Read `30-trusted-ingress-and-laravel-contract.md` after the core contract.
- `Mode C - Laravel downstream trusted service`
  - Use when the service sits behind the Ala gateway and consumes sanitized trusted headers.
  - Read `30-trusted-ingress-and-laravel-contract.md` and pair with `$alaa-trust-gateway-auth`.
- `Mode D - Laravel auth-boundary service`
  - Use when the service is allowed to satisfy trusted ingress through request guards or `Auth::viaRequest(...)` but must still expose the same outward contract.
  - Read `30-trusted-ingress-and-laravel-contract.md`, then `50-laravel-copy-baselines.md` if implementation help is needed.

## Reference files

- `10-core-service-contract.md`
  - hard contract posture
  - Ala service map
  - service identity
  - route families
  - exact `/api/health`
  - exact `/api/ready`
  - readiness naming and failure rules
- `20-operational-and-observability-contract.md`
  - `X-Request-Id`
  - `traceparent`
  - log field schema
  - event and code naming for request and readiness flows
  - `RequestObservabilityMiddleware`
- `25-end-to-end-flow-and-boundaries.md`
  - client -> gateway -> service flow
  - frontend and gateway orientation
  - operational caller expectations
  - internal HTTP and async-boundary discipline
- `30-trusted-ingress-and-laravel-contract.md`
  - `ResolveUserMiddleware`
  - trusted headers
  - actor normalization
  - auth synchronization
  - Laravel Resource-first `/api/*` responses
- `40-apply-checklist-and-anti-patterns.md`
  - step-by-step apply checklist
  - review checklist
  - anti-patterns
- `50-laravel-copy-baselines.md`
  - copy-oriented middleware and helper class baselines
- `full-guide.md`
  - the whole contract in one place when the task is broad or risky

## Working rule

- Use the smallest file that answers the task.
- Load `full-guide.md` when the task spans multiple files or multiple contract domains.
- Keep this topic map aligned with the actual reference files.
