# Accessibility Patterns

Use this file for accessibility implementation patterns beyond the blocking gates. The gates live in `90-quality-gates-and-review.md`; this file is how to satisfy them well. Accessibility here is design quality, not compliance paperwork — it usually improves the UI for everyone.

## Semantic structure

- Exactly one `h1` per page; heading levels sequential (no h2 -> h4 jumps); headings describe sections, not styling.
- Landmarks: `header`, `nav`, `main`, `footer`, `aside` — one `main` per page; name repeated landmarks (`aria-label="pagination"`).
- Skip link ("Skip to main content") as the first focusable element on content-heavy pages; visible on focus.
- Language attributes: `lang="fa"` with `dir="rtl"` for Farsi pages; mark inline foreign-language spans (`<span lang="en">`) so screen readers switch voices.

## Native-first, ARIA second

- Reach for native elements before ARIA: `button`, `a`, `details/summary`, `dialog`, `select`, real checkboxes. Quasar components carry most ARIA wiring — prefer them over hand-rolled widgets.
- A `div` with `@click` is a defect: no focus, no keyboard, no role. If it acts like a button, it is a `button`.
- ARIA only fills genuine gaps (custom comboboxes, live regions) and follows the APG pattern exactly — half-applied ARIA is worse than none.
- Links navigate, buttons act: never a link styled as a button performing a destructive action.

## Focus management

- Dialogs/sheets/drawers: focus moves in on open (first sensible element), stays trapped while open, and returns to the trigger on close. Quasar dialogs handle most of this — verify, don't assume, for custom overlays.
- SPA route changes: after navigation, move focus to the main content or new `h1` and announce the page change via a polite live region — otherwise screen-reader users hear nothing.
- After failed form submit: focus the first invalid field (`60-components-states-and-ux.md`).
- Never `outline: none` without a stronger `:focus-visible` replacement; focus order follows visual order (beware CSS `order`/`flex-direction: row-reverse` breaking it — relevant in RTL work).

## Keyboard patterns

- Standard keys behave standardly: `Esc` closes overlays, `Enter`/`Space` activate, arrows move within composite widgets (menus, tabs, radio groups), `Tab` moves between widgets, not within them.
- No keyboard traps: everything reachable is also leavable.
- Custom drag-and-drop and gesture interactions ship a keyboard/visible-control alternative.
- Roving tabindex (or `aria-activedescendant`) for composite widgets so `Tab` doesn't crawl through 50 menu items.

## Live regions and announcements

- `aria-live="polite"` for async results, toasts, and background updates; `role="alert"` only for errors needing immediate attention.
- Announce state, not noise: "3 results found", not every keystroke of a filter. One live region per concern; do not spam re-renders through it.
- Loading beyond a moment announces start and completion, not just a visual skeleton.

## Zoom, reflow, and adaptation

- 200% browser zoom and 320px-wide reflow lose no content or function — no horizontal scroll, no clipped controls.
- Layout survives increased text spacing (WCAG 1.4.12) — avoid fixed-height text containers.
- `prefers-reduced-motion` per `70-motion-and-modern-css.md`; `prefers-contrast: more` and forced-colors mode must not erase borders and focus indicators.

## Verification

- Minimum pass: keyboard-only walk of primary flows + automated scan (axe or equivalent) when tooling exists + screen-reader smoke of new flows (VoiceOver/NVDA).
- Automated scanners catch at most ~40% of issues — they supplement the keyboard/SR pass, never replace it.
- Browser-based checks follow `$alaa-frontend-developer` browser gating.

## Anti-patterns

- `div`/`span` click targets; `role="button"` on things that should be `<button>`.
- ARIA sprinkled to silence a linter without the matching keyboard behavior.
- Focus styles removed globally; modals that drop focus back to `<body>` on close.
- One giant `aria-live` region rebroadcasting the whole app state.
- Farsi pages without `lang`/`dir`, or mixed-direction text left to the browser to guess.

## Pairing guidance

- The blocking gate list and review flow: `90-quality-gates-and-review.md`
- Form and navigation a11y specifics: `60-components-states-and-ux.md`
- Motion-related preferences: `70-motion-and-modern-css.md`
