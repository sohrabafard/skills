[CmdletBinding()]
param(
  [string]$VaultPath = "",
  [string]$SourceRoot = "",
  [int]$MaxAgeDays = 90,
  [string[]]$SourceDerivedTypes = @('architecture', 'contract', 'service_ownership', 'operations'),
  [string]$OutFile = "",
  [switch]$SelfTest
)

# =============================================================================
# alaa_memory_staleness.ps1
#
# Read-only. Makes the staleness rule enforceable instead of advisory.
#
# knowledge-shape.md requires canonical_source_paths and last_verified on every
# source-derived note, and until this script existed nothing checked either. A
# note that records a fact from a repository file and does not name that file
# cannot be re-verified by anything, so it decays with no symptom. That is the
# failure this checks for: memory that goes stale silently is worse than no
# memory, because it is trusted.
#
# Assertions:
#   1. Every path in canonical_source_paths resolves on disk.
#   2. last_verified (or last_curated) is present, parseable, and no older than
#      -MaxAgeDays.
#   3. A note whose type is source-derived carries a non-empty
#      canonical_source_paths.
#
# Exit codes:
#   0  no findings
#   1  findings
#   2  could not run: the vault path did not resolve, or it holds no notes
#
# Store-agnostic by construction: it reads note frontmatter and stats the file
# system, and calls no store command.
#
# Complexity: one pass over N notes, one file-existence test per recorded path.
# O(N + P) for P recorded paths.
# =============================================================================

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot '_common.ps1')

if ($SelfTest) {
  # Case 3 is the one that cannot rot. With a zero-day threshold, any note
  # verified before today is stale, so the freshness assertion is proven to fire
  # against a committed fixture whose date only recedes further into the past. A
  # fixture carrying a hardcoded "fresh" date would silently stop testing
  # anything the day it aged past the default threshold.
  $result = Invoke-SelfTest -ScriptPath $PSCommandPath -Cases @(
    @{ Name = 'red-vault: dead path, stale date, missing field'; Expect = 1; Args = @('-VaultPath', '@fixture:red-vault@') },
    @{ Name = 'green-vault: no false positives';                 Expect = 0; Args = @('-VaultPath', '@fixture:green-vault@', '-MaxAgeDays', '36500') },
    @{ Name = 'green-vault: freshness assertion fires at 0 days'; Expect = 1; Args = @('-VaultPath', '@fixture:green-vault@', '-MaxAgeDays', '0') },
    @{ Name = 'unresolvable vault is BLOCKED, not a finding';     Expect = 2; Args = @('-VaultPath', 'no-such-vault-path-exists-here') }
  )
  exit $result
}

$vault = Resolve-VaultRoot -VaultPath $VaultPath
if (-not $vault.Ok) {
  Write-Host "BLOCKED: $($vault.Reason)"
  exit 2
}
$root = $vault.Path

# Source paths are repository paths. Resolve them against an explicit source
# root when given, then the environment, then the vault itself.
$srcRoot = $SourceRoot
if ([string]::IsNullOrWhiteSpace($srcRoot)) { $srcRoot = $env:ALAA_SOURCE_ROOT }
if ([string]::IsNullOrWhiteSpace($srcRoot)) { $srcRoot = $root }
if (-not (Test-Path -LiteralPath $srcRoot -PathType Container)) {
  Write-Host "BLOCKED: source root is not a directory: $srcRoot"
  exit 2
}

if ($MaxAgeDays -lt 0) {
  Write-Host "BLOCKED: -MaxAgeDays must be zero or greater, got $MaxAgeDays"
  exit 2
}

$mdFiles = @(Get-ChildItem -LiteralPath $root -Recurse -Filter *.md -File -ErrorAction SilentlyContinue |
  Where-Object {
    $rel = Get-RelativeNotePath -FullName $_.FullName -Root $root
    $rel -notmatch '(^|/)\.obsidian/' -and $rel -notmatch '(^|/)archive/'
  })

if ($mdFiles.Count -eq 0) {
  Write-Host "BLOCKED: no markdown notes found under $root"
  exit 2
}

$deadPaths    = @()
$staleNotes   = @()
$missingField = @()
$badDates     = @()
$cutoff       = (Get-Date).Date.AddDays(-$MaxAgeDays)

