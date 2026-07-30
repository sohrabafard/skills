[CmdletBinding()]
param(
  [switch]$Quiet
)

# =============================================================================
# run-tests.ps1 - runs every shipped script's self-test.
#
# Exit codes:
#   0  every self-test passed
#   1  at least one self-test FAILED and none was BLOCKED
#   2  at least one self-test was BLOCKED (it could not run)
#
# BLOCKED takes precedence over FAILED, and that ordering is deliberate. "The
# checker could not run" and "the checker found a problem" call for different
# human actions: the first means the environment is wrong, the second means the
# vault is. Collapsing them into one code throws away the distinction the whole
# exit-code contract exists to create, and a gate would then treat a broken
# harness as ordinary findings.
#
# The two hook scripts are deliberately absent from this list. They are exempt
# from the 0/1/2 contract because the hook protocol reserves exit 2 to mean
# "block", so a self-test asserting the contract against them would assert the
# wrong thing. See references/checkers-and-hooks.md.
# =============================================================================

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

. (Join-Path (Join-Path (Split-Path -Parent $PSScriptRoot) 'scripts') '_common.ps1')

$targets = @(
  'alaa_obsidian_linkcheck.ps1',
  'alaa_memory_staleness.ps1',
  'alaa_memory_health.ps1',
  'alaa_memory_reindex.ps1',
  'alaa_memory_post_task.ps1'
)

$psExe = Get-HostPowerShellPath
if (-not $psExe) {
  Write-Host "BLOCKED: cannot locate the PowerShell executable to run the self-tests."
  exit 2
}

$scriptDir = Join-Path (Split-Path -Parent $PSScriptRoot) 'scripts'
$passed = 0
$failed = @()
$blocked = @()

foreach ($t in $targets) {
  $path = Join-Path $scriptDir $t
  if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
    Write-Host "BLOCKED  $t : script not found at $path"
    $blocked += $t
    continue
  }

  Write-Host ""
  Write-Host "=== $t --SelfTest ==="
  if ($Quiet) {
    & $psExe '-NoProfile' '-File' $path '-SelfTest' | Out-Null
  } else {
    & $psExe '-NoProfile' '-File' $path '-SelfTest'
  }
  $code = $LASTEXITCODE

  switch ($code) {
    0 { Write-Host "  -> PASSED";  $passed++ }
    1 { Write-Host "  -> FAILED";  $failed  += $t }
    2 { Write-Host "  -> BLOCKED"; $blocked += $t }
    default {
      Write-Host "  -> FAILED (unexpected exit code $code)"
      $failed += $t
    }
  }
}

Write-Host ""
Write-Host "-----------------------------------------------"
Write-Host ("self-tests: {0} passed, {1} failed, {2} blocked, {3} total" -f $passed, $failed.Count, $blocked.Count, $targets.Count)
if ($blocked.Count -gt 0) { Write-Host ("blocked: {0}" -f ($blocked -join ', ')) }
if ($failed.Count  -gt 0) { Write-Host ("failed:  {0}" -f ($failed  -join ', ')) }

if ($blocked.Count -gt 0) { exit 2 }
if ($failed.Count  -gt 0) { exit 1 }
exit 0
