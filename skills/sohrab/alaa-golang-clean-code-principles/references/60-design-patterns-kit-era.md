# Design Patterns, Kit-Era — What Each Classic Pattern Becomes on This Platform

This file is a **decision map**, not a catalog: for each classic (GoF) pattern it names the shape that
pattern takes in an `alaa-go-chi` service, which principle governs it, and when reaching for it is wrong.
Pattern *mechanics* (functional options, constructor idioms, resilience wrappers, iterator internals) are
owned by `golang-design-patterns` and friends via the `alaa-golang` router (`50-skill-boundaries.md`) —
never re-derive them here. In Go, most patterns dissolve into interfaces, functions, and composition; the
platform question is never "how do I implement X" but "which kit or principle already owns X's job".

| Pattern | Kit-era shape | Governing principle |
|---|---|---|
| Singleton | composition root in `main` wires once; no package-level mutable state | P10 |
| Factory Method | `NewX(...)` constructors returning the consumer's interface | P5 |
| Builder | validated config structs; functional options only in library-shaped code | P10 |
| Adapter | infrastructure implementing application-owned ports | P5 |
| Decorator | contract-identical interface wrappers; `http.Handler` middleware | P5, P11 |
| Facade | kit packages over infra; use cases over multi-port flows | P1 |
| Proxy | wrappers controlling *whether/when* the real call happens (breaker, limiter) | P4, P9 |
| Composite | predicate/rule conjunction trees (`audiencekit`-style), uniform leaf/group | P13 |
| Observer | banned in-process for domain facts — outbox + broker instead | P6 |
| Strategy | strategies-as-data behind one port; selection explicit in config/DB | P5, P10 |
| Command | wire command payloads + idempotent consumers/workers | P6, P7, P8 |
| Iterator | bounded batches; `iter.Seq` range-over-func for streaming | P9 |
| State | typed status vocabulary + one transition authority | P7, P10 |
| Template Method | kit owns the skeleton, service fills the steps; funcs, not inheritance | P1 |
| Chain of Responsibility | the kit-owned middleware chain, declared once | P1, P2 |

## Singleton

The only sanctioned singleton is the composition root: `main` (via `runkit`) constructs each dependency
once at boot and injects it downward. Package-level mutable variables, `init()`-time wiring, and ad-hoc
`sync.Once` lazies in service code are review failures — they hide dependencies, break test isolation, and
smuggle state past P10's config-at-boot rule. If something must exist once process-wide, it is constructed
once in `main`, not enforced by a `GetInstance`.

## Factory Method

The Go form is a constructor: `NewPostgresNewsRepo(pool) NewsRepo` — concrete in, interface out, returning
the port the *consumer* owns (P5). Provider/variant selection is a factory as data: a map from typed
config keys to constructors, resolved once at boot. Do not build abstract-factory hierarchies or
runtime-registry factories; when selection logic outgrows a map, that is a design smell to surface, not
abstract away.

## Builder

Kit packages accept validated config structs (`configkit` output) — that is the platform's construction
story, and services should mirror it: a plain struct, validated in the constructor, immutable after boot.
The functional-options idiom (mechanics: `golang-design-patterns`) belongs in library-shaped code with many
optional knobs — kit packages themselves, not service business code. A service use case needing a builder
for its own domain objects usually means the wire struct or config struct is doing too many jobs.

## Adapter

This is P5's outward half, already mandatory: every side effect crosses a port the application owns, and an
infrastructure adapter (pgx, amqp, Redis, provider SDK) implements it. Kit-era additions: provider adapters
translate provider errors into typed `errkit` values at the adapter (P4), never let provider payload names
leak inward, and mark unknown provider behavior `NEEDS_<PROVIDER>_CONFIRMATION` (P13) instead of guessing.

## Decorator

Wrap a port with the same interface to add one cross-cutting concern: an instrumented repo that times and
counts (kit metric names, bounded labels — P11), a caching read wrapper, a logging wrapper in tests. Rules:
one concern per decorator; contract-identical surface (if the wrapper needs extra public methods the
abstraction is wrong); the inner error contract passes through untouched except the decorator's own
infrastructure failures. `httpkit`'s middleware chain is this pattern applied to `http.Handler` — and it is
kit-owned; never re-implement it (P1).

## Facade

