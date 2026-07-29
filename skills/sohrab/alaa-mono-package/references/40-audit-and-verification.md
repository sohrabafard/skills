# Audit and Verification

Open this file to close out package-boundary work and state what was validated.

## The audit order

1. Search for imports of `packages/*/src` from anywhere outside the owning package. Any hit is a boundary violation, `references/10-package-boundary-and-entrypoints.md`.
2. Run `scripts/verify-package-entrypoints.mjs` over the workspace. It executes the export-surface, peer-realpath, `sideEffects`, and specifier assertions in one pass, so do not perform them by eye.
3. If the lane was package-only, verify the changed-file list stayed inside the allowed boundary before any broader validation. Include unstaged, staged, and untracked files; an untracked file is the one that gets missed.
4. Build the application and inspect the final client asset output, when the consumption path is in scope.

Steps 1 and 3 are cheap and catch the failures that are hardest to see later. Step 2 is the one that catches the failures nothing else reports.

## What the gate asserts

`scripts/verify-package-entrypoints.mjs` reports each of these separately, so a finding names its own rule:

| Id | Assertion | Rule |
|---|---|---|
| E1 | every `exports` target exists on disk after build | `references/12-exports-map-and-conditions.md` |
| E2 | `types` is the first key in every conditions object | `references/12-exports-map-and-conditions.md` |
| E3 | no `main` or `module` alongside `exports` pointing somewhere else | `references/12-exports-map-and-conditions.md` |
| E4 | the package's entry actually loads, not merely resolves, and the process exits after importing it | `references/12-exports-map-and-conditions.md` |
| E5 | shared runtimes are peers, not dependencies, and resolve to one real path | `references/20-peer-deps-dedupe-and-build-output.md` |
| E6 | a package emitting CSS does not declare `sideEffects: false` | `references/30-assets-css-and-ssr-client-assets.md` |
| E7 | every internal specifier matches the detected manager | `references/15-package-manager-modes.md` |

E4 has two distinct failure shapes and they need different fixes. An entry that *throws* is a broken build or a missing peer. An entry that imports but leaves the process running is a module-scope side effect — a timer, a listener, a worker, an eagerly-created client — that runs inside every consumer that imports the package, on the server as well as in the browser. A package in that state cannot honestly declare `"sideEffects": false`, and the declaration and the behaviour must be reconciled rather than one of them silenced.

E4 spawns one subprocess per package and is the slow assertion. `--no-load` gives a fast manifest-only pass for an inner loop; the full pass with E4 is what runs before the work is called done.

A pipeline that treats every non-zero exit as a failure reads exit code 2 correctly; a human reading "no failures printed" does not. Print the exit code in the closeout rather than the absence of findings.

## Naming proof strength

State which of the six proof levels each check reached, using the vocabulary owned by `/alaa-testing-strategy` (`$alaa-testing-strategy`). A static inspection of a manifest and a subprocess import of a built entrypoint are different levels of evidence, and reporting the first as though it were the second is the failure this rule prevents. The not-run reporting rule is in `references/45-release-and-version-gates.md`; it applies here unchanged.

## Closeout

Report:

- the boundary rule that was at issue and what changed, by file
- the export surface before and after, if it changed, and the migration note that accompanies it per `references/45-release-and-version-gates.md`
- which gate ids ran and their results, including any that could not run and why
- whether any changed file was outside the allowed boundary, and if so which and why it was left unmade
- what remains unverified, stated as a question someone can answer
