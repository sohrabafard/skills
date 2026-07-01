# Memory, Skill Loading, and Windows Cache Friction

## Memory / continuity schema

Two equally valid shapes exist, chosen by which runtime and trigger actually apply -- neither is the "real" one with the other as a fallback:

**Codex automation framing** (used when this run is triggered as a Codex automation):

```text
Automation: upgrade all packages
Automation ID: upgrade-all-packages
Automation memory: $CODEX_HOME/automations/upgrade-all-packages/memory.md
Last run: <timestamp>
```

Codex reads this memory file at the start of the run and updates it at the end with the outcome (versions landed, blockers recorded, anything deferred). Treat it as authoritative continuation state -- if the memory says a prior run was interrupted mid-change, resume and finish that, don't start clean.

**Repo-local state-file framing** (used for a Claude Code run, a `/loop`-triggered run, any run with no Codex automation context at all, or a Codex run that also wants a durable in-repo record other agents can find later, per `$alaa-workflow`/`/alaa-workflow` conventions):

```text
docs/agents/upgrade-all-packages-execution-state.md
docs/_agent_plans/<stem>_upgrade-all-packages.md   (optional, for a fuller plan record)
```

Both forms carry the same information. Prefer whichever one this repo already has in place. **On a genuine first run, when neither file exists yet:** proceed with the sweep anyway, then create the repo-local state file before finishing -- do not wait for a second run to start tracking continuity, and do not treat the absence of a memory file as a reason to skip the state-tracking step.

## Standard skill-loading list

Every observed instance of this automation loads a fixed list of skills before touching dependencies. Adapt the exact set to what this repo actually has installed, but the shape is consistently: workflow discipline, PHP clean-code, Laravel architecture, services-contract, low-noise, observability/SOC, security-review, trust-gateway-auth, service-runtime-kit governance, and this repo's Windows/Codex runtime-ops skill. Loading the list up front, before any `composer` command runs, is itself part of the pattern -- it is not just a formality.

## Windows Composer/npm cache permission workaround

On Windows, the global Composer cache can hit rename/permission errors during `composer update`, and `npm` can hit similar issues. The fix used consistently across this portfolio is an isolated, repo-local cache directory for the duration of the run, removed afterward. Use whichever form matches the shell actually running the command -- native PowerShell (the default for a Codex app/CLI session on Windows) or a POSIX/Git-Bash shell (common for a Claude Code Bash-tool call on the same machine); `$env:VAR = "value"` is PowerShell-only syntax and silently fails as a literal command in a POSIX shell, so do not paste one form into the other runtime without translating it:

```powershell
$env:COMPOSER_HOME = "$PWD\.composer-home"
$env:COMPOSER_CACHE_DIR = "$PWD\.composer-cache"
composer update --with-all-dependencies --no-interaction --no-progress
Remove-Item -Recurse -Force .composer-home, .composer-cache -ErrorAction SilentlyContinue
```

```bash
export COMPOSER_HOME="$PWD/.composer-home"
export COMPOSER_CACHE_DIR="$PWD/.composer-cache"
composer update --with-all-dependencies --no-interaction --no-progress
rm -rf .composer-home .composer-cache
```

Do the same for `npm` if it hits an equivalent cache error (`npm_config_cache` / `$env:npm_config_cache`, pointed at a repo-local `.npm-cache` directory, in whichever shell form applies). Never leave these directories behind in the final diff -- confirm with `git status --short` that only intended dependency/doc/state files changed.

## Boost-specific friction

If the repo uses Laravel Boost, `php artisan boost:install --guidelines --mcp --skills --no-interaction` (or `boost:update`) can fail to write `.codex/config.toml` or `.agents/skills/...` on Windows with a permission error even when the rest of the run succeeds. Retry the same command once with escalation rather than skipping the Boost refresh step.
