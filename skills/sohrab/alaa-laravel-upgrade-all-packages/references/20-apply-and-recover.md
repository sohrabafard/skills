# Apply and recover

`composer.lock` declares the dependency set. `vendor/` is the installed tree. `composer update` rewrites both, and not atomically.

## Restore point

Create the branch from the clean tree: `git switch -c chore/deps-$(date +%Y%m%d)`. Record the branch-point commit in the run record. That commit is the restore point. The upgrade never commits to the default branch, so that one revert undoes it.

## Resolve

Use the repository wrapper when `SKILL.md` *Scope* found one. If the wrapper cannot express a step below, report that as the blocker; do not substitute the raw command.

1. For each package whose `latest-status` is `update-possible`, raise the constraint without resolving: `composer require <vendor/package>:<constraint> --no-update`, with `--dev` for a `require-dev` entry. Write the constraint that admits the latest stable release.
2. Resolve once: `composer update --with-all-dependencies --no-interaction`.
3. Run `composer bump`, so that each lower bound in `composer.json` equals the version the lockfile resolved.
4. With a `package.json`, move every outdated direct dependency in one command: `npm install <package>@latest ...`, with `--save-dev` for a development dependency. Then run `npm update`, so that packages inside their current ranges, transitive ones included, also move.

**Direct jump first.** Move every package, majors included, in the one resolution above. Use the **stepwise fallback** in two cases only: the resolution fails and `why-not` shows conflicts among several majors, or the final failure list cannot be assigned to causes. Then restore, and move one major at a time with the framework first, running the gates after each step. Record that the fallback ran and why.

## Blocked package

Run `composer why-not <vendor/package> <version>` and record its output verbatim. Restore that package's entry in `composer.json` to its previous constraint, resolve again, and continue. When the blocked package is the framework itself, also restore every package whose new release requires the new framework major, and report the framework as blocked.

- Never force a move past a confirmed blocker, and never hand-edit `composer.lock`.
- `--ignore-platform-req` and `--ignore-platform-reqs` are forbidden: they produce a lock that cannot install on the target runtime.
- Set `config.platform` only to the production image's actual PHP version and extensions. When you do not know them, that is the first stop condition in `SKILL.md`.
- For a test regression that only one package causes and no repair removes, pin that package to its previous version in `composer.json`, and record the failing test, the package and both versions.

## Undo

```bash
git restore --source=<branch-point-commit> -- composer.json composer.lock
composer install --no-interaction
composer validate --strict
```

Restore `package.json` and `package-lock.json` the same way, then run `npm ci`.

- Never undo with `composer update`: it resolves again and can land a third set.
- Never restore the lock without reinstalling: the gates then run against a tree that no lockfile describes.
- After an undo, run `php artisan optimize:clear`, because caches compiled under the new version still look valid.

## Interrupted resolution

A modified `composer.lock` or `vendor/` at the start of a run means an earlier resolution stopped part-way.

```bash
git status --short composer.json composer.lock
composer validate --strict                    # manifest and lock agree
composer install --dry-run --no-interaction   # lock and vendor/ agree
```

- Lock unmodified, `vendor/` out of step: run `composer install --no-interaction`. The lock is still authoritative.
- Lock modified: if the run record states the intended version set, run `composer install --no-interaction` from that lock and continue into the gates. If it does not, undo and start the run again.

## Regenerate

Regenerate what the upgrade invalidated: Laravel Boost guidelines, skills and MCP registration through the installed Boost command, and the compiled config, route and view caches. Commit each regenerated artifact with the run.

When a regeneration command cannot write its target, change one named thing and retry once: close the process that holds the file, or use a shell that can write the path. If it fails again, report the artifact as not regenerated with the path and the error text. Keep the dependency change.

## Tool failures

- **Cache permission error.** When Composer or npm fails on a path inside its global cache, rerun with a cache under the manifest root, and remove it afterwards:

```bash
printf '%s\n' '.composer-home/' '.composer-cache/' '.npm-cache/' >> "$(git rev-parse --git-path info/exclude)"
export COMPOSER_HOME="$MANIFEST_ROOT/.composer-home" COMPOSER_CACHE_DIR="$MANIFEST_ROOT/.composer-cache" npm_config_cache="$MANIFEST_ROOT/.npm-cache"
# rerun the failed command, then:
rm -rf "$COMPOSER_HOME" "$COMPOSER_CACHE_DIR" "$npm_config_cache"
```

- **Declared tool not found.** `composer config bin-dir` gives the tool directory, which is not always `vendor/bin`. Never substitute a globally installed tool for one the repository declares. Report the gate as not available and name it.
- **`vendor/` is never edited.** When an upgraded package needs different behaviour, change the service's own code, or record the package as blocked.
