---
name: alaa-laravel-upgrade-all-packages
description: "Upgrade of every direct Composer and npm dependency of a Laravel service to its latest stable release: version-gap inventory, official upgrade guides for each major move, one upgrade plan, a direct jump with a stepwise fallback, one final run of the repository gates, batch repair of every failure without weakening a test, and documentation updated to the new versions. Use to upgrade a Laravel application and its packages, a framework major included, or to act on a named advisory. Do not use for a repository with no composer.json, a dependency-freeze marker awaiting its owner, or alaa/controlled-ops and tag or Satis publication (/alaa-controlled-ops). Deep runtime verification runs only when the owner asks for it."
---

# Alaa Laravel Upgrade All Packages

You bring a Laravel service to the latest stable release of every direct dependency. You plan each major move from its official upgrade guide. You prove the result with the repository's own gates, run once at the end.

## Before the first command

Each item is a stop, not a preference.

- **Freeze marker.** A `docs/agents/dependency-freeze.md` file or an `extra.alaa.dependency-freeze` key in `composer.json` marks a frozen dependency baseline and names its owner and reason. If either exists, change no dependency and report its contents. If a human says the repository is frozen and no marker exists, write the marker from the owner and reason they give, and change nothing else.
- **ControlledOps.** `"name": "alaa/controlled-ops"` in the manifest, or a run that would cut a tag or publish to Satis, belongs to `/alaa-controlled-ops`.
- **Scope.** `git ls-files '*composer.json' | grep -v '^vendor/'` lists the manifests. Run once per manifest root and derive every path from that root. Then run `grep -rn 'composer \(update\|install\)' Makefile* .gitlab-ci.yml .github .circleci docker 2>/dev/null`. A hit means the repository wraps Composer: run the wrapper, because it can set flags and environment that the raw command omits.
- **Clean tree.** `git status --porcelain` is empty in the manifest root. Unrelated changes: stop and ask. A modified `composer.lock` or `vendor/` from an earlier run: read `references/20-apply-and-recover.md` *Interrupted resolution* first.

## Procedure

1. **Inventory.** List every direct dependency with its current version, its latest stable version and its gap class, through `references/10-version-gaps-and-guides.md`.
2. **Guides.** For each major move, read the official upgrade guide, and every intermediate guide when the gap spans several majors.
3. **Plan.** Write one plan table. Check each required change against this repository and mark the ones that do not apply.
4. **Stop conditions.** Check the list below before the first mutating command.
5. **Apply.** On one branch, raise the constraints and move everything to the latest stable release in one resolution, through `references/20-apply-and-recover.md`. Then make the code and configuration changes that the plan lists, and regenerate what the upgrade invalidated.
6. **Gates, once.** Run every repository gate one time and collect every failure into one list, through `references/30-final-gates-and-repair.md`.
7. **Repair, in one batch.** Fix the causes together, rerun the failed checks, then run every gate once more.
8. **Documentation.** Update each document that states a changed version or a changed behaviour, each regenerated artifact, and `.env.example` when a guide adds a key. Touch no other document.
9. **Commit and record.** Commit in this order: manifest and lockfiles; code and configuration changes; regenerated artifacts; documentation and the run record. Replace the content of `<repo>/docs/agents/upgrade-all-packages-execution-state.md` with this run: the plan table, the versions that landed, each blocked package with its reason, each remaining advisory, each gate with its result, and each check that did not run. Carry forward, unchanged, each unexpired advisory acceptance record and each deliberate version pin with its reason. Git history holds the earlier runs.

## Stop and ask

For each case below, leave that package at its current version, continue with every package that does not depend on it, and ask the owner in the final report.

- The latest release needs a PHP version or an extension that the production image does not have.
- A guide requires a change that stored data or running workers cannot read back: a data migration, or a new queue payload, cache, session or serialisation format.
- A `critical` or `high` advisory, or one with no severity, remains after the upgrade.
- Composer reports the package as abandoned.
- A required change needs a product or contract decision.

## Limits

These hold in every run. Each one removed hours of work that proved nothing about the upgrade.

- Take no test baseline before the upgrade, and repair a failing gate whatever its age.
- Create no scratch directory and copy no source tree. The branch point is the restore point.
- Write no test for the behaviour of a third-party package.
- Run no memory measurement, dependency-outage test or telemetry comparison. `references/50-runtime-verification.md` holds those checks for a run where the owner asks for them by name.
- Do no API contract, Postman or product documentation work, even when another loaded skill would add it. Record a finding outside the upgrade as a follow-up in the bound task store, or list it in the report.
- Run the upgrade in the lead session. Invoke the runtime orchestrator only when the owner asks for lanes.
- Run no review loop. Allow at most one review, which returns one list, repaired in one batch with no confirmation pass. A dependency audit that an orchestrator schedules is that one review.
- Load `/alaa-testing-strategy` before the gate run and the stack's clean-code skill before the first code edit. When `/alaa-workflow` applies, its plan is the plan table and its phases are the nine steps above; add none. Load another skill only when a stop condition or a failing gate names its surface.

## Named advisory

When the request names one advisory, move only the vulnerable package: raise its constraint when needed, then run `composer update <vendor/package> --with-dependencies`. Read its guide when the fix is a major move. Run steps 6 to 9 for that change alone. Do not widen the run into a full upgrade.

## Done

The run is complete when every direct dependency is at its latest stable release or listed as blocked with its reason, the final run of every gate is green, the documentation and the run record are updated, and the commits exist. Then stop. Report a gate that did not run as not run, never as passed.

## When NOT to use

- The repository has no `composer.json`: a Go module, an npm-only service, or another ecosystem.
- The repository carries a dependency-freeze marker whose named owner has not answered.
- The manifest is `alaa/controlled-ops`, or the run would cut a tag or publish to Satis: `/alaa-controlled-ops`.

## Routing

| You are about to | Read |
|---|---|
| List version gaps, decide what "latest stable" means, find or read an upgrade guide, or write the plan table | `references/10-version-gaps-and-guides.md` |
| Create the branch, raise constraints, resolve, record a blocked package, undo a change, recover an interrupted resolution, or regenerate artifacts | `references/20-apply-and-recover.md` |
| Run the final gates, build the failure list, repair, change a test, prove the application boots, or act on an audit finding | `references/30-final-gates-and-repair.md` |
| Run deep runtime verification that the owner asked for by name | `references/50-runtime-verification.md` |
