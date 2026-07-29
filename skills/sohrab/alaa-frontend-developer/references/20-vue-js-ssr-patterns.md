# Vue and SSR Patterns

Vue mechanics, SSR safety, hydration determinism, lifecycle cleanup and reactivity — the parts that are
true because the app renders on a server before it renders in a browser.

Code quality itself is not here. Composition-API typing, component decomposition, SOLID, store shape,
naming and the pattern catalogue belong to `/alaa-vue-typescript-clean-code`
(`$alaa-vue-typescript-clean-code`) `references/00-topic-map.md`. All code in this file is TypeScript
under `strict`; see `10-contract-and-boundaries.md`.

## Environment detection

```ts
export const isClient =
  typeof window !== 'undefined' && typeof document !== 'undefined'
```

Browser-only work runs in `onMounted()`. A browser global on an SSR render path is a defect, not a
compatibility note.

## SSR and hydration rules

- No `Date.now()`, `Math.random()`, unstable ids, or locale- and timezone-dependent formatting in
  SSR-rendered output. The positive replacement for formatting is in `55-i18n-locale-and-rtl.md`: an
  explicit locale and an explicit timezone, passed from the request, identical on both sides.
- List ordering is deterministic; `v-for` keys are stable, unique and primitive.
- CSS-first responsiveness rather than viewport-driven DOM branching before hydration.
- Reuse SSR-provided data instead of refetching it on first paint.
- No per-request mutable state in a module-level singleton.

## Reactivity

`ref()` for scalar state, `reactive()` for tightly related groups, `computed()` for derived values.
`shallowRef` for large structures. A `watch(..., { deep: true })` needs a named reason why no narrower
target exists, written in the diff. Inline object and array literals in a hot template force child
rerenders — hoist them.

## Lifecycle and cleanup

Everything created in `onMounted()` is torn down in `onBeforeUnmount()`: listeners, observers, timers,
subscriptions, sockets, SSE connections, `AbortController`s. Missing cleanup is the single most common
cause of memory growth after navigation.

## Pattern: request-scoped async work with abort

```ts
import { onBeforeUnmount, onMounted, ref } from 'vue'

export function useClientResource<T>(load: (init: { signal: AbortSignal }) => Promise<T>) {
  const state = ref<{ loading: boolean; data: T | null; error: unknown }>({
    loading: false, data: null, error: null,
  })
  let controller: AbortController | undefined

  onMounted(async () => {
    controller = new AbortController()
    state.value = { ...state.value, loading: true, error: null }
    try {
      state.value = { loading: false, data: await load({ signal: controller.signal }), error: null }
    } catch (error) {
      if ((error as Error).name !== 'AbortError') {
        state.value = { loading: false, data: null, error }
      }
    }
  })

  onBeforeUnmount(() => controller?.abort())
  return state
}
```

Starting a new fetch on a reactive change without aborting the previous one is a defect: the responses
race and the loser can win. Deadlines and retry policy for that fetch are in
`46-resilience-and-degradation.md`.

## Pattern: deterministic SSR shell plus client-only enhancement

Render stable server markup first. Attach viewport observers, sockets, media queries and browser storage
after mount. Below-fold islands may defer hydration — see `41-lighthouse-and-web-vitals.md` for the API
names and the rule about the primary interactive element.

## Anti-patterns

- Reading `localStorage`, `sessionStorage` or `matchMedia` in `setup()` of a server-rendered component.
- Creating a socket, an SSE client or a timer at module scope.
- SSR keys from `Date.now()`, `Math.random()` or an object identity.
- A new dependency added inside an unrelated change. A dependency lands in its own change, with the
  bundle-cost line from `41-lighthouse-and-web-vitals.md` recorded.

## Documentation

Doc comments on public composables, utilities and cross-file modules are owned by
`/alaa-frontend-doc-annotations` (`$alaa-frontend-doc-annotations`) `references/20-jsdoc-patterns.md`;
the staleness contract for a comment that records a security assumption is
`references/60-staleness-and-verification.md` there.

## Common failure signatures

| Symptom | Usual cause |
|---|---|
| hydration warning only on SSR first load | non-deterministic render, or a client-only branch |
| duplicate requests on first paint | SSR/client drift, or a double fetch |
| memory growth after navigation | a timer, listener, observer, socket or fetch never cleaned up |
| child rerender churn | unstable props, inline literals in a template, or a broad deep watcher |
| a value renders differently for two users in one session | an implicit locale or timezone; see `55-i18n-locale-and-rtl.md` |

## Pairing

- Quasar SSR APIs, boot files, `useMeta`, `useHydration`: `/alaa-quasar-app-vite-v3`
  (`$alaa-quasar-app-vite-v3`) `references/00-topic-map.md`.
- Auth propagation and token handling: `21-ssr-auth-and-session-patterns.md`.
- Realtime lifecycle: `40-performance-and-realtime.md`.
