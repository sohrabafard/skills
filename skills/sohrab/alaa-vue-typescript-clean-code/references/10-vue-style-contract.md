# Vue style contract

## Priority A: hard failures

Repair these in touched code unless doing so would change public behavior outside scope.

### Multi-word component names

Do:

- `UserCard.vue`, `CourseEnrollmentDialog.vue`, `BaseIcon.vue`.
- Use single-word `App` only for the root app component.

Do not:

- `Item.vue`, `Dialog.vue`, `Table.vue`, `Button.vue` for custom components.

### Detailed props

Do:

```ts
interface Props {
  userId: string
  readonly: boolean
  pageSize?: number
}

const props = withDefaults(defineProps<Props>(), {
  pageSize: 20,
})
```

Use runtime validators only when runtime validation is required by the repo.

Do not:

```ts
const props = defineProps(['id', 'data'])
```

unless it is an existing tiny example being deleted or immediately replaced.

### Keyed `v-for`

Do:

```vue
<CourseCard v-for="course in courses" :key="course.id" :course="course" />
```

Do not use array indexes as keys when items can be inserted, removed, sorted, filtered, or edited.

### No `v-if` with `v-for` on the same element

Do:

```ts
const activeCourses = computed(() => courses.value.filter(course => course.active))
```

```vue
<CourseCard v-for="course in activeCourses" :key="course.id" :course="course" />
```

Or move `v-if` to a wrapper when hiding the whole list.

Do not:

```vue
<CourseCard v-for="course in courses" v-if="course.active" :key="course.id" />
```

### Style containment

Do:

- Use `<style scoped>`, CSS modules, utility classes, or class/BEM naming.
- Put app-wide CSS variables, theme tokens, and reset styles in global files intentionally.

Do not:

- Leak feature-local selectors globally.
- Depend on broad element selectors that accidentally style Quasar internals.

## Priority B: enforced defaults

### One component per file

One SFC owns one component. Extract nested components when they are not trivial and local-only.

### File and component casing

Prefer `PascalCase.vue` and PascalCase imports. If the repo uses kebab-case consistently, follow it. Do not mix casing in a feature.

### Base and tightly coupled component names

- Base/presentational reusable components: `BaseButton`, `BaseIcon`, `AppDialog`, `VInput` according to repo convention.
- Parent-coupled children: `UserProfileAvatar`, `UserProfileStats`, `CourseTableRow`.

### Template component casing

In SFC templates, prefer PascalCase for components and native kebab-case for HTML/custom elements.

### Full words

Use `UserManagementTable`, not `UsrMgmtTbl`. Use abbreviations only when the domain uses them widely (`API`, `URL`, `ID`, `SSO`).

### Attribute and prop formatting

Multi-attribute tags use one attribute per line:

```vue
<QBtn
  :loading="isSubmitting"
  color="primary"
  label="Save"
  @click="submit"
/>
```

### Simple expressions

Templates should read like declarative UI:

```vue
<QBadge :color="statusColor" :label="statusLabel" />
```

Do not embed business conditions, transformations, or multi-step logic inline.

### Simple computed properties

Each computed value should express one idea. If a computed getter maps, filters, sorts, and formats, split it.

### Directive shorthand consistency

Pick one style per repo/feature. Default: `:` for `v-bind`, `@` for `v-on`, `#` for slots.

## Priority C: consistency rules

Use consistent SFC block order. Default for new files:

```vue
<script setup lang="ts">
</script>

<template>
</template>

<style scoped>
</style>
```

If the repository has a different established order, follow it and keep styles last.

Use consistent option, attribute, and import ordering. Prefer:

1. Vue imports
2. Third-party imports
3. Quasar imports
4. Stores/composables/services
5. Components
6. Types
7. Constants

## Priority D: caution rules

### `$parent` and prop mutation

Do not use `$parent`, mutate props, or pass mutable objects for children to mutate unless the contract is explicitly a mutable model object and tests cover it.

Preferred flows:

- Parent to child: props.
- Child to parent: typed emits or `defineModel` where supported.
- Cross-tree state: focused Pinia store, typed provide/inject, or service facade.

### Scoped element selectors

Prefer class selectors. Element selectors in scoped CSS may be slower and less explicit. Use them only for intentionally simple local markup.

### Global components

Register globally only for true base components or plugin surfaces. Feature components are local or auto-imported by the established tooling.
