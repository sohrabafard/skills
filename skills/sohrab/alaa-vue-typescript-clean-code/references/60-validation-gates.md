# Validation gates

Read before writing "done", "validated", "verified", or "tests pass". `SKILL.md` states the gate;
this file states what to check per artifact and which command to run. Which proof level a claim needs, and
what a test must fail on, are `78-testing-binding.md`.

## New or changed component

- Name is multi-word and matches the file name.
- Props are typed; emits are typed and named by intent; a slot whose name does not say what fills it is
  documented.
- Template expressions are simple; `v-for` has stable unique keys; no `v-if` on the same element as `v-for`.
- No prop mutation, no `$parent`.
- Styles are scoped, module-based, or utility-contained.
- Loading, empty, error, disabled, and success states are handled wherever the component can be in them.
- Accessibility is not degraded: label, role, keyboard path, focus target, and any `aria` the interaction
  needs.
- Any untrusted content the component renders goes through the rule in `72-frontend-security-binding.md`.

## New or changed composable

- Name starts with `use`; called synchronously from a setup-compatible context.
- Returns a plain object of refs, computed values, and functions.
- Every side effect it registers is cleaned up on unmount, and every exposed async surface is
  teardown-guarded per `70-async-and-failure-binding.md`.
- SSR-safe, or explicitly client-only in its name and its documentation.
- Does not own domain state that a store or service owns.
- **Ships a unit test that fails when its teardown, its error path, or its guard is removed.** Test design
  is `/alaa-testing-strategy` (`$alaa-testing-strategy`); the Vue binding is `78-testing-binding.md`.

## New or changed Pinia store

- Unique stable id; one domain or feature in scope; typed state, getters, and actions.
- No component imports.
- Actions own shared mutations and side effects.
- The setup store returns everything the app, devtools, and SSR need.
- A test covers the state transitions the change introduces, and fails if a transition is reverted.

## New or changed service, API client, or facade

- No Vue component imports.
- Typed inputs, typed domain outputs, DTO mapping at the boundary.
- Unknown errors converted to app or domain errors; cancellation supported wherever the call is
  user-visible.
- Does not trigger Quasar UI feedback unless it is explicitly a UI facade.

## New or changed boot file

- Uses the repo's boot convention (`defineBoot` where Quasar Vite conventions are in use).
- Initialization only; correctly scoped to client or server; exposes no secret and no mutable SSR global.

## Refactor and review

- The public-contract inventory in `SKILL.md` was done before the refactor, and every item is preserved or
  the break is explicit and approved.
- User-triggered mutations are double-fire safe.
- Findings are ranked: correctness and type safety, then Vue Priority A, then side effects, then state
  ownership, then async and error handling, then duplication, then readability.
- The diff is focused and reversible, and the old duplicated logic is deleted rather than left beside the
  new abstraction.

## Commands

Read `package.json` first and prefer the repository's own scripts. The typical set:

```bash
npm run typecheck        # or: npx vue-tsc --noEmit
npm run lint
npm run test
npx vitest run path/to/file.spec.ts
npm run build
```

`vue-tsc --noEmit` is the typechecker for this fleet, per the TypeScript line stated in
`24-typescript-project-and-antipatterns.md`.

**Report the exact command and the exact outcome.** If a script is absent or the runtime rejects it, report
the command and its failure text and say what was therefore not checked. An unrun check is reported as
unrun; a check that failed is reported as failed. Do not describe an expected result as an observed one.

For a change touching a published package consumed from `dist`, rebuild the package before checking the
consumer — `/alaa-mono-package` (`$alaa-mono-package`) owns that boundary.

## Reporting

The response format — what to include, what to leave out — is
`/alaa-low-noise` (`$alaa-low-noise`). This skill adds one requirement to whatever that format says: every
validation claim carries the command that produced it.