The kit packages *are* the platform's facades: `httpkit`, `pgkit`, `mqkit`, `trustkit` each give one simple
surface over messy infrastructure — which is why P1 forbids re-wrapping them (a facade over a facade is
drift). Inside a service, the use case is the facade over multi-port flows; do not add "manager"/"helper"
orchestration layers above use cases to simplify what a well-named use case should already express.

## Proxy

A proxy shares the port's interface but controls whether or when the real call happens: circuit breakers
and rate limiters around provider ports, in-flight deduplication, read-through caches that may skip the
inner call. Distinguish from Decorator by intent — decorator always delegates and adds behavior; proxy may
*refuse* (open breaker → immediate typed `errkit` error with retryability set, P4). Denial-by-proxy must
be observable (its own metric/log vocabulary, P11) and must never silently swallow the call.

## Composite

Uniform treatment of leaf and group through one small interface, evaluated recursively: audience predicates
conjoined the way `audiencekit` does (the canonical example — and because that logic must be identical
everywhere, it lives in the kit, P13), spec-style filter/eligibility rules (`AllOf`/`AnyOf` over one
`Rule` interface), stdlib composites like `io.MultiReader`. Rules: leaf and composite are
contract-identical (no "is this a group?" type-switches in callers); depth and cycles are guarded when the
tree is user- or wire-shaped; the composite evaluates — it does not hide IO per node.

## Observer

For domain facts, in-process observer/event-emitter registries are **banned**: a subscriber list inside the
process is exactly the dual-behavior, lost-on-crash notification path P6 exists to kill. Facts leave the
service through the outbox in the state-change's transaction, and observers are broker consumers with
receipts and idempotent handling (P7). If you are about to write `Subscribe(func(...))` for anything a
rollback could invalidate or another service cares about — stop; that is an outbox row.

## Strategy

Strategies-as-data behind one port: per-channel senders, per-provider clients, per-category routing — one
small interface, implementations chosen by explicit configuration or database rows (routing policies), not
by `switch` statements scattered through use cases. Selection lives in one place (boot wiring or a policy
lookup), selection inputs are typed constants (P10), and every implementation passes the same contract test
so swapping providers stays a data change, not a code hunt.

## Command

A command is a wire message: an explicit snake_case-tagged payload (P8) written to the outbox in the
producing transaction (P6) and executed by an idempotent consumer or worker proven by a run-twice test
(P7). The queued job carries ids and typed data, never fat object graphs. In-process command buses that
dispatch to handlers through reflection or string keys re-create the observer problem with extra steps —
route work through the broker or call the use case directly.

## Iterator

Traversal is bounded by construction: repositories expose paged/keyset batches, consumers process bounded
chunks, and unbounded `SELECT *` materialization is a review failure. For streaming shapes, Go's
range-over-func iterators (`iter.Seq`, Go 1.23+) are the modern idiom — mechanics and migration guidance
belong to `golang-modernize`/`golang-data-structures` via the router. An iterator that owns a goroutine
must obey P9: cancellable via `context`, drained, never leaked past its consumer.

## State

Domain lifecycles are typed status vocabularies (P10 constants, string-valued, append-only like error
codes) plus exactly one transition authority: the use case that owns the aggregate checks the transition
table and rejects impossible moves with a typed `errkit` error (P4). Status writes scattered across
handlers, workers, and seeders are how illegal states ship. Transitions that retries can replay must be
idempotent (P7): re-running "publish" on an already-published row is a no-op, not an error and not a second
outbox row.

## Template Method

Go has no inheritance, and the kit-era answer is better: **the kit owns the skeleton, the service fills the
steps.** `runkit`'s worker lifecycle, `seedkit`'s runner, `outboxkit`'s relay loop are template methods —
ordered, drained, observable skeletons where your code supplies only the domain step. Service-local
skeletons are plain functions taking funcs (or a one-method interface per step). Never emulate the
class-based form with struct embedding and overridable methods — embedding is not overriding, and the
half-overridden result is exactly the dual behavior P1 forbids.

## Chain of Responsibility

The middleware chain is this pattern, and it is declared once, kit-side, in the router builder — recovery,
correlation, trust parsing, then per-route-family additions (`trustkit.RequirePermission`,
`RequireTOTP`) readable at the route declaration (P2). Order is contract: trust parsing before permission
checks, recovery outermost. Services never hand-assemble ad-hoc handler chains or insert middleware that
re-implements a kit link (P1). Outside HTTP, prefer an explicit ordered slice of typed steps over a linked
hand-off chain — Go readers should see the order, not chase `next` pointers.
