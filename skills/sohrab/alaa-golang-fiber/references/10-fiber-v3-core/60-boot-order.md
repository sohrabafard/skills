The official Fiber API baseline for this slice was verified on **2026-07-26**; claim-specific source URLs and later refresh dates are in [SOURCES.md](../SOURCES.md).

## Boot order

1. Load and validate configuration; fail the process on any invalid or out-of-range value.
2. Construct the logger, metrics registry and tracer provider.
3. Construct database, cache and external clients.
4. Construct repositories, then application services.
5. Construct the `*fiber.App` with the validated [server bounds](./50-server-bounds.md) configuration.
6. Register middleware in the order fixed by `20-routing-middleware-errors.md`.
7. Register every route.
8. Start the listener.

Steps 6 and 7 complete before step 8, per the route-registration rule in `SKILL.md`.

Data-layer client choice, pool sizing and cache topology are owned by `/alaa-data-layer`, and the kit's `rediskit` contract is reached through
`/alaa-go-chi-development`. This skill states none of it.
