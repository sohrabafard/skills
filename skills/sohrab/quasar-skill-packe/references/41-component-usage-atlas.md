# Component Usage Atlas

Use this file when the agent needs the layer the old component-specific skills were good at: what the component is for, how it is commonly used, what to search for, and what related component to consider instead.

## How to use this atlas

1. Search the exact component name, such as `QTable` or `QDialog`.
2. Read the quick purpose, alternatives, and usage notes below.
3. Use the suggested search terms when you need deeper implementation details or official examples.
4. Pair this file with:
   - `40-components-and-layouts.md` for family routing
   - `60-guardrails-a11y-performance-monorepo.md` for accessibility and performance risk
   - `20-ssr-pwa-and-security.md` when the route is SSR, PWA, or hydration-sensitive

## High-value usage playbooks

### QTable

- Use when you need an interactive data table with sorting, filtering, selection, pagination, sticky sections, or grid mode.
- Prefer `QMarkupTable` for static markup.
- Prefer `QVirtualScroll` table mode when DOM size and scroll performance are the real problem.
- Important usage notes:
  - set a stable primitive `row-key`
  - define `columns` explicitly when you need sorting, slot targeting, or visibility control
  - treat server-side pagination as a data-flow problem, not just a visual prop choice
  - grid mode can be a valid mobile fallback
- Good search terms:
  - `row-key`, `columns`, `visible-columns`, `selection`, `server-side pagination`, `sticky header`, `sticky column`, `grid mode`, `virtual-scroll`

### QDialog

- Use for modal flows, short forms, confirmations, or overlay content that should take focus.
- Prefer the Dialog plugin when the dialog should be invoked programmatically or reused from many places.
- Prefer `QMenu`, `QPopupProxy`, or `QTooltip` when the interaction is lighter than a full modal.
- Important usage notes:
  - use `QCard` as the main child when possible, or wrap non-card content in a `div`
  - `position` is independent from `transition-show` and `transition-hide`
  - `persistent`, `seamless`, and `maximized` meaningfully change behavior
  - containerized `QLayout` inside a dialog needs explicit width or height
- Good search terms:
  - `persistent`, `seamless`, `maximized`, `position`, `transition-show`, `transition-hide`, `backdrop-filter`, `Dialog plugin`

### QSelect

- Use for single or multiple selection from an option list, optionally with filtering or custom option rendering.
- Prefer `QInput` for free text.
- Prefer `QOptionGroup` when choices should be visible inline instead of behind a popup selector.
- Important usage notes:
  - single-select model can be many shapes; multiple-select model must be an array
  - `emit-value` and `map-options` directly affect model shape
  - `use-input` turns it into a more autocomplete-like surface
  - `behavior` matters on mobile and can need conditional dialog mode on iOS
  - `options-cover` disables transitions
- Good search terms:
  - `emit-value`, `map-options`, `use-input`, `behavior`, `clearable`, `multiple`, `display-value`, `options-cover`, `new-value-mode`

### QImg

- Use for responsive image rendering with loading states, aspect ratio control, placeholders, fit modes, captions, and native lazy loading.
- Prefer raw `img` only when none of Quasar’s rendering ergonomics matter.
- Important usage notes:
  - `fit` and `position` map to CSS object-fit/object-position behavior
  - `srcset` and `sizes` are native browser features; QImg relies on them rather than abstracting them away
  - placeholder images are especially useful for large media
  - if disabling the native context menu, make sure slot content preserves pointer events correctly
- If the task is really about deterministic image delivery, shared placeholders, or SSR-safe responsive candidate generation, also open `43-image-delivery-and-placeholders.md`.
- Good search terms:
  - `ratio`, `placeholder-src`, `fit`, `position`, `srcset`, `sizes`, `loading="lazy"`, `context menu`

### QFile vs QUploader

- Use `QFile` when you only need file picking.
- Use `QUploader` when you need an upload queue, transport customization, drag and drop, or upload lifecycle control.
- Important `QFile` usage notes:
  - it is still a native file input under the hood, so the browser will not let you truly prefill it programmatically
  - showing files through the model is not the same thing as the native input having those files selected
- Important `QUploader` usage notes:
  - it needs a backend upload target
  - `accept` relies on native file input semantics and must be correct
  - `headers`, `form-fields`, `with-credentials`, and `factory` are the key transport hooks
  - `batch` changes multiple-file upload behavior
  - custom header/list slots often need `QUploaderAddTrigger`
