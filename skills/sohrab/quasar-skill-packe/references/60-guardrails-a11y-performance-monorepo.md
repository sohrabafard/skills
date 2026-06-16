# Guardrails, Accessibility, Performance, and Monorepo Packaging

Use this file whenever the task spans multiple Quasar surfaces or has high regression risk.

This file is not a component atlas. It is a compact audit guide for the mistakes that most often slip through when a task touches SSR, interactivity, performance, packaging, or deployment contracts at the same time.

For code-shape examples, pair this file with:

- `11-cli-cookbook-and-examples.md` for Quasar config, boot, routing, and bundler wiring
- `41-component-usage-atlas.md` for component/layout usage and alternatives
- `51-directive-usage-atlas.md` for directive behavior and snippet shape

## How to use this file

1. Identify the dominant risk bucket:
   - accessibility
   - SSR and hydration
   - performance
   - packaging and deployment contract
2. Run the relevant checklist below before proposing a fix.
3. If the task is still ambiguous, treat the failure signatures section as a triage map.

## Accessibility defaults

- Ensure dialogs, menus, drawers, and popup proxies move focus in and return focus out.
- Give icon-only controls an accessible name.
- Do not rely on placeholders as labels.
- Keep keyboard support for interactive rows, cards, menus, carousels, and virtualized lists.
- Prefer semantic interactive elements over clickable `div`s.
- Do not rely on color alone to signal status or validation state.
- Touch gestures and drag-like interactions need a keyboard or non-gesture fallback.
- If validation or helper text matters, keep the relationship between field, error, and hint understandable to assistive tech.
- Maintain stable primitive `:key` values in `v-for`.

✅ Do — give an icon-only control an accessible name and a real role.

```vue
<q-btn flat round icon="delete" aria-label="Delete row" @click="remove(row)" />
```

❌ Don't — ship an icon-only or clickable-`div` control with no name and no keyboard path.

```vue
<div class="cursor-pointer" @click="remove(row)"><q-icon name="delete" /></div>
```

### Accessibility audit checklist

- Can the user reach and leave the UI surface with keyboard only?
- Does focus land somewhere predictable after opening and closing overlays?
- Are virtualized rows or custom interactive containers still discoverable and operable from keyboard?
- If the UI uses slots or custom wrappers, did we accidentally remove the accessible name or semantic role?
- If the UI hides labels visually, is the accessible name still present?

## Performance defaults

- Diagnose the primary bottleneck first:
  - server render / TTFB
  - hydration / client execution
  - network / bundle waterfall
  - DOM size / reactivity / layout thrash
- Prefer route-level code splitting and on-demand imports.
- Avoid doing heavy browser-only work before hydration in SSR apps.
- Do not move large optional libraries into boot files unless the whole app truly needs them.
- Use virtualization intentionally and verify keyboard behavior after doing so.
- For `QVirtualScroll`, keep large item arrays non-reactive or frozen when possible.
- Be careful with media-heavy surfaces such as `QImg`, `QVideo`, carousels, and uploads on weak networks.
- After upgrading to Vite 8, treat optimizer, Rolldown/Oxc, or minifier behavior changes as possible root causes instead of assuming the component regressed.

### Vite 8 build-tooling facts that bite Quasar apps

Vite 8 (bundled by app-vite v3) changed the build internals. These are the ones that actually break or surprise Quasar builds:

- Dependency pre-bundling uses **Rolldown** (not esbuild); JS transforms/minify use **Oxc**; CSS minify uses **Lightning CSS**.
- The **object form of `manualChunks` is removed**. Function form is deprecated in favor of Rolldown's `codeSplitting` option.
- `build.rollupOptions` -> `build.rolldownOptions` (old name deprecated, still works for now).
- **CommonJS default-import** interop is stricter and can break a package; escape hatch `legacy.inconsistentCjsInterop: true`.
- Default browser targets rose (Chrome 111, Safari 16.4, ...); revisit `build.target` if you must support older browsers.

✅ Do — split vendor chunks with the function form (or `codeSplitting`) under `extendViteConf`.

```js
extendViteConf (viteConf) {
  return { build: { rolldownOptions: { output: { manualChunks (id) {
    if (id.includes('node_modules')) return 'vendor'
  } } } } }
}
```

