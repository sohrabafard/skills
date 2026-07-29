# Pattern selection — run this before naming any pattern

A pattern is correct only when it improves data flow, testability, encapsulation, or extension. Patterns
are answers to specific pains, so identify the observable symptom first, then confirm with the
discriminating question. **If the confirming question answers no, you picked the wrong pattern** — go back
to the table rather than bending the code to fit the name.

The catalogue is split by family so one hop reaches the pattern: structural forms in
`42-structural-patterns.md`, behavioural forms in `43-behavioral-patterns.md`, creational forms and the
async idioms in `44-creational-and-async-idioms.md`.

## Symptom to pattern

| Symptom in the code | Reach for | Confirming question |
|---|---|---|
| The same multi-step flow duplicated across composables or components, varying in some steps | Template Method (composable or renderless skeleton) | Is the skeleton stable, and are the variations strictly step-local? |
| A growing sequence of checks before an action (auth, permission, validation, throttle), each able to stop it | Chain of Responsibility | May a handler halt the request? Is chain-end behaviour defined? |
| One payload progressively transformed by ordered stages that all run (DTO to normalize to enrich to validate) | Pipeline | Does every stage always run and pass the payload on? |
| An action must be queued, retried, deferred, undone, or audited | Command | Do you need the action *as data*, not just called? |
| A component or store calls a vendor SDK or a backend shape you cannot change, and its names and types leak inward | Adapter | Is the other side unmodifiable, and does the interface need to *change shape*? |
| Cross-cutting behaviour (cache, log, permission gate, loading wrapper) must be added without touching implementations | Decorator | Does the wrapper keep the same contract and always delegate? |
| A component or composable imports Axios, an SDK, or `localStorage` directly and cannot be tested without it | Dependency inversion (typed port plus injection) | Can a fake implement the seam in one small interface? |
| A test needs heavy mocking of a concrete module instead of passing a small fake | Dependency inversion | Would swapping the provider mean editing feature components, or one binding site? |
| `if`/`switch` on a "kind" string repeated across call sites to choose behaviour | Strategy (typed map) | Do the variants share one contract and vary independently of callers? |
| One exclusive lifecycle juggled through several loosely related booleans | State (discriminated union) | Are there real named states with guarded transitions? |
| Recursive data (menus, trees, nested comments) with special-cased leaf and group handling | Composite | Can leaf and group honestly share one node contract? |
| Sibling components or composables wired to each other by name, coordination smeared across them | Mediator (orchestrator composable or host page) | Can the participants stop knowing each other entirely? |
| Names or props concatenating two variation axes (`PdfInvoicePreview`, `CsvReportExporter`) | Bridge (split the axes) | Are the axes genuinely independent hierarchies? |
| Undo, draft restore, or "discard changes" needs a prior state back | Memento (immutable snapshots) | Does the owner produce the snapshot, not outside code? |
| Families of related implementations that must never be mixed (client plus parser plus validator) | Abstract Factory (suite chosen once) | Are there two or more members whose implementations must match? |
| The same `switch` on a node kind repeated once per operation | Visitor (per-operation handler map plus `assertNever`) | Is the kind set stable while operations keep arriving? |
| One shared service or client needed app-wide (API client, event gateway, worker manager) | Singleton (module-level instance) | Is it stateless or SSR-safe, with no per-user mutable state? |
| Parts of the UI must react when shared data changes | Observer (props and emits, Pinia subscription) | Is the notification one-way, with every subscription cleaned up? |
| Access to an expensive or browser resource must be guarded, deferred, or cached | Proxy | Does the wrapper keep the contract but control when the real call happens? |
| A component juggling several low-level APIs for one high-level intent | Facade (typed service module) | Would one small typed surface hide the subsystem completely? |
| Object creation with branching or config repeated across call sites | Factory (typed creator) | Does one creator own the branching behind a stable return type? |
| Multi-step conditional construction of a config or schema (table columns, form schema) | Builder | Do call sites genuinely assemble different combinations, or would a `satisfies` literal do? |
| Custom traversal or lazy generation over large or streaming data | Iterator (generator) | Is the laziness or streaming real, not aesthetic? |
| Subclasses, wrappers, or props existing only to encode preset variants | Prototype (frozen preset registry) | Is duplicating a configured object the real need? |
| Thousands of similar immutable config objects hurting memory | Flyweight (shared frozen config) | Is there a measured memory cost? |

Callbacks and Promises are idioms rather than symptom-routed patterns: their rules are in
`44-creational-and-async-idioms.md` and apply whenever async or interop code is touched.

## Look-alike disambiguation

The pairs that get confused, stated once so no catalogue section has to restate them:

- **Adapter vs Decorator vs Proxy vs Facade.** Adapter *changes* the interface so an incompatible thing
  fits. Decorator *keeps* the interface and adds behaviour, always delegating. Proxy *keeps* the interface
  but controls whether and when the real call happens. Facade *invents* a new, simpler interface over a
  subsystem.
- **Chain of Responsibility vs Pipeline vs Decorator.** CoR handlers may handle and stop, and an unhandled
  request must have defined behaviour. Pipeline stages all run and transform one payload. Decorator layers
  always delegate inward.
- **Command vs Strategy.** Strategy is interchangeable ways of doing the *same* thing, chosen by context.
  Command reifies *an action* as an object so it can travel — queue, undo, log.
- **Template Method vs Strategy.** Template Method fixes the skeleton and varies the steps. Strategy swaps
  the whole algorithm at runtime.
- **Mediator vs Observer.** Observer's producer does not know who reacts. Mediator knows exactly who
  participates and in what order, because sequencing is the thing it owns.

## Naming patterns in code

Name a pattern in a comment or an identifier only where it tells a reader something the code does not — an
orchestrator that must stay thin, a decorator stack whose order is behaviour. A component named
`UserListFactoryStrategyProvider` describes the author's reading, not the program.
