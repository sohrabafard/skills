[CmdletBinding()]
param(
  [string]$DriftDir = "docs/drift",
  [string]$RepoRoot = ""
)

# =============================================================================
# session_start_context.ps1 - Claude Code SessionStart hook.
#
# Exempt from the checker exit contract. SessionStart is context-only and cannot
# block. This hook always exits 0. See references/checkers-and-hooks.md.
#
# Stdout is added to the session context - SessionStart is one of the few events
# where that happens rather than going to the debug log. The event cannot block.
# Keep it fast: it runs on every session.
#
# It reads the drift registry from the REPOSITORY, not from the memory store.
# That follows the registry's location (see references/drift-management.md) and
# has two side effects worth naming: it is store-agnostic, and it costs a
# directory listing instead of a store query, which matters on an event that must
# stay fast.
# =============================================================================

# Deliberately permissive. A hook that throws is worse than one that degrades,
# and every failure below is recoverable by saying less.
$ErrorActionPreference = "SilentlyContinue"

function Get-OpenDriftCount {
  param([string]$Dir)
  if ([string]::IsNullOrWhiteSpace($Dir)) { return -1 }
  try {
    if (-not (Test-Path -LiteralPath $Dir -PathType Container -ErrorAction Stop)) { return -1 }
    $open = 0
    foreach ($f in (Get-ChildItem -LiteralPath $Dir -Recurse -Filter *.md -File -ErrorAction Stop)) {
      $raw = Get-Content -LiteralPath $f.FullName -Raw -ErrorAction Stop
      if ($null -eq $raw) {
        if ($f.Length -eq 0) { continue }
        return -1
      }
      # A partial or unreadable scan cannot establish a zero count.
      if ($raw -match '(?m)^drift_status:\s*(open|analyzed|decided|fixing)\s*$') { $open++ }
    }
    return $open
  } catch {
    return -1
  }
}

try {
  $root = $RepoRoot
  if ([string]::IsNullOrWhiteSpace($root)) { $root = (Get-Location).Path }
  $driftPath = Join-Path $root $DriftDir -ErrorAction Stop
  $openCount = Get-OpenDriftCount -Dir $driftPath
} catch {
  $openCount = -1
}

# The condition tests results, not command success. The previous version set the
# warning whenever the query merely succeeded, so a search returning zero drift
# records still announced that open drift might exist - which trains the reader
# to ignore the line.
$driftLine = "- Repository drift registry observation unavailable."
if ($openCount -gt 0) {
  $driftLine = "- $openCount unresolved repository drift record(s). When an affected contract is in scope, read /alaa-memory-os references/drift-management.md and the records."
} elseif ($openCount -eq 0) {
  $driftLine = "- No unresolved records observed in the repository drift registry."
}

@"
Alaa conditional owners:
- For recall, capability ownership, durable writes or source disagreement, load /alaa-memory-os and its selected adapter.
- For active task continuity or compaction, load /alaa-workflow.
$driftLine
"@

exit 0
