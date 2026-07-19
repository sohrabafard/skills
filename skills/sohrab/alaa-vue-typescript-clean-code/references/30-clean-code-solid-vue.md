# Clean code and SOLID for Vue/Quasar/TypeScript

This file translates the requested design-principle set into enforceable frontend rules.

## Separation of concerns

Do:

- Component: renders UI and coordinates user interaction.
- Composable: reusable UI/stateful behavior such as resize, form dirty state, selection, table filters.
- Pinia store: shared application/domain state and actions.
- Service/API client: HTTP, SDK, browser API, persistence, DTO mapping.
- Validator: pure validation and user-safe error objects.
- Formatter: presentation-only value formatting.

Do not:

- Put API calls, DTO mapping, Quasar notifications, route mutation, validation, and table rendering in one component.
- Let a service import Vue components or Quasar UI primitives.
- Let a store know about DOM or component instances.

## Composition over inheritance

Do:

- Use composables, slots, scoped slots, renderless components, small service facades, and Quasar extension points.
- Use discriminated unions and strategy maps for variants.

Do not:

- Create mixins for new code.
- Build inheritance-style base components that force unrelated features into one class-like hierarchy.

## Single responsibility

A file has one primary reason to change.

Split a component when it handles three or more unrelated concerns, such as fetching, state ownership, validation, formatting, and complex rendering.

Do not split so aggressively that each prop or button becomes a component without reuse, testability, or readability benefit.

## Encapsulation

Do:

- Treat components as black boxes with typed props/emits/slots.
- Treat stores and services as modules with small public APIs.
- Hide SDK and browser API quirks behind facades/adapters.

Do not:

- Reach into child internals.
- Export mutable module globals unless they are intentional app-level singletons.
- Share raw API response shapes across the UI.

## KIC — keep it clean

Do:

- Group related functions: state, derived state, actions, lifecycle, helpers.
- Clean up listeners, timers, subscriptions, observers, object URLs, pending requests, and worker messages.
- Remove dead code, unused imports, stale comments, console logs, and temporary flags.

Do not:

- Leave cleanup to garbage collection when explicit cleanup is available.
- Keep commented-out implementations.
- Add broad TODOs without owner, reason, and boundary.

## DRY — do not repeat yourself

Do:

- Extract duplicate domain rules, mapping, validation, API calls, Quasar option builders, and repeated table column config.
- Keep duplication if two cases only look similar but change for different reasons.

Do not:

- Create generic helpers named `utils`, `common`, or `helper` with unrelated functions.
- Abstract too early based on visual similarity only.

## KISS — keep it simple and short

Do:

- Prefer obvious data flow and explicit state transitions.
- Use simple functions before patterns.
- Use pattern machinery only when it solves a current complexity.

Do not:

- Add factories, buses, dependency containers, or global stores for local one-component state.
- Hide simple logic behind clever abstractions.

## Code for the next developer

Do:

- Use names that expose intent: `isEnrollmentOpen`, `submitEnrollment`, `mapCourseDtoToCourse`.
- Comment why a non-obvious constraint exists, not what the code says.
- Add tests around edge cases and regressions.

Do not:

- Use abbreviations, negated booleans, or magic strings where a typed state is clearer.
- Depend on undocumented ordering, timing, or Quasar internals.

## Boundary naming alignment

One canonical domain term per concept, kept identical across the concept's whole artifact family.

Do:

- `CourseDto` → `mapCourseDtoToCourse` → `Course` → `useCourseFilters` → `useCourseStore` → `CourseTable.vue` → `course-table.spec.ts`.
- Pick one term (`Course`, not sometimes `Lesson`, sometimes `ClassItem`) and keep singular/plural accurate.
- Rename the whole family together when a rename is in scope; half-renamed families are worse than the old name.

Do not:

- Introduce synonyms for the same business concept across layers.
- Create files named `utils.ts`, `common.ts`, `helpers.ts`, or `manager.ts` as dumping grounds; name modules by their single responsibility.
- Use role suffixes (`Service`, `Facade`, `Adapter`) interchangeably for the same role within one repo.

## SOLID mapping

### Single Responsibility Principle

Components, composables, stores, and services must each have one reason to change.

### Open/Closed Principle

Add behavior by extension points:

- slot content
- typed strategy maps
- composables
- store actions
- adapter implementations
- Quasar props/config

Avoid central `switch` blocks that must be edited for every new variant when a typed map is cleaner.

### Liskov Substitution Principle

If multiple components/services implement the same contract, any implementation must work where the contract is expected.

Do not create optional hidden preconditions like "works only after parent calls init" unless the contract makes that explicit.

### Interface Segregation Principle

Keep APIs role-specific:

- `UserPickerProps` should not contain unrelated user-management table settings.
- A composable should not return twenty values when callers need two.
- A facade should expose domain operations, not every SDK method.

### Dependency Inversion Principle

High-level UI depends on typed abstractions:

- injection keys
- service interfaces
- store actions
- API facades
- testable adapters

Do not scatter concrete Axios/SDK/localStorage calls through feature components.
