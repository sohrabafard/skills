---
name: alaa-vue-typescript-clean-code
description: Mandatory Vue 3, Quasar, Vite, and TypeScript clean-code baseline for writing, reviewing, and refactoring frontend code with enforced Vue style-guide rules, Composition API, strict typing, SOLID, separation of concerns, composables, Pinia, design patterns, and validation gates. Use before changing Vue/Quasar/TypeScript code, creating components/composables/stores/boot files, or cleaning duplicated, weakly typed, monolithic, or hard-to-maintain frontend code.
---

# Alaa Vue TypeScript Clean Code

## Purpose

Use this skill to make Vue 3 + Quasar + Vite + TypeScript code production-grade, maintainable, readable, testable, and consistent with the official Vue style guide. The skill is mandatory quality control, not optional advice: repair violations inside the task scope or clearly mark them as blockers when they cannot be repaired safely.

## Cross-agent portability

This skill uses the core Agent Skills format so both OpenAI Codex/GPT-5.5 agents and Claude Opus/Claude Code agents can load it. Keep `SKILL.md` frontmatter limited to `name` and `description`; `agents/openai.yaml` is optional Codex UI metadata and should be ignored by other compatible agents. Do not add Claude-only frontmatter such as `context`, `model`, or hooks unless the skill is intentionally forked for Claude only.

For both model families, treat this skill as an enforced coding contract. Prefer outcome-first execution, small focused edits, repository evidence, and honest validation over process-heavy narration.

## When to use

Use this skill before any task that writes, reviews, or refactors:

- `.vue`, `.ts`, `.tsx`, `quasar.config.*`, `vite.config.*`, `src/boot/*`, `src/stores/*`, `src/router/*`, composables, services, API clients, or component libraries.
- Vue/Quasar form flows, dialogs, tables, routing, Pinia stores, boot files, SSR/PWA code, async API flows, browser API wrappers, or shared UI abstractions.
- Code described as clean code, SOLID, design patterns, best practices, technical debt, maintainability, duplication, type safety, or style-guide compliance.

## When NOT to use

Do not use this skill for:

- Backend-only work unless it changes frontend contracts consumed by Vue/Quasar code.
- Generic documentation, product planning, UI copy, or design-only tasks that do not create, review, or refactor Vue/Quasar/Vite/TypeScript code.
- Database, infrastructure, CI/CD, deployment, or API-server-only changes with no frontend contract, state, routing, component, or type-safety impact.

## Source priority

Follow sources in this order:

1. Repository-local instructions: `AGENTS.md`, `CLAUDE.md`, package scripts, ESLint/Prettier, tsconfig, Quasar/Vite config, existing architecture, design system, tests.
2. Current official docs for Vue, Quasar, Vite, Pinia, Vue Router, Vitest, Vue Test Utils, and TypeScript when behavior is version-sensitive.
3. This skill and its references.
4. The PDF-derived principles and patterns in `references/30-clean-code-solid-vue.md` and `references/40-patterns-vue-quasar.md`.

If sources conflict, preserve working repo conventions unless they violate correctness, safety, Vue Priority A rules, TypeScript soundness, or explicit user requirements.

## Required reference loading

Load only what the task needs:

- Start from `references/05-topic-map.md`: the task → shortest-reading-path table. Match the task to its row and load only the listed files; the bullets below are the per-file detail.
- Always skim `references/00-source-map.md` for source scope.
- For component/template/style work, read `references/10-vue-style-contract.md`.
- For TypeScript or Composition API work, read `references/20-typescript-composition-contract.md`.
- For clean-code/SOLID refactors, read `references/30-clean-code-solid-vue.md`.
- For pattern selection or architecture changes, read `references/40-patterns-vue-quasar.md`.
- ALWAYS, before writing or reviewing view mappers, flow composables, stores, SDK adapters, or design-system
  components in an Alaa-style repo, read `references/65-alaa-observed-patterns.md` — the project-proven
  mandatory patterns (PRVM field resolution, no shadow adapters, orchestrator splits, navigation intents,
  presence-detection merges, failure classification, route sync, teardown guards) with explicit do/don't
  examples. Each antipattern there has already shipped broken once; repeating one is a blocking finding.
- For Quasar, Vite, Pinia, router, SSR, PWA, or boot files, read `references/50-quasar-vite-pinia-contract.md`.
- Before finalizing code changes, read `references/60-validation-checklists.md`.

## Mandatory operating model

Start by inspecting the repository shape before changing code: `package.json`, `tsconfig*`, `eslint*`, `prettier*`, `quasar.config.*`, `vite.config.*`, `src/`, component patterns, stores, composables, services, boot files, and tests relevant to the task.

