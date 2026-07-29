# Topic map — the only router in this skill

`SKILL.md` is always loaded. Every file below loads only when its condition is met by the diff in front of
you. Each row names an **observable situation**, not a subject: if you cannot tell whether a row matches by
looking at the code on screen, the row is broken and fixing it comes before using it.

One file answers most tasks and two is normal. Loading every row means the task was never scoped.

| You are about to | Read |
|---|---|
| add a `.vue` file, or change a `v-for`, a `:key`, a `v-if`, a prop declaration, an attribute list, a `<style>` block, or a component's filename | `10-vue-style-contract.md` |
| write `defineProps`, `defineEmits`, `defineModel`, `defineSlots`, a `ref`/`computed` annotation, a composable signature, or an injection key | `20-typescript-composition-contract.md` |
| write a type with more than one shape, a generic parameter, `satisfies`, a type predicate, a branded id, `unknown` at a boundary, or a `switch` over a string field | `22-typescript-type-system.md` |
| edit `tsconfig*.json`, add or remove an `import type`, augment a Vue or Quasar type, or see `any`, `as unknown as`, `!`, `enum`, or `@ts-ignore` in the diff | `24-typescript-project-and-antipatterns.md` |
| notice a `useX` returning more than one responsibility, a `.ts` file past 400 lines, an SFC past 300, the same block in a third file, or a name that changes between the DTO and the component | `30-clean-code-solid-vue.md` |
| reach for a pattern by name, or feel a design is wrong without being able to say what hurts | `41-pattern-selection.md` |
| wrap an SDK, an HTTP client, `localStorage`, a browser API, or a cache; or render a recursive tree of nodes | `42-structural-patterns.md` |
| find the same `switch (kind)` in a second file, sequence guards or interceptors, queue or undo an action, or see booleans encoding one lifecycle | `43-behavioral-patterns.md` |
| write a module-level `export const someClient = ...`, build an object through branching, clone a preset, or write `await`, `.then`, or a callback parameter | `44-creational-and-async-idioms.md` |
| touch `quasar.config.*`, `vite.config.*`, `src/boot/*`, a `defineStore` call, a route record, or a Vite alias | `50-quasar-vite-pinia-contract.md` |
| write the words "done", "validated", "tests pass", or "verified" in a response | `60-validation-gates.md` |
| write a view mapper, a flow composable, a store slice, an SDK adapter, or a design-system component in a repo that has a field-source manifest or a `_resolve`-style value resolver | `65-alaa-observed-patterns.md` |
| write `await` in a component or composable, an `AbortController`, a submit handler, a `catch` block, or anything named `retry` | `70-async-and-failure-binding.md` |
| write `v-html`, render text a user or a third party supplied, read a permission inside a component or a guard, add a `VITE_` variable, build a cache or storage key, or parse or format an identifier | `72-frontend-security-binding.md` |
| delete a `console.log`, add an `onErrorCaptured` or `app.config.errorHandler`, attach a header in an HTTP interceptor, or hand an error to Notify or Dialog | `74-observability-binding.md` |
| wire a `watch` on an input to a fetch, call an API inside `v-for`, `map`, or `Promise.all` over a list, add a client-side cache, size a virtual-scroll window, or sort or filter a list whose length is not a constant | `76-load-and-concurrency-binding.md` |
| create a `.spec.ts`, mount a component, stub a store, fake a port, or claim a behaviour is proven | `78-testing-binding.md` |
| assert a version, a "latest" or "current" fact, or cite a source | `05-sources-and-freshness.md` |

## Rows that are not optional when they match

Two rows carry incidents rather than preferences, and matching them is not a suggestion:

- `65-alaa-observed-patterns.md` — every antipattern in it shipped broken once in this codebase and was
  repaired by hand. Repeating one is a blocking finding, not a style note.
- `72-frontend-security-binding.md` — the three surfaces it governs (untrusted content in a template, a
  permission read in the client, a value in `VITE_*`) have no safe default. A component that decides any of
  them locally is wrong even when it happens to be safe today.

## What is not here

This router points only inside this skill. When the question is *what the rule is* rather than *where the
Vue code for it goes*, the owner table in `SKILL.md` names the skill that owns it, and that route is taken
instead of guessing locally.
