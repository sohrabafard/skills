# Image Delivery and Placeholders

Use this file when the task is really about deterministic `QImg` delivery strategy, placeholders, responsive image candidates, or SSR-safe image sizing.

This file generalizes the value of the old image-helper skill without assuming every Quasar repo uses the same image server or placeholder pipeline.

## High-value rules

### Deterministic SSR first

- Do not measure the DOM after hydration just to compute image URLs.
- Do not "fix" SSR issues by rendering one image tree on the server and another after mount.
- Prefer stable markup plus native responsive image features.

### Placeholder strategy

- If the repo standardizes a shared placeholder image, keep it consistent across the app.
- `placeholder-src` is useful when large images or slow networks are common.
- Prefer `ratio` or deterministic sizing to preserve layout footprint and avoid CLS.

### Responsive image delivery

- If the slot size is responsive, prefer native `srcset` and `sizes`.
- If width/height are explicitly known, a single resized URL can be fine.
- If the exact slot width is not deterministic at SSR time, do not fake precision with post-hydrate measurement; use responsive candidates instead.

### Query-parameter resizing

- If the backend or CDN supports `w/h` or similar resize params, keep URL generation deterministic.
- Preserve existing query params.
- Do not keep stacking duplicate `w/h` params.
- Do not derive requested size from the original file size when the display slot is much smaller.

### Do / Don't

✅ Do — let the browser pick with native `srcset`/`sizes` plus a `ratio` to hold layout.

```vue
<q-img :src="base" :srcset="`${base}?w=480 480w, ${base}?w=960 960w`" sizes="(max-width: 600px) 480px, 960px" :ratio="16/9" />
```

❌ Don't — measure the element after mount to compute an image URL; it causes a server/client request mismatch and layout shift.

```js
onMounted(() => { url.value = `${base}?w=${el.value.clientWidth}` }) // post-hydrate measurement
```

## Decision heuristics

- Fixed-size avatar/icon/media slot:
  - use an explicit size and one resized URL
- Responsive grid/card media:
  - use `srcset` and `sizes`
- Unknown or highly dynamic slot size:
  - keep the base URL and avoid false precision unless the repo already has a deterministic sizing contract

## Good search terms

- `placeholder-src`, `ratio`, `srcset`, `sizes`, `responsive images`, `context menu`, `deterministic w/h`, `avoid DOM measurement`

## Notes

- Pair this file with `41-component-usage-atlas.md` for baseline `QImg` behavior.
- Pair this file with `20-ssr-pwa-and-security.md` when lazy loading, offline behavior, or hydration safety is involved.
