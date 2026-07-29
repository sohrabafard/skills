# Behavioural patterns in Vue, Quasar, and TypeScript

Strategy, State, Command, Chain of Responsibility, Pipeline, Template Method, Mediator, Memento, Observer,
Visitor, Iterator. Run the diagnostic in `41-pattern-selection.md` first; the look-alike distinctions live
there and are not restated here.

## Strategy

Use for replaceable behaviour: sorting, filtering, pricing, validation mode, auth provider, upload provider.

Prefer a typed strategy map over a long `if`/`else` chain. For one small varying behaviour, a typed function
parameter *is* the strategy — do not build objects until strategies carry state or several methods.

Strategies are independent and unaware of each other. If the variants know each other and trigger switching
between themselves, that is State, below, not Strategy.

## State (finite state machine)

Use when UI or domain state has explicit states and transitions: an upload lifecycle, an auth flow, a
wizard, a media player, a payment flow.

Model the states as a discriminated union and reject impossible transitions:

```ts
type UploadState =
  | { kind: 'idle' }
  | { kind: 'uploading'; progress: number; abort: AbortController }
  | { kind: 'failed'; error: AppError; attempt: number }
  | { kind: 'done'; assetId: AssetId }
```

The signal that you needed this: several loosely related booleans (`isLoading`, `hasFailed`, `isDone`) that
can be true together in combinations nobody has thought about. The union makes those combinations
unrepresentable, and the exhaustiveness rules in `22-typescript-type-system.md` make a new state a compile
error in every consumer.

Transitions belong to one function or one composable that owns the state, not to each component that
displays it.

## Command

Use for actions that need queuing, undo and redo, worker dispatch, auditability, or deferred execution.

The point is turning a method call into a stand-alone typed object, so the action can travel: be queued,
retried, delayed, sent to a worker, undone, or logged. If you only need to *call* behaviour, call a
function. Reach for Command when you need the action *as data*.

```ts
type UploadCommand =
  | { type: 'start'; fileId: FileId }
  | { type: 'pause'; uploadId: UploadId }
  | { type: 'resume'; uploadId: UploadId }
```

Route with a typed handler map. Do not pass untyped string commands with arbitrary payloads between
components, and do not let a command handler mutate unrelated UI state — a handler that reaches outside its
own slice makes the queue unreplayable, which was the reason for the pattern.

## Chain of Responsibility

Use for ordered handler chains where each handler passes on or short-circuits deliberately: HTTP
interceptor chains (auth token, correlation headers, error mapping), router guard sequences reading route
`meta`, validation chains that stop at the first definitive failure.

Do:

- Keep the chain's order explicit and declared centrally. A chain assembled implicitly across files cannot
  be debugged.
- Make short-circuiting a first-class typed outcome, not a thrown surprise.
- **Define chain-end behaviour explicitly.** A request no handler claimed must have a deliberate result:
  deny by default for auth-like chains, pass through for enrichment chains. "Fell off the end" is the
  classic Chain of Responsibility bug and it fails open.
- Type the payload flowing through the chain once; handlers do not mutate unrelated state.

Do not reorder handlers casually — order is part of the contract and is covered by a test. Do not hide a
business decision inside a transport interceptor; interceptors handle transport concerns only.

Two chain contents are owned elsewhere and are cited rather than decided here: what a route guard is
allowed to conclude about authorization is `72-frontend-security-binding.md` and
`/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`); what an interceptor attaches for tracing is
`74-observability-binding.md`.

## Pipeline

Sequential transformation of one payload through ordered stages that all run: DTO normalization (parse,
camel-case, resolve fields, validate), form-submit preparation (trim, coerce, strip empty, attach
metadata), upload preprocessing (read, resize, compress, fingerprint).

```ts
type Stage<T> = (input: T) => T
const prepareSubmit: Stage<CourseDraft>[] = [trimStrings, normalizeDigits, coerceNumbers, stripEmptyOptionals]
const payload = prepareSubmit.reduce((acc, stage) => stage(acc), draft)
```

- Keep stages pure `(T) => T`, or `(T) => Promise<T>` for async pipelines. Side effects stay out of
  transform stages.
- Type the payload once for the whole pipeline. A stage needing a different shape marks a pipeline
  boundary, not a cast.
- Declare stage order in one place and test the composed pipeline, not only the individual stages.

The submit pipeline is where digit and text normalization runs, through the shared implementation named in
`72-frontend-security-binding.md` — never as a hand-rolled `replace` inside a stage.

Do not confuse this with Chain of Responsibility: pipeline stages never short-circuit on "handled". A stage
that can reject returns a typed result and ends the pipeline explicitly, or belongs in a validation chain.
And do not build pipeline machinery for two obvious function calls.

