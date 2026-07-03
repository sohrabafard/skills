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
    "inbox_capture"
  ),
  [switch]$Strict
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command bm -ErrorAction SilentlyContinue)) {
  throw "bm command not found in PATH."
}

function Invoke-Bm {
  param([string[]]$Args, [switch]$AllowFailure)
  Write-Host "bm $($Args -join ' ')"
  & bm @Args
  $code = $LASTEXITCODE
  if ($code -ne 0 -and -not $AllowFailure) {
    throw "bm command failed with exit code $code: bm $($Args -join ' ')"
  }
  return $code
}

Invoke-Bm @("status", "--project", $Project, "--wait", "--timeout", "60")
Invoke-Bm @("doctor")

foreach ($type in $SchemaTypes) {
  $args = @("schema", "validate", $type, "--project", $Project)
  if ($Strict) { $args += "--strict" }
  $code = Invoke-Bm -Args $args -AllowFailure
  if ($code -ne 0) {
    Write-Warning "Schema validation reported issues for type: $type"
    if ($Strict) { exit $code }
  }
}

Write-Host "Basic Memory health review completed for project: $Project"
