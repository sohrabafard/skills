# Quasar, Vite, Pinia, router, SSR, and PWA contract

## Quasar SFCs

Use Composition API with `<script setup lang="ts">` for new SFCs. Use Quasar components directly unless a wrapper creates a stable design-system contract.

Do:

```vue
<QBtn
  color="primary"
  :loading="isSubmitting"
  label="Save"
  @click="submit"
/>
```

Do not:

- Wrap every Quasar component just to rename props.
- Put business logic in Quasar table slot templates.
- Depend on undocumented Quasar DOM internals.

## Quasar plugins and boot files

Use `quasar.config.*` for app-wide Quasar plugins. Use `useQuasar()` inside setup.

Boot files are for initialization only:

- HTTP client setup
- Pinia/router/plugin registration
- auth/session restore
- i18n setup
- global app properties when unavoidable

Do not:

- Put feature workflows or page-specific business logic in boot files.
- Access browser-only APIs in universal boot files without client guards.

## SSR safety

SSR-capable code must not touch browser globals during render.

Do:

```ts
onMounted(() => {
  const saved = window.localStorage.getItem(key)
})
```

or guard (match the installed `@quasar/app-vite` line — the constant differs):

```ts
// app-vite v3 (stable line since 3.0.1):
if (import.meta.env.QUASAR_CLIENT) {
  // browser-only code
}

// app-vite v2 (maintenance line):
if (process.env.CLIENT) {
  // browser-only code
}
```

Do not:

- Read `window`, `document`, `navigator`, `localStorage`, `sessionStorage`, or `matchMedia` at module top level.
- Store per-request state in singletons.

## Pinia

Use Pinia for shared mutable state.

Do:

```ts
export const useCourseStore = defineStore('course', () => {
  const courses = ref<Course[]>([])
  const isLoaded = ref(false)

  const activeCourses = computed(() => courses.value.filter(course => course.active))

  async function loadCourses() {
    courses.value = await courseApi.listCourses()
    isLoaded.value = true
  }

  return { courses, isLoaded, activeCourses, loadCourses }
})
```

Rules:

- Store ID is unique and stable.
- Store scope is focused by domain/feature.
- Actions own shared-state mutations and side effects.
- Setup stores return all state needed by SSR/devtools/plugins.
- Stores do not import components.

Do not:

- Create one god store.
- Let components directly mutate shared arrays/objects when an action is required.
- Hide store state by not returning it from setup stores.

## Router

- Lazy-load route components unless they are critical first-screen code.
- Keep route guards small; delegate auth and permissions to services/stores.
- Type route params at the component boundary.
- Avoid fetching the same data redundantly in multiple nested components.

## Vite

- Keep aliases minimal and aligned with tsconfig.
- Use dynamic imports for heavy optional components.
- Keep env access behind typed config modules.
- Do not expose secrets through `VITE_*` variables; anything shipped to client is public.

## PWA/service workers

When touching PWA behavior:

- Confirm cache strategy and invalidation.
- Avoid caching authenticated or user-specific API responses unless explicitly designed.
- Version caches and handle update prompts where user data could be stale.
- Validate install/offline behavior in browser devtools when possible.

## Browser APIs

Wrap browser APIs in composables or facades:

- storage
- resize/intersection observers
- media devices
- clipboard
- notifications
- web workers
- IndexedDB

All wrappers must handle absence, permission denial, cleanup, and SSR safety.
