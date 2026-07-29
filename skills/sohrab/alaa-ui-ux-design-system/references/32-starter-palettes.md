# Starter Palettes

Read this file when a product has no palette at all and you want a starting point that already passes the contrast gate. Adapt the hues to the brand; keep the role structure and re-run the checker after any change.

**Every value below was computed, not asserted.** The ratio beside each pair is the WCAG contrast ratio of that pair as shipped, produced by `scripts/check-design-system.mjs --palettes` on 2026-07-28. **A row with no printed ratio is not a starting point** — it is an untested guess, and shipping one is worse than shipping none.

## How to read the tables

- `oklch(L C H)` is the canonical form; the hex beside it is the sRGB rendering for tooling that cannot take `oklch()`. Derive hover, active and disabled states from these with relative color syntax, never by hand-picking a second value.
- `on-*` roles are the foreground that sits **on** that fill. **Do not assume white.** White fails on every accent in this file; that is the single most common palette defect and the reason this column exists.
- `border-subtle` separates surfaces decoratively and carries no contrast requirement. `border-strong` is the visible boundary of a control — an input whose only edge is its border — and must reach 3:1 against the adjacent surface. Using `border-subtle` as an input's only boundary is a defect.
- Every palette here is expressed for one theme. A dark counterpart is designed and measured separately; see `20-design-tokens-and-theming.md`.

## SaaS / trust

| Role | `oklch()` | sRGB | Measured pair | Ratio | Requirement |
|---|---|---|---|---|---|
| `primary` | `oklch(0.546 0.215 262.9)` | `#2563EB` | `primary` / `surface` | 5.17 | 3.0 |
| `on-primary` | `oklch(1 0 0)` | `#FFFFFF` | `on-primary` / `primary` | 5.17 | 4.5 |
| `accent` | `oklch(0.646 0.194 41.1)` | `#EA580C` | `accent` / `surface` | 3.56 | 3.0 |
| `on-accent` | `oklch(0.255 0.086 36.7)` | `#430D00` | `on-accent` / `accent` | 4.55 | 4.5 |
| `background` | `oklch(0.984 0.003 247.9)` | `#F8FAFC` | `foreground` / `background` | 13.98 | 4.5 |
| `surface` | `oklch(1 0 0)` | `#FFFFFF` | — | — | — |
| `foreground` | `oklch(0.280 0.037 260.0)` | `#1E293B` | `foreground` / `surface` | 14.63 | 4.5 |
| `muted-foreground` | `oklch(0.554 0.041 257.4)` | `#64748B` | `muted-foreground` / `surface` | 4.76 | 4.5 |
| `border-subtle` | `oklch(0.929 0.013 255.5)` | `#E2E8F0` | decorative | 1.23 | none |
| `border-strong` | `oklch(0.665 0.013 259.8)` | `#8F949C` | `border-strong` / `surface` | 3.05 | 3.0 |
| `destructive` | `oklch(0.577 0.215 27.3)` | `#DC2626` | `destructive` / `surface` | 4.83 | 4.5 |

## Dashboard / ops

| Role | `oklch()` | sRGB | Measured pair | Ratio | Requirement |
|---|---|---|---|---|---|
| `primary` | `oklch(0.398 0.177 277.4)` | `#3730A3` | `primary` / `surface` | 9.93 | 3.0 |
| `on-primary` | `oklch(1 0 0)` | `#FFFFFF` | `on-primary` / `primary` | 9.93 | 4.5 |
| `accent` | `oklch(0.600 0.104 184.7)` | `#0D9488` | `accent` / `surface` | 3.74 | 3.0 |
| `on-accent` | `oklch(0.219 0.039 183.2)` | `#00201C` | `on-accent` / `accent` | 4.58 | 4.5 |
| `background` | `oklch(0.968 0.007 247.9)` | `#F1F5F9` | `foreground` / `background` | 16.30 | 4.5 |
| `surface` | `oklch(1 0 0)` | `#FFFFFF` | — | — | — |
| `foreground` | `oklch(0.208 0.040 265.8)` | `#0F172A` | `foreground` / `surface` | 17.85 | 4.5 |
| `muted-foreground` | `oklch(0.446 0.037 257.3)` | `#475569` | `muted-foreground` / `surface` | 7.58 | 4.5 |
| `border-subtle` | `oklch(0.869 0.020 252.9)` | `#CBD5E1` | decorative | 1.48 | none |
| `border-strong` | `oklch(0.663 0.021 255.6)` | `#8B94A0` | `border-strong` / `surface` | 3.07 | 3.0 |
| `destructive` | `oklch(0.505 0.191 27.5)` | `#B91C1C` | `destructive` / `surface` | 6.47 | 4.5 |

## Premium (dark-first)

