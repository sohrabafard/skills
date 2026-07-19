# Validation checklists

Use these checklists before finalizing code changes.

## New or changed component

- Component name is multi-word and matches file name.
- Props are typed and detailed.
- Emits are typed and named by intent.
- Slots are documented or obvious.
- Template expressions are simple.
- `v-for` has stable unique keys.
- No `v-if` with `v-for` on the same element.
- No prop mutation or `$parent` access.
- Styles are scoped/module/utility-contained.
- Loading, empty, error, disabled, and success states are handled when applicable.
- Quasar components are used idiomatically.
- Accessibility is not degraded: labels, roles, keyboard behavior, focus, aria where needed.

## New or changed composable

- Name starts with `use`.
- Called synchronously from setup-compatible context.
- Returns plain object of refs/computed/functions.
- Cleans up side effects on unmount.
- Handles SSR/browser-only APIs safely.
- Does not own domain state that belongs in Pinia/service.
- Has tests or is simple enough to verify through component tests.

## New or changed Pinia store

- Unique stable store ID.
- Focused domain/feature scope.
- Typed state, computed getters, and actions.
- No component imports.
- Actions own shared mutations and side effects.
- Setup store returns all state/actions needed by app/devtools/SSR.
- Tests cover state transitions or critical actions.

## New or changed service/API/facade

- No Vue component imports.
- Accepts typed inputs and returns typed domain outputs.
- Maps DTOs at boundary.
- Converts unknown errors to app/domain errors.
- Supports cancellation/race handling when user-visible.
- Does not trigger Quasar UI feedback directly unless it is explicitly a UI facade.

## New or changed Quasar boot file

- Uses `defineBoot` if repo uses Quasar Vite boot conventions.
- Contains initialization only.
- Is client/server scoped correctly.
- Does not own feature workflows.
- Does not expose secrets or mutable SSR globals.

## Refactor/review checklist

- Public-contract inventory done before the refactor: published props/emits/slots, store public APIs, route names/paths/query params, storage keys, event names, i18n keys, SDK surfaces — all preserved or the break is explicit and approved.
- User-triggered mutations are double-fire safe (trigger disabled or request deduped while pending).
- Public behavior is preserved unless explicitly changed.
- Violations are ranked: correctness/type safety, Vue Priority A, side effects, state ownership, async/error handling, duplication, readability.
- Diff is focused and reversible.
- Old duplicated logic is removed, not left beside new abstraction.
- Tests updated for changed behavior.

## Validation commands

Inspect `package.json` first and use project scripts. Typical checks:

```bash
npm run typecheck
npm run lint
npm run test
npm run test:unit
npm run build
npx vue-tsc --noEmit
npx vitest run path/to/test.spec.ts
```

For Quasar projects, prefer repository scripts, commonly:

```bash
npm run lint
npm run test
npm run build
quasar build
```

Do not invent successful validation. Report exact commands run and outcomes.

## Failure response format for coding agents

When finalizing after tool work, include:

- Changed files.
- Key clean-code/style-guide repairs.
- Validation commands and results.
- Remaining blockers or follow-ups, if any.
