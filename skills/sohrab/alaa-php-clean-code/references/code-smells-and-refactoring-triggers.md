# Code smells and refactoring triggers (PHP 8.5 / Laravel 13)

## Contents
- How to use this file
- Bloaters
- OO abusers
- Change preventers
- Dispensables
- Couplers
- When to refactor
- When NOT to refactor
- Clean-code qualities

## How to use this file
Smells are the diagnosis layer; patterns and refactorings are the treatment layer. During review or before
a refactor, name the smell first, then apply the smallest treatment. The five families below are the
classic taxonomy translated to Laravel terms. Each smell lists: signs → treatment. Deliberate design is
not a smell — see "When NOT to refactor".

## Bloaters
- **Long method**: a controller action or service method past the size budget, or any fragment that needs a comment to explain itself → extract an intention-named private method or a focused service; decompose conditionals. Extra method calls are never the performance problem.
- **Large class**: a controller/service/job accumulating unrelated verbs → Extract Class along the seams in `SKILL.md` under Size and complexity budgets (Form Request, service per use case, repository, strategy).
- **Primitive obsession**: money, phone, national id, date ranges, tenant ids traveling as strings/ints; class constants coding a closed set → value object; backed enum. The platform's `TenantId`-style value objects exist for exactly this.
- **Long parameter list**: more than 3-4 parameters, or boolean flags steering the flow → Introduce Parameter Object (a small DTO), or split the method per flag branch.
- **Data clumps**: the same field group recurring across signatures (page/perPage/sort, from/to dates) → one typed DTO (`...FilterData`); the test: delete one field — if the rest lose meaning, they belong together.

## OO abusers
- **Switch statements**: the same `match`/`if` ladder on a type/provider/status repeated in more than one place → Strategy behind a map/factory, or polymorphism. One `match` centralized in a single factory is legitimate, not a smell.
- **Temporary field**: properties that only mean something during one operation → extract the operation plus its fields into its own class (often a method object or a pipeline stage). Octane makes this smell dangerous, not just ugly.
- **Refused bequest**: a subclass inheriting methods it stubs out or overrides to throw → replace inheritance with delegation/composition; extract the genuinely shared part into a trait-free superclass or a collaborator.
- **Alternative classes with different interfaces**: two classes doing the same job under different names (a second half-duplicate `Helper` doing what a service already does) → unify names, merge, delete one.

## Change preventers
- **Divergent change**: one class edited for many unrelated reasons (every feature touches the same god service) → split by change axis: one service per use case.
- **Shotgun surgery**: one conceptual change forcing edits in many files (a status rename touching controllers, jobs, and Blade) → gather the responsibility into one owner (enum + transition authority; a single service; a constants class). Dual of divergent change — over-fixing one creates the other.
- **Parallel inheritance hierarchies**: adding `XProvider` always forces a matching `XProviderConfig`, `XProviderResponse`, ... → collapse to one hierarchy referencing plain objects, unless the pairing is a real Abstract Factory family (then it is deliberate design).

## Dispensables
- **Comments as deodorant**: a comment explaining *what* unclear code does → extract and name the code after the comment. Keep comments that state *why* (constraints, invariants, provider quirks).
- **Duplicate code**: apply the Rule of Three (below). Same class → extract method; sibling classes → pull up or Form Template Method; same job different algorithm → pick one algorithm.
- **Lazy class / dead code / speculative generality**: pass-through wrappers, unused params, "just in case" interfaces with one implementation and no seam → inline and delete. The repo's history keeps old code; the codebase should not.
- **Data class**: an array-shaped class with only accessors whose logic lives in its callers → move the operating code into it, or make it an honest `readonly` DTO whose logic deliberately lives in services (a DTO is not a smell; a "DTO" that callers keep re-deriving things from is).

## Couplers
- **Feature envy**: a method reading another object's data more than its own → move it (data and its operations live together). Deliberate exceptions: Strategy and Visitor split behavior from data on purpose.
- **Inappropriate intimacy**: a class reaching into another's internals (public properties, `getAttributes()` spelunking, knowing a collaborator's private conventions) → move members, formalize the seam with an interface, cut bidirectional references.
- **Message chains**: `$order->customer()->first()->profile->address->city` style navigation in application code → hide behind an intention-named method on the nearest owner, or a repository/read-model method. Do not over-fix into a Middle Man.
- **Middle man**: a class whose methods only delegate → remove it and call the target. Intentional middle men are fine: cache decorators, proxies, and boundary facades exist on purpose.
- **Incomplete library class**: a vendor package missing one behavior → a small extension/wrapper at the adapter boundary, never scattered workarounds in services.

## When to refactor
- **Rule of Three**: first time, just write it; second time, wince but duplicate; third time, extract. Premature abstraction is how vague `Helper`s are born.
- Before adding a feature to a messy area: clean first — the feature slots in more easily.
- While fixing a bug: bugs live in the dirtiest code; cleaning often exposes the bug.
- During review: name smells with this vocabulary and rank them; smell names make findings precise and non-personal.
- Always inside the task's declared refactor mode (`refactor-modes.md`) — a smell is never a license to exceed the mode's blast radius.

## When NOT to refactor
- The "smell" is deliberate design: `match` inside one factory; Feature Envy inside Strategy/Visitor; Middle Man that is a Proxy/Decorator/boundary facade; framework hooks for external users.
- The cure creates worse coupling or a bigger mess than the smell (forcing parameter objects that drag in dependencies; merging parallel hierarchies into a knot).
- The code belongs to a library you don't control — adapt at the boundary instead.
- The task mode forbids it — record the smell as a follow-up finding instead of fixing it silently.

## Clean-code qualities (the definition of "clean" this pack enforces)
1. Obvious to the next developer. 2. No duplication. 3. Minimal moving parts. 4. Passes all tests — a suite that "mostly passes" signals dirty code. 5. Cheaper to maintain than it was before your change.
