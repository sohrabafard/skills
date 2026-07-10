# API Usage Atlas

Use for Quasar plugin/composable/option/util intent, confusion points, and SSR traps—not exhaustive shapes. Query installed plugin APIs via `05-authority-and-api-lookup.md`; for composables/utils inspect installed exports/types plus version-matched official docs, not `quasar describe`.

## Playbooks

### `useMeta`

Route/component title/meta updates; use function form for reactive state and treat as SSR/SEO flow: `useMeta(() => ({ title: pageTitle.value }))`. Search: `useMeta`, `reactive meta`, `title`, `meta tags`, `SSR SEO`.

### `useHydration`

Use only when completion state is genuinely needed; fix deterministic markup first, then use `QNoSsr`/`useHydration` only for truly client-only features.

✅ Do — fix id/aria mismatches with Vue 3.5 `useId()` first. ❌ Don't — hide one unstable value by wrapping a whole subtree in `QNoSsr`; it loses that subtree's SSR/SEO.

Search: `useHydration`, `isHydrated`, `QNoSsr`, `client-only`, `useId`.

### `useDialogPluginComponent` / `useFormChild`

- `useDialogPluginComponent`: custom component mounted by Dialog plugin; prefer it to hand-rolled lifecycle. Search: `useDialogPluginComponent`, `onDialogOK`, `onDialogCancel`, `dialogRef`.
- `useFormChild`: custom control participating in `QForm`; prefer it to ad-hoc registration. Search: `useFormChild`, `QForm`, `validate`, `resetValidation`.

### `Dialog`, `Notify`, `Loading`

Use respectively for modal decisions/short blocking flows, transient feedback, and global/blocking loading. Treat `html: true` and other rich-content options as security boundaries.

```js
Notify.create({ message: userText }) // Do: escaped by default
Notify.create({ message: userText, html: true }) // Don't: unsanitized XSS sink
```

Search: `Dialog plugin`, `Notify`, `Loading`, `html true`, `sanitize`.

### `Cookies`

SSR-safe read/write (`Cookies.get`/`set`; server uses `ssrContext`). Quasar 2.20 changed expiry from `expires` to `MaxAge`; audit absolute-expiry assumptions. Search: `Cookies set`, `maxAge`, `expires`, `ssrContext cookies`, `httpOnly`.

### `Screen` / `Platform`

- Prefer CSS unless JS truly needs breakpoints; intentionally opt into costly `bodyClasses: true`. Search: `Screen`, `$q.screen`, `bodyClasses`, `setSizes`, `setDebounce`.
- Use `Platform` for capability/shell differences, not brittle UA-driven product behavior. Search: `Platform`, `is.ios`, `is.android`, `electron`, `capacitor`.

### `AppVisibility` / `AppFullscreen`

Use only when visibility/fullscreen changes behavior; treat as browser/shell-sensitive in universal apps. Search: `AppVisibility`, `AppFullscreen`, `visibilitychange`, `fullscreen`.

### `useQuasar` / `$q`

Use `useQuasar()` in setup for framework services (dark, screen, language, platform); prefer a smaller API when clearer. Search: `useQuasar`, `$q`, `screen`, `lang`, `platform`, `dark`.

### Language packs, icon sets, app icons

These are build/config choices. Check mode-specific asset pipelines; preserve repo icon-system consistency. Search: `language pack`, `icon set`, `app icons`, `RTL`, `manifest icons`.

### Animations/transitions

Treat as performance/a11y choices; respect reduced motion and do not globally add animation packages without intent. Search: `animations`, `transitions`, `reduced motion`, `global animation config`.

### `date` utils

Import/destructure only what is used; locale/timezone-sensitive SSR formatting can hydrate differently.

```js
import { date } from 'quasar'; const { formatDate } = date
```

✅ Do — keep SSR output deterministic. ❌ Don't — assume stable locale/timezone output; format after mount or deliberately use `data-allow-mismatch`.

Search: `formatDate`, `addToDate`, `extractDate`, `timezone`, `tree shaking`.

### `dom` utils

Client-only by default: use after mount and throttle per-frame reads/writes. Example: `import { dom } from 'quasar'; const { offset, height } = dom`. Search: `dom utils`, `offset`, `style`, `height`, `ready`, `mounted only`.

## Selection

SEO/meta → `useMeta`; hydration state → `useHydration` after deterministic-SSR review; custom dialog → `useDialogPluginComponent`; custom form child → `useFormChild`; breakpoint JS → `Screen`; setup services → `useQuasar`; formatting/DOM → `date`/`dom` plus SSR timing.

Also load `31-ssr-pwa-and-security.md` for SSR/hydration/meta/browser-only behavior and `21-cli-vite-and-config.md` for global options/config.
