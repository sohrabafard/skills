# Companion Boundaries, Conflicts and Browser Profiles

The routing table itself is in `00-topic-map.md`. This file answers the two questions that table cannot: what to
do when two owners both look right, and which browser profile to use.

## Conflict resolution

1. An explicit user instruction wins.
2. A repo-local `AGENTS.md` rule wins over this shared skill.
3. When two companion skills both apply, this skill stays loaded as the frontend baseline and the
   specialist is loaded for the exact bounded surface it owns. Two skills loaded for one surface means the
   boundary was not read.
4. When two skills appear to state the same rule differently, the owner named in the `00-topic-map.md` table is
   right and the other copy is a defect to report, not a choice to make.

## Boundaries that are commonly got wrong

- **Quasar versus this skill.** An exact API, a `quasar.config` key, a platform mode, a Workbox recipe or
  a migration step is `/alaa-quasar-app-vite-v3`. Whether the change is safe
  under SSR, and what it costs, is here.
- **Design system versus this skill.** What it should look like, how it behaves in a failure state, how it
  reads in RTL and Persian is `/alaa-ui-ux-design-system`. Whether it can be
  built without breaking hydration is here.
- **Clean code versus this skill.** How the Vue and TypeScript is written is
  `/alaa-vue-typescript-clean-code`. What the code must be true of
  because it renders on a server is here.
- **Storage versus caching.** The Cache API and the service worker are `30-pwa-sw-and-offline.md` and the
  Quasar skill. A database, a quota, an eviction, a draft, an outbox or a downloaded media asset is
  `/alaa-indexeddb-browser-storage`.
- **Player versus this skill.** Playback, DRM, adaptive bitrate, in-app download and player analytics are
  `/alaa-shaka-player`; it names this skill as its SSR and hydration partner, so
  mounting a player without breaking SSR, and its cost on the route, are decided here —
  `references/11-vue-quasar-binding.md` there is the seam.
- **Package versus application.** Whether a package emits an asset, exposes an entry, or declares a peer
  is `/alaa-mono-package`. How the application consumes the result is here.
- **Build versus delivery.** How the bundle is produced is here and in the Quasar skill; how it is gated,
  identified, served, cached and rolled back is `/alaa-frontend-devops`, which
  owns the frontend delivery gate register and writes no provider YAML and no Dockerfile.

## Browser profile selection

- `playwright_headless` — deterministic non-visual reproduction: console evidence, network evidence,
  snapshots, smoke checks.
- `playwright_visual` — headed visual QA: screenshot review, layout inspection, responsive checks, and
  anything where seeing the rendered page is the point.
- `/playwright` — straightforward automation runs from the terminal.
- `/playwright-interactive` — a stateful, long-running debugging loop with
  repeated reloads.
- Do not select `MCP_DOCKER` to obtain a headless browser when a Playwright headless profile exists;
  reserve it for Docker-specific isolation.

## Shared HTTP browser services

When a workspace provides shared browser MCP endpoints, use the endpoint assigned to the current runtime
(Codex or Claude) and the selected headless/visual mode. Resolve addresses from the active workspace
configuration; do not infer them from names, borrow another runtime's endpoint, or launch a duplicate
stdio server. A configured URL is not proof of an MCP handshake or browser launch.

- For parallel headless work, require an isolated session per connection. Do not enable shared context
  or reuse a fixed persistent profile across concurrent tasks. Do not assume visual login state carries over.
- For visual work, establish one task owner for the runtime's persistent profile before a browser call.
  Separate Codex and Claude profiles do not isolate two tasks in the same runtime. If another task owns
  it, or ownership is unknown, wait or use an isolated headless session when that satisfies the observation.
- HTTP transport and a tab identifier do not enforce exclusive ownership. Without a verified lease/queue,
  coordinate ownership explicitly; never claim the service prevents concurrent control.
- Use DevTools only for the named debugging/performance observation. If it controls the same browser,
  it must have the same task owner. A Playwright MCP URL is not a Chrome CDP endpoint. Do not invent
  a shared DevTools HTTP backend; its transport and session behavior require separate verification.
- Release only this task's sessions/tabs. Do not stop a shared service, close another task's browser,
  clear its storage, or delete its profile. An operator drains owners before restarting or upgrading.

Installation, ports, cache paths, display environment and service lifecycle belong to the workspace setup
guide, not this reusable skill. Browser cache sharing does not share session state or cap browser count.

Whether the browser opens at all is gate 5 in `SKILL.md`, not a profile question.
