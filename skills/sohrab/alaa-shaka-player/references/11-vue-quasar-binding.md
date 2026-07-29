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
| `onBeforeUnmount` must `await` teardown. | Returning early leaves the network engine fetching segments after the route changed. |
| Follow `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`) for props (`interface Props` + `withDefaults`), composable shape, store shape and TypeScript strictness. | That skill owns those; this file states only what Shaka adds. |

## Typing the boundary without `any`

Shaka ships `.d.ts` for every build, but `package.json` `"types"` points at the **non-UI** build
(conflict C8 in `05-provenance-and-freshness.md`). Rather than `any`, declare a **structural seam**
naming only the members you call. `assets/templates/shakaTypes.ts` is that seam, ready to copy.

## Working snippet — the client-only, run-token, single-handle shape

```ts
import { onBeforeUnmount, onMounted, readonly, ref, watch, type Ref } from "vue";
import type { ShakaNamespace, ShakaPlayer } from "./shakaTypes";

export function useShakaPlayer(source: Ref<string | null>) {
  const videoEl = ref<HTMLVideoElement | null>(null);
  const buffering = ref(false);
  const errorCode = ref<number | null>(null);

  // NOT reactive. A plain closure binding: Vue can never proxy it.
  let player: ShakaPlayer | null = null;
  let run = 0;
  let disposed = false;
  const disposers: Array<() => void> = [];

  onMounted(() => { void loadSource(source.value); });
  watch(source, next => { void loadSource(next); });
  onBeforeUnmount(async () => { await dispose(); });   // awaited: teardown completes before unmount

  async function loadSource(uri: string | null): Promise<void> {
    const token = ++run;
    if (!uri || disposed) return;

    const shaka = normalize(await import("shaka-player/dist/shaka-player.ui.js"));
    if (disposed || token !== run) return;             // superseded while importing

    if (!player) {
      shaka.polyfill.installAll();
      if (shaka.Player.isBrowserSupported() === false) { errorCode.value = -1; return; }
      const next = new shaka.Player();
      await next.attach(videoEl.value!);
      if (disposed || token !== run) { await next.destroy(); return; }
      player = next;
      register(next);
    }
    try {
      await player.load(uri);
    } catch (e) {
      if (token === run) errorCode.value = (e as { code?: number }).code ?? null;
    }
  }

  function register(p: ShakaPlayer): void {
    const onBuffering = (e: unknown) => {
      buffering.value = (e as { buffering?: boolean }).buffering === true;
    };
    p.addEventListener("buffering", onBuffering);
    disposers.push(() => p.removeEventListener("buffering", onBuffering));
  }

  async function dispose(): Promise<void> {
    if (disposed) return;
    disposed = true;
    run += 1;
    while (disposers.length) disposers.pop()!();       // listeners and timers first
    const current = player;
    player = null;
    await current?.destroy();                          // then the player
  }

  // ONE handle. No second API object returned from an inner init().
  return Object.freeze({
    videoEl,
    buffering: readonly(buffering),
    errorCode: readonly(errorCode),
    dispose
  });
}

function normalize(mod: unknown): ShakaNamespace {
  const record = mod as { default?: unknown };
  return (record.default ?? mod) as ShakaNamespace;
}
```

## Quasar specifics

| Situation | What to do |
|---|---|
| SSR mode | Player code lives behind `onMounted` + dynamic `import()`. Nothing under `src/boot/` may import Shaka. |
| PWA / service worker | The Shaka bundle and `controls.modern.css` are ordinary assets; segment and manifest requests must **not** be routed through a cache-first strategy — range requests and live playlist refreshes break under it. Strategy ownership is `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`). |
| Fullscreen | Request fullscreen on the stage container, not on the `<video>` element, or your overlays disappear. When using the Shaka UI, `controls.toggleFullScreen()` handles it. |
| RTL layouts | UI config `showMenusOnTheRight` (added in 5.1.0) and the `--shaka-*` custom properties. Direction and typography are `/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`). |

**Best practice.** Keep exactly one module in the repository that imports `shaka-player`; everything
else imports your wrapper. A grep for `from "shaka-player` that returns more than one hit outside
tests is the signal that a module reached past the seam.
**Common mistake.** `const player = ref(new shaka.Player())`. Documented to fail at load time. The
second most common is putting the player into a Pinia store to "share it between routes" — Pinia state
is `reactive()`, so this is the same bug with a longer stack trace.
