# Typography and Color

Use this file when choosing fonts, building a type scale, constructing a palette, or judging contrast.

## Type scale and text rules

- Base body 16px (mobile included — below 16px triggers iOS auto-zoom); consistent scale, e.g. 12 / 14 / 16 / 18 / 24 / 32 / 48. Use `clamp()` for fluid display sizes.
- Line-height 1.5–1.75 for body; tighter (1.1–1.3) for large display text.
- Measure 45–75 characters; never edge-to-edge paragraphs on wide screens.
- Weight hierarchy: headings 600–700, body 400, labels/buttons 500. Weight and size carry hierarchy — not color alone.
- Tabular figures (`font-variant-numeric: tabular-nums`) for prices, timers, and data columns.
- Respect platform default letter-spacing; never tighten body tracking. `text-wrap: balance` for headings, `text-wrap: pretty` progressive-enhancement for body.
- Prefer wrapping over truncation; when truncating, use ellipsis plus a way to reach the full text.

## Pairing principles

- Maximum two families per product (display + body); a third only as monospace for code/data.
- Pair by contrast of personality, not similarity: expressive display + neutral body. Two similar-but-not-identical sans faces read as a mistake.
- Prefer variable fonts — one file, full weight range.
- Starting points (taste tier, not law):
  - modern SaaS / product UI: Inter, Geist, or system stack alone
  - premium / editorial: Playfair Display or Fraunces display + Inter/Source Sans body
  - playful / education: Nunito or Baloo display + readable neutral body
  - technical / dashboard: Inter or IBM Plex Sans + JetBrains Mono for data

## Farsi / RTL typography

For Farsi-first or bilingual Alaa products this section is mandatory, not optional:

- Primary Farsi families: Vazirmatn (general UI, variable), IRANSansX-class faces where licensed; pair with a Latin face of matching x-height and weight range for mixed content.
- Farsi needs larger line-height than Latin (1.7–2.0 body) and slightly larger sizes at equal perceived scale; verify the scale with real Farsi copy, not lorem.
- Use CSS logical properties (`margin-inline-start`, `padding-inline`, `text-align: start`) everywhere so the layout flips correctly under `dir="rtl"` — never left/right physical properties in RTL-capable UI.
- Numerals: decide Persian (۱۲۳) vs Latin (123) digits per product and apply consistently (`font-feature-settings`/locale formatting); mixed digit systems in one view are a defect.
- Subset fonts: load `arabic` + `latin` subsets only; Farsi webfonts are heavy and font-loading discipline matters more, not less.

## Font loading discipline

- `font-display: swap` (or `optional` for non-critical faces); preload only the one or two critical files.
- Self-host or use Google Fonts CSS2 API with explicit weights/subsets; never load whole families "just in case".
- Reserve space to avoid layout shift when the webfont lands (metric-compatible fallback via `size-adjust`/`ascent-override` when practical).

## Palette construction

- Build from product intent (`10-design-workflow.md`), then express as semantic tokens (`20-design-tokens-and-theming.md`). The palette is roles, not a list of pretty colors.
- Proportion: roughly 60% background/surfaces, 30% foreground/secondary, 10% accent. The accent is reserved for primary actions — if everything is accented, nothing is.
- Build tonal ramps in `oklch()` (perceptually uniform lightness steps); derive states with relative color syntax.
- Status colors (success/warning/destructive/info) are semantic tokens with AA-compliant foregrounds, and never the only signal — always paired with icon or text.

## Starter palettes

Taste-tier anchors, not law — adapt hues to the brand, keep the role structure, and re-verify every pair with a contrast checker before shipping:

| Intent | primary | on-primary | accent (CTA) | background | surface | foreground | muted-fg | border | destructive |
|---|---|---|---|---|---|---|---|---|---|
| SaaS / trust | `#2563EB` | `#FFFFFF` | `#EA580C` | `#F8FAFC` | `#FFFFFF` | `#1E293B` | `#64748B` | `#E2E8F0` | `#DC2626` |
| Dashboard / ops | `#3730A3` | `#FFFFFF` | `#0D9488` | `#F1F5F9` | `#FFFFFF` | `#0F172A` | `#475569` | `#CBD5E1` | `#B91C1C` |
| Premium (dark-first) | `#E7E5E4` | `#1C1917` | `#C9A962` | `#0C0A09` | `#1C1917` | `#FAFAF9` | `#A8A29E` | `#292524` | `#F87171` |
| Playful / education | `#7C3AED` | `#FFFFFF` | `#F59E0B` | `#FEFCE8` | `#FFFFFF` | `#292524` | `#57534E` | `#E7E5E4` | `#DC2626` |

Convert chosen values to `oklch()` and derive states per `20-design-tokens-and-theming.md`; record any contrast-driven adjustment next to the token.

## Contrast gates (blocking)

- Body text vs background >= 4.5:1; large text (>= 24px or 18.7px bold) >= 3:1; UI glyphs and meaningful graphics >= 3:1.
- Verify per theme with a checker — never by eye; record adjusted values in the token file ("accent darkened for 4.5:1 on surface").
- Gray-on-gray body text is the most common failure; muted text still must pass 4.5:1.

## Anti-patterns

- Three or more typefaces; decorative display faces used for body text.
- Type scale or palette that exists only in components, never as tokens.
- Farsi UI built with physical left/right properties, or checked only with English strings.
- A palette approved in light mode and assumed correct in dark mode.

## Pairing guidance

- Token wiring and dark-mode rules: `20-design-tokens-and-theming.md`
- Style-driven palette personality: `40-styles-and-visual-language.md`
- Contrast/gate verification before delivery: `90-quality-gates-and-review.md`
