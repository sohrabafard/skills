# Styles and Visual Language

Use this file when picking a visual style or checking that effects stay coherent with one. Style selection is taste-tier — this file supplies vocabulary and honest trade-offs, not a mandate.

## Style vocabulary with honest trade-offs

Read the "Do not use for" column before committing. A style that fights the product loses to a plainer one that serves it.

| Style | Signature | Best for | Do not use for | Cautions |
|---|---|---|---|---|
| Minimalism | whitespace, restrained palette, typography-led | SaaS, portfolios, premium, trust-heavy | content-poor pages that end up empty, not minimal | demands excellent typography; hides sloppiness nowhere |
| Flat / Swiss | solid colors, grid discipline, no depth | dashboards, gov/edu, information-dense | brands needing warmth or depth | can read generic without a strong grid and type |
| Glassmorphism | backdrop blur 10–20px, translucent surfaces, 1px light border | modern SaaS marketing, overlays, fintech hero | low-contrast backgrounds, critical accessibility, weak GPUs | contrast on glass must still pass 4.5:1; honor `prefers-reduced-transparency` |
| Neumorphism | soft extruded shadows, monochrome | niche showcase only | almost everything shipping | chronically fails contrast; treat as reference, not default |
| Brutalism | raw borders, radius 0, stark type, harsh contrast | portfolios, editorial, creative brands | corporate, conversion funnels, accessibility-critical | boilerplate must not soften it — no rounded corners, no soft shadows |
| Bento grids | asymmetric card mosaic, mixed tile sizes | feature overviews, product landing sections | long-form reading, dense tables | needs real content variety; empty tiles kill it |
| Aurora / gradient mesh | soft multi-hue gradient backdrops, glow | hero sections, AI/creative products, dark-first | text-heavy surfaces, print-like reading | keep text on solid surfaces; gradients behind text fail contrast |
| Claymorphism | large radius, thick soft shadows, chunky | playful, kids, education (consumer) | professional/enterprise, dense UI | pairs with rounded type; keep palette AA-compliant |
| Dark-mode-first | dark surfaces as primary theme, neon accents | dev tools, media, gaming, dashboards | long-form reading in bright environments | needs the dark-mode rules in `20-design-tokens-and-theming.md`, not just dark paint |
| Editorial / magazine | serif display, strong grid, generous imagery | content brands, premium storytelling | app-like dense interaction | imagery quality decides everything |

## Coherence rules

- One style per product. Pages may vary in intensity, never in language.
- Effects must match the style: shadow scale, blur, radius, and border treatment all come from the chosen style. A glass card with brutalist borders is two half-styles.
- Era coherence: do not mix skeuomorphic textures, Y2K chrome, and flat minimal in one interface unless the deliberate concept is collage — and then say so in MASTER.md.
- The signature effect budget is small: one memorable move (glass hero, aurora backdrop, bento section) per page reads premium; three read as noise.
- Framework fit: everything above is achievable in Tailwind or Bootstrap; Tailwind gives finer control of arbitrary effects, Bootstrap needs its variables overridden hard (radius, shadows) before it stops looking like Bootstrap. Quasar components inherit the token layer — restyle via tokens/`app.scss`, not per-component overrides.

## Choosing under uncertainty

- If the brief is vague: minimalism with one signature effect is the highest-floor default — but say that it is a default and offer one bolder alternative.
- If conversion is the goal: clarity beats novelty; spend boldness on the hero, keep forms and checkout conservative.
- If the user asks for bold/experimental: go genuinely bold (brutalism, bento, aurora) while holding the gates — do not water it down to safe-but-bland.

## Anti-patterns

- Committing to a style without checking its "do not use for" column.
- Style-by-committee: minimal layout + clay buttons + glass modals.
- Injecting default boilerplate (8px radius, soft shadows, 200ms all-transitions) into a style whose whole point is refusing it.
- Choosing a style the product's content cannot feed (bento with three features, editorial with no imagery).

## Pairing guidance

- Direction selection from product intent: `10-design-workflow.md`
- Expressing the style as tokens: `20-design-tokens-and-theming.md`
- Motion that matches the style's temperament: `70-motion-and-modern-css.md`
