# Design Patterns, Kit-Era — What Each Classic Pattern Becomes on This Platform

This file is a **decision map**, not a catalog: which pattern a symptom indicates, which kit surface or
principle already owns that pattern's job, and which look-alike it is not. It ships no implementation mechanic
— every idiom, code shape, and internal belongs to `/golang-design-patterns` (`$golang-design-patterns`) and its
neighbours through the `/alaa-golang` (`$alaa-golang`) router. In Go most patterns dissolve into interfaces,
functions, and composition; the platform question is never "how do I implement X" but "which kit or principle
already owns X's job".

## Recognize by symptom first

Pick the pattern from the pain you can point at, then confirm with the discriminating question — a "no" means a
different pattern, or none.

| Observable symptom | Pattern | Confirming question |
|---|---|---|
| The same multi-step lifecycle re-written per worker/seeder/consumer | Template Method (kit skeleton) | Does a kit runner already own this skeleton? (P1 — almost always yes) |
| A growing set of pre-handler checks, each able to reject the request | Chain of Responsibility (middleware) | Declared once at the route family, order visible? (P2) |
| One payload transformed by ordered steps that ALL run | Pipeline (ordered typed stages) | Does every stage always run and pass the payload on? |
| An action must leave the process: queued, retried, replayed, audited | Command (outbox message + consumer) | Is the action a snake_case-tagged wire struct written in the producing tx? (P6, P8) |
| Provider names, payload shapes, or errors leaking into use cases | Adapter (port implementation) | Is the translation confined to the infrastructure adapter? (P4, P5) |
| A use case imports pgx/amqp/Redis/SDK and cannot be tested with fakes | Dependency Inversion (port) | Can a fake implement the port and pass the same contract test? (P5, P12) |
| A cross-cutting concern (metrics, cache, logging) needed on an existing port | Decorator (same-interface wrapper) | One concern, contract-identical, always delegates? |
| Calls must be refused or deferred under failure (breaker open, rate limit) | Proxy | May the wrapper legitimately *not* call the inner port, observably? |
| `switch` on provider/channel/mode repeated across use cases | Strategy (implementations as data) | One narrow port, selection at one boot or policy site? (P10) |
| Status booleans multiplying, or status writes scattered across files | State (typed vocabulary + one authority) | Named states, guarded transitions, idempotent replays? (P7, P10) |
| Provider pieces resolved separately that must match each other | Abstract Factory (suite struct at boot) | Two or more members whose implementations must pair? (P10) |
| Adapter names concatenating two variation axes | Bridge (two orthogonal ports) | Are the axes genuinely independent? (P5) |
| Workers/consumers coordinating with each other directly in-process | Mediator (the use case) / outbox | Should this coordination be a broker fact instead? (P6, P13) |
| "Restore prior state" or compensation needed after failure | Memento (audit pre-image in the same tx) | Is the pre-image durable and written by its owner? (P6) |
| The same kind-`switch` repeated once per operation | Visitor (handler map per operation) | Stable kind set, operations still arriving? (P10) |
| Shared clients or config constructed lazily via package globals | Singleton (boot-owned instance) | Is construction owned once in boot wiring, with no lazy globals? (P10) |
| Env/provider/mode construction branching duplicated at call sites | Factory Method (boot constructor) | Does one boot-site constructor own the branching? (P10) |
| Long positional constructors or half-initialized structs escaping | Builder / functional options | Are invariants enforced before the value escapes? |
| Recursive domain trees special-casing leaf vs group | Composite | Can leaf and group honestly share one small interface? |
| Several parties must learn about one domain fact | Observer (outbox event + consumers) | Should listeners be broker consumers instead of in-process calls? (P6, P8) |
| Hand-rolled traversal state over collections or streams | Iterator | Does a typed bounded sequence express it without index bookkeeping? |
| Callers need a simpler surface over a subsystem | Facade (kit-owned) | Is the kit the right owner of that surface? (P1) |

## Look-alike disambiguation

- **Adapter vs Decorator vs Proxy vs Facade.** Adapter *changes* an interface to fit the port the application
  owns. Decorator *keeps* the interface and adds one concern, always delegating. Proxy *keeps* the interface but
  may refuse or defer the inner call — a typed `errkit` denial, never silence. Facade is a simpler surface over
  a subsystem, and here that is the kit's job (P1), not yours.
- **CoR vs Pipeline.** Middleware handlers may reject and stop, and chain-end behavior is kit-defined. Pipeline
  stages all run and transform one payload; pretending a transform pipeline can "short-circuit on handled" hides
  errors.
- **Command vs Strategy.** Strategy is interchangeable ways of doing the same operation behind one port. Command
  reifies *that an operation was requested* so it survives crashes and retries — here, a command that matters is
  an outbox row, not an in-memory dispatch (P6).
- **Template Method vs Strategy.** Skeleton fixed and steps vary → kit runner plus your step funcs. Whole
  algorithm varies at runtime → a port with swappable implementations.
- **Visitor vs polymorphism.** Operations keep arriving over a stable kind set → Visitor. Kinds keep arriving →
  put the behavior on the type instead.

## The map: pattern → kit-era shape

