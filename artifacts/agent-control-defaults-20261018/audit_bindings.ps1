$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$projectRoot = Split-Path -Parent $repoRoot
$artifactRoot = $PSScriptRoot
$templatePath = Join-Path $artifactRoot 'binding-template.md'
$template = [IO.File]::ReadAllText($templatePath, [Text.UTF8Encoding]::new($false, $true)).TrimEnd("`n")
$utf8 = [Text.UTF8Encoding]::new($false, $true)

$repos = @(
    @{ name='skills'; branch='main'; head='4c2a5bd66f18338f128423e2fbaf038a724efb1b'; paths=@('AGENTS.md') },
    @{ name='alaa-task-hub'; branch='main'; head='c04a599a1ec784fcf58e5034433349045e2211af'; paths=@('AGENTS.md') },
    @{ name='octane-base'; branch='main'; head='d4741e989cd959a42c496349cb91c98cdbd0b9eb'; paths=@('AGENTS.md') },
    @{ name='ci-image'; branch='main'; head='728504485339f003d0da2c434e2cc7fed54184e2'; paths=@('AGENTS.md') },
    @{ name='wa'; branch='main'; head='7dbff2ecb846588f30dd1dbd66b00dd47296a59c'; paths=@('AGENTS.md') },
    @{ name='tusd'; branch='main'; head='788de5c560ce6b8713d499f2c995abf295099f3f'; paths=@('AGENTS.md') },
    @{ name='gateway'; branch='main'; head='24c4d7ae5da1947bbe759a585318252ae2d1d447'; paths=@('AGENTS.md') },
    @{ name='alaa-go-chi'; branch='main'; head='81507da77d837d66e430e73d7bff60ae33964542'; paths=@('AGENTS.md','CLAUDE.md') },
    @{ name='authz-sidecar'; branch='main'; head='b6d2a646fea2e0515cffcdf3ead7cd77a97208a4'; paths=@('AGENTS.md','CLAUDE.md') },
    @{ name='entitlement-projector'; branch='main'; head='edde34874c1c7b7fc8d8646226ddeef0eab0593e'; paths=@('AGENTS.md','CLAUDE.md') },
    @{ name='authz-openfga'; branch='main'; head='31072f313825d6e1347b79a1e537781f8365c32c'; paths=@('AGENTS.md','CLAUDE.md') },
    @{ name='auth'; branch='main'; head='fbe6d8a6dbf6aa743a95a6a574b16218ad3acdbd'; paths=@('AGENTS.md','CLAUDE.md') },
    @{ name='deploy'; branch='main'; head='f6eee3c0863494901284dca9d261306aafc579ca'; paths=@('AGENTS.md') },
    @{ name='client'; branch='feat/sentry_setup'; head='0a041e9546088f4381a74899ba20d1e6c6476c7c'; paths=@('AGENTS.md') },
    @{ name='content'; branch='main'; head='1611503718bdcc3827ffc7f14eb0aed8fa3ce96f'; paths=@('AGENTS.md','CLAUDE.md') },
    @{ name='entitlement-api'; branch='main'; head='d18f97799420492df3e5907864be65dad46e60f5'; paths=@('AGENTS.md','CLAUDE.md') },
    @{ name='comment-service'; branch='main'; head='5880cfdbb88fd3aa793675b93ecd5857872eea5b'; paths=@('AGENTS.md','CLAUDE.md') }
)
$symlinkRepos = @('alaa-task-hub','ci-image','wa','tusd','gateway','deploy','client')
$unchangedImports = @('skills','octane-base')
$findings = [Collections.Generic.List[string]]::new()
$records = [Collections.Generic.List[object]]::new()
$allGateResults = [Collections.Generic.List[object]]::new()

