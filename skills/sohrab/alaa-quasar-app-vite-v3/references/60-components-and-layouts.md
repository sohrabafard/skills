# Components and Layouts

Use when a task names a Quasar component, layout primitive, or UI family. For exact props/events/slots/methods, first use `05-authority-and-api-lookup.md` against the installed project. Pair with `61-component-usage-atlas.md` for intent/alternatives/gotchas, `62-layout-patterns-and-examples.md` for layout-shell semantics, and `63-image-delivery-and-placeholders.md` for deterministic `QImg` delivery.

## Search and routing

1. Search the exact symbol (`QTable`, `QDialog`, etc.); if syntax matters, query the installed API.
2. Route by family below, then load `61-component-usage-atlas.md`.
3. Also load `70-guardrails-a11y-performance-monorepo.md` for large/interactive surfaces and `31-ssr-pwa-and-security.md` for SSR/PWA routes.

| Family | Symbols/topics | Also load |
| --- | --- | --- |
| Inputs/forms | `QInput`, `QField`, `QForm`, `QSelect`, `QOptionGroup`, `QCheckbox`, `QRadio`, `QToggle`, `QRange`, `QSlider`, `QKnob`, `QColor`, `QDate`, `QTime`, `QFile`, `QUploader`, `QEditor` | `64-plugins-composables-directives-options-utils.md` for validation/Dialog/options; `70` for labels, focus, keyboard |
| Actions | `QBtn`, `QBtnGroup`, `QBtnToggle`, `QBtnDropdown`, `QFab` | `70` |
| Data/virtualization | `QTable`, `QMarkupTable`, `QList`, `QItem`, `QTree`, `QTimeline`, `QChat`, `QVirtualScroll`, `QInfiniteScroll` | `70`; `31` on SSR routes |
| Overlays | `QDialog`, `QMenu`, `QTooltip`, `QPopupEdit`, `QPopupProxy` | `64`, `70` |
| Media | `QImg`, `QVideo`, `QCarousel`, `QParallax`, `QAvatar` | `31`, `70`; `63` for placeholder/ratio/responsive candidates |
| Feedback/state | `QAjaxBar`, `QLinearProgress`, `QCircularProgress`, `QInnerLoading`, `QSpinner`, `QSkeleton`, `QBanner`, `QBadge`, `QChip` | `64`, `70` |
| Layout/pages | `QLayout`, `QDrawer`, `QHeader`, `QFooter`, `QPage`, `QPageScroller`, `QPageSticky`; grid/flex, galleries, layout/page routing | `21-cli-vite-and-config.md`, `31` on SSR routes, `62` |

✅ Do — nest `QPage` inside `QPageContainer` inside `QLayout`.

❌ Don't — put `QPage` directly in `QLayout` or a route without `QPageContainer`; spacing/scrolling break.

## Cross-cutting relationships

- `QTable`/`QVirtualScroll`/`QInfiniteScroll`: performance as well as components.
- `QDialog`/`QMenu`/`QTooltip`: accessibility/focus as well as overlays.
- `QImg`/`QVideo`/`QUploader`: SSR, caching, and bandwidth.
- Layout bugs often originate in routing, boot state, or SSR conditions.
