# =============================================================================
# _common.ps1 - shared helpers for the alaa-memory-os checkers and store scripts.
# Dot-source it:  . (Join-Path $PSScriptRoot '_common.ps1')
#
# Exit-code contract for every CHECKER and STORE script here:
#   0  ran to completion, no findings
#   1  ran to completion, findings to report
#   2  could not run (path unresolved, tool absent, input unreadable)
#
# Hook scripts are EXEMPT and must always exit 0. The Claude Code hook protocol
# reserves exit 2 to mean "block" and treats exit 1 as a non-blocking error, so
# applying the contract above to a hook changes its behaviour.
# See references/checkers-and-hooks.md.
# =============================================================================

Set-StrictMode -Version Latest

function Resolve-VaultRoot {
  <#
    Precedence, highest first:
      1. -VaultPath argument
      2. $env:ALAA_MEMORY_VAULT
      3. $DocumentedDefault, but only if it exists on this machine
    Returns an object with Ok, Path and Reason. It never throws and never
    guesses: a machine-specific default that is assumed rather than tested makes
    "could not run" indistinguishable from "wrong machine", which is the exact
    ambiguity the exit-code contract exists to remove.
  #>
  param(
    [string]$VaultPath = "",
    [string]$DocumentedDefault = "D:\Sohrab\Project\agent-memory"
  )

  $candidates = @()
  if (-not [string]::IsNullOrWhiteSpace($VaultPath))            { $candidates += $VaultPath }
  if (-not [string]::IsNullOrWhiteSpace($env:ALAA_MEMORY_VAULT)) { $candidates += $env:ALAA_MEMORY_VAULT }
  if (-not [string]::IsNullOrWhiteSpace($DocumentedDefault))     { $candidates += $DocumentedDefault }

  if ($candidates.Count -eq 0) {
    return [pscustomobject]@{
      Ok = $false; Path = $null
      Reason = "No vault path given. Pass -VaultPath or set ALAA_MEMORY_VAULT."
    }
  }

  foreach ($c in $candidates) {
    $item = Get-Item -LiteralPath $c -ErrorAction SilentlyContinue
    if ($null -ne $item -and $item.PSIsContainer) {
      return [pscustomobject]@{ Ok = $true; Path = $item.FullName; Reason = "" }
    }
  }

  return [pscustomobject]@{
    Ok = $false; Path = $null
    # One string literal, deliberately. Splitting it across a "+" would bind -f
    # to the second fragment only, leaving {0} unexpanded in the first.
    Reason = ("No candidate vault path resolved to a directory. Tried: {0}. Pass -VaultPath or set ALAA_MEMORY_VAULT." -f ($candidates -join '; '))
  }
}

function Invoke-Store {
  <#
    Runs a store command and returns ONLY its exit code, as an int.

    This is the whole reason this module exists. A PowerShell function returns
    its entire output stream, so the shape

        & $exe @args
        $code = $LASTEXITCODE
        return $code

    hands the caller an array of the command's output lines with the exit code
    appended. `$result -ne 0` against that array is a filter, not a comparison:
    it yields the non-matching elements, and a non-empty array is truthy. The
    result is a check that reports failure on every run in which the command
    printed anything at all. Piping to Out-Host keeps the output off the output
    stream so the returned value is a single int.
  #>
  param(
    [Parameter(Mandatory)][string]$Exe,
    [string[]]$StoreArgs = @()
  )
  Write-Host "$Exe $($StoreArgs -join ' ')"
  & $Exe @StoreArgs 2>&1 | Out-Host
  return [int]$LASTEXITCODE
}

