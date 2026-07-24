# Project Fallbacks

Read this file only when the failing stack is Node, Vite, Vitest, Quasar, or a Yarn gate. Everything below is recorded from real sessions in one workspace. Treat it as local operational fact, not as general guidance for other repositories or ecosystems.

## Standing maintainer approval for unsandboxed validation gates

For Quasar/Vite app verification in this environment, the following gates have standing maintainer approval for unsandboxed execution when they are required validation gates, or when sandboxed esbuild `spawn EPERM` or local-server verification blocks completion:

- `yarn test`
- `yarn test:new`
- `yarn build`
- `yarn build:ssr`
- `yarn workspace <pkg> test`
- `yarn workspace <pkg> build`
- `quasar build --mode ssr`
- `yarn dev`
- `quasar dev`

Scope condition: keep the command exact and scoped. The standing approval covers each command in the shape listed above and nothing else. Do not pair it with cleanup or unrelated commands; a combined command line falls outside the approval and needs its own decision.

## `entekhabat-front` `/new` package lane

Keep these proven fallback shapes here in runtime-ops instead of repeating them in repo or package `AGENTS.md` files.

- **`vue-tsc` not resolved.** If `yarn typecheck:new` cannot resolve `vue-tsc`, retry `.\node_modules\.bin\vue-tsc.cmd --noEmit -p tsconfig.new.json`.
- **Vitest config-loader or worker-spawn friction.** If a focused Vitest run hits config-loader or worker-spawn friction, retry `node node_modules\vitest\vitest.mjs run -c <config> --configLoader native --pool threads <spec...>`.
- **`EPERM` before validation starts.** If Vitest, Vite, tsup, Quasar, or esbuild fails before the intended validation starts with `EPERM` or `spawn EPERM`, follow the exact-command retry and escalation path in `references/20-command-and-path-discipline.md` before changing source.
