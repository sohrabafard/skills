---
name: alaa-shaka-player
description: "Version-aware Shaka Player capability atlas: lifecycle, DASH and HLS, native HLS on Safari, adaptive bitrate, track and language selection, subtitles, live and low latency, unstable-network resilience and retry budgets, source switching, the networking engine and request filters, DRM, offline in-app download, ads, playback analytics, the error taxonomy, and the Vue plus Quasar binding. Use when writing, reviewing, debugging or upgrading code that constructs shaka.Player, calls player.configure(), registers a networking filter, or handles a Shaka event or error. Do not use it for a plain HTML video element with no adaptive manifest; for player-skin art direction (/alaa-ui-ux-design-system); for the IndexedDB substrate (/alaa-indexeddb-browser-storage); or for retry and degradation doctrine (/alaa-reliability-sla)."
---

# Alaa Shaka Player

## Purpose

Shaka is the playback engine; Vue and Quasar are the product shell; ads, analytics and overlays are modules that consume player events. This skill maps APIs, configuration, events and errors from a tagged baseline, with newer release deltas and consumer validation requirements in `references/05-provenance-and-freshness.md` and `references/80-version-migration-and-release-deltas.md`. It states the Shaka-side binding of doctrine other skills own.

## Router

`references/00-topic-map.md` is the only router in this skill. Read it first and load the one or two rows that match what is in front of you.

## Portability and model routing

This skill names no model and no reasoning effort. Take both from `/alaa-prompting-guide`, `references/50-effort-and-thinking.md`, at the time you run the lane. Frontmatter is `name` and `description` only; `agents/openai.yaml` is Codex-only UI metadata. Output discipline follows `/alaa-low-noise`.

## When NOT to use

The media is a single progressive MP4 with no manifest, no DRM, no track selection and no telemetry, and a bare `<video>` element already plays it.

## Non-negotiable rules

1. **Pin an exact `shaka-player` version in `package.json`** — no `^`, no `~`, no `latest`. Three vendor endpoints disagreed about "latest" on 2026-07-28 (conflict C1 in `references/05-provenance-and-freshness.md`). Before changing the pin, re-read that file's re-read rule and record the new release URL and today's date in it.
2. **Construct the Player with no arguments, then `await player.attach(video)`.** `new shaka.Player(video)` still works in 5.2.3 and logs a deprecation warning; it also hides the async attach step, which is the step that fails on iOS Safari when the element is not ready. Call `shaka.polyfill.installAll()` before `shaka.Player.isBrowserSupported()`, and register the `error` listener before `load()`.
3. **Never place the Player instance in Vue reactivity.** Upstream states that Vue's reactive Proxy converts Shaka's internal values into Proxies and this fails at load time. Hold it in a module- or closure-scoped `let`, or in a `$`- or `_`-prefixed field. If the instance must enter a container you are not allowed to change, wrap it with `markRaw` and name that container's path in the PR description.
4. **Begin teardown before unmount: invalidate pending work and snapshot the pending session once before removing listeners, then** clear every interval and timeout, remove every listener you registered on the player, on the `<video>` element and on `document`, then `await player.destroy()`. Vue does not await an async `onBeforeUnmount` callback. Keep one awaitable, idempotent disposal promise; an owner requiring completed destruction must await it before removing the component. The hook starts cleanup and handles rejection as a fallback (`references/11-vue-quasar-binding.md`). After `destroy()` the instance is dead — every method throws `LOAD_INTERRUPTED` (7000).
5. **Write the v6-ready preference spelling in every new or touched line:** `preferredAudio`, `preferredText`, `preferredVideo` as arrays. The fifteen individual `preferred*` scalars are deprecated for removal in v6.0 and are already absent from the shipped `.d.ts`, so they do not type-check. Set `abr.restrictions` (soft) rather than top-level `restrictions` (hard) unless a written requirement demands a hard cap; the hard form can fail playback outright with `RESTRICTIONS_CANNOT_BE_MET` (4012).
6. **Set all three retry budgets explicitly.** Shaka's `maxAttempts` default is `2`. Configure `manifest.retryParameters`, `streaming.retryParameters` and `drm.retryParameters` with values taken from `/alaa-reliability-sla`, `references/20-retries.md`, and keep `fuzzFactor` at `0.5` — it exists to stop client stampedes.
7. **A credential never travels as a component prop.** A manifest URL that carries a signature, and any bearer token, enter the player only through a request filter that reads a token *getter*, so the filter can refresh on retry. Never print a Shaka error object into the DOM or a log line: `error.data` for a network error carries the failing URI and its query string.
8. **Request every telemetry event name, field name and metric name from `/alaa-services-contract`.** This skill states which *quantities* playback can produce; it defines no name. Do not invent one and do not ship one that is not in that contract.

