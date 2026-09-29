For exact version provenance and live-source authority, use [authority and API lookup](../05-authority-and-api-lookup.md); do not infer an unrecorded verification date from this split.

## 5. Framework and tool deltas

### Quasar UI 2.18 -> 2.23

- 2.18: QTable `table-row-style-fn`, `table-row-class-fn`, `grid-style-fn`, `grid-class-fn`; QMenu/QBtnDropdown `no-esc-dismiss`; `evt.qAvoidFocus`; pure-CSS icons.
- 2.19: Rolldown/lightningcss/oxlint modernisation; Baseline widely-available floor (Chrome/Edge 111+, Firefox 114+, Safari/iOS 16.4+); `date/getMinDate`/`getMaxDate` return `Date` — a behaviour change.
- 2.20: smaller and faster build; `Cookies` switched from `expires` to `Max-Age`; `QPopupProxy` no longer emits `update:modelValue` from `useAnchor()`.
- 2.21: QTable `getCellValue(colName, row)`; 2.21.1 fixed Safari page-scroll loss after a CSS-based QDialog close.
- **2.22.0 (2026-07-21) and 2.23.0-2.23.3 (2026-07-24 to 2026-07-28) are not yet read.** Their release notes are UNVERIFIED here; read them live before asserting that a component, prop, or deprecation does or does not exist in 2.22 or later, and before claiming that nothing changed.

### Quasar UI v3

Planned only (input Q3-Q4 2026; hoped Q1 2027); no beta or RC on the registry. Do not confuse it with the stable CLI `@quasar/app-vite` v3. When a user says "Quasar 3", ask which one they mean.

### Vite 8

Prebundling uses Rolldown; `optimizeDeps.esbuildOptions` is deprecated and auto-mapped to `optimizeDeps.rolldownOptions`. Oxc replaces esbuild for JS transform and minify (`build.minify: 'esbuild'` deprecated). CSS minification defaults to Lightning CSS; escape hatch `build.cssMinify: 'esbuild'`. CommonJS default-import interop is stricter; escape hatch `legacy.inconsistentCjsInterop: true`. `build.rollupOptions` -> `build.rolldownOptions` and `worker.rollupOptions` -> `worker.rolldownOptions`, old names deprecated-compatible. Object-form `manualChunks` is removed and the function form is deprecated for `codeSplitting`; the code pair is in `references/70-guardrails-a11y-performance-monorepo.md`. Default targets rose to Chrome 111 / Firefox 114 / Safari 16.4. Rolldown warns more strictly on circular imports.

### Vue Router 5

Standard 4 -> 5 is non-breaking and merges `unplugin-vue-router`. Only IIFE/CDN loses the bundled devtools API, which is irrelevant to bundled Quasar. File-routing renames: `unplugin-vue-router/vite` -> `vue-router/vite`; `unplugin-vue-router` -> `vue-router/unplugin`; data loaders -> `vue-router/experimental`. app-vite v3 supports Router 5 filename routing through `build.filenameBasedRouting`; the default programmatic `src/router/` is unaffected.

### Vue 3.5 and Workbox 7.4

Vue 3.5: SSR-stable `useId()`; scoped `data-allow-mismatch` (`text`, `children`, `class`, `style`, `attribute`); async-component lazy hydration; `useTemplateRef()`; reactive props destructure. Workbox 7.4.0/7.4.1 are maintenance and security dependency bumps plus Rollup v4, with no `InjectManifest` or `GenerateSW` behaviour change — a safe bump.
