# Component usage atlas

You are choosing between two Quasar components, or a component is behaving unexpectedly. Curated intent, alternatives, gotchas, and search vocabulary; not an API specification. Search the exact component, then use `05-authority-and-api-lookup.md` for installed props/events/slots/methods/values/defaults. Pair with `60-components-and-layouts.md` (routing), `70-guardrails-a11y-performance-monorepo.md` (a11y/performance), and `31-ssr-pwa-and-security.md` (SSR/PWA/hydration).

## High-value playbooks

### `QTable`

Use for interactive sorting/filtering/selection/pagination/sticky/grid tables; use `QMarkupTable` for static markup or `QVirtualScroll` table mode for DOM/scroll cost. Set a stable primitive `row-key`; declare `columns` for sorting, slots, or visibility; treat server pagination as data flow, and take the cursor, limit, and error contract from `/alaa-keyset-pagination` (`$alaa-keyset-pagination`), `references/40-wire-contract-limits-and-errors.md`; consider grid mode on mobile.

```vue
<!-- Do: stable key + explicit columns. Don't: object/index key; selection and updates break. -->
<q-table :rows="rows" :columns="columns" row-key="id" />
```

Search: `row-key`, `columns`, `visible-columns`, `selection`, `server-side pagination`, `sticky header`, `sticky column`, `grid mode`, `virtual-scroll`.

### `QDialog`

Use for focus-taking modal flows, short forms, or confirmations. Prefer the Dialog plugin for programmatic/reused dialogs; use `QMenu`/`QPopupProxy`/`QTooltip` for lighter interactions. Prefer `QCard` as the child (otherwise wrap content in `div`); `position` is independent of `transition-show`/`transition-hide`; `persistent`, `seamless`, and `maximized` change behavior; a containerized `QLayout` needs explicit width/height.

Search: `persistent`, `seamless`, `maximized`, `position`, `transition-show`, `transition-hide`, `backdrop-filter`, `Dialog plugin`.

### `QSelect`

Use for option selection/filtering/custom rendering; use `QInput` for free text or `QOptionGroup` for visible inline choices. Multiple models must be arrays; `emit-value`/`map-options` control model shape; `use-input` makes autocomplete-like UI; mobile `behavior` may need dialog mode on iOS; `options-cover` disables transitions.

```vue
<!-- Do: ids in the model, labels in UI. Don't: bind a scalar with multiple or omit map-options unintentionally. -->
<q-select v-model="userId" :options="users" option-value="id" option-label="name" emit-value map-options />
```

Search: `emit-value`, `map-options`, `use-input`, `behavior`, `clearable`, `multiple`, `display-value`, `options-cover`, `new-value-mode`.

### `QImg`

Use for responsive images, loading states, ratio, placeholders, fit, captions, and native lazy loading. For player-driven video — adaptive bitrate, subtitles, DRM, offline download — use `/alaa-shaka-player` (`$alaa-shaka-player`), `references/11-vue-quasar-binding.md`, not `QVideo`. QImg: use raw `img` when those ergonomics add nothing. `fit`/`position` map to object-fit/object-position; `srcset`/`sizes` remain native; placeholders help large media; when disabling native context menus, preserve slot pointer events. Load `63-image-delivery-and-placeholders.md` for deterministic delivery/shared placeholders/SSR-safe candidates.

Search: `ratio`, `placeholder-src`, `fit`, `position`, `srcset`, `sizes`, `loading="lazy"`, `context menu`.

### `QFile` vs `QUploader`

- `QFile`: picking only; it is a native input and cannot be truly prefilled by script. A model display does not mean the native input holds those files.
- `QUploader`: queue, transport customization, drag/drop, lifecycle. It needs a backend; validate the native `accept`; resumable tus transport and resume matching are `/tusd-upload-platform` (`$tusd-upload-platform`); key hooks are `headers`, `form-fields`, `with-credentials`, `factory`; `batch` changes multi-file transport; custom header/list slots often need `QUploaderAddTrigger`.

✅ Do — use `QUploader` plus `factory`/`headers` for managed authenticated uploads.

❌ Don't — programmatically preselect a `QFile`; browsers forbid prefilling native file inputs.

Search: `accept`, `headers`, `form-fields`, `factory`, `with-credentials`, `batch`, `QUploaderAddTrigger`, `filter`.

### `QVirtualScroll` vs `QInfiniteScroll`

Virtualize when an already-loaded list is expensive to render; use infinite scroll for incremental loading. For `QVirtualScroll`, tune `virtual-scroll-item-size`/`virtual-scroll-slice-size`; ensure custom `scroll-target` exists and scrolls; keep `items-fn` synchronous. The row, reactivity, and item-size budgets are stated in `references/70-guardrails-a11y-performance-monorepo.md`: virtualize above 200 rendered rows, and pass an array above 500 items through `markRaw` or `Object.freeze` unless a row field is mutated in place — in which case replace the row object rather than making the array reactive.

Search: `virtual-scroll-item-size`, `slice-size`, `scroll-target`, `items-fn`, `q-virtual-scroll--with-prev`, `q-virtual-scroll--skip`.

### `QLayout`, `QDrawer`, `QPage`, `QPageSticky`, `QPageScroller`

