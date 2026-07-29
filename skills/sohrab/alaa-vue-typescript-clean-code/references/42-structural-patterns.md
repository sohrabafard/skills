# Structural patterns in Vue, Quasar, and TypeScript

Adapter, Decorator, Proxy, Facade, Bridge, Composite, Flyweight. Run the diagnostic in
`41-pattern-selection.md` first; the look-alike distinctions live there and are not restated here.

## Adapter

Use at an external boundary: backend DTOs, SDKs, browser APIs, legacy services, date libraries.

The recognition signal is that the other side's interface is wrong for you and you cannot or must not
modify it. The adapter implements the interface *your* code wants, wraps the target, and translates calls
and shapes in one place. If external names, casing, error shapes, or types appear inside components or
stores, the adapter is missing or leaking.

Do:

- Compose — wrap the target object. Never adapt by inheriting from an SDK class.
- Translate errors too: adapter output is app-owned domain errors, not vendor error objects.
- Keep one adapter per foreign boundary. When several call sites hand-fix the same SDK quirk, fixing it is
  the adapter's job.

The adapter is also the only file permitted an `any`, under the boundary rule in
`22-typescript-type-system.md`.

## Decorator

Use to add cross-cutting behaviour while preserving the API: logging around API calls, permission checks
around actions, loading and error wrappers around async commands, component wrappers that add layout or
validation while keeping the model contract, and caching around a service or adapter method.

Rules that make stacking safe:

- One concern per decorator. Stack small decorators rather than writing one mixed wrapper.
- A decorator always delegates inward and keeps the exact contract. If it needs extra public methods, the
  abstraction is wrong — that is a new service, not a decorator.
- **Stacking order is behaviour.** `retry(cache(fetch))` and `cache(retry(fetch))` differ: one caches the
  result of retrying, the other retries around a cache. Declare the order at one composition site and test
  that order.
- Decorator exists because inheritance cannot add combinations at runtime. If you are tempted to subclass
  or mixin for a cross-cutting concern, wrap instead.

Do not decorate in a way that changes event meaning, prop semantics, or accessibility behaviour without
renaming the component or the contract.

**Caching specifically.** A cache lives in the service or adapter layer as a decorator, never as ad-hoc
`ref` caches scattered through components, because a cache the UI cannot invalidate is a stale-data bug
factory. Cache keys include user and tenant scope, and writes invalidate explicitly — the reason those two
are non-negotiable, and what happens when they are missed, is `72-frontend-security-binding.md`. Time to
live, staleness, and the parallel-request cap around the cache are `76-load-and-concurrency-binding.md`.
Retry policy inside or outside the cache is `/alaa-reliability-sla` (`$alaa-reliability-sla`).

## Proxy

Use to intercept or adapt a target while preserving its external contract: an auth-header wrapper, a lazy
initialiser for an expensive client, a reactive storage wrapper, a permission-guarded resource handle.

The distinguishing move is control over *whether and when* the real call happens — the interface is
unchanged.

Do not reach for the JavaScript `Proxy` object when a normal typed function or class is clearer. Runtime
proxies interact badly with Vue's own reactive proxies and with `structuredClone`, and the debugging cost
is paid by whoever reads it next, not by whoever wrote it.

## Facade

Use to simplify a complex subsystem behind one small typed surface: a Quasar Dialog and Notify facade for
domain feedback, an HTTP facade for backend calls, an IndexedDB facade for persistence, a Web Worker facade
for background commands, a browser-API facade for storage, media, or resize.

Do:

- Return domain models and domain errors.
- Keep facade methods small and named by business use case (`enrollInCourse`, not `postEnrollment`).

Do not leak SDK response shapes or Quasar plugin details into components.

Every browser-API wrapper handles absence, permission denial, cleanup, and SSR safety. What each browser
permission requires, and how a service worker is structured, are
`/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`); IndexedDB schema, quota, and eviction are
`/alaa-indexeddb-browser-storage` (`$alaa-indexeddb-browser-storage`).

## Bridge

Use when a feature varies along two independent axes and the names start concatenating them: preview UI by
document format, chart component by data source, editor by storage backend. Split into two hierarchies —
the abstraction (the component or composable owning the UX flow) holds an injected implementation port (the
format adapter, the data source) — so each axis grows without multiplying the other.

Do not "bridge" a single-axis variation that a strategy prop already solves. Bridge is a planned split of
two hierarchies; Adapter is a retrofit for one incompatible interface.

## Composite

Use for recursive UI trees where leaf and group must be treated uniformly: navigation menus, nested
comments, tree views, folder pickers, nested form sections.

Do:

- Define one typed recursive node contract —
  `interface TreeNode { id: string; children?: readonly TreeNode[] }` — using a discriminated union when
  leaf and group carry different data.
- Render with a recursive component (or `QTree` where it fits) that calls itself for `children`.
- Keep a stable unique `:key` at every level.
- Guard depth and cycles when the input is server-shaped or user-shaped. The depth bound is a number, not
  an intention: `76-load-and-concurrency-binding.md` states where it comes from and what happens when it is
  exceeded.
- Keep per-node behaviour — select, expand, navigate — in emitted intents handled at the tree host, not
  inside each node.

Do not fork separate leaf and group components with divergent props when one contract serves both, and do
not recurse over an unbounded unvalidated structure.

## Flyweight

Rarely needed in UI code — reach for virtualization and pagination before object sharing. The legitimate
frontend forms are a shared frozen config or option object reused across thousands of rows instead of
per-row copies, and icon or format maps defined once at module scope.

Shared objects are immutable; per-row data stays in the row. Do not introduce sharing machinery without a
measured memory problem, and record the measurement beside the change so the next reader can re-check it.
