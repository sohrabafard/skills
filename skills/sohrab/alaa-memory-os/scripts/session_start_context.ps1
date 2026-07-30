[CmdletBinding()]
param(
  [string]$DriftDir = "docs/drift",
  [string]$RepoRoot = ""
)

# =============================================================================
# session_start_context.ps1 - Claude Code SessionStart hook.
#
# EXEMPT from the 0/1/2 checker contract, and converting it would change its
# behaviour: the hook protocol reserves exit 2 to mean "block" and treats exit 1
# as a non-blocking error surfaced to the user as a hook error notice. This hook
# always exits 0. See references/checkers-and-hooks.md.
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
  if (-not (Test-Path -LiteralPath $Dir -PathType Container)) { return -1 }
  $open = 0
  foreach ($f in (Get-ChildItem -LiteralPath $Dir -Recurse -Filter *.md -File)) {
    $raw = Get-Content -LiteralPath $f.FullName -Raw
    if ($null -eq $raw) { continue }
    # Counts records still awaiting a human decision. A record that reached
    # resolved or archived is history and must not be announced every session.
    if ($raw -match '(?m)^drift_status:\s*(open|analyzed|decided|fixing)\s*$') { $open++ }
  }
  return $open
}

$root = $RepoRoot
if ([string]::IsNullOrWhiteSpace($root)) { $root = (Get-Location).Path }
$driftPath = Join-Path $root $DriftDir

$openCount = Get-OpenDriftCount -Dir $driftPath

# The condition tests results, not command success. The previous version set the
# warning whenever the query merely succeeded, so a search returning zero drift
# records still announced that open drift might exist - which trains the reader
# to ignore the line.
$driftLine = ""
if ($openCount -gt 0) {
  $driftLine = "- $openCount unresolved drift record(s) in $DriftDir. If your task touches an affected contract, read them before planning."
} elseif ($openCount -eq 0) {
  $driftLine = "- No unresolved drift records in $DriftDir."
}

@"
Alaa memory governance (auto-injected):
- Repository code and docs are the source of truth; memory is a map, not proof.
- Before non-trivial, cross-service, contract-sensitive or continuation work: search memory first, then verify every recalled claim against repository files.
- Recall fails open on a five-second budget. If memory is unavailable, proceed from repository truth and say so in the final report.
- Never store secrets, raw logs, transcripts, whole documents, or active /alaa-workflow (`$alaa-workflow`) checklists.
- Contract facts must be source-backed. A proposed value needs a [proposal], [draft_contract] or [decision_needed] label.
- If two sources of truth disagree, record a drift record instead of silently picking one. Drift recording fails closed.
- Commands, version pins and store specifics live in /alaa-memory-os (`$alaa-memory-os`); this reminder does not restate them.
$driftLine
"@

exit 0
