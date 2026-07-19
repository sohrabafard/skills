# refactoring.guru distilled notes — Code smells + when to refactor (research agent output, 2026-07-19)

Sources: /refactoring/smells + 5 category pages + all 23 individual smell pages + /refactoring/when + /refactoring/what-is-refactoring.

## Smell taxonomy (5 categories, 23 smells)

### Bloaters
- **Long Method** (past ~10 lines raise questions) → Extract Method (isolate any fragment needing a comment); Replace Temp with Query; Introduce Parameter Object; Decompose Conditional. Extra calls almost never hurt performance.
- **Large Class** → Extract Class / Subclass / Interface. Payoff: less to remember, duplication removed.
- **Primitive Obsession** (money/ranges/phones as primitives; constants coding information; string keys as field names) → Replace Data Value with Object; Replace Type Code with Class/Subclasses/State-Strategy; Introduce Parameter Object.
- **Long Parameter List** (>3-4 params) → Introduce Parameter Object; Replace Parameter with Method Call; Preserve Whole Object. Ignore when removal would create unwanted dependency.
- **Data Clumps** (same variable group recurring; test: delete one — do the rest still make sense?) → Extract Class; Introduce Parameter Object; then move the operating code in.

### OO Abusers
- **Switch Statements** (same switch scattered) → "see switch, think polymorphism": Replace Type Code with Subclasses/State-Strategy; Replace Conditional with Polymorphism. Ignore when simple, or in Factory Method/Abstract Factory (legitimate switch).
- **Temporary Field** (fields meaningful only sometimes) → Extract Class (fields + their algorithm); Introduce Null Object.
- **Refused Bequest** (subclass uses only part of its inheritance) → Replace Inheritance with Delegation; or Extract Superclass for the truly shared part.
- **Alternative Classes with Different Interfaces** (two classes, same job, different names) → Rename/Move Method to unify, Extract Superclass, delete one. Ignore across libraries you don't control.

### Change Preventers
- **Divergent Change** (one class changed for many unrelated reasons) → Extract Class per change axis.
- **Shotgun Surgery** (one change → many small edits across classes) → Move Method/Field to gather the responsibility; Inline Class for emptied leftovers. Dual of Divergent Change.
- **Parallel Inheritance Hierarchies** (new subclass here forces a twin there) → one hierarchy references the other, dismantle the redundant one. Sometimes the lesser evil — ignore when merging makes a bigger mess.

### Dispensables
- **Comments** ("best comment is a good name") → Extract Method/Variable, Rename, Introduce Assertion. KEEP why-comments and genuinely complex algorithm docs.
- **Duplicate Code** → Extract Method; siblings: Pull Up / Form Template Method; same job different algorithm: Substitute Algorithm; unrelated classes: Extract Superclass/Class.
- **Lazy Class** → Inline Class; Collapse Hierarchy. Ignore when deliberately marking future intent.
- **Data Class** (fields + getters/setters only) → move the client code that operates on the data INTO the class; close over-open accessors.
- **Dead Code** → delete (IDE finds it fastest).
- **Speculative Generality** ("just in case" abstraction nothing uses) → Collapse Hierarchy, Inline Class/Method, Remove Parameter. Ignore when building a framework for external users.

### Couplers
- **Feature Envy** (method uses another object's data more than its own) → Move Method (data and its operations belong together). Ignore when the split is deliberate: Strategy, Visitor.
- **Inappropriate Intimacy** (one class using another's internals) → Move Method/Field, Hide Delegate, cut bidirectional links.
- **Incomplete Library Class** → Introduce Foreign Method (small) / Local Extension (large).
- **Message Chains** (`a.b().c().d()`) → Hide Delegate; or move the operation to the chain start. Don't overdo → creates Middle Man.
- **Middle Man** (class that only delegates) → Remove Middle Man. Ignore when intentional: Proxy, Decorator, dependency-avoidance layers.

Dual pairs: Message Chains ↔ Middle Man; Divergent Change ↔ Shotgun Surgery — over-fixing one creates the other.

## When to refactor

- **Rule of Three**: first time just do it; second time wince and duplicate; third time refactor.
- When adding a feature (clean first, feature slots in easier); when fixing a bug (bugs live in the dirtiest code — clean first and the bug shows itself); during code review (last chance before shipping).
- When NOT to: when the cure creates worse coupling or a bigger mess than the smell; when the "smell" is a deliberate pattern (switch in factories; Feature Envy in Strategy/Visitor; Middle Man in Proxy/Decorator); across libraries you don't own; why-comments; framework hooks for external users.

## Clean code qualities (the site's definition)

1. Obvious for other programmers. 2. No duplication. 3. Minimal classes/moving parts. 4. Passes all tests (a 95%-passing suite signals dirty code). 5. Easier and cheaper to maintain.
