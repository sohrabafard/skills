# Typography and Color

Read this file when choosing fonts, building a type scale, constructing a palette, or judging whether two colors may sit on each other. Persian and RTL typography is in `05-rtl-and-persian.md`; this file covers what is common to both directions.

## Type scale and text rules

- Base body 16px on every viewport including mobile — below 16px triggers iOS auto-zoom on focus. One scale, e.g. 12 / 14 / 16 / 18 / 24 / 32 / 48. `clamp()` for fluid display sizes only.
- Line-height 1.5 to 1.75 for Latin body; 1.1 to 1.3 for large display text. Persian values are in `05-rtl-and-persian.md` section 6 and are higher.
- Measure 45 to 75 characters. Never edge-to-edge paragraphs on wide screens.
- Weight hierarchy: headings 600 to 700, body 400, labels and buttons 500. Weight and size carry hierarchy; color never carries it alone.
- `font-variant-numeric: tabular-nums` for prices, timers, counters and any column of numbers.
- Respect the platform default letter-spacing; never tighten body tracking.
- Prefer wrapping over truncation. When truncating, ship a way to reach the full text, and make the truncation visible rather than a clipped edge.

## Pairing

- At most two families per product (display plus body); a third only as monospace for code and data.
- Pair by contrast of personality, not similarity. Two similar-but-not-identical sans faces read as a mistake.
- Prefer variable fonts: one file, full weight range, smaller total transfer.
- Starting points (taste tier). Licences are stated because an unstated licence is the defect: Inter (SIL OFL), Geist (SIL OFL), IBM Plex Sans (SIL OFL), JetBrains Mono (SIL OFL), Playfair Display (SIL OFL), Fraunces (SIL OFL), Nunito (SIL OFL), Baloo (SIL OFL) — all `read: unverified as of 2026-07-28` for the specific version you ship. **Verify the licence file in the package you actually install; a family name is not a licence.**
  - modern SaaS or product UI: Inter, Geist, or the system stack alone
  - premium or editorial: Playfair Display or Fraunces display plus a neutral body
  - playful or education: Nunito or Baloo display plus a readable neutral body
  - technical or dashboard: Inter or IBM Plex Sans plus JetBrains Mono for data

**Licence rule with an adjudicator:** a face whose licence permits web embedding for this product either carries an open licence in its own package, or the repository contains a licence file naming this product. If neither is true, do not ship it — substitute an OFL face and state the substitution in the delivery note. Nobody's judgement substitutes for the file.

## Font loading

- `font-display: swap`, or `optional` for non-critical faces.
- Preload at most two files, and only files used above the fold.
- Self-host, or load from a CDN with explicit weights and subsets. Never load a whole family "just in case".
- Reserve space so the swap does not shift layout: a metric-compatible fallback with `size-adjust` and `ascent-override` where practical.
- The byte budget for fonts is in `45-render-and-asset-budgets.md` and is enforced, not advisory.

## Palette construction

- Build from product intent (`10-design-workflow.md`), then express as semantic roles (`20-design-tokens-and-theming.md`). A palette is a set of roles, not a list of pretty colors.
- Proportion: roughly 60% background and surfaces, 30% foreground and secondary, 10% accent. The accent is reserved for primary actions; if everything is accented, nothing is.
- Build tonal ramps in `oklch()` so lightness steps are perceptually even, and derive states with relative color syntax.
- Status colors are semantic roles with measured foregrounds, and are never the only signal — always paired with an icon, a label, or a shape.
- Validated starting tables with printed ratios: `32-starter-palettes.md`.

## Contrast

The thresholds themselves are gates and live in `90-quality-gates-and-review.md`. This section is how to satisfy them.

- **Measure, do not judge.** `scripts/check-design-system.mjs --contrast <theme-file>` computes every `on-*` / fill pair, every foreground against every surface it can appear on, and every boundary role, per theme block. Eyeballing a pair is not verification, and a pair that "looks fine" at 3.9:1 is the most common failure in this pack's history.
- **Record the adjustment next to the token**, with the ratio: `/* accent darkened to reach 4.55 on-accent */`. A value with no recorded reason will be reverted by the next person who thinks it looks dull.
- **Gray-on-gray body text is the most common failure.** Muted text is still body text and still needs the body threshold; "muted" is not an exemption.
- **A gradient, image or glass surface behind text has no single background color.** Measure against the lightest and darkest pixel the text can sit on, and if either fails, put the text on a solid surface instead. This is why `40-styles-and-visual-language.md` warns off text on aurora and glass.
- **Disabled controls are exempt from the text threshold** and are not exempt from being distinguishable: a disabled control must still be tellable from an enabled one and from a read-only one, by more than opacity alone.
- `contrast-color()` can pick a passing foreground automatically for a known fill; see `72-modern-css-baseline-tiers.md` for its status before relying on it, and note that it does not remove the need to measure — it removes the need to guess.

## Anti-patterns

- Three or more typefaces; a decorative display face used for body text.
- A type scale or palette that exists only in components and never as tokens.
- Shipping a face whose licence nobody checked.
- A palette approved in light mode and assumed correct in dark.
- Muted body text exempted from the contrast threshold because it is meant to be quiet.
- Text placed on a gradient and measured against one of its stops.

## Pairing

- Persian faces, line heights, subsetting and digits: `05-rtl-and-persian.md`
- Token wiring and dark-mode rules: `20-design-tokens-and-theming.md`
- Validated starting palettes: `32-starter-palettes.md`
- Style-driven palette personality: `40-styles-and-visual-language.md`
- Font and image byte budgets: `45-render-and-asset-budgets.md`
- The contrast gate: `90-quality-gates-and-review.md`
