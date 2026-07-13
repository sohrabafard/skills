---
name: alaa-ui-ux-design-system
description: "Use this skill when the task involves UI/UX design decisions: design systems, design tokens, theming, dark mode, color palettes, typography, spacing, layout, landing-page structure, visual style selection, component states, shared component libraries, UX writing and microcopy, motion and animation language, modern CSS platform features, icons, imagery, favicons, data-viz design, accessibility patterns, or design review for Vue/Quasar apps styled with Tailwind or Bootstrap. Do not use it for pure frontend engineering (SSR, hydration, auth, PWA, performance plumbing) with no visual-design decision."
---

# Alaa UI/UX Design System

## Purpose

Use this as the default design-intelligence skill for the Vue 3 + Quasar + Vite app family, styled with Tailwind or Bootstrap. It owns the visual-design and UX decision layer that `$alaa-frontend-developer` deliberately does not: art direction, design tokens, theming, typography, color, layout aesthetics, motion language, icons/assets, and design-quality review.

This skill provides vocabulary, decision rules, and hard quality gates — not a fixed aesthetic. It must raise the floor (accessibility, consistency, honest trade-offs) without lowering the ceiling (the agent's creative range).

## Cross-agent portability

This skill uses the core Agent Skills format so OpenAI Codex/GPT-5.x agents and Claude (Opus/Sonnet/Fable) agents can all load it. Keep `SKILL.md` frontmatter limited to `name` and `description`; `agents/openai.yaml` is optional Codex UI metadata that other agents ignore. Do not add Claude-only frontmatter unless the skill is intentionally forked.

For every model family, treat this skill as an enforced design contract: outcome-first execution, repository evidence (existing tokens and components) before proposals, small focused changes, and honest validation against the gates. The references are written to be self-sufficient — an agent with no prior design training can follow them; an agent with strong design instincts keeps full creative freedom inside the gates.

## Design authority model

Every rule in this pack belongs to exactly one tier. Never confuse them:

1. **Gates (blocking, non-negotiable):** WCAG contrast, visible focus, keyboard reachability, `prefers-reduced-motion`, touch-target minimums, color-never-the-only-signal, zoom never disabled, one consistent icon family, tokens instead of raw hex in components. A design is not done while a gate fails.
2. **Defaults (strong, overridable by repo tokens or explicit user direction):** spacing scale, duration/easing tokens, type scale, breakpoint set, z-index scale, landing section orders. Override deliberately, not by drift.
3. **Taste (guidance, free creative space):** style selection, palette personality, imagery, composition, voice. This pack informs these choices with honest trade-offs; it never mandates them. When the user asks for something bold, be bold — inside the gates.

## Ownership

- `alaa-ui-ux-design-system` owns design direction, tokens/theming, typography/color, visual style, layout and landing structure, component-state and UX design, motion language, modern-CSS design features, icons/assets/imagery, and design-quality gates.
- `$alaa-frontend-developer` owns frontend engineering: SSR/hydration safety, auth/session, PWA/SW, performance and realtime plumbing, API shaping, QA planning, browser-debug flow. Pair with it whenever a design decision must be implemented in the app family.
- `$alaa-vue-typescript-clean-code` owns component code quality; `$alaa-quasar-app-vite-v3` owns exact Quasar APIs, transition props, `app.scss`, and build behavior.
- `$playwright` / `playwright_visual` own visual verification in a real browser; browser use stays opt-in per `$alaa-frontend-developer` rules.
- React, React Native, and non-web desktop UI stacks are out of scope. The target stack is Vue 3 + Quasar, with Tailwind or Bootstrap per repo.

## When to use

Use this skill when the task includes any of the following:

- creating or evolving a design system, design tokens, or theme (including dark mode)
- choosing a visual style, color palette, font pairing, spacing scale, or layout direction
- designing a new page, landing page, dashboard, or flow — structure, hierarchy, CTA strategy
- component visual design: states, forms, feedback, navigation patterns, empty/error/loading states
- animation, transitions, motion polish, or modern-CSS design features (View Transitions, container queries, `oklch`, `light-dark()`, scroll-driven animations)
- icons, brand assets, imagery, favicons, Open Graph images, or illustration direction
- chart and data-visualization design decisions
- reviewing existing UI for visual consistency, UX quality, or accessibility-as-design
- a UI "looks unprofessional" and the cause is unclear

## When NOT to use

Do not use this skill when:

- the task is pure frontend engineering with no visual decision — use `$alaa-frontend-developer`
- the task is exact Quasar API/config lookup — use `$alaa-quasar-app-vite-v3`
- the task is backend, infra, or non-visual work
- the repo already has a complete design system and the task only applies existing tokens mechanically

## Quick start

1. Read the repo-local `AGENTS.md` and any existing design-system artifacts (`DESIGN.md`, `design-system/`, theme/token files, `tailwind.config`/`@theme`, Bootstrap variable overrides, `app.scss`). Existing repo tokens outrank this skill's defaults.
2. Apply `$alaa-low-noise`.
3. Scale the process to the task — do not run the full workflow for a small tweak:
   - new product, site, or major redesign -> full design brief and direction per `references/10-design-workflow.md`
   - new page or feature in an existing system -> page-level spec; reuse existing tokens and style
   - component tweak or bug -> follow existing tokens; load only the single relevant reference
4. Start with `references/00-topic-map.md` unless you already know the exact reference to load, and load only the smallest relevant reference file.
5. Before delivering, run the gates in `references/90-quality-gates-and-review.md`.

## Routing map

- Design workflow, product-type-to-direction mapping, design brief, persisted design decisions (master + page overrides):
  - `references/10-design-workflow.md`
- Design tokens, semantic color roles, theming, dark mode, spacing/radius/shadow/z-index scales, Tailwind/Bootstrap/Quasar token mapping:
  - `references/20-design-tokens-and-theming.md`
- Typography (scale, pairing, loading, Farsi/RTL) and color (palette construction, starter palettes, contrast, status colors):
  - `references/30-typography-and-color.md`
- UX writing and microcopy (voice, buttons, errors, empty states, Farsi register and نیم‌فاصله discipline):
  - `references/35-ux-writing-and-microcopy.md`
- Visual style vocabulary with honest trade-offs (minimalism, glassmorphism, brutalism, bento, aurora, ...) and style-coherence rules:
  - `references/40-styles-and-visual-language.md`
- Layout, responsive rules, page-type layout defaults, landing-page structure and CTA strategy:
  - `references/50-layout-landing-and-ia.md`
- Shared component libraries, component API design, wrapping Quasar, design-system governance and drift control:
  - `references/55-component-library-and-governance.md`
- Component states, forms and feedback, navigation patterns, empty/loading/error design, chart and data-viz design:
  - `references/60-components-states-and-ux.md`
- Modern CSS platform features (Baseline tiers) and the classy-motion contract (durations, easing, stagger, reduced-motion, compositor rules):
  - `references/70-motion-and-modern-css.md`
- Icons, brand assets, imagery, favicons/OG images, illustration direction:
  - `references/80-icons-assets-and-imagery.md`
- Accessibility patterns (semantic structure, native-first ARIA, focus management, keyboard, live regions):
  - `references/85-accessibility-patterns.md`
- Blocking quality gates, design review workflow, pre-delivery checklist:
  - `references/90-quality-gates-and-review.md`

## Mandatory cross-topic rules

Apply these even when the user names only one surface:

- Any new palette, theme, or dark-mode task:
  - Also load `references/20-design-tokens-and-theming.md`; express every color as a semantic token.
  - Dark mode is designed together with light mode and contrast-tested separately — never inverted mechanically.
- Any animation, transition, or motion task:
  - Also load `references/70-motion-and-modern-css.md`.
  - Treat `prefers-reduced-motion` support as a blocking gate, not polish.
- Any style-selection task:
  - Also load `references/40-styles-and-visual-language.md`; check the style's "do not use for" column before committing.
  - Generated boilerplate (radius, shadows, transitions) must match the chosen style — never inject default rounded-soft styling into a style that forbids it.
- Any shared/reusable component task (creating, promoting, or changing one):
  - Also load `references/55-component-library-and-governance.md`; search the existing library before building anything new.
- Any user-facing copy task (buttons, errors, empty states, notifications) and any Farsi UI text:
  - Also load `references/35-ux-writing-and-microcopy.md`.
- Any icon or image task:
  - Also load `references/80-icons-assets-and-imagery.md`. No emoji as UI icons; one icon family per product.
- Any custom interactive widget, overlay, or SPA navigation flow:
  - Also load `references/85-accessibility-patterns.md`; native elements before ARIA.
- Any hero, imagery, font, effect, or embed decision on a route that will be Lighthouse-scored:
  - Design inside the performance budgets; the canonical scoring playbook is `$alaa-frontend-developer` `references/41-lighthouse-and-web-vitals.md` (target >= 90 mobile).
- Any task that ends in shipped UI:
  - Run the gates in `references/90-quality-gates-and-review.md` before calling it done.
- Any design decision that requires Vue/Quasar/Vite implementation, SSR safety, or verification planning:
  - Pair with `$alaa-frontend-developer`; it owns the engineering constraints and QA workflow.

## Companion chooser

| If the task is mainly about...                                       | Pair with                        |
|----------------------------------------------------------------------|----------------------------------|
| implementing the design in Vue/Quasar/Vite, SSR safety, QA planning  | `$alaa-frontend-developer`       |
| component code quality, composables, typing                          | `$alaa-vue-typescript-clean-code`|
| exact Quasar components, transitions, `app.scss`, build              | `$alaa-quasar-app-vite-v3`       |
| headed visual QA, screenshots, responsive checks                     | `$playwright` / `playwright_visual` |
| CI/deploy impact of asset or theme changes                           | `$alaa-frontend-devops`          |

## Maintenance rules

- Keep this skill focused on one job: design intelligence for the Vue 3 + Quasar app family with Tailwind or Bootstrap.
- Keep exactly one copy of every rule; route instead of duplicating between references.
- Re-check Baseline status for the features in `references/70-motion-and-modern-css.md` as Baseline and Interop cycles progress (last verified 2026-07-08).
- Keep gates, defaults, and taste clearly separated when adding rules; never promote taste to a gate.
- Repo-local `AGENTS.md`, existing repo design tokens, and user instructions always override this shared skill.
