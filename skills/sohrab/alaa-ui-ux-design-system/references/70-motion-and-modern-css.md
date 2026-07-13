# Motion and Modern CSS (classy animation contract)

Scope: the CSS platform features that are production-safe in mid-2026 and the motion-design rules that make app-family UIs feel premium and dignified instead of noisy. Verified 2026-07-08 against web-features/Baseline data, MDN, webkit.org, web.dev, and Interop 2026 announcements. Re-verify Baseline claims after that date (features move from Newly to Widely and Interop 2026 is actively converging the "limited" list).

Moved here from `$alaa-frontend-developer` `references/25-modern-css-and-motion.md`; this file now owns the Baseline tiers and the motion-taste contract. Theming/token recipes (oklch, `light-dark()`, `@property`) live in `20-design-tokens-and-theming.md`.

Pair with: `$alaa-frontend-developer` (SSR-safe implementation, hydration timing), `$alaa-vue-typescript-clean-code` (component/style discipline), `$alaa-quasar-app-vite-v3` (Quasar transition props, `app.scss`).

## 1. Adoption tiers — decide by Baseline status, not by fashion

Tier 1 — use unconditionally (Baseline Widely available):
container size queries + `cq*` units, `:has()`, subgrid, CSS nesting, `@layer`, logical properties, `clamp()` fluid type, `aspect-ratio`, `oklch()`/`oklab()`, `color-mix()`, `accent-color`, `color-scheme`, `<dialog>`, `linear()` easing, Web Animations API.

Tier 2 — use for evergreen targets; guard with `@supports` only when older Safari/Firefox matters (Baseline Newly available):
same-document View Transitions (cross-browser since Firefox 144, Oct 2025), `@starting-style`, `transition-behavior: allow-discrete`, Popover API, `@scope`, container style queries, `light-dark()`, relative color syntax, `@property`, `field-sizing: content`, `text-wrap: balance`, `content-visibility`.

Tier 3 — progressive enhancement only; the unenhanced state must be fully presentable (Limited availability):
cross-document View Transitions (no Firefox), scroll-driven animations (`animation-timeline: scroll()/view()` — Firefox still flagged), CSS anchor positioning (all engines ship it as of Firefox 147/151 but spec-compliance gaps remain; Interop 2026 focus), `text-wrap: pretty` (no Firefox), `interpolate-size`/`calc-size()` (Chromium only).

✅ Do — wrap Tier 3 in `@supports (animation-timeline: view())` / `@supports (anchor-name: --a)` and design the static state first.

❌ Don't — make comprehension or navigation depend on a Tier 3 effect, or add a JS polyfill for a purely decorative CSS feature.

## 2. Motion intensity tiers

Set the tier in the design brief (`10-design-workflow.md`) and record it in MASTER.md; every surface then draws from that tier, so the product has one motion temperament instead of per-page moods.

- Subtle (trust-heavy, dashboards, pro tools): micro-feedback and fades only; no parallax, no scroll choreography, no decorative loops.
- Standard (SaaS, e-commerce, content): micro-interactions plus purposeful section reveals and view transitions.
- Expressive (playful, creative, marketing heroes): choreographed staggers, scroll-driven scenes, signature moments — still inside the taste contract and gates below.

## 3. The modern motion stack (replace library habits with platform primitives)

Entry/exit for `display:none`, popovers, dialogs, toasts — the CSS-first pattern that replaces most `<Transition>` use on overlays:

```css
[popover], dialog {
  opacity: 0; translate: 0 8px;
  transition: opacity 200ms ease-out, translate 200ms ease-out,
    display 200ms allow-discrete, overlay 200ms allow-discrete;
}
:popover-open, dialog[open] { opacity: 1; translate: 0 0; }
@starting-style { :popover-open, dialog[open] { opacity: 0; translate: 0 8px; } }
```

View Transitions (same-document) — for route changes, shared-element morphs (thumbnail -> detail), and batch list reorder/filter; things Vue `<Transition>` cannot morph across components:

