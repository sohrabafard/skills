# Image Delivery and Placeholders

You are about to emit an image URL, a `srcset`, a placeholder, or a reserved size. Do not assume a shared image server or resize pipeline exists; check the repository first.

## Rules

- Keep SSR markup stable: never measure the DOM after hydration to compute URLs or render different server/mounted image trees; prefer native responsive images.
- Reuse any repo-standard placeholder. Use `placeholder-src` for large/slow media and `ratio` or deterministic dimensions to reserve space and avoid CLS.
- Responsive slot: default to `srcset` + `sizes`. Known fixed width/height: one resized URL is fine. Unknown SSR width: use candidates, not post-hydrate fake precision.
- Backend/CDN resize params (`w/h` or equivalent): generate deterministically, preserve existing query params, replace rather than stack duplicate size params, and size for the display slot—not the original file.

```vue
<!-- Do: browser selection + reserved ratio. -->
<q-img :src="base" :srcset="`${base}?w=480 480w, ${base}?w=960 960w`" sizes="(max-width: 600px) 480px, 960px" :ratio="16/9" />
```

```js
// Don't: server/client request mismatch and layout shift.
onMounted(() => { url.value = `${base}?w=${el.value.clientWidth}` })
```

## Decision table

| Slot | Default |
| --- | --- |
| Fixed avatar/icon/media | Explicit size + one resized URL |
| Responsive grid/card | `srcset` + `sizes` |
| Unknown/highly dynamic | Base URL; avoid false precision unless the repo has a deterministic contract |

Search: `placeholder-src`, `ratio`, `srcset`, `sizes`, `responsive images`, `context menu`, `deterministic w/h`, `avoid DOM measurement`.

Pair with `61-component-usage-atlas.md` for `QImg`; add `31-ssr-pwa-and-security.md` for lazy loading, offline behavior, or hydration.
