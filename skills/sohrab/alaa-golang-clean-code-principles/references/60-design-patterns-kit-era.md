# Design Patterns, Kit-Era — What Each Classic Pattern Becomes on This Platform

This file is a **decision map**, not a catalog: for each classic (GoF) pattern it names the shape that
pattern takes in an `alaa-go-chi` service, which principle governs it, and when reaching for it is wrong.
Pattern *mechanics* (functional options, constructor idioms, resilience wrappers, iterator internals) are
owned by `golang-design-patterns` and friends via the `alaa-golang` router (`50-skill-boundaries.md`) —
never re-derive them here. In Go, most patterns dissolve into interfaces, functions, and composition; the
platform question is never "how do I implement X" but "which kit or principle already owns X's job".

## Recognize by symptom first

Pick the pattern from the pain you can point at, then confirm with the discriminating question — a "no"
means a different pattern (or none).

| Observable symptom | Pattern | Confirming question |
|---|---|---|
| The same multi-step lifecycle re-written per worker/seeder/consumer | Template Method (kit skeleton) | Does a kit runner already own this skeleton? (P1 — almost always yes) |
| A growing set of pre-handler checks, each able to reject the request | Chain of Responsibility (middleware) | Declared once at the route family, order visible? (P2) |
| One payload transformed by ordered steps that ALL run | Pipeline (ordered typed stages) | Does every stage always run and pass the payload on? |
| An action must leave the process: queued, retried, replayed, audited | Command (outbox message + consumer) | Is the action a snake_case-tagged wire struct written in the producing tx? (P6, P8) |
| Provider names, payload shapes, or errors leaking into use cases | Adapter (port implementation) | Is the translation confined to the infrastructure adapter? (P4, P5) |
| A use case imports pgx/amqp/Redis/SDK and cannot be tested with fakes | Dependency Inversion (port) | Can a fake implement the port and pass the same contract test? (P5, P12) |
| A cross-cutting concern (metrics, cache, logging) needed on an existing port | Decorator (same-interface wrapper) | One concern, contract-identical, always delegates? |
| Calls must be refused/deferred under failure (breaker open, rate limit) | Proxy | May the wrapper legitimately *not* call the inner port, observably? |
| `switch` on provider/channel/mode repeated across use cases | Strategy (implementations as data) | One narrow port, selection in one boot/policy site? (P10) |
| Status booleans multiplying, or status writes scattered across files | State (typed vocabulary + one authority) | Named states, guarded transitions, idempotent replays? (P7, P10) |
| Provider pieces resolved separately that must match each other | Abstract Factory (suite struct at boot) | ≥2 members whose implementations must pair? (P10) |
| Adapter names concatenating two variation axes | Bridge (two orthogonal ports) | Are the axes genuinely independent? (P5) |
| Workers/consumers coordinating with each other directly in-process | Mediator (the use case) / outbox | Should this coordination be a broker fact instead? (P6, P13) |
| "Restore prior state" or compensation needed after failure | Memento (audit pre-image in the same tx) | Is the pre-image durable and written by its owner? (P6) |
| The same kind-`switch` repeated once per operation | Visitor (handler map per operation) | Stable kind set, operations keep arriving? (P10) |
| Shared clients or config constructed lazily via package globals | Singleton (boot-owned instance) | Is construction owned once in boot wiring, with no lazy `sync.Once` globals? (P10) |
| Env/provider/mode construction branching duplicated at call sites | Factory Method (boot constructor) | Does one boot-site constructor own the branching? (P10) |
| Long positional constructors or half-initialized structs escaping | Builder / functional options | Are invariants enforced before the value escapes? |
| Recursive domain trees special-casing leaf vs group | Composite | Can leaf and group honestly share one small interface? |
| Several parties must learn about one domain fact | Observer (outbox event + consumers) | Should listeners be broker consumers instead of in-process calls? (P6, P8) |
| Hand-rolled traversal state over collections or streams | Iterator (`range`, `iter.Seq`) | Does a typed sequence express it without index bookkeeping? |
| Callers need a simpler surface over a subsystem | Facade (kit-owned) | Is the kit the right owner of that surface? (P1) |

## Look-alike disambiguation

- **Adapter vs Decorator vs Proxy vs Facade**: Adapter *changes* an interface to fit the port the application owns; Decorator *keeps* the interface and adds one concern, always delegating; Proxy *keeps* the interface but may refuse or defer the inner call (typed `errkit` denial, never silence); Facade is a simpler surface over a subsystem — on this platform, that is the kit's job (P1), not yours.
- **CoR vs Pipeline**: middleware handlers may reject-and-stop, and chain-end behavior is kit-defined; pipeline stages all run and transform one payload — pretending a transform pipeline can "short-circuit on handled" hides errors.
- **Command vs Strategy**: Strategy is interchangeable ways of doing the same operation behind one port; Command reifies *that an operation was requested* so it survives crashes and retries — on this platform, a command that matters is an outbox row, not an in-memory dispatch (P6).
- **Template Method vs Strategy**: the skeleton is fixed and steps vary → kit runner + your step funcs; the whole algorithm varies at runtime → a port with swappable implementations.

