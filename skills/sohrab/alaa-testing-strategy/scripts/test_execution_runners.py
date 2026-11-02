#!/usr/bin/env python3
"""Topic: execution runners; layer: subprocess contract smoke.

Run canonical and both compatibility entrypoints from an unrelated, spaced cwd.
Exit 0 passes, 1 assertions fail, 2 the requested native platform is unavailable.
No Linux PowerShell invocation is reported as Windows evidence.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

PACK_ROOT = Path(__file__).resolve().parent.parent
PACKS = ("alaa-testing-strategy", "alaa-codex-orchestrator", "alaa-cc-orchestrator")


def copy_runners(destination: Path, filename: str) -> None:
    for pack in PACKS:
        target = destination / pack / "scripts" / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(PACK_ROOT.parent / pack / "scripts" / filename, target)


def posix_smoke() -> int:
    bash = shutil.which("bash")
    if not bash or os.name == "nt":
        print("UNAVAILABLE: native POSIX bash runner")
        return 2
    # One immutable runner copy per run; child processes have no shared mutation.
    with tempfile.TemporaryDirectory(prefix="alaa runner smoke ") as temporary:
        base = Path(temporary)
        packs = base / "skill packs with spaces"
        copy_runners(packs, "run-low-priority.sh")
        cwd = base / "unrelated working directory"
        cwd.mkdir()
        child = base / "argument probe.py"
        child.write_text(
            "import json, os, sys\n"
            "print(json.dumps({'args':sys.argv[2:],'cwd':os.getcwd(),"
            "'env':os.environ['ALAA_RUNNER_SMOKE']}))\n"
            "print('child stderr marker', file=sys.stderr)\n"
            "sys.exit(int(sys.argv[1]))\n", encoding="utf-8")
        arguments = ["two words", 'a"quote', "literal$()", "", "--flag=value"]
        environment = {**os.environ, "ALAA_RUNNER_SMOKE": "environment value with spaces"}
        for pack in PACKS:
            runner = packs / pack / "scripts/run-low-priority.sh"
            for option in ("-h", "--help"):
                result = subprocess.run([bash, str(runner), option], cwd=cwd,
                                        capture_output=True, text=True, timeout=20, check=False)
                assert result.returncode == 2, (pack, option, result.returncode)
                assert result.stdout == "" and result.stderr == f"Unknown option: {option}\n", (
                    pack, option, result.stdout, result.stderr)
            for exit_code in (0, 17):
                result = subprocess.run(
                    [bash, str(runner), "--priority", "BelowNormal", "--cpu-count", "0",
                     "--", sys.executable, str(child), str(exit_code), *arguments],
                    cwd=cwd, env=environment, capture_output=True, text=True, timeout=20,
                    check=False)
                assert result.returncode == exit_code, (pack, exit_code, result.stderr)
                assert json.loads(result.stdout) == {
                    "args": arguments, "cwd": str(cwd),
                    "env": environment["ALAA_RUNNER_SMOKE"]}, (pack, result.stdout)
                assert result.stderr == "child stderr marker\n", (pack, result.stderr)
    print("PASS: POSIX canonical + both adapters; 12 success/nonzero/help-rejection, argv/cwd/env/stdout/stderr probes")
    return 0


WINDOWS_DRIVER = r'''
param([string]$PackRoot)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if (-not $IsWindows) { throw 'Native Windows is required' }
$hostPath = (Get-Process -Id $PID).Path
$base = Join-Path ([IO.Path]::GetTempPath()) ('alaa runner smoke ' + [guid]::NewGuid())
New-Item -ItemType Directory -Path $base | Out-Null
try {
    $packs = Join-Path $base 'skill packs with spaces'
    $cwd = Join-Path $base 'unrelated working directory'
    New-Item -ItemType Directory -Path $cwd | Out-Null
    foreach ($pack in @('alaa-testing-strategy', 'alaa-codex-orchestrator', 'alaa-cc-orchestrator')) {
        $directory = Join-Path $packs "$pack/scripts"
        New-Item -ItemType Directory -Path $directory -Force | Out-Null
        Copy-Item -LiteralPath (Join-Path $PackRoot "$pack/scripts/Invoke-AlaaLowPriority.ps1") -Destination $directory
    }
    $child = Join-Path $base 'argument probe.ps1'
    @'
param([int]$ExitCode, [string]$First, [string]$Second)
@{ first=$First; second=$Second; cwd=(Get-Location).Path; env=$env:ALAA_RUNNER_SMOKE } | ConvertTo-Json -Compress
[Console]::Error.WriteLine('child stderr marker')
if ($ExitCode -eq 124) { Start-Sleep -Seconds 20 }
exit $ExitCode
'@ | Set-Content -LiteralPath $child
    $invoke = Join-Path $base 'invoke runner.ps1'
    @'
param([string]$Runner, [string]$HostPath, [string]$Child, [string]$Cwd, [string]$OutputBase, [int]$ExitCode)
$parameters = @{
    FilePath=$HostPath
    ArgumentList=@('-NoLogo', '-NoProfile', '-File', $Child, [string]$ExitCode, 'two words', 'a"quote')
    WorkingDirectory=$Cwd
    Environment=@{ALAA_RUNNER_SMOKE='environment value with spaces'}
    Priority='BelowNormal'
    CpuCount=0
    StdoutPath=($OutputBase + '.out')
    StderrPath=($OutputBase + '.err')
    TimeoutSeconds=$(if ($ExitCode -eq 124) { 3 } else { 15 })
}
& $Runner @parameters
exit $LASTEXITCODE
'@ | Set-Content -LiteralPath $invoke
    foreach ($pack in @('alaa-testing-strategy', 'alaa-codex-orchestrator', 'alaa-cc-orchestrator')) {
        foreach ($exitCode in @(0, 17, 124)) {
            $outputBase = Join-Path $base "$pack-$exitCode"
            $psi = [Diagnostics.ProcessStartInfo]::new()
            $psi.FileName = $hostPath
            $psi.UseShellExecute = $false
            $psi.WorkingDirectory = $cwd
            $psi.RedirectStandardOutput = $true
            $psi.RedirectStandardError = $true
            foreach ($argument in @('-NoLogo', '-NoProfile', '-File', $invoke, '-Runner',
                (Join-Path $packs "$pack/scripts/Invoke-AlaaLowPriority.ps1"), '-HostPath', $hostPath,
                '-Child', $child, '-Cwd', $cwd, '-OutputBase', $outputBase, '-ExitCode', [string]$exitCode)) {
                [void]$psi.ArgumentList.Add($argument)
            }
            $process = [Diagnostics.Process]::Start($psi)
            try {
                $stdoutTask = $process.StandardOutput.ReadToEndAsync()
                $stderrTask = $process.StandardError.ReadToEndAsync()
                if (-not $process.WaitForExit(25000)) { $process.Kill($true); throw "$pack smoke timed out" }
                $stdout = $stdoutTask.GetAwaiter().GetResult()
                $stderr = $stderrTask.GetAwaiter().GetResult()
                if ($process.ExitCode -ne $exitCode) { throw "$pack exit $($process.ExitCode) != ${exitCode}: $stderr" }
                $observed = $stdout | ConvertFrom-Json
                if ($observed.first -cne 'two words' -or $observed.second -cne 'a"quote' -or
                    $observed.cwd -cne $cwd -or $observed.env -cne 'environment value with spaces') {
                    throw "$pack lost arguments/cwd/environment: $stdout"
                }
                if ([IO.File]::ReadAllText($outputBase + '.out') -cne $stdout) { throw "$pack stdout file differs" }
                if ([IO.File]::ReadAllText($outputBase + '.err').Trim() -cne 'child stderr marker') { throw "$pack stderr file differs" }
                if ($stderr -notmatch 'child stderr marker' -or $stderr -notmatch "exitCode=$exitCode") { throw "$pack stderr/summary lost: $stderr" }
                if ($exitCode -eq 124 -and $stderr -notmatch 'timedOut=True') { throw "$pack timeout not reported" }
            } finally { $process.Dispose() }
        }
    }
    Write-Output 'PASS: Windows canonical + both adapters; 9 success/nonzero/timeout124, argv/cwd/env/output-file probes'
} finally {
    # Remove only the synthetic native-Windows fixture owned by this invocation.
    Remove-Item -LiteralPath $base -Recurse -Force
}
'''


def windows_path(path: Path) -> str:
    if os.name == "nt":
        return str(path)
    converter = shutil.which("wslpath")
    if not converter:
        raise OSError("wslpath required to pass WSL fixture paths to native Windows")
    return subprocess.check_output([converter, "-w", str(path)], text=True).strip()


def windows_smoke(powershell: str | None) -> int:
    executable = powershell or shutil.which("pwsh.exe") or shutil.which("pwsh")
    if not executable:
        print("UNAVAILABLE: native Windows PowerShell; use --powershell PATH")
        return 2
    probe = subprocess.run([executable, "-NoLogo", "-NoProfile", "-Command",
                            "[Console]::Write($IsWindows)"], capture_output=True,
                           text=True, timeout=20, check=False)
    if probe.returncode or probe.stdout.strip().casefold() != "true":
        print(f"UNAVAILABLE: PowerShell did not prove native Windows: {probe.stderr.strip()}")
        return 2
    with tempfile.TemporaryDirectory(prefix="alaa windows driver ") as temporary:
        driver = Path(temporary) / "runner smoke.ps1"
        driver.write_text(WINDOWS_DRIVER, encoding="utf-8")
        result = subprocess.run([executable, "-NoLogo", "-NoProfile", "-File",
                                 windows_path(driver), "-PackRoot",
                                 windows_path(PACK_ROOT.parent)],
                                cwd=temporary, capture_output=True, text=True,
                                timeout=90, check=False)
        if result.returncode:
            print(result.stderr, file=sys.stderr)
            return 1
        print(result.stdout.strip())
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform", choices=("posix", "windows", "all"),
                        default="windows" if os.name == "nt" else "posix")
    parser.add_argument("--powershell", help="existing native Windows pwsh executable, including a WSL path")
    args = parser.parse_args()
    try:
        results = []
        if args.platform in {"posix", "all"}:
            results.append(posix_smoke())
        if args.platform in {"windows", "all"}:
            results.append(windows_smoke(args.powershell))
        return 1 if 1 in results else 2 if 2 in results else 0
    except AssertionError as exc:
        print(f"RUNNER SMOKE FAILED: {exc}", file=sys.stderr)
        return 1
    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        print(f"RUNNER SMOKE UNAVAILABLE: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