function Invoke-Git([string]$cwd, [string[]]$arguments, [switch]$raw) {
    $info = [Diagnostics.ProcessStartInfo]::new('git')
    $info.WorkingDirectory = $cwd
    $info.UseShellExecute = $false
    $info.RedirectStandardOutput = $true
    $info.RedirectStandardError = $true
    foreach ($arg in $arguments) { [void]$info.ArgumentList.Add($arg) }
    $proc = [Diagnostics.Process]::new()
    $proc.StartInfo = $info
    [void]$proc.Start()
    if ($raw) {
        $memory = [IO.MemoryStream]::new()
        $proc.StandardOutput.BaseStream.CopyTo($memory)
        $stderr = $proc.StandardError.ReadToEnd()
        $proc.WaitForExit()
        $bytes = $memory.ToArray()
        $memory.Dispose()
        return [pscustomobject]@{ ExitCode=$proc.ExitCode; Bytes=$bytes; Output=$stderr }
    }
    $stdout = $proc.StandardOutput.ReadToEnd()
    $stderr = $proc.StandardError.ReadToEnd()
    $proc.WaitForExit()
    return [pscustomobject]@{ ExitCode=$proc.ExitCode; Output=($stdout + $stderr).TrimEnd() }
}

function Get-Sha256([byte[]]$bytes) {
    return [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($bytes)).ToLowerInvariant()
}

function Test-ByteEqual([byte[]]$left, [byte[]]$right) {
    if ($left.Length -ne $right.Length) { return $false }
    for ($i = 0; $i -lt $left.Length; $i++) { if ($left[$i] -ne $right[$i]) { return $false } }
    return $true
}

function Get-IndexEntry([string]$cwd, [string]$path) {
    $r = Invoke-Git $cwd @('ls-files','-s','--',$path)
    if ($r.ExitCode -ne 0 -or -not $r.Output) { return $null }
    $parts = $r.Output -split "`t", 2
    $meta = $parts[0] -split ' '
    return [pscustomobject]@{ mode=$meta[0]; oid=$meta[1]; stage=$meta[2] }
}

