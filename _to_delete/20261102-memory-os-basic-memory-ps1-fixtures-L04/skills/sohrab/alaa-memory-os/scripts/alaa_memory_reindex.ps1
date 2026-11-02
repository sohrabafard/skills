[CmdletBinding()]
param(
  [string]$Project = "alaa-memory",
  [string]$StoreExe = "bm",
  [switch]$Full,
  [switch]$SelfTest
)

# =============================================================================
# alaa_memory_reindex.ps1
#
# Rebuilds the store index, then reports health.
#
# Exit codes:
#   0  reindex and doctor both clean
#   1  the store ran and reported a problem
#   2  could not run: the store command is not on PATH
#
# `basic-memory sync` does not exist; reindex replaced it. See
# references/store-basic-memory.md for the pin and the re-derivation command.
#
# The previous version threw on every non-zero exit, so "store not installed"
# and "store reports a problem" both exited 1 and were indistinguishable.
# =============================================================================

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot '_common.ps1')

if ($SelfTest) {
  $result = Invoke-SelfTest -ScriptPath $PSCommandPath -Cases @(
    @{ Name = 'missing store binary is BLOCKED, not a finding'
       Expect = 2
       Args = @('-StoreExe', 'no-such-store-binary-exists-here') },
    @{ Name = 'clean store that prints output exits 0'
       Expect = 0
       Args = @('-StoreExe', '@fixture:stub-store/store_clean.ps1@') },
    @{ Name = 'store reporting a problem exits 1'
       Expect = 1
       Args = @('-StoreExe', '@fixture:stub-store/store_reports_problem.ps1@') }
  )
  exit $result
}

if (-not (Test-Tool -Name $StoreExe)) {
  Write-Host "BLOCKED: store command not found: $StoreExe"
  exit 2
}

$findings = @()

$reindexArgs = @("reindex", "-p", $Project)
if ($Full) { $reindexArgs += "--full" }
$reindexCode = Invoke-Store -Exe $StoreExe -StoreArgs $reindexArgs
if ($reindexCode -ne 0) { $findings += "reindex reported a problem (exit $reindexCode)" }

$doctorCode = Invoke-Store -Exe $StoreExe -StoreArgs @("doctor")
if ($doctorCode -ne 0) { $findings += "doctor reported a problem (exit $doctorCode)" }

Write-Host ""
if ($findings.Count -gt 0) {
  Write-Host "reindex: $($findings.Count) finding(s) for project '$Project'"
  foreach ($f in $findings) { Write-Host "- $f" }
  exit 1
}
Write-Host "reindex: clean for project '$Project'"
exit 0
