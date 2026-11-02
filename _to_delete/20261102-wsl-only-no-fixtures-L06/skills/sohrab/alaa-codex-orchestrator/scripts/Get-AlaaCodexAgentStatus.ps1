[CmdletBinding()]
param(
    [string]$SourceDirectory = (Join-Path (Split-Path -Parent $PSScriptRoot) "agents"),
    [string]$TargetDirectory = (Join-Path $HOME ".codex\agents")
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$source = (Resolve-Path -LiteralPath $SourceDirectory).Path
$grantChecker = Join-Path (Split-Path -Parent $source) "scripts\check_agent_grants.py"
$python = Get-Command python.exe -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command python -ErrorAction SilentlyContinue }
$pythonPrefix = @()
if (-not $python) {
    $python = Get-Command py.exe -ErrorAction SilentlyContinue
    if (-not $python) { $python = Get-Command py -ErrorAction SilentlyContinue }
    if (-not $python) { throw "Python 3 is required to resolve live agent grants" }
    $pythonPrefix = @("-3")
}

$materializedDirectory = Join-Path ([IO.Path]::GetTempPath()) "alaa-codex-agent-status.$([Guid]::NewGuid().ToString('N'))"
try {
    & $python.Source @pythonPrefix $grantChecker --materialize $source $materializedDirectory
    if ($LASTEXITCODE -ne 0) {
        throw "Agent grant materialization failed with exit code $LASTEXITCODE"
    }

    $rows = foreach ($sourceFile in (Get-ChildItem -LiteralPath $materializedDirectory -File -Filter "*.toml" | Sort-Object Name)) {
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
}
finally {
    if (Test-Path -LiteralPath $materializedDirectory) {
        Remove-Item -LiteralPath $materializedDirectory -Recurse -Force -ErrorAction SilentlyContinue
    }
}

$rows | Format-Table -AutoSize
if ($rows.Status -contains "Missing" -or $rows.Status -contains "Different") { exit 1 }