foreach ($repo in $repos) {
    $cwd = Join-Path $projectRoot $repo.name
    if (-not (Test-Path -LiteralPath $cwd -PathType Container)) { $findings.Add("$($repo.name): checkout missing at $cwd"); continue }
    $branchResult = Invoke-Git $cwd @('branch','--show-current')
    $headResult = Invoke-Git $cwd @('rev-parse','HEAD')
    $branch = $branchResult.Output
    $head = $headResult.Output
    if ($branch -ne $repo.branch) { $findings.Add("$($repo.name): branch expected $($repo.branch), observed $branch") }
    if ($head -ne $repo.head) { $findings.Add("$($repo.name): HEAD expected $($repo.head), observed $head") }

    $files = [Collections.Generic.List[object]]::new()
    $expectedPhysical = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
    foreach ($path in $repo.paths) { [void]$expectedPhysical.Add($path) }
    foreach ($path in $repo.paths) {
        $filePath = Join-Path $cwd $path
        if (-not (Test-Path -LiteralPath $filePath -PathType Leaf)) { $findings.Add("$($repo.name)/$path: physical file missing"); continue }
        $current = [IO.File]::ReadAllBytes($filePath)
        $headBytesResult = Invoke-Git $cwd @('show',"$($repo.head):$path") -raw
        if ($headBytesResult.ExitCode -ne 0) { $findings.Add("$($repo.name)/$path: cannot read baseline blob: $($headBytesResult.Output)"); continue }
        $baseline = [byte[]]$headBytesResult.Bytes
        $currentText = $utf8.GetString($current)
        $baselineText = $utf8.GetString($baseline)
        $startMarker = '<!-- BEGIN ALAA BEADS BINDING -->'
        $endMarker = '<!-- END ALAA BEADS BINDING -->'
        $start = $currentText.IndexOf($startMarker, [StringComparison]::Ordinal)
        $end = $currentText.IndexOf($endMarker, [StringComparison]::Ordinal)
        $baseStart = $baselineText.IndexOf($startMarker, [StringComparison]::Ordinal)
        $baseEnd = $baselineText.IndexOf($endMarker, [StringComparison]::Ordinal)
        if ($start -lt 0 -or $end -lt $start -or $baseStart -lt 0 -or $baseEnd -lt $baseStart) {
            $findings.Add("$($repo.name)/$path: marker missing or malformed"); continue
        }
        if (($currentText.IndexOf($startMarker, $start + 1, [StringComparison]::Ordinal)) -ge 0 -or
            ($currentText.IndexOf($endMarker, $end + 1, [StringComparison]::Ordinal)) -ge 0) {
            $findings.Add("$($repo.name)/$path: duplicate binding markers"); continue
        }
        $endAfter = $end + $endMarker.Length
        $baseEndAfter = $baseEnd + $endMarker.Length
        $block = $currentText.Substring($start, $endAfter - $start)
        $expectedBlock = $template.Replace('__PROJECT__', $repo.name)
        $blockMatch = $block -ceq $expectedBlock
        if (-not $blockMatch) { $findings.Add("$($repo.name)/$path: block differs from substituted template") }
        if ([Text.Encoding]::UTF8.GetString($current).StartsWith([char]0xFEFF)) { $findings.Add("$($repo.name)/$path: BOM present") }
        if ($block.Contains("`r")) { $findings.Add("$($repo.name)/$path: CR found inside binding block") }
        $preCurrent = [byte[]]$current[0..($start - 1)]
        $preBaseline = [byte[]]$baseline[0..($baseStart - 1)]
        $postCurrent = [byte[]]$current[$endAfter..($current.Length - 1)]
        $postBaseline = [byte[]]$baseline[$baseEndAfter..($baseline.Length - 1)]
        $outsideMatch = (Test-ByteEqual $preCurrent $preBaseline) -and (Test-ByteEqual $postCurrent $postBaseline)
        if (-not $outsideMatch) { $findings.Add("$($repo.name)/$path: bytes outside binding differ from baseline") }
        $index = Get-IndexEntry $cwd $path
        $statusLines = Invoke-Git $cwd @('status','--porcelain=v1','--',$path)
        $fileSha = Get-Sha256 $current
        $blockSha = Get-Sha256 ([Text.Encoding]::UTF8.GetBytes($block))
        $files.Add([pscustomobject]@{
            path=$path; mode=(if ($index) { $index.mode } else { '' }); index_oid=(if ($index) { $index.oid } else { '' });
            status=$statusLines.Output; sha256=$fileSha; block_sha256=$blockSha; block_matches_template=$blockMatch; outside_bytes_match_head=$outsideMatch
        })
    }

    $claudePath = Join-Path $cwd 'CLAUDE.md'
    $claudeIndex = Get-IndexEntry $cwd 'CLAUDE.md'
    $claudeMode = if ($claudeIndex) { $claudeIndex.mode } else { '' }
    $linkInfo = $null
    if ($symlinkRepos -contains $repo.name) {
        $item = Get-Item -LiteralPath $claudePath -Force
        $linkInfo = [pscustomobject]@{ mode=$claudeMode; link_type=$item.LinkType; target=($item.Target -join ',') }
        if ($claudeMode -ne '120000' -or $item.LinkType -ne 'SymbolicLink' -or ($item.Target -join ',') -ne 'AGENTS.md') {
            $findings.Add("$($repo.name)/CLAUDE.md: expected preserved symlink to AGENTS.md")
        }
    }
    if ($unchangedImports -contains $repo.name) {
        $currentImport = [IO.File]::ReadAllBytes($claudePath)
        $headImport = (Invoke-Git $cwd @('show',"$($repo.head):CLAUDE.md") -raw).Bytes
        if (-not (Test-ByteEqual $currentImport $headImport)) { $findings.Add("$($repo.name)/CLAUDE.md: unchanged import differs from HEAD") }
        $linkInfo = [pscustomobject]@{ mode=$claudeMode; link_type='File'; target='unchanged import'; sha256=(Get-Sha256 $currentImport) }
    }

    $statusResult = Invoke-Git $cwd @('status','--porcelain=v1','--untracked-files=all')
    $statusItems = @()
    foreach ($line in ($statusResult.Output -split "`r?`n")) {
        if (-not $line) { continue }
        $state = $line.Substring(0,2)
        $path = $line.Substring(3)
        $index = Get-IndexEntry $cwd $path
        $itemPath = Join-Path $cwd $path
        $sha = ''
        if (Test-Path -LiteralPath $itemPath -PathType Leaf) { $sha = Get-Sha256 ([IO.File]::ReadAllBytes($itemPath)) }
        $statusItems += [pscustomobject]@{ status=$state; path=$path; index_mode=(if ($index) { $index.mode } else { '' }); index_oid=(if ($index) { $index.oid } else { '' }); worktree_sha256=$sha }
    }
    $diffCheckStart = [DateTime]::UtcNow
    $timer = [Diagnostics.Stopwatch]::StartNew()
    $diffCheck = Invoke-Git $cwd @('diff','--check','--','AGENTS.md','CLAUDE.md')
    $timer.Stop()
    $gate = [pscustomobject]@{ command='git diff --check -- AGENTS.md CLAUDE.md'; cwd=$cwd; started_utc=$diffCheckStart.ToString('o'); duration_seconds=[Math]::Round($timer.Elapsed.TotalSeconds,3); exit_code=$diffCheck.ExitCode; output=$diffCheck.Output }
    $allGateResults.Add($gate)
    if ($diffCheck.ExitCode -ne 0) { $findings.Add("$($repo.name): scoped git diff --check exit $($diffCheck.ExitCode): $($diffCheck.Output)") }

    $changedNames = @($statusItems | ForEach-Object { $_.path })
    foreach ($p in $repo.paths) {
        if ($changedNames -notcontains $p) { $findings.Add("$($repo.name)/$p: expected physical binding path absent from worktree status") }
    }
    $allowedUnrelated = @()
    if ($repo.name -eq 'deploy') {
        $allowedUnrelated = @('docs/delivery-topology.md','docs/design/0001-central-multi-target-delivery.md','docs/agents/20261018-190000-deploy-central-multitarget-state.md','docs/_agent_plans/20261018-190000-deploy-central-multitarget.md')
    }
    if ($repo.name -notin @('skills','deploy')) {
        $unexpected = @($changedNames | Where-Object { $_ -notin $repo.paths })
        if ($unexpected.Count) { $findings.Add("$($repo.name): unexpected changed paths: $($unexpected -join ', ')") }
    }

    $records.Add([pscustomobject]@{
        name=$repo.name; branch=$branch; base_head=$head; expected_base_head=$repo.head;
        files=@($files); claude_binding_import=$linkInfo; worktree_status=$statusItems;
        unrelated_preserved=@($statusItems | Where-Object { $_.path -notin $repo.paths });
        scoped_diff_check=$gate
    })
    Write-Output ("{0}: HEAD/branch {1}; files {2}; diff-check {3} ({4}s)" -f $repo.name,$head,$files.Count,$diffCheck.ExitCode,$gate.duration_seconds)
}

