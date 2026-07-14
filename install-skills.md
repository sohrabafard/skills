# Install local skills

From the repository root, use one source-root list and one destination list. Add any new
vendor, local pack, or agent home to these arrays.

```powershell
cd D:\Sohrab\Project\skills
$repoRoot = (Resolve-Path ".").Path

$srcRoots = @(
    (Join-Path $repoRoot "skills\.curated")
    (Join-Path $repoRoot "skills\sohrab")
# vendor-subtrees:codex-src-roots:start
    (Join-Path $repoRoot "vendor\openfga-agent-skills\skills")
    (Join-Path $repoRoot "vendor\cc-skills-golang\skills")
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
