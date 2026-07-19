# TypeScript and Composition API contract

## SFC baseline

New Vue SFCs use:

```vue
<script setup lang="ts">
</script>
```

Do not use Options API for new code unless the repository already requires it for the touched area.

## Props

Prefer type-based props:

```ts
interface Props {
  userId: string
  status?: UserStatus
  items?: readonly Course[]
}

const props = withDefaults(defineProps<Props>(), {
  status: 'active',
  items: () => [],
})
```

Use Vue 3.5+ reactive prop destructure only when the installed Vue version supports it and the repo already accepts it.

Do not combine runtime and type declarations:

```ts
// Do not do this
const props = defineProps<Props>({ ... })
```

## Emits

Use typed emits with named tuples when supported:

```ts
const emit = defineEmits<{
  save: [payload: SaveUserPayload]
  cancel: []
  'update:page': [page: number]
}>()
```

Do not emit unnamed magic payloads. Name events as domain actions, not DOM implementation details, unless proxying a native input.

## Models

Use `defineModel<T>()` only when the repo's Vue version supports it and the pattern is already accepted. Otherwise use explicit `modelValue` and `update:modelValue`.

For custom inputs:

```ts
const model = defineModel<string>({ required: true })
```

or:

```ts
interface Props { modelValue: string }
const props = defineProps<Props>()
const emit = defineEmits<{ 'update:modelValue': [value: string] }>()
```

## Refs, reactive, computed

Do:

```ts
const isOpen = ref(false)
const selectedUser = ref<User | null>(null)
const statusLabel = computed(() => statusLabels[status.value])
```

Do not use `reactive<T>()` generic to force a type. Prefer typed object literals or interfaces inferred from initial values.

Avoid destructuring reactive objects:

```ts
// Risky if reactivity is needed
const { name } = user
```

Use `toRefs`, computed selectors, or immutable snapshots intentionally.

## Type boundaries

- API responses enter as DTO types and are mapped to domain/UI models.
- `unknown` is narrowed at boundaries.
- `any` is not allowed in touched code unless isolating an untyped third-party boundary with a comment and immediate typed wrapper.
- Use `satisfies` for config and map objects.
- Use discriminated unions for status and async states.

Example:

```ts
type AsyncState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: AppError }
```

Make branching over discriminated unions exhaustive. A `switch` over the discriminant ends with an
`assertNever` default so adding a variant becomes a compile error, not a silent fall-through:

```ts
function assertNever(value: never): never {
  throw new Error(`Unhandled variant: ${JSON.stringify(value)}`)
}
```

Vocabulary is typed constants, never scattered string literals: event names, storage keys, query-param
names, and status codes live in `as const` registries (or union types derived from them). A typo in an
inline string key is a silent bug; a typo against a registry is a compile error.

Time discipline: transport and store timestamps as UTC ISO strings (or epoch numbers) at boundaries;
convert and format only at the display edge through a formatter. Never mutate `Date` objects in place;
treat date values as immutable and put timezone assumptions in one typed module, not per component.

## Composables

Composables are `useX` functions for reusable stateful UI logic.

Do:

```ts
export function useWindowSize() {
  const width = ref(0)
  const height = ref(0)

  const update = () => {
    width.value = window.innerWidth
    height.value = window.innerHeight
  }

  onMounted(() => {
    update()
    window.addEventListener('resize', update)
  })

  onUnmounted(() => window.removeEventListener('resize', update))

  return { width, height }
}
```

Do not:

- Call composables conditionally.
- Hide domain persistence or network orchestration in UI composables when a store/service should own it.
- Return a reactive object that callers must destructure unsafely; return a plain object of refs/computed/functions.
- Touch browser APIs during SSR render.

## Provide/inject

Use typed injection keys:

```ts
export const modalServiceKey: InjectionKey<ModalService> = Symbol('modalService')
```

Co-locate mutations in the provider. Injected consumers call a typed API; they do not mutate provider internals directly.

## Error and async discipline

- Never leave promises floating. Use `await`, `void` with an explicit reason, or a tracked task helper.
- Use `try/catch/finally` around awaited user-visible operations.
- Use `AbortController` or request tokens where stale responses can overwrite newer state.
- Make user-triggered mutations double-fire safe: disable the trigger or dedupe the in-flight request (one pending promise per action key), and pass an idempotency key when the backend accepts one. Re-enable only in `finally`.
- Classify failures before fallback behavior: a definitive backend denial (validation, authorization, non-transient 4xx) surfaces a message and never retries or masquerades as success; transient transport/5xx failures may retry or degrade with honest wording.
- Surface errors through Quasar Notify/Dialog only at UI edges, not deep services.

## Version gates (verify against installed versions, do not assume)

- Vue 3.5+: `useTemplateRef()` for template refs, `useId()` for SSR-stable ids, `onWatcherCleanup()` for
  side-effect cleanup inside watchers, `watch` pause/resume, and stable reactive props destructure. Use them
  only when `package.json` proves the version and the repo already accepts the idiom.
- Vue 3.6+: the reactivity core is rewritten (alien-signals) — internal, no API change to this contract.
  Vapor mode is opt-in and experimental; do not adopt it for production code unless the repo explicitly opts in.
- Pinia 3+: Vue 3 only; `defineStore({ id: ... })` object-id form is removed — use `defineStore('id', ...)`.
- TypeScript 6+: several strict flags and ESM defaults flipped on; TS 7 is the native (Go-based) compiler.
  Keep `tsconfig` strictness explicit rather than relying on version defaults, and verify lint/build tooling
  against the installed major before recommending flags.
