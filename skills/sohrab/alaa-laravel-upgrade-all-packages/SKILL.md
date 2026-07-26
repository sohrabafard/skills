---
name: alaa-laravel-upgrade-all-packages
description: "Composer and npm dependency-upgrade sweep for a Laravel service: restore point and test baseline first, then outdated and audit state, the lockfile move, severity-based advisory triage, blocked-bump capture via composer why-not, manifest-versus-lockfile honesty, worker-boot and telemetry verification, and a revertible change. Use for a scheduled upgrade-all-packages run on a Laravel + Composer repo, an ad-hoc bring-dependencies-current request, or an advisory forcing a named dependency to move. Do not use it for a non-Composer ecosystem such as Go modules or an npm-only service; for a repo carrying a dependency-freeze marker until its named owner answers; or when the manifest is alaa/controlled-ops or the run cuts a tag or Satis publish -- that is /alaa-controlled-ops ($alaa-controlled-ops). A major framework migration is /alaa-laravel-architecture ($alaa-laravel-architecture)."
---

# Alaa Laravel Upgrade All Packages

You move a live service's dependency set and prove the service still behaves.

## Before the first command

Each item is a stop, not a preference.

- **Continuity.** `/alaa-workflow` (`$alaa-workflow`) `references/context-continuity.md` owns plan, phasing, state and resume; follow it unchanged. Two facts it cannot know: this sweep's state file is `docs/agents/upgrade-all-packages-execution-state.md`, and a dirty `composer.lock` plus a dirty `vendor/` is an interrupted **resolution**, not an interrupted plan -- diagnose that via `references/40-failure-classes.md` before reading any plan.
- **Freeze marker.** A frozen dependency baseline is detected by a `docs/agents/dependency-freeze.md` file or an `extra.alaa.dependency-freeze` key in `composer.json` naming the freeze owner and reason. If either exists, change no dependency and report its contents. If a human says the repo is frozen and no marker exists, write the marker from the owner and reason they give and change nothing else, so the next run detects it without asking.
- **Scope of the run.** `git ls-files '*composer.json' | grep -v '^vendor/'` enumerates manifests: run once per root, name that root in the state file, and derive every path from its absolute path, never from the working directory, which in a monorepo is not the manifest root. Then `grep -rn 'composer \(update\|install\)' Makefile* .gitlab-ci.yml .github .circleci docker 2>/dev/null`: any hit means Composer is wrapped, and the wrapper is what runs, since it may set flags, environment or ordering the raw commands omit.
- **ControlledOps.** `"name": "alaa/controlled-ops"` in this manifest, or a run that would cut a tag or publish to Satis, belongs to `/alaa-controlled-ops` (`$alaa-controlled-ops`), whose release gates outrank every step here.
- **Restore point and baseline.** Take both before any mutating command. A sweep with no restore point is not run; with no baseline, no later failure may be called pre-existing.

## Procedure

1. Read state: `composer outdated --direct --format=json` and `composer audit --locked --format=json`, plus `npm outdated --json` and `npm audit --json` when a `package.json` exists. A non-empty audit result reorders the work.
2. Resolve without writing: `composer update --with-all-dependencies --dry-run`. That flag applies whatever the declared constraints permit, including a major bump under a loose constraint; it is not a safe-subset flag. Classify every moved package, and split each major bump into its own change with its own gates.
3. Apply the remaining set: `composer update --with-all-dependencies --no-interaction --no-progress`. Add, remove or re-constrain nothing this run was not asked to move; that prohibition covers manifest entries only, `require`/`require-dev` and `dependencies`/`devDependencies`. Transitive packages appearing, disappearing or moving version inside `composer.lock` is the designed result of that flag: expected, and exactly what the evidence set must cover, so the lock diff is read and reported in full, never summarised.
4. When a bump is blocked, run `composer why-not <package> <version>`, record the exact blocking constraint, and leave that package where it is. Never force a bump past a confirmed blocker, never hand-edit `composer.lock`, and do not guess at the reason.
5. Regenerate what the upgrade invalidated (Laravel Boost guidelines, skills and MCP registration; compiled config, route and view caches), then align each direct constraint in `composer.json` with the version the lockfile actually resolved to. A green lockfile update does not by itself keep the manifest honest.
6. With a `package.json`, give it the same treatment and the same `why-not`-style capture for anything blocked. Decide first whether the frontend build is production surface or dev-only tooling; that answer sets which gates apply to it.
7. Verify runtime behaviour now that the lock moved. A test suite runs one request per process and proves nothing about a worker's second request.
8. Sweep docs and state files for stale version strings and leftover "blocked" or "now resolves" language from the previous run.
9. Record in the state file: versions landed, every blocker with its `why-not` output, every advisory acceptance record, the proof level reached, and the restore point.

## Gates

Show actual command output. A summary is not evidence, and a gate not run is reported as not run, never as passed.

- **Formatter.** Run the formatter the repo declares in `require-dev`, path resolved per `references/40-failure-classes.md` (`laravel/pint` -> `<bin-dir>/pint --dirty --format agent`). None declared reports `formatting gate not available: none declared`.
- **Test suite.** Green, or a failure matching the baseline under the identity rule in `references/20-breaking-change-detection.md`. A "pre-existing" claim that does not quote the baseline file path is not a claim.
- **Supply chain.** `composer validate --strict` and `composer audit` clean, or every finding carries the full acceptance record from `references/30-advisory-triage.md`. No agent accepts a finding on its own authority; critical and high have no acceptance path.
- **Proof strength.** Name the level reached from `/alaa-controlled-ops` (`$alaa-controlled-ops`) `references/40-validation-and-release-gates.md`, "Proof vocabulary". Static inspection never clears a lockfile change under the fleet SLA; `references/20-breaking-change-detection.md` sets the level per class.
- **Diff.** `git status --short`, `git diff --stat` and `git diff --check` show only intended dependency, generated-artifact, doc and state files, and no scratch or cache directory survives.

## Routing

| You are about to | Read |
|---|---|
| Take a restore point, undo a lockfile change, or revert a bump that already reached an environment | `references/10-rollback-and-blast-radius.md` |
| Capture the baseline, classify a change as major, decide whether the frontend ships, or verify what tests cannot see | `references/20-breaking-change-detection.md` |
| Act on a `composer audit` or `npm audit` finding, or decide whether and by whom one may be accepted | `references/30-advisory-triage.md` |
| Hit a resolution conflict, test regression, unwritable artifact, cache permission error, or half-applied update | `references/40-failure-classes.md` |
| Ship a framework, driver, extension or telemetry bump to a service with a long-lived worker | `references/50-runtime-verification.md` |
| Decide which skill owns a question this sweep raised, and which wins on conflict | `references/90-ownership-boundary.md` |

`/alaa-workflow` (`$alaa-workflow`) loads on every run. What this skill owns, what it does not, the ten-criterion bar, and the upstream skills this repository does not own are all in `references/90-ownership-boundary.md`.
