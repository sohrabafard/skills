# Layout Patterns and Examples

Use this file when the task is really about Quasar layout-shell behavior rather than just a component name.

This file restores the strongest parts of the old `quasar-layout-*` skills: `QLayout` semantics, `view` behavior, drawer modes, containerized layouts, and routing-with-layouts ownership.

## High-value layout playbooks

### `QLayout` and the `view` prop

- Treat `view` as layout behavior, not styling decoration.
- Always specify all layout sections in the `view` string even if some sections are not used.
- Uppercase letters in `view` matter because they change fixed-position behavior.
- Important warning:
  - CSS margins on `QLayout`, `QPageContainer`, `QHeader`, `QFooter`, or drawers can break the layout; use padding instead.

- ✅ Do — name every section in `view` and space content with padding.

```vue
<q-layout view="hHh lpR fFf">
  <q-page-container class="q-pa-md"><router-view /></q-page-container>
</q-layout>
```

- ❌ Don't — add margins to layout parts or shorten the `view` string.

```vue
<q-layout view="hhh" style="margin: 16px">  <!-- margin breaks offsets; view is incomplete -->
```

- Good search terms:
  - `view`, `uppercase fixed`, `layout builder`, `margin breaks layout`

### Containerized layouts

- Use containerized `QLayout` only when the layout must live inside a bounded box rather than own the whole window.
- Containerized layouts need explicit height or min-height.
- Drawer breakpoints in a containerized layout are based on the layout container width, not the browser window.

- Good search terms:
  - `containerized layout`, `min-height`, `layout container width`

### `QDrawer`

- Overlay mode forces fixed-position behavior regardless of lowercase/uppercase `view` letters.
- Mini mode does not apply in mobile behavior.
- `mini-to-overlay` still forces fixed positioning.
- If swipe-to-close conflicts with drawer content, search `no-swipe-close`.
- If drawer content includes images and touch gestures are involved, search `draggable="false"`.

- Minimal example:

```vue
<q-drawer
  v-model="leftDrawerOpen"
  show-if-above
  bordered
  :mini="miniState"
>
  <!-- navigation -->
</q-drawer>
```

- Good search terms:
  - `overlay mode`, `mini`, `mini-to-overlay`, `no-swipe-close`, `show-if-above`

### Routing with layouts and pages

- Prefer the layout component to own `QPageContainer` and `<router-view />`.
- Prefer page components to own `QPage`.
- Prefer nested routes over conditionally swapping layout shells inside page components.
- Quasar does not require a strict folder structure, but layout/page ownership still matters.

- Minimal route shape:

```js
const routes = [
  {
    path: '/user',
    component: () => import('layouts/UserLayout.vue'),
    children: [
      { path: 'feed', component: () => import('pages/UserFeedPage.vue') },
      { path: 'profile', component: () => import('pages/UserProfilePage.vue') }
    ]
  }
]
```

- Good search terms:
  - `routing with layouts and pages`, `nested routes`, `children routes`, `router-view`

### `QPageSticky` and `QPageScroller`

- Use them as page-level affordances, not arbitrary floating decoration.
- Check keyboard reachability and overlap with drawers, footers, and mobile safe areas.

- Good search terms:
  - `page sticky`, `page scroller`, `floating affordance`, `safe area`

## Review checklist

- Is the issue really in the layout shell, or is routing/boot/SSR state the actual cause?
- Does the `view` string still match the intended fixed/revealed behavior?
- Are margins being used where padding should be used?
- Is a containerized layout missing explicit height?
- Did drawer mode, overlay behavior, or mobile behavior change interaction expectations?

## Notes

- Pair this file with `21-cli-vite-and-config.md` when the layout issue touches routing/bootstrap structure.
- Pair this file with `31-ssr-pwa-and-security.md` when layout state depends on SSR or hydration.
