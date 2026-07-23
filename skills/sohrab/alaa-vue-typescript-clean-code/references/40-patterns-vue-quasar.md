# Design patterns for Vue, Quasar, Vite, and TypeScript

Use patterns as constraints for maintainability, not decoration. A pattern is correct only when it improves data flow, testability, encapsulation, or extension.

## Pattern selection diagnostic (run this before picking any pattern)

Patterns are answers to specific pains. Identify the observable symptom first, then confirm with the
discriminating question — if the answer is no, you picked the wrong pattern.

| Symptom in the code | Reach for | Confirming question |
|---|---|---|
| The same multi-step flow duplicated across composables/components with small variations in some steps | Template Method (composable/renderless skeleton) | Is the skeleton stable and are variations strictly step-local? |
| A growing sequence of checks before an action (auth, permission, validation, throttle), each able to stop it | Chain of Responsibility | May a handler halt the request? Is chain-end behavior defined? |
| One payload progressively transformed by ordered stages that ALL run (DTO → normalize → enrich → validate) | Pipeline | Does every stage always run and pass the payload on? |
| An action must be queued, retried, deferred, undone, or audited | Command | Do you need the action *as data*, not just called? |
| Component/store calls a vendor SDK / backend shape you cannot change, and its names/types leak inward | Adapter | Is the other side unmodifiable, and does the interface need to *change shape*? |
| Cross-cutting behavior (cache, log, permission gate, loading wrapper) must be added without touching implementations | Decorator | Does the wrapper keep the same contract and always delegate? |
| A component/composable imports Axios/SDK/localStorage directly and cannot be tested without it | Dependency Inversion (typed port + injection) | Can a fake implement the seam in one small interface? |
| `if/switch` on a "kind" string repeated across call sites to choose behavior | Strategy (typed map) | Do variants share one contract and vary independently of callers? |
| One exclusive lifecycle juggled through several loosely related booleans | State (discriminated union) | Are there real named states with guarded transitions? |
| Recursive data (menus, trees, nested comments) with special-cased leaf vs group handling | Composite | Can leaf and group honestly share one node contract? |
| Sibling components/composables wired to each other by name, coordination smeared across them | Mediator (orchestrator composable / host page) | Can participants stop knowing each other entirely? |
| Names or props concatenating two variation axes (`PdfInvoicePreview`, `CsvReportExporter` grid) | Bridge (split the axes) | Are the axes genuinely independent hierarchies? |
| Undo, draft restore, or "discard changes" needs a prior state back | Memento (immutable snapshots) | Does the owner produce the snapshot, not outside code? |
| Families of related implementations that must never be mixed (provider suite: client + parser + validator) | Abstract Factory (suite chosen once) | Are there ≥2 members whose implementations must match? |
| The same `switch` on a node kind repeated once per operation | Visitor (per-operation handler map + `assertNever`) | Is the kind set stable while operations keep arriving? |
| One shared service or client needed app-wide (API client, event gateway, worker manager) | Singleton (module-level instance) | Is it stateless or SSR-safe, with no per-user mutable state? |
| Parts of the UI must react when shared data changes | Observer (props/emits, Pinia subscription) | Is the notification one-way, with every subscription cleaned up? |
| Access to an expensive or browser resource must be guarded, deferred, or cached | Proxy | Does the wrapper keep the contract but control when the real call happens? |
| A component juggling several low-level APIs for one high-level intent | Facade (typed service module) | Would one small typed surface hide the subsystem completely? |
| Object creation with branching or config repeated across call sites | Factory (typed creator) | Does one creator own the branching behind a stable return type? |
| Multi-step, conditional construction of a config or schema (table columns, form schema) | Builder | Do call sites genuinely assemble different combinations, or would a `satisfies` literal do? |
| Custom traversal or lazy generation over large or streaming data | Iterator (generator) | Is laziness or streaming real, not aesthetic? |
| Subclasses, wrappers, or props existing only to encode preset variants | Prototype (frozen preset registry) | Is duplicating a configured object the real need? |
| Thousands of similar immutable config objects hurting memory | Flyweight (shared frozen config) | Is there a measured memory cost? |

Callbacks and Promises are idioms, not symptom-routed patterns: their rules live in their catalog sections
below and apply whenever async or interop code is touched.