Classify the task as one of these modes:

- **New feature slice**: design component boundaries, data flow, state ownership, validation, errors, loading, empty states, and tests before coding.
- **Local refactor**: preserve public behavior, improve structure/type safety, and keep the diff focused.
- **Review**: report violations by severity and give concrete repairs.
- **Repo-wide normalization**: require explicit permission before broad rewrites; otherwise propose a staged plan.

Before any refactor beyond a single local slice, inventory the public contracts the change can touch, and preserve them unless the task explicitly allows a break: published component props/emits/slots (especially design-system packages consumed from `dist`), store public state/getters/actions used across features, route names/paths/query params, storage and cache keys, emitted event names, i18n keys, and SDK adapter surfaces. A contract change smuggled into a "cleanup" is a blocking finding.

For every change, enforce these invariants:

- Component APIs are explicit: typed props, typed emits, documented slots where non-obvious, and no hidden parent coupling.
- State has one owner. UI components do not secretly own domain state that belongs in a store, composable, or service.
- Side effects are isolated and cleaned up. Event listeners, timers, observers, subscriptions, object URLs, pending requests, and watchers are disposed.
- Async flows expose loading, error, success, cancellation, and race behavior when user-visible.
- User-triggered mutations are double-fire safe: the trigger is disabled or the request deduped while in flight, and an idempotency key is passed when the backend supports one. A double-clicked submit must never create two records.
- TypeScript is strict and useful. Avoid `any`; use `unknown` only with narrowing; do not silence errors with casts unless the boundary is proven and localized.
- Accessibility and UX states are part of the implementation, not optional polish.
- Validation runs before final response when tools allow it.

## Vue style-guide enforcement

Treat Vue Priority A rules as hard failures inside touched code:

- Multi-word component names except root `App`.
- Detailed prop definitions with types, defaults, and validators where needed.
- Stable unique `:key` for every `v-for`; never rely on unstable indexes when order can change.
- Never put `v-if` and `v-for` on the same element; filter with computed data or move the condition to a wrapper.
- Scoped, CSS-module, utility-class, or BEM-style containment for component-specific styles.

Treat Priority B/C as the default contract unless the repository has a consistent stronger convention:

- One component per file when a build system is present.
- Consistent file casing; prefer `PascalCase.vue` for SFCs unless the repo standard is kebab-case.
- Base/presentational components are prefixed consistently, such as `Base`, `App`, or `V`.
- Tightly coupled children are prefixed with the parent name.
- Component names are full words, PascalCase in imports and SFC templates.
- Props are camelCase in declarations and preferably kebab-case in DOM templates when applicable.
- Multi-attribute elements use one attribute per line.
- Templates contain simple expressions; move logic to computed values or functions.
- Computed values are simple, named, and composable.
- Directive shorthands are consistent.
- SFC block order is consistent; prefer `<script setup lang="ts">`, `<template>`, `<style scoped>` unless the repo standard differs. Style blocks stay last.

Use Priority D patterns cautiously:

- Prefer props/events, typed provide/inject, or Pinia over `$parent`, prop mutation, or implicit component tree coupling.
- Avoid element selectors in scoped CSS when class selectors are clearer and less fragile.
- Do not use global components for feature-specific components; reserve them for true base components or plugin surfaces.

## TypeScript and Composition API rules

Default to `<script setup lang="ts">` for new SFCs.

Use type-only contracts:

- Prefer `defineProps<Props>()`, `withDefaults(defineProps<Props>(), defaults)`, typed `defineEmits`, typed `defineSlots`, and `defineModel<T>()` only when the installed Vue version supports it.
- Do not mix runtime and type-based prop declarations in the same component.
- Default arrays/objects through factories when required by the chosen syntax.
- Use `import type`, `Readonly`, discriminated unions, `as const`, `satisfies`, and finite state types for domain states.
- Type `ref<T>()`, `computed<T>()`, and function return values when inference is weak.
- Avoid `reactive<T>()` generics; let Vue infer from the object or use typed refs/computed values.
- Do not destructure reactive objects unless using safe patterns such as `toRefs`, Vue-supported reactive prop destructure, or plain immutable snapshots.

Composables must:

- Be named `useX`, be synchronous when called from setup, and return a plain object of refs/computed/functions.
- Accept refs/getters/plain values when useful and normalize with `toValue` when supported.
- Own UI interaction/stateful logic, not domain persistence that belongs in a store/service.
- Register side effects in lifecycle-safe locations and clean them on unmount.
- Be SSR-safe unless explicitly client-only.

## Clean-code and SOLID enforcement

