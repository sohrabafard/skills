# Vue style contract

The official Vue style guide, expressed as gates you can check against a diff.

**Scope of repair.** Repair these inside files the change already touches. A repair that would alter a
published prop, emit, slot, route name, storage key, or i18n key is not made here; it is reported as a
blocker naming the file and the symbol, because those are public contracts and `SKILL.md`'s contract
inventory governs them.

## Priority A — hard failures

A Priority A violation inside touched code is a blocking finding, not a preference.

### Multi-word component names

`UserCard.vue`, `CourseEnrollmentDialog.vue`, `BaseIcon.vue`. Single-word `App` is reserved for the root
component. `Item.vue`, `Dialog.vue`, `Table.vue`, and `Button.vue` collide with current and future HTML
elements and are rejected.

### Detailed props

```ts
interface Props {
  userId: string
  readonly: boolean
  pageSize?: number
}

const props = withDefaults(defineProps<Props>(), { pageSize: 20 })
```

`defineProps(['id', 'data'])` is rejected. The literal `20` above is an example default, not a fleet value:
page sizes, poll intervals, and limits come from `/alaa-services-contract` (`$alaa-services-contract`), and
`76-load-and-concurrency-binding.md` states where the value is read rather than typed in.

Runtime validators are used only where the repo already requires runtime validation of props.

### Keyed `v-for`

```vue
<CourseCard v-for="course in courses" :key="course.id" :course="course" />
```

An array index is not a key when items can be inserted, removed, sorted, filtered, or edited, because the
index of an item changes while its identity does not, and Vue then reuses the wrong DOM node and the wrong
component state.

### No `v-if` on the same element as `v-for`

```ts
const activeCourses = computed(() => courses.value.filter(course => course.active))
```

```vue
<CourseCard v-for="course in activeCourses" :key="course.id" :course="course" />
```

Move the condition to a computed source, or to a wrapper element when the whole list is being hidden.

### Style containment

Use `<style scoped>`, CSS modules, utility classes, or BEM-style class naming. App-wide CSS variables,
theme tokens, and resets live in global files on purpose. A feature-local selector never leaks globally,
and a broad element selector never reaches Quasar internals. Design tokens, theming, and motion themselves
belong to `/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`).

## Priority B — enforced defaults

These are the default contract; a repo-wide stronger convention wins over them, and mixing conventions
inside one feature does not.

- **One component per file.** Extract a nested component as soon as it stops being trivial and local-only.
- **Casing.** `PascalCase.vue` files and PascalCase imports, unless the repo is consistently kebab-case.
- **Base and coupled names.** Reusable presentational components carry the repo's prefix (`BaseButton`,
  `AppDialog`, `VInput`). A child that only makes sense inside one parent carries the parent's name
  (`UserProfileAvatar`, `CourseTableRow`).
- **Template casing.** PascalCase for components, kebab-case for native and custom elements.
- **Full words.** `UserManagementTable`, not `UsrMgmtTbl`. Abbreviate only where the domain does: `API`,
  `URL`, `ID`, `SSO`.
- **One attribute per line** on multi-attribute tags:

```vue
<QBtn
  :loading="isSubmitting"
  color="primary"
  label="Save"
  @click="submit"
/>
```

- **Simple template expressions.** A template reads as declarative UI: `<QBadge :color="statusColor" :label="statusLabel" />`.
  A business condition, a transformation, or multi-step logic inline in a template is moved to a computed
  value or a function, because a template expression cannot be unit-tested and cannot be typed at its use
  site.
- **Simple computed values.** One computed expresses one idea. A getter that maps and filters and sorts and
  formats is four things and splits into four.
- **Consistent directive shorthand.** Default `:` for `v-bind`, `@` for `v-on`, `#` for slots; pick one
  style per repo and keep it.

## Priority C — consistency

Default SFC block order for new files, with styles last:

```vue
<script setup lang="ts">
</script>

<template>
</template>

<style scoped>
</style>
```

An established different order in the repository wins, as long as styles stay last.

Import order, top to bottom:

1. Vue
2. Third-party packages
3. Quasar
4. Stores, composables, services
5. Components
6. Types
7. Constants

The point of the order is that a reader can find the dependency class they are looking for without reading
every line; it is not a lint rule you are inventing, so if the repo's ESLint config already sorts imports,
its order wins and this list is not applied on top of it.

## Priority D — use with caution

### `$parent` and prop mutation

Do not use `$parent`, mutate a prop, or hand a child a mutable object to write into, unless the contract is
explicitly a mutable model object and a test covers that contract. Parent to child is props; child to
parent is a typed emit or `defineModel`; across the tree it is a focused Pinia store, a typed
provide/inject, or a service facade.

### Element selectors in scoped CSS

Prefer class selectors inside `<style scoped>`. The rule holds on explicitness: `button { ... }` in a scoped
block silently claims every `button` the component renders now or later, including ones a Quasar component
puts there, while `.btn-close` claims exactly what it names. The Vue style guide additionally states that
element-attribute selectors are slower than class-attribute selectors
(`https://vuejs.org/style-guide/rules-use-with-caution.html`, `read: 2026-07-28`); upstream discussion
questions the size of that effect on current engines, so do not present the performance figure as measured.
Element selectors remain acceptable for intentionally simple local markup you fully own.

### Global components

Register globally only for true base components and plugin surfaces. A feature component is imported where
it is used, or auto-imported by whatever the repo already configured.
