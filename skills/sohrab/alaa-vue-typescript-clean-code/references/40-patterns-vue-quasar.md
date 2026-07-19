# Design patterns for Vue, Quasar, Vite, and TypeScript

Use patterns as constraints for maintainability, not decoration. A pattern is correct only when it improves data flow, testability, encapsulation, or extension.

## Singleton

Use for one app-wide gateway: API client facade, event gateway, worker manager, feature registry, or stateless utility service.

Do:

```ts
export const courseApi = createCourseApi(httpClient)
```

Do not:

- Hide mutable per-request/per-user state in module scope when SSR is possible.
- Create Java-style `getInstance()` ceremony unless repo convention requires it.

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

Use props/emits for parent-child observation, Pinia for shared domain data, and an event bus only for cross-cutting events such as auth-expired, connectivity-changed, or upload-progress notifications.

Do:

- Subscribe in `onMounted` or setup when safe.
- Unsubscribe in `onUnmounted`.
- Type event names and payloads.

Do not:

- Use an event bus to avoid designing ownership.
- Store business data only in event payloads.

## Command

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

The "skeleton with fillable steps" belongs to composition in Vue, never inheritance:

- Renderless/headless components own the algorithm (fetching, selection, keyboard handling) and expose slots/scoped slots where callers fill in the varying rendering steps.
- Composables own a fixed flow and accept typed callbacks/strategies for the varying steps (`useImportFlow({ transform, onConflict })`).
- Quasar components with slots are this pattern applied; prefer filling their slots over wrapping them.

Do not create base-component class hierarchies or mixin chains to share an algorithm skeleton; that is the inheritance form this codebase bans.

## Chain of Responsibility

Use for ordered handler chains where each handler passes on or short-circuits deliberately:

- HTTP client interceptor chains (auth token → correlation headers → retry → error mapping), each interceptor with one job.
- Router guard sequences reading route `meta` (auth → permission → data preconditions), each guard returning pass/redirect.
- Validation chains where rules run in declared order and stop at the first definitive failure.

Do:

- Keep the chain's order explicit and centrally declared; a chain assembled implicitly across files is undebuggable.
- Make short-circuiting a first-class, typed outcome, not a thrown surprise.
- Type the payload flowing through the chain once; handlers do not mutate unrelated state.

Do not:

- Reorder handlers casually — order is part of the contract; test it.
- Hide business decisions inside transport interceptors; interceptors handle transport concerns only.

## Strategy

Use for replaceable behavior: sorting, filtering, pricing, validation mode, auth provider, upload provider.

Prefer typed strategy maps over long if/else chains.

## Adapter

Use at external boundaries: backend DTOs, SDKs, browser APIs, legacy services, date libraries.

Adapters protect the UI from external shape changes.

## State (finite state machine)

This is the State pattern in its frontend form. Use when UI/domain state has explicit states and transitions: upload lifecycle, auth flow, wizard, media player, payment flow.

Do:

- Model states with discriminated unions.
- Reject impossible transitions.

Do not:

- Represent complex lifecycles as several loosely related booleans.
