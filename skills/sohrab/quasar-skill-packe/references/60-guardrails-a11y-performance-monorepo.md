# Guardrails, Accessibility, Performance, and Monorepo Packaging

Use this file whenever the task spans multiple Quasar surfaces or has high regression risk.

## Accessibility defaults

- Ensure dialogs, menus, and drawers move focus in and return focus out.
- Give icon-only controls an accessible name.
- Do not rely on placeholders as labels.
- Keep keyboard support for interactive rows, cards, menus, and virtualized lists.
- Maintain stable primitive `:key` values in `v-for`.
- Prefer semantic interactive elements over clickable `div`s.

## Performance defaults

- Prefer route-level code splitting and on-demand imports.
- Avoid doing heavy browser-only work before hydration in SSR apps.
- Use virtualization intentionally and verify keyboard behavior after doing so.
- Be careful with media-heavy surfaces such as `QImg`, `QVideo`, carousels, and uploads on weak networks.
- After upgrading to Vite 8, treat optimizer and minifier behavior changes as possible root causes.

## SSR and hydration safety defaults

- Do not let viewport-only, time-only, or random-only values affect SSR-rendered markup.
- Move browser-only side effects into client-only lifecycle hooks and clean them up.
- Treat stale cached HTML as a possible hydration root cause in PWA-enabled SSR apps.

## Monorepo and package defaults

Use these rules when Quasar code lives in workspaces or shared packages:

- Externalize `vue` and `quasar` as peer dependencies for reusable libraries.
- Dedupe `vue` and `quasar` at the bundler level when linked packages are involved.
- Import package CSS and assets through the normal build graph so the app bundle can see them.
- Do not reach into package source files directly if the package contract expects dist-only consumption.
- Validate the final client asset contract required by the host application or deployment platform.

## Easy-to-miss relationships

- Monorepo packaging bugs often look like component bugs.
- Accessibility regressions often appear only after virtualization, dialog nesting, or custom slots.
- Performance regressions after upgrades can come from Vite/Rolldown/Oxc changes rather than the component itself.
