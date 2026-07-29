# Styles and Visual Language

Read this file when picking a visual style, or when adding a shadow, blur, border or radius that is not already in the token file. Style selection is taste tier; this file supplies vocabulary and honest trade-offs, not a mandate.

## Style vocabulary with trade-offs

Read the "Do not use for" column before committing. A style that fights the product loses to a plainer one that serves it.

| Style | Signature | Best for | Do not use for | Cautions |
|---|---|---|---|---|
| Minimalism | whitespace, restrained palette, typography-led | SaaS, portfolios, premium, trust-heavy | content-poor pages that end up empty rather than minimal | demands excellent typography; hides nothing |
| Flat / Swiss | solid colors, grid discipline, no depth | dashboards, government, education, information-dense | brands needing warmth or depth | reads generic without a strong grid and type |
| Glassmorphism | backdrop blur 10-20px, translucent surfaces, 1px light border | modern SaaS marketing, overlays, fintech hero | low-contrast backdrops, accessibility-critical products, weak GPUs | text on glass must be measured against the lightest and darkest pixel behind it; `prefers-reduced-transparency` must drop the blur |
| Neumorphism | soft extruded shadows, monochrome | niche showcase only | almost everything that ships | chronically fails contrast; reference, not default |
| Brutalism | raw borders, radius 0, stark type, harsh contrast | portfolios, editorial, creative brands | corporate, conversion funnels, accessibility-critical | boilerplate must not soften it |
| Bento grids | asymmetric card mosaic, mixed tile sizes | feature overviews, product landing sections | long-form reading, dense tables | needs real content variety; empty tiles kill it |
| Aurora / gradient mesh | soft multi-hue gradient backdrops, glow | hero sections, AI and creative products, dark-first | text-heavy surfaces, print-like reading | text sits on a solid surface, never on the gradient |
| Claymorphism | large radius, thick soft shadows, chunky forms | playful, children, consumer education | professional, enterprise, dense UI | pairs with rounded type; palette must still pass the gate |
| Dark-mode-first | dark surfaces as the primary theme, neon accents | developer tools, media, gaming, dashboards | long-form reading in bright environments | needs the dark-mode rules in `20-design-tokens-and-theming.md`, not just dark paint |
| Editorial / magazine | serif display, strong grid, generous imagery | content brands, premium storytelling | app-like dense interaction | imagery quality decides everything |

## Coherence rules

- **One style per product.** Pages vary in intensity, never in language.
- **Effects come from the recorded row, not from taste in the moment.** Radius, shadow, blur and border values are taken from the row of the table above that you recorded in `MASTER.md`, expressed as tokens. A value not derivable from that row is a defect, and "it matches the style" is not a check — the recorded row is.
- **Era coherence:** do not mix skeuomorphic texture, Y2K chrome and flat minimal in one interface unless collage is the deliberate concept, and then say so in `MASTER.md`.
- **The signature effect budget is one per page.** One memorable move reads premium; three read as noise. Count them before delivery.
- **Framework fit:** every style here is achievable in Tailwind or Bootstrap. Bootstrap needs its radius and shadow variables overridden hard before it stops looking like Bootstrap. Quasar components inherit the token layer, so restyle through tokens rather than per-component overrides; the mechanism for that is owned by `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`).

## Choosing under uncertainty

- **Vague brief:** minimalism with one signature effect is the highest-floor default. Say that it is a default and offer one bolder alternative.
- **Conversion is the goal:** clarity beats novelty. Spend boldness on the hero; keep forms and checkout conservative.
- **The user asked for bold:** go genuinely bold — brutalism, bento, aurora — while holding the gates. Watering a bold request down to safe-but-bland is a failure to deliver, not caution.

## Anti-patterns

- Committing to a style without reading its "Do not use for" column.
- Style-by-committee: minimal layout, clay buttons, glass modals.
- Injecting default boilerplate (8px radius, soft shadows, a 200ms transition on everything) into a style whose whole point is refusing it.
- Choosing a style the product's content cannot feed: bento with three features, editorial with no imagery.
- Text placed on a gradient or a glass surface.
- A shadow or radius value invented at the component because the style "felt like it".

## Pairing

- Direction selection from product intent: `10-design-workflow.md`
- Expressing the style as tokens: `20-design-tokens-and-theming.md`
- Measuring text on a variable backdrop: `30-typography-and-color.md`
- Motion matching the style's temperament: `70-motion-contract.md`
- Platform support for blur, gradients and `@supports` guards: `72-modern-css-baseline-tiers.md`
