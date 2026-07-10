# Guardrails: A11y, Performance, SSR, Monorepos

Use for cross-surface/high-regression-risk tasks. Choose the dominant bucket below, run its checks, then use failure signatures for triage. For code shapes load `22-cli-cookbook-and-examples.md`; for components/layouts `61-component-usage-atlas.md`; for directives `65-directive-usage-atlas.md`.

## Accessibility

- Overlays (`QDialog`, menus, drawers, popup proxies) must move focus in and restore it out.
- Icon-only controls need accessible names; placeholders are not labels; color alone cannot convey status/error.
- Keep keyboard operation for rows, cards, menus, carousels, virtualized lists, touch/drag interactions; prefer semantic elements to clickable `div`s.
- Preserve understandable field/error/hint relationships and stable primitive `:key`s in `v-for`.

```vue
<!-- Do: named semantic control --> <q-btn flat round icon="delete" aria-label="Delete row" @click="remove(row)" />
<!-- Don't: unnamed, keyboard-inoperable control --> <div class="cursor-pointer" @click="remove(row)"><q-icon name="delete" /></div>
```

Audit: keyboard entry/exit; predictable open/close focus; operable/discoverable virtual/custom rows; custom slots/wrappers preserve role/name; visually hidden labels remain accessible.

## Performance

1. Locate the bottleneck: server/TTFB, hydration/client execution, network/bundle waterfall, or DOM/reactivity/layout thrash.
2. Prefer route splitting/on-demand imports; keep heavy optional libraries out of global boot unless every route needs them; defer browser-only work until after SSR hydration.
3. Virtualize intentionally, then retest keyboard behavior; keep large `QVirtualScroll` arrays frozen/non-reactive when possible.
4. On weak networks audit `QImg`, `QVideo`, carousel, and upload payloads.
5. After Vite 8 upgrades, investigate optimizer/Rolldown/Oxc/minifier changes before blaming components.

### Vite 8 facts

- Prebundling: Rolldown, not esbuild. JS transform/minify: Oxc. CSS minify: Lightning CSS.
- Object `manualChunks` is removed; function form is deprecated for Rolldown `codeSplitting`.
- `build.rollupOptions` → `build.rolldownOptions` (old name temporarily deprecated-compatible).
- CommonJS default-import interop is stricter; escape hatch: `legacy.inconsistentCjsInterop: true`.
- Default targets rose (Chrome 111, Safari 16.4, etc.); set `build.target` when older browsers matter.

```js
// Do: function form (or codeSplitting).
extendViteConf (viteConf) { return { build: { rolldownOptions: { output: { manualChunks (id) {
  if (id.includes('node_modules')) return 'vendor'
} } } } } }
// Don't: removed in Vite 8.
manualChunks: { vendor: ['vue', 'quasar'] }
```

Audit: where cost occurs; accidental global/boot import; excess DOM; needless reactive arrays/payloads; media/upload/carousel bandwidth vs CPU.

## SSR/hydration

- Keep viewport-, time-, random-, and locale-unstable values out of SSR markup.
- Put browser-only side effects in client lifecycle hooks and clean them up.
- Consider stale cached HTML/assets in PWA+SSR deploys; never share per-request state through module globals.
- Invalid templates (for example implicit browser-inserted table elements) can normalize into mismatches.

| Signature | Likely cause |
| --- | --- |
| Dev-only hydration mismatch | invalid HTML, browser API, nondeterminism |
| Deploy-only mismatch | stale HTML/assets in PWA/SSR rollout |
| Second user/request only | cross-request singleton/state leakage |
| Markup correct; post-mount focus/keyboard broken | overlay lifecycle or custom interactive wrapper |

## Monorepos/packages

- Reusable libraries: peer/externalize `vue` and `quasar`; bundler-dedupe both for linked packages.
- Import CSS/assets through the build graph. Respect package entrypoints/dist-only contracts; never reach into source internals.
- Validate the host/deployment client-asset contract, especially `dist/ssr/client/assets`.
- Search imports into `packages/*/src`; verify `dist/` consumption, peers/externalization, entry CSS/assets, and final output.

```json
{ "peerDependencies": { "vue": "^3.5.0", "quasar": "^2.16.0" } }
```

Align peers with the host (`@quasar/app-vite` v3 accepts `vue-router >= 5`, `pinia ^2 || ^3`).

✅ Do — let the host own one peer/externalized Vue and Quasar. ❌ Don't — put them in reusable-package `dependencies`; duplicates cause two-Vue/dedupe failures.

```js
import './style.scss'
export { default as MyWidget } from './components/MyWidget.vue'
```

Load `22-cli-cookbook-and-examples.md` for exact dedupe/alias/bundler wiring.

## Triage map

- Missing chunk/asset 404 after package change → packaging/build graph.
- A11y regression after virtualization/custom slots → keyboard/focus customization.
- Bundle growth after small refactor → boot/global import.
- Slow route without heavy component → server data, hydration volume, or media.
- Component-looking defects may be packaging; post-upgrade performance may be Vite/Rolldown/Oxc.
- Audit content-safety in `*-html` props, `QEditor`, uploads, and user-controlled labels in custom slots.
