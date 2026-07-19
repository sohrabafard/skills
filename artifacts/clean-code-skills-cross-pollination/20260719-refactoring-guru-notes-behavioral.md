# refactoring.guru distilled notes — Behavioral patterns (research agent output, 2026-07-19)

Source pages: mediator, memento, observer, state, strategy, iterator, visitor.

## Mediator

**Problem**: interdependent components develop a chaotic web of direct references; changes ripple; components can't be reused because they're hard-wired to colleagues.

**Applicability signals**: hard to change classes because tightly coupled to many others; can't reuse a component elsewhere; tons of component subclasses just to reuse basic behavior in different contexts.

**Essentials**: mediator interface (`notify(sender, event)`); concrete mediator holds all components and encodes coordination; components hold only a mediator reference and never talk to peers; mediator is a black-box router.

**Pros/Cons**: SRP/OCP, decoupling, reuse; mediator tends to become a God Object.

**Relations**: vs Facade — facade adds a simplified interface, subsystem doesn't know it and parts still talk directly; mediator centralizes ALL communication, components know only it. vs Observer — mediator kills mutual dependencies via one coordinator; observer is dynamic one-way subscription; mediator is often built ON observer; if there is no central object, it's just observers. Sender→receiver spectrum: Command = one link; CoR = along a chain; Mediator = through a center; Observer = dynamic subscription.

**Recognition heuristic**: components referencing each other by name to react to each other's changes — coordination smeared across participants.

## Memento

**Problem**: need snapshots for undo/rollback without exposing internals; external snapshot code breaks on every refactor.

**Applicability signals**: snapshots to restore previous state (undo, transaction rollback); direct field/getter access would violate encapsulation — the object itself makes the snapshot.

**Essentials**: originator creates and restores its own memento; memento immutable (constructor-only); caretaker (undo stack) stores mementos but never looks inside.

**Pros/Cons**: snapshots without breaking encapsulation; RAM cost; caretaker lifecycle tracking.

**Relations**: Memento + Command = canonical undo (command executes, memento saves pre-state). vs Prototype — simple state with no external links: a clone is a simpler snapshot.

**Recognition heuristic**: undo/rollback code reaching into another object's fields (or demanding public setters for everything) to save/restore state.

## Observer

**Problem**: one object's changes matter to an unknown, changing set of others; without subscriptions you poll wastefully or broadcast to everyone.

**Applicability signals**: the set of interested objects is unknown beforehand or changes dynamically; observation is temporary/situational (subscribers join and leave).

**Essentials**: publisher/subscriber split; subscriber interface (`update` + context args); subscribe/unsubscribe on the publisher; notify only via the interface; wiring at runtime.

**Pros/Cons**: OCP, runtime relations; notification order is random.

**Relations**: vs Mediator (see above).

**Recognition heuristic**: polling loops, or a class keeping a hard-coded list of concrete dependents it pokes after every change.

## State

**Problem**: behavior depends on current state; the machine lives as monster conditionals duplicated across methods.

**Applicability signals**: many states, state-specific code changes often; class polluted with massive state conditionals; duplicated code across similar states/transitions.

**Essentials**: state interface with only the state-dependent methods; one class per state; context delegates to current state object; transitions = swapping the state object (from context or states).

**Pros/Cons**: SRP/OCP, kills bulky conditionals; overkill for few/rarely-changing states.

**Relations**: vs Strategy — strategies are fully independent and unaware of each other; states may know each other and drive transitions. State ≈ extension of Strategy.

**Recognition heuristic**: the same `switch (status)` ladder repeated in several methods of one class, with transitions assigned deep inside branches.

## Strategy

**Problem**: a class accumulates variants of doing the same job, bloating it.

**Applicability signals**: different variants of an algorithm switchable at runtime; many similar classes differing only in one behavior; isolate business logic from algorithm details; a massive conditional switching variants of the same algorithm.

**Essentials**: strategy interface; variant classes; context delegates and holds a swappable reference; the client picks the strategy.

**Pros/Cons**: runtime swap, isolation, OCP; overkill for a couple of stable algorithms; clients must know the differences; a lambda often suffices in functional languages.

**Relations**: vs Command — Command reifies any operation for deferral/queuing/undo; Strategy = interchangeable ways of the same thing. vs Template Method — inheritance/static vs composition/runtime. vs Decorator — decorator changes the skin, strategy the guts.

**Recognition heuristic**: a `switch` choosing between interchangeable ways of computing the same result, with new variants arriving.

## Iterator

**Problem**: traversal algorithms baked into collections blur their responsibility; clients traversing directly couple to concrete structures.

**Applicability signals**: hide a complex structure from clients; deduplicate non-trivial traversal code; traverse structures of unknown types.

**Essentials**: iterator interface (next / has-more); collection returns iterators (one per traversal order); each iterator owns its traversal state; parallel independent iteration; pausable.

**Pros/Cons**: SRP/OCP, parallel iteration; overkill for simple collections; can be slower than direct access.

**Relations**: + Composite (tree traversal), + Factory Method (collection subclasses return compatible iterators), + Memento (snapshot iteration state), + Visitor (iterator walks, visitor operates).

**Recognition heuristic**: structure-specific navigation loops copy-pasted through business code instead of a "give me the next element" object.

## Visitor

**Problem**: add a new operation across a stable class hierarchy without touching those classes; the behavior doesn't belong in data-holding classes.

**Applicability signals**: run an operation over all elements of a complex structure; clean auxiliary behaviors out of business classes; behavior only meaningful for some classes of a hierarchy.

**Essentials**: visitor interface with one method per concrete element class; elements implement `accept(visitor)` calling `visitor.visitX(this)` — **double dispatch** eliminates client-side instanceof ladders; one concrete visitor per behavior.

**Pros/Cons**: OCP for new behaviors, SRP consolidation, accumulating state while traversing; every visitor changes when the element hierarchy changes; private-member access problem.

**Relations**: powerful cousin of Command; + Composite/Iterator for tree traversal. Signature move: the accept/double-dispatch pair — no `accept`, no Visitor.

**Recognition heuristic**: instanceof/type-switch ladders applying one operation differently per node class of a stable hierarchy — or a cross-cutting operation about to be pasted into every class of it.
