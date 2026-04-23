# Companion Skill Routing

Use this file when the task spans more than one frontend surface and ownership is unclear.

## Routing rules

- `$quasar-skill-packe`
  - Use for exact Quasar APIs, `quasar.config`, boot files, platform modes, components, directives, plugins, and Quasar/Vite upgrade details.
  - Pair with this skill when Quasar specifics matter more than general frontend policy.

- Visual direction beyond implementation constraints
  - This Sohrab pack does not currently include a dedicated visual-design skill.
  - Keep pure art direction out of this skill unless a concrete Vue, Quasar, Vite, SSR, accessibility, or implementation constraint is also in scope.

- `$playwright`
  - Use for straightforward real-browser automation flows from the terminal.
  - Pair when the user explicitly asks for browser validation or the task requires a deterministic browser reproduction.

- `$playwright-interactive`
  - Use for persistent iterative browser or Electron debugging with repeated reload and QA loops.
  - Pair when the debugging session is stateful or long-running.

- `$alaa-trust-gateway-auth`
  - Use for Ala gateway verification, trusted `X-*` headers, downstream auth context, refresh-cookie plus bearer-token flows, and tenant-context trust boundaries.
  - Pair when the project sits behind the Ala gateway or when frontend auth changes depend on gateway behavior.

- `$alaa-laravel-architecture`
  - Use when a frontend contract change requires backend endpoint, envelope, validation, or authorization implementation changes in the Ala Laravel stack.
  - Pair when the fix is no longer frontend-only.

- `$alaa-data-layer`
  - Use when the real problem is query shape, indexing, pagination cost, aggregate computation, or cache/DB trade-offs in the backend.
  - Pair when frontend data-shaping advice turns into schema or query work.

- `$alaa-frontend-devops`
  - Use for CI, Docker, reverse proxy, public path, remote assets, artifact locations, and deployment safety.
  - Pair when the frontend change can affect build or deployment contracts.

- `$alaa-mono-package`
  - Use for `packages/*` consumption, dist-only package rules, asset emission, and `peerDependencies` externalization.
  - Pair when workspace package boundaries or package-built assets are involved.

- `$alaa-frontend-doc-annotations`
  - Use for documentation-only JSDoc and inline-comment passes.
  - Do not use it for logic changes.

- `$openai-docs`
  - Use for authoritative current OpenAI or Codex docs, examples, models, prompt rules, or skill-authoring guidance.
  - Pair when the task includes OpenAI-specific product facts or latest-official guidance.

## Ownership notes

- This skill now owns generic frontend-facing SSR auth/session guidance, including:
  - BFF vs token-mediating backend vs browser-only flows
  - in-memory vs persistent token storage trade-offs
  - refresh orchestration and token-leakage anti-patterns
  - frontend-facing API envelopes, pagination, sparse payloads, cache validators, and UI-driven N+1 prevention
- When the work crosses from frontend policy into backend implementation, pair with the backend repo's architecture or data-layer skill instead of reviving deleted local frontend-only helper skills.

## Conflict resolution

- User instruction wins.
- Repo-local `AGENTS.md` wins over this shared skill.
- If two companion skills apply, keep this skill as the frontend-policy baseline and load the specialist skill for the exact bounded surface it owns.
