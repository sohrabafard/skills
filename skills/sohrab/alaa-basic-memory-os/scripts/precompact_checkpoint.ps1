[CmdletBinding()]
param(
  [string]$Project = "alaa-memory",
  [string]$AgentMemoryPath = "D:\Sohrab\Project\agent-memory"
)

$ErrorActionPreference = "Stop"

function Redact-Line {
  param([string]$Line)
  $patterns = @(
    '(?i)(api[_-]?key\s*[:=]\s*)\S+',
    '(?i)(token\s*[:=]\s*)\S+',
    '(?i)(password\s*[:=]\s*)\S+',
    '(?i)(secret\s*[:=]\s*)\S+',
    '(?i)(cookie\s*[:=]\s*)\S+',
    'Bearer\s+[A-Za-z0-9._\-]+'
  )
  $out = $Line
  foreach ($p in $patterns) { $out = [regex]::Replace($out, $p, '$1[REDACTED]') }
  return $out
}

try {
  $inputJson = [Console]::In.ReadToEnd()
  $hookEvent = $null
  if ($inputJson.Trim().Length -gt 0) { $hookEvent = $inputJson | ConvertFrom-Json }

  $cwd = $null
  if ($hookEvent) { $cwd = $hookEvent.cwd }
  if (-not $cwd) { $cwd = (Get-Location).Path }
  $repoName = Split-Path $cwd -Leaf
  $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
  $safeTimestamp = Get-Date -Format "yyyyMMdd-HHmmss"
  $branch = "unknown"
  $status = "git status unavailable"

  try {
    Push-Location $cwd
    $gitRoot = git rev-parse --show-toplevel 2>$null
    if ($LASTEXITCODE -eq 0 -and $gitRoot) { $repoName = Split-Path $gitRoot -Leaf }
    $branch = git branch --show-current 2>$null
    $status = git status --short 2>$null | Out-String
    Pop-Location
  } catch {
    try { Pop-Location } catch {}
  }

  $trigger = "unknown"
  $transcriptPath = ""
  if ($hookEvent) {
    if ($hookEvent.trigger) { $trigger = $hookEvent.trigger }
    if ($hookEvent.transcript_path) { $transcriptPath = $hookEvent.transcript_path }
  }

  $includeTail = $env:ALAA_MEMORY_INCLUDE_TRANSCRIPT_TAIL -eq "1"
  $tailBlock = "Transcript tail capture disabled by default to avoid secrets and memory bloat. Set ALAA_MEMORY_INCLUDE_TRANSCRIPT_TAIL=1 only for trusted local debugging."
  if ($includeTail -and $transcriptPath -and (Test-Path -LiteralPath $transcriptPath)) {
    $tailLines = Get-Content -LiteralPath $transcriptPath -Tail 40 -ErrorAction SilentlyContinue | ForEach-Object { Redact-Line $_ }
    $tailBlock = ($tailLines | Out-String)
  }

  $title = "Emergency Checkpoint - $repoName - $safeTimestamp"
  $permalink = "emergency-checkpoint-$repoName-$safeTimestamp".ToLower() -replace '[^a-z0-9\-]+','-'
  $fence = '```'

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

- [summary] PreCompact emergency checkpoint created automatically.
- [boundary] This inbox capture is not canonical memory and must be curated before becoming durable state.
- [source] Repo: $repoName | cwd: $cwd | branch: $branch
- [source] Trigger: $trigger | transcript: $transcriptPath
- [todo] Next agent should create or update a semantic handoff if the task remains active.

## Git status

${fence}text
$status
${fence}

## Transcript tail policy

${fence}text
$tailBlock
${fence}

## Relations

- governed_by [[Alaa Basic Memory Operating Rules]]
"@

  # File-first write into the vault (avoids double frontmatter from bm tool write-note),
  # then let Basic Memory index it.
  $captureDir = Join-Path $AgentMemoryPath "inbox\agent-captures"
  New-Item -ItemType Directory -Force -Path $captureDir | Out-Null
  $captureFile = Join-Path $captureDir "$title.md"
  $content | Set-Content -Encoding UTF8 -LiteralPath $captureFile

  if (Get-Command bm -ErrorAction SilentlyContinue) {
    & bm status --project $Project --wait --timeout 60 | Out-Null
  }

  @{ systemMessage = "Alaa Basic Memory emergency checkpoint created for $repoName."; continue = $true } | ConvertTo-Json -Compress
  exit 0
}
catch {
  @{ systemMessage = "Alaa Basic Memory PreCompact checkpoint failed: $($_.Exception.Message)"; continue = $true } | ConvertTo-Json -Compress
  exit 0
}
