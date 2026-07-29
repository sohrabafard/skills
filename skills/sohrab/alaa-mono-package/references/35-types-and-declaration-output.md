# Types and Declaration Output

Open this file to change what a package emits — declaration output, `moduleResolution`, or build target — or when a consumer's type checker resolves a package to `any` while the runtime import works.

## Declarations are part of the public surface

A package's `.d.ts` output is consumed exactly like its JavaScript, and it breaks in the same ways. Treat it as an emitted artifact under the same rules:

- Every `exports` entry that a TypeScript consumer can import declares a `types` condition, and it is the **first** key in that conditions object. The ordering rule and what happens when it is violated are in `references/12-exports-map-and-conditions.md`; this file states that the `.d.ts` file must exist and must typecheck standalone.
- The declaration file typechecks against the package's own `tsconfig` with no unresolved imports. A `.d.ts` that references a type from a package the consumer does not have installed makes the consumer's build fail with an error inside a file they cannot edit.
- Types a consumer must name — the props of an exported component, the shape of a returned object, an error class — are exported from the entry, not left inferred. An inferred anonymous type cannot be written down by a consumer who needs to annotate a variable.

## Symptom: the consumer sees `any`

The runtime import works and every symbol is `any`. Three causes, in the order to check them:

1. `types` is not the first key in the conditions object, so it is unreachable.
2. No `types` condition is declared at all, and the consumer's `moduleResolution` does not fall back to the legacy `types` field at the package root.
3. The `.d.ts` file the condition points at does not exist, because the declaration emit was disabled or the build wrote it elsewhere.

All three pass every check the package itself runs, which is why they need a gate: `scripts/verify-package-entrypoints.mjs` resolves the `types` condition and asserts the file exists.

## `moduleResolution`

The consumer's `moduleResolution` setting decides whether the `exports` map is consulted at all.

- `bundler`: the `exports` map is honoured, and the extensionless import styles a bundler accepts are allowed. This is the setting a bundled frontend application uses.
- `node16` / `nodenext`: the `exports` map is honoured and the file-extension and format rules are enforced strictly — an ESM import needs the extension in the specifier, and the package's `type` field decides how each file is interpreted.
- The legacy `node` setting ignores `exports` entirely and resolves through `main` and the directory tree. A package that relies on `exports` for encapsulation gets none of it from such a consumer.

Rule: state the `moduleResolution` an internal package's declarations are built and verified against in the package's `README.md`. A package whose types work under `bundler` and fail under `nodenext` is a package with an undeclared consumer requirement, and the consumer discovers it during their own migration.

TypeScript language rules, patterns, and the fleet's TypeScript version line belong to `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`). This file covers only what crosses the package boundary.

## Build target

A package's build target is a promise about which runtimes can execute its output. Two rules:

- An internal package targets what the application targets, and no lower. Targeting lower ships transpilation and polyfill weight the application already decided it does not need; targeting higher produces syntax the application's own browser matrix cannot parse, and the failure appears only on the oldest supported browser.
- The application's browser and Node targets are not this skill's values. They are set in the application's build configuration, owned by `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`), `references/21-cli-vite-and-config.md`. Read the target there; write it once, in the package's build configuration; do not copy the value into prose in this skill, where it would age.

Where a package must differ from the application target — because it is also consumed by a Node process, for example — that is a `node` condition in `exports`, and the divergence rule in `references/12-exports-map-and-conditions.md` applies.
