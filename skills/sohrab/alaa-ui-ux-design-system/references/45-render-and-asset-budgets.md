# Render and Asset Budgets

Read this file when adding a font file, a hero image, a video embed or a third-party script, and when adding a theme, density tier or preference axis that multiplies what must be verified.

A design decision with no stated budget is a decision to spend whatever it takes. Every number below is a default: overridable by a repo budget file with a stated reason, never by drift.

## Frame budget

- **A frame is 16.7 ms at 60 Hz and 8.3 ms at 120 Hz.** Any animation, scroll handler or transition that cannot finish its work inside that window drops frames, and a dropped frame during a gesture is felt even when it is not seen.
- The design consequence: animate only `transform` and `opacity`, which the compositor can run without the main thread. `filter` and `backdrop-filter` are affordable once per view, not per list item. Layout properties (`width`, `height`, `top`, `left`, `margin`, `font-size`) and `box-shadow` are never animated. The full rule and its exceptions are in `70-motion-contract.md`.
- **Interaction latency, as design targets:** visible feedback on press within **100 ms**; a state change the user initiated completes or shows progress within **300 ms**; anything past **1 s** needs an explicit designed loading state (`15-designed-failure-states.md`).
- A design that needs more than one animated element per interaction to read correctly is over-specified. Cut it before shipping it.

## Image weight

Per-image transferred size ceilings, at the width actually served:

| Role | Ceiling | Notes |
|---|---|---|
| LCP hero | **150 KB** | eager, `fetchpriority="high"`, never `loading="lazy"` |
| Above-the-fold content image | 100 KB | |
| Card or thumbnail | 40 KB | at the largest size the card renders |
| Avatar or icon-sized raster | 10 KB | prefer SVG |
| Decorative background | 60 KB | if it needs more, it is a gradient or it is cut |
| **Total images on first view** | **500 KB** | the number to defend in review |

- AVIF with a WebP fallback for photography; SVG for anything geometric. A PNG that is not a screenshot or a transparency-critical asset is a defect.
- `srcset` and `sizes` on every content image. Shipping desktop pixels to a 375px phone is the single largest image waste and the checker cannot see it — a reviewer must.
- Every image declares `width` and `height` or an `aspect-ratio`. Zero layout shift from media is a gate, not a target.
- An image that exceeds its ceiling is not shipped smaller-quality by default: first ask whether it should be an SVG, a gradient, or nothing.

## Font bytes

- **150 KB total transferred** for first-party fonts on the initial route.
- At most **three weights per family**, `woff2` only. Drop `woff` unless the repo's browser-support matrix names a browser that lacks `woff2` — as of 2026 that is unusual, and shipping both doubles the directory for no delivered bytes.
- At most **two preloaded** font files.
- Subset to the ranges the product actually renders. For a Persian product that is the Arabic range plus Latin plus U+200C; see `05-rtl-and-persian.md` section 6.
- A variable font counts once and usually wins on total bytes; prefer it when it exists.

## Third-party weight

- **Every third-party embed is a design decision before it is an engineering one.** A video player, a map, a chat widget, an analytics tag or a font CDN each buys something and costs something; name both before adding one.
- A heavy embed below the fold ships as a **facade**: a static image with the real embed loaded on interaction. Design the facade as a real state, not a placeholder.
- **Budget: at most one heavy third-party embed above the fold, and none at all on a conversion-critical flow** — checkout, authentication, payment. Their failure modes are not ours to control and their appearance is not ours to theme.

Scoring, thresholds and the measurement toolchain for all of the above are owned by `/alaa-frontend-developer` (`$alaa-frontend-developer`); CDN and build-time delivery by `/alaa-frontend-devops` (`$alaa-frontend-devops`). The numbers on this page are design ceilings that keep a direction inside those budgets, not a second scoring system.

## The theme matrix, and which cells must be verified

Every visual axis multiplies with every other. Enumerated for a product with two themes, three density tiers and two directions, plus two user preferences:

`2 themes x 3 density tiers x 2 directions x 2 (prefers-contrast) x 2 (prefers-reduced-transparency) = 48 renderings of every component`

Adding `prefers-reduced-motion` doubles it again. **This does not shrink by ignoring it**, and the failure mode of ignoring it is a real one: a component verified in light-standard-RTL and shipped, then found broken in dark-dense-LTR by a user. The doctrine behind combinatorial growth is owned by `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`); what follows is this skill's ruling on which cells are verified.

**Mandatory cells — every component, every time:**

1. Light theme, standard density, the product's primary direction.
2. Dark theme, standard density, the product's primary direction — if the product ships dark mode.
3. Primary direction with `prefers-reduced-motion: reduce` — for any component that animates.
4. **The opposite direction**, light theme, standard density — for any product that can render either. On `client` this is the LTR pass, which today exists only as islands and is the direction most likely to be broken.

**Conditional cells, verified when the condition holds:**

5. Each density tier the component actually appears in. A component used only on the dashboard needs only the dense tier.
6. `prefers-contrast: more` — for any component whose meaning depends on a border, a divider or a subtle fill.
7. `prefers-reduced-transparency` — for any component using blur or translucency.

**Everything else is verified by construction, not by rendering.** A component built entirely from logical properties and semantic tokens does not need a cell per axis, because the axis cannot reach it. That is the point of the token and logical-property rules: they convert a combinatorial verification problem into a linear one. **A component that needs many cells verified is telling you it has raw values in it.**

Record which cells were verified in the delivery note. An unverified cell is stated, and a cell nobody looked at is never reported as passing.

## Anti-patterns

- Animating a layout property because it was easier than restructuring.
- A hero image shipped at desktop resolution to every device.
- Nine font weights in two formats, none subset, none preloaded, none measured.
- A chat widget on the checkout page.
- "We will check dark mode later."
- Verifying one cell of the matrix and reporting the component as done.
- Treating an unmeasured budget as met because the page felt fast on a development machine.

## Pairing

- Compositor rules and duration tokens: `70-motion-contract.md`
- Image format, alt text and asset discipline: `80-icons-assets-and-imagery.md`
- Font selection and subsetting: `30-typography-and-color.md`, `05-rtl-and-persian.md`
- Long lists and slow networks: `65-lists-latency-and-concurrency.md`
- What proves a cell was verified: `95-design-proofs.md`
