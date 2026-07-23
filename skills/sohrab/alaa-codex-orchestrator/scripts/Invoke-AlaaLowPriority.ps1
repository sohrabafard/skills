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

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not $IsWindows) {
    throw "Invoke-AlaaLowPriority.ps1 is intended for native Windows. Use run-low-priority.sh on Unix/WSL."
}
if (-not (Test-Path -LiteralPath $WorkingDirectory -PathType Container)) {
    throw "Working directory does not exist: $WorkingDirectory"
}
if ($CpuCount -gt [Environment]::ProcessorCount) {
    throw "CpuCount $CpuCount exceeds available logical processors $([Environment]::ProcessorCount)."
}

$psi = [System.Diagnostics.ProcessStartInfo]::new()
$psi.FileName = $FilePath
$psi.WorkingDirectory = (Resolve-Path -LiteralPath $WorkingDirectory).Path
$psi.UseShellExecute = $false
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.CreateNoWindow = $true
foreach ($arg in $ArgumentList) { [void]$psi.ArgumentList.Add([string]$arg) }
foreach ($key in $Environment.Keys) { $psi.Environment[[string]$key] = [string]$Environment[$key] }

$process = [System.Diagnostics.Process]::new()
$process.StartInfo = $psi
$startedAt = [DateTimeOffset]::Now

try {
    if (-not $process.Start()) { throw "Failed to start process: $FilePath" }

    try {
        $priorityValue = [System.Enum]::Parse([System.Diagnostics.ProcessPriorityClass], $Priority)
        $process.PriorityClass = $priorityValue
    }
    catch {
        try { $process.Kill($true) } catch { }
        throw "Started process $($process.Id) but could not set priority to $Priority: $($_.Exception.Message)"
    }

    if ($CpuCount -gt 0) {
        [Int64]$mask = 0
        for ($i = 0; $i -lt $CpuCount; $i++) { $mask = $mask -bor ([Int64]1 -shl $i) }
        try { $process.ProcessorAffinity = [IntPtr]$mask }
        catch {
            try { $process.Kill($true) } catch { }
            throw "Started process $($process.Id) but could not set CPU affinity: $($_.Exception.Message)"
        }
    }

    $stdoutTask = $process.StandardOutput.ReadToEndAsync()
    $stderrTask = $process.StandardError.ReadToEndAsync()

    $completed = if ($TimeoutSeconds -gt 0) {
        $process.WaitForExit($TimeoutSeconds * 1000)
    } else {
        $process.WaitForExit()
        $true
    }

    if (-not $completed) {
        try { $process.Kill($true) } catch { & taskkill.exe /PID $process.Id /T /F | Out-Null }
        $process.WaitForExit()
    }

    $stdout = $stdoutTask.GetAwaiter().GetResult()
    $stderr = $stderrTask.GetAwaiter().GetResult()

    if ($StdoutPath) {
        $parent = Split-Path -Parent $StdoutPath
        if ($parent) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
        [System.IO.File]::WriteAllText($StdoutPath, $stdout, [System.Text.UTF8Encoding]::new($false))
    }
    if ($StderrPath) {
        $parent = Split-Path -Parent $StderrPath
        if ($parent) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
        [System.IO.File]::WriteAllText($StderrPath, $stderr, [System.Text.UTF8Encoding]::new($false))
    }

    if ($stdout) { [Console]::Out.Write($stdout) }
    if ($stderr) { [Console]::Error.Write($stderr) }

    $duration = [DateTimeOffset]::Now - $startedAt
    $effectiveExitCode = if ($completed) { $process.ExitCode } else { 124 }
    $summaryArgs = [object[]]@(
        $process.Id,
        $Priority,
        $CpuCount,
        [Math]::Round($duration.TotalMilliseconds),
        (-not $completed),
        $effectiveExitCode
    )
    $summary = [string]::Format(
        [Globalization.CultureInfo]::InvariantCulture,
        "[alaa-low-priority] pid={0} priority={1} cpuCount={2} durationMs={3} timedOut={4} exitCode={5}",
        $summaryArgs
    )
    [Console]::Error.WriteLine($summary)

    exit $effectiveExitCode
}
finally {
    $process.Dispose()
}
