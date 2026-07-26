# PHP / Laravel design patterns — the rare eight

These eight patterns are correct sometimes and over-engineering usually. They live here, not in `design-patterns.md`, so the common catalog stays cheap to load: a router row that needs one of these pulls this file instead of the whole catalog.

**Enter this file only from a diagnostic row.** The symptom → pattern table at the top of `design-patterns.md` is the entry point, and its confirming question still applies — a "no" means the pattern is wrong and you go back to the table. Reaching for one of these without a symptom is the over-patterning `design-patterns.md` exists to prevent.

The Octane shaping for Prototype and Flyweight is in `octane-clean-code.md`; the invariants those rules serve belong to `/alaa-octane-performance` (`$alaa-octane-performance`).

## Contents
- Prototype pattern
- Bridge pattern
- Flyweight pattern
- Composite pattern
- Iterator pattern
- Mediator pattern
- Memento pattern
- Visitor pattern

## Prototype pattern

### Use when
- Duplicating configured objects is cheaper or safer than reconstructing them: preset report definitions, notification templates, pre-configured query/filter DTOs.
- Subclasses or long constructors exist only to encode preset field values.

### Laravel application
- PHP's native `clone` is the mechanism; implement `__clone()` to deep-copy nested mutable objects — default clone is shallow, and a shared nested object is a cross-request leak under Octane.
- On PHP 8.5, `clone($obj, ['prop' => $v])` is the idiomatic "clone with changes" for `readonly` DTOs — Prototype and the wither pattern converge here.
- Eloquent's `replicate()` is the model-world prototype: copies attributes, drops identity (`id`, timestamps). Use it instead of hand-copying attribute arrays; review which attributes must be excluded.
- Keep preset registries explicit: a small map of named, immutable prototype instances cloned on request.

### Anti-patterns
- Field-by-field reconstruction of an object the language could clone.
- Cloning objects holding resources, PDO handles, or service references — clone data carriers, not services.
- Shallow-cloning DTOs whose nested objects then mutate shared state.

## Bridge pattern

### Use when
- A class is growing along two independent axes and subclass names start concatenating them (`SmsInvoiceNotifier`, `EmailReceiptNotifier`): every new value on either axis multiplies classes.
- You want to vary "what is being done" (message/report/export content) independently of "how it is delivered/rendered" (channel, format, backend).

### Laravel application
- The shape: the abstraction holds a constructor-injected implementation interface and delegates the low-level work; both hierarchies grow independently. Laravel notifications are bridge-shaped already — the Notification (what) is separate from channels (how); prefer that native seam over custom class grids.
- Typical Alaa seams: report definition × exporter (CSV/XLSX/PDF), document × renderer, alert × delivery channel.
- Pair with Abstract Factory only when specific abstractions may only work with specific implementations.

### Anti-patterns
- A subclass grid that doubles when either axis gains a variant — the recognition signal itself.
- "Bridging" a single-axis variation that plain Strategy already solves; Bridge is Strategy applied to a structural split of two hierarchies, planned up front.

## Flyweight pattern

### Use when — all three conditions must hold (optimization only, never preemptive)
- The app must keep a huge number of similar objects alive at once; and
- this measurably exhausts memory; and
- the objects carry duplicated state that can be extracted and shared.

### Laravel application
- Rare in request-scoped PHP: requests are short and Octane workers reset. The legitimate cousins: backed enums (interned by the engine — the idiomatic flyweight for closed sets), shared immutable config/value-object instances reused across a long-running import or queue batch.
- Shared (intrinsic) state must be immutable; per-use (extrinsic) state is passed as method arguments — an Octane rule this pattern happens to restate.
- If memory pressure in a batch job is the problem, reach first for `lazy()`/`cursor()` streaming — traversal-tool choice is in `laravel-best-practices.md` under "Large-dataset traversal"; flyweight is the answer only when the duplication itself is the cost.

### Anti-patterns
- Introducing flyweight machinery without a measured memory problem.
- Mutable "shared" instances — a shared mutable flyweight under Octane is a cross-request data leak by construction.

## Composite pattern

### Use when
- Data or rules are recursive trees and callers should treat a leaf and a group uniformly: category trees, menu/navigation structures, nested comments, organizational units, composable validation or eligibility rules.

### Laravel application
- Model the node contract as one small interface (e.g. `EligibilityRule::passes(Context $ctx): bool`); leaves implement it directly, and composites (`AllOf`, `AnyOf`) hold `RuleInterface[]` children and implement the same interface. Specification-style rule composition is the highest-value use.
- For persistent trees, pair the in-memory composite with a deliberate storage strategy (adjacency list, path/materialized path, or a package the repo already uses) — recursion in PHP must not become recursion in queries; load the tree in bounded queries, then compose.
- Blade/component nesting already gives UI composition; do not force a class-based composite for rendering.