## Ownership and boundary

This skill owns: the `player.configure()` surface and its safe defaults for this stack; the `shaka.util.Error` taxonomy and which Shaka mechanism handles each category; player lifecycle inside a Vue/Quasar SPA; DASH/HLS/DRM behaviour per browser and platform; the Shaka side of offline download; version migration across Shaka releases. Everything below is cited, never restated.

| Ground | Owner |
|---|---|
| Retry, backoff, timeout, degradation doctrine | `/alaa-reliability-sla` |
| Every event, field and metric name in a payload | `/alaa-services-contract` |
| Telemetry requirement levels and gates | `/alaa-observability-soc` |
| Threat classes, review triggers, fail-closed doctrine | `/alaa-security-review` |
| A client-supplied opaque value carries no trust | `/alaa-trust-gateway-auth` |
| Presigned media URLs, TTL and the `STORAGE_*` contract | `/alaa-minio-object-storage`, `/alaa-arvan-object-storage` |
| IndexedDB quota, eviction, persistence, mid-session eviction | `/alaa-indexeddb-browser-storage` |
| Vue component, composable and Pinia store shape; TypeScript strictness | `/alaa-vue-typescript-clean-code` |
| Quasar and Vite build, SSR and PWA config | `/alaa-quasar-app-vite-v3`, `/alaa-frontend-developer` |
| Test design and the six proof levels | `/alaa-testing-strategy` |
| Digit and text normalization of any user input | `/alaa-input-normalization` |
| Colour, type, motion and component styling of a skin | `/alaa-ui-ux-design-system` |
| Spawning, pinning and sandboxing parallel lanes | `/alaa-cc-orchestrator`, `/alaa-codex-orchestrator` |
| JSDoc and annotation shape on emitted files | `/alaa-frontend-doc-annotations` |
| Browser execution and evidence capture | `/playwright` |
| Where a skill is installed | repository `install-skills.md` |

## Implementation order

1. Read `references/00-topic-map.md` and load the rows that match the task.
2. Confirm the installed version and read `references/80-version-migration-and-release-deltas.md` for the selected target and intervening releases. Run `scripts/check-shaka-api.mjs` against the repository; its v5.2.3 rules are a historical static baseline, not proof of every newer API.
3. Write or repair the core wrapper: import, polyfill, support check, attach, `configure()`, filters, error classification, teardown (`references/20-core-lifecycle.md`, `references/15-configure-surface-and-safe-defaults.md`).
4. Add the capability the task actually asked for, one reference file at a time.
5. Add the resilience policy (`references/35-unstable-networks-and-resilience.md`) — it is not optional on a mobile network.
6. Prove it with the mode `references/90-qa-modes-and-checklist.md` selects, and record the deliverables below.

## Output expectations

Every player change ships with: the `player.configure()` block it changed, with each non-default value traced to the reference that justifies it; the error classes it newly handles and what the user sees for each; the telemetry quantities it emits and the `/alaa-services-contract` names requested for them; and the QA evidence `references/90-qa-modes-and-checklist.md` requires. Emit `.ts` and `.vue` with `lang="ts"` following `/alaa-vue-typescript-clean-code`. If the host repository is JavaScript-only, say so and stop before generating files.
