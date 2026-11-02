# Project Fallbacks

For a Node, Vite, Vitest, Quasar or Yarn failure, verify the current repository's scripts, installed Linux tools and supported flags first. Historical command shapes are candidates, not evidence that a command exists or passes in this checkout.

## Normal escalation path

A necessary gate blocked by the sandbox follows `references/10-wsl-sandbox-recovery.md`. Preserve the failed command and its proof scope. Common candidates, only when declared locally, include:

- `yarn test`, `yarn test:new`
- `yarn build`, `yarn build:ssr`
- `yarn workspace <pkg> test`, `yarn workspace <pkg> build`
- `quasar build --mode ssr`
- `yarn dev`, `quasar dev` when a development server is required for the task

These examples grant no installation or unsandboxed authority and replace no harness approval. Do not combine a gate with cleanup or unrelated effects. Verify any claimed prior approval's source and scope before relying on it.

## Historical `entekhabat-front` `/new` lane

These Linux adaptations of historical fallbacks have no observed WSL passes; verify them against the current repository before use.

- **`vue-tsc` resolution failure.** If `yarn typecheck:new` cannot resolve it, verify the installed Linux entry point and equivalent script options before considering `./node_modules/.bin/vue-tsc --noEmit -p tsconfig.new.json` from the same worktree.
- **Vitest loader or worker failure.** First classify the failure. A sandbox permission retry keeps the original command. Only with repository/version evidence that alternative flags are supported and appropriate, consider `node node_modules/vitest/vitest.mjs run -c <config> --configLoader native --pool threads <spec...>`. Changed loader/pool/spec flags are alternate evidence, not proof that the original gate passed.
- **Permission error before validation.** For Vitest, Vite, tsup, Quasar or esbuild, use the filesystem/process diagnosis in `references/20-command-and-path-discipline.md`. An error code alone does not establish sandbox causation or justify changing source.
