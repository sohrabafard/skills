# Failure Classes

Each class is symptom, diagnosis, smallest retry, escalation. "Smallest retry" always names what changes on the retry; an identical re-run is not a retry. Two things are never a retry step: `composer update` used to undo something (`10-rollback-and-blast-radius.md`), and a hand-edited `composer.lock`.

Windows sandbox specifics, locked files and path discipline are `/alaa-codex-runtime-ops` (`$alaa-codex-runtime-ops`) `references/10-windows-sandbox-recovery.md`, which wins wherever both describe the same Windows behaviour.

Command forms are given for both shells, because both occur on the same machine: native PowerShell for a Codex session on Windows, POSIX or Git-Bash for a Claude Code Bash-tool call. `$env:VAR = "value"` is PowerShell-only and, pasted into a POSIX shell, fails silently as a literal command rather than erroring. Translate; never paste one form into the other runtime.

## 1. Resolution conflict

**Symptom.** `composer update` exits non-zero with "Your requirements could not be resolved".

**Diagnosis.** `composer why-not <vendor/package> <version>` names the blocking constraint, `composer why <blocker>` names who holds it, and `composer why-not php <version>` or `composer why-not ext-<name> <version>` covers a platform block.

**Smallest retry.** Scope to one package: `composer update <vendor/package> --with-dependencies`. One subtree instead of the whole graph usually turns an unreadable conflict into a single named constraint.

**Escalation.** Record the `why-not` output verbatim, leave the package at its current version, report. Do not force the upgrade and do not guess at the reason. `--ignore-platform-req` and `--ignore-platform-reqs` are forbidden: they produce a lock that cannot install on the target runtime, moving the failure to deploy. Instead set `config.platform` in `composer.json` to the production image's actual PHP version and extension set, so resolution runs against the runtime the service has, or leave the package pinned and record why.

## 2. Test regression

**Symptom.** A post-sweep failure the baseline does not contain, under the identity rule in `20-breaking-change-detection.md`.

**Diagnosis.** Re-run that one test with the baseline's seed to separate order-dependence from a real regression; flake versus intermittent product defect is `/alaa-testing-strategy` (`$alaa-testing-strategy`) `references/50-flake.md`. If real, bisect by package, not by test: from the pre-sweep lock, `composer update <vendor/package> --with-dependencies` one package at a time. Bisecting by test says which assertion broke; bisecting by package says what to pin.

**Smallest retry.** Re-run only the failing test with the offending package moved back one version.

**Escalation.** Pin that package to its pre-sweep version in `composer.json` -- the one sanctioned manifest edit in the sweep -- recording the failing test identifier, the package and both versions, so the next run knows the pin is deliberate rather than stale. Never widen it into a general constraint change.

## 3. Unfixable audit finding

**Symptom.** `composer audit` or `npm audit` non-empty after the upgrade set is applied.

**Diagnosis, action and acceptance.** `30-advisory-triage.md`, in full. The only addition here: an audit finding is not a test failure and never carries the "pre-existing" label, which governs test results and nothing else.

## 4. Generated-artifact write failure

**Symptom.** A regeneration command fails to write while the rest of the run succeeds -- typically `php artisan boost:install --guidelines --mcp --skills --no-interaction` or `boost:update` failing on `.codex/config.toml` or a path under `.agents/skills/`.

**Diagnosis.** In order: does the parent directory exist and is it writable by the current user; is another process holding the file (editor, language server, second agent -- the common Windows case); is the target a symlink into a read-only mount or container bind.

**Smallest retry.** Re-run the same command with exactly one thing changed, and name which: the holding process closed, or a shell with write access to that path (an elevated PowerShell on Windows). Once. A second identical retry is not an escalation.

**Escalation.** Report the artifact as not regenerated, naming the path and the operating system's error text, and leave the dependency change intact. A stale generated artifact is reported, never accepted as fresh, because the next run reads it as current state.

## 5. Cache permission error

**Symptom.** `composer update` or an `npm` command fails with a rename or permission error on a path inside the global cache. Common on Windows and wherever the cache is shared between users or containers.

**Diagnosis.** The error names a path under the global Composer or npm cache, not under the repository.