| Pattern | Kit-era shape | Governing principle |
|---|---|---|
| Singleton | composition root in `main` (via `runkit`) wires once and injects downward; no package-level mutable state, no `init()` wiring, no lazy `sync.Once` in service code | P10 |
| Factory Method | `NewX(...)` returning the consumer's interface; variant selection is a map from typed config key to constructor, resolved once at boot | P5, P10 |
| Builder | validated config structs, immutable after boot; functional options belong to library-shaped code, not service business code | P10 |
| Adapter | infrastructure implementing application-owned ports; provider errors become typed `errkit` values at the adapter and provider payload names never leak inward | P4, P5 |
| Decorator | contract-identical interface wrappers, one concern each; a wrapper needing extra public methods means the abstraction is wrong | P5, P11 |
| Facade | kit packages over infrastructure; use cases over multi-port flows | P1 |
| Proxy | wrappers controlling *whether or when* the real call happens (breaker, limiter, read-through cache); a refusal is a typed `errkit` error with retryability set and its own metric and log vocabulary | P4, P9, P11 |
| Composite | predicate and rule conjunction trees (`audiencekit`-style); leaf and group contract-identical, so no "is this a group?" type switch in callers | P13 |
| Observer | banned in-process for domain facts — outbox plus broker consumers instead | P6 |
| Strategy | strategies-as-data behind one port, selection explicit in config or database rows; every implementation passes the same contract test | P5, P10, P12 |
| Command | wire command payloads plus idempotent consumers and workers; ids and typed data, never fat object graphs | P6, P7, P8 |
| Iterator | bounded batches only — paged or keyset repositories, chunked consumers; unbounded materialization is a review failure, and an iterator owning a goroutine obeys P9 | P9 |
| State | typed status vocabulary, append-only like error codes, plus exactly one transition authority; replaying `publish` on a published row is a no-op, not an error and not a second outbox row | P7, P10 |
| Template Method | kit owns the skeleton, service fills the steps; funcs, not inheritance | P1 |
| Chain of Responsibility | the kit-owned middleware chain, declared once; trust parsing before permission checks, recovery outermost | P1, P2 |
| Pipeline | ordered typed stages over one payload, every stage runs, order visible at the call site, no stage hides IO | P5 |
| Dependency Inversion | P5 itself: ports owned by the application, adapters outside | P5, P12 |
| Abstract Factory | one struct of matching port implementations per provider, wired at boot; members resolved independently in different places is the bug it prevents | P5, P10 |
| Prototype | copy deliberately; no `Clone()` framework for data that assignment already copies | P8 |
| Bridge | two orthogonal ports (what × how) instead of an adapter matrix | P5 |
| Flyweight | shared immutable lookup tables loaded once at boot; sharing machinery needs a measured problem | P10 |
| Mediator | the use case is the mediator; an in-process hub where components subscribe to each other is the Observer ban under another name | P5, P6 |
| Memento | pre-images persisted as audit rows or receipts by their own owner, never in-memory undo | P6 |
| Visitor | exhaustive kind switch closed by a loud default, or one handler map per operation; no `accept()` machinery | P10 |

## Traps the tables cannot carry

- **Observer.** About to write `Subscribe(func(...))` for anything a rollback could invalidate or another
  service cares about? Stop — that is an outbox row.
- **Template Method.** Never emulate the class-based form with struct embedding and overridable methods.
  Embedding is not overriding, and the half-overridden result is exactly the dual behavior P1 forbids.
- **Chain of Responsibility.** Chain-end behavior is kit-defined: an unmatched route renders the canonical
  404/405 envelope, an unauthorized one a typed denial. A hand-assembled chain whose unhandled request falls
  through silently is the classic CoR bug and a P1 violation twice over.
- **Facade.** A facade over a kit facade is drift. Do not add "manager" or "helper" orchestration layers above
  use cases to simplify what a well-named use case should already express.
- **Factory Method.** When selection logic outgrows the map, surface the design problem; do not absorb it into a
  runtime registry or a factory-of-factories.
- **Command.** No in-process command bus dispatching through reflection or string keys — route the work through
  the broker or call the use case directly.
- **Composite.** Guard depth and cycles when the tree is user- or wire-shaped; the composite evaluates, it does
  not hide IO per node.
- **Dependency Inversion — the recognition signals.** A use case that cannot be tested with fakes; a provider
  swap that edits business files instead of one wiring site in `main`; a port mirroring pgx, SQL, or SDK method
  names instead of what the use case needs. Each means the dependency arrow points outward.

## Code smells → where the repair lives

Smell vocabulary — bloaters, OO abusers, change preventers, dispensables, couplers — is useful for naming a
review finding. The repair routing: bloaters and line-level clarity → `/golang-code-style`
(`$golang-code-style`) through the router; couplers (feature envy, reach-ins, message chains) → P5 and P13,
meaning ports and contracts; change preventers (shotgun surgery across codes, events, metrics) → P10 vocabulary
constants; dispensables (dead code, a speculative interface with one implementation and no seam) → delete it.
The Rule of Three applies to service-local helpers; anything a second service needs is kit intake (P1), not a
third copy — file it through `/alaa-go-chi-development` (`$alaa-go-chi-development`).
