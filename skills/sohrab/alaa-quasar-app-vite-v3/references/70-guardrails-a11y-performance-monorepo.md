# Guardrails: accessibility, performance budgets, SSR, packages

You are about to ship a data grid, a virtualized list, an overlay, an upload, or media — or to explain a regression that appeared after a toolchain upgrade. Choose the dominant section, run its checks, then use the failure signatures to triage. Code shapes are `references/22-cli-cookbook-and-examples.md`; component intent is `references/61-component-usage-atlas.md`; directives are `references/65-directive-usage-atlas.md`.

## Accessibility

- Overlays — `QDialog`, `QMenu`, `QDrawer`, `QPopupProxy` — move focus in on open and restore it on close.
- Icon-only controls carry an accessible name. A placeholder is not a label, and colour alone never conveys status or error.
- Keyboard operation survives for rows, cards, menus, carousels, virtualized lists, and touch or drag interactions. Prefer a semantic element to a clickable `div`.
- Field, error, and hint relationships stay intact, and `v-for` keys stay stable and primitive.

```vue
<!-- Do: named semantic control --> <q-btn flat round icon="delete" aria-label="Delete row" @click="remove(row)" />
<!-- Don't: unnamed, keyboard-inoperable --> <div class="cursor-pointer" @click="remove(row)"><q-icon name="delete" /></div>
```

Audit: keyboard entry and exit; predictable focus on open and close; virtual and custom rows operable and discoverable; custom slots and wrappers preserving role and name; visually hidden labels still exposed. Broader accessibility patterns are `/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`), `references/85-accessibility-patterns.md`.

## Performance budgets

A structural choice with no stated budget is not a decision. State the number, then check it.

| Decision | Budget | What to do when it is exceeded |
| --- | --- | --- |
| Rows rendered into the DOM at once | **200** | above it, virtualize: `QVirtualScroll`, `QTable` virtual-scroll mode, or `QInfiniteScroll` with a page size that keeps the DOM under the budget |
| Rows a single request may return | the page size the endpoint declares | never render an unpaginated list of unknown length; the pagination contract is `/alaa-keyset-pagination` (`$alaa-keyset-pagination`), `references/40-wire-contract-limits-and-errors.md` |
| Reactive array bound to `QVirtualScroll` | **500 items** | above it, pass the array through `markRaw` or `Object.freeze`. If a row field is mutated in place, replace the row object instead of making the array reactive |
| `virtual-scroll-item-size` | the true minimum item height in pixels; the Quasar default is `24` | a value far from the real minimum makes scroll position jump; `virtual-scroll-slice-size` defaults to `10` and is raised only with a measured reason |
| `items-fn` | synchronous, O(1) per call | it runs during scroll; any await or per-call scan turns scrolling into a request waterfall |
| Cache lookup per navigation | scoped `caches.match(request, { cacheName })`, and every runtime cache capped by `ExpirationPlugin({ maxEntries })` | an unscoped lookup searches every cache in the origin — see `references/30-service-worker-excellence.md` §3 |
| Route chunk added by one feature | the repository's declared size budget, checked in CI | when the repository has none, state the before and after chunk sizes in the change description rather than reporting nothing |

The complexity reasoning behind these — how to find the real N, when a list becomes a map, and how to prove a bound — is `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`), `references/10-complexity-budget.md`, `references/20-finding-n.md`, `references/30-choosing-a-structure.md`. Render and asset budgets for the design system are `/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`), `references/45-render-and-asset-budgets.md`.

Order of investigation: (1) locate the bottleneck — server and TTFB, hydration and client execution, network and bundle waterfall, or DOM, reactivity, and layout thrash; (2) prefer route splitting and on-demand imports, and keep a heavy optional library out of global boot unless every route needs it; (3) defer browser-only work until after hydration; (4) virtualize deliberately, then retest keyboard behaviour; (5) on weak networks audit `QImg`, `QVideo`, carousel, and upload payloads; (6) after a Vite 8 upgrade, investigate the optimizer, Rolldown, Oxc, and the minifier before blaming a component.

### Vite 8 code shapes

```js
// Do: function form (or codeSplitting).
extendViteConf (viteConf) { return { build: { rolldownOptions: { output: { manualChunks (id) {
  if (id.includes('node_modules')) return 'vendor'
} } } } } }
// Don't: removed in Vite 8.
manualChunks: { vendor: ['vue', 'quasar'] }
```

The full Vite 8 delta list — prebundler, transform, CSS minifier, CJS interop, renamed options, raised targets — is `references/80-upstream-deltas-and-live-checks.md` §5.

## SSR and hydration

- Keep viewport-, time-, random-, and locale-unstable values out of SSR markup.
- Put browser-only side effects in client lifecycle hooks and clean them up.
- Consider stale cached HTML or assets in a PWA plus SSR rollout, and never share per-request state through a module global. The rules are `references/31-ssr-pwa-and-security.md`.
- An invalid template — for example an implicitly browser-inserted table element — normalizes into a mismatch.

| Signature | Likely cause |
| --- | --- |
| Hydration mismatch in dev only | invalid HTML, a browser API during render, or nondeterminism |
| Mismatch only after a deploy | stale HTML or assets in a PWA or SSR rollout |
| Wrong data for the second user or request only | a cross-request singleton or module-global leak |
| Markup correct, focus or keyboard broken after mount | overlay lifecycle or a custom interactive wrapper |

## Packages and the monorepo boundary

**`packages/*` is not this skill's ground.** Package entrypoints, exports maps, peer dependencies, dedupe, build output, declaration output, and whether an asset is reachable from an entry are all `/alaa-mono-package` (`$alaa-mono-package`) — `references/10-package-boundary-and-entrypoints.md`, `references/12-exports-map-and-conditions.md`, `references/20-peer-deps-dedupe-and-build-output.md`, `references/30-assets-css-and-ssr-client-assets.md`, `references/40-audit-and-verification.md`. Read the peer-dependency contract there; this file does not restate it.

What remains Quasar-specific: the host application owns one Vue and one Quasar instance, so a duplicate copy pulled in by a linked package produces two framework instances and failures that look like component bugs — a `QDialog` that will not close, a `$q` that is undefined inside a package component, an injection that resolves to nothing. When you see those symptoms in a workspace repository, check for a duplicate before debugging the component. `build.extendViteConf` returning `{ resolve: { dedupe: ['vue', 'quasar'] } }` is the Quasar-side expression of that fix; the package-side contract that prevents it is `/alaa-mono-package` (`$alaa-mono-package`).

## Triage map

- A missing chunk or asset 404 after a package change is packaging or the build graph.
- An accessibility regression after virtualization or custom slots is keyboard and focus customization.
- Bundle growth after a small refactor is a boot or global import.
- A slow route with no heavy component is server data, hydration volume, or media.
- A component-looking defect may be packaging; a post-upgrade performance change may be Vite, Rolldown, or Oxc.
- Audit content safety in `*-html` props, `QEditor`, uploads, and user-controlled labels in custom slots — the rule is `references/31-ssr-pwa-and-security.md` and the code pair is `references/66-api-usage-atlas.md`.

Search: `accessibility audit`, `focus trap`, `aria-label`, `virtualization threshold`, `markRaw`, `Object.freeze`, `virtual-scroll-item-size`, `items-fn`, `bundle budget`, `manualChunks`, `rolldownOptions`, `hydration signature`, `two Vue instances`, `dedupe`.
