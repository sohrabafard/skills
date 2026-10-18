# Project Fallbacks

Read this file only when the failing stack is Node, Vite, Vitest, Quasar, or a Yarn gate. Everything below is recorded from real sessions in one workspace. Treat it as local operational fact, not as general guidance for other repositories or ecosystems.

## Validation candidates for the normal escalation path

After a necessary sandboxed gate fails and prevents completion, follow
`references/20-command-and-path-discipline.md` for its exact-command retry under task authority and harness
approval policy. These Quasar/Vite command shapes are candidates; they record no approval, authorize no
unsandboxed execution and replace no harness prompt.

- `yarn test`
- `yarn test:new`
- `yarn build`
- `yarn build:ssr`
- `yarn workspace <pkg> test`
- `yarn workspace <pkg> build`
- `quasar build --mode ssr`
- `yarn dev`
- `quasar dev`

Keep the command exact and scoped. Do not combine it with cleanup or unrelated commands; those effects
require their own authority decision. Record any claimed prior approval's approver, date, source and scope
before relying on it; this file supplies none.

## `entekhabat-front` `/new` package lane

Keep these proven fallback shapes here in runtime-ops instead of repeating them in repo or package `AGENTS.md` files.

- **`vue-tsc` not resolved.** If `yarn typecheck:new` cannot resolve `vue-tsc`, retry `.\node_modules\.bin\vue-tsc.cmd --noEmit -p tsconfig.new.json`.
- **Vitest config-loader or worker-spawn friction.** If a focused Vitest run hits config-loader or worker-spawn friction, retry `node node_modules\vitest\vitest.mjs run -c <config> --configLoader native --pool threads <spec...>`.
- **`EPERM` before validation starts.** If Vitest, Vite, tsup, Quasar, or esbuild fails before the intended validation starts with `EPERM` or `spawn EPERM`, follow the exact-command retry and escalation path in `references/20-command-and-path-discipline.md` before changing source.
