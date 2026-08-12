# Install local skills

From the repository root, use one source-root list and one destination list. Add any new
vendor, local pack, or agent home to these arrays.

> The source-root lines between the `# vendor-subtrees:codex-src-roots` markers below are generated
> from `vendor/subtrees.json`. To change which directories the installer scans, read "Vendored
> source roots" near the end of this file.

```powershell
# Run this from the repository root; every path below is resolved from it.
$repoRoot = (Resolve-Path ".").Path

$srcRoots = @(
    (Join-Path $repoRoot "skills\.curated")
    (Join-Path $repoRoot "skills\sohrab")
# vendor-subtrees:codex-src-roots:start
    (Join-Path $repoRoot "vendor\openfga-agent-skills\skills")
    (Join-Path $repoRoot "vendor\cc-skills-golang\skills")
    (Join-Path $repoRoot "vendor\knowledge-work-plugins\design\skills")
    (Join-Path $repoRoot "vendor\knowledge-work-plugins\product-management\skills")
    (Join-Path $repoRoot "vendor\basic-memory\basic-memory")
    (Join-Path $repoRoot "vendor")
# vendor-subtrees:codex-src-roots:end
)

$destinations = @(
    [pscustomobject]@{ Name = "codex"; Path = (Join-Path $HOME ".codex\skills") }
    [pscustomobject]@{ Name = "claude"; Path = (Join-Path $HOME ".claude\skills") }
)

function Resolve-LinkTargetPath {
    param([Parameter(Mandatory)][string] $Path)

    try {
        return (Resolve-Path -LiteralPath $Path -ErrorAction Stop).Path
    } catch {
        return [System.IO.Path]::GetFullPath($Path)
    }
}

function Write-LinkDebugStatus {
    param(
        [Parameter(Mandatory)][string] $Status,
        [Parameter(Mandatory)][string] $DestinationName,
        [Parameter(Mandatory)][string] $SkillName,
        [Parameter(Mandatory)][string] $Source,
        [Parameter(Mandatory)][string] $Destination
    )

    if ($Status -eq "LINK") {
        Write-Host "$Status [$DestinationName] $SkillName" -ForegroundColor Yellow
    } else {
        Write-Host "$Status [$DestinationName] $SkillName"
    }

    Write-Host "  Source:      $Source"
    Write-Host "  Destination: $Destination"
}

foreach ($destination in $destinations) {
    New-Item -ItemType Directory -Force -Path $destination.Path | Out-Null
}

foreach ($srcRoot in $srcRoots) {
    if (-not (Test-Path -LiteralPath $srcRoot -PathType Container)) {
        Write-Warning "Source root missing, skipped: $srcRoot"
        continue
    }

    Get-ChildItem -LiteralPath $srcRoot -Directory |
        Where-Object {
            $_.Name -notlike ".*" -and
            (Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md") -PathType Leaf)
        } |
        ForEach-Object {
            $skillName = $_.Name
            $target = $_.FullName
            $expectedTarget = Resolve-LinkTargetPath $target

            foreach ($destination in $destinations) {
                $linkPath = Join-Path $destination.Path $skillName
                $prefix = "[$($destination.Name)] $skillName"

                $item = Get-Item -LiteralPath $linkPath -Force -ErrorAction SilentlyContinue

                if ($null -eq $item) {
                    New-Item -ItemType SymbolicLink -Path $linkPath -Target $target | Out-Null
                    Write-LinkDebugStatus -Status "LINK" -DestinationName $destination.Name -SkillName $skillName -Source $target -Destination $linkPath
                    continue
                }

                if ($item.LinkType -ne "SymbolicLink") {
                    Write-LinkDebugStatus -Status "EXIST" -DestinationName $destination.Name -SkillName $skillName -Source $target -Destination $linkPath
                    Write-Warning "Skipped: $prefix exists but is not a symlink"
                    continue
                }

                $rawTarget = @($item.Target)[0]
                $actualTarget = Resolve-LinkTargetPath ([string]$rawTarget)
                if ($actualTarget -eq $expectedTarget) {
                    Write-LinkDebugStatus -Status "EXIST" -DestinationName $destination.Name -SkillName $skillName -Source $target -Destination $linkPath
                    continue
                }

                Write-LinkDebugStatus -Status "EXIST" -DestinationName $destination.Name -SkillName $skillName -Source $target -Destination $linkPath
                Write-Warning "Skipped: $prefix target does not match"
                Write-Host "  Actual:      $rawTarget"
            }
        }
}
```
## Where a skill is installed, and how it is invoked

This file is authoritative for install paths. Three facts follow, and no document in this repository
may contradict them.

