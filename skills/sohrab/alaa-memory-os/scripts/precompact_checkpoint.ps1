[CmdletBinding()]
param(
  [string]$VaultPath = ""
)

# =============================================================================
# precompact_checkpoint.ps1 - Claude Code PreCompact hook.
#
# EXEMPT from the 0/1/2 checker contract. The hook protocol reserves exit 2 to
# mean "block" and treats exit 1 as a non-blocking error, so this script always
# exits 0, including from its error handler. Converting it to the checker
# contract would make a failed checkpoint block compaction.
# See references/checkers-and-hooks.md.
#
# It writes an inbox capture, which is NOT canonical memory. A capture must be
# curated before any of it becomes durable knowledge; that is why it is written
# with status needs_review and confidence low.
#
# Known limitation, stated rather than hidden: a silently failed checkpoint is
# indistinguishable from a successful one, because the hook cannot report failure
# without blocking. The systemMessage is the only signal.
# =============================================================================

. (Join-Path $PSScriptRoot '_common.ps1')

# _common.ps1 enables StrictMode for the checkers. Turn it off here: this hook
# reads fields from an upstream JSON payload whose schema is not guaranteed, and
# under StrictMode a missing property throws instead of yielding null. A hook
# should degrade, not throw.
Set-StrictMode -Off
$ErrorActionPreference = "Continue"

function ConvertTo-RedactedText {
  # Approved verb, unlike the previous Redact-Line. Applied to every field that
  # reaches the note, not only the transcript tail: a branch name or a git status
  # line can carry a token just as easily.
  param([string]$Text)
  if ([string]::IsNullOrEmpty($Text)) { return $Text }
  $patterns = @(
    '(?i)(api[_-]?key\s*[:=]\s*)\S+',
    '(?i)(token\s*[:=]\s*)\S+',
    '(?i)(password\s*[:=]\s*)\S+',
    '(?i)(secret\s*[:=]\s*)\S+',
    '(?i)(cookie\s*[:=]\s*)\S+',
    'Bearer\s+[A-Za-z0-9._\-]+'
  )
  $out = $Text
  foreach ($p in $patterns) { $out = [regex]::Replace($out, $p, '$1[REDACTED]') }
  return $out
}

function Get-JsonField {
  # Safe read of an optional field from a payload whose schema may change.
  param($Payload, [string]$Name)
  if ($null -eq $Payload) { return $null }
  $prop = $Payload.PSObject.Properties[$Name]
  if ($null -eq $prop) { return $null }
  return $prop.Value
}

try {
  $inputJson = [Console]::In.ReadToEnd()
  $hookEvent = $null
  if (-not [string]::IsNullOrWhiteSpace($inputJson)) { $hookEvent = $inputJson | ConvertFrom-Json }

  $cwd = Get-JsonField -Payload $hookEvent -Name 'cwd'
  if ([string]::IsNullOrWhiteSpace($cwd)) { $cwd = (Get-Location).Path }

  $repoName  = Split-Path $cwd -Leaf
  $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
  $stamp     = Get-Date -Format "yyyyMMdd-HHmmss"
  # Two compactions inside the same second produced the same filename and one
  # silently overwrote the other. The suffix removes the collision.
  $suffix    = [guid]::NewGuid().ToString('N').Substring(0, 6)
  $branch    = "unknown"
  $status    = "git status unavailable"

  try {
    Push-Location -LiteralPath $cwd
    $gitRoot = & git rev-parse --show-toplevel 2>$null
    if ($LASTEXITCODE -eq 0 -and $gitRoot) { $repoName = Split-Path $gitRoot -Leaf }
    $branch = & git branch --show-current 2>$null
    $status = (& git status --short 2>$null | Out-String)
  } finally {
    Pop-Location -ErrorAction SilentlyContinue
  }

  $branch = ConvertTo-RedactedText -Text ([string]$branch)
  $status = ConvertTo-RedactedText -Text ([string]$status)
  if ([string]::IsNullOrWhiteSpace($branch)) { $branch = "unknown" }

  # 'trigger' is not confirmed in the current PreCompact payload schema, so its
  # absence is tolerated rather than assumed. PreCompact matchers filter on
  # manual versus auto, so a payload field for it is plausible but unverified.
  $trigger = Get-JsonField -Payload $hookEvent -Name 'trigger'
  if ([string]::IsNullOrWhiteSpace($trigger)) { $trigger = "unknown" }
  $transcriptPath = [string](Get-JsonField -Payload $hookEvent -Name 'transcript_path')

  $includeTail = $env:ALAA_MEMORY_INCLUDE_TRANSCRIPT_TAIL -eq "1"
  $tailBlock = "Transcript tail capture is off by default, to keep secrets and bulk out of memory. Set ALAA_MEMORY_INCLUDE_TRANSCRIPT_TAIL=1 only for trusted local debugging."
  if ($includeTail -and -not [string]::IsNullOrWhiteSpace($transcriptPath) -and (Test-Path -LiteralPath $transcriptPath)) {
    $tail = Get-Content -LiteralPath $transcriptPath -Tail 40 -ErrorAction SilentlyContinue | Out-String
    $tailBlock = ConvertTo-RedactedText -Text $tail
  }

  $vault = Resolve-VaultRoot -VaultPath $VaultPath
  if (-not $vault.Ok) {
    @{ systemMessage = "Alaa memory checkpoint skipped: $($vault.Reason)"; continue = $true } | ConvertTo-Json -Compress
    exit 0
  }

  $title     = "Emergency Checkpoint - $repoName - $stamp-$suffix"
  $permalink = ($title.ToLower() -replace '[^a-z0-9\-]+', '-')
  $fence     = '```'

  $content = @"
---
title: $title
type: inbox_capture
status: needs_review
confidence: low
project: $repoName
permalink: $permalink
tags:
  - alaa
  - emergency-checkpoint
  - compact
created_at: "$timestamp"
canonical_source_paths: []
---

# $title

## Observations

- [summary] PreCompact checkpoint written automatically before context compaction.
- [boundary] This is an inbox capture, not canonical memory. Curate it before any of it becomes durable.
- [source] Repo: $repoName | cwd: $cwd | branch: $branch
- [source] Trigger: $trigger | transcript: $transcriptPath
- [todo] If the task is still active, write or update a handoff pointer; /alaa-workflow (`$alaa-workflow`) owns what the handoff contains.

## Git status

${fence}text
$status
${fence}

## Transcript tail policy

${fence}text
$tailBlock
${fence}

## Relations

- governed_by [[Alaa Memory Operating Rules]]
"@

  # Write the file directly, then let the store index it on its own. Going
  # through the store's note-writing tool produced doubled frontmatter.
  $captureDir = Join-Path (Join-Path $vault.Path "inbox") "agent-captures"
  New-Item -ItemType Directory -Force -Path $captureDir | Out-Null
  $captureFile = Join-Path $captureDir "$title.md"

  # Mark-less UTF-8: Windows PowerShell 5.1 would otherwise put a byte-order mark
  # immediately before the opening ---, which can break the YAML parse.
  Write-TextFileNoBom -Path $captureFile -Text $content

  # No store call here. The only reason to invoke one was `status --wait` to force
  # indexing, and that flag is a documented no-op on the current development
  # branch, so it would add latency to a blocking hook and assert nothing.

  @{ systemMessage = "Alaa memory checkpoint written for $repoName."; continue = $true } | ConvertTo-Json -Compress
  exit 0
}
catch {
  @{ systemMessage = "Alaa memory PreCompact checkpoint failed: $($_.Exception.Message)"; continue = $true } | ConvertTo-Json -Compress
  exit 0
}
