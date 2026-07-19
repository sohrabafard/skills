# refactoring.guru distilled notes — Structural patterns (research agent output, 2026-07-19)

Source pages: bridge, composite, facade, flyweight, proxy.

## Bridge

**Problem**: extending a class along two or more independent dimensions (Shape × Color, abstraction × platform) forces a subclass per combination — geometric class growth.

**Applicability signals**
- Divide a monolithic class that has several variants of some functionality (e.g., works with various database servers).
- Extend a class in several orthogonal dimensions — extract each dimension into its own hierarchy; the original delegates.
- Switch implementations at runtime (reassigning the implementation field).

**Implementation essentials**: identify orthogonal dimensions; Abstraction holds a reference to Implementation and delegates; Refined Abstractions and Concrete Implementations grow independently; client passes the implementation into the abstraction's constructor.

**Pros/Cons**: platform-independent high-level classes, OCP/SRP per axis; can overcomplicate a cohesive class.

**Relations**: vs Adapter — Bridge is designed up-front, Adapter retrofits incompatible existing code. vs Strategy/State — near-identical structure, different intent. Abstract Factory can encapsulate legal abstraction/implementation pairings.

**Recognition heuristic**: class names concatenating two variation axes (`BlueCircle`, `MySqlReportExporter`) or a subclass grid doubling whenever either axis grows.

## Composite

**Problem**: tree-structured data forces clients to know concrete classes, nesting, traversal.

**Applicability signals**: the core model is genuinely a tree; clients should treat simple and complex elements uniformly.

**Implementation essentials**: Component interface with only methods meaningful for both; leaves do real work; container delegates to children and aggregates; child management on the container (or on the interface, trading purity for uniformity).

**Pros/Cons**: polymorphic recursion, OCP; hard when leaf/container functionality differs too much (over-generalized interface).

**Relations**: vs Decorator — same recursive shape, but Decorator has ONE child and adds responsibilities; Composite has MANY children and sums their results. Pairs with Iterator/Visitor (traversal), Flyweight (shared leaves), CoR (leaf passes request up parent chain), Prototype (clone assembled trees), Builder (recursive construction).

**Recognition heuristic**: `instanceof`/type-switching plus manual recursion over nested containers to aggregate something.

## Facade

**Problem**: integrating a complex subsystem couples business logic to init rituals, dependency order, and third-party details.

**Applicability signals**: need a limited, straightforward interface to a complex subsystem; structure a subsystem into layers with one entry point per layer (subsystems talk only via facades).

**Implementation essentials**: verify a simpler interface is possible; facade owns subsystem init/lifecycle; route all client communication through it; split refined facades when one bloats.

**Pros/Cons**: isolates from complexity; risk of becoming a god object coupled to everything.

**Relations**: vs Adapter — facade defines a NEW interface, adapter makes an existing one usable; adapter wraps one object, facade a subsystem. vs Proxy — proxy keeps the SAME interface. vs Mediator — facade adds no new functionality and parts still talk directly; mediator centralizes communication, components know only the mediator. Facades often end up Singletons.

**Recognition heuristic**: the same multi-step init-and-call ritual against a subsystem copy-pasted across business logic.

## Flyweight

**Problem**: huge numbers of similar objects with duplicated per-object data exhaust RAM.

**Applicability signals (ALL must hold — narrowest GoF pattern)**: huge numbers of similar objects; RAM genuinely exhausted; objects contain duplicate extractable state. Optimization only — never preemptive.

**Implementation essentials**: split intrinsic (constant, shared, must be immutable) from extrinsic (contextual) state; methods take extrinsic state as parameters; a factory manages the shared pool.

**Pros/Cons**: large RAM savings; trades RAM for CPU and adds real complexity.

**Relations**: vs Singleton — many immutable instances differing in intrinsic state vs one mutable instance. vs Facade — opposites (many tiny shared vs one big). With Composite — shared leaf nodes.

**Recognition heuristic**: memory profile dominated by thousands of instances carrying identical heavy fields.

## Proxy

**Problem**: control access to a massive/sensitive object you can't modify; duplicating guard/lazy-init code in every client is untenable.

**Applicability signals — six scenarios**: lazy initialization (virtual proxy); access control (protection proxy); remote proxy; logging proxy; caching proxy; smart reference (dismiss heavyweight object when unused).

**Implementation essentials**: extract a service interface so proxy and service are interchangeable; proxy holds and usually manages the service's lifecycle; each method does its added work then delegates; a creation method decides proxy vs real service.

**Pros/Cons**: control without clients knowing; works when service not ready; more classes, possible latency.

**Relations**: interface test — Adapter = different interface; Proxy = same; Decorator = enhanced. Lifecycle test — proxy manages its service's lifecycle itself; decorator stacking is client-controlled. vs Facade — proxy is interchangeable with its service; facade is not.

**Recognition heuristic**: the same pre-call ceremony (guard, cache lookup, connection, logging, lazy creation) repeated around calls to one service.
