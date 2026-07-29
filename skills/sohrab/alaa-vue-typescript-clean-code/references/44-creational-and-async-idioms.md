# Creational patterns and async idioms in Vue, Quasar, and TypeScript

Singleton, Dependency injection, Factory, Abstract Factory, Builder, Prototype, plus the two idioms that
apply whenever async or interop code is touched: Callbacks and Promises. Run the diagnostic in
`41-pattern-selection.md` first.

## Singleton

Use for one app-wide gateway: an API client facade, an event gateway, a worker manager, a feature registry,
a stateless utility service.

```ts
export const courseApi = createCourseApi(httpClient)
```

Do not:

- Hide mutable per-request or per-user state in module scope where SSR is possible. Under SSR the module is
  shared across requests, so one user's data becomes another's — this is the failure mode that makes the
  rule absolute rather than stylistic.
- Create `getInstance()` ceremony unless the repo convention already requires it.
- Forget the standing criticism: a singleton is hidden global state. It couples everything that touches it
  and makes tests order-dependent. Keep singletons stateless or immutable, and pass the instance through an
  injection key wherever a test seam is needed.

## Dependency injection

Use for replaceable app services, plugin APIs, deeply nested dependencies, and test seams.

```ts
export const courseApiKey: InjectionKey<CourseApi> = Symbol('courseApi')
provide(courseApiKey, courseApi)
const courseApi = injectStrict(courseApiKey)
```

Do not use string keys, which collide silently across a large app and across packages, and do not inject a
raw mutable object for every child to write into — that is a global store with extra steps.

`injectStrict` (an `inject` that throws when the key is absent) is the form to prefer, because the
alternative is a component that silently receives `undefined` and fails three interactions later.

## Factory

Use when creating variants behind a common contract: form field builders, column builders, API adapter
selection, dynamic component maps.

One creator owns the branching and returns one stable type, so call sites stop repeating the branch. Do not
use a factory where a direct constructor or plain function is simpler — a factory with one branch is
indirection with no payoff.

## Abstract Factory

Use when a *family* of related implementations must stay consistent and never be mixed: an upload provider
suite (client, progress adapter, error mapper), an auth provider suite (SDK wrapper, token storage, claims
parser), a theming suite of base components.

Do:

- Define the suite as one typed interface — an object of related factory functions or implementations — and
  select the concrete suite once, at boot or through an injection key. Feature code receives the suite and
  never assembles members from separate configs.
- Reach for it only when two or more members must match. A single varying implementation is plain Strategy
  or Adapter.

Do not resolve family members independently in different modules, which is exactly how provider A's client
ends up paired with provider B's error mapper, producing errors nobody can map.

## Builder

Use fluent builders only for genuinely multi-step conditional configuration assembled from many optional
parts: table column sets that vary by role or feature flag, form schemas, chart configurations.

```ts
const columns = defineCourseColumns()
  .withBase()
  .withProgress({ when: isEnrolledView })
  .withActions(canManageCourses)
  .build() // build() validates and returns a readonly, typed result
```

- Validate invariants in `build()` and return an immutable typed result.
- Try a plain typed object literal with `satisfies` and small helper functions first. A builder must earn
  its keep with real conditional assembly shared across call sites.

Do not wrap a simple options object in builder ceremony, and do not leave the built object mutable and
half-initialized between steps — a half-built object handed to a component renders a half-built table.

In the example above, `canManageCourses` is a UI capability flag, not an authorization decision:
`72-frontend-security-binding.md` states what a client-side permission read may and may not conclude, and
whether the flag exists at all comes from a feature-flag or permission source, never from a literal in the
builder.

## Prototype

Cloning configured objects instead of rebuilding them: preset form schemas, table configurations, draft
templates.

Do:

- Prefer plain immutable presets plus spread or `structuredClone` for deep copies of data objects.
- Call `toRaw()` on a reactive object before `structuredClone` — proxies do not clone.
- Keep preset registries explicit: a typed map of named frozen presets, cloned on use.

Do not hand-copy objects field by field, which silently drops the field added next month, and do not clone
objects holding functions, component references, or abort controllers — clone data, re-create behaviour.

## Callbacks

Use for DOM events, library hooks, and small synchronous extension points.

Do: type the callback signature; keep the callback identity stable when cleanup depends on it (the same
reference must be passed to `removeEventListener` that was passed to `addEventListener`, so an inline arrow
function cannot be removed); remove every listener you add.

Do not use nested callbacks for async control flow that promises express better.

## Promises

The default async abstraction. Prefer `async`/`await` at call sites.

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

Three rules, and each has a visible failure when broken:

- **No floating promise.** `await` it, or `void` it with a comment saying why nobody waits. A floating
  rejection becomes an unhandled rejection with no stack that points at your code.
- **No swallowed error.** A `catch` that returns a default converts an outage into an empty screen.
- **No ignored stale response.** Without abort or a request token, the slower of two in-flight requests
  wins, and the user sees the results of a search they already changed.

Where the `AbortController` lives, who owns cancellation, how in-flight requests are deduped, and how a
failure is classified before any fallback are all `70-async-and-failure-binding.md`. Retry counts, backoff
shape, and timeout values are `/alaa-reliability-sla` (`$alaa-reliability-sla`) and
`/alaa-services-contract` (`$alaa-services-contract`); do not choose them here.