❌ Don't — use the removed object form; it silently no longer applies in Vite 8.

```js
manualChunks: { vendor: ['vue', 'quasar'] } // object form: removed in Vite 8
```

### Performance audit checklist

- Is the expensive work happening on the server, during hydration, or after interaction?
- Did a global import or boot-file change accidentally pull a heavy feature into every route?
- Are we rendering far more DOM nodes than the user can see?
- Are large arrays or payloads reactive when they do not need to be?
- Did image, upload, or carousel behavior create bandwidth pressure rather than CPU pressure?

## SSR and hydration safety defaults

- Do not let viewport-only, time-only, random-only, or locale-unstable values affect SSR-rendered markup.
- Move browser-only side effects into client-only lifecycle hooks and clean them up.
- Treat stale cached HTML as a possible hydration root cause in PWA-enabled SSR apps.
- Avoid request-crossing singletons and per-request state in module-level globals.
- Remember that browser-normalized HTML can create mismatches when the template is invalid, such as table structures that rely on implicit browser insertion.

### Hydration failure signatures

- Hydration mismatch only in development:
  - often invalid HTML, browser-only API access, or non-deterministic rendering
- Hydration mismatch only after deploy:
  - often stale HTML or stale assets under PWA/SSR rollout conditions
- Bug appears only for the second user/request on SSR:
  - often cross-request state pollution or singleton leakage
- Markup looks right but keyboard/focus behavior breaks after mount:
  - often overlay lifecycle or custom interactive wrappers, not pure hydration

## Monorepo and package defaults

Use these rules when Quasar code lives in workspaces or shared packages:

- Externalize `vue` and `quasar` as peer dependencies for reusable libraries.
- Dedupe `vue` and `quasar` at the bundler level when linked packages are involved.
- Import package CSS and assets through the normal build graph so the app bundle can see them.
- Do not reach into package source files directly if the package contract expects dist-only consumption.
- Validate the final client asset contract required by the host application or deployment platform.

### Packaging audit checklist

- Search for imports that reach into `packages/*/src` or otherwise bypass the package entrypoint.
- Check that package outputs are consumable from `dist/`, not from source internals.
- Check `peerDependencies` and bundler externalization for `vue` and `quasar`.
- Check that package entrypoints import the CSS or assets they need.
- Check the final app output for the deployment contract, especially `dist/ssr/client/assets`.

### Small packaging patterns

- Package boundary shape (align peers with the host app; app-vite v3 expects `vue-router >= 5`, `pinia ^2 || ^3`):

```json
{
  "peerDependencies": {
    "vue": "^3.5.0",
    "quasar": "^2.16.0"
  }
}
```

✅ Do — declare `vue` and `quasar` as peers and externalize them so the host owns a single copy.

❌ Don't — list `vue`/`quasar` as direct `dependencies` of a reusable package; that ships duplicate copies and triggers "two Vues" / dedupe failures when linked.

- Package entry should pull required runtime styles into the build graph:

```js
import './style.scss'

export { default as MyWidget } from './components/MyWidget.vue'
```

If you need the exact bundler/config snippet for dedupe or alias wiring, also load `11-cli-cookbook-and-examples.md`.

## Failure signatures that often fool agents

- Missing chunk or asset 404 after a package change:
  - often a packaging/build-graph problem, not a component bug
- Accessibility regression after virtualization or custom slots:
  - often a keyboard/focus problem caused by customization, not the Quasar primitive itself
- Sudden bundle growth after a "small" refactor:
  - often a boot/global import decision, not the route component
- Slow route with no obvious heavy component:
  - often server-side data work, hydration volume, or media payload, not paint alone

## Easy-to-miss relationships

- Monorepo packaging bugs often look like component bugs.
- Accessibility regressions often appear only after virtualization, dialog nesting, or custom slots.
- Performance regressions after upgrades can come from Vite, Rolldown, or Oxc behavior rather than the component itself.
- Security and content-safety concerns can hide inside convenience surfaces:
  - `*-html` props
  - `QEditor`
  - uploads
  - user-controlled labels rendered through custom slots
