# Motion Contract

Read this file when animating anything, adding a transition, or setting a duration or easing value. It holds the motion-design rules, which are durable. Which CSS features are safe to use is a separate, version-sensitive question answered in `72-modern-css-baseline-tiers.md`.

## Motion intensity tiers

Set the tier in the design brief (`10-design-workflow.md`) and record it in `MASTER.md`. Every surface then draws from that tier, so the product has one motion temperament instead of per-page moods.

- **Subtle** (trust-heavy, dashboards, professional tools): micro-feedback and fades only. No parallax, no scroll choreography, no decorative loops.
- **Standard** (SaaS, e-commerce, content): micro-interactions plus purposeful section reveals and view transitions.
- **Expressive** (playful, creative, marketing heroes): choreographed staggers, scroll-driven scenes, signature moments — still inside every rule below.

## Duration and easing

Encode these as tokens (`--motion-duration-sm/md/lg`, `--motion-ease-enter/exit`) and reference the tokens everywhere.

| Change | Duration |
|---|---|
| Feedback: hover, press, focus | 100-150 ms |
| Micro-interaction: toggle, chip, inline reveal | 150-300 ms |
| Dialog, drawer, large surface | 250-400 ms |
| Full-view transition (ceiling) | 300-500 ms |

- **Asymmetric easing:** entrances decelerate (`ease-out`, e.g. `cubic-bezier(0.2, 0, 0, 1)`) and get the full time; exits run 20-30% faster with `ease-in`. `linear` only for opacity and colour, never for spatial movement.
- **Scale duration with the distance and size of the change.** A badge and a full-screen sheet do not share a duration.
- **Premium reads as fast and decisive.** When in doubt, take the shorter value.

**Override rule:** a repository overrides a duration or an easing **only** by defining `--motion-duration-*` or `--motion-ease-*` in its theme file. A literal duration or easing written into a component remains a defect regardless of what the theme says, and `scripts/check-design-system.mjs --tokens` reports it.

## Choreography

- Stagger list entrances 20-50 ms per item, cap the whole sequence at about 600 ms, and stop staggering after about ten items. Beyond that the last item arrives after the user has stopped waiting.
- One focal element leads. Nothing competes with it.
- **Direction-bearing motion follows writing direction** (`05-rtl-and-persian.md` section 3). A drawer entering from a fixed physical side is a defect in a product that can render either direction; direction-free motion — fade, scale — needs no flip and is the safer default.

## Do not animate

- Typing and keyboard-navigation feedback.
- Dense professional tables and data entry.
- Anything on the critical input path.
- Layout that settles after load — that is a shift with an animation on it, not motion design.
- Idle attention-seeking loops.

Dignified interfaces animate state changes. They do not animate to be noticed.

## Performance rules

- **Animate `transform` and `opacity` only.** They run on the compositor. Use `filter` and `backdrop-filter` sparingly and never per list item.
- **Never animate layout** (`width`, `height`, `top`, `left`, `margin`, `padding`, `font-size`) or paint-heavy properties. For a shadow change, crossfade a pseudo-element rather than animating `box-shadow`.
- View-transition snapshots make "layout" morphs cheap; prefer them over animating real layout.
- `will-change` is set just before animating and removed after. Never blanket-applied.
- Frame and interaction budgets are in `45-render-and-asset-budgets.md`.

## Reduced motion and related preferences (blocking)

- **`prefers-reduced-motion: reduce` is honoured on every animated surface.** Replace movement with an opacity crossfade — reduce, do not erase feedback. Kill parallax, scroll-driven effects and auto-playing motion. Neutralize view-transition morphs to a crossfade or a near-zero duration.
- A component library's built-in transition classes do not necessarily honour this; verify rather than assume, and add a global override if they do not. Where that override lives in a Quasar app is owned by `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`).
- **`prefers-reduced-transparency`** drops glass and blur to a solid surface — which must itself pass contrast, since the text was measured against the blurred version.
- **`prefers-contrast: more`** drops low-contrast decorative motion and strengthens boundaries.
- **A motion change is not done until it was checked with reduced motion emulated.** The proof is in `95-design-proofs.md`; an unrun check is reported, never assumed clean.

## Anti-patterns

- A literal `200ms` in a component because the token name was not to hand.
- An 800 ms bouncing entrance on a data table because a landing-page tutorial used one.
- Animating `height` to reveal a panel.
- A dated animation vocabulary — bounce, rubber-band, flip — on a product that wants to read as serious.
- Adding an animation library for an effect the platform already provides.
- Motion that slides from a fixed physical side in a bidirectional product.
- Reduced motion implemented as "animations off", removing the feedback that told the user their click registered.

## Pairing

- Which CSS features are safe: `72-modern-css-baseline-tiers.md`
- Duration and easing tokens: `20-design-tokens-and-theming.md`
- Frame budget and interaction latency: `45-render-and-asset-budgets.md`
- Direction flipping: `05-rtl-and-persian.md`
- The motion gate and its proof: `90-quality-gates-and-review.md`, `95-design-proofs.md`
