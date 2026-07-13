# Design Tokens and Theming

Use this file for token architecture, theming, dark mode, and the shared scales (spacing, radius, shadow, z-index). Tokens are the contract between design intent and code; raw values in components are drift.

## Token architecture

Three tiers, referenced downward only:

1. Primitive: raw values (`--blue-600`, `--space-4`). Never used directly in components.
2. Semantic: role-named (`--color-primary`, `--surface`, `--space-md`, `--motion-duration-sm`). This is what components consume.
3. Component (optional): only when a component genuinely needs its own knob (`--btn-radius`).

Semantic color roles — define all of these once per theme:

`primary`, `on-primary`, `secondary`, `accent` (CTA), `background`, `surface` (card), `foreground`, `muted`, `muted-foreground`, `border`, `destructive`, `ring` (focus).

✅ Do — `background: var(--surface)` in components; change themes by remapping tokens.

❌ Don't — `#2563EB` or `bg-[#2563EB]` inside a component; per-screen ad-hoc colors; a second slightly-different gray because the token was not found.

## Modern color and theming recipe

- Define the palette in `oklch()`; derive hover/active/disabled states with relative color syntax, falling back to `color-mix()` where support must reach further back.
- Theme with `color-scheme: light dark` on `:root` plus `light-dark()` per token — not duplicated selector blocks.
- Register any custom property you animate (gradient angles, glow strength, numeric tokens) with `@property` — registration is what makes it interpolable.

```css
:root {
  color-scheme: light dark;
  --brand: oklch(0.62 0.19 260);
  --brand-hover: oklch(from var(--brand) calc(l - 0.07) c h);
  --surface: light-dark(oklch(0.99 0 0), oklch(0.22 0.02 260));
}
@property --glow { syntax: "<number>"; inherits: false; initial-value: 0; }
```

## Dark mode rules

- Design light and dark together; never invert mechanically. Dark surfaces use desaturated, slightly lifted tonal variants; pure `#000` backgrounds and pure `#FFF` text are both wrong.
- Test contrast separately per theme — light-mode-passing values routinely fail on dark surfaces.
- State parity: hover/pressed/focus/disabled must stay equally distinguishable in both themes.
- Borders and dividers must remain visible in both themes; shadows lose meaning on dark — compensate with borders or surface lightness steps.
- Modal scrim 40–60% black in both themes so foreground content clearly isolates.

## Shared scales

Spacing — 4/8px rhythm, expressed as tokens with three density tiers; pick per product (or per page override), never mix tiers casually:

| Token | Spacious (marketing) | Standard | Dense (dashboard) |
|---|---|---|---|
| `--space-sm` | 16 | 12 | 8 |
| `--space-md` | 24 | 16 | 12 |
| `--space-lg` | 48 | 32 | 16 |
| `--space-xl` | 96 | 64 | 24 |

- Radius: one small scale (e.g. 0 / 4 / 8 / 16 / full) — chosen by style; brutalism gets 0, clay gets large. Never mix arbitrary radii.
- Shadow/elevation: a single ordered scale (sm/md/lg/xl) coherent with the chosen style; no one-off shadow values.
- Z-index: a fixed layered scale (e.g. 0 / 10 dropdown / 20 sticky / 40 overlay / 100 modal / 1000 toast). Never `z-[9999]`.
- Motion tokens: `--motion-duration-sm/md/lg` and `--motion-ease-enter/exit` per `70-motion-and-modern-css.md`.

## Mapping tokens into the stack

Choose Tailwind or Bootstrap per repo; do not mix both in one app unless the repo already does.

- Tailwind v4: define tokens in `@theme` so utilities are generated from them (`bg-primary`, `text-muted-foreground`). Avoid arbitrary-value utilities (`bg-[var(--x)]`, `z-[9999]`) — they bypass the system.
- Bootstrap 5: override the CSS variables (`--bs-primary`, `--bs-body-bg`, `--bs-border-radius`, ...) and Sass maps from the same semantic tokens; use `data-bs-theme="dark"` wired to the same `light-dark()` source of truth.
- Quasar: map the same tokens into `app.scss` brand variables (`$primary`, `$dark-page`, ...) and `setCssVar`/CSS custom properties so Quasar components and custom components share one palette. Quasar Dark plugin state must follow the same theme source as `color-scheme`.

One source of truth: semantic tokens feed Tailwind, Bootstrap, and Quasar — never maintain three parallel palettes.

## Anti-patterns

- Raw hex/px/ms values scattered in components when a token exists.
- A dark theme produced by inverting the light palette.
- Two competing token systems in one repo (Tailwind config says one thing, `app.scss` another).
- Boilerplate tokens that contradict the chosen style (rounded corners and soft shadows injected into a brutalist direction).

## Pairing guidance

- Palette construction and contrast targets: `30-typography-and-color.md`
- Style coherence for radius/shadow/effects: `40-styles-and-visual-language.md`
- Implementation and SSR-safe theme switching: `$alaa-frontend-developer`; exact Quasar theming APIs: `$alaa-quasar-app-vite-v3`