- Good search terms:
  - `accept`, `headers`, `form-fields`, `factory`, `with-credentials`, `batch`, `QUploaderAddTrigger`, `filter`

### QVirtualScroll and QInfiniteScroll

- Use `QVirtualScroll` when you already have a large list and rendering cost is the main problem.
- Use `QInfiniteScroll` when you need incremental data loading based on scroll progression.
- Do not treat them as interchangeable:
  - virtualization is about render cost
  - infinite scroll is about loading progression
- Important `QVirtualScroll` usage notes:
  - `virtual-scroll-item-size` and `virtual-scroll-slice-size` matter
  - custom `scroll-target` must exist and be scrollable
  - `items-fn` must be synchronous
  - freezing or keeping large item arrays non-reactive can materially improve performance
- Good search terms:
  - `virtual-scroll-item-size`, `slice-size`, `scroll-target`, `items-fn`, `q-virtual-scroll--with-prev`, `q-virtual-scroll--skip`

### QLayout, QDrawer, QPage, QPageSticky, QPageScroller

- Use these for the application shell and route-level page composition.
- Important usage notes:
  - layout bugs often come from router structure, SSR state, or page container assumptions rather than the layout component alone
  - a `QPage` must live inside `QPageContainer`, and `QPageContainer` must live inside `QLayout`
  - the layout file usually owns `QPageContainer` and `<router-view />`, while individual page files own `QPage`
  - `view` is not decoration; it controls fixed/revealed behavior for headers, footers, and drawers
  - `QDrawer` overlay, mini mode, and mobile behavior change navigation and focus expectations in meaningful ways
  - drawers and sticky/page-scroller affordances are accessibility and responsive-behavior concerns, not just visual ones
- For deeper layout semantics such as `view`, containerized layouts, overlay/fixed behavior, and nested route structure, also open `42-layout-patterns-and-examples.md`.
- Minimal shell example:

```vue
<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn flat dense round icon="menu" @click="leftDrawerOpen = !leftDrawerOpen" />
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered>
      <!-- navigation -->
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>
```

- Page example:

```vue
<template>
  <q-page padding>
    <!-- page content -->
  </q-page>
</template>
```

- Good search terms:
  - `view`, `QPageContainer`, `router-view`, `containerized layout`, `drawer breakpoint`, `overlay`, `mini mode`, `page sticky`, `page scroller`, `routing with layouts`

### QTabs and QTabPanels

- Use for a small set of mutually exclusive views or content panels.
- Prefer routing when tabs represent durable navigation states the URL should own.
- Good search terms:
  - `keep-alive`, `animated`, `vertical`, `mobile scroll`, `route tabs`

### QMenu, QPopupProxy, QPopupEdit, QTooltip

- Use `QMenu` for contextual action menus.
- Use `QPopupProxy` or `QPopupEdit` for anchored inline editing or popover-like interaction.
- Use `QTooltip` for lightweight hints, not for required information or complex interaction.
- Important usage notes:
  - `QPopupProxy` switches between `QMenu` and `QDialog` based on screen size, so treat it as a responsive interaction primitive, not just a menu alias
  - the default `QPopupProxy` breakpoint is small-screen oriented; if the interaction depends on a different switch point, search `breakpoint`
  - some child components such as `QDate`, `QTime`, `QColor`, and `QCarousel` get special popup behavior unless you wrap them in a `div`
- Good search terms:
  - `anchor`, `self`, `cover`, `persistent`, `focus`, `keyboard`, `inline edit`, `breakpoint`, `context menu`, `pass-through props`

### QInput, QField, QForm, QOptionGroup

- Use `QField` when you need field framing and decorators around a custom control.
- Use `QInput` for freeform text-like entry.
- Use `QForm` for coordinated validation and submission.
- Use `QOptionGroup` when the UI should expose grouped discrete choices directly instead of behind a popup selector.
- Important usage notes:
  - do not wrap `QInput`, `QFile`, or `QSelect` with `QField`; those components already inherit `QField`
  - if a custom `QField` control also uses `label`, search `stack-label` to avoid label overlap with custom content
  - submit buttons inside `before`, `after`, `prepend`, or `append` slots need an explicit `@click` submit handler because those slot clicks do not bubble like many people expect
- Good search terms:
  - `rules`, `lazy-rules`, `debounce`, `mask`, `submit slot click`, `option group`, `stack-label`, `useFormChild`