**A personal skill installs under the user's home.** Both destinations above are user-level:
`Join-Path $HOME ".codex\skills"` for Codex and `Join-Path $HOME ".claude\skills"` for Claude Code.
On a POSIX shell those are `~/.codex/skills` and `~/.claude/skills`. A skill installed there follows
the user into every repository, which is what a general-purpose skill wants.

**`.agents/skills` is reserved for a skill that travels with one repository**, checked in beside the
code it governs, and it is never a target of this installer. `~/.agents/skills` is not an install
location at all: a document that names it as the user-level path is wrong, and the correct value is
`~/.codex/skills` above.

**Invocation is `/name` in Claude Code and `$name` in Codex**, and both forms name the same skill.
Whether a skill may be selected without being named is declared once per skill, in its
`agents/openai.yaml` under `policy.allow_implicit_invocation`. Read the value out of that file. A
sentence of prose asserting a value for it is a second copy of a fact the runtime reads from the
YAML, and the two will eventually disagree.

## Vendored source roots

The `# vendor-subtrees:codex-src-roots` block inside the snippet above is generated by
`python scripts\vendor_subtrees.py refresh-docs` from `vendor/subtrees.json`. The next refresh
discards an edit made inside that span. To change which directories the installer scans, edit
`vendor/subtrees.json` and run `refresh-docs`.

**How the generator picks a source root.** It walks `vendor/subtrees.json` in order and emits one
line per source root, skipping a root an earlier entry already emitted:

- An entry with a `codex_src_roots` array supplies its roots verbatim. Declare that key when the
  pack does not keep its skills at `<prefix>/skills`, or when this repository installs some of a
  pack's skills and not others.
- An entry without that key falls back to `<prefix>\skills`, emitted only when that directory
  exists on disk. `openfga-agent-skills` and `cc-skills-golang` are on that fallback.
- An entry with an empty `codex_src_roots` array emits nothing, which records that the pack is
  vendored deliberately and installed deliberately. `claude-plugins-official` is that case: it
  ships 16 `<plugin>/skills` directories and this repository installs none of them.

A `codex_src_roots` value that is not a list of non-empty strings stops `refresh-docs` with a
message naming the entry, and leaves both documents unchanged. A declared root that does not exist
on disk is still emitted, and `refresh-docs` reports it on stderr, because the installer's own loop
prints `Source root missing, skipped` for it -- dropping the line would hide the typo instead of
showing it.

**Why an array and not directory discovery.** `knowledge-work-plugins` ships 17 `<plugin>/skills`
directories and this repository installs 2 of them, `design` and `product-management`. Which 2 is a
decision this repository makes, and nothing in the directory tree records it, so no probe can
reproduce the intended set.

**`vendor` is a source root in its own right.** `skill-temporal-developer` is a single skill whose
`SKILL.md` sits at the top of its own prefix, so the directory the installer has to scan is the
parent, `vendor`. That root is declared on the `skill-temporal-developer` entry.

**basic-memory installs from `vendor\basic-memory`.** The entry's `source_path: "skills"` flattens
upstream's `skills/` directory straight into `vendor\basic-memory`, so its 14 vendored skills sit
directly there. `vendor\basic-memory\basic-memory` is a nested duplicate holding 5 of the 14.
Until 2026-07-31 the block named that nested directory, so the installer linked 5 of 14 and never
installed `memory-ci-capture`, `memory-curate`, `memory-defrag`, `memory-ingest`,
`memory-lifecycle`, `memory-literary-analysis`, `memory-reflect`, `memory-research` or
`memory-tasks`.

**One-time cleanup on a machine that installed before 2026-07-31.** Five links in `~\.codex\skills`
and `~\.claude\skills` still point into the nested duplicate. The installer prints
`Skipped: [codex] memory-capture target does not match` for each one and changes nothing, so the
links have to be removed once. Run this from the repository root to see them:

```powershell
$stale = Join-Path (Resolve-Path ".").Path "vendor\basic-memory\basic-memory"
foreach ($dest in @("$HOME\.codex\skills", "$HOME\.claude\skills")) {
    Get-ChildItem -LiteralPath $dest -Force -ErrorAction SilentlyContinue |
        Where-Object { $_.LinkType -eq "SymbolicLink" -and (@($_.Target)[0]) -like "$stale*" } |
        ForEach-Object { Write-Host "stale: $($_.FullName) -> $(@($_.Target)[0])" }
}
```

Replace the last line's `Write-Host` with `Remove-Item -LiteralPath $_.FullName -Force` to delete
exactly the links that listing named, then run the install snippet at the top of this file again.
The filter matches only a symlink whose target is inside the nested duplicate, so a link that
already points at `vendor\basic-memory` is left in place.

