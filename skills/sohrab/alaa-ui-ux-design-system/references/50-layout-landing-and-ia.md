# Layout, Landing Structure, and Information Architecture

Use this file for page layout rules, responsive behavior, page-type defaults, and landing-page structure.

## Layout defaults

- Mobile-first; systematic breakpoints (375 / 768 / 1024 / 1440) — never per-component ad-hoc breakpoints.
- Consistent max content width per page type on desktop; readable measure inside it. No horizontal scroll at any supported width; verify 375px explicitly.
- 4/8px spacing rhythm from the token scale (`20-design-tokens-and-theming.md`); vertical rhythm tiers (e.g. 16/24/32/48) by hierarchy level — sibling sections get equal spacing.
- Gutters grow with viewport; edge-to-edge only for deliberate full-bleed sections.
- `min-h-dvh` over `100vh`; `viewport` meta never disables zoom.
- Layered z-index from the token scale only.
- Fixed headers/bars reserve space for underlying content (scroll-padding, content insets); nothing hides behind sticky UI.
- Hierarchy via size, spacing, and contrast — color is reinforcement, never the only carrier.
- RTL: build with logical properties from the start (`30-typography-and-color.md`); a Farsi flip must be a `dir` switch, not a redesign.

## Page-type layout defaults

Defaults tier — deviate deliberately:

- Dashboard / ops: full-width or 1400px, 12-column, dense spacing tier, persistent sidebar >= 1024px, tables and cards over decoration.
- Landing / marketing: centered container, spacious tier, section-based, one signature visual moment.
- Checkout / critical flows: single narrow column, zero decorative distraction, step indicator, conservative motion.
- Auth: centered narrow card (360–420px), minimal chrome, one action per screen.
- Pricing: side-by-side comparison (stack on mobile), one recommended tier highlighted, FAQ below.
- Settings / forms: left section-nav plus single-column form region; group related fields.
- Blog / docs / editorial: measure-first single column, sticky in-page TOC on wide screens.

## Landing-page structure

Section-order playbook (default, reorder with reasons):

1. Hero — value proposition in one sentence, one primary CTA, one supporting visual
2. Social proof strip — logos, counts, or ratings (proof before claims)
3. Problem -> solution framing
4. Features / benefits — bento or alternating rows; benefits phrased as outcomes
5. Deep proof — testimonials with name+role+photo (3–5), case numbers, demo
6. Pricing (when public)
7. FAQ — objection handling
8. Final CTA — repeat the primary action; nothing new after it

CTA strategy:

- Exactly one primary CTA per screenful; secondary actions visually subordinate (ghost/link).
- The accent color is spent only on CTAs (`30-typography-and-color.md`); repeated final CTA closes the page.
- CTA copy is a verb with an outcome ("Start learning free"), not "Submit".
- Above-the-fold must stand alone: value proposition + CTA + proof visible without scrolling on 375px.

## Anti-patterns

- Fixed pixel container widths that break between breakpoints; desktop-first retrofitted to mobile.
- Equal visual weight on competing CTAs; accent color spent on decoration.
- Landing pages that state features without proof, or bury the CTA below unexplained sections.
- Dense dashboard patterns on marketing pages and vice versa (one spacing tier per page type).
- Sections whose internal spacing exceeds the spacing between sections (rhythm inversion).

## Pairing guidance

- Spacing/density tokens: `20-design-tokens-and-theming.md`
- Component-level states and forms inside these layouts: `60-components-states-and-ux.md`
- Responsive verification in a real browser: `$playwright` / `playwright_visual` via `$alaa-frontend-developer` QA gating
