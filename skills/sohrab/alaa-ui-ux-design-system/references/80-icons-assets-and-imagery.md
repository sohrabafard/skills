# Icons, Assets, and Imagery

Use this file for icon systems, brand assets, images, favicons/app identity, and illustration direction.

## Icon discipline (gates)

- Vector icons only. Emojis are never UI icons — they are font-dependent, inconsistent across platforms, and outside the token system.
- One icon family per product, declared in MASTER.md. Consistent stroke width (e.g. 1.5px or 2px) and corner language within a hierarchy level; filled vs outline is a hierarchy signal (e.g. filled = active nav), never random mixing.
- Sizes are tokens (`--icon-sm: 16`, `--icon-md: 20/24`, `--icon-lg: 32`) — no arbitrary per-use sizes.
- Icons align to the text baseline/optical center with consistent padding; icon glyphs meet 3:1 contrast (4.5:1 when small and meaning-bearing).
- Icon-only buttons: `aria-label` and >= 44px touch target, always.

## Icon libraries for the Vue stack

Pick one primary set per product; fall back only within the same visual style:

- Quasar projects: `@quasar/extras` sets — Material Symbols (rounded/sharp/outlined) or MDI — zero extra dependency, tree-shaken by name.
- Framework-agnostic Vue: Phosphor (`@phosphor-icons/vue`, weight-consistent, huge range), Lucide (`lucide-vue-next`, clean 2px stroke), Heroicons (`@heroicons/vue`, pairs with Tailwind aesthetics), Tabler (dense-UI friendly).
- Bootstrap-styled projects: Bootstrap Icons fit natively; Lucide also sits well.
- Fallback rule: when the primary set lacks a glyph, first search the full primary set for a semantically close icon; only then borrow from one designated fallback set matched in stroke and corner style. Never mix three sets.

## Brand assets and logos

- Use official brand assets with their clear-space and color rules; never recolor, stretch, or redraw third-party logos, and never guess asset paths.
- Product logo ships as SVG with defined minimum size and clear space; a monochrome variant for dark surfaces is part of the token/theme work, not an afterthought.

## Images

- Format: AVIF/WebP with fallback; SVG for anything geometric.
- Every image declares dimensions or `aspect-ratio` — zero CLS from media. `object-fit: cover` with a defined focal point for cards/heroes.
- Lazy-load below the fold; the LCP hero image loads eagerly with `fetchpriority="high"` — never `loading="lazy"` on it. The hero visual is a Lighthouse decision: design it so it can ship as an optimizable image/SVG in server HTML, not a JS-composed scene (playbook: `$alaa-frontend-developer` `references/41-lighthouse-and-web-vitals.md`).
- Responsive `srcset`/`sizes` for content imagery; do not ship desktop pixels to phones.
- Meaningful images get descriptive `alt`; decorative images get `alt=""` — never missing alt.
- Consistent treatment (radius from the token scale, same overlay/duotone recipe) so mixed-source photos read as one product.

## Favicons, app identity, and social images

Ship this set for every public product — a missing favicon reads as unfinished:

- SVG favicon (theme-aware via `prefers-color-scheme` inside the SVG) plus 32px `favicon.ico` fallback.
- `apple-touch-icon` 180x180 (opaque background, no transparency).
- PWA manifest icons 192 and 512 including a maskable variant (safe zone: keep the mark inside the inner 80%).
- `theme-color` meta for light and dark (`media` attribute) matched to the surface token.
- Open Graph: `og:image` 1200x630 (readable at thumbnail size — large mark + short claim, no UI screenshots with tiny text), `og:title/description`, `twitter:card summary_large_image`.
- Keep source artwork in the repo (SVG master) so regeneration is deterministic; document the export set in MASTER.md.

## Illustration direction

- One illustration language per product: consistent stroke weight, palette drawn from the design tokens, same level of abstraction. Never mix 3D renders, flat line art, and hand-drawn doodles.
- Illustrations serve state and story (empty states, onboarding, errors) — decorative filler dilutes them.
- Prefer SVG; recolor via `currentColor`/CSS variables so illustrations follow theme switches.

## Anti-patterns

- Emoji as navigation/status icons; three icon sets in one app; per-use pixel sizes.
- Raster logos scaled up; recolored partner logos.
- Hero images without dimensions (CLS), heavy PNGs where AVIF/SVG belongs.
- No favicon/OG set, or an OG image that is an unreadable full-page screenshot.
- Illustrations whose palette ignores the design tokens.

## Pairing guidance

- Token scales for icon sizes/radius: `20-design-tokens-and-theming.md`
- Image performance budgets and delivery: `$alaa-frontend-developer` (performance) and `$alaa-frontend-devops` (CDN/build)
- Quasar icon set wiring: `$alaa-quasar-app-vite-v3`
