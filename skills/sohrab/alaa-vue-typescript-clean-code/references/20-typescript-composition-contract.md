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
- Surface errors through Quasar Notify/Dialog only at UI edges, not deep services.
