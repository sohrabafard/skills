# Plugins, Composables, Directives, Options, and Utils

You are using a Quasar plugin, composable, directive, global option, or util and do not know which file covers it. This table indexes those surfaces; skill-level routing is `references/00-topic-map.md`. For installed component/directive/plugin shapes, first use `05-authority-and-api-lookup.md`; for composables/utils inspect installed `quasar` exports/types plus version-matched official docs (`quasar describe` does not cover them). Load `65-directive-usage-atlas.md` for directive intent/snippets and `66-api-usage-atlas.md` for plugin/composable/option/util intent and SSR traps.

| Surface | Exact coverage | Rules/routes |
| --- | --- | --- |
| Plugins | `AppFullscreen`, `AppVisibility`, `BottomSheet`, `Dialog`, `Loading`, `Notify`, `Platform` | Load `31-ssr-pwa-and-security.md` for universal apps, `70-guardrails-a11y-performance-monorepo.md` for focus/motion/heavy work, `66` for intent/snippets. Plugin failures may really be component-family failures (`Loading` often pairs with progress/dialogs). |
| Composables | `useDialogPluginComponent`, `useFormChild`, `useHydration`, `useId`, `useInterval`, `useMeta`, `useQuasar`, `useRenderCache`, `useSplitAttrs`, `useTick`, `useTimeout` | Search exact name; load `31` for SSR-sensitive `useHydration`/`useId`/`useMeta`/`useRenderCache`; load `66` for behavior/snippets. `useMeta` is commonly route/data-flow work. |
| Directives | `ClosePopup`, `Intersection`, `Morph`, `Mutation`, `Ripple`, `ScrollFire`, `TouchHold`, `TouchPan`, `TouchRepeat`, `TouchSwipe` | Touch requires keyboard/a11y fallback; observers require cleanup/hydration parity; load `65` for behavior/value shapes. |
| Global options | animations, app icons, internationalization, global node, icon libraries, platform detection, icon sets, language packs, RTL, `Screen`, `SEO`, transitions, `$q` | Always load `21-cli-vite-and-config.md`; also `31` for `SEO`/`Screen`/platform and `66` for `Screen`, SEO/meta, icons/languages, `$q`. |
| Utils | color, date, DOM, event bus, formatter, morph, scrolling, type checking, other helpers | Date/DOM/scrolling can break SSR render paths; locale/timezone/environment can drift formatter/color output. Load `66` for tree-shaking, imports, DOM timing, or deterministic dates. |

✅ Do — call composables at `setup()` / `<script setup>` top level so they bind to the component instance.

❌ Don't — call them in `onMounted`, event handlers, `setTimeout`, or async callbacks; binding and SSR parity may break.

`Ripple`, touch directives, and visibility/platform plugins can also be reduced-motion/a11y work. Quasar-specific directive/plugin/composable/option/util shapes are easy to misremember; load the relevant atlas whenever exact behavior matters.
