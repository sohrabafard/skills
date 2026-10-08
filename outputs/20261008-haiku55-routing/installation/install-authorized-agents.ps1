[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$RepoRoot,
    [Parameter(Mandatory)][string]$ClaudeTarget,
    [Parameter(Mandatory)][string]$CodexTarget,
    [Parameter(Mandatory)][string]$BackupDirectory
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$taskRoot = (Resolve-Path -LiteralPath $RepoRoot).Path
$taskEvidence = $PSScriptRoot
$taskCcSource = Join-Path $taskRoot 'skills/sohrab/alaa-cc-orchestrator/agents'
$taskCodexSource = Join-Path $taskRoot 'skills/sohrab/alaa-codex-orchestrator/agents'

function Hash-File([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Assert-OrdinaryDirectory([string]$Path) {
    $item = Get-Item -LiteralPath $Path -Force
    if (-not $item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
        throw 'Authorized agent target must be an ordinary directory'
    }
    return (Resolve-Path -LiteralPath $Path).Path
}
function Assert-Contained([string]$Path, [string]$Root) {
    $absolute = [IO.Path]::GetFullPath($Path)
    $prefix = [IO.Path]::GetFullPath($Root).TrimEnd('\','/') + [IO.Path]::DirectorySeparatorChar
    if (-not $absolute.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw 'Computed agent or staging path escaped its authorized directory'
    }
}
function File-Inventory([string]$Directory) {
    $records = @{}
    foreach ($file in Get-ChildItem -LiteralPath $Directory -File -Force) {
        $records[$file.Name] = Hash-File $file.FullName
    }
    return $records
}

$taskClaude = Assert-OrdinaryDirectory $ClaudeTarget
$taskCodex = Assert-OrdinaryDirectory $CodexTarget
$taskExpectedClaude = [IO.Path]::GetFullPath((Join-Path $env:USERPROFILE '.claude/agents'))
$taskExpectedCodex = [IO.Path]::GetFullPath((Join-Path $env:USERPROFILE '.codex/agents'))
if ($taskClaude -ine $taskExpectedClaude -or $taskCodex -ine $taskExpectedCodex) {
    throw 'Targets differ from the explicitly authorized user-level agent directories'
}
$taskCcFiles = @(Get-ChildItem -LiteralPath $taskCcSource -File -Filter '*.md' | Sort-Object Name)
$taskCodexFiles = @(Get-ChildItem -LiteralPath $taskCodexSource -File -Filter '*.toml' | Sort-Object Name)
if ($taskCcFiles.Count -ne 28 -or $taskCodexFiles.Count -ne 27) { throw 'Unexpected source roster' }
$taskCcBefore = File-Inventory $taskClaude
$taskCodexBefore = File-Inventory $taskCodex
$taskConfigPaths = @((Join-Path $env:USERPROFILE '.codex/config.toml'), (Join-Path $env:USERPROFILE '.claude/settings.json'))
$taskConfigHashes = @{}
foreach ($path in $taskConfigPaths) { if (Test-Path -LiteralPath $path -PathType Leaf) { $taskConfigHashes[$path] = Hash-File $path } }

# Backup only source-managed names and documented installed sentinels.
$taskBackupBase = 'V:\cache\alaa-agent-install'
Assert-Contained $BackupDirectory $taskBackupBase
if (Test-Path -LiteralPath $BackupDirectory) { throw 'Backup directory must be new' }
New-Item -ItemType Directory -Path $BackupDirectory | Out-Null
$taskBackup = (Resolve-Path -LiteralPath $BackupDirectory).Path
$taskBackupRecords = [Collections.Generic.List[object]]::new()
$taskRuntimes = @(
    @{Name='claude'; Target=$taskClaude; Files=$taskCcFiles; Extra=@()},
    @{Name='codex'; Target=$taskCodex; Files=$taskCodexFiles; Extra=@('.alaa-codex-orchestrator.version','.alaa-codex-orchestrator.mcp-inventory')}
)
foreach ($runtime in $taskRuntimes) {
    $backupRuntime = Join-Path $taskBackup $runtime.Name
    New-Item -ItemType Directory -Path $backupRuntime | Out-Null
    $names = @($runtime.Files | ForEach-Object Name) + @($runtime.Extra)
    foreach ($name in $names) {
        $installed = Join-Path $runtime.Target $name
        Assert-Contained $installed $runtime.Target
        if (-not (Test-Path -LiteralPath $installed)) { continue }
        $item = Get-Item -LiteralPath $installed -Force
        if ($item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'Managed target is not an ordinary file' }
        $backupFile = Join-Path $backupRuntime $name
        Assert-Contained $backupFile $taskBackup
        $beforeHash = Hash-File $installed
        Copy-Item -LiteralPath $installed -Destination $backupFile
        if ((Hash-File $backupFile) -ne $beforeHash) { throw 'Backup hash verification failed' }
        $taskBackupRecords.Add([ordered]@{runtime=$runtime.Name; name=$name; sha256=$beforeHash; backup=(Join-Path $runtime.Name $name)})
    }
}
$taskBackupRecords | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $taskBackup 'manifest.json') -Encoding utf8

# The approved native installer creates only GUID-named children of this verified target.
# The target is ordinary; generated leaf names contain no separators or caller input.
Assert-Contained (Join-Path $taskCodex '.alaa-codex-orchestrator.materialized.containment-check') $taskCodex
Assert-Contained (Join-Path $taskCodex 'alaa-implementer.toml.tmp.containment-check') $taskCodex

$taskCcValidation = & python -B (Join-Path $taskRoot 'skills/sohrab/alaa-cc-orchestrator/scripts/validate_pack.py') 2>&1
$taskCcExit = $LASTEXITCODE
$taskCcValidation | Set-Content -LiteralPath (Join-Path $taskEvidence 'claude-preflight.log') -Encoding utf8
if ($taskCcExit -ne 0) { throw "Claude source preflight failed with exit $taskCcExit; installed targets untouched" }

foreach ($source in $taskCcFiles) {
    $destination = Join-Path $taskClaude $source.Name
    Assert-Contained $destination $taskClaude
    Copy-Item -LiteralPath $source.FullName -Destination $destination -Force
    if ((Hash-File $destination) -ne (Hash-File $source.FullName)) { throw 'Claude installed hash differs from source' }
}

$taskInstaller = Join-Path $taskRoot 'skills/sohrab/alaa-codex-orchestrator/scripts/Install-AlaaCodexAgents.ps1'
$taskCodexOutput = & $taskInstaller -TargetDirectory $taskCodex 2>&1
$taskCodexExit = $LASTEXITCODE
$taskCodexOutput | Set-Content -LiteralPath (Join-Path $taskEvidence 'codex-installer.log') -Encoding utf8
if ($taskCodexExit -ne 0) { throw "Codex installer failed with exit $taskCodexExit" }

$taskCcNames = @($taskCcFiles | ForEach-Object Name)
$taskCodexNames = @($taskCodexFiles | ForEach-Object Name) + @('.alaa-codex-orchestrator.version','.alaa-codex-orchestrator.mcp-inventory')
foreach ($name in $taskCcBefore.Keys) {
    if ($name -notin $taskCcNames -and (Hash-File (Join-Path $taskClaude $name)) -ne $taskCcBefore[$name]) { throw 'Unrelated Claude agent changed' }
}
foreach ($name in $taskCodexBefore.Keys) {
    if ($name -notin $taskCodexNames -and (Hash-File (Join-Path $taskCodex $name)) -ne $taskCodexBefore[$name]) { throw 'Unrelated Codex agent changed' }
}
foreach ($path in $taskConfigHashes.Keys) { if ((Hash-File $path) -ne $taskConfigHashes[$path]) { throw 'Unrelated runtime configuration changed' } }
$taskResidue = @(Get-ChildItem -LiteralPath $taskCodex -Force | Where-Object { $_.Name -match '^\.alaa-codex-orchestrator\.(?:materialized\.|install\.lock)' -or $_.Name -match '\.toml\.tmp\.' })
if ($taskResidue.Count) { throw 'Native installer staging residue requires inspection; no broad cleanup permitted' }
$taskInstalled = [Collections.Generic.List[object]]::new()
foreach ($runtime in $taskRuntimes) {
    foreach ($source in $runtime.Files) {
        $taskInstalled.Add([ordered]@{runtime=$runtime.Name; name=$source.Name; source_sha256=(Hash-File $source.FullName); installed_sha256=(Hash-File (Join-Path $runtime.Target $source.Name))})
    }
}
$taskReceipt = [ordered]@{
    status='INSTALLED'; claude_target=$taskClaude; codex_target=$taskCodex;
    claude_managed_count=28; codex_managed_count=27; backup_directory=$taskBackup;
    backed_up_count=$taskBackupRecords.Count; claude_preflight_exit=$taskCcExit; codex_installer_exit=$taskCodexExit;
    unrelated_files_and_config='preserved'; rule_writer_files='preserved as unrelated source-unmanaged names';
    staging='native GUID-child paths contained; no residue'; installed_files=$taskInstalled;
    limits='Claude Code 2.1.289 is below Haiku5.5 minimum2.1.293; definitions installed only. No CLI upgrade, activation, serving-identity or live-model proof.'
}
$taskReceipt | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $taskEvidence 'receipt.json') -Encoding utf8
[ordered]@{Status='INSTALLED'; Claude=28; Codex=27; BackupCount=$taskBackupRecords.Count; Backup=$taskBackup; Evidence=$taskEvidence; ClaudeHaikuActivation='BLOCKED_BY_CURRENT_VERSION'} | ConvertTo-Json -Compress
