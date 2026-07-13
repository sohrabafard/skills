# Quality Gates and Design Review

Use this file before delivering any shipped UI, and for design/UX review requests. This is the single copy of the gates — other references point here instead of duplicating.

## Blocking gates

A design is not done while any of these fails. They are never traded for aesthetics:

1. Contrast: body text >= 4.5:1, large text and UI glyphs >= 3:1, per theme, verified with a checker.
2. Focus: visible focus-visible ring on every interactive element; keyboard reaches everything in visual order.
3. Labels: form fields have visible labels; icon-only buttons have `aria-label`; meaningful images have alt text.
4. Color is never the only signal for state, status, or data.
5. `prefers-reduced-motion` honored on every animated surface (`70-motion-and-modern-css.md` §5).
6. Touch targets >= 44x44px with >= 8px gaps; zoom never disabled.
7. Both themes shipped when dark mode exists — tested, not inferred from light.
8. Tokens, not raw values, in components; one icon family; effects coherent with the declared style.
9. No layout shift from media, fonts, async content, or hover states.
10. RTL products: layout verified under `dir="rtl"` with real Farsi content.

## Review workflow

For "review this UI/design" requests:

1. Read the persisted design system (MASTER.md / tokens) first — findings are deviations from the repo's own contract, then from this pack's gates and defaults.
2. Pass in severity order: gates -> consistency (tokens, spacing rhythm, icon family, style coherence) -> UX patterns (states, forms, navigation per `60-components-states-and-ux.md`) -> taste (offer, don't impose).
3. Report each finding as: what, where, severity (blocker / high / polish), and the smallest concrete fix. Do not pad reviews with taste rewrites of working design.
4. Static inspection first (source, tokens, templates); browser evidence only per `$alaa-frontend-developer` browser gating, with `playwright_visual` for layout/responsive/theme proof.

## Pre-delivery checklist

Run once, honestly, before calling UI work done:

- [ ] Gates 1–10 above pass
- [ ] All component states designed and reachable (default/hover/focus/active/disabled/loading/error/empty)
- [ ] 375px and desktop verified; no horizontal scroll; nothing hidden behind fixed bars
- [ ] Dark and light themes verified independently (when both exist)
- [ ] Reduced-motion emulated and acceptable
- [ ] Spacing follows the token rhythm; z-index only from the scale
- [ ] One primary CTA per screen; accent color spent only on actions
- [ ] Empty/error/edge content (long text, zero items, slow network) does not break the layout
- [ ] Favicon/OG set present for public-facing products (`80-icons-assets-and-imagery.md`)

What was not checked gets said explicitly — an unchecked box is a statement, not a failure.

## Severity model

- Blocker: a gate fails, or the UI misleads (fake affordance, invisible focus, color-only status).
- High: consistency break (off-token values, mixed icon sets, rhythm violations), missing states, broken responsive behavior.
- Polish: taste-tier improvements — propose with rationale, never block on them.

## Pairing guidance

- Engineering verification (SSR, hydration, PWA, perf evidence): `$alaa-frontend-developer` `references/50-qa-and-verification.md`
- Browser-based visual proof: `$playwright` / `playwright_visual`
- Component/UX pattern details behind the checklist: `60-components-states-and-ux.md`