### QDate, QTime, QColor, QSlider, QRange, QKnob

- Use these for structured value picking, not just decorative controls.
- Watch model shape and formatting assumptions carefully in SSR or localized apps.
- Good search terms:
  - `range`, `with-seconds`, `mask`, `options`, `readonly`, `emit-immediately`

## Searchable quick index

These short descriptions are here so the agent can search exact component names quickly without returning to the old one-skill-per-component catalog.

### Buttons, badges, chips, and feedback

- `QBtn`: primary action button
- `QBtnDropdown`: button with dropdown/menu behavior
- `QBtnGroup`: grouped button actions
- `QBtnToggle`: mutually exclusive button selection
- `QFab`: floating action launcher
- `QBadge`: compact status or count badge
- `QBanner`: inline attention or warning surface
- `QChip`: compact token/tag/status UI
- `QAjaxBar`: top-edge network activity indicator
- `QInnerLoading`: content-area loading overlay
- `QLinearProgress`: linear progress bar
- `QCircularProgress`: circular progress indicator
- `QSpinner`: generic loading spinner
- `QSkeleton`: placeholder loading shape

### Forms and structured input

- `QInput`: freeform text input
- `QField`: wrapper shell for custom field content
- `QForm`: grouped validation and submission surface
- `QSelect`: popup select and autocomplete-like picker
- `QOptionGroup`: grouped radios, checkboxes, or toggles
- `QCheckbox`: boolean or multi-choice checkbox
- `QRadio`: single-choice radio
- `QToggle`: switch-style boolean control
- `QFile`: file picker only
- `QUploader`: managed upload workflow
- `QDate`: date picker
- `QTime`: time picker
- `QColor`: color picker
- `QRange`: dual-ended range picker
- `QSlider`: numeric slider
- `QKnob`: knob-style numeric control
- `QEditor`: rich text editor

### Tables, lists, trees, and scrolling

- `QTable`: interactive data table
- `QMarkupTable`: static table markup
- `QList` / `QItem`: list and row primitives
- `QTree`: hierarchical explorer/tree
- `QTimeline`: chronological event presentation
- `QChat`: chat-thread presentation
- `QVirtualScroll`: virtualized large-list renderer
- `QInfiniteScroll`: scroll-triggered incremental loading
- `QScrollArea`: styled scroll container
- `QScrollObserver`: scroll activity observer
- `QIntersection`: visibility-driven rendering or observation
- `QResizeObserver`: size-change observation

### Overlays and contextual surfaces

- `QDialog`: modal overlay
- `QMenu`: contextual floating menu
- `QTooltip`: lightweight hover/focus hint
- `QPopupProxy`: anchored popup shell that can switch between menu and dialog
- `QPopupEdit`: inline-edit popup
- `QNoSsr`: explicitly client-only subtree wrapper

### Media and visuals

- `QImg`: responsive image with loading states
- `QVideo`: embedded video wrapper
- `QCarousel`: slide-based media/content carousel
- `QParallax`: parallax media section
- `QAvatar`: avatar/media shape
- `QIcon`: icon rendering primitive

### Layout and navigation surfaces

- `QLayout`: application shell container
- `QDrawer`: side drawer navigation/content
- `QPage`: route page container
- `QPageScroller`: floating scroll-to-position control
- `QPageSticky`: sticky floating page child
- `QTabs`: tab navigation strip
- `QTabPanels`: tab panel content container
- `QToolbar`: toolbar row
- `QBreadcrumbs`: breadcrumb navigation
- `QSeparator`: visual divider
- `QSpace`: flex spacer

### Structural and specialty helpers

- `QCard`: card content container
- `QBar`: compact horizontal action/info row
- `QResponsive`: aspect-ratio-aware container
- `QSlideTransition`: slide transition wrapper
- `QSlideItem`: swipeable row interaction
- `QExpansionItem`: expandable section or row
- `QStepper`: step-based workflow container
- `QPagination`: page-number navigation
- `QRating`: star-like rating control
- `QSplitter`: resizable pane split

## Notes

- The atlas intentionally restores the strongest part of the old component-specific skills: quick component intent, decision heuristics, gotchas, and search vocabulary, without forcing the agent to scan dozens of tiny files.
- Legacy helper names like `button-family`, `input-family`, or `overview` should be treated as family guides rather than exact Quasar APIs.
- If you need the exact old search behavior, search the component symbol here first, then use `80-legacy-skill-coverage.md`.