Look-alike disambiguation (the pairs agents most often confuse):

- **Adapter vs Decorator vs Proxy vs Facade**: Adapter *changes* the interface to make an incompatible thing fit; Decorator *keeps* the interface and adds behavior, always delegating; Proxy *keeps* the interface but controls whether/when the real call happens; Facade *invents* a new, simpler interface over a subsystem.
- **Chain of Responsibility vs Pipeline vs Decorator**: CoR handlers may handle-and-stop (and an unhandled request must have defined behavior); Pipeline stages all run and transform one payload; Decorator layers always delegate inward.
- **Command vs Strategy**: Strategy is interchangeable ways of doing the *same* thing, chosen by context; Command reifies *an action* as an object so it can travel (queue, undo, log).
- **Template Method vs Strategy**: Template Method fixes the skeleton and varies steps; Strategy swaps the whole algorithm at runtime.

## Singleton

Use for one app-wide gateway: API client facade, event gateway, worker manager, feature registry, or stateless utility service.

Do:

```ts
export const courseApi = createCourseApi(httpClient)
```

Do not:

- Hide mutable per-request/per-user state in module scope when SSR is possible.
- Create Java-style `getInstance()` ceremony unless repo convention requires it.
- Forget the classic criticisms: a singleton is hidden global state — it couples everything that touches it and makes tests order-dependent. Keep singletons stateless/immutable, and prefer passing the instance through an injection key when a test seam is needed.

## Dependency injection

Use for replaceable app services, plugin APIs, deeply nested dependencies, and test seams.

Do:

```ts
export const courseApiKey: InjectionKey<CourseApi> = Symbol('courseApi')
provide(courseApiKey, courseApi)
const courseApi = injectStrict(courseApiKey)
```

Do not:

- Use string keys that can collide in large apps.
- Inject raw mutable objects and let every child mutate them.

## Observer

The defining signal: the set of interested parties is unknown to the producer or changes at runtime — the
producer announces; subscribers decide to care. Vue's reactivity, `watch`, props/emits, and Pinia
subscriptions are all Observer already; hand-rolled subscription lists are almost never needed. If the
producer must know exactly who reacts and in what order, that is a workflow owned by an orchestrator
(Mediator), not Observer.

Use props/emits for parent-child observation, Pinia for shared domain data, and an event bus only for cross-cutting events such as auth-expired, connectivity-changed, or upload-progress notifications.

Do:

- Subscribe in `onMounted` or setup when safe.
- Unsubscribe in `onUnmounted`.
- Type event names and payloads.

Do not:

- Use an event bus to avoid designing ownership.
- Store business data only in event payloads.

## Command

The point of Command is turning a method call into a stand-alone typed object, so the action can travel:
be queued, retried, delayed, sent to a worker, undone, or logged. If you only need to *call* behavior,
call a function; reach for Command when you need the action *as data*. (Strategy varies how one thing is
done; Command reifies that a thing was requested.)

Use for actions that need queuing, undo/redo, worker dispatch, auditability, or deferred execution.

Do:

```ts
type UploadCommand =
  | { type: 'start'; fileId: string }
  | { type: 'pause'; uploadId: string }
  | { type: 'resume'; uploadId: string }
```

Route with a typed handler map.

Do not:

- Pass untyped string commands and arbitrary payloads between components.
- Let command handlers mutate unrelated UI state.

## Proxy

Use to intercept or adapt a target API while preserving its external contract: API retry wrapper, auth header wrapper, cache wrapper, reactive storage wrapper.

Do not use JavaScript `Proxy` when a normal typed function or class is clearer.

## Decorator

Use to add cross-cutting behavior while preserving API:

- logging around API calls
- permission checks around actions
- loading/error wrappers around async commands
- component wrappers that add layout/validation while preserving model contract
- caching around a service/adapter method: same signature, explicit cache keys that include user/tenant scope, explicit invalidation on writes

Caching lives in the service/adapter layer as a decorator, never as ad-hoc `ref` caches scattered through components; a cache the UI cannot invalidate is a stale-data bug factory.

Decorator rules that make stacking safe:

