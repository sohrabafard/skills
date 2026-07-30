[CmdletBinding()]
param(
  [string]$Project = "alaa-memory",
  [string]$VaultPath = "",
  [string]$StoreExe = "bm",
  [string[]]$SchemaTypes = @(),
  [switch]$RunReindex,
  [switch]$SelfTest
)

# =============================================================================
# alaa_memory_post_task.ps1
#
# Post-task pass over the store: optional reindex, schema validation for the
# types the task touched, health check, then the vault's uncommitted-change
# summary so the human can see what the task wrote.
#
# Exit codes:
#   0  everything the store ran came back clean
#   1  the store ran and reported a problem
#   2  could not run: the store command is not on PATH, or the vault path did not
#      resolve to a directory
#
# Two defects this replaces:
#   - Schema validation failures only produced a warning and did not affect the
#     exit code, so a validation failure exited 0 and a gate read it as a pass.
#   - The vault path was a hardcoded machine-specific default, so on any other
#     machine the script failed in a way indistinguishable from a store problem.
#     Resolve-VaultRoot now tries the argument, then ALAA_MEMORY_VAULT, then the
#     documented default only if it actually exists.
# =============================================================================

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot '_common.ps1')

if ($SelfTest) {
  $result = Invoke-SelfTest -ScriptPath $PSCommandPath -Cases @(
    @{ Name = 'missing store binary is BLOCKED, not a finding'
       Expect = 2
       Args = @('-StoreExe', 'no-such-store-binary-exists-here', '-VaultPath', '@fixture:green-vault@') },
    @{ Name = 'unresolvable vault is BLOCKED, not a finding'
       Expect = 2
       Args = @('-StoreExe', '@fixture:stub-store/store_clean.ps1@', '-VaultPath', 'no-such-vault-path-exists-here') },
    @{ Name = 'clean store that prints output exits 0'
       Expect = 0
       Args = @('-StoreExe', '@fixture:stub-store/store_clean.ps1@', '-VaultPath', '@fixture:green-vault@', '-SchemaTypes', 'drift') },
    @{ Name = 'schema validation failure exits 1, not 0'
       Expect = 1
       Args = @('-StoreExe', '@fixture:stub-store/store_reports_problem.ps1@', '-VaultPath', '@fixture:green-vault@', '-SchemaTypes', 'drift') }
  )
  exit $result
}

if (-not (Test-Tool -Name $StoreExe)) {
  Write-Host "BLOCKED: store command not found: $StoreExe"
  exit 2
}

$vault = Resolve-VaultRoot -VaultPath $VaultPath
if (-not $vault.Ok) {
  Write-Host "BLOCKED: $($vault.Reason)"
  exit 2
}

$findings = @()

Push-Location -LiteralPath $vault.Path
try {
  if ($RunReindex) {
    $code = Invoke-Store -Exe $StoreExe -StoreArgs @("reindex", "-p", $Project)
    if ($code -ne 0) { $findings += "reindex reported a problem (exit $code)" }
  }

  # Report only: see references/store-basic-memory.md on --wait being a no-op.
  [void](Invoke-Store -Exe $StoreExe -StoreArgs @("status", "--project", $Project))

  foreach ($type in $SchemaTypes) {
    $code = Invoke-Store -Exe $StoreExe -StoreArgs @("schema", "validate", $type, "--project", $Project)
    if ($code -ne 0) { $findings += "schema validation reported issues for type '$type' (exit $code)" }
  }

  $doctorCode = Invoke-Store -Exe $StoreExe -StoreArgs @("doctor")
  if ($doctorCode -ne 0) { $findings += "doctor reported a problem (exit $doctorCode)" }

  # The vault's own change summary. Reported, never a finding: uncommitted notes
  # are the expected state at the end of a task, not a defect.
  #
  # Both conditions are required. Checking only that git exists made the script
  # run git inside a directory that is not a work tree, and git then printed its
  # entire usage text - the exact output-noise class /alaa-low-noise
  # ($alaa-low-noise) exists to prevent.
  if (-not (Test-Tool -Name 'git')) {
    Write-Host "git not on PATH; skipping the vault change summary."
  } else {
    $insideWorkTree = (& git rev-parse --is-inside-work-tree 2>$null)
    if ($LASTEXITCODE -eq 0 -and "$insideWorkTree".Trim() -eq 'true') {
      Write-Host ""
      Write-Host "Vault working-tree changes:"
      & git status --short
      & git diff --stat
    } else {
      Write-Host "Vault is not inside a git work tree; skipping the change summary."
    }
  }
}
finally {
  Pop-Location
}

Write-Host ""
if ($findings.Count -gt 0) {
  Write-Host "post-task: $($findings.Count) finding(s) for project '$Project'"
  foreach ($f in $findings) { Write-Host "- $f" }
  exit 1
}
Write-Host "post-task: clean for project '$Project'"
exit 0
