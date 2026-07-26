# Rollback And Blast Radius

Recovery for a dependency change. Failure doctrine is `/alaa-reliability-sla` (`$alaa-reliability-sla`) and every platform number is `alaa-services-contract references/22-failure-load-and-deprecation-contract.md`; neither covers undoing a lockfile move.

`composer.lock` declares the set; `vendor/` is the installed tree, and `vendor/composer/installed.json` records what was written into it. `composer update` rewrites both, not atomically, so an interrupt between them leaves a worktree no gate can describe.

## Restore point, before the first mutating command

1. `git status --porcelain` is empty. Anything else is unrelated work (stop and ask) or an interrupted prior resolution (`40-failure-classes.md`).
2. Record the commit and copy the lockfiles out of the tree, so a botched restore cannot destroy the record of where the sweep started:

```bash
MANIFEST_ROOT=/absolute/path/to/manifest/root     # the root this run covers
SCRATCH="$MANIFEST_ROOT/.upgrade-scratch"
printf '%s\n' '.upgrade-scratch/' >> "$(git rev-parse --git-path info/exclude)"
mkdir -p "$SCRATCH"
git rev-parse HEAD > "$SCRATCH/pre-sweep-commit"
cp "$MANIFEST_ROOT/composer.lock" "$SCRATCH/composer.lock.pre"
[ -f "$MANIFEST_ROOT/package-lock.json" ] && cp "$MANIFEST_ROOT/package-lock.json" "$SCRATCH/package-lock.json.pre"
```

The exclude entry is written before the directory exists, so a run that dies mid-sweep leaves nothing untracked. `git rev-parse --git-path info/exclude` resolves from a subdirectory and from a linked worktree, which a literal `.git/info/exclude` does not, and the pattern carries no leading slash so it matches at any depth.

3. `git switch -c chore/deps-$(date +%Y%m%d)`. The sweep never commits to the default branch: the revert unit must be separable from everything else landing that day.
4. Three commits, in order: manifest and lockfile; regenerated artifacts; docs and state. A mixed commit cannot be reverted without dragging documentation backwards.

## Restoring

```bash
git restore --source="$(cat "$SCRATCH/pre-sweep-commit")" -- composer.json composer.lock
composer install --no-interaction
composer validate --strict
```

- **Never restore with `composer update`.** It re-resolves and can land a third set matching neither side. Restore the lock, then install.
- **Never restore the lock without reinstalling.** A restored lock over a new `vendor/` is the same inconsistency, and the suite then reports on a tree no lockfile describes.
- **Never restore with `--no-dev`** where the tests must run: the dev tree disappears silently and the test gate becomes unrunnable while looking merely absent.

Deleting `vendor/` is safe only after the lock is restored and `composer validate --strict` passes; under the new lock it just reinstalls the new set.

## Revertible after the change reached an environment

A git revert restores the manifest and lock, not the running service.

- **The deployed artifact.** The service runs an image built from a lock. The deploy-level revert is redeploying the previously known-good image digest; the git revert only makes the *next* build reproduce it. Record the pre-sweep digest beside the pre-sweep commit, or the revert has no target. Image and registry mechanics `/alaa-docker-production` (`$alaa-docker-production`); pipeline sequencing `/alaa-cicd-laravel-postgres` (`$alaa-cicd-laravel-postgres`).
- **Regenerated artifacts.** Boost guidelines, skills and MCP registration, compiled frontend assets, generated config: each is committed with the bump that produced it. Split across commits, reverting the bump leaves a new-version artifact beside an old-version lock and nothing reports it.
- **Compiled caches and booted workers.** Caches compiled under the new version still look valid, so `php artisan optimize:clear` (or the repo's wrapper) is part of the revert. A worker holds the booted application, so a revert is not live until workers restart: `/alaa-octane-performance` (`$alaa-octane-performance`) `references/worker-lifecycle-and-failure.md`.

## Blast radius, stated before the bump

Record what each moved package can reach; this sets the gate level in `20-breaking-change-detection.md`.

- **Who pulls it in:** `composer depends <vendor/package>`, with `--tree` when unclear. `require-dev`-only and absent from every container build stage means it does not reach the request path.
- **Which surfaces load it:** routes, queue consumers, scheduled commands and console entrypoints on its code path. A bump reaching only a console command keeps the gate proportionate.
- **Whether it crosses a trust boundary:** authentication, authorization, request parsing, deserialisation, template rendering, outbound HTTP. If it does, `30-advisory-triage.md` and `/alaa-security-review` (`$alaa-security-review`) apply on top.

## One repository per diff

A run that also updates a sibling repository commits and reports each separately, naming the absolute root each diff covers. A combined diff cannot be reverted per repository, and the restore point above belongs to one root.
