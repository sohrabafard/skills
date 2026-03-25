# Plugins, Composables, Directives, Options, and Utils

Use this file when the task names a Quasar plugin API, composable, directive, global option, or utility helper.

## Plugins

- `AppFullscreen`, `AppVisibility`, `BottomSheet`, `Dialog`, `Loading`, `Notify`, `Platform`

Also load:

- `20-ssr-pwa-and-security.md` for universal apps
- `60-guardrails-a11y-performance-monorepo.md` for focus, reduced motion, or heavy runtime work

## Composables

- `useDialogPluginComponent`, `useFormChild`, `useHydration`, `useId`, `useInterval`
- `useMeta`, `useQuasar`, `useRenderCache`, `useSplitAttrs`, `useTick`, `useTimeout`

Rules:

- `useHydration`, `useId`, `useMeta`, and `useRenderCache` are SSR-sensitive. Always pair them with `20-ssr-pwa-and-security.md`.
- Search by exact composable name before using vague phrases like "hydration helper" or "meta composable".

## Directives

- `ClosePopup`, `Intersection`, `Morph`, `Mutation`, `Ripple`, `ScrollFire`
- `TouchHold`, `TouchPan`, `TouchRepeat`, `TouchSwipe`

Rules:

- Touch directives often imply accessibility and keyboard fallback work.
- DOM-observer directives often imply cleanup and hydration parity concerns.

## Global options

- animations, app icons, internationalization, global node, icon libraries, platform detection
- icon sets, language packs, RTL support, Screen plugin, SEO, transitions, the `$q` object

Rules:

- Option-level changes almost always require `10-cli-vite-and-config.md`.
- `SEO`, `Screen`, and platform detection often also require `20-ssr-pwa-and-security.md`.

## Utils

- color, date, DOM, event bus, formatter, morph, scrolling, type checking, and other helpers

Rules:

- Date, DOM, and scrolling helpers often become SSR hazards if used in render paths.
- Formatter and color helpers can still create hydration drift if locale/timezone or environment assumptions change.

## Easy-to-miss relationships

- Many plugin issues are really component-family issues. Example: `Loading` often pairs with progress indicators and dialogs.
- `useMeta` is usually a route/data-loading concern, not only a composable concern.
- `Ripple`, touch directives, and visibility/platform plugins can become reduced-motion or accessibility questions.
