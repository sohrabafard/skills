# Vue, JavaScript, and SSR Patterns

Use this file for Vue mechanics, JavaScript module hygiene, SSR safety, hydration determinism, lifecycle cleanup, and reactivity decisions.

## Prime directive

Write clean, deterministic frontend code that stays safe under SSR, hydration, and bundlers. Default to JavaScript plus JSDoc unless the repo already standardizes on TypeScript.

## Environment detection

Use explicit browser guards:

```js
export const isClient =
  typeof window !== 'undefined' && typeof document !== 'undefined'
```

- Prefer `onMounted()` for browser-only work.
- Do not assume browser globals are safe during SSR.

## SSR and hydration rules

- Avoid `Date.now()`, `Math.random()`, unstable IDs, or implicit locale/timezone formatting in SSR-rendered output.
- Keep list ordering deterministic.
- Use stable, unique, primitive `v-for` keys.
- Prefer CSS-first responsiveness over viewport-driven DOM branching before hydration.
- Reuse SSR-provided data when a repo pattern exists instead of double-fetching on the client.
- Do not store per-request mutable state in module-level singletons.

## Reactivity discipline

- Prefer `ref()` for scalar state and `reactive()` for tightly related grouped state.
- Avoid large reactive objects that hide dependencies.
- Prefer `computed()` for derived values instead of recomputing in templates.
- Avoid `watch(..., { deep: true })` unless there is no better target to watch.
- Avoid inline object and array creation in hot templates when it causes child rerenders.

## Lifecycle and cleanup

Anything created in `onMounted()` needs cleanup in `onBeforeUnmount()`:

- event listeners
- observers
- timers
- subscriptions
- socket or SSE connections
- `AbortController`s

## Data-fetching defaults

- Follow the repo's established SSR data path first.
- If a repo uses Quasar `preFetch`, server boot files, or another SSR bootstrap pattern, stay aligned with that path.
- Keep server-side auth mapping server-side only.

## SSR-safe patterns

Pattern: request-scoped async work with cleanup

```js
import { onBeforeUnmount, onMounted, ref } from 'vue'

export function useClientResource(load) {
  const state = ref({ loading: false, data: null, error: null })
  let controller

  onMounted(async () => {
    controller = new AbortController()
    state.value = { ...state.value, loading: true, error: null }

    try {
      const data = await load({ signal: controller.signal })
      state.value = { loading: false, data, error: null }
    } catch (error) {
      if (error.name !== 'AbortError') {
        state.value = { loading: false, data: null, error }
      }
    }
  })

  onBeforeUnmount(() => controller?.abort())

  return state
}
```

Pattern: deterministic SSR shell plus client-only enhancement

- Render stable SSR markup first.
- Attach viewport observers, sockets, media queries, and browser storage only after mount.
- Reuse SSR-fetched data instead of immediately refetching on first paint.

## Anti-patterns

- Reading `localStorage`, `sessionStorage`, or `matchMedia` in `setup()` for a component that renders on the server
- Creating sockets, SSE clients, or timers at module scope
- Generating SSR keys from `Date.now()`, `Math.random()`, or unstable object references
- Starting a new fetch on every reactive change without aborting the previous one
- Using inline object literals in hot templates when they force unnecessary child rerenders

## JavaScript module hygiene

- Prefer small pure functions with explicit inputs and outputs.
- Avoid module-level side effects that vary by request, time, or environment.
- Use `AbortController` for cancellable async work and always abort on cleanup.
- Avoid introducing new dependencies unless the user explicitly asks or the task clearly justifies them.

## JSDoc default

For public composables, utilities, or modules that cross file boundaries, prefer English JSDoc that explains:

- what it does
- why it exists
- how it works
- usage shape
- constraints or trade-offs

For documentation-only changes, pair with `$inline-doc-writer`.

## Modern Vue guidance

- Prefer Composition API and repo-established patterns.
- Use newer Vue 3.5 features only when they improve clarity and fit the repo's existing style.
- Do not add novelty for its own sake.

## Common failure signatures

- Hydration warnings only on SSR first load:
  - usually a non-deterministic render or client-only branch
- Duplicate requests on first paint:
  - usually SSR/client drift or double-fetch
- Memory growth after navigation:
  - usually missing cleanup for timers, listeners, observers, sockets, or fetches
- Child rerender churn:
  - often unstable props, inline objects, or broad deep watchers

## Pairing guidance

- Exact Quasar SSR APIs, boot files, `useMeta`, or `useHydration`:
  - Pair with `$quasar-skill-packe`
- SSR auth propagation, token storage, refresh, or protected-route decisions:
  - Also load `21-ssr-auth-and-session-patterns.md`
- Realtime lifecycle:
  - Also load `40-performance-and-realtime.md`
