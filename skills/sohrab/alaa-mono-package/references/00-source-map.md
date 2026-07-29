# Source Map

This file is the source-provenance ledger for this skill, not a router. The router is `references/00-topic-map.md`.

Open this file before asserting a version, a resolution semantic, or a claim about current package-manager or bundler behaviour that this skill does not already state.

## Source priority

Consult in this order and stop at the first that answers the question.

1. Repo-local package contracts, because they are the only evidence of what this workspace actually does: the root `package.json` (`packageManager`, `engines`, `scripts`), the workspace manifest, the lockfile, each package's `exports` and build script, the emitted `dist/`, and the imports that consume it.
2. The in-fleet owner of the subject. Version ranges, bundler wiring, proof levels, and threat classification are not looked up on the internet first; they are looked up in the owning skill, listed with file paths in `references/90-companion-boundary.md`.
3. Official documentation for the exact tool in use:
   - Node.js packages and resolution: https://nodejs.org/api/packages.html
   - pnpm, including filtering and workspace protocol: https://pnpm.io/
   - TypeScript module resolution: https://www.typescriptlang.org/docs/handbook/modules/reference.html
   - Vite: https://vite.dev/
   - Quasar CLI with Vite: https://quasar.dev/quasar-cli-vite/
4. Official release notes and registry metadata when the documentation is ambiguous about a version boundary.
5. Community issues and answers, as candidate failure modes to reproduce locally. Never as the source of a rule.

Resolution semantics are the area of this ecosystem where blog-era advice is most often wrong and most often copied. Condition ordering, `types` placement, subpath patterns, self-reference, and the `main`-versus-`exports` precedence are verified against source 3 every time they are asserted, not remembered.

## Freshness triggers

Re-verify before changing advice when the task involves: a peer range for a shared runtime; `exports`, module format, declaration output, or CSS and asset side effects; dependency optimisation, library mode, SSR externalisation, or chunking; a lockfile or package-manager migration; or any supply-chain claim about hoisting, dedupe, transitive dependencies, or provenance.

## Recording a claim

Every version-sensitive or behaviour-sensitive claim carries a `read: <ISO date>` on the same line, and a source URL where one exists. A claim that could not be verified ships as `read: unverified as of <ISO date>` and stays in the file rather than being dropped or asserted.

"Not documented" means searched in sources 1 to 3 and not found. It is not proof that the behaviour is absent.

## Community-evidence boundary

Community material may identify a failing edge case to reproduce. It does not override the lockfile, the official manager documentation, or the actual emitted artifact. When a forum answer and the emitted `dist/` disagree, the `dist/` is what ships.

## Anti-pattern

Resolving a duplicate-runtime warning by bundling a second copy of the runtime inside a package. That converts an install-time warning into a permanent runtime defect and hides the real cause. The peer contract and the single-realpath assertion in `references/20-peer-deps-dedupe-and-build-output.md` are the fix; `scripts/verify-package-entrypoints.mjs` is how you find which package did it.
