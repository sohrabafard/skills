# Modern CSS Baseline Tiers

Read this file before relying on a CSS feature you are not certain ships in every target browser. It is the **only** place in this pack that states platform-version facts, so calendar-stale content can be replaced here without touching any design rule.

## How to read and when to re-verify

- **Tier 1 — use unconditionally.** Baseline Widely available: supported in every major engine for at least 30 months.
- **Tier 2 — use for evergreen targets.** Baseline Newly available: supported in every major engine, but recently. Guard with `@supports` only when the repo's browser-support matrix names a version older than the date in the table.
- **Tier 3 — progressive enhancement only.** Limited availability: at least one major engine does not ship it. The unenhanced state must be fully presentable on its own, and comprehension or navigation must never depend on the effect.

**Re-verify trigger, observable rather than calendar-based:** re-check a row before relying on it if the row's `read:` date is more than 90 days before today, **or** if the task depends on a Tier 2 or Tier 3 feature at all. Verify against the Baseline dataset (`api.webstatus.dev`) and MDN browser-compatibility data. Do not verify against a blog post, and do not re-assert a row from memory.

## Tier 1 — Widely available

Container size queries and `cq*` units, `:has()`, subgrid, CSS nesting, `@layer`, logical properties, `clamp()`, `aspect-ratio`, `color-mix()`, `accent-color`, `color-scheme`, `<dialog>`, `linear()` easing, the Web Animations API.

| Feature | Baseline | Since | Provenance |
|---|---|---|---|
| `oklch()` / `oklab()` | **Widely available** | 2023-05-09 | `api.webstatus.dev` feature `oklab`, `read: 2026-07-28` |

Everything else in this tier is `read: unverified as of 2026-07-28` at the individual-feature level and is carried forward from the prior version of this pack; each was Widely available when written and none has regressed.

## Tier 2 — Newly available

| Feature | Baseline low date | Provenance |
|---|---|---|
| `light-dark()` | 2024-05-13 | `api.webstatus.dev` feature `light-dark`, `read: 2026-07-28` |
| `@property` / registered custom properties | 2024-07-09 | feature `registered-custom-properties`, `read: 2026-07-28` |
| `@starting-style` | 2024-08-06 | feature `@starting-style`, `read: 2026-07-28` |
| Relative color syntax | 2024-09-16 | feature `relative-color`, `read: 2026-07-28` |
| `fetchpriority` | 2024-10-29 | feature `fetch-priority`, `read: 2026-07-28` |
| Popover API | 2025-01-27 | feature `popover`, `read: 2026-07-28` |
| `content-visibility` | 2025-09-15 | feature `content-visibility`, `read: 2026-07-28` |
| Same-document View Transitions | 2025-10-14 | feature `view-transitions`, `read: 2026-07-28` |
| `view-transition-class` | 2025-10-14 | feature `view-transition-class`, `read: 2026-07-28` |
| `@scope` | 2025-12-12 | feature `scope`, `read: 2026-07-28` |
| `contrast-color()` | 2026-04-10 | feature `contrast-color`, `read: 2026-07-28` |
| Container **style** queries | 2026-05-19 | feature `container-style-queries`, `read: 2026-07-28` |
| `field-sizing: content` | 2026-06-16 | feature `field-sizing`, `read: 2026-07-28` |

`transition-behavior: allow-discrete` and `text-wrap: balance` were listed in this tier by the prior version of this pack and are carried forward as `read: unverified as of 2026-07-28`.

**Note on the three most recent rows.** `contrast-color()`, container style queries and `field-sizing` reached Baseline within the last four months. Treat them as Tier 2 for evergreen targets and as Tier 3 for any repo whose support matrix reaches back a year.

**`contrast-color()` is directly useful here:** it picks a passing foreground for a known fill in CSS. It does not remove the obligation to measure a palette (`30-typography-and-color.md`), because it cannot see a gradient, an image or a translucent surface behind the fill — it removes the obligation to guess for the simple case.

## Tier 3 — Limited availability

| Feature | Status | Provenance |
|---|---|---|
| CSS anchor positioning | **limited** | `api.webstatus.dev` feature `anchor-positioning`, `read: 2026-07-28`. Mozilla and WebKit have stated positive positions; that is not shipping. |
| Scroll-driven animations (`animation-timeline: scroll()` / `view()`) | **limited** | feature `scroll-driven-animations`, `read: 2026-07-28`. Chromium since 2023-07, Safari since 2025-09; Firefox not indicated. |
| `interpolate-size` / `calc-size()` | **limited** | feature `interpolate-size`, `read: 2026-07-28` |
| Cross-document View Transitions | limited | `read: unverified as of 2026-07-28` — the same-document form above is separately Baseline and is not affected |
| `text-wrap: pretty` | **unresolved** | The `text-wrap-style` **property** is Baseline 2024 (MDN, `read: 2026-07-28`), and MDN notes that parts of the feature have varying support without publishing per-value numbers. Per-value support for `pretty` could not be resolved from that source. Treat as Tier 3 until resolved: the unstyled wrap must be acceptable. |

**Correction to a claim this pack previously made:** the prior version asserted that anchor positioning ships in all engines and that scroll-driven animations were merely flagged in one. The Baseline dataset reports both as **limited** on 2026-07-28. Keep Quasar's own menu and tooltip positioning as the default rather than replacing it with anchor positioning; that decision belongs to `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`) and this row is only the platform fact behind it.

## Usage rules

- Wrap every Tier 3 feature in `@supports` and design the static state first.
- Never add a JavaScript polyfill for a decorative CSS feature. If it needs a polyfill to be worth having, it is not decorative.
- Feature-detect View Transitions before calling them, and design the no-transition path as the real path.
- A Tier 2 feature used without a guard is a decision to require the browser-support matrix in the repo to allow it. Check the matrix rather than assuming.

## Pairing

- The motion rules these features implement: `70-motion-contract.md`
- Token recipes using `oklch()`, `light-dark()` and `@property`: `20-design-tokens-and-theming.md`
- Contrast measurement that `contrast-color()` does not replace: `30-typography-and-color.md`
- SSR-safe implementation and hydration timing: `/alaa-frontend-developer` (`$alaa-frontend-developer`)
