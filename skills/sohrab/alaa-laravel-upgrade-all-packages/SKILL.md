---
name: alaa-laravel-upgrade-all-packages
description: "Run a safe, complete Composer (and npm, when present) dependency-upgrade sweep for a Laravel service -- check outdated/audit state, apply the compatible upgrade set, record any blocked major-version constraint via composer why-not, refresh generated Boost artifacts, keep composer.json and package.json constraints honest against the lockfile, sweep stale version strings from docs and state, and pass the full validation gate before declaring done. Use for a scheduled or recurring upgrade-all-packages automation on a Laravel + Composer repo, or any ad-hoc bring-dependencies-current request. Not for Go modules, npm-only, or other non-Composer ecosystems."
---

# Alaa Laravel Upgrade All Packages

## Purpose

This is a recurring maintenance run that has already happened, independently and in near-identical shape, across most of the Laravel/Composer services in this portfolio. The real risk in this sweep is never the version bump itself -- it is continuity (a prior run left the worktree mid-change and a fresh run must recognize and finish that instead of starting over) and stale prose (old version numbers or "blocked"/"now resolves" language left behind in docs and state after the refresh). Treat both as first-class parts of the job, not afterthoughts.

## When to use

- A scheduled or recurring "upgrade all packages" automation fires for a Laravel + Composer repo.
- The user asks, ad hoc, to bring a Laravel repo's dependencies current.

## When NOT to use

- The repo is not Laravel/Composer-based (Go modules, a plain npm-only service). The constraint model and validation commands are different enough that this procedure does not transfer cleanly -- treat that as a separate, not-yet-written procedure.
- The repo is intentionally frozen at a dependency baseline for release-stability reasons. Pause and record why instead of silently skipping or silently upgrading anyway.
- The repo is a monorepo with more than one `composer.json`. Run this procedure once per manifest root rather than assuming a single repo-wide upgrade covers all of them, and say explicitly which root each run covers.
- The repo wraps Composer behind another entrypoint (a `Makefile` target, a Docker-exec script, a custom CI job). Find and use that wrapper first -- it may set flags, environment, or ordering the raw `composer` commands below would otherwise miss -- and fall back to the raw commands only if no wrapper exists.

## Procedure

1. Check for continuity first, using whichever mechanism this run actually has -- these are equally valid, not a default-plus-exception pair: a Codex automation memory file (`$CODEX_HOME/automations/<id>/memory.md`) if this run was triggered as a Codex automation, or a repo-local `docs/agents/upgrade-all-packages-execution-state.md` state file (per `$alaa-workflow`/`/alaa-workflow` conventions) for a Claude Code run, a `/loop`-triggered run, or any Codex run that also wants a durable in-repo record. If neither file exists, this is a first run: proceed with the sweep and create the repo-local state file before finishing, so the next run -- regardless of which agent or runtime triggers it -- has something to read. If a continuity file already shows modifications matching a prior run's scope sitting in the working tree, treat that as an interrupted run to verify and finish, not to discard or redo.
2. Load this repo's mandatory skills for dependency work before touching anything -- typically architecture, PHP clean-code, services-contract, low-noise, observability, security-review, trust-gateway-auth, runtime-kit governance, and the Windows/sandbox runtime-ops skill.
3. Query current state before changing anything: `composer outdated --direct --format=json` and `composer audit --locked`, plus `npm outdated --json` and `npm audit --json` if the repo has a `package.json`.
4. Apply the safe, compatible upgrade set with `composer update --with-all-dependencies`. When a major-version bump is blocked, run `composer why-not <package> <version>` to get the exact blocking constraint and record it -- do not force the upgrade or guess at the reason.
5. Refresh any generated artifacts the upgrade affects (for example, Laravel Boost guidelines/skills/MCP regeneration), then align `composer.json`'s direct version constraints with what the lockfile actually resolved to. A green lockfile update does not by itself keep the manifest honest.
6. If the repo has a `package.json`, give its dependencies the same safe-upgrade treatment as a secondary step, using the same why-not-style investigation for anything blocked. First establish whether the frontend build is decorative dev tooling or actually ships (an SSR/Inertia view layer, a production asset pipeline the app serves) -- if it ships, treat it as equally load-bearing as the Composer side for validation purposes, not as a lesser afterthought.
7. Sweep docs and state files for stale version strings or outdated "blocked"/"now resolves" language left over from the previous run.
8. Run the full validation gate and show the actual output, not a bare summary: formatting (for example `vendor/bin/pint --dirty --format agent`), the full test suite, `composer validate --strict`, `composer audit`, and, if the repo has a `package.json`, `npm audit` plus the repo's actual frontend build command when that build ships to production (an `npm audit` pass alone does not prove the build still works).
9. Update this automation's memory/state file with the run's outcome: versions landed, any blocker recorded, anything left for next time.

## Validation

- Full test suite passes, or any pre-existing failure is explicitly identified as pre-existing and unrelated to this sweep.
- `composer validate --strict` and `composer audit` are clean, or every remaining finding is explicitly recorded as an accepted, currently-unfixable upstream issue.
- If the frontend build ships to production, it actually builds successfully after the npm upgrade, not just passes `npm audit`.
- `git status --short` / `git diff --stat` / `git diff --check` confirm only the intended dependency, doc, and state files changed.

## Safety rules

- Never install a new package or change an unrelated constraint while running this sweep -- scope strictly to upgrading dependencies already in the manifest.
- Never force a major-version bump past a confirmed blocking constraint; record the blocker instead.
- If a Windows Composer/npm cache permission error appears mid-run, use an isolated repo-local cache directory for the duration of the run, then remove it -- see `references/10-memory-and-skill-loading.md` and `$alaa-codex-runtime-ops`/`/alaa-codex-runtime-ops`. Do not escalate broadly or abandon the sweep over this.
- Do not let this automation silently touch a sibling repo (for example, a shared skills repo it also happens to update) without clearly separating that diff from the target repo's own changes.

## Companion routing

- `$alaa-controlled-ops`/`/alaa-controlled-ops` -- if the repo being upgraded is the ControlledOps package itself, or a service adopting it, that skill's release/Satis rules take precedence over this skill's generic steps.
- `$alaa-codex-runtime-ops`/`/alaa-codex-runtime-ops` -- for Windows sandbox and package-manager cache friction encountered mid-sweep.
- `$alaa-workflow`/`/alaa-workflow` -- for the repo-local state-file convention when no Codex automation memory file applies, or when this sweep is one phase of a larger plan.
- `$alaa-php-clean-code`/`/alaa-php-clean-code`, `$alaa-laravel-architecture`/`/alaa-laravel-architecture` -- general Laravel conventions this sweep must not violate.

## Reference navigation

- `references/10-memory-and-skill-loading.md` -- the automation memory-file schema, the standard skill-loading list, and the Windows cache-permission workaround in full.
