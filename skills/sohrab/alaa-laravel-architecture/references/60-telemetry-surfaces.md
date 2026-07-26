# Telemetry surfaces this skill's layer map creates

Five surfaces exist **because** of the layer map: each sits at a boundary the map defines, so its emission point is known before the code is written. That is why this skill states that they must be observable — a boundary whose crossing leaves no trace is a boundary no operator can reason about during an incident.

**This file names no field, no metric, and no requirement level.** `/alaa-services-contract` (`$alaa-services-contract`) owns every name; `/alaa-observability-soc` (`$alaa-observability-soc`) owns whether a signal is required, its cardinality budget, and its sampling. On whether something is required, SOC wins. On what it is called, the contract wins.

| Surface | Emission point the layer map fixes | Where its name comes from |
|---|---|---|
| An authorization decision denied | the Service, at its Policy/Gate call — the one layer permitted to make the decision, so a denial cannot be emitted from two places or missed at one | the "Authorization and validation" family in `alaa-services-contract references/24-metric-registry.md` |
| A cache read served, missed, or invalidated | the repository decorator — the only class that knows caching exists | **no registered name exists today.** Request one from `/alaa-services-contract` rather than inventing a near-miss; a family invented per service cannot be read by one fleet panel |
| An outbox row written, claimed, published, or failed | the Service for the write, the publisher worker for the rest | the "Outbox" family in `alaa-services-contract references/24-metric-registry.md` |
| A fallback taken: a lazily-read config or cached value that answered from its declared default | the consuming class at first use, per `references/20-composition-and-boot.md` | the dependency-failure names in the contract's registry |
| An error envelope rendered, distinguishing a domain exception a Service raised from an unexpected exception | the single exception handler of `references/40-degraded-mode.md` | the contract's error and dependency families |

## Why each one is not optional

- **The denial.** Without it, a permission regression is reported by users rather than observed, and a tenant-isolation failure looks exactly like normal traffic.
- **The decorator.** A cache whose hit ratio is unobserved cannot be distinguished from a cache that is not being used, which is precisely the state that failure class 1 in `references/50-failure-recovery.md` produces.
- **The outbox transitions.** Depth and oldest-row age are the only signals that separate "consumers are idle because nothing happened" from "consumers are idle because delivery stopped". Both look identical at the endpoint, which keeps returning success.
- **The fallback.** A silent default is the one failure mode that produces a wrong answer with a healthy-looking response. This signal is what makes the safe default safe.
- **The render.** The ratio of domain-raised failures to unexpected exceptions is what distinguishes a service rejecting bad input correctly from a service crashing, at the same status code.

## Two obligations that are not this skill's to soften

- Trace context propagates across every hop, including the queue hop between a Service's emission and a listener or publisher worker. The outbox row is a hop: a correlation identifier written on the row is what keeps a trace joined across it. The requirement level is `/alaa-observability-soc`'s, and it is not weakened by the hop being asynchronous.
- The correlation fields on the rendered error response are attached by the single handler, using the mechanism in `alaa-services-contract references/50-laravel-copy-baselines.md`.

## What never enters any of these signals

No secret, no credential, no personal data, and no raw exception text on a client-visible surface. What may appear in the error envelope's `meta` is fixed by `alaa-services-contract references/10-core-service-contract.md`; what may appear in a log or span is `/alaa-observability-soc`'s, and `/alaa-security-review` (`$alaa-security-review`) holds the verdict when the two are read differently.