$physical = @($records | ForEach-Object { $_.files }).Count
$symlinks = $symlinkRepos.Count
$logical = $physical + $symlinks
$bindingTemplateSha = Get-Sha256 ([Text.Encoding]::UTF8.GetBytes($template))
$manifest = [pscustomobject]@{
    schema_version=1; generated_utc=[DateTime]::UtcNow.ToString('o'); source_template_sha256=$bindingTemplateSha;
    counts=[pscustomobject]@{ repositories=$records.Count; physical_changed_binding_files=$physical; logical_binding_paths=$logical; preserved_symlinks=$symlinks; unchanged_imports=$unchangedImports.Count };
    repositories=@($records); findings=@($findings)
}
$json = $manifest | ConvertTo-Json -Depth 12
[IO.File]::WriteAllText((Join-Path $artifactRoot 'verification-bindings.json'), $json + "`n", [Text.UTF8Encoding]::new($false))
if ($findings.Count) {
    Write-Output "BINDING AUDIT FINDINGS: $($findings.Count)"
    $findings | ForEach-Object { Write-Output "- $_" }
    exit 1
}
if ($records.Count -ne 17 -or $physical -ne 25 -or $logical -ne 32) {
    Write-Output "BINDING AUDIT COUNT MISMATCH: repos=$($records.Count), physical=$physical, logical=$logical"
    exit 1
}
Write-Output "BINDING AUDIT PASS: $($records.Count) repositories, $physical physical files, $logical logical paths, $symlinks symlinks, $($unchangedImports.Count) unchanged imports"