**Smallest retry.** Re-run with an isolated cache anchored to the manifest root -- not the working directory, which in a monorepo is not the manifest root, and not `$PWD`, which in PowerShell is a `PathInfo` object whose interpolation yields a provider-qualified path that breaks on a PSDrive or a UNC path. Register the ignore patterns before creating anything, per the exclude rule in `10-rollback-and-blast-radius.md`:

```bash
MANIFEST_ROOT=/absolute/path/to/manifest/root      # the root this run covers
printf '%s\n' '.composer-home/' '.composer-cache/' '.npm-cache/' >> "$(git rev-parse --git-path info/exclude)"
export COMPOSER_HOME="$MANIFEST_ROOT/.composer-home"
export COMPOSER_CACHE_DIR="$MANIFEST_ROOT/.composer-cache"
export npm_config_cache="$MANIFEST_ROOT/.npm-cache"
composer update --with-all-dependencies --no-interaction --no-progress
rm -rf "$COMPOSER_HOME" "$COMPOSER_CACHE_DIR" "$npm_config_cache"
```

```powershell
$ManifestRoot = 'C:\absolute\path\to\manifest\root'   # a literal, or (Convert-Path $PWD)
Add-Content -Path (git rev-parse --git-path info/exclude) -Value '.composer-home/', '.composer-cache/', '.npm-cache/'
$env:COMPOSER_HOME      = Join-Path $ManifestRoot '.composer-home'
$env:COMPOSER_CACHE_DIR = Join-Path $ManifestRoot '.composer-cache'
$env:npm_config_cache   = Join-Path $ManifestRoot '.npm-cache'
composer update --with-all-dependencies --no-interaction --no-progress
Remove-Item -Recurse -Force $env:COMPOSER_HOME, $env:COMPOSER_CACHE_DIR, $env:npm_config_cache -ErrorAction SilentlyContinue
```

**Escalation.** Confirm cleanup by both checks, since either can pass while the other fails: `git status --short` shows only intended files, and none of the three directories still exists on disk. Then `/alaa-codex-runtime-ops` (`$alaa-codex-runtime-ops`). Do not escalate privileges broadly and do not abandon the sweep over a cache error.

## 6. Partially-applied update

**Symptom.** A resolution was interrupted and the worktree now describes two dependency sets at once. This is the resume trigger `SKILL.md` names.

**Diagnosis.** Three commands, where the reading matters more than the output:

```bash
git status --short composer.json composer.lock
composer validate --strict                    # manifest and lock agree, via content-hash
composer install --dry-run --no-interaction    # lock and vendor/ agree
```

- Lock modified **and** `vendor/` modified: interrupted resolution; neither artifact is authoritative.
- Lock modified, `vendor/` consistent with the old lock: the resolution wrote the lock and never installed.
- Lock unmodified, `vendor/` modified: interrupted install; the lock is still authoritative, and this is the cheap case.

**Smallest retry.** For an interrupted install, `composer install --no-interaction` alone returns `vendor/` to the lock, where `composer update` would re-resolve into a third state. For the other two the decision comes from the state file: if it records the intended version set, `composer install --no-interaction` from the new lock and continue into the gates; if it does not, restore the pre-sweep lock per `10-rollback-and-blast-radius.md` and run the sweep again, because an unknown partial resolution is not a state any gate can describe.

**Escalation.** Never hand-edit `composer.lock`, and never commit a lock whose `content-hash` disagrees with `composer.json`; `composer validate --strict` catches it. Report which reading applied and which path was taken.

## 7. A declared tool is not where it was expected

**Symptom.** `vendor/bin/<tool>` is absent, or the tool runs but is not the version the repo declares.

**Diagnosis.** `composer config bin-dir` gives the configured directory, which is not always `vendor/bin`; `composer show --direct` says whether the tool is declared at all. The wrapper entrypoint detected in `SKILL.md` may be the only supported invocation.

**Smallest retry.** Invoke through the resolved bin-dir, or through the repo's wrapper target.

**Escalation.** A tool the repo does not declare is never substituted with a globally installed one of unknown version and configuration. Report the gate as unavailable and name it -- `formatting gate not available: none declared` -- so the missing gate appears in the report rather than disappearing from it.