## The map: pattern → kit-era shape

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
| Pipeline | ordered typed stages over one payload; every stage runs | P5 |
| Dependency Inversion | P5 itself: ports owned by the application, adapters outside | P5, P12 |
| Abstract Factory | provider suite = struct of matching port implementations wired at boot | P5, P10 |
| Prototype | value-copy semantics; explicit deep copies for slices/maps; no clone frameworks | P8 |
| Bridge | two orthogonal ports (what × how) instead of an adapter matrix | P5 |
| Flyweight | shared immutable config/lookup tables; optimization only, measured need | P10 |
| Mediator | the use case is the mediator; no in-process component hubs | P5, P6 |
| Memento | pre-images persisted as audit rows / receipts, never in-memory undo | P6 |
| Visitor | exhaustive type/kind switch or handler map on typed constants; no accept() machinery | P10 |

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
checks, recovery outermost. Chain-end behavior is defined by the kit (unmatched → canonical 404/405
envelope; unauthorized → typed denial) — a hand-rolled chain whose unhandled requests fall through
silently is the classic CoR bug and a P1 violation twice over. Services never hand-assemble ad-hoc handler
chains or insert middleware that re-implements a kit link (P1). Outside HTTP, prefer an explicit ordered
slice of typed steps over a linked hand-off chain — Go readers should see the order, not chase `next`
pointers.

## Pipeline

Sequential transformation of one payload through ordered stages that all run — distinct from CoR because
no stage short-circuits on "handled"; a stage either transforms the payload or returns a typed error that
ends the run. The Go shape is deliberately plain: an ordered slice of `func(ctx context.Context, p *Payload) error`
executed in a loop, declared and tested as one composed unit. Use it where a use case's preparation steps
(normalize → enrich → validate → stamp) are genuinely independent and reorderable; do not build pipeline
machinery for two calls, and do not let stages hide IO — side effects stay behind ports (P5) and stage
order stays visible at the call site.

## Dependency Inversion

Not a pattern to "apply" here — it is P5, already mandatory: the application owns small consumer-shaped
ports; infrastructure implements them; imports flow inward only. The recognition signals are the useful
part: a use case that cannot be tested with fakes, a provider swap that edits business files instead of
one wiring site in `main`, or a port that mirrors pgx/SQL/SDK method names instead of what the use case
needs — each means the dependency arrow points outward and must be inverted. Contract tests at the port
(P12) are what keep every implementation, fake, and decorator honestly substitutable.

## The remaining classics, kit-era stances

- **Abstract Factory** — the need is real when a provider requires several *matching* pieces (sender +
  delivery-report parser + webhook verifier): define the suite as one struct of ports, construct one
  concrete suite per provider at boot, select by config (P10). Members resolved independently from config
  in different places is the bug this prevents. No factory-of-factories machinery.
- **Prototype** — Go's value semantics make copies free; the pattern reduces to: copy deliberately.
  Slices, maps, and pointers inside copied structs still alias (aliasing depth: `golang-safety`); deep-copy
  explicitly where mutation follows. Preset wire payloads are plain exported values copied on use. Never
  build a `Clone()` framework for data that assignment already copies.
- **Bridge** — when adapter names start concatenating two axes (`BaleTemplateRenderer`,
  `MedianaPlainRenderer`), split into two orthogonal ports: what is produced (renderer) × how it is
  delivered (channel client). Each axis grows independently; wiring at boot pairs them. An adapter matrix
  that doubles per new value on either axis is the recognition signal.
- **Flyweight** — legitimate only as shared *immutable* lookup tables and config loaded once at boot
  (P10). Go's real memory answers are streaming, bounded batches, and profiling
  (`golang-performance`); never introduce sharing machinery without a measured problem.
- **Mediator** — the use case already plays this role: handlers, workers, and consumers never coordinate
  with each other directly; they call use cases, and cross-service coordination travels as broker facts
  (P6, P13). An in-process hub where components subscribe to each other is the Observer ban wearing a
  different name.
- **Memento** — "restore prior state" on this platform means durable pre-images: audit rows written in the
  same transaction (P6), receipts, and status history — never in-memory undo stacks that a crash erases.
  The originator writes its own pre-image; consumers of audit data never reconstruct it from live tables.
- **Visitor** — Go has no double dispatch; the honest forms are an exhaustive `switch` on a typed
  kind/constant (P10) closed by a default that fails loudly, or a handler map keyed by kind — one map per
  operation. Choose it when operations keep arriving over a stable kind set; if kinds keep arriving,
  put the behavior on the type instead. `accept()` hierarchies are un-idiomatic here; for AST-scale
  traversal precedents route to the `alaa-golang` tree.

## Code smells → where the repair lives

Smell vocabulary (bloaters, OO abusers, change preventers, dispensables, couplers) is useful for naming
review findings; the platform routing for repairs: bloaters and line-level clarity → `golang-code-style`
via the router; couplers (feature envy, reach-ins, message chains) → P5/P13 (ports, contracts, no
reach-ins); change preventers (shotgun surgery on codes/events/metrics) → P10 vocabulary constants;
dispensables (dead code, speculative interfaces with one implementation and no seam) → delete, per the
kit-first rule that unused shared shapes belong to the kit or nowhere. The Rule of Three applies to
service-local helpers; anything needed by two services is kit intake (P1), not a third copy.
