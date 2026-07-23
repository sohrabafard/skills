[CmdletBinding()]
param(
    [string]$SourceDirectory = (Join-Path (Split-Path -Parent $PSScriptRoot) "agents"),
    [string]$TargetDirectory = (Join-Path $HOME ".codex\agents")
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-FileHashHex {
    param([Parameter(Mandatory)][string]$Path)
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

$source = (Resolve-Path -LiteralPath $SourceDirectory).Path
New-Item -ItemType Directory -Path $TargetDirectory -Force | Out-Null
$target = (Resolve-Path -LiteralPath $TargetDirectory).Path

$agentFiles = @(Get-ChildItem -LiteralPath $source -File -Filter "*.toml" | Sort-Object Name)
if ($agentFiles.Count -eq 0) {
    throw "No agent TOML files found in: $source"
}

$lockPath = Join-Path $target ".alaa-codex-orchestrator.install.lock"
$lockStream = $null
$changed = 0
$unchanged = 0
$backupDirectory = $null
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss-fff"

try {
    $lockStream = [System.IO.File]::Open(
        $lockPath,
        [System.IO.FileMode]::OpenOrCreate,
        [System.IO.FileAccess]::ReadWrite,
        [System.IO.FileShare]::None
    )

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
}
finally {
    if ($lockStream) { $lockStream.Dispose() }
    Remove-Item -LiteralPath $lockPath -Force -ErrorAction SilentlyContinue
}

$result = [ordered]@{
    Status = "OK"
    InstalledOrUpdated = $changed
    AlreadyCurrent = $unchanged
    TargetDirectory = $target
    BackupDirectory = $backupDirectory
}
$result | ConvertTo-Json -Compress
