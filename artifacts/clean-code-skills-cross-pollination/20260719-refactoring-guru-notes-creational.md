# refactoring.guru distilled notes — Creational patterns (research agent output, 2026-07-19)

Source pages: factory-method, abstract-factory, builder, prototype, singleton.

# Factory Method

**Problem**
Code becomes tightly coupled to concrete classes (e.g., a logistics app hard-wired to `Truck`); adding a new type (`Ship`) forces edits across the codebase and breeds scattered conditionals that switch behavior on object type.

**Applicability signals**
- Use when you don't know beforehand the exact types and dependencies of the objects your code should work with — it separates construction from usage, so new product subclasses can be added without touching existing code.
- Use when you want to let users of your library or framework extend its internal components — expose an overridable factory method instead of hard-coding component types.
- Use when you want to save system resources by reusing existing objects instead of rebuilding them — a constructor must return a new object, but a factory method can implement pooling.

**Implementation essentials**
- Give all products a common interface; the factory method returns that interface type.
- Replace direct constructor calls with calls to the factory method.
- Subclass-per-product, or a parameter on the factory method to select among products.

**Pros / Cons**
- Pros: decouples creator from concrete products; centralizes creation (SRP); new products without breaking client code (OCP).
- Cons: many new subclasses raise complexity.

**Relations**
- "Entry-level" creational pattern: designs start with Factory Method and evolve toward Abstract Factory, Prototype, or Builder.
- Abstract Factory is frequently implemented as sets of Factory Methods; factory method can be a step in a Template Method.
- Vs Prototype: Prototype isn't inheritance-based but requires complicated clone initialization.

**Recognition heuristic**
`new ConcreteClass()` scattered through business logic plus `if/switch` on a type flag deciding which class to instantiate.

# Abstract Factory

**Problem**
Creating families of related products in multiple variants while keeping them consistent — objects from one family must match each other — without modifying existing code per new variant.

**Applicability signals**
- Code needs to work with various families of related products without depending on their concrete classes.
- A class has a set of Factory Methods that blur its primary responsibility — extract into a standalone factory.

**Implementation essentials**
- Matrix of product types × variants; abstract interface per product type; factory interface with one creation method per product; one concrete factory per variant.
- App instantiates one concrete factory at boot based on configuration, passes it around.

**Pros / Cons**
- Pros: guarantees family compatibility; decouples clients; SRP/OCP.
- Cons: many interfaces/classes — considerable complexity.

**Relations**
- Vs Factory Method: one product vs whole families. Vs Builder: AF returns product immediately; Builder runs steps first.
- Can be a Facade alternative for hiding subsystem creation; often a Singleton.

**Recognition heuristic**
Multiple parallel class families that must not be mixed + variant-selection conditionals repeated at every creation site.

# Builder

**Problem**
Complex objects with many optional parts force telescoping constructors or a subclass explosion per configuration combination.

**Applicability signals**
- Get rid of telescoping constructors — build step by step using only needed steps.
- Different representations of the same product sharing construction steps that differ in details.
- Constructing Composite trees or complex objects with deferred/recursive steps.

**Implementation essentials**
- Base builder interface with common steps; concrete builder per representation holding its product.
- Result-fetching on the concrete builder; optional Director encapsulating reusable step sequences.

**Pros / Cons**
- Pros: incremental construction; reuse across representations; isolates construction (SRP).
- Cons: multiple new classes.

**Relations**
- Vs Abstract Factory: Builder = steps then fetch; AF = immediate. Director+builders ≈ Bridge shape. Often Singleton.

**Recognition heuristic**
Constructor with a long tail of mostly-null optional parameters, or calls needing a comment per argument.

# Prototype

**Problem**
External copying is impossible (private fields) and couples to the concrete class, which may be unknown behind an interface.

**Applicability signals**
- Code shouldn't depend on concrete classes of objects it must copy (third-party objects behind interfaces).
- Reduce subclasses that only differ in initialization — keep pre-built prototypes and clone them.

**Implementation essentials**
- `clone` method; copy constructor per class copying all fields (incl. private, via self-access); `clone` = `new OwnClass(this)`.
- Optional prototype registry (name → prototype) handing out clones.
- Deep-copy semantics for nested objects / back-references need deliberate handling.

**Pros / Cons**
- Pros: class-agnostic cloning; drop repeated init code; presets without inheritance.
- Cons: circular references make cloning tricky.

**Relations**
- Copy-constructor alone still requires knowing the concrete class; Prototype hides it behind polymorphic `clone`.
- Abstract Factory can be composed of Prototypes; complements Composite/Decorator (clone assembled structures).

**Recognition heuristic**
Field-by-field reconstruction to duplicate an object, or dummy subclasses whose only difference is preset values.

# Singleton

**Problem**
Ensure one instance (shared resource) + provide safe global access. Solving both in one class violates SRP by design.

**Applicability signals**
- A class should have a single instance available to all clients (shared DB object).
- Stricter control over globals — nothing but the class can replace the cached instance.

**Implementation essentials**
- Private static instance field; public static lazy `getInstance()`; private constructor; thread-safe lazy init in multithreaded programs.

**Pros / Cons**
- Pros: guaranteed single instance; global access; lazy init.
- Cons (criticisms): violates SRP; can mask bad design (components knowing too much about each other); multithreading care; hard to unit test (private constructor + static method defeat mocking).

**Relations**
- Facade often becomes a Singleton. Flyweight ≠ Singleton: Flyweight has many immutable instances with shared intrinsic state; Singleton is one, possibly mutable, instance.

**Recognition heuristic**
A class reached from everywhere via a static accessor whose hidden shared state makes tests order-dependent.