**Editing `vendor/subtrees.json` is allowed; editing anything else under `vendor/` is not.** The
never-edit rule in `skills/sohrab/AGENTS.md` protects upstream content that a later
`git subtree pull` overwrites. This file is not that. Every subtree prefix is `vendor/<name>`, so a
pull writes only inside a sibling directory and cannot reach `vendor/subtrees.json`, and
`scripts/vendor_subtrees.py` writes the file itself when `add` records a new vendor.

## install subagents

Run from the repository root. `$repoRoot` is resolved from the working directory for the same reason
the snippet at the top of this file does it: an absolute path from one machine is wrong on every
other one.

```powershell
$repoRoot = (Resolve-Path ".").Path

# Claude world — once, applies to every project
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\agents" | Out-Null
Copy-Item (Join-Path $repoRoot "skills\sohrab\alaa-cc-orchestrator\agents\*.md") "$env:USERPROFILE\.claude\agents\"

# Codex world — once, applies to every project
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\agents" | Out-Null
Copy-Item (Join-Path $repoRoot "skills\sohrab\alaa-codex-orchestrator\agents\*.toml") "$env:USERPROFILE\.codex\agents\"
```

### The `alaa-rule-writer` specialist

The two runtimes reach this agent by different routes, and only one of them is a command.

**Claude Code: nothing to run.** The definition ships inside the plugin and Claude loads it from the
plugin-root `agents/` directory once the plugin is installed or enabled, so rebuilding and
reinstalling the plugin is the whole update path. Do not copy a wrapper into
`$env:USERPROFILE\.claude\agents` and do not write an installation sentinel; a hand-placed copy
would shadow the packaged one and then go stale silently.

**Codex: one copy, since Codex has no plugin.** Run from the repository root:

```powershell
$repoRoot = (Resolve-Path ".").Path
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\agents" | Out-Null
Copy-Item (Join-Path $repoRoot "skills\sohrab\alaa-prompting-guide\assets\rule-writer\codex\alaa-rule-writer.toml") "$env:USERPROFILE\.codex\agents\" -Force
```

`-Force` replaces a differing prior version and keeps no backup, matching both orchestrator packs.
Run `python skills\sohrab\alaa-prompting-guide\scripts\check_rule_writer_grants.py` first; exit `0`
is the gate, and `1` or `2` both fail it.


## install browser:
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.playwright-mcp-profile" | Out-Null
npm install playwright
npx playwright install chromium
npm install -g -D @axe-core/playwright
npx @playwright/mcp@latest --port 8931 --browser chromium --user-data-dir "$env:USERPROFILE\.playwright-mcp-profile"

codex config: substitute your own home directory for `USER_HOME` below. Codex reads this file as
TOML and does not expand an environment variable inside it, so the path has to be absolute and
cannot be written portably the way the PowerShell lines above are.

```
[mcp_servers.playwright_visual]
command = "npx"
args = [
  "-y",
  "@playwright/mcp@latest",
  "--browser",
  "chromium",
  "--user-data-dir",
  "USER_HOME\\.playwright-mcp-profile"
]
startup_timeout_sec = 60
tool_timeout_sec = 300
enabled = true
```

## install openfga vendoor
first add vendor skill
```bash
git remote add openfga-upstream https://github.com/openfga/agent-skills.git
git subtree add --prefix vendor/openfga-agent-skills openfga-upstream main --squash
```
Then update later with:
```bash
git fetch openfga-upstream
git subtree pull --prefix vendor/openfga-agent-skills openfga-upstream main --squash
```
Then hook it into your existing install pattern by linking the vendored skill folder into Codex:
```bash
$srcRoot = Join-Path (Resolve-Path ".").Path "vendor\openfga-agent-skills\skills"
$dstRoot = "$HOME\.codex\skills"

New-Item -ItemType Directory -Force -Path $dstRoot | Out-Null

Get-ChildItem $srcRoot -Directory | ForEach-Object {
    $linkPath = Join-Path $dstRoot $_.Name
    if (-not (Test-Path $linkPath)) {
        New-Item -ItemType SymbolicLink -Path $linkPath -Target $_.FullName | Out-Null
        Write-Host "Linked: $($_.Name)"
    } else {
        Write-Host "Exists: $($_.Name)"
    }
}
```
after any `openfga-upstream` update and pull it please run:
```bash
git fetch openfga-upstream
git subtree pull --prefix vendor/openfga-agent-skills openfga-upstream main --squash
```
then
```bash
node .\vendor\openfga-agent-skills\scripts\build-agents-md.js
```

