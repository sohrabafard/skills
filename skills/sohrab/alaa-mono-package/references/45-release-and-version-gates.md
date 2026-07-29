# Release and Version Gates

Open this file to bump a package version, change a package's public surface, or hand a consumer a changed entrypoint.

## Vocabulary: mirrored, not invented

The fleet already has a package-release skill: `/alaa-controlled-ops` (`$alaa-controlled-ops`), the PHP and Composer analogue, whose `references/40-validation-and-release-gates.md` established the shape. **This file mirrors that shape and does not route to it**, because its gate commands are Composer-specific and its Satis publication step has no JavaScript equivalent — routing would send an agent to a file with no runnable command in it.

Three things are mirrored deliberately, so the two sides of the fleet use one vocabulary:

- **Package gates** and **adopter gates** as the two categories. Package gates run in the package; adopter gates run in the consumer.
- **A gate that did not run is reported as not run, never as passed.** A gate with an unmet precondition has a false branch that names the precondition, and it never reports clean.
- Proof strength is named from the six-level vocabulary owned by `/alaa-testing-strategy` (`$alaa-testing-strategy`), not from a parallel set invented here.

## Package gates

Run all of these in the package before its version changes:

| Gate | Command | False branch |
|---|---|---|
| typecheck | the package's own `typecheck` script | script absent: report `typecheck not run: no typecheck script in <pkg>`, and add one |
| unit tests | the package's own `test` script | dependencies not installed: install, then run; if install fails, report `tests not run` with the failure output |
| build | the package's `build` script | an upstream `dist/` is missing: `references/18-build-order-and-graph.md` |
| export surface | `scripts/verify-package-entrypoints.mjs <package-dir>` | exit code 2: build the graph first, `references/18-build-order-and-graph.md` |
| lockfile integrity | the frozen install, `references/15-package-manager-modes.md` | a modified lockfile fails the gate |

## Adopter gates

Run these in the consuming application after the package changes, before the change is called done:

- Build the application and confirm the package's built entrypoint is the one that was consumed, not its source.
- Confirm the package's assets and CSS are present in the final client asset output, per `references/30-assets-css-and-ssr-client-assets.md`.
- Confirm the single-realpath assertion still holds for every shared runtime, per `references/20-peer-deps-dedupe-and-build-output.md`.

Generic application-level delivery validation is not repeated here; it belongs to `/alaa-frontend-devops` (`$alaa-frontend-devops`), `references/40-verification-and-rollback.md`.

## When the version changes

An internal, unpublished package still carries a version, and it still means something: it is the identifier a consumer's error report will quote. Bump it whenever the built output changes in a way a consumer can observe.

| Change | Version |
|---|---|
| an `exports` subpath or condition removed, retargeted, or renamed | major |
| an exported symbol removed or its type narrowed | major |
| a peer range narrowed | major |
| a new `exports` subpath or a new exported symbol | minor |
| a peer range widened | minor |
| behaviour fixed with no surface change | patch |
| `sideEffects` changed | minor at least, because it changes what the consumer's bundler emits |

## The consumer migration note

**When an entrypoint changes, a migration note is written in the same commit**, in the package's `CHANGELOG.md`, containing exactly four things:

1. The old import line, written out.
2. The new import line, written out.
3. Whether the old line still works, and if it does, until which version.
4. The command that finds every occurrence in the repository, written out so a consumer can run it rather than compose it.

A changelog entry that says "moved the entrypoint" and does not contain those four is not a migration note. The reader of a migration note is someone who did not make the change and does not know why it happened.

## The export-surface document

Every package's `README.md` documents its export surface: for each subpath in `exports`, one line giving what it is for and the consumer that uses it. This is the artifact the "small and explicit public surface" criterion in `references/10-package-boundary-and-entrypoints.md` is checked against — a subpath with no line is either undocumented or unnecessary, and both are findings.

Keep it in `README.md` rather than a generated document, because it is read by someone who has just opened the package directory and is deciding what to import.