## Template Method

Recognize the need: the same multi-step flow duplicated in several places with small variations in
individual steps — three import flows differing only in parsing, three pickers differing only in rendering.
The cure is one owner for the skeleton; callers extend *particular steps*, never the structure or the step
order.

In Vue the skeleton belongs to composition, never inheritance:

- Renderless or headless components own the algorithm — fetching, selection, keyboard handling — and expose
  slots and scoped slots where callers fill in the varying rendering.
- Composables own a fixed flow and accept typed callbacks for the varying steps:
  `useImportFlow({ transform, onConflict })`.
- A Quasar component with slots is this pattern already applied; fill its slots rather than wrapping it.

Do:

- Keep the step order fixed and non-overridable; expose only the intended steps as typed callbacks or slots.
- Distinguish required steps (no default — the type requires them) from optional hooks (safe no-op defaults).
- Keep hooks few. A skeleton with ten injectable steps is not an algorithm, it is an escape hatch.

Do not create base-component hierarchies or mixin chains to share a skeleton. If callers need to replace the
*whole* algorithm at runtime rather than fill steps, that is Strategy.

## Mediator

Use when sibling components coordinate through a web of refs and relayed emits, or when a page's children
each know the others' state. The host page or one orchestrator composable becomes the mediator: children
are props-in and events-out and know only their own contract; the mediator owns the coordination policy.

Do:

- Keep children mediator-blind: they emit intents, the mediator decides.
- Keep the mediator thin — policy and sequencing only. Heavy logic stays in the focused composables it
  composes.

Do not let the mediator grow into a god composable; the size budgets in `SKILL.md` are the gate, and the
incident that produced them is in `65-alaa-observed-patterns.md`. Do not use a global event bus as an
anonymous mediator for a feature flow; buses are for rare cross-cutting notifications only.

## Memento

Use when prior state must be restorable: form "discard changes", multi-step wizard back-navigation, undo in
an editor, optimistic-update rollback.

Do:

- Snapshot immutably at the owner. The store or composable that owns the state produces and restores
  snapshots; outside code never assembles a snapshot from the owner's internals.
- `toRaw()` a reactive object before `structuredClone` — a proxy does not clone.
- Bound the history: cap undo depth, and clear snapshots on scope disposal.
- Pair with Command for an undo stack: the command carries the pre-image it needs to revert.

Do not let a rollback masquerade as success after a definitive backend denial. Failure classification comes
first — `70-async-and-failure-binding.md`.

## Observer

The defining signal: the set of interested parties is unknown to the producer, or changes at runtime. The
producer announces; subscribers decide to care.

Vue's reactivity, `watch`, props and emits, and Pinia subscriptions are all Observer already; a hand-rolled
subscription list is almost never needed. Use props and emits for parent-child, Pinia for shared domain
data, and an event bus only for genuinely cross-cutting events such as auth-expired,
connectivity-changed, or upload-progress.

Do: subscribe in `onMounted` or in setup where safe, unsubscribe in `onUnmounted`, and type event names and
payloads. Do not use an event bus to avoid designing ownership, and do not store business data only in an
event payload — a subscriber that mounts late then has no way to learn the current value.

If the producer must know exactly who reacts and in what order, that is a workflow owned by a mediator.

## Visitor

The TypeScript form is functional: a discriminated union of node kinds plus one handler map per operation,
closed by exhaustiveness. Adding a kind becomes a compile error in every operation map.

```ts
const renderNode: { [K in Node['kind']]: (n: Extract<Node, { kind: K }>) => VNode } = {
  text: renderText,
  image: renderImage,
  quiz: renderQuiz,
}
```

Use when several operations — render, validate, export, price — each branch over the same stable set of node
kinds. Do not build classic `accept()` double-dispatch machinery in TypeScript; exhaustive unions already
give the guarantee. If the kinds change often while the operations are stable, use ordinary per-kind
components instead — the pattern is optimised for the opposite ratio.

## Iterator

Prefer typed array methods and computed chains for ordinary traversal. Use generators (`function*`) only
for genuinely lazy or streaming sequences: paginated API pages, chunked file processing, infinite-scroll
feeds.

Do:

- Keep each generator step pure, or make single-pass consumption explicit in the name.
- Pair any potentially unbounded sequence with pagination or a bounded viewport — the iterator pattern in a
  UI ends at a bounded window. Which paging contract to use is
  `/alaa-keyset-pagination` (`$alaa-keyset-pagination`); the window sizing is
  `76-load-and-concurrency-binding.md`.

Do not materialise a huge array only to `.map().filter()` it for a viewport showing twenty rows, and do not
hand-write iterator classes where `for...of` over a generator already reads clearly.