function Test-Tool {
  param([Parameter(Mandatory)][string]$Name)
  return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

function Get-RelativeNotePath {
  <# Vault-relative path with forward slashes, so exclusion globs compare the
     same way on Windows and elsewhere. Backslash globs silently match nothing
     off Windows, which widens the checked set instead of failing. #>
  param(
    [Parameter(Mandatory)][string]$FullName,
    [Parameter(Mandatory)][string]$Root
  )
  $rel = $FullName
  if ($FullName.Length -gt $Root.Length -and $FullName.StartsWith($Root)) {
    $rel = $FullName.Substring($Root.Length)
  }
  $rel = $rel -replace '^[\\/]+', ''
  return ($rel -replace '\\', '/')
}

function Get-NoteFrontmatter {
  <# Returns a hashtable of top-level scalar keys plus any simple list values,
     or $null when the file has no frontmatter block. Deliberately small: this
     is not a YAML parser, and anything needing one belongs in the vendored
     store skills, not here. #>
  param([Parameter(Mandatory)][string]$Raw)

  if ($Raw -notmatch '(?s)\A---\r?\n(.*?)\r?\n---') { return $null }
  $block = $Matches[1]
  $out = @{}
  $currentKey = $null
  foreach ($line in ($block -split "\r?\n")) {
    if ($line -match '^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$') {
      $currentKey = $Matches[1]
      $value = $Matches[2].Trim().Trim('"').Trim("'")
      if ($value -eq '') { $out[$currentKey] = @() } else { $out[$currentKey] = $value }
    }
    elseif ($null -ne $currentKey -and $line -match '^\s+-\s*(.+?)\s*$') {
      $item = $Matches[1].Trim().Trim('"').Trim("'")
      if ($out[$currentKey] -isnot [array]) { $out[$currentKey] = @() }
      $out[$currentKey] += $item
    }
  }
  return $out
}

function Write-TextFileNoBom {
  <# Windows PowerShell 5.1 writes a byte-order mark with -Encoding UTF8 and
     PowerShell 7 does not. A mark immediately before the opening --- can break
     the YAML parse on whatever later reads the note, so never rely on the
     host's default. #>
  param(
    [Parameter(Mandatory)][string]$Path,
    [Parameter(Mandatory)][AllowEmptyString()][string]$Text
  )
  $enc = New-Object System.Text.UTF8Encoding($false)
  [System.IO.File]::WriteAllText($Path, $Text, $enc)
}

function Get-HostPowerShellPath {
  <# Path to the PowerShell executable currently running, for a self-test that
     re-invokes its own script as a child process. Re-invoking is deliberate:
     the defect this replaces was in the exit path itself, and only a child
     process observes a real exit code. #>
  $p = (Get-Process -Id $PID).Path
  if (-not [string]::IsNullOrWhiteSpace($p)) { return $p }
  foreach ($n in @('pwsh', 'powershell')) {
    $c = Get-Command $n -ErrorAction SilentlyContinue
    if ($c) { return $c.Source }
  }
  return $null
}

function Get-FixturePath {
  param([Parameter(Mandatory)][string]$Name)
  $p = Join-Path (Join-Path (Split-Path -Parent $PSScriptRoot) 'test') (Join-Path 'fixtures' $Name)
  $resolved = Resolve-Path -LiteralPath $p -ErrorAction SilentlyContinue
  if ($resolved) { return $resolved.Path }
  return $null
}

function Invoke-SelfTest {
  <#
    Runs $ScriptPath as a child process once per case and asserts the observed
    exit code. Asserts on the exit code and never on report text: prose drifts,
    the exit code is the contract, and the defect this replaces was in the exit
    path itself.

    Each case is a hashtable: Name, Args, Expect. Any element of Args of the form
    @fixture:NAME@ is replaced with the resolved path of test/fixtures/NAME, so a
    case can point at a fixture vault or at a stub store without knowing where
    the skill is installed.

    Returns 0 when every case matched, 1 when any case mismatched, 2 when the
    harness itself could not run.
  #>
  param(
    [Parameter(Mandatory)][string]$ScriptPath,
    [Parameter(Mandatory)][hashtable[]]$Cases
  )

  $psExe = Get-HostPowerShellPath
  if (-not $psExe) {
    Write-Host "BLOCKED: cannot locate the PowerShell executable to re-invoke $ScriptPath"
    return 2
  }

  $failed = 0
  foreach ($case in $Cases) {
    $resolvedArgs = @()
    foreach ($a in @($case.Args)) {
      if ("$a" -match '^@fixture:(.+)@$') {
        $fixture = Get-FixturePath -Name $Matches[1]
        if (-not $fixture) {
          Write-Host ("BLOCKED  {0}: fixture '{1}' not found" -f $case.Name, $Matches[1])
          return 2
        }
        $resolvedArgs += $fixture
      } else {
        $resolvedArgs += "$a"
      }
    }

    & $psExe @(@('-NoProfile', '-File', $ScriptPath) + $resolvedArgs) | Out-Null
    $observed = $LASTEXITCODE
    if ($observed -eq $case.Expect) {
      Write-Host ("PASS     {0}: expected {1}, observed {2}" -f $case.Name, $case.Expect, $observed)
    } else {
      Write-Host ("FAIL     {0}: expected {1}, observed {2}" -f $case.Name, $case.Expect, $observed)
      $failed++
    }
  }

  if ($failed -gt 0) { Write-Host "self-test: $failed case(s) failed"; return 1 }
  Write-Host "self-test: all cases passed"
  return 0
}