foreach ($f in $mdFiles) {
  $rel = Get-RelativeNotePath -FullName $f.FullName -Root $root
  $raw = Get-Content -LiteralPath $f.FullName -Raw -ErrorAction SilentlyContinue
  if ($null -eq $raw) { $raw = "" }
  $fm = Get-NoteFrontmatter -Raw $raw
  if ($null -eq $fm) { continue }

  $type = ""
  if ($fm.ContainsKey('type') -and $fm['type'] -is [string]) { $type = $fm['type'] }

  $paths = @()
  if ($fm.ContainsKey('canonical_source_paths')) {
    if ($fm['canonical_source_paths'] -is [array]) { $paths = @($fm['canonical_source_paths']) }
    elseif ($fm['canonical_source_paths'] -is [string] -and $fm['canonical_source_paths'] -ne '[]') {
      $paths = @($fm['canonical_source_paths'])
    }
  }

  # Assertion 3
  if ($SourceDerivedTypes -contains $type -and $paths.Count -eq 0) {
    $missingField += [pscustomobject]@{ Note = $rel; Field = 'canonical_source_paths'; Type = $type }
  }

  # Assertion 1
  foreach ($p in $paths) {
    if ([string]::IsNullOrWhiteSpace($p)) { continue }
    $candidate = $p
    if (-not [System.IO.Path]::IsPathRooted($candidate)) { $candidate = Join-Path $srcRoot $p }
    if (-not (Test-Path -LiteralPath $candidate)) {
      $deadPaths += [pscustomobject]@{ Note = $rel; Path = $p }
    }
  }

  # Assertion 2. last_curated stands in for last_verified on curated lessons.
  $stampKey = ""
  foreach ($k in @('last_verified', 'last_curated')) {
    if ($fm.ContainsKey($k) -and $fm[$k] -is [string] -and -not [string]::IsNullOrWhiteSpace($fm[$k])) {
      $stampKey = $k; break
    }
  }

  if ($stampKey -eq "") {
    if ($SourceDerivedTypes -contains $type) {
      $missingField += [pscustomobject]@{ Note = $rel; Field = 'last_verified'; Type = $type }
    }
  } else {
    $parsed = [datetime]::MinValue
    if ([datetime]::TryParse($fm[$stampKey], [ref]$parsed)) {
      if ($parsed.Date -lt $cutoff) {
        $ageDays = [int]((Get-Date).Date - $parsed.Date).TotalDays
        $staleNotes += [pscustomobject]@{ Note = $rel; Field = $stampKey; Stamp = $parsed.ToString('yyyy-MM-dd'); AgeDays = $ageDays }
      }
    } else {
      $badDates += [pscustomobject]@{ Note = $rel; Field = $stampKey; Value = $fm[$stampKey] }
    }
  }
}

$sb = [System.Text.StringBuilder]::new()
[void]$sb.AppendLine("# Memory Staleness Report")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("- Vault: $root")
[void]$sb.AppendLine("- Source root: $srcRoot")
[void]$sb.AppendLine("- Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm')")
[void]$sb.AppendLine("- Notes scanned: $($mdFiles.Count)")
[void]$sb.AppendLine("- Freshness threshold: $MaxAgeDays day(s), so anything verified before $($cutoff.ToString('yyyy-MM-dd')) is stale")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("## Recorded source paths that no longer exist ($($deadPaths.Count))")
[void]$sb.AppendLine("")
if ($deadPaths.Count -gt 0) {
  foreach ($d in ($deadPaths | Sort-Object Note, Path)) { [void]$sb.AppendLine("- ``$($d.Note)`` -> ``$($d.Path)``") }
} else { [void]$sb.AppendLine("- none") }
[void]$sb.AppendLine("")
[void]$sb.AppendLine("## Notes past the freshness threshold ($($staleNotes.Count))")
[void]$sb.AppendLine("")
if ($staleNotes.Count -gt 0) {
  foreach ($s in ($staleNotes | Sort-Object -Property AgeDays -Descending)) {
    [void]$sb.AppendLine("- ``$($s.Note)`` $($s.Field)=$($s.Stamp), $($s.AgeDays) day(s) old")
  }
} else { [void]$sb.AppendLine("- none") }
[void]$sb.AppendLine("")
[void]$sb.AppendLine("## Source-derived notes missing a required field ($($missingField.Count))")
[void]$sb.AppendLine("")
if ($missingField.Count -gt 0) {
  foreach ($m in ($missingField | Sort-Object Note, Field)) {
    [void]$sb.AppendLine("- ``$($m.Note)`` (type: $($m.Type)) has no ``$($m.Field)``")
  }
} else { [void]$sb.AppendLine("- none") }
[void]$sb.AppendLine("")
[void]$sb.AppendLine("## Unparseable date values ($($badDates.Count))")
[void]$sb.AppendLine("")
if ($badDates.Count -gt 0) {
  foreach ($b in ($badDates | Sort-Object Note)) {
    [void]$sb.AppendLine("- ``$($b.Note)`` $($b.Field)=``$($b.Value)`` is not a date")
  }
} else { [void]$sb.AppendLine("- none") }

$text = $sb.ToString()
Write-Host $text

if (-not [string]::IsNullOrWhiteSpace($OutFile)) {
  Write-TextFileNoBom -Path $OutFile -Text $text
  Write-Host "Report saved: $OutFile"
}

$findings = $deadPaths.Count + $staleNotes.Count + $missingField.Count + $badDates.Count
if ($findings -gt 0) {
  Write-Host "staleness: $findings finding(s)"
  exit 1
}
Write-Host "staleness: clean"
exit 0
