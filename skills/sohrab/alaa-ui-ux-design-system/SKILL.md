---
name: alaa-ui-ux-design-system
description: "Use this skill when the task involves UI/UX design decisions: design systems, design tokens, theming, dark mode, color palettes, typography, spacing, layout, landing-page structure, visual style selection, component states and designed failure states, shared component libraries, UX writing and microcopy, RTL and Persian typography, motion language, modern CSS platform features, icons, imagery, favicons, data-viz design, accessibility patterns, render and asset budgets, or design review for Vue/Quasar apps styled with Tailwind or Bootstrap. Do not use it for pure frontend engineering (SSR, hydration, auth, PWA, performance plumbing) with no visual-design decision, for exact Quasar API or config lookup, or when the repo already has a complete design system and the task only applies its existing tokens mechanically."
---

# Alaa UI/UX Design System

## Purpose

The design-intelligence layer for the Vue 3 + Quasar + Vite app family, styled with Tailwind or Bootstrap. It owns art direction, tokens, theming, typography, color, layout, RTL and Persian rendering, motion, icons, and design-quality review.

The floor is the gate list in `references/90-quality-gates-and-review.md`. No rule in this pack may forbid a visual choice that passes every gate in that list.

## When NOT to use

Stop and route when the task carries **no visual-design decision** — frontend engineering, SSR, auth, PWA plumbing or performance work; when it needs an exact Quasar API, prop or config key, by the deciding test that a rule surviving a change of component library is this skill's and a rule naming a Quasar symbol is not; or when the repository already has a complete design system and the task only applies its existing tokens mechanically. The ownership section below names each owner.

## Design authority model

Every rule in this pack belongs to exactly one tier. Never confuse them.

1. **Gates (blocking):** the numbered list in `references/90-quality-gates-and-review.md`. A design is not done while one fails, and none is skippable by disclosure.
2. **Defaults (overridable by a repo token file or explicit user direction, never by drift):** spacing scale, duration and easing tokens, type scale, breakpoints, z-index scale, landing section order.
3. **Taste (free creative space):** style selection, palette personality, imagery, composition, voice. This pack supplies trade-offs; it never mandates. When the user asks for bold, be bold inside the gates.

## Ownership and disclaimers

This skill owns design direction, tokens, typography and color, visual style, layout and IA, component and failure-state design, RTL and Persian rendering, motion, icons and imagery, render budgets, and the design gates. It owns none of the following and cites rather than restates them:

| Ground | Owner |
|---|---|
| The quality bar itself, breaking-change doctrine | `/alaa-project-constitution` (`$alaa-project-constitution`) |
| Every registered name and value: metric and event names, permission-bit meanings, Jalali-vs-Gregorian wire format | `/alaa-services-contract` (`$alaa-services-contract`) |
| Folding Persian, Arabic and other non-ASCII digits to ASCII at every input boundary | `/alaa-input-normalization` (`$alaa-input-normalization`) |
| The permission-bitmap decoder | `/alaa-permission-generator` (`$alaa-permission-generator`) |
| The server-side authorization boundary | `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) |
| Requirement levels for anything emitted from the UI | `/alaa-observability-soc` (`$alaa-observability-soc`) |
| Threat classes for untrusted content, `v-html`, paste | `/alaa-security-review` (`$alaa-security-review`) |
| Degradation doctrine behind offline, slow and partial states | `/alaa-reliability-sla` (`$alaa-reliability-sla`) |
| Test design and the proof levels behind any check named here | `/alaa-testing-strategy` (`$alaa-testing-strategy`) |
| Visual-regression baseline storage and CI wiring | `/alaa-frontend-devops` (`$alaa-frontend-devops`) |
| Combinatorial-explosion doctrine behind the theme matrix | `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) |
| Pre-implementation design of a page or flow before pixels | `/alaa-system-design` (`$alaa-system-design`) |
| Frontend engineering, Lighthouse scoring, browser gating | `/alaa-frontend-developer` (`$alaa-frontend-developer`) |
| Component code shape, typing, composables | `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`) |
| Runtime and effort doctrine across agent families | `/alaa-prompting-guide` (`$alaa-prompting-guide`) |
| Output discipline | `/alaa-low-noise` (`$alaa-low-noise`) |

**The Quasar seam, deciding test:** a rule that would still hold if the component library were replaced belongs here; a rule that names a Quasar prop, plugin, directive or config key belongs to `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`). The token that feeds `app.scss` is ours; the `setCssVar` call and the `transition-show` prop name are not.

React, React Native and non-web desktop stacks are out of scope.

## Router

`references/00-topic-map.md` is the only router in this skill. Open it unless you already know the exact reference file, then load the smallest one that answers the question.

## Five rules that hold without reading any file

1. A color, spacing, radius, shadow or z-index value written into a component is a defect; components consume semantic tokens only.
2. Contrast, visible focus, keyboard reach and `prefers-reduced-motion` block delivery. They are never traded for aesthetics and never waived by disclosure.
3. Direction is set with the `dir` attribute and CSS. Never insert U+200E, U+200F or U+2066-U+2069 into content, and never treat a rendered Persian digit as evidence of the stored value.
4. Hiding or disabling a control is a presentation choice and never a security control. The server re-checks every action.
5. A design rule with no tool that reports its violation is a preference. Run `scripts/check-design-system.mjs` before claiming a token, theme, contrast or RTL-icon rule holds.

## Entry protocol

This is not the design procedure; the only ordered design procedure in this pack is in `references/10-design-workflow.md`. Before routing:

1. Read the repo-local `AGENTS.md` and the repo's own token and theme sources. Repo tokens outrank every default in this pack.
2. Apply `/alaa-low-noise` (`$alaa-low-noise`).
3. Open `references/00-topic-map.md`.

## Maintenance rules

- Keep exactly one copy of every rule. Route instead of duplicating between references.
- Platform-version claims live only in `references/72-modern-css-baseline-tiers.md`, each with its own `read:` date. Re-verify that file when a task depends on a Tier 2 or Tier 3 feature, or when its stamps are more than 90 days older than today.
- Never promote a taste-tier rule to a gate; a new gate needs a check in `scripts/check-design-system.mjs` or a named manual proof in `references/95-design-proofs.md`.
- Repo-local `AGENTS.md`, existing repo tokens, and user instructions override this shared skill.
