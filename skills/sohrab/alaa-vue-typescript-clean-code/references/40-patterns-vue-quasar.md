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

## Strategy

Use for replaceable behavior: sorting, filtering, pricing, validation mode, auth provider, upload provider.

Prefer typed strategy maps over long if/else chains.

## Adapter

Use at external boundaries: backend DTOs, SDKs, browser APIs, legacy services, date libraries.

Adapters protect the UI from external shape changes.

## Finite state machine

Use when UI/domain state has explicit states and transitions: upload lifecycle, auth flow, wizard, media player, payment flow.

Do:

- Model states with discriminated unions.
- Reject impossible transitions.

Do not:

- Represent complex lifecycles as several loosely related booleans.
