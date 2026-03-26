# Companion Skill Routing

Use this file when the task spans more than one frontend surface and ownership is unclear.

## Routing rules

- `$quasar-skill-packe`
  - Use for exact Quasar APIs, `quasar.config`, boot files, platform modes, components, directives, plugins, and Quasar/Vite upgrade details.
  - Pair with this skill when Quasar specifics matter more than general frontend policy.

- `$frontend-skill`
  - Use for premium visual direction, composition, imagery, and motion language.
  - Pair with this skill when the UI needs stronger art direction, not just safe implementation.

- `$playwright`
  - Use for straightforward real-browser automation flows from the terminal.
  - Pair when the user explicitly asks for browser validation or the task requires a deterministic browser reproduction.

- `$playwright-interactive`
  - Use for persistent iterative browser or Electron debugging with repeated reload and QA loops.
  - Pair when the debugging session is stateful or long-running.

- `$api-designer`
  - Use for request and response envelopes, pagination, filtering, sorting, cacheability, and backward-compatible API contract changes.
  - Pair when frontend work depends on changing or formalizing backend contract shape.

- `$ssr-auth-guard`
  - Use for cookie-to-header mapping, SSR auth fetch wrappers, login or logout flows, and token-leakage prevention.
  - Pair when auth or protected-route behavior is in scope.

- `$devops-engineer`
  - Use for CI, Docker, reverse proxy, public path, remote assets, artifact locations, and deployment safety.
  - Pair when the frontend change can affect build or deployment contracts.

- `$monorepo-packages-contract-guard`
  - Use for `packages/*` consumption, dist-only package rules, asset emission, and `peerDependencies` externalization.
  - Pair when workspace package boundaries or package-built assets are involved.

- `$inline-doc-writer`
  - Use for documentation-only JSDoc and inline-comment passes.
  - Do not use it for logic changes.

- `$openai-docs`
  - Use for authoritative current OpenAI or Codex docs, examples, models, prompt rules, or skill-authoring guidance.
  - Pair when the task includes OpenAI-specific product facts or latest-official guidance.

## Conflict resolution

- User instruction wins.
- Repo-local `AGENTS.md` wins over this shared skill.
- If two companion skills apply, keep this skill as the frontend-policy baseline and load the specialist skill for the exact bounded surface it owns.
