# Architecture and module seams

## The three layers

**Layer 1 — the core wrapper.** One module owns: dynamic import, `shaka.polyfill.installAll()`,
`shaka.Player.isBrowserSupported()`, construction, `attach()`, `configure()`, networking filters,
`load()`, error classification, and teardown. It exposes **one** lifecycle handle. Nothing else in
the application calls a Shaka method.

**Layer 2 — modules that consume player events.** Ads, analytics, overlays and markers, and any
schedule or playlist driver. Each subscribes to player events and reads `getStats()`. **None mutates
core internals.**

**Layer 3 — the Vue/Quasar shell.** Controls, menus, overlays, dialogs. It reads the wrapper's
reactive state and calls the wrapper's actions. It never touches `shaka.*`.

## Why the seams sit exactly there

| Seam | Invariant that makes it safe |
|---|---|
| Core / modules | Every module input is a player **event** or a `getStats()` snapshot — both read-only. A module cannot corrupt playback state because it has no writable handle to it. |
| Modules / shell | The shell renders from reactive refs the wrapper owns. Shaka's own instance is never reactive (upstream: Vue's reactive Proxy breaks Shaka at load time), so the boundary is also what keeps reactivity out. |
| Core / networking | Filters are the only place a credential enters. One place to audit, one place to refresh. See `42-media-url-trust-and-presigned.md`. |

## Two lifecycle handles is the defect to look for

The failure this layering exists to prevent: a composable that returns `{init, load, destroy}` while
`init` **also** returns an object with its own `load`/`destroy`. Two callers then hold two handles to
one player and both can destroy it. Return one frozen object. The teardown path must be reachable from
exactly one place.

## Parallel work

The module seams — **core / ads / analytics / overlay and markers / conductor / QA** — are the safe
parallel-work boundaries, because each consumes player events and none mutates core internals; two
lanes editing two modules cannot produce a playback bug in the other's module. How lanes are spawned,
pinned, sandboxed and merged is owned by `/alaa-cc-orchestrator` (`$alaa-cc-orchestrator`) and
`/alaa-codex-orchestrator` (`$alaa-codex-orchestrator`). This skill defines the boundary; it does not
define a role roster, and a role name from those orchestrators wins over any name used here.

## Working snippet — the module boundary in one file

```ts
// The core wrapper exposes a read-only event surface. Modules get this, not the player.
export interface PlayerEventPort {
  on(event: string, listener: (payload: unknown) => void): () => void;
  stats(): Readonly<Record<string, unknown>>;
}

// A module. It cannot reach the player: no method here can change playback.
export function createRebufferWatcher(port: PlayerEventPort) {
  let events = 0;
  let startedAt: number | null = null;
  let accumulatedMs = 0;

  const off = port.on("buffering", payload => {
    const buffering = (payload as { buffering?: boolean }).buffering === true;
    if (buffering) {
      startedAt = performance.now();
      events += 1;
      return;
    }
    if (startedAt !== null) {
      accumulatedMs += performance.now() - startedAt;
      startedAt = null;
    }
  });

  return Object.freeze({
    // Quantities only. The NAMES these are reported under come from
    // /alaa-services-contract ($alaa-services-contract) - see 60-analytics-and-getstats.md.
    quantities: () => ({ rebufferEventCount: events, rebufferMilliseconds: accumulatedMs }),
    dispose: off
  });
}
```

## Where each Alaa product concern lives

| Concern | Layer | Reference |
|---|---|---|
| Quality / audio / subtitle menus | 3, driven by 1 | `26-tracks-audio-video-text.md` |
| Watch-time and QoE | 2 | `60-analytics-and-getstats.md` |
| Ads and interstitials | 2 | `55-ads-vast-vmap-and-ima.md` |
| Timeline markers, chapters, share links | 2 | `30-playback-speed-seek-trickplay.md`, `42-media-url-trust-and-presigned.md` |
| Schedule / playlist driving `load()` | 2 | `37-switching-source.md` |
| Downloaded-for-offline library | 2 | `50-offline-and-in-app-download.md` |

**Best practice.** Give every module a `dispose()` that the core wrapper calls in its own teardown, in
registration order reversed, before `player.destroy()`.
**Common mistake.** Letting a module hold the player directly "just for one call" — the call is always
`player.configure()` or `selectVariantTrack()`, and it is always the one that races the core wrapper's
own reconfiguration on the next `load()`.
