[CmdletBinding()]
param(
    [string]$TargetSkillDirectory = (Join-Path $HOME ".agents\skills\alaa-codex-orchestrator")
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$sourceSkillDirectory = (Resolve-Path -LiteralPath (Split-Path -Parent $PSScriptRoot)).Path
$targetParent = Split-Path -Parent $TargetSkillDirectory
New-Item -ItemType Directory -Path $targetParent -Force | Out-Null
$targetFull = [System.IO.Path]::GetFullPath($TargetSkillDirectory)

$separatorChars = [char[]]@([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
$normalizedSource = $sourceSkillDirectory.TrimEnd($separatorChars)
$normalizedTarget = $targetFull.TrimEnd($separatorChars)
if ($normalizedSource -ieq $normalizedTarget) {
    & (Join-Path $sourceSkillDirectory "scripts\Install-AlaaCodexAgents.ps1")
    return
}

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss-fff"
$backupDirectory = $null
$stagingDirectory = "$targetFull.tmp.$([Guid]::NewGuid().ToString('N'))"

try {
    Copy-Item -LiteralPath $sourceSkillDirectory -Destination $stagingDirectory -Recurse -Force
    if (-not (Test-Path -LiteralPath (Join-Path $stagingDirectory "SKILL.md"))) {
        throw "Staged skill is missing SKILL.md"
    }
    $validator = Join-Path $stagingDirectory "scripts\validate_pack.py"
    $python = Get-Command python.exe -ErrorAction SilentlyContinue
    if (-not $python) { $python = Get-Command python -ErrorAction SilentlyContinue }
    if ($python) {
        & $python.Source $validator
        if ($LASTEXITCODE -ne 0) { throw "Skill validation failed" }
    }
    else {
        $pyLauncher = Get-Command py.exe -ErrorAction SilentlyContinue
        if (-not $pyLauncher) { $pyLauncher = Get-Command py -ErrorAction SilentlyContinue }
        if ($pyLauncher) {
            & $pyLauncher.Source -3 $validator
            if ($LASTEXITCODE -ne 0) { throw "Skill validation failed" }
        }
        else {
            $tomlCount = @(Get-ChildItem -LiteralPath (Join-Path $stagingDirectory "agents") -Filter "*.toml" -File).Count
            if ($tomlCount -ne 16) { throw "Expected 16 agent TOMLs; found $tomlCount" }
        }
    }

    if (Test-Path -LiteralPath $targetFull) {
        $backupRoot = Join-Path $targetParent ".alaa-codex-orchestrator-backups"
        New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null
        $backupDirectory = Join-Path $backupRoot $timestamp
        Move-Item -LiteralPath $targetFull -Destination $backupDirectory
    }
    Move-Item -LiteralPath $stagingDirectory -Destination $targetFull
    & (Join-Path $targetFull "scripts\Install-AlaaCodexAgents.ps1")

    [ordered]@{
        Status = "OK"
        SkillDirectory = $targetFull
        PreviousSkillBackup = $backupDirectory
    } | ConvertTo-Json -Compress
}
catch {
    if ((-not (Test-Path -LiteralPath $targetFull)) -and $backupDirectory -and (Test-Path -LiteralPath $backupDirectory)) {
        Move-Item -LiteralPath $backupDirectory -Destination $targetFull -ErrorAction SilentlyContinue
    }
    throw
}
finally {
    if (Test-Path -LiteralPath $stagingDirectory) {
        Remove-Item -LiteralPath $stagingDirectory -Recurse -Force -ErrorAction SilentlyContinue
    }
}
