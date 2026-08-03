[CmdletBinding()]
param(
    [string]$SourceDirectory,
    [string]$TargetDirectory = (Join-Path $HOME ".codex\agents")
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not $SourceDirectory) {
    $scriptRoot = $PSScriptRoot
    if (-not $scriptRoot -and $PSCommandPath) { $scriptRoot = Split-Path -Parent $PSCommandPath }
    if (-not $scriptRoot -and $MyInvocation.MyCommand.Path) { $scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path }
    if (-not $scriptRoot) {
        throw "Cannot resolve the script location in this invocation style; pass -SourceDirectory <skill-root>\agents explicitly."
    }
    $SourceDirectory = Join-Path (Split-Path -Parent $scriptRoot) "agents"
}

function Get-FileHashHex {
    param([Parameter(Mandatory)][string]$Path)
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

$source = (Resolve-Path -LiteralPath $SourceDirectory).Path
$agentFiles = @(Get-ChildItem -LiteralPath $source -File -Filter "*.toml" | Sort-Object Name)
if ($agentFiles.Count -eq 0) {
    throw "No agent TOML files found in: $source"
}

$grantChecker = Join-Path (Split-Path -Parent $source) "scripts\check_agent_grants.py"
if (-not (Test-Path -LiteralPath $grantChecker)) {
    throw "Agent grant checker not found: $grantChecker"
}
$python = Get-Command python.exe -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command python -ErrorAction SilentlyContinue }
$pythonPrefix = @()
if (-not $python) {
    $python = Get-Command py.exe -ErrorAction SilentlyContinue
    if (-not $python) { $python = Get-Command py -ErrorAction SilentlyContinue }
    if (-not $python) {
        throw "Python 3 is required to validate agent grants before installation"
    }
    $pythonPrefix = @("-3")
}

New-Item -ItemType Directory -Path $TargetDirectory -Force | Out-Null
$target = (Resolve-Path -LiteralPath $TargetDirectory).Path

$lockPath = Join-Path $target ".alaa-codex-orchestrator.install.lock"
$lockStream = $null
$changed = 0
$unchanged = 0
$backupDirectory = $null
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss-fff"
$materializedDirectory = Join-Path $target ".alaa-codex-orchestrator.materialized.$([Guid]::NewGuid().ToString('N'))"

try {
    $lockStream = [System.IO.File]::Open(
        $lockPath,
        [System.IO.FileMode]::OpenOrCreate,
        [System.IO.FileAccess]::ReadWrite,
        [System.IO.FileShare]::None
    )

    & $python.Source @pythonPrefix $grantChecker --materialize $source $materializedDirectory
    if ($LASTEXITCODE -ne 0) {
        throw "Agent grant materialization failed with exit code $LASTEXITCODE"
    }
    $agentFiles = @(Get-ChildItem -LiteralPath $materializedDirectory -File -Filter "*.toml" | Sort-Object Name)

    foreach ($sourceFile in $agentFiles) {
        $destination = Join-Path $target $sourceFile.Name
        $sourceHash = Get-FileHashHex -Path $sourceFile.FullName

        if (Test-Path -LiteralPath $destination) {
            $destinationHash = Get-FileHashHex -Path $destination
            if ($sourceHash -eq $destinationHash) {
                $unchanged++
                continue
            }

            if (-not $backupDirectory) {
                $backupDirectory = Join-Path $target ".alaa-codex-orchestrator-backups\$timestamp"
                New-Item -ItemType Directory -Path $backupDirectory -Force | Out-Null
            }
            Copy-Item -LiteralPath $destination -Destination (Join-Path $backupDirectory $sourceFile.Name) -Force
        }

        $tempPath = "$destination.tmp.$([Guid]::NewGuid().ToString('N'))"
        try {
            Copy-Item -LiteralPath $sourceFile.FullName -Destination $tempPath -Force
            if ((Get-FileHashHex -Path $tempPath) -ne $sourceHash) {
                throw "Hash mismatch while staging $($sourceFile.Name)"
            }

            if (Test-Path -LiteralPath $destination) {
                [System.IO.File]::Replace($tempPath, $destination, $null, $true)
            }
            else {
                [System.IO.File]::Move($tempPath, $destination)
            }

            if ((Get-FileHashHex -Path $destination) -ne $sourceHash) {
                throw "Hash mismatch after installing $($sourceFile.Name)"
            }
            $changed++
        }
        finally {
            if (Test-Path -LiteralPath $tempPath) {
                Remove-Item -LiteralPath $tempPath -Force -ErrorAction SilentlyContinue
            }
        }
    }

    Copy-Item -LiteralPath (Join-Path $materializedDirectory ".alaa-codex-orchestrator.mcp-inventory") `
        -Destination (Join-Path $target ".alaa-codex-orchestrator.mcp-inventory") -Force
}
finally {
    if ($lockStream) { $lockStream.Dispose() }
    Remove-Item -LiteralPath $lockPath -Force -ErrorAction SilentlyContinue
    if (Test-Path -LiteralPath $materializedDirectory) {
        Remove-Item -LiteralPath $materializedDirectory -Recurse -Force -ErrorAction SilentlyContinue
    }
}

$versionFile = Join-Path (Split-Path -Parent $source) "VERSION"
if (Test-Path -LiteralPath $versionFile) {
    Copy-Item -LiteralPath $versionFile -Destination (Join-Path $target ".alaa-codex-orchestrator.version") -Force
}

$result = [ordered]@{
    Status = "OK"
    InstalledOrUpdated = $changed
    AlreadyCurrent = $unchanged
    TargetDirectory = $target
    BackupDirectory = $backupDirectory
}
$result | ConvertTo-Json -Compress