| Role | `oklch()` | sRGB | Measured pair | Ratio | Requirement |
|---|---|---|---|---|---|
| `primary` | `oklch(0.923 0.003 48.7)` | `#E7E5E4` | `primary` / `surface` | 13.93 | 3.0 |
| `on-primary` | `oklch(0.216 0.006 56.0)` | `#1C1917` | `on-primary` / `primary` | 13.93 | 4.5 |
| `accent` | `oklch(0.748 0.098 85.8)` | `#C9A962` | `accent` / `surface` | 7.77 | 3.0 |
| `on-accent` | `oklch(0.375 0.044 83.9)` | `#4C3F25` | `on-accent` / `accent` | 4.56 | 4.5 |
| `background` | `oklch(0.147 0.004 49.2)` | `#0C0A09` | `foreground` / `background` | 18.92 | 4.5 |
| `surface` | `oklch(0.216 0.006 56.0)` | `#1C1917` | — | — | — |
| `foreground` | `oklch(0.985 0.001 106.4)` | `#FAFAF9` | `foreground` / `surface` | 16.74 | 4.5 |
| `muted-foreground` | `oklch(0.716 0.009 56.3)` | `#A8A29E` | `muted-foreground` / `surface` | 6.93 | 4.5 |
| `border-subtle` | `oklch(0.269 0.006 34.3)` | `#292524` | decorative | 1.15 | none |
| `border-strong` | `oklch(0.513 0.006 48.6)` | `#6A6664` | `border-strong` / `surface` | 3.08 | 3.0 |
| `destructive` | `oklch(0.711 0.166 22.2)` | `#F87171` | `destructive` / `surface` | 6.32 | 4.5 |

## Playful / education

| Role | `oklch()` | sRGB | Measured pair | Ratio | Requirement |
|---|---|---|---|---|---|
| `primary` | `oklch(0.541 0.247 293.0)` | `#7C3AED` | `primary` / `surface` | 5.70 | 3.0 |
| `on-primary` | `oklch(1 0 0)` | `#FFFFFF` | `on-primary` / `primary` | 5.70 | 4.5 |
| `accent` | `oklch(0.673 0.151 65.0)` | `#D47F00` | `accent` / `surface` | 3.07 | 3.0 |
| `on-accent` | `oklch(0.297 0.068 63.1)` | `#442400` | `on-accent` / `accent` | 4.56 | 4.5 |
| `background` | `oklch(0.987 0.026 102.2)` | `#FEFCE8` | `foreground` / `background` | 14.67 | 4.5 |
| `surface` | `oklch(1 0 0)` | `#FFFFFF` | — | — | — |
| `foreground` | `oklch(0.269 0.006 34.3)` | `#292524` | `foreground` / `surface` | 15.17 | 4.5 |
| `muted-foreground` | `oklch(0.444 0.010 73.6)` | `#57534E` | `muted-foreground` / `surface` | 7.63 | 4.5 |
| `border-subtle` | `oklch(0.923 0.003 48.7)` | `#E7E5E4` | decorative | 1.26 | none |
| `border-strong` | `oklch(0.665 0.002 17.2)` | `#959393` | `border-strong` / `surface` | 3.06 | 3.0 |
| `destructive` | `oklch(0.577 0.215 27.3)` | `#DC2626` | `destructive` / `surface` | 4.83 | 4.5 |

## What changed in these tables, and why it matters

The four palettes previously shipped in this pack were correct in structure and wrong in values. They supplied no `on-accent` role at all, so an agent following them reused white on the accent, and the measured result on 2026-07-28 was:

| Palette | Accent | White on accent, as shipped | Verdict |
|---|---|---|---|
| SaaS / trust | `#EA580C` | 3.56 | fails 4.5 |
| Dashboard / ops | `#0D9488` | 3.74 | fails 4.5 |
| Premium | `#C9A962` | 2.25 | fails 4.5 and 3.0 |
| Playful / education | `#F59E0B` | 2.15 | fails 4.5 and 3.0 |

All four failed the contrast gate of the very pack that shipped them, at the exact place the pack reserves the accent for the primary call to action. The single `border` role also ran 1.15 to 1.48 against its surface, which is fine as decoration and fails as an input's only boundary — hence the split into `border-subtle` and `border-strong`.

The Playful accent was additionally darkened from `oklch(0.769 0.165 70.1)` to `oklch(0.673 0.151 65.0)` because at its original lightness it reached only 2.15 against a white surface, so an accent-filled button had no discernible edge.

## Using a palette

1. Copy the whole table into the repo's token file. Do not take individual values; the ratios are properties of pairs.
2. Rename `primary` and `accent` hues to the brand, keeping the `L` and `C` of the row you started from, then **re-run the checker**. Changing hue at constant lightness usually preserves the ratios; changing lightness never does.
3. Design the dark counterpart alongside, do not invert (`20-design-tokens-and-theming.md`).
4. Record any contrast-driven adjustment next to the token, with the ratio.

## Pairing

- Token architecture, roles and the lookup rule: `20-design-tokens-and-theming.md`
- Building a palette from product intent rather than starting here: `30-typography-and-color.md`
- The contrast gate itself: `90-quality-gates-and-review.md`
- Regenerating these ratios: `scripts/check-design-system.mjs --palettes`
