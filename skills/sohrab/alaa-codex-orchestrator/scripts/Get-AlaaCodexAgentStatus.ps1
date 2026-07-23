[CmdletBinding()]
param(
    [string]$SourceDirectory = (Join-Path (Split-Path -Parent $PSScriptRoot) "agents"),
    [string]$TargetDirectory = (Join-Path $HOME ".codex\agents")
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$source = (Resolve-Path -LiteralPath $SourceDirectory).Path
$rows = foreach ($sourceFile in (Get-ChildItem -LiteralPath $source -File -Filter "*.toml" | Sort-Object Name)) {
    $destination = Join-Path $TargetDirectory $sourceFile.Name
    $sourceHash = (Get-FileHash -LiteralPath $sourceFile.FullName -Algorithm SHA256).Hash
    if (-not (Test-Path -LiteralPath $destination)) {
        [pscustomobject]@{ Agent = $sourceFile.BaseName; Status = "Missing"; Path = $destination }
        continue
    }
    $targetHash = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash
    [pscustomobject]@{
        Agent = $sourceFile.BaseName
        Status = if ($sourceHash -eq $targetHash) { "Current" } else { "Different" }
        Path = $destination
    }
}

$rows | Format-Table -AutoSize
if ($rows.Status -contains "Missing" -or $rows.Status -contains "Different") { exit 1 }