- One concern per decorator; stack small decorators (log → cache → retry) instead of writing one mixed wrapper.
- A decorator always delegates inward and keeps the exact contract; if it needs extra public methods, the abstraction is wrong (that is a new service, not a decorator).
- Stacking order is behavior — `retry(cache(fetch))` and `cache(retry(fetch))` differ; declare the order in one composition site and test it.
- Decorator exists because inheritance cannot add combinations at runtime; if you are tempted to subclass or mixin for a cross-cutting concern, wrap instead.

Do not decorate in a way that changes event meaning, prop semantics, or accessibility behavior without renaming the component/contract.

## Facade

Use to simplify complex APIs:

- Quasar Dialog/Notify facade for domain-specific feedback
- Axios/Fetch facade for backend calls
- IndexedDB/Dexie facade for persistence
- Web Worker facade for background commands
- Browser API facade for storage/media/resize

Do:

- Return domain models and domain errors.
- Keep facade methods small and named by business use case.

Do not:

- Leak SDK response shapes or Quasar plugin details into components.

## Callbacks

Use for DOM events, library hooks, and small synchronous extension points.

Do:

- Type callback signatures.
- Ensure callback identity is stable when cleanup requires it.
- Remove listeners.

Do not:

- Use nested callbacks for async control flow that should be promises.

## Promises

Use for asynchronous operations. Prefer `async/await` at call sites.

Do:

```ts
try {
  state.value = { status: 'loading' }
  const course = await courseApi.getCourse(id, { signal })
  state.value = { status: 'success', data: course }
} catch (error) {
  if (isAbortError(error)) return
  state.value = { status: 'error', error: toAppError(error) }
}
```

Do not:

- Swallow errors.
- Ignore stale-response races.
- Chain `.then()` deeply when `await` is clearer.

## Factory

Use when creating variants behind a common contract: form field builders, column builders, API adapter selection, dynamic component maps.

Do not use a factory when a direct constructor/function is simpler.

## Builder

Use fluent builders only for genuinely multi-step, conditional configuration assembled from many optional parts: table column sets that vary by role/feature flags, form schemas, chart configurations.

Do:

```ts
const columns = defineCourseColumns()
  .withBase()
  .withProgress({ when: isEnrolledView })
  .withActions(userCan('course.manage'))
  .build() // build() validates and returns a readonly, typed result
```

- Validate invariants in `build()` and return an immutable typed result.
- Prefer plain typed object literals with `satisfies` and small helper functions first; a builder must earn its keep with real conditional assembly shared across call sites.

Do not:

- Wrap a simple options object in builder ceremony.
- Leave the built object mutable and half-initialized between steps.

## Composite

Use for recursive UI trees where leaf and group must be treated uniformly: navigation menus, nested comments, tree views, folder pickers, nested form sections.

Do:

- Define one typed recursive node contract: `interface TreeNode { id: string; children?: readonly TreeNode[] }` with a discriminated union when leaf and group carry different data.
- Render with a recursive component (or `QTree` when it fits) that takes the node contract; the component calls itself for `children`.
- Keep stable unique `:key` at every level; guard depth and cycles when input is server- or user-shaped.
- Keep per-node behavior (select, expand, navigate) in emitted intents handled at the tree host, not inside each node.

Do not:

- Fork separate leaf/group components with divergent props when one contract serves both.
- Recurse over unbounded, unvalidated structures without a depth guard.

## Iterator

Prefer typed array methods and computed chains for ordinary traversal. Use generators (`function*`) only for real lazy/streaming sequences: paginated API pages, chunked file processing, infinite-scroll feeds.

Do:

- Keep generators pure per step or explicitly single-pass.
- Pair any potentially unbounded sequence in the UI with pagination or virtual scrolling (`QVirtualScroll`, QTable server-side pagination); the iterator pattern in a UI ends at a bounded viewport.

Do not:

- Materialize huge arrays just to `.map().filter()` them for a viewport that shows twenty rows.
- Hand-write iterator classes where `for...of` over a generator or array already reads clearly.

## Template Method

Recognize the need: the same multi-step flow is duplicated in several places with small variations in
individual steps (three import flows differing only in parsing; three pickers differing only in rendering).
The cure is one owner for the skeleton — callers extend *particular steps*, never the structure or step
order.

The "skeleton with fillable steps" belongs to composition in Vue, never inheritance:

