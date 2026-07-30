[CmdletBinding()]
param(
  [string]$VaultPath = "",
  [string]$OutFile = "",
  [string]$Project = "",
  [switch]$IncludeStoreOrphans,
  [switch]$StrictHygiene,
  [switch]$SelfTest
)

# =============================================================================
# alaa_obsidian_linkcheck.ps1
#
# Read-only wiki-link health check over a file-backed memory vault. Changes
# nothing on disk except the report file.
#
# Assertions:
#   1. Every wiki link resolves to a note filename, title, alias, or permalink.
#   2. Every note has at least one incoming wiki link.          (hygiene)
#   3. Every note has a "## Relations" section.                 (hygiene)
#
# Exit codes:
#   0  no broken links (and, with -StrictHygiene, no hygiene findings either)
#   1  findings
#   2  could not run: the vault path did not resolve to a directory
#
# Why only assertion 1 sets exit 1 by default: a broken link points at nothing
# and is unambiguously a defect. An orphan note that is correct and findable by
# search is not. A checker that exits 1 on every real vault gets switched off,
# and then assertion 1 stops being checked too. Pass -StrictHygiene to make all
# three count.
#
# Complexity: one pass builds a link-target index over N notes, then each of the
# L links costs one dictionary lookup. O(N + L). The earlier version scanned
# every note for every link, which is O(N x L) and unusable on a vault of a few
# thousand notes.
#
# Windows is the target platform. Vault-relative paths are normalised to forward
# slashes before any comparison, because a backslash glob matches nothing off
# Windows and would silently widen the checked set.
# =============================================================================

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot '_common.ps1')

if ($SelfTest) {
  $result = Invoke-SelfTest -ScriptPath $PSCommandPath -Cases @(
    @{ Name = 'red-vault has a broken link'; Expect = 1; Args = @('-VaultPath', '@fixture:red-vault@') },
    @{ Name = 'green-vault is clean';        Expect = 0; Args = @('-VaultPath', '@fixture:green-vault@') },
    @{ Name = 'green-vault strict hygiene';  Expect = 0; Args = @('-VaultPath', '@fixture:green-vault@', '-StrictHygiene') },
    @{ Name = 'unresolvable vault is BLOCKED, not a finding'; Expect = 2; Args = @('-VaultPath', 'no-such-vault-path-exists-here') }
  )
  exit $result
}

$vault = Resolve-VaultRoot -VaultPath $VaultPath
if (-not $vault.Ok) {
  Write-Host "BLOCKED: $($vault.Reason)"
  exit 2
}
$root = $vault.Path

$mdFiles = @(Get-ChildItem -LiteralPath $root -Recurse -Filter *.md -File -ErrorAction SilentlyContinue |
  Where-Object {
    $rel = Get-RelativeNotePath -FullName $_.FullName -Root $root
    $rel -notmatch '(^|/)\.obsidian/' -and $rel -notmatch '(^|/)archive/'
  })

if ($mdFiles.Count -eq 0) {
  Write-Host "BLOCKED: no markdown notes found under $root"
  exit 2
}

# --- One pass: per-note record, plus an index from every link-target form to the
#     notes that form addresses. Titles, permalinks and aliases are indexed too,
#     so a link written as a title credits the note it names. The earlier version
#     accepted such a link as valid but credited nothing, which reported the
#     target as an orphan.
$notes = @{}
$targetIndex = New-Object 'System.Collections.Generic.Dictionary[string,System.Collections.Generic.List[string]]' ([System.StringComparer]::OrdinalIgnoreCase)

function Add-Target {
  param([string]$Key, [string]$NoteId)
  if ([string]::IsNullOrWhiteSpace($Key)) { return }
  $k = $Key.Trim()
  if (-not $targetIndex.ContainsKey($k)) {
    $targetIndex[$k] = New-Object 'System.Collections.Generic.List[string]'
  }
  if (-not $targetIndex[$k].Contains($NoteId)) { $targetIndex[$k].Add($NoteId) }
}

foreach ($f in $mdFiles) {
  $id = $f.FullName
  $raw = Get-Content -LiteralPath $id -Raw -ErrorAction SilentlyContinue
  if ($null -eq $raw) { $raw = "" }
  $base = [System.IO.Path]::GetFileNameWithoutExtension($f.Name)

  $notes[$id] = @{
    Rel      = (Get-RelativeNotePath -FullName $id -Root $root)
    Base     = $base
    Raw      = $raw
    Incoming = 0
  }

  Add-Target -Key $base -NoteId $id

  $fm = Get-NoteFrontmatter -Raw $raw
  if ($null -ne $fm) {
    foreach ($key in @('title', 'permalink')) {
      if ($fm.ContainsKey($key) -and $fm[$key] -is [string]) { Add-Target -Key $fm[$key] -NoteId $id }
    }
    if ($fm.ContainsKey('aliases') -and $fm['aliases'] -is [array]) {
      foreach ($a in $fm['aliases']) { Add-Target -Key $a -NoteId $id }
    }
  }
}

