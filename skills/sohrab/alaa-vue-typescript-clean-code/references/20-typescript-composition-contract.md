# TypeScript and Composition API contract

The shape of a Vue component's and composable's typed surface. The type system itself — unions,
exhaustiveness, generics, `satisfies`, branded ids, narrowing — is `22-typescript-type-system.md`;
compiler flags, module syntax, augmentation, and the antipattern catalogue are
`24-typescript-project-and-antipatterns.md`.

## SFC baseline

New SFCs use `<script setup lang="ts">`. Options API is used for new code only where the repository already
requires it for the touched area, and that requirement is named in the response.

## Props

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

Type-based declaration is the default. Runtime and type declarations are never combined in one component
(`defineProps<Props>({ ... })` is rejected) — the two forms disagree about defaults and about what the
compiler can see, and a component using both has two prop contracts.

Array and object defaults go through a factory, because a shared literal default is one object shared by
every instance.

Reactive prop destructure is used only when the installed Vue version supports it and the repo already
accepts the idiom; `props.x` in a watcher or computed is otherwise the reading form, because a plain
destructure takes a value once and never updates.

## Emits

```ts
const emit = defineEmits<{
  save: [payload: SaveUserPayload]
  cancel: []
  'update:page': [page: number]
}>()
```

Every emit is typed with a named tuple. Events are named as domain actions (`save`, `enroll`,
`retryRequested`), not as DOM implementation details, except when the component is proxying a native input.
The event *name* is a contract: adding one is additive, renaming one is a breaking change, and the fleet's
event-name vocabulary belongs to `/alaa-services-contract` (`$alaa-services-contract`).

## Models

`defineModel<T>()` where the installed Vue version supports it and the repo accepts it:

```ts
const model = defineModel<string>({ required: true })
```

Otherwise the explicit pair:

```ts
interface Props { modelValue: string }
const props = defineProps<Props>()
const emit = defineEmits<{ 'update:modelValue': [value: string] }>()
```

## Refs, reactive, computed

```ts
const isOpen = ref(false)
const selectedUser = ref<User | null>(null)
const statusLabel = computed(() => statusLabels[status.value])
```

Annotate `ref<T>()`, `computed<T>()`, and function return types wherever inference is weak or wherever the
inferred type is wider than the contract you mean (`ref(null)` infers `null`, not `User | null`).

Do not use the `reactive<T>()` generic to force a type; let Vue infer from a typed object literal, or use
typed refs and computed values. Do not destructure a reactive object unless you are using `toRefs`, a
supported reactive prop destructure, or a deliberate immutable snapshot — a plain destructure reads the
value once and the binding never updates again, and the symptom is a screen that shows a stale number with
no error anywhere.

## Type boundaries

- An API response enters as a DTO type and is mapped to a domain or UI model before it reaches a component.
  A raw response shape does not travel past the adapter.
- `unknown` is narrowed at the boundary; `any` is not used. `22-typescript-type-system.md` owns the
  narrowing forms and the adapter rule.
- Vocabulary is typed constants, never scattered string literals: event names, storage keys, query-param
  names, and status codes live in one `as const` registry per family, or in a union derived from it. A typo
  against an inline string is a silent bug; a typo against a registry is a compile error. The *values* in
  those registries — which key, which param name, which code — are owned by
  `/alaa-services-contract` (`$alaa-services-contract`); this file owns only the requirement that they sit
  in a typed registry.
- Time: transport and store timestamps in the wire form at boundaries, convert and format only at the
  display edge through a formatter module, and never mutate a `Date` in place. Which wire form, and which
  timezone the product displays, are `/alaa-services-contract` (`$alaa-services-contract`) values.

## Composables

A composable is a `useX` function for reusable stateful UI logic. It is called synchronously from a
setup-compatible context, and it returns a plain object of refs, computed values, and functions — never a
reactive object that callers must destructure to use.

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

It accepts refs, getters, or plain values where that widens its usefulness, and normalizes them with
`toValue` where supported.

Rejected: calling a composable conditionally or inside a callback; owning domain persistence or network
orchestration that a store or service owns; touching a browser global during SSR render. Generic
composables — a `useX<T>` with a constraint — are `22-typescript-type-system.md`. Teardown obligations and
what a composable must expose for an async flow are `70-async-and-failure-binding.md`.

## Provide and inject

```ts
export const modalServiceKey: InjectionKey<ModalService> = Symbol('modalService')
```

Injection keys are `Symbol`-based and typed, because a string key silently collides across a large app and
across packages. Mutation lives with the provider; an injected consumer calls a typed API and does not
reach into provider internals.

## Version gates

Verify against the installed version before using any of these. `scripts/check-frontend-versions.mjs`
prints installed versus latest for the packages named here; `05-sources-and-freshness.md` owns how to read
the result.

- **Vue 3.5+**: `useTemplateRef()`, `useId()` for SSR-stable ids, `onWatcherCleanup()` for side-effect
  cleanup inside a watcher, `watch` pause and resume, and stable reactive props destructure. Use them only
  when `package.json` proves the version and the repo already accepts the idiom.
- **Vue 3.6**: at release candidate, with Vapor mode complete (`read: 2026-07-28`). The reactivity core is
  rewritten internally, which changes nothing in this contract. Vapor mode is not adopted for production
  code unless the repository explicitly opts in, in a file you can point at.
- **Pinia 3**: Vue 3 only, and the `defineStore({ id: ... })` object-id form is removed — `defineStore('id', ...)`
  is the surviving signature (`https://pinia.vuejs.org/cookbook/migration-v2-v3.html`, `read: 2026-07-28`).
- **TypeScript**: the fleet line, and why, are in `24-typescript-project-and-antipatterns.md`. Do not infer
  a TypeScript version rule from anything in this file.