- Renderless/headless components own the algorithm (fetching, selection, keyboard handling) and expose slots/scoped slots where callers fill in the varying rendering steps.
- Composables own a fixed flow and accept typed callbacks/strategies for the varying steps (`useImportFlow({ transform, onConflict })`).
- Quasar components with slots are this pattern applied; prefer filling their slots over wrapping them.

Do:

- Keep the skeleton's step order fixed and non-overridable; expose only the intended steps as typed callbacks/slots.
- Distinguish required steps (no default — the type requires them) from optional hooks (safe no-op defaults before/after key steps).
- Keep hooks few; a skeleton with ten injectable steps is not an algorithm, it is an escape hatch.

Do not create base-component class hierarchies or mixin chains to share an algorithm skeleton; that is the inheritance form this codebase bans. If callers need to replace the *whole* algorithm at runtime rather than fill steps, that is Strategy, not Template Method.

## Chain of Responsibility

Use for ordered handler chains where each handler passes on or short-circuits deliberately:

- HTTP client interceptor chains (auth token → correlation headers → retry → error mapping), each interceptor with one job.
- Router guard sequences reading route `meta` (auth → permission → data preconditions), each guard returning pass/redirect.
- Validation chains where rules run in declared order and stop at the first definitive failure.

Do:

- Keep the chain's order explicit and centrally declared; a chain assembled implicitly across files is undebuggable.
- Make short-circuiting a first-class, typed outcome, not a thrown surprise.
- Define chain-end behavior explicitly: a request no handler claimed must have a deliberate result (deny by default for auth-like chains, pass-through for enrichment chains) — "fell off the end" is the classic CoR bug.
- Type the payload flowing through the chain once; handlers do not mutate unrelated state.

Do not:

- Reorder handlers casually — order is part of the contract; test it.
- Hide business decisions inside transport interceptors; interceptors handle transport concerns only.
- Use CoR where every stage must always run and transform the data — that is a Pipeline (below), and pretending it can short-circuit hides bugs.

## Pipeline

Sequential transformation of one payload through ordered stages that all run: DTO normalization chains
(parse → camelCase → resolve fields → validate), form-submit preparation (trim → coerce → strip empty →
attach metadata), upload preprocessing (read → resize → compress → fingerprint).

Do:

```ts
type Stage<T> = (input: T) => T
const prepareSubmit: Stage<CourseDraft>[] = [trimStrings, coerceNumbers, stripEmptyOptionals, stampClientMeta]
const payload = prepareSubmit.reduce((acc, stage) => stage(acc), draft)
```

- Keep stages pure `(T) => T` (or `(T) => Promise<T>` for async pipelines); side effects stay out of transform stages.
- Type the payload once for the whole pipeline; a stage that needs a different shape marks a pipeline boundary, not a cast.
- Declare stage order in one place and test the composed pipeline, not only individual stages.

Do not:

- Confuse with Chain of Responsibility: pipeline stages never short-circuit on "handled"; a stage that can reject should return a typed result and end the pipeline explicitly, or belongs in a validation chain.
- Build pipeline machinery for two obvious function calls — compose plainly until order genuinely evolves.

## Strategy

Use for replaceable behavior: sorting, filtering, pricing, validation mode, auth provider, upload provider.

Prefer typed strategy maps over long if/else chains. For one tiny varying behavior, a typed function
parameter IS the strategy — do not build objects until strategies carry state or several methods.
Strategies are independent and unaware of each other; if the variants know each other and trigger
switching between themselves, that is the State pattern, not Strategy.

## Abstract Factory

Use when a *family* of related implementations must stay consistent and never be mixed: an upload provider
suite (client + progress adapter + error mapper), an auth provider suite (SDK wrapper + token storage +
claims parser), a theming suite of base components.

Do:

- Define the suite as one typed interface (an object of related factory functions or implementations) and select the concrete suite once — at boot or via an injection key; feature code receives the suite, never assembles members from separate configs.
- Reach for it only when ≥2 members must match; a single varying implementation is plain Strategy/Adapter.

Do not resolve family members independently in different modules, allowing provider A's client to pair with provider B's error mapper.

## Prototype

Cloning configured objects instead of rebuilding them: preset form schemas, table configurations, draft
templates.

Do:

