# Exports Map and Conditions

Open this file to add, remove, rename, or repoint an entry in a package's `exports` map, to add a subpath or a condition, or when a consumer's types resolve to `any` while the runtime import works.

Everything below is verified against https://nodejs.org/api/packages.html, `read: 2026-07-28`.

## The rule

**Every condition a package declares must be provably importable, and the proof is `scripts/verify-package-entrypoints.mjs`.** A declared condition that resolves to a file that does not exist, or to a file that throws when evaluated, is a broken public surface that produces no build error in the package that declares it. It fails in the consumer, at a distance, and the stack trace points at the consumer.

## Condition matching is ordered and first-match

Within a conditions object, key order is significant. Node walks the keys in declaration order and takes the first whose condition is active. Order from most specific to least specific.

- **`types` comes first.** A `types` key placed after `import` is unreachable, TypeScript falls back to an implicit `any` for the whole package, and nothing in the package's own build reports it. This is the single most common silent defect in an `exports` map.
- **`default` comes last**, and is the only unconditional fallback. A key after `default` is dead.
- Between them, order specific to general: `node-addons`, `node`, `browser`, `development`/`production`, `module-sync`, `import`, `require`.

```json
{
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.mjs",
      "default": "./dist/index.mjs"
    },
    "./style.css": "./dist/style.css"
  }
}
```

*(Shape read from `packages/sdk-core/package.json` and `packages/design-system-vue/package.json` in the live `client` repository, `read: 2026-07-28`.)*

## `exports` encapsulates the package

When `exports` is present, a consumer can import only the subpaths it lists. Every other path inside the package is unreachable, including paths that used to work. This is the property that makes the package boundary real, and it is why the boundary rule in `references/10-package-boundary-and-entrypoints.md` is enforceable rather than aspirational.

Consequences to hold:

- Every importable path is listed in `exports`. A path a consumer needs and `exports` omits must fail at resolution time; adding it to the map is the fix, not working around it.
- `exports` takes precedence over `main` in every supported Node version, and `module` is not a Node field at all. Keeping `main` beside `exports` gives a consumer a path that resolves under one toolchain and not under another. Where a bundler still requires `main`, point it at the same file the `default` condition points at, and record on that line which consumer requires it.
- Subpath patterns use `*` as a literal string replacement: `"./features/*.js": "./src/features/*.js"`. A `null` target excludes a path from an otherwise matching pattern.
- A package may import itself by its own name if `exports` allows the path. Prefer that to a relative path across the package's own boundary, so internal and external consumers exercise the same map.

## The dual-package hazard

**Symptom:** a value that must be a singleton behaves as though there are two of it — a store that is empty when read from one module and populated when read from another, an `instanceof` check failing against an object of visibly the correct class, a framework warning about being loaded twice, a registry that a plugin registered into and a component cannot see.

**Cause:** the package is loaded twice in one process under two formats or two resolutions. Any module-level state exists once per copy.

**Rule:** every internal package emits ESM only. `exports` declares no `require` condition unless the package's `README.md` names the CommonJS consumer that requires it and states what module-level state the package holds. If it holds none, say so on that line; that is what makes the exception checkable.

## A peer satisfied at two versions

**Symptom:** the framework warns that two instances are active; a composable or a context created by one module is invisible to another; two copies of the same component library disagree about a global registry.

**Cause:** two packages declare the same peer with ranges that do not intersect, or one declares it as a dependency rather than a peer, so the installer places a second copy inside that package's own `node_modules`.

**Detection:** resolve the name from every workspace package and from the root app and compare the resolved real paths. More than one distinct path is the defect. `scripts/verify-package-entrypoints.mjs` performs exactly this check; the peer contract itself is `references/20-peer-deps-dedupe-and-build-output.md`.

## SSR and client resolving differently

**Symptom:** a component renders on the server and throws in the browser, or hydration reports a mismatch, and the two environments are loading different files.

**Cause:** a conditions object whose `node` and `browser` branches point at different builds, combined with a bundler that resolves the browser branch while the SSR runtime resolves the `node` branch. Two builds mean two behaviours, and the difference is invisible in a single-environment test.

**Rule:** an internal package declares a `browser` or `node` condition only when the two targets need genuinely different code, and when it does, the package's own test suite runs under both conditions. A package with one implementation declares neither, so there is nothing to diverge.
