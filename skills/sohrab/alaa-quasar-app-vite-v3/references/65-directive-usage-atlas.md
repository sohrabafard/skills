# Directive Usage Atlas

Load only when directive behavior/snippet shape matters; use `64-plugins-composables-directives-options-utils.md` as the light entry. Examples are curated starts—query the installed directive API via `05-authority-and-api-lookup.md` for exact values/modifiers/arguments.

## Playbooks

### `v-close-popup`

Use inside real child content of `QMenu`, `QDialog`, or `QPopupProxy` to close the nearest popup chain; use direct `v-model` control when no parent-child popup chain exists. No value closes one parent; `v-close-popup="2"` closes multiple levels; chained `QMenu`s count as one level; visually nested sibling dialogs do not share a chain.

```vue
<q-menu><q-list>
  <q-item clickable v-close-popup @click="selectRow(row)"><q-item-section>Edit</q-item-section></q-item>
</q-list></q-menu>
<q-btn label="Save and close all" color="primary" v-close-popup="2" />
```

✅ Do — use it in a real popup child. ❌ Don't — use it across sibling dialogs; toggle their `v-model`s.

Search: `close popup levels`, `v-close-popup 2`, `dialog menu chain`, `QPopupProxy separates chains`.

### `v-intersection`

Use for visibility-triggered lazy rendering/loading/analytics/reveal; prefer `QIntersection` when a component expresses the task better. Keep placeholder size stable; in universal apps keep SSR markup deterministic and start visibility work after mount. Verify the easy-to-misremember callback/options shape:

```vue
<div v-intersection="onIntersection" class="preview-card">...</div>
<div v-intersection="{ handler: onIntersection, cfg: { threshold: 0.4 } }" />
```

```js
function onIntersection (entry) { if (entry.isIntersecting) loadMore() }
```

Search: `handler`, `cfg`, `threshold`, `once`, `lazy render`, `placeholder height`.

### `v-ripple`

Use on genuinely interactive surfaces; prefer Quasar buttons/items, which already align ripple and semantics. Ripple is never the only affordance and never decoration on disabled/non-interactive wrappers.

```vue
<div v-ripple role="button" tabindex="0" class="cursor-pointer q-pa-sm rounded-borders">Open details</div>
```

✅ Do — add `role`, `tabindex`, and a keyboard handler to a custom surface (or use `QBtn`/`QItem`). ❌ Don't — imply interaction with ripple where none exists.

Search: `v-ripple`, `keyboard fallback`, `focus visible`, `reduced motion`.

### Touch directives

`TouchPan`, `TouchSwipe`, `TouchHold`, and `TouchRepeat` add gestures; they do not replace keyboard/desktop interaction. Search: `touch pan prevent`, `touch swipe mouse`, `touch hold`, `keyboard alternative`.

## Selection

- Popup close: `v-close-popup`.
- Visibility work: `v-intersection` or `QIntersection`.
- Ink feedback: `v-ripple` on an accessible interactive surface.
- Gesture: touch directive plus keyboard/desktop fallback.

Concept-only reminders, one-line descriptions, and directives mirroring standard Vue behavior do not need examples. Pair with `31-ssr-pwa-and-security.md` for hydration timing, client APIs, or SSR visibility-driven loading.