Use for app shells and route pages. Layout and page ownership is stated once, in `references/62-layout-patterns-and-examples.md`. `view` controls fixed/revealed header/footer/drawer behavior. Drawer overlay/mini/mobile behavior changes navigation and focus; sticky/scroller affordances require responsive/a11y review. Layout bugs may instead be router, SSR-state, or container assumptions. Load `62-layout-patterns-and-examples.md` for `view`, containerization, overlay/fixed, and nested routes.

```vue
<q-layout view="lHh Lpr lFf">
  <q-header><q-toolbar><q-btn icon="menu" @click="leftDrawerOpen = !leftDrawerOpen" /></q-toolbar></q-header>
  <q-drawer v-model="leftDrawerOpen" show-if-above bordered><!-- navigation --></q-drawer>
  <q-page-container><router-view /></q-page-container>
</q-layout>
<!-- page file --> <q-page padding><!-- content --></q-page>
```

Search: `view`, `QPageContainer`, `router-view`, `containerized layout`, `drawer breakpoint`, `overlay`, `mini mode`, `page sticky`, `page scroller`, `routing with layouts`.

### `QTabs` and `QTabPanels`

Use for a small set of exclusive views; use routing when the URL should own durable navigation state. Search: `keep-alive`, `animated`, `vertical`, `mobile scroll`, `route tabs`.

### `QMenu`, `QPopupProxy`, `QPopupEdit`, `QTooltip`

Use `QMenu` for contextual actions, `QPopupProxy`/`QPopupEdit` for anchored popover/inline editing, and `QTooltip` only for optional lightweight hints. `QPopupProxy` responsively switches `QMenu`/`QDialog`; search `breakpoint` when its small-screen default is wrong. `QDate`, `QTime`, `QColor`, and `QCarousel` get special popup behavior unless wrapped in `div`.

Search: `anchor`, `self`, `cover`, `persistent`, `focus`, `keyboard`, `inline edit`, `breakpoint`, `context menu`, `pass-through props`.

### `QInput`, `QField`, `QForm`, `QOptionGroup`

Use `QField` around custom controls, `QInput` for free text, `QForm` for coordinated validation/submission, and `QOptionGroup` for visible grouped choices. Never wrap `QInput`/`QFile`/`QSelect` in `QField` (they inherit it). For a custom labeled `QField`, search `stack-label`. Submit controls in `before`/`after`/`prepend`/`append` slots need explicit `@click` because clicks do not bubble as expected.

```vue
<!-- Do: QForm owns submit and rules. Don't: double-wrap inherited QField controls. -->
<q-form @submit.prevent="onSubmit"><q-input v-model="email" :rules="[v => !!v || 'Required']" /><q-btn type="submit" label="Save" /></q-form>
```

Search: `rules`, `lazy-rules`, `debounce`, `mask`, `submit slot click`, `option group`, `stack-label`, `useFormChild`.

### `QDate`, `QTime`, `QColor`, `QSlider`, `QRange`, `QKnob`

Use for structured value picking; verify model/format assumptions in SSR/localized apps. Search: `range`, `with-seconds`, `mask`, `options`, `readonly`, `emit-immediately`.

## Searchable quick index

| Group | Exact symbols and intent |
| --- | --- |
| Actions/feedback | `QBtn` action; `QBtnDropdown` dropdown button; `QBtnGroup` grouped actions; `QBtnToggle` exclusive selection; `QFab` floating launcher; `QBadge` status/count; `QBanner` notice; `QChip` token/tag/status; `QAjaxBar` network indicator; `QInnerLoading` content overlay; `QLinearProgress` linear progress; `QCircularProgress` circular progress; `QSpinner` spinner; `QSkeleton` placeholder |
| Forms/input | `QInput` text; `QField` custom-field shell; `QForm` validation/submission; `QSelect` select/autocomplete; `QOptionGroup` radios/checkboxes/toggles; `QCheckbox`; `QRadio`; `QToggle`; `QFile`; `QUploader`; `QDate`; `QTime`; `QColor`; `QRange`; `QSlider`; `QKnob`; `QEditor` rich text |
| Data/scroll | `QTable`; `QMarkupTable`; `QList`/`QItem`; `QTree`; `QTimeline`; `QChat`; `QVirtualScroll`; `QInfiniteScroll`; `QScrollArea`; `QScrollObserver`; `QIntersection`; `QResizeObserver` |
| Overlays | `QDialog`; `QMenu`; `QTooltip`; `QPopupProxy` menu/dialog popup; `QPopupEdit`; `QNoSsr` client-only subtree |
| Media | `QImg`; `QVideo`; `QCarousel`; `QParallax`; `QAvatar`; `QIcon` |
| Layout/navigation | `QLayout`; `QDrawer`; `QPage`; `QPageScroller`; `QPageSticky`; `QTabs`; `QTabPanels`; `QToolbar`; `QBreadcrumbs`; `QSeparator`; `QSpace` |
| Structural/specialty | `QCard`; `QBar`; `QResponsive`; `QSlideTransition`; `QSlideItem`; `QExpansionItem`; `QStepper`; `QPagination`; `QRating`; `QSplitter` |

This atlas preserves legacy intent/search behavior (including stable `key` reuse and field `label` semantics) without claiming exact installed APIs. Treat legacy `button-family`, `input-family`, and `overview` as family guides. For exact old-name routing, search the symbol here, then open `85-legacy-skill-coverage.md`.
