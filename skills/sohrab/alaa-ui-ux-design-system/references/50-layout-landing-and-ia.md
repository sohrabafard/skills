# Layout, Landing Structure and Information Architecture

Read this file when setting a breakpoint, a container width, a section order, or the placement of a call to action.

## Layout defaults

- Mobile-first. Systematic breakpoints (375 / 768 / 1024 / 1440); never a per-component ad-hoc breakpoint.
- One consistent maximum content width per page type on desktop, with a readable measure inside it. No horizontal scroll at any supported width; verify 375px explicitly.
- 4/8 spacing rhythm from the token scale (`20-design-tokens-and-theming.md`). Vertical rhythm tiers by hierarchy level; sibling sections get equal spacing.
- Gutters grow with the viewport. Edge-to-edge only for a deliberate full-bleed section.
- `min-h-dvh` over `100vh`. The viewport meta never disables zoom.
- Layering from the z-index token scale only.
- Fixed headers and bars reserve space for the content beneath them, using scroll padding and content insets. Nothing hides behind sticky UI, including the focus ring of a control scrolled to by keyboard.
- Hierarchy comes from size, spacing and contrast. Colour reinforces it and never carries it alone.
- **Build with logical properties from the start** (`05-rtl-and-persian.md` section 5). A direction flip must be a `dir` switch, never a redesign.

## Page-type defaults

Defaults tier — deviate deliberately and say so.

- **Dashboard / ops:** full-width or a 1400px maximum, twelve columns, dense spacing tier, persistent sidebar from 1024px, tables and cards over decoration.
- **Landing / marketing:** centred container, spacious tier, section-based, one signature visual moment.
- **Checkout / critical flows:** a single narrow column, zero decorative distraction, a step indicator, conservative motion, no third-party embeds (`45-render-and-asset-budgets.md`).
- **Authentication:** a centred narrow card (360-420px), minimal chrome, one action per screen.
- **Pricing:** side-by-side comparison stacking on mobile, one recommended tier highlighted, questions below.
- **Settings / forms:** a section navigation beside a single-column form region; related fields grouped.
- **Blog / docs / editorial:** measure-first single column, in-page contents sticky on wide screens.

## Landing-page structure

Default section order; reorder with reasons.

1. Hero — the value proposition in one sentence, one primary action, one supporting visual
2. Social proof strip — logos, counts or ratings; proof before claims
3. Problem to solution framing
4. Features and benefits — bento or alternating rows; benefits phrased as outcomes
5. Deep proof — testimonials with name, role and photo (three to five), case numbers, a demo
6. Pricing, when public
7. Questions — objection handling
8. Final call to action — repeat the primary action; nothing new after it

Call-to-action strategy:

- **Exactly one primary action per screenful.** Secondary actions are visually subordinate.
- The accent role is spent only on primary actions (`32-starter-palettes.md`), never on decoration.
- The wording rule for the action itself is in `35-ux-writing-and-microcopy.md` and is not repeated here.
- **Above the fold must stand alone:** value proposition, action and one piece of proof visible without scrolling at 375px.

## Anti-patterns

- Fixed pixel container widths that break between breakpoints; desktop-first retrofitted to mobile.
- Equal visual weight on competing actions; the accent spent on decoration.
- A landing page that states features without proof, or buries the action below unexplained sections.
- Dense dashboard rhythm on a marketing page, or marketing rhythm on a dashboard.
- Sections whose internal spacing exceeds the spacing between sections.
- A sticky bar that covers the element the keyboard just focused.

## Pairing

- Spacing and density tokens: `20-design-tokens-and-theming.md`
- Direction and logical properties: `05-rtl-and-persian.md`
- Components and forms inside these layouts: `60-components-states-and-ux.md`
- Hero image and embed weight: `45-render-and-asset-budgets.md`
- Responsive verification in a real browser: `95-design-proofs.md`
