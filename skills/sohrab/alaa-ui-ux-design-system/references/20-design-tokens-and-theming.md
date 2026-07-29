# Design Tokens and Theming

Read this file before writing any color, spacing, radius, shadow or z-index value, and whenever a theme is added or changed. Tokens are the contract between design intent and code; a raw value in a component is drift.

## Token architecture

Three tiers, referenced downward only:

1. **Primitive:** raw values (`--blue-600`, `--space-4`). Never referenced from a component.
2. **Semantic:** role-named (`--color-primary`, `--surface`, `--space-md`, `--motion-duration-sm`). This is what components consume.
3. **Component:** only when a component genuinely needs its own knob (`--btn-radius`), and only when the knob is named in that component's documentation.

## The required semantic role set

Every declared theme defines **every** role below. A theme missing one is invalid, not merely incomplete, because the missing role silently falls back to the previous theme's value and produces a light-mode panel on a dark page.

| Group | Roles |
|---|---|
| Brand | `primary`, `on-primary`, `secondary`, `accent`, `on-accent` |
| Ground | `background`, `surface`, `surface-muted`, `foreground`, `muted-foreground` |
| Boundary | `border-subtle`, `border-strong`, `ring` |
| Status, each with a foreground and a fill | `success`, `on-success`, `warning`, `on-warning`, `destructive`, `on-destructive`, `info`, `on-info` |

**Every fill role has a paired `on-*` role, and the pair is measured.** The absence of an `on-*` role is what makes an agent reach for white, and white fails on most accents. See `32-starter-palettes.md`.

**Theme-invariant tokens are declared once, in the base theme only:** spacing, radius, type scale, weights, line heights, motion durations and easings, z-index. Re-declaring them per theme creates two sources of truth for a value that has one. Only tokens whose value actually depends on the theme — colors, shadows, and any gradient — appear in a theme block.

`scripts/check-design-system.mjs --themes` reports any role present in one theme block and absent from another, and separates genuinely theme-invariant tokens from omissions.

## The lookup rule and the fallback rule

Two rules that together close the hole named in every anti-pattern list and never previously stated as a procedure.

**Lookup.** Before writing a value, search the token file for the role that describes what the value *means* — not for a matching color. `#F3F4F6` and "a slightly lighter gray for the card behind the form" are the same search, and only the second finds `--surface-muted`.

**Fallback, when the lookup finds nothing.** In order, stopping at the first that applies:

1. A semantic role exists with a slightly different name — use it and do not add a synonym. Two roles that resolve to the same value are the drift this file exists to prevent.
2. The need is genuinely new and will recur — add one semantic role, in the token file, in **every** theme, with a comment stating what it means, then run the checker.
3. The need is genuinely new and will not recur — it is a component token, declared in that component and named in its documentation.
4. None of the above applies — the value does not belong in the design system. Say so and ask, rather than inventing a near-duplicate.

**Never resolve a failed lookup by writing a literal.** The named failure mode is "a second slightly-different gray because the token was not found"; it is produced by skipping this list, and it is why `scripts/check-design-system.mjs --tokens` fails a build on any color literal outside the theme file.

## Modern color and theming

- Define the palette in `oklch()`; derive hover, active and disabled states with relative color syntax, falling back to `color-mix()` where support must reach further back.
- Theme with `color-scheme: light dark` on `:root` plus `light-dark()` per token rather than duplicated selector blocks. A `[data-theme]` attribute block is the alternative when the theme must be selectable independently of the OS preference; pick one mechanism per repo and do not run both.
- Register any custom property you animate with `@property`; registration is what makes it interpolable.
- Baseline status for each feature named here is in `72-modern-css-baseline-tiers.md`. Check it before relying on one.

```css
:root {
  color-scheme: light dark;
  --brand: oklch(0.62 0.19 260);
  --brand-hover: oklch(from var(--brand) calc(l - 0.07) c h);
  --surface: light-dark(oklch(0.99 0 0), oklch(0.22 0.02 260));
}
@property --glow { syntax: "<number>"; inherits: false; initial-value: 0; }
```

## Dark mode

- Design light and dark together; never invert. Dark surfaces use desaturated, slightly lifted tonal variants; pure `#000` backgrounds and pure `#FFF` text are both wrong.
- **Measure contrast per theme.** A pair that passes in light routinely fails in dark, and nothing about the light measurement predicts the dark one. Run `scripts/check-design-system.mjs --contrast` against each theme block separately.
- State parity: hover, pressed, focus and disabled stay equally distinguishable in both themes.
- Borders and dividers stay visible in both. Shadows lose meaning on dark surfaces — compensate with `border-subtle` or a surface lightness step, not with a heavier shadow.
- Modal scrim 40-60% black in both themes so the foreground isolates.

## Shared scales

Spacing on a 4/8 rhythm with three density tiers. Pick one tier per product or per page override; never mix tiers within a page.

| Token | Spacious (marketing) | Standard | Dense (dashboard) |
|---|---|---|---|
| `--space-sm` | 16 | 12 | 8 |
| `--space-md` | 24 | 16 | 12 |
| `--space-lg` | 48 | 32 | 16 |
| `--space-xl` | 96 | 64 | 24 |

- **Radius:** one scale (0 / 4 / 8 / 16 / full), chosen by style. Brutalism takes 0, clay takes large. A radius not on the scale is a defect.
- **Shadow:** one ordered scale (sm / md / lg / xl) coherent with the style. No one-off shadow values.
- **Z-index:** a fixed layered scale (0 / 10 dropdown / 20 sticky / 40 overlay / 100 modal / 1000 toast). `z-[9999]` and any literal z-index in a component are defects.
- **Motion:** `--motion-duration-sm/md/lg` and `--motion-ease-enter/exit` per `70-motion-contract.md`.

## Mapping tokens into the stack

One source of truth: semantic tokens feed Tailwind, Bootstrap and Quasar. Never maintain parallel palettes. Choose Tailwind or Bootstrap per repo; do not mix both in one app unless the repo already does.

- **Tailwind v4:** define tokens in `@theme` so utilities are generated from them. Arbitrary-value utilities (`bg-[var(--x)]`, `z-[9999]`, `text-[13px]`) bypass the system and are reported by the checker.
- **Bootstrap 5:** override the CSS variables and Sass maps from the same semantic tokens, and wire the dark selector to the same source of truth.
- **Quasar:** the token values are ours; the mechanism by which they reach Quasar — the brand variable names in `app.scss`, `setCssVar`, the Dark plugin's state — is owned by `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`). What this skill requires is only the outcome: **Quasar components and custom components resolve to one palette, and the framework's theme state and the CSS `color-scheme` never disagree.** How that is wired is that skill's ground.

## Anti-patterns

- A raw hex, `rgb()`, `oklch()`, px radius, box-shadow or z-index literal in a component when a role exists.
- A dark theme produced by inverting the light palette.
- A theme block that redeclares spacing, radius or type scale.
- A theme missing a role that another theme declares.
- A fill role with no `on-*` counterpart.
- Two token systems in one repo disagreeing with each other.
- Adding a synonym role because the lookup used a color rather than a meaning.

## Pairing

- Validated starting values with printed ratios: `32-starter-palettes.md`
- Palette construction from product intent, contrast targets: `30-typography-and-color.md`
- Style coherence for radius, shadow and effects: `40-styles-and-visual-language.md`
- Platform support for `oklch()`, `light-dark()`, `@property`: `72-modern-css-baseline-tiers.md`
- Proving a token change: `95-design-proofs.md`
