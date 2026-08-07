[CmdletBinding()]
param(
    [string]$TargetSkillDirectory = (Join-Path $HOME ".codex\skills\alaa-codex-orchestrator")
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

# The previous directory is moved aside only so a failed swap can be undone; it is removed on
# success, so no copy of a prior version is retained.
$replacedDirectory = $null
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
            throw "Python 3 is required to validate the staged skill and its agent grants"
        }
    }

    if (Test-Path -LiteralPath $targetFull) {
        $replacedDirectory = "$targetFull.replaced.$([Guid]::NewGuid().ToString('N'))"
        Move-Item -LiteralPath $targetFull -Destination $replacedDirectory
    }
    Move-Item -LiteralPath $stagingDirectory -Destination $targetFull
    & (Join-Path $targetFull "scripts\Install-AlaaCodexAgents.ps1")

    [ordered]@{
        Status = "OK"
        SkillDirectory = $targetFull
    } | ConvertTo-Json -Compress
}
catch {
    if ((-not (Test-Path -LiteralPath $targetFull)) -and $replacedDirectory -and (Test-Path -LiteralPath $replacedDirectory)) {
        Move-Item -LiteralPath $replacedDirectory -Destination $targetFull -ErrorAction SilentlyContinue
    }
    throw
}
finally {
    if (Test-Path -LiteralPath $stagingDirectory) {
        Remove-Item -LiteralPath $stagingDirectory -Recurse -Force -ErrorAction SilentlyContinue
    }
    if ($replacedDirectory -and (Test-Path -LiteralPath $replacedDirectory)) {
        Remove-Item -LiteralPath $replacedDirectory -Recurse -Force -ErrorAction SilentlyContinue
    }
}