Apply these as coding gates:

- **Separation of concerns**: Vue components render and coordinate UI; composables encapsulate reusable UI/stateful logic; Pinia owns shared app state; services own API/browser/SDK logic; validators own validation; formatters own formatting.
- **Composition over inheritance**: prefer composables, slots, renderless components, Quasar components, adapters, and small services over mixins or inheritance-style base components.
- **Single responsibility**: every component, composable, store, service, and function has one reason to change.
- **Encapsulation**: expose small typed APIs and hide implementation details.
- **KIC**: clean up resources and keep code physically organized.
- **DRY**: extract duplicated behavior after the abstraction is stable; do not create vague utilities for accidental similarity.
- **Boundary naming alignment**: one canonical domain term per concept across its whole artifact family — DTO, mapper, service, store, composable, component, and test center on the same word (`CourseDto` → `mapCourseDtoToCourse` → `useCourseFilters` → `CourseTable` → `course.store.ts`). Do not let synonyms drift across layers, and do not create vague buckets named `utils`, `common`, `helper`, or `manager`.
- **KISS**: choose the simplest design that handles the real requirements and edge cases.
- **Code for the next developer**: names, data flow, and tests must make intent obvious.

### Size and complexity budgets (hard gates, not advice)

Qualitative SRP guidance is not enough; enforce these numbers on every file you create or materially change
(repo-local rules may set stricter numbers — they win):

- A composable, store, service, or util `.ts`/`.js` file: **≤ 400 lines**.
- An SFC (`.vue`): **≤ 300 lines** of template + script combined.
- One exported primary unit per file (its own types and private helpers ride along; unrelated exports do not).
- A single function: **≤ 60 lines**. A `useX` composable's returned surface stays cohesive around ONE
  responsibility — if one composable returns filters AND transport verbs AND drafts AND lifecycle sync, it is at
  least three composables plus one thin orchestrator, not one file.

When a budget is crossed, split BEFORE declaring the work done, along these standard seams:

- pure policy/classification/formatting → standalone pure modules (no Vue imports; trivially unit-testable)
- view/filter/selection state → one focused `useX`
- drafts/dialog/detail state → one focused `useX`
- transport/side-effect verbs → one focused `useX` that receives the state composables' narrow surfaces
- one thin orchestrator composable that composes the above and exposes the page's stable public surface

Deliberate data registries (mock rows, static option tables) are the standing exception — data rows are not logic.
Files already over budget before your change: never silently grow them; bring the touched responsibility under
budget or record explicitly why not.

SOLID mapping for Vue:

- SRP: split UI, state, API, validation, mapping, and formatting.
- OCP: extend with slots, props, strategy maps, composables, and typed adapters; do not edit central switch logic for every new variant.
- LSP: components/services with the same contract must be substitutable without hidden preconditions.
- ISP: keep props/emits/composable return APIs small and role-specific.
- DIP: high-level UI depends on typed ports/interfaces, injection keys, stores, or facades, not concrete SDK calls scattered through components.

## Design pattern selection

Use patterns deliberately and name them in code comments only when it clarifies architecture. Before
picking one, run the symptom → pattern diagnostic at the top of `references/40-patterns-vue-quasar.md`;
choosing by symptom (what hurts) beats choosing by name.

- **Singleton**: module-level service, API client, event gateway, or worker manager. Do not hide mutable per-user state in SSR-capable singletons.
- **Dependency injection**: typed injection keys for plugins, replaceable services, deeply nested context, or test seams. Prefer `Symbol` keys.
- **Observer**: props/emits for parent-child, Pinia for shared data, event bus only for cross-cutting notifications. Always unsubscribe.
- **Command**: undo/redo, queues, worker messages, background jobs, bulk actions, typed action intents. Use discriminated unions and handler maps.
- **Proxy**: adapters around browser APIs, SDKs, API clients, or reactivity boundaries. Avoid clever `Proxy` magic for ordinary state.
- **Decorator**: wrappers/composables/components that add behavior while preserving the target API.
- **Facade**: simple typed API over complex APIs: Quasar plugins, Axios, IndexedDB, upload SDKs, workers, auth, notifications.
- **Callbacks**: allowed for DOM events, library interop, and hooks; typed, cancellable where needed, and cleaned up.
- **Promises**: default async abstraction; use `async/await`, `try/catch`, `finally`, abort/race handling, and no floating promises.
- **Factory/Strategy/Adapter**: use for variant creation, replaceable behavior, and external integration boundaries.
- **State (FSM)**: explicit UI/domain state transitions modeled as discriminated unions; impossible transitions rejected.
- **Builder**: fluent construction only for genuinely multi-step, conditional configuration (table column sets, form schemas); plain typed literals with `satisfies` first.
- **Composite**: recursive component trees (menus, nested comments, tree views) with one typed node contract for leaf and group; guard depth and keys.
- **Iterator**: prefer array methods and typed collections; generators only for real lazy/streaming traversal; pair unbounded lists with pagination/virtual scrolling.
- **Template Method**: renderless components and slots as the skeleton with caller-supplied steps; composition over inheritance, never base-class hierarchies.
- **Chain of Responsibility**: HTTP interceptor chains, router guard sequences, validation chains — ordered, explicit, each handler passes or short-circuits deliberately; chain-end behavior defined.
- **Pipeline**: ordered pure stages that all run, transforming one typed payload (DTO normalization, submit preparation); distinct from CoR because no stage short-circuits on "handled".
- **Mediator**: host page or orchestrator composable coordinates mediator-blind children (props-in/events-out); never a web of siblings knowing each other.
- **Memento**: owner-built immutable snapshots for undo/draft-restore/rollback; bounded history, `toRaw` before cloning.
- **Abstract Factory / Prototype / Bridge / Flyweight / Visitor**: see the catalog — provider suites chosen once; frozen preset registries; two-axis splits; shared immutable config (measured need only); per-operation handler maps over stable unions.

