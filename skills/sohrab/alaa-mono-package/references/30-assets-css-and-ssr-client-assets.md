# Assets, CSS, and Client Assets

Open this file to add a CSS file, a font, an image, or any non-JS asset to a package, to change how one is referenced, or when a component renders unstyled in the consumer application.

## The rule

A package's runtime CSS and assets must be **reachable from a declared entry** so the application's bundler pulls them into the graph and emits them. Reachability is this skill's decision. Whether the emitted files then landed where the deployment serves them is `/alaa-frontend-devops` (`$alaa-frontend-devops`), `references/10-build-contract-and-artifacts.md`.

Reachable means one of exactly two things:

1. The CSS is imported from a module that the entry imports, transitively, so it is part of the module graph.
2. The CSS is published as its own subpath in `exports` — `"./style.css": "./dist/style.css"` — and every consumer imports that subpath explicitly. If this form is used, the package's `README.md` names the import line the consumer must add, because nothing else will tell them.

A package that does both has two ways to get the same CSS and will ship it twice.

## `sideEffects` is the field that silently removes it

**Symptom:** components render unstyled in the consumer application; the CSS is present in the package's `dist/` and absent from the final client asset output; it works in the package's own test run and not in the application.

**Cause:** `"sideEffects": false` in the package manifest. It tells the bundler that no module in this package does anything but export, so an imported-for-effect CSS module is tree-shaken away. It is a blanket claim, and it is false the moment the package ships a stylesheet.

**Rule:** a package that emits CSS declares `sideEffects` as an array listing every style extension it emits, not `false`.

```json
{ "sideEffects": ["**/*.css", "**/*.scss"] }
```

A package that emits no CSS may declare `"sideEffects": false`, and should, because it makes the application's tree-shaking effective. `scripts/verify-package-entrypoints.mjs` asserts the pairing: CSS emitted plus `sideEffects: false` is a failure.

*(Both shapes are live in `client`: `packages/design-system-vue/package.json` declares the array form and ships `dist/style.css`; `packages/sdk-core/package.json` declares `false` and emits no CSS. `read: 2026-07-28`.)*

## Referencing an asset

Reference a package asset with a static specifier the bundler resolves at build time: a plain `import`, or `new URL('./x.png', import.meta.url)`. A path assembled from a runtime variable is invisible to the bundler, so the file is never emitted and the URL points at nothing in production while working in development, where the source tree is still on disk.

This is the rule that "use deterministic asset paths" was standing in for. The test is mechanical: can the specifier be read as a literal string from the source without executing it? If not, the bundler cannot see it either.

Copying an asset into a side directory during a package build, outside the module graph, has the same effect: the application's build never learns the file exists.

## Fonts and media

Fonts referenced from a package's CSS are pulled in by the CSS loader and follow the CSS rule above. Media files referenced only from a template string, a configuration value, or an API response are **not** package assets in this sense — they are runtime URLs, and where they are hosted is `/alaa-frontend-devops` (`$alaa-frontend-devops`), `references/30-serving-caching-and-public-path.md`. Do not try to make the bundler emit them.

## Verifying

Build the application, then confirm each package asset the package declares is present in the final client asset output. When it is absent, work backwards through this file: static specifier, then `sideEffects`, then reachability from an entry. When it is present but served wrongly, the finding is not here; it is in the delivery skill.
