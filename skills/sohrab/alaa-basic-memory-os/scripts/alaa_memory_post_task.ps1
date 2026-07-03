[CmdletBinding()]
param(
  [string]$Project = "alaa-memory",
  [string]$AgentMemoryPath = "D:\Sohrab\Project\agent-memory",
  [string[]]$SchemaTypes = @(),
  [switch]$RunReindex
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $AgentMemoryPath)) {
  throw "Agent memory path not found: $AgentMemoryPath"
}

Push-Location $AgentMemoryPath
try {
  if ($RunReindex) {
    & bm reindex -p $Project
    if ($LASTEXITCODE -ne 0) { throw "bm reindex failed" }
  }

  & bm status --project $Project --wait --timeout 60
  if ($LASTEXITCODE -ne 0) { throw "bm status failed" }

  foreach ($type in $SchemaTypes) {
    & bm schema validate $type --project $Project
    if ($LASTEXITCODE -ne 0) { Write-Warning "Schema validation reported issues for $type" }
  }

  & bm doctor
  if ($LASTEXITCODE -ne 0) { throw "bm doctor failed" }

  if (Get-Command git -ErrorAction SilentlyContinue) {
    git status --short
    git diff --stat
  }
}
finally {
  Pop-Location
}