## Quasar, Vite, Pinia, router, SSR, and PWA rules

- Use Quasar components and plugins idiomatically; do not wrap them unless adding a stable design-system API.
- Use `useQuasar()` inside setup for Quasar plugins; configure app-wide plugins through `quasar.config.*` and boot files.
- Boot files initialize app-level dependencies only. Do not put feature business logic in boot files.
- Guard browser-only APIs (`window`, `document`, `localStorage`, `navigator`, `ResizeObserver`, service workers) for SSR and call them in `onMounted` or client-only boot files.
- Use Pinia for shared mutable state. Stores have unique IDs, focused scope, typed state/getters/actions, and return all state in setup stores.
- Declare per-route auth/permission posture in route `meta`; guards read the meta. Scattered per-component auth checks are a review failure.
- Never render unbounded lists: server-side pagination or `QVirtualScroll`/virtualized rendering for large datasets.
- Never issue one request per rendered item. A fetch, permission check, or store read inside a `v-for` or a `map` over a list whose length is not a constant is the same defect as an N+1 query; `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) owns the resolution and the bound on that list, and this skill owns the composable and component shape the resolution lands on.
- Use route-level lazy loading and dynamic imports for heavy optional components.
- Keep Vite aliases, env variables, and build configuration typed and minimal.
- PWA/service-worker behavior must be cache-safe, version-aware, and validated in browser/devtools when touched.

## To do / Not to do

Do:

- Slice UIs into layout, smart/coordinator, presentational, form/control, and base components.
- Keep domain logic out of templates.
- Create typed mappers between API DTOs and UI/domain models.
- Represent async and form state explicitly.
- Keep Quasar markup readable; extract repeated table/form/dialog configuration.
- Add or update tests around changed behavior.
- Leave the touched area cleaner than found.

Do not:

- Create mammoth components that fetch data, mutate stores, validate forms, render complex UI, and call SDKs at once.
- Mutate props, use `$parent`, rely on component tree luck, or use event buses for domain state.
- Add `any`, broad casts, disabled lint rules, or `// @ts-ignore` without a localized proof and reason.
- Duplicate API calls, mapping logic, validation rules, magic strings, status constants, or Quasar option lists.
- Use mixins for new code.
- Introduce global CSS or global components for feature-local concerns.
- Swallow promise errors, ignore abort/race behavior, or leave subscriptions alive.
- Commit, push, deploy, delete broad files, or run destructive commands without explicit permission.

## Validation and completion

Before final response, run the most relevant available checks:

- Type check: `npm run typecheck`, `vue-tsc --noEmit`, or project equivalent.
- Lint/format: `npm run lint`, `npm run format:check`, or project equivalent.
- Tests: targeted Vitest/Vue Test Utils/E2E tests for changed behavior.
- Build/smoke: `npm run build`, Quasar build/dev smoke, or the cheapest safe check.

If a check cannot run, state the exact reason and the next best verification. Do not claim validation passed unless it actually ran.

## Stop rules

Ask one narrow question and stop only when missing information would materially change public API, architecture, data ownership, side effects, destructive operations, security/privacy constraints, or validation expectations.

If the requested change conflicts with these rules, implement the safest compliant version and call out the conflict. If compliance requires a larger refactor outside scope, mark the out-of-scope repair as a blocker or follow-up with file-level evidence.
