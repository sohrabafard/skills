Version-sensitive claims in this topic depend on [Shaka provenance and freshness](../05-provenance-and-freshness.md).

## Lifecycle and leaks

| Symptom | Fix |
|---|---|
| Memory grows after route changes; network activity continues after unmount | Clear timers, remove **every** listener, then start destruction. Vue does not await `onBeforeUnmount`; await the shared disposal promise in the removal owner when completion is required (`../11-vue-quasar-binding.md`). `20-…` |
| Events fire twice | Two Players on one element — usually declarative UI setup (`video['ui']`) plus a manually constructed Player. `65-…` |
| Two callers can destroy the same player | The composable returned two lifecycle handles. Return one frozen object. `10-…` |
| Everything throws `LOAD_INTERRUPTED` (7000) | The Player was used after `destroy()`. It is dead; construct a new one. `20-…` |
| A custom UI element leaks | Since v4.0, `IUIElement` plugins must implement `release()`, not `destroy()`. `65-…` |
| Changing source loses all filters and config | You destroyed and reconstructed the Player. `load()` is the switch. `37-…` |
## Diagnostics workflow

1. Reproduce on a **minimal known-good stream** first; that separates "the player" from "this asset".
2. Load `dist/shaka-player.compiled.debug.js` in a lab page — the debug build retains logging and the
   uncompiled error `message` is `'Shaka Error CATEGORY.CODE_NAME (data)'` rather than a bare number.
3. Capture the emitted event sequence, `downloadfailed` payloads (**type and status, never the URI**)
   and `getStats()` at failure. Choose the evidence mode from `../90-qa-modes-and-checklist.md`.
4. Check `../05-provenance-and-freshness.md` before carrying forward any workaround: an open issue is a
   symptom, never a fixed behaviour.

**Best practice.** Start from the error **code**, not the message — the compiled build's message is
only `'Shaka Error <code>'`, so a symptom search on message text finds nothing.
**Common mistake.** Reaching for a custom workaround before checking whether the current release
already fixed it. `../80-version-migration-and-release-deltas.md` lists the last two minors' fixes, and
5.2.1–5.2.3 alone repaired playhead position after an MSE reload, header isolation across retries, and
MSE append failure on variant switch.
