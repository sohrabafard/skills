# Quality Gates and Design Review

Read this file before delivering any shipped UI, and for every "review this design" request. **This is the single copy of the gates.** Every other file in this pack points here rather than restating a threshold.

## Blocking gates

A design is not done while any of these fails. None is traded for aesthetics, and **none is skippable by disclosing that it was skipped.** An unverified gate blocks delivery exactly as a failed one does.

Conformance target: **WCAG 2.2 Level AA** (`85-accessibility-patterns.md`). Where a gate is stricter than the standard, it says so.

1. **Contrast.** Body text at least 4.5:1 against its background; large text (24px, or 18.7px bold) and meaning-bearing graphics at least 3:1. Measured per theme with a tool, never by eye. (WCAG 1.4.3, 1.4.11.)
2. **Focus.** A visible focus-visible indicator on every interactive element; the keyboard reaches everything in visual order; a focused element is never obscured by sticky UI. (2.4.7, 2.4.3, 2.4.11.)
3. **Names.** Every form field has a visible label; every icon-only control has an accessible name; every meaningful image has descriptive alt text and every decorative image an empty one. (1.1.1, 3.3.2, 4.1.2.)
4. **Colour is never the only signal** for state, status, selection or a data series. (1.4.1.)
5. **`prefers-reduced-motion` is honoured** on every animated surface (`70-motion-contract.md`). (2.3.3.)
6. **Touch targets at least 44x44 CSS px with at least 8px between them; zoom is never disabled.** *Stricter than the standard by choice:* WCAG 2.2 AA (2.5.8) requires 24x24; 44x44 is the platform convention and this pack keeps it. (1.4.4, 1.4.10.)
7. **Both themes ship when dark mode exists**, each measured independently. Every theme declares every semantic role (`20-design-tokens-and-theming.md`).
8. **Tokens, not raw values, in components.** One icon family. Effects derivable from the recorded style row.
9. **No layout shift** from media, fonts, async content, or hover and focus states.
10. **RTL products render correctly under both directions** with real Persian content: logical properties, mirrored direction-bearing icons, direction-aware motion, correct LTR islands (`05-rtl-and-persian.md`).
11. **Every data-bearing surface designs its failure states** and they are distinguishable from each other: empty, error, not permitted, offline (`15-designed-failure-states.md`).
12. **No fake affordance.** No control that looks actionable and cannot act, none that looks inert and will act, and no state indicator reporting an unconfirmed result. No flow whose safety depends on a hidden control (`25-untrusted-content-and-ui-authority.md`).
13. **Performance-affecting design choices stay inside the budgets.** The hero or LCP visual is server-renderable and optimizable, every async surface reserves its space, fonts are subset with metric-matched fallbacks, and heavy third-party embeds ship as facades. Design ceilings are in `45-render-and-asset-budgets.md`; the canonical scoring playbook and its target value are owned by `/alaa-frontend-developer` (`$alaa-frontend-developer`) `references/41-lighthouse-and-web-vitals.md` and are not restated anywhere in this pack.

Gates 1, 7, 8 and 10 are partly machine-checkable: `scripts/check-design-system.mjs` reports on contrast, theme role completeness, token drift and direction-bearing icons. A passing script is not a passing gate — it is the part of the gate a machine can see.

## Review workflow

For a "review this UI" request:

1. **Read the persisted design system first** — `MASTER.md`, the token file, the component index. A finding is a deviation from the repo's own contract before it is a deviation from this pack.
2. **Pass in severity order:** gates, then consistency (tokens, spacing rhythm, icon family, style coherence), then UX patterns (interaction states, failure states, forms, navigation), then taste — which is offered, never imposed.
3. **Report each finding as:** what, where (`file:line`), severity, and the smallest concrete fix. Do not pad a review with taste rewrites of working design.
4. **Static inspection first** — source, tokens, templates, and the checker. Browser evidence follows `/alaa-frontend-developer` (`$alaa-frontend-developer`) browser gating, with visual tooling for layout, responsive and theme proof.

## Pre-delivery checklist

Run once, honestly, before calling UI work done.

- [ ] Gates 1-13 above pass, each verified rather than assumed
- [ ] `scripts/check-design-system.mjs` run, and its output attached or its failure explained
- [ ] All interaction states designed and reachable (`60-components-states-and-ux.md`)
- [ ] All failure states designed and distinguishable (`15-designed-failure-states.md`)
- [ ] 375px and desktop verified; no horizontal scroll; nothing hidden behind fixed bars
- [ ] Both themes verified independently, where both exist
- [ ] Both directions verified with real Persian content, where the product is bidirectional
- [ ] Reduced motion emulated and acceptable
- [ ] The theme-matrix cells named mandatory in `45-render-and-asset-budgets.md` verified, and the rest listed as unverified
- [ ] Spacing follows the token rhythm; z-index only from the scale
- [ ] One primary action per screen; the accent spent only on actions
- [ ] Long text, zero items, thousands of items and a slow connection do not break the layout
- [ ] Every error surface carries a copyable reference (`28-ui-diagnosability.md`)
- [ ] Favicon and social-image set present for a public-facing product

**Gates 1-13 are not skippable; an unverified gate blocks delivery.** The remaining checklist items may be reported unchecked with a stated reason — that is a statement about coverage, not a waiver.

## Severity model

- **Blocker:** a gate fails or is unverified.
- **High:** a consistency break (off-token values, mixed icon sets, rhythm violations), a missing state, or broken responsive behaviour.
- **Polish:** taste-tier improvement. Proposed with a rationale, never blocking.

## Pairing

- How to satisfy the accessibility gates well: `85-accessibility-patterns.md`
- What each verification must leave behind: `95-design-proofs.md`
- Engineering verification, SSR and performance evidence: `/alaa-frontend-developer` (`$alaa-frontend-developer`) `references/50-qa-and-verification.md`
- Test design behind these checks: `/alaa-testing-strategy` (`$alaa-testing-strategy`)
