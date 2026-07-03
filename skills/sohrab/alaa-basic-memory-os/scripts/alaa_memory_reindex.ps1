[CmdletBinding()]
param(
  [string]$Project = "alaa-memory"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command bm -ErrorAction SilentlyContinue)) {
  throw "bm command not found in PATH."
}

& bm reindex -p $Project
if ($LASTEXITCODE -ne 0) { throw "bm reindex failed" }

& bm status --project $Project --wait --timeout 60
if ($LASTEXITCODE -ne 0) { throw "bm status failed" }

& bm doctor
if ($LASTEXITCODE -ne 0) { throw "bm doctor failed" }

Write-Host "Reindex and health check completed for project: $Project"
