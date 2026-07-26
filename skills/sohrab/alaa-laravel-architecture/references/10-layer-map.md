# The layer map — what each layer may contain, and what may cross between them

The legal and forbidden edges are in `SKILL.md`. This file states what may live inside each layer and what a boundary permits to cross it.

## What each layer may contain

**Controller.** Orchestration only: take a FormRequest, hand `validated()` to a Service, return a Resource. It cannot tell whether caching exists.

**Service.** Business rules, domain invariants, the authorization call, and the emission of domain events (`references/30-events-and-outbox-seam.md` fixes the moment). It is the only layer that calls a Policy or Gate, so an authorization decision is never made twice and never skipped by a second caller. It returns domain objects or DTOs, never an array shaped for JSON.

**Repository.** Data access only: query composition, persistence, atomic updates and counters. It resolves the public identifier to whatever internal key the store uses, and that translation is the only place the internal key is known outside the store.

**DTO.** The object that crosses a layer boundary, in both directions.

**Resource / Transformer.** Output mapping only. It owns the JSON shape of a success response.

**Policy / Gate.** Authorization predicates, called from a Service. A Policy performs no write and emits no event.

**Observer.** Reacts to a model change to trigger a mechanical side effect. It holds no domain decision: a decision a user initiated is made in the Service, where the invariant and the authorization already are, so the two never disagree.

**Enum.** The closed set behind an event type, a status, or a code, so a value cannot drift by typo across layers.

## The class name binds the class to its layer

The name is how the next reader knows which rules above apply without opening the file, so the binding is architectural rather than cosmetic:

- Service: `<Domain>Service`
- Repository: `<Store><Domain>Repository` behind `<Domain>RepositoryInterface`; the store in the name is what makes a second implementation obviously substitutable
- Cache decorator: `Cached<Domain>Repository`
- DTO: `<Domain>Data`, `<Domain>FilterData`
- Event: past tense and domain-specific
- Factory: `<Thing>Factory`

A class whose name does not place it in a layer is placed by whoever reads it next, and two readers place it differently. Naming and file-shape rules beyond this binding are `/alaa-php-clean-code`'s (`$alaa-php-clean-code`).

## What may cross a boundary

**A typed object crosses; an array does not.** A raw array carries no shape a reader or a static analyser can check, so a field added at one end is silently absent at the other.

**A request object does not cross out of the HTTP layer.** A Service that reads `$request` cannot be called by a job, a console command, or a consumer, so the business rule becomes reachable from exactly one transport.

**An Eloquent model does not cross a public contract.** Serializing a model publishes whatever columns and loaded relations happen to exist at that moment, so a migration becomes a breaking API change. Cross the boundary with a DTO and serialize through a Resource.

**Absence and null are different facts at the DTO boundary.** The DTO is the layer where a PATCH that clears a field is distinguished from a PATCH that does not mention it, because it is the last place both facts still exist — after it, one has been collapsed into the other. The rule for expressing the distinction is `alaa-php-clean-code references/laravel-best-practices.md`, "Partial updates (PATCH semantics)"; this skill adds only that the DTO, not the Service and not the model, is where it is expressed.

## Identifiers

- A response exposes the public identifier and never an internal key. This is **mandatory**, not a preference: an exposed internal key becomes a URL a client stores, and from then on the key's format, its sequence, and the row count it leaks are part of the public contract.
- Route binding and request filters accept the public identifier. The Repository resolves it.
- A Repository may hold the internal key. Nothing above it may.
- The identifier's **format, its field name, and the validation rule that accepts it** are `/alaa-services-contract`'s (`$alaa-services-contract`); this skill owns only which layer knows which identifier.

`scripts/architecture-gate.sh` check `L2-public-id-leak` fails a build on the mechanical form of this defect.

## Persistence naming versus public naming

These are two namespaces, and the Resource, DTO, and FormRequest boundary is where they are translated.

- Persistence-facing identifiers stay `lower_snake_case`: tables, columns, indexes, constraints, and the raw attribute names used by Repositories, factories, seeders, and database assertions.
- A public contract that already uses a different spelling keeps it, translated at the boundary. Do not rename a column to match a public field, and do not rename a public field to match a column: one breaks a deployed client, the other breaks every query.

## Where the response envelope is produced

- A success response is produced by a Resource. No Controller assembles one.
- An error response is produced by one framework exception handler, from a domain exception a Service raised. No Controller assembles one, because an envelope assembled at N call sites drifts at N call sites — see `references/50-failure-recovery.md` for what that drift looks like once it is in production.
- The envelope's **keys, its error code names, its casing rule, and what may go in `meta`** are fixed exactly by `alaa-services-contract references/10-core-service-contract.md`. This skill states no key and no code name.

**When the repository's existing envelope does not conform:** do not silently refactor it inside a feature change, and do not leave it. Migrate it through the deprecation procedure in `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`. When that window cannot be opened within the current change, record the divergence in the repository's own `AGENTS.md`, name the route group affected, and report it in the change's summary. Silence here is what leaves two endpoint families answering differently for a year.

## Validation

Every write endpoint validates in a FormRequest. A Controller passes `validated()` onward and adds nothing. A Service performs no field validation: it enforces invariants, which are statements about domain state, not about input shape. Config keys are validated separately — `references/70-config-contract.md`.

## Lists

A list route paginates by keyset cursor; offset pagination is forbidden fleet-wide by `alaa-services-contract references/25-end-to-end-flow-and-boundaries.md`, and the maximum page size is a value in `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`. Whether a route paginates at all, its ordering tuple, its index, and the cursor's contents belong to `/alaa-keyset-pagination` (`$alaa-keyset-pagination`).

This skill owns only the placement: the cursor and the page size arrive as a typed filter DTO, and the Repository translates the cursor into a predicate. A Controller that builds a cursor, or a Service that receives raw query parameters, has moved the pagination contract into the wrong layer.

## Upstream rules this skill overrides

A production Laravel repository may ship `.agents/skills/laravel-best-practices/`. **That skill is not owned by this repository, can be re-pulled or reworded between runs, and loses to this skill on every rule below.**

- Its `rules/architecture.md` demonstrates `Context::add('tenant_id', $request->header('X-Tenant-ID'))`. **Tenant identity never comes from a client-supplied header.** Derivation is `/alaa-trust-gateway-auth`'s (`$alaa-trust-gateway-auth`); copying that example makes every tenant boundary in the service forgeable by the caller.
- Its `rules/architecture.md` Action example calls Eloquent directly and takes `array $data`. Both edges are forbidden here: the persistence call goes through the repository interface and the input crosses as a DTO. Use its Action shape only inside those two constraints.
- Its `rules/caching.md` recommends `once()` for per-request memoization. Under a long-lived worker, the lifetime of a service the worker resolved once is the worker's lifetime, so `once()` on such a service is cross-request state — a memoized roles or permissions lookup returns the first request's answer to every later request on that worker. `/alaa-octane-performance` (`$alaa-octane-performance`) owns what a worker may retain.
- Its `rules/style.md` forbids comments outside config files. Invariant docblocks and test-intent comments are required regardless.
