# Source Map

Use this file when package-boundary guidance depends on current bundler, package-manager, Vue, Quasar, or Vite behavior.

## Source Priority

Prefer sources in this order:

1. Repo-local package contracts: root `package.json`, workspace config, lockfile, package `exports`, package build scripts, emitted `dist/`, and consuming imports.
2. Official package-manager docs for the repo's actual manager: Yarn, npm, pnpm, or Bun.
3. Official bundler/framework docs:
   - Vite docs and migration guide: https://vite.dev/
   - Vue release policy: https://vuejs.org/about/releases
   - Quasar CLI with Vite docs: https://quasar.dev/quasar-cli-vite/
   - TypeScript docs when declarations or project references are in scope: https://www.typescriptlang.org/docs/
4. Official release notes and npm metadata for package version drift.
5. Community issues and StackOverflow answers only for troubleshooting leads.

## Freshness Triggers

Re-check official sources before changing advice for:

- peer dependency ranges for Vue, Quasar, Vite, TypeScript, or shared UI packages
- package `exports`, ESM/CJS format, declaration output, or CSS/asset side effects
- Vite dependency optimization, library mode, SSR externalization, or manual chunking
- lockfile or package-manager migration
- security or supply-chain claims about hoisting, dedupe, transitive dependencies, or package provenance

## Community Troubleshooting Boundary

Community material can help identify a failing package-manager edge case, but it must not override the repo's lockfile, official package-manager docs, or the actual emitted package artifact.

## Small Anti-Pattern

Anti-pattern: resolving a duplicate Vue warning by bundling a second Vue copy inside an internal package.

Better path: make Vue a peer dependency, ensure the root app provides the runtime, verify the package `exports` point to built files, and inspect the final bundle for duplicate framework instances.