- Prefer plain immutable presets + spread/`structuredClone` for deep copies of data objects.
- `toRaw()` reactive objects before `structuredClone` — proxies do not clone.
- Keep preset registries explicit: a typed map of named frozen presets, cloned on use.

Do not hand-copy objects field-by-field, and do not clone objects holding functions, component references, or abort controllers — clone data, re-create behavior.

## Bridge

Use when a feature varies along two independent axes and names start concatenating them: preview UI ×
document format, chart component × data source, editor × storage backend. Split into two hierarchies —
the abstraction (component/composable owning UX flow) holds an injected implementation port (format
adapter, data source) — so each axis grows without multiplying the other.

Do not "bridge" a single-axis variation that a strategy prop already solves; Bridge is the planned split of two hierarchies, Adapter is the retrofit for one incompatible interface.

## Mediator

Use when sibling components coordinate through a web of refs/emits relayed between them, or a page's
children each know the others' state. The host page or one orchestrator composable becomes the mediator:
children are props-in/events-out and know only their own contract; the mediator owns the coordination
policy. This is the Alaa orchestrator-composable pattern viewed from the GoF side.

Do:

- Keep children mediator-blind: they emit intents; the mediator decides.
- Keep the mediator thin — policy and sequencing only; heavy logic stays in the focused composables it composes.

Do not let the mediator grow into a god composable (split by the budget rules), and do not use a global event bus as an anonymous mediator for feature flows — buses are for rare cross-cutting notifications only.

## Memento

Use when prior state must be restorable: form "discard changes", multi-step wizard back-navigation,
undo in editors, optimistic-update rollback.

Do:

- Snapshot immutably at the owner: the store/composable that owns the state produces and restores snapshots (`structuredClone` of raw state, or persisted drafts); outside code never assembles snapshots from the owner's internals.
- Bound the history: cap undo depth; clear snapshots on scope disposal.
- Pair with Command for undo stacks: the command stores the pre-image it needs to revert.

Do not snapshot reactive proxies directly (`toRaw` first), and do not let rollback masquerade as success after a definitive backend denial — failure classification still applies.

## Flyweight

Rarely needed in UI code — reach for virtualization and pagination before object sharing. The legitimate
frontend forms: shared frozen config/option objects reused across thousands of rows instead of per-row
copies, and icon/format maps defined once at module scope. Shared objects must be immutable; per-row data
stays in the row. Do not introduce sharing machinery without a measured memory problem.

## Visitor

The TS form is functional: a discriminated union of node kinds plus one handler map per operation, closed
by `assertNever` — adding a kind becomes a compile error in every operation map. Use when several
operations (render, validate, export, price) each branch over the same stable set of node kinds.

```ts
const renderNode: { [K in Node['kind']]: (n: Extract<Node, { kind: K }>) => VNode } = {
  text: renderText,
  image: renderImage,
  quiz: renderQuiz,
}
```

Do not build classic `accept()`/double-dispatch machinery in TypeScript — exhaustive unions already provide the guarantee; and if kinds change often while operations are stable, use ordinary per-kind components/polymorphism instead.

## Adapter

Use at external boundaries: backend DTOs, SDKs, browser APIs, legacy services, date libraries.

The recognition signal: the other side's interface is wrong for you and you cannot (or must not) modify
it — a vendor SDK, a backend contract, a legacy module. The adapter implements the interface *your* code
wants, wraps the incompatible target, and translates calls and shapes in one place. If external names,
casing, error shapes, or types appear inside components/stores, the adapter is missing or leaking.

Adapters protect the UI from external shape changes.

Do:

- Compose (wrap the target object); never "adapt" by inheriting from SDK classes.
- Translate errors too: adapter output is app-owned domain errors, not vendor error objects.
- Keep one adapter per foreign boundary; when several call sites hand-fix the same SDK quirk, that is the adapter's job.

Do not confuse with Decorator (same interface, adds behavior) or Facade (new simplified interface over a whole subsystem): Adapter's defining move is *changing* an existing interface to fit an expected one.

## State (finite state machine)

This is the State pattern in its frontend form. Use when UI/domain state has explicit states and transitions: upload lifecycle, auth flow, wizard, media player, payment flow.

Do:

- Model states with discriminated unions.
- Reject impossible transitions.

Do not:

- Represent complex lifecycles as several loosely related booleans.