- Always feature-detect: `if (!document.startViewTransition) { mutate(); return }`.
- Vue integration: `document.startViewTransition(async () => { mutateState(); await nextTick() })` — the update callback must not settle until the new DOM is committed.
- Router integration: wrap navigation in a `beforeResolve` hook; register client-side only (Quasar boot file guarded for SSR) and skip the first hydration render, or the initial paint animates.
- Give morphing items a unique `view-transition-name` (via `v-bind()` in style or inline style) and a shared `view-transition-class` for group styling. Vue core has no native integration (vuejs/core#7881); do not wait for one.
- Keep Vue `<Transition>`/`<TransitionGroup>` for component-scoped enter/leave and continuous drag FLIP; never run both mechanisms on the same elements — the snapshot captures mid-flight states.

Scroll-driven animations (Tier 3): reveal/parallax via `animation-timeline: view()` inside `@supports`, transform/opacity only so they run off the main thread; the page must read perfectly without them.

Springs: there is no native `spring()`. Use `linear()` with generated stops (values >1 overshoot) stored as a custom property; use WAAPI or motion.dev only for gesture-driven, interruptible physics.

Sizing to content: `field-sizing: content` for auto-growing inputs/textareas (Tier 2); animate to `height: auto` via `interpolate-size` where available, with the `grid-template-rows: 0fr -> 1fr` trick as the cross-browser fallback.

Anchored UI: CSS anchor positioning can progressively replace hand-rolled tooltip/menu positioning, but keep Quasar's QMenu/QTooltip as the default until Interop 2026 closes the spec gaps.

## 4. Motion taste — the "classy and dignified" contract

These are hard defaults for app-family UIs; repo design tokens may override them:

- Duration scale as tokens, not ad-hoc numbers: ~100–150ms feedback (hover, press), 150–300ms micro-interactions, 250–400ms dialogs/large surfaces, 300–500ms absolute ceiling for full-view transitions. Premium reads as fast and decisive.
- Asymmetric easing: entrances decelerate (`ease-out`, e.g. `cubic-bezier(0.2, 0, 0, 1)`) and get the time; exits are 20–30% faster with `ease-in`. `linear` only for opacity/color, never for spatial movement.
- Scale duration with distance/size of change; a badge and a full-screen sheet do not share a duration.
- Choreography: stagger list entrances 20–50ms per item, cap the whole sequence at ~600ms and stop staggering after ~10 items; one focal element leads, nothing competes.
- Do NOT animate: typing/keyboard-nav feedback, dense pro-tool tables, the critical input path, post-load layout shifts, or idle attention-seeking loops. Dignified UIs animate state changes only.
- Quasar note: the Animate.css vocabulary shipped via `@quasar/extras` (`bounce`, `rubberBand`, ...) reads dated for premium UI. Restrict `transition-show`/`transition-hide` to subdued pairs (`fade`, `scale`, `jump-up`) with token durations, and build custom motion with the platform stack above instead of adding animation libraries.

✅ Do — encode durations/easings as design tokens (`--motion-duration-sm`, `--motion-ease-enter`) and reference them everywhere.

❌ Don't — copy a 800ms bouncing entrance onto a data table because a landing-page tutorial used one; frequency of the interaction, not novelty, decides the motion budget.

## 5. Accessibility and performance gates (blocking, not advisory)

- `prefers-reduced-motion: reduce` support is mandatory in every animated surface: replace movement with opacity crossfades (reduce, don't erase feedback), kill parallax/scroll-driven effects/auto-playing motion, and neutralize view-transition morphs (`::view-transition-group(*) { animation-duration: 0.05s }` or crossfade-only). Quasar's built-in transition classes do not honor it automatically — add a global override in `app.scss`.
- Also respect `prefers-reduced-transparency` (drop glass/blur) and `prefers-contrast: more` (drop low-contrast decorative motion).
- Compositor-only rule: animate `transform` and `opacity`; `filter`/`backdrop-filter` sparingly. Never animate layout (`width/height/top/left/margin/font-size`) or paint-heavy properties (`box-shadow` — crossfade a pseudo-element instead). View-transition snapshots make "layout" morphs cheap — prefer them over animating real layout.
- `will-change` discipline: set just before animating, remove after; never blanket-apply. Use `content-visibility: auto` / `contain` on long pages.
- Verification: a motion change is not done until it was checked with reduced-motion emulated and (when perf-sensitive) with DevTools performance/layers evidence or a Playwright check per `$alaa-frontend-developer` `references/50-qa-and-verification.md`.
