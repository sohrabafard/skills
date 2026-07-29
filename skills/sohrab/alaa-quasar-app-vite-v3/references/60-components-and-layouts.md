# Components and layouts — family index

You have a component family in mind but not an exact symbol: "a table", "a picker", "an overlay", "a page shell". This table indexes Quasar symbols by family; skill-level routing is `references/00-topic-map.md`.

For exact props, events, slots, and methods, query the installed project first — `references/05-authority-and-api-lookup.md`. Then use `references/61-component-usage-atlas.md` for intent, alternatives, and gotchas, `references/62-layout-patterns-and-examples.md` for shell semantics, and `references/63-image-delivery-and-placeholders.md` for `QImg` delivery.

| Family | Symbols | Also load |
| --- | --- | --- |
| Inputs and forms | `QInput`, `QField`, `QForm`, `QSelect`, `QOptionGroup`, `QCheckbox`, `QRadio`, `QToggle`, `QRange`, `QSlider`, `QKnob`, `QColor`, `QDate`, `QTime`, `QFile`, `QUploader`, `QEditor` | `64` for validation and Dialog; `70` for labels, focus, and keyboard |
| Actions | `QBtn`, `QBtnGroup`, `QBtnToggle`, `QBtnDropdown`, `QFab` | `70` |
| Data and virtualization | `QTable`, `QMarkupTable`, `QList`, `QItem`, `QTree`, `QTimeline`, `QChat`, `QVirtualScroll`, `QInfiniteScroll` | `70` for the row and reactivity budgets; `31` on SSR routes |
| Overlays | `QDialog`, `QMenu`, `QTooltip`, `QPopupEdit`, `QPopupProxy` | `64`, `70` |
| Media | `QImg`, `QVideo`, `QCarousel`, `QParallax`, `QAvatar` | `63` for delivery; `31`, `70`. Player-driven video is `/alaa-shaka-player` (`$alaa-shaka-player`) |
| Feedback and state | `QAjaxBar`, `QLinearProgress`, `QCircularProgress`, `QInnerLoading`, `QSpinner`, `QSkeleton`, `QBanner`, `QBadge`, `QChip` | `64`, `70`; failure states are `34` |
| Layout and pages | `QLayout`, `QDrawer`, `QHeader`, `QFooter`, `QPage`, `QPageScroller`, `QPageSticky`; grid and flex, layout and page routing | `62`, `21`; `31` on SSR routes |

✅ Do — nest `QPage` inside `QPageContainer` inside `QLayout`. Ownership and the route shapes are `references/62-layout-patterns-and-examples.md`.

❌ Don't — place `QPage` directly inside `QLayout` or into a route without `QPageContainer`; spacing and scrolling break in ways that look like CSS bugs.

## Cross-cutting relationships

- `QTable`, `QVirtualScroll`, and `QInfiniteScroll` are performance decisions with budgets, not only components — `references/70-guardrails-a11y-performance-monorepo.md`. Their server-side paging contract is `/alaa-keyset-pagination` (`$alaa-keyset-pagination`).
- `QDialog`, `QMenu`, and `QTooltip` are accessibility and focus decisions as well as overlays.
- `QImg`, `QVideo`, and `QUploader` reach into SSR, caching, and bandwidth. `QUploader` transport over tus is `/tusd-upload-platform` (`$tusd-upload-platform`).
- A layout bug frequently originates in routing, boot state, or an SSR condition rather than in the shell.

Search: `component family`, `which component`, `QTable`, `QDialog`, `QLayout`, `QPageContainer`, `virtualization`, `overlay`, `media component`.
