# Layout Patterns and Examples

You are building or fixing an app shell: `QLayout` `view`, drawers, a containerized layout, or which component owns `QPageContainer` and `<router-view />`. This file owns layout and page ownership; no other file in this pack restates it.

## Playbooks

### `QLayout` / `view`

- `view` defines behavior, not decoration: include every section; uppercase changes fixed positioning.
- Never margin `QLayout`, `QPageContainer`, `QHeader`, `QFooter`, or drawers; use padding or offsets break.

```vue
<!-- Do --> <q-layout view="hHh lpR fFf"><q-page-container class="q-pa-md"><router-view /></q-page-container></q-layout>
<!-- Don't: incomplete view + broken offsets --> <q-layout view="hhh" style="margin:16px">
```

Search: `view`, `uppercase fixed`, `layout builder`, `margin breaks layout`.

### Containerized layouts

Use only inside a bounded box; set explicit height/min-height. Drawer breakpoints use container width, not window width. Search: `containerized layout`, `min-height`, `layout container width`.

### `QDrawer`

- Overlay mode forces fixed positioning regardless of `view` case; so does `mini-to-overlay`.
- Mini mode does not apply in mobile behavior.
- For gesture conflicts search `no-swipe-close`; for touchable image content search `draggable="false"`.

```vue
<q-drawer v-model="leftDrawerOpen" show-if-above bordered :mini="miniState"><!-- navigation --></q-drawer>
```

Search: `overlay mode`, `mini`, `mini-to-overlay`, `no-swipe-close`, `show-if-above`.

### Routing with layouts/pages

The layout should own `QPageContainer` + `<router-view />`; pages own `QPage`. Prefer nested routes to conditional shell swapping. Folder structure is flexible; ownership is not.

```js
const routes = [{ path: '/user', component: () => import('layouts/UserLayout.vue'), children: [
  { path: 'feed', component: () => import('pages/UserFeedPage.vue') },
  { path: 'profile', component: () => import('pages/UserProfilePage.vue') }
] }]
```

Search: `routing with layouts and pages`, `nested routes`, `children routes`, `router-view`.

### `QPageSticky` / `QPageScroller`

Use as page affordances, not decoration; verify keyboard reachability and overlap with drawers, footers, and mobile safe areas. Search: `page sticky`, `page scroller`, `floating affordance`, `safe area`.

## Review

- Is routing/boot/SSR state, not the shell, the cause?
- Does `view` still express intended fixed/revealed behavior? Are margins used instead of padding?
- Does a containerized layout have height? Did drawer overlay/mobile mode change interaction?

Also load `21-cli-vite-and-config.md` for routing/bootstrap and `31-ssr-pwa-and-security.md` for SSR/hydration state.