## vendored skill packs

This repository tracks upstream skill packs under `vendor/`. Metadata-backed entries use `git subtree`; pinned or source-path snapshots are committed vendor directories and are refreshed manually.

<!-- vendor-subtrees:install-list:start -->
Current vendored upstreams:
- [`vendor/openfga-agent-skills`](vendor/openfga-agent-skills/) from `https://github.com/openfga/agent-skills.git`
- [`vendor/cc-skills-golang`](vendor/cc-skills-golang/) from `https://github.com/samber/cc-skills-golang.git`
- [`vendor/claude-plugins-official`](vendor/claude-plugins-official/) from `https://github.com/anthropics/claude-plugins-official.git`
- [`vendor/knowledge-work-plugins`](vendor/knowledge-work-plugins/) from `https://github.com/anthropics/knowledge-work-plugins.git`
- [`vendor/basic-memory`](vendor/basic-memory/) from `https://github.com/basicmachines-co/basic-memory.git`
- [`vendor/skill-temporal-developer`](vendor/skill-temporal-developer/) from `https://github.com/temporalio/skill-temporal-developer.git`
<!-- vendor-subtrees:install-list:end -->

The source of truth for subtree definitions is:

```powershell
vendor/subtrees.json
```

Important behavior:
- vendored files are committed into this repository like normal files
- when you sync vendor updates locally and push to `origin`, every future clone of `origin` already gets those vendor files
- another clone does not need a separate subtree pull unless you want to refresh directly from upstream vendors again
- local Git configuration does not travel through `origin`, so subtree remotes and hook activation still need one setup command per clone

One-time setup per clone to make plain `git pull` also sync all configured subtrees:

```powershell
python scripts\vendor_subtrees.py install-hooks
```

That command:
- configures `core.hooksPath=.githooks` for the current clone
- ensures all subtree remotes from `vendor/subtrees.json` exist locally

After that, the repo-managed `post-merge` and `post-rewrite` hooks call the shared sync script after pull, merge, and rebase flows.

Manual subtree commands are still available:

```powershell
python scripts\vendor_subtrees.py list
python scripts\vendor_subtrees.py ensure-remotes
python scripts\vendor_subtrees.py sync
python scripts\vendor_subtrees.py refresh-docs
```

Notes:
- `python scripts\vendor_subtrees.py sync` fetches each syncable vendor remote and runs `git subtree pull --squash` for existing subtree-backed prefixes
- if a syncable configured prefix is missing locally, the script bootstraps it with `git subtree add --squash`
- pinned or source-path snapshots are reported and skipped because they do not have subtree metadata to pull from
- `python scripts\vendor_subtrees.py sync` requires a clean worktree; hook-driven sync skips automatically when the worktree is dirty
- when `openfga-agent-skills` changes, the sync script also runs `node vendor/openfga-agent-skills/scripts/build-agents-md.js`

To headlessly add a new vendor from only its Git URL:

```powershell
python scripts\vendor_subtrees.py add https://github.com/org/repo.git
```

Optional overrides are available when needed:

```powershell
python scripts\vendor_subtrees.py add https://github.com/org/repo.git --branch main --name repo --prefix vendor\repo --remote repo-upstream
```

That command only vendors the repository, updates `vendor/subtrees.json`, and refreshes the docs. It does not auto-enable hooks and it does not auto-link the new vendored skills into Codex.

Recommended pattern as vendored packs grow:
- keep vendors committed under `vendor/`
- expose only the specific skills you want Codex to see
- avoid bulk-linking every vendored skill pack unless you really want all of them routed

Selective vendored skill exposure is managed with:

```powershell
python scripts\vendor_skill_links.py vendors
python scripts\vendor_skill_links.py list --vendor cc-skills-golang
python scripts\vendor_skill_links.py link --vendor cc-skills-golang --skill golang-testing --skill golang-troubleshooting
python scripts\vendor_skill_links.py link --vendor cc-skills-golang --skill-prefix golang-samber- --dry-run
python scripts\vendor_skill_links.py unlink --vendor cc-skills-golang --all --dry-run
```

Notes:
- `vendors` shows each vendored pack that has a `skills/` directory
- `list` shows available vendored skills plus whether each one is already linked into `~/.codex/skills`
- `link` creates only the symlinks you explicitly selected
- `unlink` removes only matching symlinks that point at the expected vendored skill directories
- the script refuses to overwrite conflicting existing destinations

To link vendored skills, add the relevant vendored `skills/` directory to `$srcRoots`
in the unified local install snippet above. The vendored source-root lines in that
snippet are refreshed by `python scripts\vendor_subtrees.py refresh-docs`.
