[CmdletBinding()]
param(
  [string]$Project = "alaa-memory",
  [string]$StoreExe = "bm",
  [string[]]$SchemaTypes = @(
    "architecture",
    "contract",
    "service_ownership",
    "operations",
    "lesson_collection",
    "work_pattern",
    "project_index",
    "project_state",
    "handoff",
    "research",
    "inbox_capture",
    "drift"
  ),
  [switch]$IncludeOrphans,
  [switch]$Strict,
  [switch]$SelfTest
)

# =============================================================================
# alaa_memory_health.ps1
#
# Store-side health review for a file-backed memory store.
#
# Exit codes:
#   0  every check the store ran came back clean
#   1  the store ran and reported a problem
#   2  could not run: the store command is not on PATH
#
# The 1-versus-2 split is the point. The previous version threw on a missing
# store binary, which exits 1, so a gate could not tell "no tool installed" from
# "validation failed" - and a missing tool then read as a real failure while a
# real failure could read as a pass.
#
# -Strict passes --strict to the store's own schema validation. It does NOT
# change the exit contract: findings are always 1. The previous version used it
# to `exit $code` where $code was an array, which exits 0, so the mode named
# "Strict" turned a validation failure into a pass.
#
# `bm status` is run for its report only and never affects the exit code. On the
# store's development branch `--wait` is a documented compatibility no-op, so
# gating on it asserts nothing. See references/store-basic-memory.md.
# =============================================================================

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot '_common.ps1')

if ($SelfTest) {
  $result = Invoke-SelfTest -ScriptPath $PSCommandPath -Cases @(
    @{ Name = 'missing store binary is BLOCKED, not a finding'
       Expect = 2
       Args = @('-StoreExe', 'no-such-store-binary-exists-here') },
    @{ Name = 'clean store that prints output exits 0 (array-capture regression)'
       Expect = 0
       Args = @('-StoreExe', '@fixture:stub-store/store_clean.ps1@', '-SchemaTypes', 'drift') },
    @{ Name = 'store reporting a problem exits 1, not its raw code'
       Expect = 1
       Args = @('-StoreExe', '@fixture:stub-store/store_reports_problem.ps1@', '-SchemaTypes', 'drift') },
    @{ Name = '-Strict on a reported problem exits 1, not 0'
       Expect = 1
       Args = @('-StoreExe', '@fixture:stub-store/store_reports_problem.ps1@', '-SchemaTypes', 'drift', '-Strict') }
  )
  exit $result
}

if (-not (Test-Tool -Name $StoreExe)) {
  Write-Host "BLOCKED: store command not found: $StoreExe"
  exit 2
}

$findings = @()

# Report only. Never fatal, for the reason in the header.
[void](Invoke-Store -Exe $StoreExe -StoreArgs @("status", "--project", $Project))

$doctorCode = Invoke-Store -Exe $StoreExe -StoreArgs @("doctor")
if ($doctorCode -ne 0) { $findings += "doctor reported a problem (exit $doctorCode)" }

foreach ($type in $SchemaTypes) {
  $validateArgs = @("schema", "validate", $type, "--project", $Project)
  if ($Strict) { $validateArgs += "--strict" }
  $code = Invoke-Store -Exe $StoreExe -StoreArgs $validateArgs
  if ($code -ne 0) { $findings += "schema validation reported issues for type '$type' (exit $code)" }
}

if ($IncludeOrphans) {
  Write-Host "Notes with no incoming or outgoing relations:"
  [void](Invoke-Store -Exe $StoreExe -StoreArgs @("orphans", "--project", $Project))
}

Write-Host "Open drift pointers in the store, if any are retained:"
[void](Invoke-Store -Exe $StoreExe -StoreArgs @("tool", "search-notes", "--type", "drift", "--project", $Project))

Write-Host ""
if ($findings.Count -gt 0) {
  Write-Host "health: $($findings.Count) finding(s) for project '$Project'"
  foreach ($f in $findings) { Write-Host "- $f" }
  exit 1
}
Write-Host "health: clean for project '$Project'"
exit 0
