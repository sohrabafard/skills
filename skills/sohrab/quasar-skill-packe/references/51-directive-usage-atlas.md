# Directive Usage Atlas

Use this file when the task names a Quasar directive and the agent needs more than a symbol list: what the directive is for, what behavior is easy to miss, and which minimal snippet shape is safest to start from.

Only load this file when directive behavior or snippet shape matters. Keep `50-plugins-composables-directives-options-utils.md` as the lighter entry point.

## High-value directive playbooks

### `v-close-popup`

- Use inside `QMenu`, `QDialog`, or `QPopupProxy` content when a click should close the nearest popup chain.
- Prefer direct `v-model` control when the popup relationship is not a real parent-child chain.
- Important usage notes:
  - without a value, it closes the parent popup
  - `v-close-popup="2"` or higher closes multiple popup levels
  - chained `QMenu` instances count as one level
  - sibling dialogs do not become closable together just because they are visually nested

```vue
<q-menu>
  <q-list>
    <q-item clickable v-close-popup @click="selectRow(row)">
      <q-item-section>Edit</q-item-section>
    </q-item>
  </q-list>
</q-menu>
```

```vue
<q-btn label="Save and close all" color="primary" v-close-popup="2" />
```

- Good search terms:
  - `close popup levels`, `v-close-popup 2`, `dialog menu chain`, `QPopupProxy separates chains`

### `v-intersection`

- Use when visibility changes should trigger work such as lazy rendering, data loading, analytics, or progressive reveal.
- Prefer `QIntersection` when the task is better expressed as a component rather than a bare directive.
- Important usage notes:
  - the callback shape and options object are easy to misremember, so start from a small example
  - intersection logic often needs a stable placeholder size to avoid layout jumps
  - in universal apps, keep SSR markup deterministic and let visibility-triggered work happen after mount

```vue
<div
  v-intersection="onIntersection"
  class="preview-card"
>
  ...
</div>
```

```js
function onIntersection (entry) {
  if (entry.isIntersecting) {
    loadMore()
  }
}
```

```vue
<div
  v-intersection="{
    handler: onIntersection,
    cfg: { threshold: 0.4 }
  }"
/>
```

- Good search terms:
  - `handler`, `cfg`, `threshold`, `once`, `lazy render`, `placeholder height`

### `v-ripple`

- Use on genuinely interactive surfaces, not purely decorative wrappers.
- Prefer built-in Quasar button/list components when possible because they already align ripple with interaction semantics.
- Important usage notes:
  - do not let ripple become the only affordance; keyboard focus and accessible labeling still matter
  - avoid adding ripple to disabled or non-interactive containers just for visual effect

```vue
<div
  v-ripple
  role="button"
  tabindex="0"
  class="cursor-pointer q-pa-sm rounded-borders"
>
  Open details
</div>
```

- Good search terms:
  - `v-ripple`, `keyboard fallback`, `focus visible`, `reduced motion`

### Touch directives

- `TouchPan`, `TouchSwipe`, `TouchHold`, and `TouchRepeat` are gesture helpers, not full interaction design solutions.
- Prefer them when gesture input is additive, not when it would make the feature unusable from keyboard or desktop interaction alone.
- Good search terms:
  - `touch pan prevent`, `touch swipe mouse`, `touch hold`, `keyboard alternative`

## Directive selection heuristics

- Need popup closing inside menu/dialog content:
  - start with `v-close-popup`
- Need visibility-based loading or reveal:
  - start with `v-intersection` or evaluate `QIntersection`
- Need ink feedback on an interactive surface:
  - start with `v-ripple`
- Need gesture input:
  - start with a touch directive, then verify keyboard and desktop fallback

## What usually does NOT need examples

- a reminder that directives exist
- simple one-line conceptual descriptions
- APIs where Quasar mirrors standard Vue directive behavior without extra semantics

## Notes

- These examples are intentionally minimal. They are here because directive value shapes and popup-chain behavior are easy to get slightly wrong from memory.
- Pair this file with `20-ssr-pwa-and-security.md` if the directive affects hydration timing, client-only APIs, or visibility-based data loading in SSR routes.
