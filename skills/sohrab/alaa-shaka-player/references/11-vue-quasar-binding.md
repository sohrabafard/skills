# Vue 3 + Quasar binding

Upstream documents framework integration for **Vue only, and only as a warning**. Everything below the
first section is this skill's own ground, not a restatement of an upstream page.

## The one upstream fact, verbatim

From `.../blob/v5.2.3/docs/tutorials/faq.md` (`verified`, read 2026-07-28):

> *"Currently, Shaka Player does not support being made into a Vue reactive object. When Vue wraps an
> object in a reactive Proxy, it also wraps nested objects. This results in Vue converting some of our
> internal values into Proxy objects, which causes failures at load-time. If you want to use Shaka
> Player in Vue, avoid making it into a reactive object; so don't declare it using a `ref()`, and if
> you put your player instance into a `data()` object, you can prefix the property name with `"$"` or
> `"_"` to make Vue not proxy them."*

The same hazard applies to any deep-proxying container: Pinia state, `reactive()`, MobX, Valtio.

React, Angular and Svelte guidance: `not documented` — searched all 34 files in `docs/tutorials/` and
`README.md` for "React", "Angular", "Svelte" on 2026-07-28; only Vue is addressed, plus a
Create-React-App note in the transmux-worker tutorial about the `public/` folder.

## The rules that follow

| Rule | Why |
|---|---|
| Hold the instance in a **closure-scoped `let`** inside the composable. Not `ref`, not `shallowRef`, not `reactive`, not a Pinia state field. | `shallowRef` is safe for the *instance* but invites a later refactor to `ref`; a plain `let` cannot be widened by accident. |
| Expose only **derived primitives** as `ref`s: `currentTime`, `duration`, `paused`, `buffering`, plus plain-object track option rows you built yourself. | Track objects returned by `getVariantTracks()` are Shaka's own objects; map them into your own plain rows before they touch reactivity. |
| Run every Shaka call **client-side only**: dynamic `import()` inside `onMounted`, never at module top level. | Quasar SSR and PWA prerender execute module top level on the server, where `HTMLMediaElement` does not exist. |
| Guard every async step with a **run token**. | A `src` change during `await ensurePlayer()` otherwise loads into a destroyed or superseded player. |
| Start cleanup synchronously in `onBeforeUnmount`; handle its asynchronous rejection. | Vue invokes hooks without awaiting their promises. An owner requiring settled destruction awaits the exposed `dispose()` before removing the component. |
| Follow `/alaa-vue-typescript-clean-code` for props (`interface Props` + `withDefaults`), composable shape, store shape and TypeScript strictness. | That skill owns those; this file states only what Shaka adds. |

## Typing the boundary without `any`

Shaka ships `.d.ts` for every build, but `package.json` `"types"` points at the **non-UI** build
(conflict C8 in `05-provenance-and-freshness.md`). Rather than `any`, declare a **structural seam**
naming only the members you call. `assets/templates/shakaTypes.ts` is that seam, ready to copy.

## Lifecycle implementation and proof

Use `assets/templates/useShakaPlayer.ts` and `assets/templates/ShakaPlayer.vue` as the single
implementation: client-only import, run tokens, synchronous invalidation/listener cleanup, a shared
idempotent disposal promise, and destruction of instances whose attach finishes after disposal.
A null source unloads playback; it does not permanently dispose the handle.

Vue's [lifecycle API](https://vuejs.org/api/composition-api-lifecycle.html#onbeforeunmount) and
[tagged renderer](https://github.com/vuejs/core/blob/v3.5.43/packages/runtime-core/src/renderer.ts)
(`unmountComponent`, read 2026-09-29) invoke before-unmount hooks synchronously without awaiting
returned promises. Do not claim that an async hook delays DOM removal.

```ts
// In the parent/controller that owns removal, while the child still exists:
await playerHandle.dispose();
showPlayer.value = false;
```

If disposal rejects, the controller handles the failure before deciding whether to remove/retry;
never log the raw Shaka error. The unmount hook remains a fallback for uncontrolled removal and
handles rejection with the wrapper's safe classifier. Test repeated disposal while destruction or
attachment is pending, null-source unload, and superseded loads. Node doubles prove orchestration;
real browser playback and network shutdown require `90-qa-modes-and-checklist.md`.

## Quasar specifics

| Situation | What to do |
|---|---|
| SSR mode | Player code lives behind `onMounted` + dynamic `import()`. Nothing under `src/boot/` may import Shaka. |
| PWA / service worker | The Shaka bundle and `controls.modern.css` are ordinary assets; segment and manifest requests must **not** be routed through a cache-first strategy — range requests and live playlist refreshes break under it. Strategy ownership is `/alaa-quasar-app-vite-v3`. |
| Fullscreen | Request fullscreen on the stage container, not on the `<video>` element, or your overlays disappear. When using the Shaka UI, `controls.toggleFullScreen()` handles it. |
| RTL layouts | UI config `showMenusOnTheRight` (added in 5.1.0) and the `--shaka-*` custom properties. Direction and typography are `/alaa-ui-ux-design-system`. |

**Best practice.** Keep exactly one module in the repository that imports `shaka-player`; everything
else imports your wrapper. A grep for `from "shaka-player` that returns more than one hit outside
tests is the signal that a module reached past the seam.
**Common mistake.** `const player = ref(new shaka.Player())`. Documented to fail at load time. The
second most common is putting the player into a Pinia store to "share it between routes" — Pinia state
is `reactive()`, so this is the same bug with a longer stack trace.

Serialize initial attachment and obsolete-instance destruction on the same video element. A run token
alone cannot stop an old `destroy()` from clearing a newer player's media state. After cleanup fails,
refuse a new attachment until a fresh owner can establish safe ownership. The canonical template
captures the pending session exactly once before disposal removes listeners; observer failure cannot
skip destruction. Null, undefined and primitive cleanup rejections map to the safe default error.
