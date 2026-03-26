# Peer Dependencies, Dedupe, and Build Output

Use this file when the task affects package build config or shared dependencies.

## Dependency rules

- Shared frontend dependencies such as `vue` and `quasar` should not be bundled into internal package outputs.
- Use `peerDependencies` where that is the repo contract.
- Keep bundler externalization and root-app dedupe rules aligned.

## Output rules

- Packages should emit stable ESM outputs unless the repo explicitly requires something else.
- Package entry files should be predictable and documented.
- Do not break the root app by changing package output shape silently.

## Common failure modes

- duplicate Vue runtime
- duplicate Quasar runtime
- package output that works locally but breaks in the final app build
- source-only imports that hide missing dist output problems
