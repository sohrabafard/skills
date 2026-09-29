Version-sensitive claims in this topic depend on [Vue and TypeScript sources and freshness](../05-sources-and-freshness.md).

## Declaration merging and module augmentation

Augmentation is how a Vue or Quasar type gains a field your repo needs, in one place, with the compiler
enforcing it everywhere.

Route meta — this is what makes `meta.requiresAuth` a checked field rather than a hopeful one:

```ts
// src/types/router.d.ts
import 'vue-router'

declare module 'vue-router' {
  interface RouteMeta {
    requiresAuth?: boolean
    permissions?: readonly PermissionKey[]
  }
}
```

Vite environment variables, so `import.meta.env.VITE_API_BASE_URL` is typed and a missing one is a compile
error:

```ts
// src/types/env.d.ts
interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string
}
interface ImportMeta { readonly env: ImportMetaEnv }
```

Global component properties added by a boot file, so `this.$myThing` and template usage type-check:

```ts
declare module 'vue' {
  interface ComponentCustomProperties {
    $formatCurrency: (value: number) => string
  }
}
```

Rules: augmentations live in `src/types/*.d.ts` and are included by `tsconfig`, never scattered beside
feature code; an augmentation file that contains a top-level `import`/`export` becomes a module, so
`declare module` inside it is the augmentation form and `declare global` is needed for true globals; and an
augmentation only ever adds — narrowing or redefining an upstream member breaks at the next upgrade in a
way that is very hard to trace.

Which environment variables may exist at all, and which are forbidden, is
`../72-frontend-security-binding.md`. Global component properties added by boot files are
`../50-quasar-vite-pinia-contract.md`.
