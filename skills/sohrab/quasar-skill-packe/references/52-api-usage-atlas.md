# API Usage Atlas

Use this file when the task names a Quasar plugin, composable, option, or util and the agent needs more than a category list.

This file restores the high-value part of the old API micro-skills: what the API is really for, what it is often confused with, and which SSR or usage traps matter.

## High-value playbooks

### `useMeta`

- Use for route- or component-driven title/meta updates.
- Prefer a function form when the meta must react to state.
- Treat it as part of SSR/SEO flow, not just a local composable.

```js
useMeta(() => ({
  title: pageTitle.value
}))
```

- Good search terms:
  - `useMeta`, `reactive meta`, `title`, `meta tags`, `SSR SEO`

### `useHydration`

- Use when the component truly needs to know whether hydration has completed.
- Do not use it as a blanket excuse to hide unstable SSR output.
- Prefer fixing deterministic markup first; use `QNoSsr` or `useHydration` only when the feature is genuinely client-only.

- Good search terms:
  - `useHydration`, `isHydrated`, `QNoSsr`, `client-only`

### `useDialogPluginComponent`

- Use when a custom component is being mounted through the Dialog plugin.
- Prefer it over hand-rolled plumbing for dialog plugin lifecycle.

- Good search terms:
  - `useDialogPluginComponent`, `onDialogOK`, `onDialogCancel`, `dialogRef`

### `useFormChild`

- Use when a custom field/control should participate in `QForm` validation.
- Prefer it over inventing ad-hoc validation registration.

- Good search terms:
  - `useFormChild`, `QForm`, `validate`, `resetValidation`

### `Dialog`, `Notify`, and `Loading`

- `Dialog` is for modal decisions or short blocking flows.
- `Notify` is for transient feedback.
- `Loading` is for blocking or global loading state.
- Treat `html: true` and similar content-rich options as security boundaries; sanitize untrusted content.

- Good search terms:
  - `Dialog plugin`, `Notify`, `Loading`, `html true`, `sanitize`

### `Screen`

- Prefer responsive CSS when that is enough.
- Use `Screen` or `$q.screen` when JavaScript logic truly depends on breakpoint state.
- Remember that `bodyClasses: true` has a cost and should be enabled intentionally.

- Good search terms:
  - `Screen`, `$q.screen`, `bodyClasses`, `setSizes`, `setDebounce`

### `Platform`

- Use for platform capability differences or shell-specific branching.
- Do not overfit product behavior to brittle user-agent assumptions.

- Good search terms:
  - `Platform`, `is.ios`, `is.android`, `electron`, `capacitor`

### `AppVisibility` and `AppFullscreen`

- Use them only when visibility or fullscreen state actually affects behavior.
- Treat them as browser- or shell-sensitive APIs in universal apps.

- Good search terms:
  - `AppVisibility`, `AppFullscreen`, `visibilitychange`, `fullscreen`

### `useQuasar` and `$q`

- Use `useQuasar()` inside setup when you need access to framework services such as dark mode, screen, language, or platform.
- Do not reach for `$q` where a smaller API would be clearer.

- Good search terms:
  - `useQuasar`, `$q`, `screen`, `lang`, `platform`, `dark`

### Language packs, icon sets, and app icons

- Treat language packs, icon sets, and app icons as build/config choices, not random UI tweaks.
- Check mode-specific asset pipelines when app icons or manifests are involved.
- Prefer repo consistency over mixing icon systems casually.

- Good search terms:
  - `language pack`, `icon set`, `app icons`, `RTL`, `manifest icons`

### Animations and transitions

- Treat them as a performance and accessibility choice, not only styling.
- Respect reduced-motion expectations and avoid adding animation packages globally without intent.

- Good search terms:
  - `animations`, `transitions`, `reduced motion`, `global animation config`

### `date` utils

- Prefer tree-shaken imports or destructuring to avoid pulling in more than you need.
- Treat locale/timezone-sensitive formatting in SSR as a potential hydration risk.

```js
import { date } from 'quasar'

const { formatDate } = date
```

- Good search terms:
  - `formatDate`, `addToDate`, `extractDate`, `timezone`, `tree shaking`

### `dom` utils

- Treat DOM utils as client-only by default.
- Use them after mount and avoid per-frame reads/writes without throttling.

```js
import { dom } from 'quasar'

const { offset, height } = dom
```

- Good search terms:
  - `dom utils`, `offset`, `style`, `height`, `ready`, `mounted only`

## Selection heuristics

- SEO/meta:
  - start with `useMeta`
- SSR hydration state:
  - start with `useHydration`, but verify that the real fix is not deterministic SSR
- Custom dialog component:
  - start with `useDialogPluginComponent`
- Custom `QForm` child:
  - start with `useFormChild`
- Breakpoint-driven JS:
  - start with `Screen`
- Framework service access in setup:
  - start with `useQuasar`
- Formatting or DOM helpers:
  - start with `date` or `dom`, then check SSR timing

## Notes

- Pair this file with `20-ssr-pwa-and-security.md` whenever the API can affect SSR, hydration, meta timing, or browser-only behavior.
- Pair this file with `10-cli-vite-and-config.md` when the API question is actually a global option or config question.
