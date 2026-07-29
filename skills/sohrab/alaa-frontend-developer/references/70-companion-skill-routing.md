# Companion Boundaries, Conflicts and Browser Profiles

The routing table itself is in `SKILL.md`. This file answers the two questions that table cannot: what to
do when two owners both look right, and which browser profile to use.

## Conflict resolution

1. An explicit user instruction wins.
2. A repo-local `AGENTS.md` rule wins over this shared skill.
3. When two companion skills both apply, this skill stays loaded as the frontend baseline and the
   specialist is loaded for the exact bounded surface it owns. Two skills loaded for one surface means the
   boundary was not read.
4. When two skills appear to state the same rule differently, the owner named in the `SKILL.md` table is
   right and the other copy is a defect to report, not a choice to make.

## Boundaries that are commonly got wrong

- **Quasar versus this skill.** An exact API, a `quasar.config` key, a platform mode, a Workbox recipe or
  a migration step is `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`). Whether the change is safe
  under SSR, and what it costs, is here.
- **Design system versus this skill.** What it should look like, how it behaves in a failure state, how it
  reads in RTL and Persian is `/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`). Whether it can be
  built without breaking hydration is here.
- **Clean code versus this skill.** How the Vue and TypeScript is written is
  `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`). What the code must be true of
  because it renders on a server is here.
- **Storage versus caching.** The Cache API and the service worker are `30-pwa-sw-and-offline.md` and the
  Quasar skill. A database, a quota, an eviction, a draft, an outbox or a downloaded media asset is
  `/alaa-indexeddb-browser-storage` (`$alaa-indexeddb-browser-storage`).
- **Player versus this skill.** Playback, DRM, adaptive bitrate, in-app download and player analytics are
  `/alaa-shaka-player` (`$alaa-shaka-player`); it names this skill as its SSR and hydration partner, so
  mounting a player without breaking SSR, and its cost on the route, are decided here —
  `references/11-vue-quasar-binding.md` there is the seam.
- **Package versus application.** Whether a package emits an asset, exposes an entry, or declares a peer
  is `/alaa-mono-package` (`$alaa-mono-package`). How the application consumes the result is here.
- **Build versus delivery.** How the bundle is produced is here and in the Quasar skill; how it is gated,
  identified, served, cached and rolled back is `/alaa-frontend-devops` (`$alaa-frontend-devops`), which
  owns the frontend delivery gate register and writes no provider YAML and no Dockerfile.

## Browser profile selection

- `playwright_headless` — deterministic non-visual reproduction: console evidence, network evidence,
  snapshots, smoke checks.
- `playwright_visual` — headed visual QA: screenshot review, layout inspection, responsive checks, and
  anything where seeing the rendered page is the point.
- `/playwright` (`$playwright`) — straightforward automation runs from the terminal.
- `/playwright-interactive` (`$playwright-interactive`) — a stateful, long-running debugging loop with
  repeated reloads.
- Do not select `MCP_DOCKER` to obtain a headless browser when a Playwright headless profile exists;
  reserve it for Docker-specific isolation.

Whether the browser opens at all is gate 5 in `SKILL.md`, not a profile question.
