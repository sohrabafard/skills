# Accessibility Patterns

Read this file when adding a click handler to a non-button, opening an overlay, changing route in a single-page app, or writing ARIA. The blocking thresholds live in `90-quality-gates-and-review.md`; this file is how to satisfy them well.

**Conformance target: WCAG 2.2 Level AA.** WCAG 2.2 is the current W3C Recommendation and is also ISO/IEC 40500:2025; WCAG 3.0 remains a working draft and is not a target (`w3.org/WAI/standards-guidelines/wcag/`, `read: 2026-07-28`). Where this pack is stricter than 2.2 AA it says so explicitly rather than implying the standard requires it.

## Semantic structure

- Exactly one `h1` per page. Heading levels are sequential, with no jump from `h2` to `h4`. Headings describe sections, not styling.
- Landmarks — `header`, `nav`, `main`, `footer`, `aside` — with one `main` per page and a name on each repeated landmark.
- A skip link as the first focusable element on content-heavy pages, visible on focus.
- **Language attributes:** the page language and direction on the root element, and an inline language attribute on any span in another language, so a screen reader switches voice. Direction mechanics are in `05-rtl-and-persian.md`.

## Native first, ARIA second

- Reach for `button`, `a`, `details`/`summary`, `dialog`, `select` and real form controls before ARIA. Framework components carry most of the wiring already; prefer them to hand-rolled widgets.
- **A `div` with a click handler is a defect:** no focus, no keyboard, no role, no accessible name. If it acts like a button, it is a button.
- ARIA fills genuine gaps only — a custom combobox, a live region — and then follows the authoring-practices pattern exactly. Half-applied ARIA is worse than none, because it promises behaviour that is not there.
- **Links navigate, buttons act.** Never a link styled as a button performing a destructive action.

## Focus management

- **Dialogs, sheets and drawers:** focus moves in on open to the first sensible element, stays trapped while open, and **returns to the trigger on close**. Verify this for every custom overlay rather than assuming the framework did it.
- **Route changes in a single-page app:** after navigation, move focus to the main content or the new heading and announce the change through a polite live region. Without this a screen-reader user hears nothing at all when the page changes.
- After a failed form submit, focus the first invalid field.
- **Never remove an outline without a stronger `:focus-visible` replacement.** Focus order follows visual order; `order` and `row-reverse` break that, and are twice as easy to get wrong under RTL.
- A focused element is never hidden behind a sticky bar (`50-layout-landing-and-ia.md`).

Relevant success criteria: 2.4.3 focus order, 2.4.7 focus visible, 2.4.11 focus not obscured (minimum) — the last is new in 2.2 and is the sticky-bar case.

## Keyboard

- Standard keys behave standardly: `Esc` closes an overlay, `Enter` and `Space` activate, arrows move within a composite widget, `Tab` moves between widgets rather than within them.
- **No keyboard traps.** Everything reachable is leavable.
- Drag-and-drop and gesture interactions ship a keyboard or visible-control alternative (2.5.7 dragging movements, 2.5.1 pointer gestures).
- Roving tabindex, or an active-descendant relationship, for composite widgets so `Tab` does not crawl through fifty menu items.

## Live regions

- A polite live region for async results, toasts and background updates; an assertive alert role only for errors needing immediate attention.
- **Announce state, not noise.** "3 results found", not every keystroke of a filter. One live region per concern; never rebroadcast the whole application state through one.
- Loading that runs beyond a moment announces its start and its completion, not only its skeleton.

## Zoom, reflow and adaptation

- 200% browser zoom and 320px-wide reflow lose no content and no function: no horizontal scroll, no clipped control (1.4.10 reflow, 1.4.4 resize text).
- Layout survives increased text spacing (1.4.12 text spacing) — avoid fixed-height text containers.
- `prefers-reduced-motion` per `70-motion-contract.md`. `prefers-contrast: more` and forced-colours mode must not erase borders or focus indicators.

## Verification

**Minimum pass, with no self-granted exception:**

1. A keyboard-only walk of every primary flow.
2. An automated scan. Run the repository's own integration if it has one; otherwise run `npx @axe-core/cli <url>`. **If neither can run in this environment, say so in the delivery note and list which flows were walked by keyboard instead. An unrun scan is reported, never assumed clean.**
3. A screen-reader smoke test of any new flow.

**An automated scan finds a minority of accessibility defects** — the classes it can detect mechanically, such as missing names, contrast on solid backgrounds, and structural errors. It does not detect a wrong reading order, a misleading label, or a trap. It supplements the keyboard and screen-reader passes and never replaces them. (The frequently-quoted "about 40%" figure has no primary source this pack can cite, so it is stated qualitatively rather than as a number.)

Test design and the proof levels this sits inside are owned by `/alaa-testing-strategy` (`$alaa-testing-strategy`); browser-based checks follow `/alaa-frontend-developer` (`$alaa-frontend-developer`) browser gating. What artefact each check must produce is in `95-design-proofs.md`.

## Anti-patterns

- `div` and `span` click targets; `role="button"` on something that should be a `<button>`.
- ARIA added to silence a linter without the matching keyboard behaviour.
- Focus styles removed globally; a modal that drops focus back to the document body on close.
- One giant live region rebroadcasting application state.
- A Persian page with no language or direction attribute, or mixed-direction text left to the browser to guess — the positive replacement is in `05-rtl-and-persian.md` section 1.
- Reporting an accessibility pass when the scan did not run.

## Pairing

- The blocking thresholds: `90-quality-gates-and-review.md`
- Form and navigation specifics: `60-components-states-and-ux.md`
- Direction, language and bidi: `05-rtl-and-persian.md`
- Motion preferences: `70-motion-contract.md`
- What each check must leave behind: `95-design-proofs.md`
