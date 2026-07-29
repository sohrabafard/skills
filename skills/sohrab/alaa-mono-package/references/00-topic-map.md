# Topic Map

The single router for this skill. Every row names an observable situation. Match your situation, open that one file, and stop.

## Routes by what you are about to do

| You are about to… | Read |
|---|---|
| add, remove, rename, or repoint an entry in a package's `exports` map, or add a subpath or a condition | `references/12-exports-map-and-conditions.md` |
| write or change a dependency specifier for an internal workspace package, or run a filtered workspace command | `references/15-package-manager-modes.md` |
| move a dependency between `dependencies`, `devDependencies`, and `peerDependencies` | `references/20-peer-deps-dedupe-and-build-output.md` |
| decide the order in which packages build, or find that a build read an upstream `dist/` that was not there | `references/18-build-order-and-graph.md` |
| add a CSS file, a font, an image, or any non-JS asset to a package, or change how one is referenced | `references/30-assets-css-and-ssr-client-assets.md` |
| change what a package emits: format, declaration output, `moduleResolution`, or build target | `references/35-types-and-declaration-output.md` |
| import from another package, or find an import that reaches into `packages/*/src` | `references/10-package-boundary-and-entrypoints.md` |
| begin work in a lane where only one package or package family is writable | `references/10-package-boundary-and-entrypoints.md` |
| bump a package version, change a package's public surface, or hand a consumer a changed entrypoint | `references/45-release-and-version-gates.md` |
| add a dependency from outside the workspace, enable an install script, or answer a question about lockfile integrity | `references/50-supply-chain-and-provenance.md` |
| close out package work and say what was validated | `references/40-audit-and-verification.md` |
| decide whether a rule belongs to this skill or to another owner, or need the file path inside that owner's skill | `references/90-companion-boundary.md` |
| assert a version, a resolution semantic, or a "current behaviour" claim that this skill does not already state | `references/00-source-map.md` |

## Routes by symptom

| You are seeing… | Read |
|---|---|
| a peer dependency conflict at install, or a framework warning that two copies are loaded | `references/20-peer-deps-dedupe-and-build-output.md` |
| a component rendering unstyled in the consumer app, or a package's CSS missing from the final build | `references/30-assets-css-and-ssr-client-assets.md` |
| a consumer's type checker resolving a package's types to `any` while the runtime import works | `references/12-exports-map-and-conditions.md` |
| an import of a package path that resolves in the editor and throws at runtime, or the reverse | `references/12-exports-map-and-conditions.md` |
| a package that passes its own tests and fails when consumed from `dist` | `references/18-build-order-and-graph.md` |
| a package asset present in the package's `dist/` and absent from the final client asset output | `references/30-assets-css-and-ssr-client-assets.md` |
| a wrong asset URL in an SSR page | `/alaa-frontend-devops` (`$alaa-frontend-devops`), `references/30-serving-caching-and-public-path.md` — the served base is that skill's |
| two parallel builds producing different `dist/` contents for the same commit | `references/18-build-order-and-graph.md` |
| a state singleton behaving as though there are two of it | `references/12-exports-map-and-conditions.md`, the dual-package hazard |