# --- Scan links. Strips an optional #heading and an optional |display label.
$broken = @()
$linkRegex = [regex]'\[\[([^\]\|#]+)(?:#[^\]\|]*)?(?:\|[^\]]*)?\]\]'

foreach ($id in @($notes.Keys)) {
  foreach ($m in $linkRegex.Matches($notes[$id].Raw)) {
    $target = $m.Groups[1].Value.Trim()
    # Template placeholders are not links: [[<Project> Index]] and the like.
    if ($target -match '^<.*>$' -or $target -match '<[A-Za-z]') { continue }

    if ($targetIndex.ContainsKey($target)) {
      foreach ($credited in $targetIndex[$target]) { $notes[$credited].Incoming++ }
    } else {
      $broken += [pscustomobject]@{ File = $notes[$id].Rel; Link = $target }
    }
  }
}

$excludeGlobs = @('00-control/templates/*', '00-control/schemas/*', 'projects/_template/*')
$orphans = @()
$noRelations = @()
foreach ($id in @($notes.Keys)) {
  $rel = $notes[$id].Rel
  $skip = $false
  foreach ($g in $excludeGlobs) { if ($rel -like $g) { $skip = $true; break } }
  if ($skip) { continue }
  if ($notes[$id].Incoming -eq 0) { $orphans += $rel }
  if ($notes[$id].Raw -notmatch '(?m)^##\s+Relations') { $noRelations += $rel }
}

# --- Report
$sb = [System.Text.StringBuilder]::new()
[void]$sb.AppendLine("# Wiki Link Check Report")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("- Vault: $root")
[void]$sb.AppendLine("- Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm')")
[void]$sb.AppendLine("- Notes scanned: $($mdFiles.Count)")
[void]$sb.AppendLine("- Hygiene findings affect the exit code: $([bool]$StrictHygiene)")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("## Broken wiki links ($($broken.Count))")
[void]$sb.AppendLine("")
if ($broken.Count -gt 0) {
  foreach ($b in ($broken | Sort-Object File, Link)) {
    [void]$sb.AppendLine("- ``$($b.File)`` -> [[$($b.Link)]] not found")
  }
} else { [void]$sb.AppendLine("- none") }
[void]$sb.AppendLine("")
[void]$sb.AppendLine("## Orphan notes, no incoming wiki link ($($orphans.Count))")
[void]$sb.AppendLine("")
if ($orphans.Count -gt 0) { foreach ($o in ($orphans | Sort-Object)) { [void]$sb.AppendLine("- ``$o``") } }
else { [void]$sb.AppendLine("- none") }
[void]$sb.AppendLine("")
[void]$sb.AppendLine("## Notes without a Relations section ($($noRelations.Count))")
[void]$sb.AppendLine("")
if ($noRelations.Count -gt 0) { foreach ($n in ($noRelations | Sort-Object)) { [void]$sb.AppendLine("- ``$n``") } }
else { [void]$sb.AppendLine("- none") }

$text = $sb.ToString()
Write-Host $text

if ($IncludeStoreOrphans -and (Test-Tool -Name 'bm')) {
  Write-Host "Store relation-graph orphans:"
  $storeArgs = @('orphans')
  if (-not [string]::IsNullOrWhiteSpace($Project)) { $storeArgs += @('--project', $Project) }
  # -Project is honoured rather than a hardcoded project name: the earlier
  # version ignored its own parameters and always queried one fixed project.
  [void](Invoke-Store -Exe 'bm' -StoreArgs $storeArgs)
}

if (-not [string]::IsNullOrWhiteSpace($OutFile)) {
  Write-TextFileNoBom -Path $OutFile -Text $text
  Write-Host "Report saved: $OutFile"
}

$hygieneCount = $orphans.Count + $noRelations.Count
$findings = $broken.Count
if ($StrictHygiene) { $findings += $hygieneCount }

if ($findings -gt 0) {
  Write-Host "linkcheck: $($broken.Count) broken link(s), $hygieneCount hygiene finding(s)"
  exit 1
}
Write-Host "linkcheck: clean ($hygieneCount hygiene finding(s) not counted)"
exit 0
