# Quasar, Vite, Pinia, and router contract

The Vue-shaped rules for the app shell. Quasar CLI semantics, `quasar.config` options, app-vite line
detection, service-worker depth, and browser-permission flows are
`/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`) and are not decided here.

## Quasar components and boot files

Use Quasar components directly. Wrap one only to create a stable design-system contract — a wrapper that
just renames props adds a file, a test, and a version to maintain, and hides the upstream documentation
from the next reader.

Use `useQuasar()` inside setup; register app-wide plugins through `quasar.config.*`.

A boot file initializes app-level dependencies only: HTTP client setup, Pinia, router, and plugin
registration, session restore, i18n. A feature workflow or page-specific logic in a boot file runs on every
page load of the app, including the ones that do not need it, and is a review failure.

## SSR safety — the shape rule

**A browser global is read inside `onMounted`, inside an explicitly client-only boot file, or behind the
build-time client guard — never at module top level, and never during render.**

```ts
onMounted(() => {
  const saved = window.localStorage.getItem(key)
})
```

The guard *constant* differs by `@quasar/app-vite` line, and picking it is not this skill's decision: read
the installed line and the correct constant from
`/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`). Do not copy a guard constant from memory or from
another repository.

Per-request state is never stored in a module-level singleton (`44-creational-and-async-idioms.md`).

SSR authentication and session handling, PWA and offline policy, and Web Vitals are
`/alaa-frontend-developer` (`$alaa-frontend-developer`). A service-worker change is verified per
`/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`); this skill does not accept a service-worker change
as validated by typecheck and lint alone.

## Pinia

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

- The store id is unique and stable. It is a persistence and devtools key, so renaming it is a breaking
  change.
- Scope is one domain or feature. One god store makes every feature's tests depend on every other feature.
- Actions own shared-state mutations and side effects; a component does not mutate a shared array directly
  where an action exists.
- A setup store returns everything SSR, devtools, and plugins need. State not returned is invisible to
  hydration, and the symptom is a value that is correct on the server and empty in the browser.
- Stores do not import components.
- The Pinia major gate, including which `defineStore` signature survives, is
  `20-typescript-composition-contract.md`.

## Router

- Lazy-load route components unless they are critical first-screen code, and use dynamic imports for heavy
  optional components.
- Declare each route's auth and permission posture in typed route `meta`, and let guards read the meta as
  an explicit ordered chain. A route whose trust posture cannot be read from its route record is
  undeclared, and scattered per-component auth checks are a review failure. **What a guard's conclusion is
  worth — and specifically that it is a UI decision and not an authorization decision — is
  `72-frontend-security-binding.md`**, with the doctrine owned by
  `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`).
- Type route params at the component boundary; `route.params.id` is `string | string[]` until you narrow it.
- Do not fetch the same data redundantly in several nested components on one route.
- Route `meta` is typed by augmentation, per `24-typescript-project-and-antipatterns.md`.

## Vite

- Keep aliases minimal and identical to the `tsconfig` paths, so the editor, the typechecker, and the
  bundler agree.
- Keep environment access behind one typed config module rather than reading `import.meta.env` across the
  codebase; the env type declaration is in `24-typescript-project-and-antipatterns.md`.
- Which variables may exist, and the rule that a `VITE_*` value is public, are
  `72-frontend-security-binding.md`.
