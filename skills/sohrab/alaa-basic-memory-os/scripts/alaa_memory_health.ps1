[CmdletBinding()]
param(
  [string]$Project = "alaa-memory",
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
  [switch]$Strict
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command bm -ErrorAction SilentlyContinue)) {
  throw "bm command not found in PATH."
}

function Invoke-Bm {
  param(
    [string[]]$BmArgs,
    [switch]$AllowFailure
  )
  Write-Host "bm $($BmArgs -join ' ')"
  & bm @BmArgs
  $code = $LASTEXITCODE
  if ($code -ne 0 -and -not $AllowFailure) {
    throw "bm command failed with exit code ${code}: bm $($BmArgs -join ' ')"
  }
  return $code
}

Invoke-Bm -BmArgs @("status", "--project", $Project, "--wait", "--timeout", "60") | Out-Null
Invoke-Bm -BmArgs @("doctor") | Out-Null

foreach ($type in $SchemaTypes) {
  $validateArgs = @("schema", "validate", $type, "--project", $Project)
  if ($Strict) { $validateArgs += "--strict" }
  $code = Invoke-Bm -BmArgs $validateArgs -AllowFailure
  if ($code -ne 0) {
    Write-Warning "Schema validation reported issues for type: $type"
    if ($Strict) { exit $code }
  }
}

if ($IncludeOrphans) {
  Write-Host ""
  Write-Host "Orphan notes (no incoming/outgoing relations):"
  Invoke-Bm -BmArgs @("orphans", "--project", $Project) -AllowFailure | Out-Null
}

Write-Host ""
Write-Host "Open drift notes (analyze with prompt 14, fix with prompt 15):"
Invoke-Bm -BmArgs @("tool", "search-notes", "--type", "drift", "--project", $Project) -AllowFailure | Out-Null

Write-Host ""
Write-Host "Basic Memory health review completed for project: $Project"
