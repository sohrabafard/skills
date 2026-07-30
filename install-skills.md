# Install local skills

From the repository root, use one source-root list and one destination list. Add any new
vendor, local pack, or agent home to these arrays.

> **One source-root line in the generated block below names the wrong directory.**
> `vendor\basic-memory\basic-memory` holds 5 of the 14 vendored basic-memory skills; the other
> 9 sit one level up at `vendor\basic-memory`. That block is machine-generated, so the correct
> root is maintained by hand on the line after the block's `:end` marker. Read "Vendored source
> roots" below before you change either one.

```powershell
cd D:\Sohrab\Project\skills
$repoRoot = (Resolve-Path ".").Path

$srcRoots = @(
    (Join-Path $repoRoot "skills\.curated")
    (Join-Path $repoRoot "skills\sohrab")
# vendor-subtrees:codex-src-roots:start
    (Join-Path $repoRoot "vendor\openfga-agent-skills\skills")
    (Join-Path $repoRoot "vendor\cc-skills-golang\skills")
    (Join-Path $repoRoot "vendor\basic-memory\basic-memory")
    (Join-Path $repoRoot "vendor\knowledge-work-plugins\design\skills")
    (Join-Path $repoRoot "vendor\knowledge-work-plugins\product-management\skills")
    (Join-Path $repoRoot "vendor")
# vendor-subtrees:codex-src-roots:end
    # Maintained by hand, deliberately outside the generated block above: the generator emits
    # only <prefix>\skills, which does not exist for a source_path snapshot, so it omits this
    # root. Without this line the installer links 5 of 14 basic-memory skills. A future
    # generator fix may emit the same root inside the block; a duplicate is harmless, because
    # the loop below reports EXIST and skips a link that already points at the same target.
    (Join-Path $repoRoot "vendor\basic-memory")
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

## Vendored source roots: what the generated block gets wrong

The `# vendor-subtrees:codex-src-roots` block inside the snippet above is regenerated by
`python scripts\vendor_subtrees.py refresh-docs` from `vendor/subtrees.json`. Never hand-edit inside
that block; the next refresh discards the edit. Two things are true about it today, both verified on
2026-07-30.

**The basic-memory root inside the block is wrong.** It names `vendor\basic-memory\basic-memory`, a
nested duplicate directory holding 5 skills -- `memory-capture`, `memory-continue`,
`memory-metadata-search`, `memory-notes`, `memory-schema`. The 14 real vendored skills sit directly
under `vendor\basic-memory`. With only the generated line, the installer links 5 of 14, and the other
9 -- `memory-ci-capture`, `memory-curate`, `memory-defrag`, `memory-ingest`, `memory-lifecycle`,
`memory-literary-analysis`, `memory-reflect`, `memory-research`, `memory-tasks` -- are never
installed. That is why `(Join-Path $repoRoot "vendor\basic-memory")` is maintained by hand on the
line after the block's `:end` marker: a line there is outside the replaced span and survives every
refresh.

**Refreshing the block today would make it worse, so this is a code defect and not a data defect.**
`scripts/vendor_subtrees.py` builds the block by emitting exactly one line per manifest entry,
hardcoded as `<prefix>\skills`, and only when `<prefix>/skills` exists on disk. Of the six subtrees
in `vendor/subtrees.json`, only `openfga-agent-skills` and `cc-skills-golang` keep their skills
there. `basic-memory` is a `source_path: "skills"` snapshot, which flattens upstream's `skills/`
directly into `vendor\basic-memory`, and `knowledge-work-plugins` keeps its skills at
`<prefix>\<plugin>\skills`. The generator can express neither shape, so a refresh run today emits
two lines and drops four, including both `knowledge-work-plugins` roots and the bare `vendor` root.
The four wrong or unreproducible lines now in the block are therefore stale hand-written text that no
refresh has overwritten yet, not generator output.

The durable fix is an optional per-entry `codex_src_roots` array in `vendor/subtrees.json`, emitted
verbatim, with today's `<prefix>\skills` probe kept as the fallback when the key is absent. That
touches `vendor/subtrees.json`, which is this repository's own manifest rather than upstream content
but still sits under the never-edit-`vendor/` rule, so it is an owner decision and not a routine
edit. Until it is made, do not run `refresh-docs` expecting the block to improve.

## install subagents
```powershell
# Claude world — once, applies to every project
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\agents" | Out-Null
Copy-Item "D:\Sohrab\Project\skills\skills\sohrab\alaa-cc-orchestrator\agents\*.md" "$env:USERPROFILE\.claude\agents\"

# Codex world — once, applies to every project
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\agents" | Out-Null
Copy-Item "D:\Sohrab\Project\skills\skills\sohrab\alaa-codex-orchestrator\agents\*.toml" "$env:USERPROFILE\.codex\agents\"
```


## install browser:
New-Item -ItemType Directory -Force -Path "C:\Users\CIT\.playwright-mcp-profile" | Out-Null
npm install playwright
npx playwright install chromium
npm install -g -D @axe-core/playwright
npx @playwright/mcp@latest --port 8931 --browser chromium --user-data-dir "C:\Users\CIT\.playwright-mcp-profile"

codex config:
```
[mcp_servers.playwright_visual]
command = "npx"
args = [
  "-y",
  "@playwright/mcp@latest",
  "--browser",
  "chromium",
  "--user-data-dir",
  "C:\\Users\\CIT\\.playwright-mcp-profile"
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
$srcRoot = "D:\Sohrab\Project\skills\vendor\openfga-agent-skills\skills"
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
