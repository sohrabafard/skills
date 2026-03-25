# Components and Layouts

Use this file when the task names a Quasar component, a layout primitive, or a UI family.

## Search strategy

- Search the exact component name first, for example `QTable` or `QDialog`.
- Then classify by family below.
- For large or interactive UI surfaces, also read `60-guardrails-a11y-performance-monorepo.md`.
- For SSR/PWA routes, also read `20-ssr-pwa-and-security.md`.

## Component families

### Inputs and forms

- `QInput`, `QField`, `QForm`, `QSelect`, `QOptionGroup`, `QCheckbox`, `QRadio`, `QToggle`
- `QRange`, `QSlider`, `QKnob`, `QColor`, `QDate`, `QTime`
- `QFile`, `QUploader`, `QEditor`

Also load:

- `50-plugins-composables-directives-options-utils.md` when validation helpers, dialog plugins, or option-level config matter
- `60-guardrails-a11y-performance-monorepo.md` for labels, focus order, and keyboard behavior

### Buttons, actions, and command surfaces

- `QBtn`, `QBtnGroup`, `QBtnToggle`, `QBtnDropdown`, `QFab`

Also load:

- `60-guardrails-a11y-performance-monorepo.md`

### Data display and virtualized structures

- `QTable`, `QMarkupTable`, `QList`, `QItem`, `QTree`, `QTimeline`, `QChat`
- `QVirtualScroll`, `QInfiniteScroll`

Also load:

- `60-guardrails-a11y-performance-monorepo.md`
- `20-ssr-pwa-and-security.md` if the route is SSR-rendered

### Dialogs, menus, and overlays

- `QDialog`, `QMenu`, `QTooltip`, `QPopupEdit`, `QPopupProxy`

Also load:

- `50-plugins-composables-directives-options-utils.md`
- `60-guardrails-a11y-performance-monorepo.md`

### Media and imagery

- `QImg`, `QVideo`, `QCarousel`, `QParallax`, `QAvatar`

Also load:

- `20-ssr-pwa-and-security.md`
- `60-guardrails-a11y-performance-monorepo.md`

### Feedback and state indicators

- `QAjaxBar`, `QLinearProgress`, `QCircularProgress`, `QInnerLoading`, `QSpinner`, `QSkeleton`
- `QBanner`, `QBadge`, `QChip`

Also load:

- `50-plugins-composables-directives-options-utils.md`
- `60-guardrails-a11y-performance-monorepo.md`

### Layout and page primitives

- `QLayout`, `QDrawer`, `QHeader`, `QFooter`, `QPage`, `QPageScroller`, `QPageSticky`
- Grid/flex foundations, gallery patterns, routing with layouts and pages

Also load:

- `10-cli-vite-and-config.md`
- `20-ssr-pwa-and-security.md` for SSR routes

## Easy-to-miss relationships

- `QTable`, `QVirtualScroll`, and `QInfiniteScroll` are usually performance questions as much as component questions.
- `QDialog`, `QMenu`, and `QTooltip` are accessibility and focus-management questions as much as component questions.
- `QImg`, `QVideo`, and `QUploader` often intersect with SSR, caching, and bandwidth constraints.
- Layout bugs frequently come from routing, boot-time state, or SSR-only conditions instead of the layout component itself.
