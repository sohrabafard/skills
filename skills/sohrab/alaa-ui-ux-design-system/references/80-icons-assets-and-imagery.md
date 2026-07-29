# Icons, Assets and Imagery

Read this file when adding an icon, an image, a logo, a favicon or an Open Graph image. Direction-bearing icons are governed by `05-rtl-and-persian.md` section 2; byte ceilings by `45-render-and-asset-budgets.md`.

## Icon discipline

- **Vector only. An emoji is never a UI icon** — it is font-dependent, renders differently on every platform, cannot be themed, and sits outside the token system.
- **One icon family per product**, declared in `MASTER.md`. Consistent stroke width within a hierarchy level. Filled versus outline is a hierarchy signal (filled marks the active navigation item), never a random mix.
- **Sizes are tokens** (`--icon-sm: 16`, `--icon-md: 20/24`, `--icon-lg: 32`). No per-use pixel sizes.
- Icons align to the text baseline or optical centre with consistent padding. Icon glyphs meet the non-text contrast threshold, and the body threshold when small and meaning-bearing.
- **An icon-only button always carries an accessible name and a 44x44 target.** An icon is not a label.
- **Direction-bearing icons are resolved by role, never by physical name** (`05-rtl-and-persian.md` section 2). `scripts/check-design-system.mjs --icons` reports violations.

## Choosing a family

Pick one primary set per product; fall back only within the same visual style.

- **Licences, because an unstated licence is the defect.** Phosphor is MIT (`github.com/phosphor-icons/core`, `read: 2026-07-28`). Material Symbols, MDI, Lucide, Heroicons, Tabler and Bootstrap Icons are each commonly distributed under a permissive licence, but the specific version you install is what governs: `read: unverified as of 2026-07-28`. **Read the licence file in the package you actually install and record it in `MASTER.md`.** `client` uses Phosphor.
- Which set a framework bundles, and how it is tree-shaken or wired at build time, is owned by `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`). A bundling claim is not a design rule and is not asserted here.
- **Fallback rule:** when the primary set lacks a glyph, first search the whole primary set for a semantically close one. Only then borrow from one designated fallback set matched in stroke weight and corner language. Never three sets.

## Brand assets and logos

- Use official brand assets with their clear-space and colour rules. **Never recolour, stretch or redraw a third-party logo**, and never guess an asset path.
- A third-party logo carries its owner's usage terms; those terms are the adjudicator, not taste. If they cannot be found, do not use the logo.
- The product logo ships as SVG with a defined minimum size and clear space. A monochrome variant for dark surfaces is part of the theme work, not an afterthought.
- A logo is never mirrored under RTL.

## Images

- **Format:** AVIF with a WebP fallback for photography; SVG for anything geometric. Weight ceilings are in `45-render-and-asset-budgets.md`.
- **Every image declares dimensions or an `aspect-ratio`.** Zero layout shift from media is a gate. `object-fit: cover` with a defined focal point for cards and heroes.
- **Lazy-load below the fold. The LCP hero loads eagerly with `fetchpriority="high"` and never `loading="lazy"`.** Design the hero so it can ship as an optimizable image or SVG in server HTML rather than as a scene composed in JavaScript.
- `srcset` and `sizes` on content imagery. Never ship desktop pixels to a phone.
- **Meaningful images get descriptive alt text; decorative images get an empty alt attribute. Missing alt is never correct** — the two cases have different right answers and both are explicit.
- One consistent treatment — radius from the token scale, one overlay or duotone recipe — so photographs from mixed sources read as one product.
- An uploaded image is untrusted content (`25-untrusted-content-and-ui-authority.md`).

## Favicons, app identity and social images

Ship this set for every public product; a missing favicon reads as unfinished. Every number below is a platform convention: `read: unverified as of 2026-07-28`, re-verify once against the platform's own current documentation rather than carrying them on trust.

- SVG favicon, theme-aware through `prefers-color-scheme` inside the SVG, plus a 32px `.ico` fallback.
- `apple-touch-icon` at 180x180, opaque background, no transparency.
- Web app manifest icons at 192 and 512 including a maskable variant, with the mark inside the inner 80% safe zone.
- `theme-color` for light and dark through the `media` attribute, matched to the surface role.
- `og:image` at 1200x630, readable at thumbnail size — a large mark and a short claim, never a screenshot of the interface with small text — plus title, description, and a large-image card declaration.
- Keep the source artwork in the repository as an SVG master so regeneration is deterministic, and record the export set in `MASTER.md`.

## Illustration

- One illustration language per product: consistent stroke weight, a palette drawn from the tokens, one level of abstraction. Never mix 3D renders, flat line art and hand-drawn doodles.
- Illustrations serve a state or a story — empty states, onboarding, errors. Decorative filler dilutes them.
- Prefer SVG and recolour through `currentColor` or custom properties so illustrations follow theme switches.

## Anti-patterns

- Emoji as navigation or status icons; three icon sets in one app; per-use pixel sizes.
- A physical-direction icon name at a call site in a bidirectional product.
- A raster logo scaled up; a recoloured partner logo.
- A hero image with no declared dimensions.
- A heavy PNG where AVIF or SVG belongs.
- No favicon or social-image set, or a social image that is an unreadable full-page screenshot.
- Illustrations whose palette ignores the tokens.
- An icon family adopted without reading its licence.

## Pairing

- Direction and mirroring: `05-rtl-and-persian.md`
- Icon size and radius tokens: `20-design-tokens-and-theming.md`
- Weight ceilings and third-party budget: `45-render-and-asset-budgets.md`
- Uploaded and user-supplied images: `25-untrusted-content-and-ui-authority.md`
- Icon set wiring in the framework: `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`)
- CDN and build-time delivery: `/alaa-frontend-devops` (`$alaa-frontend-devops`)
