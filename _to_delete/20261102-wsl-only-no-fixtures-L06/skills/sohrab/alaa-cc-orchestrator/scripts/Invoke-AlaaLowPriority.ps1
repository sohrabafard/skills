[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$FilePath,
    [string[]]$ArgumentList = @(),
    [ValidateSet("Idle", "BelowNormal", "Normal")][string]$Priority = "BelowNormal",
    [ValidateRange(0, 63)][int]$CpuCount = 0,
    [string]$WorkingDirectory = (Get-Location).Path,
    [hashtable]$Environment = @{},
    [ValidateRange(0, 2147483647)][int]$TimeoutSeconds = 0,
    [string]$StdoutPath,
    [string]$StderrPath
)

# Compatibility entrypoint; preserve the canonical runner's arguments and status.
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$runner = Join-Path $PSScriptRoot "../../alaa-testing-strategy/scripts/Invoke-AlaaLowPriority.ps1"
if (-not (Test-Path -LiteralPath $runner -PathType Leaf)) {
    throw "Missing canonical testing-strategy runner: $runner. Provide a compatible alaa-testing-strategy package; no automatic installation."
}
& $runner @PSBoundParameters
exit $LASTEXITCODE
