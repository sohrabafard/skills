# Plugins, Composables, Directives, Options, and Utils

Use this file when the task names a Quasar plugin API, composable, directive, global option, or utility helper.

For exact installed component/directive/plugin API availability and option/value shapes, first follow `05-authority-and-api-lookup.md`.
For composables and utils, inspect installed `quasar` exports/type declarations plus version-matched official docs; `quasar describe` does not cover those surfaces.
For directive intent, gotchas, and minimal snippets, pair this file with `65-directive-usage-atlas.md`.
For plugin, composable, option, and util intent and SSR traps, pair this file with `66-api-usage-atlas.md`.

## Plugins

- `AppFullscreen`, `AppVisibility`, `BottomSheet`, `Dialog`, `Loading`, `Notify`, `Platform`

Also load:

- `31-ssr-pwa-and-security.md` for universal apps
- `70-guardrails-a11y-performance-monorepo.md` for focus, reduced motion, or heavy runtime work
- `66-api-usage-atlas.md` when usage intent or a common snippet shape matters

## Composables

- `useDialogPluginComponent`, `useFormChild`, `useHydration`, `useId`, `useInterval`
- `useMeta`, `useQuasar`, `useRenderCache`, `useSplitAttrs`, `useTick`, `useTimeout`

Rules:

- `useHydration`, `useId`, `useMeta`, and `useRenderCache` are SSR-sensitive. Always pair them with `31-ssr-pwa-and-security.md`.
- ✅ Do — call these composables in `setup()` / `<script setup>` top level so they bind to the right instance.
- ❌ Don't — call them inside `onMounted`, event handlers, `setTimeout`, or other async callbacks; they will not bind correctly and may break SSR parity.
- Search by exact composable name before using vague phrases like "hydration helper" or "meta composable".
- When the task is specifically about composable behavior or snippet shape, also load `66-api-usage-atlas.md`.

## Directives

- `ClosePopup`, `Intersection`, `Morph`, `Mutation`, `Ripple`, `ScrollFire`
- `TouchHold`, `TouchPan`, `TouchRepeat`, `TouchSwipe`

Rules:

- Touch directives often imply accessibility and keyboard fallback work.
- DOM-observer directives often imply cleanup and hydration parity concerns.
- When the task is specifically about a directive's behavior or snippet shape, also load `65-directive-usage-atlas.md`.

## Global options

- animations, app icons, internationalization, global node, icon libraries, platform detection
- icon sets, language packs, RTL support, Screen plugin, SEO, transitions, the `$q` object

Rules:

- Option-level changes almost always require `21-cli-vite-and-config.md`.
- `SEO`, `Screen`, and platform detection often also require `31-ssr-pwa-and-security.md`.
- When the task is specifically about `Screen`, SEO/meta wiring, icon/language packs, or `$q` usage, also load `66-api-usage-atlas.md`.

## Utils

- color, date, DOM, event bus, formatter, morph, scrolling, type checking, and other helpers

Rules:

- Date, DOM, and scrolling helpers often become SSR hazards if used in render paths.
- Formatter and color helpers can still create hydration drift if locale/timezone or environment assumptions change.
- When the task is specifically about tree-shaking, import shape, DOM access timing, or date-format determinism, also load `66-api-usage-atlas.md`.

## Easy-to-miss relationships

- Many plugin issues are really component-family issues. Example: `Loading` often pairs with progress indicators and dialogs.
- `useMeta` is usually a route/data-loading concern, not only a composable concern.
- `Ripple`, touch directives, and visibility/platform plugins can become reduced-motion or accessibility questions.
- The model usually knows what directives are, but Quasar-specific popup, touch, and observer directives are worth loading examples for because the directive value shapes and interaction semantics are easy to misremember.
- The same pattern applies to plugins, composables, options, and utils: the concept is often familiar, but the Quasar-specific shape and SSR implications are worth loading from `66-api-usage-atlas.md` when the exact API matters.