### Good defaults
- Guard depth and cycles explicitly when input is user-shaped.
- Keep leaf and composite behavior contract-identical (LSP): callers never type-check for "is this a group".

### Anti-patterns
- A composite interface with `addChild`/`removeChild` on leaves that throw `NotSupported` — split the mutable-tree API from the evaluation API.
- Unbounded recursive queries (N+1 per tree level) hidden behind an elegant in-memory composite.

## Iterator pattern

### Use when
- A traversal should be consumed lazily without materializing the whole dataset, or a custom aggregate should be `foreach`-able without exposing internals.

### Laravel application
- PHP generators (`yield`) are the idiomatic iterator: streaming file lines, paginated API pages, transformed rows. Laravel's `LazyCollection` (and `lazy()`/`cursor()` on queries) is the framework-native generator wrapper — prefer it over hand-written `Iterator` implementations.
- Choose the traversal tool by mutation and memory behaviour: `laravel-best-practices.md` under "Large-dataset traversal" holds the two facts upstream omits, and upstream `rules/db-performance.md` and `rules/collections.md` hold the enumeration with examples. When the collection grows with tenants, rows, history, or fan-out, the bound itself is owned by `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`).
- Implement `IteratorAggregate` (returning a generator) on domain collections when a typed collection object earns its keep; implement the low-level `Iterator` interface only for genuinely custom traversal state.

### Anti-patterns
- Materializing huge arrays and then "optimizing" downstream, when a generator/LazyCollection keeps memory flat.
- Generators with hidden side effects per step — iteration must be re-runnable or explicitly single-pass.
- A custom collection class that re-implements twenty Collection methods for one use site.

## Mediator pattern

### Use when
- A set of collaborators has developed a web of direct references — each knows several others by name, reacts to their changes, and none can be reused or tested alone.
- Coordination logic for one workflow is smeared across its participants instead of living in one place.

### Laravel application
- The everyday mediator is a plain orchestrating service: participants (validators, calculators, notifiers) know nothing about each other; the service sequences them. If a "service" mostly relays messages between components that also still talk directly, it is not a mediator — finish the decoupling or remove it.
- Laravel's event dispatcher is a platform mediator for *decoupled reactions* (listeners don't know the dispatching code); use it for genuinely independent side effects, not to hide a required sequential workflow — a workflow scattered across listeners becomes untraceable.
- Distinguish from Facade: a facade simplifies an existing subsystem that still works without it; a mediator is the only channel through which participants may interact.

### Anti-patterns
- The mediator growing into a god object that knows every participant's internals — keep participants' contracts narrow.
- Event-listener chains that implement an ordered business transaction implicitly (listener A dispatches event B ...). Sequences belong in a service or pipeline where the order is readable.

## Memento pattern

### Use when
- A prior state must be restorable — undo, draft/restore, compensation on failure — without exposing the object's internals for outsiders to copy.

### Laravel application
- Persisted snapshots are the platform form: audit tables storing before/after images, versioned drafts, soft-state checkpoints. The row is the memento; the caretaker (history table) never interprets it beyond storage.
- Eloquent's `getOriginal()` / `getChanges()` are built-in micro-mementos for a model's in-request lifecycle — use them for audit payloads instead of hand-tracking prior values.
- Pair with Command for undo-style flows: the job stores the pre-image it needs for compensation; keep mementos immutable and lifecycle-bounded (retention policy owned by the data layer).
- In-memory undo stacks across requests do not exist under Octane — state that must survive the request lives in the database or cache with explicit keys and TTLs.

### Anti-patterns
- "Snapshots" assembled by reading another object's public getters field-by-field — the owner builds its own snapshot.
- Unbounded history tables with no retention decision.

## Visitor pattern

### Use when
- A new operation must run across a stable, heterogeneous object structure (document nodes, rule trees, catalog entries of different classes) without adding that operation to every class — especially when several such operations (export, render, validate, price) keep arriving.

### Laravel application
- Classic double dispatch (`accept(Visitor)` on every node) is heavy in PHP; prefer the pragmatic form first: a handler map keyed by node class or backed enum (`match` on `$node::class`), one handler object per operation. This keeps the operation consolidated without touching node classes.
- Reach for real `accept()`-based Visitor only when the structure is deep, recursive, and traversal must accumulate state across nodes (report generation over a rule AST).
- The trade the classic pattern makes: adding an operation is cheap; adding a node class means updating every visitor/handler map. Choose it only when the node set is stable and operations vary — if nodes vary and operations are stable, use ordinary polymorphism instead.

### Anti-patterns
- `instanceof` ladders duplicated per operation across services — the exact smell either form of Visitor exists to remove.
- A visitor demanding public access to every node internal; give nodes intention-named accessors for what operations legitimately need.
