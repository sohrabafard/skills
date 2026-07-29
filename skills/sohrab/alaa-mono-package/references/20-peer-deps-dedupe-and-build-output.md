# Peer Dependencies, Dedupe, and Build Output

Open this file to move a dependency between `dependencies`, `devDependencies`, and `peerDependencies`, or when a peer conflict appears at install or a framework warns that two copies are loaded.

## The peer contract

`SKILL.md` states which names are peers. Two things complete the contract here: each of those names also appears in the package's build `external` list, so the package's own bundle never inlines a copy; and the application provides the single instance that every package binds to.

How the single-instance requirement is checked: resolve each name from every workspace package and from the root application and compare the resolved real paths. Two paths means two copies, which means two module registries, and the symptom is in `references/12-exports-map-and-conditions.md` under a peer satisfied at two versions. `scripts/verify-package-entrypoints.mjs` performs the resolution and reports every distinct path with the packages that reach it.

*(The live `client` repository declares `quasar` and `vue` as peers in `packages/design-system-vue/package.json` and lists no framework runtime in its `dependencies`. `read: 2026-07-28`.)*

The version *ranges* — which major of `vue-router`, which range of `pinia`, which Node floor — are not this skill's values. They are owned by `/alaa-services-contract` (`$alaa-services-contract`), and their consequences for a Quasar app-vite v3 application by `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`), `references/21-cli-vite-and-config.md`. Read the range there and write it once, in the package manifest.

## Choosing the section

| The package… | Section | Because |
|---|---|---|
| calls the dependency at runtime and the application also uses it | `peerDependencies` | one instance must serve both, so the application resolves it |
| calls it at runtime and no consumer shares it | `dependencies` | the package owns the instance; duplication is harmless |
| uses it only to build, test, or typecheck itself | `devDependencies` | it must not reach a consumer's install graph |
| declares it as a peer and needs it to develop | `peerDependencies` **and** `devDependencies` | the peer states the contract; the dev entry makes the package buildable alone |

A runtime dependency the application also uses, placed in `dependencies`, is how a second copy gets installed. That is the defect this table exists to prevent.

## Dedupe wiring

Keeping the bundler's externalisation aligned with the application's dedupe configuration is required. **This skill does not write the bundler configuration.** The `resolve.dedupe` wiring, library-mode configuration, and dependency-optimisation settings belong to `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`), `references/22-cli-cookbook-and-examples.md`.

What this skill supplies is the input that wiring needs: the exact set of names that must resolve once, which is the peer contract above. When the single-realpath assertion fails and the manifests are correct, the fault is in the wiring and the finding goes to that skill with the resolved paths attached.

## Output format

- Every internal package emits ESM. The `require` condition and the dual-package hazard it creates are `references/12-exports-map-and-conditions.md`.
- Declaration output, `moduleResolution` consequences, and build targets are `references/35-types-and-declaration-output.md`.
- A change to a package's output shape — the emitted file names, the formats emitted, the presence of a declaration file — is a consumer-visible change and follows `references/45-release-and-version-gates.md`.

## What a duplicate looks like before it is diagnosed

Record these so the next occurrence is recognised rather than re-derived: a framework warning that it is loaded twice; an injected value present in one component and absent in another; a plugin registered on one instance and invisible to the other; `instanceof` failing against an object of the right class; a store whose state resets when read through a different import path.

All five have one cause and one detection method, above. Do not resolve any of them by bundling a second copy of the runtime inside the package; that converts an install-time warning into a permanent runtime defect.
